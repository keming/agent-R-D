# 产品开发全流程—
扩大后的生态系统：8 系统全景

```
                    ┌──────────────────────────────────────────┐
                    │          PRODUCT DISCOVERY               │
                    │  pm-skills (150+ PM skills/commands)     │
                    │  gstack /office-hours /plan-ceo-review   │
                    │  ce-strategy                             │
                    └────────────────┬─────────────────────────┘
                                     │
                    ┌────────────────▼─────────────────────────┐
                    │         ARCHITECTURE DESIGN              │
                    │  architecture-copilot (苏格拉底教练)      │
                    │  architecting-solutions (PRD 产出)       │
                    │  gstack /autoplan (全维度评审)            │
                    └────────────────┬─────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
 ┌────────────▼──────┐  ┌────────────▼──────┐  ┌───────────▼──────────┐
 │  ★ API CONTRACT   │  │  ★ DATA MODEL     │  │  ★ OBSERVABILITY    │
 │  api-designer     │  │  db-skills        │  │  otel-instrumentation│
 │  api-contract     │  │  (schema/migrate/ │  │  otel-collector      │
 │  (6步design-first)│  │   audit/optimize) │  │  otel-semantic-conv  │
 └────────┬──────────┘  └────────┬──────────┘  │  otel-ottl           │
          │                      │              └───────────┬──────────┘
          └──────────────────────┼──────────────────────────┘
                                 │
                    ┌────────────▼─────────────────────────────┐
                    │           IMPLEMENTATION                 │
                    │  superpowers TDD + SDD (纪律)            │
                    │  ce-plan → ce-work (规划→并行执行)        │
                    │  superpowers writing-plans (任务拆解)     │
                    │  pm-skills sprint-plan (Sprint 计划)     │
                    └────────────────┬────────────────────────┘
                                     │
                    ┌────────────────▼─────────────────────────┐
                    │           QUALITY ASSURANCE              │
                    │  ce-code-review (14+ reviewer)           │
                    │  gstack /review + /codex (跨模型)         │
                    │  gstack /qa (浏览器端到端)                │
                    │  gstack /cso (安全审计)                   │
                    │  pm-ai-shipping (intended-vs-implemented) │
                    └────────────────┬────────────────────────┘
                                     │
                    ┌────────────────▼─────────────────────────┐
                    │           SHIP & REFLECT                 │
                    │  gstack /ship → /land-and-deploy         │
                    │  ce-commit-push-pr                       │
                    │  ce-compound (知识沉淀)                   │
                    │  gstack /retro (回顾)                     │
                    │  gstack /canary (线上监控)                │
                    └──────────────────────────────────────────┘
```

---

## 四、完整的产品开发全流程（12 阶段）

### Phase 1: DISCOVER — 发现机会
```
pm-skills /brainstorm /discover /triage-requests
→ 生成 idea → 识别 8 类假设 → 设计验证实验
```
| 已有 | 缺口 |
|------|------|
| brainstorm-ideas-new, identify-assumptions-new, prioritize-assumptions, brainstorm-experiments-new | — |

### Phase 2: RESEARCH — 研究用户与市场
```
pm-skills /research-users /competitive-analysis
→ 用户画像 + JTBD + 竞品分析 + 市场容量
```
| 已有 | 缺口 |
|------|------|
| user-personas, competitor-analysis, customer-journey-map, market-sizing | — |

### Phase 3: STRATEGIZE — 制定战略
```
pm-skills /strategy /value-proposition /business-model /pricing
→ 9 部分产品战略画布 + 价值主张 + 商业模式
```
| 已有 | 缺口 |
|------|------|
| product-strategy, value-proposition, lean-canvas, pricing-strategy, SWOT/PESTLE/Ansoff | — |

### Phase 4: ARCHITECT — 架构设计
```
architecture-copilot (8 阶段苏格拉底教练)
  → 灵魂六问 → 信封估算 → 质量属性排序 → ADR
gstack /autoplan (全维度评审)
architecting-solutions (PRD 级别方案设计)
```
| 已有 | 缺口 |
|------|------|
| 系统级架构方法论, 25 个系统模板, AI 系统专项, 反挑战 | — |

### Phase 5: ★ API CONTRACT — API 契约设计
```
api-designer (6 步 design-first)
  1. 分析领域 → 2. 建模资源 → 3. 设计端点
  4. 编写 OpenAPI 3.1 YAML → 5. @redocly/cli lint 验证
  6. @stoplight/prism mock server → 演进规划
api-contract (contract lifecycle)
  → MSW frontend mock → Pact consumer-driven testing → type generation
```
| 已有（新增） | 剩余缺口 |
|-------------|---------|
| REST API design + mock + validate + contract test | gRPC proto 设计, GraphQL schema 设计（已有 Apollo graphql-schema 可选装） |

### Phase 6: ★ DATA MODEL — 数据模型设计
```
db-skills query-database-schema (探查 live schema)
  → 了解现状 → 设计新 schema
db-skills write-safe-migrations (零停机迁移)
  → expand-contract 模式 → up/down scripts → rollback
db-skills debug-slow-queries
  → EXPLAIN → 索引建议
db-skills data-quality-audit
  → null/重复/孤儿/越界检查
```
| 已有（新增） | 剩余缺口 |
|-------------|---------|
| schema 探查 + 安全迁移 + 慢查询诊断 + 数据质量审计 | ER 图生成（建议用 DBML + Kroki），规范化分析 |

