"""Whisper importer using transformers."""

import typing as t

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


class TranscribeChunk(t.TypedDict):
    """Chunked text with timestamp (start, end)."""

    timestamp: tuple[float, float]
    text: str


class TranscribeResult(t.TypedDict):
    """Result from transcribe."""

    text: str
    chunks: list[TranscribeChunk]


class HFWhisperImporter:
    def __init__(self, *, model_id: str) -> None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            use_safetensors=True,
        )
        model.to(device)
        processor = AutoProcessor.from_pretrained(model_id)

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )

        generate_kwargs = {
            "task": "transcribe",
            "language": "sv",
        }

        self._pipe = pipe
        self._generate_kwargs = generate_kwargs

    def transcribe(self, audio_path: str) -> TranscribeResult:
        """Transcribe audio from given path.

        Args:
            audio_path: A path to the audio to transcribe.

        Returns:
            The transcribed text along with chunks.
        """
        return self._pipe(audio_path, chunk_length_s=30, generate_kwargs=self._generate_kwargs, return_timestamps=True)


if __name__ == "__main__":
    import sys

    importer = HFWhisperImporter(model_id="KBLab/kb-whisper-tiny")
    audio_path = sys.argv[1]

    res = importer.transcribe(audio_path)
    print(res)
