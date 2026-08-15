# ClimateCulturome / 地微知候

ClimateCulturome 是一个面向环境梯度与宿主微生物组研究的 AI Scientist Skill。它帮助 Agent 先判断数据能支持什么，再选择合适的环境与微生物分析方法，最后把结果整理成可追溯、可验证的科学主张。

它特别适合高原、山地、寒区等环境梯度明显的研究，也可用于其他需要联合分析 16S / ITS / 宏基因组与地球系统环境数据的场景。

## 它做什么

ClimateCulturome 关注的是科研判断链，而不是单一统计脚本：

- 检查样本、站点、时间、生态位和批次等研究设计信息；
- 根据 summary 或 sample-level matrix 的数据层级限制分析范围；
- 组织温度、降水、气压/氧分压、湿度、植被等环境变量；
- 连接环境变化与微生物响应，同时处理共线性和混杂；
- 将描述性关联整理为可证伪假说，而不是直接写成机制结论；
- 用 evidence grading、provenance 和 claim ledger 保留证据链。

核心原则很简单：**结论不能比证据走得更远。**

## 适用场景

例如：

- 不同海拔或区域之间的宿主肠道微生物比较；
- 宿主与土壤、植物、水体等生态位的联合研究；
- 微生物组与 ERA5、CMIP6、SoilGrids 等环境数据的整合；
- 从探索性结果生成下一步统计验证或实验假说；
- 需要 claim-evidence、provenance 或科研审计链的 AI Scientist 工作流。

## 安装与环境

需要 Python 3.10+，推荐使用 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync --group dev
```

仓库入口是 [`SKILL.md`](SKILL.md)。具体科学规则和执行分支按需放在 `workflows/` 与 `references/` 中，Agent 不需要一次性加载全部内容。

## CLI

预检输入：

```bash
uv run climateculturome preflight --request data_templates/request.example.json
```

执行分析并写出结果：

```bash
uv run climateculturome run --request request.json --output output/
```

检查输出是否满足审计要求：

```bash
uv run climateculturome audit --output output/
```

请求格式见：

```text
data_templates/request.schema.json
data_templates/request.example.json
```

## 仓库结构

```text
SKILL.md                     # Agent 入口与核心决策规则
workflows/                   # 各阶段执行流程
references/                  # 证据、统计、科学边界与输出规范
climateculturome_skill/      # Python CLI 与审计实现
data_templates/              # 输入模板
examples/                    # 示例
scripts/                     # 验证脚本
tests/                       # 测试
```

## 测试

```bash
./scripts/run_tests.sh
```

或分别运行：

```bash
uv run python scripts/validate_skill.py
uv run pytest -q
```

## License

MIT，见 [`LICENSE`](LICENSE)。
