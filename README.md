# ClimateCulturome / 地微知候

ClimateCulturome 是一个面向高原/山地环境—宿主微生物连续体研究的可复用 AI Scientist Skill。

它把科研流程组织为：

**数据治理 → 地球系统环境构建 → 微生物组描述与统计边界控制 → 环境—微生物候选关联 → 可证伪假说 → 人工验证 → provenance / claim-evidence 审计**

本仓库是**纯 Skill 包**：包含 Skill 定义、工作流、参考规范、Python CLI、测试与空白模板，但不包含任何真实项目数据、真实采样点、真实研究结果、真实报告或个人信息。

## 目录

```text
SKILL.md                     # Skill 主定义
skill.json                   # Skill 元数据
climateculturome_skill/      # Python 实现与 CLI
workflows/                   # 分阶段科研工作流
references/                  # 科学边界、证据等级、统计方法等参考
examples/                    # 全部为虚构的正向/反向示例
data_templates/              # 空白/占位输入模板
scripts/                     # 本地验证脚本
tests/                       # 单元测试
```

## 环境

需要 Python 3.10+，推荐使用 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync --group dev
```

## 运行

预检一个请求：

```bash
uv run climateculturome preflight --request data_templates/request.example.json
```

执行并输出审计结果：

```bash
uv run climateculturome run --request request.json --output output/
uv run climateculturome audit --output output/
```

`data_templates/request.example.json` 仅包含占位符路径。真实数据必须在运行时由用户提供。

## 测试

```bash
./scripts/run_tests.sh
```

或：

```bash
uv run python scripts/validate_skill.py
uv run pytest -q
```

## 数据与隐私边界

仓库明确禁止内置：

- 真实样本表、ASV/OTU/feature matrix；
- 真实站点坐标与受试者信息；
- 真实丰度、统计结果和当前研究发现；
- EarthLink 或其他智能体的真实导出报告；
- 真实 claim ledger、provenance、运行日志；
- 未公开论文结果、个人信息和团队隐私。

示例目录中的案例全部为合成/虚构案例。

## License

MIT，见 [`LICENSE`](LICENSE)。
