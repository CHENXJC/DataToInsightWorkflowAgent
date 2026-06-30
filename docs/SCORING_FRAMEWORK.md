# Scoring Framework

## 设计原则

评分体系不能只给一个总分。D2I 的目标是判断资料在学习、商业、项目、作品集、求职、内容和行动上的不同价值。

每个维度使用 0-5 分：

- 0：无明显价值
- 1：价值很弱
- 2：有一点参考价值
- 3：有明确价值
- 4：高价值，值得优先处理
- 5：非常高价值，应进入重点行动队列

## 分类体系

| Category | 中文说明 |
|---|---|
| `course_learning` | 课程 / 学习资料 |
| `business_signal` | 商业信号 |
| `project_asset` | 项目资产 |
| `career_asset` | 求职资产 |
| `market_signal` | 市场 / 行业信号 |
| `customer_pain` | 用户痛点 |
| `operation_issue` | 运营问题 |
| `content_idea` | 内容选题 |
| `ai_workflow_idea` | AI 工作流想法 |
| `low_value_noise` | 低价值噪音 |
| `duplicate_reference` | 重复参考 |
| `needs_review` | 需要人工复核 |

## 多维评分字段

| Field | 中文说明 | 评分重点 |
|---|---|---|
| `learning_value` | 学习价值 | 是否能沉淀知识、辅助课程/技能提升 |
| `business_value` | 商业价值 | 是否包含市场机会、客户需求、服务化可能 |
| `project_value` | 项目转化价值 | 是否能转成 agent、skill、automation 或产品功能 |
| `portfolio_value` | 作品集展示价值 | 是否适合 GitHub、README、截图、demo 展示 |
| `career_value` | 求职价值 | 是否能辅助简历、面试、岗位理解 |
| `content_value` | 内容创作价值 | 是否能转成文章、视频、案例、观点 |
| `actionability` | 可行动性 | 是否能明确下一步动作 |
| `novelty` | 新颖度 | 是否有新信息、新角度或差异化 |
| `evidence_strength` | 证据强度 | 是否有足够上下文、例子或来源说明 |
| `reuse_potential` | 复用潜力 | 是否能长期复用到知识库、项目或流程 |
| `urgency` | 紧急程度 | 是否需要近期处理 |
| `strategic_fit` | 长期方向匹配度 | 是否匹配 AI agent、workflow、商业自动化和作品集方向 |

## overall_score

D2I-002 建议先使用简单平均分：

```text
overall_score = average(all score dimensions)
```

后续可以为不同目标添加权重，例如：

- portfolio mode：提高 `portfolio_value`、`project_value`、`strategic_fit`
- career mode：提高 `career_value`、`actionability`
- business mode：提高 `business_value`、`customer_pain` 相关权重

## priority_level

| Priority | 建议规则 |
|---|---|
| `High` | overall_score >= 4.0，且 actionability 或 strategic_fit >= 4 |
| `Medium` | overall_score >= 3.0，值得保留但不一定马上处理 |
| `Low` | overall_score >= 2.0，有参考价值但优先级低 |
| `Noise` | overall_score < 2.0，或 category 为 `low_value_noise` |
| `Needs Review` | 信息不足、分类不确定、证据弱但潜在价值不低 |

## recommended_route

推荐路由应该说明下一步去哪里：

- `knowledge_base`
- `agenthub`
- `project_backlog`
- `portfolio_pipeline`
- `career_workspace`
- `content_pipeline`
- `report_export`
- `review_queue`
- `ignore`

## keep_or_ignore

| Value | 说明 |
|---|---|
| `keep` | 进入洞察和行动建议 |
| `ignore` | 作为噪音忽略 |
| `review` | 进入人工复核 |
| `merge` | 与重复资料合并 |

## 输出字段

每条 scored item 至少包含：

- `overall_score`
- `priority_level`
- `recommended_route`
- `keep_or_ignore`
- `reason`

## 示例

```json
{
  "item_id": "demo_004",
  "category": "project_asset",
  "overall_score": 4.2,
  "priority_level": "High",
  "recommended_route": "portfolio_pipeline",
  "keep_or_ignore": "keep",
  "reason": "This item can become a reusable portfolio artifact and supports AgentHub integration."
}
```
