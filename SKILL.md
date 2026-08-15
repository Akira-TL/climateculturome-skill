---
name: climateculturome
version: 3.1.0
description: >-
  用于高原、山地及其他环境梯度下的环境—宿主微生物连续体研究。负责判断输入数据能支持什么分析，
  组织环境变量与微生物组分析，生成可证伪假说，并用 evidence grading、provenance 和 claim-evidence
  审计约束结论强度。适用于 16S/ITS/宏基因组与地球系统环境数据的联合研究。
argument-hint: "<request.json 或项目数据目录>"
license: MIT
metadata:
  domain: earth-science, plateau-ecology, microbiome, ai-scientist
  evidence_model: A/B/C/D
  primary_language: zh-CN
---

# ClimateCulturome / 地微知候

ClimateCulturome 用来把“环境梯度如何关联宿主与环境微生物变化”这类问题拆成可执行、可审计的科研流程。先判断数据边界，再选择分析方法；结论只能写到当前证据真正支持的位置。

## 工作流程

### 1. 先判断输入能支持什么

读取数据目录、样本/站点元数据、微生物矩阵或汇总表、taxonomy、局地环境测量和外部环境数据配置。

先确认：

- 样本、站点、时间、生态位和批次能否正确对应；
- 是否有样本级矩阵，还是只有组级 summary；
- 是否存在真实经纬度和采样时间；
- missing、zero、`<LOD` 是否被正确区分；
- 重复测量、分层结构和潜在混杂是否可识别。

需要完整 intake 规则时读取 `workflows/01_data_intake_and_governance.md`；输入要求见 `references/data_requirements.md`。

### 2. 构建环境背景

有可靠空间与时间锚点时，再匹配地球系统环境变量。变量选择应服从研究问题，不机械堆积指标。

常见变量包括温度、降水、气压/氧分压、湿度、土壤水分、辐射、风和植被状态。需要外部数据源、时间窗口或提取策略时读取：

- `workflows/02_earth_system_environment.md`
- `references/earth_system_sources.md`

如果没有真实坐标，不把行政区中心、平均海拔或推测位置冒充采样点；此时只能做区域级背景描述，或明确要求补充定位信息。

### 3. 按数据层级选择微生物分析

只有组级 summary 时，停留在组成、prevalence、共享出现、描述性排序和候选异常等层面。

有 sample-level matrix 后，才考虑 Alpha/Beta diversity、PERMANOVA/PERMDISP、差异丰度、source tracking、网络、约束排序、mixed model 等正式推断；进入这些分析前仍需检查样本量、重复结构、组成型数据特性和混杂。

具体方法选择读取：

- `workflows/03_microbiome_descriptive.md`
- `references/statistical_methods.md`

### 4. 连接环境与微生物

先处理环境变量的共线性，再建立少量可解释的环境轴，并在 niche/domain 层面连接微生物响应。site、region、year、batch 等设计因素应进入模型或敏感性分析，而不是事后用文字解释掉。

需要环境—微生物联合分析时读取 `workflows/04_environment_microbiome_linkage.md`。

### 5. 生成可证伪假说

从当前结果中筛选少量值得验证的候选机制。每条假说至少回答：

- 为什么会生成这条假说；
- 当前证据是什么；
- 哪些替代解释同样成立；
- 什么观测或实验结果会推翻它；
- 下一步最小验证是什么。

默认每轮生成 2–4 条。详细格式见 `workflows/05_hypothesis_generation.md`。

### 6. 人工验证与审计

在形成最终科学表述前，检查统计模型、taxonomy 分辨率、生态学合理性、空间/时间/批次混杂和因果措辞。需要审核流程时读取 `workflows/06_human_validation.md`。

输出 claim ledger、provenance 或研究报告前读取 `references/output_contract.md`；遇到中断、缺失输入或外部数据失败时读取 `workflows/08_failure_recovery.md`。

## 科学边界

以下边界始终成立：

- **共享出现不是迁移证据。** 同一 taxon 同时出现在环境与宿主中，只能先记为 shared occurrence / source-tracking candidate。
- **空间梯度不是时间变化。** 不把不同海拔、纬度或区域的横截面差异直接写成气候变化效应。
- **海拔通常是代理变量。** 优先分解气压/氧分压、温度、水分、植被、土壤和管理因素，而不是把所有差异归因于“海拔”。
- **summary 不能产生样本级显著性。** 没有样本级矩阵时，不伪造 PERMANOVA、差异丰度、网络或 mixed model 结果。
- **候选关联不是因果机制。** 描述性共变只能推动下一步验证，不能自动升级为机制结论。

更完整的边界与反例见 `references/scientific_boundaries.md`。

## 证据分级

主要科学主张使用 A/B/C/D 四级证据：

- **A — Uploaded Fact**：由输入文件直接支持；
- **B — Matched External Evidence**：由真实空间/时间锚点匹配公开数据得到；
- **C — Descriptive Candidate**：描述性共变、排序、共享出现或候选异常；
- **D — Hypothesis / Requires Validation**：仍需正式统计、独立数据、时间序列或实验验证。

每条重要 claim 都应能追溯到 supporting inputs，并写清 boundary、alternative explanations 和 next validation。细则见 `references/evidence_grading.md`。

## 按需读取

不要一次性加载整个仓库。根据当前阶段读取对应文档：

| 当前任务 | 读取 |
| --- | --- |
| 快速了解完整流程 | `workflows/00_quickstart.md` |
| 数据 intake / 主键 / 缺失值 | `workflows/01_data_intake_and_governance.md` |
| ERA5、CMIP6 等环境数据 | `workflows/02_earth_system_environment.md`、`references/earth_system_sources.md` |
| 微生物描述与统计方法 | `workflows/03_microbiome_descriptive.md`、`references/statistical_methods.md` |
| 环境—微生物联合分析 | `workflows/04_environment_microbiome_linkage.md` |
| 假说生成 | `workflows/05_hypothesis_generation.md` |
| 人工审核 | `workflows/06_human_validation.md` |
| 比赛证据包装 | `workflows/07_competition_evidence_packaging.md` |
| 输出文件与字段契约 | `references/output_contract.md` |
| 术语不确定 | `references/glossary.md` |

## 完成条件

一次分析完成时，应满足：

1. 数据层级与研究设计已经明确，分析没有越过输入边界；
2. 主要 claim 都有证据等级和可追溯输入；
3. 关联、迁移、时间变化和因果机制没有混写；
4. 关键替代解释与下一步验证已记录；
5. 需要正式推断但输入不足时，明确返回受限状态，而不是补造结果；
6. 最终输出符合 `references/output_contract.md`。

CLI 入口：

```bash
climateculturome preflight --request request.json
climateculturome run --request request.json --output output/
climateculturome audit --output output/
```
