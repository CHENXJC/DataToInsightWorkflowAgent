# AgentHub Integration Contract

## 目标

DataToInsightWorkflowAgent 需要预留 AgentHubControlCenter 可读取的标准化契约，让未来总控台可以显示该 Agent 的状态、能力、安全模式和最近输出摘要。

## Files

- `agent_manifest.json`
- `agent_contract.json`

## agent_manifest.json

Manifest 用于描述 Agent 本身：

- `agent_id`
- `name`
- `display_name_zh`
- `category`
- `status`
- `version`
- `local_first`
- `public_safe`
- `demo_mode`
- `capabilities`
- `entrypoint`
- `docs`
- `report_path`
- `contract_path`
- `last_updated`

## agent_contract.json

Contract 用于描述输入、输出、评分、行动建议和 AgentHub summary：

- `input_schema`
- `output_schema`
- `scoring_schema`
- `action_schema`
- `agenthub_summary_schema`

## AgentHub Summary Fields

未来 AgentHubControlCenter 应该可以读取并展示：

- Agent 名称
- 当前状态
- 能力列表
- 是否 demo mode
- 是否 public-safe
- 最近报告路径
- 高价值信号数量
- 推荐行动数量
- 可路由目标 Agent

## Integration Stage

D2I-001 只完成 contract planning。

D2I-004 才进行 AgentHubControlCenter runtime integration。

## Safety Boundary

AgentHub 读取 manifest / contract 时，不应该读取 `.env`、token、credential、secret，也不应该扫描 demo_data/private 或 outputs 里的非公开生成物。
