# 케이스 = 단위 시술 — 제품 연결 케이스 층 통일 · 케이스 고민 직접 붙이기 — 리포트(data 워커 · 2026-11-20)

> 발주 `case-unit` 사용자 결정(11-20). 작업 사본 `silver-model/` 에서만 고쳤다. 허브 레포 · DB · stg · 사용자 포트(18105 · 18222) 손댐 0 · 커밋 0.
> 공개 silver · gold 에서 병원 이름 grep 0 · 진료항목 코드 grep 0(324 코드 대조).

## 1. 결과 한 줄

`product_procedure` 81 → **0**(헤더만) · case_product **+1090**(469 → 1559 · 이미 있던 쌍 0 · 재료 불일치로 뺀 쌍 0) · 새 부위 빈 일반 케이스 3 · 케이스 고민 **14 케이스 · 20 행** 붙임 · 닿는 고민 0 이라 비운 케이스 **73** · 부위 빈 케이스(물려받기 유지) **166** · **silver-check PASS(WARN 5) · gold-check PASS(FAIL 0 · WARN 10)** · `gold_hash` **7b8669b7…** · `aux_hash` **624f1e25…** · 매핑 JSON 324(두 경로 sha256 같음 `58613ce7…`).

## 2. 셈 다시 확인(코디 셈과 다른 것)

- 케이스 341 · product_procedure 81 행 · case_product 469 — 코디 셈과 같다.
- **product_procedure 의 시술은 12 가 아니라 18**(PRC-100 21 · PRC-001 17 · PRC-111 9 · PRC-110 6 · PRC-122 5 · PRC-104 · 106 · 312 · 120 각 3 · PRC-103 · 107 2 · PRC-101 · 102 · 105 · 112 · 116 · 003 · 547 각 1).
- 고민(indication procedure_case) 있는 케이스 91 · 없는 케이스 250 — 같다. 케이스 0 시술 PRC-101 · 102 · 112 — 같다.

## 3. silver 바뀐 수(기준 `archive/silver-before-clinic-a-20261119-b3/` = 2차 뒤)

| 표 | 전 → 후 | 내용 |
|---|---|---|
| product_procedure | 81 → **0** | 헤더만 |
| case_product | 469 → 1559 | +1090(그 시술의 케이스마다 펼침) |
| procedure_case | 341 → 344 | +3 부위 빈 일반 케이스(CAS-1072 PMMA영구필러 · CAS-1073 폴리아크릴아미드겔 필러 · CAS-1074 꿀광주사) |
| indication | 1705 → 1725 | +20(procedure_case 대상) |
| source_ref | 48,508 → 50,189 | product_procedure 대상 112 행 지움 · 새 행 근거 덧붙임(case_product = 원래 product_procedure 행 근거 그대로 · indication = 시술 indication 행 근거 + 닿은 concern_site 행 근거 · 새 케이스 3 = user.csv) |
| user.csv(로컬) | 395 → 398 | 새 케이스 3 줄(basis 「사용자 결정 2026-11-20 · 케이스 = 단위 시술(제품 연결 케이스 층 통일)」) |

- 그 밖 54 표 바이트 같음. 케이스 · 제품 코드 바뀜 0 → **v5 CSV 바이트 그대로**(fill 다시 돌려 cmp 같음).
- 스크립트 `drafts/clinic-supplement/clinic-a-20261119/build_batch3.py`(기준 b3 에서 다시 돌려도 같은 바이트 · gold-check A3 확인) · 기록 `batch3-log.json`.
- 규칙 그대로 적용한 판정:
  - 재료: 케이스 `material_code` 가 있고 제품 `product_material` 이 있는데 위아래(조상 · 자손)로 닿지 않으면 뺀다 — **해당 0**(제품 재료 행이 없으면 판정 근거가 없어 넣음).
  - 고민: 시술 indication 고민 중 concern_site 부위가 케이스 부위의 자기 · 조상 · 자손이면 붙임 · note · site_code 는 시술 indication 행 값 그대로 · 같은 고민은 한 번.
  - **뗀 원장 자리 근거 3 접두(사용자 11-15 · silver-check E6)는 concern_site 근거 복사에서 뺐다** — 처음 실행에서 E6 FAIL 2(IND-1725 · 1732 가 `taxonomy.json:/modality/8/products/6/…` 를 받음). 검사 규칙이 정한 목록이라 스크립트에서 걸렀다(검사는 안 고침).
