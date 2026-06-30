"""Public showcase pre-release checks for DataToInsightWorkflowAgent.

The check is intentionally conservative: it scans file names and known public
metadata only. It does not open sensitive-looking files.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "PROJECT_STATUS.md",
    "agent_manifest.json",
    "agent_contract.json",
    "app.py",
    "demo_data/demo_items.json",
    "docs/PUBLIC_RELEASE_CHECKLIST.md",
    "docs/SECURITY_AND_PRIVACY.md",
    "release/public_showcase_manifest.json",
]

REQUIRED_SCREENSHOTS = [
    "docs/screenshots/01_dashboard_hero.png",
    "docs/screenshots/02_overview_metrics.png",
    "docs/screenshots/03_workflow_map.png",
    "docs/screenshots/04_high_value_signals.png",
    "docs/screenshots/05_action_board.png",
    "docs/screenshots/06_noise_review_queue.png",
    "docs/screenshots/07_processed_items_table.png",
    "docs/screenshots/08_export_agenthub_panel.png",
    "docs/screenshots/09_agenthub_d2i_card.png",
]

REQUIRED_GITIGNORE_PATTERNS = [
    ".env",
    "token.json",
    "credentials.json",
    "outputs/*",
    ".venv/",
]

SENSITIVE_FILENAME_RE = re.compile(
    r"(^\.env$|\.env$|token|credential|secret|\.key$|\.pem$)",
    re.IGNORECASE,
)

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


@dataclass
class CheckResult:
    passed: list[str]
    warnings: list[str]
    failures: list[str]

    def pass_check(self, message: str) -> None:
        self.passed.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)


def iter_project_files(root: Path) -> Iterable[Path]:
    """Yield project files while skipping dependency, VCS, and cache folders."""

    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            yield path


def load_json(path: Path) -> tuple[dict | None, str | None]:
    """Load public metadata JSON."""

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except OSError as exc:
        return None, str(exc)
    except json.JSONDecodeError as exc:
        return None, f"{exc.msg} at line {exc.lineno}"
    if not isinstance(data, dict):
        return None, "JSON root is not an object"
    return data, None


def check_required_files(result: CheckResult) -> None:
    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path
        if path.is_file():
            result.pass_check(f"required file exists: {relative_path}")
        else:
            result.fail(f"missing required file: {relative_path}")


def check_sensitive_file_names(result: CheckResult) -> None:
    matches = []
    for path in iter_project_files(ROOT):
        if SENSITIVE_FILENAME_RE.search(path.name):
            matches.append(str(path.relative_to(ROOT)))
    if matches:
        for match in matches:
            result.warn(f"sensitive-looking file name found, content not read: {match}")
    else:
        result.pass_check("no sensitive-looking file names found")


def check_gitignore(result: CheckResult) -> None:
    gitignore_path = ROOT / ".gitignore"
    if not gitignore_path.is_file():
        result.fail(".gitignore is missing")
        return
    text = gitignore_path.read_text(encoding="utf-8")
    for pattern in REQUIRED_GITIGNORE_PATTERNS:
        if pattern in text:
            result.pass_check(f".gitignore contains {pattern}")
        else:
            result.fail(f".gitignore missing {pattern}")


def check_public_metadata(result: CheckResult) -> None:
    manifest, manifest_error = load_json(ROOT / "agent_manifest.json")
    if manifest_error:
        result.fail(f"agent_manifest.json invalid: {manifest_error}")
    else:
        result.pass_check("agent_manifest.json is parseable")
        if manifest and manifest.get("public_safe") is True and manifest.get("demo_mode") is True:
            result.pass_check("agent_manifest declares public_safe and demo_mode")
        else:
            result.fail("agent_manifest must declare public_safe=true and demo_mode=true")

    contract, contract_error = load_json(ROOT / "agent_contract.json")
    if contract_error:
        result.fail(f"agent_contract.json invalid: {contract_error}")
    else:
        result.pass_check("agent_contract.json is parseable")
        if contract and "agenthub_summary_schema" in contract:
            result.pass_check("agent_contract includes agenthub_summary_schema")
        else:
            result.fail("agent_contract missing agenthub_summary_schema")

    summary_path = ROOT / "outputs" / "agenthub_summary.json"
    if summary_path.exists():
        summary, summary_error = load_json(summary_path)
        if summary_error:
            result.fail(f"outputs/agenthub_summary.json invalid: {summary_error}")
        else:
            result.pass_check("outputs/agenthub_summary.json is parseable")
            if summary and summary.get("total_items_processed") == 14:
                result.pass_check("AgentHub summary contains expected demo item count")
            else:
                result.warn("AgentHub summary demo item count is not 14")
    else:
        result.warn("outputs/agenthub_summary.json is missing; run the CLI demo before release")


def check_release_manifest(result: CheckResult) -> None:
    release_manifest, error = load_json(ROOT / "release" / "public_showcase_manifest.json")
    if error:
        result.fail(f"release/public_showcase_manifest.json invalid: {error}")
        return

    assert release_manifest is not None
    expected_true = [
        "local_first",
        "public_safe",
        "demo_mode",
        "synthetic_demo_data_only",
        "agenthub_ready",
    ]
    for field in expected_true:
        if release_manifest.get(field) is True:
            result.pass_check(f"release manifest {field}=true")
        else:
            result.fail(f"release manifest {field} must be true")

    push_status = release_manifest.get("github_push_status")
    release_ready = release_manifest.get("public_release_ready")
    if push_status == "not_executed" and release_ready is False:
        result.pass_check("release manifest is in pre-push mode")
    elif push_status == "pushed" and release_ready is True:
        result.pass_check("release manifest is in pushed public-release mode")
        if release_manifest.get("github_repo"):
            result.pass_check("release manifest includes github_repo")
        else:
            result.fail("github_repo is required after push")
    else:
        result.fail("public_release_ready and github_push_status are inconsistent")

    if release_manifest.get("screenshots_status") == "captured":
        result.pass_check("screenshots_status is captured")
    else:
        result.fail("screenshots_status must be captured after D2I-006")

    if release_manifest.get("screenshots_count") == len(REQUIRED_SCREENSHOTS):
        result.pass_check("screenshots_count matches required screenshot set")
    else:
        result.fail("screenshots_count must be 9 after D2I-006")


def check_screenshots(result: CheckResult) -> None:
    png_signature = b"\x89PNG\r\n\x1a\n"
    for relative_path in REQUIRED_SCREENSHOTS:
        path = ROOT / relative_path
        if not path.is_file():
            result.fail(f"missing screenshot: {relative_path}")
            continue
        if path.stat().st_size <= len(png_signature):
            result.fail(f"screenshot is empty or too small: {relative_path}")
            continue
        with path.open("rb") as screenshot_file:
            signature = screenshot_file.read(len(png_signature))
        if signature == png_signature:
            result.pass_check(f"screenshot PNG signature ok: {relative_path}")
        else:
            result.fail(f"screenshot is not a PNG file: {relative_path}")


def check_readme_public_surface(result: CheckResult) -> None:
    readme_path = ROOT / "README.md"
    if not readme_path.is_file():
        return
    text = readme_path.read_text(encoding="utf-8")
    release_manifest, release_error = load_json(ROOT / "release" / "public_showcase_manifest.json")
    checkpoint = ""
    if not release_error and release_manifest:
        checkpoint = str(release_manifest.get("checkpoint", "") or "")

    required_phrases = [
        "local-first",
        "public-safe",
        "demo-mode",
        "synthetic demo data",
        "AgentHub",
    ]
    if checkpoint:
        required_phrases.append(checkpoint)
    for phrase in required_phrases:
        if phrase in text:
            result.pass_check(f"README contains {phrase}")
        else:
            result.fail(f"README missing {phrase}")

    if "F:\\AIProjects" in text:
        result.warn("README contains local absolute Windows project path")
    else:
        result.pass_check("README avoids local absolute Windows project paths")


def run_checks() -> CheckResult:
    result = CheckResult(passed=[], warnings=[], failures=[])
    check_required_files(result)
    check_sensitive_file_names(result)
    check_gitignore(result)
    check_public_metadata(result)
    check_release_manifest(result)
    check_screenshots(result)
    check_readme_public_surface(result)
    return result


def print_summary(result: CheckResult) -> None:
    status = "FAIL" if result.failures else "WARNING" if result.warnings else "PASS"
    print(f"PUBLIC_RELEASE_CHECK_STATUS={status}")
    print(f"PASS_COUNT={len(result.passed)}")
    print(f"WARNING_COUNT={len(result.warnings)}")
    print(f"FAIL_COUNT={len(result.failures)}")

    for message in result.passed:
        print(f"PASS: {message}")
    for message in result.warnings:
        print(f"WARNING: {message}")
    for message in result.failures:
        print(f"FAIL: {message}")


def main() -> int:
    result = run_checks()
    print_summary(result)
    return 1 if result.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
