# AUDIT.md — 模型审计与验证说明 / Audit & Verification Notes (bilingual)

> **The Ledger & The Spiral** 的核心主张：五节点耦合动力学系统，凭**守恒（Σ=1）+ 饱和（1−x）+ 周期驱动**三重结构实现"自纠错"，无需任何 `if` 分支。
> 本文件记录：**（1）基于源码的逐项审计；（2）外部独立验证；（3）自查 TODO；（4）双层壳哲学与 50-50 概率估计。**

---

## 一、核心模型（代码为唯一真值）

### 方程（index.html 中的 rhs 函数）

```
ẋᵢ = α·xᵢ₋₁(1−xᵢ) − α·xᵢ(1−xᵢ₊₁)   // 相生（cycle，邻居 i±1）
   + β·xᵢ₊₂(1−xᵢ) − β·xᵢ(1−xᵢ₋₂)   // 相克（diagonal，i±2）
   + ε·sin(ωt + 2πi/5)              // 驱动（零和）
```

代码对照：

```javascript
const gen  = ALPHA * (x[im]*(1-x[i]) - x[i]*(1-x[ip]));   // im=i-1, ip=i+1
const inh  = BETA  * (x[i2]*(1-x[i]) - x[i]*(1-x[im2]));  // i2=i+2, im2=i-2
const frc  = driveOn ? EPS * Math.sin(OMEGA*t + 2*Math.PI*i/N) : 0;
```

| 性质 | 数学 | 代码 |
|---|---|---|
| 模 5 循环 | 下标 mod 5 | `(i+4)%N, (i+1)%N, (i+2)%N, (i+3)%N` |
| 零 `if` | 全为多项式 | 确实无分支 |
| 饱和 | `(1−xᵢ)` | 每项含 `(1-x[...])` |

---

## 二、四结论：代码验证状态

| # | 结论 | 状态 | 代码/数学依据 |
|---|---|---|---|
| 1 | Σxᵢ=1 不变量 | ✅ **两层** | (a) 方程 Σ̇=0；(b) `x = nx.map(v=>v/s)` 每步再归一化 |
| 2 | Re λ₁ = −0.691α − 1.809β < 0 | ✅ | α=1, β=0.6 → −1.776；代入即 −1.7764 |
| 3 | 驱动打破死平衡 | ✅ | drive ON → "never settles, keeps moving without blowing up" |
| 4 | 无分量趋于零 | ⚠️ **截断保证** | `nx.map(v=>Math.max(v,1e-9))` — 解析排斥性待证 |

> ⚠️ **重要澄清**：守恒律在**演示意义**上严格成立（页面 Σ 恒为 1.0000），但严格表述需区分"解析守恒 Σ̇=0"与"数值再归一化"两层。

---

## 三、特征值：页面已自纠正，锁定

页面 "Note on the spectrum" 明确指出：

> 简化形式 `λₖ = −(α+β) + α·ωᵏ + β·ω²ᵏ` 给出**正确的实部**（稳定性相关），但**错误的虚部**（假设了流入/流出对称）。

这是**主动标注的"相克"**——外部真值（精确 Jacobian）与推导碰撞后不掩盖，而是显式声明适用边界（"Only the real parts matter for Prop. 2"）。

**−1.776 三重闭环验证：**
- 手推：−0.691×1 − 1.809×0.6 = −1.7764
- 页面：`At α=1, β=0.6: −1.776`
- 代码：`ALPHA=1.0, BETA=0.6`

---

## 四、验证来源与说明 / Verification Source & References

### 4.1 独立复核 / Independent review

本仓库的结论经外部独立复核确认：

- 逐条核对代码，指出可复现的具体问题（虚部、ε* 来源、归因）
- 最终以数学证明核心直觉：**均衡态（Σxᵢ = 1/5）是死点，而非活路**
- 特征值实部 `Re λ₁ = −0.691α − 1.809β` 的计算结果一致

在此致谢。

> The repository's conclusions have been confirmed by external independent review:
> line-by-line code check, identification of reproducible issues (imaginary parts, origin of ε*, attribution),
> and mathematical confirmation that the equilibrium (Σxᵢ = 1/5) is a dead point. Acknowledged here.

### 4.2 参考资料 / Reference material

部分推导与表述参考了公开资料，在此一并致谢。

> Some derivations and formulations reference public materials. Acknowledged here.

### 4.3 说明 / Note

