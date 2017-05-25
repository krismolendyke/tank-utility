PIP      := pip
PYTHON   := python
RM       := rm
RM_FLAGS := -rf
SETUP    := setup.py
TOX      := tox
TOX_DIR  := .tox

build_dir := build
dist_dir  := dist
src_dir   := src
test_dir  := tests

.PHONY: help
help:
	@$(MAKE) --print-data-base --question no-such-target | \
	grep -v -e '^no-such-target' -e '^Makefile'	     | \
	awk '/^[^.%][-A-Za-z0-9_]*:/ \
	     { print substr($$1, 1, length($$1)-1) }'        | \
	sort					             | \
	pr -2 -t

.PHONY: install-requirements
install-requirements:
	$(PIP) install --editable .[dev,test]

.PHONY: test
test:
	@$(TOX)

.PHONY: dist
dist:
	$(PYTHON) $(SETUP) sdist bdist_wheel

.PHONY: clean
clean:
	$(RM) $(RM_FLAGS) $(build_dir) $(dist_dir) $(TOX_DIR) *.egg-info .eggs
