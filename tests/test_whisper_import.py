from syrupy.assertion import SnapshotAssertion

from sbx_whisper_import import whisper_import


def test_transcribe_and_prepare_spans(snapshot: SnapshotAssertion) -> None:
    text, spans, starts, ends = whisper_import._transcribe_and_prepare_spans(
        model_size="tiny",
        model_verbosity="standard",
        temperature=0.0,
        source_filename="assets/aspenstrom_varldsforklaring_aspenstrom.mp3",
    )

    assert text == snapshot
    assert spans == snapshot
    assert starts == snapshot
    assert ends == snapshot
