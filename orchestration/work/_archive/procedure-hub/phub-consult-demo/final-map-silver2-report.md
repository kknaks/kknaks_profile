# 최종 매핑 v5 → silver 2차 → gold → 새 코드 → 매핑 JSON — 리포트(data 워커 · 2026-11-19)

> 브리프 `final-map-silver2-task.md` + 코디 답 4(11-19 · 전부 추천대로). 작업 사본 `silver-model/` 에서만 고쳤다. 허브 레포 · DB · stg 수정 0 · 커밋 0 · 서브에이전트 0.
> 공개 silver · gold 에서 병원 이름 grep 0 · 진료항목 코드 grep 0(324 코드 전부 대조). 「명동점」 은 로컬 근거 파일 `user.csv` basis 칸에만 있다.

## 1. 결과 한 줄

v5 324 줄(매핑 칸 빈칸 0 · 「허브 추가 필요」 0 · 코드 전부 새 silver 에 실재) · silver 2차(새 제품 21 · 회사 4 · 재료 1 · 시술 1 · 일반 케이스 73 · case_product +137) · **silver-check PASS(WARN 5) · gold-check PASS(FAIL 0 · WARN 10)** · `gold_hash` **d84e4b8e…** · `aux_hash` **1a8d2099…** · 매핑 JSON 324 항목 · 두 경로 git 무시 확인.

## 2. v5 상태별 수 (`reference/…/myeongdong-kos-medical-services-20261119.v5.csv` · v4 82 칸 + `상태`)

| 상태 | 줄 |
|---|---|
| 매핑됨 | 297 |
| 매핑됨(제품 확인 필요) | 8 |
| 허브 대상 아님(시술 해당 없음 — 마취 · 팩 · 수액 · 감초 · 혈액 줄기세포 · 회원권) | 13 |
| 시술 확인 필요 | **6** |
| 계 | 324 |

- 빈칸: 매핑 칸(허브 시술 코드 ~ 상태) 0. KOS 원문 칸(구성 용량 · 설명 등)의 빈칸 9,941 은 v4 와 같은 수(KOS 가 비워 준 값 — 손대지 않음).
- 재현: `reference/…/build_v5.py plan|fill`(PEEL_REP_CODE=PRC-503) → `build_mapping_json.py`.
- 적용한 결정(요약): 포트라 5 → PRC-007 + CAS-064 + 포트라 PRD-358 · KK주사 2 → PRC-120 · 엑소제 2 → PRC-122 · 필링 1종 선택 · 예스필 → **PRC-503 + CAS-5009**(코디 답 ① — PRC-503 에 부위 빈 기본 케이스 CAS-5009 가 이미 있어 새로 만들지 않음 · 새로 만들면 C3 중복) · 수액 3 · 감초 · 다이어트 · 트라마돌 · 혈액 줄기세포 → 해당 없음 · 필러 녹이는 주사 → 새 시술 PRC-130 필러 용해 + CAS-1045 + 히알라제 PRD-733 · 대표 제품(CO2 7 → PRD-315 · 엑소좀 → PRD-170 · 태반주사 → PRD-720 · 순수톡신 → PRD-008 · 스킨보톡스(제품명 없음) → 하이톡스 PRD-022) · 세라핏 배합 6 성분 → 「해당 없음(세라핏 배합 성분)」 · 26-CERAFIT-30 → 밀리핏주사 PRD-729 · 필링제 7 칸 · 아쿠아필링기 · 이온토 → 「해당 없음(…)」 · 리쥬란 힐러/HB → 규칙 R(A/B = 케이스 1 + 제품 2) PRD-151 + PRD-152.
- 케이스 규칙: 얼굴(1단 SITE-007) · 부위 없음 = **그 시술의 부위 빈 일반 케이스**(부위 · 조직 · 해부 · 세부 재료 · 방법 모두 빈 케이스 — 없으면 새로) · 그 밖 부위 = 시술 × 부위 케이스(없으면 새로) · v4 에 이미 코드가 있던 칸은 그대로.

