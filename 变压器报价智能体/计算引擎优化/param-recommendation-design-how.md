# 三相变压器参数推荐系统设计文档

## 一、总体方案

### 1.1 目标

新建方案后，用户点击"智能推荐"，系统基于历史 `FULL` 级计算记录的特征重要度权重，自动给出铁心直径、低压匝数、绕线高度等 5 个关键优化范围参数的推荐值。用户选一组填入，替代手工设置，缩小搜索空间从而加速计算。

### 1.2 核心链路

```
                          ┌─ 权重计算链 ────────────────────────┐
                          │  FULL 记录 → 方差归约 → 权重表                             │
                          │              → 回测 → 覆盖率对比                           │
                          │              → 前端确认 → is_active=1                      │
                          └───────────────────────────────┘
                                          ↓ 权重驱动
                          ┌─ 推荐链 ─────────────────┐
新版方案 → 硬门槛筛选 → 加权相似度 → Top-N 历史记录 → 三组推荐范围  │
                          └──────────────────────┘
```

### 1.3 输入特征（22 维，从方案配置提取）

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

> **排除说明**：辐向绕制系数 LVSRC/HVSRC 仅参与辐向尺寸计算，不在 LVRH/HVRH 公式中，因此不纳入推荐特征。绝缘参数、油箱参数、材料单价等亦不参与 5 个输出的计算。

### 1.4 推荐输出（5 维）

| 输出 | 字段名 | 单位 | 搜索空间大小（典型值） |
|---|---|---|---|
| 铁心直径 | `crgod` | mm | 200-400 → 40 步 |
| 低压匝数 | `lvt` | 匝 | 5-30 → 26 步 |
| 低压绕线高度 | `lvrh` | mm | 400-1200 |
| 高压绕线高度 | `hvrh` | mm | 400-1200 |
| 磁通密度 | `ct` | T | 0.9-1.7 |

---

## 二、权重计算

### 2.1 数据准备

从三张表联查——方案配置取 22 维输入特征，方案记录取 5 维输出参数，只取 `compliance_level = 'FULL'` 的完整计算记录：

```sql
SELECT
    -- 性能指标 (6)
    c.performanceIndex->>'$.capacity'              AS P,
    c.performanceIndex->>'$.highVoltageRated'       AS hvn,
    c.performanceIndex->>'$.lowVoltageRated'        AS lvn,
    c.performanceIndex->>'$.noLoadStandard'         AS p0,
    c.performanceIndex->>'$.loadStandard'           AS pk,
    c.performanceIndex->>'$.impedanceStandard'      AS uk,
    -- 硬门槛 (4)
    c.performanceIndex->>'$.windingConnection'      AS hvlvwm2,
    c.performanceIndex->>'$.windingMethodType'      AS hvlvwm1,
    c.performanceIndex->>'$.frequency'              AS hz,
    -- 绕法 (1)
    c.craftCore->>'$.isRolledCore'                  AS coretype,
    -- 高压线圈 (5)
    c.craftHighCoil->>'$.channelCount'              AS hv_ch_cnt,
    c.craftHighCoil->>'$.channelType'               AS hv_ch_type,
    c.craftHighCoil->>'$.wireSpecification'         AS hvwg,
    c.craftHighCoil->>'$.axialWindingCount'         AS hvapn,
    c.craftHighCoil->>'$.radialWindingCount'        AS hvrpn,
    c.craftHighCoil->>'$.axialWindingCoefficient'   AS hvarc,
    -- 低压线圈 (5)
    c.craftLowCoil->>'$.channelCount'               AS lv_ch_cnt,
    c.craftLowCoil->>'$.channelType'                AS lv_ch_type,
    c.craftLowCoil->>'$.wireSpecification'          AS lvwg,
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
JOIN tb_scheme_record_three_phase r ON r.scheme_config_id = c.id
WHERE r.compliance_level = 'FULL'
  AND r.is_deleted = 0 AND c.is_deleted = 0
```

### 2.2 特征分桶规则

| 特征类型 | 条件 | 分桶方式 |
|---|---|---|
| 硬门槛（枚举） | 值域 ≤ 5 个不同值 | 按枚举值直接分组 |
| 小整数 | 值域 ≤ 3 个不同值 | 按值分组 |
| 数值连续 | 其余 | 等频分 5 桶（每桶记录数大致相等） |
| 数组（油道） | 多选值 | 按数组元素组合分组（如 [0,1], [1,2] 各为一组） |

### 2.3 方差归约公式

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

### 2.4 边界处理

