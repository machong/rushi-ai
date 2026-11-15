# 数据目录

- `sources/`：经典/视频来源、版本、许可证明与核验日期。
- `raw/`：有权处理的原始资料。
- `transcripts/`：OCR、ASR 与人工校订结果。
- `candidates/`：尚待人工审核的候选问答。
- `reviewed/`：人工审核通过、含审核字段的 JSONL 记录。
- `examples/`：可提交的格式示例，不是已批准训练数据。
- `exports/v001/`：命令导出的 train/valid/test、审核快照和哈希清单。

除格式示例与本说明外，数据默认被 Git 忽略；公开前逐项检查权利与隐私。


首本全文工作包位于 `candidates/diamond-full/`。其中 `review-worksheets.jsonl` 是带 null 的人工工作单，不是训练JSONL；`chapter-pairs.json` 保存机械对应和版本差异。老师讲解缓存保存在 `raw/diamond-full/hsingyun/`，来源和哈希在 `sources/diamond-full/`。只有完成老师原讲解选段、人工审核和许可确认后，才形成可转入 reviewed 的问答。
