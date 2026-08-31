
# [reviewer_spec] 검수 R3 — WP-125 (예약→회의 체인 착지 작업서) + 경미 2건 정리분

너는 **mediness `reviewer_spec` 워커**다. R2 PASS 뒤 planner 가 구현 WP 를 썼다. 이번엔 **WP-125 와 경미 정리분**을 검수한다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec` (read-only — 미커밋 변경 + untracked WP 1개 위. stash·checkout·복원 금지)

## 1. 먼저 읽을 것

- `products/mediness/30-work/work-125-reservation-meeting-autoregister.md` ← 검수 대상 (untracked 신규)
- `git diff` 의 30-work.md·log.md·spec-031·spec-151 변경분 (3자 동기 + 경미 2건 정리)
- SPEC-151 §7.9 / SPEC-031 §3 — WP 가 계약을 확장·왜곡하지 않았는지의 기준
- 네 R2 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-spec-report-r2.md` — 경미 3건의 원문
- 조사 리포트: `.../work/meeting-room-workflow/research-meeting-create-flow.md` — WP 의 코드 좌표 대조용

## 2. 판정할 것

1. **계약 확장 0 인가** — WP 의 작업 항목·Scope·Phase 가 SPEC-151 §7.9 / SPEC-031 §3 에 없는 동작을 만들지 않는가. 비목표가 스펙의 무개정 목록과 일치하는가.
2. **WP 몫으로 넘겨진 항목이 전부 실렸나** — P0 실사 3건(participants 형태 실측 · §7.2 컬럼 대조 · 멱등 보증 수단), W-4, R1 주의점 ①.
3. **코드 좌표가 조사 리포트·실코드와 맞나** — Code Surface 표의 심볼(파일·함수)이 실재하는가. 줄번호 단정이 없는가.
4. **3자 동기** — 30-work.md WP List·Status Board·Spec Coverage 에 WP-125 가 규약대로 등재됐나. doc_no(DOC-245)·WP 번호가 유일한가.
5. **경미 2건(RW-1 라벨 수치·RW-2 파급 bullet 대칭)이 정확히 반영됐나** — 새 모순 없이.
6. `python3 scripts/lint-pipeline.py --strict` 1회 — mediness 범위 ERROR 0.
7. **테스트 계획 충분성** — 조합표 A~D·동기화 분기·멱등·source 게이트·역해소 경계가 커버되나.

## 3. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-wp-report.md`

- 판정(PASS/WARN/FAIL) + 항목별 근거(파일·절). 리포 파일 수정·생성 금지.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ae5c9156-a854-48b7-8f65-528976906150 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_spec 완료: <판정 한 줄>" \
  --body "판정 / 항목별 근거 / 신규 문제 유무 / lint 결과"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] reviewer_spec WP 검수 완료 — <판정>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] reviewer_spec: <질문>" --enter`
