# 三相变压器参数推荐系统设计文档

## 一、Why — 为什么做

### 1.1 现状：暴力穷举，99% 迭代无效(已经有一定的剪枝策略，但是仍然很多)

三相优化计算是一个 10 层嵌套循环结构：

```
硅钢片牌号 × LVT × 铁心直径 × 低压线厚 × 低压线宽 ×
低压层数 × 高压线厚 × 高压线宽 × 高压层数 × 油箱参数
```

每层 5-50 个候选值，乘起来有百万次甚至10^16 量级 `calculate()` 调用，每次 `calculate()` 有1000多行代码执行，而最终产生一个 `complianceLevel=FULL` 的合理方案只需要几万条——超过 99% 的计算迭代在碰运气。

问题不在计算引擎本身——引擎能算出正确结果，**问题在搜索空间**。每个方案建好后，优化范围参数（铁心直径、低压匝数、绕线高度、磁通密度）由人工凭经验设置，范围宽则迭代量巨大。典型例子：铁心直径设 200-400mm，实际最优值永远落在 350-395 之间——200-349 那 30 步全是白算的。

### 1.2 候选方案对比

解决搜索空间过大的问题有四种可能路径：

| 方案 | 思路 | 优点 | 致命缺陷 |
|---|---|---|---|
| **A. 模型替代计算** | 用 ML 模型直接预测最优参数，跳过穷举循环 | 速度极快，毫秒级出结果 | 预测值可能与物理计算不一致，存在偏差风险；客户验收时需要可复现的计算过程，模型黑盒无法解释；任何一个预测错误都会导致设计报废 |
| **B. 启发式剪枝** | 在循环中途根据中间结果跳过后续层级 | 改动小，不改搜索范围 | 剪枝条件无法穷尽所有情况，可能误杀有效方案；铁心直径第一轮算出的空载损耗高，但后面可以靠优化绕组补偿——过早剪枝看不到全局 |
| **C. 缩小搜索范围（当前方案）** | 用历史数据学习哪些参数范围更可能出 FULL 结果，推荐用户缩小范围后交计算引擎正常跑 | 计算引擎逻辑完全不变，结果零偏移；可解释（推荐基于 N 条相似历史记录）；用户可选择是否采纳 | 需要历史数据积累；冷启动时依赖人工经验兜底 |
| **D. 混合模型** | 模型预测 + 小范围搜索兜底 | 兼顾速度与精度 | 复杂度高，两个系统需要维护同步 |

**选择 C 的原因**：它不改变计算引擎的一行代码。计算引擎已经经过充分验证，能保证结果的物理正确性。方案 A 的风险在于——如果模型预测的铁心直径是 370mm，但物理公式算出来的最优值是 365mm，这个 5mm 偏差可能在阻抗验证时导致方案不合格，。方案 C 不存在这个问题：它只是把搜索范围从 [200,400] 缩小到 [350,390]，365 和 370 都在里面，引擎自己会找到真正的 365。

### 1.3 核心思路

```
历史 FULL 记录                   新方案
      │                              │
      ▼                              ▼
方差归约 → 特征重要度权重     提取 22 维输入特征
      │                              │
      ▼                              ▼
  权重存表  ←──────────→  加权相似度匹配历史记录
      │                              │
      ▼                              ▼
  回测验证覆盖率             Top-N 记录 → 三组推荐范围
      │                              │
      ▼                              ▼
  前端确认更新                用户选一组填入优化范围
                                        │
                                        ▼
                              计算引擎正常跑（结果零偏移）
```

---

## 二、What — 做什么

### 2.1 目标

新建方案后，用户点击"智能推荐"，系统基于历史 FULL 级计算记录自动给出铁心直径、低压匝数、绕线高度等 5 个关键参数的推荐范围，替代手工设置(后续可拓展更多的外层循环参数)。

### 2.2 两条链

**权重计算链**：从 FULL 记录中提取 22 维输入特征和 5 维输出参数，用方差归约计算每个特征对每个输出参数的重要度，存权重表。附带回测验证新权重覆盖率，前端确认后生效。

**推荐链**：读当前生效权重 → 硬门槛筛选历史记录 → 加权相似度排序 → 取 Top-N 统计输出参数分布 → 返回三组推荐范围。

