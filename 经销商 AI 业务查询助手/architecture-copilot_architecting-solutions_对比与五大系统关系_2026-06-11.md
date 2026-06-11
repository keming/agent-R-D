# architecture-copilot vs architecting-solutions 对比，及与五大系统的关系

> 2026-06-11 | 五系统全景：gstack · compound-engineering · superpowers · architecture-copilot · architecting-solutions

---

## 一、architecture-copilot vs architecting-solutions：核心差异

### 一句话差异

| | architecture-copilot | architecting-solutions |
|---|---|---|
| **一句话** | 苏格拉底式架构教练——**问你问题，让你自己想清楚** | PRD 驱动的方案设计师——**分析代码、提出方案、写出 PRD** |
| **角色** | 教练 / 引导者 | 设计师 / 产出者 |
| **方法** | Socratic（提问→收敛） | Directive（分析→提案→写文档） |
| **输出** | 架构全景图、ADR、风险清单、演进路线 | 一份 PRD markdown 文件（`docs/` 目录） |
| **来源** | study8677/awesome-architecture (26 章 + 25 模板) | 本地自定义 skill |
| **语言** | 中英混合（以中文为主） | 英文（含中文触发词） |

### 详细对比矩阵

| 维度 | architecture-copilot | architecting-solutions |
|------|---------------------|----------------------|
| **核心理念** | "架构是从约束里逼出来的，不是画出来的" | "简洁优先，反对过度工程" |
| **提问风格** | 一次 1-3 个紧密关联问题，逐步深入 | 一次问清需求、约束、成功标准 |
| **方案输出** | 不给方案，帮你想清楚后自己画 | 给 3 个方案选项（最小/中等/全面）供选择 |
| **代码分析** | 不做——"不陷入语言/框架/语法" | 核心步骤——grep/find 分析现有代码 |
| **架构图** | ASCII 图，严格分层（Context→Container→Component） | 不强制画图，写在 PRD 里 |
| **数据模型** | 数据模型 + 存储选型表 + 一致性分析 | 组件定义 + state 设计 + API 规格 |
| **规模估算** | 信封背面估算（QPS/存储/带宽/AI token/成本） | 不做 |
| **质量属性** | 10 个质量属性逐项排序 + 冲突点破 | 约束识别，不系统化 |
| **ADR** | 核心产出物（状态/背景/候选/决定/理由/代价） | 不做 |
| **风险分析** | 反挑战阶段系统化攻击方案软肋 | PRD 中标注风险 |
| **AI 系统** | 深度覆盖（幻觉/提示注入/成本漂移/eval/人审） | 不专门覆盖 |
| **25 个系统模板** | 内建知识锚点映射（从电商到 Codex Agent） | 无 |
| **最佳场景** | 新系统从 0 设计、系统设计面试、架构评审、技术方案讨论 | 已有代码库、要写 PRD、要出具体实现方案 |

### 工作流对比

```
architecture-copilot (8 阶段):
  阶段0: 一句话定位
    → 阶段1: 业务本质与范围（做什么/不做什么）
    → 阶段2: 灵魂六问（规模/读写比/一致性/增长/失败代价/约束）
    → 阶段3: 信封背面估算（QPS/存储/AI成本）
    → 阶段4: 质量属性取舍（10 属性排序 + 冲突点破）
    → 阶段5: 关键决策追问（存储选型/同步异步/缓存/状态/单体拆分）
    → 阶段6: 收敛产出（全景图/数据流/数据模型/ADR/演进路线/风险）
    → 阶段7: 反挑战（一致性/韧性/规模/安全/AI特有/演进）

architecting-solutions (7 步骤):
  步骤1: 澄清需求
    → 步骤2: 识别约束
    → 步骤3: 分析现有代码库（grep/find）
    → 步骤4: 研究最佳实践（如需要）
    → 步骤5: 设计方案（3 选项：最小/中等/全面）
    → 步骤6: 生成 PRD 文档（docs/ 目录）
    → 步骤7: 与用户验证
```

---

## 二、两者与 gstack / compound-engineering / superpowers 的关系

### 2.1 定位图谱

```
              架构专项深度
                    ↑
                    │  architecture-copilot (最深——系统级架构方法论)
                    │  architecting-solutions (深——实现级方案设计)
                    │
        ┌───────────┼───────────┐
        │           │           │
   gstack       compound-eng  superpowers
   (广度最大)    (代码质量深)   (纪律最严)
        │           │           │
        └───────────┼───────────┘
                    ↓
              开发全流程覆盖
```

**关键洞察**: architecture-copilot 和 architecting-solutions 是**架构维度的垂直专家**，而 gstack/ce/superpowers 是**研发流程的水平平台**。它们不竞争——它们在填充平台"够用但不专精"的架构缺口。

### 2.2 与 gstack 的关系