### Phase 7: ★ OBSERVABILITY — 可观测性设计
```
otel-instrumentation
  → auto + manual instrumentation for 10+ languages
otel-semantic-conventions
  → 标准化属性名, span kind, status code
otel-collector
  → receivers → processors → exporters → K8s deployment
otel-ottl
  → transform / filter / redact / enrich telemetry
```
| 已有（新增） | 剩余缺口 |
|-------------|---------|
| OTel 插桩 + 语义约定 + collector + 数据变换 | SLO/SLI 定义（参考 agent-reliability-engineering 仓库），告警规则，runbook |

### Phase 8: PRD & VALIDATION — PRD 与验证
```
pm-skills /write-prd (8 部分 PRD)
  → Summary + Background + Objective + Segments + Value Props + Solution + Release
pm-skills /pre-mortem (预尸检)
  → 想象上线 14 天后失败 → Tigers/Paper Tigers/Elephants
pm-skills /red-team-prd (红队攻击)
  → 攻击 load-bearing assumptions → kill criteria
```
| 已有 | 缺口 |
|------|------|
| PRD 撰写 + 预尸检 + 红队审查 + test scenarios | — |

### Phase 9: IMPLEMENT — 实现
```
superpowers TDD + SDD (纪律化实现)
ce-plan → ce-work (规划→并行执行)
pm-skills /sprint (Sprint 计划)
```
| 已有 | 缺口 |
|------|------|
| TDD 铁律, 子代理驱动开发, 并行工作树, Sprint 管理 | — |

### Phase 10: REVIEW — 代码审查
```
ce-code-review (14+ 类型化 reviewer)
gstack /review + /codex (跨模型复查)
```
| 已有 | 缺口 |
|------|------|
| 安全/性能/API 契约/数据迁移/可靠性/维护性审查 | — |

### Phase 11: QA & AUDIT — 测试与审计
```
gstack /qa (浏览器端到端)
pm-skills /test-scenarios (测试场景生成)
pm-ai-shipping /ship-check
  → /document-app → /derive-tests → /security-audit-static
  → /performance-audit-static → intended-vs-implemented
```
| 已有 | 缺口 |
|------|------|
| 端到端测试, 测试场景, AI 代码审计, 安全审计, 性能审计 | — |

### Phase 12: SHIP & GROW — 发布与增长
```
gstack /ship → /land-and-deploy → /canary
pm-skills /plan-launch (GTM)
pm-skills /north-star (北极星指标)
ce-compound (知识沉淀)
gstack /retro (回顾)
```
| 已有 | 缺口 |
|------|------|
| 发布, 部署, 监控, GTM, 指标, 知识管理, 回顾 | — |

---

## 五、8 系统角色速查

| 系统 | 一句话角色 | 阶段 |
|------|-----------|------|
| **pm-skills** | PM 全流程——从发现到增长 | Phase 1-3, 8, 12 |
| **architecture-copilot** | 苏格拉底架构教练 | Phase 4 |
| **architecting-solutions** | PRD 级方案设计师 | Phase 4 |
| **api-designer** ★ | API 契约设计—6 步 design-first | Phase 5 |
| **api-contract** ★ | API 契约生命周期—mock + contract test | Phase 5 |
| **db-skills** ★ | 数据模型—schema/migrate/audit/optimize | Phase 6 |
| **dash0hq/otel** ★ | 可观测性—插桩/collector/semantic/OTTL | Phase 7 |
| **gstack** | 全流程平台—策略到上线 | Phase 1, 4, 10-12 |
| **compound-engineering** | 代码质量 + 知识复利 | Phase 9-10, 12 |
| **superpowers** | 开发纪律—TDD + SDD | Phase 9 |

★ = 本轮新安装

---

## 六、还未覆盖的缺口（未来可补）

| 缺口 | 严重度 | 建议方案 |
|------|--------|---------|
| gRPC proto 设计 | 低（多数项目用 REST） | 暂无成熟的 AI agent skill |
| ER 图生成 | 低（可用 DBML + Kroki 手写） | bruce-drawio 可生成 draw.io XML |
| SLO/SLI/告警规则 | 中 | agent-reliability-engineering 仓库作为方法论参考 |
| runbook/incident response | 低 | 参考 agent-reliability-engineering 的 SKILL.md as runbook 模式 |
| CI/CD pipeline 设计 | 中 | 暂无专用 skill，需手动设计 |
| 无障碍 (a11y) 审计 | 低 | 暂无专用 skill |
| 国际化 (i18n) 设计 | 低 | 暂无专用 skill |
| 技术债管理 | 中 | 暂无专用 skill |



### 推荐的最小启动集合

如果从零开始只用最少 skill 完成一个产品，推荐：

```
pm-skills (PM 全流程)
  + architecture-copilot (架构设计)
  + api-designer (API 契约)
  + db-skills (数据模型)
  + superpowers (开发纪律)
  + ce-code-review (代码审查)
  + gstack /ship (发布)
```
