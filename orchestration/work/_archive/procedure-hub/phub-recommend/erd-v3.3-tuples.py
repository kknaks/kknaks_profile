#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v3.3 — 분해·실측기. v3.2 분해기(erd-v3.2-tuples.py · 동결 · 수정 없음)를 그대로 돌리고, 발주서 erd-v3.3-brief.md 의 사용자 결정 A~G 중 실측에 닿는 것을 더한다. 독립 실행.
원장 21 = 브론즈 **3판** `bronze/phub-ledger/`(HASHES.txt 검증) · 2판 `bronze/phub-ledger-v2/`(v3.2 실측 기준 · 대조).

v3.2 → v3.3 (실측에 닿는 것):
  V3.3-A 구성품 — 값 0 의 근거: 원장 전수에서 팁·카트리지·핸드피스·트랜스듀서가 나오는 자리(시술 라벨 자리 0 · 주의·설명 문장만).
  V3.3-B 분석기 — kiwipiepy 판(.venv-kiwi) · 등록할 사전 값(사용자 단어) 수. 분해 자체는 v3.2 규칙 그대로(분석기는 실버 lib · 8차).
  V3.3-C R2 를 사전 값에도 — 바탕 사전에서 「혈관 폐색」→ 폐색(옛 값은 분해 꼴) · 부위 동맥·정맥·안동맥 추가 → (폐색, 혈관)·(폐색, 동맥)… 단위 실측 · 폐색 ≠ 색전 확인 · R30 후보(원장 문구 근거) · 승인 씨앗 21 의 locator.
  V3.3-D 접미사 쌍 20 — 지금 노드·사전에 양쪽이 있는지 · ⑦ strong suffix 쌍 수.
  V3.3-E category — v3.2 산출물의 category 자리 수(실측) · v3.3 레코드에서 0.
  V3.3-F 세분 묶음 — 깊이·세기 말이 든 시술 라벨 자리 · 수식어로 떼면 같아지는 라벨 묶음 · 실 재질/형태 토큰 · 성분 what 수.
  V3.3-G 3판 — synergy from/to 정식 이름 분해 결과(2판 나란히) · 분류 항목 523 · M8-6 항목 2 · 「Mxx-」 접두 남은 자리.
  사전 값 출처(provenance) — ERD 값 전부(49 사전 · 정준값·동의어)에 원장 locator 를 실측으로 붙이고 출처 없는 값을 전수로 뽑는다(삭제 0).

