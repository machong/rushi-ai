"""轻量命令行；数据工具仅使用 Python 标准库。"""
import argparse
import importlib.metadata
import json
import platform
import sys
from pathlib import Path

from rushi.data.dataset import export_dataset, load_records, validate


def main(argv=None):
    parser = argparse.ArgumentParser(prog="rushi", description="如是训练项目工具")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="检查 Python、架构与 MLX 安装状态")
    check = commands.add_parser("validate", help="检查审核记录；不会自动批准")
    check.add_argument("source", type=Path)
    check.add_argument("--for-export", action="store_true")
    export = commands.add_parser("export", help="导出审核通过的数据集到新目录")
    export.add_argument("source", type=Path)
    export.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            try:
                mlx_version = importlib.metadata.version("mlx-lm")
            except importlib.metadata.PackageNotFoundError:
                mlx_version = "未安装"
            ready = sys.version_info >= (3, 10) and platform.system() == "Darwin" and platform.machine() == "arm64" and mlx_version != "未安装"
            print(json.dumps({"python": platform.python_version(), "platform": platform.system(),
                              "architecture": platform.machine(), "mlx_lm": mlx_version,
                              "training_prerequisites_present": ready}, ensure_ascii=False, indent=2))
            return 0 if ready else 1
        if args.command == "validate":
            records = load_records(args.source)
            errors = validate(records, args.for_export)
            if errors:
                raise ValueError("\n".join(errors))
            print(f"结构校验通过：{len(records)} 条；这不代表已完成内容或授权审核。")
        elif args.command == "export":
            print(json.dumps(export_dataset(args.source, args.output), ensure_ascii=False))
    except (ValueError, OSError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    return 0
