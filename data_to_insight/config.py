"""Project constants for DataToInsightWorkflowAgent."""

PACKAGE_NAME = "DataToInsightWorkflowAgent"
VERSION = "0.7.0"
AGENT_ID = "data_to_insight_workflow_agent"
STATUS = "D2I-007-FINAL-PUBLIC-RELEASE-CHECK-AND-GITHUB-RELEASE-COMPLETE"
DEFAULT_INPUT_PATH = "demo_data/demo_items.json"
DEFAULT_OUTPUT_DIR = "outputs"
DEMO_REPORT_NAME = "demo_insight_report.md"
AGENTHUB_SUMMARY_NAME = "agenthub_summary.json"

CATEGORIES = [
    "course_learning",
    "business_signal",
    "project_asset",
    "career_asset",
    "market_signal",
    "customer_pain",
    "operation_issue",
    "content_idea",
    "ai_workflow_idea",
    "low_value_noise",
    "duplicate_reference",
    "needs_review",
]

SCORE_DIMENSIONS = [
    "learning_value",
    "business_value",
    "project_value",
    "portfolio_value",
    "career_value",
    "content_value",
    "actionability",
    "novelty",
    "evidence_strength",
    "reuse_potential",
    "urgency",
    "strategic_fit",
]

PRIORITY_LEVELS = [
    "High",
    "Medium",
    "Low",
    "Noise",
    "Needs Review",
]

ACTION_TYPES = [
    "save_to_knowledge_base",
    "route_to_existing_agent",
    "create_project_idea",
    "use_for_assignment",
    "use_for_portfolio",
    "use_for_job_search",
    "use_for_content_creation",
    "generate_report",
    "enrich_with_more_data",
    "review_later",
    "ignore_as_noise",
]

ROUTE_DECISIONS = [
    "keep",
    "archive",
    "ignore",
    "review_later",
    "route_to_agent",
    "convert_to_project",
]

ROUTE_TARGETS = [
    "PersonalKnowledgeAgent",
    "AgentHubControlCenter",
    "SocialPainFinderAgent",
    "BusinessOpsAgent",
    "CareerPilotAgent",
    "NewsSignalAgent",
    "VideoExtractSkill",
    "DataToInsightWorkflowAgent",
    "None",
]
