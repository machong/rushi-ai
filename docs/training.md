# 第一次训练

开始前请阅读[训练方法](training_method.md)、[来源政策](source_policy.md)及[审核标准](review_rubric.md)。

1. 使用原生 ARM64 Python 3.10+（建议新建 Python 3.12 环境），在仓库根目录执行：

   ```sh
   python3.12 -m venv .venv
   source .venv/bin/activate
   python -m pip install -e '.[train]'
   rushi doctor
   python -m pip freeze > configs/environment.local.txt
   ```

   `environment.local.txt` 是本机安装快照，首次实际安装后生成；本机已安装的版本见该快照；已验证 MLX GPU 计算、模型推理与训练命令入口，尚未验证实际微调。

2. 核实中文小模型的许可、MLX 支持与资源需求，固定模型仓库修订号并下载到独立本地目录；在运行记录中保存 ID、revision、量化方式、许可证与模型文件哈希。先完成一次基础推理。
3. 人工审核数据，导出独立版本：

   ```sh
   rushi validate data/reviewed/records.jsonl --for-export
   rushi export data/reviewed/records.jsonl --output data/exports/v001
   ```

4. 按 `evaluations/run-template.json` 建立运行记录。先保存测试题的基座回答、提示词、聊天模板、随机种子和生成参数。
5. 复制 `configs/lora.example.yaml` 为本次运行配置，填写固定的本地模型路径、数据目录和全新的适配器目录。20 步仅用于流程实验，不是质量建议。

   ```sh
   mlx_lm.lora --help
   mlx_lm.lora --config configs/lora.local.yaml
   ```

6. 留存配置、终端日志、依赖版本、数据 manifest 和适配器文件。确认实际产生适配器权重，然后在相同模型、提示词与生成设置下比较加载/不加载适配器的回答。
7. 使用独立题集进行盲评，记录经典忠实度、出处、义理、慈悲、自主性和稳健性。损失下降不等于质量提升。

单题推理记录工具见 `scripts/baseline.py`；批量盲评自动化尚未实现。
本项目不会自动下载模型、转录视频或把示例当成训练材料。

官方依据（初始化时核对）：
- https://github.com/ml-explore/mlx-lm
- https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md


## 当前本机状态（2026-11-08）

- Python 3.12.16（项目 `.tools/python/`），虚拟环境 `.venv/`。
- macOS 26.5.1，Apple M5 Pro，24 GiB 统一内存。
- MLX 0.32.4 / mlx-lm 0.32.2；完整依赖见 `configs/environment.local.txt`。
- 模型与固定 revision 见 `configs/model.json`；已下载到本机 `models/`。
- 已完成一条中文基线推理：`evaluations/runs/baseline-001.json`。包含模型哈希、完整提示词、采样参数、回答、耗时和峰值内存。
- 此题与字段示例相近，仅用于流程验证，不算独立测试；回答尚未通过经义审核。模型关于“经典中并无”的表述没有检索证据，需在后续评估中检查过度自信。
- 尚无已批准训练集，未启动参数训练，也未产生适配器。

日常使用：

```sh
source .venv/bin/activate
rushi doctor
python scripts/baseline.py --output evaluations/runs/baseline-002.json
```

加载训练后适配器进行同题对比时增加 `--adapter-path adapters/本次运行目录`。
Metal GPU 在受限沙箱内可能不可访问；请在正常的本机终端执行推理与训练。
`doctor` 只检查安装前提，不代表 GPU 实际可访问；本次已另外验证真实 GPU 计算。