| 情况 | 原因 | 处理 |
|---|---|---|
| X 只有 1 个值（如全 50Hz） | 分组前后方差不变 | importance = 0 |
| 某组仅 1 条记录 | 无法计算组内方差 | 丢弃该组，不计入加权平均 |
| global_var = 0（所有 Y 相同） | 分母为零 | importance = 0，无需推荐 |
| importance < 0（方差反而变大了） | 随机噪声 | 取 0 |

### 2.5 回测

每次重算权重后自动跑回测，验证新权重质量：

```
步骤：
  1. 全量 FULL 记录随机打乱
  2. 抽 20% 作为验证集，80% 作为训练集
  3. 训练集计算权重，对验证集每条记录做推荐（标准策略，Top-20 ±1σ）
  4. 统计每个输出参数的覆盖率：

      覆盖率 = 验证集实际值落在推荐范围内的记录数 / 验证集总记录数

  5. 同时用当前生效权重对验证集做一次推荐，得到旧权重覆盖率
```

### 2.6 存储

表 `tb_feature_weight`，每次重算生成新 version，初始 `is_active = 0`：

```sql
CREATE TABLE tb_feature_weight (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT,
    target_param  VARCHAR(32)   NOT NULL COMMENT 'CRGOD/LVT/LVRH/HVRH/CT',
    feature_name  VARCHAR(64)   NOT NULL COMMENT 'P/HVN/LVN/hvlvwm2/...',
    importance    DECIMAL(10,6) NOT NULL DEFAULT 0 COMMENT '重要度 0~1',
    version       INT           NOT NULL DEFAULT 1,
    sample_count  INT           NOT NULL DEFAULT 0 COMMENT '训练集记录数',
    is_active     TINYINT       NOT NULL DEFAULT 0 COMMENT '0待确认 1生效',
    create_time   DATETIME      DEFAULT CURRENT_TIMESTAMP,
    update_time   DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_version (version),
    INDEX idx_active_target (is_active, target_param),
    UNIQUE KEY uk_version_param_feat (version, target_param, feature_name)
) COMMENT '特征重要度权重表';
```

用户确认后，旧 version 全部 `is_active = 0`，新 version 全部 `is_active = 1`。

---

## 三、推荐接口

### 3.1 权重聚合

权重表按 `(target_param, feature_name)` 存，即同一个特征 P 对 CRGOD 的重要度和对 LVT 的重要度不同。推荐排序时需要每个 feature 一个单一权重，取**均值**聚合：

```
importance_agg[f] = mean(importance[crgod][f], importance[lvt][f],
                         importance[lvrh][f], importance[hvrh][f],
                         importance[ct][f])
```

> 取均值而非 max，原因：均值对所有输出参数平等对待。若取 max，则某特征只对 CT 重要（但对其他 4 个无用）也会获得高权重，偏离推荐目标。

### 3.2 推荐流程

1. 读取当前生效权重（`is_active = 1`），按 3.1 聚合为单一权重
2. 读取目标方案配置，提取 22 维输入特征
3. **硬门槛**筛选：HVLVWM2、LVWG、HVWG、HZ 必须完全相同
4. 若匹配记录数不足，执行**降级策略**（见 3.3）
5. 对通过门槛的每条历史记录计算**加权相似度分**：

```
score = Σ( importance_agg[f] × sim(f_target, f_history) )

其中：
  枚举特征: sim = 1（相同）| 0（不同）
  数组特征（油道）: sim = Jaccard 相似度（交集 / 并集）
  数值特征: sim = min(v_target, v_history) / max(v_target, v_history)
            防御：若任一值为 null 或 0，sim = 0
```

> 数值相似度用 min/max 替代原来的 ratio 公式，保证对称性：A 对 B 的相似度 = B 对 A 的相似度。f_target=0 时 min/max=0 直接返回 0，无需额外防御。

6. 按 score 降序排列，取 Top-N 条历史记录
7. 统计这 N 条的输出参数分布，生成推荐范围

### 3.3 硬门槛降级策略

4 个硬门槛筛选后，候选池可能不足 K 条。三个策略共享同一个候选池（降级触发条件：候选池 < 15 条），按统一的 degradation_level 逐级放宽：

| 序号 | 放宽动作 | 说明 |
|---|---|---|
| 0 | 全部匹配 | 首选，不做任何放宽 |
| 1 | 去掉 HVWG | 高压线规不同但低压相同，记录仍有参考价值 |
| 2 | 去掉 LVWG | 线规都不同的极端情况 |
| 3 | 去掉 HZ | 50Hz 和 60Hz 的历史混合使用 |
| 4 | 仅保留 HVLVWM2 | 最后一个硬门槛不松开 |

每降一级前检查是否满足最少需要量 K：

