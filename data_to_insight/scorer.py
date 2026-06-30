"""Multi-dimensional value scoring for demo items."""

from __future__ import annotations

from data_to_insight.config import SCORE_DIMENSIONS
from data_to_insight.schemas import ClassificationResult, NormalizedItem, ScoreBreakdown, ScoreResult


BASE_SCORES: dict[str, dict[str, int]] = {
    "course_learning": {
        "learning_value": 5,
        "business_value": 2,
        "project_value": 2,
        "portfolio_value": 2,
        "career_value": 3,
        "content_value": 3,
        "actionability": 3,
        "novelty": 2,
        "evidence_strength": 3,
        "reuse_potential": 4,
        "urgency": 2,
        "strategic_fit": 3,
    },
    "business_signal": {
        "learning_value": 3,
        "business_value": 5,
        "project_value": 4,
        "portfolio_value": 4,
        "career_value": 2,
        "content_value": 4,
        "actionability": 4,
        "novelty": 3,
        "evidence_strength": 3,
        "reuse_potential": 4,
        "urgency": 3,
        "strategic_fit": 4,
    },
    "market_signal": {
        "learning_value": 3,
        "business_value": 4,
        "project_value": 3,
        "portfolio_value": 3,
        "career_value": 2,
        "content_value": 4,
        "actionability": 3,
        "novelty": 3,
        "evidence_strength": 3,
        "reuse_potential": 3,
        "urgency": 3,
        "strategic_fit": 4,
    },
    "customer_pain": {
        "learning_value": 3,
        "business_value": 5,
        "project_value": 4,
        "portfolio_value": 4,
        "career_value": 2,
        "content_value": 4,
        "actionability": 5,
        "novelty": 3,
        "evidence_strength": 4,
        "reuse_potential": 4,
        "urgency": 4,
        "strategic_fit": 5,
    },
    "operation_issue": {
        "learning_value": 3,
        "business_value": 5,
        "project_value": 4,
        "portfolio_value": 4,
        "career_value": 2,
        "content_value": 3,
        "actionability": 5,
        "novelty": 3,
        "evidence_strength": 4,
        "reuse_potential": 4,
        "urgency": 4,
        "strategic_fit": 5,
    },
    "project_asset": {
        "learning_value": 3,
        "business_value": 4,
        "project_value": 5,
        "portfolio_value": 5,
        "career_value": 4,
        "content_value": 4,
        "actionability": 4,
        "novelty": 3,
        "evidence_strength": 4,
        "reuse_potential": 5,
        "urgency": 3,
        "strategic_fit": 5,
    },
    "career_asset": {
        "learning_value": 3,
        "business_value": 2,
        "project_value": 2,
        "portfolio_value": 3,
        "career_value": 5,
        "content_value": 2,
        "actionability": 4,
        "novelty": 2,
        "evidence_strength": 3,
        "reuse_potential": 3,
        "urgency": 4,
        "strategic_fit": 4,
    },
    "ai_workflow_idea": {
        "learning_value": 3,
        "business_value": 4,
        "project_value": 5,
        "portfolio_value": 4,
        "career_value": 3,
        "content_value": 4,
        "actionability": 3,
        "novelty": 4,
        "evidence_strength": 2,
        "reuse_potential": 5,
        "urgency": 3,
        "strategic_fit": 5,
    },
    "content_idea": {
        "learning_value": 2,
        "business_value": 3,
        "project_value": 2,
        "portfolio_value": 3,
        "career_value": 2,
        "content_value": 5,
        "actionability": 3,
        "novelty": 3,
        "evidence_strength": 2,
        "reuse_potential": 3,
        "urgency": 2,
        "strategic_fit": 3,
    },
    "needs_review": {
        "learning_value": 2,
        "business_value": 2,
        "project_value": 2,
        "portfolio_value": 1,
        "career_value": 1,
        "content_value": 2,
        "actionability": 1,
        "novelty": 3,
        "evidence_strength": 1,
        "reuse_potential": 2,
        "urgency": 1,
        "strategic_fit": 2,
    },
    "duplicate_reference": {
        "learning_value": 1,
        "business_value": 1,
        "project_value": 1,
        "portfolio_value": 1,
        "career_value": 1,
        "content_value": 1,
        "actionability": 1,
        "novelty": 0,
        "evidence_strength": 1,
        "reuse_potential": 1,
        "urgency": 0,
        "strategic_fit": 1,
    },
    "low_value_noise": {
        "learning_value": 0,
        "business_value": 0,
        "project_value": 0,
        "portfolio_value": 0,
        "career_value": 0,
        "content_value": 1,
        "actionability": 0,
        "novelty": 0,
        "evidence_strength": 0,
        "reuse_potential": 0,
        "urgency": 0,
        "strategic_fit": 0,
    },
}


def clamp_score(value: int) -> int:
    """Keep a score inside the required 0-5 range."""

    return max(0, min(5, value))


def score_item(item: NormalizedItem, classification: ClassificationResult) -> ScoreResult:
    """Score one item across the D2I dimensions."""

    scores = BASE_SCORES[classification.classification].copy()
    searchable = f"{item.title} {item.normalized_text} {' '.join(item.tags)}".lower()

    if "portfolio" in searchable or "github" in searchable:
        scores["portfolio_value"] = clamp_score(scores["portfolio_value"] + 1)
    if "automation" in searchable or "workflow" in searchable:
        scores["business_value"] = clamp_score(scores["business_value"] + 1)
        scores["strategic_fit"] = clamp_score(scores["strategic_fit"] + 1)
    if "no evidence" in searchable or "not enough context" in searchable:
        scores["evidence_strength"] = clamp_score(scores["evidence_strength"] - 2)
        scores["actionability"] = clamp_score(scores["actionability"] - 1)

    ordered_scores = {dimension: clamp_score(scores.get(dimension, 0)) for dimension in SCORE_DIMENSIONS}
    overall_score = round(sum(ordered_scores.values()) / len(SCORE_DIMENSIONS), 2)

    if classification.classification == "needs_review":
        priority = "Needs Review"
    elif overall_score >= 4.0:
        priority = "High"
    elif overall_score >= 3.0:
        priority = "Medium"
    elif overall_score >= 2.0:
        priority = "Low"
    else:
        priority = "Noise"

    return ScoreResult(
        scores=ScoreBreakdown(ordered_scores),
        overall_score=overall_score,
        priority_level=priority,
    )
