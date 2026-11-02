# [architect] 회의록 계약 정정 3차 — payload 드로어를 회의록 것으로 · MCP 배치 · 토큰 · 웜스타트 닫기 · 보고

발주: `docs-v1-meeting-reflow3-brief.md` · 정본: `reference/2026-09-06-task-management-app/Meeting flow.md` **§0 MF-64(정정) · 66 · 67 · 68 · 69 · 70 과 각 본문**(§1-5 · §3-4 · §3-5) · 2026-09-07

## 0. 한 줄

**다섯만 옮겼다.** MF-67(payload 드로어는 회의록 것 — 업무 탭 드로어 재사용 폐기) · MF-64 정정(칩은 둘로 갈린다 · `POST …/lines` 가 액션·업무 줄에 한해 `payload` 복원) · MF-66 전파(DEC-003 §5 · ERD M-14 · M-14-a) · MF-68 · 69(MCP 별도 컨테이너 · 단명 토큰 = `auth_session(kind='meeting')` 행 → OQ-9 · SYS-OQ-4 닫힘) · MF-70(웜스타트 실패 처리 없음 → OQ-8 닫힘). **2차에서 내가 쓴 「업무 탭 드로어에 슬롯을 얹어 재사용」 문장은 내가 지웠다** — SPEC-008 U-9 · U-10 재작성, SPEC-003 U-1 · U-3 문단 삭제, frontend 규칙 8 재작성, SPEC-008 정합 #1 삭제. 고친 파일 **9개**. grep 셋 통과.

## 1. 다섯 — 어느 문서 어느 절을 어떻게

### ① MF-67 — payload 드로어는 회의록 것이다 (MF-13 · 14 정정)