- 고민 없는 케이스(지금) = 239 = 비운 73 + 부위 빈 166(아래 목록 수와 같음).

### 옮긴 제품 연결(시술별 · case_product 새 행)

| 시술 | 새 연결 |
|---|---|
| PRC-001 보톡스 | 493 |
| PRC-003 피코레이저 | 7 |
| PRC-100 히알루론산 필러 | 462 |
| PRC-101 PMMA영구필러 | 1 |
| PRC-102 폴리아크릴아미드겔 필러 | 1 |
| PRC-103 PLLA | 8 |
| PRC-104 CaHA | 3 |
| PRC-105 콜라겐 필러 | 1 |
| PRC-106 PCL | 9 |
| PRC-107 PDLLA | 2 |
| PRC-110 PN주사 | 24 |
| PRC-111 물광주사 | 9 |
| PRC-112 꿀광주사 | 1 |
| PRC-116 PRP | 3 |
| PRC-120 줄기세포배양액 | 6 |
| PRC-122 줄기세포유래 엑소좀 | 15 |
| PRC-312 고주파 | 42 |
| PRC-547 초음파관리 | 3 |
| 계 | 1090 |

### 고민 붙인 케이스 14(새 indication 20 행)

- CAS-004 보톡스 × SITE-073 턱끝: CON-171 자갈턱
- CAS-005 보톡스 × SITE-036 코등: CON-018 콧등 주름
- CAS-006 보톡스 × SITE-067 입꼬리: CON-034 입꼬리 처짐
- CAS-007 보톡스 × SITE-070 잇몸: CON-180 잇몸미소
- CAS-008 보톡스 × SITE-037 코끝: CON-035 코끝 처짐
- CAS-018 보톡스 × SITE-093 손: CON-254 손 다한증
- CAS-019 보톡스 × SITE-097 발: CON-255 발 다한증
- CAS-096 보톡스 × SITE-001 전신: CON-253 겨드랑이 다한증 · CON-254 손 다한증 · CON-255 발 다한증 · CON-165 승모근 발달 · CON-198 종아리 굵음 · CON-011 목주름 · CON-020 목 앞쪽 세로주름
- CAS-100 보톡스 × SITE-144 침샘: CON-171 자갈턱
- CAS-1008 히알루론산 필러 × SITE-046 팔자주름: CON-009 팔자주름
- CAS-102 보톡스 × SITE-146 턱밑샘: CON-171 자갈턱
- CAS-1024 PN주사 × SITE-019 눈 주변: CON-017 눈밑주름
- CAS-3009 PDO 코그실 × SITE-035 코: CON-023 얼굴 처짐
- CAS-3045 크라이오리포라이시스 × SITE-077 턱밑: CON-164 이중턱

### 닿는 고민 0 이라 비운 케이스 73(부위 있음 · 시술 고민을 물려받음)

