"""걷혀 나간 잔디 잡의 잔여 테스트 (KDEV-WORK-017 P5).

`TestWriteDaily`·`TestLLM*` 계열은 `main_job`·`llm`·`upsert` 와 함께 지웠다 —
그 코드가 사라졌으므로 붙들고 있으면 걷어낸 경로를 되살리는 압력이 된다.
남은 것은 여전히 쓰이는 `read_daily_narrative` 하나다.
"""

from __future__ import annotations

from datetime import date

from service.jobs.inputs import read_daily_narrative


class TestDailyNarrativeRead:
    def test_returns_none_when_missing(self):
        assert read_daily_narrative(date(2099, 1, 1)) is None

    def test_returns_body_when_exists(self):
        # M1에서 박은 daily/2026-05-01.md 활용
        body = read_daily_narrative(date(2026, 5, 1))
        assert body is not None
        assert "오늘 한 일" in body
