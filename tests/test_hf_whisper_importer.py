import pytest
from syrupy.assertion import SnapshotAssertion

from sbx_whisper_import import cli
from sbx_whisper_import.hf_whisper_importer import HFWhisperImporter


def test_aspenstrom(snapshot_json: SnapshotAssertion) -> None:
    res = cli._run_transcription(["--model-size", "tiny", "assets/aspenstrom_varldsforklaring_aspenstrom.mp3"])

    assert res == snapshot_json


def test_invalid_model_size_raises_value_error(snapshot: SnapshotAssertion) -> None:
    with pytest.raises(ValueError) as exc:
        HFWhisperImporter(model_size="huge")

    assert str(exc) == snapshot


def test_invalid_model_verbosity_raises_value_error(snapshot: SnapshotAssertion) -> None:
    with pytest.raises(ValueError) as exc:
        HFWhisperImporter(model_size="medium", model_verbosity="subtitle")

    assert str(exc) == snapshot
