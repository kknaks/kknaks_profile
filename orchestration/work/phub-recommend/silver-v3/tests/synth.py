# -*- coding: utf-8 -*-
"""합성 원장 조각 — 실제 원장 21 + step1 의 **형식**(키 경로·레코드 모양)만 따르는 작은 가짜 데이터.

실제 원장·실제 결정은 쓰지 않는다(그것은 check.py 몫). 이름은 전부 지어낸 것(알파톡신·베타필러·감마레이저 · 가나제약 …).
ERD 는 실제 `erd-v3.1.json`(시맨틱 층 — 규칙·관계·결정 kind 의 정본)을 읽되 source_files 의 step1 해시만 합성 파일 해시로 바꾼다.
잎 키 행선지 표는 실제 `erd-v3.1-column-map.md`(시맨틱 층)를 그대로 쓴다.

workspace(tmp) 하나 = bronze/ · step1-products.json · erd.json · dict.json · decisions/ · out/.
"""
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
BUILDER = os.path.dirname(HERE)
ERD_DIR = os.path.dirname(BUILDER)
sys.path.insert(0, BUILDER)

from lib.util import mkid, norm  # noqa: E402

ERD_PATH = os.path.join(ERD_DIR, "erd-v3.1.json")
ERD32_PATH = os.path.join(ERD_DIR, "erd-v3.2.json")   # v3.2 합성 빌드(Workspace(erd_path=ERD32_PATH)) — 시험 test_v32
ERD33_PATH = os.path.join(ERD_DIR, "erd-v3.3.json")   # v3.3 합성 빌드(분석기 · 워크스페이스 안 캐시) — 시험 test_v33 · test_edge_refs
COLMAP_PATH = os.path.join(ERD_DIR, "erd-v3.1-column-map.md")

LEDGER_FILES = ["anatomy-danger-zones.json", "combo-recipes.json", "complications.json", "consent-checklist.json", "contraindications.json", "extracted.json",
                "literature-evidence.json", "market-pricing.json", "patient-education.json", "pih-risk.json", "post-procedure-timeline.json", "pre-procedure-checklist.json",
                "problem-combos.json", "problem-packages.json", "procedure-comparison.json", "procedure-profiles.json", "products.json", "synergy.json", "taxonomy.json",
                "treatment-optimization.json", "treatment-sequence.json"]


def _sha(b):
    return hashlib.sha256(b).hexdigest()


