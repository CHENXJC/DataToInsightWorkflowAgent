# AgentHub Handoff

## Purpose

This document explains how AgentHubControlCenter should read and display DataToInsightWorkflowAgent during `D2I-004-AGENTHUB-CONTROLCENTER-INTEGRATION`.

## Files AgentHub Should Read

| File | Purpose |
| --- | --- |
| `agent_manifest.json` | Agent identity, Chinese display name, category, capabilities, safety flags, entrypoints, and local paths. |
| `agent_contract.json` | Input/output/action/scoring/AgentHub summary schema contract. |
| `outputs/agenthub_summary.json` | Latest public-safe demo pipeline metrics and route summary. |
| `outputs/demo_insight_report.md` | Latest Markdown demo insight report for manual review. |

## D2I Summary Fields

`outputs/agenthub_summary.json` provides:

- `agent_id`
- `agent_name`
- `status`
- `demo_mode`
- `public_safe`
- `total_items_processed`
- `high_value_signals`
- `medium_value_items`
- `low_value_or_noise_items`
- `recommended_actions_count`
- `top_routes`
- `latest_report_path`
- `capabilities`
- `generated_at`

## Dashboard

Manual launch command:

```powershell
cd F:\AIProjects\DataToInsightWorkflowAgent
python -m streamlit run app.py
```

## Report Paths

- Markdown report: `outputs/demo_insight_report.md`
- AgentHub summary JSON: `outputs/agenthub_summary.json`

## Public-safe Status

- Local-first: yes
- Public-safe: yes
- Demo-mode: yes
- Real connector: no
- External API call: no
- Secret required: no
- Real user file processing: no

## Current Checkpoint

`D2I-004-AGENTHUB-CONTROLCENTER-INTEGRATION-COMPLETE`
