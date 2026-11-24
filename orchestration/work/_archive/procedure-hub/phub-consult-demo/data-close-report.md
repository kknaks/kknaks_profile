# 데이터 마감 — 고민 0 케이스 35 · 엑시머 · BBL 매핑 → gold → JSON (data 워커 · 2026-11-20)

발주 `task_901ac7f4ce35` · `ctx_80828a246aa9`(사용자 승인 11-20 「응!」). 커밋 0 · 허브 레포 · DB · stg 0 · 사용자 포트 0.

## 1. 결과 한 줄

- **고민 0 케이스 = 0**(387 케이스 전부 고민 1 이상) · **위층 indication 0** · 케이스 코드 바뀜 0(기존 386 그대로 · 새 CAS-136 끝에).
- 조사 표 142 줄 → 케이스 고민 **129 쌍**(후보 35 · note 「후보」) + 새 케이스 3 쌍. 근거 줄 종류: 원장 109 · 외부 16 · 같은 시술 다른 케이스 12 · 사용자 제공 5.
- 새 고민 3 · 새 원리 1(MEC-108) · 엑시머 PRC-030 overview · mechanism · mechanism_code 채움 · 새 케이스 1(CAS-136 IPL × 몸 × 피지샘) · case_product +1.
- v5 CSV 는 BBL 8 줄 중 **케이스가 바뀐 5 줄만** 바뀜(3 줄은 표와 원래 값이 같음) · 그 밖 316 줄 바이트 같음.
- **silver-check PASS(WARN 5) · gold-check PASS(FAIL 0 · WARN 10)** · `gold_hash` **57b420ad…** · `aux_hash` **51e3760a…** · 매핑 JSON 324 두 경로 같은 해시.

## 2. 표별 전 → 후(silver)

| 표 | 전 → 후 | 무엇 |
|---|---|---|
| concern | 266 → 269 | 새 고민 3 |
| mechanism | 54 → 55 | MEC-108 자외선 광면역조절 |
| procedure | 140 → 140 | PRC-030 빈 칸 3 채움 |
| procedure_case | 386 → 387 | CAS-136 |
| case_method | 397 → 398 | CME-0398 CAS-136 광 조사 |
| case_product | 1559 → 1560 | CPR-1564 CAS-136 ↔ PRD-323 BBL클리어 |
| indication | 2427 → 2559 | +132(조사 129 쌍 + CAS-136 3) · 위층 0 |
| source_ref | 55853 → 56073 | +220 |
| 그 밖 51 표 | 바이트 같음 | gold-check A1 묶음 6 |

케이스 빈칸: 부위 0 · 방법 0 · 조직 0 · 재료 19(이전과 같음 · 새 케이스는 0).

## 3. 고민 0 케이스 35 — 붙은 고민

