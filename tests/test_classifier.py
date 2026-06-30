from pathlib import Path

from data_to_insight.classifier import classify_item
from data_to_insight.intake import load_demo_items
from data_to_insight.normalizer import normalize_items


ROOT = Path(__file__).resolve().parents[1]


def test_classifier_produces_multiple_categories():
    items = normalize_items(load_demo_items(ROOT / "demo_data" / "demo_items.json"))
    categories = {classify_item(item).classification for item in items}

    assert len(categories) >= 6
    assert "course_learning" in categories
    assert "project_asset" in categories
    assert "career_asset" in categories
    assert "low_value_noise" in categories
    assert "needs_review" in categories
