"""Signal modules that generate independent evidence."""

from sherlock_candidate_identifier.signals.base import CandidateSignal
from sherlock_candidate_identifier.signals.behavior_signal import BehaviorSignal
from sherlock_candidate_identifier.signals.llm_signal import LLMSignal
from sherlock_candidate_identifier.signals.metadata_signal import MetadataSignal
from sherlock_candidate_identifier.signals.name_signal import NameSignal
from sherlock_candidate_identifier.signals.transcript_signal import TranscriptSignal
from sherlock_candidate_identifier.signals.video_signal import VideoSignal

__all__ = [
    "BehaviorSignal",
    "CandidateSignal",
    "LLMSignal",
    "MetadataSignal",
    "NameSignal",
    "TranscriptSignal",
    "VideoSignal",
]
