import json
from pathlib import Path

from data_to_insight.intake import load_demo_items


ROOT = Path(__file__).resolve().parents[1]


def test_demo_items_json_can_be_loaded():
    path = ROOT / "demo_data" / "demo_items.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    items = load_demo_items(path)

    assert len(data) >= 12
    assert len(items) == len(data)
    assert all(item.synthetic for item in items)
    assert all(item.sensitivity_level == "public_safe" for item in items)