### 남은 「확인 필요」

**시술 확인 필요 6 줄**(병원 확인): KS주사 2(26-KSJS-3CC · 26-KSJS-6CC) · 셀코어(26-SKBST-CLCR-5CC) · 이온자임 미백관리(26-MBGRJ-IONJ) · 라라젯(26-LALAJET) · 플래티넘PTT(26-ptt). 제품(인주셀 · 셀코어 · 이온자임 · 플래티넘PTT · 라라젯 PRD-662)은 코드가 있고 시술 · 케이스 칸만 「확인 필요」.

**제품 확인 필요 8 줄**(코디 답 ③ — 병원 질문 목록에): LED 재생레이저 「LED 기기」(26-LED) · 염증주사 「트리암」 2(26-JJSJSF-JJSTR · 26-JJSJSE-JJSTR-1QUANTITY) · 마늘주사 · 멀티비타민 · 백옥 · 신데렐라주사(26-SJS-MANE · MTBJS · BJS · SDRJS) · 얼굴필러 「수입」(26-PPSFL-IMPT-1CC). 시술 · 케이스 코드는 있음.

## 3. silver 바뀐 수(기준 `archive/silver-before-clinic-a-20261119-b2/` = 부위 묶음 뒤 · 끝 덧붙임만)

| 표 | 전 → 후 | + |
|---|---|---|
| product | 315 → 336 | 21 |
| organization | 202 → 206 | 4(수도그룹 · 대한뉴팜 · 트리시스 · 메딕콘) |
| material | 143 → 144 | 1(MAT-119 히알루로니다제) |
| procedure | 138 → 139 | 1(PRC-130 필러 용해) |
| procedure_material | 175 → 176 | 1 |
| procedure_case | 268 → 341 | 73 |
| case_product | 332 → 469 | 137 |
| product_organization | 575 → 590 | 15 |
| product_material | 390 → 398 | 8 |
| product_modality | 317 → 337 | 20(플래티넘PTT 는 계열 근거 없어 0) |
| alias | 992 → 993 | 1(procedure PRC-130 「필러 녹이는 주사」) |
| source_ref | 48,226 → 48,508 | 282(전부 `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>` · 근거 종류 「사용자 제공」) |
| 근거 파일 user.csv | 113 → 395 줄 | 282(basis 4 가지: 「사용자 결정 2026-11-19 · 명동점 진료항목」 / 「식약처 <허가번호 · 품목기준코드>」 / 「웹 확인(사용자 조사) · 식약처 허가 미확인」 / 「… · 식약처 허가 미확인」 · CAS-5009 ↔ 제품 줄은 「대표 시술 지정(사용자 11-19 · 필링 계열 대표)」 — 다만 필링 줄 제품은 해당 없음이라 실제 연결 0) |

- 그 밖 46 표 바이트 같음. 기존 행 수정 0(site 포함).
- 스크립트 `drafts/clinic-supplement/clinic-a-20261119/build_batch2.py`(입력 `batch2-input.json` — 병원 이름 · 진료항목 코드 없음 · `build_v5.py plan` 이 씀) · 출력 `new-codes.json` · `case-product-skipped.json`. 기준 사본에서 다시 돌려도 같은 바이트(직접 확인 + gold-check A3).
- 코드 대역: 기존 꼴(같은 계열 대역의 다음 번호) — 톡신 PRD-022 · 필러 083 · 콜라겐 129~131 · 스킨부스터/엑소 179~183 · 키트 205 · 레이저 357~358 · 니들RF 564 · 관리 장비 685~690 · 약제 733 · 케이스 CAS-096~ / 1045~ / 3045~ / 5082~.
- 생성 문서 다시 뽑음: `notes/silver-tables.md`(`--write-docs`) · `notes/vocabulary.csv`(`glossary-build.py` — **gold 빌드 뒤에** 다시 뽑아야 V1 통과: g_edge · g_node · g_profile · g_scope 의 evidence_kind 에 「사용자 제공」 이 새로 생김).

