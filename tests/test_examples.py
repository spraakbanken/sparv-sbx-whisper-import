import shutil
from pathlib import Path

import sparv
from syrupy.assertion import SnapshotAssertion


def test_example_hello_whisper_mp3(setup_sparv: None, snapshot: SnapshotAssertion) -> None:  # noqa: ARG001
    base_dir = Path("examples/hello-whisper-mp3")
    export_dir = base_dir / "export"
    snakemake_dir = base_dir / ".snakemake"
    sparv_workdir = base_dir / "sparv-workdir"
    if export_dir.exists():
        shutil.rmtree(export_dir, ignore_errors=False)
    if snakemake_dir.exists():
        shutil.rmtree(snakemake_dir, ignore_errors=False)
    if sparv_workdir.exists():
        shutil.rmtree(sparv_workdir, ignore_errors=False)

    args = ["--dir", "examples/hello-whisper-mp3", "run", "xml_export:pretty", "--log", "--cores", "1"]

    with sparv.call(args) as sparv_call:
        for log_message in sparv_call:
            print(log_message)  # noqa: T201
        success = sparv_call.get_return_value()
        assert success

    export_file = export_dir / "xml_export.pretty" / "aspenstrom_varldsforklaring_aspenstrom_export.xml"

    export_content = export_file.read_text()

    assert export_content == snapshot