| gstack 覆盖的架构相关能力 | architecture-copilot 如何更强 | architecting-solutions 如何互补 |
|---|---|---|
| `/plan-eng-review` 做架构审查 | AC 更系统化：灵魂六问 + 信封估算 + 质量属性排序 + 反挑战 | AS 更落地：分析现有代码 + 给具体文件路径 |
| `/plan-ceo-review` 做战略审查 | AC 有 25 个系统模板做领域匹配 | — |
| `/autoplan` 全管线一次跑 | AC 单维度深挖，不追求广度 | AS 产 PRD，不产评审报告 |
| 无专用架构设计 skill | **AC 填补了这个空白** | **AS 填补了 PRD 写作空白** |

**协同模式**: gstack `/autoplan` 做方案评审 → architecture-copilot 做深度架构设计 → architecting-solutions 产出具体 PRD

### 2.3 与 compound-engineering 的关系

| compound-eng 覆盖的架构相关能力 | architecture-copilot 如何不同 | architecting-solutions 如何互补 |
|---|---|---|
| `ce-plan` 做技术方案规划 | AC 不写计划，AC 让你想清楚再写 | AS 产出更结构化的 PRD 文档 |
| `ce-code-review` 做架构审查 (ce-architecture-strategist) | AC 是设计时教练，不是审查者 | AS 产出的 PRD 可直接喂给 ce-work |
| `ce-compound` 沉淀架构经验 | AC 的方法论本身就是可沉淀的 | — |
| `ce-brainstorm` 做需求分析 | AC 从架构视角提问，ce-brainstorm 从产品视角 | — |

**协同模式**: architecture-copilot 想清楚架构 → architecting-solutions 出 PRD → ce-plan 做实现规划 → ce-work 执行 → ce-code-review 审查 → ce-compound 沉淀

### 2.4 与 superpowers 的关系

| superpowers 覆盖的架构相关能力 | architecture-copilot 如何不同 | architecting-solutions 如何互补 |
|---|---|---|
| `brainstorming` 做设计细化 | AC 是架构维度，sp brainstorming 是功能维度 | AS 产出 PRD 比 sp brainstorming 的 spec 更技术化 |
| `writing-plans` 出详细实现计划 | AC 不写代码级计划 | AS 的 PRD 是 writing-plans 的前置输入 |
| 无架构专项能力 | **AC 填补空白** | **AS 填补 PRD 空白** |

**协同模式**: architecture-copilot 定架构方向 → architecting-solutions/PRD → superpowers brainstorming 做功能 spec → writing-plans 拆任务 → SDD 执行

---

## 三、五大系统全景关系图

```
                         ┌─────────────────────────────────────────┐
                         │           PRODUCT DISCOVERY              │
                         │                                         │
                         │  gstack /office-hours (产品假设挑战)      │
                         │  gstack /plan-ceo-review (战略审查)       │
                         │  ce-strategy (产品锚点)                   │
                         └────────────────┬────────────────────────┘
                                          │
                         ┌────────────────▼────────────────────────┐
                         │         ARCHITECTURE DESIGN             │
                         │                                         │
                         │  ★ architecture-copilot (苏格拉底教练)    │
                         │    灵魂六问 → 估算 → 质量属性 → ADR       │
                         │  ★ architecting-solutions (PRD 产出)     │
                         │    代码分析 → 3 方案 → PRD 文档           │
                         │                                         │
                         │  gstack /plan-eng-review (架构审查)       │
                         │  gstack /autoplan (全维度评审)            │
                         └────────────────┬────────────────────────┘
                                          │
                         ┌────────────────▼────────────────────────┐
                         │           IMPLEMENTATION                 │
                         │                                         │
                         │  superpowers TDD (纪律)                   │
                         │  superpowers SDD (子代理执行)              │
                         │  ce-plan → ce-work (规划→执行)            │
                         │  superpowers writing-plans (任务拆解)     │
                         └────────────────┬────────────────────────┘
                                          │
                         ┌────────────────▼────────────────────────┐
                         │           QUALITY ASSURANCE              │
                         │                                         │
                         │  ce-code-review (14+ reviewer 类型)       │
                         │  gstack /review (员工工程师审查)           │
                         │  gstack /codex (跨模型复查)               │
                         │  gstack /qa (浏览器端到端测试)             │
                         │  gstack /cso (安全审计)                   │
                         └────────────────┬────────────────────────┘
                                          │
                         ┌────────────────▼────────────────────────┐
                         │           SHIP & REFLECT                 │
                         │                                         │
                         │  gstack /ship → /land-and-deploy         │
                         │  ce-commit-push-pr                       │
                         │  ce-compound (知识沉淀)                   │
                         │  gstack /retro (回顾)                    │
                         └─────────────────────────────────────────┘
```

---

## 四、何时用谁：架构场景决策矩阵

