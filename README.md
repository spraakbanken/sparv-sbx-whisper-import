# sparv-sbx-whisper-import

Allow Sparv to import audio as text with KB Whisper.

## Prerequisites

- `ffmpeg` installed.

## Usage

[!NOTE] Only one importer can be used and only one file type can be used.

### Install

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

### Annotations

The following annotations are created:

- `text`
- `utterance` with attributes `start` and `end`, in seconds for the audio file.

Sample output:

```xml
<?xml version='1.0' encoding='utf-8'?>
<text>
  <utterance end="6.0" start="0.0">
    <token>Världsförklaring</token>
    <token>.</token>
  </utterance>
</text>
```

### Configuration

The default model size is `small` and the default verbosity is `standard`.

To change the model size and/or model verbosity to use, add the following to your `config.yaml`:

```yaml
import:
  text_annotation: text
  # needed to use sbx_whisper_import
  importer: sbx_whisper_import:parse

sbx_whisper_import:
  # One of "tiny", "base", "small", "medium" or "large"
  model_size: small
  # One of "subtitle", "standard" or "strict" (low verbosity to high verbosity)
  # NOTE: model size "medium" does support the verbosity "subtitle"
  model_verbosity: standard

xml_export:
  annotations:
    - text
    - segment.token
```

## Metadata

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
