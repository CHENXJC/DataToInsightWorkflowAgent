# Screenshots Guide

Checkpoint: `D2I-006-SCREENSHOT-CAPTURE-AND-README-SCREENSHOT-UPDATE-COMPLETE`

This guide defines the public-safe screenshot set for the GitHub showcase. Do not create fake screenshots. Capture these images only from the local Streamlit dashboard and AgentHubControlCenter after running the demo pipeline with synthetic data.

## Safety Rules

- Use synthetic demo data only.
- Do not show real customer files, personal notes, private reports, API keys, tokens, credentials, or `.env` files.
- Do not capture local folders that expose private files.
- Keep screenshots focused on the product UI and public-safe demo output.
- Store screenshots under `docs/screenshots/` only after manual capture.

## Required Screenshots

| No. | File | Page source | Screenshot content | Capability shown | Public-safe | Capture status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `docs/screenshots/01_dashboard_hero.png` | D2I Dashboard | Project header, status badges, local-first/demo-mode notice | Product positioning and safety boundary | Yes | Captured |
| 2 | `docs/screenshots/02_overview_metrics.png` | D2I Dashboard | Total items, high-value signals, medium items, review/noise items, actions | Metric summarization | Yes | Captured |
| 3 | `docs/screenshots/03_workflow_map.png` | D2I Dashboard | Input -> normalize -> classify -> score -> filter -> recommend -> export | End-to-end workflow design | Yes | Captured |
| 4 | `docs/screenshots/04_high_value_signals.png` | D2I Dashboard | Top public-safe demo signals and reasons | Insight extraction and priority scoring | Yes | Captured |
| 5 | `docs/screenshots/05_action_board.png` | D2I Dashboard | Recommended actions, priorities, targets, next steps | Action recommendation workflow | Yes | Captured |
| 6 | `docs/screenshots/06_noise_review_queue.png` | D2I Dashboard | Items marked noise or needs review | Noise filtering and safe uncertainty handling | Yes | Captured |
| 7 | `docs/screenshots/07_processed_items_table.png` | D2I Dashboard | Filterable processed items table | Structured output and auditability | Yes | Captured |
| 8 | `docs/screenshots/08_export_agenthub_panel.png` | D2I Dashboard | Markdown report path, AgentHub summary path, capability list | Export readiness and AgentHub handoff | Yes | Captured |
| 9 | `docs/screenshots/09_agenthub_d2i_card.png` | AgentHubControlCenter | D2I card in the local AgentHub registry view | Cross-agent registry integration | Yes | Captured |

## Capture Commands

Run the D2I dashboard:

```powershell
python -m streamlit run app.py --server.headless true --server.port 8523
```

Run AgentHubControlCenter separately when capturing screenshot 9:

```powershell
python -m streamlit run app.py --server.headless true --server.port 8524
```

## Capture Notes

All 9 screenshots were captured from real local Streamlit pages in D2I-006. The AgentHub screenshot is cropped to the main content area to avoid exposing unnecessary local sidebar path details.
