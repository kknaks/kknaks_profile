# -*- coding: utf-8 -*-
"""ERD v3.1 잎 키 행선지 규칙. v3(erd_colmap_v3.py) 위에 V3.1-1~10 이 닿는 행만 바꾼다.
  이동(표적 변경 · MOVES_V31 · 29 행):
    V3.1-7  consent-checklist categories[].mandatory_disclosures[] : 개체 modality.mandatory_disclosures → 개체 clinical_rule.text(kind=disclosure · R32 basis=ledger · 문구 사전 kind=disclosure 로도)
    V3.1-10 표현 관련 28 행(adverse_expression.text 21 · patient_text 4 · accuracy_score/accuracy_note/added_at 3) : 개체 adverse_expression.* → 사전 dict:phrase_dictionary(문구 사전 항목 · R15 source_phrases 부록 · 단위 explanations · 게이트 unlinked_phrases)
  비고만(NOTE_CHANGES_V31):
    V3.1-4  사람 조건 이름 9 키(person_condition.name 그대로 · 조건 사전 출처 · 단위 식별 · phrases[] 부록) · consent categories[].id(R16 끝 = 조건 단위)
    V3.1-2  제품 note·legal_warning·regulatory_status(product.* 그대로 · clinical_rule(product_note) 출처 후보 · R32 는 edge_create)
    V3.1-5  R12 자리 잎 키(annual_plans schedule procedures · optimal_combo · sequence · comparison name · combos) 와 market-pricing name(회·차 → session_count/session_index · qualifier_text)
    V3.1-9  complications name(단위 세 칸 · 경과는 R15.course) · complications duration/onset(엣지 그대로)
COLMAP · MOVES(이전 판) · MOVES_V31 · NOTE_CHANGES_V31 · resolve 를 노출한다. erd_build_v31.py 가 읽는다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v3 as V3  # noqa
import erd_spec_v31 as S  # noqa

COLMAP = {f: list(rows) for f, rows in V3.COLMAP.items()}
MOVES = list(V3.MOVES)
MOVES_V22 = list(V3.MOVES_V22)
MOVES_V23 = list(V3.MOVES_V23)
MOVES_V24 = list(V3.MOVES_V24)
MOVES_V3 = list(V3.MOVES_V3)
NOTE_CHANGES_V3 = list(V3.NOTE_CHANGES_V3)
MOVES_V31 = []
NOTE_CHANGES_V31 = []


def _find(file, path):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            return i, r
    for r in rows:
        if not isinstance(r[0], str) and r[0].match(path):
            return None, r
    raise KeyError(f"{file} {path}")


def _move(file, path, dest, target, suffix):
    i, r = _find(file, path)
    new = (path, dest, target, (r[3] + " · " if r[3] else "") + suffix)
    old = f"{r[1]}:{r[2]}"
    if i is None:
        COLMAP[file].insert(0, new)
    else:
        COLMAP[file][i] = new
    MOVES_V31.append((file, path, old, f"{dest}:{target}"))


def _note(file, path, suffix):
    i, r = _find(file, path)
    new = (path, r[1], r[2], (r[3] + " · " if r[3] else "") + suffix)
    if i is None:
        COLMAP[file].insert(0, new)
    else:
        COLMAP[file][i] = new
    NOTE_CHANGES_V31.append((file, path, r[2], suffix))


# ---- V3.1-7 필수 고지 → clinical_rule(disclosure)
_move("consent-checklist.json", "categories[].mandatory_disclosures[]", "개체", "clinical_rule.text",
      "v3.1(V3.1-7): 문장마다 clinical_rule(kind=disclosure · 원문 · locator) · R32 rule_applies_to(basis=ledger · scope=modality · severity=info) 로 categories[].id 계열에 · 같은 문장은 문구 사전(phrase_dictionary · kind=disclosure) 항목으로 부작용 단위에 닿는다(R15 source_phrases · disclosure=true) · modality.mandatory_disclosures 속성 삭제")

# ---- V3.1-10 표현 28 행 → 문구 사전
_EXPR = [("consent-checklist.json", "categories[].emergency_signs[]"), ("extracted.json", "{code}.safety.common[]"), ("extracted.json", "{code}.safety.uncommon[]"), ("extracted.json", "{code}.safety.serious[]"), ("extracted.json", "{code}.safety.emergency[]"),
         ("literature-evidence.json", "categories.{code}.adverse_effects[].statement"), ("literature-evidence.json", "categories.{code}.adverse_effects[].patient_ko"), ("literature-evidence.json", "categories.{code}.adverse_effects[].patient_en"), ("literature-evidence.json", "categories.{code}.adverse_effects[].patient_zh"), ("literature-evidence.json", "categories.{code}.adverse_effects[].patient_ja"),
         ("literature-evidence.json", "categories.{code}.adverse_effects[].accuracy_score"), ("literature-evidence.json", "categories.{code}.adverse_effects[].accuracy_note"), ("literature-evidence.json", "categories.{code}.adverse_effects[].added_at"),
         ("post-procedure-timeline.json", "timelines[].phases[].normal[]"), ("post-procedure-timeline.json", "timelines[].phases[].abnormal[]"), ("post-procedure-timeline.json", "timelines[].phases[].caution[]"), ("post-procedure-timeline.json", "timelines[].phases[].emergency[]"),
         ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.common[]"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.serious[]"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.long_term[]"),
         ("taxonomy.json", "modality[].extracted.safety.common[]"), ("taxonomy.json", "modality[].extracted.safety.uncommon[]"), ("taxonomy.json", "modality[].extracted.safety.serious[]"),
         ("taxonomy.json", "modality[].products[].extracted.safety.common[]"), ("taxonomy.json", "modality[].products[].extracted.safety.serious[]"), ("taxonomy.json", "modality[].products[].extracted.safety.common_side_effects[]")]
for f, p in _EXPR:
    leaf = p.rsplit(".", 1)[-1].replace("[]", "")
    what = ("문헌 정확도·등록일 → 항목 accuracy[]" if leaf in ("accuracy_score", "accuracy_note", "added_at") else "환자 설명 → 항목 translations[](en/zh/ja · 자리 ko 는 자기 항목) · 단위 explanations[] 부록" if leaf.startswith("patient_") else "문구 → 정규화형 항목(status auto|approved|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases")
    _move(f, p, "사전", "dict:phrase_dictionary", f"v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — {what}")

# ---- V3.1-4 조건 사전 · 단위 식별 · 문장 부록
for k in S.CONDITION_KIND_BY_SOURCE:
    f, p = k.split(":", 1)
    _note(f, p, f"v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind={S.CONDITION_KIND_BY_SOURCE[k]}) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases")
_note("consent-checklist.json", "categories[].id", "v3.1(V3.1-4): R16 끝은 조건 단위(CND- · 사전 정준값+kind) · v3.1(V3.1-7): R32(basis=ledger) from 계열")
_note("pre-procedure-checklist.json", "category_specific[].id", "v3.1(V3.1-4): R16 끝은 조건 단위(CND-)")

# ---- V3.1-2 제품 note 규칙 문장 후보
for f, p in [("products.json", "prp_exosome.products[].legal_warning"), ("products.json", "prp_exosome.products[].regulatory_status"), ("taxonomy.json", "modality[].products[].note")]:
    _note(f, p, "v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보 — 규칙 문장이면 edge_create(R32 rule_applies_to · from_ref locator)가 레코드와 엣지를 세운다(값 자동 생성 없음 · 실측 §9.7.2)")
for sec in ("botulinum_toxin", "skin_booster", "prp_exosome"):
    _note("products.json", f"{sec}.products[].note", "v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보(「화장품 허가. 주사/주입 사용 금지」 류) — R32 는 edge_create 로만 · 실측 §9.7.2")

# ---- V3.1-5 회·차 자리
for f, p in [("treatment-optimization.json", "annual_plans[].schedule[].procedures[]"), ("treatment-optimization.json", "by_concern[].severity_levels[].optimal_combo[]"), ("treatment-sequence.json", "common_combos[].sequence[]"), ("procedure-comparison.json", "comparisons[].procedures[].name"), ("problem-packages.json", "problems[].complaints[].combos[].combo[]")]:
    _note(f, p, "v3.1(V3.1-5): `\\d+회` → R12.session_count · `\\d+차` → R12.session_index(R12 자리)")
for f, p in [("problem-packages.json", "problems[].complaints[].procedures[].name"), ("treatment-optimization.json", "by_age_group[].recommended_base[]"), ("treatment-optimization.json", "by_age_group[].avoid[]"), ("treatment-optimization.json", "by_age_group[].upgrade[]"), ("synergy.json", "links[].from"), ("synergy.json", "links[].to"), ("treatment-sequence.json", "incompatible_same_day[].pair[]"), ("treatment-sequence.json", "minimum_intervals[].from"), ("treatment-sequence.json", "minimum_intervals[].to"), ("market-pricing.json", "categories[].items[].name")]:
    _note(f, p, "v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음)")

# ---- V3.1-9 단위 세 칸 · 경과는 엣지
_note("complications.json", "categories[].complications[].name", "v3.1(V3.1-9): 단위 = (사건, 부위, 물질) 세 칸 · 상대 부위는 none(relative_site_text 보존) · 이름의 경과 조각은 category → 단위 R15.course · raw_name 은 그대로")
_note("complications.json", "categories[].id", "v3.1(V3.1-9): R15.course 는 이 category → 단위 엣지의 속성(이름의 경과 조각) · v3.1(V3.1-10): 문구 유래 엣지는 source_phrases 부록")
_note("literature-evidence.json", "categories.{code}.adverse_effects[].citations[].pmid", "v3.1(V3.1-10): 문헌 문구의 인용은 문구 사전 항목 citations[](개체 아님) · R19 from 에서 adverse_expression 삭제")

# ---- V3.1-6 stopwords 겹침
_note("taxonomy.json", "modality[].group", "v3.1(V3.1-6): modality_group 값 「관리」가 stopword 와 겹친다 — 통째 일치가 먼저 · 분해 사전이 아니라 충돌 없음(overlap 목록)")


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