| 策略 | 最少需要 K |
|---|---|
| 精准 | 5 条 |
| 标准 | 10 条 |
| 广泛 | 15 条 |

API 返回结果中标记 `degradation_level`：0 = 全匹配 / 1 = 去掉 HVWG / ... / 4 = 仅保留 HVLVWM2。前端展示时标注"推荐可信度：高/中/低"对应 degradation_level 0-1 / 2-3 / 4。

### 3.4 三组推荐策略

| 策略 | N | 最少需要 | 推荐范围 | 用途 |
|---|---|---|---|---|
| **精准** | 5 | 5 | min ~ max（最窄） | 数据充足且有高相似度记录时首选 |
| **标准** | 20 | 10 | mean ± 1σ | 一般场景，平衡精度与覆盖 |
| **广泛** | 50 | 15 | mean ± 2σ（兜底） | 数据稀疏时保证命中，范围最宽 |

如果降级到最终仍不够最少需要量，该策略返回空，并在 API 响应中标记 `insufficient_data: true`。前端展示"该策略数据不足，请使用其他策略或手动设置"。

### 3.5 推荐结果示例

```
精准推荐（基于 5 条记录，最高相似度 94%）
  CRGOD: [350, 390] mm     当前方案原范围: [200, 400] mm
  LVT:   [10, 14] 匝        当前方案原范围: [5, 30] 匝
  LVRH:  [580, 650] mm     当前方案原范围: [400, 1000] mm
  HVRH:  [550, 620] mm     当前方案原范围: [400, 1000] mm
  CT:    [1.62, 1.68] T    当前方案原范围: [0.9, 1.7] T
```

### 3.6 API

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
    }
  },
  "weights": [
    {"target_param": "crgod", "feature_name": "P", "importance": 0.562},
    {"target_param": "crgod", "feature_name": "hvn", "importance": 0.231}
  ]
}
```

---

## 四、前端方案

### 4.1 入口

方案编辑页（优化设计 > 方案管理 > 编辑方案），在"优化范围"配置区域上方，增加两个按钮：

- **"智能推荐"** — 主按钮，点击对当前方案生成推荐
- **"权重管理"** — 文字按钮，点击进入权重管理

### 4.2 推荐弹窗

弹窗宽度约 700px，顶部为三组推荐 Tab（精准 / 标准 / 广泛），中间展示推荐参数表格，底部为操作区。

**表格列**：

| 参数名 | 原范围 | 推荐范围 | 缩小比例 |
|---|---|---|---|
| 铁心直径 | 200 ~ 400 mm | 350 ~ 390 mm | 缩小 80% |
| 低压匝数 | 5 ~ 30 匝 | 10 ~ 14 匝 | 缩小 84% |
| ... | | | |

**底部信息栏**：

```
基于 [187] 条历史记录 | 权重版本 v3 | 最高相似度 94%
```

**底部操作**：`[应用精准] [应用标准] [应用广泛] [关闭]`

### 4.3 权重管理弹窗

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

### 4.4 交互流程

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

## 五、数据库

```sql
CREATE TABLE tb_feature_weight (
    id            BIGINT PRIMARY KEY AUTO_INCREMENT,
    target_param  VARCHAR(32)     NOT NULL COMMENT 'CRGOD/LVT/LVRH/HVRH/CT',
    feature_name  VARCHAR(64)     NOT NULL COMMENT 'P/HVN/LVN/hvlvwm2/...',
    importance    DECIMAL(10,6)   NOT NULL DEFAULT 0 COMMENT '重要度 0~1',
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

---

## 六、后期拓展方向

当前 v1 只推荐 5 个最外层循环参数（CRGOD、LVT、LVRH、HVRH、CT），覆盖 10 层循环的前 3 层。后续可沿以下方向深入。

### 6.1 内层参数推荐（v2）

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

### 6.2 有监督模型（v3）

方差归约属无监督方法。FULL 记录超过 500 条后可升级为 XGBoost 多输出回归——输入 22 维参数 + 外层推荐值，输出最优线厚、线宽、层数组合。Java 侧通过 PMML 文件加载，毫秒级推理。

### 6.3 失败路径学习

每个被 reject 的 WorkItem 携带失败原因（磁通密度超限/高度超限/温升超限），将其与参数组合关联存储。推荐时标记相似方案的高频失败区域，推荐范围自动避开。

### 6.4 冷启动

初次部署无历史数据时，预置人工专家权重（version=0, source='manual'），FULL 记录积累后自动切换到数据驱动权重。

### 6.5 单相推广

单相计算循环结构与三相高度相似，直接复用方差归约 + 加权推荐框架，仅需替换特征映射表和输出参数表。
