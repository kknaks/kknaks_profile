# [planner] fix-1 — 검수 review-doc-1 반영 + 결정 C17(저장 충돌)

맥락이 없으면 읽어라: 원 브리프 `day-chart-photo-spec-brief.md` · 네 보고 `planner-1-report.md` · 검수 `review-doc-1-report.md` (모두 이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/`) · 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` **C17 · C17-기본값 새로 추가됨**.
워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` (네 미커밋 변경 위에 이어서). allowed_paths · 금지 = 원 브리프 §5 · §7 그대로.

## 1. 결정 C17 반영 (OQ-83 ⓐ 를 닫는다)
- 「걸린 줄만 빼고 나머지 저장」 기본값을 취소선 + 「→ C17 · 사용자 2026-11-24」로 바꾼다.
- [저장] → 서버가 그 탭 시술들의 **KOS 지금 값**(간호관리 = assignee memo · 의사 = doctor memo + 집도의)을 읽어 **연 때 값**과 비교(+ 지금 `baseLogId` 검사 유지). 다른 줄이 하나라도 → **탭 전체 저장 안 함**(이력 · outbox · event 0) · 응답 = 걸린 줄의 **KOS 지금 글 + 줄바꿈 + 요청 글**로 채운 칸 · 담당자 = KOS 값 · 안 걸린 줄 = 요청 그대로 · 토스트(글자 OQ). 다시 [저장] = 같은 확인.
- 「연 때 값」을 무엇으로 비교하는지(열 때 응답에 KOS 기준값을 실어 요청에 되돌려 받는지 · `baseLogId` 로 충분한지)를 정하고 근거를 적는다. KOS 읽기 API(어느 경로 · 시스템 vs 직원 토큰)를 코드 사실(`emr/kos/`)에서 찾아 인용. 못 찾으면 OQ + 기본값.
- C17-기본값: KOS 확인 실패 = DAY 사본만으로 검사하고 저장 · 이어 붙인 글 한도 초과 = 저장 때 길이 오류. 시술 전 의사차트(결정 (가) — DAY 에만)는 KOS 값이 없으니 확인 대상 아님인지 적는다.
- 매트릭스 · API 응답 모양 · 검사 순서 · §4 차이 표 · 10-decision · log 갱신.

## 2. WARN 반영 (기본값 = 코디)
- W1: 저장 이벤트 = 요청 하나에 1행 · 규칙 27 `task.doctor_change` 는 줄마다 그대로 · outbox intent 는 전부 `visit.chart_save` 하나에 묶는다.
- W2: 사진 직원 토큰 없음 · KOS 401 = **지금 코드 공지 저장과 같게 세션 만료 처리**(기본값) · 그 밖 KOS 실패 = 503 `kos_unavailable`. SPEC-006 어긋남은 「무관(기존)」 한 줄.
- W3: 썸네일/원본은 **목록 조각을 그릴 때 한 번에 서명**(`generate-signed-urls-with-param` 1회) — 기본값 · 캐시 없음 · OQ-87 에 붙임. 삭제 행 = 1 목록 → 2 삭제 → 3 목록(규칙 39 ③ 과 맞춤).
- W4: 사진 = KOS 호출 동안 DB transaction 을 열지 않는다 → 결과 뒤 `event_log` 1행 따로 커밋.
- W5 · W6: 취소선 + 개정 ㉘ 표시.
- W7: 검사 순서 400 → 404 로(바로 시작과 같게) · 섞인 경우는 C17 로 다시 정리.
- W8: JSON 짝 **만들지 않는다** — 「없음 — 웹만」 · 옛 `/api/tasks/{id}/chart` 는 지우는 대상으로 적는다.
- W9: 열 때 「최근 저장」 = 그 차트 종류 `tasks[].{chart}.savedAt` 최댓값(새 칸 없음).
- 「직원이 실물에서 만날 자리」 중 사진 읽기 토큰 = **직원 토큰 그대로**(기본값 · DAY 로그인 중엔 KOS 토큰이 있음) — OQ 로 한 줄.

## 3. 검증 · 보고
lint `--strict` products/day ERROR 0. 커밋 금지. 보고 = 이 폴더 `planner-fix-1-report.md`(바꾼 곳 절:줄 · 닫은/새 OQ) + preamble 의 worker_done 두 채널.
