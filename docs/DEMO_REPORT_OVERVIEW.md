# Demo Report Overview

Checkpoint: `D2I-006-SCREENSHOT-CAPTURE-AND-README-SCREENSHOT-UPDATE-COMPLETE`

The demo pipeline uses only `demo_data/demo_items.json`, which contains public-safe synthetic examples.

## Latest Demo Metrics

| Metric | Value |
| --- | ---: |
| Total items processed | 14 |
| High-value signals | 4 |
| Medium-value items | 5 |
| Low/noise/review items | 5 |
| Recommended actions | 23 |

## Top Routes

- `DataToInsightWorkflowAgent`: 9
- `AgentHubControlCenter`: 2
- `None`: 3

`None` means the item is noise or does not need routing to another agent.

## Output Paths

- Markdown report: `outputs/demo_insight_report.md`
- AgentHub summary JSON: `outputs/agenthub_summary.json`

## Public-Safe Note

This document intentionally summarizes the report instead of copying large sections from `outputs/`. Generated outputs remain ignored by default and should be manually reviewed before any public release.
