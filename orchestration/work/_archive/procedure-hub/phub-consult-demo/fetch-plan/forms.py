"""할 일 2 — 장부 실제 말 → 질문 꼴 전수(읽기만 · LLM 0). 꼴 = 이해 호출이 고른 대상 표 · kinds + 말 낱말 규칙.
한 말이 여러 꼴이면 위에서부터 첫 꼴 하나(차례 = FORMS). 실행: python3 forms.py → out/forms.json · out/forms.md
"""
import json, re, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGERS = [Path("/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/runs/consult/turns.jsonl"),
           Path("/private/tmp/claude-501/-Users-kknaks-orca-workspaces-clinic-chat-phub-consult-demo/a6af7bd8-5374-42fc-854f-496eb6878c39/scratchpad/fixEchat/turns.jsonl")]
TARGET = {"procedure", "modality", "procedure_case"}
FORMS = [  # (꼴, 판정)
    ("F01 바로잡기", lambda q, t, k, kind, first: bool(re.search(r"말고 .*(얘기|말)|그게 아니라|그거 말고|그대로 두라", q)) and not re.search(r"말고 다른", q)),
    ("F02 넓히기 · 뺌", lambda q, t, k, kind, first: bool(re.search(r"말고 다른|빼고|다른 시술|상관없이|전체로", q))),
    ("F03 그중에서 · 고르기", lambda q, t, k, kind, first: bool(re.search(r"그중|중에서|만 관심|로 할게|로 안내|받고 싶|맞고 싶|받아보고", q))),
    ("F04 명동점 밖 · 있나 물음", lambda q, t, k, kind, first: bool(re.search(r"명동점|여기(엔|에는|서)", q))),
    ("F05 가격 · 샷 · 회차", lambda q, t, k, kind, first: bool(re.search(r"가격|얼마|비용|샷|몇 ?번|몇 ?회|회차|용량", q)) or "offer" in k),
    ("F06 부작용 · 회복 · 금기", lambda q, t, k, kind, first: bool(re.search(r"부작용|아파|통증|붓기|회복|다운타임|위험|안 ?되는", q)) or bool(set(k) & {"adverse", "recovery", "contraindication", "avoid"})),
    ("F07 같이 받기 · 순서", lambda q, t, k, kind, first: bool(re.search(r"같이|함께|동시|순서|간격", q)) or bool(set(k) & {"combo", "same_day", "order_interval"})),
    ("F08 비교", lambda q, t, k, kind, first: bool(re.search(r"차이|비교|뭐가 (더|나아)|나아\?|어떤 게 좋", q))),
    ("F09 전반 설명", lambda q, t, k, kind, first: bool(re.search(r"전반|설명해|알려줘|안내해", q))),
    ("F10 원리", lambda q, t, k, kind, first: bool(re.search(r"원리|어떻게 (작용|되는)|방식", q)) or "mechanism" in k),
    ("F11 효과 확인", lambda q, t, k, kind, first: bool(re.search(r"효과|돼 ?\?|되나|오래|유지|언제부터", q)) or "outcome" in k),
    ("F12 정체 묻기(뭐야)", lambda q, t, k, kind, first: bool(re.search(r"뭐야|머야|뭔가요|뭐예요|무엇", q)) or "overview" in k),
    ("F13 종류 · 뭐가 있어", lambda q, t, k, kind, first: bool(re.search(r"뭐뭐|뭐가 있|어떤 시술|무슨 시술|종류|뭐 하면|추천", q)) or "lineup" in k or "indication" in k),
    ("F14 시술 · 제품 이름만", lambda q, t, k, kind, first: bool(t & (TARGET | {"product"}))),
    ("F15 효과 바람", lambda q, t, k, kind, first: "effect" in t),
    ("F16 고민(+부위)", lambda q, t, k, kind, first: "concern" in t),
    ("F17 부위만 · 첫 턴", lambda q, t, k, kind, first: t == {"site"} and first),
    ("F18 부위만 · 주제 있음", lambda q, t, k, kind, first: t == {"site"} and not first),
    ("F19 맞장구 · 불만(talk)", lambda q, t, k, kind, first: kind == "talk"),
    ("F20 이해 실패 · 대상 없음(장부)", lambda q, t, k, kind, first: not t),
]


def main():
    seen = set()
    out = defaultdict(list)
    for lp in LEDGERS:
        if not lp.exists():
            continue
        for x in lp.read_text().splitlines():
            r = json.loads(x)
            if r.get("phase") != "end" or (r.get("asked_at") or "")[:10] < "2026-11-18":
                continue
            u = ((r.get("consult") or {}).get("understand") or {}).get("accepted") or {}
            key = (r["conv_id"], r["turn"])
            if key in seen:
                continue
            seen.add(key)
            q = r.get("question") or ""
            t = {x.get("table") for x in u.get("targets") or []}
            k = list(u.get("kinds") or [])
            kind = u.get("kind") or ""
            first = r["turn"] == 1
            form = next((f for f, fn in FORMS if fn(q, t, k, kind, first)), "F99 그 밖")
            out[form].append({"conv": r["conv_id"][:4], "turn": r["turn"], "q": q, "tables": sorted(t), "kinds": k,
                              "kind": kind, "mat": bool(((r.get("material") or {}).get("new_lines")))})
    rows = sorted(out.items())
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out/forms.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    lines = ["| 꼴 | 턴 수 | 자료 있는 턴 | 예(장부 실제 말) |", "|---|---:|---:|---|"]
    for f, xs in rows:
        ex = " · ".join(f"「{x['q'][:24]}」" for x in xs[:3])
        lines.append(f"| {f} | {len(xs)} | {sum(1 for x in xs if x['mat'])} | {ex} |")
    lines.append(f"| 합 | {sum(len(v) for v in out.values())} | | |")
    (HERE / "out/forms.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


main()