| 케이스 | 고민(후보 표시) | 수 |
|---|---|---|
| CAS-028 | 문신 | 1 |
| CAS-044 | 국소 지방 · 복부 지방 · 러브핸들 · 허벅지 지방 | 4 |
| CAS-051 | 문신 | 1 |
| CAS-057 | 여드름흉터 · 모공 · 주름 · 피부결 · 잔주름 · 광손상 (후보) | 6 |
| CAS-058 | 피부톤 불균일 (후보) · 모공 확대 · 색소침착 | 3 |
| CAS-059 | 피부 탄력 저하 · 얼굴 처짐 · SMAS 이완 (후보) · 잔주름 (후보) | 4 |
| CAS-063 | 급성 여드름 · 면포 · 구진 · 농포 · 여드름 · 피지 과다분비 · 염증성 여드름 · 여드름 후 홍반 (후보) | 8 |
| CAS-064 | 피부 이완 · 피부 탄력 저하 · 팔뚝 처짐 (후보) · 피부 처짐 | 4 |
| CAS-070 | 피로 · 피부 칙칙함 (후보) | 2 |
| CAS-3030 | 국소 지방 · 셀룰라이트 · 피부 이완 · 팔뚝 처짐 · 복부 처짐 · 얼굴 처짐 (후보) | 6 |
| CAS-3052 | 국소 지방 · 셀룰라이트 · 피부 이완 · 팔뚝 처짐 · 복부 처짐 · 얼굴 처짐 (후보) | 6 |
| CAS-3051 | 얼굴 처짐 · 피부 탄력 저하 · 이중턱 · 목주름 (후보) | 4 |
| CAS-3032 | 얼굴 처짐 · 피부 탄력 저하 (후보) · 주름 (후보) | 3 |
| CAS-5030 | 피부결 · 모공 확대 · 피부톤 불균일 | 3 |
| CAS-5032 | 모공 · 피부결 · 여드름흉터 (후보) · 각질 축적 (후보) | 4 |
| CAS-5033 | 여드름흉터 · 색소침착 · 피부톤 불균일 · 주름 (후보) · 모공 확대 · 각질 축적 (후보) | 6 |
| CAS-5042 | 색소침착 · 피부톤 불균일 · 피부 칙칙함 (후보) · 각질 축적 (후보) | 4 |
| CAS-5049 | 모공 확대 · 모공 막힘 · 피지 과다분비 (후보) · 피부 탄력 저하 (후보) · 주름 (후보) | 5 |
| CAS-5051 | 피부 탄력 저하 · 잔주름 · 피부톤 불균일 · 윤기 부족 | 4 |
| CAS-5063 | 기미 · 색소침착 · 여드름 (후보) | 3 |
| CAS-5064 | 미세주름 · 피부 탄력 저하 · 수분 부족 · 잔주름 · 피부톤 불균일 (후보) | 5 |
| CAS-5065 | 수분 부족 · 피부 탄력 저하 · 잔주름 | 3 |
| CAS-5066 | 수분 부족 (후보) · 피부 칙칙함 (후보) · 피부 탄력 저하 (후보) · 잔주름 (후보) | 4 |
| CAS-5067 | 여드름흉터 · 피부 탄력 저하 · 미세주름 | 3 |
| CAS-5068 | 박스카흉터 · 여드름흉터 · 미세주름 · 피부 탄력 저하 | 4 |
| CAS-5069 | 여드름흉터 · 피부톤 불균일 (후보) · 피부 재생력 저하 (후보) | 3 |
| CAS-5072 | 수분 부족 · 주름 · 볼륨 손실 (후보) · 피부 탄력 저하 | 4 |
| CAS-1045 | 필러 부작용 · 얼굴 좌우 비대칭 (후보) | 2 |
| CAS-101 | 귀밑샘 비대 · 윤곽 (후보) · 자갈턱 (후보) | 3 |
| CAS-1066 | 허벅지 지방 · 국소 지방 | 2 |
| CAS-1067 | 허벅지 지방 · 국소 지방 | 2 |
| CAS-1068 | 허벅지 지방 · 국소 지방 | 2 |
| CAS-1071 | 국소 지방 · 브래지어 라인 지방 (후보) · 부유방 (후보) | 3 |
| CAS-1072 | 볼륨 손실 · 윤곽 · 팔자주름 · 여드름흉터 | 4 |
| CAS-1073 | 볼륨 손실 · 윤곽 · 깊은주름 · 팔자주름 | 4 |
| CAS-136 | 여드름 · 급성 여드름 · 염증성 여드름 | 3 |

- 「후보」 는 케이스 × 고민 쌍의 근거 줄이 모두 확신 「후보」 일 때만 note 에 적었다. 확실 줄이 하나라도 있으면 note 빈칸.
- 근거(source_ref)
  - 원장: 조사 표 포인터 그대로(`phub-ledger/` 접두 뗌).
  - 외부: URL.
  - 사용자 제공: user.csv 결정 줄과 Sciton URL.
  - 같은 시술 다른 케이스: user.csv 결정 줄(근거 케이스 · 조사 표 줄 번호).
  - 사용자 제공 · 같은 시술 다른 케이스는 `build_batch6.py` 가 user.csv 결정 줄로 남겼다(status 확인).

## 4. 새 고민 · 원리 · 시술 · 케이스

| 코드 | 무엇 | 비고 |
|---|---|---|
| CON-287 필러 부작용 | 위 CON-278 기타 · 중분류 · filler complications | 원장 complications 포인터 2 + 논문 2 |
| CON-288 귀밑샘 비대 | 위 CON-275 윤곽 · 중분류 · parotid gland hypertrophy | 논문 2 |
| CON-289 부유방 | 위 CON-181 국소 지방 · 소분류 · accessory breast | 논문 · 임상시험 등록 |
| MEC-108 자외선 광면역조절 | UVB photoimmunomodulation · 위 없음 | **그림 없음** — 다음 그림 묶음 대상(silver-check I2 예외) |
| PRC-030 엑시머 레이저 | mechanism_code = MEC-108 · overview · mechanism = excimer-overview.md 문안 그대로 | 근거 = user.csv 결정 줄(문안) + 원장 4 + 논문 4 |
| CAS-136 | PRC-006 IPL × SITE-147 몸 × TIS-021 피지샘 · MAT-220 광대역 빛 · MET-111 광 조사 | 고민 여드름 · 급성 여드름 · 염증성 여드름(BBL 조사 Forever Clear) · 제품 BBL클리어 |

