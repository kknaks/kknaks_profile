# -*- coding: utf-8 -*-
"""ERD v2 잎 키 행선지 규칙. v1.1 규칙(erd_colmap_v11.py) 위에 구조 변경 2건의 이동만 덧씌운다.
  ① taxonomy 항목 행 procedure.* → catalog_item.*
  ② adverse_effect.name 행 → dict:adverse_event_type(complications 이름 = 사전 뼈대) / adverse_expression.text(문구·문장·징후·환자 설명)
     literature adverse_effects 의 patient_*/accuracy_*/added_at → adverse_expression.*
각 항목: (path 또는 regex, dest, target, note). MOVES = (file, path, v1.1 target, v2 target) 이동 표.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v11 as V11  # noqa

COLMAP = {f: list(rows) for f, rows in V11.COLMAP.items()}
MOVES = []


def _replace(file, path, dest, target, note):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            if r[2] != target or r[1] != dest:
                MOVES.append((file, path, f"{r[1]}:{r[2]}", f"{dest}:{target}"))
            rows[i] = (path, dest, target, note)
            return
    raise KeyError(f"{file} {path}")


# ---- ① taxonomy 항목 → catalog_item (v1.1 procedure 행 전부)
for path, dest, target, note in list(COLMAP["taxonomy.json"]):
    if isinstance(path, str) and target.startswith("procedure."):
        _replace("taxonomy.json", path, dest, "catalog_item." + target[len("procedure."):], note + " · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26)")
_replace("taxonomy.json", "modality[].subcategories[].items[].name", "개체", "catalog_item.name",
         "분류 항목 이름 그대로. R3 제품 일치(같은 계열 제품명) · v2: 분해 규칙 §1.4 로 procedure 튜플 원천 ①")
_replace("taxonomy.json", "modality[].subcategories[].items[].id", "개체", "catalog_item.aliases", "질문 4 · v2: CAT- 개체의 alias")

# ---- ② 부작용: complications 이름 = 사건 사전 뼈대 (분해 → adverse_effect 튜플)
_replace("complications.json", "categories[].complications[].name", "사전", "dict:adverse_event_type",
         "v2: 65 이름을 분해한 사건 조각이 사전 뼈대(표기 변형 = 동의어). 이름 하나 → 튜플(event×site×course) 하나 이상 → R15(계열 → 튜플)")
_replace("complications.json", "categories[].complications[].duration", "엣지", "R15.duration", "v2: 「영구적」·「비가역적」은 경과 사전(course) 동의어 출처이기도 함")

# ---- ② 문구·문장·징후·환자 설명 → adverse_expression (분해 → R29 expresses)
_AEX = "개체", "adverse_expression.text"
_replace("literature-evidence.json", "categories.{code}.adverse_effects[].statement", *_AEX, "kind=evidence_statement · v2: v1.1 adverse_effect(literature_claim) 에서 이동. R19 cites · R20 · R29")
for lang in ["ko", "en", "zh", "ja"]:
    _replace("literature-evidence.json", f"categories.{{code}}.adverse_effects[].patient_{lang}", "개체", "adverse_expression.patient_text", f"kind=patient_text, lang={lang} · 같은 문헌 레코드의 statement 표현과 같은 튜플(§1.5)")
_replace("literature-evidence.json", "categories.{code}.adverse_effects[].accuracy_score", "개체", "adverse_expression.accuracy_score", "v2: adverse_effect 에서 이동")
_replace("literature-evidence.json", "categories.{code}.adverse_effects[].accuracy_note", "개체", "adverse_expression.accuracy_note", "v2: adverse_effect 에서 이동")
_replace("literature-evidence.json", "categories.{code}.adverse_effects[].added_at", "개체", "adverse_expression.added_at", "v2: adverse_effect 에서 이동")
_replace("consent-checklist.json", "categories[].emergency_signs[]", *_AEX, "kind=emergency_sign · R29 → R15(frequency_class=emergency)")
for k in ["normal", "abnormal", "caution", "emergency"]:
    note = "kind=symptom_phrase · R29 → R15(reaction_level=%s)" % k + (" · normal 문구는 사전 원천 아님(표현만, 닿으면 엣지 표시)" if k == "normal" else "")
    _replace("post-procedure-timeline.json", f"timelines[].phases[].{k}[]", *_AEX, note)
for k in ["common", "uncommon", "serious", "emergency"]:
    _replace("extracted.json", f"{{code}}.safety.{k}[]", *_AEX, f"kind=safety_phrase · R29 → R15(frequency_class={k})")
for k in ["common", "uncommon", "serious"]:
    _replace("taxonomy.json", f"modality[].extracted.safety.{k}[]", *_AEX, f"kind=safety_phrase · R29 → R15(계열, frequency_class={k})")
for k, fc in [("common", "common"), ("serious", "serious"), ("common_adverse_effects", "common(동의 키)"), ("serious_adverse_effects", "serious(동의 키)"), ("long_term", "long_term")]:
    _replace("taxonomy.json", f"modality[].subcategories[].items[].extracted.safety.{k}[]", *_AEX, f"kind=safety_phrase · R29 → R15(catalog_item→승격 규칙, frequency_class={fc})")
for k, fc in [("common", "common"), ("serious", "serious"), ("common_side_effects", "common(동의 키)")]:
    _replace("taxonomy.json", f"modality[].products[].extracted.safety.{k}[]", *_AEX, f"kind=safety_phrase · R29 → R15(product, frequency_class={fc})")

# ---- 시술 축 참조 자리: 행선지는 v1.1 그대로(엣지 속성), 비고에 v2 튜플 원천 표시만
_NOTE_V2 = " · v2: 분해 → procedure 튜플(§1.4) 원천"
for f, p in [("market-pricing.json", "categories[].items[].name"), ("synergy.json", "links[].from"), ("synergy.json", "links[].to"),
             ("problem-packages.json", "problems[].complaints[].procedures[].name"), ("problem-packages.json", "problems[].complaints[].combos[].combo[]"),
             ("procedure-comparison.json", "comparisons[].procedures[].name"), ("treatment-optimization.json", "by_concern[].severity_levels[].optimal_combo[]"),
             ("treatment-optimization.json", "annual_plans[].schedule[].procedures[]"), ("treatment-sequence.json", "common_combos[].sequence[]"),
             ("treatment-sequence.json", "incompatible_same_day[].pair[]"), ("post-procedure-timeline.json", "timelines[].name")]:
    rows = COLMAP[f]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == p:
            rows[i] = (r[0], r[1], r[2], r[3] + _NOTE_V2)


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
