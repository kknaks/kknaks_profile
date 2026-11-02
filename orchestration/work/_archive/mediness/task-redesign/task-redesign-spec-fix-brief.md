
# [planner] 재발주 R2 — 리뷰 FAIL 6건 정정 (폐기 개념 잔존 스윕)

너는 앞서 task·incident 재정비 스펙을 작성한 **mediness `planner` 워커**다. reviewer_spec 검수에서 **FAIL** 이 났다 — 산출물 자체는 결정 SoT 정합 통과인데, **네가 손대지 않은 주변 SPEC 에 이번 라운드가 폐기한 개념이 활성 계약으로 잔존**한다.

리뷰 리포트(필독): `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/review-spec-report.md`

워크트리·allowed_paths·완료 보고 방식은 원 브리프와 동일 (`task-redesign-spec-brief.md`). **이번 taskId/dispatchId 는 이 dispatch 의 preamble 값을 쓴다.**

## 고칠 것 — FAIL 6건 (근거 = 리포트)

- **V-1** `spec-150:578` — `/decline` endpoint 활성 잔존 → 제거/폐기 정정
- **V-2** `spec-155:847` — 「재배정된 task 는 수신자의 수락 대기로 선다」 = 결정 SoT(재배정=todo 리셋) 정면 위반. `:795` 도 함께 정정. 인용 대상 SPEC-154 §4.8 과 일치시켜라
- **V-3** `spec-155:537/609/670/834-841/860` + `spec-060:56/240/445` — decline REST·MCP 툴·카운트 활성 잔존 (WP-124 P5 가 지우려는 대상인데 SPEC 이 살아 있음 = SPEC→WP 역방향) → 폐기 정정
- **V-4** `spec-230:95/316/318/319` — 수락 대기 칩·「여섯 상태」 → 5값으로 정정
- **V-5** `spec-154:715·2357` — `accepted_at` 이 같은 파일 `:754` 폐기 선언과 모순 → 구 서술 삭제 («개정=추가+구 서술 grep 삭제» 절차 준수)
- **V-6** `spec-150:567` — D-13 `/slack/complete` 잔존 → 제거

## 함께 정정 — WARN 2건

- **W-1** `20-spec.md:133/200` — SPEC-152 제목 미동기 (에러 트리거 기반으로)
- **W-2** WP-124 `covers` 에 SPEC-031(P6)·110/113(P7) 추가 + 30-work.md Spec Coverage 동기

## 코디 판단 (W-4)

`decision-tracking-engine.md`·`spec-113` 의 `is_required` 게이트는 **A축(폐기 예정 원장) 소유이므로 지금 지우지 않는다.** 대신 두 문서의 해당 절에 「A축 폐기 계획(decision_execution_task.md §이관·폐기)과 함께 소멸 예정」 표기가 이미 있는지 확인하고, 없으면 한 줄 폐기 예정 노트만 단다. W-3(21-html 시안)·W-5(spec-125:616 의도된 동형 서술)는 손대지 않는다.

## 검증

1. 정정 후 **폐기 키워드 grep 스윕 재실행** — `accept_pending`·수락 대기·`decline`·`task_declined`·`accepted_at`·`/slack/complete` 가 products/mediness/ 에서 활성 계약으로 잡히면 안 된다 (개정 이력·«폐기됨» 명시문·동결 work-074·A축 폐기 예정 문서는 허용)
2. `python3 scripts/lint-pipeline.py --strict` — mediness 범위 ERROR 0
3. 리포트 말미 「재검수용 8항목 체크리스트」를 스스로 통과시켜라

## 하지 말 것

- 원 브리프의 범위 제약 전부 유지 (코드 레포 수정 금지 · WP2 작성 금지 · 결정 SoT 밖 발명 금지)
- 이번에 통과한 산출물(도메인 문서 2건·ERD·WP-124 본문·spec-152)을 불필요하게 다시 고치지 마라 — 정정 범위는 위 목록이다

완료 보고는 원 브리프 §9 와 동일한 2채널. taskId/dispatchId 는 **이 dispatch 의 preamble** 값.
