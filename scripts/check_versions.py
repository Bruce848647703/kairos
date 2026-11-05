#!/usr/bin/env python3
"""检查各 kairos-* 仓库的 pyproject 版本与包内 __version__ 是否一致。

用法（在 kairos 索引仓库根目录）::

    python scripts/check_versions.py

退出码 0 表示全部一致；1 表示存在缺失或不一致。脚本只读，不修改文件。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION_RE = re.compile(r'(?m)^version = "([^"]+)"$')


def main() -> int:
    repos = sorted(p for p in ROOT.glob("kairos-*") if (p / "pyproject.toml").exists())
    if not repos:
        print(f"未找到 kairos-* 仓库（查找目录: {ROOT}）", file=sys.stderr)
        return 1

    problems = []
    for repo in repos:
        pyproject = repo / "pyproject.toml"
        match = VERSION_RE.search(pyproject.read_text(encoding="utf-8"))
        if not match:
            problems.append(f"{repo.name}: pyproject.toml 缺少 version")
            continue
        expected = match.group(1)
        inits = sorted(repo.glob("kairos_*/__init__.py"))
        if not inits:
            print(f"{repo.name:26} {expected:8} (无 Python 包，跳过 __version__)")
            continue
        for init in inits:
            found = re.search(r'(?m)^__version__ = "([^"]+)"$',
                              init.read_text(encoding="utf-8"))
            if not found:
                problems.append(f"{repo.name}: {init.relative_to(repo)} 缺少 __version__")
            elif found.group(1) != expected:
                problems.append(
                    f"{repo.name}: pyproject={expected} 与 "
                    f"{init.relative_to(repo)}={found.group(1)} 不一致")
        print(f"{repo.name:26} {expected:8}")

    if problems:
        print("\n版本检查失败:", file=sys.stderr)
        for item in problems:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("\n版本检查通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())