### 새 제품 21

| 코드 | 이름 | 종류 | 상위 | 이름 확인 | 식약처 |
|---|---|---|---|---|---|
| PRD-022 | 하이톡스 | 약제 | - | 확인 | true |
| PRD-083 | 레스틸렌아이라이트 | 필러 | PRD-051 | 웹·식약처 미확인 | - |
| PRD-129 | 쥬베룩스킨 | 콜라겐 자극 주사제 | PRD-105 | 확인 | true |
| PRD-130 | 올리디아120 | 콜라겐 자극 주사제 | PRD-110 | 확인 | true |
| PRD-131 | 올리디아365 | 콜라겐 자극 주사제 | PRD-110 | 확인 | true |
| PRD-179 | 하이주 | 스킨부스터 | - | 확인 | true |
| PRD-180 | 인주셀 | 스킨부스터 | - | 웹·식약처 미확인 | - |
| PRD-181 | 셀코어 | 스킨부스터 | - | 웹·식약처 미확인 | - |
| PRD-182 | 라쥬니스 | 줄기세포·엑소좀 제제 | - | 웹·식약처 미확인 | - |
| PRD-183 | 엑소제 | 줄기세포·엑소좀 제제 | - | 웹·식약처 미확인 | - |
| PRD-205 | 프로디젠 | 키트 | - | 웹·식약처 미확인 | - |
| PRD-357 | 피코라이트블랙 | 장비 | - | 확인 | true |
| PRD-358 | 포트라 | 장비 | - | 웹·식약처 미확인 | - |
| PRD-564 | 포텐자펌핑팁 | 장비 | PRD-550 | 확인 | true |
| PRD-685 | 소노케어 | 장비 | - | 웹·식약처 미확인 | - |
| PRD-686 | 오투덤 | 장비 | - | 웹·식약처 미확인 | - |
| PRD-687 | 울킨 | 장비 | - | 웹·식약처 미확인 | - |
| PRD-688 | 크라이오셀 | 장비 | - | 웹·식약처 미확인 | - |
| PRD-689 | 이온자임 | 장비 | - | 웹·식약처 미확인 | - |
| PRD-690 | 플래티넘PTT | 장비 | - | 웹·식약처 미확인 | - |
| PRD-733 | 히알라제 | 약제 | - | 확인 | true |

### 새 회사 · 재료 · 시술

- ORG-211 수도그룹
- ORG-212 대한뉴팜
- ORG-213 트리시스
- ORG-214 메딕콘
- MAT-119 히알루로니다제(hyaluronidase · 물질)
- PRC-130 필러 용해(계열 M2 · 원리 MEC-064 · 재료 MAT-119 · 다른 이름 「필러 녹이는 주사」 · overview/mechanism 빈칸 — 지어 넣지 않음)

### 새 일반 케이스 73(시술 × 부위 · 부위 빈칸 = 그 시술의 부위 빈 케이스)

