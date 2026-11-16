# -*- coding: utf-8 -*-
"""형태소 분석기 호출·캐시(V3.3-B · 발주서 silver-build-8-brief.md 절대 규칙).

kiwipiepy(판 고정 0.24 · 실제 0.24.1)는 `silver-v3/.venv-kiwi` 에만 있다. build.py 는 시스템 python3 로 돌므로 분석기 호출은
`.venv-kiwi/bin/python lib/kiwi_worker.py` 서브프로세스로 감싸고, 결과를 캐시에 보존한다.
  캐시 키 = 분석기 판 + 등록 사전 해시(사용자 단어로 등록한 사전 표면형 전부의 sha256) + 문구(NFC · 글자 그대로).
  정본 캐시 = `silver-v3/cache/kiwi-cache.json`(빌드마다 누적 · 없으면 venv 로 채운다) · 산출 = `out/kiwi-cache.json`(이번 빌드가 실제로 읽은 항목만 · 정렬 · 재실행 바이트 동일).
캐시에 전부 있으면 venv 없이도 같은 결과(check ④). 캐시에 없는 문구가 있고 venv 도 없으면 빌드 거부(BuildRefused).
"""
import hashlib
import json
import os
import subprocess
import unicodedata
from collections import OrderedDict

from .load import BuildRefused

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CACHE = os.path.join(HERE, "cache", "kiwi-cache.json")
DEFAULT_PYTHON = os.path.join(HERE, ".venv-kiwi", "bin", "python")
WORKER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kiwi_worker.py")
TOP_N = 10


def nfc(s):
    return unicodedata.normalize("NFC", str(s))


class Analyzer:
    """사전 표면형을 등록(register)한 뒤 tokens(text)/anom(text) 를 준다. 결과는 전부 캐시에서 — 없으면 venv 워커를 한 번 부른다(ensure 로 미리 모아서)."""

    def __init__(self, cache_path=None, python=None, pinned="0.24", save=True):
        self.cache_path = cache_path or DEFAULT_CACHE
        self.python = python or DEFAULT_PYTHON
        self.pinned = pinned
        self.save_enabled = save
        self.store = {"kiwi_version": None, "top_n": TOP_N, "dicts": {}}
        if os.path.exists(self.cache_path):
            with open(self.cache_path, encoding="utf-8") as f:
                self.store = json.load(f)
        self.dict_hash = None
        self.registered = []
        self.used = {}            # dict_hash → set(text)
        self.calls = 0            # venv 워커 호출 횟수
        self.miss_texts = 0       # 캐시에 없어 워커에 보낸 문구 수
        self.lazy_misses = 0      # ensure 밖에서 생긴 미스(tokens 호출 때)

    # ------------------------------------------------------------------ 등록
    def register(self, surfaces):
        vals = sorted({nfc(v).strip() for v in surfaces if str(v).strip()})
        self.registered = vals
        self.dict_hash = hashlib.sha256("\n".join(vals).encode("utf-8")).hexdigest()
        d = self.store["dicts"].setdefault(self.dict_hash, {"n_registered": len(vals), "registered_sha256": self.dict_hash, "entries": {}})
        d["n_registered"] = len(vals)
        self.used.setdefault(self.dict_hash, set())
        return self.dict_hash

    @property
    def version(self):
        return self.store.get("kiwi_version")

    def _entries(self):
        if self.dict_hash is None:
            raise RuntimeError("Analyzer.register(surfaces) 먼저")
        return self.store["dicts"][self.dict_hash]["entries"]

    # ------------------------------------------------------------------ 채우기
    def ensure(self, texts):
        """캐시에 없는 문구만 모아 워커를 한 번 부른다. → 새로 채운 수."""
        E = self._entries()
        missing = sorted({nfc(t) for t in texts if nfc(t) not in E})
        if not missing:
            return 0
        self._run(missing)
        return len(missing)

    def _run(self, texts):
        if not os.path.exists(self.python):
            raise BuildRefused(f"분석기 캐시({self.cache_path})에 없는 문구 {len(texts)} · 분석기 인터프리터 없음({self.python}) — kiwipiepy {self.pinned} venv 가 필요하다")
        req = {"registered": self.registered, "texts": texts, "top_n": self.store.get("top_n") or TOP_N}
        p = subprocess.run([self.python, WORKER], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
        if p.returncode != 0:
            raise BuildRefused("분석기 워커 실패: " + p.stderr.decode("utf-8", "replace")[-800:])
        res = json.loads(p.stdout.decode("utf-8"))
        ver = res["version"]
        if not str(ver).startswith(self.pinned):
            raise BuildRefused(f"kiwipiepy 판 {ver} ≠ 고정 {self.pinned}(ERD V3.3-B)")
        if self.store.get("kiwi_version") not in (None, ver):
            raise BuildRefused(f"캐시의 kiwipiepy 판 {self.store.get('kiwi_version')} ≠ 지금 {ver} — 캐시를 새로 만들어야 한다")
        self.store["kiwi_version"] = ver
        if res.get("failed"):
            self.store["dicts"][self.dict_hash]["register_failed"] = res["failed"]
        E = self._entries()
        for t, r in res["results"].items():
            E[t] = {"tokens": r["tokens"], "rank": r["rank"], "anom": r["anom"]}
        self.calls += 1
        self.miss_texts += len(texts)
        self.save()

    def save(self):
        if not self.save_enabled:
            return
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        tmp = self.cache_path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(self.store, f, ensure_ascii=False, sort_keys=True, indent=0)
            f.write("\n")
        os.replace(tmp, self.cache_path)

    # ------------------------------------------------------------------ 조회
    def _get(self, text):
        E = self._entries()
        t = nfc(text)
        if t not in E:
            self.lazy_misses += 1
            self._run([t])
        self.used[self.dict_hash].add(t)
        return E[t]

    def tokens(self, text):
        """[(form, tag, start, end)] — 원문 글자 범위(NFC 기준)."""
        return [tuple(x) for x in self._get(text)["tokens"]]

    def anom(self, text):
        return [tuple(x) for x in self._get(text)["anom"]]

    def rank(self, text):
        return self._get(text)["rank"]

    # ------------------------------------------------------------------ 산출(out/kiwi-cache.json)
    def used_dump(self):
        dicts = OrderedDict()
        for dh in sorted(self.used):
            E = self.store["dicts"][dh]["entries"]
            ents = OrderedDict((t, E[t]) for t in sorted(self.used[dh]) if t in E)
            dicts[dh] = OrderedDict([("n_registered", self.store["dicts"][dh]["n_registered"]), ("registered_sha256", dh), ("n_entries", len(ents)), ("entries", ents)])
        return OrderedDict([("analyzer", "kiwipiepy"), ("kiwi_version", self.store.get("kiwi_version")), ("pinned", self.pinned), ("top_n", self.store.get("top_n") or TOP_N),
                            ("key", "kiwi_version + registered_sha256(등록 사전 표면형 전부 · 정렬 · sha256) + text(NFC)"), ("dicts", dicts)])

    def stats(self):
        return {"kiwi_version": self.store.get("kiwi_version"), "pinned": self.pinned, "cache_path": self.cache_path, "worker_calls": self.calls, "miss_texts": self.miss_texts, "lazy_misses": self.lazy_misses,
                "dicts_used": {dh: len(v) for dh, v in self.used.items()}, "entries_used": sum(len(v) for v in self.used.values()), "cache_entries_total": sum(len(d["entries"]) for d in self.store["dicts"].values())}
