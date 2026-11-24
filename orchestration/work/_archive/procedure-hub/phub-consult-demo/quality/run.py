"""상담 품질 기준선 측정 — 빈 포트에 앱을 띄워 시나리오를 실제 HTTP 경로로 흘린다(실제 이해 · 답 호출).

차례: 앱 기동(18222 와 같은 env · 장부는 따로 CHAT_DIR) → 시나리오마다 `GET /`(새 대화) → 턴마다 `POST /c/<id>/turns`
→ SSE `/c/<id>/turns/<n>/events` 가 `done | turn_error` 까지 → `GET /c/<id>/items`(화면 목록 · 주제 머리 · 얼굴 점 조각)
→ 끝나면 장부 줄을 대화 id 로 모아 턴마다 한 줄(`turns.jsonl`)로 남긴다 → 앱을 끈다.

실행(cwd 무관):
  python3 run.py --port 18241 --runs 3 --par 4 [--only S01,S03] [--ledger-dir <스크래치>] [--app <앱 폴더> --app-commit <커밋>]
  (--app: git archive 로 푼 앱 폴더 등 — 기본 = 앱 워크트리 · SPEC-012 WP-0 은 35b56e5 를 따로 풀어 돌림)
결과: out/base-<시각>/turns.jsonl · conv_ids.json · screens/<run>-<sid>-T<n>.html · meta.json
장부 원본(병원 가격이 든 「## 자료」 포함)은 --ledger-dir 에만 두고, 결과에는 필요한 칸만 옮긴다.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = Path("/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo")
ENV = {
    "CHAT_STATE": "on",
    "CHAT_KOS_MAP": "data/kos/myeongdong-mapping-20261120-v3.json",
    "CHAT_KOS_MAP_SHA": "d21903f5",
    "CHAT_IMAGE_DIR": "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images",
}
FORBIDDEN_PORTS = {18222, 18105}
HUB_HEALTH = "http://127.0.0.1:18105/procedure-hub/gold/health"  # 앱 기본 허브(GET 만) — 측정 gold 고정(SPEC-012 C1 · C2)


def hub_build() -> dict:
    """허브 gold_hash · aux_hash · loaded_at(GET) — 못 읽으면 error 칸."""
    try:
        st, _, body = http("GET", HUB_HEALTH, timeout=20)
        b = json.loads(body).get("build") or {}
        return {k: b.get(k) for k in ("gold_hash", "aux_hash", "loaded_at")}
    except Exception as e:  # noqa: BLE001
        return {"error": type(e).__name__}


def tree_hashes(app: Path) -> dict:
    """프롬프트 파일 · git diff · 미추적 포함 해시(sha256 앞 16). git 폴더가 아니면 프롬프트만."""
    import hashlib
    out = {"prompt_sha": hashlib.sha256((app / "prompts/consult.json").read_bytes()).hexdigest()[:16]}
    try:
        diff = subprocess.run(["git", "-C", str(app), "diff"], capture_output=True, check=True).stdout
        names = subprocess.run(["git", "-C", str(app), "ls-files", "--others", "--exclude-standard"], capture_output=True,
                               check=True, text=True).stdout.split()
        extra = b"".join((app / n).read_bytes() for n in names)
        out["diff_sha"] = hashlib.sha256(diff).hexdigest()[:16]
        out["diff_untracked_sha"] = hashlib.sha256(diff + extra).hexdigest()[:16]
    except Exception as e:  # noqa: BLE001
        out["git_error"] = type(e).__name__
    return out


# ---------- HTTP ----------
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # noqa: D401
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def http(method: str, url: str, data: dict | None = None, timeout: float = 60) -> tuple[int, dict, str]:
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method)
    if body is not None:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with OPENER.open(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read().decode("utf-8", "replace") if e.fp else ""


def wait_turn(base: str, cid: str, n: int, timeout: float = 600) -> str:
    """SSE 를 읽어 done · turn_error 를 기다린다(끊기면 다시 붙음)."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            req = urllib.request.Request(f"{base}/c/{cid}/turns/{n}/events")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if r.status == 204:
                    return "gone"
                for raw in r:
                    ln = raw.decode("utf-8", "replace").strip()
                    if ln.startswith("event:"):
                        ev = ln.split(":", 1)[1].strip()
                        if ev in ("done", "turn_error"):
                            return ev
            return "closed"
        except urllib.error.HTTPError as e:
            if e.code == 204:
                return "gone"
            time.sleep(2)
        except Exception:  # noqa: BLE001 — 끊김 → 다시
            time.sleep(2)
    return "timeout"