| 케이스 | 시술 | 부위 |
|---|---|---|
| CAS-1045 | PRC-130 필러 용해 | (부위 빈) |
| CAS-096 | PRC-001 보톡스 | SITE-001 전신 |
| CAS-097 | PRC-001 보톡스 | SITE-039 비익 |
| CAS-098 | PRC-001 보톡스 | SITE-062 윗입술 |
| CAS-099 | PRC-001 보톡스 | SITE-124 앞허벅지 |
| CAS-100 | PRC-001 보톡스 | SITE-144 침샘 |
| CAS-101 | PRC-001 보톡스 | SITE-145 귀밑샘 |
| CAS-102 | PRC-001 보톡스 | SITE-146 턱밑샘 |
| CAS-103 | PRC-002 선택적 광열 레이저 | (부위 빈) |
| CAS-104 | PRC-002 선택적 광열 레이저 | SITE-013 하안면 |
| CAS-105 | PRC-002 선택적 광열 레이저 | SITE-014 이마 |
| CAS-106 | PRC-002 선택적 광열 레이저 | SITE-015 미간 |
| CAS-107 | PRC-002 선택적 광열 레이저 | SITE-051 볼 |
| CAS-108 | PRC-002 선택적 광열 레이저 | SITE-073 턱끝 |
| CAS-109 | PRC-002 선택적 광열 레이저 | SITE-075 턱선 |
| CAS-110 | PRC-002 선택적 광열 레이저 | SITE-077 턱밑 |
| CAS-111 | PRC-002 선택적 광열 레이저 | SITE-079 목 |
| CAS-112 | PRC-002 선택적 광열 레이저 | SITE-085 헤어라인 |
| CAS-113 | PRC-002 선택적 광열 레이저 | SITE-094 손등 |
| CAS-114 | PRC-002 선택적 광열 레이저 | SITE-101 팔뚝 |
| CAS-115 | PRC-002 선택적 광열 레이저 | SITE-103 허벅지 |
| CAS-116 | PRC-002 선택적 광열 레이저 | SITE-105 종아리 |
| CAS-117 | PRC-002 선택적 광열 레이저 | SITE-106 무릎 |
| CAS-118 | PRC-002 선택적 광열 레이저 | SITE-110 복부 |
| CAS-119 | PRC-002 선택적 광열 레이저 | SITE-130 베렛나루 |
| CAS-120 | PRC-002 선택적 광열 레이저 | SITE-131 하완 |
| CAS-121 | PRC-002 선택적 광열 레이저 | SITE-132 팔꿈치 |
| CAS-122 | PRC-002 선택적 광열 레이저 | SITE-133 손목 |
| CAS-123 | PRC-002 선택적 광열 레이저 | SITE-134 발목 |
| CAS-124 | PRC-002 선택적 광열 레이저 | SITE-135 뒷목 |
| CAS-125 | PRC-002 선택적 광열 레이저 | SITE-136 손가락 |
| CAS-126 | PRC-002 선택적 광열 레이저 | SITE-137 발가락 |
| CAS-127 | PRC-002 선택적 광열 레이저 | SITE-138 발등 |
| CAS-128 | PRC-002 선택적 광열 레이저 | SITE-139 유륜 |
| CAS-129 | PRC-006 IPL | (부위 빈) |
| CAS-130 | PRC-006 IPL | SITE-001 전신 |
| CAS-1046 | PRC-100 히알루론산 필러 | (부위 빈) |
| CAS-1047 | PRC-100 히알루론산 필러 | SITE-001 전신 |
| CAS-1048 | PRC-100 히알루론산 필러 | SITE-025 눈꺼풀 |
| CAS-1049 | PRC-100 히알루론산 필러 | SITE-026 안와상부 |
| CAS-1050 | PRC-100 히알루론산 필러 | SITE-109 엉덩이 |
| CAS-1051 | PRC-100 히알루론산 필러 | SITE-117 어깨 |
| CAS-1052 | PRC-100 히알루론산 필러 | SITE-143 쇄골 |
| CAS-1053 | PRC-103 PLLA | (부위 빈) |
| CAS-1054 | PRC-104 CaHA | (부위 빈) |
| CAS-1055 | PRC-110 PN주사 | (부위 빈) |
| CAS-1056 | PRC-116 PRP | SITE-051 볼 |
| CAS-1057 | PRC-120 줄기세포배양액 | (부위 빈) |
| CAS-1058 | PRC-122 줄기세포유래 엑소좀 | (부위 빈) |
| CAS-1059 | PRC-123 DCA 지방분해 주사 | (부위 빈) |
| CAS-1060 | PRC-123 DCA 지방분해 주사 | SITE-001 전신 |
| CAS-1061 | PRC-123 DCA 지방분해 주사 | SITE-051 볼 |
| CAS-1062 | PRC-123 DCA 지방분해 주사 | SITE-101 팔뚝 |
| CAS-1063 | PRC-123 DCA 지방분해 주사 | SITE-112 옆구리 |
| CAS-1064 | PRC-123 DCA 지방분해 주사 | SITE-115 브라라인 |
| CAS-1065 | PRC-123 DCA 지방분해 주사 | SITE-123 심부볼 |
| CAS-1066 | PRC-123 DCA 지방분해 주사 | SITE-125 허벅지 안 |
| CAS-1067 | PRC-123 DCA 지방분해 주사 | SITE-126 허벅지 밖 |
| CAS-1068 | PRC-123 DCA 지방분해 주사 | SITE-127 허벅지 승마 |
| CAS-1069 | PRC-123 DCA 지방분해 주사 | SITE-128 상복부 |
| CAS-1070 | PRC-123 DCA 지방분해 주사 | SITE-129 하복부 |
| CAS-1071 | PRC-123 DCA 지방분해 주사 | SITE-142 부유방 |
| CAS-3046 | PRC-311 HIFU | (부위 빈) |
| CAS-3047 | PRC-311 HIFU | SITE-019 눈 주변 |
| CAS-3048 | PRC-312 고주파 | (부위 빈) |
| CAS-3049 | PRC-312 고주파 | SITE-019 눈 주변 |
| CAS-3050 | PRC-312 고주파 | SITE-075 턱선 |
| CAS-3051 | PRC-313 마이크로웨이브 | (부위 빈) |
| CAS-3052 | PRC-313 마이크로웨이브 | SITE-001 전신 |
| CAS-3053 | PRC-316 니들RF | (부위 빈) |
| CAS-3054 | PRC-316 니들RF | SITE-001 전신 |
| CAS-5082 | PRC-547 초음파관리 | (부위 빈) |
| CAS-5083 | PRC-551 멀티니들 주입 | (부위 빈) |

