# 场景驱动的隐性知识蒸馏智能体 — 产品设计文档

> 基于 pm-skills 五阶段产品设计方法论（Pawel Huryn / The Product Compass）

## 元数据

| 字段 | 值 |
|------|-----|
| **项目名称** | 场景驱动的隐性知识蒸馏智能体 |
| **项目英文名** | Scenario-Driven Tacit Knowledge Distillation Agent |
| **设计日期** | 2026-06-16 |
| **方法论** | pm-skills v1.x（68 skills + 42 commands） |
| **设计者** | Hermes Agent @ 陈科明数字分身 |
| **技术基底** | LLM Agent + CBR（案例推理）+ 场景化知识库 + 自修正回路 |
| **初装场景** | 电力/工业设备现场故障诊断 |
| **目标客户** | 轨物科技现有物联网客户（制造业/电力企业） |

## 配套文件

| 文件 | 说明 |
|------|------|
| raw/场景驱动的隐性知识蒸馏_深度调研报告_deepseek_2026-06-16.md | 技术深度调研（横纵分析） |
| 本文 | pm-skills 五阶段产品设计（从 Discover 到 Sprint Plan） |

## 设计状态总览

| Phase | 阶段 | 状态 | 关键产出 |
|-------|------|------|---------|
| Phase 1 | DISCOVER | 完成 | 问题陈述、8 类风险假设、Top 3 实验设计 |
| Phase 2 | RESEARCH | 完成 | 3 个用户画像、7 条 Job Story、竞品分析、旅程地图、OST |
| Phase 3 | STRATEGIZE | 完成 | 价值主张画布、9 部分产品策略、精益画布、定价策略 |
| Phase 4 | MEASURE | 完成 | 北极星指标（知识复用率）、3 组 OKR、三阶段 Roadmap |
| Phase 5 | EXECUTE | 完成 | Pre-Mortem、Red Team、8 条用户故事、6 个测试场景、12 周 Sprint Plan |

## 关键选择（概念验证阶段）

| 决策 | 选择 | 依据 |
|------|------|------|
| Agent 框架 | Hermes Agent | 已部署、框架成熟、支持技能体系 + 子 Agent 并行 |
| 知识存储格式 | 场景化结构化库（非纯向量库） | 场景匹配需要结构化上下文-决策-例外三元组 |
| 追问触发机制 | 事件驱动（修正/异常触发） | 减少对专家的打扰频率 |
| 首场景 | 设备故障诊断 | 高频、专家经验集中、轨物现有数据可用 |
| 部署模式 | 混合部署（SaaS + 本地可选） | 适配客户不同网络环境与数据安全要求 |

---

> **下一步**：进入 Phase 0 验证（Concierge MVP + Data Audit + Landing Page），确认 3 个最高风险假设后再做 MVP Go/No-Go 决策。
