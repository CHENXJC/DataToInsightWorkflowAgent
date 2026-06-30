from pathlib import Path

from data_to_insight.classifier import classify_item
from data_to_insight.config import ACTION_TYPES, ROUTE_TARGETS
from data_to_insight.intake import load_demo_items
from data_to_insight.noise_filter import decide_route
from data_to_insight.normalizer import normalize_items
from data_to_insight.recommender import recommend_actions
from data_to_insight.scorer import score_item


ROOT = Path(__file__).resolve().parents[1]


def test_recommender_generates_action_type_and_target():
    item = normalize_items(load_demo_items(ROOT / "demo_data" / "demo_items.json"))[0]
    classification = classify_item(item)
    score = score_item(item, classification)
    route = decide_route(classification, score)
    actions = recommend_actions(classification, score, route)

    assert actions
    assert actions[0].action_type in ACTION_TYPES
    assert actions[0].target in ROUTE_TARGETS
    assert actions[0].next_step