### 2.3 对计算引擎的影响

零。推荐改变的是优化范围的输入值，计算引擎的 10 层循环逻辑、物理公式、验证条件全部不变。推荐范围比人工范围窄，意味着引擎跑完全一样的过程，但迭代次数大幅减少。物理结果与使用人工范围一致，只是更快。

## 三、How — 详细设计

### 3.1 输入特征（22 维，从方案配置提取）

| 分组 | 数量 | 特征 | 来源字段 | 类型 |
|---|---|---|---|---|
| 硬门槛 | 4 | HVLVWM2 | `PerformanceIndex.windingConnection` | 枚举 |
| | | LVWG | `CraftLowCoil.wireSpecification` | 枚举 |
| | | HVWG | `CraftHighCoil.wireSpecification` | 枚举 |
| | | HZ | `PerformanceIndex.frequency` | 0/1 |
| 性能指标 | 6 | P（容量） | `PerformanceIndex.capacity` | 数值 |
| | | HVN | `PerformanceIndex.highVoltageRated` | 数值 |
| | | LVN | `PerformanceIndex.lowVoltageRated` | 数值 |
| | | P0 | `PerformanceIndex.noLoadStandard` | 数值 |
| | | PK | `PerformanceIndex.loadStandard` | 数值 |
| | | UK | `PerformanceIndex.impedanceStandard` | 数值 |
| 绕法 | 2 | HVLVWM1 | `PerformanceIndex.windingMethodType` | 枚举 |
| | | CORETYPE | `CraftCore.isRolledCore` | 0/1 |
| 油道 | 4 | HV 油道数量 | `CraftHighCoil.channelCount` | 数组 |
| | | HV 油道类型 | `CraftHighCoil.channelType` | 数组 |
| | | LV 油道数量 | `CraftLowCoil.channelCount` | 数组 |
| | | LV 油道类型 | `CraftLowCoil.channelType` | 数组 |
| 并绕 | 4 | LVAPN | `CraftLowCoil.axialWindings` | 1/2 |
| | | LVRPN | `CraftLowCoil.radialWindings` | 1/2 |
| | | HVAPN | `CraftHighCoil.axialWindingCount` | 1/2 |
| | | HVRPN | `CraftHighCoil.radialWindingCount` | 1/2 |
| 绕制系数 | 2 | LVARC | `CraftLowCoil.axialWindingCoefficient` | 数值 |
| | | HVARC | `CraftHighCoil.axialWindingCoefficient` | 数值 |


> **已知权衡**：
> - 权重均值聚合可能稀释单目标强特征（某特征对 CRGOD=0.9 但对其他=0，聚合后仅 0.18）。当前取均值保证排序稳定性，后续可评估加权方案。
> - 等频分桶对容量等离散标准值不精确（500 和 800 可能同一桶），可考虑按实际物理意义的手动分桶。
> - min/max 相似度只看比例，100→200 和 1000→1100 的绝对差不同但 sim 差异大。对容量和电压可改用绝对距离归一化。
> - 油道数组组合可能产生稀疏组，方差归约时标注组内记录数 < 3 的组为不可靠。
> - 相似度百分比 = score / max_possible_score × 100%，其中 max_possible_score = Σ(importance_agg[f] × 1)，即所有特征完全匹配时的理想分。

> **排除说明**：辐向绕制系数 LVSRC/HVSRC 仅参与辐向尺寸计算，不在 LVRH/HVRH 公式中，因此不纳入推荐特征。绝缘参数、油箱参数、材料单价等亦不参与 5 个输出的计算。

### 3.2 输出参数与循环结构的关系

5 个推荐输出在计算引擎中的角色分为两类：

| 输出 | 角色 | 类型 |
|---|---|---|
| CRGOD 铁心直径 | 第 3 层循环变量 | 直接控制循环步数 |
| LVT 低压匝数 | 第 2 层循环变量 | 直接控制循环步数 |
| LVRH 低压绕线高度 | 第 9 层计算值,超出范围即 reject | 约束(跳过内层循环) |
| HVRH 高压绕线高度 | 第 9 层计算值,超出范围即 reject | 约束(跳过内层循环) |
| CT 磁通密度 | 第 3 层计算值,超出范围即 reject | 约束(跳过绝大部分循环) |

