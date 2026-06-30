# D2I Project Plan

## 项目一句话定位

DataToInsightWorkflowAgent 是一个本地优先、安全演示模式的数据洞察工作流智能体，把杂乱 demo 资料、笔记、报告和项目输出转化为分类结果、价值评分、洞察信号和下一步行动建议。

## 面向谁

- AI 产品型创作者
- 商科 / Marketing 背景的作品集建设者
- SME AI workflow consultant
- 需要整理学习资料、项目输出和商业信号的人
- 未来需要接入 AgentHubControlCenter 的本地 Agent 使用者

## 解决什么问题

用户经常积累大量资料，但真正有价值的内容很分散。这个项目解决的是“资料很多，但不知道哪些值得保留、复用、转成项目、用于求职或变成商业机会”的问题。

## 为什么适合当前作品集

- 展示从信息整理到商业洞察的完整 workflow
- 展示分类、评分、过滤、推荐动作的 Agent 产品思维
- 展示 public-safe 和 local-first 的工程边界
- 为 AgentHubControlCenter 提供未来可接入的标准 contract

## MVP 范围

D2I-001 只做规划、契约、文档和项目骨架。

D2I-002 再实现 demo data pipeline：

1. Load synthetic demo items
2. Normalize input fields
3. Classify content type
4. Score value dimensions
5. Filter noise
6. Extract insight signals
7. Recommend actions
8. Export Markdown / JSON report

## 暂时不做

- 不接真实 connector
- 不读取真实 `.env`、token、credential、secret
- 不处理真实敏感文件
- 不做真实外部动作
- 不做复杂 UI
- 不做云部署
- 不做 SaaS 化

## 技术结构

```text
data_to_insight/
├── __init__.py
├── config.py
└── schemas.py
```

D2I-001 只保留配置常量和 schema 骨架。业务逻辑会在 D2I-002 后逐步加入。

## 数据流

```text
Synthetic Demo Data
-> Normalized Records
-> Classified Records
-> Scored Signals
-> Filtered Insight Signals
-> Action Recommendations
-> Markdown / JSON Report
-> AgentHub Summary
```

## 作品集展示价值

README 和后续截图应该突出：

- 杂乱资料进入后的 workflow
- 高价值信号榜单
- 行动建议面板
- AgentHub-ready 输出
- public-safe demo mode

## 风险与边界

- 不使用真实个人隐私或真实客户数据
- 不暴露 token、API key、secret
- 不把 outputs 中的生成物推到公开仓库
- 不声称当前阶段已经支持真实 connector
- 不把演示评分包装成专业建议或投资建议
