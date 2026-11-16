# -*- coding: utf-8 -*-
"""ERD v3.3 잎 키 행선지 규칙. v3.2(erd_colmap_v32.py) 위에 A~G 가 닿는 행의 **비고만** 바꾼다 — 행선지·표적 이동 0(개체·관계 신설은 구성품(R36)뿐이고 그 원장 칸은 없다).
  비고만(NOTE_CHANGES_V33): synergy from/to(G 3판 정식 이름) · taxonomy items[].name(G M8-6 항목 2 · A 구성품 칸 없음) · complications name(C R2 사전 값 · E category 삭제) · safety 칸(B 분석기 · E 분류는 frequency_class) ·
                          complications severity(E 분류는 원장 값) · anatomy zones name_ko · vessels[].danger(C 부위 동맥·정맥·안동맥) · products ingredient/material(F 설계안 참고) · taxonomy problem label(C 승인 씨앗 15 는 결정 레코드)
  미래 칸(FUTURE_COLUMNS_V33 · A): 원장에 없는 구성품 칸 — 1,072 행에 들지 않고 별도 절로 표기.
COLMAP · MOVES*(이전 판) · MOVES_V33(=[]) · NOTE_CHANGES_V33 · FUTURE_COLUMNS_V33 · resolve 를 노출한다. erd_build_v33.py 가 읽는다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v32 as V32  # noqa
import erd_spec_v33 as S33  # noqa

COLMAP = {f: list(rows) for f, rows in V32.COLMAP.items()}
MOVES, MOVES_V22, MOVES_V23, MOVES_V24, MOVES_V3, MOVES_V31, MOVES_V32 = list(V32.MOVES), list(V32.MOVES_V22), list(V32.MOVES_V23), list(V32.MOVES_V24), list(V32.MOVES_V3), list(V32.MOVES_V31), list(V32.MOVES_V32)
NOTE_CHANGES_V32 = list(V32.NOTE_CHANGES_V32)
SCRUBBED_V32 = list(V32.SCRUBBED_V32)
MOVES_V33 = []
NOTE_CHANGES_V33 = []
FUTURE_COLUMNS_V33 = list(S33.FUTURE_COLUMNS_V33)


def _find_(file, path):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            return i, r
    for r in rows:
        if not isinstance(r[0], str) and r[0].match(path):
            return None, r
    raise KeyError(f"{file} {path}")


def _note(file, path, suffix):
    i, r = _find_(file, path)
    new = (path, r[1], r[2], (r[3] + " · " if r[3] else "") + suffix)
    if i is None:
        COLMAP[file].insert(0, new)
    else:
        COLMAP[file][i] = new
    NOTE_CHANGES_V33.append((file, path, r[2], suffix))


# ---- G 원장 3판
for k in ("from", "to"):
    _note("synergy.json", f"links[].{k}", "v3.3(V3.3-G · 3판): 줄임말 18종 59자리 → taxonomy 정식 이름(「Mxx-」 접두 제거 · 부위는 「이름 부위」 · README 규칙 2) — §1.3 분해가 접두 없이 정식 이름에 닿는다 · 남은 「Mxx-」 접두 자리는 4판 후보(사용자)")
_note("taxonomy.json", "modality[].subcategories[].items[].name", "v3.3(V3.3-G · 3판): M8-6 기타 항목 2 신설(저출력레이저(LLLT) · 다이오드 레이저 · name 만) → 분류 항목 523 · v3.3(V3.3-A): 구성품(팁·카트리지 …)은 이 칸의 값이 아니다 — 원장 칸 없음 · 미래 칸(아래 절)")
# ---- C 사건 사전 값에도 R2 · 부위 3 · E category 삭제
_note("complications.json", "categories[].complications[].name", "v3.3(V3.3-C): 사전 값 「혈관 폐색」은 사건 폐색 + 부위 혈관(R2 를 사전 값에도 · 분해 꼴 raw_variant) · 폐색 ≠ 색전 · v3.3(V3.3-E): 사건 사전 category 없음 — 분류는 severity(이 레코드) · frequency_class · course 만")
_note("complications.json", "categories[].complications[].severity", "v3.3(V3.3-E): 부작용 분류는 원장 값만 — 이 severity(R15 속성) · taxonomy/extracted safety 칸(frequency_class) · R15 course. ERD v2 의 category 7분류는 삭제")
for f, p in V32._SAFETY:
    _note(f, p, "v3.3(V3.3-B): 토큰화는 형태소 분석기(kiwipiepy 0.24 · 사전 값 사용자 단어) 품사로 — 목록은 보조 · v3.3(V3.3-E): 칸 이름(common/uncommon/serious)이 분류(frequency_class) · 사건 사전 category 없음")
_note("anatomy-danger-zones.json", "zones[].vessels[].danger", "v3.3(V3.3-C(2)): site 사전 layer 값 동맥·정맥·안동맥(parent 혈관/동맥 · 사용자 승인 11-06)의 출처 후보 자리 — locator 는 실측 §9.20")
_note("anatomy-danger-zones.json", "zones[].name_ko", "v3.3(V3.3-C(2)·(4)): site 사전에 동맥·정맥·안동맥 추가(ERD 값 · parent) · 승인 씨앗 부위 15 는 ERD 값이 아니라 결정 레코드(dictionary_add · 8차 적용)")
_note("taxonomy.json", "problem[].subcategories[].label", "v3.3(V3.3-C(4)): 승인 씨앗 부위 15(눈밑·눈꺼풀·코끝·목주름·얼굴 전체·바디 전체·복부·옆구리·팔뚝·허벅지·종아리·힙·가슴·겨드랑이·두피)는 결정 레코드(dictionary_add · 8차) — ERD 사전 값 아님")
# ---- F 설계안 참고(값 변경 없음)
for f, p in (("products.json", "biostimulator.products[].ingredient"), ("products.json", "skin_booster.products[].ingredient"), ("products.json", "thread_lift.products[].material")):
    try:
        _note(f, p, "v3.3(V3.3-F): 「무엇을·어떻게 세분」 묶음 설계안(성분·소모품·실 재질/형태·깊이·세기)의 원장 근거 자리 — 어느 안도 적용하지 않음 · 승인 씨앗 성분 6(HA·히알루론산·TCA·글리콜산·살리실산·페놀)은 결정 레코드(8차)")
    except KeyError:
        pass


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
