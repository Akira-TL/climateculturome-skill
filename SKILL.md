---
name: climateculturome
version: 3.1.0
description: >-
  ClimateCulturome（地微知候）是一套面向高原/山地环境—宿主微生物连续体研究的 AI Scientist Skill。
  它负责数据治理、地球系统环境变量设计、微生物组描述与推断边界控制、环境—微生物候选关联、
  可证伪假说生成、人工验证规划、provenance 与 claim-evidence 审计。
  Skill 本身不包含任何真实项目数据、真实采样点、真实报告或既有研究结论。
argument-hint: "<request.json 或项目数据目录>"
license: MIT
metadata:
  domain: earth-science, plateau-ecology, microbiome, ai-scientist
  evidence_model: A/B/C/D
  primary_language: zh-CN
  data_policy: no-embedded-project-data
---

# ClimateCulturome / 地微知候 Skill

## 1. 目标

把“环境—宿主微生物连续体”的科研探索组织成一条可复用、可审计、可证伪的 AI Scientist 工作流：

**数据治理 → 环境背景构建 → 微生物结构分析 → 环境—微生物关联 → 假说生成 → 人工验证 → 证据审计**

本 Skill 适合：

- 高原、山地、寒区或其他具有明显环境梯度的生态系统；
- 宿主粪便/肠道与植物、土壤、水体等多生态位联合研究；
- 16S/ITS/宏基因组等微生物数据；
- 公开地球系统数据与局地实测环境数据联合分析；
- AI Scientist 科研比赛或需要 provenance / claim-evidence ledger 的研究流程。

## 2. Skill 不携带真实研究数据

本 Skill **禁止内置**：

- 真实样本表、真实 ASV/OTU/feature matrix；
- 真实站点坐标、真实受试者信息；
- 真实组间丰度与统计结果；
- EarthLink 或其他智能体的真实导出报告；
- 当前项目的 claim ledger、真实 provenance、运行日志；
- 未公开论文结果、个人信息、团队信息。

真实数据只在运行时由用户提供。

## 3. 核心科学原则

### 3.1 数据层级决定能做什么

仅有组级 summary 时，可以做：

- 组成描述；
- prevalence 描述；
- 跨生态位共享出现；
- 候选排序；
- 假说生成。

但**不能**声称完成：

- Alpha/Beta diversity 正式推断；
- PERMANOVA / PERMDISP；
- ANCOM-BC / LEfSe；
- FEAST / SourceTracker；
- 共现网络；
- RDA / db-RDA / CCA；
- variance partitioning；
- mixed model；
- SEM；
- 因果推断。

### 3.2 共享出现 ≠ 迁移

同一分类单元出现在宿主与环境中，只能称为：

> 跨生态位共享出现 / source-tracking candidate

不能直接称为：

> 从环境迁移进入宿主 / 来源贡献已被证明

### 3.3 空间梯度 ≠ 时间变化

不同海拔/纬度/区域站点之间的空间差异，不能直接替代：

- 气候变化时间序列；
- 长期重复采样；
- before/after 实验。

### 3.4 海拔通常是代理变量

海拔可能同时关联：

- 气压与氧分压；
- 温度；
- 辐射；
- 水分；
- 植被；
- 土壤；
- 人类管理。

因此优先构造**复合环境主轴**，而不是把全部差异写成“海拔导致”。

### 3.5 不生成伪坐标

若没有真实采样经纬度：

- 不得用县中心、行政区中心或平均海拔替代；
- 不得将近似点位包装成真实采样点；
- 只能进行区域级背景描述，或要求补充坐标。

## 4. 强制证据分级

每个主要科学主张使用以下证据等级：

- **A — Uploaded Fact**：输入文件直接支持的事实。
- **B — Matched External Evidence**：依据真实空间/时间锚点从公开数据库匹配得到的结果。
- **C — Descriptive Candidate**：描述性共变、排序、共享出现、候选异常。
- **D — Hypothesis / Requires Validation**：需要样本级统计、独立验证、时间序列或实验才能成立。

每条 Claim 至少包含：

```yaml
claim:
evidence_level:
supporting_inputs:
status:
boundary:
alternative_explanations:
next_validation:
```

## 5. 标准执行流程

### Step 0 — Intake / Preflight

读取：

- dataset registry；
- sample/site metadata；
- microbiome matrix 或 summary；
- taxonomy；
- local environmental measurements；
- external-data configuration。

检查：

