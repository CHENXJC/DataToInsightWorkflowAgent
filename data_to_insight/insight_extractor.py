"""Extract actionable signals from classified and scored demo items."""

from __future__ import annotations

from data_to_insight.schemas import ClassificationResult, KeySignal, NormalizedItem, ScoreResult


SIGNAL_TEMPLATES = {
    "course_learning": (
        "Learning material can be turned into structured study or assignment-ready arguments.",
        "It helps convert messy course notes into reusable knowledge assets.",
        "PersonalKnowledgeAgent / assignment support / study brief",
    ),
    "business_signal": (
        "Business review patterns point to service and workflow improvement opportunities.",
        "Repeated market friction can become a consulting offer or automation workflow.",
        "BusinessOpsAgent / content idea / service offer research",
    ),
    "market_signal": (
        "Market feedback reveals demand patterns that can inform positioning and content.",
        "Public-safe review themes can support business opportunity scoring.",
        "NewsSignalAgent / SocialPainFinderAgent / content pipeline",
    ),
    "customer_pain": (
        "Customer pain indicates repeated manual work that may be automated.",
        "Clear pain points are useful for SME workflow consulting and project ideation.",
        "SocialPainFinderAgent / BusinessOpsAgent / project backlog",
    ),
    "operation_issue": (
        "Operational friction suggests a workflow automation opportunity.",
        "Repeated coordination issues can become a practical local-first tool or service.",
        "BusinessOpsAgent / AgentHubControlCenter / automation plan",
    ),
    "project_asset": (
        "Project output can be reused as portfolio evidence and AgentHub-ready context.",
        "Reusable project assets strengthen GitHub showcase and cross-agent routing.",
        "AgentHubControlCenter / portfolio pipeline / README case",
    ),
    "career_asset": (
        "Career material can be converted into job-search actions and portfolio positioning.",
        "It helps connect projects to employable skills and interview evidence.",
        "CareerPilotAgent / resume update / interview prep",
    ),
    "ai_workflow_idea": (
        "AI workflow idea may become a reusable agent or automation pattern.",
        "It can expand the portfolio if evidence and target user are clarified.",
        "DataToInsightWorkflowAgent / AgentHubControlCenter / project backlog",
    ),
    "content_idea": (
        "Content idea can become a public-safe explanation or case study.",
        "It supports portfolio storytelling and market education.",
        "Content pipeline / README case / article outline",
    ),
    "needs_review": (
        "Potential signal needs more context before it becomes actionable.",
        "Weak evidence should not be over-promoted in a public demo report.",
        "Review queue / enrichment task",
    ),
    "duplicate_reference": (
        "Duplicate reference should be merged rather than treated as a fresh signal.",
        "Deduplication keeps the workflow focused on new value.",
        "Archive / merge reference",
    ),
    "low_value_noise": (
        "Low-value item should be filtered out of the main action board.",
        "Filtering noise shows the agent can reduce information overload.",
        "Ignore / archive",
    ),
}


def extract_key_signals(
    item: NormalizedItem,
    classification: ClassificationResult,
    score: ScoreResult,
) -> list[KeySignal]:
    """Create one concise key signal for a processed item."""

    category = classification.classification
    signal, why_it_matters, possible_use = SIGNAL_TEMPLATES[category]
    evidence = item.normalized_text[:180]
    if len(item.normalized_text) > 180:
        evidence += "..."

    return [
        KeySignal(
            signal=signal,
            why_it_matters=f"{why_it_matters} Priority: {score.priority_level}.",
            evidence=evidence,
            possible_use=possible_use,
        )
    ]