| 케이스 | 시술 | 부위 |
|---|---|---|
| CAS-1000 | PRC-100 히알루론산 필러 | SITE-036 코등 |
| CAS-1001 | PRC-100 히알루론산 필러 | SITE-037 코끝 |
| CAS-1002 | PRC-100 히알루론산 필러 | SITE-014 이마 |
| CAS-1003 | PRC-100 히알루론산 필러 | SITE-073 턱끝 |
| CAS-1004 | PRC-100 히알루론산 필러 | SITE-060 입술 |
| CAS-1005 | PRC-100 히알루론산 필러 | SITE-034 애교살 |
| CAS-1009 | PRC-100 히알루론산 필러 | SITE-079 목 |
| CAS-1010 | PRC-100 히알루론산 필러 | SITE-075 턱선 |
| CAS-1011 | PRC-100 히알루론산 필러 | SITE-016 관자놀이 |
| CAS-1032 | PRC-118 지방이식 | SITE-014 이마 |
| CAS-1038 | PRC-123 DCA 지방분해 주사 | SITE-077 턱밑 |
| CAS-1039 | PRC-124 콜산 지방분해 주사 | SITE-077 턱밑 |
| CAS-3029 | PRC-312 고주파 | SITE-079 목 |
| CAS-3032 | PRC-314 HIFES | SITE-007 얼굴 |
| CAS-1043 | PRC-100 히알루론산 필러 | SITE-120 마리오네트라인 |
| CAS-092 | PRC-001 보톡스 | SITE-016 관자놀이 |
| CAS-093 | PRC-001 보톡스 | SITE-046 팔자주름 |
| CAS-094 | PRC-001 보톡스 | SITE-060 입술 |
| CAS-1044 | PRC-100 히알루론산 필러 | SITE-015 미간 |
| CAS-097 | PRC-001 보톡스 | SITE-039 비익 |
| CAS-098 | PRC-001 보톡스 | SITE-062 윗입술 |
| CAS-099 | PRC-001 보톡스 | SITE-124 앞허벅지 |
| CAS-101 | PRC-001 보톡스 | SITE-145 귀밑샘 |
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
| CAS-130 | PRC-006 IPL | SITE-001 전신 |
| CAS-1047 | PRC-100 히알루론산 필러 | SITE-001 전신 |
| CAS-1048 | PRC-100 히알루론산 필러 | SITE-025 눈꺼풀 |
| CAS-1049 | PRC-100 히알루론산 필러 | SITE-026 안와상부 |
| CAS-1050 | PRC-100 히알루론산 필러 | SITE-109 엉덩이 |
| CAS-1051 | PRC-100 히알루론산 필러 | SITE-117 어깨 |
| CAS-1052 | PRC-100 히알루론산 필러 | SITE-143 쇄골 |
| CAS-1056 | PRC-116 PRP | SITE-051 볼 |
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
| CAS-3047 | PRC-311 HIFU | SITE-019 눈 주변 |
| CAS-3049 | PRC-312 고주파 | SITE-019 눈 주변 |
| CAS-3050 | PRC-312 고주파 | SITE-075 턱선 |
| CAS-3052 | PRC-313 마이크로웨이브 | SITE-001 전신 |
| CAS-3054 | PRC-316 니들RF | SITE-001 전신 |

### 부위 빈 케이스 166(결정대로 붙이지 않음 · 시술 고민 물려받기)

PRC-002(7) · PRC-003(4) · PRC-004(2) · PRC-005(2) · PRC-006(3) · PRC-007(1) · PRC-008(1) · PRC-009(1) · PRC-010(1) · PRC-011(1) · PRC-012(1) · PRC-013(1) · PRC-015(1) · PRC-016(2) · PRC-017(1) · PRC-018(1) · PRC-019(1) · PRC-020(3) · PRC-021(1) · PRC-022(2) · PRC-023(1) · PRC-024(1) · PRC-025(1) · PRC-026(1) · PRC-027(1) · PRC-028(1) · PRC-029(1) · PRC-100(2) · PRC-101(1) · PRC-102(1) · PRC-103(2) · PRC-104(1) · PRC-105(1) · PRC-106(1) · PRC-107(1) · PRC-108(1) · PRC-109(1) · PRC-110(2) · PRC-111(1) · PRC-112(1) · PRC-115(1) · PRC-116(1) · PRC-120(2) · PRC-122(2) · PRC-123(1) · PRC-125(1) · PRC-126(1) · PRC-127(1) · PRC-130(1) · PRC-300(1) · PRC-301(1) · PRC-302(1) · PRC-303(1) · PRC-304(1) · PRC-305(1) · PRC-306(2) · PRC-307(2) · PRC-308(1) · PRC-309(1) · PRC-310(1) · PRC-311(3) · PRC-312(9) · PRC-313(2) · PRC-314(1) · PRC-315(1) · PRC-316(9) · PRC-317(1) · PRC-500(5) · PRC-501(1) · PRC-502(1) · PRC-504(1) · PRC-505(1) · PRC-507(1) · PRC-509(1) · PRC-510(1) · PRC-511(1) · PRC-513(1) · PRC-514(1) · PRC-515(1) · PRC-516(1) · PRC-517(1) · PRC-518(1) · PRC-520(1) · PRC-522(1) · PRC-523(1) · PRC-524(1) · PRC-525(1) · PRC-526(1) · PRC-527(1) · PRC-528(1) · PRC-529(1) · PRC-530(1) · PRC-531(1) · PRC-532(1) · PRC-533(1) · PRC-534(1) · PRC-535(1) · PRC-536(1) · PRC-537(1) · PRC-539(1) · PRC-540(1) · PRC-541(1) · PRC-542(1) · PRC-543(1) · PRC-547(2) · PRC-549(1) · PRC-550(4) · PRC-551(3) · PRC-552(1) · PRC-553(1) · PRC-554(1) · PRC-557(1) · PRC-558(1)

