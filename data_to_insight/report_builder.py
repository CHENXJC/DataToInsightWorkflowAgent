"""Build Markdown reports for the D2I demo pipeline."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from data_to_insight.schemas import PipelineSummary, ProcessedInsightItem


def _first_signal(item: ProcessedInsightItem) -> str:
    return item.key_signals[0].signal if item.key_signals else ""


def _first_action(item: ProcessedInsightItem) -> str:
    if not item.recommended_actions:
        return ""
    action = item.recommended_actions[0]
    return f"{action.action_type} -> {action.target}"


def build_markdown_report(
    processed_items: list[ProcessedInsightItem],
    summary: PipelineSummary,
) -> str:
    """Return the Markdown report content."""

    top_routes = Counter()
    for item in processed_items:
        top_routes[item.recommended_route] += 1

    top_high_value = [
        item for item in processed_items if item.priority_level == "High" and item.keep_or_ignore != "ignore"
    ][:5]
    low_or_noise = [
        item
        for item in processed_items
        if item.priority_level in {"Low", "Noise", "Needs Review"}
        or item.keep_or_ignore in {"ignore", "archive", "review_later"}
    ]

    lines = [
        "# DataToInsightWorkflowAgent Demo Insight Report",
        "",
        "## Executive Summary",
        "",
        f"- Total items processed: {summary.total_items_processed}",
        f"- High-value signals: {summary.high_value_signals}",
        f"- Medium-value references: {summary.medium_value_items}",
        f"- Low-value/noise items: {summary.low_value_or_noise_items}",
        f"- Recommended actions count: {summary.recommended_actions_count}",
        "- Top recommended routes: "
        + ", ".join(f"{route} ({count})" for route, count in top_routes.most_common(5)),
        "",
        "## Top High-Value Signals",
        "",
    ]

    for item in top_high_value:
        lines.extend(
            [
                f"### {item.title}",
                "",
                f"- Classification: `{item.classification}`",
                f"- Score: {item.overall_score}",
                f"- Key signal: {_first_signal(item)}",
                f"- Recommended action: {_first_action(item)}",
                f"- Recommended route: `{item.recommended_route}`",
                "",
            ]
        )

    lines.extend(["## Processed Items", ""])

    for item in processed_items:
        lines.extend(
            [
                f"### {item.title}",
                "",
                f"- Classification: `{item.classification}`",
                f"- Overall score: {item.overall_score}",
                f"- Priority level: `{item.priority_level}`",
                f"- Keep or ignore: `{item.keep_or_ignore}`",
                f"- Key signal: {_first_signal(item)}",
                f"- Recommended action: {_first_action(item)}",
                f"- Recommended route: `{item.recommended_route}`",
                f"- Reason: {item.reason}",
                "",
            ]
        )

    lines.extend(["## Noise / Low-Value Items", ""])

    for item in low_or_noise:
        lines.append(
            f"- **{item.title}**: `{item.keep_or_ignore}` / `{item.priority_level}` - {item.reason}"
        )

    lines.extend(
        [
            "",
            "## AgentHub Summary",
            "",
            "- Agent: DataToInsightWorkflowAgent",
            "- Status: D2I-002-DEMO-DATA-PIPELINE-MVP-COMPLETE",
            f"- Latest report path: `{summary.latest_report_path}`",
            f"- AgentHub summary path: `{summary.agenthub_summary_path}`",
            f"- Top routes: {summary.top_routes}",
            "",
            "## Public-safe Notice",
            "",
            "All data in this report is synthetic demo data. This run used no real connector, no real user files, no external API call, and no secret/token/credential input.",
        ]
    )

    return "\n".join(lines) + "\n"


def write_markdown_report(
    processed_items: list[ProcessedInsightItem],
    summary: PipelineSummary,
    output_path: str | Path,
) -> Path:
    """Write the Markdown report."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_markdown_report(processed_items, summary), encoding="utf-8")
    return path