### case_product 에 안 넣은 64(이미 product_procedure 로 시술에 닿는 제품 — 코디 답 ②(a))

- PRD-003 제오민 ×23: CAS-001 · CAS-002 · CAS-003 · CAS-004 · CAS-005 · CAS-006 · CAS-007 · CAS-009 · CAS-011 · CAS-012 · CAS-013 · CAS-015 · CAS-016 · CAS-017 · CAS-018 · CAS-019 · CAS-092 · CAS-097 · CAS-098 · CAS-099 · CAS-100 · CAS-101 · CAS-102
- PRD-008 코어톡스 ×21: CAS-001 · CAS-002 · CAS-003 · CAS-004 · CAS-005 · CAS-006 · CAS-007 · CAS-009 · CAS-011 · CAS-012 · CAS-016 · CAS-017 · CAS-018 · CAS-019 · CAS-092 · CAS-097 · CAS-098 · CAS-099 · CAS-100 · CAS-101 · CAS-102
- PRD-054 벨로테로 ×7: CAS-1005 · CAS-1006 · CAS-1009 · CAS-1044 · CAS-1046 · CAS-1048 · CAS-1049
- PRD-063 에피티크 ×4: CAS-1047 · CAS-1050 · CAS-1051 · CAS-1052
- PRD-066 셀레스텔라 ×2: CAS-1046 · CAS-1047
- PRD-104 래디어스 ×1: CAS-1054
- PRD-106 쥬베룩볼륨 ×1: CAS-1020
- PRD-152 리쥬란 HB+ ×1: CAS-1055
- PRD-160 스킨바이브 ×1: CAS-1026
- PRD-161 리바이브 ×1: CAS-1026
- PRD-164 힐로웨이브 ×1: CAS-1026
- PRD-170 셀엑소좀 ×1: CAS-1058

## 4. 검사 결과

### silver-check

