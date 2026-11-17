
# 재개 노트 — fix-feedback (day)

**지금**: planner 완료(spec-report.md · 스펙 미커밋 5파일 · lint 0 error 코디 확인 · Delivery #254 L2 승인 대기 — v2 재결속 뒤 승인). review-doc-1 = WARN(FAIL 0 · 착수 막는 OQ 기본값 없음) → spec-2 완료(기본값 18 · 정렬 쿼리 `sort=room` · lint 0 error 코디 확인) → review-doc-2 WARN(FAIL 0 · D1 undo-home 응답 = 판 전체 다시 받기 · sort 는 GET 쿼리만 — 브리프에 박음) → be · fe 완료(be-1 · fe-1 · not-infra 948 passed · infra 13 pending — Docker 꺼짐) → review-code-1 WARN(FAIL 0 · W1 infra 13 미실행 · W2 알림 prime 실패 시 쏟아짐 · W3 conflict 글자 · W5 · W6 · W8 스펙 반영 · W4 · W7 · W9 수용/사소). Docker 복구(디스크 가득으로 엔진 crash · 죽은 backend 프로세스 kill 후 재시작) → 코디 직접: infra 13 passed · 전체 1281 passed · day-local 을 fix-feedback 코드로 재빌드(`docker compose -p day-local -f <코드 워크트리>/deploy/compose.local.yaml --env-file ~/git/CENTURION_DAY/deploy/local.env --profile app up -d --build --wait` · http://127.0.0.1:11040 · migration 없음) → 사용자 E2E 1회차 끝(E1 ~ E6 · F-5 포함 결정) → 2루프 끝(spec-3 · 4 · review-doc-3 FAIL 1(문서 한 줄 · PR 전 정리) · be-2 · fe-2 · review-code-2 WARN(N1) · be-3 N1 고침) · 코디 전체 1298 passed · day-local 재빌드(14:58) → **사용자 E2E 2회차 대기**. 완료 알림이 코디를 못 깨우는 일 반복 — 발주 뒤 직접 확인할 것. 호출 취소 KOS HAR 사용자에게 요청함(없으면 「정할 것」). 2루프 = E2E 피드백 + W2 · W3 · (W5 · W6 · W8 스펙) 한 묶음. 사용자 확인 대기 2: F-4 원장 계정 웹에서만 뜸 OK? · F-1 KOS 되돌리기 HAR. F-5 는 사용자가 뒤에 추가
**다음**: 사용자 「로컬 E2E 할 수 있게 코드 구현까지」(11-17) — planner 완료 → reviewer_doc 검수(FAIL 이면 재발주) → be · fe 발주(묻지 않음) → reviewer 코드 검수 → 로컬 스택 준비 · 사용자 E2E. Delivery 승인 · PR 머지는 E2E 뒤 사용자(fix-web 과 같은 순서)

세팅: `scripts/new-work.sh day fix-feedback` · 설정 SSOT `config/projects/day.json`
코디handle: `term_94fbe396-828d-4fa4-8bd8-829294f10614`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- 코디: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback`
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec` (브랜치 `kknaksss/fix-feedback-spec` · base origin/main `c3639503`)
- 코드: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` (base origin/dev `4f8316a7`) — be · fe 브리프는 깔아만 둠



## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [ ] 스펙 마무리(코드 뒤 · PR 전 · planner 한 판): review-doc-3 F1(spec-005:444 migration 문장 취소선 — be 브리프에 「알림 · migration 없음」 고정으로 대신하고 코드 진행) · W1(spec-005:34) · W2(spec-003:70) · W4(규칙 38 원래 알림으로 수락 결과) · W3(log 그대로 · PR 본문) · 그리고 옛 항목: review-doc-2 D1(spec-002 :586 undo-home 응답 = 판 전체 다시 받기 · :584 sort 는 GET 만) · D2 · D3(log.md:17 PR 칸) · D4(옛 room.order) — 구현 방식 확정 뒤 planner 한 판
- [ ] be · fe 완료 → reviewer 코드 검수 → 로컬 스택 준비 · 사용자 E2E
- [!] **새 항목(범위 밖 · 11-17 E2E 중 발견)**: KOS 로그인 기기 제한 — sign-in 401 `SignInLimitExceeded`(errorProperties user reason 10) · `maxSignInCount` 5 · 조회 `common/user/v1/queries/get-active-sign-ins` · 해제 `common/user/v1/commands/revoke-active-sign-in`(email · password · signInId). DAY 는 sign-in 400/401 을 전부 「비밀번호 틀림」으로 처리(`emr/kos/staff_client.py:88-90`) · 다른 기기 로그인에 밀린 직원 토큰 401 → 세션 종료 · 시스템 계정(동기화)도 같은 제한. 11-17 코디가 사용자 요청으로 시스템 계정의 52.231.77.47(DAY 서버) 외 로그인 3개 해제. 근거 HAR `~/Downloads/기기로그인.har`(비밀번호 평문 포함 — 레포에 넣지 않음)
- [!] F-5(더보기 → 이전 단계 되돌리기)는 보류 — 사용자가 더 줄 것이 있음

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-17 | F-1 귀가 대기 취소 = 단순 되돌리기(이전 상태 = 완료로 복귀) · ⋮ 더보기에. F-5 와 묶지 않음 | 사용자 |
| 2026-11-17 | F-2 탭 [시술순 \| 방별순] — 시술순 = 오더지 순 · D&D / 방별순 = 룸 오름차순 · D&D 없음 · 빈방 제외(다음 스펙) | 사용자 |
| 2026-11-17 | F-3 버튼 이름 = 「바로 시작」(일괄 시작 아님). 시작 규칙은 조사 뒤 논의 | 사용자 |
| 2026-11-17 | F-4 웹 알림 = B 까지(탭 열림 · OS 알림) · 원장 호출만 · 원천은 기존 알림 행. 웹 푸시(C)는 다음 스펙 | 사용자 |
| 2026-11-17 | F-5 보류 | 사용자 |
| 2026-11-17 | F-6 작성된 차트만 아이콘 · 미작성 표시 안 함 · 모든 영역 같은 규칙 | 사용자 |
| 2026-11-17 | F-7 간호 · 관리 · 기타 = 대리 수락(그대로) / 원장 계정 = 로그인 계정이 집도의로 바로 수락 | 사용자 |
| 2026-11-17 | F-3 = 「선택한 줄 바로 시작」(일괄 시작이라 부르지 않음). 집도의 없는 시술(예: 마스크팩)이 실제로 있다 → 지금 규칙(집도의 있어야 시작 · `no_doctor`)으로는 부족. 넓히는 방식(B 준비중 전부 / C 시술별)은 더 논의 | 사용자 · research-1 |
| 2026-11-17 | F-3 = 바로 시작은 집도의 없이도 된다 — 선택한 준비중 줄에 KOS 집도의가 있으면 그대로 시작, **없으면 병원 시스템 계정을 KOS 집도의로 쓰고(`change-tasks-doctors`) 시작**. 시스템 계정이 KOS 집도의로 남는 것 괜찮음. 11-09 「원장 없이 시작 없음」(SPEC-002 U-7)을 이 방식으로 뒤집는다 | 사용자 · HAR `~/Downloads/시스템배정.har`(호출 없이 `change-tasks-doctors`[시스템 계정] 200 → `change-tasks-complete` 200 · 사용자 관찰: 의사 배정하면 KOS 바로 진행중 · 시스템 계정은 관리자라 배정 가능). HAR 은 토큰이 있을 수 있어 레포에 넣지 않음 |
| 2026-11-17 | F-4 웹 OS 알림은 **늘 띄운다**(탭이 앞이어도 · 다른 모니터여도) — 기본값 OQ-N9 「document.hidden 일 때만」 뒤집음 | 사용자(E2E E5) |
| 2026-11-17 | F-5 = E4 정의(준비중 ⋮ 없음 · 호출 → 호출 취소 + 취소 알림 · 진행중 → 시작 취소 · 완료 → 완료 취소) · 2루프에 포함 | 사용자(E2E E4) |
| 2026-11-17 | E6 차트 창 여는 곳 = 시술 이름 글자만 · 호버 「차트 작성」 | 사용자 |
| 2026-11-17 | 호출 취소(F-5) = 기능은 이번에 · **호출 취소 알림은 앱 업데이트 뒤로 미룸**(A — 심사 중 앱 배지 어긋남 · migration 피함). 앱 푸시는 알림과 함께 다음(심사에 영향 있으면 다음) | 사용자 |
| 2026-11-17 | KOS 에는 호출 취소가 없고 재호출만 있음 → 호출 취소는 **DAY 만**(KOS 쓰기 없음 · KOS 데스크엔 「호출」이 남는 것 감수) · OQ-68 닫음 | 사용자 |
| 2026-11-17 | F-7 = 웹도 앱처럼(원장 계정 = 본인 즉시 수락 · 그 밖 = 원장 골라 대리 수락) | 사용자 · research-1 Q6 |
| 2026-11-17 | F-6 = 미완료 줄은 지금처럼 아이콘 없음. 완료 줄 · 시술 완료 탭에서 작성된 차트만 파란(brand) 아이콘, 미작성(disabled)은 안 그림 | 사용자 · research-1 Q10 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| (없음 — be-3 N1 완료 · 해제) | | | | | Run `run_0b77ffc804ba` |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 피드백: `e2e-feedback.md`
- 리포트: `research-1-report.md`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-17` planner 디스크 가득(ENOSPC)으로 멈춤 → 사용자 비움 → 재개 · 완료
- `2026-11-17` 피드백 7건 수집 · 결정 · slug 세움 · researcher 발주(orca 새 버전 — run-create + worker-start --terminal)

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