# ===========================================================================
# 합성 원장 21 + step1
# ===========================================================================
def ledger():
    L = {}
    L["taxonomy.json"] = {
        "modality": [
            {"id": "M1", "category": "알파톡신", "category_en": "Alpha Toxin", "group": "주사",
             "subcategories": [
                 {"id": "M1-1", "label": "주름알파", "items": [
                     {"id": "M1-1-1", "name": "알파원", "detail": "합성 항목"},
                     {"id": "M1-1-2", "name": "알파원 이마", "detail": "합성", "extracted": {"safety": {"common": ["멍"], "contraindications": ["가상 금기"]}}},
                     {"id": "M1-1-3", "name": "알파원 미지조각", "verification_needed": "확인 필요(합성)"},
                     {"id": "M1-1-4", "name": "알파원 이마 미간", "classification_issue": "합성 메모", "correction_note": "합성 교정"},
                     {"id": "M1-1-5", "name": "알파원 주사"},
                     {"id": "M1-1-6", "name": "알파원 볼", "reclassified_to": "M2"},
                     {"id": "M1-1-7", "name": "알파톡신 이마", "canonical_category": "M1 > 주름알파"},
                     {"id": "M1-1-8", "name": "알파투 이마+미간"},
                 ]},
                 {"id": "M1-2", "label": "턱알파", "items": [
                     {"id": "M1-2-1", "name": "알파원 턱 주사"},
                     {"id": "M1-2-2", "name": "알파원 주사법 턱"},
                     {"id": "M1-2-3", "name": "알파원+베타원"},
                     {"id": "M1-2-4", "name": "알파원 베타원"},
                     {"id": "M1-2-5", "name": "베타필러 턱"},
                 ]},
             ],
             "extracted": {"overview": "알파 개요(taxonomy)", "mechanism": "가상 기전", "indications": {"primary": ["주름"], "extended": []},
                           "contraindications": {"absolute": ["임신"], "relative": ["가상 상대 금기"]},
                           "safety": {"common": ["멍"], "uncommon": [], "serious": ["공기색전"]}, "onset_duration": {"onset": "3일", "peak": "2주", "duration": "4개월"},
                           "aftercare": ["냉찜질"], "related_techniques": []},
             "products": [
                 {"id": "M1-P1", "name": "알파원", "name_en": "AlphaOne", "manufacturer": "가나제약", "country": "한국", "mfds": False,
                  "extracted": {"overview": "알파원 개요", "safety": {"common": ["멍"]}}},
                 {"id": "M1-P2", "name": "알파투", "name_en": "AlphaTwo", "manufacturer": "다라제약", "country": "미국", "mfds": True},
                 {"id": "M1-P3", "name": "알파톡", "name_en": "AlphaTok", "manufacturer": "가나제약", "country": "한국", "mfds": True},
             ]},
            {"id": "M2", "category": "베타필러", "category_en": "Beta Filler", "group": "주사",
             "subcategories": [
                 {"id": "M2-1", "label": "볼륨베타", "items": [
                     {"id": "M2-1-1", "name": "베타원 볼"},
                     {"id": "M2-1-2", "name": "알파원 이마"},
                     {"id": "M2-1-3", "name": "주름알파 볼"},
                 ]},
             ],
             "products": [{"id": "M2-P1", "name": "베타원", "name_en": "BetaOne", "manufacturer": "마바제약", "country": "한국", "mfds": True}]},
            {"id": "M3", "category": "감마레이저", "category_en": "Gamma Laser", "group": "장비",
             "subcategories": [
                 {"id": "M3-1", "label": "토닝감마", "items": [
                     {"id": "M3-1-1", "name": "감마토닝"},
                     {"id": "M3-1-2", "name": "감마원 피부"},
                     {"id": "M3-1-3", "name": "감마토닝 볼"},
                 ]},
                 {"id": "M3-2", "label": "감마투", "items": []},
             ],
             "products": [{"id": "M3-P1", "name": "감마원", "name_en": "GammaOne", "manufacturer": "가나제약", "country": "독일"}]},
        ],
        "problem": [
            {"id": "P1", "category": "주름고민", "category_en": "Wrinkle", "subcategories": [
                {"id": "P1-1", "label": "이마", "items": [{"id": "P1-1-1", "name": "이마 주름", "detail": "합성", "modality_ref": ["M1", "X9"]}]},
                {"id": "P1-2", "label": "잔주름", "items": [{"id": "P1-2-1", "name": "눈가 잔주름", "modality_ref": ["M1"]}]},
            ]},
        ],
    }
    L["products.json"] = {
        "version": "1", "updated": "2026-01-01", "description": "합성",
        "toxin": {"category_id": "M1", "products": [
            {"name": "알파원", "name_en": "AlphaOne", "manufacturer": "가나제약", "country": "일본", "mfds": True},
            {"name": "알파투", "name_en": "AlphaTwo", "manufacturer": "다라제약", "country": "미국", "mfds": True},
            {"name": "알파톡", "name_en": "AlphaTok", "manufacturer": "가나제약", "country": "한국", "mfds": True},
            {"name": "알파쓰리", "name_en": "AlphaThree", "manufacturer": "가나제약", "country": "미국", "mfds": True, "note": "합성"},
        ]},
        "filler": {"category_id": "M2", "products": [{"name": "베타원", "name_en": "BetaOne", "manufacturer": "마바제약", "country": "한국", "mfds": True}]},
        "device": {"category_id": ["M3", "M1"], "products": [{"name": "감마원", "name_en": "GammaOne", "manufacturer": "가나제약", "country": "독일", "type": "장비"}]},
    }
    L["procedure-profiles.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성", "profiles": [
        {"id": "M1", "name": "알파톡신", "name_en": "Alpha Toxin", "phase": "주입", "phaseOrder": 1, "mechanism": ["injection"], "moa_summary": "합성", "aftercare": ["냉찜질"]},
        {"id": "M2", "name": "베타필러", "name_en": "Beta Filler", "phase": "주입", "phaseOrder": 2, "mechanism": ["injection", "regenerative"]},
        {"id": "M3", "name": "감마레이저", "name_en": "Gamma Laser", "phase": "에너지", "phaseOrder": 3, "mechanism": ["thermal", "regeneration"]},
    ]}
    L["extracted.json"] = {
        "M1": {"name": "알파톡신", "safety": {"common": ["주사 부위 부종", "새로운증상"], "uncommon": ["이마", "이마 부종"], "serious": ["부종 일시적"]}, "source": "합성 교과서 1장",
               "name_en": "Alpha Toxin", "overview": "알파 개요(extracted)", "mechanism": "가상 기전", "aftercare": ["냉찜질"],
               "indications": {"primary": ["주름"], "extended": []}, "procedure_id": "alpha-toxin", "contraindications": {"absolute": ["임신"], "relative": []},
               "related_techniques": ["알파원 시술"]},
        "M3": {"name": "감마레이저", "safety": {"common": ["피부 괴사"], "serious": None}, "source": "합성 교과서 2장"},
    }
    L["complications.json"] = {"severity_levels": {"mild": "가벼움", "moderate": "중간", "severe": "심함", "critical": "위급"}, "categories": [
        {"id": "M1", "name": "알파톡신", "complications": [
            {"name": "멍", "severity": "mild", "incidence": "흔함", "onset": "즉시", "risk_factors": [], "management": "냉찜질", "prevention": "압박", "evidence": "https://example.invalid/a; https://example.invalid/b", "duration": "1주"},
            {"name": "멍 (타박상)", "severity": "mild"},
            {"name": "주사 부위 부종", "severity": "가상등급"},
            {"name": "공기색전", "severity": "critical"},
            {"name": "색전", "severity": "critical"},
            {"name": "이마/미간 통증", "severity": "mild"},
            {"name": "지연성 통증", "severity": "mild"},
            {"name": "괴사 (이마)", "severity": "severe"},
            {"name": "미지증상 멍", "severity": "mild", "risk_factors": ["가상요인"]},
            {"name": "피부 괴사", "severity": "severe"},
            {"name": "부종 · 공기", "severity": "mild"},
            {"name": "혈전 색전", "severity": "critical"},
        ]},
        {"id": "M2", "name": "베타필러", "complications": [
            {"name": "멍", "severity": "mild"},
            {"name": "부종", "severity": "mild"},
            {"name": "카테터 감염", "severity": "severe"},
            {"name": "아나필락시스", "severity": "critical"},
        ]},
    ]}
    L["consent-checklist.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성", "categories": [
        {"id": "M1", "name": "알파톡신", "mandatory_disclosures": ["합성 고지", "멍 가능"], "contraindications": ["임신", "가상 질환"], "emergency_signs": ["멍", "공기색전 의심"]},
    ]}
    L["contraindications.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성", "rules": [
        {"from": "M1", "from_name": "알파톡신", "to": "M3", "to_name": "감마레이저", "level": "caution", "interval": "2주", "note": "합성"},
    ]}
    L["literature-evidence.json"] = {"version": "1", "updated": "2026-01-01", "source_method": "합성 방법",
        "accuracy_summary": {"scored_by": "합성", "rubric": "5=정확", "overall_average": 4.0, "n_scored": 1},
        "categories": {
            "M1": {"name": "알파톡신",
                   "moa": [{"statement": "Alpha blocks fake receptors.", "citations": [{"pmid": "100001", "title": "가짜 논문"}], "accuracy_score": 5, "patient_ko": "가짜 수용체를 막는다", "added_at": "2026-01-01"}],
                   "adverse_effects": [
                       {"statement": "멍", "citations": [{"doi": "10.0/fake"}], "accuracy_score": 4, "patient_ko": "멍", "patient_en": "bruise", "added_at": "2026-01-01"},
                       {"statement": "멍", "citations": [], "patient_ko": "부종 일시적"},
                       {"statement": "Fake bruising", "citations": [], "patient_ko": "멍"},
                   ],
                   "effects": [{"statement": "Fake wrinkles reduced.", "citations": [{"oa_url": "https://example.invalid/oa"}], "patient_ko": "주름이 준다"}]},
            "M2": {"name": "베타필러", "moa": [], "adverse_effects": [], "effects": []},
        }}
    L["market-pricing.json"] = {"version": "1", "updated": "2026-01-01", "currency": "KRW", "note": "합성 가격", "categories": [
        {"id": "M1", "name": "알파톡신", "items": [
            {"name": "알파원 이마", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파톡신(다라제약)", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파톡신(가나제약)", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파톡신(마바제약)", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파톡신(알파투)", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파톡신(베타원)", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파원 4회", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파원 진정관리", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파원 국산", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파원 2cc", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파원 주사 주사법", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파원 열", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파원 피부", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "알파원 턱 주사", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "미지조각2 이마", "unit": "회", "low": 1, "mid": 2, "high": 3},
        ]},
        {"id": "M2", "name": "베타필러", "items": [
            {"name": "베타필러(사아제약)", "unit": "cc", "low": 1, "mid": 2, "high": 3},
            {"name": "베타필러 볼", "unit": "cc", "low": 1, "mid": 2, "high": 3},
            {"name": "주름알파", "unit": "cc", "low": 1, "mid": 2, "high": 3},
            {"name": "알파톡", "unit": "cc", "low": 1, "mid": 2, "high": 3},
        ]},
        {"id": "M3", "name": "감마레이저", "items": [
            {"name": "감마원 볼", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "감마원,볼", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "감마원 턱", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "감마원  턱", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "감마원(얼굴)", "unit": "회", "low": 1, "mid": 2, "high": 3},
            {"name": "이마", "unit": "회", "low": 1, "mid": 2, "high": 3},
        ]},
    ]}
    L["patient-education.json"] = {"version": "1", "updated": "2026-01-01", "categories": [
        {"id": "M1", "name": "알파톡신", "patient_name": "알파 주사", "simple_explanation": "합성 설명", "how_it_works": "합성", "duration_simple": "4개월", "pain_level": "낮음", "downtime": "없음",
         "common_concerns": [{"q": "아픈가요", "a": "합성 답"}]},
        {"id": "M9", "name": "없는 계열", "patient_name": "없음"},
    ]}
    L["pih-risk.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성", "risk_levels": {"low": "낮음"}, "notes": {"M1_to_M2": "합성 노트", "M3": "감마 노트"},
                          "procedures": [
                              {"category": "M1", "subcategory": "주름알파", "name": "알파원(이마)", "procedure_ref": "M1-1-2", "pih_risk": "low", "pih_rate": "1%", "fitzpatrick_note": "합성", "risk_factors": [], "prevention": "합성"},
                              {"category": "M1", "subcategory": "주름알파", "name": "알파원 이마 다른이름", "procedure_ref": "M1-1-2", "pih_risk": "low"},
                              {"category": "M3", "subcategory": "토닝감마", "name": "감마", "procedure_ref": "M3", "pih_risk": "moderate"},
                              {"category": "M9", "subcategory": "?", "name": "없음", "procedure_ref": "Z9-9", "pih_risk": "low"},
                          ]}
    L["post-procedure-timeline.json"] = {"version": "1", "updated": "2026-01-01", "consensus_method": "합성 합의", "reaction_levels": {"normal": "정상", "abnormal": "이상", "caution": "주의", "emergency": "응급"},
                                         "timelines": [{"id": "alpha", "category": "M1", "name": "알파톡신", "phases": [
                                             {"period": "1일", "label": "직후", "normal": ["멍", "미지반응"], "abnormal": ["부종 일시적"], "caution": [], "emergency": ["공기색전"]}]},
                                                       {"id": "alpha2", "category": "M1-1", "name": "알파원 이마", "phases": []}]}
    L["pre-procedure-checklist.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성",
                                         "universal_checks": [{"id": "U1", "label": "알레르기 확인", "type": "must_check", "description": "합성"}],
                                         "category_specific": [{"id": "M1", "name": "알파톡신", "checks": [{"label": "임신 여부", "type": "absolute_contraindication"}]}]}
    L["problem-combos.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성", "combos": [
        {"problem_id": "P1", "problem": "주름고민", "packages": [
            {"id": "PK1", "tier": "basic", "tierLabel": "기본", "name": "주름 기본", "procedures": ["M1", "M3", "Q7"], "productTier": "국산", "products": ["알파원"], "priceRange": "합성"}]}]}
    L["problem-packages.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성", "problems": [
        {"problem_id": "P1", "problem": "주름고민", "complaints": [
            {"cc": "이마 주름", "cc_detail": "합성", "cc_group": "이마",
             "procedures": [{"name": "알파원 이마", "category": "M1", "role": "주", "products": ["알파원", "없는제품"]},
                            {"name": "알파원 터치업", "category": "M1", "role": "보조", "products": []}],
             "combos": [{"name": "알파 콤보", "combo": ["알파원", "베타원 볼"], "reason": "합성", "evidence": "합성"}], "alternatives": []},
            {"cc": "합성 호소", "cc_detail": "합성", "cc_group": "없는그룹", "procedures": [], "combos": []},
        ]}]}
    L["procedure-comparison.json"] = {"version": "1", "updated": "2026-01-01", "comparisons": [
        {"id": "c-alpha", "title": "주름고민", "subtitle": "합성", "evidence_notes": [], "procedures": [
            {"name": "알파원 터치업", "category": "M1", "mechanism_simple": "합성", "pain": "1", "downtime": "0", "pih_risk": "low"},
            {"name": "알파원(알파투/알파톡)", "category": "M1"},
            {"name": "감마원 볼 유지 관리", "category": "M3"},
        ]},
        {"id": "c-none", "title": "없는 고민", "procedures": []},
    ]}
    L["synergy.json"] = {"version": "1", "updated": "2026-01-01", "links": [
        {"from": "M1-알파원", "from_category": "M1", "to": "M3-감마원", "to_category": "M3", "type": "함께", "reason": "합성", "timing": "같은 날", "target": "리프팅"},
        {"from": "M1-알파원 이마", "from_category": "M1", "to": "M2-베타원 볼", "to_category": "M2", "type": "다음에", "reason": "합성"},
        {"from": "M2", "from_category": "M2", "to": "M3-감마원", "to_category": "M3", "type": "대신", "reason": "합성"},
    ]}
    L["treatment-optimization.json"] = {"version": "1", "updated": "2026-01-01", "consensus_method": "합성 합의", "optimization_principles": ["합성 원칙"],
        "by_concern": [{"concern": "주름고민", "concern_en": "Wrinkle", "icon": "w", "severity_levels": [
            {"level": "경미 (fine)", "optimal_combo": ["알파원 이마+미간", "알파투/베타원", "알파원+베타원/감마원", "베타필러(턱+볼)", "알파톡신 이마/미간", "알파투 베타원"], "sequence": "합성", "rationale": "합성", "contraindicated_combos": []},
            {"level": "중등", "optimal_combo": ["알파원(이마)", "감마원 피부 1차"]}]},
                       {"concern": "없는고민", "severity_levels": [{"level": "경미", "optimal_combo": []}]}],
        "by_age_group": [{"age": "30대", "primary_concerns": ["주름고민", "없는고민"], "recommended_base": ["알파원(알파투/알파톡)"], "avoid": ["알파원 이마 미간"], "maintenance": "합성", "upgrade": ["알파원 베타원"], "note": "합성"}],
        "combination_rules": [{"rule": "합성 규칙", "detail": "합성", "evidence": "합성 근거", "consensus": "강", "priority": "높음"}],
        "annual_plans": [{"plan_name": "합성 플랜", "age_group": "30대", "annual_budget_range": "합성", "focus": "합성",
                          "schedule": [{"month": 1, "procedures": ["알파원 1차", "베타원 미지조각", "알파원 열 주사"]}, {"month": 2, "procedures": ["M1", "알파원 터치업 집중", "M1-1", "M1-2-3", "M1-1-2"]}]}]}
    L["treatment-sequence.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성", "principles": ["합성 순서 원칙"],
        "sequence_order": [{"order": 1, "phase": "준비", "categories": ["M1", "M1-1", "M2-볼륨베타", "M3-감마원"], "reason": "합성"}],
        "incompatible_same_day": [{"pair": ["알파원", "감마원"], "reason": "합성"}],
        "common_combos": [{"name": "기본 콤보", "sequence": ["알파원", "감마원"], "total_time": "1시간", "note": "합성"}],
        "minimum_intervals": [{"from": "알파원", "to": "베타원", "min_days": 7, "source": "합성 교과서", "reason": "합성"}, {"from": "베타원", "to": "감마원", "min_months": 1, "reason": "합성"}]}
    L["combo-recipes.json"] = {"version": "1", "updated": "2026-01-01", "description": "합성", "recipes": [
        {"id": "R1", "name": "알파 레시피", "subtitle": "합성", "goal": "합성", "intensity": "기본", "procedures": ["M1", "M3", "M1-1-1", "M1-1", "Q8"], "expectedResults": "합성", "followUp": [{"week": 1, "action": "합성"}]}]}
    L["anatomy-danger-zones.json"] = {"version": "1", "updated": "2026-01-01", "consensus_method": "합성 합의",
        "critical_safety_facts": {"mechanism": "합성 사실"},
        "zones": [
            {"id": "forehead", "name_ko": "이마", "name_en": "Forehead", "danger_level": 2, "danger_color": "orange",
             "vessels": [{"name": "가상동맥 (Fake artery)", "depth_mm": 1.0, "diameter_mm": 0.5, "course": "합성", "danger": "합성", "note": "합성", "depth_range_mm": [1.0, 2.0]}],
             "nerves": [{"name": "가상신경", "type": "motor", "significance": "합성"}], "safe_injection_depth": "합성", "tissue_data": {"notes": "합성", "skin_to_periosteum_mm": 3.0},
             "clinical_pearls": ["합성"], "botox_specific": {"target_muscle": "가상근", "risk": "합성", "safe_zone": "합성", "diffusion_range_cm": "1", "key_warning": "합성", "dose_range": "1"},
             "filler_specific": {"risk_level": 2, "primary_risk": "합성", "safe_technique": "합성", "max_per_point_ml": 0.1, "preferred_product": "베타원"}},
            {"id": "glabella", "name_ko": "미간", "name_en": "Glabella", "danger_level": 3, "danger_color": "red", "vessels": [], "nerves": []},
        ]}
    L["step1-products.json"] = {"version": 1, "generated_at": "2026-01-02", "scope": "합성 조사", "items": [
        {"ledger_id": "S1", "segment": "합성", "source": "합성", "family": {"code": "M1", "name": "알파톡신"}, "1_identity": {"kind": "제품", "basis": "합성", "basis_type": "합성"},
         "2_names": {"display_name": "알파원", "ledger_name": "알파원", "search_names": [{"name": "AlphaOne", "lang": "en"}]},
         "4_license": {"status": "정상", "kind": "의약품", "licenses": [{"license_no": "1", "kind": "의약품", "state": "정상", "official_name": "알파원주", "manufacturer": "가나제약", "source": "식약처 합성API"}], "history": [], "recommendable": True},
         "6_companies": {"manufacturer": [{"name": "가나제약"}], "conflicts": [{"field": "manufacturer", "license": "가나제약", "other": "가나", "source": "합성", "note": "합성"}]},
         "evidence": ["https://example.invalid/s1"], "active": True},
        {"ledger_id": "S2", "segment": "합성", "source": "합성", "family": {"code": "기타", "name": "기타"}, "1_identity": {"kind": "제품", "basis": "합성", "basis_type": "합성"},
         "2_names": {"display_name": "새제품", "search_names": []}, "4_license": {"status": "확인 불가", "licenses": [], "history": []},
         "6_companies": {"conflicts": []}, "active": True},
        {"ledger_id": "S3", "segment": "합성", "source": "합성", "family": {"code": "M2", "name": "베타필러"}, "1_identity": {"kind": "제품", "basis": "합성", "basis_type": "합성"},
         "2_names": {"display_name": "베타신제품", "search_names": []}, "4_license": {"status": "미허가", "licenses": [], "history": []},
         "6_companies": {"conflicts": []}, "active": True},
    ]}
    return L


