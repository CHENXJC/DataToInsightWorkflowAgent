"""Schemas for the D2I synthetic demo pipeline."""

from dataclasses import dataclass, field

from data_to_insight.config import SCORE_DIMENSIONS


@dataclass(frozen=True)
class RawDemoItem:
    """Public-safe synthetic input item loaded from demo_data."""

    item_id: str
    source_type: str
    title: str
    raw_text: str
    language: str
    source_origin: str
    created_at: str
    tags: list[str]
    sensitivity_level: str = "public_safe"
    synthetic: bool = True


@dataclass(frozen=True)
class NormalizedItem:
    """Normalized record used by downstream pipeline steps."""

    item_id: str
    source_type: str
    title: str
    normalized_text: str
    language: str
    source_origin: str
    created_at: str
    tags: list[str]
    sensitivity_level: str
    synthetic: bool = True


@dataclass(frozen=True)
class ClassificationResult:
    """Rule-based classification result."""

    classification: str
    confidence: float
    matched_rules: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ScoreBreakdown:
    """Multi-dimensional score container using the 0-5 D2I scale."""

    values: dict[str, int] = field(default_factory=dict)

    def validate_dimensions(self) -> bool:
        return set(self.values).issubset(set(SCORE_DIMENSIONS))


@dataclass(frozen=True)
class ScoreResult:
    """Scoring result with an overall priority label."""

    scores: ScoreBreakdown
    overall_score: float
    priority_level: str


@dataclass(frozen=True)
class RouteDecision:
    """Noise-filtering and route decision."""

    keep_or_ignore: str
    recommended_route: str
    reason: str


@dataclass(frozen=True)
class KeySignal:
    """Actionable signal extracted from an item."""

    signal: str
    why_it_matters: str
    evidence: str
    possible_use: str


@dataclass(frozen=True)
class ActionRecommendation:
    """Recommended next action for a scored insight signal."""

    action_type: str
    target: str
    priority: str
    reason: str
    next_step: str


@dataclass(frozen=True)
class ProcessedInsightItem:
    """End-to-end processed output for one demo item."""

    item_id: str
    source_type: str
    title: str
    normalized_text: str
    category: str
    classification: str
    scores: dict[str, int]
    overall_score: float
    priority_level: str
    keep_or_ignore: str
    key_signals: list[KeySignal]
    recommended_actions: list[ActionRecommendation]
    recommended_route: str
    reason: str


@dataclass(frozen=True)
class InsightSignal:
    """Backward-compatible single insight shape for AgentHub planning."""

    item_id: str
    category: str
    scores: ScoreBreakdown
    overall_score: float
    priority_level: str
    insight_signal: str
    recommended_action: ActionRecommendation
    keep_or_ignore: str
    reason: str


@dataclass(frozen=True)
class AgentHubSummary:
    """Summary object reserved for AgentHubControlCenter integration."""

    agent_name: str
    status: str
    capabilities: list[str]
    demo_mode: bool
    public_safe: bool
    latest_report_path: str
    high_value_signal_count: int
    recommended_action_count: int
    route_targets: list[str]


@dataclass(frozen=True)
class PipelineSummary:
    """Aggregated pipeline output summary."""

    total_items_processed: int
    high_value_signals: int
    medium_value_items: int
    low_value_or_noise_items: int
    recommended_actions_count: int
    top_routes: dict[str, int]
    latest_report_path: str
    agenthub_summary_path: str
    generated_at: str


# Backward-compatible alias from D2I-001.
DemoItem = RawDemoItem
