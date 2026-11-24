# [backend] 기능 3 — 공지 수정 + KOS 공지 동기화
결정 R58 ~ R61(`/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` 마지막 절) · 계약 `contract-v3-notice.md` · 조사 `research-notice-1-report.md`(이 폴더 · cc 표 1 · KOS 표 2 · §3 · §4) 이 정본.
할 일: ① `EmrAdapter` 에 공지 읽기 · 만들기 · 고치기 · 지우기(업체 경계 시험 지킴 · KOS 내부 API 는 브라우저 UA 필요 — 기존 어댑터 규약) ② `PUT /reservations/notice` — 누른 직원 토큰 · 저장 직전 다시 읽기 · 분기 · 검사 · 오류 · event_log · 성공 뒤 그 날짜 다시 읽어 DAY notice + external_ref 맞춤 ③ 공지 동기화 R60(오늘 회차 · 날짜 회차) ④ 권한 키 `reservation.notice` edit + 데이터 migration(다음 번호 · heads 하나) ⑤ 보기 모델 notice{content, editable, date}(첫 공지 하나) ⑥ 시험(가짜 KOS 로 분기 4 · 409 · 502 · 403 · 길이 · 동기화). 관련 시험만.
**실물 1회**: 데모 테넌트(`deploy/kos-demo.env` 쓰는 로컬 설정 — 값 출력 금지)로 오늘+1일 공지 create → change → delete 를 실제로 한 번 돌려 결과(HTTP 상태만)를 리포트에. 다른 날짜 · 다른 테넌트 금지. 직원 토큰이 막히면 그 사실만 보고(우회 금지).
템플릿 · JS · CSS 는 frontend 몫. 커밋 · push · 스택(11040) 금지. 리포트 `be-feat-3-report.md`(이 폴더) · worker_done.