| 문서 · 절 | 어떻게 |
|---|---|
| **SPEC-008 U-9**(재작성 · 제목 「업무 payload 드로어 — 업무 줄이 여는 회의록 드로어」) | 「업무 상세 드로어 + 헤더 슬롯」 계약을 **폐기**하고 **회의록 드로어**로 다시 씀. 성격 대비(업무 드로어 = 업무를 고치는 자리 / payload 드로어 = 줄에 붙일 값을 적는 자리)를 본문에 박음. **필드 = 변경분 일곱 + 헤더 업무 셀렉터**로 좁힘 — 제목·유형·설명·시작일 **없음**, 참고자료·결과자료·로그·첨부 블록 **안 그림**(전 판은 SPEC-003 U-3 블록 전부를 그렸다). 필드 표 신설(출발값 = 고른 업무의 현재 값, `payload` 가 있으면 그 값이 이김 · 메모·할일·연관은 **추가분**). **시각 참조는 SPEC-003 U-3(`TaskDetailDrawer`)의 부품 규격**임을 명시, 새 시안 없음. **`RelationPopover` 는 그대로 재사용**(업무 화면 부품 · 드로어 아님 · 단일 선택 prop 하나) |
| **SPEC-008 U-10**(재작성 · 제목 「액션 payload 드로어 — 액션 줄이 여는 회의록 드로어」) | 같은 방식. **필드 = `payload` 키 일곱 + 안건(고정)**. 상태 필드 없음 · 참고자료·연관·결과자료·첨부·로그 **안 그림**. 프리필 표를 `payload` 키 기준으로 다시 씀. **시각 참조는 SPEC-003 U-1(`TaskCreateDrawer`)** |
| SPEC-008 U-6 · U-11 · S-6 · S-8 · S-9 · AC · §1 Context(In · Scope) · 머리말 · §7 제외 표(L2306~2599 · L2600~2882 행) · §8 근거 표(U-6 · U-9 · U-10 행) | 드로어 이름을 「업무 탭의 새 업무 드로어 / 업무 상세 드로어」 → **「액션 payload 드로어 / 업무 payload 드로어」**로 전면 교체. 옛 시안(L2306~2882) 제외 사유를 **「`payload` 가 없던 시안이라 참고하지 않는다」**로 고침 |
| SPEC-008 AC | **신규 1건** — 「업무 탭 드로어는 회의록 때문에 달라진 것이 없다」(업무 탭에서 열면 안건 칸도 「저장/넣기」 푸터도 없다). 기존 AC 3건에 「필드는 이 일곱뿐 / 변경분 일곱뿐」 조건 추가 |
| SPEC-008 §7 닫은 것 | **MF-67 행 신설** · MF-13 · 14 행 재작성 · **정합 #1 을 「삭제」로 전환**(SPEC-003 에 슬롯을 더하지 않는다. 남는 것은 U-8 `RelationPopover` 0건 폴백 · 단일 선택 하나) |
| **SPEC-003 U-1 · U-3** | **「회의록에서 열 때」 문단 2건 삭제.** 자리에 **「회의록은 이 드로어를 열지 않는다」** 한 줄씩 — 「이 드로어는 회의록 때문에 달라지는 것이 없다」 · 「SPEC-008 U-9/U-10 이 부품 규격만 시각 참조로 가리킨다」. **U-8 의 「회의록도 이 팝오버를 그대로 쓴다(단일 선택)」는 그대로 유지** |
| DEC-003 §5 업무 연동 | 「드로어는 업무 탭의 것」 → **「드로어는 회의록 것이고 액션·업무 각각 하나」**. 성격 대비 · 필드 = `payload` 키 · 시각 규격만 가리킨다 · 업무 셀렉터(`RelationPopover` · 0건이면 「전체」)를 한 셀에 |
| DEC-003 §8 Out(내 업무) · 머리말 ⑤ · Resulting Spec(SPEC-003 행 신설) | 「드로어는 업무 탭 것을 재사용」 → 「드로어는 회의록 것이다」 |
| ERD `meeting.md` M-14 · M-14-a · 머리말 | 「업무 줄 드로어의 헤더 셀렉터」 → 「**업무 payload 드로어**의 헤더 셀렉터 · 그 드로어는 회의록 것」. M-14-a 에 「드로어의 필드는 `payload` 키 그대로」 한 항목 추가 |
| **frontend README §2 규칙 8**(재작성) · FE-18 · 머리말 | 규칙 8 을 **「회의록의 payload 드로어는 회의록 것이고, 업무 탭 드로어는 손대지 않는다」**로 다시 씀 — 7개 하위 항목(둘을 `features/meetings/components/` 에 · `features/tasks` 수정 금지(반려) · 시각 규격만 가리켜 조립 · `RelationPopover` 재사용 · `prefill`·`submitMode` · 액션·업무 각각 하나 · 필드는 `payload` 키만 · 칩 둘 갈래). **규칙 4 의 드로어 재사용 예외는 캘린더 ↔ 업무·회의 드로어에만 남는다**고 못박음 |

### ② MF-64 정정 — 칩은 둘로 갈린다 (「칩 넷이 같다」 폐기)

