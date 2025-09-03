"""Sparv plugin to import audio files as text with Whisper."""

from sbx_whisper_import.whisper_import import parse_mp3

__all__ = ["parse_mp3"]

__description__ = "Import audio files as text with Whisper."

__version__ = "0.1.0"
