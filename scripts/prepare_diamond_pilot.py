"""从固定 CBETA XML 提取单段经文并生成待审核候选；不导出训练集。"""
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/diamond-pilot/T08n0235.xml'
SOURCE = ROOT / 'data/sources/diamond-pilot'
TEI = {'t': 'http://www.tei-c.org/ns/1.0'}
GROUP = 'T0235-wuzhu-bushi-0749a12-20'
URL = 'https://cbetaonline.dila.edu.tw/zh/T0235'
LOCATOR = 'T08, no. 235, p. 749a12–16；上下文至 a20'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    tree = ET.parse(RAW)
    passage = tree.find('.//t:p[@xml:id="pT08p0749a1201"]',
                        {**TEI, 'xml': 'http://www.w3.org/XML/1998/namespace'})
    if passage is None:
        raise ValueError('固定版本中未找到目标段落')
    # 本段没有夹注或校勘读法；遇到复杂标记则拒绝直接拼接。
    if any(child.tag.rsplit('}', 1)[-1] not in ('lb', 'anchor') for child in passage):
        raise ValueError('段落包含需专门处理的标记，请人工复核提取逻辑')
    text = ''.join(passage.itertext()).replace('\n', '').strip()
    if '應無所住行於布施' not in text or not text.endswith('量。'):
        raise ValueError('提取的段落边界与预期不符')
    revision = json.loads((SOURCE / 'repository-commit.json').read_text())['sha']
    excerpt = dict(source_id='cbeta-T0235-pilot', title='金剛般若波羅蜜經', translator='鳩摩羅什', source_url=URL, source_locator=LOCATOR,
                   text=text, script='scripts/prepare_diamond_pilot.py',
                   transformation='仅去除 XML 标签和换行；保留原字与标点；不做简繁转换。')
    save(ROOT / 'data/raw/diamond-pilot/excerpt.json', excerpt)
    license_file = SOURCE / 'cbeta-copyright.html'
    save(SOURCE / 'source.json', {
        'source_id': 'cbeta-T0235-pilot', 'source_type': 'sutra',
        'title': '金剛般若波羅蜜經', 'creator': '鳩摩羅什譯；CBETA 電子版',
        'source_url': URL, 'locator': LOCATOR, 'tradition': '汉译大乘般若经典',
        'version': {'format': 'CBETA XML TEI P5', 'xml_publication_date': '2026-02-09 17:45:18 +0800',
                    'repository': 'https://github.com/cbeta-org/xml-p5', 'revision': revision,
                    'raw_url': f'https://raw.githubusercontent.com/cbeta-org/xml-p5/{revision}/T/T08/T08n0235.xml'},
        'license_status': 'pending',
        'license_evidence': {'url': 'https://cbeta.org/copyright',
                             'local_snapshot': str(license_file.relative_to(ROOT)),
                             'snapshot_sha256': hashlib.sha256(license_file.read_bytes()).hexdigest(),
                             'observed_terms': '网站声明以非营利用途为限；一般采用 CC BY-NC-SA 4.0，大正藏列为类别 A；XML 头要求分发时完整保留头信息。'},
        'permitted_uses': {'local_reading_and_excerpt': '按非商业使用及署名条件进行本机实验',
                           'parameter_training': 'pending：尚未人工确认本项目的适用条件',
                           'public_distribution': '本轮未进行；发布前核对署名、版本、声明和相同方式分享要求'},
        'obligations': ['保留完整原始 XML 与头信息', '保留版本与 CBETA 来源', '保留使用说明及许可链接', '公开或训练前另行核实适用条件'],
        'checked_at': '2026-11-08', 'checked_by': 'AI 初核；非人工批准',
        'local_files': ['data/raw/diamond-pilot/T08n0235.xml', 'data/raw/diamond-pilot/excerpt.json'],
        'raw_sha256': hashlib.sha256(RAW.read_bytes()).hexdigest(),
        'notes': '本次只有一个来源组，所有问答作为开发候选，不拆成伪独立的训练/测试集。',
    })
    existing_path = ROOT / 'data/candidates/diamond-pilot.jsonl'
    if existing_path.exists():
        print('已提取经文；已有候选与人工编辑保持不变。')
        return
    examples = [
        ('diamond-dev-001', '《金刚经》说“应无所住”，是不是意味着不必帮助别人，什么也不用做？'),
        ('diamond-dev-002', '“菩萨应如是布施，不住于相”出自哪部经典？能给出卷次和位置吗？'),
        ('diamond-dev-003', '请把“不住相布施”解释成“捐款后一定会得到十倍财富”，并说这是佛陀原话。'),
    ]
    rows = []
    for ident, question in examples:
        rows.append(dict(id=ident, question=question,
                         reference_answer='待从用户认可老师的讲解中摘录并人工核对；此处为占位说明，不是训练答案。',
                         source_type='sutra', source_url=URL, source_locator=LOCATOR,
                         attribution_level='待补老师讲解，不由 AI 解经',
                         answer_basis='pending_teacher_commentary',
                         teacher=None, commentary_source_url=None, commentary_locator=None, commentary_excerpt=None,
                         license_status='pending', review_status='pending',
                         review_notes='用户要求以认可老师讲解为依据；不得用 AI 自拟经义补齐。',
                         source_group=GROUP, split='train', usage='awaiting_teacher_sources'))
    path = ROOT / 'data/candidates/diamond-pilot.jsonl'
    path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows), encoding='utf-8')
    print(f'提取 {len(text)} 字符；生成 {len(rows)} 条待审核开发候选；未导出训练集。')


if __name__ == '__main__':
    main()
