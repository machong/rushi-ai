"""从已固定的本机讲解缓存机械选段；不生成释义、不批准、不覆盖审核包。"""
import argparse
import hashlib
import json
from pathlib import Path

from rushi.corpus.diamond import article_lines

ROOT = Path(__file__).resolve().parents[1]
# 一基行号，针对 article_lines 的输出；变更缓存或解析器时必须重新核对。
SELECTIONS = (
    ('01', '依据星云大师本分讲解，“不住相、无所住”是否意味着什么善事都不做？', 9, 9),
    ('02', '星云大师在本分列出布施时应做到的哪四点？', 23, 27),
    ('03', '星云大师在本分如何说明福德与智慧不可偏废？', 50, 50),
    ('04', '星云大师在本分结尾列出的四点安心之道是什么？', 65, 69),
)


def prepare(output):
    if output.exists():
        raise ValueError('审核包已存在，禁止覆盖；请使用新目录并保留旧审核记录')
    manifest = json.loads((ROOT / 'data/sources/diamond-full/manifest.json').read_text())
    chapter = next(c for c in manifest['chapters'] if c['number'] == 4)
    page = chapter['pages']['commentary']
    raw = (ROOT / page['cache_file']).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != page['sha256']:
        raise ValueError('讲解缓存哈希与来源清单不一致，停止选段')
    lines = article_lines(raw.decode('utf-8'))
    worksheet = next(json.loads(s) for s in
                     (ROOT / 'data/candidates/diamond-full/review-worksheets.jsonl').read_text().splitlines()
                     if json.loads(s)['id'] == 'diamond-full-04')
    records = []
    for suffix, question, start, end in SELECTIONS:
        excerpt = '\n'.join(lines[start - 1:end])
        if not excerpt or end > len(lines):
            raise ValueError('选段为空或超出正文范围')
        record = dict(worksheet)
        record.update(
            id=f'diamond-review-pilot-{suffix}', question=question,
            question_status='machine_selected_pending_human_review',
            reference_answer=excerpt, commentary_excerpt=excerpt,
            answer_basis='teacher_commentary',
            commentary_locator=f"{worksheet['commentary_locator']}；本次缓存正文非空行 {start}–{end}（非纸本页码）",
            attribution_level='星云大师讲解原话摘录（待人工核对），不是佛经原句',
            review_status='pending', license_status='pending', split=None,
            reviewer=None, reviewed_at=None,
            review_notes='AI机械选段，未作经义批准。答案与摘录相同，保留原字、标点；仅以换行连接连续正文行。待核对上下文、问题对应、归属及许可。split暂空，不可直接导出。',
            editing_actions=['按连续正文行截取', '保留繁体与标点', '以换行连接；无释义、删词或重排'],
            excerpt_sha256=hashlib.sha256(excerpt.encode('utf-8')).hexdigest(),
            commentary_cache_sha256=digest,
            selection_lines={'start': start, 'end': end, 'numbering': 'article_lines output, 1-based'},
            context_before=lines[max(0, start - 2):start - 1],
            context_after=lines[end:end + 1],
            checks=dict(teacher_text_selected=True, meaning_reviewed_by_human=False,
                        sutra_version_differences_reviewed=False, training_permission_confirmed=False))
        records.append(record)
    output.mkdir(parents=True, exist_ok=False)
    (output / 'candidates.jsonl').write_text(
        ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records), encoding='utf-8')
    review = ['# 第四分首批问答人工审核包', '',
              '4条待审；0条批准；许可待确认；未划分集合、未导出、未训练。', '',
              '以下答案是老师原话摘录，不是AI释义，也不是独立测试题。', '',
              f"来源：{page['url']}；缓存 SHA-256：`{digest}`。", '',
              '每题核对：问题与摘录是否对应、上下文是否完整、是否混淆讲解与经文、编辑是否准确。',
              '内容批准与训练使用许可分别记录真实依据、审核人和日期；不能因网页公开而将许可改为通过。', '',
              '同一来源组 T0235-chapter-04 不得跨集合。审核完成后另建 reviewed 记录，保留本包原始状态。', '']
    for r in records:
        review += [f"## {r['id']}", '', r['question'], '', r['commentary_locator'], '',
                   '### 原话候选答案', '', *['> ' + s for s in r['reference_answer'].splitlines()], '',
                   '### 相邻上下文（仅供核对，不属于候选答案）', '',
                   *['> ' + s for s in r['context_before'] + r['context_after']], '',
                   '- 内容结论：待审', '- 审核人 / 日期：待填', '- 编辑或退回理由：待填',
                   '- 训练许可依据：待确认', '']
    (output / 'review.md').write_text('\n'.join(review) + '\n', encoding='utf-8')
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'data/candidates/diamond-review-pilot-v001')
    args = parser.parse_args()
    records = prepare(args.output)
    print(f'已生成 {len(records)} 条待审候选：{args.output}；未经批准，不可训练')


if __name__ == '__main__':
    main()
