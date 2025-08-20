from syrupy.assertion import SnapshotAssertion

from sbx_whisper_import.hf_whisper_importer import HFWhisperImporter


def test_aspenstrom(snapshot: SnapshotAssertion) -> None:
    importer = HFWhisperImporter(model_id="KBLab/kb-whisper-tiny")

    res = importer.transcribe("assets/aspenstrom_varldsforklaring_aspenstrom.mp3")

    assert snapshot == res["text"]
