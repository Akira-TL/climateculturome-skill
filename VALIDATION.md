# Validation

仓库验证分三层：Skill 结构、科研边界和发布卫生。

## 运行

```bash
uv run python scripts/validate_skill.py
uv run pytest -q
```

`validate_skill.py` 检查入口文件、元数据、请求 schema、示例标记和仓库结构；`pytest` 覆盖 evidence grading、数据治理、微生物分析边界等行为。

## 验收重点

- `SKILL.md` 能作为独立入口，并能按需路由到 `workflows/` 与 `references/`；
- summary 与 sample-level 数据不会被混用；
- shared occurrence、空间梯度和候选关联不会被升级为迁移、时间变化或因果结论；
- claim 的证据等级、来源和验证路径可追溯；
- 示例、模板和发布包不混入项目运行产物或私有数据。

验证通过只说明 Skill 的结构与已编码规则符合预期，不替代具体研究中的统计审核。