| 문서 · 절 | 어떻게 |
|---|---|
| **SPEC-008 U-7 안건별 추가 행**(재작성) | 「넷 다 같은 방식 — 줄 먼저」 → **「+ 논의 · + 결정 → U-8, 「추가」에 줄」 / 「+ 연관 업무 · + 액션 아이템 → payload 드로어가 바로, 「저장」에 줄 + `payload` 한 요청」**. 어느 쪽이든 닫으면 줄이 없다. 「왜 줄 먼저를 접었나」(드로어 둘 연달아) 근거 포함 |
| **SPEC-008 U-8**(재작성) | 제목을 **「논의 · 결정 전용」**으로. 종류 세그먼트에서 **「업무」·「액션」 고정 갈래 삭제** — 「논의 ↔ 결정」만. 기대 결과에 「논의·결정 줄에 `payload` 를 실으면 422」 |
| SPEC-008 U-9 · U-10 | **진입점 둘**(줄 버튼 · 칩)을 명시. 「저장」이 **줄에서 열었으면 `PATCH …/lines`, 칩으로 열었으면 `POST …/lines`** 임을 푸터 절에. 「취소」의 결과도 갈래별로(줄 그대로 / 줄이 안 생김) |
| **SPEC-008 §4 API 표 · `POST …/lines` 본문 · Validation · Case Matrix** | 2차에서 뺀 `payload` 를 **복원** — 액션·업무 줄에 한해 `payload`(업무 줄은 `taskId` 도). 요청 예시 3개(논의 / 액션 / 업무). **`newTask` 는 여전히 없음**, 논의·결정에 오면 422. **업무는 안 생긴다 — `task_service` 미호출**을 표·불릿·구현 규칙 세 곳에 |
| SPEC-008 §5 Flow · 구현 규칙 · 낙관적 갱신 | 시퀀스를 「+ 결정 → U-8」 / 「+ 액션 → payload 드로어 → `POST lines {…, payload}`」 둘로 분리. 구현 규칙 「`POST lines` 는 줄만 만든다」 → 「줄과 `payload` 를 함께 만든다(액션·업무에 한해)」. **「드로어를 연달아 둘 띄우지 않는다」** 반려 조건 추가 |
| SPEC-008 S-6-a(신규 시나리오) · AC 2건 재작성 + 1건 신설 · §7 닫은 것(MF-64 정정 행 신설) · U-8 행 재작성 | 사용자가 화면에서 확인할 문장으로 |
| DEC-003 §5 | 「칩 넷은 전부 줄이 먼저」 → 「칩은 둘로 갈린다」 + 왜(본문 필수 · 드로어 둘) |
| ERD `meeting.md` M-14 · M-14-a | 「`POST …/lines` 는 `task_id` 를 받지 않는다」 → **「`kind='task'` 줄에 한해 함께 받는다 · 그래도 업무는 안 생긴다」**. `payload` 를 쓰는 표면이 **둘**(`POST` · `PATCH`)임을 명시 |
| backend README §10 회의록 행 | `POST …/lines` 의 `payload` 복원을 API 표면 형태 규약에 |
| frontend README 규칙 8 | 칩 둘 갈래 · 「드로어 연달아 둘 = 반려」 |

### ③ MF-66 전파 — 푸터 모드별

| 문서 · 절 | 어떻게 |
|---|---|
| **DEC-003 §5 업무 연동** | **「푸터는 모드별이다(MF-66) — 편집 「취소 · 저장」(payload 만 · 업무 없음) / 보기 「취소 · 넣기」(업무 생성·갱신). ⛔ 한 푸터에 셋을 두지 않는다」** 한 절 추가(전에는 「둘 다 「넣기」」로 읽히는 문장이었다) |
| **ERD `meeting.md` M-14** | 하위 불릿 신설 — 모드별 푸터 · **「「둘 다 「넣기」」로 읽지 않는다」** |
| **ERD `meeting.md` M-14-a** | 「사람이 드로어에서 「저장」」 → 「**회의록 payload 드로어**에서 「저장」」 + 「푸터가 모드별이라 `payload` 를 붙이는 것과 업무를 바꾸는 것이 화면에서도 갈린다」 |
| SPEC-008 · frontend README | 이미 있었음(2차) — `submitMode` 위치만 정리(아래 §3) |

### ④ MF-68 · MF-69 — MCP 별도 컨테이너 · 단명 토큰 = `auth_session` 행 (OQ-9 · SYS-OQ-4 닫힘)

