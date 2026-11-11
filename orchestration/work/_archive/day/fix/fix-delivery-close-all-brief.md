# [planner] Delivery 다섯 건 닫기 — #241 · #234 · #235 · #236 · #239 (실물 검증은 다음 작업으로)

너는 day planner 워커(같은 터미널)다.

## 사용자 결정 (2026-11-11 — 이것이 승인 근거다)

- 「아 그럼 스테이블에 올리고 다 닫자」
- 「다음 작업이라고, 이제 다 한 거잖아. **검증은 다음에 하자니까.** 닫는 데 문제가 있어?」
- 다음 작업 = 「웹 버그 수정 · prod 배포 · 앱 일부 작은 수정 · 문서 정리」(실물 검증이 여기로 간다)

→ **Delivery 다섯 건을 전부 닫는다.** 구현은 전부 머지 · dev 배포됐다. 아직 하지 않은 **실물 검증**(사용자 실기기 · TestFlight · 데모 지점 실물 · APNs 실수신 등 「사람이 실물에서 봐야 하는」 수용 항목)은 각 Delivery 의 결과 계약 **범위에서 빼** 「다음 작업의 검증으로 넘김」으로 기록하고 닫는다.

## 사실 (코디 확인)

- 스펙: mediness `origin/main` = **`19f7e401`**(#931 DAY-SPEC-002 stable) — 그 앞 `caf7f3eb`(#930 SPEC-000 stable) · `1a450bcf`(#929 3차 스펙). **DAY SPEC 000 ~ 005 전부 stable.**
- 코드: 2차 = PR #238 → `dev` 스쿼시 `aa7853cd`(head `b8a59cc3`) · 3차 = PR #242 → `dev` 스쿼시 `7b099e8f`(head `87cf2dec`) · 둘 다 dev 배포 성공.
- #241 은 v6 로 `spec-baseline:ready`(네가 함).
- 3차 실물(코디 · dev 서버): 통역 사전 로그 · 저장소 올리기 → 크기 → 전체/범위 읽기 → 경로 → 없는 키 → 지우기 통과 · api 오류 로그 0. 실제 Soniox(워커): 7개 언어 ready · ko ↔ zh-Hant 왕복 · 멈춤 35초 뒤 두 번째 발화 · 로컬 키 비움 `no_api_key` · 권한 없는 계정 403. TestFlight DAY Dev 0.1.0 (2) 업로드 · VALID · 수출 규정 자동(코디 ASC 재조회).
- 근거 리포트(3차): `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/` 의 `be-*-report.md` · `app-*-report.md` · `review-*-report.md` · `app-testflight-upload-2-report.md`. 2차 근거: `…/orchestration/work/_archive/day/day-procedure-board-2/` · `_archive/day/day-app/` 의 리포트 · 회고 `para/projects/company/day/log/2026-11-11-*.md`.

## 할 것 — Delivery 마다 (순서: #241 → #234 → #236 → #239 → #235)

레포 Skill · 규칙(`start-delivery` · `review-delivery` · `spec-sync` · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`)대로, 네 `spec-stable-report.md` 의 단계표를 따른다.

1. **범위 정리(scope delta)** — 실물 검증 수용 항목을 범위에서 뺀다. 뺀 항목은 Non-Goals 나 후속 표기에 「다음 작업(웹 버그 수정 · prod 배포 · 앱 작은 수정 · 문서 정리)의 검증으로 넘김 — 사용자 2026-11-11」로 **무엇을 뺐는지 항목 그대로** 남긴다. **구현 범위(Target Delta)는 늘리지도 줄이지도 않는다.** 시험 · 리뷰 · 코디/워커 실물로 근거가 있는 항목은 빼지 않는다.
2. **baseline 재결속** — 새 `origin/main`(`19f7e401`)으로. `missing_target_specs = []` 확인.
3. **승인** — 계약이 바뀌었으니 새 plan_digest 에 receipt `{decision: approved, reviewer_type: human, reviewer: kknaksss}` 를 적용한다(근거 = 위 사용자 결정). 위험 등급이 올라가거나 구현 범위가 달라지면 승인하지 말고 멈춘다.
4. **review-delivery** — 남은 수용 항목 **전부**에 결과와 근거를 단다. **근거가 실제로 있는 것만 `pass`**: 시험 수치 · 리뷰 판정 · 코디/워커 실물 확인 리포트(위 경로의 파일 이름 · 줄). 근거를 못 찾은 항목이 남으면 **`pass` 로 적지 말고** 그 항목도 「실물/후속으로 넘길 것」인지 판단해 1 로 돌아가거나(같은 사용자 결정의 범위 안일 때), 아니면 멈추고 보고한다. per_spec 판단은 구현과 스펙을 실제로 대조해 정한다(추측 금지).
5. **spec-sync** — 도구가 문서 sync PR 을 만든다(이 단계의 커밋 · push · PR 생성은 도구가 하는 것이므로 허용). PR 이 열리면 **코디에게 알리고 머지를 기다린다**:
   `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[sync PR] planner: Delivery #<번호> sync PR mediness#<PR> 열림 — 머지 요청" --enter`
   코디가 스쿼시 머지하고 `[머지됨] #<PR> <sha>` 를 보낸다. sync PR 은 「Delivery 당 최대 하나」 규칙을 지킨다. 앞 Delivery 의 sync PR 이 머지되면 `origin/main` 이 움직인다 — 다음 Delivery 는 그 새 revision 으로 묶는다.
6. **닫기** — `complete-delivery`. 닫힌 뒤 Issue 상태 · 라벨을 재조회한다.

## 멈추는 곳 (우회하지 않는다)

- 도구가 거절하는데 규칙 안에서 풀 길이 없을 때 · 위험 등급/구현 범위가 달라질 때 · 근거 없는 수용 항목을 `pass` 로 적어야만 넘어갈 때 · #235 처럼 수용 항목이 많아(53) 다른 Delivery(#241)가 뒤에 바꾼 계약과 부딪혀 판단이 갈릴 때 — 그 Delivery 는 **멈추고 상태를 보고**하고 **다음 Delivery 로 넘어간다**(하나가 막혀도 나머지는 닫는다).
- 안 한 확인을 한 것으로 적지 않는다. 뺀 항목 목록이 다음 작업의 검증 목록이 된다.

## 하지 말 것

- 스펙 내용 수정(도구의 sync 가 만드는 변경 제외) · 코드 수정 · MCP Task 카드 처리 · 값(키 · 계정 이름 · 주소) 기재.
- request · 결과 파일은 `…/work/fix/delivery/` 에 Delivery 번호별로 복사해 둔다(네 scratchpad 는 아카이브 때 사라진다).

## 보고

**Delivery 하나가 닫히거나 막힐 때마다** 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/delivery-close-all-report.md` 에 한 절씩 덧붙인다(워커가 죽어도 남게): 번호 · 뺀 수용 항목(그대로) · 남긴 항목과 근거 · contract_version · plan_digest · sync PR · 최종 상태(닫힘 / 막힘 + 이유).

전부 끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "닫힘 N / 막힘 N(번호 · 이유) / 다음 작업으로 넘긴 검증 항목 수"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
