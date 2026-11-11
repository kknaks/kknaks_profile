# 리뷰 리포트 — day-app Delivery #235 v7 입력(직원 내부 채팅) / doc (2026-11-10)

- 대상: profile `delivery-request-v7.json` · `chat-wp-report.md`
- 대조 원천:
  - `delivery-request-v6.json` · `delivery-v6-approved-result.json` · `delivery-v6-apply-result.json`(contract `6352e9c4…` · plan `05b0e270…`)
  - 스펙 트리 HEAD `53adbd49126c12c887b897854107aa7310cc4f75`(SPEC-004 · 000 · 003 · 001)
  - `chat-decisions-20261110.md` · `chat-spec-rereview.md`
  - 코드 day-app `b6c034bf` · 옆 CENTURION_DAY `kknaksss/day-procedure-board-2`(`a1c90b9d` · `caa72435`)
  - 프로토 `77173cf8` `service/push.py`(모두 read-only)
- 방법:
  - JSON 파싱 · 실제 schema · harness 모델 1회
  - v6 ↔ v7 경로 diff(바뀐 키 90개 전수 읽기)
  - 옛 범위 문장 grep · migration 파일 sha256 · 머리 실측
  - 수정 · 하위 위임 없음

## 판정: WARN (FAIL 0 · WARN 4)

같은 #235 · `day/day-app` · contract v6 → **v7(정확히 1 증분)** · L3 · baseline `9692e1fb`(= 로컬 `origin/main`) pending 정직 · 구현 원천 `53adbd49`가 모두 맞다.
- `53adbd49`: origin/main의 자손 · products/day tree `c08475fe…` · `7cf28b30..53adbd49` diff = 재검수 PASS 본 5파일 · SPEC-004 `status: stable`.
- 결과 계약:
  - 사용자 원문 3건과 맞게 채팅 앱 + 서버(HTTP 20 · 스트림 6종 · 첨부 · 기기 등록 · 채팅 APNs)로 넓혔다.
  - Android · 알림센터 · 원장 호출 발송 · 상담사 호출 확장은 non_goals로 막았다(NG0 · NG11).
  - 채팅 push를 OQ나 D2 핑계로 빼지 않았다.
  - 키 · Apple · Blob · 실기기는 사용자 설정 · pending으로 분리했다(A0 · deps[13]).
  - mock만으로 완료를 금지하고 스크래치 PG/Redis E2E를 필수로 했다(A0 · verification[5][6]).
- 안전 항목(병원 격리 · 멱등 응답 검증 먼저 · clientId 지운 행 · seq · 초대 경계 · 첨부 MIME/Range · 재접속 tombstone · 다기기 읽음 · device 늦은 PUT/DELETE · namespace 원자성)이 A29 ~ A40 · review_surface에 매핑돼 있다.
- 동시성은 「동시 요청 포함 API 테스트」로 검증 가능하게 적혀 있다.
- migration 한 head 최소안은 실물로 실행 가능하다(아래).

WARN 4건은 다음과 같다(W4는 코디 후속 `delivery_b88ace9d03be` 확인분):
- W1: rollback의 옛 문장 · migration 되돌림
- W2: APNs 실패 처리의 원천 미지정
- W3: 누적 경로 검사의 v1 범위 문장
- W4: 구현 제약의 옛 `need` 표기

## FAIL

없음.

## WARN

### W1. rollback — 「migration 없음」 옛 문장이 남았고, 채팅 커밋 revert가 이미 적용된 0006/0007 migration 파일까지 지우는 경우를 막지 않는다
- 위치:
  - `delivery-request-v7.json` `$.execution.rollback[5]` = 「migration 없음」(v6 문장 그대로)
  - `$.execution.rollback[0]` 「앱 · 서버 채팅 커밋 revert → … 새 migration은 null 허용 칸 · 색인 추가뿐이라 revert 시에도 schema · 데이터를 지우지 않는다(downgrade를 운영에서 돌리지 않음)」
