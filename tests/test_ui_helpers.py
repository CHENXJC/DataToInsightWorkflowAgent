from pathlib import Path

from data_to_insight.ui_helpers import (
    build_summary_metrics,
    export_panel_status,
    filter_items,
    flatten_actions,
    get_high_value_items,
    get_noise_review_items,
    group_actions_by_priority,
    run_dashboard_pipeline,
)


ROOT = Path(__file__).resolve().parents[1]


def _dashboard_data(tmp_path):
    return run_dashboard_pipeline(ROOT / "demo_data" / "demo_items.json", tmp_path)


def test_summary_metrics_can_be_built_from_pipeline_output(tmp_path):
    _items, summary = _dashboard_data(tmp_path)
    metrics = build_summary_metrics(summary)

    assert metrics["total_items_processed"] == 14
    assert metrics["high_value_signals"] >= 1
    assert metrics["recommended_actions_count"] >= 1
    assert metrics["top_recommended_route"] in {"DataToInsightWorkflowAgent", "AgentHubControlCenter", "None"}


def test_priority_filter_can_filter_items(tmp_path):
    items, _summary = _dashboard_data(tmp_path)
    high_items = filter_items(items, priority="High")

    assert high_items
    assert all(item["priority_level"] == "High" for item in high_items)


def test_classification_filter_can_filter_items(tmp_path):
    items, _summary = _dashboard_data(tmp_path)
    project_items = filter_items(items, classification="project_asset")

    assert project_items
    assert all(item["classification"] == "project_asset" for item in project_items)


def test_route_filter_can_filter_items(tmp_path):
    items, _summary = _dashboard_data(tmp_path)
    routed_items = filter_items(items, route="AgentHubControlCenter")

    assert routed_items
    assert all(item["recommended_route"] == "AgentHubControlCenter" for item in routed_items)


def test_action_board_data_can_be_flattened_and_grouped(tmp_path):
    items, _summary = _dashboard_data(tmp_path)
    actions = flatten_actions(items)
    grouped = group_actions_by_priority(actions)

    assert actions
    assert all("source_title" in action for action in actions)
    assert sum(len(group) for group in grouped.values()) == len(actions)


def test_high_value_items_can_be_identified(tmp_path):
    items, _summary = _dashboard_data(tmp_path)
    high_items = get_high_value_items(items)

    assert high_items
    assert all(item["priority_level"] == "High" for item in high_items)


def test_noise_review_items_can_be_identified(tmp_path):
    items, _summary = _dashboard_data(tmp_path)
    queue_items = get_noise_review_items(items)

    assert queue_items
    assert any(item["keep_or_ignore"] in {"ignore", "review_later", "archive"} for item in queue_items)


def test_export_paths_are_reported():
    status = export_panel_status(ROOT)

    assert status["markdown_report_path"].name == "demo_insight_report.md"
    assert status["agenthub_summary_path"].name == "agenthub_summary.json"
    assert status["agent_manifest_exists"] is True
    assert status["agent_contract_exists"] is True
