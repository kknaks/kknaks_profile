# [researcher] 상담 입력 전수 표 + 실패 층 + 소넷 후보 뽑기 시안 측정

너는 **procedure-hub `researcher` 워커**다. 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/researcher/role.md`(+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`). Procedure Hub 데이터는 공개 정보다. 키 · 비밀값 · 접속 문자열은 찍지 마라.

경로:
- `P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev`
- gold(읽기만): `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/gold/` · silver 같은 폴더 위
- 앱(읽기만 · 코드 고치지 마라): `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev` — 상담 흐름 `clinic_chat/consult/turn.py` · 걷기 `clinic_chat/walk/front.py` · `entry.py` · 객체 `consult/state.py` · 조회 `consult/plan.py` · 장부 `runs/consult/turns.jsonl` · CLI 인자 `clinic_chat/llm/chat_cli.py` `chat_args`
- 허브(읽기만): `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev` · 떠 있는 허브 **18105 는 GET/조회만**

먼저 읽어라: `$W/_RESUME.md` 맨 위 「다음」 · §2 맨 위 행(11-18 결정) · `$W/SPEC-006-consult-v03.md` 개요 · `$W/SPEC-001-hub-gold-mcp.md` §concern_candidates.

## 배경 — 정해진 것(다시 논의하지 마라)

- 상담 채팅이 고칠 때마다 구멍이 났다. 사용자 결정(11-18): **증상 패치를 멈추고, 입력 전수 표 → 실패 표 → 설계 한 번.** 완료 기준 = 표 통과율.
- 장부로 확인한 실패 층(conv 44b267e97f6d4df4 · 2d16997adb7847b0):
  - 턱에 살이 너무 많아보여 → resolve 가 부위 「턱」만 냄 → 후보가 0 이 아니라 입구 고르기가 안 돎 → 턱살 CON-168 이 Jev 에 안 감(**후보 층**)
  - 사각턱인데 ? → Jev 고민 CON-161 0.91 > 부위 SITE-076 0.89 인데 겹침 규칙이 부위를 고름(**앱 규칙 층**)
  - 눈에 주름도 → Jev 판단 맞음 · 객체 조회 QY5 에 부위 턱 · 사각턱 · 눈 셋 다 실림(**앱 규칙 층** — 쌓인 부위) + 눈 SITE-018 ≠ 눈 주변 SITE-019(**데이터 층**)
  - 지방이 두꺼운 느낌이야 → resolve 0 → 입구 고르기 Jev 38 요청 · 10.1초로 얼굴 지방 CON-169 맞힘(**맞지만 느림**)
- **결정: resolve(글자 맞춤)를 후보 관문에서 뺀다. 소넷이 대화 맥락을 읽고 gold 목록 안에서 후보를 뽑는다.** 모델은 설정값(지금 소넷 · 느리면 하이쿠). gold 에 없는 코드는 앱이 버린다. MCP 도구 루프 · 임베딩은 안 쓴다. Jev 는 점수 · 턴 종류 판정으로 남기되 이번 측정에서 Jev 있음/없음을 비교한다.

## 할 것

### 1. 입력 전수 표(여러 턴 대화)
- **대화 단위**로 짓는다(한 줄 문장 표가 아니다). 대화 40~80 개 · 턴 합 200~400.
- 축:
  - 의도 꼴: 고민만 · 부위만 · 고민+부위 · 넓은 고민+부위(주름+눈) · 시술 · 계열 · 제품/브랜드 · 앞 되물음에 대한 답(「네」「두 번째요」) · 앞 대화 참조(「그거 아파요?」「아까 거랑 같이」) · 화제 전환(다른 고민) · 섞인 말(고민 둘) · 거둠(「그건 말고」) · 잡담/불만(「왜 못 채워」)
  - 말 꼴: 이름 그대로 · 조사 끼임(턱에 살) · 어순 바뀜 · 줄임(지방 주사) · 자기 말로 바꿔 말하기(얼굴 아래가 두꺼워) · 오타/띄어쓰기
  - 데이터 조합: **gold 에서 실제로 뽑는다**(고민 · 부위 · concern_site · 시술 · 계열 · 제품 · 별칭 `g_entry`). 고민마다 부위 있음/없음 · 하위 고민 있음/없음 · 시술로 닿음/안 닿음이 고르게 섞이게.
- 턴마다 **정답 키**: 기대 대상 코드(표, 코드) · 기대 턴 종류(new/follow/talk) · 기대 부위 거르개(이번 턴 부위) · 기대 점 부위. 정답을 gold 에서 어떻게 정했는지 근거 칸. **애매한 턴은 「애매」 표지로 따로**(정답을 지어내지 마라).
- 표는 기계가 읽는 파일로: `$W/research-input-space/conversations.jsonl`(대화 · 턴 · 꼴 태그 · 정답 키 · 근거).

