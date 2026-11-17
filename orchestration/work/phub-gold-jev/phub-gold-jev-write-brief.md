# [writer] SPEC-001 허브 gold MCP · SPEC-002 채팅 3열 비교 시험 — 초안

너는 **procedure-hub `writer` 워커**다. **앞 판의 맥락이 하나도 없다** — 아래 「읽을 것」만으로 일한다.
먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/writer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리(코디 워크트리 · 공유): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온`
base `origin/main` — 커밋 · PR 은 코디네이터 몫. **코디가 같은 트리에서 일한다 — 아래 두 파일 외에는 만들거나 고치지 마라.**

## 1. SSOT — 먼저 읽을 것

경로 접두어 `P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온`,
`W=$P/orchestration/work/phub-gold-jev`,
`SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model` (gitignore · 로컬 데이터).

1. `$W/_RESUME.md` §2 결정 표 ← **이 작업의 정본.** 여기 결정과 다르게 쓰지 마라
2. `$W/research-gold-connect.md` ← 조사 리포트. §0 「정할 것」 D1~D12 와 §1~§6 근거. **D 표의 결정 상태는 아래 §2 를 따른다**
3. `$P/para/resources/note/ai/llms.txt` ← Jev 사용 정본(Noul fan-out · answer_ready = 종료 제안 · 후보는 허용 관계에서만)
4. `$SM/gold/README.md` · `$SM/gold/semantic-map.md` · `$SM/gold/questions.csv`(헤더 · id · range · status 만 — 본문은 SPEC 에 옮기지 마라) · `g_*.csv` 헤더(`head -1`)
5. 옛 문서 꼴 참고(내용은 옛 체계 — **꼴만**): `$P/orchestration/work/phub-recommend/SPEC-005.md`(허브 · frontmatter 꼴) · `$P/orchestration/work/phub-recommend/SPEC-006.md`(앱) · `$P/reference/2026-10-30-hub-evals/README.md`(채점 두 층 · 가리기 · runs.jsonl)
6. 옛 코드(배관 재사용 판정 근거 · 읽기만): 허브 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`(`git show HEAD:` 로) · 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` · 배포 `~/git/PROCEDURE-HUB` 의 `git show origin/release/v1.2.0:docs/guides/deployment.md`

**기대는 개념**
- `$P/para/areas/concept/cs/artifact-traceability.md` — 모든 응답 행이 gid → g_evidence → silver → source_ref 로 되짚히게 계약을 쓴다

## 2. 배경 · 결정 상태

옛 PROCEDURE-HUB gold(PR #31)는 버리고, 11-16 확정한 새 gold 15표 기준으로 허브 MCP · 채팅 시험을 처음부터 다시 한다. 이번 판은 **SPEC 두 개 초안**이다. WORK(구현 계획)는 SPEC 이 사용자 리뷰를 통과한 뒤 따로 쓴다.

조사 리포트 D 표의 상태(사용자 11-16):

| D | 상태 |
|---|---|
| D1 허브 자리 | **정함** — PROCEDURE-HUB `release/v1.2.0` 에서 새 브랜치 · 새 모듈. 고도화해 **stg 로 올린다**(다른 서비스가 쓰도록). 머지 · 배포 · stg 데이터 반입은 각각 별도 승인 |
| D2 저장 | **정함(조사 추천에서 바뀜)** — **DB 없음.** gold CSV 15 + silver `source_ref` 를 허브 시작 때 메모리로. gold 해시 기록 · 응답 머리에. DB화는 시험 뒤 「다음 범위」 — **repository 층만 바꾸면 되게** |
| D3 source_ref | 추천 채택 — 적재(메모리) |
| D4 도구 | 추천 채택 — 조사 §6-3 의 8도구 |
| D5 호출 길 | 추천 채택 — 앱 걷기 = REST · LLM 직접 질의 = MCP · 같은 service 코어 |
| D6 Jev 판단 지점 | 추천 채택 — 범위 Choice 1 + 후보 Noul fan-out + answer_ready Noul · 입구 겹침은 범위 규칙 먼저 |
| D7 Noul 문턱 | 추천 채택 — 임시 yes 0.7 · no 0.3 · 사이 보류, 1회차 trace 로 보정(설정값) |
| D8 LLM | **정함** — 지금 **CLI 구독**(로컬 로그인 · `claude -p`), DB화 때 SDK. 답 모델 = **Sonnet 또는 Haiku**(설정으로 고름). 채점 = Opus 기본(코디 기본값 · 사용자가 바꿀 수 있음) |
| D9 앱 자리 | 추천 채택 — clinic_chat 새 브랜치(main 기준) · 새 case 모듈 |
| D10 Jev 언어 | 추천 채택 — instructions 영어 · state 는 한국어 이름 + 코드 |
| D11 시험 세트 | **초안으로 쓴다(사용자 리뷰)** — 37 + 조사 §5-3 추가 묶음 + **범위 밖 질문**(비교 · 문헌 등 — 「범위 밖」 종료 확인) |
| D12 역방향 >255 | 추천 채택 — Noul 32개 묶음으로 전부 |
| 비교 열 | **정함 — 3열**: A 원장 JSON(LLM 이 도구로 원장 탐색) · B gold 그래프 + Jev(제품 구조) · C gold MCP 직접(Jev 없음). 같은 질문 · 같은 LLM · 같은 답 프롬프트 |
| 채점 기준 | **정함** — questions.csv 답 키(silver 유래). 원장 ≠ silver 곳(`$SM/notes/ledger-check-list.csv`)에서 A 가 원장 값을 말하면 「원장 오류 따라감」 으로 따로 셈 · 원장 = silver 질문만 모은 점수 따로(공정성) · 두 층(결정론 검사 + LLM 채점 가리기) |
| 질문 범위 | **정함** — 37 은 표본. 채팅은 범위 8 안의 아무 질문. 범위 밖은 지어내지 않고 「범위 밖」 종료 |

## 3. 계약 — 쓸 문서 두 개

### `$W/SPEC-001-hub-gold-mcp.md` (허브)

frontmatter 는 옛 SPEC-005 꼴(type · id · title · status: draft · product · feature: phub-gold-jev · version 0.1.0 · created_at/updated_at 2026-11-16 · links.decisions/sources). 절:

1. 목적 · 범위(허브 = 결정론 · LLM 없음 · 읽기 전용) · 범위 밖
2. 입력 데이터 — gold 15표 + `source_ref` · 로컬 경로 env(이름 제안) · 시작 때 적재 · 파일별 sha256 + gold 해시(gold-check 값) 기록 · 적재 실패 = 시작 실패 · **레포에 CSV 커밋 금지**
3. 계층 — router(REST) · MCP 서버 → service(공용 코어) → repository(지금 CSV 메모리 · 나중 DB 로 갈아끼움). 메모리 색인 목록(조사 §6-2 의 색인 열을 메모리 색인으로)
4. **도구 8 계약** — 도구마다 입력(이름 · 타입 · 필수 · 기본값 · 한도) · 출력(필드 이름은 gold CSV 헤더 그대로) · 읽는 표 · 쪽 넘김(cursor) · 오류. 공통 응답 머리 `build{gold_hash, loaded_at}` · `request` · 행마다 `gold_table` · `gid` · `evidence_kind` (+ `layer{role, path, holder}`). REST 경로 · MCP 이름 대응 표
5. 조회 규칙 — semantic-map §5 물려받기 · §6 범위별 표 · resolve(norm 식 = `gold-build.py` norm 과 같게 · 조사 떼기 목록) — 규칙 원문을 베끼지 말고 절 번호로 가리키고, 도구가 지켜야 할 것만
6. 근거 추적 — evidence 도구로 gid → g_evidence → source_ref
7. 옛 PR #31 에서 가져갈 틀 / 버릴 것(조사 §3-3 그대로 · 파일 경로)
8. stg — 경로(feat → release/v1.2.0 → stg PR · Azure 자동 · `deployment.md`) · 이번 판은 **로컬 시험까지**. stg 데이터 반입 방법은 **열린 것**
9. 시험(허브 단위) — 데이터 env 없으면 skip · 도구별 기대(37 문항의 gold_pointers 로 되짚기)
10. 열린 것 — 결정 안 된 것만(번호 · 추천)

### `$W/SPEC-002-chat-eval.md` (앱 · 실험)

frontmatter 같은 꼴. 절:

1. 목적 — 3열 비교로 「gold + Jev」 제품 구조가 원장 대비 정확 · 안전 · 빠른지
2. 열 정의 A · B · C — 각 열의 정보 경로 · 같은 것(질문 · LLM · 답 프롬프트 · 모델 설정)과 다른 것. **A 의 원장 탐색 도구를 어떻게 줄지**(예: CLI 의 Read/Grep 을 원장 폴더로 제한 · 앱 로컬 MCP)는 선택지 + 추천으로 열린 것에
3. B 걷기 루프 — 조사 §6-4 단계 0~8 · 범위별 허용 표 · Jev 요청 꼴(state 필드 · 질문 id 규칙 · 32 묶음) · 문턱(설정) · 방문 장부
4. 앱 hard gate — 조사 §6-4 의 목록(점수로 빼면 안 되는 것)
5. 종료 상태 — 근거 충족 · 후보 소진 · 원천 미확정 · 실행 중단 · **범위 밖** · 입구 없음 — 각각 답에서 어떻게 말하나
6. LLM 호출 — CLI 구독(`claude -p` · 모델 Sonnet/Haiku 설정) · 옛 `llm/cli.py` 에서 가져갈 것 · 답 프롬프트 원칙(verified 행만 · 인용은 gid)
7. 기록 — runs.jsonl 한 질문 한 줄 · 열별 단계 ms · 토큰 · Jev/도구 호출 수 · trace(후보 · Noul · 결정 · 이유) · model id
8. 채점 — 기준(답 키) · ① 결정론 검사(코드 · 숫자 · gate 위반) ② LLM 채점(Opus · 열 가리기 · 순서 섞기 · 열마다 따로) · 항목(정확성 · 안전 · 불확실 표시 · 근거 추적) · 「원장 오류 따라감」 분류 · 점수 두 벌(전체 / 원장 = silver 질문만)
9. 시험 세트 초안 — 37(id · range 만 표로) + 추가 묶음(묶음 이름 · 문항 수 · 무엇을 보나) + 범위 밖. **질문 문장은 SPEC 에 쓰지 말고** 세트 파일 위치(gitignore 로컬)만 정한다 · 답 키 만드는 법
10. 지표 · 보고서 꼴 — 열별 표 · 범위별 · 상태별
11. 열린 것

## 4. 먼저 읽을 핵심 파일

- `$W/research-gold-connect.md` §0 · §1-6 · §3 · §5-2 · §5-3 · §6
- `$SM/gold/semantic-map.md` §1 · §3 · §5 · §6
- `$P/para/resources/note/ai/llms.txt` §2 · §3 · §4

## 5. allowed_paths — 이 밖은 건드리지 마라

- `$W/SPEC-001-hub-gold-mcp.md` · `$W/SPEC-002-chat-eval.md` **두 파일만** 새로 쓴다.
- `_RESUME.md` · 조사 리포트 · 브리프 · 데이터 · 코드 레포는 읽기만. 임시 파일은 네 세션 scratchpad 에만.

## 6. 진행

1. 읽을 것을 읽는다.
2. SPEC-001 → SPEC-002 순서로 쓴다. 모든 요구에 근거(`_RESUME §2 날짜` · 조사 리포트 절 · 파일:줄)를 단다.
3. 스스로 검사(§8) 후 보고.

## 7. 범위 제약 — 하지 말 것

- **결정을 새로 만들지 마라.** §2 에 없는 정책은 「열린 것」 으로 추천과 함께.
- 옛 체계(노드 13종 · fact section 18 · intent 12 · 25타입 247필드)를 새 계약에 끌어오지 마라.
- **공개 레포다** — 회사 데이터 본문(시술 설명 · 원장 문장 · 답 원문 · 가격 · 질문 문장) · 비밀값 · 내부 URL 을 쓰지 마라. 표 · 칸 이름 · 코드 · 셈 · 질문 id 까지. 공개 도메인이 아닌 회사 호스트는 「stg Gateway」 처럼 이름으로만.
- 외부 API(Jev · Claude 등) 호출 금지 · `.env` 열지 마라 · 서버 · docker 띄우지 마라 · 코드 레포 작업 트리 변경 금지.
- WORK 문서는 이번에 쓰지 마라.

## 8. 검증

```
모든 결정·요구가 _RESUME §2 결정 · 조사 리포트 · 코드(파일:줄) 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. public — 키 · 토큰 · 실명 0(grep)
```

- 도구 8 의 출력 필드 이름이 실제 gold CSV 헤더와 같은지 스크립트로 대조하고 결과를 보고에 적는다.
- `git -C $P status --porcelain` 에서 네 변경이 두 파일뿐인지 확인(코디 변경은 무관).
- 회사 데이터 본문 · 비밀값 grep 결과를 보고에 적는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_95e86b96-831a-4d31-aa96-58649a80d244 --from term_52911d22-9af5-40fc-a00c-850bdce66f86 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
