# chat-wp 결과 보고 — Delivery #235 v7 입력(직원 내부 채팅)

## 상태: done (입력 JSON · 보고만 · GitHub · CLI apply · 승인 receipt · SPEC · 코드 · 커밋 없음)

## 산출물 (허용 2개)
- `delivery-request-v7.json` — v6(승인본과 같은 파일 · contract `sha256:6352e9c4…` · plan `sha256:05b0e270…`)에서 갱신 · CLI 입력 · WP 원장은 GitHub #235
- `chat-wp-report.md` — 이 보고서 · `delivery-request-v6.json` 보존(무수정)

## 결속
| 칸 | 값 |
|---|---|
| idempotency · issue | `day/day-app` · #235 · contract_version **7** · L3 |
| target_specs | **DAY-SPEC-003 · DAY-SPEC-001 · DAY-SPEC-004(신규) · DAY-SPEC-000(device 절 개정 — 실제 schema/migration 영향)** · SPEC-002 는 board 무변경이라 넣지 않음 |
| baseline | latest origin/main `9692e1fb461bf8c4e52bf489e37ab8ff875f9918`(로컬 ref · 코디 fetch) · main 에 SPEC-003/004 없음 · SPEC-001 draft · SPEC-000 device 개정 전 → **pending** |
| 구현 원천 | SPEC PR #921 exact head `53adbd49126c12c887b897854107aa7310cc4f75`(origin/main 9692 위 rebase · products/day tree `c08475fe…` = 재검수 PASS 본) — main ready 로 쓰지 않음 · 선머지 요구 없음 |
| 코드 | CENTURION_DAY day-app `b6c034bfa239bd4f12f1a29c6e58c74d82c87de6` · PR #237 → dev 하나 · 머지는 사용자 마지막 |
| 사용자 원문 | 「응 일단 채팅 기능 스펙부터 앱 구현 까지 진행하자」 · 「아 백엔드 저쪽은 일단 끝나서 우리가 가면 돼!」 · 「채팅 상대는 같은 병원 활성 직원」(scope_delta) — 코디 해석 · 구현 상세는 execution 쪽에만 |
| plan_digest | 만들지 않음(harness 계산) |

## v6 대비 바뀐 곳 (복사만 하지 않고 대조)
- title 간결화 · scope_delta 새로 · target_specs · baseline · review_surface[0] 원천 갱신 + 8개 추가(범위 확대 · 격리 · 경계/동시성 · 첨부/개인정보 · 읽음/배지/배너 · 기기/APNs · migration 한 head · 회귀).
- target_delta +2([v7 앱] · [v7 서버]) · [v2 ①②] 「채팅은 자리만」→「v6 까지 자리만」 · v1 푸시 항목에 「v7 기기 등록 서버 구현 · 원장 호출 발송 밖」.
- acceptance: A0 완료 정의(누적 v7 · 스크래치 PG/Redis API E2E 필수 · mock 만 완료 금지 · 옛 수치 근거 아님 · 실키/실기기 pending 구분) · A10 · A11(권한 = SPEC-004 §4 카메라/사진만 더함) · A12(backend 재검증) · A13(v7 경로 = code_surface) · A14(채팅 API 0건 → v7 A29 ~ A39) 정합 + **A29 ~ A40 신규 12개**.
- non_goals: NG0(D-2 채팅 밖 발송만 밖) · NG4(code_surface 밖 금지로) · NG6(「채팅 기능」 제거) 정정 + 4개 추가(알림센터 · Android/FCM · 실설정/배포/머지 · 옆 branch merge/0006 수정 · 원천에 없는 기능/ESC 정책).
- implementation_constraints +3(원형 · 새 SDK 공식 문서 · lock · 비밀) · [5] v2 ~ v6 만 app/ 로 한정 · starting_points 교체(코드/앱 경로 · 원천 · migration 원천 · baseline 기록).

