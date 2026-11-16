# batch-02 묶음 검토 — 원장 5개 1차 결과

- 검토: 독립 Opus 검토 워커(reviewer_doc) · `task_8332526dcb8f` / `ctx_68a17c6bda51` · 2026-11-09
- 기준: [1차 조사 스킬](./ledger-first-pass/SKILL.md)의 산출물 계약·종료 기준, [재개 노트](./_RESUME.md), [발주 기록](./batch-02-dispatches.json)
- 범위: anatomy-danger-zones · combo-recipes · consent-checklist · contraindications · extracted. 다른 원장은 열지 않았다. 원본·결과·공통 문서는 고치지 않았다. 이 파일 하나만 만들었다(독립 대조 스크립트는 세션 스크래치패드에만 있음).
- 이 검토는 **1차 수집 계약 충족 여부**를 본다. 의미 조사·임상 사실 검증·형태소 전체 정답 판정은 하지 않았다.

## 0. 결론

| 원장 | 판정 | 1차 범위 종료 | 원장 전체 | 고쳐야 할 추출 오류 |
|---|---|---|---|---|
| anatomy-danger-zones | **WARN** (막지 않음) | 가능 | 완료 아님 | 0 — 미표시 오분절 17출현 기록 권고(§2.1) |
| combo-recipes | **PASS** | 가능 | 완료 아님 | 0 |
| consent-checklist | **PASS** (형식 비고 1) | 가능 | 완료 아님 | 0 |
| contraindications | **PASS** (형식 비고 1) | 가능 | 완료 아님 | 0 |
| extracted | **WARN** (분류만) | 가능 | 완료 아님 | 0 — I 6건 재분류 권고(§2.5) |

다섯 원장 모두에서 아래 항목은 **찾지 못했다**: 원문 누락, 원문 변형, 잘못된 Pointer, 잘못된 문자구간, 자료형 변형, 명시하지 않은 추출 실패, 구획 소유 누락·중복. 그래서 1차 종료를 막는 수정 요청은 없다.

WARN 두 건은 기록 보완 권고다. anatomy 는 알려진 한계 목록에 들어가지 않은 오분절이 있고, extracted 는 미결 분류 글자가 다른 원장과 다르게 쓰였다. 둘 다 SKILL 종료 기준상 1차 종료를 막지 않는다. 보완은 해당 원장 폴더의 `issues.md` 에 한 절을 더하는 정도다. 같은 원장을 재조사할 필요는 없다.

원장 전체 완료는 다섯 모두 **아님**이다. 각 `issues.md` 의 B·I·P·F 미결과 의미 분해·정규화가 남아 있다.

## 1. 검토 방법과 범위 (전수 / 표본 / 자동 구분)

### 1.1 기계 대조 — 전수 (5개 모두)

`verify.py` 를 재사용하지 않고 별도 스크립트로 원본을 다시 열거해 대조했다. 원본은 `json.loads` 와 `object_pairs_hook` 로 읽었다.

| 대조 | 방법 | 결과(5개 모두) |
|---|---|---|
| 원본 해시·중복 키 | sha256 재계산, 중복 키 감지 | 발주 기록 해시와 일치 · 중복 키 0 |
| 구조 ↔ source-map | 전체 경로(컨테이너·말단·빈 컨테이너) 집합을 source-map `nodes[].pointer` 와 양방향으로 비교. 말단마다 값·자료형을 비교하고, 기록된 리터럴/값 구간(`span`·`literal_cp`·`literal_span`·`value_span`·`inner_file_span_cp`)을 원문에서 잘라 재파싱 | 누락 0 · 불필요 0 · 중복 0 · 값/자료형/구간 불일치 0 |
| coverage 구획 소유 | 구획별 소유 Pointer 합집합을 전체 경로와 비교(누락·초과·다중 소유). `owned_leaf_pointers` 가 있으면 말단 집합과도 비교 | 누락 0 · 초과 0 · 다중 소유 0 |
| 형태소 | 기록 값 = 원문 값. 토큰마다 `값[구간] == surface` 확인, 파일 구간이 있으면 `원문[파일구간]` 도 대조. 문자열 말단마다 분석 또는 제외 사유 확인 | 불일치 0 · 미처리 문자열 0 |
| 표현 | 표현 항목마다 `값[구간] == text` 확인, 파일 구간이 있으면 함께 확인 | 불일치 0 |
| 읽기 문서 원문 | 모든 말단(문자열·숫자·null)에 대해, 백틱으로 감싼 Pointer 가 있는 행 주변에 원문 값(`\|` 이스케이프 허용)이 있는지 확인 | 누락 0(5개 모두) |
| 목차·앵커 | coverage `review_file`·`review_anchor` 실재, `review.md` 에서 분할 문서로 가는 링크 확인 | §1.3 |

