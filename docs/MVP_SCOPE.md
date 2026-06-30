# MVP Scope

## 当前阶段：D2I-001

D2I-001 只完成项目地基：

- 项目结构
- README / status / docs
- workflow map
- scoring framework
- action recommendation framework
- demo data plan
- public-safe rules
- AgentHub manifest / contract
- minimal Python package skeleton

不实现真实数据处理功能。

## D2I-002 MVP 范围

D2I-002 目标是用 synthetic demo data 跑通最小闭环：

1. 读取 demo items
2. 标准化字段
3. 进行规则型分类
4. 计算多维评分
5. 过滤低价值噪音
6. 提取洞察信号
7. 生成行动建议
8. 导出 Markdown / JSON demo report

## 内容分类体系

| Category | 中文说明 | 用途 |
|---|---|---|
| `course_learning` | 课程 / 学习资料 | 用于学习沉淀、作业准备、知识库积累 |
| `business_signal` | 商业信号 | 用于发现机会、趋势、产品化方向 |
| `project_asset` | 项目资产 | 用于作品集、GitHub 展示、后续 agent 复用 |
| `career_asset` | 求职资产 | 用于简历、面试、岗位匹配 |
| `market_signal` | 市场 / 行业信号 | 用于市场观察、行业判断、内容选题 |
| `customer_pain` | 用户痛点 | 用于产品机会、服务方案、商业洞察 |
| `operation_issue` | 运营问题 | 用于流程优化、自动化机会识别 |
| `content_idea` | 内容选题 | 用于文章、视频、社媒内容储备 |
| `ai_workflow_idea` | AI 工作流想法 | 用于新 agent / skill / automation 规划 |
| `low_value_noise` | 低价值噪音 | 用于过滤、忽略或降低优先级 |
| `duplicate_reference` | 重复参考 | 用于去重或合并引用 |
| `needs_review` | 需要人工复核 | 用于不确定、证据不足或边界复杂内容 |

## MVP 输入格式

D2I-002 的 demo item 建议包含：

- `item_id`
- `title`
- `source_type`
- `raw_summary`
- `context`
- `synthetic`
- `created_for_demo`

## MVP 输出格式

每条 demo item 至少输出：

- `category`
- `scores`
- `overall_score`
- `priority_level`
- `insight_signal`
- `recommended_action`
- `keep_or_ignore`
- `reason`

## 成功标准

- 可以使用 synthetic demo data 跑完整个 pipeline
- 输出结果能解释为什么保留或忽略某条信息
- 输出能被导出为 Markdown / JSON
- 不需要任何真实 connector
- 不读取任何 secret
- 结果适合公开截图展示
