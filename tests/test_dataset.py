import json
import tempfile
import unittest
from pathlib import Path

from rushi.data.dataset import export_dataset, validate


def record(index, split):
    return dict(id=str(index), question=f"问题{index}", reference_answer="已核对回答",
                source_type="sutra", answer_basis="source_metadata", source_url="https://example.org/source",
                source_locator=f"段落{index}", attribution_level="解释",
                license_status="permitted", review_status="approved",
                review_notes="测试夹具，不是真实审核结果", source_group=str(index), split=split)


class DatasetTests(unittest.TestCase):
    def test_reject_unreviewed_and_unlicensed(self):
        row = record(1, "train")
        row.update(review_status="draft", license_status="pending")
        self.assertEqual(len(validate([row], for_export=True)), 2)

    def test_group_leakage_and_normalized_duplicate(self):
        a, b = record(1, "train"), record(2, "test")
        b.update(source_group=a["source_group"], question=a["question"] + "？")
        self.assertEqual(len(validate([a, b])), 2)

    def test_reject_ai_interpretation_even_if_marked_approved(self):
        row = record(1, "train")
        row["answer_basis"] = "ai_generated"
        self.assertTrue(validate([row], for_export=True))
        row["answer_basis"] = "teacher_commentary"
        self.assertTrue(validate([row], for_export=True))
        row.update(teacher="测试讲者", commentary_source_url="https://example.org/lecture",
                   commentary_locator="00:01–00:30", commentary_excerpt="测试讲解摘录")
        self.assertEqual(validate([row], for_export=True), [])

    def test_export_snapshot_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "reviewed.jsonl"
            rows = [record(i, split) for i, split in enumerate(("train", "valid", "test"))]
            source.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
            destination = Path(folder) / "v001"
            self.assertEqual(export_dataset(source, destination), dict(train=1, valid=1, test=1))
            training = json.loads((destination / "train.jsonl").read_text())
            self.assertEqual(set(training), {"messages"})
            self.assertTrue((destination / "reviewed.snapshot.jsonl").exists())
            with self.assertRaises(FileExistsError):
                export_dataset(source, destination)

    def test_failure_leaves_no_export(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "reviewed.jsonl"
            source.write_text(json.dumps(record(1, "train")), encoding="utf-8")
            destination = Path(folder) / "v001"
            with self.assertRaises(ValueError):
                export_dataset(source, destination)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
