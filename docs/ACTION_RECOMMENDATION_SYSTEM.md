# Action Recommendation System

## 目标

行动建议系统把洞察从“有用信息”转成“下一步应该做什么”。它的价值在于减少用户二次判断成本。

## Action Types

| Action Type | 适用条件 | 目标位置 | 输出格式 | 示例 |
|---|---|---|---|---|
| `save_to_knowledge_base` | 学习价值或复用潜力高 | 本地知识库 / Markdown note | structured note | 把 consumer behaviour 笔记整理进营销知识库 |
| `route_to_existing_agent` | 与已有 Agent 能力匹配 | AgentHubControlCenter route target | route object | 把项目状态 note 路由给 AgentHubControlCenter |
| `create_project_idea` | project_value、portfolio_value、strategic_fit 高 | project backlog | project idea card | 把 AI workflow 想法转成 D2I 后续功能候选 |
| `use_for_assignment` | 学习资料、课程案例、作业相关 | assignment workspace | study brief | 把微观经济学案例转成作业参考摘要 |
| `use_for_portfolio` | 作品集展示价值高 | portfolio pipeline | portfolio note | 把 VideoExtractSkill 输出摘要转成 README case |
| `use_for_job_search` | 求职价值高 | career workspace | job search note | 把岗位描述摘要转成简历关键词 |
| `use_for_content_creation` | 内容价值高 | content pipeline | content outline | 把 SME 自动化痛点转成文章选题 |
| `generate_report` | 高价值信号数量足够 | outputs report | Markdown / JSON report | 生成本周 high-value insight report |
| `enrich_with_more_data` | 潜在价值高但证据不足 | review queue | enrichment task | 对 restaurant operations issue 补充更多样例 |
| `review_later` | 分类不确定或需要人工判断 | review queue | review item | 把边界模糊的 market signal 标记为复核 |
| `ignore_as_noise` | 低价值、重复、无行动价值 | ignored bucket | reason only | 忽略重复截图摘要或空泛观点 |

## 推荐逻辑

D2I-002 建议先使用规则映射：

- `course_learning` -> `save_to_knowledge_base` or `use_for_assignment`
- `project_asset` -> `use_for_portfolio` or `route_to_existing_agent`
- `business_signal` -> `create_project_idea` or `generate_report`
- `career_asset` -> `use_for_job_search`
- `content_idea` -> `use_for_content_creation`
- `ai_workflow_idea` -> `create_project_idea`
- `low_value_noise` -> `ignore_as_noise`
- `duplicate_reference` -> `review_later` or merge into existing note
- `needs_review` -> `review_later`

## 输出 schema

```json
{
  "action_type": "use_for_portfolio",
  "target_location": "portfolio_pipeline",
  "priority_level": "High",
  "recommended_next_step": "Turn this project output into a README case study.",
  "output_format": "markdown_note",
  "reason": "The item has high project and portfolio value."
}
```

## 产品边界

行动建议只生成本地建议，不自动发送邮件、不修改外部系统、不创建真实任务、不执行账号操作。
