# 第一本：《金刚经》全文处理记录

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
| 01 | 法會因由分第一 | 0748c20–0748c24 | [004册 p031　講話](https://books.masterhsingyun.org/ArticleDetail/artcle251) | 待核对 |
| 02 | 善現啟請分第二 | 0748c24–0749a04 | [004册 p045　講話](https://books.masterhsingyun.org/ArticleDetail/artcle254) | 未检出 |
| 03 | 大乘正宗分第三 | 0749a05–0749a11 | [004册 p061　講話](https://books.masterhsingyun.org/ArticleDetail/artcle257) | 未检出 |
| 04 | 妙行無住分第四 | 0749a12–0749a20 | [004册 p079　講話](https://books.masterhsingyun.org/ArticleDetail/artcle260) | 未检出 |
| 05 | 如理實見分第五 | 0749a21–0749a25 | [004册 p095　講話](https://books.masterhsingyun.org/ArticleDetail/artcle263) | 待核对 |
| 06 | 正信希有分第六 | 0749a26–0749b11 | [004册 p111　講話](https://books.masterhsingyun.org/ArticleDetail/artcle266) | 待核对 |
| 07 | 無得無說分第七 | 0749b12–0749b18 | [004册 p133　講話](https://books.masterhsingyun.org/ArticleDetail/artcle269) | 待核对 |
| 08 | 依法出生分第八 | 0749b18–0749b25 | [004册 p151　講話](https://books.masterhsingyun.org/ArticleDetail/artcle272) | 未检出 |
| 09 | 一相無相分第九 | 0749b26–0749c15 | [004册 p173　講話](https://books.masterhsingyun.org/ArticleDetail/artcle276) | 待核对 |
| 10 | 莊嚴淨土分第十 | 0749c16–0749c25 | [004册 p195　講話](https://books.masterhsingyun.org/ArticleDetail/artcle280) | 待核对 |
| 11 | 無為福勝分第十一 | 0749c25–0750a05 | [004册 p215　講話](https://books.masterhsingyun.org/ArticleDetail/artcle284) | 待核对 |
| 12 | 尊重正教分第十二 | 0750a06–0750a10 | [004册 p235　講話](https://books.masterhsingyun.org/ArticleDetail/artcle288) | 待核对 |
| 13 | 如法受持分第十三 | 0750a11–0750a26 | [004册 p253　講話](https://books.masterhsingyun.org/ArticleDetail/artcle292) | 待核对 |
| 14 | 離相寂滅分第十四 | 0750a27–0750c06 | [004册 p273　講話](https://books.masterhsingyun.org/ArticleDetail/artcle296) | 待核对 |
| 15 | 持經功德分第十五 | 0750c07–0750c23 | [004册 p299　講話](https://books.masterhsingyun.org/ArticleDetail/artcle300) | 待核对 |
| 16 | 能淨業障分第十六 | 0750c24–0751a07 | [004册 p317　講話](https://books.masterhsingyun.org/ArticleDetail/artcle303) | 待核对 |
| 17 | 究竟無我分第十七 | 0751a08–0751b12 | [005册 p007　講話](https://books.masterhsingyun.org/ArticleDetail/artcle878) | 待核对 |
| 18 | 一體同觀分第十八 | 0751b13–0751b28 | [005册 p033　講話](https://books.masterhsingyun.org/ArticleDetail/artcle882) | 待核对 |
| 19 | 法界通化分第十九 | 0751b29–0751c04 | [005册 p055　講話](https://books.masterhsingyun.org/ArticleDetail/artcle891) | 未检出 |
| 20 | 離色離相分第二十 | 0751c05–0751c11 | [005册 p071　講話](https://books.masterhsingyun.org/ArticleDetail/artcle898) | 未检出 |
| 21 | 非說所說分第二十一 | 0751c11–0751c19 | [005册 p089　講話](https://books.masterhsingyun.org/ArticleDetail/artcle902) | 未检出 |
| 22 | 無法可得分第二十二 | 0751c20–0751c23 | [005册 p111　講話](https://books.masterhsingyun.org/ArticleDetail/artcle906) | 待核对 |
| 23 | 淨心行善第二十三 | 0751c24–0751c28 | [005册 p135　講話](https://books.masterhsingyun.org/ArticleDetail/artcle909) | 待核对 |
| 24 | 福智無比分第二十四 | 0751c29–0752a04 | [005册 p153　講話](https://books.masterhsingyun.org/ArticleDetail/artcle913) | 未检出 |
| 25 | 化無所化分第二十五 | 0752a05–0752a10 | [005册 p169　講話](https://books.masterhsingyun.org/ArticleDetail/artcle916) | 待核对 |
| 26 | 法身非相分第二十六 | 0752a11–0752a18 | [005册 p187　講話](https://books.masterhsingyun.org/ArticleDetail/artcle921) | 待核对 |
| 27 | 無斷無滅分第二十七 | 0752a19–0752a25 | [005册 p205　講話](https://books.masterhsingyun.org/ArticleDetail/artcle927) | 待核对 |
| 28 | 不受不貪分第二十八 | 0752a25–0752b02 | [005册 p225　講話](https://books.masterhsingyun.org/ArticleDetail/artcle930) | 待核对 |
| 29 | 威儀寂靜分第二十九 | 0752b03–0752b05 | [005册 p243　講話](https://books.masterhsingyun.org/ArticleDetail/artcle933) | 未检出 |
| 30 | 一合理相分第三十 | 0752b06–0752b14 | [005册 p265　講話](https://books.masterhsingyun.org/ArticleDetail/artcle936) | 待核对 |
| 31 | 知見不生分第三十一 | 0752b15–0752b23 | [005册 p285　講話](https://books.masterhsingyun.org/ArticleDetail/artcle939) | 待核对 |
| 32 | 應化非真分第三十二 | 0752b23–0752c02 | [005册 p303　講話](https://books.masterhsingyun.org/ArticleDetail/artcle942) | 未检出 |

机械比对先去除标点和空白，仅用于识别版本文本对应，不评价经义对错。“未检出”不等于人工校订通过。全部32段按原顺序拼回后与本次CBETA正文逐字一致，无缺段、重叠或丢字。

## 版本差异

例如第1分有“鉢／缽”异体，第5分有“則／即”差异，第13分等存在增删字串。讲解所依据的版本与本次CBETA校订文本并不完全一致；保留两者，不静默把老师的引文改成另一底本。

22分需要文字版本差异复核：1、5、6、7、9、10、11、12、13、14、15、16、17、18、22、23、25、26、27、28、30、31。

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
