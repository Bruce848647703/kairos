# Changelog

## 2026-11-05 · 系列维护版本

本仓库是 Kairos 量化系列的索引仓库；实际变更发生在各 `kairos-*` 子仓库。

### 修复
- **CLI 顶层帮助被默认子命令吞掉**：`kairos-vol` / `kairos-rates` / `kairos-microstructure` / `kairos-terminal` 直接执行 `--help` 时只显示默认子命令的帮助。现在 `-h/--help/--version` 交给顶层解析器，其他裸选项仍转发给默认子命令。
- **补齐 `--version`**：上述 4 个 CLI 现在与 `kairos-clean` 一致，支持 `--version`。
- **回归测试**：新增 CLI 版本号、顶层帮助、默认子命令测试（`kairos-terminal/tests/test_cli.py` 等）。
- **死代码与未使用导入**：清理 86 处（ruff `F401/F541/F841`），全部仓库 `ruff check --select F,E9` 通过。
- **测试断言补强**：`kairos-data` 的资产类别覆盖、`kairos-microstructure` 的排队位置测试从“算了但没断言”改为真实断言。

### 维护
- 版本号 patch 升级：`kairos-*` 0.1.0 → 0.1.1，`kairos-clean` 0.1.3 → 0.1.4，`kairos-terminal` 0.5.0 → 0.5.1。
- `requires-python` 统一为 `>=3.9`（3.8 已 EOL）。
- 所有 `pyproject.toml` 增加 `[project.urls]`（Homepage / Source / Issues）。
- `kairos-ml` / `kairos-portfolio` / `kairos-risk` 的 `dev` extra 加入 `scipy`，CI 能覆盖 scipy 分支。
- GitHub Actions 矩阵统一为 Python 3.9 / 3.12 / 3.13；安装改为 `pip install -e ".[dev]"`，避免手工依赖列表掩盖缺失依赖；CLI 仓库增加 `--version` / `--help` 冒烟测试。
- 索引 README 修正测试数（1983）、各仓库测试数（clean 27、microstructure 42、rates 42、terminal 131、vol 58）与研究结论数（12 篇笔记 / 147 条可溯源发现），并修正“任一仓库都能跑 `examples/run_all.py`”的错误说明。

### 工具
- 新增索引仓库 `Makefile`：`make test` / `make lint` / `make versions` / `make check`。
- 新增 `scripts/check_versions.py`：校验每个仓库 `pyproject.toml` 与包内 `__version__` 一致，发版前一条命令即可发现漏改。

### 验证
- 16 个仓库共 **1983 个测试全部通过**（本地 Python 3.13.5 / numpy 2.1.3 / pandas 2.3.3）。
- 16 个仓库均可构建 wheel（`pip wheel . --no-deps`）。
- 14 个离线 `demo` 入口全部 exit 0。