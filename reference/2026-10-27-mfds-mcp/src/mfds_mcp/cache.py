"""응답 캐시 · 하루 호출 수.

- 캐시 키 = sha256(서비스 | 오퍼레이션 | 키 뺀 파라미터를 이름순 정렬한 질의 문자열). 페이지 번호는 키에서 빼고 파일 이름에 붙인다.
- 파일 이름은 해시 + 페이지 번호뿐이다(질의 문자열 · URL 을 파일 이름에 쓰지 않는다).
- 내용은 API 원본 응답 JSON 그대로 + fetched_at + 키 뺀 query.
- 호출 수는 `_calls/<YYYY-MM-DD>.json`(한국 시간 날짜)에 서비스별로 센다. 캐시 적중은 세지 않는다.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

KST = timezone(timedelta(hours=9))


def cache_key(service: str, operation: str, query: dict[str, Any]) -> str:
    params = {k: v for k, v in query.items() if k != "pageNo"}
    qs = urlencode(sorted((k, str(v)) for k, v in params.items()))
    return hashlib.sha256(f"{service}|{operation}|{qs}".encode()).hexdigest()


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


class Cache:
    def __init__(self, root: Path, ttl_days: int) -> None:
        self.root = root
        self.ttl = timedelta(days=ttl_days)

    def _path(self, key: str, page: int) -> Path:
        return self.root / f"{key}_p{page}.json"

    def get(self, key: str, page: int, now: datetime | None = None) -> dict[str, Any] | None:
        path = self._path(key, page)
        if not path.is_file():
            return None
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
            fetched_at = datetime.fromisoformat(entry["fetched_at"])
        except (ValueError, KeyError, OSError):
            return None
        if (now or datetime.now(UTC)) - fetched_at > self.ttl:
            return None
        return entry

    def put(self, key: str, page: int, query: dict[str, Any], response: Any, fetched_at: datetime) -> dict[str, Any]:
        entry = {"fetched_at": fetched_at.isoformat(), "query": query, "response": response}
        _write_json(self._path(key, page), entry)
        return entry

    def stats(self) -> dict[str, int]:
        entries = 0
        size = 0
        if self.root.is_dir():
            for p in self.root.glob("*_p*.json"):
                entries += 1
                size += p.stat().st_size
        return {"entries": entries, "bytes": size}


class CallCounter:
    def __init__(self, root: Path) -> None:
        self.dir = root / "_calls"

    @staticmethod
    def today(now: datetime | None = None) -> str:
        return (now or datetime.now(UTC)).astimezone(KST).date().isoformat()

    def _path(self, day: str) -> Path:
        return self.dir / f"{day}.json"

    def counts(self, now: datetime | None = None) -> dict[str, int]:
        path = self._path(self.today(now))
        if not path.is_file():
            return {}
        try:
            return {str(k): int(v) for k, v in json.loads(path.read_text(encoding="utf-8")).items()}
        except (ValueError, OSError, AttributeError):
            return {}

    def total(self, now: datetime | None = None) -> int:
        return sum(self.counts(now).values())

    def add(self, service: str, now: datetime | None = None) -> None:
        counts = self.counts(now)
        counts[service] = counts.get(service, 0) + 1
        _write_json(self._path(self.today(now)), counts)
