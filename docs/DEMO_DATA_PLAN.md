# Demo Data Plan

## 原则

D2I 默认使用 public-safe synthetic demo data。Demo data 必须能展示真实使用方向，但不能包含真实个人隐私、真实 token、真实客户数据、真实敏感课程文件或真实账号信息。

## Demo item schema

每条 demo item 建议包含：

- `item_id`
- `title`
- `source_type`
- `raw_summary`
- `context`
- `expected_category`
- `synthetic`
- `created_for_demo`

## 建议的 12 条 synthetic demo items

| ID | Title | Type | Expected Category | 后续可转化为 |
|---|---|---|---|---|
| `demo_001` | Marketing segmentation notes | 学习类 | `course_learning` | 学习笔记、作业素材、知识库条目 |
| `demo_002` | Consumer behaviour assignment notes | 学习类 | `course_learning` | 作业结构、案例观点、考试复习卡片 |
| `demo_003` | Microeconomics case note | 学习类 | `course_learning` | 经济学案例摘要、学习洞察 |
| `demo_004` | VideoExtractSkill output summary | 项目类 | `project_asset` | README case、项目复用资产 |
| `demo_005` | AgentHub project status note | 项目类 | `project_asset` | AgentHub route、项目状态摘要 |
| `demo_006` | BusinessOpsAgent demo report | 项目类 | `project_asset` | 运营分析报告、作品集素材 |
| `demo_007` | SME customer feedback | 商业类 | `customer_pain` | 用户痛点、服务机会、商业信号 |
| `demo_008` | Restaurant operations issue | 商业类 | `operation_issue` | 自动化机会、流程优化建议 |
| `demo_009` | Local service business review summary | 商业类 | `business_signal` | 市场信号、内容选题、服务化方向 |
| `demo_010` | Resume feedback note | 求职类 | `career_asset` | 简历优化行动、求职知识库 |
| `demo_011` | Job description summary | 求职类 | `career_asset` | 岗位关键词、技能差距分析 |
| `demo_012` | Interview reflection note | 求职类 | `career_asset` | 面试复盘、下一步练习计划 |

## 每条 demo item 的目标输出

每条 demo item 后续应该能被转化成：

- 分类结果
- 价值评分
- 洞察信号
- 下一步行动建议
- keep / ignore / review 判断

## 禁止内容

- 真实姓名、电话、邮箱、地址
- 真实客户数据
- 真实课程付费材料原文
- token、API key、password、secret
- 私人报告全文
- 不能公开展示的截图或文件

## D2I-002 建议

D2I-002 可以新增：

```text
demo_data/demo_items.json
```

该文件只包含 synthetic demo items，不包含真实数据。