| 원장 | 노드 | 말단 | 자료형 | 구획 | 형태소 적용/제외 | 토큰 | 표현 항목 |
|---|---|---|---|---|---|---|---|
| anatomy-danger-zones | 615 | 483 | str 376 · int 22 · float 85 | 12 | 331 / 152(+필드명 74) | 4,273 | 1,330 (수동 352 · 정규식 568 · 절 410) |
| combo-recipes | 192 | 141 | str 113 · int 28 | 8 | 78 / 35 | 961 | 633 |
| consent-checklist | 376 | 306 | str 306 | 18 | 287 / 19 말단 + 필드명 9 | 3,770 | 929 |
| contraindications | 221 | 192 | str 192 | 2 | 109 / 83 | 741 | 292 |
| extracted | 958 | 719 | str 717 · null 2 | 18 | 648 / 71 | 9,940 | 3,907 |

빈 문자열·빈 배열·빈 객체는 다섯 원장 모두 0 이다. null 은 extracted 의 `/M10/safety/serious` 와 `/M13/safety/serious` 두 곳뿐이다. 이 둘은 `extracted/review.md` §2.1 의 별도 행(97행)과 형태소 제외(155행), B1 에 기록돼 있다.

### 1.2 verify.py 재실행 — 읽기 전용

`PYTHONDONTWRITEBYTECODE=1` 로 각 결과 폴더에서 실행했다. 출력은 스크래치패드에만 남겼다. 실행 전후 `git status` 가 같았고 `__pycache__` 도 생기지 않았다.

| 원장 | 종료 코드 | 결과 |
|---|---|---|
| anatomy-danger-zones | 0 | checks=34135 fails=0 · 해시 시작=끝 |
| combo-recipes | 0 | checks=92 failure_count=0 |
| consent-checklist | 0 | failure_count 0 · 해시 시작=끝 |
| contraindications | 0 | checks 77 · failed 0 · VERIFY PASS |
| extracted | 0 | checks=182 failures=0 · 해시 시작=끝 |

이 결과는 각 작업자가 만든 검사기가 통과했다는 뜻이다. 의미 정답을 보증하지 않는다.

### 1.3 coverage 구획 수·분할 문서·앵커 — 보고 수치 확인

| 원장 | 보고 | 실제 기록 | 목차 접근 |
|---|---|---|---|
| anatomy-danger-zones | 12 구획 | coverage 12(S00 루트 + zone 11) · `review-part-S00~S11.md` 12개 | `review.md` §구획 목차(204행)에서 12개 모두 링크 |
| combo-recipes | 8 구획 | 8(S0 + recipe 7) · 단일 `review.md` · `<a id="s0~s7">` | 목차 → 앵커 8개 모두 실재 |
| consent-checklist | 18 구획 | 18(S00 + category 17) · 단일 `review.md` | 목차 → `#s00~#s17` 모두 실재 |
| contraindications | 2 구획 | 2(S0 메타 + S1 rules 27) · 단일 `review.md` | 목차 링크 정상. coverage `review_anchor` 는 slug 가 아니라 제목 문자열이다(형식 비고) |
| extracted | 18 구획 · 17 분할 문서 | 18(S00 루트 + 항목 17) · `review-part-01-M10 … 17-M9.md` 17개 · S00 은 `review.md#s00-루트` | 17개 모두 `review.md` 에서 링크. `review-template.md` 는 build 입력 틀(`{{…}}` 자리표시자)이고 결과 문서가 아니다 |

상위 공유 문맥은 다섯 원장 모두 루트/배열 컨테이너를 첫 구획이 소유한다. 다른 구획은 `context_refs`·`shared_context`·`context` 로 참조만 한다. 소유와 참조가 섞인 곳은 없다.

