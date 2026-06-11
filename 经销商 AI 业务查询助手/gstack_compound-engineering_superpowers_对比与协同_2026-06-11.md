# gstack、compound-engineering、superpowers 三者的异同与协同指南

> 2026-06-11 | 基于本地安装版本分析：gstack v1.56, compound-engineering v3.11.1, superpowers v5.1.0

---

## 一、一页概览

| 维度 | gstack | compound-engineering | superpowers |
|------|--------|---------------------|-------------|
| **作者** | Garry Tan (YC) | Compound Engineering 团队 | Jesse Vincent / Prime Radiant |
| **技能数量** | 60+ | 30+ (含 43 个 sub-agent) | 14 |
| **核心隐喻** | 一支"专家团队" | 知识复利引擎 | 一套"铁律方法论" |
| **核心哲学** | Boil the Lake（AI 让完整性成本趋零） | Knowledge Compounds（每次工作让下次更容易） | Hard Gates（强制纪律，杜绝走捷径） |
| **纪律严格度** | 中等（自动决策为主，品味决策上浮） | 低-中（引导式，尊重用户判断） | 极高（硬门禁、铁律、反合理化表格） |
| **最适合** | 从想法到上线的全流程产品开发 | 工程团队的代码质量与知识沉淀 | 追求代码质量和纪律的严肃开发 |

---

## 二、深层哲学对比

### 2.1 对"AI 能做什么"的假设

```
gstack:           AI 让完整性边际成本趋零 → 应该做完整的事（Boil the Lake）
compound-eng:     AI 是知识放大器 → 每次解决问题的经验应该沉淀为可复用知识
superpowers:      AI 会走捷径,需要强制约束 → 必须用铁律防止代理人偷懒
```

这三个假设并不矛盾——它们是在不同维度上的互补洞察：
- gstack 解决 **"做多少"** 的问题（激励做完整）
- compound-engineering 解决 **"学到什么"** 的问题（激励沉淀知识）
- superpowers 解决 **"怎么做"** 的问题（约束执行纪律）

### 2.2 决策权归属

| 系统 | 决策模式 | 用户体验 |
|------|---------|---------|
| gstack | `/autoplan` 用 6 条决策原则自动决策，只把品味决策上浮 | "一命令，全审完" |
| compound-eng | agent 给出分析，用户做决策 | 专家建议式 |
| superpowers | 技能本身是硬约束，但用户指令优先级最高 | 铁律执行式 |

### 2.3 "用户"是谁

- **gstack**: 创业者和技术负责人——想要一个人 + AI 顶一支团队
- **compound-engineering**: 专业工程团队——想要跨 session、跨成员的知识复利
- **superpowers**: AI agent 本身——技能是为 agent 行为塑形，人类是"合作伙伴"

---

## 三、功能矩阵对比

### 3.1 研发全流程覆盖

```
阶段              gstack                    compound-eng           superpowers
─────────────────────────────────────────────────────────────────────────────
产品发现/策略      /office-hours             ce-strategy            —
                  /plan-ceo-review          ce-brainstorm          brainstorming
                  
方案设计           /plan-eng-review          ce-plan                writing-plans
                  /autoplan                 
                  
视觉设计           /design-consultation      ce-frontend-design     —
                  /design-shotgun           
                  /design-html              
                  
实现              （依赖外部 agent）          ce-work                subagent-driven-dev
                                                            executing-plans
                                                            test-driven-dev
                                                            
代码审查           /review (员工工程师级)     ce-code-review         requesting-code-review
                  /codex (跨模型)           (14+ reviewer types)   receiving-code-review
                  
浏览器测试/QA      /qa /qa-only              ce-test-browser        —
                  /browse (真实 Chromium)    
                  
安全检查           /cso                      ce-security-reviewer   —
                  
部署/发布          /ship                     ce-commit-push-pr      finishing-a-dev-branch
                  /land-and-deploy          lfg (全自动)
                  
线上监控           /canary                   —                      —
                  
知识沉淀           /learn                    ce-compound            writing-skills
                  /document-release         ce-compound-refresh    
                  
回顾              /retro                    —                      —
```

### 3.2 独有能力（仅一个系统具备）

**仅 gstack 有:**
- 真实 Chromium 浏览器集成（截图、点击、表单、断言）
- 跨模型审查（Claude + Codex 双模型共识/分歧分析）
- 设计多方案生成与视觉迭代（/design-shotgun）
- 完整的 ship → deploy → canary 生产部署链
- 团队回顾（/retro）
- Prompt 注入防御（ML 分类器 + canary token + 多模型判决）
- 设计师-实现双向审计（plan-design-review ↔ design-review）

