# Development Roadmap

## D2I-001

Project planning, workflow map, scoring framework, AgentHub contract.

Status: complete.

Deliverables:

- README
- PROJECT_STATUS
- Docs
- AgentHub manifest / contract
- Minimal Python package skeleton
- Public-safe project structure

## D2I-002

Demo data pipeline MVP.

Status: complete.

Scope:

```text
读取 synthetic demo data
-> 标准化
-> 分类
-> 评分
-> 噪音过滤
-> 洞察提取
-> 行动建议
-> Markdown / JSON export
```

Recommended deliverables:

- `demo_data/demo_items.json`
- `data_to_insight/loader.py`
- `data_to_insight/classifier.py`
- `data_to_insight/scorer.py`
- `data_to_insight/recommender.py`
- `data_to_insight/exporter.py`
- focused tests
- sample public-safe demo report

Implemented deliverables:

- `demo_data/demo_items.json`
- `data_to_insight/intake.py`
- `data_to_insight/normalizer.py`
- `data_to_insight/classifier.py`
- `data_to_insight/scorer.py`
- `data_to_insight/noise_filter.py`
- `data_to_insight/insight_extractor.py`
- `data_to_insight/recommender.py`
- `data_to_insight/report_builder.py`
- `data_to_insight/agenthub_exporter.py`
- `data_to_insight/pipeline.py`
- `data_to_insight/cli.py`
- focused tests
- `outputs/demo_insight_report.md`
- `outputs/agenthub_summary.json`

## D2I-003

Streamlit dashboard.

Status: complete.

Views:

- Overview
- Data Intake
- Classification
- Insight Signals
- Action Board
- Export

Implemented views:

- Hero / project header
- Sidebar controls
- Overview metrics
- Workflow map
- High-value signals
- Action board
- Noise / review queue
- Processed items table
- Export / AgentHub panel
- Public-safe notice

Boundary:

- Use synthetic demo data only.
- Do not connect real external services.

## D2I-004

AgentHubControlCenter integration.

Goal:

让 AgentHub 读取 manifest、contract 和 demo report，并在总控台显示状态、能力、public-safe 状态、high-value signals、recommended actions 和 route targets。

## D2I-005

Public showcase preparation.

Scope:

- README polish
- screenshots guide
- demo report
- safety check
- GitHub public release preparation

Boundary:

- Do not publish until user explicitly asks.
- Do not push automatically.
