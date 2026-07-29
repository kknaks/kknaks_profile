"""승인 파이프라인 — 접수 → 자동 준비 → 게이트 체인 (KDEV-WORK-014).

`service/knowledge_capture/` 와의 경계: 저쪽은 **노트 한 건을 만드는 법**(AI 호출·파싱·
렌더)을 안다. 이쪽은 **언제 무엇을 만들지 사람이 정하는 절차**를 안다.
"""

from .definitions import PIPELINES, Pipeline, Stage, pipeline_for
from .flow import harvest_preparation, start_preparation
from .intake import IntakeResult, intake
from .prepare import (
    PREPARABLE_STATUSES,
    PrepareResult,
    Summarizer,
)
from .urls import detect_source_kind, normalize_url, youtube_video_id

__all__ = [
    "PIPELINES",
    "Pipeline",
    "Stage",
    "pipeline_for",
    "start_preparation",
    "harvest_preparation",
    "IntakeResult",
    "intake",
    "PREPARABLE_STATUSES",
    "PrepareResult",
    "Summarizer",
    "detect_source_kind",
    "normalize_url",
    "youtube_video_id",
]