1. 数据集是否属于同一采样设计；
2. site/sample/date/niche 主键；
3. 是否有真实坐标；
4. 是否存在跨批次同名站点；
5. 缺失是否被误当 0；
6. `<LOD` 是否被错误数值化；
7. 是否存在样本级矩阵；
8. 是否具备正式统计的必要输入。

### Step 1 — Earth-system environment

对有真实坐标的采样单元，优先构建：

- temperature；
- precipitation；
- surface pressure；
- dry/moist pO₂；
- relative humidity；
- soil moisture；
- shortwave/longwave radiation；
- cloud cover；
- wind；
- vegetation / LAI / NDVI（按可用性）。

建议窗口：

- sampling month；
- previous 30 days；
- previous 3 months；
- previous 12 months；
- climatology；
- historical trend；
- future scenario（若研究问题需要）。

所有外部数据必须记录：

- source；
- version；
- variable；
- spatial resolution；
- temporal resolution；
- extraction method；
- access date；
- transformation；
- uncertainty。

### Step 2 — Microbiome analysis

#### 仅 summary 可用

允许：

- composition；
- prevalence；
- shared taxa；
- descriptive rank/order；
- candidate outlier；
- domain/niche comparison。

#### 有 sample-level matrix

可进一步进入：

- Alpha diversity；
- Beta diversity；
- PERMANOVA + PERMDISP；
- compositional differential abundance；
- core microbiome；
- source tracking；
- network；
- constrained ordination；
- hierarchical/mixed modeling。

但必须先检查统计假设、样本量、重复结构和混杂。

### Step 3 — Environment × Microbiome linkage

优先顺序：

1. 先识别环境共线性；
2. 构造少量可解释环境轴；
3. 再连接微生物响应；
4. niche/domain 分层；
5. 显式纳入 site/region/year/batch；
6. 进行 sensitivity analysis；
7. 记录替代解释。

### Step 4 — Hypothesis generation

每轮优先生成 2–4 条可证伪假说。

每条必须包含：

- `hypothesis`
- `why_generated`
- `current_evidence`
- `evidence_level`
- `alternative_explanations`
- `falsifiable_prediction`
- `next_validation`
- `stop_condition`

AI 不应把候选规律升级成已证实机制。

### Step 5 — Human validation

人工审核至少覆盖：

- 样本和元数据真实性；
- 统计模型；
- 生态学合理性；
- taxonomy 分辨率；
- 空间/时间/批次混杂；
- 因果措辞；
- 独立验证方案。

### Step 6 — Audit

标准输出：

```text
audit.json
provenance.json
workflow_trace.jsonl
claim_ledger.csv
descriptive_candidates.csv
hypotheses.json
reproducibility_manifest.json
scientific_report.md
```

## 6. 推荐输出状态

- `BLOCKED_BY_INPUTS`：缺少关键输入。
- `DESCRIPTIVE_ONLY`：只能描述，不足以正式推断。
- `READY_FOR_STATISTICAL_VALIDATION`：样本级数据齐备，可进入正式统计。
- `READY_FOR_HUMAN_REVIEW`：AI 分析完成，待人工审核。
- `VALIDATED_WITH_LIMITATIONS`：人工验证完成，但仍有明确限制。

不要使用“competition_ready=true”替代科学审核。

## 7. 正向与反向用例

- `examples/positive/`：展示应当怎样解释。
- `examples/negative/`：展示必须阻止的过度推断。
- 所有示例均为**虚构案例**，不对应任何真实项目或真实站点。

## 8. 参考文档

- `references/data_requirements.md`
- `references/evidence_grading.md`
- `references/earth_system_sources.md`
- `references/statistical_methods.md`
- `references/scientific_boundaries.md`
- `references/output_contract.md`
- `references/competition_alignment.md`
- `references/glossary.md`

## 9. CLI

```bash
climateculturome preflight --request request.json
climateculturome run --request request.json --output output/
climateculturome audit --output output/
```

详细请求格式见：

```text
data_templates/request.schema.json
data_templates/request.example.json
```

其中 `request.example.json` 只包含占位符，不包含真实数据。

## 10. 完成判据

一个合格运行至少满足：

- 不跨设计自动合并；
- 不使用伪坐标；
- 不把 missing 当 zero；
- 不凭 summary 生成样本级显著性；
- 不把 shared taxa 写成 transfer；
- 不把 space-for-time 当成真实时间变化；
- 所有 C/D claim 有替代解释；
- provenance 可追溯；
- 结论强度与证据等级一致。

**Skill 的自动审计只验证工作流与表述边界，不替代科研人员的统计审核和学术判断。**
