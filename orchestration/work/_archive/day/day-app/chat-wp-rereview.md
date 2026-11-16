# 리뷰 리포트 — day-app Delivery #235 v7 입력 W1 ~ W4 + 실행 경계 정정 재검수 / doc (2026-11-10)

- 대상: profile `delivery-request-v7.json`(제자리 정정) · `chat-wp-fix-report.md`
- 근거:
  - 앞 리뷰 `chat-wp-review.md` W1 ~ W4 · 참고
  - 코디 후속(`delivery_b88ace9d03be`) · `chat-wp-fix-brief.md`
  - 코드 day-app `b6c034bf` · 프로토 `77173cf8` `service/push.py`(read-only)
- 방법:
  - 앞 리뷰 때 남긴 v6 → 옛 v7 경로 diff(scratchpad)로 옛 v7을 복원해 새 v7과 경로 단위로 비교했다.
  - 새로 적힌 코드 경로 26개의 실재를 확인했다.
  - schema · 모델을 1회 돌렸다.
  - 수정 · 하위 위임 없음.

## 판정: PASS (FAIL 0 · WARN 0)

## 변경 범위 (실측)

- 옛 v7 → 새 v7 바뀐 키는 **정확히 16개**다(planner 보고와 같음): `acceptance[13]` · `[36]` · `[40]` · `execution.code_surface[0]` · `[2]` · `[5]` · `[6]` · `[7]` · `[8]` · `[9]` · `phases[12]` · `rollback[0]` · `[5]` · `verification[2]` · `implementation_constraints[0]` · `review_surface[19]`.
- 그 밖은 모두 무변경이다: contract_version 7 · L3 · target_specs 003/001/004/000 · baseline `9692e1fb` pending · scope_delta · A0 ~ A12 · A14 ~ A35 · A37 ~ A39 · non_goals · dependencies · 항목 수(acceptance 41 · code_surface 10).
- 검증: JSON 파싱 OK · `delivery-request.schema.json` **0 errors** · `DeliveryRequest.model_validate` **OK**(v7 · L3 · baseline `9692e1fb` · acceptance 41).

## 지적별 확인

| 지적 | 새 문장 | 결과 |
|---|---|---|
| W1 rollback | `rollback[0]` 「**기능 코드만** revert · migration 0006 · 0007과 그 model 선언은 남겨 둔다(forward-only — stamp 뒤 파일 삭제 시 기동 · 배포 막힘) · schema · 데이터 삭제 · 운영 downgrade 없음」 · `rollback[5]` 「v1 ~ v6 없음 · v7 = 0006(옆 원천) · 0007 증분 · forward-only」 · A40에 「forward-only(revert 때도 파일 유지)」 | PASS — 모순 해소 · 데이터 삭제 0 · fail-closed(rollback[1]) · 데모 이메일 비우기 금지(rollback[4]) 그대로 |
| W2 APNs 실패 | A36 · phases[12]: 재시도 · 죽은 토큰 = 프로토 `service/push.py:28-31 · 286-306` 그대로(네트워크 · 5xx · 429 → 1회 · 410/400 `BadDeviceToken` · `DeviceTokenNotForTopic` · `Unregistered` → `token_removed` + 결속 해제 · 그 밖 `failed`) · 결속 해제는 **보낸 시점 결속 · 토큰이 지금도 같을 때만**(새 토큰 · 새 세션 보존 · 방식은 구현 선택) | PASS — 원천 줄 일치(앞 리뷰 실측 `push.py:28 RETRY` · `:31 DEAD_400` · `:293 410/DEAD_400`) · 「같을 때만」은 SPEC-000 device 규칙(늦은 이전 세션 · 새 등록 보존)을 발송 쪽에 그대로 적용한 것으로 새 정책이 아니다 · 검증 가능 |
| 코디 후속 skipped_no_key | A36 「`push_log.status = skipped_no_key`(기존 PushStatus 값 · 새 enum/칸/migration 없음) · 보내기 요청 · 화면은 실패로 다루지 않음(메시지는 정상 전송)」 · phases[12] 기존 status 4값 | PASS — `enums/misc.py:25-29` · `0002` DB enum과 일치 |
| W3 누적 경로 | A13 · verification[2] 「v1 범위 ∪ v7 code_surface 안」 · A40 같은 식 | PASS |
| W4 `need` | constraints[0] = SPEC-003 §4 규칙 1 목록(`can*` · `canRecall` · `pickable` · `needs` · `inbox.section` · `doctors[].status` · `anesthesia.long` · `lastSeconds` · 순서) | PASS — `53adbd49 spec-003:642`와 같음 |
| 참고 phases 표기 | review_surface[19] 「(아래 phases 9)」 | PASS |

## 코디 실행 경계 추가분 — 실물 확인

| 칸 | 확인 |
|---|---|
| code_surface[0] 라우터 조립 | `backend/day/public.py:65` `api_routers()` · `runtime/main.py:18 · 53`이 그것만 import · include · `tests/architecture/test_import_boundaries.py` 실재 — 맞다 |
| code_surface[2] | `day/errors.py` 실재 · `enums/misc.py`는 「필요할 때만 · 기존 값 재사용」 — 새 enum 정책 아님 |
| code_surface[5] 태스크 · 배포 | `day/tasks/__init__.py` · `runtime/tasks.py` 실재 · `deploy/compose.yaml:22-24` `env_file` = `config/${DAY_DEPLOY_ENV}.env` + `${DAY_APP_ENV_FILE:-/etc/day/<env>/app.env}` — 「전달 확인만 · 비밀은 app.env/Key Vault · 실설정 · 기동 변경 없음」과 맞다 · `deploy/config/{dev,prod}.env` · `local.env.example` · `compose.local.yaml` 실재 |
| code_surface[6] 테스트 | `tests/migrations/{test_alembic,test_offline_sql}.py` · `tests/day/{test_column_snapshot,test_constraints,test_models,test_enum_labels}.py` · `tests/deploy` 실재 |
| code_surface[7] 앱 | `ui/{shell,theme,format,widgets}.dart` 실재 · 「채팅 기능 경계 안의 app/ 파일은 목록 밖도 허용 · app/ 밖 우회 금지」 — 앱 쪽 경로 검사를 예시 목록으로 완화했지만 app/ · 채팅 기능으로 묶여 있어 범위 확대는 아니다 |
| code_surface[8] iOS | `ios/Runner.xcodeproj/project.pbxproj` · `ios/NativeLogicTests` · `ios/Podfile` · `app/README.md` 실재 · 새 Swift 파일 등록 필요는 사실 |
| code_surface[9] 금지 | `routers/kit*` · common의 다른 업무 코드 추가 — 금지 범위가 넓어짐(축소 방향) |

## 남은 것 (결함 아님)

- 코디: CLI plan(origin/main · origin/dev 재 fetch — 로컬 `origin/dev`는 아직 `91728737`) → L3 새 plan_digest 사람 승인 → #235 apply → backend · mobile 분담 발주.
- 코드 · migration · 스크래치 E2E · 시각 증거 · 실 APNs/Blob/실기기는 모두 미실행(pending)이다.