| 문서 · 절 | 어떻게 |
|---|---|
| **backend README §4 디렉토리** | `app/mcp/` 블록 신설(도구 7개 · back REST 래퍼). `ai_schemas/` 각주를 「MCP 배치 위치는 OQ-9」 → **「MCP 서버는 여기 없다 — `app/mcp/` 별도 서비스」**. 아래에 한 문단 — **FastAPI 안에 두지 않는다 · compose 에 back · worker · mcp 셋 · `worker→mcp→back` 한 방향 · back 은 mcp 를 import 하지 않고 mcp 는 DB 를 모른다** |
| **backend README §5-2** | **토큰 발급 자리 = `meeting_service` 의 `/start`**(전이와 같은 트랜잭션에서 `auth_session(kind='meeting')` INSERT · 해시만 저장) · **폐기 자리 = `meeting_finalize_service`**(② 종결 시 행 DELETE · best-effort · `revoked_at` 안 찍음). 무상태 JWT 를 안 쓰는 이유 명시 |
| backend README §8-3 · §10 MCP 행 · §10 회의록 행 · §11 env · 머리말 | `MCP_BASE_URL` · `MCP_SERVER_URL` · `MEETING_TOKEN_TTL_MIN` 3행 추가. MCP 도구 행에 「별도 컨테이너 · `auth_session(kind='meeting')` 인증」 |
| **system README Components · 런타임 배치 · §codex 설정 · External Integrations · 흐름 ③ · 불변식 · 결정 요약 · SYS-OQ-4 · 머리말** | Components 「MCP 도구 7개」 → **「MCP 서버(`app/mcp/` 별도 컨테이너)」**(하지 않는 것: DB 접근 · FastAPI 안에 들어가지 않음). §codex 끝에 토큰 문단 신설(발급·검증·폐기=행 삭제 · 무상태 JWT 안 씀). 흐름 ③ mermaid — `/start` 에 `auth_session INSERT`, 폐기를 `auth_session 행 DELETE` 로, participant 이름을 「MCP 서버(별도 컨테이너)」로. **불변식 13 · 14 · 15 신설**(열둘 → 열다섯) · **SYS-15 · SYS-16 신설** · **SYS-OQ-4 닫힘** |
| **ERD `account.md`** | Entities 표 `auth_session` 에 `kind ∈ {refresh, meeting}`. **A-13 신설**(발급 · 검증 · 폐기=행 삭제 · 왜 무상태 JWT 가 아닌가 네 항목). **A-7 에 「이 규칙은 `kind='refresh'` 행에만」 한 구절** |
| **ERD `database/README.md`** | §1 ERD `auth_session` 에 `kind` · `meeting_id` · 주석 3줄 · 관계선 `meeting ||--o| auth_session` 추가. §2 표 · §4 인덱스 표(`(meeting_id) WHERE kind='meeting'`) |
| DEC-003 §2 · §8 「AI 도구 연결」 · OQ-9 · 머리말 ⑦ · Resulting Spec | §8 에 **「배치」 행 신설**(별도 컨테이너) · 「토큰」 행 재작성(발급·검증·폐기 · 무상태 JWT 안 씀). **OQ-9 를 `~~OQ-9~~` 해소로 전환.** Resulting Spec 에 **MCP work(new)** 행 |
| SPEC-008 §5 Flow · OQ 처리 표 · §7 닫은 것 | Flow 의 「단명 토큰 best-effort 폐기」 → 「`auth_session` 행 DELETE」. OQ-9 행을 닫힘으로. §7 에 「MF-68 · 69 MCP · 토큰」 행 — **이 spec 이 닿는 것은 ② 종결 시 행 삭제 하나** |

### ⑤ MF-70 — 웜스타트 실패 처리 없음 (OQ-8 닫힘)

