# batch-01 최종 메모 — 기록·분류 보완 (코디 확인 전)

- 작성: Opus writer · `task_13017333a603` / `ctx_b00064993d59` · 2026-11-09
- 근거: [batch-01 묶음 검토](./batch-01-review.md) §3·§5, [브리프](./batch-01-final-brief.md)
- 범위: 검토가 지적한 위치·문서만 원문·결과 파일과 대조해 **기록·분류만** 고쳤다. 원장 재조사, 의미 모델 설계, 후속 판단 확정, 후보 보충, 새 JSON 생성은 하지 않았다. 원본·JSON·스킬·검토 리포트·발주 기록·procedure-profiles 는 건드리지 않았다. 커밋하지 않았다.

## 0. 결론

| 원장 | 1차 수집 범위 | 원장 전체 | 이번 반영 |
|---|---|---|---|
| products | 종료 가능(검토 PASS) · 코디 확인 전 | **완료 아님** | B5·B6 분류 병기 |
| procedure-comparison | 종료 가능(PASS) · 코디 확인 전 | **완료 아님** | 상태 줄을 review·validation 맨 위로 |
| complications | 종료 가능(WARN, 막지 않음) · 코디 확인 전 | **완료 아님** | 카테고리 id·name Pointer 행, A 보충 기록 |
| treatment-sequence | 종료 가능(PASS) · 코디 확인 전 | **완료 아님** | B1 잠정 해석 병기, C1·C3·C5·C6 후속 과제로 |
| synergy | 종료 가능(WARN, 분류만) · 코디 확인 전 | **완료 아님** | U1·U2 재분류, 「전층」 한계 기록 |

batch-01 의 **현재 사용자 선택 대기는 0건**이다. 미결이 닫혔다는 뜻은 아니다. 이번 작업으로 사용자 결정을 받은 항목은 없다.

## 1. 지적별 반영

| # | 지적(검토 §) | 반영 경로 | 상태 |
|---|---|---|---|
| 1 | products B5 = 외부 사실 확인(§3.1) | `first-pass/products/issues.md` B5 아래 병기 행 · 요약 B 행 | 반영. B 번호·7묶음 유지 |
| 2 | products B6 일부 = 해석 과제, F2·F3 와 겹침(§3.1) | 같은 파일 B6 아래 병기 행. 원문 단서 「뉴메코(Newmeco, 메디톡스 계열)」를 원본에서 확인했다. 단서가 없는 부분(앨러간/애브비)은 원문 부족 그대로 | 반영. 해석은 확정하지 않음 |
| 3 | procedure-comparison 상태 줄 맨 위·「코디 확인 전」(§3.2) | `review-template.md` + 생성 `review.md` 제목 바로 아래, `validation.md` 맨 위. §7 원래 표시는 그대로 | 반영 |
| 4 | complications 카테고리 id·name 개별 Pointer 행(§3.3-1) | `build.py` 카테고리 제목 뒤에 `\| id \| /categories/N/id \| … \|`·`name` 행 생성 4줄 추가 → `review.md` 에 반영. 값은 원본에서 확인. **카테고리는 0~9 의 10개**라 20값이다(검토 문구 「1~9 · 18값」보다 2값 많다. `/categories/0` 도 같은 형식이 아니었다) | 반영 |
| 5 | complications 미표시 오분절 2출현(§3.3) | `issues.md` 「A 보충」 표: `/categories/6/complications/2/risk_factors/4` [8,10) 시/NNB+술/NNG · `/categories/7/complications/1/incidence` [37,39) 전/NNG+층/XSN(같은 값의 T15-01 「동상」과 별개) | 위치 기록. **토큰은 교정하지 않았다** — 원시 출력 그대로이며 A1 107출현 집계에 들지 않는다 |
| 6 | complications 「삽입 깊이」 구절 후보 한계(§3.3-2) | 같은 표: `/categories/3/complications/5/prevention` [3,8). 이 값의 후보는 E02039(값 전체)·E02040~E02043 뿐임을 확인 | 한계 기록. 후보 보충 안 함(후속) |
| 7 | complications 같은 구간 57쌍(§3.3-3) | 같은 표: `expressions.json` 을 다시 세어 57쌍 = keyword+keyword 49 + keyword+regex `'…시'` 8(모두 「필요 시」), 셋 이상 묶음 0. 영향: 범주별 후보 수가 57만큼 부풀려짐. 「완전 중복 0」은 method·keyword 를 넣은 비교 | 기록. **의도된 겹침인지는 확정하지 않았다**(검토 관찰과 재계산 사실만) |
| 8 | treatment-sequence B1(§3.4) | `issues.md` B1 · `review-notes.md` + 생성 `review.md` 의 `/minimum_intervals/2` 잠정 관찰 행. 원본 reason 확인 | 「하한 0 잠정 해석(확정 아님) + 숫자 칸 단독 사용 위험」 병기. 원문 부족 관찰 유지 |
| 9 | treatment-sequence C1·C3·C5·C6(§3.4·§4) | `issues.md` 요약 C 행 · §C 머리글 · §E | 「후속 비교 뒤 사용자 결정 후보」 → 후속 의미 조사·원장 간 비교 과제(C1·C3=D4, C5=D2·D3, C6=D6). 실제 원본 수정 제안이 생길 때만 사용자에게 묻는다고 적음. §C 불일치 관찰 표는 그대로 |
| 10 | synergy U1·U2 재분류(§3.5) | `issues.md` 머리 분류·요약 U 행·§U(재분류 문단 + 「현재 분류」 행)·F1 근거 · `review-template.md` + 생성 `review.md` §0 「열린 미결」·§9 · `validation.md` 맨 위·§6 | U1 → F1 후속 의미 검토 후보, U2 → 실버 변환 규칙 검토 후보. U 번호·원문·이유·선택지·영향 그대로. 현재 선택 대기 0. 삭제·수정 승인/방향 확정 아님 |
| 11 | synergy `/links/55/reason` [35,37) 「전층」(§3.5) | `issues.md` A' · `review.md` §0 「알려진 분석 오류」 행 | 알려진 한계로 기록. 원시 토큰 전/MM+층/NNG 미교정. 이 출현은 `pos_review` 에 작성자 판정 `verdict: ok` 로 이미 있고, 그 판정은 고치지 않고 함께 적었다 |

