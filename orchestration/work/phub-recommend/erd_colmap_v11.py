# -*- coding: utf-8 -*-
"""ERD v1.1 잎 키 행선지 규칙. v1 규칙(erd_colmap.py) 위에 A·C 변경분만 덧씌우고 step1-products.json(499 잎) 을 추가한다.
각 항목: (path 또는 regex, dest, target, note) · dest ∈ 개체 / 사전 / 엣지 / 브론즈 / 버림
"""
import copy
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap as V1  # noqa

COLMAP = {f: list(rows) for f, rows in V1.COLMAP.items()}


def _replace(file, path, dest, target, note):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            rows[i] = (path, dest, target, note)
            return
    raise KeyError(f"{file} {path}")


# ---- A. 8-2 cc_group / 8-4 기법 사전
_replace("problem-packages.json", "problems[].complaints[].cc_group", "사전", "dict:problem_subcategory_label",
         "8-2 처분: (problem_id, label) 로 고민 하위분류 결합(R7). 부위 라벨 10 은 dict:site 동의어에도 · complaint.cc_group_raw 원문")
_replace("taxonomy.json", "problem[].subcategories[].label", "개체", "problem_subcategory.label",
         "= 사전 problem_subcategory_label 정준값. 부위 라벨 10 만 부위 사전(R11)")
_replace("taxonomy.json", "modality[].subcategories[].label", "개체", "modality_subcategory.label", "8-4 처분: 기법 사전 아님 — 하위분류 개체로만")
_replace("products.json", "energy_device.products[].type", "사전", "dict:product_type", "8-4 처분: 기법 사전 아님 — 제품 유형 사전만")
_replace("pih-risk.json", "procedures[].subcategory", "엣지", "R15.subcategory_label", "8-4 처분: 하위분류 label 정규화 일치 시 하위분류 연결, 아니면 라벨만")
_replace("procedure-profiles.json", "profiles[].mechanism[]", "사전", "dict:technique", "R5 — 기법 사전의 유일한 출처(8-4)")

