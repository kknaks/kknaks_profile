"""node-audit.md / node-audit.json 생성 — node-audit-coverage.py(§0) + node-audit.py(§1~§4) 를 돌려 묶고 §5 설계 초안을 붙인다.

읽기 전용 · 결정론(같은 입력이면 두 번 같음). 허브 18005 는 GET resolve 만.
실행: python3 node-audit-report.py  → 같은 폴더에 node-audit.json · node-audit.md
"""
from __future__ import annotations

import collections
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOLD = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json")
RAW = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26")
HUB = "http://127.0.0.1:18005/procedure-hub/gold/resolve"
K7 = ["concern", "site", "technique", "purpose", "check_condition", "package", "combo"]


def run(script: str) -> dict:
    out = subprocess.run([sys.executable, str(HERE / script)], capture_output=True, check=True, env={"PYTHONHASHSEED": "0", "PATH": "/usr/bin:/bin"})
    return json.loads(out.stdout.decode("utf-8"))


def resolve(text: str) -> list[str]:
    with urllib.request.urlopen(HUB + "?" + urllib.parse.urlencode({"text": text}), timeout=20) as r:
        d = json.loads(r.read().decode("utf-8"))
    return sorted({c["id"] for m in d.get("matches") or [] for c in m.get("candidates") or []} | {f"menu:{x}" if isinstance(x, str) else f"menu:{x.get('label') or x.get('name')}" for m in d.get("matches") or [] for x in m.get("menu_candidates") or []})


def pct(a: int, b: int) -> str:
    return f"{a / b * 100:.1f}%" if b else "–"


def cell(s) -> str:
    return str(s if s is not None else "").replace("|", "／").replace("\n", " ")[:90]