**직접 읽음 상태는 작업자의 주장이다.** coverage·reading-log 의 `direct_read`/`read_status` 값과 읽기 기록은 실재한다. 하지만 기계 대응만으로는 실제로 읽었는지 증명할 수 없다. 내가 확인한 것은 기록이 있다는 사실, 그리고 아래 §1.4 범위에서 관찰 내용이 원문과 맞는다는 사실이다.

### 1.4 독립 읽기 검토 — 범위

| 원장 | 원본 읽기 | 결과 문서 읽기 |
|---|---|---|
| combo-recipes | **전수** — 7 recipe 전체 값 | issues.md 전체 · review.md 상태·컬럼·S0·S1 전체, 나머지 구획은 머리말·절 구조 |
| contraindications | **전수** — 27 rule × 7칸 + 메타 3 | issues.md 전체 · review.md 상태·컬럼·S0·rule 0~1, validation §5 |
| anatomy-danger-zones | **표본** — critical_safety_facts 전체, zone 11개의 등급 3칸, issues 가 인용한 값 약 15개 | issues.md 전체 · review.md 상태·컬럼 표 · review-part-S07 전체 · validation 읽기 검토 절 |
| consent-checklist | **표본** — I1·I3·I4·I5 인용 값, K01 대상 값 | issues.md 전체 · review.md 상태·컬럼·목차·S04 전체 |
| extracted | **표본** — M10 전체, M11 mechanism·uncommon, M9 contraindications | issues.md 전체 · review.md 상태·§2.1·관찰 일부 · review-part-01-M10 머리말·구조 |

anatomy·consent·extracted 는 **표본 읽기 검토**다. 전체 의미 검토로 보지 않는다. 표본에서 확인한 issues 의 원문 인용·구조 주장(예: anatomy 「danger_level = risk_level 11/11」, 「diffusion_range_cm 문자열」, 문장 중복 2쌍, consent I1·I3·I5, extracted M10 null·HIFES/HIFEM, M11 색소침착 진술)은 모두 원문과 맞았다.

미표시 오분절은 기계 휴리스틱으로 **전수** 탐색했다. 휴리스틱은 「한 어절 안에서 MAG·MM·NR·MAJ 토큰 바로 뒤에 붙은 명사」이고, 각 원장의 분절 표시 기록과 비교했다(§2). 이 휴리스틱 밖의 오분절은 탐색하지 않았다.

## 2. 원장별 결과

### 2.1 anatomy-danger-zones — WARN (1차 종료 가능)

- 결과: `first-pass/anatomy-danger-zones/` · 컬럼 표 `review.md` §전체 컬럼 구성(34행), 변형·선택 필드 §(123행) · 값은 `review-part-S00~S11.md` §원문 값, 관찰은 같은 파일 §잠정 관찰.
- 근거: §1.1·1.2 전부 통과. 구획 12개 모두 coverage 상 `done` 이고 분할 문서와 상위 문맥 참조가 있다. 숫자 리터럴(`3.0` 등)이 원문 그대로 실려 있다(A-fix-2). 원문 값 칸과 잠정 관찰 칸은 분리돼 있다.
- **수정 필요(추출 오류): 0.**
- **기록 보완 권고 — 미표시 오분절(알려진 한계에 추가)**. `segmentation_review` 는 직접 고른 낱말 64개만 대상으로 했다. 그래서 아래 출현이 K 목록과 review-part 분절 표에 없다. 교정은 요구하지 않는다. `issues.md` K 절에 위치·영향을 추가하면 된다.

  | 원시 토큰 | Pointer [값 기준 코드 포인트] | 영향 |
  |---|---|---|
  | 안/MAG + 동맥 | `/zones/0/vessels/1/danger` [0,3) 「안동맥」 | 부정 부사 「안」 오탐. consent-checklist 는 같은 오분절을 K01(high)로 기록했다 |
  | 이/MM + 신경 | `/zones/7/nerves/1/name` [0,3) · `/zones/8/nerves/0/name` [0,3) · `/zones/8/tissue_data/notes` [49,52) · `/zones/8/clinical_pearls/4` [12,15) · `/zones/8/filler_specific/primary_risk` [0,3) · `/zones/9/nerves/1/name` [0,3) | 「이신경」(이 = 턱)이 관형사 「이」+신경이 돼 부위어가 사라진다 |
  | 이/MM + 동맥 | `/zones/8/vessels/0/name` [0,3) · `/zones/8/clinical_pearls/4` [16,19) · `/zones/8/filler_specific/primary_risk` [15,18) | 같은 영향 |
  | 이/MM + 부 · 근 · 하부 | `/zones/8/botox_specific/risk` [25,27) · `/zones/8/botox_specific/safe_zone` [0,2) · `/zones/9/nerves/0/significance` [12,14) · `/zones/10/nerves/0/significance` [4,7) | 같은 영향 |
  | 이/MM + 개 | `/zones/2/nerves/1/name` [0,6) 「이개측두신경」 · `/zones/10/nerves/0/significance` [0,2) 「이개」 | 「이개」(귓바퀴)가 사라진다. 같은 형태의 `/zones/10/nerves/0/name`(대이개신경)은 K01 에 이미 있다 |
  | 거/MM + 상 | `/zones/7/botox_specific/dose_range` [24,26) 「거상」 | 관형사 오탐 |

