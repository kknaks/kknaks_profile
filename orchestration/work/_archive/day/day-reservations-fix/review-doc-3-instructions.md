# [reviewer_doc] 예약 현황판 SPEC 개정 — 3차 검수(고침 3 고친 줄만)

같은 터미널이면 2차 맥락 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec` 미커밋 변경. **파일을 고치지 마라.**

## 읽을 것
- 2차 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-doc-2-report.md`
- 고침 3 지시 · 보고: 같은 폴더 `planner-fix-3-instructions.md` · `planner-fix-3-report.md`
- 결정 표: 같은 폴더 `_RESUME.md` §2 (맨 위 R45 ~ R48 · R41 닫음 행)

## 볼 것
1. W2-1 ~ W2-9 가 고쳐졌나(파일:줄) — 특히 **살아 있는 배치 정의가 Rule 15 ⓐ ~ ⓙ 하나뿐**인지(취소선 밖 옛 30분 칸 문장 0 · 직접 grep)
2. ⓖ ~ ⓙ 가 결정 표 행 · 2차 제안 문장과 맞나 · 서로 한 그림인가
3. 고침 3 이 새로 어긋남을 만들었나(spec-006 ↔ spec-003 앱 · 20-spec · log)
4. 공개 KOS 새 호출 0 · 지어낸 문구 0 · lint products/day ERROR 0
1차 · 2차에서 이미 ✓ 인 것은 다시 파지 마라.

## allowed_paths
- 리포트 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-doc-3-report.md`

## 하지 말 것
파일 수정 · 커밋 · push · KOS 호출 · dev / prod 접속.

## 리포트 모양
맨 위 판정(PASS / WARN / FAIL) 한 줄 · 남은 지적(파일:줄 · 근거 · 고칠 방향) → W2 대조 표.

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