缩小 CRGOD/LVT 直接减少循环步数。主要计算逻辑在循环计算最内层，缩小 LVRH/HVRH/CT 让更多组合在第 3/9 层提前 reject，跳过后续深度循环。CT 在最早节点拦截，是最关键的约束参数。

### 3.3 推荐输出（5 维）

| 输出 | 字段名 | 单位 | 搜索空间大小（典型值） |
|---|---|---|---|
| 铁心直径 | `crgod` | mm | 200-400 → 40 步 |
| 低压匝数 | `lvt` | 匝 | 5-30 → 26 步 |
| 低压绕线高度 | `lvrh` | mm | 400-1200 |
| 高压绕线高度 | `hvrh` | mm | 400-1200 |
| 磁通密度 | `ct` | T | 0.9-1.7 |

---

### 3.4 权重计算

### 3.4.1 数据准备

从三张表联查——方案配置取 22 维输入特征，方案记录取 5 维输出参数，只取 `compliance_level = 'FULL'` 的完整计算记录（每个 config 只保留价格最低的一条，取最低价记录：消除同一 config 多次运行的统计偏差，同时使推荐偏向最优成本方案）：

> **注**：一个 scheme_config 可对应多条 FULL record（多次优化运行）。这些记录共享相同输入特征但输出参数不同，会在方差归约中扎堆在同一分桶组内。若单个 config 平均产生多条记录，应在计算前按 config 去重（每个 config 只保留价格最低的一条），避免聚类偏差。

```sql
SELECT
    -- 性能指标 (6): capacity, HVN, LVN, P0, PK, UK
    c.performanceIndex->>'$.capacity'              AS P,
    c.performanceIndex->>'$.highVoltageRated'       AS hvn,
    c.performanceIndex->>'$.lowVoltageRated'        AS lvn,
    c.performanceIndex->>'$.noLoadStandard'         AS p0,
    c.performanceIndex->>'$.loadStandard'           AS pk,
    c.performanceIndex->>'$.impedanceStandard'      AS uk,
    -- 硬门槛 (4): HVLVWM2, HZ, LVWG, HVWG
    c.performanceIndex->>'$.windingConnection'      AS hvlvwm2,
    c.performanceIndex->>'$.frequency'              AS hz,
    c.craftLowCoil->>'$.wireSpecification'          AS lvwg,
    c.craftHighCoil->>'$.wireSpecification'         AS hvwg,
    -- 绕法 (2): HVLVWM1, CORETYPE
    c.performanceIndex->>'$.windingMethodType'      AS hvlvwm1,
    c.craftCore->>'$.isRolledCore'                  AS coretype,
    -- 高压线圈 (5): 油道/并绕/系数
    c.craftHighCoil->>'$.channelCount'              AS hv_ch_cnt,
    c.craftHighCoil->>'$.channelType'               AS hv_ch_type,
    c.craftHighCoil->>'$.axialWindingCount'         AS hvapn,
    c.craftHighCoil->>'$.radialWindingCount'        AS hvrpn,
    c.craftHighCoil->>'$.axialWindingCoefficient'   AS hvarc,
    -- 低压线圈 (5): 油道/并绕/系数
    c.craftLowCoil->>'$.channelCount'               AS lv_ch_cnt,
    c.craftLowCoil->>'$.channelType'                AS lv_ch_type,
    c.craftLowCoil->>'$.axialWindings'              AS lvapn,
    c.craftLowCoil->>'$.radialWindings'             AS lvrpn,
    c.craftLowCoil->>'$.axialWindingCoefficient'    AS lvarc,
    -- 输出参数 (5)
    r.schemeData->>'$.crgod'                        AS crgod,
    r.schemeData->>'$.lvt'                          AS lvt,
    r.schemeData->>'$.lvrh'                         AS lvrh,
    r.schemeData->>'$.hvrh'                         AS hvrh,
    r.schemeData->>'$.ct'                           AS ct
FROM tb_scheme_config_three_phase c
-- 注: ->> 返回字符串，P/HVN/LVN/P0/PK/UK 等数值字段需在应用层 CAST 为数值类型
JOIN tb_scheme_record_three_phase r ON r.scheme_config_id = c.id
WHERE r.compliance_level = 'FULL'
  AND r.is_deleted = 0 AND c.is_deleted = 0
```

