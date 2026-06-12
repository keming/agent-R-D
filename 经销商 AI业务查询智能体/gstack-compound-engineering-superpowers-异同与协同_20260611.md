# gstack、Compound Engineering、Superpowers 的异同与协同使用

日期：2026-06-11

## 一句话结论

这三者不是同一类东西：

- **Superpowers** 更像“纪律层”：强制 AI Agent 在动手前先用合适的技能、先澄清、先计划、必要时先测试。
- **Compound Engineering** 更像“工程操作系统”：把想法、需求、计划、实现、评审、打磨、沉淀串成可重复循环。
- **gstack** 更像“专家角色包”：把一个通用 Agent 拆成 CEO、工程经理、设计、QA、发布、调试等不同视角来审视工作。

最好的协同方式不是三套流程同时启动，而是分层使用：

> Superpowers 定规矩，Compound Engineering 跑主流程，gstack 补专家视角。

## 三者各自解决什么问题

### 1. Superpowers：防止 Agent 乱来

Superpowers 的核心价值不是“多几个命令”，而是把人类高级工程师的工作纪律固化进 Agent 行为中。

它解决的问题：

- Agent 一上来就写代码，不问清楚需求。
- 没有测试，没有回归验证。
- 计划没评审，边写边猜。
- 明明有适用技能，却靠临场发挥。
- 会话中断或上下文丢失后，工作方法漂移。

适合用在：

- 需求还不清楚时，先进入 brainstorming / planning。
- 需要 TDD 或严格验证的代码任务。
- 调试复杂问题时，要求系统化定位根因。
- 创建或修改技能时，用技能自身的方法论保证质量。

不适合单独承担：

- 多角色代码评审。
- 大规模并行代理协作。
- 长期工程知识沉淀。
- 产品、设计、发布等跨角色工作流。

### 2. Compound Engineering：让每次工作都让系统变聪明

Compound Engineering 的核心不是“让 Agent 写更多代码”，而是让每个需求、bug、评审和经验都沉淀成下一次可复用的上下文。

它解决的问题：

- 每次和 AI 协作都像从零开始。
- 代码评审意见没有沉淀，下次继续犯同样错误。
- 需求、计划、实现和复盘断裂。
- 团队规范只存在人脑里，没有变成 Agent 可读取的规则。
- Agent 能干活，但不能持续改进。

典型循环：

```text
Ideate → Brainstorm → Plan → Work → Review → Polish → Compound → Repeat
```

在项目中通常对应：

```text
AGENTS.md / CLAUDE.md       常驻项目规则
docs/brainstorms/           需求与问题定义
docs/plans/                 实施计划
docs/solutions/             可复用经验、模式、踩坑记录
code review agents          多视角评审
specialized agents          研究、性能、安全、测试、设计等分工
```

适合用在：

- 正式工程任务。
- 需要从需求到 PR 的完整闭环。
- 需要多 Agent 评审、测试、研究。
- 需要把成功经验和失败教训写回项目记忆。
- 企业项目、长期项目、多人协作项目。

不适合单独承担：

- 极短的一次性问答。
- 没有 repo、没有可沉淀上下文的临时任务。
- 纯角色扮演式的“CEO/设计/QA 视角”审查。

### 3. gstack：把 Agent 变成一组专家角色

gstack 的核心价值是角色化：让 AI 不再只是“一个会写代码的人”，而是在不同阶段切换为 CEO reviewer、engineering manager、designer、QA lead、release engineer、debugger 等专家视角。

它解决的问题：

- Agent 只按实现者视角思考，缺少产品、质量、发布、安全等横向审视。
- 计划看起来能做，但没有 CEO/业务视角拷问价值。
- 代码能跑，但没有 QA 视角找边界。
- UI 能显示，但没有设计视角挑体验。
- 发布前没有 release manager 视角检查风险。

适合用在：

- 方案评审。
- 产品方向审查。
- UI/UX 质检。
- 发布前检查。
- QA 测试计划。
- 让不同角色对同一方案提出挑战。

不适合单独承担：

- 严格 TDD。
- 长期工程记忆沉淀。
- 企业级流程治理。
- 项目级知识库与复盘系统。

## 对比表

