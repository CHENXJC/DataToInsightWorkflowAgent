"""End-to-end synthetic demo data pipeline."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from data_to_insight.agenthub_exporter import export_agenthub_summary
from data_to_insight.classifier import classify_item
from data_to_insight.config import AGENTHUB_SUMMARY_NAME, DEFAULT_OUTPUT_DIR, DEMO_REPORT_NAME
from data_to_insight.insight_extractor import extract_key_signals
from data_to_insight.intake import load_demo_items
from data_to_insight.noise_filter import decide_route
from data_to_insight.normalizer import normalize_items
from data_to_insight.recommender import recommend_actions
from data_to_insight.report_builder import write_markdown_report
from data_to_insight.schemas import PipelineSummary, ProcessedInsightItem
from data_to_insight.scorer import score_item


def _path_for_summary(path: Path) -> str:
    return path.as_posix()


def process_items(input_path: str | Path) -> list[ProcessedInsightItem]:
    """Run intake through recommendations and return processed items."""

    raw_items = load_demo_items(input_path)
    normalized_items = normalize_items(raw_items)
    processed: list[ProcessedInsightItem] = []

    for item in normalized_items:
        classification = classify_item(item)
        score = score_item(item, classification)
        route = decide_route(classification, score)
        signals = extract_key_signals(item, classification, score)
        actions = recommend_actions(classification, score, route)
        processed.append(
            ProcessedInsightItem(
                item_id=item.item_id,
                source_type=item.source_type,
                title=item.title,
                normalized_text=item.normalized_text,
                category=classification.classification,
                classification=classification.classification,
                scores=score.scores.values,
                overall_score=score.overall_score,
                priority_level=score.priority_level,
                keep_or_ignore=route.keep_or_ignore,
                key_signals=signals,
                recommended_actions=actions,
                recommended_route=route.recommended_route,
                reason=route.reason,
            )
        )

    return processed


def build_summary(
    processed_items: list[ProcessedInsightItem],
    report_path: Path,
    agenthub_summary_path: Path,
) -> PipelineSummary:
    """Build aggregate pipeline summary."""

    route_counts = Counter(item.recommended_route for item in processed_items)
    low_or_noise = sum(
        1
        for item in processed_items
        if item.priority_level in {"Low", "Noise", "Needs Review"}
        or item.keep_or_ignore in {"ignore", "archive", "review_later"}
    )

    return PipelineSummary(
        total_items_processed=len(processed_items),
        high_value_signals=sum(1 for item in processed_items if item.priority_level == "High"),
        medium_value_items=sum(1 for item in processed_items if item.priority_level == "Medium"),
        low_value_or_noise_items=low_or_noise,
        recommended_actions_count=sum(len(item.recommended_actions) for item in processed_items),
        top_routes=dict(route_counts.most_common()),
        latest_report_path=_path_for_summary(report_path),
        agenthub_summary_path=_path_for_summary(agenthub_summary_path),
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def run_pipeline(
    input_path: str | Path,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> tuple[list[ProcessedInsightItem], PipelineSummary]:
    """Run the complete D2I demo pipeline and write report outputs."""

    output_root = Path(output_dir)
    report_path = output_root / DEMO_REPORT_NAME
    agenthub_summary_path = output_root / AGENTHUB_SUMMARY_NAME

    processed_items = process_items(input_path)
    summary = build_summary(processed_items, report_path, agenthub_summary_path)
    write_markdown_report(processed_items, summary, report_path)
    export_agenthub_summary(processed_items, summary, agenthub_summary_path)

    return processed_items, summary


def processed_items_to_dicts(processed_items: list[ProcessedInsightItem]) -> list[dict]:
    """Return JSON-serializable processed items."""

    return [asdict(item) for item in processed_items]