## execution 요약
- **code_surface**: backend `routers/api/{chat,devices}.py` · services(chat · chat_events Redis · devices · APNs push · 첨부 저장소 로컬/Blob) · queries/dtos/schemas · models(Device 칸 · 옆 0006 가져오면 EventLog Index 선언) · migrations(0006 원천 byte + 새 0007) · tasks/runtime · config · deploy env 이름/compose 전달 · pyproject/uv.lock · tests / app `lib/chat/*` · `ui/chat_*` · 셸 · day_api · chat_stream · push_coordinator · session_controller · copy · iOS AppDelegate · Info.plist · pubspec/lock · Podfile.lock · tests. **변경 금지**: 웹 frontend · board API/SSE · 원장 호출 상태 · emr/KOS · 다른 패키지.
- **dependencies +4**: SPEC 원천 · migration 한 head 최소안 · 사용자 설정 · backend/mobile disjoint 병렬(WP 리뷰 뒤 · 각 리뷰 후 통합).
- **phases 8 ~ 14**: 기준 확인 → 서버 기반(migration · 저장소) → 채팅 API → 실시간 → 기기 · 푸시 → 앱 채팅 → 검증 · 통합.
- **verification +4**: 서버 pytest/infra 스크래치 · ruff · architecture · migration(heads = 1) · 동시성 / 로컬 E2E(두 병원 · 다중 병원 계정 · 미실행 pending) / 앱 analyze · test · native · unsigned · 폰/아이패드 프로토 원형 시각 증거 / 경로 · 비밀 · lock.
- **rollback +2**: 커밋 revert(채팅 자리만으로 · null 칸 · 색인은 데이터 삭제 없이 둠) · 설정 비우기 fail-closed(APNs 키 없음 = skipped_no_key · 저장소 없음 = 409 photo_disabled) — 데이터 삭제 · 권한 완화로 끄지 않음.
- **open_questions +3**: SPEC-004 기본값(OQ-C3/C4/C5/C8 — 재승인 대상 아님) · C9/C10 · migration 방식 착수 시 확정.

## migration 근거 (read-only 확인)
- 앱 tree head `0005_outbox_sender`(versions 0001 ~ 0005).
- 옆 원천: `CENTURION_DAY kknaksss/day-procedure-board-2` `a1c90b9d…`(origin branch 포함 · 옆 tree HEAD caa72435) `backend/migrations/versions/20261110_0006_event_log_visit_type.py` — **sha256 fb0351828664e0e709ab56fa962bc31151f5ae905fe24b9d7a17c6b7b50e0739** · revision 0006 · down 0005 · 내용 = event_log (visit_id, type) 부분 색인. 옆 model `models/task.py` EventLog 에 같은 Index 선언이 있음 → 가져오면 model 선언도 같게(컬럼 스냅샷 · alembic 테스트 정합).
- 최소안 = 그 파일만 byte 그대로 + 새 0007 이 잇기 / 동등 대안 검토 — 착수 시 최신 dev · 옆 PR 상태로 확정(open_questions).

## 인수조건 ↔ SPEC 매핑
| v7 | SPEC |
|---|---|
| A29 | SPEC-004 C-A1 · C-A2 · §3 권한·격리 |
| A30 | C-A3 · C-A4 |
| A31 | C-A5 · C-A7 · C-A8 · §3 동시성·멱등 |
| A32 | C-A6 · C-A12 |
| A33 | C-A11 · §3 실시간 · 케이스 「스트림 끊김」 |
| A34 | C-A9 · C-A10 · §3 첨부 · §4 권한 |
| A35 | C-A13 · U-8 |
| A36 | C-A14 · §3 채팅 푸시 |
| A37 | C-A18 · SPEC-000 §3 07 device 규칙 · SPEC-003 §3 푸시 |
| A38 | C-A15 · C-A17 |
| A39 | C-A16 |
| A40 | SPEC-003 회귀 · migration(SPEC-000 개정 칸) |

## 검증
- JSON parse OK · jsonschema(delivery-request + delivery-issue execution ref) **0 errors** · `DeliveryRequest.model_validate` **OK**(v7 · L3 · target 4 · baseline 9692e1fb) — 각 1회(정합 수정 뒤 최종본 기준)
- 항목 수: target_delta 20 · acceptance 41 · non_goals 15 · review_surface 21 · execution(code_surface 10 · dependencies 15 · phases 15 · verification 9 · rollback 6 · open_questions 6)
- full SHA 14개 실제 rev — 옛 실행 SPEC head(1551fa22 · cdde456a · d6d961e9 · 4a5d4a47 · 06239a1c)는 v2 ~ v6 기록 문장이라 그대로 둠(rebase 뒤 브랜치에는 53adbd49 만 현행)
- v6 → v7 모순 검사: 「app/ 만」 · 「채팅 자리만」 · 「D-2 미구현 · 담당 미배정」 · 「채팅 API 0건」 · 「알림 · 마이크만」 문장을 모두 v7 범위로 한정 · 정정

## 기본값 구현 확인 vs 사용자 필수 결정
- 기본값(새 정책 아님 · 재승인 불필요): SPEC-004 OQ-C3 · C4 · C5 · C8 · migration 통합 방식 · 저장소 추상 · APNs 클라이언트/JWT 라이브러리 선택.
- 사용자 필수(코드 완료 조건 아님): APNs 키 · Apple App ID/Push/서명 · Azure Blob 리소스/키 · 운영 앞단 본문 한도 · 머지 시점 · DAY-ESC-001 회신.

## 다음
- 코디: 독립 리뷰 → CLI plan(origin/main 재 fetch) → L3 새 plan_digest 승인(사용자 원문 결속은 코디) → #235 apply → backend · mobile 발주(disjoint) → 각 리뷰 → 통합.
