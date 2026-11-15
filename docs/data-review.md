# 数据审核约定

**新增约定（2026-11-08）：** 经义解释和标准答案须依据用户认可老师的实际讲解，不采用 AI 按经文字面自拟的释义；没有讲解则待补。具体见[讲解依据约定](commentary_policy.md)及[资料线索](commentary_sources.md)。

字段示例见 `data/examples/review-record.jsonl`。所有字段必须保留；审核意见不得为空。

- `review_status`：draft / pending / approved / rejected。
- `license_status`：pending / permitted / prohibited / original_example。
- `permitted` 表示已人工核实允许此次模型训练；证据、署名要求和核验日期记录在来源档案与 review_notes。
- `source_group`：同一经文段落、讲经片段及其近似改写必须共用一个组。人工把相关材料归入同组，不要仅使用问答 ID。
- `split`：人工指定 train / valid / test，同组不得跨集合。测试题独立保留，不参与调参。
- 逐项检查术语、上下文、引用、宗派、解释层次与非操纵性；不确定时保持 pending。

`validate` 检查字段与重复；`export` 额外要求审核通过、许可明确、来源可定位，且三个集合均非空。
任意不合格记录都会使整个导出失败，不静默丢弃。导出目录禁止覆盖。

自动检查只能识别同组跨集合与规范化后重复的问题；不能判断经义、授权真实性或语义近似，仍须人工复核。

完整的资料登记要求见[来源政策](source_policy.md)，内容准入和独立测试评分见[审核标准](review_rubric.md)。
