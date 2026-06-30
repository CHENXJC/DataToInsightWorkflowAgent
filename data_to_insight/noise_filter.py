"""Noise filtering and route decision logic."""

from __future__ import annotations

from data_to_insight.schemas import ClassificationResult, RouteDecision, ScoreResult


def decide_route(classification: ClassificationResult, score: ScoreResult) -> RouteDecision:
    """Decide whether to keep, ignore, review, route, or convert an item."""

    category = classification.classification
    values = score.scores.values

    if category == "low_value_noise" or score.priority_level == "Noise":
        return RouteDecision(
            keep_or_ignore="ignore",
            recommended_route="None",
            reason="Low score or explicit noise category; not worth action in the main pipeline.",
        )

    if category == "duplicate_reference":
        return RouteDecision(
            keep_or_ignore="archive",
            recommended_route="None",
            reason="Duplicate reference should be archived or merged instead of treated as a new signal.",
        )

    if category == "needs_review" or values["evidence_strength"] <= 1:
        return RouteDecision(
            keep_or_ignore="review_later",
            recommended_route="DataToInsightWorkflowAgent",
            reason="Potentially useful but evidence or context is too weak for immediate action.",
        )

    if values["project_value"] >= 5 and values["strategic_fit"] >= 5:
        return RouteDecision(
            keep_or_ignore="convert_to_project",
            recommended_route="AgentHubControlCenter",
            reason="Strong project and strategic fit; convert into a project or AgentHub route.",
        )

    if category in {"project_asset", "ai_workflow_idea"}:
        return RouteDecision(
            keep_or_ignore="route_to_agent",
            recommended_route="AgentHubControlCenter",
            reason="Agent or project asset should be routed to the control center.",
        )

    return RouteDecision(
        keep_or_ignore="keep",
        recommended_route="DataToInsightWorkflowAgent",
        reason="Useful item with enough score and evidence to keep in the insight report.",
    )