코드: CAS-020 CAS-024 CAS-027 CAS-028 CAS-031 CAS-044 CAS-045 CAS-047 CAS-048 CAS-051 CAS-054 CAS-056 CAS-058 CAS-059 CAS-060 CAS-063 CAS-064 CAS-065 CAS-066 CAS-067 CAS-068 CAS-069 CAS-070 CAS-073 CAS-074 CAS-075 CAS-076 CAS-077 CAS-078 CAS-079 CAS-080 CAS-081 CAS-082 CAS-083 CAS-084 CAS-085 CAS-086 CAS-087 CAS-088 CAS-089 CAS-090 CAS-091 CAS-1012 CAS-1013 CAS-1018 CAS-1019 CAS-1020 CAS-1021 CAS-1022 CAS-1023 CAS-1026 CAS-1027 CAS-1029 CAS-1035 CAS-1036 CAS-1040 CAS-1041 CAS-1042 CAS-3000 CAS-3001 CAS-3002 CAS-3003 CAS-3004 CAS-3005 CAS-3006 CAS-3007 CAS-3010 CAS-3011 CAS-3012 CAS-3013 CAS-3014 CAS-3015 CAS-3016 CAS-3019 CAS-3020 CAS-3021 CAS-3022 CAS-3023 CAS-3024 CAS-3025 CAS-3026 CAS-3030 CAS-3033 CAS-3034 CAS-3036 CAS-3037 CAS-3038 CAS-3039 CAS-3040 CAS-3041 CAS-3042 CAS-3043 CAS-3044 CAS-5000 CAS-5001 CAS-5002 CAS-5003 CAS-5005 CAS-5008 CAS-5010 CAS-5013 CAS-5016 CAS-5019 CAS-5020 CAS-5021 CAS-5023 CAS-5024 CAS-5025 CAS-5026 CAS-5027 CAS-5028 CAS-5030 CAS-5032 CAS-5033 CAS-5034 CAS-5035 CAS-5036 CAS-5037 CAS-5038 CAS-5039 CAS-5040 CAS-5041 CAS-5042 CAS-5043 CAS-5044 CAS-5045 CAS-5046 CAS-5047 CAS-5049 CAS-5050 CAS-5051 CAS-5052 CAS-5054 CAS-5061 CAS-5063 CAS-5064 CAS-5065 CAS-5066 CAS-5067 CAS-5068 CAS-5069 CAS-5072 CAS-5073 CAS-5074 CAS-5077 CAS-5078 CAS-5079 CAS-1045 CAS-103 CAS-129 CAS-1046 CAS-1053 CAS-1054 CAS-1055 CAS-1057 CAS-1058 CAS-1059 CAS-3046 CAS-3048 CAS-3051 CAS-3053 CAS-5082 CAS-5083 CAS-1072 CAS-1073 CAS-1074

### 케이스에도 시술에도 닿지 않는 제품 21(옮기기 전부터 product_procedure 에 없던 제품 — 이번 범위 밖)