### 2. 지금 시스템 실행 → 실패 표(층별)
- 앱 코드를 **가져다 부르기만** 하는 스크립트(네 scratchpad)로 각 대화를 턴 순서대로 돈다: 상담 켠 상태(CHAT_STATE=on)의 걷기 · Jev · 객체 갱신 · 객체 기준 조회 · 리스트 · 점까지. **답 LLM(소넷 답)은 부르지 않는다.** 허브는 18105 · Jev 는 앱 `.env` 의 키(찍지 마라).
- 턴마다 기록: resolve 후보 · Jev 점수 · 확정 대상 · 객체 diff · 조회 요청(부위 거르개) · 리스트 시술 코드 · 점 부위.
- 정답과 견줘 실패를 **층으로 가른다**: 후보(정답이 후보에 없음) · Jev(후보에 있는데 점수로 떨어짐/잘못 고름) · 앱 규칙(Jev 는 맞는데 겹침 · 부위 쌓임 · 객체 미반영 등) · 데이터(gold 에 길이 없음 — 부위 계층 · concern_site 등). 꼴별 × 층별 실패 수 표 + 층마다 대표 턴 3개(장부 근거).
- 데이터 층 실패는 **무엇을 보강하면 되는지** 목록(코드 · 근거). 지어내지 말고 gold/silver 로 확인된 것만.

### 3. 소넷 후보 뽑기 시안 측정
- 시안 프롬프트(네 scratchpad): 대화 지금까지 · 지금 객체 요약 · **gold 목록**(고민 · 부위 · 시술 · 계열 · 제품 코드+이름 · 별칭은 넣는 판/안 넣는 판 둘 다 재 봄) → 출력 JSON: 이번 턴 후보 `[{table, code}]` · 턴 종류 · 이번 턴 부위. 앱이 gold 에 없는 코드는 버린다(버린 수도 센다).
- 호출은 **앱과 같은 격리 인자**로 `claude -p`(`chat_cli.chat_args` 꼴 참고 · `--setting-sources ""` · `--strict-mcp-config` · tools 없음). 모델 `sonnet` 기본 · 같은 표를 `haiku` 로 한 번 더(비교값).
- 잴 것(꼴별): 정답 대상 포함률(recall) · 군더더기(precision) · 지어낸 코드 비율 · 턴 종류 정답률 · 이번 턴 부위 정답률 · **지연**(턴당 ms 중앙값 · p90 — CLI 시작 포함) · 목록 토큰 수 · 캐시 효과(같은 대화 둘째 턴부터).
- Jev 비교: 소넷 후보 → Jev 점수로 확정한 판 vs 소넷 후보 그대로 확정한 판의 정답률 · 지연.
- 비용 줄이기: 전수 표 전부를 소넷 · 하이쿠로 다 돌리기 어렵다면 꼴마다 고르게 뽑은 표본(턴 120 이상)으로 하고 뽑은 방식을 적어라.

### 4. 리포트
`$W/research-input-space.md`: 머리 요약(수 위주) → 표 1(꼴 × 층 실패 수 — 지금 시스템) → 표 2(지금 vs 소넷 vs 하이쿠 vs 소넷+Jev: 포함률 · 정답률 · 지연) → 데이터 보강 목록 → 앱 규칙 고칠 곳 목록(겹침 · 부위 거르개 · 점 · 객체 반영 등 — 코드 자리 `file:line`) → 「정할 것」(추천 붙임 · 사용자 몫만).

## allowed_paths

- **쓰기: `$W/research-input-space.md` 1개 + `$W/research-input-space/` 폴더**(jsonl · csv · 실행 결과 요약). 스크립트 · 임시 파일은 네 scratchpad.
- 같은 `$W` 폴더에 다른 파일이 많다 — 다른 파일은 만들거나 고치지 마라.

## 하지 마라

- 앱 · 허브 · silver/gold 코드 · 데이터 수정 · 커밋 금지. DB 쓰기 금지.
- 18105 재시작 · 18222 · 18432 건드리지 마라(18105 는 조회만). 서버를 새로 띄워야 하면 18224 만(끝나면 내림 · `lsof` 0).
- 결정하지 마라 — 「정할 것」 으로 올려라. 전체 pytest 돌리지 마라(이번 일에 시험 없음).
- 소넷 · 하이쿠 호출은 측정에 필요한 만큼만. 진행 중 `[진행] researcher: <단계> …` 한 줄을 코디 터미널로(1 · 2 · 3 끝날 때).

## 완료 보고 — 문구 변경 금지

> 핸들 · taskId · dispatchId 는 dispatch preamble 값을 믿어라.

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher(input-space) 완료: <한 줄>" \
  --body "변경 파일 / 대화 · 턴 수 / 층별 실패 수 / 소넷 · 하이쿠 포함률 · 지연 / 정할 것" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] researcher(input-space) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
