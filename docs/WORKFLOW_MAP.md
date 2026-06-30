# Workflow Map

DataToInsightWorkflowAgent 的核心工作流是：

```text
Data Intake
-> Data Normalization
-> Content Classification
-> Value Scoring
-> Noise Filtering
-> Insight Extraction
-> Action Recommendation
-> Report / AgentHub Export
```

## 1. Data Intake 数据进入

- 输入：synthetic demo notes、课程笔记摘要、项目输出摘要、业务反馈摘要、求职材料摘要。
- 处理逻辑：读取公开安全的 demo item，不读取真实隐私文件、不连接真实外部服务。
- 输出：raw demo records。
- 用户价值：把分散资料先放进统一入口，为后续分类和评分做准备。
- 后续实现：D2I-002 使用本地 JSON / CSV demo file，字段保持简单。

## 2. Data Normalization 数据标准化

- 输入：raw demo records。
- 处理逻辑：统一字段名称、source type、title、summary、context、created_at、synthetic flag。
- 输出：normalized records。
- 用户价值：减少后续处理混乱，让不同来源的资料可以进入同一套 workflow。
- 后续实现：用 Python dataclass 或 TypedDict 做基础 schema 校验。

## 3. Content Classification 内容分类

- 输入：normalized records。
- 处理逻辑：按照 category taxonomy 判断资料属于学习、商业、项目、求职、市场、用户痛点、运营问题、内容选题、AI workflow 想法、噪音、重复参考或需要人工复核。
- 输出：classified records。
- 用户价值：用户可以快速知道资料属于哪类资产，避免所有内容混在一起。
- 后续实现：先用 rule-based keyword mapping，再预留 LLM 分类接口但不在 D2I-001 接入。

## 4. Value Scoring 价值评分

- 输入：classified records。
- 处理逻辑：按 learning_value、business_value、project_value、portfolio_value、career_value、content_value、actionability、novelty、evidence_strength、reuse_potential、urgency、strategic_fit 进行 0-5 分评分。
- 输出：scored records with overall_score。
- 用户价值：把“看起来有用”变成可比较的优先级，帮助用户决定先处理什么。
- 后续实现：D2I-002 先用规则权重，后续再考虑可配置 scoring profile。

## 5. Noise Filtering 噪音过滤

- 输入：scored records。
- 处理逻辑：根据 overall_score、priority_level、duplicate flag、evidence strength 和 category 判断 keep_or_ignore。
- 输出：kept signals、noise items、needs_review items。
- 用户价值：减少信息过载，把低价值、重复和不确定内容从主视图里分离。
- 后续实现：先输出明确 reason，避免黑箱过滤。

## 6. Insight Extraction 洞察提取

- 输入：kept signals 和 needs_review items。
- 处理逻辑：提炼 one-line insight、evidence snippet、opportunity angle、risk note。
- 输出：insight signals。
- 用户价值：用户不只是看到摘要，而是看到可以用于学习、项目、求职、内容或商业判断的洞察。
- 后续实现：先使用模板化规则生成简短 insight，后续可接 LLM 但默认 demo mode。

## 7. Action Recommendation 行动建议

- 输入：insight signals。
- 处理逻辑：根据 category、priority_level、score profile 和 user direction 推荐下一步动作。
- 输出：action recommendations。
- 用户价值：把洞察转化成行动，例如保存到知识库、路由到已有 Agent、生成报告、变成项目想法或暂时忽略。
- 后续实现：D2I-002 实现 action type mapping 和解释字段。

## 8. Report / AgentHub Export 报告与总控输出

- 输入：insight signals、action recommendations、summary metrics。
- 处理逻辑：生成 Markdown / JSON demo report，并产出 AgentHub summary schema。
- 输出：report file、agenthub_summary object。
- 用户价值：用户可以截图展示，也可以让 AgentHubControlCenter 汇总多个 Agent 状态和输出。
- 后续实现：D2I-002 导出本地 demo report，D2I-004 再接入 AgentHubControlCenter。
