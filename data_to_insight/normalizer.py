"""Normalize demo data records for downstream processing."""

from __future__ import annotations

import re

from data_to_insight.schemas import NormalizedItem, RawDemoItem


def normalize_text(text: str) -> str:
    """Collapse whitespace and keep public-safe text readable."""

    return re.sub(r"\s+", " ", text).strip()


def normalize_item(item: RawDemoItem) -> NormalizedItem:
    """Normalize one raw demo item."""

    return NormalizedItem(
        item_id=item.item_id,
        source_type=item.source_type.strip().lower(),
        title=normalize_text(item.title),
        normalized_text=normalize_text(item.raw_text),
        language=item.language.strip().lower(),
        source_origin=item.source_origin.strip(),
        created_at=item.created_at,
        tags=[tag.strip().lower() for tag in item.tags],
        sensitivity_level=item.sensitivity_level,
        synthetic=item.synthetic,
    )


def normalize_items(items: list[RawDemoItem]) -> list[NormalizedItem]:
    """Normalize a list of raw demo items."""

    return [normalize_item(item) for item in items]
