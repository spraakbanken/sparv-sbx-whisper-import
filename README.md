# sparv-sbx-whisper-import

[![PyPI version](https://badge.fury.io/py/sparv-sbx-whisper-import.svg)](https://pypi.org/project/sparv-sbx-whisper-import)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sparv-sbx-whisper-import)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/sparv-sbx-whisper-import)](https://pypi.org/project/sparv-sbx-whisper-import/)

[![Maturity badge - level 2](https://img.shields.io/badge/Maturity-Level%202%20--%20First%20Release-yellowgreen.svg)](https://github.com/spraakbanken/getting-started/blob/main/scorecard.md)
[![Stage](https://img.shields.io/pypi/status/sparv-sbx-whisper-import)](https://pypi.org/project/sparv-sbx-whisper-import/)

[![CI(release)](https://github.com/spraakbanken/sparv-sbx-whisper-import/actions/workflows/release.yml/badge.svg)](https://github.com/spraakbanken/sparv-sbx-whisper-import/actions/workflows/release.yml)

This [Sparv](https://github.com/spraakbanken/sparv) plugin makes it possible to use audio files as input to Sparv. The audio is transcribed to text using [transformers](https://github.com/huggingface/transformers) and the [KB Whisper models](https://huggingface.co/KBLab/kb-whisper-small).

## Prerequisites

- Python 3.11 or higher
- [Sparv](https://github.com/spraakbanken/sparv)
- [`ffmpeg`](https://ffmpeg.org/) installed and available in your `PATH`

## Install

Install in a virtual environment:

```shell
pip install sparv-sbx-whisper-import
```

or if you have installed [`sparv`](https://github.com/spraakbanken/sparv) with [`pipx`](https://pipx.pypa.io/latest/):

```shell
pipx inject sparv sparv-sbx-whisper-import
```

or if you have installed [`sparv`](https://github.com/spraakbanken/sparv) with [`uv-pipx`](https://github.com/pytgaen/uv-pipx):

```shell
uvpipx install sparv-sbx-whisper-import --inject sparv
```

## Usage

To use audio files as input to Sparv, first create a corpus and a Sparv configuration file. For more information about creating a corpus, see the [Sparv documentation](https://spraakbanken.gu.se/sparv/user-manual/intro/). Possible configuration options are described [below](#configuration).

Once your corpus and configuration file are set up, [run Sparv as usual](https://spraakbanken.gu.se/sparv/user-manual/running-sparv/):

```shell
sparv run
```

### Supported audio formats

> [!NOTE]
> Only one file type and one importer can be used within a corpus. If you want to process multiple file types, please create separate corpora.

The following audio formats are supported:

| Audio format | Importer (in config)           |
| ------------ | ------------------------------ |
| **MP3**      | `sbx_whisper_import:parse_mp3` |
| **OGG**      | `sbx_whisper_import:parse_ogg` |
| **WAV**      | `sbx_whisper_import:parse_wav` |

Do you miss some audio format?
Please check the [tracking issue](https://github.com/spraakbanken/sparv-sbx-whisper-import/issues/16) or open a new issue to request support for additional formats.

### Command-line interface

You can use this plugin from the command-line as

```shell
# Activate virtual environment
> sbx-whisper-import --help
usage: sbx-whisper-import [-h] [--model-size MODEL_SIZE] [--verbosity VERBOSITY] INPUT

Transcribe audio file with KB-Whisper. Output is in JSON.

positional arguments:
  INPUT                 audio input to trancribe in one of the formats MP3, OGG or WAV

options:
  -h, --help            show this help message and exit
  --model-size MODEL_SIZE
                        set the size of the model
  --verbosity VERBOSITY
                        set the verbosity of the model
```

## Configuration

To use this plugin, specify the appropriate importer for your audio files in the Sparv configuration file (`config.yaml`).

The default model size is `small` and the default verbosity is `standard`. You can change these settings as described below.

```yaml
import:
  text_annotation: text
  # needed to use sbx_whisper_import, use one of the lines below
  importer: sbx_whisper_import:parse_mp3
  # importer: sbx_whisper_import:parse_ogg
  # importer: sbx_whisper_import:parse_wav

sbx_whisper_import:
  # One of "tiny", "base", "small", "medium" or "large"
  model_size: small
  # One of "subtitle", "standard" or "strict" (low verbosity to high verbosity)
  # NOTE: model size "medium" does support the verbosity "subtitle"
  model_verbosity: standard

export:
  annotations:
    - text
    - <token>
```

## Annotations

The following annotations are created by the plugin:

- `text` with the attribute `source_filename`, which indicates the name of the audio file from which the text was transcribed.
- `utterance` with the attributes `start` and `end`, which indicate the timestamps (in seconds) of the utterance within the audio file.

Sample output:

```xml
<?xml version='1.0' encoding='utf-8'?>
<text source_filename="example.mp3">
  <utterance end="6.0" start="0.0">
    <token>Världsförklaring</token>
    <token>.</token>
  </utterance>
</text>
```

## Metadata

The following table lists the exact models and revisions used for each combination of model size and model verbosity.

| Model Size | Model Verbosity | Model used                                                                | Revision used                              |
| ---------- | --------------- | ------------------------------------------------------------------------- | ------------------------------------------ |
| `tiny`     | `subtitle`      | [KBLab/kb-whisper-tiny](https://huggingface.co/KBLab/kb-whisper-tiny)     | `238d279d9821c32b905fcaff6ce9dad38ad00ab7` |
| `tiny`     | `standard`      | [KBLab/kb-whisper-tiny](https://huggingface.co/KBLab/kb-whisper-tiny)     | `e2bca57c3eee6144b9fefd07749580034cfa9686` |
| `tiny`     | `strict`        | [KBLab/kb-whisper-tiny](https://huggingface.co/KBLab/kb-whisper-tiny)     | `ea2a872f41f543aaadea23e185e974d1ab29ba2b` |
| `base`     | `subtitle`      | [KBLab/kb-whisper-base](https://huggingface.co/KBLab/kb-whisper-base)     | `7a57b541ccf4aebef73ecfdc064ef4b5cab3b02e` |
| `base`     | `standard`      | [KBLab/kb-whisper-base](https://huggingface.co/KBLab/kb-whisper-base)     | `1ee0facc30bb1f26492bb1360a99d552e25a31c2` |
| `base`     | `strict`        | [KBLab/kb-whisper-base](https://huggingface.co/KBLab/kb-whisper-base)     | `be19431a3fb78b71ac1525bcafe792220b314c9e` |
| `small`    | `subtitle`      | [KBLab/kb-whisper-small](https://huggingface.co/KBLab/kb-whisper-small)   | `8d49820338edb72829d1c44fa70a2ba94a4a20fa` |
| `small`    | `standard`      | [KBLab/kb-whisper-small](https://huggingface.co/KBLab/kb-whisper-small)   | `728c681653e2732ff64618e7f607f509ec87472a` |
| `small`    | `strict`        | [KBLab/kb-whisper-small](https://huggingface.co/KBLab/kb-whisper-small)   | `066ef166dd25b4b27039517ca77af30c1c10688a` |
| `medium`   | `subtitle`      | NOTE: subtitle not present for kb-whisper-medium                          | -                                          |
| `medium`   | `standard`      | [KBLab/kb-whisper-medium](https://huggingface.co/KBLab/kb-whisper-medium) | `32529a74c6662479625746edce7f16fe743fe011` |
| `medium`   | `strict`        | [KBLab/kb-whisper-medium](https://huggingface.co/KBLab/kb-whisper-medium) | `51990d2cd5d0cf120b3eceb812bc5407a171a220` |
| `large`    | `subtitle`      | [KBLab/kb-whisper-large](https://huggingface.co/KBLab/kb-whisper-large)   | `50b62f493fa513926007d388f76cce9659bce123` |
| `large`    | `standard`      | [KBLab/kb-whisper-large](https://huggingface.co/KBLab/kb-whisper-large)   | `9e03cd21c14d02c57c33ae90b5803b54995ff241` |
| `large`    | `strict`        | [KBLab/kb-whisper-large](https://huggingface.co/KBLab/kb-whisper-large)   | `ea0a8ac1cda8eab8777bf8d74440eb7606825d8f` |

## Changelog

This project keeps a [changelog](./CHANGELOG.md).

## Minimum supported Python version

This library tries to support as many Python versions as possible.
When a Python version is added or dropped, this library's minor version is bumped.

- v0.1.0: Python 3.11

## Development

### Development prerequisites

- [`uv`](https://docs.astral.sh/uv/)
- [`pre-commit`](https://pre-commit.org)

For starting to develop on this repository:

- Clone the repo `git clone https://github.com/spraakbanken/sparv-sbx-whisper-import.git`
- Setup environment: `make dev`
- Install `pre-commit` hooks: `pre-commit install`

Do your work.

Tasks to do:

- Test the code with `make test` or `make test-w-coverage`.
- Test the examples with `make test-examples`.
- Lint the code with `make lint`.
- Check formatting with `make check-fmt`.
- Format the code with `make fmt`.
- Type-check the code with `make type-check`.

This repo uses [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

### Release a new version

- Prepare the CHANGELOG: `make prepare-release` and then edit `CHANGELOG.md`.
- Add to git: `git add CHANGELOG.md`
- Commit with `git commit -m 'chore(release): prepare release'` or `cog commit chore 'prepare release' release`.
- Bump version (depends on [`bump-my-version](https://callowayproject.github.io/bump-my-version/))
  - Major: `make bumpversion part=major`
  - Minor: `make bumpversion part=minor`
  - Patch: `make bumpversion part=patch` or `make bumpversion`
- Push `main` and tags to GitHub: `git push main --tags` or `make publish`
  - GitHub Actions will build, test and publish the package to [PyPi](https://pypi.prg).
- Add metadata for [Språkbanken's resource](https://spraakbanken.gu.se/resurser)
  - Generate metadata: `make generate-metadata`
  - Upload the files from `examples/metadata/export/sbx_metadata/utility` to <https://github.com/spraakbanken/metadata/tree/main/yaml/analysis>.

## License

This repository is licensed under the [MIT](./LICENSE) license.