실측은 넷: ① v3.2 2판 실측(erd-v3.2-tuples.json 그대로) ② v3.2 사전 · 3판(G 만의 효과) ③ **v3.3 사전 · 3판(정본)** ④ 참고 — 승인 씨앗 21 을 8차 적용했다고 가정(적용 아님).
입력(같은 폴더): erd-v3.3-dictionaries.json(없으면 erd-v3.2-dictionaries.json 에서 v3.3 바탕을 만든다) · erd-v3.3.json(없으면 erd_spec_v33) · erd-v3.2-tuples.py · erd-v3.2-tuples.json · erd-v3.1-tuples.json · bronze/phub-ledger/ · bronze/phub-ledger-v2/
출력: 표준 출력에 §9 표 + erd-v3.3-tuples.json(main 실행 때)
실행: python3 erd-v3.3-tuples.py
"""
import copy
import importlib.util
import json
import os
import re
import subprocess
import sys
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "bronze", "phub-ledger")
LEDGER_V2 = os.path.join(HERE, "bronze", "phub-ledger-v2")
STEP1 = "step1-products.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


T32 = load_module("erd_v32_tuples", os.path.join(HERE, "erd-v3.2-tuples.py"))
V31, V3 = T32.V31, T32.V3
norm, mkid, md_table, locator, _dedupe, bronze_check, raw_tokens = T32.norm, T32.mkid, T32.md_table, T32.locator, T32._dedupe, T32.bronze_check, T32.raw_tokens
sys.path.insert(0, HERE)
import erd_spec_v33 as S33  # noqa

CUR = T32.CUR
HANGUL = T32.HANGUL


# ---------------------------------------------------------------------------
# 규칙 데이터 — erd-v3.3.json(있으면) → 아니면 v3.3 명세 · D = erd_spec_v33(부위 닫힌 목록에 동맥·정맥·안동맥)
# ---------------------------------------------------------------------------
def rule_data33():
    D = S33
    tok = {"particles": D.PARTICLES, "verb_endings": D.VERB_ENDINGS, "grammar_words": D.GRAMMAR_WORDS, "stem_min_len": D.STEM_MIN_LEN, "relaxed_suffixes": D.RELAXED_SUFFIXES}
    kinds = {"conj_particles": D.CONJ_PARTICLES, "predicate_endings": D.PREDICATE_ENDINGS, "core_exclude": D.CORE_EXCLUDE, "note_words": D.NOTE_WORDS, "sentence_min_tokens": D.SENTENCE_MIN_TOKENS, "sentence_min_grammar": D.SENTENCE_MIN_GRAMMAR, "sentence_latin_ratio": D.SENTENCE_LATIN_RATIO, "fallback_core": D.FALLBACK_CORE, "dup_prefix_min": D.DUP_PREFIX_MIN}
    equip = {"families": D.EQUIP_FAMILIES, "extra_subcats": D.EQUIP_EXTRA_SUBCATS, "exclude_subcat_words": D.EQUIP_EXCLUDE_SUBCAT_WORDS, "exclude_name_words": D.EQUIP_EXCLUDE_NAME_WORDS, "abbrev_min_len": D.ABBREV_MIN_LEN}
    for name in ("erd-v3.3.json", "erd-v3.2.json"):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            j = json.load(open(p, encoding="utf-8"))
            tok = j["resolve_rules"].get("tokenize", tok)
            kinds = j["tuple_rules"].get("phrase_kinds", kinds)
            equip = j["tuple_rules"].get("equipment", equip)
            break
    return tok, kinds, equip, D


T32.rule_data = rule_data33


# ---------------------------------------------------------------------------
# v3.3 바탕 사전 — v3.2 ERD 값에서 (C) 「혈관 폐색」→ 폐색 · 부위 3 · (E) category 삭제
# ---------------------------------------------------------------------------
def prepare_base_v33(dic32):
    """v3.2 사전 파일(파생 항목 포함) → v3.3 바탕(파생·문구 사전 제외 · C·E 적용). 바뀐 자리를 함께 돌려준다."""
    dj = copy.deepcopy(dic32)
    dj["dictionaries"] = [d for d in dj["dictionaries"] if d["name"] != "phrase_dictionary"]
    for d in dj["dictionaries"]:
        d["entries"] = [e for e in d["entries"] if e.get("origin") not in ("ledger", "taxonomy")]
    D = {d["name"]: d for d in dj["dictionaries"]}
    changes = {"category_removed": 0, "category_review_removed": 0, "event_decomposed": [], "site_added": []}
    # E — category 삭제(전 사전 · 사건 사전만 가진 키지만 전수로 뗀다)
    for d in dj["dictionaries"]:
        for e in d["entries"]:
            if "category" in e:
                e.pop("category")
                changes["category_removed"] += 1
            if "category_review" in e:
                e.pop("category_review")
                changes["category_review_removed"] += 1
    # C(1) — R2 를 사전 값에도
    ev = D["adverse_event_type"]
    for old, new, site, syn_note, basis in S33.EVENT_DECOMPOSED_V33:
        e = next((x for x in ev["entries"] if norm(x["canonical"]) == norm(old)), None)
        if e is None:
            continue
        old_id = e["id"]
        e["canonical"] = new
        e["id"] = mkid("DIC", f"adverse_event_type|{new}")
        e["aliases"] = _dedupe(list(e.get("aliases") or []) + [old_id])
        e["decomposed_from"] = {"value": old, "event": new, "site": site, "rule": "R2(V3.3-C(1)) — 사전 값에도", "old_id": old_id, "synonyms": syn_note, "basis": basis, "raw_variant_preserved": True}
        e["synonyms"] = [s for s in e.get("synonyms", []) if norm(s["value"]) != norm(old)]
        changes["event_decomposed"].append({"old": old, "new": new, "site": site, "old_id": old_id, "new_id": e["id"], "synonyms": [s["value"] for s in e["synonyms"]]})
    # C(2) — 부위 3(ERD 값 · 사용자 승인 11-06) · parent 계층
    st = D["site"]
    by = {norm(x["canonical"]): x for x in st["entries"]}
    for val, kind, parent, basis in S33.SITE_ADDED_V33:
        if norm(val) in by:
            continue
        pe = by.get(norm(parent)) if parent else None
        e = OrderedDict([("id", mkid("DIC", f"site|{val}")), ("canonical", val), ("sources", []), ("synonyms", []), ("definition", None), ("site_kind", "layer"), ("zone_id", None), ("name_en", None), ("members", None),
                         ("kind", kind), ("parent", parent), ("parent_id", pe["id"] if pe else None), ("added_in", "v3.3(V3.3-C(2))"), ("basis", basis)])
        st["entries"].append(e)
        by[norm(val)] = e
        changes["site_added"].append({"value": val, "kind": kind, "parent": parent, "id": e["id"]})
    for e in st["entries"]:
        e.setdefault("parent", None)
    dj["erd_version"] = "v3.3"
    dj["bronze_version"] = 3
    return dj, changes


def base_dictionary33(dic):
    """v3.3 사전 파일(파생 항목 포함) → 분해 바탕(파생·문구 사전 제외)."""
    return T32.base_dictionary(dic)


# ---------------------------------------------------------------------------
# 원장 전수 문자열 — 모든 잎(문자열·수) · (file, path, locator, text) · 사전 값 출처(provenance)에 쓴다
# ---------------------------------------------------------------------------
_CODE_KEY = re.compile(r"^(M\d+|auto-)")


def ledger_strings(L, step1=None):
    out = []

    def walk(x, path, idx, file):
        if isinstance(x, dict):
            keys = list(x.keys())
            codey = len(keys) >= 3 and all(_CODE_KEY.match(str(k)) for k in keys)
            for k, v in x.items():
                seg = "{code}" if codey else str(k)
                walk(v, (path + "." + seg) if path else seg, idx + [str(k)] if codey else idx, file)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, path + "[]", idx + [str(i)], file)
        elif isinstance(x, (str, int, float)) and not isinstance(x, bool):
            s = str(x).strip()
            if s:
                out.append((file, path, f"{file}:{path}@{'/'.join(idx)}", s))
    for f in sorted(L):
        walk(L[f], "", [], f)
    if step1 is not None:
        walk(step1, "", [], STEP1)
    return out


def _path_rx(declared):
    """ERD 출처 키 'file:path' → (file, regex) · `*` · `{code}` 는 한 구간."""
    f, p = declared.split(":", 1)
    rx = "^" + re.escape(p).replace(r"\*", r"[^.]+").replace(r"\{code\}", r"[^.]+") + "$"
    return f, re.compile(rx)


def provenance(dic, strings, max_loc=12):
    """ERD 사전 값(파생 제외 · 정준값+동의어) 하나하나에 원장 locator. → ({entry id: prov}, 출처 없는 값 목록, 요약)."""
    toks_cache = {}
    ntext = [(f, p, loc, norm(t), t) for f, p, loc, t in strings]

    def tokens_of(i):
        if i not in toks_cache:
            toks_cache[i] = {norm(x) for x in raw_tokens(ntext[i][4])}
        return toks_cache[i]
    prov, unsourced, summ = {}, [], Counter()
    for d in dic["dictionaries"]:
        if d["name"] == "phrase_dictionary":
            continue
        for e in d["entries"]:
            if e.get("origin") in ("ledger", "taxonomy"):
                continue
            surfaces = [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]
            ns = [norm(s) for s in surfaces if norm(s)]
            declared = []
            for s in e.get("sources", []) or []:
                if s.get("file") and s.get("path") and not str(s["file"]).startswith("("):
                    declared.append(_path_rx(f"{s['file']}:{s['path']}"))
            for s in e.get("synonyms", []):
                for ss in s.get("sources", []) or []:
                    if ss.get("file") and ss.get("path") and not str(ss["file"]).startswith("("):
                        declared.append(_path_rx(f"{ss['file']}:{ss['path']}"))
            erd_default = any(str(s.get("file", "")).startswith("(ERD") or s.get("kind") == "default" for s in e.get("sources", []) or [])
            key_kind = [s for s in (e.get("sources", []) or []) if s.get("kind") == "key" and s.get("file") and s.get("path")]
            if key_kind:
                # 출처 종류 key — 그 경로의 키 이름이 값(safety.common[] · min_months · durationMin …) · 그 경로가 원장에 있으면 출처 있음(locator = 그 경로의 자리)
                kl = []
                for s in key_kind:
                    f0, rx0 = _path_rx(f"{s['file']}:{s['path']}")
                    for f, p, loc, nt, t in ntext:
                        if f == f0 and rx0.match(p):
                            kl.append(loc)
                            if len(kl) >= max_loc:
                                break
                    if kl:
                        break
                if kl:
                    pr = {"status": "ledger(key)", "match": "key", "n": len(kl), "locators": kl[:max_loc], "declared_paths": sorted({f"{s['file']}:{s['path']}" for s in e.get("sources", []) or []})}
                    prov[e["id"]] = pr
                    summ[(d["name"], "ledger(key)")] += 1
                    continue
            hit_decl, hit_any, token_hit = [], [], False
            for i, (f, p, loc, nt, t) in enumerate(ntext):
                ok = None
                for s in ns:
                    if s and s in nt:
                        ok = s
                        break
                if ok is None:
                    continue
                if not token_hit and ok in tokens_of(i):
                    token_hit = True
                if any(f == df and rx.match(p) for df, rx in declared):
                    if len(hit_decl) < max_loc:
                        hit_decl.append(loc)
                elif len(hit_any) < max_loc:
                    hit_any.append(loc)
                if len(hit_decl) >= max_loc and len(hit_any) >= max_loc and token_hit:
                    break
            n_any = sum(1 for f, p, loc, nt, t in ntext if any(s in nt for s in ns)) if (hit_decl or hit_any) else 0
            if hit_decl:
                status, match = "ledger", "token" if token_hit else "substring"
            elif hit_any and not declared:
                status, match = "ledger(경로 미선언 · v3.3 추가 값)", "token" if token_hit else "substring"
            elif hit_any:
                status, match = "ledger(경로 어긋남)", "token" if token_hit else "substring"
            elif erd_default:
                status, match = "erd_default", None
            else:
                status, match = "missing", None
            pr = {"status": status, "match": match, "n": n_any, "locators": (hit_decl + hit_any)[:max_loc], "declared_paths": sorted({f"{s['file']}:{s['path']}" for s in e.get("sources", []) or []})}
            prov[e["id"]] = pr
            summ[(d["name"], status)] += 1
            if status in ("missing", "erd_default"):
                unsourced.append({"dictionary": d["name"], "id": e["id"], "canonical": e["canonical"], "synonyms": surfaces[1:], "declared": pr["declared_paths"], "status": status, "why": "ERD 정의 기본값(원장에 값이 없는 자리를 채우는 정의값)" if status == "erd_default" else "원장 21 + step1 전수에서 정준값·동의어 어느 표면형도 0회"})
    by_dict = OrderedDict()
    for (dn, stt), n in sorted(summ.items()):
        by_dict.setdefault(dn, {})[stt] = n
    return prov, unsourced, {"by_dictionary": by_dict, "total": sum(summ.values()), "by_status": dict(Counter(stt for (dn, stt) in summ.elements()))}


# ---------------------------------------------------------------------------
# A — 구성품 말이 원장 어디에 나오나(값 0 의 근거)
# ---------------------------------------------------------------------------
def component_evidence(strings, L):
    words = S33.COMPONENT_EVIDENCE_WORDS
    rows, by_path = [], Counter()
    label_hits = [{"label": lab, "slot": slot, "locator": loc, "words": [w for w in words if norm(w) in norm(lab)]} for slot, f, p, loc, lab, hint in T32.procedure_label_sites(L) if lab is not None and any(norm(w) in norm(lab) for w in words)]
    label_paths = {"taxonomy.json:modality[].subcategories[].items[].name", "synergy.json:links[].from", "synergy.json:links[].to", "market-pricing.json:items[].name"}
    for f, p, loc, t in strings:
        nt = norm(t)
        hit = [w for w in words if norm(w) in nt]
        if not hit:
            continue
        rows.append({"words": hit, "file": f, "path": p, "locator": loc, "text": t[:120], "in_label_slot": f"{f}:{p}" in label_paths})
        by_path[f"{f}:{p}"] += 1
    exact = Counter()
    for w in words:
        exact[w] = sum(1 for r in rows if w in r["words"])
    return {"words": words, "occurrences": len(rows), "by_word": dict(exact), "by_path": dict(by_path.most_common()), "label_slot_hits": label_hits, "rows": rows[:60], "phrase_포텐자_팁": sum(1 for f, p, loc, t in strings if "포텐자" in t and "팁" in t)}


# ---------------------------------------------------------------------------
# B — 분석기 판 · 등록할 사전 값 수(분해는 v3.2 규칙 그대로)
# ---------------------------------------------------------------------------
def kiwi_probe(dic):
    py = S33.KIWI_PYTHON
    out = {"interpreter": os.path.relpath(py, HERE), "available": os.path.exists(py), "version": None, "pinned": S33.KIWI_PINNED, "pinned_ok": None, "user_words": len(T32.all_surfaces(dic)), "error": None}
    if out["available"]:
        try:
            r = subprocess.run([py, "-c", "import kiwipiepy; print(kiwipiepy.__version__)"], capture_output=True, text=True, timeout=120)
            out["version"] = (r.stdout or "").strip() or None
            out["error"] = (r.stderr or "").strip()[-200:] or None
        except Exception as ex:  # noqa
            out["error"] = repr(ex)
    if out["version"]:
        out["pinned_ok"] = out["version"].startswith(S33.KIWI_PINNED + ".") or out["version"] == S33.KIWI_PINNED
    return out


# ---------------------------------------------------------------------------
# C — R2 사전 값 · 부위 3 · 폐색 ≠ 색전 · R30 후보 · 승인 씨앗
# ---------------------------------------------------------------------------
def r2_dictionary_measure(R, dic33, changes, texts, strings):
    ad = R["adverse"]
    units = ad["tuples"]
    surf = T32.all_surfaces(dic33)
    D = {d["name"]: d for d in dic33["dictionaries"]}
    out = {"decomposed": changes["event_decomposed"], "old_surface_in_dictionary": [c["old"] for c in changes["event_decomposed"] if norm(c["old"]) in surf]}
    rows = []
    for c in changes["event_decomposed"]:
        us = [t for t in units if norm(t["event"]) == norm(c["new"])]
        rows.append({"event": c["new"], "units": [{"id": t["id"], "site": t["site"] or "none", "qualifier": t["qualifier"] or "none", "n_sources": len(t["sources"]), "origins": t["origins"]} for t in us],
                     "unit_event_site": [t["id"] for t in us if norm(t["site"] or "") == norm(c["site"])], "n_units": len(us)})
    out["event_units"] = rows
    # 옛 글자 「혈관 폐색」이 든 문구 자리가 어디에 붙었나
    old_rows = []
    for c in changes["event_decomposed"]:
        key = norm(c["old"])
        for e in ad["phrase_dictionary"]:
            hits = [v for v in e["raw_variants"] if key in norm(v)]
            if hits:
                old_rows.append({"phrase": hits[0][:80] + (f" (+{len(hits) - 1} 변형)" if len(hits) > 1 else ""), "status": e["status"], "units": e["units"], "events": e["parsed"].get("events"), "sites": e["parsed"].get("sites"), "n": len(hits)})
        for r in ad["complications"]:
            if key in norm(r["text"]):
                old_rows.append({"phrase": r["text"][:80], "status": "complications:" + r["status32"], "units": r["unit_ids"], "events": r.get("event_fragments"), "sites": [c_["site"] for c_ in r["candidates"] if c_.get("site")], "n": 1})
    out["old_value_phrases"] = old_rows
    # 붙은 꼴(「혈관폐색」) — 목록 규칙 실측에서는 토큰 하나라 가르지 못해 새 노드로 선다 · 분석기(V3.3-B · dryrun3 N3)가 부위+사건으로 가른다
    out["attached_form_nodes"] = [{"canonical": n["canonical"], "n_locators": n["n_locators"], "locators": n["locators"][:4], "note": "붙은 꼴 — 이 실측(v3.2 목록 규칙)은 한 토큰을 가르지 못해 새 노드 · 분석기 적용(8차)에서 R2 로 (폐색, 혈관)에 모인다(dryrun3 §2 (라) N3)"} for n in ad["ledger_events"] if any(norm(n["canonical"]) == norm(c["old"]) for c in changes["event_decomposed"])]
    # 부위 3
    site_rows = []
    for val, kind, parent, basis in S33.SITE_ADDED_V33:
        tl = T32.token_locators(texts, val, CUR.get("tok"))
        sub = [(f, p, loc, t) for f, p, loc, t in strings if norm(val) in norm(t)]
        us = [t for t in units if norm(t["site"] or "") == norm(val)]
        site_rows.append({"value": val, "kind": kind, "parent": parent, "id": mkid("DIC", f"site|{val}"), "token_locators": [x["locator"] for x in tl][:12], "n_token": len(tl), "n_substring": len(sub), "substring_paths": dict(Counter(f"{f}:{p}" for f, p, loc, t in sub).most_common(6)),
                          "units_with_site": [{"id": t["id"], "event": t["event"]} for t in us], "basis": basis})
    out["sites_added"] = site_rows
    # 폐색 ≠ 색전
    ev = D["adverse_event_type"]
    e_p = next((x for x in ev["entries"] if norm(x["canonical"]) == norm("폐색")), None)
    e_s = next((x for x in ev["entries"] if norm(x["canonical"]) == norm("색전")), None)
    shared = set(norm(s["value"]) for s in (e_p or {}).get("synonyms", [])) & set(norm(s["value"]) for s in (e_s or {}).get("synonyms", []))
    both = []
    for e in ad["phrase_dictionary"]:
        evs = {norm(x) for x in (e["parsed"].get("events") or [])}
        if evs & {"폐색", "막힘"} and "색전" in evs:
            both.append({"phrase": e["raw_variants"][0][:90], "events": sorted(evs), "units": e["units"], "n": len(e["locators"])})
    for r in ad["complications"]:
        evs = {norm(x) for x in (r.get("event_fragments") or [])}
        if evs & {"폐색", "막힘"} and "색전" in evs:
            both.append({"phrase": r["text"][:90], "events": sorted(evs), "units": r["unit_ids"], "n": 1})
    dup_ps = [d for d in ad["duplicate_pairs"] if {norm(d["new"]), norm(d["existing"])} >= {"폐색", "색전"}]
    out["occlusion_embolism"] = {"shared_synonyms": sorted(shared), "phrases_with_both": both, "dup_pairs_between": dup_ps, "same_unit": any(len({norm(ad_["event"]) for ad_ in units if ad_["id"] in b["units"]} & {"폐색", "색전"}) == 2 and len(b["units"]) == 1 for b in both)}
    # R30 후보 — 원장 문구(부작용 문구 · complications 이름 · 동의서 고지·응급 징후 · 타임라인 줄) 한 문구에 둘 다
    cands = []
    seen = set()
    sources = [(ax, kind, f, p, loc, t) for ax, kind, f, p, loc, t, mod in texts if ax == "adverse"]
    for cat in R["adverse"]["disclosures"]:
        sources.append(("consent", "disclosure", "consent-checklist.json", "categories[].mandatory_disclosures[]", cat["locator"], cat["text"]))
    for s in R["adverse"]["emergency_signs"]:
        for loc in s["locators"]:
            sources.append(("consent", "emergency", "consent-checklist.json", "categories[].emergency_signs[]", loc, s["text"]))
    for T in R["adverse"]["timelines"]:
        for P in T["phases"]:
            for ln in P["lines"]:
                sources.append(("timeline", ln["reaction_level"], "post-procedure-timeline.json", "timelines[].phases[].*[]", ln["locator"], ln["text"]))
    causal = ("인한", "의한", "일으킬", "일으켜", "유발", "이어", "진행", "→", "시 ")
    for frm, to, fw, tw in S33.R30_CANDIDATE_RULES:
        for ax, kind, f, p, loc, t in sources:
            nt = norm(t)
            if any(norm(w) in nt for w in fw) and any(norm(w) in nt for w in tw):
                k = (frm, to, loc)
                if k in seen:
                    continue
                seen.add(k)
                cands.append({"from": frm, "to": to, "text": t[:110], "locator": loc, "table": ax, "kind": kind, "causal_marker": any(c in t for c in causal), "status": "proposed(edge_create · 레코드 없음)"})
    out["r30_candidates"] = cands
    out["r30_edges"] = 0
    return out


def approved_seeds_measure(seeds):
    out = {"site": [], "ingredient_material": []}
    srows = {norm(r["value"]): r for r in seeds["site"]["rows"]}
    for val, kind, parent in S33.SEED_APPROVED_V33["site"]:
        r = srows.get(norm(val))
        locs = (r or {}).get("locators", [])
        syn = [(x["value"], x["n"], x["locators"][:3]) for x in (r or {}).get("synonyms", []) if x["n"]]
        out["site"].append({"value": val, "kind": kind, "parent": parent, "n": (r or {}).get("n", 0), "locators": locs[:12], "synonym_locators": syn, "status": "승인됨 · 8차 적용", "decision": "dictionary_add(site · kind · parent) · 8차", "in_erd_dictionary": False, "ledger_evidence": bool(locs or syn)})
    irows = {norm(r["value"]): r for r in seeds["ingredient_material"]["rows"]}
    for val, _, _ in S33.SEED_APPROVED_V33["ingredient_material"]:
        r = irows.get(norm(val))
        out["ingredient_material"].append({"value": val, "n": (r or {}).get("n", 0), "locators": (r or {}).get("locators", [])[:12], "basis": (r or {}).get("basis"), "status": "승인됨 · 8차 적용", "decision": "dictionary_add(ingredient_material) · 8차", "in_erd_dictionary": False, "ledger_evidence": bool((r or {}).get("locators"))})
    dropped = [r for r in seeds["ingredient_material"]["rows"] if r.get("status") == "proposed" and norm(r["value"]) not in {norm(v) for v, _, _ in S33.SEED_APPROVED_V33["ingredient_material"]}]
    out["ingredient_dropped_by_coordinator"] = [{"value": r["value"], "n": r["n"], "basis": r.get("basis"), "note": "기계 오추출(코디 판단 · 기본값 버림) — 심부·딥·얕은·약한은 F 묶음의 깊이·세기 값"} for r in dropped]
    return out


# ---------------------------------------------------------------------------
# D — 접미사 쌍 20 · 3쌍 · ⑦ suffix 쌍
# ---------------------------------------------------------------------------
def suffix_measure(R, dic33):
    ad = R["adverse"]
    surf = {}
    for e in next(d for d in dic33["dictionaries"] if d["name"] == "adverse_event_type")["entries"]:
        surf.setdefault(norm(e["canonical"]), "adverse_event_type:" + e["canonical"])
        for s_ in e.get("synonyms", []):
            surf.setdefault(norm(s_["value"]), "adverse_event_type:" + e["canonical"])
    nodes = {norm(n["canonical"]): n for n in ad["ledger_events"]}
    dup_keys = {frozenset((norm(d["new"]), norm(d["existing"]))): d for d in ad["duplicate_pairs"]}

    def where(x):
        n = norm(x)
        if n in surf:
            return "dictionary:" + surf[n]
        if n in nodes:
            return f"ledger_node({nodes[n]['n_locators']})"
        return "없음(v3.2 규칙 분해에서는 노드 아님 · 분석기 노드)"
    rows = []
    for a, b, rule, canon, dec in S33.SUFFIX_PAIRS_V33:
        d = dup_keys.get(frozenset((norm(a), norm(b))))
        rows.append({"a": a, "b": b, "rule": rule, "canonical": canon, "decision": dec, "a_where": where(a), "b_where": where(b), "dup_pair_in_v33": bool(d), "dup_grade": d["grade"] if d else None,
                     "canonical_in_user_list": any(norm(c) == norm(canon.split("(")[0]) for c in S33.CANONICAL_PHENOMENON_NAMES), "dictionary_side_is_suffix_form": norm(a) in surf and not norm(b) in surf})
    non = [{"a": a, "b": b, "a_where": where(a), "b_where": where(b), "dup_pair_in_v33": frozenset((norm(a), norm(b))) in dup_keys, "decision": "사용자 결정 필요(임상 동치 · 접미사 아님)"} for a, b in S33.NON_SUFFIX_PAIRS_V33]
    suffix_dups = [d for d in ad["duplicate_pairs"] if any(r.startswith("suffix_") for r in d["rules"])]
    return {"pairs": rows, "non_suffix_pairs": non, "dup_suffix_pairs_total": len(suffix_dups), "dup_suffix_by_rule": dict(Counter(r for d in suffix_dups for r in d["rules"] if r.startswith("suffix_"))),
            "dup_suffix_pairs_in_20": sum(1 for r in rows if r["dup_pair_in_v33"]), "dup_suffix_감각": [d for d in suffix_dups if "suffix_감각" in d["rules"]],
            "pairs_already_same_dictionary_value": sum(1 for a, b, *_ in S33.SUFFIX_PAIRS_V33 if norm(a) in surf and norm(b) in surf and surf[norm(a)] == surf[norm(b)])}


# ---------------------------------------------------------------------------
# E — category 자리 수(v3.2 산출물 실측) · v3.3 에서 0
# ---------------------------------------------------------------------------
def _count_key(x, key):
    n = 0
    if isinstance(x, dict):
        n += 1 if key in x else 0
        for v in x.values():
            n += _count_key(v, key)
    elif isinstance(x, list):
        for v in x:
            n += _count_key(v, key)
    return n


def category_measure(R, dic33, erd33=None):
    out = {"v32": {}, "v33": {}}
    for name, key in (("erd-v3.2-dictionaries.json", "category"), ("erd-v3.2-dictionaries.json", "category_review"), ("erd-v3.2-tuples.json", "event_category")):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            j = json.load(open(p, encoding="utf-8"))
            if name.endswith("dictionaries.json"):
                D = {d["name"]: d for d in j["dictionaries"]}
                out["v32"][f"{name}:{key}"] = sum(1 for e in D["adverse_event_type"]["entries"] if key in e)
            else:
                out["v32"][f"{name}:{key}"] = sum(1 for t in j["adverse"]["tuples"] if key in t)
    p = os.path.join(HERE, "erd-v3.2.json")
    if os.path.exists(p):
        j = json.load(open(p, encoding="utf-8"))
        out["v32"]["erd-v3.2.json:decision_kinds.new_value 「category」"] = sum(1 for k in j["decision_kinds"] if "category" in (k.get("new_value") or ""))
    out["v33"]["dictionaries:category"] = sum(_count_key(d["entries"], "category") for d in dic33["dictionaries"])
    out["v33"]["dictionaries:category_review"] = sum(_count_key(d["entries"], "category_review") for d in dic33["dictionaries"])
    out["v33"]["tuples:event_category"] = _count_key(R["adverse"]["tuples"], "event_category") + _count_key(R["adverse"].get("folded", []), "category")
    if erd33 is not None:
        out["v33"]["erd.json:decision_kinds.new_value 「category」"] = sum(1 for k in erd33["decision_kinds"] if "category" in (k.get("new_value") or ""))
    out["touched_table"] = [{"artifact": a, "where": b, "v32_count": c, "disposition": d} for a, b, c, d in S33.CATEGORY_TOUCHED_V33]
    out["ledger_occurrences_of_7_labels"] = None   # 채움: ledger_label_count
    return out


def category_labels_in_ledger(strings):
    labels = ["국소 일시 반응", "염증/감염", "구조/이물", "전신", "색소", "신경", "혈관"]
    exact = {lab: sum(1 for f, p, loc, t in strings if norm(t) == norm(lab)) for lab in labels}
    return {"labels": labels, "exact_value_occurrences": exact, "note": "7 라벨이 원장 잎 값 그대로인 자리 수(부분 문자열 아님 · 「혈관」「색소」「신경」은 낱말로는 나오지만 분류 라벨 값으로는 0)"}


def strip_category(R):
    n = 0
    for t in R["adverse"]["tuples"]:
        if "event_category" in t:
            t.pop("event_category")
            n += 1
    for t in R["adverse"].get("folded", []) or []:
        if "category" in t:
            t.pop("category")
            n += 1
    s = R["adverse"]["summary"]
    for k in ("complications_by_category", "tuples_by_category"):
        if k in s:
            s.pop(k)
            n += 1
    return n


# ---------------------------------------------------------------------------
# F — 「무엇을·어떻게 세분」 묶음 실측(설계안 근거 · 적용 0)
# ---------------------------------------------------------------------------
def f_bundle_measure(R, L, v32tup=None):
    sites = [x for x in T32.procedure_label_sites(L) if x[4] is not None]
    depth = [norm(w) for w in S33.F_DEPTH_WORDS]
    thread_tok = {norm(w) for w in S33.F_THREAD_WORDS}
    res_by_label = {}
    for slot, rows in R["procedure"]["references"].items():
        for r in rows:
            res_by_label[(str(r["label"]), r.get("hint"))] = r
            res_by_label.setdefault((str(r["label"]), None), r)
    for r in R["procedure"]["market_pricing"]:
        res_by_label[(str(r["label"]), r.get("hint"))] = r
        res_by_label.setdefault((str(r["label"]), None), r)
    cat_by_name = {(r["name"], r["family"]): r for r in R["procedure"]["catalog"]}
    drows, trows = [], []
    for slot, f, p, loc, lab, hint in sites:
        nl = norm(lab)
        toks = {norm(t) for t in raw_tokens(lab)}
        dw = [w for w in S33.F_DEPTH_WORDS if norm(w) in nl and not (norm(w) == "중간" and "중간깊이" in nl)]
        tw = [w for w in S33.F_THREAD_WORDS if (norm(w) in toks) or (norm(w) != "실" and norm(w) in nl)]
        r = cat_by_name.get((lab, hint)) if slot.startswith("①") else (res_by_label.get((str(lab), hint)) or res_by_label.get((str(lab), None)))
        res = (r or {}).get("result") or (r or {}).get("tuple_status")
        wk = (r or {}).get("what_kind")
        if dw:
            stripped = nl
            for w in sorted(depth, key=len, reverse=True):
                stripped = stripped.replace(w, "")
            drows.append({"label": lab, "slot": slot, "locator": loc, "depth_words": dw, "stripped": stripped, "result": res, "what_kind": wk, "unresolved_reason": (r or {}).get("unresolved_reason"), "unregistered": (r or {}).get("unregistered")})
        if tw:
            trows.append({"label": lab, "slot": slot, "locator": loc, "thread_words": tw, "result": res, "what_kind": wk})
    groups = defaultdict(list)
    for r in drows:
        groups[r["stripped"]].append(r["label"])
    all_labels = defaultdict(set)
    for slot, f, p, loc, lab, hint in sites:
        all_labels[norm(lab)].add(str(lab))
    collide = {}
    for k, v in groups.items():
        existing = sorted(all_labels.get(k, set()))
        if existing or len(set(v)) >= 2:
            collide[k] = {"depth_labels": sorted(set(v)), "collides_with": existing}
    for r in drows:
        r["collides_with_existing_label"] = sorted(all_labels.get(r["stripped"], set()))
    ing_what = [r for r in R["procedure"]["catalog"] if r.get("what_kind") == "ingredient"]
    comp_what = [r for r in R["procedure"]["catalog"] if r.get("what_kind") == "component"]
    opts = []
    for o in S33.F_OPTIONS_V33:
        opts.append({"option": o[0], "structure": o[1], "changes": o[2], "pros": o[3], "cons": o[4]})
    return {"depth_label_slots": len(drows), "depth_labels_distinct": len({r["label"] for r in drows}), "depth_rows": drows, "depth_by_word": dict(Counter(w for r in drows for w in r["depth_words"])), "depth_slot_results": dict(Counter(str(r["result"]) for r in drows)),
            "collision_groups_if_modifier_dropped": collide, "collision_groups": len(collide), "thread_label_slots": len(trows), "thread_rows": trows[:40], "thread_by_word": dict(Counter(w for r in trows for w in r["thread_words"])),
            "ingredient_what": len(ing_what), "component_what": len(comp_what), "options": opts, "applied": None,
            "impact": {"F-1": f"PRC- 식별자 전부 재계산({R['procedure']['summary'].get('catalog_items')} 항목 튜플 + 참조 튜플) · 깊이 라벨 자리 {len(drows)} 가 자기 튜플을 가짐 · 충돌 묶음 {len(collide)} 해소",
                       "F-2": f"technique 속성 2 · 깊이 라벨 자리 {len(drows)}(지금 technique 칸은 전부 none — §9.5 catalog_technique none 비율 {R['procedure']['summary'].get('catalog_technique_none_ratio')}) 는 「none + depth」 · 실 재질/형태가 한 라벨에 둘 이상인 자리 {sum(1 for r in trows if len(r['thread_words']) >= 2)} 는 못 받음",
                       "F-3": f"개체 1 · 관계 1 · spec 행 ≥ 깊이 {len(drows)} + 실 재질/형태 {len(trows)} + 성분 what {len(ing_what)} · 식별자 불변 · R15 금기 엣지가 spec 집합을 봐야 함"}}


# ---------------------------------------------------------------------------
# G — 3판 · synergy 정식 이름 · M8-6 항목 2 · 「Mxx-」 접두
# ---------------------------------------------------------------------------
SYNERGY_SLOT = "synergy.links[].from/to (노드 52)"


def ledger3_measure(R, L, L2, v32tup):
    s3, s2 = L["synergy.json"]["links"], L2["synergy.json"]["links"]
    vals3 = Counter([l["from"] for l in s3] + [l["to"] for l in s3])
    vals2 = Counter([l["from"] for l in s2] + [l["to"] for l in s2])
    pref3 = {v: n for v, n in vals3.items() if re.match(r"^M\d+-", v)}
    changed = [{"i": i, "from_v2": b["from"], "to_v2": b["to"], "from_v3": a["from"], "to_v3": a["to"]} for i, (a, b) in enumerate(zip(s3, s2)) if (a["from"], a["to"]) != (b["from"], b["to"])]
    slot3 = R["procedure"]["references"].get(SYNERGY_SLOT, [])
    slot2 = (v32tup or {}).get("procedure", {}).get("references", {}).get(SYNERGY_SLOT, [])
    tx3 = L["taxonomy.json"]["modality"]
    tx2 = L2["taxonomy.json"]["modality"]
    names2 = {it["name"] for m in tx2 for sc in m["subcategories"] for it in sc["items"]}
    new_items = [{"family": m["id"], "subcategory": sc["id"], "label": sc["label"], "name": it["name"], "id": it["id"]} for m in tx3 for sc in m["subcategories"] for it in sc["items"] if it["name"] not in names2]
    cat = {(r["name"], r["family"]): r for r in R["procedure"]["catalog"]}
    for it in new_items:
        r = cat.get((it["name"], it["family"]))
        it["catalog"] = {"what_kind": (r or {}).get("what_kind"), "status": (r or {}).get("tuple_status") or (r or {}).get("status"), "result": (r or {}).get("result")} if r else None
    rows = []
    for r in slot3:
        rows.append({"label": r["label"], "hint": r.get("hint"), "result": r.get("result"), "unresolved_reason": r.get("unresolved_reason"), "unregistered": r.get("unregistered")})
    return {"bronze_version": 3, "catalog_items": R["procedure"]["summary"].get("catalog_items"), "catalog_items_v2": (v32tup or {}).get("procedure", {}).get("summary", {}).get("catalog_items"),
            "synergy_links": len(s3), "synergy_values_distinct_v3": len(vals3), "synergy_values_distinct_v2": len(vals2), "synergy_prefixed_distinct_v3": len(pref3), "synergy_prefixed_slots_v3": sum(pref3.values()), "synergy_prefixed_values": sorted(pref3),
            "synergy_changed_slots": sum(1 for c in changed for k in ("from", "to") if c[f"{k}_v2"] != c[f"{k}_v3"]), "synergy_changed_links": len(changed), "changed_examples": changed[:60],
            "synergy_slot_result_v3": dict(Counter(str(r.get("result")) for r in slot3)), "synergy_slot_result_v2": dict(Counter(str(r.get("result")) for r in slot2)), "synergy_slot_rows_v3": rows,
            "synergy_site_suffix_labels": [v for v in vals3 if " " in v and not re.match(r"^M\d+-", v)], "new_taxonomy_items": new_items, "kind_assessment": S33.G_KIND_ASSESSMENT}


# ---------------------------------------------------------------------------
# 참고 실행 — 승인 씨앗 21 을 8차 적용했다고 가정(적용 아님 · 파일에 쓰지 않는다)
# ---------------------------------------------------------------------------
def projection_approved(dic33_base):
    dj = copy.deepcopy(dic33_base)
    Dn = {d["name"]: d for d in dj["dictionaries"]}
    added = Counter()
    by = {norm(e["canonical"]): e for e in Dn["site"]["entries"]}
    for val, kind, parent in S33.SEED_APPROVED_V33["site"]:
        if norm(val) in by:
            continue
        e = {"id": mkid("DIC", f"site|{val}"), "canonical": val, "sources": [], "synonyms": [], "definition": None, "kind": kind, "parent": parent, "link": "projection"}
        Dn["site"]["entries"].append(e)
        by[norm(val)] = e
        added["site:value"] += 1
    have = {norm(e["canonical"]) for e in Dn["ingredient_material"]["entries"]}
    for val, _, _ in S33.SEED_APPROVED_V33["ingredient_material"]:
        if norm(val) in have:
            continue
        Dn["ingredient_material"]["entries"].append({"id": mkid("DIC", f"ingredient_material|{val}"), "canonical": val, "sources": [], "synonyms": [], "definition": None, "link": "projection"})
        added["ingredient_material:value"] += 1
    return dj, dict(added)


# ---------------------------------------------------------------------------
# 전체 실행
# ---------------------------------------------------------------------------
def run_everything33(dic33, rules, L, rrules, v31tup, v32tup, dic32=None, L2=None, changes=None, step1=None):
    base33 = base_dictionary33(dic33)
    tokr, kinds, equip, D = rule_data33()
    # ② v3.2 사전 · 3판(G 만의 효과)
    Ra = None
    if dic32 is not None:
        base32 = T32.base_dictionary(dic32)
        Ra = T32.run_all32(base32, rules, L, rrules, v31tup)
        strip_category(Ra)
    # v3.1 규칙 · 3판(토큰화가 없앤 조각 셈의 기준)
    R31 = V31.run_all(base33, rules, L, rrules, json.load(open(os.path.join(HERE, "erd-v3-tuples.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "erd-v3-tuples.json")) else None)
    sets31 = T32.unregistered_sets(R31)
    # ③ v3.3 사전 · 3판(정본)
    R = T32.run_all32(base33, rules, L, rrules, v31tup)
    n_strip = strip_category(R)
    R["erd_version"] = "v3.3"
    R["bronze_version"] = 3
    R["procedure"]["summary"]["bronze_version"] = 3
    R["bronze_check"] = bronze_check(LEDGER)
    vocab, vlocs, texts = R["_vocab"]
    skip = {norm(w) for w in tokr["grammar_words"]} | {norm(w["word"]) for w in rules["adverse"]["adverse_stopwords"]["words"]}
    surf = T32.all_surfaces(base33)
    sv, sl = Counter(), defaultdict(list)
    for w, n in vocab.items():
        st = CUR["tok"].strip(w, lambda x: False)
        k = norm(st[0]) if st else w
        sv[k] += n
        for l_ in vlocs.get(w, []):
            if len(sl[k]) < 12 and l_ not in sl[k]:
                sl[k].append(l_)
    pairs = T32.variant_pairs(sv, sl, surf, skip)
    seeds = T32.seed_candidates(R, base33, L, D)
    R["r33"] = T32.r33_rows(R)
    gone = T32.disappeared(R["tokenizer"]["log"], sets31)
    # ④ 참고 — 승인 씨앗 21 적용 가정
    pdic, added = projection_approved(base33)
    tok_saved = dict(CUR)
    RP = T32.run_all32(pdic, rules, L, rrules, v31tup)
    strip_category(RP)
    CUR.clear()
    CUR.update(tok_saved)
    before = T32._metrics(v32tup) if v32tup else None
    base3 = T32._metrics(Ra) if Ra is not None else None
    after = T32._metrics(R)
    R["v32"] = OrderedDict([("regression_v31", {"note": "v3.3: 회귀 기준은 v3.2 2판 실측(before) ↔ v3.2 사전·3판(baseline_v32_ledger3) ↔ v3.3 사전·3판(after)"}), ("disappeared_by_tokenizer", gone), ("variant_pairs", pairs), ("seeds", seeds),
                            ("projection", {"added": added, "R": T32._metrics(RP), "note": "승인 씨앗 21(부위 15 · 성분 6) 8차 적용 가정 — 적용 아님"}),
                            ("before", before), ("baseline_v32_ledger3", base3), ("after", after), ("tokenizer_words", T32._tok_table(tokr, R["tokenizer"])), ("kinds_rules", kinds), ("equipment_rules", {k: v for k, v in equip.items()})])
    # ---- v3.3 실측
    strings = ledger_strings(L, step1)
    prov, unsourced, prov_sum = provenance(dic33, strings)
    R["v33"] = OrderedDict([
        ("bronze", {"version": 3, "dir": "bronze/phub-ledger", "previous_dir": "bronze/phub-ledger-v2", "check": R["bronze_check"], "hashes_changed_from_v2": _hash_diff(LEDGER, LEDGER_V2)}),
        ("ledger_strings", {"count": len(strings), "files": len({f for f, p, loc, t in strings})}),
        ("base_changes", changes or {}),
        ("component", component_evidence(strings, L)),
        ("kiwi", kiwi_probe(base33)),
        ("r2_dictionary", r2_dictionary_measure(R, base33, changes or {"event_decomposed": [], "site_added": []}, texts, strings)),
        ("seeds_approved", approved_seeds_measure(seeds)),
        ("suffix", suffix_measure(R, base33)),
        ("category", category_measure(R, base33)),
        ("f_bundle", f_bundle_measure(R, L, v32tup)),
        ("ledger3", ledger3_measure(R, L, L2, v32tup) if L2 is not None else None),
        ("provenance", {"summary": prov_sum, "unsourced": unsourced, "by_id": prov}),
        ("category_stripped_from_records", n_strip),
        ("deltas", _deltas(before, base3, after)),
    ])
    R["v33"]["category"]["ledger_occurrences_of_7_labels"] = category_labels_in_ledger(strings)
    R["_strings"] = strings
    return R


def _hash_diff(d3, d2):
    import hashlib
    out = []
    for f in sorted(x for x in os.listdir(d3) if x.endswith(".json")):
        a = hashlib.sha256(open(os.path.join(d3, f), "rb").read()).hexdigest()[:16]
        b = hashlib.sha256(open(os.path.join(d2, f), "rb").read()).hexdigest()[:16] if os.path.exists(os.path.join(d2, f)) else None
        if a != b:
            out.append({"file": f, "v3": a, "v2": b})
    return out


def _deltas(before, base3, after):
    keys = ["units", "ledger_events", "unresolved_9", "catalog_self", "ref_unresolved", "market_unresolved", "equipment_products", "ingredient_what", "adverse_kind_unregistered", "reference_tables_unregistered_distinct", "reference_tables_unregistered_total", "procedure_unregistered_distinct", "procedure_unregistered_total", "condition_units", "condition_raw"]
    out = []
    for k in keys:
        b = (before or {}).get(k)
        g = (base3 or {}).get(k)
        a = (after or {}).get(k)
        out.append({"key": k, "v32_ledger2": b, "v32_ledger3": g, "v33_ledger3": a, "delta_G": (g - b) if isinstance(b, int) and isinstance(g, int) else None, "delta_CE": (a - g) if isinstance(a, int) and isinstance(g, int) else None, "delta_total": (a - b) if isinstance(a, int) and isinstance(b, int) else None})
    return out


# ---------------------------------------------------------------------------
# 표 — v3.2 표(§9.9~9.17 · 재사용) + v3.3 표(§9.18~9.25)
# ---------------------------------------------------------------------------
_kv, _locs = T32._kv, T32._locs


def before_after_md33(R):
    V = R["v32"]
    b, g, a, p = V["before"], V["baseline_v32_ledger3"], V["after"], V["projection"]["R"]
    o = ["#### 9.10 규칙·원장 적용 전후 (① v3.2 사전·2판 = erd-v3.2-tuples.json · ② v3.2 사전·3판(G 만) · ③ v3.3 사전·3판(정본) · ④ 참고: 승인 씨앗 21 적용 가정 — 적용 아님)", ""]
    keys = ["adverse_kind_unregistered", "reference_tables_unregistered_distinct", "reference_tables_unregistered_total", "safety_by_status", "units", "ledger_events", "raw_name_units", "ref_unresolved", "market_unresolved", "unresolved_9", "catalog_self", "catalog_by_what_kind", "procedure_unregistered_distinct", "procedure_unregistered_total", "condition_units", "condition_raw", "condition_unregistered_distinct", "condition_unregistered_total", "equipment_products", "ingredient_what"]
    rows = [(k, (b or {}).get(k, "—"), (g or {}).get(k, "—"), (a or {}).get(k, "—"), (p or {}).get(k, "—")) for k in keys]
    o.append(md_table(["지표", "① v3.2·2판", "② v3.2·3판", "③ v3.3·3판", "④ 참고(씨앗 21)"], rows))
    o.append("")
    o.append(f"- ④ 참고 실행에서 더한 값: {_kv(V['projection']['added'])} — 사전 파일에 쓰지 않았다(승인 씨앗은 8차 결정 레코드).")
    o.append(f"- 토큰화가 없앤 조각(v3.1 규칙 기준 · 3판): " + " · ".join(f"{ax} {v['distinct']}" for ax, v in V["disappeared_by_tokenizer"].items()) + ".")
    o.append("")
    return "\n".join(o)


def v33_md(R):
    X = R["v33"]
    o = []
    A = o.append
    # 9.18 A
    c = X["component"]
    A("#### 9.18 제품 구성품(V3.3-A) — 값 0 의 근거: 팁·카트리지·핸드피스·트랜스듀서가 원장 어디에 나오나")
    A("")
    A(f"- 원장 21 + step1 잎 문자열 {X['ledger_strings']['count']} 중 구성품 말이 든 자리 **{c['occurrences']}** · 말별 {_kv(c['by_word'])} · 「포텐자」와 「팁」이 같은 값에 있는 자리 {c['phrase_포텐자_팁']} · **시술 라벨 자리(분류 항목 이름 · 참조 라벨) 적중 {len(c['label_slot_hits'])}** → 구성품 값 0(구조만 · 미래 칸 {len(S33.FUTURE_COLUMNS_V33)}).")
    A("")
    A(md_table(["#", "원장 자리(파일:경로)", "자리 수"], [(i + 1, f"`{k}`", v) for i, (k, v) in enumerate(c["by_path"].items())]))
    A("")
    A(md_table(["#", "말", "파일", "경로", "라벨 자리?", "원문"], [(i + 1, ", ".join(r["words"]), r["file"], f"`{r['path']}`", "예" if r["in_label_slot"] else "—", r["text"]) for i, r in enumerate(c["rows"][:30])]))
    A("")
    A("미래 칸(원장 칸 없음 · 생기면 그 칸에서 값을 세운다):")
    A("")
    A(md_table(["#", "미래 칸", "행선지", "표적", "비고"], [(i + 1, f"`{a}`", b, f"`{c_}`", d) for i, (a, b, c_, d) in enumerate(S33.FUTURE_COLUMNS_V33)]))
    A("")
    # 9.19 B
    k = X["kiwi"]
    A("#### 9.19 토큰화 = 형태소 분석기(V3.3-B) — 판 고정 · 등록할 사전 값 · 분해는 v3.2 규칙 그대로(분석기는 실버 lib · 8차)")
    A("")
    A(f"- kiwipiepy 인터프리터 `{k['interpreter']}` 있음 {k['available']} · 설치 판 **{k['version']}** · 고정 판 {k['pinned']} · 일치 {k['pinned_ok']}" + (f" · 오류 {k['error']}" if k.get("error") else "") + f" · 사용자 단어로 등록할 사전 표면형(정준값·동의어 · catalog_item_name·문구 사전 제외) **{k['user_words']}**.")
    A(f"- 이 실측(§9.9~9.17)의 노드·exact/new 수는 **v3.2 목록 규칙**으로 센 값이다(분석기 미적용). 분석기 적용 수치는 `silver-v3/out-dryrun3/report.md` §5(사전 사건 43 · 새 노드 179 · 사건 노드 222 · ⑦ strong 36)에 있고, 8차 빌드가 정본이 된다. v3.2 목록({len(R['v32']['tokenizer_words'])} 원소)은 §9.11 그대로 보존 — 역할은 「분석기 보조 목록」.")
    A("")
    # 9.20 C
    r2 = X["r2_dictionary"]
    A("#### 9.20 R2 를 사건 사전 값에도(V3.3-C) — 「혈관 폐색」→ 폐색 + 혈관 · 부위 동맥·정맥·안동맥 · 폐색 ≠ 색전 · R30 후보(제안)")
    A("")
    for d in r2["decomposed"]:
        A(f"- 사전 값 **「{d['old']}」({d['old_id']}) → 「{d['new']}」({d['new_id']})** · 부위 말 「{d['site']}」 · 남은 동의어 {d['synonyms']} · 옛 글자가 사전 표면형에 남아 있나: {'예' if d['old'] in r2['old_surface_in_dictionary'] else '아니오(분해 꼴 · raw_variant)'}.")
    for r in r2["event_units"]:
        A(f"- 사건 「{r['event']}」 단위 **{r['n_units']}**: " + " · ".join(f"({r['event']}, {u['site']}, {u['qualifier']}) `{u['id']}` 자리 {u['n_sources']}" for u in r["units"]) + f" — (폐색, 혈관) 단위 {'있음 ' + str(r['unit_event_site']) if r['unit_event_site'] else '**없음**'}.")
    A("")
    for n in r2["attached_form_nodes"]:
        A(f"- 붙은 꼴 「{n['canonical']}」(자리 {n['n_locators']}): {n['note']}.")
    A("")
    A("옛 글자 「혈관 폐색」이 든 문구·이름 자리가 어디에 붙었나:")
    A("")
    A(md_table(["#", "원문", "판정", "사건 조각", "부위 조각", "단위", "자리 수"], [(i + 1, r["phrase"], r["status"], ", ".join(r.get("events") or []) or "—", ", ".join(r.get("sites") or []) or "—", ", ".join(r["units"]) or "—", r["n"]) for i, r in enumerate(r2["old_value_phrases"])]))
    A("")
    A("부위 3(ERD 값 · 사용자 승인 11-06 · parent 계층):")
    A("")
    A(md_table(["#", "값", "kind", "parent", "id", "토큰 자리", "부분 문자열 자리", "경로(상위)", "이 부위를 가진 단위", "근거"], [(i + 1, s["value"], s["kind"], s["parent"] or "—", s["id"], s["n_token"], s["n_substring"], _kv(s["substring_paths"]), ", ".join(f"{u['event']}·{u['id']}" for u in s["units_with_site"]) or "—", s["basis"]) for i, s in enumerate(r2["sites_added"])]))
    A("")
    oe = r2["occlusion_embolism"]
    A(f"- 폐색 ≠ 색전: 공유 동의어 {oe['shared_synonyms'] or 0} · 둘을 잇는 ⑦ 쌍 {len(oe['dup_pairs_between'])} · 한 문구에 둘이 같이 나온 자리 {len(oe['phrases_with_both'])}(한 단위로 접힌 것 {'있음' if oe['same_unit'] else '0'}) — 접지 않았다.")
    A("")
    A(md_table(["#", "원문(둘 다 나옴)", "사건 조각", "단위", "자리 수"], [(i + 1, b["phrase"], ", ".join(b["events"]), ", ".join(b["units"]) or "—", b["n"]) for i, b in enumerate(oe["phrases_with_both"])]))
    A("")
    A(f"R30 leads_to 후보(**제안** · edge_create 는 사용자 · 엣지 {r2['r30_edges']} · 레코드 만들지 않았다) — 원장 한 문구에 두 사건 말이 함께 나온 자리 {len(r2['r30_candidates'])}:")
    A("")
    A(md_table(["#", "후보", "원문", "테이블", "인과 표지", "locator"], [(i + 1, f"{c_['from']} → {c_['to']}", c_["text"], f"{c_['table']}·{c_['kind']}", "예" if c_["causal_marker"] else "—", f"`{c_['locator']}`") for i, c_ in enumerate(r2["r30_candidates"])]))
    A("")
    # 9.21 승인 씨앗
    sa = X["seeds_approved"]
    A("#### 9.21 승인 씨앗(V3.3-C(4)) — 「승인됨 · 8차 적용」(dictionary_add 결정 레코드 · ERD 사전 값 아님) · locator 는 v3.2 씨앗 후보 행(3판 재실측)")
    A("")
    A(md_table(["#", "사전", "값", "kind", "parent", "자리 수", "locator(최대 3)", "동의어 자리", "상태", "결정"], [(i + 1, "site", s["value"], s["kind"], s["parent"] or "—", s["n"], _locs(s["locators"], 3), " · ".join(f"{v}({n})" for v, n, l in s["synonym_locators"]) or "—", s["status"], s["decision"]) for i, s in enumerate(sa["site"])] +
                 [(len(sa["site"]) + i + 1, "ingredient_material", s["value"], "—", "—", s["n"], _locs(s["locators"], 3), s.get("basis") or "—", s["status"], s["decision"]) for i, s in enumerate(sa["ingredient_material"])]))
    A("")
    A(f"성분 씨앗 17 중 버린 {len(sa['ingredient_dropped_by_coordinator'])}(코디 판단 · 기본값 버림 · 「사용자 결정 필요」): " + " · ".join(f"{r['value']}({r['n']})" for r in sa["ingredient_dropped_by_coordinator"]) + ".")
    A("")
    # 9.22 D
    sf = X["suffix"]
    A("#### 9.22 접미사 표기 꼴(V3.3-D) — 쌍 20(fold_approve 결정 · 8차) · 접미사 아닌 3쌍(사용자) · 이 실측(v3.2 규칙)에서의 자리")
    A("")
    A(md_table(["#", "a", "b", "규칙", "대표 이름(현상 · 사용자 목록)", "a 위치", "b 위치", "⑦ 쌍(이 실측)", "결정"], [(i + 1, r["a"], r["b"], r["rule"], r["canonical"] + ("" if r["canonical_in_user_list"] else " ⚠목록 밖"), r["a_where"], r["b_where"], (r["dup_grade"] or "—") if r["dup_pair_in_v33"] else "—", r["decision"]) for i, r in enumerate(sf["pairs"])]))
    A("")
    A(md_table(["#", "a", "b", "a 위치", "b 위치", "⑦ 쌍", "결정"], [(i + 1, r["a"], r["b"], r["a_where"], r["b_where"], "예" if r["dup_pair_in_v33"] else "—", r["decision"]) for i, r in enumerate(sf["non_suffix_pairs"])]))
    A("")
    A(f"- 이 실측의 ⑦ suffix 쌍 {sf['dup_suffix_pairs_total']}({_kv(sf['dup_suffix_by_rule'])}) · 20 쌍 중 이 실측에도 ⑦ 로 서는 쌍 {sf['dup_suffix_pairs_in_20']} · 「감각」 접미 쌍 {len(sf['dup_suffix_감각'])}(⑦ 후보 그대로 · 사용자 결정 없음) · 20 쌍을 위해 사전에 더한 동의어 **0**(결정 레코드 몫).")
    A("")
    # 9.23 E
    ce = X["category"]
    A("#### 9.23 adverse_event_type.category 삭제(V3.3-E) — 닿은 자리 전수 · 원장 출처 0")
    A("")
    A(f"- v3.2 산출물의 category 자리(실측): {_kv(ce['v32'])} · v3.3: {_kv(ce['v33'])} · 실측 레코드에서 뗀 키 {X['category_stripped_from_records']}.")
    lab = ce["ledger_occurrences_of_7_labels"]
    A(f"- 7 라벨이 원장 잎 값 그대로인 자리: {_kv(lab['exact_value_occurrences'])} — {lab['note']}.")
    A("")
    A(md_table(["#", "산출물", "자리", "v3.2 수", "처리"], [(i + 1, r["artifact"], r["where"], r["v32_count"], r["disposition"]) for i, r in enumerate(ce["touched_table"])]))
    A("")
    # 9.24 F
    fb = X["f_bundle"]
    A("#### 9.24 「무엇을·어떻게 세분」 묶음(V3.3-F) — 원장 근거 · 설계안 3 · 영향 수치 · **적용 0**")
    A("")
    A(f"- 깊이·세기 말({', '.join(S33.F_DEPTH_WORDS)})이 든 시술 라벨 자리 **{fb['depth_label_slots']}**(distinct 라벨 {fb['depth_labels_distinct']}) · 말별 {_kv(fb['depth_by_word'])} · 지금 분해 결과 {_kv(fb['depth_slot_results'])} · 깊이 말을 수식어로 떼면 **원장의 다른 라벨과 같아지는 묶음 {fb['collision_groups']}**: " + " · ".join(f"「{'」·「'.join(v['depth_labels'])}」→「{'」·「'.join(v['collides_with']) or '(서로)'}」" for v in fb["collision_groups_if_modifier_dropped"].values()) + ".")
    A(f"- 실 재질/형태 말({', '.join(S33.F_THREAD_WORDS)})이 든 라벨 자리 {fb['thread_label_slots']} · 말별 {_kv(fb['thread_by_word'])} · 한 라벨에 둘 이상 {sum(1 for r in fb['thread_rows'] if len(r['thread_words']) >= 2)}(상위 40 행 안) · 성분 what {fb['ingredient_what']} · 구성품 what {fb['component_what']}.")
    A("")
    A(md_table(["#", "라벨", "자리", "깊이·세기 말", "뗀 뒤", "뗀 뒤 같아지는 원장 라벨", "결과", "what", "locator"], [(i + 1, r["label"], r["slot"][:28], ", ".join(r["depth_words"]), r["stripped"], ", ".join(r.get("collides_with_existing_label") or []) or "—", str(r["result"]), str(r["what_kind"] or "—"), f"`{r['locator']}`") for i, r in enumerate(fb["depth_rows"])]))
    A("")
    A(md_table(["안", "구조", "바뀌는 자리", "장점", "단점 · 열린 질문", "영향(실측)"], [(o_["option"], o_["structure"], o_["changes"], o_["pros"], o_["cons"], fb["impact"][o_["option"].split()[0]]) for o_ in fb["options"]]))
    A("")
    A("어느 안도 적용하지 않았다(개체 22 · 속성·사전 값 추가 0) — 「사용자 결정 필요」.")
    A("")
    # 9.25 G
    g = X["ledger3"]
    if g:
        A("#### 9.25 원장 3판(V3.3-G) — synergy 정식 이름 · M8-6 항목 2 · 분류 항목 523 · 「Mxx-」 접두 남은 자리")
        A("")
        A(f"- 분류 항목 {g['catalog_items_v2']} → **{g['catalog_items']}** · synergy 링크 {g['synergy_links']} · from/to distinct {g['synergy_values_distinct_v2']} → {g['synergy_values_distinct_v3']} · 바뀐 자리 {g['synergy_changed_slots']}(링크 {g['synergy_changed_links']}) · 남은 「Mxx-」 접두 값 {g['synergy_prefixed_distinct_v3']}종 {g['synergy_prefixed_slots_v3']}자리(4판 후보 · 사용자) · 「이름 부위」 꼴 {len(g['synergy_site_suffix_labels'])}: {', '.join(g['synergy_site_suffix_labels'])}.")
        A(f"- synergy 자리 분해 결과 2판 {_kv(g['synergy_slot_result_v2'])} → 3판 {_kv(g['synergy_slot_result_v3'])}.")
        A("")
        A(md_table(["#", "계열", "하위분류", "새 항목(3판)", "id", "분류 항목 튜플"], [(i + 1, it["family"], f"{it['subcategory']} {it['label']}", it["name"], it["id"], _kv(it["catalog"]) if it["catalog"] else "—") for i, it in enumerate(g["new_taxonomy_items"])]))
        A("")
        A(md_table(["#", "링크", "2판 from → to", "3판 from → to"], [(i + 1, c_["i"], f"{c_['from_v2']} → {c_['to_v2']}", f"{c_['from_v3']} → {c_['to_v3']}") for i, c_ in enumerate(g["changed_examples"])]))
        A("")
        A(g["kind_assessment"])
        A("")
    # provenance
    pv = X["provenance"]
    A("#### 9.26 사전 값 출처(provenance) — ERD 값 전부(정준값·동의어)에 원장 locator · 출처 없는 값 전수(삭제 0 · 사용자)")
    A("")
    A(f"- ERD 사전 값 {pv['summary']['total']} 전수 대조(원장 21 + step1 잎 {X['ledger_strings']['count']}): 상태별 {_kv(pv['summary']['by_status'])}. 「ledger(경로 어긋남)」= 선언한 출처 경로가 아닌 자리에서만 찾은 값(출처는 있음 · 경로 비고).")
    A("")
    A(md_table(["사전", "ledger", "경로 어긋남", "erd_default", "missing"], [(dn, v.get("ledger", 0), v.get("ledger(경로 어긋남)", 0), v.get("erd_default", 0), v.get("missing", 0)) for dn, v in pv["summary"]["by_dictionary"].items()]))
    A("")
    A(f"**출처 없는 값 {len(pv['unsourced'])}**(전수 · 삭제하지 않았다):")
    A("")
    A(md_table(["#", "사전", "id", "값", "동의어", "선언한 출처", "상태", "왜"], [(i + 1, u["dictionary"], u["id"], u["canonical"], ", ".join(u["synonyms"]) or "—", ", ".join(f"`{x}`" for x in u["declared"]) or "—", u["status"], u["why"]) for i, u in enumerate(pv["unsourced"])]) if pv["unsourced"] else "(없음)")
    A("")
    # deltas
    A("#### 9.27 실측 요약 델타 — v3.2(2판) → v3.2 사전·3판(G) → v3.3 사전·3판(C·E)")
    A("")
    A(md_table(["지표", "v3.2·2판", "v3.2·3판", "v3.3·3판", "Δ G", "Δ C·E", "Δ 합"], [(d["key"], d["v32_ledger2"], d["v32_ledger3"], d["v33_ledger3"], d["delta_G"], d["delta_CE"], d["delta_total"]) for d in X["deltas"]]))
    A("")
    return "\n".join(o)


def full_md(R):
    return "\n".join([T32.kinds_md(R), before_after_md33(R), T32.tokenizer_md(R), T32.variants_md(R), T32.nodes_md(R), T32.tables_md(R), T32.inherit_md(R), T32.equipment_md(R), T32.seeds_md(R), v33_md(R)])


def slim(R):
    X = T32.slim(R)
    X.pop("_strings", None)
    return X


def load_all33():
    p33 = os.path.join(HERE, "erd-v3.3-dictionaries.json")
    dic32 = json.load(open(os.path.join(HERE, "erd-v3.2-dictionaries.json"), encoding="utf-8"))
    changes = None
    if os.path.exists(p33):
        dic = json.load(open(p33, encoding="utf-8"))
        changes = dic.get("v33_base_changes")
    else:
        dic, changes = prepare_base_v33(dic32)
    files = [f for f in os.listdir(LEDGER) if f.endswith(".json")]
    L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in files}
    L2 = {f: json.load(open(os.path.join(LEDGER_V2, f), encoding="utf-8")) for f in files} if os.path.isdir(LEDGER_V2) else None
    e33 = os.path.join(HERE, "erd-v3.3.json")
    erd = json.load(open(e33 if os.path.exists(e33) else os.path.join(HERE, "erd-v3.2.json"), encoding="utf-8"))
    rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    if not os.path.exists(e33):
        rules = json.loads(json.dumps(S33.TUPLE_RULES, ensure_ascii=False, default=lambda o: list(o) if isinstance(o, (set, tuple)) else str(o)))
        rrules = json.loads(json.dumps(S33.RESOLVE_RULES, ensure_ascii=False, default=lambda o: list(o) if isinstance(o, (set, tuple)) else str(o)))
        e32 = json.load(open(os.path.join(HERE, "erd-v3.2.json"), encoding="utf-8"))
        rules["adverse"]["adverse_stopwords"] = e32["tuple_rules"]["adverse"]["adverse_stopwords"]
        rules["condition"] = e32["tuple_rules"]["condition"]
    v31 = json.load(open(os.path.join(HERE, "erd-v3.1-tuples.json"), encoding="utf-8"))
    v32 = json.load(open(os.path.join(HERE, "erd-v3.2-tuples.json"), encoding="utf-8"))
    step1 = json.load(open(os.path.join(HERE, STEP1), encoding="utf-8")) if os.path.exists(os.path.join(HERE, STEP1)) else None
    return dic, dic32, rules, rrules, L, L2, v31, v32, changes, step1


def main():
    dic, dic32, rules, rrules, L, L2, v31, v32, changes, step1 = load_all33()
    bc = bronze_check(LEDGER)
    assert bc["hashes_file"] and not bc["mismatch"], f"브론즈 3판 해시 불일치 {bc}"
    R = run_everything33(dic, rules, L, rrules, v31, v32, dic32=dic32, L2=L2, changes=changes, step1=step1)
    print(full_md(R))
    json.dump(slim(R), open(os.path.join(HERE, "erd-v3.3-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n→ erd-v3.3-tuples.json")


if __name__ == "__main__":
    main()