# ---------- 화면 조각 읽기 ----------
class Screen(HTMLParser):
    """`#procedure-list` + `#face-marks` 조각 → 주제 머리 · 지금 주제 · 카드 · 점."""

    def __init__(self) -> None:
        super().__init__()
        self.topics: list[dict] = []
        self.cards: list[dict] = []
        self.dots: list[dict] = []
        self.labels: list[dict] = []
        self.site_filter: str | None = None
        self._topic: dict | None = None
        self._in_cond = False
        self._in_name = False
        self._card: dict | None = None
        self._in_label: dict | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        if a.get("id") == "procedure-list":
            self.site_filter = a.get("data-site-filter")
        if tag == "details" and "cs-topic" in cls.split():
            self._topic = {"id": a.get("data-topic-id"), "current": "data-topic-current" in a, "conds": []}
            self.topics.append(self._topic)
        if tag == "span" and "cs-topic__cond" in cls.split() and self._topic is not None:
            self._in_cond = True
            self._topic["conds"].append("")
        if tag == "article" and "cs-pcard" in cls.split():
            self._card = {"code": a.get("data-code"), "kind": a.get("data-kind"), "site": a.get("data-site"),
                          "points": a.get("data-points"), "name": ""}
            self.cards.append(self._card)
        if tag == "div" and "cs-pcard__name" in cls.split():
            self._in_name = True
        if tag == "span" and "cs-pcard__unit" in cls.split():
            self._in_name = False
        if tag == "circle" and "cs-dot" in cls.split():
            self.dots.append({"site": a.get("data-site-code"), "other": "cs-dot--other" in cls.split(),
                              "topic": a.get("data-topic"), "pressed": a.get("aria-pressed") == "true"})
        if tag == "span" and "cs-label" in cls.split():
            self._in_label = {"site": a.get("data-site-code"), "other": "cs-label--other" in cls.split(), "name": ""}
            self.labels.append(self._in_label)

    def handle_endtag(self, tag):
        if tag == "span":
            self._in_cond = False
            self._in_label = None
        if tag == "div":
            self._in_name = False
        if tag == "article":
            self._card = None
        if tag == "details":
            self._topic = None

    def handle_data(self, d):
        if self._in_cond and self._topic is not None:
            self._topic["conds"][-1] += d.strip()
        if self._in_name and self._card is not None:
            self._card["name"] += d.strip()
        if self._in_label is not None:
            self._in_label["name"] += d.strip()

    def view(self) -> dict:
        cur = [t for t in self.topics if t["current"]]
        return {"topics": self.topics, "current_topic": cur[0]["id"] if cur else None,
                "cards": [c["code"] for c in self.cards], "card_names": [c["name"] for c in self.cards],
                "dots": self.dots, "labels": self.labels, "site_filter": self.site_filter}


def screen_of(base: str, cid: str) -> tuple[dict, str]:
    st, _, html = http("GET", f"{base}/c/{cid}/items")
    p = Screen()
    p.feed(html)
    v = p.view()
    v["status"] = st
    return v, html


# ---------- 장부 → 턴 한 줄 ----------
KEEP_CONSULT = ("topics", "active_topic", "topic", "conditions", "fetch", "turn_kind", "follow_target", "ask", "ask_why",
                "empty", "after", "close", "viewing")


