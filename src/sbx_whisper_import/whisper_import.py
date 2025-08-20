from sparv import api as sparv_api
from sparv.api import Output, Source, SourceFilename, SourceStructure, Text

from sbx_whisper_import.hf_whisper_importer import HFWhisperImporter

logger = sparv_api.get_logger(__name__)


@sparv_api.importer(
    "Import audio with Whsiper",
    file_extension="mp3",
    outputs=["text"],
    text_annotation="text",
)
def parse(
    source_file: SourceFilename = SourceFilename(),
    source_dir: Source = Source(),
) -> None:
    """Transcribe audio file as input to Sparv."""
    importer = HFWhisperImporter(model_id="KBLab/kb-whisper-tiny")

    res = importer.transcribe(str(source_dir.get_path(source_file, ".mp3")))

    logger.debug("res=%s", res)

    Text(source_file).write(res["text"])

    # Make up a text annotation surrounding the whole file
    text_annotation = "text"
    Output(text_annotation, source_file=source_file).write([(0, len(res["text"]))])
    SourceStructure(source_file).write([text_annotation])
