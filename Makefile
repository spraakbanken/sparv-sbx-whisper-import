
# use this Makefile as base in your project by running
# git remote add make https://github.com/spraakbanken/python-uv-make-conf
# git fetch make
# git merge --allow-unrelated-histories make/main
#
# To later update this makefile:
# git fetch make
# git merge make/main
#
.default: help

.PHONY: help
help:
	@echo "usage:"
	@echo "dev | install-dev"
	@echo "   setup development environment"
	@echo "install"
	@echo "   setup production environment"
	@echo ""
	@echo "info"
	@echo "   print info about the system and project"
	@echo ""
	@echo "test"
	@echo "   run all tests"
	@echo ""
	@echo "test-w-coverage [cov=] [cov_report=]"
	@echo "   run all tests with coverage collection. (Default: cov_report='term-missing', cov='--cov=${PROJECT_SRC}')"
	@echo ""
	@echo "lint"
	@echo "   lint the code"
	@echo ""
	@echo "lint-fix"
	@echo "   lint the code and try to fix it"
	@echo ""
	@echo "type-check"
	@echo "   check types"
	@echo ""
	@echo "fmt"
	@echo "   format the code"
	@echo ""
	@echo "check-fmt"
	@echo "   check that the code is formatted"
	@echo ""
	@echo "bumpversion [part=]"
	@echo "   bumps the given part of the version of the project. (Default: part='patch')"
	@echo ""
	@echo "bumpversion-show"
	@echo "   shows the bump path that is possible"
	@echo ""
	@echo "publish [branch=]"
	@echo "   pushes the given branch including tags to origin, for CI to publish based on tags. (Default: branch='main')"
	@echo "   Typically used after 'make bumpversion'"
	@echo ""
	@echo "prepare-release"
	@echo "   run tasks to prepare a release"
	@echo ""

PLATFORM := `uname -o`
REPO := spraakbanken/sparv-sbx-whisper-import
PROJECT_SRC := src/sbx_whisper_import

ifeq (${VIRTUAL_ENV},)
  VENV_NAME = .venv
  INVENV = uv run
else
  VENV_NAME = ${VIRTUAL_ENV}
  INVENV =
endif

default_cov := "--cov=${PROJECT_SRC}"
cov_report := "term-missing"
cov := ${default_cov}

all_tests := tests
tests := tests

info:
	@echo "Platform: ${PLATFORM}"
	@echo "INVENV: '${INVENV}'"

dev: install-dev

# setup development environment
install-dev: install-pre-commit
	uv sync --all-packages --dev

# install pre-commit hooks
install-pre-commit: .git/hooks/pre-commit
.git/hooks/pre-commit: .pre-commit-config.yaml
	@if command -v pre-commit > /dev/null; then pre-commit install; else echo "WARN: 'pre-commit' not installed"; fi

# setup production environment
install:
	uv sync --all-packages --no-dev

lock: uv.lock

uv.lock: pyproject.toml
	uv lock

.PHONY: test
test:
	${INVENV} pytest -vv ${tests}

.PHONY: test-w-coverage
# run all tests with coverage collection
test-w-coverage:
	${INVENV} pytest -vv ${cov} --cov-report=term-missing --cov-report=xml:coverage.xml --cov-report=lcov:coverage.lcov ${all_tests}

.PHONY: doc-tests
doc-tests:
	${INVENV} pytest ${cov} --cov-report=term-missing --cov-report=xml:coverage.xml --cov-report=lcov:coverage.lcov --doctest-modules ${PROJECT_SRC}

.PHONY: type-check
# check types
type-check:
	${INVENV} mypy ${PROJECT_SRC} ${tests}

.PHONY: lint
# lint the code
lint:
	${INVENV} ruff check ${PROJECT_SRC} ${tests}

.PHONY: lint-fix
# lint the code (and fix if possible)
lint-fix:
	${INVENV} ruff check --fix ${PROJECT_SRC} ${tests}

part := "patch"
bumpversion:
	${INVENV} bump-my-version bump ${part}

bumpversion-show:
	${INVENV} bump-my-version show-bump

# run formatter(s)
fmt:
	${INVENV} ruff format ${PROJECT_SRC} ${tests}

.PHONY: check-fmt
# check formatting
check-fmt:
	${INVENV} ruff format --check ${PROJECT_SRC} ${tests}

build:
	uv build

branch := "main"
publish:
	git push -u origin ${branch} --tags


.PHONY: prepare-release
prepare-release: update-changelog tests/requirements-testing.lock

# we use lock extension so that dependabot doesn't pick up changes in this file
tests/requirements-testing.lock: pyproject.toml
	uv export --dev --format requirements-txt --no-hashes --no-emit-project --output-file $@

.PHONY: update-changelog
update-changelog: CHANGELOG.md

