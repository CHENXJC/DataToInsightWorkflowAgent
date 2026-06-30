import json
from pathlib import Path

from data_to_insight.agenthub_exporter import build_agenthub_summary
from data_to_insight.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]


def test_agenthub_exporter_generates_parseable_summary(tmp_path):
    processed, summary = run_pipeline(ROOT / "demo_data" / "demo_items.json", tmp_path)
    payload = build_agenthub_summary(processed, summary)
    exported = json.loads((tmp_path / "agenthub_summary.json").read_text(encoding="utf-8"))

    assert payload["agent_id"] == "data_to_insight_workflow_agent"
    assert payload["demo_mode"] is True
    assert payload["public_safe"] is True
    assert exported["high_value_signals"] == summary.high_value_signals
    assert "AgentHubControlCenter" in exported["top_routes"]