- 근거: v7 code_surface[4]가 `0006`(옆 원천) + 새 `0007`을 더한다(A40 · phases[9]). DB가 `0007`로 stamp된 뒤 그 migration 파일까지 revert하면 alembic이 현재 revision을 찾지 못해 다음 기동 · 배포가 막힌다(fail-open은 아니지만 회복 경로가 끊김).
- 영향: rollback 항목끼리 모순(migration 있음/없음)이 생기고, 실제 되돌림 절차가 비어 있다.
- 최소 정정:
  - rollback[5]를 「v1 ~ v6은 migration 없음 · v7은 0006(옆 원천) · 0007 증분」으로 고친다.
  - rollback[0]에 「revert는 앱 · 서버 기능 코드만 — migration 파일 0006 · 0007은 남겨 둔다(forward-only · 칸 · 색인은 null/추가만이라 남아도 무해)」 한 구절을 단다.
  - 데이터 삭제 · downgrade 금지는 지금 그대로 둔다.

### W2. A36 「전송 재시도 규칙」과 죽은 토큰 처리가 원천 근거 없이 비어 있다
- 위치: `$.acceptance[36]` 「… 키 없음 = skipped_no_key로 쌓고 실패 처리 · 전송 재시도 규칙 — APNs는 테스트 더블로 완료 …」 · `$.execution.phases[12]` 「재시도 · push_log · 키 없음 = skipped_no_key」
- 근거:
  - SPEC-004 §3 「채팅 푸시」 · SPEC-003 §3 「푸시」에는 재시도 · 죽은 토큰 규칙이 없다(grep 0).
  - 프로토 B/`service/push.py:28-31 · 286-306`은 네트워크 · 5xx · 429 → 1회만 재시도 · 410 또는 400(`BadDeviceToken` · `DeviceTokenNotForTopic` · `Unregistered`) → 그 기기 행 정리 + `token_removed`이다.
  - DAY `push_log.status` enum에도 `token_removed`가 있다(SPEC-000 :1008).
- 영향: 「규칙」이 정의되지 않아 A36을 검증할 수 없다. 죽은 토큰을 DAY 새 device 규칙(세션 결속 · namespace) 아래에서 어떻게 정리할지(결속 해제 vs 소프트 삭제)를 구현 워커가 추측하게 된다. 퇴사 · 비활성은 받는 사람에서 빠지는 것으로 이미 덮인다.
- 최소 정정:
  - 새 정책은 짓지 않는다. A36 · phases[12]에 「재시도 · 죽은 토큰 = 프로토 B/`service/push.py:28-31 · 286-306` 그대로(1회 재시도 · 410/DEAD_400 → `token_removed` 기록 + 그 device 결속 해제)」로 원천을 박는다.
  - 결속 해제 방식(`login_session_id` 비움 vs `deleted_at`)은 execution 구현 선택으로 적는다.
- **코디 후속 — `skipped_no_key`는 새 enum · 칸이 아니다(실측)**:
  - 기존 `PushStatus`(CENTURION_DAY `backend/day/enums/misc.py:25-29`) = `sent` · `failed` · `skipped_no_key` · `token_removed`.
  - DB enum `push_status`도 `0002_data_model_first_data_model.py:100`에 이미 같은 네 값이 있다.
  - SPEC-000 `push_log.status`(:1008)도 같다.
  - 따라서 A36의 `skipped_no_key` · `token_removed`는 **기존 상태값 사용**이다. 새 칸 · 새 enum 정책 추가가 아니고 migration도 필요 없다.
  - 다만 A36 「skipped_no_key로 쌓고 **실패 처리**」는 `status = failed`로도 읽힌다. 「`status = skipped_no_key`(기존 값)로 쌓는다 · 보내기 요청 · 화면은 실패로 다루지 않는다」로 다듬으면 모호함이 없다(W2 정정과 함께).

