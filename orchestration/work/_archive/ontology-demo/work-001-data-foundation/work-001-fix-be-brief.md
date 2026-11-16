
# [backend] WORK-001 검수 FAIL 수정 — 차단 3건 (+경고 검토)

너는 **ontology-demo `backend` 워커**다. 같은 워크트리, WORK-001 이어서. 리뷰 리포트를 먼저 읽어라 (read-only):
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/work-001-data-foundation/review-work-001-report.md`

## 차단 3건 — 리뷰어 해법대로 고친다 (코디 승인)

1. **계층 경계** (gold.py:262): 골드가 `bronze_nexus_promotion_v2s` 직접 읽기 금지. 해법 — 실버(`silver_promotions` 또는 매핑 테이블)에 원천 v2 `source_id` 1컬럼을 보존해 골드는 실버만 읽게. 추가 컬럼은 이식 원칙과 무충돌(재현 대조는 기존 공유 컬럼 기준 유지).
2. **게이트 실패 시 이전 DB 유지** (REBUILD_MISMATCH — SPEC-001 §5): 빌드를 스테이징 후 스왑(또는 단일 트랜잭션)으로 — 게이트 2·3 실패 시 기존 DB 가 그대로 남아야 한다. 실패 주입 테스트로 증명.
3. **강남언니 정합률 게이트 차단력 복원**: 원본 `reviews_finalize.py:117` 의 sys.exit(2) 동등물(예외로 빌드 중단) 복원 — 출력만 하는 게이트는 게이트가 아니다.

## 경고 9건 — 리포트에서 읽고 각각 「수정함 / 수정 안 함+사유」로 보고에 명시.

## 완료 기준

- 게이트 1·2·3 + P5 1:1 전항 재통과 수치 · 실패 주입 테스트 포함 테스트 전건 통과(네가 만든/고친 파일만) · 변경 파일 목록.
- 보고: 동일 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f8-... ← **preamble 이 맞다**, 아래 명령의 핸들 사용), subject "backend 완료: WORK-001 fix".

```bash
orca orchestration send --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: WORK-001 fix" --body "차단 3건 처리 / 경고 9건 각 판정 / 게이트 재실행 수치 / 테스트"
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --text "[worker_done] backend 완료 — WORK-001 fix. 상세는 인박스." --enter
```
