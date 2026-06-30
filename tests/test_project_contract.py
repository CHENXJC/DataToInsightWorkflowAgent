import json
from pathlib import Path

from data_to_insight.config import ACTION_TYPES, CATEGORIES, SCORE_DIMENSIONS


ROOT = Path(__file__).resolve().parents[1]


def test_manifest_has_required_agenthub_fields():
    manifest = json.loads((ROOT / "agent_manifest.json").read_text(encoding="utf-8"))
    required = {
        "agent_id",
        "name",
        "display_name_zh",
        "category",
        "status",
        "version",
        "local_first",
        "public_safe",
        "demo_mode",
        "capabilities",
        "entrypoint",
        "docs",
        "report_path",
        "contract_path",
        "last_updated",
    }

    assert required.issubset(manifest)
    assert manifest["local_first"] is True
    assert manifest["public_safe"] is True
    assert manifest["demo_mode"] is True


def test_contract_has_required_schema_sections():
    contract = json.loads((ROOT / "agent_contract.json").read_text(encoding="utf-8"))

    for section in [
        "input_schema",
        "output_schema",
        "scoring_schema",
        "action_schema",
        "agenthub_summary_schema",
    ]:
        assert section in contract

    assert set(SCORE_DIMENSIONS).issubset(set(contract["scoring_schema"]["dimensions"]))
    assert set(ACTION_TYPES).issubset(set(contract["action_schema"]["action_types"]))


def test_taxonomy_includes_required_categories():
    required_categories = {
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
    }

    assert required_categories.issubset(set(CATEGORIES))


def test_public_safe_placeholder_files_exist():
    assert (ROOT / "outputs" / ".gitkeep").exists()
    assert (ROOT / "demo_data" / "README.md").exists()