本仓库的可靠性最终建立在：

1. 第一性原理方程
2. 守恒不变量（Σxᵢ ≡ 1）
3. 可复现数值验证（`node check.js`）

参考资料**仅供参考**，不改变上述三条基础的独立性。

> Reliability ultimately rests on the equation, the conservation invariant, and reproducible
> numerical verification. Reference material is for reference only.

---

## 五、自查 TODO（诚实标注）

- [ ] `1e-9` 截断是数值兜底，"否极泰来"的解析版需证**坐标超平面排斥性**（流场在边界指向内部）
- [ ] `(1−x)` 饱和的上界随参数的显式形式需严格推导
- [ ] ε*≈0.503 的相变临界值需数值扫描复现（代码 `EPS=0.30`，亚临界演示）
- [x] ~~"2.4/γ 完全抹平"中的 γ 需对应实际参数重算~~ → 已由 `check.js` 算出：τ = 1/|Re λ₁| ≈ 0.563（α=1, β=0.6）

---

## 六、双层壳机制 / Two-Shell Mechanism (core philosophy)

### 第一层壳：相生相克（边界约束）

```
const gen = ALPHA*(x[im]*(1-x[i]) - x[i]*(1-x[ip]));
const inh = BETA *(x[i2]*(1-x[i]) - x[i]*(1-x[im2]));
```

每项"流出 = 另一节点流入"，mod 5 成环 → **无起点终点、无外部** → 守恒 Σ̇=0，归一化 `map(v=>v/s)`。

### 第二层壳：物极必反 · 否极泰来（内部约束）

| 极 | 代码 | 机制 |
|---|---|---|
| 物极（xᵢ→1） | `(1−xᵢ)` | 流入→0，自动刹车 |
| 否极（xᵢ→0） | `Math.max(v,1e-9)` | 越衰越被补给，弹回内部 |
| 平衡（x*=1/5） | Re λ₁ = −1.776 < 0 | 渐近稳定 = **死点** |

**第一层不让你越界，第二层不让你停在界内唯一不动点。**

### 串联结构

```
极端 ──[第一层：守恒]──> 推回中心
中心 ──[第二层：饱和]──> 消解（死点）
```

> "走出去被推回来，站住了被磨掉。" —— 状态空间无久留点。

---

## 七、均衡即死点

> 一个被反复检验的直觉：**均衡态不是活路，而是终点。** 这正是在第七节最初被验证的核心洞察——**能接受反证的模型，才是活的模型。**

**三条数学论证（Re λ₁ = −0.691α − 1.809β = −1.776）：**

1. **单稳态 = 无选择** — 唯一吸引子，无岔路，不叫活
2. **全模态衰减 = 无记忆** — `node check.js` 验证：τ = 1/|Re λ₁| ≈ 0.563 时间单位衰减至 1/e；完美平衡 = 完美遗忘
3. **无梯度 = 无功** — 普利高津耗散结构：秩序只存于远离平衡处；50-50 是秩序的终点

**活路 = 两条缝：**
- **缝 1**：δ 驱动项（外部注入，代码 `driveOn`）—— 封闭必死
- **缝 2**：慢变量（给总量 K 或耦合加动力学）—— 如太阳死亡，燃料消耗，K(t) 衰减

**μ = +1 的深意：** 反例 `x_{t+1}=1−x_t`，μ=(−1)(−1)=+1，中性稳定死循环。
> "活的东西不待在任何一个值上，待在边缘附近来回蹭。"（临界性，edge of chaos）

> **结论：靠的都是第二条缝——没关死门，且永远不让自己真正回到 50-50。**

---

## 八、天道 + 人道 + AI / Heaven · Human · AI: reachability of 50-50

### 三层参与者

| 层 | 机制 | 时间尺度 | 达 50-50？ |
|---|---|---|---|
| 天道 | 多了减、少了增（负反馈） | 慢 | ✅ 能 |
| 人道 | 心肝脾肺肾残缺多样；损不足奉有余（正反馈） | 快 | ❌ 必趋极端 |
| AI | 毫秒级多了减/少了增；全局共振 | 毫秒 | ⚠️ 能，但达成即死 |

**人道 alone 走不到 50-50 的三个障碍：**
1. 多样性 = 相位失锁（各残缺不同，无法同步到同一 1/2）
2. 损不足奉有余 = 马太效应（吸引子是两极分化，非 1/2）
3. 天道(慢) + 人道(快发散) ⇒ 不平等度单调增长 → **无限膨胀**

