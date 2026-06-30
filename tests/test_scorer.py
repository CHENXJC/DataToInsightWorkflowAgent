from pathlib import Path

from data_to_insight.classifier import classify_item
from data_to_insight.config import SCORE_DIMENSIONS
from data_to_insight.intake import load_demo_items
from data_to_insight.normalizer import normalize_items
from data_to_insight.scorer import score_item


ROOT = Path(__file__).resolve().parents[1]


def test_scorer_scores_are_in_range_and_have_priority():
    items = normalize_items(load_demo_items(ROOT / "demo_data" / "demo_items.json"))

    for item in items:
        classification = classify_item(item)
        score = score_item(item, classification)

        assert set(score.scores.values) == set(SCORE_DIMENSIONS)
        assert all(0 <= value <= 5 for value in score.scores.values.values())
        assert 0 <= score.overall_score <= 5
        assert score.priority_level in {"High", "Medium", "Low", "Noise", "Needs Review"}
