# [app] 채팅 3열 시험 앱 — clinic_chat 새로 세우기 (WORK-002 전체)

너는 **phub-gold-jev 앱 워커**(Python · 실험 앱)다. **앞 판의 맥락이 하나도 없다** — 아래 「읽을 것」만으로 일한다. 역할 문서는 backend 것을 따른다(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/backend/role.md` (+ 같은 폴더 `rules.md` · `workflow.md`) — 「PROCEDURE-HUB」 를 이 앱 레포로 바꿔 읽어라

작업 워크트리: `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev` (branch `kknaksss/phub-gold-jev`, base `origin/main` — 파일 3개뿐 · **공개 레포**) — 너 혼자 쓴다. `.env` 에 `TYPESAFE_API_KEY` 가 이미 있다(코디가 넣음 · gitignore). **값을 출력하지 마라.**

## 1. SSOT — 먼저 읽을 것

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev` · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(로컬 데이터 · 읽기만)

- `$W/WORK-002-app.md`(0.2.0) ← **구현 계획. WP-1 → WP-8 · 완료 조건 · 실물 확인 E1 ~ E6 · e2e 명령표 그대로**
- `$W/SPEC-002-chat-eval.md`(0.4.1) ← **계약. 여기 없는 건 발명하지 마라** · `$W/SPEC-001-hub-gold-mcp.md` §4 · 부록 A ← 허브 도구 계약(클라이언트 · 모의 허브의 꼴)
- `$W/_RESUME.md` §2 ← 결정(폭은 빠짐없이 · 깊이만 Jev · 안전 정보 강제 첨부 없음 · 틀린 말 검사만 · Sonnet 추론 없이 · CLI 구독 · 미확인 키로 채점 금지 · 세 상태도 단계 ⑤ 호출 · 테스트 ≠ 상담)
- Jev: `$P/para/resources/note/ai/llms.txt`
- 옛 틀(읽기만 · `git show HEAD:`): `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` — WORK-002 가 가리키는 파일:줄만. **옛 case3 걷기 · section · intent 체계는 가져오지 마라**

## 2. 배경

같은 질문을 A 원장 · B gold + Jev · C gold MCP 직접 세 열로 돌려 「질문 하나에서 연결된 정보가 빠짐없이 보이나」 를 잰다. 허브는 다른 워커(backend)가 PROCEDURE-HUB 에서 병행 구현 중 — 로컬 `127.0.0.1:18105`.

## 3. 계약

허브 도구 계약 = SPEC-001 §4 · 부록 A. **허브가 아직 없을 때는 WORK-002 §11 대로** — WP-1 · WP-2 · WP-5 를 먼저, WP-3 · WP-4 는 모의 응답(꼴만 · 규칙 계산 금지)으로 단위 시험까지. **코디가 「허브 준비」 를 알려 주면** 실물 연결(E4)과 WP-6 · 실물 확인을 진행한다. 그전에 할 게 없으면 그 상태를 코디에게 알리고 기다려라(§9 질문 방식).

## 5. allowed_paths

- 작업 워크트리 전체(새 패키지 · 테스트 · `pyproject.toml` · `uv.lock` · `.env.example` 에 env 이름 추가 · README 의 e2e 절).
- **공개 레포** — 키 · 회사 데이터 본문(질문 문장 · 답 · 원장 · gold 값) · 사용자 홈 절대 경로를 커밋될 파일에 넣지 마라. 세트 · 답 키 · runs 는 WORK-002 가 정한 gitignore 로컬 자리에만. 모의 허브 응답은 **가짜 코드 · 가짜 이름**.

## 6. 구현 단계

WORK-002 WP-1 → WP-8 (§11 순서 · 병행). 실물 확인 E1 ~ E6 은 네가 돌린다(Jev 1회 · `claude -p` Sonnet 1회 — 추론 끄기 가능 여부 첫 확인 · Haiku 1회 · 허브 1회 · 세 열 한 질문 · 합성 키 배관). 구독 · 키가 네 세션에서 안 잡히면 「못 돌림」 으로 보고(코디가 돌린다). 추가 32 문항은 WORK-002 대로 **draft 초안**까지(사용자 확정 대기).

## 7. 범위 제약 — 하지 말 것

- 커밋 · push · PR 금지(코디 몫). 사용자 포트(18005 · 18210) · 사용자 프로세스 금지. 허브 18105 는 backend 워커 · 코디가 띄운다 — 네가 허브 레포를 건드리지 마라.
- 실물 호출은 E1 ~ E6 범위만(전체 세트 batch 를 돌리지 마라 — 사용자 e2e 몫).
- SPEC · WORK 를 고치지 마라(구멍은 보고).

## 8. 검증

- `uv sync` · `uv run ruff check .` · `uv run pytest -q`(실호출 없는 시험) — 각 1회.
- E1 ~ E6 결과(성공 여부 · ms · 모델 id · 추론 끔 가능 여부) · WP-8 e2e 명령표가 실제로 도는지(한 질문 · 한 열).
- 끝에 `git -C <워크트리> status --porcelain --ignored` 로 커밋될 것 / gitignore 된 것 분리 보고 · 비밀값 grep 결과.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_95e86b96-831a-4d31-aa96-58649a80d244 --from term_9479e697-850b-415b-b319-691ac4f4d772 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "app 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 \
  --text "[worker_done] app 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 --text "[질문] app: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
