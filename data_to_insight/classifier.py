"""Rule-based demo classifier."""

from __future__ import annotations

from data_to_insight.config import CATEGORIES
from data_to_insight.schemas import ClassificationResult, NormalizedItem


KEYWORD_RULES: list[tuple[str, str, list[str]]] = [
    ("low_value_noise", "noise_or_duplicate", ["low_value_noise", "generic quote", "no evidence"]),
    ("duplicate_reference", "duplicate_reference", ["repeated", "duplicate", "same reference"]),
    ("needs_review", "needs_review", ["needs_review", "unclear", "not enough context", "maybe"]),
    ("customer_pain", "customer_pain", ["customer_pain", "staff waste time", "manual", "pain", "feedback"]),
    ("operation_issue", "operation_issue", ["operation_issue", "restaurant", "stock", "shift", "supplier", "delays"]),
    ("career_asset", "career_asset", ["resume", "job_description", "interview", "career", "job search"]),
    ("project_asset", "project_asset", ["videoextractskill", "agenthub", "businessopsagent", "portfolio", "project_asset"]),
    ("ai_workflow_idea", "ai_workflow_idea", ["ai workflow", "agent", "automation workflow"]),
    ("business_signal", "business_signal", ["business_signal", "pricing", "booking", "service business", "automation consulting"]),
    ("market_signal", "market_signal", ["market_signal", "reviews", "demand", "market"]),
    ("content_idea", "content_idea", ["content", "article", "topic", "video idea"]),
    ("course_learning", "course_learning", ["marketing", "consumer", "microeconomics", "assignment", "course", "learning"]),
]


def classify_item(item: NormalizedItem) -> ClassificationResult:
    """Classify one normalized item using source, title, tags, and text."""

    searchable = " ".join(
        [
            item.source_type,
            item.title.lower(),
            item.normalized_text.lower(),
            " ".join(item.tags),
        ]
    )

    matched: list[str] = []
    for category, rule_name, keywords in KEYWORD_RULES:
        if any(keyword in searchable for keyword in keywords):
            matched.append(rule_name)
            if category in CATEGORIES:
                return ClassificationResult(
                    classification=category,
                    confidence=0.86 if len(matched) == 1 else 0.92,
                    matched_rules=matched,
                )

    return ClassificationResult(
        classification="needs_review",
        confidence=0.45,
        matched_rules=["fallback_needs_review"],
    )


def classify_items(items: list[NormalizedItem]) -> list[ClassificationResult]:
    """Classify a list of normalized items."""

    return [classify_item(item) for item in items]
