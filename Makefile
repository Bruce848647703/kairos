PY ?= python3
REPOS := $(wildcard ../kairos-*)

.PHONY: help test lint versions check

help:
	@echo "targets: test lint versions check"
	@echo "  test      跑所有兄弟仓库的 pytest"
	@echo "  lint      用 ruff 检查所有仓库（F/E9）"
	@echo "  versions  列出各仓库 pyproject 版本"
	@echo "  check     版本一致性 + 全量测试"
	@echo "  可用 PY=/path/to/python make test 指定解释器"

test:
	@set -e; for d in $(REPOS); do \
		echo "== $$d"; \
		(cd $$d && $(PY) -m pytest --tb=short -q); \
	done

lint:
	ruff check $(REPOS) --select F,E9 --exclude build --exclude '*.egg-info' --exclude __pycache__

versions:
	@grep -H '^version = ' $(addsuffix /pyproject.toml,$(REPOS))

check:
	$(PY) scripts/check_versions.py
	$(MAKE) test