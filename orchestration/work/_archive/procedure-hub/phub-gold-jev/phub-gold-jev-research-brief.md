# [researcher] 새 gold × 허브 MCP × Jev × LLM 연결 — 처음부터 다시 짓기 위한 조사

너는 **procedure-hub `researcher` 워커**다(read-only). **앞 판의 맥락이 하나도 없다** — 아래 「읽을 것」만으로 일한다.
먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리(코디 워크트리 · 공유): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온`
base `origin/main` — PR 은 코디네이터 몫. **코디가 같은 트리에서 일한다 — 리포트 파일 1개 외에는 아무것도 만들거나 고치지 마라.**

## 1. SSOT — 먼저 읽을 것

이 작업의 경로 접두어 `P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온`,
`SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model` (gitignore · 로컬 데이터).

**새 데이터(이번 기준)**
- `$SM/gold/README.md` · `$SM/gold/semantic-map.md` · `$SM/gold/gold-final-notes.md` ← 새 gold 15표의 정본
- `$SM/gold/g_*.csv`(15표) · `$SM/gold/questions.csv`(37문항) · `$SM/gold/gold-build.py` · `$SM/gold/gold-check.py`
- `$SM/notes/silver-erd.md` · `$SM/notes/silver-tables.md` · `$SM/notes/glossary.md` · `$SM/notes/vocabulary.csv`
- `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/_RESUME.md` §2 결정 표(특히 11-16 gold 결정: 저장소 = 관계형 먼저 + 그래프 내보내기 · 근거 표 참조)

**Jev 사용법(이번 기준)**
- `$P/para/resources/note/ai/llms.txt` ← 공식 llms.txt 정리. **후보마다 Noul + answer_ready Noul 한 요청 · 하나만 고를 때만 Choice · 후보는 허용된 관계에서만 · 종료는 앱이 검증.** 원문 링크가 그 안에 있다
- `$P/orchestration/work/phub-recommend/wp10-typesafe-primitive-correction.md` ← Choice 반복 → Noul 로 바꾼 정정
- `$P/orchestration/work/phub-recommend/jev-research.md` §1~§3 · §7(255 선택지 한도 · 한국어 · 순서 기울기)

**옛 구현(잘못된 옛 gold 위에 지은 것 — 이어 쓰지 않는다. 배관 재사용 여부만 본다)**
- 허브: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` 브랜치 `kknaksss/phub-recommend`(PR #31) — `backend/app/modules/gold/*` · `backend/app/router/gold.py` · `backend/app/model/gold.py` · `backend/app/schema/gold.py` · `backend/alembic/versions/b2026103*` · `backend/scripts/gold_*.py` · `backend/docs/gold-local.md` · 레포 `AGENTS.md`
- 앱: `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 브랜치 `kknaksss/hub-evals` — `clinic_chat/clients/{jev_client,hub_mcp,hub_rest,anthropic_client}.py` · `clinic_chat/llm/` · `clinic_chat/cases/{case3,loop}.py` · `README.md`
- 두 레포 모두 **미커밋 수정이 있다**(허브 8파일 · 앱 16파일 — 11-02~03 WP-8~10). **건드리지 마라**(stash · checkout · reset 금지). 커밋본은 `git show HEAD:<경로>`, 미커밋은 `git diff` 로 읽기만. 리포트에서 둘을 구분해 적는다.
- 옛 설계 흐름 참고: `$P/reference/2026-10-30-hub-evals/HANDOFF.md` · `$P/reference/2026-11-03-procedure-hub-data-and-traversal/WORK.md`(§4~§6 탐색·종료 원칙은 유효, 그 안의 「25타입 247필드 설계안」은 11-04 에 폐기됨) · `$P/orchestration/work/phub-recommend/phub-recommend-jev-walk-addendum.md`

**기대는 개념**
- `$P/para/areas/concept/cs/artifact-traceability.md` — 연결 설계의 모든 응답이 gold 행 → silver 근거로 되짚어져야 한다는 기준으로 쓴다

## 2. 배경

옛 PROCEDURE-HUB gold(PR #31)는 데이터 설계가 틀린 위에 지어져 버린다. 11-16 에 silver 57표 · gold 15표를 새로 확정했다
(gold-check: 되짚기 · 값 포함 · 재빌드 해시 통과, 구조 문제 0). 이제 **새 gold 를 기준으로 허브 MCP · 질문 시험을 처음부터 다시** 한다.
런타임 구조는 유지: 질문 → 허브(결정론 · LLM 없음)에서 후보 → Jev(llms.txt 방식)로 갈래 판단 → 앱이 근거·범위·종료 검증 → LLM 이 답 생성.

이 조사는 **연결 설계안과 시험 질문을 사용자와 닫기 위한 재료**다. 너는 결정하지 않는다 — 추천과 근거를 붙여 「정할 것」으로 모은다.

## 3. 계약

해당 없음(조사).

## 4. 질문 — 각 답에 근거(파일:줄 · 표.칸 · 셈 명령과 결과)를 붙여라

**Q1. 새 gold 구조**
- 15표 각각: 역할 · 키 · 행 수 · 다른 표와 잇는 칸. `g_node.node_table` 별 노드 수, `g_edge.edge_type` 별 엣지 수(src/dst 노드 종류 쌍까지).
- 근거 경로: gold 행 → `g_evidence` → silver 표·행. 응답에 근거를 실을 때 필요한 최소 칸.
- `semantic-map.md` §5(물려받기 `g_scope`) · §6(표 ↔ 질문 범위)을 요약해 **조회 규칙**을 표로.

**Q2. 옛 허브가 읽는 구조(PR #31 커밋본)**
- 입력(ingest) 형식 · DB 스키마(모델 · alembic) · 빌드 · 발행 단위.
- 도구 전부(MCP `tools.py` · `mcp_server.py` · REST `router/gold.py`): 이름 · 입력 · 출력 꼴 · 쓰는 옛 표/칸. T1 resolve · T8 neighbors · T9 vocab 등 번호 체계 그대로.

**Q3. 옛 ↔ 새 대조**
- 옛 도구마다: 새 gold 로 그대로 가능 / 바꿔야 함(무엇을) / 불가 / 필요 없음.
- 새 gold 로 질문 37개를 돌리는 데 **새로 필요한 도구**(예: 노드의 이웃 후보를 허용된 관계로 · 노드의 facet(효과·부작용·금기·같은 날·회복·상품) 읽기 · 근거 펼치기).
- 배관 재사용 판정: 서버 골격 · MCP 서버 틀 · 빌드/발행 · resolve(조사 떼기 등) · 테스트 틀 — 「다시 쓴다 / 틀만 가져간다 / 버린다」와 이유.

**Q4. 앱(clinic_chat) 배관**
- Jev 클라이언트 · LLM 호출(CLI · SDK) · 걷기 루프 · 기록(trace · runs) 구조. 커밋본과 미커밋(WP-10 Noul 정정)이 각각 llms.txt 패턴과 어디서 맞고 어디서 어긋나는지.
- 새로 지을 앱에서 가져갈 것 / 버릴 것.

**Q5. 질문 37개 × 걷기**
- 질문마다 한 행: id · 범위 · 시작 노드 종류 · 거칠 엣지 종류 · 읽을 gold 표 · Jev 판단 지점(Choice 인지 Noul fan-out 인지, 후보 수 셈 — 255 넘는 곳 표시) · 앱 hard gate(안전·금기 등 점수로 빼면 안 되는 것) · 현 상태(답함/원장 확인/silver 빈칸).
- 후보 수는 실제 gold 에서 센다(예: 그 노드의 이웃 수 최대·중앙).
- 시험 세트 추천: 37개를 그대로 쓸지, 무엇을 더할지(예: 오타 · 두 시술 · 해당 없음 · 원장 확인 상태 질문) — 추천만.

**Q6. 연결 설계 선택지**
- 허브: PROCEDURE-HUB 의 어디에(새 브랜치 base `release/v1.2.0` 전제), 저장(11-16 결정 「관계형 먼저 + 그래프 내보내기」를 따를 때 표 → DB 스키마 대응), 적재(gold CSV 그대로 ingest?) · 버전/해시.
- MCP 도구 최소 집합 초안(이름 · 입력 · 출력 · 읽는 표 · 근거 실림).
- 앱: Jev + LLM 걷기 루프 초안(llms.txt §3 그대로) · 종료 상태(근거 충족 / 후보 소진 / 원천 미확정 / 실행 중단) · 기록할 것.
- 선택지마다 추천 · 근거 · 위험. 마지막에 **「정할 것」 표**(사용자가 고를 것만 · 각각 추천 포함).

## 5. allowed_paths — 이 밖은 건드리지 마라

- **쓰기: `$P/orchestration/work/phub-gold-jev/research-gold-connect.md` 1개만.**
- 그 밖은 전부 읽기 전용. 임시 파일이 필요하면 네 세션 scratchpad 에만.

## 6. 진행

1. 「읽을 것」을 읽는다.
2. Q1 → Q6 순서로 셈 · 대조 · 정리. 셈은 python/csv 로 직접 하고 명령을 리포트에 남긴다.
3. 리포트 머리에 **요약(질문당 2~3줄) + 「정할 것」 표**, 본문에 근거.

## 7. 범위 제약 — 하지 말 것

- **결정하지 마라.** 추천은 하되 「정할 것」으로 모은다.
- **Jev · Claude · Codex 등 외부 API 를 호출하지 마라.** 키를 읽거나 출력하지 마라(`.env` 열지 마라).
- 서버 · docker 를 띄우지 마라. 사용자 포트(18210 등)를 건드리지 마라.
- 두 코드 레포의 작업 트리를 바꾸지 마라(stash · checkout · reset · 파일 수정 금지). fetch 도 하지 마라.
- **공개 레포다 — 리포트에 회사 데이터 본문을 싣지 마라.** 표 이름 · 칸 이름 · id · 셈 · 질문 id/범위까지만. 시술 설명 · 원장 문장 · 답 원문 · 가격 값 인용 금지. 비밀값 · 내부 URL 금지.
- silver/gold 를 고치지 마라. `gold-check.py` · `silver-check.py` 는 돌려도 된다 — 코디가 11-16 원장 경로를 고쳤다(A3 통과). 남는 FAIL 은 G1 · G3(silver-check) · 그로 인한 A2 — 이 작업 폴더 `orchestration/work/phub-gold-jev/` 가 미추적이라 나는 git 상태 검사뿐이다. 이미 알려진 것이니 나머지 판정만 인용.
- 옛 설계(25타입 247필드 · 옛 gold 노드 체계)를 새 설계의 기준으로 끌어오지 마라.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · 표.칸 · 셈 명령과 결과). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다.
```

- 끝내기 전 `git -C $P status --porcelain` 에서 네가 만든 변경이 리포트 1개뿐인지 확인한다(코디 변경은 무관).
- 리포트에 회사 데이터 본문이 없는지 스스로 훑는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_95e86b96-831a-4d31-aa96-58649a80d244 --from term_a4e2d363-b057-4ec8-bd9f-21592b448287 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
