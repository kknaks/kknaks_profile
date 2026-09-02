
# [reviewer_spec] 재검수 R2 — FAIL 2건 해소 확인 (SPEC-151 §7.9 / SPEC-031 정합)

너는 **mediness `reviewer_spec` 워커**다. 네가 직전에 FAIL 을 준 planner 산출물이 수정됐다(R2, diff 3파일 +145/−7). **재검수만** 한다 — 전면 재리뷰가 아니다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec` (read-only — planner 미커밋 변경 위. stash·checkout·복원 금지)

## 1. 먼저 읽을 것

- 네 원 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-spec-report.md` — V-1·V-2·W-1·W-2 의 「권장 수정」이 기준이다
- `git diff` 로 R2 변경분 확인

## 2. 판정할 것

1. **V-1 해소됐나** — SPEC-031 §Validation·§케이스 매트릭스에 경로 단서가 섰고, SPEC-151 §7.9.2 문면이 「요청 스키마의 검증」으로 정정됐나. 같은 문서 안 「필수·422」↔「비적용」 동시 발화가 사라졌나.
2. **V-2 해소됐나** — 회의 쪽 처분 2종이 SPEC-031 에 섰나. 「닫는다 = 대기 회의 soft delete」가 기존 도메인 어휘(state enum 무신설·`deleted_at` 행 보존·read override 전제와 정합) 안에서 성립하나. `:1388`·`:1389` 인접 bullet 단서와 OPEN-031-Y 「부분 해소」 표기가 OQ 의 실제 범위(3표면)와 이제 맞나.
3. **W-1·W-2 반영됐나** — 멱등 불변식의 신설 명시 / 「실행 축은 체인 끝까지 진행 중」 명문화.
4. **수정이 새 모순을 만들지 않았나** — R2 가 건드린 자리(§Validation·케이스 매트릭스·OPEN-031-Y·개정 노트들) 주변만 본다.
5. `python3 scripts/lint-pipeline.py --strict` 1회 — mediness 범위 ERROR 0.

## 3. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-spec-report-r2.md`

- 판정(PASS/WARN/FAIL) + 항목별(V-1·V-2·W-1·W-2·신규모순) 근거. 리포 파일 수정·생성 금지.

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
  --body "판정 / 항목별 해소 여부 / 신규 모순 유무 / lint 결과"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] reviewer_spec 재검수 완료 — <판정>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] reviewer_spec: <질문>" --enter`
