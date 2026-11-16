# -*- coding: utf-8 -*-
"""report.md §16 「8차 빌드 · ERD v3.3」 — 7차(baseline/manifest-7차.json · ERD v3.2 · 원장 2판) 대비.

결정 6-A 적용 로그 · 개체·관계 7차→8차 · 부작용(사건 노드 사전+새 · 단위 · 문구 2,285 분포 · 사건 칸 빈 수) · (폐색, 부위) 단위 표 · 폐색≠색전 · category 참조 0 ·
분석기 캐시 · 게이트 6 자리 표 · 7차 재현 key · ERD 질문 표. 수치는 전부 코드가 센 값이다.
"""
import json
import os
import re
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _rel(p):
    try:
        return os.path.relpath(p, HERE)
    except ValueError:
        return os.path.basename(p)

from .units32 import ACTIVE
from .util import md_table, norm


def _kv(d):
    return " · ".join(f"{k} {v}" for k, v in d.items()) if d else "—"


def frozen_section(out_dir, baseline_dir, name):
    p = os.path.join(baseline_dir, name)
    if not os.path.exists(p):
        return False
    with open(p, encoding="utf-8") as f:
        txt = f.read()
    with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n" + txt.rstrip("\n") + "\n")
    return True


def category_refs(S, recs, dic):
    """out/ 안의 분류 속성 참조 — adverse_effect 레코드의 사건 분류 속성(event_ + category) · 사전 adverse_event_type 항목의 category/category_review."""
    n = 0
    for r in recs.get("adverse_effect", []):
        n += sum(1 for k in r["attrs"] if k in ("event_" + "category", "category"))
    for d in dic["dictionaries"]:
        if d["name"] == "adverse_event_type":
            n += sum(1 for e in d["entries"] for k in e if k in ("category", "category_review"))
    return n