**조사 표와 다르게 한 것(검사 규칙 때문)**
- 새 고민 이름의 괄호를 뺐다(D2 이름 괄호 0): 「필러 부작용(과교정 · 결절 · 비대칭)」 → 「필러 부작용」. 귀밑샘 비대 · 부유방도 같다. 괄호 안 말은 description 으로 옮겼다.
- MEC-108 설명에서 「308nm」 을 뺐다(D7 사전 설명 수치 0). 시술 PRC-030 의 overview · mechanism 문안에는 그대로 있다.

**BBL 제품 확인**: 표대로 케이스가 바뀐 자리의 BBL 제품을 확인했다. 없던 연결은 CAS-136 ↔ PRD-323 하나뿐이라 그것만 더했다.
- CAS-060 · 061: PRD-321 히어로 · 320 포에버영 이미 있음.
- CAS-063: PRD-323 클리어 이미 있음.
- CAS-130: PRD-320 이미 있음.

**CAS-064 확인**: 조사 표 고민(피부 이완 · 피부 탄력 저하 · 피부 처짐 · 팔뚝 처짐(후보))이 붙었다. BBL 스킨타이트 매핑은 그대로다.

## 5. BBL 8 줄 전 → 후(v5 CSV)

| 진료항목 코드 | 진료항목 | 케이스 전 → 후 | 상태 |
|---|---|---|---|
| 26-BBL-1MODE | BBL HERO (1가지 모드) | CAS-129 → CAS-060 + CAS-061 | 매핑됨 → **매핑됨(확인 필요: BBL 필터)** |
| 26-BBL-2MODE | BBL HERO (2가지 모드) | CAS-129 → CAS-060 + CAS-061 | 매핑됨 → **매핑됨(확인 필요: BBL 필터)** |
| 26-BBL-CLER-FACE | BBL 클리어 (페이스) | CAS-129 → CAS-063 | 매핑됨 |
| 26-BBL-CLER-BODY | BBL 클리어 (바디) | CAS-130 → **CAS-136** | 매핑됨 |
| 26-BBL-FRYG-FACE | BBL 포에버영 (페이스) | CAS-129 → CAS-060 + CAS-061 | 매핑됨 |
| 26-BBL-FRYG-BODY | BBL 포에버영 (바디) | CAS-130 (같음) | 매핑됨 |
| 26-BBL-SKTY-FACE | BBL 스킨타이트 (페이스) | CAS-064 (같음) | 매핑됨 |
| 26-BBL-SKTY-BODY | BBL 스킨타이트 (바디) | CAS-064 (같음) | 매핑됨 |

- 바뀐 5 줄은 채움 메모 끝에 「/ 11-20 BBL 매핑: …」 를 덧붙였다. HERO 두 줄의 메모는 「필터 조합 병원 확인」 이다.
- 헤더와 그 밖 316 줄은 기준 사본(`archive/silver-before-clinic-a-20261119-b6/v5.csv`)과 바이트가 같다.
- `허브 부위 코드` 칸은 손대지 않았다(발주 범위 = 케이스 칸). CLER-BODY 의 부위 코드는 SITE-001 그대로다. 새 케이스 CAS-136 의 부위는 SITE-147 몸이라 둘이 다르다. 맞출지는 판단할 일이다.
- 매핑 JSON 은 `build_mapping_json.py` 그대로 만들었다. 그래서 HERO 두 줄의 상태가 JSON 에서는 「매핑됨」 이다. 이 스크립트는 「시술 확인 필요」 만 따로 둔다. 「확인 필요: BBL 필터」 는 v5 CSV 에만 남는다. 앱에 띄우려면 스크립트를 한 줄 고쳐야 한다(범위 밖이라 안 고침).

## 6. 검사