### W3. A13 · verification[2]의 「누적 diff = v1 범위 안」이 v7 backend 채팅 변경과 충돌한다
- 위치:
  - `$.acceptance[13]` 「코드 PR 하나(#237 → dev)의 누적 변경은 v1 범위(app/ · backend D-1 로그인 관련 파일과 그 테스트 · deploy/config env 이름 placeholder · AGENTS.md 「앱」 문장) 안이고, … v7 채팅 커밋(b6c034bf 이후)의 변경은 Execution code_surface … 안」
  - `$.execution.verification[2]` 「누적 `git diff --name-only origin/dev...HEAD`가 v1 A13 범위 안」
- 근거: v7은 `backend/day/routers/api/chat.py` · services · models · migrations · deploy env · pyproject 등 v1 범위 밖 경로를 추가한다(code_surface[0] ~ [6]).
- 영향: v7 구현 뒤 누적 diff는 정의상 「v1 범위 안」을 만족할 수 없다. 이 검사가 그대로면 늘 실패하거나, 실패를 무시하는 습관이 생긴다.
- 최소 정정: 두 자리를 「누적 diff = v1 범위 ∪ v7 code_surface 안」(또는 「v1 범위 + `b6c034bf..HEAD`는 code_surface」)으로 고친다.

### W4. `implementation_constraints[0]`의 옛 서버 칸 이름 `need`(코디 후속 확인)
- 위치: `$.implementation_constraints[0]` 「앱은 서버 계산 값(can* · pickable · **need** · inbox.section · doctors[].status · 순서)만 쓰고 …」(v1부터 그대로 · v6에서도 같음)
- 근거: v3 로컬 API 정합 뒤 SPEC-003 §4 규칙 1(`53adbd49` `spec-003-mobile-app.md:642`) = `can*` · `canRecall` · `pickable` · `needs` · `inbox.section` · `doctors[].status` · `anesthesia.long` · `lastSeconds` · 순서. 카드 `need` 키는 소비 원천(옆 backend `a1c90b9d board_rules.py:621`)에 없다. 같은 JSON의 constraints[7]은 이미 `needs`로 맞다.
- 영향: 같은 입력 안에서 옛 칸과 새 칸을 동시에 가리킨다. 구현 워커가 옛 `need`를 다시 읽는 코드를 둘 근거로 오해할 수 있다(v7 범위는 아니지만 회귀 계약의 문장).
- 최소 정정: constraints[0]를 SPEC-003 규칙 1 목록(`canRecall` · `needs` · `anesthesia.long` · `lastSeconds` 포함)으로 맞춘다.

## 결속 · 범위 실측

| 점검 | 결과 |
|---|---|
| JSON · schema · 모델 | 파싱 OK · `delivery-request.schema.json`(Draft 2020-12 · 같은 폴더 registry) **0 errors** · `DeliveryRequest.model_validate` **OK**(v7 · L3 · target `DAY-SPEC-003/001/004/000` · baseline `9692e1fb…`) |
| 버전 | #235 현재 v6(`delivery-v6-apply-result.json` contract `6352e9c4…` · plan `05b0e270…`) + 1 = 7 · scope_delta가 그 digest를 인용 · 승인 receipt · 승인 주장 없음 |
| target_specs | +SPEC-004 · +SPEC-000(device 개정 = 실제 schema/migration 영향) · SPEC-002 제외(board 무변경) — 합당 |
| 원천 SHA | `53adbd49` = SPEC PR #921 head · `origin/main 9692e1fb`의 자손 · products/day tree `c08475fe007c65eca160ece434acada493f2a996`(실측 일치) · SPEC-004 stable · 「6종」 · 「늦은 이전 세션」 반영 · main ready로 쓰지 않음 · 선머지 요구 없음 |
| 코드 · PR | `b6c034bf` · PR #237 → dev 하나 · 머지 사용자 마지막(scope_delta · NG12) |
| 옛 범위 문장 정합 | grep 「app/ 만 · backend 수정 없음 · 자리만 · API 호출 0 · 알림 · 마이크만 · 담당 미배정 · D-2」 → 모두 「v2 ~ v6 / v6까지」로 한정되거나 v7 범위를 명시했다(A11 · A12 · A14 · target_delta[4] · [8] · deps[5] · NG0 · NG4 · NG6 · constraints[5]). 예외는 W1(rollback[5]) · W3(A13 · verification[2]) |
| 범위 확대 차단 | NG0(원장 호출 · 상담사 · 띄우기 발송) · NG11(알림센터 · Android · FCM · 알림 kind 확장) · NG13(옆 branch 전체 merge · dev 선머지 · 원천 0006 수정 · 옆 트리 편집) · NG14(DAY-ESC-001 정책 · 원천에 없는 기능) · code_surface[9](웹 · board API/SSE · 원장 호출 상태 · emr/KOS 변경 금지) |
| 원천 디자인 · 문구 | constraints[8] · A39(프로토 77173cf8 원형 나란히 시각 증거 · 새 글자 0) |
| 완료 vs pending | A0 · A34 · A36 · deps[13] · verification[6] — mock만 완료 금지 · 스크래치 PG/Redis E2E 필수 · Blob · APNs · 실기기 · 배포는 pending 분리 · 서명 0 |
| 검증 계획 | 서버 `pytest -m "not infra"` + `scripts/test.sh -q`(스크래치) · ruff · architecture · migration(heads = 1 · up/down · offline SQL) · 동시성 / 로컬 E2E(두 병원 · 다중 병원 계정) / 앱 analyze · test · native · unsigned · 시각 증거 / 경로 · 비밀 · lock |
| fail-closed | 키 없음 = `skipped_no_key` · 저장소 없음 = 409 `photo_disabled` · 데이터 삭제 · 권한 완화로 끄지 않음 · 데모 이메일 목록을 비우는 prod fail-open 금지 문장 유지(rollback[4]) |

## migration 한 head — read-only 실물

| 확인 | 결과 |
|---|---|
| 앱 tree | `b6c034bf` versions = 0001 ~ 0005 · head `0005_outbox_sender` |
| 옆 원천 | `a1c90b9d` · `caa72435`(옆 HEAD) · `origin/kknaksss/day-procedure-board-2`(= caa72435) 모두 0001 ~ 0006 · `20261110_0006_event_log_visit_type.py` sha256 **fb035182…0739**(세 ref 같음 · WP 값 일치) · `revision 0006_event_log_visit_type` · `down_revision 0005_outbox_sender` |
| 공통 조상 | 앱과 옆의 `0005_outbox_sender` 파일 sha256 `d2cf9587…909c` 동일 → 0006 byte 복사 + 새 0007(down = 0006)은 한 head로 실행 가능 · 옆 머지 때 같은 파일 · 같은 revision이라 충돌 없음 |
| model 정합 | 옆 `models/task.py:158-159` `Index("ix_event_log_visit_id_type", …)` — WP가 「model Index 선언도 같게」로 적음(code_surface[3] · A40) |
| 주의 | 로컬 `origin/dev` = `91728737`(fetch 시점 그대로). WP phases[8] · deps[12] · open_questions[5]가 「착수 전 최신 origin/dev · 옆 PR 상태 재확인」을 요구 — 그대로 유효(옆이 dev에 먼저 들어가면 0006은 가져오지 않고 0007만 잇는 길도 같은 결과) |

## 참고 (결함 아님)

- `$.review_surface[19]` 끝 「(아래 phases 2)」는 v7 migration 단계인 phases[9]를 가리켜야 한다(표기 오류).
- title이 v6의 누적 나열에서 「… 직원 내부 채팅(v7)」으로 줄었다. scope_delta · target_delta가 누적을 담아 계약 손실은 없다.
- 원장 호출 푸시 처리 회귀는 review_surface[20]에 「기기 필터가 세션 병원 = 일의 병원으로 좁아짐 · 받는 사람 정책 무변경」으로 들어가 있다(앞 리뷰 참고 반영 확인).
- mobile-deployment §5-3 권한 목록 · OQ-C3/C4/C5/C8 기본값은 open_questions[3]에 「재승인 대상 아님」으로 남아 있다. 미결을 새로 만든 것은 없다.

## 남은 것

- planner: W1(rollback[0] · [5]) · W2(A36 · phases[12] 원천 고정 · skipped_no_key 문장) · W3(A13 · verification[2] 범위식) · W4(constraints[0] `needs`) 최소 정정 → 재검수.
- 코디: CLI plan(origin/main · origin/dev 재 fetch) → L3 새 plan_digest 사람 승인 → #235 apply → backend · mobile 분담 발주.
- 실제 실행은 아직 하지 않았다: 코드 · migration · E2E · 시각 증거 · 실 APNs/Blob/실기기 모두 pending.