- 분류 비고(선택): ADZ-F06 「관자궁」(`/zones/2/clinical_pearls/6`) ↔ 「관골궁」(`/zones/6/vessels/0/course`)은 같은 원장 안에서 표기가 맞지 않는다. 그래서 I 로 분류하고 F 를 함께 붙이는 편이 다른 원장의 I 기준과 맞는다. 원본은 고치지 않는다.
- 형식 비고: `review.md` 상태 표의 「읽기 검토」 칸에 작성자 자신의 재독이라는 점이 적혀 있지 않다(validation.md 읽기 검토 절도 같다). 내용상 과장은 아니다. 다른 원장처럼 「독립 검토자 아님」을 한 줄 넣기를 권한다.
- 알려진 한계: K01~K05(분절 117/249, 하안검 form 3, 범위 표기 36, 기호, 부정·가능성 범위).
- 열린 후속: I 4 · B 5 · P 11 · F 3 · C 0.

### 2.2 combo-recipes — PASS

- 결과: `first-pass/combo-recipes/` · 컬럼 표 `review.md` §컬럼 구성(30행) · 구획 S0~S7 각 §원문 값 / §잠정 관찰 (원문 아님) / §알려진 오분절.
- 근거: 원본 7 recipe 를 전수 읽어 대조했다. issues 의 B-1~B-10, P-1~P-8, F-1~F-7, I-1 인용은 모두 원문과 맞았다. A-4 에서 week 를 주·개월로 환산한 판정을 지우고 B-4 로 둔 처리는 SKILL 의 「단위 부여 금지」와 맞는다. 휴리스틱 후보 1건은 이미 표시돼 있었다(미표시 0).
- 수정 필요: 0. 분류 비고: B-6 「클」(`/recipes/2/repeatCycle`)은 원문이 잘렸거나 오기일 수 있다. 지금처럼 B 로 두고 원본 확인 후보로만 남겨도 된다.
- 알려진 한계: K-1~K-13(29출현) · 태그 비일관 · 필드명 SL.
- 열린 후속: B 10 · P 8 · F 7 · I 1 · C 0.

### 2.3 consent-checklist — PASS (형식 비고 1)

- 결과: `first-pass/consent-checklist/` · 컬럼 표 `review.md` §컬럼 구성(13행) · 구획 S00~S17 각 원문 표 + 「잠정 관찰」 표(원문 인용 칸 별도).
- 근거: §1.1·1.2 전부 통과. 표본 인용(I1·I3·I4·I5, K01)이 원문과 맞았다. 「안동맥 → 안/MAG」를 high 로 기록했다. 휴리스틱 후보 6건 중 미표시 3건은 「수일·수주·수개월」의 수/MM 인데, 이는 「몇」의 뜻이라 정상 분석으로 판단했다(오분절 아님).
- 형식 비고: 필드명 9개(전부)를 Kiwi 적용 대상에서 빼고 사유를 기록했다. 다른 네 원장은 필드명에도 Kiwi 를 돌려 SL 토큰을 남겼다. SKILL 이 허용하는 「분석 부적합 + 제외 사유 기록」에 해당하므로 막지 않는다. 원장 간 형식 차이로만 남긴다. KG4 「lemma 미제공, 만들지 않음」도 SKILL 기준에 맞는다.
- 수정 필요: 0.
- 알려진 한계: K01~K34(49출현) · KG1~KG4 · 표현 후보 표시 X01~X12, 공백 G01~G03.
- 열린 후속: B 5묶음 · I 6 · F 8묶음 · P(관찰 표) · C 0.

