"""Dashboard data helpers for the Streamlit UI."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from data_to_insight.config import (
    AGENTHUB_SUMMARY_NAME,
    DEFAULT_INPUT_PATH,
    DEFAULT_OUTPUT_DIR,
    DEMO_REPORT_NAME,
)
from data_to_insight.pipeline import run_pipeline


PRIORITY_OPTIONS = ["All", "High", "Medium", "Low", "Noise", "Needs Review"]
CLASSIFICATION_OPTIONS = [
    "All",
    "course_learning",
    "business_signal",
    "project_asset",
    "career_asset",
    "market_signal",
    "customer_pain",
    "operation_issue",
    "content_idea",
    "ai_workflow_idea",
    "low_value_noise",
    "duplicate_reference",
    "needs_review",
]
ROUTE_OPTIONS = [
    "All",
    "PersonalKnowledgeAgent",
    "AgentHubControlCenter",
    "SocialPainFinderAgent",
    "BusinessOpsAgent",
    "CareerPilotAgent",
    "NewsSignalAgent",
    "VideoExtractSkill",
    "DataToInsightWorkflowAgent",
    "None",
]


def project_root() -> Path:
    """Return the repository root."""

    return Path(__file__).resolve().parents[1]


def get_default_paths(root: Path | None = None) -> dict[str, Path]:
    """Return the default local demo paths used by the dashboard."""

    base = root or project_root()
    output_dir = base / DEFAULT_OUTPUT_DIR
    return {
        "input_path": base / DEFAULT_INPUT_PATH,
        "output_dir": output_dir,
        "report_path": output_dir / DEMO_REPORT_NAME,
        "agenthub_summary_path": output_dir / AGENTHUB_SUMMARY_NAME,
        "manifest_path": base / "agent_manifest.json",
        "contract_path": base / "agent_contract.json",
    }


def _as_dict(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    return value


def run_dashboard_pipeline(
    input_path: str | Path,
    output_dir: str | Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Run the local demo pipeline and return UI-friendly dictionaries."""

    processed_items, summary = run_pipeline(input_path, output_dir)
    return [_as_dict(item) for item in processed_items], asdict(summary)


def load_agenthub_summary(summary_path: str | Path) -> dict[str, Any]:
    """Load an existing AgentHub summary JSON file."""

    return json.loads(Path(summary_path).read_text(encoding="utf-8"))


def load_or_run_dashboard_data(
    input_path: str | Path,
    output_dir: str | Path,
    force_run: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load existing demo outputs or regenerate them when requested/missing."""

    output_root = Path(output_dir)
    summary_path = output_root / AGENTHUB_SUMMARY_NAME

    if force_run or not summary_path.exists():
        return run_dashboard_pipeline(input_path, output_dir)

    summary = load_agenthub_summary(summary_path)
    return summary.get("items", []), summary


def build_summary_metrics(summary: dict[str, Any]) -> dict[str, Any]:
    """Build the dashboard metric values from a pipeline summary."""

    top_routes = summary.get("top_routes", {})
    top_route = "None"
    if isinstance(top_routes, dict) and top_routes:
        top_route = max(top_routes.items(), key=lambda item: item[1])[0]

    return {
        "total_items_processed": summary.get("total_items_processed", 0),
        "high_value_signals": summary.get("high_value_signals", 0),
        "medium_value_items": summary.get("medium_value_items", 0),
        "low_value_or_noise_items": summary.get("low_value_or_noise_items", 0),
        "recommended_actions_count": summary.get("recommended_actions_count", 0),
        "top_recommended_route": top_route,
    }


def filter_items(
    items: list[dict[str, Any]],
    priority: str = "All",
    classification: str = "All",
    route: str = "All",
) -> list[dict[str, Any]]:
    """Apply sidebar filters to processed items."""

    filtered = items
    if priority != "All":
        filtered = [item for item in filtered if item.get("priority_level") == priority]
    if classification != "All":
        filtered = [item for item in filtered if item.get("classification") == classification]
    if route != "All":
        filtered = [item for item in filtered if item.get("recommended_route") == route]
    return filtered


def get_high_value_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return high-priority insight items."""

    return [item for item in items if item.get("priority_level") == "High"]


def get_noise_review_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return low/noise/review items for the filtering queue."""

    non_keep_routes = {"ignore", "archive", "review_later"}
    low_priorities = {"Low", "Noise", "Needs Review"}
    return [
        item
        for item in items
        if item.get("priority_level") in low_priorities
        or item.get("keep_or_ignore") in non_keep_routes
        or item.get("classification") in {"low_value_noise", "needs_review", "duplicate_reference"}
    ]


def flatten_actions(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten nested recommended actions for the Action Board."""

    actions: list[dict[str, Any]] = []
    for item in items:
        for action in item.get("recommended_actions", []):
            actions.append(
                {
                    "source_item_id": item.get("item_id", ""),
                    "source_title": item.get("title", ""),
                    "classification": item.get("classification", ""),
                    "overall_score": item.get("overall_score", 0),
                    "action_type": action.get("action_type", ""),
                    "target": action.get("target", "None"),
                    "priority": action.get("priority", item.get("priority_level", "")),
                    "reason": action.get("reason", ""),
                    "next_step": action.get("next_step", ""),
                }
            )
    return actions


def group_actions_by_priority(actions: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group actions into dashboard sections."""

    groups = {
        "High Priority Actions": [],
        "Medium Priority Actions": [],
        "Low Priority Actions": [],
        "Review Later / Ignore": [],
    }
    for action in actions:
        priority = action.get("priority")
        action_type = action.get("action_type")
        if priority == "High":
            groups["High Priority Actions"].append(action)
        elif priority == "Medium":
            groups["Medium Priority Actions"].append(action)
        elif priority == "Low":
            groups["Low Priority Actions"].append(action)
        elif priority in {"Noise", "Needs Review"} or action_type in {"review_later", "ignore_as_noise"}:
            groups["Review Later / Ignore"].append(action)
        else:
            groups["Low Priority Actions"].append(action)
    return groups


def build_processed_table(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return compact table rows for processed items."""

    return [
        {
            "item_id": item.get("item_id", ""),
            "title": item.get("title", ""),
            "source_type": item.get("source_type", ""),
            "classification": item.get("classification", ""),
            "overall_score": item.get("overall_score", 0),
            "priority_level": item.get("priority_level", ""),
            "keep_or_ignore": item.get("keep_or_ignore", ""),
            "recommended_route": item.get("recommended_route", ""),
        }
        for item in items
    ]


def export_panel_status(root: Path | None = None) -> dict[str, Any]:
    """Return export file paths and existence flags for the dashboard."""

    paths = get_default_paths(root)
    return {
        "markdown_report_path": paths["report_path"],
        "agenthub_summary_path": paths["agenthub_summary_path"],
        "agent_manifest_path": paths["manifest_path"],
        "agent_contract_path": paths["contract_path"],
        "markdown_report_exists": paths["report_path"].exists(),
        "agenthub_summary_exists": paths["agenthub_summary_path"].exists(),
        "agent_manifest_exists": paths["manifest_path"].exists(),
        "agent_contract_exists": paths["contract_path"].exists(),
    }