**반영하지 않은 것(브리프 계약 밖):** complications B4·B8, procedure-comparison B9·B6 의 분류 비고(검토 §3.2·§3.3)는 이번 브리프 §3 에 없어서 손대지 않았다. 검토도 이 둘을 「지금 분류도 받아들일 수 있다」·「표시하기를 권한다」 수준으로 적었다.

## 2. 검증 (실제 실행)

| 확인 | 결과 |
|---|---|
| verify.py 5개(읽기 전용, `PYTHONDONTWRITEBYTECODE=1`, 레포 루트) | products exit 0 · failure_count 0 · procedure-comparison exit 0 · failure_count 0 · complications exit 0 · failure_count 0(check_runs 89,629) · treatment-sequence exit 0 · checks 32 failure_count 0 · synergy exit 0 · failure_count 0 |
| 원본 해시 | `phub-recommend/bronze/phub-ledger/` 24파일 sha256 변경 전후 동일 |
| first-pass 전체 88파일 | 바뀐 파일 15개, 모두 `.md` 이고 하나만 `complications/build.py` 다. **JSON 0개 변경.** `__pycache__` 없음 |
| 생성 원고 ↔ 실제 Markdown | 실제 트리에서는 build 를 돌리지 않았다. 대신 scratchpad 에 complications·procedure-comparison·treatment-sequence·synergy 폴더를 복사하고 원본 디렉토리를 심볼릭 링크로 걸어 각 build.py 를 실행했다(Kiwi 0.24.1). 생성된 전 파일(review.md·source-map·morphology·expressions·build-output 등)이 실제 트리 파일과 **바이트 동일** → 재생성해도 이번 보완이 유지되고 JSON 은 그대로다. products 는 생성물(review.md)을 바꾸지 않아 생략 |

바뀐 파일: products `issues.md` · procedure-comparison `review-template.md`·`review.md`·`validation.md` · complications `build.py`·`review-template.md`·`review.md`·`issues.md` · treatment-sequence `issues.md`·`review-notes.md`·`review.md` · synergy `issues.md`·`review-template.md`·`review.md`·`validation.md` · 그리고 `_RESUME.md`, 이 메모.

## 3. 남은 것 — 구분

- **1차 수집:** 다섯 원장 모두 종료 가능 판정이고 이번에 기록·분류를 맞췄다. 최종 확인은 코디가 한다.
- **원장 전체:** 다섯 모두 **미완료**다. 아래 항목이 열려 있다.
- **알려진 분석 한계(교정 안 함):** products K 32 · procedure-comparison A1~A4 · complications A1~A4 + 미표시 오분절 2·「삽입 깊이」 후보 한계·같은 구간 57쌍 · treatment-sequence A2 69·A3 19 · synergy A' + 「전층」 1. 표시·기록 밖 토큰의 정확성은 보장하지 않는다.
- **원문 부족:** products B 7(B5 외부 사실 확인, B6 일부 해석 과제 병기) · procedure-comparison B 9 · complications B 9 · treatment-sequence B 10(B1 잠정 해석 병기) · synergy B 10.
- **잠정·원문 내 불일치:** products P 2 · complications P 4 · treatment-sequence C 8(관찰 유지) · synergy P 5.
- **후속 의미 조사·검토 후보:** products F 7 · procedure-comparison F 7 · complications F 9 · treatment-sequence D 8(C1·C3·C5·C6 포함) · synergy F 10 + U 2(U1 → F1, U2 → 실버 변환 규칙).
- **현재 사용자 선택 대기:** 0. 실제 원본 수정 제안이 필요해질 때만 사용자에게 올린다.
