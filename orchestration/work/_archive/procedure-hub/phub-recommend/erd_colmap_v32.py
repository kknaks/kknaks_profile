# -*- coding: utf-8 -*-
"""ERD v3.2 잎 키 행선지 규칙. v3.1(erd_colmap_v31.py) 위에 V3.2-0~9 가 닿는 행만 바꾼다.
  이동(MOVES_V32): 타임라인 9 행(id · category · name · period · label · normal/abnormal/caution/emergency → post_procedure_timeline · R33) · consent emergency_signs(→ emergency_sign.text) ·
                   문헌 adverse_effects 8 행(statement · patient_ko/en/zh/ja · accuracy_score/note · added_at → evidence_statement.* · kind=adverse_effects)
  비고만(NOTE_CHANGES_V32): 부작용 문구 safety.* 13 행(V3.2-0 노드 원칙 · V3.2-7 메모) · complications name · mandatory_disclosures(문구 사전 아님 · adverse_ref) · taxonomy 항목 name(V3.2-5) · products ingredient/material(V3.2-6) · 부위 출처(V3.2-4 parent) · consent categories[].id(R35) · 인용 pmid
COLMAP · MOVES*(이전 판) · MOVES_V32 · NOTE_CHANGES_V32 · resolve 를 노출한다. erd_build_v32.py 가 읽는다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v31 as V31  # noqa
import erd_spec_v32 as S32  # noqa

COLMAP = {f: list(rows) for f, rows in V31.COLMAP.items()}
MOVES, MOVES_V22, MOVES_V23, MOVES_V24, MOVES_V3, MOVES_V31 = list(V31.MOVES), list(V31.MOVES_V22), list(V31.MOVES_V23), list(V31.MOVES_V24), list(V31.MOVES_V3), list(V31.MOVES_V31)
NOTE_CHANGES_V31 = list(V31.NOTE_CHANGES_V31)
MOVES_V32 = []
NOTE_CHANGES_V32 = []
_find = None


def _find_(file, path):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            return i, r
    for r in rows:
        if not isinstance(r[0], str) and r[0].match(path):
            return None, r
    raise KeyError(f"{file} {path}")


def _move(file, path, dest, target, suffix):
    i, r = _find_(file, path)
    new = (path, dest, target, (r[3] + " · " if r[3] else "") + suffix)
    old = f"{r[1]}:{r[2]}"
    if i is None:
        COLMAP[file].insert(0, new)
    else:
        COLMAP[file][i] = new
    MOVES_V32.append((file, path, old, f"{dest}:{target}"))


def _note(file, path, suffix):
    i, r = _find_(file, path)
    new = (path, r[1], r[2], (r[3] + " · " if r[3] else "") + suffix)
    if i is None:
        COLMAP[file].insert(0, new)
    else:
        COLMAP[file][i] = new
    NOTE_CHANGES_V32.append((file, path, r[2], suffix))


_TL = "post-procedure-timeline.json"
_move(_TL, "timelines[].id", "개체", "post_procedure_timeline.ledger_id", "v3.2(V3.2-9): 타임라인 개체 식별(TML-sha256(id))")
_move(_TL, "timelines[].category", "엣지", "R33.from(proc_axis)+target_depth", "v3.2(V3.2-9): R33 has_timeline 의 계열 끝(이름이 튜플로 해결되지 않을 때) · R15 는 타임라인 줄 참조로만")
_move(_TL, "timelines[].name", "개체", "post_procedure_timeline.name", "v3.2(V3.2-9): 시술명 원문 · §1.3 분해 → R33 끝(튜플)")
_move(_TL, "timelines[].phases[].period", "개체", "post_procedure_timeline.phases", "v3.2(V3.2-9): 단계 period(dict:period) — v3.1 R15.period 대체")
_move(_TL, "timelines[].phases[].label", "개체", "post_procedure_timeline.phases", "v3.2(V3.2-9): 단계 label(dict:phase_label) — v3.1 R15.phase_label 대체")
for lv in ("normal", "abnormal", "caution", "emergency"):
    _move(_TL, f"timelines[].phases[].{lv}[]", "개체", "post_procedure_timeline.lines", f"v3.2(V3.2-9 · V3.2-0): 줄(reaction_level={lv}) — 문구 사전이 아니라 타임라인 줄 · parsed · adverse_ref(이미 있는 단위 참조 · R34) · " + ("닿지 않으면 정상 경과 메모" if lv == "normal" else "ref|ref_partial|none"))
_move("consent-checklist.json", "categories[].emergency_signs[]", "개체", "emergency_sign.text", "v3.2(V3.2-0): 응급 징후 줄 — 자기 테이블(SGN-) · parsed · adverse_ref(참조 · R35) · 문구 사전 아님")
_LIT = "literature-evidence.json"
for leaf, tgt in (("statement", "statement"), ("patient_ko", "patient_text"), ("patient_en", "patient_text"), ("patient_zh", "patient_text"), ("patient_ja", "patient_text"), ("accuracy_score", "accuracy_score"), ("accuracy_note", "accuracy_note"), ("added_at", "added_at")):
    _move(_LIT, f"categories.{{code}}.adverse_effects[].{leaf}", "개체", f"evidence_statement.{tgt}", "v3.2(V3.2-0): 문헌 adverse_effects 는 evidence_statement(kind=adverse_effects) · statement·patient_ko 는 refer 분해로 adverse_ref · 단위 general_description 이 참조(V3.2-8)")
_SAFETY = [("extracted.json", "{code}.safety.common[]"), ("extracted.json", "{code}.safety.uncommon[]"), ("extracted.json", "{code}.safety.serious[]"), ("extracted.json", "{code}.safety.emergency[]"),
           ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.common[]"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.serious[]"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]"),
           ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.long_term[]"),
           ("taxonomy.json", "modality[].extracted.safety.common[]"), ("taxonomy.json", "modality[].extracted.safety.uncommon[]"), ("taxonomy.json", "modality[].extracted.safety.serious[]"),
           ("taxonomy.json", "modality[].products[].extracted.safety.common[]"), ("taxonomy.json", "modality[].products[].extracted.safety.serious[]"), ("taxonomy.json", "modality[].products[].extracted.safety.common_side_effects[]")]
for f, p in _SAFETY:
    _note(f, p, "v3.2(V3.2-0 · V3.2-7): 부작용 문구 종류 — exact(사전 그대로) | new(사전에 없으면 멤버 핵심어가 원장 사건 노드 · ⑦ 후보) | note(메모) | sentence(설명문) · unlinked 없음 · 토큰화 V3.2-1")
_note("complications.json", "categories[].complications[].name", "v3.2(V3.2-0): raw_name 없음 — 미등록 조각이 있으면 핵심어 원장 사건 노드(origin=ledger · ⑦)")
_note("complications.json", "categories[].complications[].management", "v3.2(V3.2-8): 단위 general_management 의 참조 대상(값 복사 없음)")
_note("consent-checklist.json", "categories[].mandatory_disclosures[]", "v3.2(V3.2-0): 문구 사전 항목이 아니다 — clinical_rule.parsed · adverse_ref(참조만)")
_note("consent-checklist.json", "categories[].id", "v3.2(V3.2-0): emergency_sign.modality_codes · R15(계열 → 단위) emergency_sign_refs")
_note("taxonomy.json", "modality[].subcategories[].items[].name", "v3.2(V3.2-5): 장비 계열·하위분류 항목 이름은 product_name 사전 값(origin=taxonomy · 자동 등록 · 제외 규칙) → 항목 what=product 승격")
for f, p in (("products.json", "biostimulator.products[].ingredient"), ("products.json", "skin_booster.products[].ingredient"), ("products.json", "thread_lift.products[].material")):
    try:
        _note(f, p, "v3.2(V3.2-6): 성분 사전 값 — 시술 분해 사전(what=ingredient · primary 없을 때)")
    except KeyError:
        pass
for f, p in (("anatomy-danger-zones.json", "zones[].name_ko"), ("taxonomy.json", "problem[].subcategories[].label")):
    _note(f, p, "v3.2(V3.2-4): site 사전 값 출처 · parent(계층) 필드 · 닫힌 목록(값 추가는 승인)")


# ---- 검토 S-3 — 비고의 옛 구조 잔재(표현 개체 · R29 · raw_name · unlinked) 정리(표적 그대로 · 비고만)
SCRUBBED_V32 = []
for _f, _rows in COLMAP.items():
    for _i, _r in enumerate(_rows):
        if isinstance(_r[3], str) and any(b in _r[3] for b in S32.BANNED):
            _n = S32.scrub(_r[3])
            if _n != _r[3]:
                _rows[_i] = (_r[0], _r[1], _r[2], _n)
                SCRUBBED_V32.append((_f, _r[0] if isinstance(_r[0], str) else _r[0].pattern, _r[2]))


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