| 你的情况 | 第一选择 | 第二选择 | 为什么 |
|----------|---------|---------|--------|
| "我有一个新系统想法，帮我想清楚架构" | **architecture-copilot** | gstack /plan-eng-review | AC 的苏格拉底方法最适合从 0 到 1 |
| "我有一段现有代码，帮我设计改造方案" | **architecting-solutions** | ce-plan | AS 会分析现有代码，给具体方案 |
| "帮我审一下这个技术方案的架构" | **architecture-copilot** (读图模式) | gstack /autoplan | AC 读图四步法 + gstack 多维度评审 |
| "我有个 PRD，帮我审一下技术和架构" | **gstack /autoplan** | architecture-copilot | autoplan 做全维度，AC 深挖架构 |
| "我要写一个带架构设计的 PRD" | **architecting-solutions** | ce-plan | AS 最擅长产出 PRD 文档 |
| "我的系统涉及 AI/LLM/RAG，需要架构指导" | **architecture-copilot** | — | 只有 AC 有 AI 系统专项模板和成本估算 |
| "我想系统性地学习和练习架构设计" | **architecture-copilot** | — | 教练模式最适合学习 |
| "已有代码库，重构前需要架构分析" | **architecting-solutions** | ce-architecture-strategist | AS 的代码分析步骤 + ce 的审查 agent |
| "端到端：从想法到代码到上线" | **gstack 全流程** | AC(架构) + sp(纪律) + ce(审查) | gstack 管总流程，专项专家补位 |

---

## 五、架构维度能力对比总表

| 能力 | gstack | compound-eng | superpowers | arch-copilot | arch-solutions |
|------|--------|-------------|-------------|-------------|---------------|
| 苏格拉底式引导 | — | — | — | ★★★★★ | — |
| PRD 产出 | — | ★★★ (ce-plan) | ★★ (brainstorming) | — | ★★★★★ |
| 代码级方案设计 | — | ★★★★ (ce-plan) | ★★★ (writing-plans) | — | ★★★★ |
| 系统级架构方法论 | ★★★ (/plan-eng) | ★★ (ce-arch-strategist) | — | ★★★★★ | ★★ |
| 质量属性系统分析 | ★★★ | — | — | ★★★★★ | ★ |
| 信封背面估算 | — | — | — | ★★★★★ | — |
| ADR 决策记录 | — | — | — | ★★★★★ | — |
| 25 个系统模板 | — | — | — | ★★★★★ | — |
| AI 系统专项 | ★★ | — | — | ★★★★★ | — |
| 反挑战/死穴分析 | ★★★ | ★★★ (adversarial reviewer) | — | ★★★★★ | — |
| 架构图 (ASCII) | ★★★ | — | — | ★★★★★ | ★★ |
| 演进路线规划 | ★★ | — | — | ★★★★★ | — |
| 代码库分析 (grep/find) | ★★ | ★★★★ | — | — | ★★★★★ |
| React/Hook 专项 | — | — | — | — | ★★★★ |
| 多方案对比 | ★★★★ | ★★ | ★★ | ★★★ | ★★★★★ |
| 跨模型架构审查 | ★★★★ (/codex) | — | — | — | — |

---

## 六、推荐的协同工作流

### 工作流 1：从零开始的新产品

```
architecture-copilot (阶段 0-7)
  产出：一句话定位 + 架构全景图 + ADR + 风险清单
    ↓
gstack /autoplan
  产出：CEO + Design + Eng + DX 全维度评审报告
    ↓
architecting-solutions
  产出：docs/xxx-prd.md (具体实现方案)
    ↓
superpowers brainstorming → writing-plans
  产出：详细 spec + 任务拆解
    ↓
superpowers SDD + TDD
  产出：代码 (纪律化实现)
    ↓
ce-code-review
  产出：14 维度代码审查
    ↓
gstack /qa → /ship → /land-and-deploy
  产出：上线
    ↓
ce-compound
  产出：docs/solutions/ 知识沉淀
```

### 工作流 2：现有代码库的功能扩展

```
architecting-solutions (分析现有代码 → 3 方案 → PRD)
    ↓
architecture-copilot 读图模式 (审 PRD：本质/全景/取舍/死穴)
    ↓
ce-plan → ce-work → ce-code-review
    ↓
gstack /qa → /ship
    ↓
ce-compound
```

### 工作流 3：架构评审（已有方案）

```
architecture-copilot 读图模式
  产出：结论/关键风险/必问问题/建议补的 ADR/下一步验证
    ↓
gstack /plan-eng-review (补充工程维度)
    ↓
gstack /autoplan (如需要设计+DX维度)
    ↓
architecting-solutions (如评审判定需要重写方案)
```

---

## 七、总结

### 五句话记住五个系统

| 系统 | 记住这句 |
|------|---------|
| **gstack** | 从想法到上线，你有 **一支 23 人专家团队** |
| **compound-engineering** | 每次工作都让下次更容易——**知识复利** |
| **superpowers** | AI 会走捷径，**铁律**让它走不了 |
| **architecture-copilot** | 不给你答案，**问你问题**直到你想清楚 |
| **architecting-solutions** | 分析你的代码，**写好 PRD** 等你审批 |

### 最重要的协同原则

> **架构层** (AC + AS) 想清楚做什么、怎么做 →
> **流程层** (gstack + ce + sp) 把它做出来、审清楚、推上线、沉淀好

五个系统不冲突——它们在不同层次、不同阶段解决不同问题。选一个流程平台为主力，用架构专家补充你最缺的深度。