### 3.4.2 特征分桶规则

| 特征类型 | 条件 | 分桶方式 |
|---|---|---|
| 硬门槛（枚举） | 值域 ≤ 5 个不同值 | 按枚举值直接分组 |
| 小整数 | 值域 ≤ 3 个不同值 | 按值分组 |
| 数值连续 | 其余 | 等频分 5 桶（每桶记录数大致相等） |
| 数组（油道） | 多选值 | 按数组元素组合分组（如 [0,1], [1,2] 各为一组） |

### 3.4.3 方差归约公式

对每一个输出参数 Y（如 CRGOD）和每一个输入特征 X（如 P），计算 X 对 Y 的方差归约重要度：

```
    全局方差    global_var = Σ(y_i - mean)² / N

    按 X 分组   group_var_g = Σ(y_j - mean_g)² / n_g          # 第 g 组组内方差
    加权平均    residual_var = Σ(n_g × group_var_g) / N        # 分组后剩余的方差

    重要度      importance = (global_var - residual_var) / global_var

    取值范围    0 ≤ importance ≤ 1
               0 = 该特征对 Y 无解释力（分组后方差不变）
               1 = 该特征完全解释了 Y 的方差（组内无差异）
```

**直观解释**：如果 global_var = 100，按容量分桶后各组内平均方差降到 38，则容量对铁心直径的重要度 = (100-38)/100 = 0.62。意味着"知道容量"能帮你消除 62% 的不确定性。

> **注意**：方差归约天然偏向高基数特征。分 5 桶的连续特征比二分特征（如 CORETYPE 0/1）拥有更多分组，即使无预测力其 residual_var 也因分组更细而偏低，importance 虚高。因此不同特征间的 importance 绝对值不可直接比较，应在同一特征类型内（连续型 vs 连续型、二分类 vs 二分类）做相对排序。后续可改用效应量指标（如 ω²）修正此偏差。

### 3.4.4 边界处理

| 情况 | 原因 | 处理 |
|---|---|---|
| X 只有 1 个值（如全 50Hz） | 分组前后方差不变 | importance = 0 |
| 某组仅 1 条记录 | 无法计算组内方差 | 丢弃该组，不计入加权平均 |
| global_var = 0（所有 Y 相同） | 分母为零 | importance = 0，无需推荐 |
| importance < 0（方差反而变大了） | 随机噪声 | 取 0 |

### 3.4.5 回测

每次重算权重后自动跑回测，验证新权重质量：

```
步骤：
  1. 全量 FULL 记录按 create_time 排序
  2. 前 80% 作为训练集，后 20% 作为验证集（时间切分，模拟真实泛化）
  3. 训练集计算权重，对验证集每条记录分别用三种策略做推荐，各自统计覆盖率
  4. 统计每个输出参数的覆盖率：

      覆盖率 = 验证集实际值落在推荐范围内的记录数 / 验证集总记录数

  5. 同时用当前生效权重对验证集做一次推荐，得到旧权重覆盖率
```

### 3.4.6 存储