def main() -> None:
    cov = run("node-audit-coverage.py")
    na = run("node-audit.py")
    g = json.loads(GOLD.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in g["nodes"]}
    deg = collections.Counter()
    for e in g["edges"]:
        deg[e["from_id"]] += 1
        deg[e["to_id"]] += 1
    fc = collections.Counter()
    for f in g["facts"]:
        for i in {f["owner_id"], *(f.get("attached_to") or [])}:
            fc[i] += 1
    L: list[str] = []
    w = L.append
    T = cov["total"]
    J = T["judged"]

    # ── §0 커버리지 ──
    w("# 원장 → 골드 커버리지 · 빈 노드 · 고립 · 입구 점검(조사 · 설계만)\n")
    w(f"- 골드 `{cov['gold_build']}` · 원장 `{cov['raw_dir']}`(21 파일) · 실버 정본 11 파일 · fullrun-v2 `{na['batch']}`(문항 {na['rows']} · 같은 문항 두 번은 늦은 쪽)")
    w("- 재생성: `python3 node-audit-report.py`(→ `node-audit-coverage.py` · `node-audit.py` 를 돌림) · 두 번 돌려 바이트 같음 확인 · 데이터 수정 없음 · 허브는 GET resolve 만")
    w("- **결론 · 적용 없음 — 숫자 · 근거만.** 적용은 사용자 결정 뒤 별도 발주\n")
    w("## 0. 원장 → 골드 커버리지 전수(보충 · 1번)\n")
    w("판정(앞이 이김): **①** 골드 fact 원문에 있음 · **②** fact 는 아니고 골드 노드 · 엣지 · globals 속성(또는 fact 부가칸 meta)에만 · **③** 실버 정본 11 파일에는 있는데 골드에 안 나감 · **④** 실버에도 없음.  ")
    w("정규화 = triage 식(소문자 · 공백 · 기호 제거). 8자 이상 = 원장 값이 골드 문자열 안에 포함 → 조각 합(골드 문자열들이 원장 값의 80% 이상 덮음) → 3-gram ≥ 0.8. 8자 미만(짧은 값) = 같음 또는 「길이 ≤ 2×+4 인 골드 문자열 안 포함」(triage 짧은 인용 규칙). 경로 = 배열 인덱스 → [] · 코드 키 → {code} · products 분류 키 → {category} — source-map 517 칸과 전부 일치.  ")
    w("**한계**: 값 기준(문맥 없음) — 같은 문장이 **다른 노드**에 fact 로 붙어 있어도 ①. 「이 노드에 붙었나」는 §1 · §4 에서 따로 봄. 짧은 값(숫자 · 코드 · 한 낱말)은 우연 일치가 있어 따로 셈.\n")
    w("### 0-1. 전체\n")
    w("| 묶음 | 잎 | 판정 대상 | ① fact | ② 속성만 | ③ 실버만 | ④ 실버에도 없음 | 구조값(불리언 · null) | 빈 값 |")
    w("|---|---|---|---|---|---|---|---|---|")
    w(f"| 전체 | {T['leaves']} | {J} | {T['①']} ({pct(T['①'], J)}) | {T['②']} ({pct(T['②'], J)}) | {T['③']} ({pct(T['③'], J)}) | {T['④']} ({pct(T['④'], J)}) | {T['구조값']} | {T['빈 값']} |")
    for cl in ("내용", "메타 · 보관"):
        jj = T[f"{cl}:judged"]
        w(f"| {cl} 칸 | {T[f'{cl}:leaves']} | {jj} | {T[f'{cl}:①']} ({pct(T[f'{cl}:①'], jj)}) | {T[f'{cl}:②']} ({pct(T[f'{cl}:②'], jj)}) | {T[f'{cl}:③']} ({pct(T[f'{cl}:③'], jj)}) | {T[f'{cl}:④']} ({pct(T[f'{cl}:④'], jj)}) | {T[f'{cl}:구조값']} | {T[f'{cl}:빈 값']} |")
    lj = sum(T[f"long{k}"] for k in "①②③④")
    sj = sum(T[f"short{k}"] for k in "①②③④")
    w(f"| 긴 값(≥8자) | – | {lj} | {T['long①']} ({pct(T['long①'], lj)}) | {T['long②']} ({pct(T['long②'], lj)}) | {T['long③']} ({pct(T['long③'], lj)}) | {T['long④']} ({pct(T['long④'], lj)}) | – | – |")
    w(f"| 짧은 값(<8자) | – | {sj} | {T['short①']} ({pct(T['short①'], sj)}) | {T['short②']} ({pct(T['short②'], sj)}) | {T['short③']} ({pct(T['short③'], sj)}) | {T['short④']} ({pct(T['short④'], sj)}) | – | – |")
    w(f"\n「내용 칸」 = source-map 행선지에 속성 · 노드 · 엣지가 하나라도 있는 칸 · 「메타 · 보관」 = 행선지가 리니지 · 버림 · 원문 보관뿐. ② 중 fact 부가칸(meta)만 = {T['②m(fact 부가칸)']}(도구가 `with_meta` 일 때만 보임).\n")
    w("### 0-2. 파일별\n")
    w("| 파일 | 판정 대상 | ① | ② | ③ | ④ | ① 비율 |")
    w("|---|---|---|---|---|---|---|")
    for fn, v in sorted(cov["by_file"].items(), key=lambda x: (-x[1]["judged"], x[0])):
        w(f"| {fn} | {v['judged']} | {v['①']} | {v['②']} | {v['③']} | {v['④']} | {pct(v['①'], v['judged'])} |")
    rows = cov["rows"]
    w("\n### 0-3. 파일 × 필드 경로 — ①이 아닌 잎이 많은 순(② + ③ + ④ ≥ 1 · 전부는 json `coverage.rows`)\n")
    w("| 파일 | 경로 | 칸 | 대상 | ① | ② | ③ | ④ | ① 비율 | 예(① 아닌 것) | ②③ 가 있는 곳(첫째) |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    nonfact = sorted([r for r in rows if r["②"] + r["③"] + r["④"] > 0], key=lambda r: (-(r["②"] + r["③"] + r["④"]), r["file"], r["path"]))
    for r in nonfact[:80]:
        ex = r["examples"].get("④") or r["examples"].get("③") or r["examples"].get("②")
        wh = next((x for x in r["where_top"] if not x.startswith("①")), "")
        w(f"| {r['file']} | `{r['path']}` | {r['class']} | {r['judged']} | {r['①']} | {r['②']} | {r['③']} | {r['④']} | {pct(r['①'], r['judged'])} | {cell(ex)} | {cell(wh)} |")
    w(f"\n(① 아닌 잎이 있는 경로 {len(nonfact)} / 전체 경로 {len(rows)} — 80 줄까지만 표시)\n")

    # ④
    w("### 0-4. ④ 실버에도 없음 — 큰 필드부터 · 왜 빠졌나\n")
    NOTE = {
        ("extracted.json", "{code}.extracted_at"): "source-map B01: extracted 원천 메타 = 「브론즈 리니지 · 미정」 — 실버 어느 단계도 안 받음(결정 없음)",
        ("extracted.json", "{code}.source"): "같음(「일반 의학 지식」 같은 출처 문자열) — 8단계 evidence_source 는 literature/guides/web 만 받음 · 결정 없음",
        ("extracted.json", "{code}.source_type"): "같음 · 결정 없음",
        ("extracted.json", "{code}.updated"): "같음 · 결정 없음",
        ("extracted.json", "{code}.procedure_id"): "2단계 「리니지 · 끝(계열 동의어 대조 · 정본 step2)」 — 코드 값이라 대조에만 쓰고 안 실음(결정대로)",
        ("extracted.json", "{code}.name_en"): "2단계 리니지 · 끝 — 계열 영문명은 step2 정본 이름을 씀(원천 표기 6 은 안 옮김 · 결정대로)",
        ("extracted.json", "{code}.name"): "2단계 리니지 · 끝(같음)",
        ("taxonomy.json", "modality[].subcategories[].label"): "2 · 3단계 「속성 · 끝」 판정 근거로만 씀 — 「용도별」 같은 묶음 라벨 11 은 노드 · 속성 어디에도 안 옮김(결정은 「판정」까지 · 실음 여부 결정 없음)",
        ("problem-packages.json", "problems[].complaints[].combos[].reason"): "8단계 「엣지 속성 · 미정」(시너지 주장 evidence) — 146 중 137 은 붙고 짧은 이유 9(「단독 시술」 등)만 빠짐 · 결정 없음",
        ("products.json", "{category}.products[].manufacturer"): "1단계 「원문 보관 · 끝」 — 업체 표기는 허가 기준 6_companies 로 바꿈(원천 표기 7 은 원문 보관 · 결정대로)",
        ("taxonomy.json", "modality[].products[].manufacturer"): "1단계 6_companies(허가 기준) — 원천 표기 4 는 버림(결정대로)",
        ("taxonomy.json", "modality[].subcategories[].items[].ingredient_basis"): "**5단계 「단위 시술 ingredient 속성 · 결정됨」인데 step5-units.json 에 글이 없음** — step5-units.md:438~440 은 이 칸을 동의어 판정 근거로만 인용(마케팅명 = 동의어). 결정과 실물이 다름",
        ("taxonomy.json", "modality[].subcategories[].items[].naming_caveat"): "**5단계 「name_status · 주의 문구 원문 — S14」 결정(step5-units.md:1436)인데 주의 문구 원문이 실버에 없음** — 결정과 실물이 다름",
        ("taxonomy.json", "modality[].subcategories[].items[].canonical_category"): "2단계 리니지 · 끝(계열 판정 근거) — 결정대로",
        ("pih-risk.json", "procedures[].fitzpatrick_note"): "5단계 「표시」(step5-units.md:1391 S10 — 26행 3층에 붙임) — 22 는 붙고 4 빠짐 · 빠진 4 에 대한 결정 없음",
        ("products.json", "{category}.products[].name_en"): "1단계 원문 보관 · 끝(search_names 로 대체) — 3 은 표기 차이로 안 붙음",
        ("taxonomy.json", "modality[].products[].name_en"): "1단계 search_names — 3 은 표기 차이",
        ("products.json", "{category}.products[].regulatory_status"): "5단계 「allowed_routes [도포] 가드」(step5-units.md:1401) 로 바꿈 — 원문 문장은 안 실음 · 원문 보관 결정 없음",
        ("taxonomy.json", "modality[].products[].extracted.safety.common_side_effects"): "5단계 키 정규화(safety.common · step5-units.md:1437) — 2 는 값 표기 차이로 안 붙음 · 결정 없음",
        ("taxonomy.json", "modality[].subcategories[].items[].classification_issue"): "2단계 리니지 · 끝(조사 정정 근거) — 결정대로",
        ("taxonomy.json", "modality[].subcategories[].items[].correction_note"): "2단계 리니지 · 끝 — 결정대로",
        ("taxonomy.json", "modality[].subcategories[].items[].verification_needed"): "1단계 4_license 가 대체 — 결정대로",
    }
    w("| 파일 | 경로 | ④ / 대상 | 예 | source-map 행선지(단계 · 종류 · 상태) | 왜 빠졌나(기록 인용) | 결정 있음? |")
    w("|---|---|---|---|---|---|---|")
    four = sorted([r for r in rows if r["④"]], key=lambda r: (-r["④"], r["file"], r["path"]))
    undecided = []
    for r in four:
        sm = r["source_map"]
        dest = " · ".join(f"{x['stage']}/{x['kind']}/{x['status']}" for x in sm["destinations"])
        note = NOTE.get((r["file"], r["path"]))
        if not note:
            if all(x["kind"] in ("리니지", "버림", "원문 보관") for x in sm["destinations"]):
                note = f"브론즈 메타 칸({sm['destinations'][0]['target'] if sm['destinations'] else ''}) — {sm['destinations'][0]['basis'] if sm['destinations'] else ''}"
            else:
                note = f"source-map: {sm['destinations'][0]['target'] if sm['destinations'] else ''}"
        decided = "있음(결정대로 안 실음)"
        if (r["file"], r["path"]) not in NOTE and sm["status"] != "미정" and any(x["kind"] not in ("리니지", "버림", "원문 보관") for x in sm["destinations"]):
            note += " — 행선지가 속성인데 실버에 글 없음"
            decided = "**결정 있음 · 실물 없음**"
        elif "결정과 실물이 다름" in note:
            decided = "**결정 있음 · 실물 없음**"
        elif sm["status"] == "미정" or "결정 없음" in note:
            decided = "**없음**"
        if decided != "있음(결정대로 안 실음)":
            undecided.append({"file": r["file"], "path": r["path"], "n": r["④"], "decided": decided, "note": note})
        w(f"| {r['file']} | `{r['path']}` | {r['④']} / {r['judged']} | {cell(r['examples'].get('④'))} | {dest} | {note} | {decided} |")
    w(f"\n**결정 없이(또는 결정과 다르게) 빠진 것** — {len(undecided)} 경로 · 잎 {sum(x['n'] for x in undecided)}:\n")
    for x in undecided:
        w(f"- {x['file']} `{x['path']}` {x['n']} — {x['decided']}")
    # ② ③
    w("\n### 0-5. ② · ③ — 어디에 있고 어느 도구 · 섹션으로 내보내면 되나(추천 · 내용 칸 상위)\n")
    SEC = [
        (r"salesPitch|upsellHook|clinicalRationale|riskBenefit|expectedResult", "combo 노드 — T7 combos · peek/expand section `market`(판매 문구) · `evidence`(근거) 로 fact 화"),
        (r"^market-pricing|price|\.(low|mid|high|spec)$", "시장가 — 단위 시술/제품 `market` fact(가격 · 규격) — T3 card · expand"),
        (r"citations|journal|doi|pmid|pmc|authors|added_at", "evidence_source 노드 속성 — 출처 표기는 지금처럼 속성(인용 목록) · fact 화 불필요(추천)"),
        (r"\.id$|_id$|problem_id|category_id", "식별자 — 내보낼 필요 없음"),
        (r"vessels|nerves|course|depth|tissue|danger", "site_caution 엣지 속성 → 부위 노드 `site_caution` fact(위치 · 혈관 · 깊이) — T10 peek · T11 expand(부위 시작 걸음)"),
        (r"risk_factors|fitzpatrick|pih", "`safety.pih` fact(위험 요인 문장) — 지금 meta 에만"),
        (r"checks\[\]\.type|grade", "확인 조건 등급 — requires_check 엣지 resolved · T5 checks 가 이미 냄(fact 불필요)"),
        (r"name_en|search_names|aliases|synonym|\.name$|\.label$", "이름 · 동의어 — resolve 사전(fact 불필요)"),
        (r"links\[\]\.(from|to|target|type)", "시너지 엣지 끝점 · 종류 — 엣지로 이미 표현(③ 는 6단계 notes 원문만)"),
    ]
    agg = collections.defaultdict(lambda: [0, 0, []])
    for r in rows:
        if r["class"] != "내용" or r["②"] + r["③"] == 0:
            continue
        sec = next((s for rx, s in SEC if re.search(rx, f"{r['file'].replace('.json', '')}:{r['path']}" if rx.startswith("^") else r["path"])), "그 밖 — 소유 노드의 가장 가까운 section(overview · method · aftercare) fact 로")
        a = agg[sec]
        a[0] += r["②"]
        a[1] += r["③"]
        a[2].append(f"{r['file'].replace('.json', '')}.{r['path']}({r['②'] + r['③']})")
    w("| 내보낼 자리(추천) | ② | ③ | 경로(많은 순 앞 5) |")
    w("|---|---|---|---|")
    for sec, (a2, a3, ps) in sorted(agg.items(), key=lambda x: (-(x[1][0] + x[1][1]), x[0])):
        ps = sorted(ps, key=lambda p: (-int(re.search(r"\((\d+)\)$", p).group(1)), p))
        w(f"| {sec} | {a2} | {a3} | {cell(' · '.join(ps[:5]))[:300]} |")

    # ── §1 빈 노드 ──
    AN = na["nodes"]
    w("\n## 1. 빈 노드(사실 0) — 원천 재료 전수\n")
    w("셈: 사실 0 = gold-export fact 의 owner_id ∪ attached_to 에 한 번도 없음(코디 셈과 같음). 재료 = 원장 레코드 중 **이름 칸**(name · label · problem · concern · cc · category · zone · condition 등)이 노드 이름 · 실버 동의어 · 사전 표현(조건 붙은 CC 행 제외)과 같은 「자기 레코드」의 잎(id 류 뺌). 재료 종류는 잎 키로 나눔. 「정의 · 설명」 = 자기 레코드 **바로 아래**(taxonomy 는 extracted. 아래 포함)의 description · overview · definition · explanation · simple_ · analogy · summary · subtitle 칸 — 하위 항목(시술 · 제품) 설명은 「하위 항목」으로 따로. 괄호 별칭 = 원장 문자열 「X(Y)」 에서 X 나 Y 가 노드 말일 때 반대쪽(잡음 있음 → 사람 확인). 언급 = 다른 레코드 문장 안에 노드 말이 나옴(3자 이상 · 2자는 짧은 칸만).\n")
    w("| 종류 | 노드 | 사실 0 | 재료 있음(자기 레코드) | 재료 없음 | 정의 · 설명 있음 | 괄호 별칭 후보 있음 | 언급만 있음 |")
    w("|---|---|---|---|---|---|---|---|")
    tot_e = tot_m = tot_d = 0
    for k in K7:
        ns = [n for n in AN.values() if n["kind"] == k]
        e = [n for n in ns if n["empty"]]
        m = sum(n["has_material"] for n in e)
        dd = sum(n["has_definition"] for n in e)
        tot_e += len(e)
        tot_m += m
        tot_d += dd
        w(f"| {k} | {len(ns)} | {len(e)} | {m} | {len(e) - m} | {dd} | {sum(bool(n['alias_candidates']) for n in e)} | {sum(1 for n in e if not n['has_material'] and n['mentions_count'])} |")
    w(f"| 합 | – | {tot_e} | **{tot_m}** | {tot_e - tot_m} | {tot_d} | – | – |")
    mk = collections.Counter()
    mk_nodes = collections.Counter()
    for n in AN.values():
        if n["empty"]:
            for kk, v in n["materials_count"].items():
                mk[kk] += v
                mk_nodes[kk] += 1
    w("\n재료 종류별 셈(빈 노드 전체 · 잎 수 / 그 재료가 있는 노드 수): " + " · ".join(f"{kk} {mk[kk]}/{mk_nodes[kk]}" for kk in sorted(mk, key=lambda x: (-mk_nodes[x], x))))
    notfact = sum(n["materials_not_fact"] for n in AN.values() if n["empty"])
    w(f"\n빈 노드 재료 중 골드에 fact 로도 없는 것(②③④) = {notfact} 잎 — 나머지는 골드에 fact 로 있지만 **다른 노드(시술 · 제품 · 조합)** 에 붙어 있음(이 노드에서 걸으면 안 보임).\n")
    w("### 1-1. 노드별(빈 노드 전부)\n")
    w("| 노드 | 이름 | 엣지 | 자기 레코드(수 · 첫째) | 재료 종류별 수 | 정의 | 괄호 별칭 후보(앞 3) | 언급 수 |")
    w("|---|---|---|---|---|---|---|---|")
    for nid in na["empty_ids"]:
        n = AN[nid]
        al = " · ".join(sorted({a["alias"] for a in n["alias_candidates"]})[:3])
        w(f"| `{nid}` | {cell(n['name'])} | {n['edges']} | {n['self_records_n']} · {cell(n['self_records'][0] if n['self_records'] else '')} | {cell(json.dumps(n['materials_count'], ensure_ascii=False))[:120]} | {'○' if n['has_definition'] else '✗'} | {cell(al)} | {sum(n['mentions_count'].values())} |")
    w("\n### 1-2. 원장에 정의 · 설명 자체가 없는 노드(7 종류 전체 — 사실 있는 노드 포함)\n")
    w("「정의 없음」 = 자기 레코드가 없거나, 있어도 바로 아래에 정의 · 설명 칸이 없음. 예 `팔자주름`(concern:auto-83 · 사실 3) — 자기 레코드 4(anatomy-danger-zones nasolabial · market-pricing 「팔자주름 (HA 1cc)」 · problem-packages cc · taxonomy 항목) = 위치 7 · 위험 8 · 가격 3 · 영문 1 · 별칭 후보(코입술주름 등)만 있고 정의 문장 없음.\n")
    w("| 종류 | 노드 | 정의 없음 | 그중 재료(위치 · 위험 · 가격 · 시술)는 있음 | 정의 없음 이름(앞 30) |")
    w("|---|---|---|---|---|")
    nodef_total = 0
    nodef_list = {}
    for k in K7:
        ns = sorted([n for n in AN.values() if n["kind"] == k], key=lambda n: n["id"])
        nd = [n for n in ns if not n["has_definition"]]
        nodef_total += len(nd)
        nodef_list[k] = [n["id"] for n in nd]
        w(f"| {k} | {len(ns)} | {len(nd)} | {sum(n['has_material'] for n in nd)} | {cell(' · '.join(n['name'] for n in nd[:30]))[:400]} |")
    w(f"| 합 | {sum(1 for n in AN.values() if n['kind'] in K7)} | **{nodef_total}** | – | – |")
    w("\n정의 있는 노드: " + " · ".join(f"{n['name']}({n['kind']})" for n in sorted(AN.values(), key=lambda n: n["id"]) if n["kind"] in K7 and n["has_definition"]))
    w("\n→ concern · site · technique · purpose 는 원장에 「X 란 무엇」 문장이 거의 없다(정의 있음 concern 2 · site 3 · technique 1 · purpose 0). 「팔자주름이 뭔가요」 는 **원장 재료로는 정의 문장을 만들 수 없음** — 위치(해부 · 혈관) · 위험 등급 · 대표 시술 · 가격으로 「설명」은 조립 가능, 정의 문장 자체는 원천 보강(의료진 · 새 원천) 몫.\n")

    # ── §2 고립 ──
    w("## 2. 고립 노드(엣지 0) — 왜 · 이을 후보\n")
    iso = na["isolated"]
    w("| 종류 | 고립 | 사실 있음 |")
    w("|---|---|---|")
    for k, c in sorted(collections.Counter(i["kind"] for i in iso).items()):
        w(f"| {k} | {c} | {sum(1 for i in iso if i['kind'] == k and i['facts'])} |")
    # 연간 플랜 구성 후보 — 원장 schedule 을 resolve
    to = json.loads((RAW / "treatment-optimization.json").read_text(encoding="utf-8"))
    plan_cands = {}
    for p in to.get("annual_plans") or []:
        texts = sorted({re.sub(r"\s*\d+\s*(회|차)\s*$", "", x).strip() for s in p.get("schedule") or [] for x in s.get("procedures") or []})
        res = {t: resolve(t) for t in texts}
        plan_cands[p["age_group"]] = {"texts": texts, "resolved": {t: v for t, v in res.items() if v}, "unresolved": [t for t, v in res.items() if not v],
                                      "focus": p.get("focus"), "focus_resolved": resolve(p.get("focus") or "")}
    cand_rows = []
    for i in iso:
        if i["kind"] == "evidence_source":
            continue
        nid = i["id"]
        if nid.startswith("combo:RC-AN-"):
            pc = plan_cands.get(nid.split("RC-AN-")[1], {})
            why = "실버 앵커 = 연령대(age_group) — 고민 · 목적 노드 아님 · components 칸 없음(7단계가 연간 플랜 schedule 을 구성으로 안 풂)"
            cand = f"combo_component 후보 {len(pc.get('resolved', {}))}/{len(pc.get('texts', []))} 말(원장 annual_plans.schedule[].procedures — 허브 resolve 로 닿음: {cell(', '.join(sorted(pc.get('resolved', {}))))}) · 안 닿음 {cell(', '.join(pc.get('unresolved', [])))} · anchors_combo 후보 = focus 「{pc.get('focus')}」 resolve → {cell(', '.join(pc.get('focus_resolved', [])))}"
        elif nid == "combo:RC-PC-P1-1":
            why = "앵커 = P1 쁘띠시술(고민 노드 아님 · J5 메뉴 이름 속성만) · 구성 「보톡스 단독」 = 고민(대분류)에 부위 없음 · 이름 · 제품으로 못 좁힘(R23) → units 0 · 계열 엣지도 안 만듦"
            cand = "① 메뉴 「쁘띠시술」 → 이 조합(menu_labels 에는 이미 RC-PC-P1-1 이 있음 — 그래프 엣지만 없음) ② combo_component → family:M1(계열만 · 원장 problem-combos.combos[0].packages[0].procedures) — 근거 = 같은 P1 의 P1-2 · P1-3 는 엣지 있음"
        elif nid.startswith("product:"):
            why = f"1단계 허가 「확인 불가」 · recommendable false — 2단계 원장님 문의 3(알렉스필 · 더마큐어 · 벨르업 · _RESUME 10-28 「사용자가 따로 문의」)"
            cand = "product_family 후보 = 2단계 문의 답 뒤(지금 이으면 열린 것을 추측으로 메움) — 대기"
        elif nid.startswith("purpose:"):
            why = "7단계 「목적 · 고민 대응 없음」 — 메뉴(M16-1 미백/항산화 · M16-3 재생/면역 · P4-3 항산화수액)에서만 나온 목적 · 고민 앵커 없음"
            cand = "treats(목적 → 단위 시술) 후보 = 메뉴 M16 하위 단위 시술(원장 taxonomy modality M16 subcategories) — 이름 근거만 · 효과 근거 문장 없음 → 사람 확인"
        elif nid.startswith("package:"):
            why = "6단계 일반 패키지 · components 0 — 원장에 시장가 이름(market-pricing 「프리미엄 스킨케어 (풀코스)」)만 · 구성 시술 원문 없음"
            cand = "contains 후보 없음(원장에 구성 없음) — 원천 보강 몫"
        else:
            why, cand = i["silver_why"][:200], "–"
        cand_rows.append({"id": nid, "name": i["name"], "facts": i["facts"], "why": why, "candidates": cand})
    w("\n| 노드 | 이름 | 사실 | 왜 고립(실버 기록) | 원천으로 이을 후보(종류 · 근거) |")
    w("|---|---|---|---|---|")
    for c in cand_rows:
        w(f"| `{c['id']}` | {c['name']} | {c['facts']} | {c['why']} | {c['candidates']} |")
    evk = collections.Counter(json.loads(i["silver_why"]).get("kind") for i in iso if i["kind"] == "evidence_source")
    w(f"\nevidence_source 고립 39: 종류 {dict(sorted(evk.items()))} · 39 전부 `used_by`(8단계 주장 R8-…)가 있음 — 골드는 cites 엣지를 문헌 진술(evidence_statement → 문헌)에서만 만들고, 8단계 주장(엣지 속성 claim)이 가리키는 가이드 · 웹 · 내부 출처에는 엣지가 없음. 후보 = 주장이 붙은 엣지(procedure_relation · requires_check)의 evidence 에 출처 id 를 싣거나 `cites_claim` 엣지 — 39 전부 근거 있음(used_by). 「출처 아님(이유 문장)」 1 은 이을 대상 아님.\n")
    iso_link = sum(1 for c in cand_rows if not c["id"].startswith("product:") and not c["id"].startswith("package:")) + sum(1 for i in iso if i["kind"] == "evidence_source" and json.loads(i["silver_why"]).get("kind") != "출처 아님(이유 문장)")
    w(f"**원천으로 이을 수 있는 고립 = {iso_link}** / {len(iso)}(combo 4 · purpose 2(사람 확인) · evidence_source 38) · 못 이음 = product 3(문의 대기) · package 1(원천에 구성 없음) · evidence_source 1(출처 아님).\n")

    # ── §3 입구 ──
    w("## 3. 입구 — fullrun-v2 case3 되돌아감 15(no_start 12 · no_facts 3)\n")
    w("말마다: 조사를 뗀 꼴(은 · 는 · 이 · 가 · 을 · 를 · 와 · 과 · 랑 · 에 · 만 · 도 · 부터 · 만으로 …, 남는 말 2자 이상)로 허브 resolve(GET) 다시 · semantic 사전 정확 일치 · 원장 잎에 그 말이 든 경로 수.\n")
    cc_pat = {}
    for n in g["nodes"]:
        if n["kind"] == "check_condition":
            for t in str((n["attrs"].get("silver") or {}).get("match_pattern") or "").split("|"):
                if t:
                    cc_pat.setdefault(t, []).append(n["id"])
    menu_labels = sorted((g["build"]["counts"].get("menu_labels") or {}).keys())
    entry_cands = []
    w("| 문항 | 되돌아감 | 질문 | 그때 resolve 후보 | 조사 떼면 닿는 말 → 노드 | 사전에 없고 원천에 있는 말(→ 닿을 노드) | 원인 |")
    w("|---|---|---|---|---|---|---|")
    for r in na["fallback_rows"]:
        strip_hits, add = [], []
        for x in r["words"]:
            m = [i for i in (x["hub_resolve_stripped"] or {}).get("matches") or [] if not i.startswith("none:")]
            if m and x["stripped"] != x["word"]:
                strip_hits.append(f"{x['word']}→{x['stripped']}: {', '.join(m[:2])}")
            pat = [nid for t, ids in cc_pat.items() if t == x["stripped"] for nid in ids]
            if not m and pat:
                add.append(f"{x['stripped']} → {', '.join(pat)}(확인 조건 match_pattern · 사전엔 없음)")
            if x["stripped"] in ("쁘띠",):
                add.append("쁘띠 → menu 쁘띠시술(RC-PC-P1-1~3 · 원장 combo-recipes 「동안 쁘띠 패키지」 · problem-combos P1)")
            if x["stripped"] == "초음파":
                add.append("초음파 → family:M9(원장 「고강도 집속 초음파(HIFU)」 · 괄호 별칭) — 사전엔 없음")
        cands = r["resolve"]["candidates"] or []
        if r["fallback"] == "no_facts":
            cause = f"시작 노드 {r['start']} 사실 0(§1 빈 노드)"
        elif not cands and (strip_hits or add):
            cause = "resolve 0 → 조사 · 사전 보강으로 시작 가능"
        elif not cands:
            cause = "resolve 0 · 원천에 노드 말 없음(일반 질문)"
        elif any(c.startswith("none:") for c in cands):
            cause = "후보가 트리 항목(none) — 메뉴 후보는 있었으나 시작 선택지 아님"
        else:
            cause = "후보 있음 · Jev 「해당 없음」(두 시술 · 비교 의도 시작 문제 — 사전 아님)"
        e = {"q": r["q"], "fallback": r["fallback"], "question": r["question"], "candidates": cands, "strip_hits": strip_hits, "dict_add": add, "cause": cause, "items": r["items"]}
        entry_cands.append(e)
        w(f"| {r['q']} | {r['fallback']} | {cell(r['question'])} | {cell(', '.join(cands))} | {cell(' / '.join(strip_hits))[:200]} | {cell(' / '.join(sorted(set(add))))[:240]} | {cause} |")
    w(f"\n원인 셈: " + " · ".join(f"{k} {v}" for k, v in sorted(collections.Counter(e["cause"].split("(")[0].split(" →")[0] if not e["cause"].startswith("시작 노드") else "시작 노드 사실 0" for e in entry_cands).items())))
    w("\n참고: 「PN·PDRN 제품은 …」 질문 통째 resolve 는 0 인데 「PN」 · 「PDRN」 낱말 하나씩은 U5-018 에 닿음(접두 단계 · 낱말 하나일 때만) — 질의 쪽 낱말 나눔 · 조사 떼기 문제.\n")
    ut = na["unmatched_top"]
    STOP = re.compile(r"(요|까|나요|죠|데|고|면|서|도|게|지|는|은|을|를|가|이|한|된|될|할|던|며|니|다)\??$")
    w(f"### 3-1. 239 문항 resolve 「unmatched」 말 빈도(서로 다른 말 {na['unmatched_distinct']} · 합 {na['unmatched_total']})\n")
    w("상위 25(대부분 기능어):  " + " · ".join(f"{u['word']} {u['n']}" for u in ut[:25]))
    hits = [u for u in ut if any(not i.startswith("none:") for i in (u["hub_resolve_stripped"] or {}).get("matches") or [])]
    strip_only = [u for u in hits if u["stripped"] != u["word"]]
    w(f"\n**낱말 하나로 resolve 하면 닿는 말 {len(hits)}개(문항 등장 {sum(u['n'] for u in hits)})** — 그중 **조사를 떼야 닿는 말 {len(strip_only)}** · 나머지 {len(hits) - len(strip_only)} 은 조사 없이도 낱말 하나면 닿는데 질문 통째로는 안 닿은 말(질의 낱말 나눔 · 접두 단계 문제). 「주사 · 장비 → concern:P13」 · 「볼살 → PU-07」 같은 접두 일치는 맞는지 사람 확인:\n")
    w("| 말 | 등장 | 뗀 꼴 | 닿는 노드 | 문항 |")
    w("|---|---|---|---|---|")
    for u in sorted(hits, key=lambda u: (-u["n"], u["word"])):
        w(f"| {u['word']} | {u['n']} | {u['stripped']} | {cell(', '.join(i for i in u['hub_resolve_stripped']['matches'] if not i.startswith('none:'))[:3] and ', '.join([i for i in u['hub_resolve_stripped']['matches'] if not i.startswith('none:')][:3]))} | {', '.join(u['questions'][:4])} |")
    content = [u for u in ut if u not in hits and len(u["stripped"]) >= 2 and u["raw_leaves_containing"] >= 1 and not STOP.search(u["stripped"])
               and u["stripped"] not in ("시술", "피부", "효과", "같은", "여러", "일반", "다른", "바로", "항상", "완전히", "처음", "미용")]
    pat_hits = []
    for u in content:
        if u["stripped"] in cc_pat and u["stripped"] not in [x["stripped"] for x in pat_hits]:
            pat_hits.append(u)
    w(f"\n**조사 떼도 안 닿고 원장에는 있는 내용 말 {len(content)}개** — 그중 확인 조건 match_pattern 에만 있는 말 {len(pat_hits)}({', '.join(u['stripped'] for u in pat_hits)}) · 나머지 앞 40: " +
      " · ".join(f"{u['stripped']}({u['n']} · 원장 {u['raw_leaves_containing']})" for u in sorted(content, key=lambda u: (-u["n"], u["stripped"]))[:40]))
    dict_cands = len(strip_only) + len(pat_hits) + 2  # + 쁘띠 · 초음파
    w(f"\n**입구 사전 후보 = {dict_cands}**(조사 떼기로 닿는 말 {len(strip_only)} · 확인 조건 match_pattern → 사전 {len(pat_hits)} · 원장 근거 새 표현 2: 「쁘띠」 → 메뉴 쁘띠시술 · 「초음파」 → M9). 「손주사 · 기계주사」 는 원장 0 → 사전 후보 아님(사람 확인).\n")

    # ── §4 효과 추정 ──
    w("## 4. 효과 추정 — fullrun-v2 case3 실패 행 중 닫힐 가능성(행 단위)\n")
    fr = na["fail_rows"]
    items_c = collections.Counter(k for r in fr for k, v in r["items"].items() if v == "실패")
    w(f"case3 실패 행(5 항목 중 하나라도 실패) = {len(fr)} · 항목별 실패 {dict(sorted(items_c.items()))} · 답에 「정보 없음」류 문구 {sum(r['answer_unknown'] for r in fr)} 행 · 판사 실패 주장 중 「정보 없음이라 했다」 류 {sum(c['noinfo_claim'] for r in fr for c in r['fail_claims'])}.\n")
    qg = collections.Counter(c["quote_gold"] for r in fr for c in r["fail_claims"] if c["quote_gold"])
    w(f"판사 인용(원장 quote)의 커버리지 판정: {dict(sorted(qg.items()))} → **실패 인용의 대부분(①)은 골드 fact 에 이미 있음** — 「원장 → 골드 미적재」 보다 「걸음이 그 노드 · 섹션에 못 감」 이 큼(rerun-v8a 「못 받음」 과 같은 방향).\n")
    eff = {}
    entry_q = {e["q"]: e for e in entry_cands}
    for r in fr:
        why = []
        e = entry_q.get(r["q"])
        if e and e["fallback"] == "no_facts":
            why.append(f"A 빈 시작 노드({r['start']}) 채움 → 걷기 시작")
        if e and e["cause"].startswith("resolve 0 → "):
            why.append("B 입구(조사 · 사전) → 시작 노드 생김")
        if e and e["cause"].startswith("후보가 트리 항목"):
            why.append("B' 메뉴 후보를 시작으로(쁘띠시술 → 조합)")
        mat = sorted({n for c in r["fail_claims"] for n in c.get("quote_in_node_material") or []})
        if mat:
            why.append(f"C 실패 인용이 걸은 빈 노드의 원천 재료에 있음({', '.join(mat[:3])})")
        isol = sorted({n for c in r["fail_claims"] for n in c.get("quote_in_isolated_material") or []})
        if isol:
            why.append(f"D 고립 노드 연결({', '.join(isol)})")
        cv = sorted({c["quote_gold"] for c in r["fail_claims"] if c["quote_gold"] in ("②", "③", "④")})
        if cv:
            why.append(f"E 실패 인용이 골드 fact 아님({'/'.join(cv)}) → 커버리지 보강")
        if why:
            eff[r["q"]] = {"q": r["q"], "question": r["question"], "fails": [k for k, v in r["items"].items() if v == "실패"], "why": why,
                           "on_topic": r["items"].get("on_topic") == "실패", "unknown": r["answer_unknown"]}
    # 일반 질문(Q205 · Q206 · Q059 · Q042 등)은 노드로 못 닫음 — B 에서 빠짐
    w("| 문항 | 질문 | 실패 항목 | 닫힐 근거 |")
    w("|---|---|---|---|")
    for q in sorted(eff):
        x = eff[q]
        w(f"| {q} | {cell(x['question'])} | {', '.join(x['fails'])} | {' · '.join(x['why'])} |")
    n_on = sum(x["on_topic"] for x in eff.values())
    n_un = sum(x["unknown"] for x in eff.values())
    w(f"\n**닫힐 가능성 행 = {len(eff)}** / 실패 {len(fr)}(on_topic 실패 {n_on} / {items_c.get('on_topic', 0)} · 「정보 없음」류 답 {n_un} / {sum(r['answer_unknown'] for r in fr)}). 근거별: " +
      " · ".join(f"{k} {v}" for k, v in sorted(collections.Counter(w_[0] for x in eff.values() for w_ in x["why"]).items())) +
      ". 「가능성」 = 그 근거가 고쳐지면 걸음이 원천 근거에 닿을 수 있는 행(답 생성 · 채점 흔들림 15~20% 는 안 셈) — 상한에 가까운 추정.\n")
    rest_on = [r["q"] for r in fr if r["items"].get("on_topic") == "실패" and r["q"] not in eff]
    w(f"on_topic 실패 중 위 근거로 안 닫히는 행: {', '.join(rest_on)} — A~E 근거에 안 걸림(원인 미분류 · Q206 은 시작 노드 없는 일반 질문).\n")

    # ── §5 설계 초안 ──
    w("## 5. 설계 초안 — 실버 10단계(가칭 · 노드 설명 사실) · 사전 보강 · 고립 연결 (적용 금지)\n")
    w("### 5-1. 레코드 꼴(9단계 records 와 같은 꼴 · 새 owner 종류만)\n")
    w("```json\n{\"id\": \"S10:<원장 파일>.<구체 경로>\", \"owner\": \"concern:P6\", \"section\": \"overview|site_caution|market|evidence|method\",\n \"kind\": \"이름 · 별칭 | 영문 | 위치 | 위험 등급 | 대표 시술 | 가격 | 하위 항목 요약 | 정의(원천에 있을 때만)\",\n \"text\": \"<원문 그대로>\", \"origin\": {\"file\": \"anatomy-danger-zones\", \"path\": \"zones[5].danger_level\"},\n \"rule\": \"N10-1 자기 레코드\", \"class\": \"한 원천|여러 원천\", \"same_as\": [], \"status\": \"자동|사람 확인\"}\n```")
    w("### 5-2. 붙이는 규칙(추천)\n")
    w("- **N10-1 자기 레코드**: 이름 칸 = 노드 이름 · 실버 동의어 · 사전 표현(조건 없는 행)인 원장 레코드의 바로 아래 잎 → 그 노드 fact. 섹션 = 재료 종류(위치 · 위험 → site_caution · 가격 → market · 정의 · 설명 → overview · 대표 시술 → overview(목록 한 줄)). id 류 · 리니지 칸은 안 붙임")
    w("- **N10-2 하위 항목 요약**: 자기 레코드 아래 하위 항목(시술 · 제품 · 패키지)은 원문을 복사하지 않고 「하위 N개 — 이름 목록」 한 fact + 이미 있는 하위 노드 id 참조(DB 는 가리키기만 원칙)")
    w("- **N10-3 같은 글 합침**: 같은 원문이 여러 레코드 → 하나(class 여러 원천 · same_as) — 9단계 D9-3 ① 그대로")
    w("- **N10-4 정의 없음은 만들지 않음**: 정의 문장이 원장에 없으면 fact 를 만들지 않고 `state: 정보 없음(gap)` 한 줄(현 골드 gap 규칙) — 답은 「원장에 정의 없음 + 위치 · 시술은 이렇다」 로")
    w("- **N10-5 괄호 별칭**: 자동으로 안 붙임 — 후보 목록 → 사람 확인(잡음 큼: 「볼 (처짐)」 같은 꼴)")
    w("### 5-3. 사전 보강 규칙(추천)\n")
    w("- **D-a 질의 조사 떼기**: resolve 질의 쪽에서 낱말 끝 조사(5-3 목록) 떼고 다시 완전 일치 — 사전 행 추가 없음 · 10-30 「허브 resolve 조사 떼기(질의 쪽)」 결정의 실행")
    w("- **D-b 확인 조건 match_pattern → 사전**: check_condition 의 match_pattern 낱말(감염 · 염증 · 결핵 …)을 사전 표현으로(mode 후보)")
    w("- **D-c 메뉴 접두**: 「쁘띠」 → 메뉴 쁘띠시술(J5 메뉴 경로 · 원장 combo-recipes 「동안 쁘띠 패키지」)")
    w("- **D-d 괄호 별칭 중 원장 근거 있는 것**: 「초음파」 → M9(「고강도 집속 초음파 (HIFU)」) — 후보 목록은 사람 확인")
    w("### 5-4. 고립 연결 규칙(추천)\n")
    w("- **L-a 연간 플랜**: annual_plans.schedule[].procedures 를 7단계 R21~R24(이름 · 부위 · 제품으로 내림)로 combo_component · focus 낱말을 고민 앵커로(R12~R22)")
    w("- **L-b 메뉴 조합**: 앵커 없는 메뉴 조합은 계열 엣지(combo_component → family)라도 냄 — RC-PC-P1-1 → M1")
    w("- **L-c 8단계 출처**: 주장 used_by 가 있는 evidence_source 는 주장이 붙은 엣지 evidence 에 출처 id(또는 cites_claim 엣지)")
    w("- **L-d 목적 PU-09 · PU-11**: 메뉴 M16 하위 단위 시술로 treats — 효과 문장 없음 → 사람 확인")
    w("### 5-5. 「사람 확인」 자리\n")
    alias_n = sum(n["alias_candidates_n"] for n in AN.values() if n["empty"])
    w(f"- 괄호 별칭 후보 {alias_n}(빈 노드 · 잡음 큼) · 사전 밖 말 「손주사 · 기계주사」(원장 0) · 목적 PU-09 · PU-11 treats · 정의 없는 노드 {nodef_total} 중 정의 문장을 원천 보강할지(의료진 · 새 원천) · 결정과 실물이 다른 5단계 2칸(ingredient_basis 6 · naming_caveat 6)")
    w("### 5-6. decisions 초안(추천값)\n")
    decisions = [
        {"id": "D10-1", "q": "빈 노드에 원장 자기 레코드 잎을 fact 로 붙일까", "recommend": "붙임(N10-1 · 섹션은 재료 종류) — 하위 항목은 요약 한 줄(N10-2)", "why": f"빈 노드 {tot_e} 중 재료 있음 {tot_m}"},
        {"id": "D10-2", "q": "정의 문장이 원장에 없는 노드", "recommend": "만들지 않음 · gap 표시(N10-4) — 정의 원천 보강은 별도 결정", "why": f"7 종류 {nodef_total} 노드 정의 없음"},
        {"id": "D10-3", "q": "resolve 질의 조사 떼기", "recommend": "넣음(D-a · 질의 쪽만)", "why": f"조사를 떼야 닿는 말 {len(strip_only)} · 낱말 하나면 닿는 말 {len(hits)} · 되돌아감 Q066 · Q203"},
        {"id": "D10-4", "q": "확인 조건 match_pattern 을 사전으로", "recommend": "넣음(D-b · mode 후보)", "why": "Q204 「감염」 → C-INFECT"},
        {"id": "D10-5", "q": "「쁘띠」 메뉴 접두 · 「초음파」 → M9", "recommend": "넣음(D-c · D-d)", "why": "Q238 · Q082"},
        {"id": "D10-6", "q": "고립 조합 4 · evidence_source 38 연결", "recommend": "L-a · L-b · L-c 대로", "why": "Q238 정답 인용이 고립 RC-PC-P1-1 에 있음"},
        {"id": "D10-7", "q": "커버리지 ② 속성만(내용 칸) 을 fact 로", "recommend": "판매 문구 · 시장가 · site_caution 위치는 fact 화 · 식별자 · 출처 표기 · 동의어는 그대로", "why": "§0-5"},
        {"id": "D10-8", "q": "결정 없이 · 결정과 다르게 빠진 ④", "recommend": "5단계 ingredient_basis · naming_caveat 는 결정대로 실음(원문) · extracted 리니지 4칸은 브론즈 메타로 두고 안 실음 · 나머지는 원문 보관", "why": "§0-4"},
    ]
    w("| id | 질문 | 추천 | 근거 |")
    w("|---|---|---|---|")
    for d in decisions:
        w(f"| {d['id']} | {d['q']} | {d['recommend']} | {d['why']} |")
    w("### 5-7. 아직 안 정한 것\n")
    w("- 10단계를 실버 단계로 둘지 · 골드 빌드 규칙(gold-prep)으로 둘지(실버 정본에 owner 를 노드 id 로 쓰는 첫 단계)")
    w("- case3 걸음이 빈 노드의 새 fact 를 실제로 받는지 — 의도 묶음(I-02 overview+method 등)에 site_caution · market 이 없어 시작 노드에서 안 펼칠 수 있음(SPEC-006 몫)")
    w("- 효과 추정은 상한 — 실제는 재빌드 뒤 같은 50/239 재측정으로만 확인")

    summary = {
        "coverage": {k: T[k] for k in ("leaves", "judged", "①", "②", "③", "④")},
        "coverage_rate": {k: round(T[k] / J, 4) for k in ("①", "②", "③", "④")},
        "undecided_missing_paths": len(undecided), "undecided_missing_leaves": sum(x["n"] for x in undecided),
        "empty_nodes": tot_e, "empty_with_material": tot_m, "empty_with_definition": tot_d,
        "no_definition_nodes_all7": nodef_total, "isolated": len(iso), "isolated_linkable": iso_link,
        "entry_dict_candidates": dict_cands, "strip_josa_hits": len(strip_only), "single_word_hits": len(hits), "fail_rows": len(fr), "closable_rows": len(eff),
    }
    w("\n## 요약 숫자\n")
    w("```json\n" + json.dumps(summary, ensure_ascii=False, indent=1) + "\n```")
    (HERE / "node-audit.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    out = {"summary": summary, "coverage": cov, "audit": na, "isolated_candidates": cand_rows, "plan_candidates": plan_cands,
           "entry": entry_cands, "effect": [eff[q] for q in sorted(eff)], "no_definition": nodef_list, "undecided_missing": undecided,
           "decisions_draft": decisions}
    (HERE / "node-audit.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