```
F* · R* · D* · A* · C1~C12 · E* · O* · I* · S1 · S2 · V* · Q1 · N* · G1 · G2 : 통과
G3 : FAIL 0 · WARN 5   M .gitignore · M orchestration/config/projects/procedure-hub.json · M orchestration/work/README.md
                       · M para/projects/company/procedure-hub/work-index.md · ?? reference/2026-11-19-myeongdong-kos/
silver 해시 37716b4286d5a4b4791c7130798b34778409bb145a6573613a034fe7e97a2ffa
PASS (WARN 5)
```

### gold-build → gold-check

```
A1 · A2 · A3 · K1~K7 · M1 · V1 · Q1 · H1 · G1 : 통과
WARN A2 ×5 · G1 ×5   작업 사본 밖 변경(데이터 아님 — 부위 묶음 때와 같은 5 줄)
== FAIL 0 · WARN 10
PASS
```

- 첫 실행에서 V1 FAIL 1(값 목록을 gold 빌드 전에 뽑음) → gold 뒤 `glossary-build.py` 다시 → 통과. 순서 문제라 스크립트는 안 고쳤다.

### 고친 검사 스크립트(작업 사본 `gold/gold-check.py` 만 · 코디 답 ④ · 고치기 전 사본 `archive/scripts-before-batch2/`)

```diff
+B2 = os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119-b2')          # 묶음 2 기준 사본(부위 묶음 뒤)
+B2S = os.path.join(B2, 'silver')
+B2_APPEND = {f + '.csv' for f in ('product', 'organization', 'material', 'procedure', 'procedure_material', 'procedure_case', 'case_product',
+                                  'product_organization', 'product_material', 'product_modality', 'alias', 'source_ref')}
@@ a1() — 부위 묶음 규칙은 그대로 두고 대상만 SILVER → B2S(기준 1 → b2)
-        pa, pb = os.path.join(CLINIC_BASE, fn), os.path.join(SILVER, fn)
+        pa, pb = os.path.join(CLINIC_BASE, fn), os.path.join(B2S, fn)
-    new_site = … os.path.join(SILVER, 'site.csv') …   (new_ans · source_ref 대조도 같은 식으로 SILVER → B2S)
+    new_site = … os.path.join(B2S, 'site.csv') …
+    # 묶음 2: 기준 = b2 — 표마다 기준 바이트 + 끝 덧붙임만(B2_APPEND) · source_ref 덧붙임은 ref 머리 drafts/clinic-supplement/ 만 · 그 밖 표 바이트 같음
+    for fn in sorted(os.listdir(B2S)):
+        a, b = open(os.path.join(B2S, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
+        if fn in B2_APPEND:
+            if not b.startswith(a): bad('A1', f'묶음 2 {fn} 앞쪽(기존 행) 바이트가 바뀜')
+            elif fn == 'source_ref.csv':
+                for r in …덧붙인 행: if not r[3].startswith(CLINIC_REF): bad('A1', …)
+        elif a != b: bad('A1', f'묶음 2 {fn} 바뀜(덧붙임 허용 표 밖)')
@@ a3() — 사슬: 보강 + 부위 묶음 재현 → b2 와 대조 → 그 위 build_batch2 재현 → 지금 silver · user.csv 와 대조
-            if … != open(os.path.join(SILVER, fn), 'rb').read(): bad('A3', f'silver {fn} 재현 다름(보강 + 묶음)')
-        if … != open(…/'user.csv') …: bad('A3', '묶음 근거 파일 user.csv 재현 다름')
+            if … != open(os.path.join(B2S, fn), 'rb').read(): bad('A3', f'silver {fn} 재현 다름(보강 + 묶음 → 기준 b2)')
+        if … != open(os.path.join(B2, 'user.csv'), 'rb').read(): bad('A3', '… 재현 다름(기준 b2)')
+        out3 = os.path.join(tmp, 'batch2')
+        subprocess.run([sys.executable, …/'build_batch2.py', B2S, os.path.join(B2, 'user.csv'), out3], check=True, …)
+        for fn in sorted(os.listdir(os.path.join(out3, 'silver'))):
+            if … != open(os.path.join(SILVER, fn), 'rb').read(): bad('A3', f'silver {fn} 재현 다름(묶음 2)')
+        if open(os.path.join(out3, 'user.csv'), 'rb').read() != …지금 user.csv: bad('A3', '… 재현 다름(묶음 2)')
```

