# [reviewer_doc] 예약 현황판 SPEC 개정 — 2차 검수(고침 1 · 고침 2 반영분)

너는 **day `reviewer_doc` 워커**다. 같은 터미널이면 1차 맥락 그대로. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/reviewer/role.md`(+ 같은 폴더).

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec` — 미커밋 변경 전체가 대상(base `origin/main` `b9ac374e`). **파일을 고치지 마라**(stash · checkout · reset 금지).

## 1. SSOT
- `_RESUME.md` §2 결정 표 2026-11-27 행(위 행이 아래 행을 덮음 · 취소선 = 뒤집힘) — 특히 맨 위 **R41 닫음(5장 규칙 + 오픈 시간 기준 1시간 행)** · **R45 ~ R48 코디 기본값**
- 1차 검수: `review-doc-1-report.md` · 고침 지시 · 보고: `planner-fix-1-instructions.md` · `planner-fix-1-report.md` · `planner-fix-2-instructions.md` · `planner-fix-2-report.md` (모두 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/`)
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix`

## 2. 볼 것
1. 1차 W1 ~ W7 이 실제로 고쳐졌나(파일:줄). W8 은 PR 때라 제외
2. 1차 OQ 닫힘이 결정 표 행 그대로 본문 규칙이 됐나
3. **새 배치 규칙(spec-006 Functional Rule 15)**: 5장 · 1시간 행 · 길이 비례 · 줄 접기가 spec-006 · spec-003(앱) · 20-spec · 10-decision 에서 한 정의로 맞나 · R64 · R70 · R71 · R73 · R33 과 어긋남 · 「상한 없음」 잔재
4. OQ-R45 ~ R48 = 결정 표 코디 기본값으로 본문에 넣을 수 있는지(넣을 문장 제안) · 다른 남은 OQ 가 구현을 막는지
5. 공개(open) KOS 호출 새로 둔 곳 = FAIL · 지어낸 화면 문구 = FAIL
6. `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0

## 3. allowed_paths
- 리포트 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-doc-2-report.md`

## 4. 하지 말 것
파일 수정 · 커밋 · push · KOS 호출 · dev / prod 접속.

## 5. 리포트 모양
맨 위 판정(PASS / WARN / FAIL) 한 줄 · FAIL / WARN 목록(파일:줄 · 근거 · 고칠 방향) → W 대조 표 → 배치 규칙 대조 표 → 남은 OQ 표(막는지).

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