| 문서 · 절 | 어떻게 |
|---|---|
| **DEC-003 §7 웜스타트 행** | 「실패의 기록·재시도 경로는 OQ-8」 → **「실패 처리를 따로 만들지 않는다 — 별도 기록 테이블 · 재시도 경로 · 재웜스타트 갈래가 없고 남기는 것은 예외 전파 로그뿐」** + 두 경로(회의 중 배치 미제출 / 종료 후 ② `final_failed`) + BASE-003 L43 인용 |
| DEC-003 §4 `/start` 행 · 머리말 ⑦ · **OQ-8 닫기** | `~~OQ-8~~` 해소로 전환(근거: 실패한 적이 없고 워커가 내려간 경우뿐) |
| **backend README §5-2 · §8-3 두 행** | 「실패 기록·재시도는 OQ-8」 → **「처리를 만들지 않는다 · 코드에 없어야 한다(검수 항목)」**. ② 행에 「세션이 없는 회의(웜스타트 실패)도 이 경로 — 새 세션으로 웜스타트부터 다시 하는 갈래를 만들지 않는다」 |
| system README 흐름 ③ · 불변식 15 · SYS-14 | mermaid 에 Note 한 줄 · 불변식 15 신설 |
| **SPEC-008 §4 `/end` 불릿 · OQ 처리 표 · §7 닫은 것** | 「② 를 어떻게 여나는 OQ-8」 → **「그 회의는 ② 에서 세션이 없어 `final_failed` 로 간다 — 별도 기록·재웜스타트 갈래를 만들지 않는다(MF-70)」** |

## 2. 고친 파일 아홉

```
20-spec/spec-008-meeting-close.md              U-6 · U-7 · U-8 · U-9 · U-10 · U-11 · S-6 · S-6-a(신규) · S-7 · S-8 · S-9 ·
                                               §1 Context · §4 API 표 · POST lines · Validation 3행 · Case Matrix ·
                                               §5 Flow · 구현 규칙 5항 · AC(30→32) · §7 닫은 것 4행 · 제외 2행 ·
                                               OQ 처리 표 · 정합 #1 삭제 · §8 근거 표 3행 · 머리말
20-spec/spec-003-tasks-crud.md                 U-1 · U-3 「회의록에서 열 때」 문단 삭제 → 「열지 않는다」 한 줄씩. U-8 유지
10-decision/decision-003-meeting-notes.md      머리말(31→34 · MF-1~MF-70 · ⑤⑥⑦) · §2 · §4 · §5 · §7 · §8(배치·토큰 행) ·
                                               OQ-8 · OQ-9 닫기 · Resulting Spec 2행 추가
40-architecture/database/domains/meeting.md    머리말 · M-14 · M-14-a
40-architecture/database/domains/account.md    Entities `auth_session` · A-7 · **A-13 신설**
40-architecture/database/README.md             §1 ERD(`kind`·`meeting_id`·관계선) · §2 표 · §4 인덱스
40-architecture/backend/README.md              머리말 · §4(app/mcp) · §5-2 · §8-3 2행 · §10 2행 · §11 env 3행
40-architecture/system/README.md               머리말 · Overview 4 · 런타임 배치 · Components · §codex · Integrations ·
                                               흐름 ③ mermaid · 불변식 13·14·15 · SYS-15·16 · SYS-OQ-4 닫기
40-architecture/frontend/README.md             머리말 · §2 규칙 8 재작성 · FE-18
```

## 3. grep 셋

| # | 검사 | 결과 |
|---|---|---|
| 1 | `grep -rn "agendaSlot\|taskSelectorSlot"` | **0건** — 폐기 기록에서도 프롭 이름을 지우고 「안건 슬롯 · 업무 셀렉터 슬롯 · 프리필 · 푸터 모드 prop」으로 풀어 썼다 |
| 2 | `grep -rn "submitMode"` | **3건 — SPEC-008 U-9(L299) · U-10(L327) · frontend README §2 규칙 8(L178)뿐.** 구현 규칙 · §7 · SPEC-003 에서 제거 |
| 3 | `grep -rn "31건"` | **0건** — DEC-003 · backend · system · frontend README 머리말을 「34건 · MF-1 ~ MF-70」으로 |
| + | `grep -rn "업무 탭 드로어\|슬롯만 더한다"` | 남은 히트는 **전부 「재사용하지 않는다 · 손대지 않는다 · 폐기」 문장**이다(회의록 드로어 설명에 「업무 탭 드로어를 쓴다」는 0건) |
| + | `grep -rn "칩 넷이 같다\|넷 다 같은 방식"` | 폐기 기록 외 0건. `content` 필수 규칙의 「칩 넷 어느 쪽이든」은 지금도 참이라 유지 |

