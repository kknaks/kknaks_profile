
# [reviewer_spec] 재검수 R4 — WP-125 V-3 해소 확인 (파급 가드 · source 한정)

너는 **mediness `reviewer_spec` 워커**다. 네가 FAIL 을 준 WP-125 가 수정됐다. **재검수만** 한다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec` (read-only — stash·checkout·복원 금지)

## 1. 먼저 읽을 것

- 네 원 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-wp-report.md` (V-3·V-3b·WARN 의 권장 수정이 기준)
- `git diff` + `products/mediness/30-work/work-125-reservation-meeting-autoregister.md` 의 R3 변경분

## 2. 판정할 것

1. **V-3 해소됐나** — P3 진입 가드가 「연결 + source」 2겹으로 섰고 P1 판정 재사용(정의 한 자리)인가. :166 괄호가 코드 사실대로 정정됐나(구 예약 = 연결 없음 / 모달 발 = source 배제). 비목표·Scope 에 모달 발 축이 명시됐고 P5 가 8종(모달 발 음성 단언 포함)인가.
2. **V-3b 해소됐나** — SPEC-151 §7.9.5 가 「자동 등록한 회의」로 한정됐고 경계 문단이 OPEN-031-Y 를 대신 닫지 않는가. SPEC-031 §3 의 두 파급 bullet 도 같은 한정으로 정렬됐고 OPEN-031-Y 열린 목록에 모달 발 축이 추가됐나.
3. **WARN(절 번호) 정정됐나.**
4. **수정이 새 모순을 만들지 않았나** — R3 가 건드린 자리 주변만.
5. `python3 scripts/lint-pipeline.py --strict` 1회 — mediness 범위 ERROR 0.

## 3. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-wp-report-r2.md`

- 판정(PASS/WARN/FAIL) + 항목별 근거. 리포 파일 수정·생성 금지.

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
  --text "[worker_done] reviewer_spec WP 재검수 완료 — <판정>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] reviewer_spec: <질문>" --enter`
