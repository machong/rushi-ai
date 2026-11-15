"""生成全文处理报告；已存在的人工来源许可记录不覆盖。仓库根目录运行。"""
from pathlib import Path
import json
import hashlib
root=Path.cwd()
folder=Path('data/sources/diamond-full')
pairs=json.loads(Path('data/candidates/diamond-full/chapter-pairs.json').read_text())
summary=json.loads(Path('data/candidates/diamond-full/summary.json').read_text())
source={
 'source_id':'hsingyun-diamond-full-official', 'source_type':'commentary',
 'teacher':'星云大师','title':'金剛經講話1、2','publisher_site':'佛光山星云大师全集',
 'catalog_url':'https://books.masterhsingyun.org/Article/CpChapterMenu?bookno=5',
 'catalog_snapshot':'data/sources/diamond-full/hsingyun-menu.html',
 'catalog_snapshot_sha256':hashlib.sha256((folder/'hsingyun-menu.html').read_bytes()).hexdigest(),
 'edition_note':'官方全集004、005册；采用抓取日期与页面哈希固定网页版本，不虚构纸本版次或ISBN',
 'collected_date':'2026-11-08','checked_by':'AI机械提取和页面归属初核；未人工批准',
 'license_status':'pending','license_evidence':{
  'observed_notice':'Copyright © 著作權 佛光山 所有 All Rights Reserved.',
  'snapshot':'data/sources/diamond-full/hsingyun-catalog.html',
  'snapshot_sha256':hashlib.sha256((folder/'hsingyun-catalog.html').read_bytes()).hexdigest(),
  'training_permission_found':False},
 'permitted_uses':{'local_source_inspection':'本轮仅作公开页面阅读核对与本机缓存，不作授权结论',
                   'parameter_training':'未找到明确许可，待权利方依据核实',
                   'public_dataset_or_adapters':'未批准，未公开分发'},
 'local_manifest':'data/sources/diamond-full/manifest.json',
 'robot_rules_check':'公开robots.txt请求返回404；不将未提供抓取规则理解为训练授权',
 'notes':['老师选择依据用户指定名单','不混合南怀瑾、杨宁或其他老师的解释',
          '讲解、译文与原典注释单独登记','不同三十二分标题分别保留，不把现代标题冒充佛经原句']}