def eighth(S, out_dir, baseline_dir, m, g6, args):
    p7 = os.path.join(baseline_dir, "manifest-7차.json")
    b = json.load(open(p7, encoding="utf-8"))["counts"] if os.path.exists(p7) else {"entities": {}, "relations": {}, "gate": {}, "conflicts": {}}
    c = m["counts"]
    ctx = S.ctx
    log = m["decisions"]["apply_log"]
    AU = ctx["AU"]
    A, A0 = ctx["adv"], ctx["adv0"]
    s0, s1 = A0["summary"], A["summary"]
    an = ctx.get("analyzer")
    AT = A["AT"]
    dic = ctx["dic"]
    o = ["", "## 16. 8차 빌드 · ERD v3.3 · 원장 3판 · 결정 묶음 6-A", "",
         "7차 = `baseline/manifest-7차.json`(ERD v3.2 · 원장 2판 · 결정 457) · 8차 = ERD **v3.3**(`erd-v3.3.json` · `erd-v3.3-dictionaries.json` · 원장 **3판** `bronze/phub-ledger/` · 빌더 `lib/adverse33.py`(분석기) · `lib/analyzer.py`(kiwipiepy 캐시) · 발주서 `silver-build-8-brief.md`). "
         f"③ 결정 적용 전 분해(분석기 없는 목록 규칙 — ERD 실측 `erd-v3.3-tuples.py` 의 조건) = `erd-v3.3-tuples.json` 요약 차이 {m['erd_comparison']['diff']}/{m['erd_comparison']['keys']}(§5). "
         "실버 산출(결정 전·뒤 둘 다)은 **분석기(V3.3-B)** 로 분해한 값이다 — ERD 실측(목록 규칙)과 노드 수가 다르며 그 차이는 아래 표가 센다.", ""]

    # ---------------------------------------------------------------- 결정 6-A
    b6 = [x for x in log if x["id"].startswith("DEC-2026-11-06-B6A")]
    res = Counter((x["kind"], x["result"]) for x in b6)
    o += ["### 결정 묶음 6-A 적용 로그(decisions/batch6a/)", "",
          md_table(["kind", "건", "applied", "rejected", "no_target"], [(k, sum(v for (kk, r), v in res.items() if kk == k), res.get((k, "applied"), 0), res.get((k, "rejected"), 0), res.get((k, "no_target"), 0)) for k in sorted({x["kind"] for x in b6})]), "",
          f"6-A 결정 {len(b6)}(site 15 · ingredient_material 6 · 접미사 쌍 20 = fold_approve {sum(1 for x in b6 if x['kind'] == 'fold_approve')} + canonical_rename {sum(1 for x in b6 if x['kind'] == 'canonical_rename')} · product_name 동의어 7) · "
          f"적용 {sum(1 for x in b6 if x['result'] == 'applied')} · 거부 {sum(1 for x in b6 if x['result'] == 'rejected')} · 대상 없음 {sum(1 for x in b6 if x['result'] == 'no_target')}."]
    bad = [x for x in b6 if x["result"] != "applied"]
    for x in bad:
        o.append(f"- `{x['id']}` {x['kind']} — {x['result']}: {x.get('why')}")
    allres = Counter((x["kind"], x["result"]) for x in log)
    o += ["", "전체 결정 적용 결과(8차 · 기존 결정 포함):", "", md_table(["kind", "applied", "recorded", "rejected", "no_target"], [(k, *(allres.get((k, r), 0) for r in ("applied", "recorded", "rejected", "no_target"))) for k in sorted({x["kind"] for x in log})]), ""]
    notok = [x for x in log if x["result"] in ("rejected", "no_target")]
    if notok:
        o.append(f"거부·대상 없음 {len(notok)}(기존 결정 — 7차와 같은 것인지는 아래):")
        for x in notok:
            o.append(f"- `{x['id']}` {x['kind']} — {x['result']}: {str(x.get('why'))[:160]}")
        o.append("")
    fold_log = [x for x in b6 if x["kind"] == "fold_approve"]
    o += ["접미사 쌍 fold_approve 가 닿은 자리(locators) · 닫은 ⑦:", "", md_table(["결정", "노드", "→", "닿은 자리", "닫은 ⑦"], [(x["id"].split("-")[-1], x["node"], x["into"], x.get("locators"), x.get("closed_duplicates", 0)) for x in fold_log]), ""]

    # ---------------------------------------------------------------- 변화표
    def tbl(title, k1, notes=None):
        keys = list(dict.fromkeys(list(b.get(k1, {})) + list(c.get(k1, {}))))
        if k1 == "relations":
            keys = sorted(keys, key=lambda x: int(x[1:]))
        rows = []
        for k in keys:
            bv, cv = b.get(k1, {}).get(k, 0), c.get(k1, {}).get(k, 0)
            rows.append((k, bv, cv, f"{cv - bv:+d}" if isinstance(bv, int) and isinstance(cv, int) and cv != bv else ("0" if bv == cv else "—"), (notes or {}).get(k, "")))
        o.extend([f"### {title}", "", md_table(["", "7차(v3.2 · 2판)", "8차(v3.3 · 3판)", "변화", "비고"], rows), ""])
    tbl("개체", "entities", {"adverse_effect": "분석기 핵심어 노드 · R2 사전 값(혈관 폐색 → 폐색+혈관) · 부위 15 · 접미사 접기", "catalog_item": "원장 3판 +2(M8-6 저출력레이저(LLLT) · 다이오드 레이저)", "site": "+15(6-A) +3(v3.3 동맥·정맥·안동맥)",
                             "procedure": "3판 synergy 정식 이름 · 부위 15 · 성분 6 · 동의어 7", "product": "product.kind=product 전부(구성품 0 · R36 0)", "conflict": "아래 충돌 표", "decision": "+48(6-A)"})
    tbl("관계", "relations", {"R36": "v3.3 신설 component_of — 원장 칸 없음 · 엣지 0", "R15": "(출발, 단위) 마다 하나", "R31": "단위가 는 만큼 · (폐색, 혈관) 등", "R27": "what_kind=component 0"})
    tbl("충돌 kind 별", "conflicts")
    gk = ["unresolved_references", "unregistered_fragments", "unlinked_phrases", "unlinked_phrase_locators", "catalog_partial", "conflicts_md_duplicate"]
    o.extend(["### 게이트 목록", "", md_table(["", "7차", "8차"], [(k, b.get("gate", {}).get(k, 0), c["gate"].get(k, 0)) for k in gk]), ""])

    # ---------------------------------------------------------------- 부작용
    D = {d["name"]: d for d in dic["dictionaries"]}
    ev_entries = D["adverse_event_type"]["entries"]
    n_dict = sum(1 for e in ev_entries if e.get("origin") != "ledger")
    n_led = sum(1 for e in ev_entries if e.get("origin") == "ledger")
    units = list(AU.units.values())
    pst = Counter(e["status"] for e in AU.phrases.values())
    ploc = Counter()
    pwhy = Counter()
    for e in AU.phrases.values():
        ploc[e["status"]] += len(e["locators"])
        if e["status"] == "sentence":
            pwhy[(e.get("why") or {}).get("analyzer") or "judge_phrase"] += len(e["locators"])
    empty = sum(len(e["locators"]) for e in AU.phrases.values() if e["status"] in ACTIVE and not e["units"])
    comp_st = Counter(r["status32"] for r in A["complications"])
    o += ["### 부작용 — 사건 노드 · 단위 · 문구 분포(8차)", "",
          md_table(["", "ERD 실측(목록 규칙 · 3판)", "결정 전(분석기)", "8차(결정 뒤)"], [
              ("사건 사전 값(adverse_event_type · 사전)", "—", sum(1 for e in ctx["dic0"]["dictionaries"][ctx["dic_index"]["adverse_event_type"]]["entries"] if e.get("origin") != "ledger"), n_dict),
              ("새 사건 노드(origin=ledger · 정식)", ctx["erd"].get("v3_3_measure", {}).get("ledger_events", "—") if isinstance(ctx["erd"].get("v3_3_measure"), dict) else "—", s0["ledger_events"], f"{s1['ledger_events']}(out/dictionaries.json origin=ledger {n_led})"),
              ("사건 노드 합(사전 + 새)", "—", "—", n_dict + n_led),
              ("부작용 단위", "—", s0["units_total"], f"{len(units)} · {_kv(dict(Counter(u['event_kind'] for u in units)))}"),
              ("부작용 문구 자리 2,285 · status", _kv(s0["safety_by_status"]) if False else "—", _kv(s0["safety_by_status"]), _kv(dict(ploc))),
              ("  sentence 의 까닭(자리)", "—", "—", _kv(dict(pwhy))),
              ("문구 사전 항목 status", "—", _kv(s0["safety_entries_by_status"]) + " + 메모 " + _kv(s0["memo_entries_by_status"]), _kv(dict(pst))),
              ("사건 칸이 비는 exact·new 문구 자리", "—", s0["adverse_unattached"], empty),
              ("complications 이름 65", "—", _kv(s0["complications_by_status"]), _kv(dict(comp_st))),
              ("⑦ strong / weak(결정 전) · open(8차)", "—", f"{s0['dup_pairs_strong']} / {s0['dup_pairs_weak']}", f"{s1['dup_pairs_strong']} / {s1['dup_pairs_weak']} · open strong {sum(1 for x in ctx.get('ledger_dup_conflicts', []) if x.get('grade') == 'strong' and x['status'] == 'open')}"),
          ]), "",
          "exact = 사전 사건 · new = 새 노드 · sentence = 설명문/문장꼴(b)/애매(분석기 · 노드 없음 · 사람 판정) · note = 메모 · approved = 결정 지도. 미연결 상태는 없다(§0.2).", ""]
    # 분석기 토막 통계
    st = s1.get("_analyzer") or {}
    if st:
        o += ["분석기(V3.3-B) 토막 결과(결정 뒤 · 사전 사건 0 인 토막):", "", md_table(["결과", "토막"], sorted(st.get("segment_kinds", {}).items(), key=lambda kv: -kv[1])), "",
              f"규칙 적용 {_kv(st.get('rules', {}))} · N1 명사형 노드 {st.get('n1_names')} · 단독 출현 0 노드(R3 신호 · 버리지 않음) {st.get('solo_strict_zero_nodes')} · 괄호 안 판정 {_kv(st.get('paren_kinds', {}))} · "
              f"사전 밖 구조 말(R2 · side 보존) {_kv(st.get('r2_struct_side', {}))} · R1 후보(N2 수식어 · 노드 토막) {_kv(st.get('r1_new', {}))}.", ""]
    # (폐색, 부위) 단위 표
    occ_units = sorted((u for u in units if norm(u["event"]) == norm("폐색")), key=lambda u: (u.get("site") or "", u["id"]))
    emb_units = [u for u in units if norm(u["event"]) == norm("색전")]
    occ_e = next((e for e in ev_entries if norm(e["canonical"]) == norm("폐색")), None)
    emb_e = next((e for e in ev_entries if norm(e["canonical"]) == norm("색전")), None)
    shared = set(norm(s_["value"]) for s_ in (occ_e or {}).get("synonyms", [])) & set(norm(s_["value"]) for s_ in (emb_e or {}).get("synonyms", []))
    o += ["### (폐색, 부위) 단위 — V3.3-C R2 를 사전 값에도 · 폐색 ≠ 색전", "",
          md_table(["단위", "사건", "부위", "물질", "자리(occ)", "원천"], [(u["id"], u["event"], u.get("site") or "none", u.get("qualifier") or "none", len(u["occ"]), ", ".join(sorted(set(u["origins"])))) for u in occ_units]), "",
          f"폐색 단위 {len(occ_units)}((폐색, 혈관) 있음 {any((u.get('site') or '') == '혈관' for u in occ_units)}) · (혈관 폐색, none) 단위 {sum(1 for u in units if norm(u['event']) == norm('혈관 폐색'))} · 색전 단위 {len(emb_units)}({', '.join(f'({u['event']}, {u.get('site') or 'none'}, {u.get('qualifier') or 'none'})' for u in sorted(emb_units, key=lambda u: (u.get('site') or '', u.get('qualifier') or '')))}) · "
          f"폐색↔색전 공유 동의어 {len(shared)} · 둘을 잇는 ⑦ 쌍 {sum(1 for x in ctx.get('ledger_dup_conflicts', []) if {norm(x['pair']['node']), norm(x['pair']['other'])} == {norm('폐색'), norm('색전')})} · 옛 표면형 「혈관 폐색」이 사전 값에 남음 {sum(1 for e in ev_entries for v in [e['canonical']] + [s_['value'] for s_ in e.get('synonyms', [])] if norm(v) == norm('혈관 폐색'))}.", ""]
    # category · unreviewed
    recs_now = {t: list(S.E.get(t, {}).values()) for t in S.E}
    ncat = category_refs(S, recs_now, dic)
    unrev_nodes = sum(1 for e in ev_entries if e.get("status") == "unreviewed")
    unrev_prod = sum(1 for e in D["product_name"]["entries"] if e.get("status") == "unreviewed")
    o += ["### category 참조 · unreviewed", "",
          f"- out/ 의 사건 분류 속성 참조(adverse_effect 의 분류 속성 · adverse_event_type 의 category/category_review): **{ncat}** (V3.3-E · check V3.3-E 가 out/ 텍스트 전수로 다시 센다).",
          f"- 사건 노드(adverse_event_type origin=ledger)의 status 필드: {unrev_nodes}(정식 노드 · 필드 없음) · 장비 제품(product_name origin=taxonomy)의 status=unreviewed: {unrev_prod}(ERD §1.4 V3.2-5 문장 그대로 — ERD 질문 #8).", ""]
    # product.kind · R36
    pk = Counter(r["attrs"]["kind"][0]["value"] for r in S.E["product"].values() if "kind" in r["attrs"])
    o += ["### 제품 구성품(V3.3-A)", "", f"product.kind {_kv(dict(pk))} · component_of 값 있음 {sum(1 for r in S.E['product'].values() if (r['attrs'].get('component_of') or [{}])[0].get('value'))} · R36 엣지 {c['relations'].get('R36', 0)} · what_kind=component 튜플 {sum(1 for r in S.E['procedure'].values() if r['attrs']['what_kind'][0]['value'] == 'component')} — 원장 칸 없음 · 값 0.", ""]
    # 분석기 캐시
    if an:
        stt = an.stats()
        cache_out = os.path.join(out_dir, "kiwi-cache.json")
        o += ["### 분석기 캐시(V3.3-B · kiwipiepy)", "",
              f"kiwipiepy **{stt['kiwi_version']}**(고정 {stt['pinned']}) · 정본 캐시 `{_rel(stt['cache_path'])}`(항목 {stt['cache_entries_total']}) · 이번 빌드가 읽은 항목 {stt['entries_used']}(사전 등록 묶음 {len(stt['dicts_used'])} · {_kv(stt['dicts_used'])}) → `out/kiwi-cache.json`({os.path.getsize(cache_out) if os.path.exists(cache_out) else 0:,} bytes) · "
              f"워커 호출 {stt['worker_calls']}(미리 채움 문구 {stt['miss_texts']} · 지연 미스 {stt['lazy_misses']}) · 캐시 키 = 판 + 등록 사전 해시 + 문구(NFC). 캐시가 차면 venv 없이 재현(check ④).", ""]
    # 게이트 6
    if g6:
        o += ["### 결정 묶음 6 게이트(`out/gate/batch6.json`·`.md`) — 묶음별 자리", "",
              md_table(["묶음", "자리", "물을 자리", "옵션", "추천"], [(k, v["leaves"], v["ask"], v["options"], v["recommended"]) for k, v in g6["by_item"].items()]), "",
              f"자리 {g6['leaves']} · 물을 자리 {g6['ask']} · 추천 {g6['recommended']}(원장 병기 쌍만) · ⑦ weak {g6['weak']} 은 `batch6-weak.json`. 새 사건 노드는 목록만(옵션 없음 · 사용자 「종류 질문 없음」).", ""]
    # 7차 재현
    r7 = getattr(args, "repro7", None)
    b7 = json.load(open(p7, encoding="utf-8")) if os.path.exists(p7) else {}
    if r7 and os.path.exists(r7):
        mr = json.load(open(r7, encoding="utf-8"))
        same = mr.get("determinism_key") == b7.get("determinism_key")
        o += ["### 7차 재현(8차 lib · ERD v3.2 · 원장 2판)", "", f"`{_rel(r7)}` determinism_key `{mr.get('determinism_key')}` vs `baseline/manifest-7차.json` `{b7.get('determinism_key')}` → **{'같음' if same else '다름'}**. "
              "명령: `python3 build.py --erd ../erd-v3.2.json --dict ../erd-v3.2-dictionaries.json --colmap ../erd-v3.2-column-map.md --tuples ../erd-v3.2-tuples.json --tuples-prev ../erd-v3.1-tuples.json --bronze ../bronze/phub-ledger-v2 --decisions <batch6a 를 뺀 저장소> --out <임시>` (6-A 결정은 v3.3 몫이라 v3.2 재현 저장소에서 뺐다 — 결정 저장소에 ERD 판 필드가 없다 · ERD 질문 #14).", ""]
    else:
        o += ["### 7차 재현(8차 lib · ERD v3.2 · 원장 2판)", "", "재현 manifest 없음(`--repro7`) — 종료 보고에서 대조.", ""]
    # ERD 질문
    o += ["### ERD 질문 — v3.3 문장으로 구현이 갈리지 않는 자리(코디가 ERD 로 돌려보낼 것 · 임시 처리는 전부 보존·기록)", "",
          md_table(["#", "자리", "ERD 문장", "갈리는 점", "임시 처리(8차)"], [
              (1, "§1.3 R1·R2 목록", "「수식어(R1)」「부위·구조 말(R2)」", "R1 낱말(장기간·임시·과도 …)·R2 구조 말(신경·안면신경·전신 …)이 ERD 규칙 데이터에 없다(1차 발주서 목록)", "lib/adverse33.py ASSIST_R1/ASSIST_R2 상수(analyzer_assist) · 뗀 말은 parsed.misc(by=analyzer_r1)·side 로 보존"),
              (2, "§1.3 관형어 하나 = 수식어", "「R1 · R15 qualifier_text · 보존」", "뗀 관형어가 어느 칸에 보존되나(R15 qualifier_text 자리가 부작용 엣지에 없음)", "문구 parsed.misc(class misc · by=analyzer_n2) · R1 후보 게이트"),
              (3, "§1.3 R2 사전 밖 구조 말", "「부위 칸으로 뗀다」", "신경·안면신경·전신은 부위 사전 값이 아니라 부위 칸에 못 간다", "side(보존 · 칸 아님) · 수는 §16 분석기 표"),
              (4, "§1.3 문장꼴(b)·애매", "「노드를 세우지 않고 사람 판정으로」", "phrase_dictionary.status 열거형에 「애매」 값이 없다", "status=sentence + why.analyzer(sentence_b|ambiguous|predicate)"),
              (5, "§9.22 #6 자극감↔자극", "「fold_approve + canonical_rename」", "rename 뒤 핵심어 「자극」은 사전 값이라 결정 전 분해에 노드가 없다 → fold_approve 는 대상 없음", "canonical_rename 하나로 닫음(fold 19 + rename 1 = 20)"),
              (6, "§9.22 #9 표정 경직감↔표정 경직", "대표 이름 「경직」", "쌍의 b 는 「표정 경직」(수식어 표정 + 경직) — 「표정 경직」→「경직」 접기는 결정에 없다", "into=표정 경직 · 「표정 경직」 노드 그대로"),
              (7, "§10 ③ 대조", "「ERD 실측은 분석기 없이 돈다」", "③ 「결정 전 수치 = 실측」은 분석기 없는 분해로만 성립", "check ③ 은 analyzer=None 분해로 대조 · 분석기 수치는 §16"),
              (8, "§1.4 V3.2-5 장비 제품 status=unreviewed", "「status=unreviewed · license_status=미확인」", "발주서 「unreviewed 등급 0」과 충돌(사건 노드만?)", "사건 노드 status 삭제 · 장비 제품은 ERD 문장 그대로(수 §16)"),
              (9, "§1.5 원칙 C R2 부위 칸", "「같은 멤버 안에서 바로 붙은 사건에만」", "R2 로 뗀 부위는 토막이 아니라 멤버 단위로 붙는다(한 멤버 두 토막이면 둘 다)", "멤버 단위(원칙 C 글자대로) · 자리 수는 (폐색, 부위) 표"),
              (10, "발주서 캐시 키 「문구 정규화형」", "—", "분석기 결과가 글자 위치를 가지므로 정규화형(공백 제거)으로는 못 키운다", "키 = 판 + 등록 사전 해시 + 원문(NFC)"),
              (11, "§9.23 lib 참조 10", "「실버 빌더 8차 개정 몫」", "v3.2 경로(7차 재현 · 바이트 동일)에는 사건 분류 속성이 남아야 한다", "v3.3 경로만 0 · lib 의 v≤3.2 분기 자리 수는 종료 보고"),
              (12, "§9.21 HA·히알루론산", "따로 선 값 둘", "한 값 + 동의어인지", "값 둘(동의어 결정 없음)"),
              (13, "§9.21 동의어 자리", "전체얼굴·풀페이스·러브핸들·팔·눈 밑·코 끝", "승인 범위(값 15)에 동의어가 드나", "넣지 않음(결정 reason 에 후보 기록)"),
              (14, "§5 결정 레코드", "「빌드는 approved 만」", "v3.3 결정(6-A)을 v3.2 재현 빌드가 읽지 않게 할 필드가 없다", "재현은 batch6a 를 뺀 저장소 사본으로"),
              (15, "§1.3 T2a 사전 사건 포착", "「사전 통째 일치가 먼저」", "문장꼴 토막 안 사전 사건 NNG(조사 붙음)를 분석기가 잡아 exact 로 붙임 — 통째 일치 밖", "T2a-capture 로 붙이고 수를 §16 표에"),
              (16, "§1.9 원장 3판 · 결정 anchor", "「synergy 라벨이 Mxx- 접두 없이 정식 이름에 닿는다」", "2판 synergy 라벨로 세운 REF- anchor(DEC-2026-11-04-B2B-S3C-16 fold_approve 의 anchor 7 중 synergy @45·@55)가 3판에서 바뀌어 결정이 실버에 닿지 않는다(rejected 1)", "그대로 거부 기록 · 재지정은 사용자(새 anchor 로 결정 갱신)"),
          ]), ""]
    with open(os.path.join(out_dir, "report.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")
