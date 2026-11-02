
# [reviewer_code] WP-125 코드 검수 — BE(81파일) + FE(36파일) 전체 diff

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 문서들)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-redesign` (base `origin/dev`)
**read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다. 범위 산정은 `git diff origin/dev` + staged(`--cached`) + untracked 3건(0135 migration·round_eval.py·test_0135).

## 판정 기준 (SoT)

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/30-work/work-125-task-ledger-unification.md` — 빌드 계획
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/40-architecture/domains/runtime_task.md` — 상태·전이·이벤트 정본
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/_RESUME.md` §2 — 결정 SoT
- 발주 브리프 2장: `.../task-redesign-be-brief.md` · `.../task-redesign-fe-brief.md` (allowed_paths·계약·제약)

## 체크리스트

1. **결정 SoT 준수**: 5값 enum(양쪽 동시)·accepted_at drop(+RAISE 가드)·decline 축 완전 제거·재배정 todo 리셋+terminal 가드+담당자 본인 가능·생성 초기값 전부 todo·명시 시작만(자동전환·즉시 in_progress 0)·회의록 canonical·P7 은 라우트 등록 해제(주석 비활성)까지만
2. **invariant**: 두 enum 값 동형 유지 · done⟂canceled 재배정 불가 · 삭제⟂취소 배제 앵커 무효화 없음 · done⇒체크리스트 완료 · 과거 task_accepted/declined 이벤트 행 보존(마이그레이션이 지우지 않는지)
3. **P8 seam**: 라운드 평가가 `apply_user_transition` 안쪽으로 — 완료 표면 4개(incident PATCH·canonical transition·task-completions·MCP) 전부 같은 seam 을 지나는지. **판정 규칙 자체를 고치지 않았는지**(WP-126 소관 침범 금지)
4. **합성 전이 통합**: `apply_transition_chain` 1곳 + 표면별 경로표 — 기존 3중 구현 잔존 없는지
5. **allowed_paths**: BE=back/·mcp/ 만, FE=front/ 만 — diff 로 교차 침범 0 확인
6. **BE↔FE 계약 정합**: allowed_transitions 축·declined 파생 제거·decline BFF↔REST 짝 맞음·라벨 사전 소비
7. **회귀 위험**: 전이표 축소로 죽는 기존 호출부(파일:줄), 마이그레이션 다운그레이드 경로, WP-114 착지분 회귀 여부
8. 워커 자가보고 미결 5건(RAISE 가드 대체·채팅 blocked→done 합성 보존·알림⑧ 결번·SPEC-060 수치 실측 차이·OI-4 미착수)의 처리 적정성

## 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/review-code-report.md` — 판정(PASS/WARN/FAIL) + 위반 목록(파일:줄 + 근거 규칙). 문체 지적으로 FAIL 금지.

## 완료 보고 — 문구 변경 금지

> ⚠ 핸들은 dispatch preamble 값을 믿어라.

- 커밋·push·PR 금지.
- 끝나면 두 명령 모두 실행:

```bash
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_96c72726-814b-440e-9e29-2da11115ee1d \
  --type worker_done \
  --task-id <dispatch preamble 의 taskId> \
  --dispatch-id <dispatch preamble 의 dispatchId> \
  --subject "reviewer_code 완료: <판정 한 줄>" \
  --body "판정 / 체크리스트 항목별 결과 / 위반 목록(파일:줄) / 미결"

orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] reviewer_code 완료 — <판정 한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --text "[질문] reviewer_code: <질문>" --enter`