# ---- C. step1-products.json (조사 산출물) — 설계·식별자는 브론즈, 제품 속성의 출처 키만 개체/사전
S1 = "step1-products.json"
_s1 = [
    ("version", "개체", "source_file.version", "파일 메타"),
    ("generated_at", "개체", "source_file.updated", "파일 메타(생성일 2026-10-28, 조사 10-29 판)"),
    ("scope", "개체", "source_file.description", "파일 메타"),
    (re.compile(r"^basis\..*"), "브론즈", "bronze", "step1 작업 근거 메타(결정·조사 파일 목록) — 설계"),
    (re.compile(r"^summary\..*"), "브론즈", "bronze", "파일 수준 집계값 — 실버는 항목 단위에서 재계산"),
    (re.compile(r"^shared_license\[\]\..*"), "브론즈", "bronze", "라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서"),
    (re.compile(r"^lines\..*"), "브론즈", "bronze", "제품 라인 설계(라인명 키) — 설계라 들이지 않음"),
    (re.compile(r"^open\[\]\..*"), "브론즈", "bronze", "step1 열린 질문 — 작업 상태"),
    # items — 식별자·설계
    ("items[].ledger_id", "개체", "product.aliases", "step1 ledger_id 는 alias 로만(product.survey_ledger_id)"),
    ("items[].segment", "브론즈", "bronze", "step1 작업 구간 — 설계"),
    ("items[].source", "브론즈", "bronze", "step1 행 출처 구분(ledger/site_device/…) — 설계"),
    ("items[].active", "브론즈", "bronze", "step1 활성 플래그 — 작업 상태"),
    ("items[].gate", "브론즈", "bronze", "step1 게이트 메모 — 작업 상태"),
    ("items[].change_vs_draft", "브론즈", "bronze", "step1 초안 대비 변경 메모 — 작업 상태"),
    ("items[].note", "개체", "product.survey_note", "조사 메모(신뢰 3)"),
    ("items[].open[]", "브론즈", "bronze", "step1 열린 질문 — 작업 상태"),
    ("items[].open", "브론즈", "bronze", "빈 배열 365"),
    ("items[].family.code", "엣지", "R4.from(modality)", "계열 힌트(M코드일 때만). `현장 기기`·`원천 항목 없음` = 계열 없음"),
    ("items[].family.name", "브론즈", "bronze", "`M코드 계열명 · 하위분류` 합성 — 계열은 code 로 확정"),
    (re.compile(r"^items\[\]\.1_identity\..*"), "브론즈", "bronze", "step1 1_identity(종류·근거) — 설계. ERD 에 들이지 않음(C)"),
    # 2_names
    ("items[].2_names.display_name", "개체", "product.survey_names", "대표 이름(alias). 원장 대응은 B 분해 규칙으로만"),
    ("items[].2_names.ledger_name", "개체", "product.survey_names", "원장 표기 이름(alias). null 2 = 미입력"),
    ("items[].2_names.search_names[].name", "개체", "product.survey_names", "검색 이름(alias, 신뢰 3)"),
    ("items[].2_names.search_names[].lang", "개체", "product.survey_names", "이름 언어(한/영)"),
    ("items[].2_names.search_names", "개체", "product.survey_names", "빈 배열 120 = null ⑤"),
    ("items[].2_names.name_basis[]", "브론즈", "bronze", "이름별 근거 문장 — 조사 메모"),
    ("items[].2_names.ledger_maker_texts[]", "브론즈", "bronze", "원장 업체 표기 원문(오기 포함) — 제조사 사전 일치 자동 아님"),
    # 4_license
    ("items[].4_license.status", "사전", "dict:license_status", "product.license_status. 「확인 불가」도 값 그대로"),
    ("items[].4_license.kind", "사전", "dict:license_kind", "product.license_kind. null 140 = 미입력"),
    ("items[].4_license.reason", "브론즈", "bronze", "판정 사유 문장 — 판정"),
    ("items[].4_license.recommendable", "브론즈", "bronze", "step1 추천 가능 판정 — 다음 실버 빌드 결정 후보, ERD 속성 아님"),
    ("items[].4_license.license_basis", "브론즈", "bronze", "허가 연결 근거 메모"),
    ("items[].4_license.licenses", "개체", "product.licenses", "빈 배열 189 = null ⑤"),
    ("items[].4_license.licenses[].state", "사전", "dict:license_state", "product.licenses.state (허가 건 상태)"),
    ("items[].4_license.licenses[].kind", "사전", "dict:license_kind", "product.licenses.kind"),
    (re.compile(r"^items\[\]\.4_license\.licenses\[\]\.kpic\..*"), "개체", "product.licenses.kpic.*", "KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3)"),
    (re.compile(r"^items\[\]\.4_license\.licenses\[\]\.(.+)$"), "개체", "product.licenses.*", "허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3"),
    ("items[].4_license.history", "개체", "product.license_history", "빈 배열 335 = null ⑤"),
    ("items[].4_license.history[].state", "사전", "dict:license_state", "product.license_history.state (취소·취하·만료)"),
    ("items[].4_license.history[].kind", "사전", "dict:license_kind", "product.license_history.kind"),
    (re.compile(r"^items\[\]\.4_license\.history\[\]\.kpic\..*"), "개체", "product.license_history.kpic.*", "키 이름 보존"),
    (re.compile(r"^items\[\]\.4_license\.history\[\]\.(.+)$"), "개체", "product.license_history.*", "취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다"),
    ("items[].4_license.reference", "브론즈", "bronze", "빈 배열 300"),
    (re.compile(r"^items\[\]\.4_license\.reference\[\]\..*"), "브론즈", "bronze", "참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음"),
    (re.compile(r"^items\[\]\.4_license\.unlinked_use_mismatch\[\]\..*"), "브론즈", "bronze", "용도 불일치로 연결 안 한 허가 — 후보"),
    (re.compile(r"^items\[\]\.4_license\.queries_emedi\[\]\..*"), "브론즈", "bronze", "emedi 질의 로그 — 조사 과정"),
    ("items[].4_license.queries_emedi[].name_hits", "브론즈", "bronze", "빈 배열"),
    (re.compile(r"^items\[\]\.4_license\.approval\..*"), "브론즈", "bronze", "코디 검수 승인 기록 — 작업 상태"),
    ("items[].4_license.distribution_sources[].url", "개체", "citation.url", "kind=url(유통 근거 가격표) → 제품 R19"),
    ("items[].4_license.distribution_sources[].text", "개체", "citation.text", "유통 근거 설명"),
    # 5_spec
    ("items[].5_spec", "브론즈", "bronze", "null 5 = 미입력"),
    ("items[].5_spec.license", "개체", "product.spec", "null 51 = 미입력"),
    ("items[].5_spec.license[]", "개체", "product.spec", "문자열형 2 — 규격 문장 원문(③ 분해는 실버 빌더)"),
    (re.compile(r"^items\[\]\.5_spec\.license\[\]\..*"), "개체", "product.spec.*", "허가 기준 포장단위·함량 — 키 이름 보존"),
    (re.compile(r"^items\[\]\.5_spec\.license_spec\[\]\..*"), "개체", "product.spec.*", "허가 키 기준 규격 — 키 이름 보존"),
    ("items[].5_spec.license_spec", "개체", "product.spec", "빈 배열 117 = null"),
    (re.compile(r"^items\[\]\.5_spec\.history_license\[\]\..*"), "브론즈", "bronze", "취소 이력 허가의 규격 — 이력 허가는 product.license_history 로 충분"),
    (re.compile(r"^items\[\]\.5_spec\.market(_pricing)?(\[\]\..*)?$"), "브론즈", "bronze", "market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items)"),
    ("items[].5_spec.note", "브론즈", "bronze", "규격 메모"),
    ("items[].5_spec.rule_note", "브론즈", "bronze", "규격 규칙 메모"),
    ("items[].5_spec.license_pack", "브론즈", "bronze", "`해당 없음(의료기기 장비 …)` 설명 문장"),
    ("items[].5_spec.content", "브론즈", "bronze", "`해당 없음(장비)` 설명 문장"),
    ("items[].5_spec.license_unlinked_note", "브론즈", "bronze", "메모"),
    # 6_companies
    (re.compile(r"^items\[\]\.6_companies\.(manufacturer|importer|seller|license_holder|other)\[\]\.(name|basis|original|role|period)$"), "개체", "product.companies.*", "역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로"),
    ("items[].6_companies.license_holder", "개체", "product.companies", "빈 배열 393 = null"),
    ("items[].6_companies.other", "개체", "product.companies", "빈 배열 391 = null"),
    ("items[].6_companies.conflicts", "개체", "conflict", "빈 배열 384 = 충돌 없음(명시적 빈 목록)"),
    (re.compile(r"^items\[\]\.6_companies\.conflicts\[\]\..*"), "개체", "conflict.values", "kind=value_conflict(허가 값 vs 다른 출처) — 「덮어쓰지 않음」 그대로"),
    (re.compile(r"^items\[\]\.6_companies\.company_search_names\[\]\..*"), "브론즈", "bronze", "회사 검색 이름(오기 포함) — 조사 과정"),
    # 7_site_use
    ("items[].7_site_use", "브론즈", "bronze", "null 5"),
    (re.compile(r"^items\[\]\.7_site_use\..*"), "브론즈", "bronze", "현장 사진 연결 — ERD 범위 밖(사진 자산은 별도)"),
    # evidence
    ("items[].evidence", "브론즈", "bronze", "빈 배열 87"),
    ("items[].evidence[]", "브론즈", "bronze", "문자열형 근거(질의 로그)"),
    ("items[].evidence[].urls[]", "개체", "citation.url", "kind=url → 제품 R19"),
    (re.compile(r"^items\[\]\.evidence\[\]\.(type|detail|source)$"), "브론즈", "bronze", "조사 근거 메모(유형·설명·출처 문장)"),
    # 설계·식별자·작업 상태
    (re.compile(r"^items\[\]\.(dedup|line|recheck)\..*"), "브론즈", "bronze", "중복·라인·재탐색 설계/과정 — 들이지 않음"),
    (re.compile(r"^items\[\]\.(line_children|merged_from|merged_into|merged_ledger_ids|moved_note|moved_to|shared_license_with|use_mismatch|weak_link)(\[\])?$"), "브론즈", "bronze", "step1 식별자 설계(병합·이동·라인) — 들이지 않음"),
    (re.compile(r"^items\[\]\.taxonomy_product(_ids\[\]|\..*)$"), "브론즈", "bronze", "step1 이 적어 둔 taxonomy 제품 대응 — 원장 대응은 B 분해 규칙으로만 하므로 쓰지 않는다(C)"),
]
COLMAP[S1] = _s1


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