表 `tb_feature_weight`，每次重算生成新 version，初始 `is_active = 0`。表结构见 [3.7 数据库](#37-数据库)。

用户确认后，旧 version 全部 `is_active = 0`，新 version 全部 `is_active = 1`。

### 3.5 推荐接口

### 3.5.1 权重聚合

权重表按 `(target_param, feature_name)` 存，即同一个特征 P 对 CRGOD 的重要度和对 LVT 的重要度不同。推荐排序时需要每个 feature 一个单一权重，取**均值**聚合：

```
importance_agg[f] = mean(importance[crgod][f], importance[lvt][f],
                         importance[lvrh][f], importance[hvrh][f],
                         importance[ct][f])
```

> 取均值而非 max，原因：均值对所有输出参数平等对待。若取 max，则某特征只对 CT 重要（但对其他 4 个无用）也会获得高权重，偏离推荐目标。

### 3.5.2 推荐流程

1. 读取当前生效权重（`is_active = 1`），取各 target_param 下该特征 importance 的均值作为聚合权重
2. 读取目标方案配置，提取 22 维输入特征
3. **硬门槛**筛选：HVLVWM2、LVWG、HVWG、HZ 必须完全相同
4. 若匹配记录数不足，执行**降级策略**（见 3.5.3）
5. 对通过门槛的每条历史记录计算**加权相似度分**：

```
score = Σ( importance_agg[f] × sim(f_target, f_history) )

其中：
  枚举特征: sim = 1（相同）| 0（不同）
  数组特征（油道）: sim = Jaccard 相似度（交集 / 并集）
  数值特征: sim = min(v_target, v_history) / max(v_target, v_history)
            防御：任一 null→sim=0；两者同为 0→sim=1（完全一致）；仅一侧为 0→sim=0
```

> 数值相似度用 min/max 替代原来的 ratio 公式，保证对称性：A 对 B 的相似度 = B 对 A 的相似度。零值由防御规则统一处理（两零→1，一零→0）。

6. 按 score 降序排列，取 Top-N 条历史记录
7. 统计这 N 条的输出参数分布，生成推荐范围

### 3.5.3 硬门槛降级策略

4 个硬门槛筛选后，候选池可能不足 K 条。候选池共享，三个策略各自带 degradation_level，降级触发按各自的 K（精准=5/标准=10/广泛=15）：

| 序号 | 放宽动作 | 说明 |
|---|---|---|
| 0 | 全部匹配 | 首选 |
| 1 | 去掉 HVWG | 高压线规放宽，低压仍相同 |
| 2 | 去掉 LVWG | 线规全部放宽 |
| 3 | 去掉 HZ | 仅保留 HVLVWM2，最终兜底 |

每降一级前检查是否满足最少需要量 K：

| 策略 | 最少需要 K |
|---|---|
| 精准 | 5 条 |
| 标准 | 10 条 |
| 广泛 | 15 条 |

API 返回结果中三个策略各自带 `degradation_level`：0 = 全匹配 / 1 = 去掉 HVWG / 2 = 去掉 LVWG / 3 = 仅保留 HVLVWM2。前端展示时标注"推荐可信度：高/中/低"对应 degradation_level 0 / 1-2 / 3。

### 3.5.4 三组推荐策略

| 策略 | N | 最少需要 | 推荐范围 | 用途 |
|---|---|---|---|---|
| **精准** | 5 | 5 | min ~ max（最窄） | 数据充足且有高相似度记录时首选 |
| **标准** | 20 | 10 | mean ± 1σ | 一般场景，平衡精度与覆盖 |
| **广泛** | 50 | 15 | mean ± 2σ（兜底） | 数据稀疏时保证命中，范围最宽 |

如果降级到最终仍不够最少需要量，该策略返回空，并在 API 响应中标记 `insufficient_data: true`。前端展示"该策略数据不足，请使用其他策略或手动设置"。

### 3.5.5 推荐结果示例

```
精准推荐（基于 5 条记录，最高相似度 94%）
  CRGOD: [350, 390] mm     当前方案原范围: [200, 400] mm
  LVT:   [10, 14] 匝        当前方案原范围: [5, 30] 匝
  LVRH:  [580, 650] mm     当前方案原范围: [400, 1000] mm
  HVRH:  [550, 620] mm     当前方案原范围: [400, 1000] mm
  CT:    [1.62, 1.68] T    当前方案原范围: [0.9, 1.7] T
```

### 3.5.6 API

| 方法 | 路径 | 入参 | 返回 |
|---|---|---|---|
| `GET` | `/schemeConfig/{id}/param-suggestions` | 方案 ID | 三组推荐参数 + 元信息 |
| `POST` | `/param-suggestions/recalculate` | — | 新权重 + 新旧回测对比 |
| `POST` | `/param-suggestions/confirm` | `{version: N}` | 确认结果 |

`recalculate` 返回的结构：

```json
{
  "newVersion": 3,
  "sampleCount": 187,
  "backtest": {
    "new_coverage": {
      "crgod": 0.94, "lvt": 0.88, "lvrh": 0.82, "hvrh": 0.79, "ct": 0.91
    },
    "old_coverage": {
      "crgod": 0.91, "lvt": 0.90, "lvrh": 0.85, "hvrh": 0.81, "ct": 0.89
    },
    "coverage_by_strategy": {
      "strict":   {"crgod": 0.85, "lvt": 0.76, "lvrh": 0.70, "hvrh": 0.65, "ct": 0.80},
      "standard": {"crgod": 0.94, "lvt": 0.88, "lvrh": 0.82, "hvrh": 0.79, "ct": 0.91},
      "loose":    {"crgod": 0.98, "lvt": 0.95, "lvrh": 0.91, "hvrh": 0.89, "ct": 0.97}
    }
  },
  "weights": [
    {"target_param": "crgod", "feature_name": "P", "importance": 0.562},
    {"target_param": "crgod", "feature_name": "hvn", "importance": 0.231}
  ]
}
```

> 策略 key 映射：`strict` = 精准，`standard` = 标准，`loose` = 广泛。前端 Tab 用中文展示，调 API 用英文 key。

---

### 3.6 前端方案

### 3.6.1 入口

方案编辑页（优化设计 > 方案管理 > 编辑方案），在"优化范围"配置区域上方，增加两个按钮：

- **"智能推荐"** — 主按钮，点击对当前方案生成推荐
- **"权重管理"** — 文字按钮，点击进入权重管理

### 3.6.2 推荐弹窗

弹窗宽度约 700px，顶部为三组推荐 Tab（精准 / 标准 / 广泛），中间展示推荐参数表格，底部为操作区。

**表格列**：

| 参数名 | 原范围 | 推荐范围 | 缩小比例 (1 - new/old) |
|---|---|---|---|
| 铁心直径 | 200 ~ 400 mm | 350 ~ 390 mm | 缩小 80% |
| 低压匝数 | 5 ~ 30 匝 | 10 ~ 14 匝 | 缩小 84% |
| ... | | | |

**底部信息栏**：

```
基于 [187] 条历史记录 | 权重版本 v3 | 最高相似度 94%
```

**底部操作**：`[应用精准] [应用标准] [应用广泛] [关闭]`

### 3.6.3 权重管理弹窗

弹窗宽度约 800px，顶部"重新计算权重"按钮，中间为权重对比 + 回测对比，底部确认/取消。

**权重对比区**（按 target_param 分组，左右两栏）：

```
┌─ CRGOD 铁心直径 ──────────────────────┐
│  特征      旧权重    新权重    变化                          │
│  P         0.543    0.562    +0.019                          │
│  HVN       0.225    0.231    +0.006                          │
│  CORETYPE  0.031    0.028    -0.003                          │
│  ...                                                         │
└───────────────────────────────┘
```

**回测对比区**（关键！用户决策依据）：

| 输出参数 | 旧权重覆盖率 | 新权重覆盖率 | 变化 |
|---|---|---|---|
| CRGOD 铁心直径 | 91% | 94% | +3% |
| LVT 低压匝数 | 90% | 88% | -2% |
| LVRH 低压高度 | 85% | 82% | -3% |
| HVRH 高压高度 | 81% | 79% | -2% |
| CT 磁通密度 | 89% | 91% | +2% |
| **综合** | **87.2%** | **86.8%** | **-0.4%** |

用户看到 LVT/LVRH/HVRH 覆盖率略降、CRGOD/CT 提升，综合几乎持平，自行决定是否更新。

**底部操作**：`[确认更新权重] [取消]`

### 3.6.4 交互流程

```
方案编辑页
  ├─ 点"智能推荐"
  │    ├─ 无生效权重 → 提示"暂无权重数据，请先计算权重" → 引导去"权重管理"
  │    └─ 有权重 → 弹推荐结果 → 选一组 → 填入优化范围
  │
  └─ 点"权重管理"
       ├─ 展示当前生效权重版本 + 历史版本列表
       ├─ 点"重新计算" → 后端跑方差归约 + 回测 → 返回新旧对比
       ├─ 用户审阅覆盖率变化
       ├─ 点"确认更新" → 旧版本 is_active=0，新版本 is_active=1
       └─ 点"取消" → 不修改
```

---

### 3.7 数据库

```sql
CREATE TABLE tb_feature_weight (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT,
    target_param  VARCHAR(32)     NOT NULL COMMENT 'CRGOD/LVT/LVRH/HVRH/CT',
    feature_name  VARCHAR(64)     NOT NULL COMMENT 'P/HVN/LVN/hvlvwm2/...',
    importance    DECIMAL(10,6)   NOT NULL DEFAULT 0 COMMENT '重要度 0~1',
    source        VARCHAR(16)     NOT NULL DEFAULT 'data' COMMENT 'manual/data',
    version       INT             NOT NULL DEFAULT 1 COMMENT '权重版本号',
    sample_count  INT             NOT NULL DEFAULT 0 COMMENT '训练集记录数',
    is_active     TINYINT         NOT NULL DEFAULT 0 COMMENT '0待确认 1生效',
    create_time   DATETIME        DEFAULT CURRENT_TIMESTAMP,
    update_time   DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_version (version),
    INDEX idx_active_target (is_active, target_param),
    UNIQUE KEY uk_version_param_feat (version, target_param, feature_name)
) COMMENT '特征重要度权重表';
```

- `source = 'manual'`：冷启动专家权重，初始 is_active=1，确保首次使用即有可用权重
- `source = 'data'`：数据驱动权重，随 FULL 记录积累自动更新

---

## 四、Result — 预期效果与迭代

当前 v1 只推荐 5 个最外层循环参数（CRGOD、LVT、LVRH、HVRH、CT），直接缩小第 2-3 层循环（CRGOD/LVT），并通过约束参数在第 3/9 层提前短路（CT/LVRH/HVRH）。后续可沿以下方向深入。

### 4.1 内层参数推荐（v2）

外层推荐缩小了前 3 层循环，但 4-9 层（线厚、线宽、层数）仍遍历全量数据字典。历史充足后可扩展：

| 循环层 | 参数 | 当前候选规模 | 推荐目标 |
|---|---|---|---|
| 4 低压线厚 | InitLVILT | 箔材/扁线列表，30-80 | Top-10 线厚 |
| 5 低压线宽 | InitLVILW | 箔材/扁线列表，10-30 | Top-5 线宽 |
| 7 高压线厚 | InitHVILT | 圆线/扁线列表，20-50 | Top-10 线厚 |
| 8 高压线宽 | InitHVILW | 扁线列表，10-20 | Top-5 线宽 |
| 9 高压层数 | HVL | [HVLMIN, HVLMAX] | 推荐范围 |

> 第 6 层（LVL）通常只有 1-2 个候选，不纳入推荐。第 10 层（油箱参数）对外层无影响，暂不推荐。

内层推荐的输入特征除 22 维方案参数外，额外加入外层实际取值（CRGOD/LVT/CT），构成二级级联推荐。

### 4.2 有监督模型（v3）

方差归约为监督式关联度量。FULL 记录超过 500 条后可升级为 XGBoost 多输出回归——输入 22 维参数 + 外层推荐值，输出最优线厚、线宽、层数组合。Java 侧通过 PMML 文件加载，毫秒级推理。

### 4.3 失败路径学习

每个被 reject 的 WorkItem 携带失败原因（磁通密度超限/高度超限/温升超限），将其与参数组合关联存储。推荐时标记相似方案的高频失败区域，推荐范围自动避开。

### 4.4 冷启动

初次部署时预置人工专家权重（version=0, source='manual', is_active=1）和一批代表性历史记录（≥20 条，覆盖常见容量/电压/绕法组合），确保推荐链有数据可匹配。

**专家规则**：按容量分档给出固定推荐范围，由人工经验维护，表结构如下：

| 容量范围 kVA | 绕法 | CRGOD mm | LVT 匝 | LVRH mm | HVRH mm | CT T |
|---|---|---|---|---|---|---|
| 500-800 | Ddyn11 | 300-360 | 16-24 | 450-650 | 420-600 | 1.55-1.68 |
| 800-1250 | Ddyn11 | 330-390 | 12-20 | 500-700 | 470-650 | 1.55-1.68 |
| ... | ... | ... | ... | ... | ... | ... |

历史记录 < 20 条时走专家规则，不走相似度匹配。专家规则表随实际数据积累逐步替换为数据驱动权重。参见 3.6.4 交互流程。

### 4.5 单相推广

单相计算循环结构与三相高度相似，直接复用方差归约 + 加权推荐框架，仅需替换特征映射表和输出参数表。
