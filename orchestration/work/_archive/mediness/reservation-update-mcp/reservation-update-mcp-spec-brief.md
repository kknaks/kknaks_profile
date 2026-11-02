
# [planner] 스펙 반영 — ① 사후 변경 MCP 툴 신설 계약 ② 시각 해석 규칙 개정 (명시 날짜·시간 존중 + 지난 시간 되묻기)

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

이 워크트리는 지금 planner 너 혼자다. base 는 방금 머지된 SPEC-151 §7.9(예약→회의 체인, PR #665) **포함** 상태다.

## 1. SSOT — 먼저 읽을 것

- `products/mediness/20-spec/spec-151-ax-assistant-reservation.md` — 채팅·예약 게이트 계약. ① 의 사후 변경 게이트(§5.1·§6.2)와 ② 의 접수 계약이 여기 산다
- `products/mediness/20-spec/spec-060-*.md` (MCP 툴 인벤토리 소유 SPEC — 정확한 파일명은 리포에서 확인) — ① 툴 등재 자리. `mediness.reservation_cancel_request` 가 등재된 방식이 표본
- 코드 실측 참조 (mediness-app read-only, 절대경로 `/Users/kknaks/orca/workspaces/mediness-app/reservation-update-mcp/`):
  - `mcp/app/tools/reservation_cancel_request.py` — ① 의 동형 표본 (off-graph amendment 카드 생성 · 409 amendment_target_invalid)
  - `mcp/app/tools/reservation_revise.py` — 승인 대기 전용 손. docstring 의 「REST 는 있었고 MCP 손만 없었다」 전례가 이번 ① 과 같은 결
  - `back/app/routers/action_runtime_v2.py:2027-2059` — cancel-request·update-request REST 두 형제 (update 쪽만 MCP 손이 없다)
  - `back/app/services/action_runtime/chat/provider.py:26-30` — ② 의 대상 `TIME_RESOLUTION_RULE` 원문
  - `back/app/schemas/` 및 접수 검증 — ② 에서 「지난 시각 시작」을 서버가 거부하는지 실측할 것

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

**① 사후 변경 MCP 손 부재** (2026-08-31 prod 실사용 실측): MCP(에이전트) 표면으로 잡은 완료 예약을 사용자가 "시간 변경해줘" 하면 에이전트가 「승인난 회의는 변경이 안 된다」고 답한다. 실제로는 back REST(`POST /reservations/{run_id}/update-request`, off-graph 변경 amendment 카드)가 **있는데 MCP 툴만 없다** — cancel 은 `reservation_cancel_request` 로 있고 update 만 빠졌다. `reservation_revise` docstring 에 기록된 것과 같은 실패 모드의 재발이다.

**② 시각 해석 규칙의 침묵 조정** (2026-08-31 prod 실측, actions `918e4411`): 15:08 에 "오늘 오후 3시부터 4시까지" 예약 요청 → 시작 시각이 8분 지났다는 이유로 **말없이 9/1 15:00 으로** 잡혔다. 현행 `TIME_RESOLUTION_RULE` 은 "지난 시각 + 명시 날짜 없음 → 내일" 만 규정해, 명시 날짜가 있는 충돌 케이스를 모델이 임의로(침묵 조정으로) 메꿨다.

## 3. 계약 (2026-08-31 사용자 확정 — 재론 금지, 이대로 스펙에 반영)

**①** `mediness.reservation_update_request` 툴 신설 계약 — 기존 update-request REST 의 thin wrapper. `reservation_cancel_request` 와 동형(카드 즉시 생성·409 계약·leaf = 감싸는 REST 의 leaf — 새 leaf·새 REST 신설 0). 인벤토리 등재 방식도 cancel 선례 그대로.

**②** 시각 해석 규칙 개정:
1. **명시적 날짜+시간이 있으면 그 날짜·시간 그대로 잡는다** — 침묵 조정(내일로 밀기) 금지. "오늘 15시" 를 15:08 에 요청해도 오늘 15:00 이다 (진행 중 회의도 방은 지금 필요하다).
2. **명시한 시각이 이미 완전히 지났으면 턴을 하나 더 써서 되묻는다** — 「이미 지난 시간인데 예약을 잡을까요?」 → **잡아 달라 = 말한 그대로 카드 생성(승인 게이트 진행)** / **아니 = 취소(카드 미생성)**.
3. 기존 규칙 중 유지되는 것 — 오전/오후 모호 시각의 「가장 가까운 미래」 해석, 날짜를 안 준 지난 시각의 「내일」 조정. 바뀌는 것은 **명시 날짜가 있는 경우의 처분**뿐이다.
- ⚠ **서버 검증 대조 필수**: 접수·실행 경로에 「시작이 과거면 거부」 검증이 있는지 실측하고, 있으면 ②-2 의 「그대로 잡기」가 통과하도록 계약을 어디까지 여는지(접수 허용 범위·THE CONNECT 거부 시 표면화)를 스펙이 정의한다. 코드가 막고 있는데 프롬프트만 고치면 침묵 실패가 침묵 조정 자리를 대신할 뿐이다.

## 4. 먼저 읽을 핵심 파일

§1 의 코드 실측 참조 5개. v1/모달 경로는 무관 — 건드리지 마라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/mediness/`
- `context/`

## 6. 구현 단계

1. §1 문서·코드 실측을 읽고, ① 의 소유 절(SPEC-060 인벤토리 + SPEC-151 MCP/게이트 절)과 ② 의 소유 절(SPEC-151 접수·시각 해석 자리 — 없으면 어디 신설할지 판단)을 확정한다.
2. ① 툴 계약을 개정으로 반영한다 — cancel 선례와 동형임을 명시하고, 다른 것(대상 축·입력 shape)만 적는다.
3. ② 규칙 개정을 반영한다 — §3-② 의 3항 + 되묻기 턴의 계약(질문 문구 축·예/아니오 각 처분·카드 생성 시점) + 서버 검증 대조 결과. 실측과 스펙이 갈리면 코드에서 정하지 말고 스펙이 정본을 정한다.
4. log.md 에 entry. 개정 노트는 각 SPEC 관례대로.

## 7. 범위 제약 — 하지 말 것

- **WP·코드 작성 금지** — 다음 발주다. 새 REST·새 leaf·새 카드 유형 신설 금지 (① 은 wrapper 뿐이다).
- §3 확정을 재론하지 마라. 모순되는 사실을 발견하면 §9 방식으로 물어라.
- 회의 자동 등록 체인(§7.9)·모달 경로·회의관리 화면은 무개정 — ① 의 변경 카드가 승인·실행되면 §7.9.5 파급이 **이미** 회의를 따라가게 한다. 그 사실을 ① 계약에 참조로만 적는다.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → mediness 범위 ERROR 0 (타 제품 기존 WARN 무관 분리). 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
