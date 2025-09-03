import shutil
from pathlib import Path

import pytest
import sparv
from syrupy.assertion import SnapshotAssertion


@pytest.mark.parametrize("extension", ["mp3"])
def test_example_aspenstrom_mp3(extension: str, snapshot: SnapshotAssertion) -> None:
    example = f"examples/aspenstrom-{extension}"
    base_dir = Path(example)
    export_dir = base_dir / "export"
    snakemake_dir = base_dir / ".snakemake"
    sparv_workdir = base_dir / "sparv-workdir"
    if export_dir.exists():
        shutil.rmtree(export_dir, ignore_errors=False)
    if snakemake_dir.exists():
        shutil.rmtree(snakemake_dir, ignore_errors=False)
    if sparv_workdir.exists():
        shutil.rmtree(sparv_workdir, ignore_errors=False)

    args = ["--dir", example, "run", "xml_export:pretty", "--log", "--cores", "1"]

    with sparv.call(args) as sparv_call:
        for log_message in sparv_call:
            print(log_message)  # noqa: T201
        success = sparv_call.get_return_value()
        assert success

    export_file = export_dir / "xml_export.pretty" / "aspenstrom_varldsforklaring_aspenstrom_export.xml"

    export_content = export_file.read_text()

    assert export_content == snapshot
