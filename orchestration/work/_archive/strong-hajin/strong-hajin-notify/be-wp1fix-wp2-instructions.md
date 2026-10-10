# [backend] WP1-BE 검수 WARN 4 손질 → 이어서 WP2-BE

## 1. WP1-BE WARN 4 (`/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp1-be-report.md` §WARN)
- **W-1**: `backend/tests/architecture/test_operation_inventory.py` 파일 목록에 `http_events.py` + 코드 레포 `docs/unified-operations-inventory.json` 에 `GET /api/events/stream` 행 · `http_count` +1 (이 JSON 파일 하나는 allowed_paths 에 더한다). WP2 알림 API 행도 같은 방식으로 더할 것
- **W-2**: `backend/migrations/manual/2026-10-08-notifications-v2.sql` 머리 주석에 「② 이미지 반영 뒤 같은 파일을 한 번 더 — 사이에 옛 이미지가 쓴 빈 `seq` 를 채운다(다시 돌려도 안전)」 절차. (WORK-013 반영 순서 문장은 코디가 고친다)
- **W-3**: **코드를 SPEC 에 맞춘다** — 커서 > 회원 최대 순번이면 `resync` 만 · 시험 하나
- **W-4**: `test_events_stream.py` 에 연결을 닫은 뒤 허브 구독자가 비었다는 단언

## 2. 이어서 WORK-013 「Phase WP2-BE」
- **할 일**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md` **「Phase WP2-BE」 절** 체크박스 전부 + Code Surface **WP2 표** 전부 · 원칙 P-1~P-10
- **계약**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-011-notifications.md` §4.2(생성 — 사건×관계 68행 · 원칙 셋 + 예외 · 관계 우선 담당>요청자>배정자>참조 · 회의 소유자>참석자>공유받음 · 슬랙 채널 합침 · 설정 거름 · 옛 생성 1곳 흡수) · §4.3(판정 재료 `from_me`) · §4.4(설정) · §4.5(알림 API · `/api/me/badges` · 메시지함 읽음 → 알림 읽음) · 백필 SQL · `spec-008` 안 읽음 판정(`raw.user`)
- **P0 결과 반영**(`/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/p0-report.md`): 카톡 「내가 보냄」 은 수집기가 `authorId == NTChatContext.userId` 로 올린다(WP4 에서 수집기를 고친다) — WP2-BE 는 **업로드 줄의 표지 필드를 받아 `from_me` 에 저장**하는 서버 쪽만(표지가 없으면 `null` = 내 것 아님). 기존 행 백필은 실명을 SQL 에 박지 않고 `psql -v` 인자로
- **conversation_worker 에서 업무 사건이 나는지**(WORK Open Issues I-1 · `BA:1790`)를 첫날 확인하고 리포트에
- 검증은 **WP2-BE 「시험」 줄의 Makefile 타겟·파일만**(전체 스위트 · `make verify` · `uv run pytest` 직접 금지) · 격리 PostgreSQL 은 별도 포트
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-wp1fix-report.md`(WARN 4 — 짧게) · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-wp2-report.md`(체크박스별 파일:줄 · Code Surface 대비 · 시험 수치 · 미결)
- 금지는 앞 브리프 그대로(커밋 · 사용자 포트 · 스택 · 운영 · 문서 · `frontend/` — frontend 워커가 WP1-FE 중)

## 완료 보고 — 앞 브리프 §7 두 명령 그대로
subject 「backend 완료: WP1 손질 + WP2-BE」 · text 「[worker_done] backend WP1 손질 + WP2-BE 완료 — <한 줄>. 리포트 be-wp2-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
