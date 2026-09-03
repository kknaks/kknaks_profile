
# [planner] SPEC-120 §3.3 정정 — 데일리 리포트 생략 규칙 폐지, 활성 구성원 전원 표기

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/report-all-members-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

<같은 워크트리를 다른 워커와 공유하면 여기에 경고를 적는다. 예: "BE 워커가 `back/` 에서 병렬 작업 중 — 건드리지 마라.">

## 1. 할 일 — 스펙 정정 1건 (사용자 확정 2026-09-03)

정본: `products/mediness/20-spec/spec-120-task-slack-notify.md`

**바꿀 계약**: §3.3 「전날 활동 0 ∧ 열린 태스크 0 인 사람은 댓글을 만들지 않는다(생략)」 → **폐지**.
실기동 첫 발송(09-03)에서 천수정(활동 0·열린 0)이 빠졌고, 사용자 확정: 「0건이어도 전원 다 보여야
한다 — 그래야 조질 수 있다」. 새 계약:

- 개인별 댓글 모수 = **활성 조직 구성원 명부 전원**(태스크 보유 여부 무관) — C레벨(org_role
  ceo·coo·cto·cmo 유효 부여) 제외는 불변
- 0건인 사람도 5칸 전부 0 으로 표기
- 관련 문구 정합: §3.1 「개인 축」·§3.2 모수 서술이 「태스크 있는 사람」을 전제하면 함께 정정
- 개정은 취소선 + 날짜 + 사유(실기동 발견·사용자 확정) — 원문을 지우지 않는다
- 20-spec.md 최종 수정 체인에 한 줄 추가 + spec-120 front matter last_updated 갱신

검증: `python3 scripts/lint-pipeline.py --strict` 로 mediness 범위 신규 ERROR/WARN 0 확인.
**커밋·push·PR 금지** — 워크트리에 변경만 남긴다(코디가 검증 후 커밋한다).

코드는 코디가 병렬로 수정 중(dev 직반영) — 스펙이 코드 착지를 기다리지 않는다.

## (이하 완료 보고 — 원본 유지)
## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to <코디handle — stale 이라 미치환. 직접 확인해 채울 것> --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal <코디handle — stale 이라 미치환. 직접 확인해 채울 것> \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal <코디handle — stale 이라 미치환. 직접 확인해 채울 것> --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
