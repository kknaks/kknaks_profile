"""SPEC-011 실물 재생 — 빈 포트에 띄운 앱(18222 와 같은 env · 장부는 따로 CHAT_DIR)에 3 대화를 실제 이해 · 답 호출로 다시 돌린다.

차례: 서버는 바깥에서 띄운다(이 스크립트는 HTTP 만). 대화마다 `GET /` → `POST /c/<id>/turns` → SSE `done | turn_error` 까지 기다림.
실행: python live3.py <base_url> <tag>  → out/live_<tag>.json(대화 id 목록)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
CONVS = {
    "03b8": ["팔자주름에 대해서 고민이돼", "미간에 주름도 고민이야", "얼굴에 탄력이 좀 떨어지는거 같은데",
             "그중에서 소프웨이브, 써마지, 울쎄라만 관심이 잇어", "고주파 원리가 머야 ?", "응 고주파에 대해서 전반적으로 설명해줘"],
    "ecc6": ["요즘 피부 탄력이 저하 되서 고민이야", "얼굴에", "얼굴에"],
    "73bd": ["얼굴에 피부 탄력이 없어져서 걱정이야", "아 주름이 눈가 입꼬리에 잇어", "아 눈가는 볼뉴머 이ㅃ고리는 필러를 맞고 싶어",
             "입꼬리에는 필러를 맞고 싶다니까"],
}


def wait_turn(c: httpx.Client, cid: str, n: int, timeout: float = 400) -> str:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with c.stream("GET", f"/c/{cid}/turns/{n}/events", timeout=timeout) as r:
                if r.status_code == 204:
                    return "gone"
                ev = None
                for ln in r.iter_lines():
                    if ln.startswith("event:"):
                        ev = ln.split(":", 1)[1].strip()
                        if ev in ("done", "turn_error"):
                            return ev
        except httpx.HTTPError:
            time.sleep(2)
    return "timeout"


def main():
    base, tag = sys.argv[1], sys.argv[2]
    only = sys.argv[3].split(",") if len(sys.argv) > 3 else list(CONVS)
    out = {}
    with httpx.Client(base_url=base, follow_redirects=False, timeout=60) as c:
        for name in only:
            r = c.get("/")
            cid = r.headers["location"].rsplit("/", 1)[1]
            res = []
            for i, q in enumerate(CONVS[name], 1):
                t = time.time()
                p = c.post(f"/c/{cid}/turns", data={"text": q})
                ev = wait_turn(c, cid, i) if p.status_code == 200 else f"post_{p.status_code}"
                res.append({"turn": i, "q": q, "event": ev, "s": round(time.time() - t, 1)})
                print(name, cid[:8], i, ev, res[-1]["s"], flush=True)
            out[name] = {"conv_id": cid, "turns": res}
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / f"out/live_{tag}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