| 维度 | Superpowers | Compound Engineering | gstack |
| --- | --- | --- | --- |
| 核心定位 | 方法纪律与技能触发 | 工程循环与知识复利 | 专家角色与多视角审查 |
| 主要问题 | Agent 不按流程、不测试、不澄清 | 每次协作不沉淀，工程能力不复利 | 通用 Agent 缺少产品/设计/QA/发布视角 |
| 抽象层级 | 工作方法层 | 工程系统层 | 角色视角层 |
| 主要形态 | composable skills + instructions | plugin + skills + agents + docs 结构 | SKILL.md 角色包 / slash command 工作流 |
| 主流程能力 | 强 | 很强 | 中 |
| 角色评审能力 | 中 | 强 | 很强 |
| 长期记忆沉淀 | 中 | 很强 | 弱到中 |
| TDD/验证纪律 | 很强 | 强 | 中 |
| 产品/业务挑战 | 中 | 强 | 很强 |
| 企业项目适配 | 适合作为底层纪律 | 适合作为主工作流 | 适合作为评审补充 |
| 最大风险 | 太机械，简单任务也变重 | 流程较重，需要持续维护 | 角色很多，容易和主流程打架 |

## 推荐协同架构

### 分层模型

```text
┌──────────────────────────────────────┐
│ gstack：专家角色层                     │
│ CEO / EM / Designer / QA / Release    │
│ 作用：挑战、评审、补盲区                │
└──────────────────────────────────────┘
                  ▲
                  │ 在关键节点调用
                  │
┌──────────────────────────────────────┐
│ Compound Engineering：工程主流程层      │
│ Ideate / Brainstorm / Plan / Work      │
│ Review / Polish / Compound             │
│ 作用：把工作从想法推进到可交付并沉淀      │
└──────────────────────────────────────┘
                  ▲
                  │ 全程受约束
                  │
┌──────────────────────────────────────┐
│ Superpowers：纪律与技能触发层           │
│ 先问、先计划、先测试、先用技能           │
│ 作用：防止 Agent 跳步骤、乱发挥          │
└──────────────────────────────────────┘
```

### 协同原则

1. **只设一个主流程**

   日常工程任务以 Compound Engineering 为主流程。不要让 Superpowers、Compound Engineering、gstack 同时争夺“谁来指挥任务”。

2. **Superpowers 做底线，不做总指挥**

   它负责提醒 Agent：该用技能就用技能，该问问题就问问题，该测试就测试。它不负责定义完整工程生命周期。

3. **Compound Engineering 做项目记忆和工程闭环**

   正式任务从 brainstorm / plan / work / review / compound 走。任务结束后，必须问一句：这次有什么经验值得写进 AGENTS.md 或 docs/solutions？

4. **gstack 只在关键节点插入**

   不要每一步都叫 gstack。最有价值的节点是：

   - 需求成形后：CEO / Product 视角审查“值不值得做”。
   - 技术方案后：Engineering Manager / Architect 视角审查“复杂度是否合理”。
   - UI 出来后：Designer / QA 视角审查“体验是否像人用的”。
   - 发布前：Release Manager / QA 视角审查“会不会炸”。

5. **冲突时按项目规则优先**

   优先级建议：

   ```text
   用户明确指令
   > 项目 AGENTS.md / CLAUDE.md
   > 安全与合规要求
   > Compound Engineering 当前计划
   > Superpowers 技能纪律
   > gstack 角色建议
   ```

## 推荐工作流

### 场景 A：从 0 做一个新功能

```text
1. Superpowers
   触发 brainstorming / planning 纪律，先澄清问题。

2. Compound Engineering / ce-brainstorm
   输出需求文档：用户、问题、范围、成功标准、边界。

3. gstack CEO / Product reviewer
   审查这个功能是否值得做，是否和业务目标一致。

4. Compound Engineering / ce-plan
   输出实施计划：文件、模块、测试、风险、验证。

5. gstack Engineering Manager / Architect reviewer
   审查方案是否过度设计，边界是否清楚。

6. Compound Engineering / ce-work
   按计划实现，并执行测试。

7. Compound Engineering / ce-code-review
   多 Agent 代码审查。

8. gstack QA / Release reviewer
   从真实用户流程和发布风险角度再压一遍。

9. Compound Engineering / ce-compound
   把踩坑、模式、约束写回 docs/solutions 或 AGENTS.md。
```

### 场景 B：修一个复杂 bug

```text
1. Superpowers
   触发系统化 debugging：复现、假设、验证，不许乱改。

2. Compound Engineering / ce-debug
   查根因，补回归测试，修复。

3. gstack QA / Debugger
   从边界条件和用户路径补充反例。

4. Compound Engineering / ce-code-review
   审查修复是否引入副作用。

5. Compound Engineering / ce-compound
   写入“这个 bug 类别以后如何避免”。
```

### 场景 C：做架构方案或产品方案

```text
1. Superpowers
   要求先澄清约束，不直接画架构。

2. Compound Engineering / ce-brainstorm 或 ce-plan
   形成结构化方案：范围、约束、风险、路径。

3. gstack CEO / Architect / Security / QA
   分别挑战：
   - 是否解决真问题？
   - 架构是否太重？
   - 安全边界在哪里？
   - 上线后第一个失败点是什么？

4. Compound Engineering
   把最终决策沉淀成 ADR、AGENTS.md 规则、eval 门禁。
```

