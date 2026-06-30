from data_to_insight.normalizer import normalize_item
from data_to_insight.schemas import RawDemoItem


def test_normalizer_generates_standard_fields():
    item = RawDemoItem(
        item_id="demo_test",
        source_type=" Learning_Note ",
        title="  Sample   Note ",
        raw_text="Line one.\n\nLine two.",
        language="EN",
        source_origin="synthetic_demo",
        created_at="2026-06-30",
        tags=[" Marketing ", " Course "],
    )

    normalized = normalize_item(item)

    assert normalized.source_type == "learning_note"
    assert normalized.title == "Sample Note"
    assert normalized.normalized_text == "Line one. Line two."
    assert normalized.language == "en"
    assert normalized.tags == ["marketing", "course"]