### 2.4 contraindications — PASS (형식 비고 1)

- 결과: `first-pass/contraindications/` · 컬럼 표 `review.md` §컬럼 구성 표(29행) · S0(49행) · S1 rule 별 `### /rules/N` 원문 표 + 「직접 읽기 표현」 + 「잠정 관찰 (원문 아님)」.
- 근거: 원본 27 rule 을 전수 읽어 대조했다. level 집계(caution 14 · safe 8 · warning 5), from/to ID 집합, M10 부재, I1~I3, P2(같은/반대 순서 rule), P4·P6, B3·B4·B6 인용이 모두 원문과 맞았다. 「드물게」류 빈도어가 이 원장에 없다는 진술도 맞다. 휴리스틱 후보는 0건이었다.
- 구획 2개는 원장이 6,390 bytes 라 적절하다. S1 하나가 189 말단을 소유하지만 rule 단위 소제목으로 나눠 읽혀 있다.
- 형식 비고: coverage `review_anchor` 값이 `#slug` 가 아니라 제목 문자열(「S0 · 최상위 메타데이터」)이다. 목차 링크(`#s0--최상위-메타데이터`)는 정상이라 접근에는 문제가 없다. rule 0 관찰의 「반대 순서: rule 3·6·13」에는 rule 2 가 빠져 있다. issues P2 에는 들어 있다.
- 수정 필요: 0.
- 알려진 한계: K1(23출현) · K2~K4.
- 열린 후속: B 6 · I 3 · P 7 · F 6 · C 0.

### 2.5 extracted — WARN (분류만 · 1차 종료 가능)

- 결과: `first-pass/extracted/` · 컬럼 표 `review.md` §2.1 컬럼 구성 표(85행), §2.2 객체 키 구성 변형(132행), §2.3 형태소 적용·제외(145행) · 값은 `review-part-NN-M*.md` §1 모든 값, 관찰은 §2, 오분절은 §4.
- 근거: §1.1·1.2 전부 통과. null 2개가 컬럼 표·제외·B1 에 반영돼 있다. 상태 표가 「자체 판정 · 독립 검토 전」이라고 정직하게 적었다. 휴리스틱 후보 9건 중 미표시 4건은 수/MM(수주·수개월~수년), 이/MM 「이때」(정상 분석), 「뾰족턱」 뾰족/MAG(품사만 다르고 구간 손실 없음, K2 성격)이다. 기록 보완은 선택 사항이다.
- **분류 보완 권고(종료 차단 아님):** 아래 I 항목은 값끼리 서로 맞지 않는 사례가 아니다. **필드 이름과 내용의 성격이 다르다는 에이전트 해석**이다. anatomy 는 같은 종류를 ADZ-P22(P)로, consent 는 F8(F)로 분류했다. P(또는 F)로 옮기기를 권한다.
  - I6 (`/M1/safety/serious/1` 외) — safety 칸 안의 비사건 진술
  - I7 (`/M13/onset_duration/duration`) — duration 칸의 비기간 진술
  - I8 (`/M15/contraindications/absolute/0` 외) — contraindications 칸의 비환자조건 진술
  - I9 (`/M8/safety/uncommon/0`) — uncommon 칸 안의 「흔함」(그룹 이름과 값의 대조)
  - I11 (`/M3/safety/serious/1`) — 바이오스티뮬레이터 항목의 필러 위험
  - I13 (`/M5/aftercare/2`, `/M5/indications/extended/3`) — 칸 안의 병합 권고

  값끼리 실제로 맞지 않는 I1·I2·I3·I5·I10·I12 는 I 로 둔다. I4(한 값 안 시점 혼재)는 경계 사례라 작성자 판단에 맡긴다.