| 항목 | 결과 |
|---|---|
| 고민 0 케이스 | **0** |
| 위층 indication | **0** |
| 새 값 source_ref | 빠진 것 0(새 indication 132 · 고민 3 · 원리 · PRC-030 칸 3 · CAS-136 칸 4 · case_method · case_product) |
| 케이스 코드 | 기존 386 행 바이트 같음 · 새 1 끝에 |
| build_batch6.py 재현 | 두 번 돌려 같은 바이트 · gold-check A3 묶음 6 재현 통과 |
| silver-check | **PASS**(WARN 5 — 작업 사본 밖 git) · `--write-docs` 로 notes/silver-tables.md 다시 뽑음 |
| gold-build → glossary-build → gold-check | **PASS**(FAIL 0 · WARN 10) · gold-build 는 고치지 않음 |
| 병원 이름 · 진료항목 코드 grep(silver · gold) | 0 |
| v5 CSV | BBL 5 줄만 바뀜(8 줄 중) · 316 줄 같음 |
| 매핑 JSON | items 324 · groups 131 같음 · 케이스 바뀐 항목 = BBL 5 · 그 밖 319 항목 같음(meta 만 새로) · 케이스 코드 전부 silver 에 있음 · 두 경로 `git check-ignore` 무시 |

### gold 표(전 → 후)

g_edge 14063 → 14200 · g_entry 2731 → 2734 · g_evidence 40680 → 40978 · g_indication 13629 → 13911 · g_node 1684 → 1688 · g_profile 880 → 881 · g_scope 7245 → 7251 · questions 37(내용 바뀜) · 나머지 8 표 바이트 같음.

### 해시

- `gold_hash` 43b95e4e… → **57b420ad10d34ff7d3764fd7afbf7d1d731b1d27a1d29984d011d3a61586ec44**
- `aux_hash` 58297d11… → **51e3760a82df45de2011b59868a723532af9c7732163e1eee31472ceb8a93b34**
- 계산은 허브 `inputs.py` 식으로 했다. 묶음 전 값 43b95e4e · 58297d11 이 같은 식으로 다시 나오는 것을 먼저 확인했다.
- 매핑 JSON sha256 **95275b6671d76acd5b000e013a6d61820cea3b8526818e78095dc89fb1f233d5** 이고 두 경로가 같다.
  - `clinic_chat/phub-consult-demo/data/kos/`
  - `git/clinic_chat/data/kos/`

### 검사 고친 것(diff · 고치기 전 사본 `archive/scripts-before-batch6/`)

- silver-check
  - I2: 묶음 6 새 원리(batch6-log `new_mechanisms`)는 그림 행 없어도 통과. **그림 없는 원리 = MEC-108**.
  - C8: 묶음 6 시술(PRC-030)은 user.csv 승인 문안 줄을 줄 단위로도 대조한다. 결정 줄이 「이름 줄바꿈 문안」 이라 문장 나눔만으로는 첫 문장이 안 떨어진다.
  - C3 예외 목록에 batch6-log dup_groups 를 더했다(지금 0).
- gold-check
  - A1: 묶음 5 대조 대상을 b6 로 바꿨다. 묶음 6 허용을 더했다. 7 표는 끝 덧붙임이고, procedure 는 PRC-030 의 빈칸 3 채움만 허용한다.
  - A3: 묶음 5 재현은 b6 와 대조한다. 묶음 6 재현은 지금 silver · user.csv · batch6-log 와 대조한다.
- v5 바뀐 줄 기록은 `batch6-v5-log.json` 에 따로 둔다. 재현 모드는 v5 를 안 쓰기 때문이다.

<details><summary>silver-check.py diff</summary>