## 4. 읽기 하나 — 사용자가 다르게 보면 여기만 (새 결정이 아니라 본문을 이은 것)

| # | 읽기 | 근거 | 다르게 보면 |
|---|---|---|---|
| ① | **`auth_session` 에 `meeting_id` 컬럼을 하나 둔다** — `kind='meeting'` 행에만 값 | MF-69 「검증 — MCP 가 부르는 REST 가 **그 행으로 계정 · 회의 범위를 본다**」. 「회의 범위」를 행이 알려면 회의를 가리키는 컬럼이 있어야 한다. 부분 인덱스 `(meeting_id) WHERE kind='meeting'` 도 같은 이유(폐기 = 그 회의 행 DELETE) | 회의 id 를 토큰 payload 에만 담고 컬럼을 안 두는 안도 있다. 그러면 「폐기 = 행 삭제」에서 지울 행을 회의로 찾을 수 없어 계정 전체를 훑어야 한다 — 그래서 컬럼을 뒀다. **컬럼을 안 두기로 하면** `database/README.md` §1 · §4 · `account.md` A-13 · `meeting.md` 머리말 네 곳만 고치면 된다 |
| ② | **업무 payload 드로어의 필드 출발값은 「고른 업무의 현재 값」이고 `payload` 가 있으면 그 값이 이긴다** — 진행 메모 · 할일 · 연관은 **추가분만** 적는다 | MF-14 「업무를 안 골랐으면 본문 비활성」(현재 값에 기대는 문장) · MF-65 그림의 「일정 2026-09-07 ─ 2026-09-14 / 상태 진행중」 · M-14-a 「메모에 **새 항목 추가** · 할일 **추가** · 연관 **추가**」 | 「현재 값을 안 보여 주고 변경분 칸만 빈 채로 연다」로 읽으면 무엇을 바꾸는지 확인할 근거가 화면에 없다. SPEC-008 U-9 필드 표에 이 읽기를 명시해 뒀다 |

## 5. 코디가 볼 것 — 이 발주 밖이라 손대지 않은 것

- **SPEC-007 에 OQ-8 · OQ-9 참조 4곳이 남아 있다**(L411 「기록·재시도는 DEC-003 OQ-8」 · L425 「배치 위치·토큰 인프라는 DEC-003 OQ-9」 · L500 · L711~712). **둘 다 닫혔으므로 이제 사실이 아니다.** 브리프 산출물 목록에 SPEC-007 이 없어 건드리지 않았다 — **다음 발주에서 「MF-70 로 처리 없음 / MF-68·69 로 별도 컨테이너·`auth_session` 행」으로 바꿔야 한다.**
- **WORK-008** — `newTask` 갈래 · 「업무 연결」 · 「업무 탭 드로어 재사용」 · 후보 고르기 앞 단계가 옛 설계 그대로다. 재발주 전 갱신 필요.
- **`app/mcp/` · compose 3서비스 · `auth_session.kind` 마이그레이션**은 **MCP work** 로 나가야 한다(DEC-003 Resulting Spec 에 행을 하나 새로 넣어 뒀다).
- `frontend/README.md` §2 의 제목이 「규칙 여섯」인데 항목이 여덟이다(내 발주 전부터 그랬다). 이번에 고치지 않았다.
- 2차 보고서(`docs-v1-meeting-reflow2-report.md`) §1 표의 「SPEC-003 U-1 · U-3 에 슬롯을 더했다」와 §2 체크 두 줄은 **이 발주로 폐기**됐다.
