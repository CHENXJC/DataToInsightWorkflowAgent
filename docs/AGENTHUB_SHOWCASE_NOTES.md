# AgentHub Showcase Notes

Checkpoint: `D2I-007-FINAL-PUBLIC-RELEASE-CHECK-AND-GITHUB-RELEASE-COMPLETE`

DataToInsightWorkflowAgent is AgentHub-ready through local manifest and summary files. AgentHubControlCenter reads these files as metadata and does not execute D2I actions automatically.

## Files Read By AgentHub

| File | Purpose |
| --- | --- |
| `agent_manifest.json` | Agent identity, category, status, capabilities, safety flags, dashboard path, report path, and summary path |
| `agent_contract.json` | Input, output, scoring, action, and AgentHub summary contract |
| `outputs/agenthub_summary.json` | Latest synthetic demo summary metrics and route counts |
| `docs/AGENTHUB_HANDOFF.md` | Human-readable handoff guide |

## Current AgentHub Status

- Registered status: verified locally
- Summary read status: verified locally
- Dashboard path: `app.py`
- Markdown report path: `outputs/demo_insight_report.md`
- AgentHub summary path: `outputs/agenthub_summary.json`
- Public-safe status: enabled
- Demo-mode status: enabled
- Local-first status: enabled

## Displayed Fields

AgentHubControlCenter displays:

- Agent name
- Chinese name
- Category
- Status and checkpoint
- Local-first / public-safe / demo-mode / safe-mode flags
- Capabilities
- Dashboard path
- Markdown report path
- AgentHub summary path
- Total items processed
- High-value signals
- Medium-value items
- Low/noise/review items
- Recommended actions
- Top routes
- Latest report path

## Capabilities

- data_intake
- normalization
- classification
- value_scoring
- noise_filtering
- insight_extraction
- action_recommendation
- report_export
- streamlit_dashboard
- agenthub_export