def slim(row: dict) -> dict:
    c = row.get("consult") or {}
    u = c.get("understand") or {}
    it = row.get("items") or {}
    return {
        "turn": row.get("turn"), "question": row.get("question"), "answer": row.get("answer"),
        "end_state": row.get("end_state"), "error": row.get("error"), "kinds": row.get("kinds"),
        "kinds_by": ((row.get("trace") or {}).get("front") or {}).get("kinds_by"),
        "consult": {k: c.get(k) for k in KEEP_CONSULT},
        "understand": {"parsed": u.get("parsed"), "accepted": u.get("accepted"), "dropped": u.get("dropped"),
                       "error": u.get("error"), "ms": u.get("ms")},
        "items": {"codes": it.get("codes"), "conditions": it.get("conditions"),
                  "turn_conditions": it.get("turn_conditions"), "blocked": it.get("blocked"),
                  "pick_zero": it.get("pick_zero"), "name_hits": it.get("name_hits")},
        "tokens": row.get("tokens"), "timing": row.get("timing"),
        "material_size": {k: (row.get("material_size") or {}).get(k) for k in ("msg_bytes", "est_tokens")},
        "llm": {k: (row.get("llm") or {}).get(k) for k in ("answered", "error", "result_subtype", "mode")},
    }


def ledger_rows(ledger_dir: Path) -> dict[tuple[str, int], dict]:
    out: dict[tuple[str, int], dict] = {}
    f = ledger_dir / "turns.jsonl"
    if not f.exists():
        return out
    for ln in f.read_text().splitlines():
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if r.get("phase") == "end" or "answer" in r:
            out[(r.get("conv_id"), r.get("turn"))] = r
    return out


# ---------- 한 대화 ----------
def run_conv(base: str, run: int, sc: dict, out: Path) -> dict:
    st, h, _ = http("GET", f"{base}/")
    loc = h.get("location") or h.get("Location") or ""
    cid = loc.rsplit("/", 1)[-1]
    res = {"run": run, "sid": sc["id"], "conv_id": cid, "turns": []}
    for i, t in enumerate(sc["turns"], 1):
        t0 = time.time()
        ps, _, body = http("POST", f"{base}/c/{cid}/turns", {"text": t["text"]}, timeout=120)
        ev = wait_turn(base, cid, i) if ps == 200 and "data-turn" in body else f"post_{ps}"
        scr, html = screen_of(base, cid)
        (out / "screens" / f"r{run}-{sc['id']}-T{i}.html").write_text(html)
        res["turns"].append({"n": i, "q": t["text"], "event": ev, "s": round(time.time() - t0, 1), "screen": scr})
        print(f"r{run} {sc['id']} T{i} {ev} {res['turns'][-1]['s']}s", flush=True)
    return res


def start_app(port: int, ledger_dir: Path, log: Path, app: Path = A) -> subprocess.Popen:
    env = {**os.environ, **ENV, "CHAT_DIR": str(ledger_dir)}
    p = subprocess.Popen(["uv", "run", "python", "-m", "clinic_chat.consult", "--port", str(port)], cwd=app, env=env,
                         stdout=log.open("w"), stderr=subprocess.STDOUT, start_new_session=True)
    base = f"http://127.0.0.1:{port}"
    for _ in range(120):
        time.sleep(1)
        if p.poll() is not None:
            raise SystemExit(f"앱이 바로 끝났다 — {log}")
        try:
            st, _, _ = http("GET", f"{base}/convs", timeout=5)
            if st == 200:
                return p
        except Exception:  # noqa: BLE001
            pass
    raise SystemExit("앱 기동 시간 초과")


def stop_app(p: subprocess.Popen) -> None:
    try:
        os.killpg(p.pid, signal.SIGTERM)
        p.wait(timeout=20)
    except Exception:  # noqa: BLE001
        os.killpg(p.pid, signal.SIGKILL)