PRD-102 엘란쎄 S · PRD-103 엘란쎄 M · PRD-107 쥬베룩 파인 · PRD-108 쥬베룩 울트라 · PRD-150 리쥬란 · PRD-180 인주셀 · PRD-181 셀코어 · PRD-251 테스리프트 · PRD-253 에버라인 · PRD-255 잼버실 · PRD-268 엘리실 · PRD-269 로즈실 · PRD-345 E-MAX · PRD-509 이모드 · PRD-600 더마펜 · PRD-680 헤어셀 · PRD-689 이온자임 · PRD-690 플래티넘PTT · PRD-783 노바스템 · PRD-784 미라셀 · PRD-785 사파이어레이저

## 4. 확인 예

- **CAS-006 입꼬리 보톡스(SITE-067)** — 고민: CON-034 입꼬리 처짐(이제 이 하나 · 전에는 시술 고민 전부 물려받아 다한증 · 사각턱까지 나옴). 제품 19: 하이톡스 · 보톡스 · 디스포트 · 제오민 · 다복스 · 메디톡신 · 코어톡스 · 이노톡스 · 더톡신 · 원더톡스 · 리즈톡신 · 리즈톡스 · 비비톡신 · 톡스온 · 에이비오톡신 · 센독스 · 보리톡스 · 퓨어녹스 · 뉴럭스(나보타 · 보툴렉스 · 티엠버스는 다른 케이스에만 원장 연결이 있어 여기 없음).
- **CAS-003 눈가 보톡스(SITE-019)** — 제품 21: 보톡스 · 나보타 · 보툴렉스 · 하이톡스 · 디스포트 · 제오민 · 다복스 · 메디톡신 · 코어톡스 · 이노톡스 · 더톡신 · 원더톡스 · 리즈톡신 · 리즈톡스 · 비비톡신 · 톡스온 · 에이비오톡신 · 센독스 · 보리톡스 · 퓨어녹스 · 뉴럭스. 고민 CON-007 눈가주름(원래 있던 행 · **같은 고민 2 행은 전부터 있던 중복** — 손대지 않음).

## 5. 검사

### silver-check

```
전 기준 통과 · C12(제품이 둘 다) 0 · E6 0
G3 : WARN 5(작업 사본 밖 — .gitignore · config · work README · work-index · reference/)
PASS (WARN 5)  · silver 해시 fd2dad097f912fc01334bc4df944381977eac0254e167d584394cfa36443d0c4
```

### gold-build → gold-check

```
A1 · A2 · A3 · K1~K7 · M1 · V1 · Q1 · H1 · G1 : 통과(K7 product_procedure 0)
WARN A2 ×5 · G1 ×5(작업 사본 밖)
== FAIL 0 · WARN 10 · PASS
```

- gold-build · gold 계약이 product_procedure 행을 요구하지 않았다(0 행으로 빌드 · K5 · K7 통과) — 멈출 자리 없음.
- 생성 문서 다시 뽑음: `notes/silver-tables.md`(--write-docs) · `notes/vocabulary.csv`(gold 뒤 glossary-build).

### 고친 검사 스크립트(작업 사본 `gold/gold-check.py` 만 · 고치기 전 사본 `archive/scripts-before-batch3/`)

```diff
+B3 = os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119-b3')          # 묶음 3 기준 사본(2차 뒤 · 사용자 11-20)
+B3S = os.path.join(B3, 'silver')
+B3_APPEND = {f + '.csv' for f in ('procedure_case', 'case_product', 'indication')}
@@ a1() 묶음 2 비교 대상: 지금 silver → b3
-        a, b = open(os.path.join(B2S, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
+        a, b = open(os.path.join(B2S, fn), 'rb').read(), open(os.path.join(B3S, fn), 'rb').read()
@@ a1() 묶음 3(b3 → 지금 silver)
+    for fn in sorted(os.listdir(B3S)):
+        if fn in B3_APPEND: 기준 바이트 + 끝 덧붙임만
+        elif fn == 'product_procedure.csv': 헤더만
+        elif fn == 'source_ref.csv': 기준에서 product_procedure 대상 행만 빠진 것 + 끝 덧붙임(대상 표 case_product · indication · procedure_case 만)
+        elif a != b: bad('A1', f'묶음 3 {fn} 바뀜(허용 표 밖)')
@@ a3() 사슬: 보강 재현 · 묶음 2 재현 → b3 대조 · 그 위 build_batch3 재현 → 지금 silver · user.csv 대조
-            if … != open(os.path.join(SILVER, fn), 'rb').read():   (silver-supplement 3 표)
+            if … != open(os.path.join(B3S, fn), 'rb').read():
-            if open(os.path.join(out3, 'silver', fn), …) != open(os.path.join(SILVER, fn), …): bad('A3', '… (묶음 2)')
+            if open(os.path.join(out3, 'silver', fn), …) != open(os.path.join(B3S, fn), …): bad('A3', '… (묶음 2 → 기준 b3)')
+        (user.csv 도 b3 대조)
+        out4 = os.path.join(tmp, 'batch3')
+        subprocess.run([sys.executable, …/'build_batch3.py', B3S, os.path.join(B3, 'user.csv'), out4], check=True, …)
+        for fn in sorted(os.listdir(os.path.join(out4, 'silver'))): 지금 silver 와 바이트 대조 → bad('A3', '… (묶음 3)')
+        out4/user.csv ↔ 지금 user.csv
```

