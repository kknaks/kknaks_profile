"""Apply Executor — 승인된 것을 실제 파일·커밋으로 (KDEV-WORK-015 P4)."""

from .executor import ApplyOutcome, apply_item, latest_plan

__all__ = ["ApplyOutcome", "apply_item", "latest_plan"]