def port_busy(port: int) -> bool:
    import socket
    s = socket.socket()
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--par", type=int, default=4)
    ap.add_argument("--only", default="")
    ap.add_argument("--ledger-dir", default="")
    ap.add_argument("--tag", default="base")
    ap.add_argument("--app", default=str(A))  # 앱 폴더(기본 = 앱 워크트리)
    ap.add_argument("--app-commit", default="")  # --app 이 git 폴더가 아니면(archive) 커밋을 적는다
    a = ap.parse_args()
    if a.port in FORBIDDEN_PORTS or port_busy(a.port):
        raise SystemExit(f"포트 {a.port} 는 쓸 수 없다(18222 · 18105 금지 · 빈 포트만)")
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    out = HERE / "out" / f"{a.tag}-{stamp}"
    (out / "screens").mkdir(parents=True, exist_ok=True)
    ledger_dir = Path(a.ledger_dir) if a.ledger_dir else Path(os.environ.get("TMPDIR", "/tmp")) / f"quality-ledger-{stamp}"
    ledger_dir.mkdir(parents=True, exist_ok=True)
    scs = json.loads((HERE / "scenarios.json").read_text())["scenarios"]
    if a.only:
        keep = set(a.only.split(","))
        scs = [s for s in scs if s["id"] in keep]
    app = Path(a.app)
    commit = a.app_commit or subprocess.run(["git", "-C", str(app), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    meta = {"started": dt.datetime.now().isoformat(timespec="seconds"), "port": a.port, "runs": a.runs, "par": a.par,
            "app_commit": commit, "app_dir": str(app), "env": ENV, "ledger_dir": str(ledger_dir), "scenarios": [s["id"] for s in scs]}
    meta["hub_start"] = hub_build()
    meta["tree"] = tree_hashes(app)  # 검수 r4 P1-1 — 측정한 프롬프트 · 작업 트리(sha256 앞 16)
    meta["gold_hash"] = meta["hub_start"].get("gold_hash")
    p = start_app(a.port, ledger_dir, out / "app.log", app)
    base = f"http://127.0.0.1:{a.port}"
    convs: list[dict] = []
    try:
        jobs = [(r, s) for r in range(1, a.runs + 1) for s in scs]
        with cf.ThreadPoolExecutor(max_workers=a.par) as ex:
            futs = {ex.submit(run_conv, base, r, s, out): (r, s["id"]) for r, s in jobs}
            for f in cf.as_completed(futs):
                try:
                    convs.append(f.result())
                except Exception as e:  # noqa: BLE001
                    print("대화 실패", futs[f], repr(e), flush=True)
    finally:
        time.sleep(2)
        stop_app(p)
    rows = ledger_rows(ledger_dir)
    with (out / "turns.jsonl").open("w") as fh:
        for c in sorted(convs, key=lambda x: (x["sid"], x["run"])):
            for t in c["turns"]:
                row = rows.get((c["conv_id"], t["n"]))
                rec = {"run": c["run"], "sid": c["sid"], "conv_id": c["conv_id"], "n": t["n"], "q": t["q"],
                       "event": t["event"], "wall_s": t["s"], "screen": t["screen"],
                       "ledger": slim(row) if row else None}
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    meta["ended"] = dt.datetime.now().isoformat(timespec="seconds")
    meta["hub_end"] = hub_build()
    led_hash = sorted({(r.get("build") or {}).get("gold_hash") for r in rows.values() if (r.get("build") or {}).get("gold_hash")})
    meta["ledger_gold_hashes"] = led_hash  # 앱이 턴마다 장부에 남긴 gold(허브 응답) — 셋이 같아야 한 gold 위 측정
    if meta["hub_end"].get("gold_hash") != meta["gold_hash"] or len(led_hash) > 1:
        print("경고: 측정 중 허브 gold 가 바뀌었다 — 이 결과로 전 → 후 비교 금지", flush=True)
    meta["convs"] = len(convs)
    meta["turns"] = sum(len(c["turns"]) for c in convs)
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    (out / "conv_ids.json").write_text(json.dumps({f"r{c['run']}-{c['sid']}": c["conv_id"] for c in convs}, indent=1))
    print("OUT", out)


if __name__ == "__main__":
    main()
