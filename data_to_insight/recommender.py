"""Recommend next actions for processed demo items."""

from __future__ import annotations

from data_to_insight.schemas import ActionRecommendation, ClassificationResult, RouteDecision, ScoreResult


ACTION_BY_CATEGORY = {
    "course_learning": ("save_to_knowledge_base", "PersonalKnowledgeAgent"),
    "business_signal": ("create_project_idea", "BusinessOpsAgent"),
    "market_signal": ("use_for_content_creation", "NewsSignalAgent"),
    "customer_pain": ("route_to_existing_agent", "SocialPainFinderAgent"),
    "operation_issue": ("route_to_existing_agent", "BusinessOpsAgent"),
    "project_asset": ("use_for_portfolio", "AgentHubControlCenter"),
    "career_asset": ("use_for_job_search", "CareerPilotAgent"),
    "ai_workflow_idea": ("create_project_idea", "DataToInsightWorkflowAgent"),
    "content_idea": ("use_for_content_creation", "DataToInsightWorkflowAgent"),
    "needs_review": ("review_later", "DataToInsightWorkflowAgent"),
    "duplicate_reference": ("review_later", "None"),
    "low_value_noise": ("ignore_as_noise", "None"),
}


NEXT_STEP_BY_ACTION = {
    "save_to_knowledge_base": "Save the structured note into a local knowledge base.",
    "route_to_existing_agent": "Route the signal to the most relevant existing agent.",
    "create_project_idea": "Turn this signal into a small project idea card.",
    "use_for_assignment": "Convert the note into assignment-ready arguments.",
    "use_for_portfolio": "Use the item as portfolio evidence or README case material.",
    "use_for_job_search": "Convert the item into resume, job matching, or interview prep material.",
    "use_for_content_creation": "Turn the signal into a content outline or public-safe example.",
    "generate_report": "Include the item in a Markdown insight report.",
    "enrich_with_more_data": "Collect more public-safe context before deciding.",
    "review_later": "Put the item into a review queue.",
    "ignore_as_noise": "Ignore this item in the main action workflow.",
}


def recommend_actions(
    classification: ClassificationResult,
    score: ScoreResult,
    route: RouteDecision,
) -> list[ActionRecommendation]:
    """Generate recommended actions for one scored item."""

    if route.keep_or_ignore == "ignore":
        action_type, target = "ignore_as_noise", "None"
    elif route.keep_or_ignore == "review_later":
        action_type, target = "review_later", "DataToInsightWorkflowAgent"
    elif route.keep_or_ignore == "convert_to_project":
        action_type, target = "create_project_idea", route.recommended_route
    else:
        action_type, target = ACTION_BY_CATEGORY[classification.classification]

    actions = [
        ActionRecommendation(
            action_type=action_type,
            target=target,
            priority=score.priority_level,
            reason=route.reason,
            next_step=NEXT_STEP_BY_ACTION[action_type],
        )
    ]

    if score.priority_level in {"High", "Medium"} and route.keep_or_ignore not in {"ignore", "review_later"}:
        actions.append(
            ActionRecommendation(
                action_type="generate_report",
                target="DataToInsightWorkflowAgent",
                priority=score.priority_level,
                reason="Useful enough to include in the demo insight report.",
                next_step=NEXT_STEP_BY_ACTION["generate_report"],
            )
        )

    return actions