silver-check · gold-build 는 안 고쳤다.

## 6. gold · 해시

| 파일 | 행 전 → 후 |
|---|---|
| g_indication | 5839 → **12219**(제품 경유 후보가 케이스 단위로 펼쳐짐) |
| g_scope | 4882 → 7074 |
| g_evidence | 29823 → 38587 |
| g_edge · g_node | 10974 → 13183 · 1639 → 1642 |
| g_profile | 834 → 837(새 케이스 3) |
| g_offer · questions | 행 같음 · 내용 바뀜(제품 → 시술 경유가 케이스 경유로) |
| 나머지 | 바이트 같음 |

- `gold_hash` **d84e4b8e… → 7b8669b7f5204f233ac16cc445fd4507a43cfb4a8d7eaa4ae6daa5cd1186a8ae**(허브 `inputs.py` 식)
- `aux_hash` **1a8d2099… → 624f1e253189b2d3848b11c222788d7cec77d8da729ba7af74f922e4047bbd46**

## 7. 매핑 JSON

- 같은 두 경로 · 같은 꼴 · `build_mapping_json.py` 로 다시 · meta 해시 = §6 새 값 · items 324 · groups 131 · 두 파일 sha256 `58613ce767099c1a0552afe5eff442cff29eb3988758ffcf8d4ba0a368a75080` 같음 · 둘 다 `.gitignore data/` 무시 확인.
- v5 의 케이스 · 제품 코드 바뀜 0(항목 내용은 앞 판과 같고 meta 해시 · made_at 만 바뀜).

## 8. 검토할 자리(규칙대로 했지만 뜻이 어색한 것)

- **조상 · 자손 규칙과 1단 부위**: CAS-096 보톡스 × 전신(SITE-001)은 자손 부위 고민을 모두 받아 7 개(겨드랑이 · 손 · 발 다한증 · 승모근 · 종아리 · 목주름 2)가 붙었다. 바디보톡스 일반 케이스라 틀리진 않지만 넓다.
- **조상(2단) 경유 짝**: CAS-100 보톡스 × 침샘 · CAS-102 보톡스 × 턱밑샘 → 자갈턱(concern_site 가 2단 「턱」 에 걸려 있음) · CAS-3009 PDO 코그실 × 코 → 얼굴 처짐(1단 「얼굴」). 침샘 보톡스 ↔ 자갈턱은 뜻이 다르다 — 조상 범위를 2단 이하로 줄일지 · 손으로 뺄지는 사용자 판단.
- 닿는 고민 0 인 73 케이스는 concern_site(103 행)가 성겨서다 — 고민을 붙이려면 concern_site 보강이 먼저.
- 케이스에도 시술에도 닿지 않는 제품 21(§3 목록)은 이번 범위 밖(옮기기 전부터 연결 없음 · 2차 새 제품 인주셀 · 셀코어 · 이온자임 · 플래티넘PTT 포함 — 시술 확인 필요 줄의 제품).
- 시술 indication 에 붙은 `indication_condition`(사람 조건)은 케이스 고민 행으로 복사하지 않았다(발주 범위 밖).
