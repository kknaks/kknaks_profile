# [reviewer] WP19 코드 검수 — 통역 기록 보관 기간 env (D-42 · SPEC 0.7.0)

너는 **interpret-pwa `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

앞 맥락이 없다. **read-only** — 레포 파일 수정 금지 · 산출은 리포트 1개. backend 는 끝났다(병렬 작업 없음).

## 1. SSOT

- SPEC `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 0.7.0 — §2.4 `INTERPRET_RECORD_KEEP_DAYS` 행 · **§5.9 「보관 기간 — env」 표 · 「삭제 규칙」** · 기동 ② ④ · §9.1 「기록」 ⑦ ⑨ (a)(b)(c)
- WORK `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` WP19 행 — 산출 파일 · 완료 조건
- DEC D-42(`/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` 98줄)
- backend 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp19-be-report.md`

## 2. 무엇을 보나 (`git -C /Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea diff` — 미커밋 변경 6파일)

1. SPEC §5.9 표의 갈래마다 코드 · 시험이 맞나 — 비었음 · 공백만(경고 0) / 십진 숫자 1 이상(` 7 ` · `07`) / 그 밖(`0` · `-1` · `abc` · `+7` · `7.0`) 경고 1줄 · 기동 성공 · 기록 켜짐 / 기록 끔 + 값
2. **off 일 때 삭제가 정말 0 인가** — 기동 때 `sweep` · 24시간 태스크 둘 다. 로그 `keep_days=off` · `sweep: deleted=` 줄 0
3. **조용히 통과하는 자리** — 시험이 off 를 「삭제 0」으로만 보고 태스크가 만들어졌는지는 안 보는 식의 빈틈 · 설정 클래스에서 기동이 죽을 경로(타입 · env_ignore_empty) · 유니코드 숫자 · 아주 큰 N
4. D-41 그대로여야 하는 것(줄 모양 · term 판정 · 넣지 않는 것 · 쓰기 실패) 무변경 · `test_api_surface.py` 무변경
5. allowed_paths(`back/` · `.env.example`) 밖 변경 0 · 키 · 기록 문장 0
6. 관문 명령을 직접 1회: `cd back && uv run ruff check . && uv run pytest -q tests/test_records.py tests/test_api_surface.py tests/test_interpret.py`
7. 배포(WP20) 때 운영에서 볼 자리 — 「사용자가 실물에서 만날 자리」 한두 줄

## 3. 산출

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/review-wp19-code-report.md` — 판정 **PASS / WARN / FAIL** · 지적마다 `파일:줄` + 근거(SPEC 절 · D-번호)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_232921f4-67a5-40d5-a490-47b7d1b09da4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
