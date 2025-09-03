"""Sparv importer for using Whisper."""

from sparv import api as sparv_api
from sparv.api import Config, Output, Source, SourceFilename, SourceStructure, Text

from sbx_whisper_import.hf_whisper_importer import HFWhisperImporter

logger = sparv_api.get_logger(__name__)


@sparv_api.importer(
    "Import audio from MP3 with Whisper",
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
def parse_mp3(
    source_file: SourceFilename = SourceFilename(),
    source_dir: Source = Source(),
    model_size: str = Config("sbx_whisper_import.model_size"),
    model_verbosity: str = Config("sbx_whisper_import.model_verbosity"),
) -> None:
    """Transcribe mp3 file as input to Sparv."""
    transcribe_audio(
        source_file=source_file,
        source_dir=source_dir,
        model_size=model_size,
        model_verbosity=model_verbosity,
        extension=".mp3",
    )


def transcribe_audio(
    source_file: SourceFilename,
    source_dir: Source,
    model_size: str,
    model_verbosity: str,
    extension: str,
) -> None:
    """Transcribe audio file as input to Sparv."""
    importer = HFWhisperImporter(model_size=model_size, model_verbosity=model_verbosity)

    res = importer.transcribe(str(source_dir.get_path(source_file, extension)))

    logger.debug("res=%s", res)

    Text(source_file).write(res["text"])

    utterance_spans: list[tuple[int, int]] = []
    utterance_starts: list[float] = []
    utterance_ends: list[float] = []
    curr_start: int = 0
    curr_end: int = 0
    for chunk in res["chunks"]:
        utterance_starts.append(chunk["timestamp"][0])
        utterance_ends.append(chunk["timestamp"][1])
        curr_end += len(chunk["text"])
        utterance_spans.append((curr_start, curr_end))
        curr_start = curr_end

    # Make up a text annotation surrounding the whole file
    text_annotation = ["text", "text:source_filename", "utterance", "utterance:start", "utterance:end"]
    source_file_name = f"{source_file}{extension}"
    Output("text", source_file=source_file).write([(0, len(res["text"]))])
    Output("text:source_filename", source_file=source_file).write([source_file_name])
    Output("utterance", source_file=source_file).write(utterance_spans)
    Output("utterance:start", source_file=source_file).write(utterance_starts)
    Output("utterance:end", source_file=source_file).write(utterance_ends)
    SourceStructure(source_file).write(text_annotation)
