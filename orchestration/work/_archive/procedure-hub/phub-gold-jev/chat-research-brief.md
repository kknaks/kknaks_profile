# [researcher] 상담 채팅 — 기억 방식 · 상담 프롬프트 · 얼굴 점 · htmx 화면 조사

너는 **procedure-hub `researcher` 워커**다(read-only). 앞 판의 맥락이 없다 — 아래 「읽을 것」만으로 일한다.
먼저 역할 문서를 읽어라: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/researcher/role.md`(+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리(코디 워크트리 · 공유): `P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` — **리포트 파일 1개 외에는 만들거나 고치지 마라.**

경로: `W=$P/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · FastAPI · 시험 화면 18220 은 코디 것) · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만 · **다른 워커가 지금 backend/ 를 고치는 중** — 읽기만 · 지금 상태가 흔들릴 수 있음을 감안) · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`

## 1. 배경 · 정해진 것(다시 논의하지 마라)

연결 시험(v06-37)이 끝났다. 이번 세션 목표 = **상담 채팅** — 채팅 기능 먼저. `$W/_RESUME.md` §2 11-17 행이 정본이다. 요점:

- **화면(사용자 지시)**: 왼쪽 위 = 얼굴 그림 + 부위 점 · 왼쪽 아래 = 시술 리스트 · 오른쪽 = 채팅창.
  ```
  [얼굴 + 점]   | 채팅창
  [시술 리스트] |
  ```
- **흐름**: 「팔자주름이 고민돼요」 → 시술 검색(허브 · B 흐름 = gold + Jev 가 맨 앞에서 판단) → 시술 리스트 만들기 → 얼굴의 팔자 위치에 점.
- **얼굴 그림**: 사용자 PNG `/Users/kknaks/Downloads/미니멀 인체 해부학 삼면도.png`(1448×1086 · 세 패널 중 **왼쪽 얼굴 패널만**)을 벡터화해 부위마다 좌표. 몸통 두 패널은 이번엔 안 씀.
- **렌더링 = 서버사이드 + htmx**(사용자 지시).
- **점 기준 기본값 = 고민 부위**(silver `concern_site`) — 시술을 누르면 그 시술 부위(`offer_site`)도 보일지는 사용자 결정 대기.
- LLM 은 DB 화와 함께 SDK 로 간다(11-16 D8 결정) — 다만 CLI `--resume` 과 SDK 캐싱을 **비교해 보고** 정한다(NEXT-SESSION).
- 상담 원칙(`$W/NEXT-SESSION-chat-prompt.md` 「이번에 할 것」 3): 짧게 → 필요할 때 깊게 · 안전 정보를 처음부터 붙이지 않음 · 묻지 않은 것 안 붙임 · 우열 판정 안 함(차이를 물으면 각각) · 층을 밝힘 · 앱이 답 문장을 짓지 않음 · 지어낸 숫자 0. **테스트(빠짐없이) ≠ 상담.**
- 11-17 사용자 결정: Procedure Hub 데이터(원장 · silver · gold)는 **공개 정보** — 리포트에 이름 · 값을 실어도 된다. 비밀값 · 키 · 내부 URL 은 금지 그대로.
- 허브는 병행으로 로컬 DB 판을 짓는 중(SPEC-003 · WORK-010) — 채팅은 허브 HTTP 계약(SPEC-001 도구 9)만 보면 된다. 허브가 CSV 판이든 DB 판이든 응답은 같다.

## 2. 읽을 것

- `$W/_RESUME.md` §2 · `$W/NEXT-SESSION-chat-prompt.md` · `$W/batch-v06-summary.md`
- 계약: `$W/SPEC-001-hub-gold-mcp.md`(도구 9 · 특히 `concern_candidates` · `facets` · `scope` · resolve) · `$W/SPEC-002-chat-eval.md` §3-2a(LLM 에 싣는 칸) · §3-7(P11 · FT8)
- 앱 코드: `$A/clinic_chat/` 전부(특히 `runner.py` · `walk/` · `columns/` · `clients/` · `llm/{cli,cli_process,auth}.py` · `web/server.py` · `web/static/` · `prompts.py`) · `$A/prompts/{common,col_b,judge}.md` · `$A/README.md` · `$A/pyproject.toml`
- Jev: `$P/para/resources/note/ai/llms.txt`
- silver 부위: `$SM/silver/{site,concern_site,offer_site,anatomy_site,concern}.csv` · `$SM/notes/silver-erd.md` · 허브가 부위를 어떻게 내는지 `$H/backend/app/modules/gold/{concern,service,repository}.py`(`sites_of_concern` 등)
- 그림: 위 PNG(Read 로 열어 봐도 된다)
- Anthropic SDK · 프롬프트 캐싱 · Claude Code CLI `--resume` · `-p` 세션: **claude-api 스킬 · 공식 문서 기준 — 추측 금지**(못 찾으면 「확인 안 됨」).

## 3. 질문 — 답마다 근거(파일:줄 · 문서 절 · 셈 명령과 결과)

**Q1. 대화 기억 — CLI `--resume` vs SDK 프롬프트 캐싱**
- 각각: 기억이 어디에 저장되나 · 이어 붙이는 법 · 첫 답 속도 · 캐시 적중 조건(최소 길이 · TTL · 무엇이 접두가 되나) · 비용(지금 CLI 는 구독 · SDK 는 API 키) · 모델(Sonnet / Haiku) · 추론 끄기 가능 여부 · 스트리밍.
- **재료(gold 묶음)를 대화 사이에 어떻게 들고 가나**: 턴마다 새로 읽은 재료 vs 앞 턴 재료 재사용 · 캐시 접두에 무엇을 두면 적중이 오르나(시스템 프롬프트 · 앞 대화 · 재료 순서).
- 지금 앱 `llm/cli*.py` 가 CLI 를 어떻게 부르나 · SDK 로 바꿀 자리.
- 대화 장부(턴 · 고른 대상 · 읽은 재료 id · 답)를 어디에 둘지 — 앱 메모리 / 파일 / DB.

**Q2. 상담 프롬프트**
- 시험 프롬프트 3(common · col_b · judge)에서 상담에 남길 것 / 버릴 것(「빠짐없이」 등 시험 전용)을 줄 단위로.
- 「짧게 → 필요할 때 깊게」 를 어떻게 나누나: 첫 턴(고민 → 시술 이름 목록 + 층 · 한 줄) / 다음 턴(한 시술 상세 · 차이) — 각 단계에 LLM 에 싣는 칸(§3-2a 기준)과 Jev 판단 지점.
- **시술 리스트 칸과 채팅 답을 어떻게 가르나**: 리스트는 앱이 허브 행으로 결정론적으로 짓고(답 문장 아님) · 채팅은 LLM 이 짧게 — 그때 LLM 이 리스트를 다시 읊지 않게.
- 초안 꼴만(문구 확정은 사용자) · 시험 v06-37 의 B 실패 꼴(Q01 · Q03 목록 줄임 · Q09 · Q13)이 상담에서 문제인지.

**Q3. 얼굴 벡터화 · 부위 좌표**
- PNG 왼쪽 패널 자르기 · 벡터화 길(예: potrace · 손 SVG · 원본 PNG 를 SVG `<image>` 로 깔고 점만 SVG) — 각각 품질 · 의존 · 공개 레포에 둘 수 있는지(그림 출처는 사용자 파일). 이 기계에 무엇이 깔려 있나(`which potrace` 등 — 설치하지 마라).
- silver `site` 89 중 **얼굴 · 머리 · 목 쪽 부위** 전수(코드 · 이름 · parent) · 좌우 짝(팔자 · 광대 등 두 점) · 정면 그림에 안 보이는 부위(두피 · 정수리 · 구강 · 잇몸 · 귀 뒤 등) 처리.
- 좌표 표 꼴 제안(`site_code → [(x,y)…]` 0~1 비율 · 점 / 영역) · 누가 어떻게 찍나(초안 = 워커 · 확인 = 사용자 눈) · 부모 부위만 나올 때(예: 「얼굴」) 처리.
- 고민 → 부위: `concern_site`(95) 로 고민마다 부위가 몇 개 · 부위 없는 고민 수 · 하위 고민 펼침 때 부위. 시술 → 부위: `offer_site` 수. 허브가 이걸 응답으로 내나(지금 `sites_of_concern` 앱 호출 0 — 조사 research-db §0-1) · 안 내면 허브에 무엇이 필요한가.

**Q4. htmx 화면 구조**
- 지금 앱 `web/server.py` · `static/` 구조(SSE · 열 동시 실행) — 이어 쓸 것 / 새로 지을 것. 18220 시험 화면은 그대로 두고 새 화면을 어디에(라우트 · 포트 후보 — 18210 · 18005 금지 · 18105 · 18106 · 18107 · 18220 · 18221 · 18432 사용 중).
- 서버사이드 템플릿(Jinja2 등 — 의존 추가 필요 여부) · htmx 조각 갈아 끼우기(채팅 말풍선 · 시술 리스트 · 얼굴 점 세 칸을 한 응답에서 `hx-swap-oob` 로?) · 스트리밍(htmx SSE 확장 · 첫 글자 속도) · htmx 를 어디서 싣나(CDN 고정 판 / 로컬 파일).
- 화면 문구는 짓지 않는다(사용자 · 시안 몫) — 빈 칸 · 자리 표시만.

**Q5. 끝에서 끝 흐름 초안**
- 「팔자주름이 고민돼요」 한 턴: 앱 → Jev → 허브 호출(도구 · 요청 꼴) → 리스트 행 · 부위 코드 · LLM 입력 · 답 — 단계별 시간 예상(v06-37 B 첫 답 중앙 2.3s 기준).
- 다음 턴 예(「그중 필러는 얼마나 가요?」 · 「보톡스랑 뭐가 달라요?」)에서 기억이 무엇을 들고 와야 하나.

**Q6. 정할 것** — 리포트 머리에 요약(질문당 2~3줄) + 「정할 것」 표(사용자가 고를 것만 · 각각 추천 · 근거 · 위험). 결정하지 마라.

## 4. allowed_paths

- **쓰기: `$W/research-chat.md` 1개만.** 임시 파일 · 그림 실험은 네 세션 scratchpad 에만.

## 5. 하지 말 것

- 결정하지 마라. **외부 API(Claude · Jev) 호출 금지** · `.env` 열지 마라 · 키 출력 금지. 공식 문서 읽기(웹)는 된다.
- 서버 · docker 를 띄우거나 내리지 마라. 사용자 포트 금지. 앱 · 허브 작업 트리를 바꾸지 마라(stash · checkout · reset · fetch · 파일 수정 금지). 패키지 설치 금지.
- 디스크 여유가 적다 — 큰 파일 만들지 마라.

## 6. 검증

질문마다 답 + 근거. 확인 못 한 것은 「확인 안 됨」. 끝내기 전 `git -C $P status --porcelain` 에서 네 변경이 리포트 1개뿐인지 확인.

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. 다르면 preamble 쪽으로만.

- **커밋·push·PR 하지 마라.** 끝나면 아래 두 명령을 모두 실행한다.

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher(채팅) 완료: <한 줄>" \
  --body "변경 파일 / 요약 / 정할 것 개수 / 미결·주의점"

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] researcher(채팅) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 --text "[질문] researcher(채팅): <질문>" --enter`