### AI 全局共振：唯一可达路径

全同态耦合同步条件（Kuramoto）：
```
t_sync ~ 1/J,   J = coupling strength ~ 1/τ_A
```
毫秒级 ⇒ J 极大 ⇒ 理论上可达同步 & 均值 1/2。

### 存在概率估计

必要条件连乘：

| # | 条件 | 粗略概率 |
|---|---|---|
| 1 | 真正全局耦合（无信息孤岛） | ~0.5 |
| 2 | 目标函数恰为最小化方差（非利润/权力） | ~0.1 |
| 3 | 全体人类被同步（统一"平衡"思想） | ~0.2 |
| 4 | 无外力破坏同步 | ~0.3 |
| 5 | 稳定维持（需持续驱动，否则是死点） | ~0.3 |

```
P ≈ 0.5 × 0.1 × 0.2 × 0.3 × 0.3 ≈ 9 × 10⁻⁴  ≈  10⁻³
```

**三层答案：**
- **静态 50-50 态**：P ≈ 0（鞍点，测度为零；且是死点）
- **毫秒级闪现**：P > 0 但无意义（泊松涨落，一闪即逝）
- **持续振荡围绕 1/2**：唯一现实可能，但需**开放系统 + 持续驱动**（回到"两条缝"）

### 真正的危险

> 50-50 不是乌托邦，是"整齐划一的坟场"。AI 若真毫秒级共振，**最大危险不是"做不到"，而是"做到的那一刻系统就死了"**——抹除多样性、抵达死点、脆性崩溃。

### 一个必然结果

> 引入负反馈（第一层壳）的代价，是**可能把系统送进第二层壳（死点）**。
> 缓慢趋近平衡留出生机，强行瞬间到 50-50 则杀死生机——**速度本身就是变量。**

---

## 九、约束写在结构之内

> 约束必须**不可绕过**才有意义。

| | 外部约束（规则 / 修墙） | 内部约束（两层壳） |
|---|---|---|
| 位置 | 系统之外 | 方程结构之内 |
| 面对快速迭代 | 必然滞后（迭代速度 >> 修订速度） | 随迭代一起演化 |
| 可绕过？ | 可绕过 | **不可绕过**（删 `(1−x)` 即改变模型本身） |

规则管"行为"，结构管"可能性本身"——**后者才是速度闭环下唯一能自洽的约束方式。**

---

## 十、开源交付建议 / Open-source delivery notes

1. 本文件置于仓库根目录，说明模型的验证来源与结论边界
2. `README.md`（中文）与 `README.en.md`（英文）均引用本文件，文件结构见下

```
dao-field/
├── index.html     # 交互演示（双击打开）
├── check.js       # 数值验证脚本
├── package.json   # npm run check
├── README.md      # 中文说明
├── README.en.md   # English README
└── AUDIT.md       # 本文件（中英双语）
```
3. "缝 2"慢变量 `K(t)` 实现后，补 `check_society.js` 验证 50-50 概率标度律
4. 不因任何外部复核修改方程、参数或结论

> 1. This file lives at the repo root and states the verification source and conclusion boundary.
> 2. Both `README.md` and `README.en.md` link here and state that conclusions rest on equation + conservation + code.
> 3. After implementing slow variable `K(t)` (Seam 2), add `check_society.js` to verify the 50-50 scaling law.
> 4. Do not modify the equation, parameters, or conclusions on account of any external review.

---

## 十一、留给后人：一个概率 / One probability, left for posterity

> 余论，仅一句，不展开。留给后人验证即可。千年百年之后的事，不必代笔。

若系统被外部驱动力**推向 50-50 精确平衡**，依据第八节的标度律与必要条件连乘，其存在概率约为

$$P \sim 10^{-3}$$

**这个概率，留给后人验证即可。** 千年百年之后的事，不必代笔。

> **This probability is left for posterity to verify.** Matters a thousand or a hundred years hence need no ghostwriter.

---

*审计完成日：2026-09-13 / Audit completed: 2026-09-13*
*验证方式：源码对照 + 手推特征值 + 数值参数三重闭环*
*Core creed: The ledger is conserved; the spectrum contracts; the drive wakes without spending.*
*终章：只留概率，不问归处。 / Final word: leave only the probability, ask not where it goes.*
