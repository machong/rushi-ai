"""准备全经32分来源对应表与待审核工作单，不自动解经或导出训练数据。"""
import hashlib
import json
from pathlib import Path

from rushi.corpus.diamond import article_lines, original_section, cbeta_main, align_chapters

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/candidates/diamond-full'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    manifest = json.loads((ROOT / 'data/sources/diamond-full/manifest.json').read_text())
    original_xml = ROOT / 'data/raw/diamond-pilot/T08n0235.xml'
    cbeta, lines = cbeta_main(original_xml)
    originals, cache = [], []
    for chapter in manifest['chapters']:
        pages = {}
        for kind, page in chapter['pages'].items():
            path = ROOT / page['cache_file']
            if hashlib.sha256(path.read_bytes()).hexdigest() != page['sha256']:
                raise ValueError(f'缓存哈希不匹配：{path}')
            pages[kind] = article_lines(path.read_text(encoding='utf-8'))
        title, original = original_section(pages['original_notes'])
        originals.append(original)
        cache.append((title, pages))
    aligned, similarity = align_chapters(cbeta, originals)
    OUT.mkdir(parents=True, exist_ok=True)
    pairs, worksheets = [], []
    for chapter, matched, (traditional_title, pages) in zip(manifest['chapters'], aligned, cache):
        number = chapter['number']
        group = f'T0235-chapter-{number:02d}'
        locator = f"T08, no. 235, 卷一, {lines[matched['cbeta_start']]}–{lines[matched['cbeta_end'] - 1]}"
        # 保存的是引用指针；不将整部受版权保护的讲解复制到可分发的问答包中。
        pair = dict(matched, traditional_chapter_label=traditional_title,
                    commentary_chapter_label=chapter['official_chapter_label'],
                    source_group=group, cbeta_locator=locator, teacher='星云大师',
                    teacher_work=chapter['book'], pages=chapter['pages'],
                    commentary_nonempty=bool(pages['commentary']),
                    translation_nonempty=bool(pages['translation']),
                    commentary_line_count=len(pages['commentary']),
                    annotation_line_count=len(pages['original_notes']),
                    review_status='pending', license_status='pending')
        pairs.append(pair)
        worksheet = dict(id=f'diamond-full-{number:02d}', source_group=group,
                         question=f"请依据星云大师《金刚经讲话》第{number}分的实际讲解说明本分内容，并区分经文与讲解。",
                         question_status='draft_for_human_refinement',
                         reference_answer=None, answer_basis='pending_teacher_commentary',
                         teacher='星云大师', source_type='commentary',
                         source_url='https://cbetaonline.dila.edu.tw/zh/T0235', source_locator=locator,
                         commentary_source_url=chapter['pages']['commentary']['url'],
                         commentary_locator=f"{chapter['book']}／{chapter['official_chapter_label']}／{chapter['pages']['commentary']['label']}",
                         commentary_excerpt=None,
                         commentary_cache_file=chapter['pages']['commentary']['cache_file'],
                         attribution_level='待依据老师原讲解人工选段，不由AI自拟释义',
                         license_status='pending', review_status='pending', split=None,
                         review_notes='工作单不是训练样本。待授权确认后由人工选择讲解段落、细化问题、核对删节，再批准与划分。',
                         checks={'teacher_text_selected': False, 'meaning_reviewed_by_human': False,
                                 'sutra_version_differences_reviewed': False, 'training_permission_confirmed': False})
        worksheets.append(worksheet)
    save(OUT / 'chapter-pairs.json', pairs)
    worksheet_file = OUT / 'review-worksheets.jsonl'
    # 人工工作单不得被后续机械提取覆盖。
    if worksheet_file.exists():
        existing = {row['id']: row for row in (json.loads(line) for line in worksheet_file.read_text().splitlines() if line.strip())}
        if set(existing) != {row['id'] for row in worksheets}:
            raise ValueError('工作单ID不匹配，禁止覆盖人工记录')
        for row in worksheets:
            preserved = existing[row['id']]
            # 仅刷新机械定位字段，保留人工选段、审核与问题修改。
            for key in ('source_locator', 'commentary_locator', 'commentary_source_url', 'commentary_cache_file'):
                preserved[key] = row[key]
        worksheets = [existing[row['id']] for row in worksheets]
    worksheet_file.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in worksheets), encoding='utf-8')
    save(ROOT / 'data/raw/diamond-full/cbeta-main.json', {
        'title': '金剛般若波羅蜜經', 'translator': '鳩摩羅什', 'text': cbeta,
        'start_locator': lines[0], 'end_locator': lines[-1],
        'raw_xml_file': str(original_xml.relative_to(ROOT)),
        'raw_xml_sha256': hashlib.sha256(original_xml.read_bytes()).hexdigest(),
        'note': '正文与原XML标题、译者题记、卷尾题记及附文真言分开；原XML完整保留。'})
    summary = dict(chapters=len(pairs), official_pages=96, cbeta_main_characters=len(cbeta),
                   cbeta_characters_covered=sum(len(p['cbeta_text']) for p in pairs),
                   normalized_similarity=similarity,
                   chapters_with_edition_differences=[p['number'] for p in pairs if p['differences_ignoring_punctuation']],
                   commentary_coverage=sum(p['commentary_nonempty'] for p in pairs),
                   candidate_worksheets=len(worksheets), approved_training_samples=0,
                   approved_validation_samples=0, approved_test_samples=0,
                   status='source_preparation_complete_human_review_and_permission_pending')
    save(OUT / 'summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