**仅 compound-engineering 有:**
- 14+ 类型化代码审查 agent（安全、性能、数据迁移、API 契约、可靠性等）
- 知识复利闭环（ce-compound → docs/solutions/ → ce-compound-refresh）
- 置信度门控查找管线（0/25/50/75/100 anchor）
- 概念词汇基础设施（CONCEPTS.md 防止同义词漂移）
- 跨平台技能设计（同一份 SKILL.md 在 Claude Code / Codex / Cursor 中运行）
- 流程废气与产出物分离纪律

**仅 superpowers 有:**
- 铁律级 TDD 强制执行（RED-GREEN-REFACTOR 不可跳过）
- 12 条"红旗"合理化防御表（防止 agent 用话术跳过流程）
- 对抗性压力测试技能质量（用 subagent 模拟时间压力/沉没成本/权威施压场景）
- 两级审查循环（先 spec 合规审查，再代码质量审查）
- 连续自主执行模式（禁止在任务间暂停询问"要继续吗"）
- 出处感知清理（只清理 superpowers 自己创建的 worktree）

---

## 四、重叠与互补分析

### 4.1 三者都覆盖的能力（但深浅不同）

**代码审查:**

| | gstack /review | ce-code-review | superpowers SDD 审查 |
|---|---|---|---|
| 审查者数量 | 1（员工工程师级） | 6-15（并行派遣） | 2（spec 审查 + 代码质量审查） |
| 跨模型 | 支持（+ Codex） | 不支持 | 不支持 |
| 自动修复 | 有 | 安全修复自动应用 | 有（循环修复） |
| 置信度量化 | 无 | 5 级 anchor (0-100) | 无 |
| 适用场景 | 快速 PR 审查 | 深度多维度审查 | 迭代开发中的任务级审查 |

**规划:**

| | gstack /autoplan | ce-plan | superpowers writing-plans |
|---|---|---|---|
| 审查维度 | CEO+设计+工程+DX | 技术实现计划 | 工程实现计划 |
| 粒度 | 宏观评审 | 中等 | 极细（每步 2-5 分钟） |
| 自动决策 | 6 原则自动决策 | 用户决策 | 用户确认 |
| 产物 | 评审报告 | 实现计划 | 带代码块和验证命令的计划 |

**调试:**

| | gstack /investigate | ce-debug | superpowers systematic-debugging |
|---|---|---|---|
| 方法论 | 铁律：不调查不修 | 因果链纪律 | 4 阶段根因分析 |
| 停止条件 | 3 次修复失败 | 智能升级 | 基于证据 |

### 4.2 互补关系图

```
                    gstack 擅长
                    ╱          ╲
        产品思维/策略            视觉设计/QA/部署
       ╱                              ╲
      │                                │
      │      compound-eng 擅长          │
      │      代码质量/知识沉淀           │
      │                                │
      ╲                              ╱
       ╲          ╱──────────╲      ╱
        superpowers 擅长              │
        开发纪律/TDD/防走捷径  ───────┘
```

三个系统覆盖了不同的"质量纵深"：
- **gstack**: 从产品策略到生产部署的**水平宽度**
- **compound-engineering**: 代码质量和知识的**垂直深度**
- **superpowers**: 开发执行的**纪律密度**

---

## 五、协同使用指南

### 5.1 按项目阶段选择主力系统

```
项目阶段          主力系统           辅助系统            为什么
──────────────────────────────────────────────────────────────────
0. 产品探索       gstack             —                  /office-hours 挑战前提
                 /office-hours                          /plan-ceo-review 战略审查

1. 方案设计       gstack             superpowers        gstack 做多维度评审
                 /autoplan           brainstorming      superpowers 出详细 spec

2. 详细规划       superpowers        compound-eng       superpowers 出极细任务拆解
                 writing-plans       ce-plan            ce-plan 做架构验证

3. 编码实现       superpowers        compound-eng       superpowers 保证 TDD 纪律
                 subagent-driven-dev ce-work            ce-work 管理工作树并行

4. 代码审查       compound-eng       gstack             ce-code-review 深度多维度
                 ce-code-review      /review            gstack 跨模型复查关键路径

5. 浏览器测试     gstack              —                  只有 gstack 有真实浏览器
                 /qa /browse

6. 安全检查       gstack              compound-eng       /cso 做全面审计
                 /cso                ce-security-review  ce 做增量安全审查

7. 知识沉淀       compound-eng        gstack             ce-compound 结构化沉淀
                 ce-compound          /learn             /learn 做轻量标记

8. 发布上线       gstack              —                  /ship → /land-and-deploy
                 /ship                                 → /canary 完整链路
```