```diff
--- archive/scripts-before-batch6/silver-check.py	2026-11-20 13:50:30
+++ drafts/silver-check/silver-check.py	2026-11-20 14:50:04
@@ -36,6 +36,13 @@
 if os.path.exists(_B5):
     B4_LOG.setdefault('dup_groups', set())
     B4_LOG['dup_groups'] |= {frozenset(g) for g in json.load(open(_B5, encoding='utf-8')).get('dup_groups', [])}
+_B6 = os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'batch6-log.json')          # 묶음 6(데이터 마감 · 사용자 11-20) — 새 원리 그림 없음(I2) · 승인 문안 시술(C8)
+B6_LOG = {'new_mechanisms': set(), 'procedures': set()}
+if os.path.exists(_B6):
+    _j6 = json.load(open(_B6, encoding='utf-8'))
+    B6_LOG = {'new_mechanisms': {m[0] for m in _j6.get('new_mechanisms', [])}, 'procedures': {m[0] for m in _j6.get('procedure', [])}}
+    B4_LOG.setdefault('dup_groups', set())
+    B4_LOG['dup_groups'] |= {frozenset(g) for g in _j6.get('dup_groups', [])}
 # 11-16 아카이브 이동(work/<slug>/ → work/_archive/procedure-hub/<slug>/) 뒤에도 원장을 찾도록
 # 위로 올라가며 orchestration/work 를 찾는다. 원장은 열린 작업 work/phub-recommend/bronze/ 에 있다.
 WORK = SM
@@ -690,7 +697,8 @@
             ts = texts('procedure', p['code'], fld)
             rest = p[fld]
             for x in sorted(set(ts), key=len, reverse=True):
-                for s in sorted(re.split(r'(?<=[.다])\s+', x), key=len, reverse=True):
+                # 묶음 6: 사용자 승인 문안(user.csv 결정 줄 = 이름 · 결정 · 근거 줄바꿈)은 줄 단위로도 대조
+                for s in sorted(re.split(r'(?<=[.다])\s+', x) + (x.split('\n') if p['code'] in B6_LOG['procedures'] else []), key=len, reverse=True):
                     rest = rest.replace(s, '')
                 rest = rest.replace(x, '')
             if not ts or rest.strip():
@@ -949,7 +957,7 @@
     img_codes = {r['target_code'] for r in D['concept_image']}
     # 묶음 4(케이스 보충 · 사용자 11-20): 새 방법 사전 항목은 그림 행 없이 둠 — 다음 그림 묶음 대상(case-fill-report.md 목록)
     for c in sorted(dict_codes - img_codes):
-        if c in B4_LOG.get('new_methods', set()):
+        if c in B4_LOG.get('new_methods', set()) or c in B6_LOG['new_mechanisms']:          # 묶음 6 새 원리 — 다음 그림 묶음 대상(data-close-report.md 목록)
             continue
         hit('I2', 'FAIL', 'concept_image', c, '사전 코드에 그림 행 없음')
     for c in sorted(img_codes - dict_codes):
```
</details>

<details><summary>gold-check.py diff</summary>

