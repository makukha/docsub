SHELL=/bin/bash -euo pipefail


.PHONY: build
build: dist

dist: src/**/* pyproject.toml README.md uv.lock
	uv lock
	rm -rf $@
	cd $(@D) && uv build -o dist


.PHONY: docs
docs: \
	README.md \
	docs/_static/badge-coverage.svg \
	docs/_static/badge-tests.svg

README.md: FORCE
	uv run docsub sync -i $@

docs/_static/badge-coverage.svg: .tmp/coverage.xml
	uv run genbadge coverage --local -i $< -o $@

docs/_static/badge-tests.svg: .tmp/junit.xml
	uv run genbadge tests --local -i $< -o $@


FORCE:
