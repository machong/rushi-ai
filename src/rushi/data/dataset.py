"""审核记录校验与显式分组导出；不自动批准或推断来源。"""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

SPLITS = ("train", "valid", "test")
REQUIRED = (
    "id", "question", "reference_answer", "source_type", "source_url",
    "source_locator", "attribution_level", "license_status", "review_status",
    "review_notes", "source_group", "split",
)


def normalized(text):
    return re.sub(r"[\W_]+", "", unicodedata.normalize("NFKC", text).casefold())


def load_records(path):
    records = []
    with Path(path).open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"第 {number} 行 JSON 无效：{exc.msg}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"第 {number} 行必须是 JSON 对象")
            records.append(row)
    if not records:
        raise ValueError("数据文件为空")
    return records


def validate(records, for_export=False):
    errors = []
    ids, groups, questions = set(), {}, {}
    for number, row in enumerate(records, 1):
        label = f"第 {number} 条"
        missing = [key for key in REQUIRED if key not in row]
        if missing:
            errors.append(f"{label} 缺少字段：{', '.join(missing)}")
            continue
        invalid = [key for key in REQUIRED if key not in ("source_url", "source_locator")
                   and (not isinstance(row[key], str) or not row[key].strip())]
        invalid += [key for key in ("source_url", "source_locator")
                    if row[key] is not None and
                    (not isinstance(row[key], str) or not row[key].strip())]
        if invalid:
            errors.append(f"{label} 字段必须是非空字符串（来源字段可为 null）：{', '.join(invalid)}")
            continue
        if row["id"] in ids:
            errors.append(f"{label} id 重复：{row['id']}")
        ids.add(row["id"])
        split = row["split"]
        if split not in SPLITS:
            errors.append(f"{label} split 必须为 train / valid / test")
        if row["review_status"] not in ("draft", "pending", "approved", "rejected"):
            errors.append(f"{label} review_status 无效")
        if row["license_status"] not in ("pending", "permitted", "prohibited", "original_example"):
            errors.append(f"{label} license_status 无效")
        group = row["source_group"]
        if group in groups and groups[group] != split:
            errors.append(f"{label} 来源组 {group} 跨数据集，可能泄漏")
        groups[group] = split
        question = normalized(row["question"])
        if not question:
            errors.append(f"{label} 问题缺少有效文字")
        if question in questions:
            errors.append(f"{label} 问题与第 {questions[question]} 条重复")
        questions[question] = number
        if for_export:
            # 经义答案必须以真实老师讲解为依据；原文只可用于引用和元数据核对。
            if row["source_type"] in ("sutra", "commentary", "video_lecture"):
                basis = row.get("answer_basis")
                if basis == "source_metadata":
                    pass  # 仅经名、译者、卷页等事实；是否混入释义仍由人工审核。
                elif basis != "teacher_commentary":
                    errors.append(f"{label} 经义答案缺少老师讲解依据，禁止 AI 自拟解经")
                else:
                    fields = ("teacher", "commentary_source_url", "commentary_locator", "commentary_excerpt")
                    if any(not isinstance(row.get(key), str) or not row[key].strip() for key in fields):
                        errors.append(f"{label} 老师、讲解链接、定位与原文摘录必须完整")
            if row["review_status"] != "approved":
                errors.append(f"{label} 尚未审核通过")
            if row["license_status"] != "permitted":
                errors.append(f"{label} 未明确获准训练（示例不可导出）")
            if not row["source_url"] or not row["source_locator"]:
                errors.append(f"{label} 缺少可追溯来源或定位")
    return errors


def export_dataset(source, destination):
    records = load_records(source)
    errors = validate(records, for_export=True)
    if errors:
        raise ValueError("\n".join(errors))
    counts = {split: sum(row["split"] == split for row in records) for split in SPLITS}
    if not all(counts.values()):
        raise ValueError("train、valid、test 都必须包含独立审核样本，请显式划分")
    destination = Path(destination)
    # 禁止覆盖旧版本，保证每次导出独立留档。
    destination.mkdir(parents=True, exist_ok=False)
    manifest = {"format_version": 1, "records": [], "files": {}, "counts": counts}
    for split in SPLITS:
        lines = []
        for row in records:
            if row["split"] != split:
                continue
            lines.append(json.dumps({"messages": [
                {"role": "user", "content": row["question"]},
                {"role": "assistant", "content": row["reference_answer"]},
            ]}, ensure_ascii=False))
            manifest["records"].append({key: row[key] for key in ("id", "source_group", "split")})
        content = ("\n".join(lines) + "\n").encode("utf-8")
        (destination / f"{split}.jsonl").write_bytes(content)
        manifest["files"][f"{split}.jsonl"] = hashlib.sha256(content).hexdigest()
    # 保留实际参与导出的审核记录快照，避免原始文件后来改变。
    snapshot = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records)
    (destination / "reviewed.snapshot.jsonl").write_text(snapshot, encoding="utf-8")
    manifest["review_snapshot_sha256"] = hashlib.sha256(snapshot.encode("utf-8")).hexdigest()
    (destination / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return counts
