import json
from pathlib import Path

from data_to_insight.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_runs_end_to_end(tmp_path):
    processed, summary = run_pipeline(ROOT / "demo_data" / "demo_items.json", tmp_path)

    report_path = tmp_path / "demo_insight_report.md"
    agenthub_path = tmp_path / "agenthub_summary.json"

    assert len(processed) >= 12
    assert summary.total_items_processed == len(processed)
    assert summary.high_value_signals >= 1
    assert summary.medium_value_items >= 1
    assert summary.low_value_or_noise_items >= 1
    assert report_path.exists()
    assert agenthub_path.exists()
    assert "Public-safe Notice" in report_path.read_text(encoding="utf-8")
    assert json.loads(agenthub_path.read_text(encoding="utf-8"))["total_items_processed"] == len(processed)