```diff
--- archive/scripts-before-batch6/gold-check.py	2026-11-20 13:51:59
+++ gold/gold-check.py	2026-11-20 14:50:59
@@ -83,6 +83,10 @@
 B5S = os.path.join(B5, 'silver')
 B5_APPEND = {f + '.csv' for f in ('concern', 'tissue', 'procedure', 'material', 'procedure_material', 'case_method')}
 B5_CHANGE = {f + '.csv' for f in ('indication', 'indication_condition', 'citation_link', 'statement_translation', 'concern_site', 'site', 'procedure_case', 'source_ref')}
+B6 = os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119-b6')          # 묶음 6 기준 사본(5차 뒤 · 데이터 마감 · 사용자 11-20 「응!」)
+B6S = os.path.join(B6, 'silver')
+B6_APPEND = {f + '.csv' for f in ('concern', 'mechanism', 'procedure_case', 'case_method', 'case_product', 'indication', 'source_ref')}
+B6_PROC_ROWS = ('PRC-030',)          # 엑시머 — mechanism_code · overview · mechanism 빈칸 → 값
 B2_APPEND = {f + '.csv' for f in ('product', 'organization', 'material', 'procedure', 'procedure_material', 'procedure_case', 'case_product',
                                   'product_organization', 'product_material', 'product_modality', 'alias', 'source_ref')}
 
@@ -192,12 +196,12 @@
     # 묶음 5(build_batch5.py · 사용자 11-20 고민 → 케이스): 기준 = b5 — 사전 표 끝 덧붙임 · 고민 · 부위 · 케이스 · 근거 표는 바뀜 허용(재현 A3 가 바이트 대조)
     #   그 밖 표 바이트 같음 · indication 위층 줄 0 · 위층 아닌 기존 줄은 그대로 남거나 지워짐(내용 안 바뀜)
     for fn in sorted(os.listdir(B5S)):
-        a, b = open(os.path.join(B5S, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
+        a, b = open(os.path.join(B5S, fn), 'rb').read(), open(os.path.join(B6S, fn), 'rb').read()
         if fn in B5_APPEND:
             if not b.startswith(a):
                 bad('A1', f'묶음 5 {fn} 앞쪽(기존 행) 바이트가 바뀜')
         elif fn == 'indication.csv':
-            ra, rb = rows(os.path.join(B5S, fn)), rows(os.path.join(SILVER, fn))
+            ra, rb = rows(os.path.join(B5S, fn)), rows(os.path.join(B6S, fn))
             old = {r[0]: r for r in ra[1:]}
             for r in rb[1:]:
                 if r[1] in ('procedure', 'modality', 'package'):
@@ -208,6 +212,29 @@
             continue
         elif a != b:
             bad('A1', f'묶음 5 {fn} 바뀜(허용 표 밖)')
+    # 묶음 6(build_batch6.py · 데이터 마감): 기준 = b6 — 7 표 끝 덧붙임(기존 행 바이트 그대로) · procedure 는 PRC-030 빈 칸 3 만 · 그 밖 표 바이트 같음
+    for fn in sorted(os.listdir(B6S)):
+        a, b = open(os.path.join(B6S, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
+        if fn in B6_APPEND:
+            if not b.startswith(a):
+                bad('A1', f'묶음 6 {fn} 앞쪽(기존 행) 바이트가 바뀜')
+        elif fn == 'procedure.csv':
+            ra, rb = rows(os.path.join(B6S, fn)), rows(os.path.join(SILVER, fn))
+            if ra[0] != rb[0] or len(ra) != len(rb):
+                bad('A1', '묶음 6 procedure 헤더 · 행 수')
+            h = ra[0]
+            for x, y in zip(ra[1:], rb[1:]):
+                if x == y:
+                    continue
+                if x[0] not in B6_PROC_ROWS or x[0] != y[0]:
+                    bad('A1', f'묶음 6 procedure {x[0]} 바뀜(허용 = PRC-030)')
+                    continue
+                for col in h:
+                    i = h.index(col)
+                    if x[i] != y[i] and (col not in ('mechanism_code', 'overview', 'mechanism') or x[i]):
+                        bad('A1', f'묶음 6 procedure {x[0]} 칸 {col} 바뀜(허용 = 빈칸 채움)')
+        elif a != b:
+            bad('A1', f'묶음 6 {fn} 바뀜(허용 표 밖)')
     now = sorted(f for f in os.listdir(SILVER) if f.endswith('.csv'))
     if now != sorted(os.listdir(CLINIC_BASE)):
         bad('A1', f'silver 표 목록 ≠ 묶음 기준 사본: {sorted(set(now) ^ set(os.listdir(CLINIC_BASE)))}')
@@ -276,11 +303,21 @@
         out6 = os.path.join(tmp, 'batch5')
         subprocess.run([sys.executable, os.path.join(cd, 'build_batch5.py'), B5S, os.path.join(B5, 'user.csv'), out6], capture_output=True, text=True, check=True)
         for fn in sorted(os.listdir(os.path.join(out6, 'silver'))):
-            if open(os.path.join(out6, 'silver', fn), 'rb').read() != open(os.path.join(SILVER, fn), 'rb').read():
-                bad('A3', f'silver {fn} 재현 다름(묶음 5)')
-        for fn in ('user.csv', 'batch5-log.json'):
-            if open(os.path.join(out6, fn), 'rb').read() != open(os.path.join(cd, fn), 'rb').read():
-                bad('A3', f'묶음 5 {fn} 재현 다름')
+            if open(os.path.join(out6, 'silver', fn), 'rb').read() != open(os.path.join(B6S, fn), 'rb').read():
+                bad('A3', f'silver {fn} 재현 다름(묶음 5 → 기준 b6)')
+        if open(os.path.join(out6, 'user.csv'), 'rb').read() != open(os.path.join(B6, 'user.csv'), 'rb').read():
+            bad('A3', '묶음 5 user.csv 재현 다름(→ 기준 b6)')
+        if open(os.path.join(out6, 'batch5-log.json'), 'rb').read() != open(os.path.join(cd, 'batch5-log.json'), 'rb').read():
+            bad('A3', '묶음 5 batch5-log.json 재현 다름')
+        # 묶음 6: b6 위에 build_batch6.py 재현 → 지금 silver · user.csv · batch6-log 와 바이트 대조
+        out7 = os.path.join(tmp, 'batch6')
+        subprocess.run([sys.executable, os.path.join(cd, 'build_batch6.py'), B6S, os.path.join(B6, 'user.csv'), out7], capture_output=True, text=True, check=True)
+        for fn in sorted(os.listdir(os.path.join(out7, 'silver'))):
+            if open(os.path.join(out7, 'silver', fn), 'rb').read() != open(os.path.join(SILVER, fn), 'rb').read():
+                bad('A3', f'silver {fn} 재현 다름(묶음 6)')
+        for fn in ('user.csv', 'batch6-log.json'):
+            if open(os.path.join(out7, fn), 'rb').read() != open(os.path.join(cd, fn), 'rb').read():
+                bad('A3', f'묶음 6 {fn} 재현 다름')
         if open(os.path.join(tmp, 'same-day-judgment.csv'), 'rb').read() != open(os.path.join(NOTES, 'same-day-judgment.csv'), 'rb').read():
             bad('A3', 'notes/same-day-judgment.csv 재현 다름')
     finally:
```
</details>

