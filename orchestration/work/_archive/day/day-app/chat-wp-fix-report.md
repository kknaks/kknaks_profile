# chat-wp-fix 결과 보고 — WP v7 리뷰 W1 ~ W4 + 코디 실행 경계 최소 정정

## 상태: done (version 7 유지 · JSON · 보고만 · SPEC · 코드 · GitHub · 커밋 · 하위 위임 없음)

- 수정 파일: `delivery-request-v7.json`(제자리) · 신규 `chat-wp-fix-report.md`. 수정 전 사본 = scratchpad `v7-before-fix.json`(비교용).
- 유지: contract_version 7 · L3 · target_specs 003/001/004/000 · baseline 9692e1fb pending · SPEC 원천 53adbd49 · 코드 b6c034bf · PR #237 → dev 하나 · 머지 마지막 · 공식 문서/lock · 실키 사용자 · 스크래치 E2E. 항목 수 불변(target_delta 20 · acceptance 41 · non_goals 15 · review_surface 21 · code_surface 10).

## 바뀐 key (경로 diff 실측 16개)

| key | before → after | 근거 |
|---|---|---|
| `execution.rollback[0]` | 「채팅 커밋 revert · migration 은 칸 추가뿐」 → **기능 코드만 revert · migration 0006/0007 과 그 model 선언은 남김(forward-only · stamp 뒤 파일 삭제 시 기동/배포 막힘)** · schema/데이터 삭제 · 운영 downgrade 없음 | W1 |
| `execution.rollback[5]` | 「migration 없음」 → 「v1 ~ v6 없음 · v7 = 0006(옆 원천) · 0007 증분 · forward-only」 | W1 |
| `acceptance[36]` A36 | 「키 없음 = skipped_no_key 로 쌓고 실패 처리 · 전송 재시도 규칙」 → `status = skipped_no_key`(기존 PushStatus · 새 enum/칸/migration 없음) · 보내기/화면은 실패 아님 · 재시도 · 죽은 토큰 = 프로토 `service/push.py:28-31 · 286-306` 그대로(네트워크 · 5xx · 429 → 1회 · 410 / 400 `BadDeviceToken` · `DeviceTokenNotForTopic` · `Unregistered` → `token_removed` + 결속 해제 · 그 밖 `failed`) · 결속 해제는 **보낸 시점 결속 · 토큰이 지금도 같을 때만**(새 토큰/세션 보존 · 방식은 구현 선택) | W2 · 코디 후속(PushStatus 실측 `enums/misc.py:25-29`) |
| `execution.phases[12]` | 「재시도 · 키 없음 = skipped_no_key」 → 위와 같은 원천 고정 · 기존 status 4값 | W2 |
| `acceptance[13]` A13 | 누적 diff 「v1 범위 안」 → 「v1 범위 ∪ v7 code_surface 안」 | W3 |
| `execution.verification[2]` | 누적 「v1 A13 범위 안」 → 「v1 A13 범위 ∪ v7 code_surface 안」 | W3 |
| `implementation_constraints[0]` | `need` → SPEC-003 §4 규칙 1 목록(`can*` · `canRecall` · `pickable` · `needs` · `inbox.section` · `doctors[].status` · `anesthesia.long` · `lastSeconds` · 순서) | W4 |
| `review_surface[19]` | 「(아래 phases 2)」 → 「(아래 phases 9)」 | 참고 |
| `execution.code_surface[0]` | 라우터 조립 = `backend/day/public.py` `api_routers`(runtime/main.py 가 include · runtime 은 day.public 만 import — test_import_boundaries) | 코디 실행 경계(현 코드 실측) |
| `execution.code_surface[2]` | + `dtos/devices.py` · `schemas/devices.py` · `enums/misc.py`(필요 시만 · 기존 값 재사용) · `day/errors.py` | 코디 |
| `execution.code_surface[5]` | 태스크 = `backend/day/tasks/` + `day/tasks/__init__.py` 등록(worker/scheduler 는 CLI 모듈 인자 `day.tasks`) · runtime/tasks.py 무변경 기본 · common/config.py 설정 항목만(common 다른 업무 코드 확장 0) · `deploy/config/{dev,prod}.env` 이름 placeholder · **`deploy/compose.yaml`**(api · worker · scheduler 가 env_file 로 받는 전달 확인만 · 비밀은 서버 app.env/Key Vault) · local.env.example · compose.local.yaml · pyproject/uv.lock — 실설정 · 기동 변경 0 | 코디(compose.yaml env_file 실측) |
| `execution.code_surface[6]` | 테스트 실제 경로: `tests/day/{chat,devices}/` · `tests/migrations/{test_alembic,test_offline_sql}.py` · `tests/day/{test_column_snapshot,test_constraints,test_models,test_enum_labels}.py` · `tests/architecture/*` · `tests/deploy/*`(env 계약이 바뀌면) | 코디 |
| `execution.code_surface[7]` | 앱: 기존 `ui/{shell,theme,format,widgets}.dart` 재사용 명시 · **채팅 기능 경계 안의 app/ 파일은 목록 밖이어도 허용(목록 = 예시 · app/ 밖 우회 금지)** | 코디 |
| `execution.code_surface[8]` | 새 Swift 파일 + `Runner.xcodeproj/project.pbxproj` 소스 등록 · `app/ios/NativeLogicTests` · `ios/Podfile` · `app/README.md`(채팅 빌드 · 권한 · 설정) 추가 | 코디 |
| `execution.code_surface[9]` | 변경 금지에 `routers/kit*` · common 의 다른 업무 코드 추가 | 코디 |
| `acceptance[40]` A40 | + 「migration forward-only(revert 때도 파일 유지) · 변경 경로 = 누적 v1 범위 ∪ code_surface(A13)」 | rollback · 범위 체크 반영 |

새 제품 정책 · 새 enum/칸 · 새 API 0. 재시도 · 죽은 토큰은 원천(77173cf8) 고정이고, 「보낸 시점 결속 · 토큰 같을 때만 해제」는 SPEC-000 device 규칙(늦은 이전 세션 · 새 등록 보존)을 발송 쪽에 그대로 적용한 경계다.

## 실측 근거
- 라우터: `backend/day/public.py`(api_routers · web_routers) → `backend/runtime/main.py:52-56` include.
- 태스크: `backend/day/tasks/__init__.py`(「새 모듈은 여기서 import 해 등록」) · `runtime/worker.py:1-12` · `scheduler.py:1`.
- 배포: `deploy/compose.yaml:23-25` env_file = `config/${DAY_DEPLOY_ENV}.env` + `${DAY_APP_ENV_FILE:-/etc/day/<env>/app.env}` · local = `compose.local.yaml` environment 블록.
- PushStatus = `sent · failed · skipped_no_key · token_removed`(`backend/day/enums/misc.py:25-29`).
- 프로토 `service/push.py:28-31`(RETRY · DEAD_400) · `:284-306`(재시도 1회 · 410/400 dead → 행 삭제 + token_removed).

## 검증 (최종 1회)
- JSON parse OK · jsonschema(delivery-request + delivery-issue execution ref) **0 errors** · `DeliveryRequest.model_validate` **OK**(v7 · L3 · target 4 · baseline 9692e1fb)
- 수정 전/후 leaf 경로 diff = **16개**(위 표) · 나머지 그대로

## 남은 것
- 코디: 재검수 → CLI plan(origin/main · origin/dev 재 fetch) → L3 새 plan_digest 사람 승인 → #235 apply → backend · mobile 분담 발주.
- 코드 · migration · E2E · 시각 증거 · 실 APNs/Blob/실기기는 모두 미실행(pending).