## 针对企业 Agent 项目的落地建议

对“经销商 AI 业务查询助手”这类企业 Agent 项目，推荐这样组合：

### 1. 用 Superpowers 守住工作纪律

每次做需求、代码、评审前，要求 Agent：

- 先读 AGENTS.md。
- 先识别是否有适用 skill。
- 信息不足时先问，不要猜。
- 涉及代码行为变化时，先定义验证方式。
- 涉及 AI 输出质量时，必须考虑 eval。

### 2. 用 Compound Engineering 管完整交付

建议建立项目结构：

```text
docs/
  brainstorms/      需求讨论与业务边界
  plans/            技术实施计划
  solutions/        可复用经验
  adr/              架构决策记录
evals/
  dealer-queries/   经销商常见问题黄金集
```

典型沉淀：

- “订单数据不能进向量库”写成 ADR。
- “dealer_id 必须来自登录态，不能来自模型抽取”写进 AGENTS.md。
- “模型不能编造价格、型号、订单状态”写成 eval 门禁。
- “配件适配必须有结构化适配依据”写成业务规则。

### 3. 用 gstack 做关键评审角色

对企业项目最值得引入的 gstack 角色视角：

- **CEO / Product**：这个 Agent 是否真能降低经销商时间成本？
- **Engineering Manager**：MVP 有没有过度平台化？
- **Architect**：工具边界、权限边界、数据一致性是否清楚？
- **Security**：经销商越权、提示注入、敏感订单泄露怎么防？
- **QA Lead**：无结果、模糊型号、错误适配、订单状态异常怎么测？
- **Release Manager**：上线灰度、回滚、监控、告警是否齐全？

## 不建议的用法

### 1. 三套都全量打开

结果会变成：

- 每个工具都想定义流程。
- Agent 反复计划，不动手。
- 角色评审太多，核心任务推进变慢。
- 用户被流程淹没。

### 2. 用 gstack 替代项目规范

gstack 的角色建议是通用专家视角，不了解您的行业、客户、数据和权限约束。企业项目必须以 AGENTS.md、ADR、eval 和真实业务数据为准。

### 3. 用 Superpowers 替代工程记忆

Superpowers 能保证“这一次别乱来”，但不能自动把“这一次学到的东西”变成项目资产。复利部分要靠 Compound Engineering。

### 4. 用 Compound Engineering 替代人类判断

Compound Engineering 可以把中间过程自动化，但最重要的两端仍然需要人：

- 开始时判断什么值得做。
- 结束时判断做出来的东西是否真的好。

## 我的推荐默认配置

如果只能选一个主轴：

> 以 Compound Engineering 为主轴。

如果要加纪律：

> 在 AGENTS.md 中吸收 Superpowers 的“先用技能、先澄清、先验证”规则。

如果要加评审：

> 在关键节点调用 gstack 角色，而不是让它接管全流程。

推荐默认协同方式：

```text
日常开发：
Superpowers 纪律
→ Compound Engineering 主流程
→ CE review
→ CE compound

重要功能：
Superpowers 纪律
→ CE brainstorm
→ gstack Product/CEO challenge
→ CE plan
→ gstack Architect/EM challenge
→ CE work
→ CE code-review
→ gstack QA/Release challenge
→ CE compound

企业 Agent / AI 产品：
Superpowers 纪律
→ CE strategy / brainstorm / plan
→ gstack Security / QA / Product challenge
→ CE eval / review / compound
```

## 最简心法

可以把三者理解成一句话：

> Superpowers 让 Agent 像受过训练的工程师；Compound Engineering 让团队越做越强；gstack 让同一个 Agent 暂时拥有一支专家评审团。

真正高效的组合不是“装更多工具”，而是明确分工：

- 谁定规矩？
- 谁跑主流程？
- 谁做挑战评审？
- 谁负责把经验写回系统？

只要这四个问题清楚，三者可以互补；如果这四个问题不清楚，三者会互相打架。

## 资料来源

- gstack GitHub：<https://github.com/garrytan/gstack>
- gstack AGENTS.md：<https://github.com/garrytan/gstack/blob/main/AGENTS.md>
- Superpowers GitHub：<https://github.com/obra/superpowers>
- Compound Engineering Plugin GitHub：<https://github.com/everyinc/compound-engineering-plugin>
- Compound Engineering 官方指南：<https://every.to/guides/compound-engineering>
- Compound Engineering 方法论文章：<https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents>

