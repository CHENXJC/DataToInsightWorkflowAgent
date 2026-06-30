from pathlib import Path

from data_to_insight.classifier import classify_item
from data_to_insight.intake import load_demo_items
from data_to_insight.noise_filter import decide_route
from data_to_insight.normalizer import normalize_items
from data_to_insight.scorer import score_item


ROOT = Path(__file__).resolve().parents[1]


def test_noise_filter_identifies_keep_and_non_keep_routes():
    items = normalize_items(load_demo_items(ROOT / "demo_data" / "demo_items.json"))
    decisions = []

    for item in items:
        classification = classify_item(item)
        score = score_item(item, classification)
        decisions.append(decide_route(classification, score).keep_or_ignore)

    assert any(decision in {"keep", "route_to_agent", "convert_to_project"} for decision in decisions)
    assert any(decision in {"ignore", "archive", "review_later"} for decision in decisions)
