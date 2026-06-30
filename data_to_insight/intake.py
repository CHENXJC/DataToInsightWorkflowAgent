"""Load public-safe synthetic demo items."""

from __future__ import annotations

import json
from pathlib import Path

from data_to_insight.schemas import RawDemoItem


def load_demo_items(input_path: str | Path) -> list[RawDemoItem]:
    """Load synthetic demo items from a local JSON file."""

    path = Path(input_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Demo data must be a list of items.")

    items: list[RawDemoItem] = []
    for record in data:
        item = RawDemoItem(
            item_id=str(record["item_id"]),
            source_type=str(record["source_type"]),
            title=str(record["title"]),
            raw_text=str(record["raw_text"]),
            language=str(record["language"]),
            source_origin=str(record["source_origin"]),
            created_at=str(record["created_at"]),
            tags=[str(tag) for tag in record.get("tags", [])],
            sensitivity_level=str(record.get("sensitivity_level", "public_safe")),
            synthetic=bool(record.get("synthetic", True)),
        )
        if item.sensitivity_level != "public_safe":
            raise ValueError(f"{item.item_id} is not public-safe demo data.")
        if not item.synthetic:
            raise ValueError(f"{item.item_id} must be marked synthetic.")
        items.append(item)

    return items