silver-check · gold-build 는 안 고쳤다(근거 종류 식 · 경로는 부위 묶음 때 것 그대로).

## 5. gold · 해시

| 파일 | 행 전 → 후 |
|---|---|
| g_entry | 2680 → 2704(+24 = 새 제품 21 · 시술 1 · 별칭 1 · 재료 1 — 회사는 입구 아님) |
| g_profile | 739 → 834(+95 = 케이스 73 · 제품 21 · 시술 1) |
| g_scope | 4202 → 4882 |
| g_indication | 4866 → 5839(**+973 전부 reach 「제품 경유」** — 새 case_product 로 제품의 적응이 그 케이스 시술 후보로 닿음) |
| g_node · g_edge | 1545 → 1639 · 10389 → 10974 |
| g_evidence | 27779 → 29823 |
| questions | 37 → 37(행 같음 · 시범 답 글 일부가 새 후보로 바뀜 — Q1 통과) |
| 나머지 8 표 | 바이트 같음 |

- `gold_hash` **ece5d2be… → d84e4b8e0ff0feb30533195d759e4ac9c3116017a22f9429447718420978268d**(허브 `inputs.py` 식 — 이전 값 재현 확인)
- `aux_hash` **e0813c0a… → 1a8d2099182f5fd271e8dcebd15fff9f44aeba93be4e404b6d86390952a95187**(source_ref 만 바뀜)
- 영향: 상담 시 고민 → 시술 후보에 「제품 경유」 후보가 늘어난다(예 Q06 · Q08 답 글). 허브 반입 전 전후 비교에서 볼 자리.

## 6. 매핑 JSON

- `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/data/kos/myeongdong-mapping-20261119.json` · `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261119.json`(같은 바이트 · 메인 로컬은 `data/kos/` 폴더 만들고 파일 하나만 복사 — 다른 것 안 건드림 · `git status` 변화 0)
- 두 경로 `git check-ignore` → `.gitignore:8 data/` 로 무시됨.
- items **324**(status 매핑됨 318 · 시술 확인 필요 6 · note: 허브 대상 아님 13 · 제품 확인 필요 8) · groups **131**(KOS 시술별) · 제품 연결 295 · meta 해시 = §5 새 값.
- 가격 · KOS id(uuid) 0(grep). case_product 에 안 넣은 64 짝도 JSON 에는 케이스 + 제품 그대로 있다.

## 7. 남은 것 · 확인 필요

- 시술 확인 필요 6 · 제품 확인 필요 8 = 병원 질문 목록(§2).
- 새 제품 13(웹 확인 · 미확인)은 이름 확인 「웹·식약처 미확인」 · mfds 빈칸. 올리디아120 · 365 는 식약처 허가 단위(제허 21-599)만 확인 · 모델명은 「외 48건」 안.
- 필러 용해 PRC-130 의 overview · mechanism 은 빈칸(원장 · 사용자 근거 문장 없음 — 지어 넣지 않음).
- `site.parent_code` 처럼 `product.parent_code` 스키마 뜻은 「원장이 포함 관계로 적은 것만」 인데 하위 제품 5(쥬베룩스킨 · 올리디아 2 · 포텐자펌핑팁 · 레스틸렌아이라이트)는 사용자 결정 · 식약처 근거다. 스키마 문구는 안 고쳤다.
- 허브 레포 반영 · DB 적재 · stg 는 다음 단계(SPEC-009 §5 P7 · P8).