.PHONY: CHANGELOG.md
CHANGELOG.md:
	git cliff --unreleased --prepend $@

# update snapshots for `syrupy`
.PHONY: snapshot-update
snapshot-update:
	${INVENV} pytest --snapshot-update

### === project targets below this line ===
install-dev-metadata:
	uv sync --all-packages --group metadata --dev

.PHONY: generate-metadata
generate-metadata: install-dev-metadata src/sbx_whisper_import/metadata.yaml
	rm -rf examples/metadata/export/sbx_metadata
	cd examples/metadata; ${INVENV} sparv run sbx_metadata:plugin_analysis_metadata_export

assets:
	test -d $@ || mkdir $@

download-audio: assets/aspenstrom_varldsforklaring_aspenstrom.mp3\
	assets/aspenstrom_trappan_aspenstrom.mp3

assets/aspenstrom_varldsforklaring_aspenstrom.mp3: assets
	curl https://litteraturbanken.se/ljudochbild/wp-content/uploads/2019/11/aspenstrom_varldsforklaring_aspenstrom.mp3 --output "$@"

assets/aspenstrom_trappan_aspenstrom.mp3: assets
	curl https://litteraturbanken.se/ljudochbild/wp-content/uploads/2019/11/aspenstrom_trappan_aspenstrom.mp3 --output "$@"

assets/%.wav: assets/%.mp3
	ffmpeg -i $< -y $@

assets/%.ogg: assets/%.mp3
	ffmpeg -i $< -y $@

prepare-assets: download-audio\
	assets/aspenstrom_varldsforklaring_aspenstrom.wav\
	assets/aspenstrom_trappan_aspenstrom.wav\
	assets/aspenstrom_varldsforklaring_aspenstrom.ogg\
	assets/aspenstrom_trappan_aspenstrom.ogg

test-aspenstrom-mp3:
	rm -rf examples/aspenstrom-mp3/.snakemake examples/aspenstrom-mp3/export examples/aspenstrom-mp3/sparv-workdir
	cd examples/aspenstrom-mp3; ${INVENV} sparv run --stats
	diff examples/aspenstrom-mp3/export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.xml\
	    examples/aspenstrom-mp3/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml
	diff examples/aspenstrom-mp3/export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.xml\
	    examples/aspenstrom-mp3/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml

test-aspenstrom-ogg:
	rm -rf examples/aspenstrom-ogg/.snakemake examples/aspenstrom-ogg/export examples/aspenstrom-ogg/sparv-workdir
	cd examples/aspenstrom-ogg; ${INVENV} sparv run --stats
	diff examples/aspenstrom-ogg/export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.xml\
	    examples/aspenstrom-ogg/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml
	diff examples/aspenstrom-ogg/export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.xml\
	    examples/aspenstrom-ogg/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml

test-aspenstrom-wav:
	rm -rf examples/aspenstrom-wav/.snakemake examples/aspenstrom-wav/export examples/aspenstrom-wav/sparv-workdir
	cd examples/aspenstrom-wav; ${INVENV} sparv run --stats
	diff examples/aspenstrom-wav/export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.xml\
	    examples/aspenstrom-wav/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml
	diff examples/aspenstrom-wav/export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.xml\
	    examples/aspenstrom-wav/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml

test-examples: test-aspenstrom-mp3 test-aspenstrom-wav

update-example-snapshots: update-aspenstrom-mp3-snapshot update-aspenstrom-ogg-snapshot update-aspenstrom-wav-snapshot

update-aspenstrom-mp3-snapshot:\
	examples/aspenstrom-mp3/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml\
	examples/aspenstrom-mp3/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml

examples/aspenstrom-mp3/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml: examples/aspenstrom-mp3/export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.xml
		@cp $< $@

examples/aspenstrom-mp3/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml: examples/aspenstrom-mp3/export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.xml
	@cp $< $@


update-aspenstrom-ogg-snapshot:\
	examples/aspenstrom-ogg/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml\
	examples/aspenstrom-ogg/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml

examples/aspenstrom-ogg/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml: examples/aspenstrom-ogg/export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.xml
		@cp $< $@

examples/aspenstrom-ogg/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml: examples/aspenstrom-ogg/export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.xml
	@cp $< $@

update-aspenstrom-wav-snapshot:\
	examples/aspenstrom-wav/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml\
	examples/aspenstrom-wav/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml

examples/aspenstrom-wav/expected_export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.gold.xml: examples/aspenstrom-wav/export/xml_export.pretty/aspenstrom_trappan_aspenstrom_export.xml
		@cp $< $@

examples/aspenstrom-wav/expected_export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.gold.xml: examples/aspenstrom-wav/export/xml_export.pretty/aspenstrom_varldsforklaring_aspenstrom_export.xml
	@cp $< $@