### 5.2 三种典型工作流

#### 工作流 A：创业项目全流程（gstack 为主，superpowers 为辅）

```
/office-hours          → 产品假设
/autoplan               → 全维度方案评审
superpowers:brainstorming → 详细 spec
superpowers:writing-plans  → 任务拆解
superpowers:TDD + SDD      → 纪律化编码
ce-code-review             → 深度代码审查
gstack:/qa                 → 浏览器端到端测试
gstack:/ship               → 发布
ce-compound                → 沉淀经验
```

#### 工作流 B：团队工程迭代（compound-eng 为主，gstack 为辅）

```
ce-brainstorm           → 需求分析（WHAT）
ce-plan                 → 技术方案（HOW）
ce-work                 → 并行实现（工作树隔离）
ce-code-review          → 14 维度审查
gstack:/review + /codex  → 跨模型复查关键路径
ce-commit-push-pr       → 提交 PR
ce-compound             → 写入 docs/solutions/
gstack:/retro            → 周回顾
```

#### 工作流 C：高质量 solo 开发（superpowers 为主）

```
superpowers:brainstorming     → 设计文档
superpowers:writing-plans      → 详细计划
superpowers:using-git-worktrees → 隔离工作区
superpowers:subagent-driven-dev → TDD + 两级审查 + 连续执行
gstack:/review                  → 最终代码审查
superpowers:finishing-branch    → 合并/PR
ce-compound                     → 沉淀关键经验
```

### 5.3 避免冲突：谁说了算

当三个系统的指令冲突时，优先级：

```
1. 用户的 CLAUDE.md / AGENTS.md 显式指令    ← 最高
2. 当前激活的 skill 的指令                   ← 当前任务上下文
3. superpowers 方法论约束 (如 TDD 铁律)      ← 如果你认同纪律优先
4. gstack 完整性原则 (Boil the Lake)        ← 如果你认同完整性优先
5. 系统默认行为                              ← 最低
```

**关键原则**:
- superpowers 说"写测试前不能写代码"、gstack 说"做完整"——不矛盾。先写测试再写完整实现。
- ce-code-review 有 14 个 reviewer、gstack /review 有 1 个——可以先后使用，ce 做深度，gstack 做快速复查。
- 不要同时激活多个同类 skill。规划用 gstack 还是 superpowers？选一个，不要并行。

---

## 六、何时用哪个（决策速查表）

| 你的情况 | 选这个 | 而非 |
|----------|--------|------|
| "我想验证产品想法是否靠谱" | gstack /office-hours | ce-brainstorm |
| "帮我审一下这个方案" | gstack /autoplan | 手动询问 |
| "我要写一个极详细的实现计划" | superpowers writing-plans | ce-plan |
| "我要保证每个任务都写测试" | superpowers TDD + SDD | gstack |
| "审一下这段代码有没有安全漏洞" | ce-code-review | gstack /review |
| "在浏览器里测一下这个页面" | gstack /qa | 手动测试 |
| "我想把这次的经验沉淀下来" | ce-compound | /learn |
| "帮我把代码推到生产环境" | gstack /ship | 手动操作 |
| "我想让 AI 自己连续工作几小时" | superpowers SDD | ce-work |
| "我要设计一个好看的界面" | gstack /design-shotgun | ce-frontend-design |

---

## 七、总结

### 一句话差异

- **gstack** 让你有 **一支团队**（CEO → 设计师 → 工程师 → QA → SRE）
- **compound-engineering** 让你有 **一个不断变聪明的工程系统**（代码审查→知识沉淀→复利）
- **superpowers** 让你有 **一套不可违背的工程纪律**（TDD→审查→证据→完成）

### 一句话协同

> 用 **superpowers** 管纪律（怎么写），用 **compound-engineering** 管质量（写多好），用 **gstack** 管全流程（从想法到上线）。

### 最重要的建议

**不要试图同时精通三者。** 从一个开始：
1. 如果你最缺产品方向 → 从 gstack 开始
2. 如果你最缺代码质量 → 从 compound-engineering 开始
3. 如果你最缺开发纪律 → 从 superpowers 开始

掌握一个后再引入第二个，清晰理解每个系统的边界，避免重复和冲突。
