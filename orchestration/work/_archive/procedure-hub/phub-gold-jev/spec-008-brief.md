# [writer] SPEC-008 상담 입구 소넷 전환(앱 0.4) + SPEC-001 0.8.0 resolve 축소 — 초안

너는 **procedure-hub `writer` 워커**다. 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/writer/role.md`(+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`). Procedure Hub 데이터 공개. 키 · 비밀값 금지.

경로: `P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev` · 앱(읽기만) `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev` · 허브(읽기만) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`.

## 1. 정본 — 먼저 읽을 것

1. `$W/_RESUME.md` §2 **맨 위 11-18 행 전부**(D-1 ~ D-15 · 「소넷으로만 — Jev 뺌」 · 「resolve 최소 목록 꼴 · 입력 정리는 채팅 단」). **여기와 다르게 쓰지 마라 · 다시 논의하지 마라.**
2. `$W/research-input-space.md`(실패 층 · AR-1~12 앱 규칙 자리 · DA-1~6 · §3 소넷 시안) + `$W/research-input-space/pick-prompt.md`(시안 프롬프트 · 호출 인자) + `$W/review-input-space.md`(검수 WARN — R-1~R-11 · 빠진 정할 것 → D 표로 닫힘).
3. 지금 계약: `$W/SPEC-006-consult-v03.md`(상담 0.3 — 객체 · 장부 · 화면 · SSE) · `$W/SPEC-005-consult-state.md` · `$W/SPEC-004-consult-chat.md` · `$W/SPEC-001-hub-gold-mcp.md`(0.7.2 — §4-1 · §5-1 · NM) · `$W/SPEC-002-chat-eval.md`(걷기 ①~③ — 시험 앱 B 열).
4. 앱 코드(지금 동작 근거): `clinic_chat/consult/turn.py` · `state.py` · `plan.py` · `carry.py` · `turn_kind.py` · `blanks.py` · `sites.py` · `listing.py` · `walk/front.py` · `entry.py` · `depth.py` · `value_pick.py` · `llm/chat_cli.py` · `prompts/consult.json`.

## 2. 쓸 것

### `$W/SPEC-008-consult-entry.md` (앱 · 상담 0.4 · 새 문서)

frontmatter 는 SPEC-006 꼴(version 0.1.0 · created 2026-11-18 · links.decisions = `_RESUME` §2 11-18 행). 절:

1. 목적 · 범위 — 상담 켠 상태(CHAT_STATE=on)의 턴 흐름에서 **Jev 와 resolve 맞춤 꼴을 걷어 내고** 소넷 「이해」 호출 하나로 바꾼다. 시험 앱 B 열 · 상담 끈 상태 경로는 범위 밖(D-2 — 옛 판 그대로 · 코드 경로를 나눠 둔다).
2. **새 턴 흐름** — 단계별 입력 · 출력 · 실패: ① 목록 적재(허브 resolve 목록 꼴 · gold_hash 단위 캐시 · 820 항목 + 별칭 — D-3) ② **이해 호출**(소넷 · thinking 끔 D-4 · 같은 격리 인자 · 시스템 글 = 규칙 + 목록 · 턴 메시지 = 대화(손님 말 · 그 턴 대상 · **앞 답 요약 · 보여 준 리스트 이름** D-8) + 객체 + 이번 말) → JSON 출력 계약(대상 `[{table, code, sure: true|false}]` D-9 · 턴 종류 · 이번 턴 부위 · 거둠 · **정보 종류**(D-11 · 지금 KIND 14 코드 그대로)) ③ 앱 검증(gold 에 없는 코드 버림 · 셈 · D-7 같은 이름은 가장 넓은 것 하나) ④ 객체 갱신(애매 = guess + 되묻기 · D-5 말 안 한 고민 안 붙임 · D-6 부위 잇기 조건 · D-12) ⑤ 객체 기준 조회(부위 거르개 = **이번 턴 부위만** · AR-4) ⑥ 화면(점 = **말한 고민 부위만** · AR-5) ⑦ 빈 칸 · 되묻기 ⑧ 답(소넷 · 지금 그대로) ⑨ 장부.
3. **값 고르기 · 깊이 판단 자리(D-11)** — 지금 걷기 ②~③(depth · value_pick · answer_ready)가 상담에서 하는 일을 먼저 세고(코드 근거), 소넷 꼴로 둘지 · 객체 기준 조회로 이미 덮여 필요 없는지를 판정해 계약으로 쓴다. 필요 없다고 판정하면 그 근거(그 단계가 상담 답 재료에 보태던 것)를 표로.
4. 실패 길(D-10 — 10초 · 오류 · JSON 깨짐 → 대상 없이 되묻기 · 옛 resolve 로 안 돌아감) · 설정값 목록(이름 · 기본값 — 모델 · 시간 한도 · 별칭 넣기 · 목록 캐시).
5. 앱 규칙 고칠 곳 — AR-1 ~ AR-12 마다 새 흐름에서 **없어짐 / 고침 / 그대로** 와 고친 꼴(DA-1 은 AR-11 조회 규칙으로: 부위만 → `concern_site` 로 선택지).
6. 장부 · 패널 · SSE 변경(지금 필드 가운데 없어지는 것 — Jev noul · resolve 후보 · 입구 고르기 — 와 새 필드 — 이해 호출 입력 바이트 · 출력 · 버린 코드 · ms).
7. 프롬프트 — `prompts/consult.json` 새 절(이해 호출 규칙) 초안 · 시안 `pick-prompt.md` 를 바탕으로 하되 **예문은 입력 전수 표 턴과 겹치지 않게**(검수 R-4). 초안 표지 · 사용자 확인 대상.
8. 시험 — 입력 전수 표 재실행이 완료 조건(D-14: 앱 전체 8 검사 90%↑ · 입구 3 검사 95%↑ · 정답 키 꼴마다 표본 사람 검수 · 애매 14 채점 밖 D-15) + 단위 시험 목록(검증 · 객체 · 부위 거르개 · 점 · 실패 길).
9. 정할 것(있으면 · 추천 붙임 — D 표로 닫힌 것은 다시 올리지 마라).

### `$W/SPEC-001-hub-gold-mcp.md` → **0.8.0** (허브 · 고침)

- 맨 위 변경 기록에 0.8.0: **resolve 맞춤 꼴 = 정확한 이름 → 코드만**(D-1). `text` 의 `norm` 이 `g_entry.norm` 과 **같을 때만** 후보 · 부분 일치(R2) · 덮임(R7 `covered_by`) · 줄임(NM · `abbr`) 지움. 목록 꼴 그대로. 응답 필드를 어떻게 남길지(지울 것 · 남길 것 · `matched` 꼴)를 표로 — 쓰는 곳(허브 MCP · 앱 상담 · 시험 앱 B 열)별 영향 표. 시험 앱 B 열은 D-2 로 옛 판(0.7.2 커밋)에 묶는다는 것을 적는다.
- §4-1 · §5-1(R1~R8) · §5-11 NM · 시험 표(T15 · NM 시험) 를 그에 맞게 고친다. 다른 도구 계약은 건드리지 않는다.

## 3. allowed_paths

쓰기: `$W/SPEC-008-consult-entry.md`(새) · `$W/SPEC-001-hub-gold-mcp.md`(0.8.0 고침) **둘만**. 임시는 scratchpad. 같은 폴더에 다른 문서가 많다 — 건드리지 마라.

## 4. 하지 마라

코드 · 데이터 수정 · 서버 · DB · LLM · Jev 호출 금지. 정해진 결정을 바꾸지 마라. 화면 문구를 지어 넣지 마라(시안 · SPEC 에 없으면 빈칸 + 정할 것).

## 5. 완료 보고 — 문구 변경 금지

> 핸들 · taskId · dispatchId 는 dispatch preamble 값을 믿어라.

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer(SPEC-008 · SPEC-001 0.8.0) 완료: <한 줄>" \
  --body "변경 파일 / 절 요약 / AR 처분 수 / 정할 것 / 주의점" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] writer(SPEC-008) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
