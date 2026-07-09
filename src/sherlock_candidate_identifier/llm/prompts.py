"""Prompt construction for single-participant role assessment."""

import json

from sherlock_candidate_identifier.models import MeetingState, Participant


def build_participant_prompt(participant: Participant, state: MeetingState) -> str:
    """Build a grounded prompt that evaluates exactly one participant."""

    metadata = state.metadata
    meeting_speaking_seconds = sum(
        item.speaking_duration_seconds for item in state.participants.values()
    )
    speaking_share = (
        participant.speaking_duration_seconds / meeting_speaking_seconds
        if meeting_speaking_seconds
        else 0.0
    )
    context = {
        "candidate_metadata": {
            "name": metadata.candidate_name,
            "email": metadata.candidate_email,
            "calendar_title": metadata.calendar_title,
            "interviewer_names": metadata.interviewer_names,
            "interviewer_emails": metadata.interviewer_emails,
        },
        "participant": {
            "display_name": participant.display_name,
            "email": participant.email,
            "transcript": participant.transcript_text,
            "speaking_statistics": {
                "duration_seconds": participant.speaking_duration_seconds,
                "turn_count": participant.speaking_turn_count,
                "transcript_turn_count": participant.transcript_turn_count,
                "meeting_speaking_share": round(speaking_share, 4),
            },
            "camera_status": participant.camera_on,
            "face_count": participant.face_count,
            "webcam_activity": participant.webcam_activity_score,
        },
    }
    return (
        "Evaluate only the participant in the supplied interview context. "
        "Determine whether their role is candidate, interviewer, observer, or unknown. "
        "Use weak signals together and remain uncertain when evidence is insufficient. "
        "Score ranges from -1 (definitely not candidate) to 1 (definitely candidate); "
        "confidence ranges from 0 to 1. Return only JSON with keys role, score, "
        "confidence, reason, and evidence.\n\n"
        f"Context:\n{json.dumps(context, ensure_ascii=True, indent=2)}"
    )