## 7. 확인 시험 — 고민 15 + 4(명동점 진료항목 · 전 = b6 silver + v5 기준 · 후 = 지금)

고민은 그 고민 + 아래 고민으로 찾는다.
- 「여드름(바디)」 는 여드름 계열 중 몸(SITE-147) 아래 케이스만 센다.
- 엉뚱은 기계 검사다. 다음 중 하나에 걸리면 엉뚱으로 센다.
  - 얼굴 피부 상태 고민 × 몸 케이스
  - 제모 항목
  - 부위 고민인데 케이스 부위가 고민 부위 위아래 밖

| 고민 | 케이스 전 → 후 | 진료항목 전 → 후 | 빠짐 | 새로 닿은 진료항목 | 엉뚱 |
|---|---|---|---|---|---|
| 여드름 | 37 → 41 | 34 → 37 | 0 | BBL 클리어 (바디) · BBL 클리어 (페이스) · 이온 비타민 미백관리 | 1 BBL 클리어 (바디)(CAS-136) |
| 기미 | 35 → 36 | 28 → 27 | 2 BBL 클리어 (바디) · BBL 클리어 (페이스) | 이온 비타민 미백관리 | 0 |
| 모공 | 44 → 50 | 31 → 31 | 0 | — | 0 |
| 입꼬리 처짐 | 1 → 1 | 4 → 4 | 0 | — | 0 |
| 팔자주름 | 23 → 25 | 23 → 23 | 0 | — | 0 |
| 다한증 | 5 → 5 | 15 → 15 | 0 | — | 0 |
| 피부 탄력 저하 | 42 → 54 | 39 → 60 | 0 | BBL 스킨타이트 (바디) · BBL 스킨타이트 (페이스) · [추가옵션] 포트라 10KJ 추가 (단독 사용 불가) · 맞춤형 관리 케어 프로그램 (LDM 6'/SONO/오투덤 택 1) · 오투덤 · 온다리프팅 얼굴 · 온다리프팅 얼굴 60KJ · 온다리프팅 얼굴 추가 · 티타늄리프팅 · 티타늄리프팅 추가 · 포트라 · 포트라 60KJ | 0 |
| 이중턱 | 10 → 11 | 5 → 12 | 0 | 온다리프팅 얼굴 · 온다리프팅 얼굴 60KJ · 온다리프팅 얼굴 추가 | 0 |
| 눈가주름 | 21 → 21 | 18 → 18 | 0 | — | 0 |
| 사각턱 | 1 → 1 | 5 → 5 | 0 | — | 0 |
| 셀룰라이트 | 4 → 6 | 3 → 9 | 0 | 온다리프팅 바디 · 온다리프팅 바디 추가 | 0 |
| 잡티 | 13 → 13 | 13 → 11 | 2 BBL 클리어 (바디) · BBL 클리어 (페이스) | — | 0 |
| 홍조 | 15 → 15 | 14 → 17 | 0 | BBL HERO (1가지 모드) · BBL HERO (2가지 모드) · BBL 포에버영 (페이스) | 0 |
| 볼륨 손실 | 37 → 40 | 31 → 31 | 0 | — | 0 |
| 피부 건조 | 10 → 10 | 5 → 5 | 0 | — | 0 |
| 여드름(바디) | 0 → 1 | 0 → 1 | 0 | BBL 클리어 (바디) | 1 BBL 클리어 (바디)(CAS-136) |
| 피부 처짐 | 6 → 7 | 16 → 28 | 0 | BBL 스킨타이트 (바디) · BBL 스킨타이트 (페이스) · [추가옵션] 포트라 10KJ 추가 (단독 사용 불가) · 티타늄리프팅 · 티타늄리프팅 추가 · 포트라 · 포트라 60KJ | 0 |
| 문신 | 2 → 4 | 0 → 2 | 0 | 문신제거 레터링 1x10 · 문신제거 명함크기 | 0 |
| 부유방 | 0 → 1 | 0 → 1 | 0 | 세라핏 부유방 지방분해주사 | 0 |

### 읽기

- **빠짐 4 는 의도한 것이다**(기미 · 잡티 → BBL 클리어 바디 · 페이스).
  - 전에는 클리어가 CAS-129 · 130(IPL × 멜라닌)에 매핑되어 색소 고민에 닿았다.
  - 표대로 CAS-063 · 136(피지샘)으로 바꿔 여드름 쪽으로 옮겼다. 기미 · 잡티는 여전히 HERO · 포에버영 항목에 닿는다.
- **엉뚱 1(여드름 × CAS-136 BBL 클리어 바디)은 사용자 결정이다.**
  - 고민 범위 표(concern-scope.csv)는 여드름을 「얼굴 피부 상태」 로 둔다. 그래서 몸 케이스가 기계 검사에 걸린다.
  - 몸 여드름을 허브에 둔다면 여드름 범위를 「피부 전반」 으로 넓힐지 판단해야 한다(열린 것).
- 새로 닿은 것
  - 문신 0 → 2(문신제거 2)
  - 부유방 0 → 1(세라핏 부유방)
  - 여드름(바디) 0 → 1(BBL 클리어 바디)
  - 피부 처짐 16 → 28 · 피부 탄력 저하 39 → 60(BBL 스킨타이트 · 포트라 · 티타늄 · 온다 · 오투덤)
  - 이중턱 5 → 12(온다 얼굴)
  - 셀룰라이트 3 → 9(온다 바디)
  - 홍조 14 → 17(HERO 1 · 2 모드 · 포에버영 페이스 → CAS-061 혈관)

## 8. 열린 것

- HERO 1 · 2 모드의 실제 필터 조합 — 병원 확인이 필요하다. v5 에는 「매핑됨(확인 필요: BBL 필터)」 으로 적었다. JSON 상태는 「매핑됨」 이다(§5).
- MEC-108 그림 — 다음 그림 묶음에서 만든다.
- 여드름 고민 범위(몸 여드름) — §7.
- v5 CLER-BODY 의 `허브 부위 코드` 칸 — 지금 SITE-001 이고 새 케이스는 SITE-147 이다.
- 후보 35 쌍(note 「후보」) — 사람 검수 대상이다. 목록은 `concern-zero-fill.csv` 확신 칸과 `research-concern-zero.md` §2 에 있다.
- DCA 허벅지 · 부유방은 허가 외 사용이다. 상담 문구를 어떻게 할지 판단해야 한다(research-concern-zero.md §4).
- 로컬 허브(18105)는 다시 띄우지 않았다. 새 gold 를 쓰려면 다시 띄워야 한다(발주 범위 밖 · 사용자 포트).

## 9. 파일

- 스크립트 · 로그
  - `silver-model/drafts/clinic-supplement/clinic-a-20261119/build_batch6.py`
  - `batch6-log.json` · `batch6-v5-log.json` · `user.csv`(+34 줄 · 결정 줄 L2198 ~ L2231)
- 기준 사본: `silver-model/archive/silver-before-clinic-a-20261119-b6/`(silver · user.csv · v5.csv)
- 고치기 전 사본
  - 검사 스크립트: `archive/scripts-before-batch6/`
  - gold: `archive/gold-before-batch6/`
- 검사 스크립트(고침)
  - `drafts/silver-check/silver-check.py`
  - `gold/gold-check.py`
- 다시 뽑은 것: silver 8 표 · gold · `notes/silver-tables.md` · `notes/vocabulary.csv`
- 매핑: `reference/2026-11-19-myeongdong-kos/myeongdong-kos-medical-services-20261119.v5.csv` · 매핑 JSON 두 경로