# ===========================================================================
# 합성 사전 — 실제 사전과 같은 이름·모양(dictionaries[].entries[])
# ===========================================================================
def _e(name, canonical, synonyms=(), **kw):
    e = {"id": mkid("DIC", f"{name}|{canonical}"), "canonical": canonical, "sources": [{"file": "synthetic", "path": "synthetic", "n": 1, "kind": "value"}],
         "synonyms": [s if isinstance(s, dict) else {"value": s, "link": "synthetic", "sources": []} for s in synonyms], "definition": None}
    e.update(kw)
    return e


_ERD = None


def _erd():
    """시맨틱 층(erd-v3.1.json) — 규칙 데이터의 값 목록(조직층 · 수식 값 · 수식어 목록)은 ERD 정의라 합성 사전·시험에도 그대로 쓴다."""
    global _ERD
    if _ERD is None:
        with open(ERD_PATH, encoding="utf-8") as f:
            _ERD = json.load(f)
    return _ERD


def dictionaries():
    D = []

    def add(name, entries, kind="value"):
        D.append({"name": name, "label": name, "kind": kind, "entries": entries, "canonical_count": len(entries), "synonym_count": sum(len(x["synonyms"]) for x in entries), "candidates": []})

    code = lambda v: {"value": v, "link": "code", "sources": []}  # noqa
    add("modality", [_e("modality", "알파톡신", [code("M1"), "알파", "알파톡"], code="M1"), _e("modality", "베타필러", [code("M2"), "베타"], code="M2"),
                     _e("modality", "감마레이저", [code("M3"), "감마"], code="M3")])
    add("problem", [_e("problem", "주름고민", [code("P1")], code="P1")])
    add("site", [_e("site", "이마", ["forehead"], site_kind="backbone", zone_id="forehead", kind="anatomical"),
                 _e("site", "미간", [], site_kind="backbone", zone_id="glabella", kind="anatomical"),
                 _e("site", "턱", [], site_kind="taxonomy_site_label", kind="anatomical"),
                 _e("site", "볼", [], site_kind="taxonomy_site_label", kind="anatomical"),
                 _e("site", "얼굴", [], site_kind="taxonomy_site_label", kind="region"),
                 ] + [_e("site", v, [], site_kind="layer", kind="layer") for v in _erd()["tuple_rules"]["adverse"]["site_layers"]])
    add("technique", [_e("technique", "injection", ["주사", "주사법"]), _e("technique", "thermal", ["열"]), _e("technique", "regenerative"), _e("technique", "regeneration")])
    for nm, vals in [("severity", ["mild", "moderate", "severe", "critical"]), ("reaction_level", ["normal", "abnormal", "caution", "emergency"]), ("pih_risk_level", ["low", "moderate"]),
                     ("interaction_level", ["caution"]), ("condition_level", ["absolute", "relative", "consent", "must_check", "unspecified"]), ("synergy_type", ["함께", "다음에", "대신"]),
                     ("package_tier", ["basic"]), ("period", ["1일"]), ("phase_label", ["직후"]), ("evidence_level", ["A"]), ("rule_priority", ["높음"]), ("consensus", ["강"]),
                     ("accuracy_rubric", ["5"]), ("anesthesia", ["없음"]), ("position", ["누움"]), ("floor_phase", ["주입"]), ("session_phase", ["준비"]), ("modality_group", ["주사", "장비"]),
                     ("source_type", ["교과서"]), ("nerve_type", ["motor"]), ("danger_level", ["2", "3"]), ("purpose_label", ["리프팅"]), ("country", ["한국", "미국", "일본", "독일"]),
                     ("ingredient_material", ["HA"]), ("product_type", ["장비"]), ("age_group", ["30대"]), ("pain_scale", ["1"]), ("frequency_class", ["common", "uncommon", "serious", "emergency", "long_term"]),
                     ("license_status", ["정상", "확인 불가", "미허가"]), ("license_kind", ["의약품"]), ("license_state", ["정상"])]:
        add(nm, [_e(nm, v) for v in vals])
    add("concern_severity", [_e("concern_severity", "경미", ["경미 (fine)"]), _e("concern_severity", "중등")])
    add("product_tier", [_e("product_tier", "국산"), _e("product_tier", "수입")])
    add("unit", [_e("unit", "1회"), _e("unit", "2cc"), _e("unit", "KRW")])
    add("manufacturer", [_e("manufacturer", "가나제약", ["가나"]), _e("manufacturer", "다라제약"), _e("manufacturer", "마바제약/사아제약")])
    add("problem_subcategory_label", [_e("problem_subcategory_label", "이마", [code("P1-1")], code="P1", subcategory_id="P1-1", is_site=True),
                                      _e("problem_subcategory_label", "잔주름", [code("P1-2")], code="P1", subcategory_id="P1-2", is_site=False)])
    add("product_name", [_e("product_name", "알파원", ["AlphaOne"], code="M1"), _e("product_name", "알파투", ["AlphaTwo"], code="M1"),
                         _e("product_name", "알파톡", ["AlphaTok"], code="M1"), _e("product_name", "알파쓰리", [], code="M1"),
                         _e("product_name", "베타원", ["BetaOne"], code="M2"), _e("product_name", "감마원", ["GammaOne"], code="M3"),
                         _e("product_name", "감마투", [], code="M3"), _e("product_name", "공용원", [], code="M1|M2"), _e("product_name", "알파원 HB+", [], code="M1")], kind="entity_name_index")
    add("modality_subcategory_label", [_e("modality_subcategory_label", "주름알파", [code("M1-1")], code="M1"), _e("modality_subcategory_label", "턱알파", [code("M1-2")], code="M1"),
                                       _e("modality_subcategory_label", "볼륨베타", [code("M2-1")], code="M2"), _e("modality_subcategory_label", "토닝감마", [code("M3-1")], code="M3"),
                                       _e("modality_subcategory_label", "감마투", [code("M3-2")], code="M3")],
        kind="entity_name_index")
    names = {}
    for m in ledger()["taxonomy.json"]["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                names.setdefault(it["name"], []).append(m["id"])
    add("catalog_item_name", [_e("catalog_item_name", n, [], code="|".join(c)) for n, c in names.items()], kind="entity_name_index")
    add("adverse_event_type", [_e("adverse_event_type", "멍", ["타박상"], category="국소 일시 반응"), _e("adverse_event_type", "부종", ["붓기"], category="국소 일시 반응"),
                               _e("adverse_event_type", "색전", [], category="혈관"), _e("adverse_event_type", "괴사", [], category="혈관"),
                               _e("adverse_event_type", "통증", [], category="국소 일시 반응"), _e("adverse_event_type", "감염", [], category="염증/감염"),
                               _e("adverse_event_type", "과민반응", ["아나필락시스"], category="전신")])
    add("course", [_e("course", "미상"), _e("course", "일시", ["일시적"]), _e("course", "지연", ["지연성"]), _e("course", "영구")])
    add("relative_site", [_e("relative_site", "주사 부위", ["주입 부위"])])
    add("adverse_qualifier", [_e("adverse_qualifier", v, kind="기전" if v.endswith("성") else "물질") for v in _erd()["tuple_rules"]["adverse"]["qualifier_values"]])
    # v3.1(V3.1-4) 조건 사전 — 원장 사람 조건 이름의 조각(kind 는 그 값이 나타난 원장 키에서)
    add("person_condition", [_e("person_condition", "임신", kind="condition|check", kinds=["condition", "check"]), _e("person_condition", "알레르기", kind="check", kinds=["check"]),
                             _e("person_condition", "30대", kind="age_group", kinds=["age_group"]), _e("person_condition", "가상 상대 금기", ["가상상대금기"], kind="condition", kinds=["condition"])])
    # v3.1(V3.1-10) 문구 사전 — 분해가 쓰는 색인(빌드가 채운다)
    D.append({"name": "phrase_dictionary", "label": "안전 문구 사전", "kind": "phrase_index", "entries": [], "canonical_count": 0, "synonym_count": 0, "candidates": [], "removed_synonyms": [], "removed_entries": []})
    return {"erd_version": "v3.1", "synthetic": True, "dictionaries": D}


# ===========================================================================
# workspace
# ===========================================================================
class Workspace:
    """합성 입력 한 벌 — 결정·원장을 바꿔 가며 빌드한다."""

    def __init__(self, root=None, L=None, dic=None, hashes=True, changelog=True, erd_path=None, erd_patch=None):
        self.erd_path = erd_path or ERD_PATH
        self.erd_patch = erd_patch
        self.root = root or tempfile.mkdtemp(prefix="silver-conf-", dir=os.environ.get("SILVER_TEST_TMP"))
        self.bronze = os.path.join(self.root, "bronze")
        self.step1 = os.path.join(self.root, "step1-products.json")
        self.erd = os.path.join(self.root, "erd-v3.1.json")
        self.dict = os.path.join(self.root, "erd-v3.1-dictionaries.json")
        self.decisions = os.path.join(self.root, "decisions")
        self.out = os.path.join(self.root, "out")
        os.makedirs(self.bronze, exist_ok=True)
        os.makedirs(self.decisions, exist_ok=True)
        self.L = L if L is not None else ledger()
        self.dic = dic if dic is not None else dictionaries()
        self.write_inputs(hashes=hashes, changelog=changelog)

    @staticmethod
    def _dump(path, obj):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)

    def write_inputs(self, hashes=True, changelog=True):
        for f in LEDGER_FILES:
            self._dump(os.path.join(self.bronze, f), self.L[f])
        self._dump(self.step1, self.L["step1-products.json"])
        if hashes:
            self.write_hashes()
        if changelog:
            with open(os.path.join(self.bronze, "CHANGELOG.md"), "w", encoding="utf-8") as fh:
                fh.write("# 합성 원장 변경 이력\n\n| 판 | 날짜 | 바탕 | 변경 | 누가 |\n|---|---|---|---|---|\n| 1 | 2026-01-01 | 합성 | 없음 | — |\n| 2 | 2026-01-02 | 1판 | 합성 변경 | 시험 |\n")
        erd = json.load(open(self.erd_path, encoding="utf-8"))
        if self.erd_patch:
            self.erd_patch(erd)   # 시험용 규칙 데이터 바꾸기(예: 장비 계열을 합성 계열로)
        with open(self.step1, "rb") as fh:
            h = _sha(fh.read())
        for s in erd["source_files"]:
            if s["kind"] == "research_artifact":
                s["sha256"] = h
            else:
                with open(os.path.join(self.bronze, s["file"]), "rb") as fh:
                    s["sha256"] = _sha(fh.read())
        self.erd_obj = erd
        self._dump(self.erd, erd)
        if erd.get("erd_version") == "v3.3":
            self.dic = dict(self.dic, erd_version="v3.3")
            for d in self.dic["dictionaries"]:
                if d["name"] == "adverse_event_type":
                    d["entries"] = [{k: v for k, v in e.items() if k != "category"} for e in d["entries"]]   # V3.3-E
        self._dump(self.dict, self.dic)
        # ERD 실측(erd-v3-tuples.json) 자리 — 합성 원장에는 실측이 없다(report 의 대조 표만 빈다)
        self._dump(os.path.join(self.root, "none-tuples.json"), {"procedure": {"summary": {}, "tuples": [], "catalog": []}, "adverse": {"summary": {}, "tuples": [], "complications": [], "phrase_dictionary": [], "edges": []},
                                                                 "condition": {"summary": {}, "units": []}})

    def write_hashes(self, override=None):
        lines = []
        for f in LEDGER_FILES:
            with open(os.path.join(self.bronze, f), "rb") as fh:
                h = _sha(fh.read())
            lines.append(f"{(override or {}).get(f, h[:16])} {f}")
        with open(os.path.join(self.bronze, "HASHES.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def add_decisions(self, decs, folder="t"):
        d = os.path.join(self.decisions, folder)
        os.makedirs(d, exist_ok=True)
        for x in decs:
            self._dump(os.path.join(d, f"{x['id']}.json"), x)

    def args(self, **kw):
        a = SimpleNamespace(bronze=self.bronze, step1=self.step1, erd=self.erd, dict=self.dict, colmap=COLMAP_PATH, tuples=os.path.join(self.root, "none-tuples.json"),
                            tuples_prev=None, decisions=self.decisions, out=self.out, baseline=os.path.join(self.root, "baseline", "manifest-1차.json"), bootstrap=False, propose=False,
                            kiwi_cache=os.path.join(self.root, "kiwi-cache.json"), kiwi_python=None)   # v3.3 합성 빌드: 분석기 캐시는 워크스페이스 안(정본 캐시를 더럽히지 않는다 · venv 로 채운다)
        for k, v in kw.items():
            setattr(a, k, v)
        return a

    def build(self):
        from lib import pipeline
        return pipeline.run(self.args())

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


def dec(id_, kind, target, new_value, decided_at="2026-02-01", status="approved", **kw):
    d = {"id": id_, "kind": kind, "target": target, "new_value": new_value, "reason": "합성 시험", "decided_by": "시험" if status == "approved" else None,
         "decided_at": decided_at, "status": status, "source_refs": [{"kind": "ledger", "ref": "taxonomy.json:modality[].id@0"}]}
    d.update(kw)
    return d


def log_of(S, did):
    return [x for x in S.apply_log if x["id"] == did]


def ref_anchor(label, hint):
    return mkid("REF", f"{label}|{hint}")


def cat_id(fam, name):
    return mkid("CAT", f"{fam}|{name}")
