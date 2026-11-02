
# [planner] 환류 — §7.2 문면 정정(코드 실측) + §7.9.6 채팅 표면 문면 (PR #665 브랜치)

너는 **mediness `planner` 워커**다. WP-125 코드 착지(P0 실사)에서 스펙 문면 2곳이 코드 실측과 어긋난 게 확인됐다. **문면 환류만** 한다 — 계약 재설계 아님.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec` (브랜치 `meeting-room-workflow-spec`, PR #665 열려 있음 — base 는 커밋된 상태, 네 변경은 미커밋으로 남겨라)

## 1. 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/wp125-backend-report.md` §6 — P0-② 실측 상세 (§7.2 불일치의 근거)
- `products/mediness/20-spec/spec-151-ax-assistant-reservation.md` §7.2 · §7.9.6

## 2. 고칠 것

**① §7.2 참석자 해소 문면 정정 (W-6)** — 문면은 「organization_member.display_name / work_email」인데 코드 실측은 **users.name / users.email 조인**이다(workflow.py 정방향 술어). §7.2 의 해당 서술을 코드 실측에 맞게 정정하라 — 어느 원장의 어느 컬럼을 읽는지 정확히. §7.9.3 의 「코드가 SoT · 술어를 되쓴다」 문면과 이제 정합해야 한다. 개정 노트에 한 줄(코드 실측 환류·판정 동작 변경 0)을 남겨라.

**② §7.9.6 채팅 표면 문면 정정 (W-2 코디 판정)** — 「채팅: 완료 안내에 회의도 등록됐다는 한 줄이 붙는다」가 실제 구조와 다르다. BE 에 고정 문구 템플릿이 없고 **채팅은 카드 참조를 렌더**하며 회의 참조·미등록 사유는 **카드 facts** 에 실린다(코드 착지 확정). §7.9.6 채팅 행을 그 구조대로 고쳐라 — 별도 문구 신설이 필요해지면 그때 별건이라는 단서 포함.

log.md 는 기존 spec-change 행(PR #665)에 이 환류를 반영할 한 구절만 추가 (새 행 만들지 마라 — 같은 PR 이다).

## 3. 하지 말 것

- 위 2곳 외 개정 금지. §7.9 계약 본문·WP-125 무변경. 커밋·push 금지(코디가 한다).

## 4. 검증

```
python3 scripts/lint-pipeline.py --strict → mediness 범위 ERROR 0. 1회만
```

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_6a44553f-d13c-48f6-93ab-bda16d83ffec --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "2곳 각각 처리 / lint 결과"

# (2) 직접 주입
orca terminal send --terminal term_6a44553f-d13c-48f6-93ab-bda16d83ffec \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6a44553f-d13c-48f6-93ab-bda16d83ffec --text "[질문] planner: <질문>" --enter`