- 수정 필요(추출 오류): 0.
- 형식 비고: `review-template.md` 는 build.py 가 읽는 자리표시자 틀이다(batch-01 complications·synergy 와 같은 방식). 목차에 링크되지 않아 혼동 위험은 작다.
- 알려진 한계: K1(34출현·규칙 20) · K2~K5. 3회차 대조 범위 밖 토큰의 정확성은 보장하지 않는다고 스스로 밝혔다.
- 열린 후속: B 10 · I 13(재분류 시 감소) · P 4 · F 11 · C 0.

## 3. 미결 분류 대조

로컬 문서의 문자 뜻은 원장마다 조금씩 다르다(A·B·C·I·P·F·K). 건수를 합산하지 않았다. 의미 기준으로만 대조했다.

- **원문 부족(B)으로 위장한 에이전트 과제:** 찾지 못했다. 다섯 원장의 B 는 모두 「원문에 무엇이 없는가 + 제한되는 판단」 형태다. combo B-1(M 코드 대응)은 원장 안에서는 원문 부족이 맞다. 다른 원장과 연결하는 일은 F-4 로 따로 분리돼 있다.
- **사용자에게 불필요하게 넘긴 항목:** 없다. 다섯 모두 C 0 이고 근거 절이 있다. 원본 변경 제안을 선택 대기로 올린 곳도 없다(원본 보존 지시와 맞다).
- **I 와 C 구분:** 다섯 모두 원문 내 불일치를 C 로 올리지 않았다. 경계가 다르게 쓰인 곳은 extracted 의 필드-내용 성격 판단(§2.5)과 anatomy F06(§2.1) 두 곳이다.
- **해결로 센 미결:** 없다. A 는 수정·재검증 기록이 있고, B·I·P·F 는 모두 열림으로 표시돼 있다.

현재 사용자 선택이 필요한 항목은 **0** 이다.

## 4. 원장 간 차이 — 후속 비교 후보로만

통합 의미를 확정하지 않는다. 비교 단계에서 볼 자리를 적어 둔다.

- 같은 오분절이 원장마다 다른 등급으로 기록됐다: 「안동맥 → 안/MAG」는 consent K01(high), anatomy 는 미표시.
- 필드명을 형태소 분석에 넣었는지가 다르다: consent 는 제외, 나머지는 Kiwi SL 토큰.
- 구간 기준 표기가 다르다: anatomy·combo·extracted 는 `span`(값 기준) + `file_*span`, consent 는 `start/end`, contraindications 는 `span_cp`·`file_span_cp`. 모두 코드 포인트 `[start,end)` 로 명시돼 있고 재현된다.
- level/등급 체계: contraindications `level`(safe·caution·warning), anatomy `danger_level`/`risk_level`(2~5), consent·extracted 의 absolute/relative 구분. 모두 척도 정의가 없다는 B 로 남아 있다.
- 기호 「+」「/」「→」의 용법이 README 규칙과 다르다는 관찰이 다섯 원장에 모두 있다(ADZ-P09·P10, combo F-3, contraindications P3, extracted P3, consent B5).

## 5. 종료 가능 여부와 요청

| 원장 | 1차 범위 종료 | 반드시 고칠 것 | 권고(선택, 종료 전후 무관) |
|---|---|---|---|
| anatomy-danger-zones | 가능 | 없음 | `first-pass/anatomy-danger-zones/issues.md` K 절에 §2.1 표의 미표시 오분절 17출현 추가 · 읽기 검토가 작성자 재독임을 명시 · F06 → I 병기 |
| combo-recipes | 가능 | 없음 | — |
| consent-checklist | 가능 | 없음 | — |
| contraindications | 가능 | 없음 | (선택) coverage `review_anchor` 를 `#s0--최상위-메타데이터`·`#s1--rules-전체` 형식으로 |
| extracted | 가능 | 없음 | `first-pass/extracted/issues.md` I6·I7·I8·I9·I11·I13 을 P(또는 F)로 재분류 |

이 판정은 1차 수집 계약 충족 여부에 대한 것이다. **다섯 원장 모두 원장 전체 완료가 아니다.** 의미 조사·공통 모델·실버 변환은 별도 단계다.
