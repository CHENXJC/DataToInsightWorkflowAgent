"""Command line interface for the D2I demo pipeline."""

from __future__ import annotations

import argparse

from data_to_insight.config import DEFAULT_INPUT_PATH, DEFAULT_OUTPUT_DIR
from data_to_insight.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run DataToInsightWorkflowAgent demo pipeline.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo_parser = subparsers.add_parser("run-demo", help="Run the synthetic demo data pipeline.")
    demo_parser.add_argument("--input", default=DEFAULT_INPUT_PATH, help="Path to demo_items.json.")
    demo_parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run-demo":
        _processed_items, summary = run_pipeline(args.input, args.output_dir)
        print(f"Processed items: {summary.total_items_processed}")
        print(f"High-value signals: {summary.high_value_signals}")
        print(f"Medium-value items: {summary.medium_value_items}")
        print(f"Low/noise/review items: {summary.low_value_or_noise_items}")
        print(f"Recommended actions: {summary.recommended_actions_count}")
        print(f"Report path: {summary.latest_report_path}")
        print(f"AgentHub summary path: {summary.agenthub_summary_path}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
