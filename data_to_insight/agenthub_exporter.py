"""Export AgentHub-compatible summary JSON."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from data_to_insight.config import AGENT_ID, PACKAGE_NAME, STATUS
from data_to_insight.schemas import PipelineSummary, ProcessedInsightItem


CAPABILITIES = [
    "synthetic_demo_data_intake",
    "data_normalization",
    "rule_based_classification",
    "multi_dimension_scoring",
    "noise_filtering",
    "insight_signal_extraction",
    "action_recommendation",
    "markdown_report_export",
    "agenthub_summary_export",
]


def build_agenthub_summary(
    processed_items: list[ProcessedInsightItem],
    summary: PipelineSummary,
) -> dict:
    """Build a JSON-serializable AgentHub summary object."""

    return {
        "agent_id": AGENT_ID,
        "agent_name": PACKAGE_NAME,
        "status": STATUS,
        "demo_mode": True,
        "public_safe": True,
        "total_items_processed": summary.total_items_processed,
        "high_value_signals": summary.high_value_signals,
        "medium_value_items": summary.medium_value_items,
        "low_value_or_noise_items": summary.low_value_or_noise_items,
        "recommended_actions_count": summary.recommended_actions_count,
        "top_routes": summary.top_routes,
        "latest_report_path": summary.latest_report_path,
        "capabilities": CAPABILITIES,
        "generated_at": summary.generated_at,
        "route_targets": sorted({item.recommended_route for item in processed_items}),
        "items": [asdict(item) for item in processed_items],
    }


def export_agenthub_summary(
    processed_items: list[ProcessedInsightItem],
    summary: PipelineSummary,
    output_path: str | Path,
) -> Path:
    """Write AgentHub summary JSON."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_agenthub_summary(processed_items, summary)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
