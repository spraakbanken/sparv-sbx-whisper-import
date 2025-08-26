"""Sparv importer for using Whisper."""

from sparv import api as sparv_api
from sparv.api import Config, Output, Source, SourceFilename, SourceStructure, Text

from sbx_whisper_import.hf_whisper_importer import HFWhisperImporter

logger = sparv_api.get_logger(__name__)


@sparv_api.importer(
    "Import audio with Whsiper",
    file_extension="mp3",
    outputs=["text"],
    text_annotation="text",
    config=[
        Config(
            "sbx_whisper_import.model_size",
            "small",
            description="The size of the model. Defaults to 'small'",
            datatype=str,
        ),
        Config(
            "sbx_whisper_import.model_verbosity",
            "standard",
            description="The verbosity of the model. Defaults to 'standard'",
            datatype=str,
        ),
    ],
)
def parse(
    source_file: SourceFilename = SourceFilename(),
    source_dir: Source = Source(),
    model_size: str = Config("sbx_whisper_import.model_size"),
    model_verbosity: str = Config("sbx_whisper_import.model_verbosity"),
) -> None:
    """Transcribe audio file as input to Sparv."""
    importer = HFWhisperImporter(model_size=model_size, model_verbosity=model_verbosity)

    res = importer.transcribe(str(source_dir.get_path(source_file, ".mp3")))

    logger.debug("res=%s", res)

    Text(source_file).write(res["text"])

    # Make up a text annotation surrounding the whole file
    text_annotation = "text"
    Output(text_annotation, source_file=source_file).write([(0, len(res["text"]))])
    SourceStructure(source_file).write([text_annotation])