if not (folder/'source.json').exists():
 (folder/'source.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
# 两份来源许可分开，原典固定版本沿用已有来源档案。
(folder/'cbeta-reference.json').write_text(json.dumps({
 'source_id':'cbeta-T0235-full','source_type':'sutra',
 'title':'金剛般若波羅蜜經','translator':'鳩摩羅什','canon':'T08, no. 235, 卷一',
 'source_url':'https://cbetaonline.dila.edu.tw/zh/T0235',
 'repository_revision':'8ebac86d00719479db5777dc6cd77ba111c3067a',
 'raw_file':'data/raw/diamond-pilot/T08n0235.xml',
 'raw_sha256':hashlib.sha256(Path('data/raw/diamond-pilot/T08n0235.xml').read_bytes()).hexdigest(),
 'license_reference':'data/sources/diamond-pilot/source.json',
 'copyright_notice_snapshot':'data/sources/diamond-pilot/cbeta-copyright.html',
 'scope':'正文自如是我闻至信受奉行；附文真言保留在原XML但不并入正文',
 'license_status':'pending','checked_at':'2026-11-08'
},ensure_ascii=False,indent=2)+'\n')
text='''# 第一本：《金刚经》全文处理记录

日期：2026-11-08。主线：鸠摩罗什译经文 + 用户认可的星云大师《金刚经讲话》两册。**目前完成全文资料准备和机械核对；尚未完成人工经义审核、训练许可确认、样本准入与参数训练。**

## 处理范围

- [CBETA《金刚般若波罗蜜经》卷一](https://cbetaonline.dila.edu.tw/zh/T0235)：使用固定仓库修订号 `8ebac86d00719479db5777dc6cd77ba111c3067a`，原 XML 完整保留。
- [佛光山官方《金刚经讲话》两册目录](https://books.masterhsingyun.org/Article/CpChapterMenu?bookno=5)：004、005册，三十二分，每分分别登记讲解、译文、原典与注释，共96个页面。
- 仅以这一位老师为本轮解释主线，不将其他老师的观点合成为新解释。经文是核对依据，AI 不按字面撰写经义答案。

正文边界为“如是我闻”至“信受奉行”。标题、译者题记、卷尾题记和附文真言在原 XML 中保留，机械提取时与正文分开。三十二分的章题是分章体系，分别保留常见章题与本书章题，不当作佛陀原句。

## 各步骤的实际状态

| 步骤 | 结果 | 状态 |
| --- | --- | --- |
| 经文获取与版本固定 | 完整 XML、来源版本、哈希 | 已完成机械登记 |
| 老师讲解来源 | 官方两册、96个页面均有独立缓存和哈希 | 已完成获取与归属初核 |
| 全文章节对应 | 32/32分，经文6,443字符（含标点，不计空白）连续覆盖 | 已完成机械匹配，待人工核对 |
| 版本差异记录 | 22分发现去除标点后仍存在的字词/增删差异 | 已记录，未擅自裁定或统一 |
| 训练用途许可 | 网站标明佛光山版权所有，未找到明确模型训练许可 | pending |
| 问答材料 | 32份逐分工作单，带实际讲解指针与卷页 | 待人工细化问题并选取老师讲解 |
| 内容审核与批准 | AI未替代人填写审核结论 | 0条 approved |
| 训练/验证/测试划分 | 尚无合格样本；不将重复片段或近似问答拆开 | 未执行 |
| 训练与独立评估 | 无本轮适配器、无本轮训练后分数 | 未执行 |

这里的“工作单”不是已经完成的问答数据。参考答案和讲解摘录保留为 null，缺失位置不填 AI 释义，也不以占位文字冒充可训练内容。经义答案须从老师实际讲解选取并由人工核对，不能只因填写了URL就视为完成。

## 三十二分对应与审核入口

经文位置均属 T08, no. 235, 卷一。下表链接直达对应老师讲解，章题采用原典页面常见标题；书中另有不同章节标题，已在本机对应表同时保留。

| 分 | 原典章题 | CBETA页行范围 | 老师讲解（书册/起始页） | 文字版本差异 |
| --- | --- | --- | --- | --- |
'''
for p in pairs:
 loc=p['cbeta_locator'].split('卷一, ')[1]
 label=p['pages']['commentary']['label']
 book=p['teacher_work'].split('金剛經講話')[0].strip()
 text+=f"| {p['number']:02d} | {p['traditional_chapter_label']} | {loc} | [{book}册 {label}]({p['pages']['commentary']['url']}) | {'待核对' if p['differences_ignoring_punctuation'] else '未检出'} |\n"
text+='''
机械比对先去除标点和空白，仅用于识别版本文本对应，不评价经义对错。“未检出”不等于人工校订通过。全部32段按原顺序拼回后与本次CBETA正文逐字一致，无缺段、重叠或丢字。

## 版本差异

例如第1分有“鉢／缽”异体，第5分有“則／即”差异，第13分等存在增删字串。讲解所依据的版本与本次CBETA校订文本并不完全一致；保留两者，不静默把老师的引文改成另一底本。

22分需要文字版本差异复核：'''+ '、'.join(str(n) for n in summary['chapters_with_edition_differences'])+'''。

详细逐字差异与章节对应在本机 `data/candidates/diamond-full/chapter-pairs.json`；这些是文本差异，不是AI判定的义理错误。

## 逐分人工工作单怎样填写

每分已建立一条工作单（ID `diamond-full-01` 至 `diamond-full-32`），包含原典定位、老师姓名、本书章题、讲解起始页、实际链接和缓存指针。位置：`data/candidates/diamond-full/review-worksheets.jsonl`。

1. 打开老师讲解，选择与题目对应的完整语义片段，登记原话及更具体的段落定位；不能仅拿本分首页代替具体答案位置。
2. 将当前的整分概括性占位问题细化成能由该片段直接回答的问题；需要多条问答时使用新ID，但保持相关来源组一致。
3. 参考答案以老师实际讲解为依据；如需删节或重排，保留原始摘录与编辑记录，不增添解释、不冒称佛陀原话。
4. 复核与该讲解对应的经文版本差异；确认是所选版本的引文，不擅自改字。
5. 分别填写内容审核与训练许可结论。只有实际完成后，才记录审核人、日期并改为 approved/permitted；不能让AI自动填写。
6. 合格记录再转入 reviewed；在检查同源片段、重复引文和近似问答之后，决定训练/验证/测试归属。当前工作单 split 为 null。

工作单保留 null 是有意的：它无法通过当前训练导出校验，以免误把未完成资料作为已核实答案。当前没有生成 `data/train.jsonl`、`valid.jsonl`、`test.jsonl`。

## 使用条件待确认

官网页脚标明佛光山版权所有，未发现明确的模型训练许可；公开阅读不自动解决模型训练、制作问答数据及发布适配器的使用范围。本机仅缓存公开页面用于本次来源检查，不对该用途作权利认定，也不将整部讲解作为可分发成果提供。

如有许可文件或需向权利方确认，应具体覆盖：所用作品和版本、非商业本机LoRA微调、讲解片段转问答、是否发布数据或适配器、署名及其他条件。许可依据与确认日期登记在 `data/sources/diamond-full/source.json`。本轮没有向他人发送消息或请求。

## 可复现的工具与文件

```sh
source .venv/bin/activate
# 默认只检查已有缓存，不会联网；首次获取才显式加 --fetch
python scripts/collect_diamond_full.py
python scripts/prepare_diamond_full.py
python scripts/report_diamond_full.py
python -m unittest discover -s tests -v
```

- `data/sources/diamond-full/manifest.json`：全部96个页面的链接、缓存与SHA-256。
- `data/sources/diamond-full/source.json`：老师讲解来源与使用条件状态。
- `data/sources/diamond-full/cbeta-reference.json`：经文原始版本、许可记录指针。
- `data/raw/diamond-full/cbeta-main.json`：完整正文与提取边界。
- `data/candidates/diamond-full/chapter-pairs.json`：32分全文对应、页行与版本差异。
- `data/candidates/diamond-full/review-worksheets.jsonl`：待人工选段与审核工作单。
- `data/candidates/diamond-full/summary.json`：覆盖检查与真实进度。

真实素材、缓存和工作单默认被Git忽略。报告主要提供来源索引与处理状态，没有复制整部老师讲解。
'''
Path('docs/experiments/diamond_full.md').write_text(text)
print('已生成全文处理报告和来源登记。')
