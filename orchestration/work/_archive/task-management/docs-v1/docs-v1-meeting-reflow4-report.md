# 회의록 계약 정정 4차 — MF-71 전파 + WORK-015 (architect)

- 일자: 2026-09-08
- 브리프: `orchestration/work/docs-v1/docs-v1-meeting-reflow4-brief.md`
- 정본: `reference/2026-09-06-task-management-app/Meeting flow.md` §0 **MF-71** · §2-3 본문(MF-50 · 51 괄호 정정 포함)
- 산출: 문서 4건 정정 + `ai-prompt-draft.md` 정정 블록 1 + **WORK-015 신규** + `30-work/README.md`
- **코드 워크트리·`orchestration/` 미변경. 커밋·push 없음.**

---

## 0. 옮긴 결정 한 줄

```
전   중간 배치가 list_agendas · get_agenda 로 사람 안건·줄을 읽고 미러 안건(source_agenda_id)을 만든다
후   중간 배치는 발화만 보고 AI 혼자 안건·줄을 만든다 — 도구 셋(list_tasks · get_task · list_work_types)만 열리고,
     humanAgendaId 는 항상 null(서버가 무시) · 미러 없음 · AI 안건 전부 신설(source_agenda_id NULL)
불변 스키마 한 벌(MF-52) · 전량 교체(MF-53) · 검증 순서 0~5 · 최종(MF-56) · 프론트
```

---

## 1. `10-decision/decision-003-meeting-notes.md`

| 절 | 전 | 후 |
|---|---|---|
| frontmatter | `updated_at: 2026-09-07` | `2026-09-08` |
| 서두 근거 표기 | 「결정 34건 — `MF-1 ~ MF-70`」 | 「결정 35건 — `MF-1 ~ MF-71`」 |
| 서두 개정 노트 | ⑦(MF-68·69·70)까지 | **⑧ 신설** — 「중간 배치는 AI 혼자 쓴다」 · 도구를 안 준다 · 미러 없음 · 근거(회의 9 톤 전이) |
| **§2 AI 의 데이터 접근** | 「AI 는 **API 래퍼 도구 7개**로만 읽는다」 | 「도구(최대 7개) … **여는 도구는 단계별로 다르다** — 중간은 업무 셋, 최종만 일곱. 잠그는 것은 프롬프트가 아니라 `enabled_tools`」(근거에 MF-71 추가) |
| **§4 AI 트랙 안건 축** | 「`list_agendas()` 로 사람 안건과 자기 안건을 **함께 조회**해 거기 맞춰 채운다」 | 「**발화만 보고 스스로 가른다. 사람 안건을 조회하지 않는다** — 미러 없음 · 전부 신설 · 합치는 것은 최종 한 번. 앞 배치 안건도 조회하지 않는다(전량 교체라 세션이 안고 간다)」 |
| **§4 배치 입력** | 「안건 · 사람 줄 · AI 줄 · 업무 · 유형은 **AI 가 도구로 그 순간 조회**한다」 | 「**조회할 수 있는 것은 업무 · 유형뿐**. 안건 · 사람 줄 · AI 줄은 **싣지도 조회하지도 않는다**」 |
| **§8 도구 표** | 「도구 7개」 한 행 | 제목을 「도구 7개**(최종 기준)**」로 + **「단계별 도구」 행 신설**(중간 셋 / 최종 일곱 · 이유 · 막는 손은 `enabled_tools` · `get_meeting`·`get_account` 도 중간엔 없다) |
| §STT 배치 입출력 | 입력·출력만 | 「조회 도구는 **중간 셋 · 최종 일곱**(MF-71)」 한 구 추가 |
| Resulting Spec | SPEC-006·7·8 「MF-1~70 반영」 | 「+ 2026-09-08 MF-71」 · reflow4 리포트 경로 추가 · **WORK-015 행 신설** · MCP work 행에 「서버는 일곱을 다 노출한다 — 중간 셋은 워커 설정」 |

**OQ**: 닫을 것 없음. 열린 OQ-10 · 11 · 12 는 전부 최종·유형 쪽이라 MF-71 에 걸리지 않는다.

---

## 2. `20-spec/spec-007-meeting-live.md` (v0.0.2 → **v0.0.3**)

| 절 | 전 | 후 |
|---|---|---|
| frontmatter | `version: 0.0.2` · `updated_at: 09-07` | `0.0.3` · `09-08` |
| 서두 개정 노트 | v0.0.2 까지 | **v0.0.3 블록 신설** — 무엇이 바뀌고 **무엇이 안 바뀌는지**(스키마 한 벌 · 전량 교체 · 검증 0~5 · 최종 · 프론트) |
| §1 Business Requirement | 「사람이 적은 줄을 볼 도구가 없던 것도 `get_agenda(id)` 로 닫힌다」 | 그 문장 삭제 → **불릿 신설**: 「회의 중 AI 는 사람 것을 보지 않는다」 + 회의 9 근거 + 「F-10 의 새 답은 **중복을 최종이 흡수한다**」 |
| **U-4 배치 반영** | 「미러한 AI 안건(`sourceAgendaId` 있음)은 사람 안건 `state` 배지, 신설은 캡션」 | 「회의 중 AI 안건은 **전부 신설** → **배지 없이 캡션 하나뿐. 미러 배지 갈래는 없다**」 |
| S-4 시나리오 1·2 | 「AI 는 `list_agendas()` · `get_agenda(id)` 로 사람이 적은 줄을 보고 요약」 · 「안건 1(사람 안건 미러, 배지 완료)」 | 「**발화만 보고 가른다**. 업무를 가리킬 때만 셋을 부른다」 · 「**안건 둘 다 「AI 안건」 캡션** — 제목이 비슷해도 별개」 |
| **§4 도구 표** | 7행 · 「단계」 없음 | **「단계」 열 신설** — 앞 넷 「**최종만**」 / 뒤 셋 「**중간 · 최종**」 + 표 위 ⚠ 블록 |
| §4 allow list 불릿 | 「`enabled_tools` = 위 7개만」 | 「**단계별로 두 벌** — 중간 업무 셋 / 최종 일곱. 프롬프트가 아니라 도구를 안 준다. `-c` 는 resume 에도 산다」 |
| §4 배치 입력 3행 | 「싣지 않는다. AI 가 `list_agendas()` → `get_agenda(id)` → … **순으로 조회**」 | 「**싣지도 조회하지도 않는다.** 부를 수 있는 것은 업무 셋뿐 · **「조회 순서」 절을 프롬프트에 두지 않는다**」 |
| §4 배치 출력 JSON | `"humanAgendaId": 12, // 미러하면 그 id` | `"humanAgendaId": null, // 회의 중 항상 null(값이 와도 서버가 무시)` · title 주석도 정정 |
| **§4 검증 2** | 「참조한 `humanAgendaId` 가 이 회의의 사람 안건(AI 안건 id 면 위반)」 | 「**회의 중 검사 대상이 아니다** — 무엇이 오든 무시하고 `null` 저장. **폐기 사유 아님.** 사람 안건 참조 검사는 최종에만」 |
| §4 검증 3 | 「업무 참조 사후 검사」 | 「**회의 중 참조 검사는 업무뿐이다**」 명시 |
| §4 검증 5 | 「`humanAgendaId` 가 있으면 `source_agenda_id` = 그 id(제목 복사), 없으면 NULL」 | 「**`source_agenda_id` 는 항상 `NULL`** — 미러 갈래 없음 · 제목은 출력의 `title` 그대로」 |
| §4 Flow(mermaid) | `participant M as MCP 도구 7개` · `Q->>M: list_agendas() · get_agenda(id) · list_tasks() …` | `MCP 도구 (중간 3 / 최종 7)` · `Q->>M: list_tasks() · get_task(id) · list_work_types() (중간은 셋뿐 — MF-71)` |
| §4 Data Contract | 「AI 안건 배지 / 「AI 안건」 캡션 ← `source_agenda_id` → 사람 안건 `state` / null」 | 「「AI 안건」 캡션 ← `source_agenda_id` **회의 중 항상 null** 이므로 캡션 하나뿐」 |
| §5 Implementation Rules | 「AI 는 `ai` 에만 쓰고 **읽기는 도구로 한다** — `list_agendas()`·`get_agenda(id)` 로 조회」 | 「**회의 중에는 사람 것을 읽지도 않는다** — 조회 도구도 열지 않는다 · **미러 안건을 만들지 않는다**」 |
| §5 옵션 빌더 | 「allow list 와 토큰을 빌더가 붙인다」 | 「**빌더는 `phase` 를 받아 `enabled_tools` 를 두 벌로 낸다**」 |
| **§6 AC** | 「워커가 `list_agendas`·`get_agenda` 를 **부른 흔적이 있다**」 | 「**부른 흔적이 없다**」 + 업무 셋만 보인다 |
| §6 AC | — | **2항목 신설** — ① AI 탭 배지 0 · `source_agenda_id` 전부 NULL ② 사람 안건을 적어도 AI 탭에 사본이 안 생긴다 |
| §6 AC | 「codex 설정에 `enabled_tools` 7개 · …」 | **두 줄로 분리** — 중간 옵션 문자열 `enabled_tools` **셋** · 안건 도구 **0건** / 나머지 설정 항목 |
| §7-A | 「MF-50 · 51 배치 입력 = 발화만 · `list_agendas()` 는 둘 다」 | MF-50 행으로 좁히고 **MF-71 행 신설**(「MF-51 의 `list_agendas()` 는 **최종 전용**으로 좁혀졌다」) |
| §7-C ERD 표 | `source_agenda_id` = 「AI 안건이 미러하는 사람 안건」 | 「**`merged` 안건이 가리키는 사람 안건** — `ai` 는 항상 NULL. 컬럼은 두고 회의 중 배치가 채우지 않는다」 |
| §7-D D-1 | 「2026-09-07 재정정(MF-50): 읽기는 도구로」 | 「**2026-09-08 재재정정(MF-71): 회의 중에는 읽지도 않는다**」 |
| §8 근거 표 | — | **MF-71 행 신설** + 「AI 는 AI 탭만」 행에 「회의 중 사람 것을 읽지 않는다」 추가 · 「배치 입력」 행 문구 정정 |

---

## 3. `40-architecture/backend/README.md`

| 절 | 전 | 후 |
|---|---|---|
| 서두 개정 노트 | 2026-09-07(MF) 부터 | **2026-09-08(MF-71) 블록을 맨 위에** — `enabled_tools` 두 벌 · 미러 안건 없음 · 걸린 절 목록 |
| §3 디렉토리 `app/mcp/` | 「도구 7개 …」 | 「**서버는 일곱을 다 노출한다. 중간에 셋만 여는 것은 워커 쪽 `enabled_tools`**」 한 줄 추가 |
| **§5-2 웜스타트 조회** | 「프로젝트·업무·안건·유형은 AI 가 **MCP 도구 7개**로 조회 — (일곱 나열)」 | 「프로젝트·업무·유형 … **여는 도구는 단계별로 다르다** — **중간 = 셋** / **최종 = 일곱**(나열)」 |
| **§5-2 배치 입력** | 「입력은 발화 하나뿐 · 스냅샷은 낡는다」 한 줄 | 그 줄 유지 + **불릿 신설** — 조회도 안 한다 · 프롬프트에서 「조회 순서」·「안건이 늘어나면 잘못」 삭제 · ① 미러 없음 ② `_parse_output(fill_final=False)` 이 `humanAgendaId` 무시(폐기 아님) ③ 앞 배치 조회 불필요 · **최종 경로 불변** |
| **§5-2 옵션 빌더** | 「빌더가 만드는 것 ① allow list(`enabled_tools` 7개)」 | 「**빌더는 `phase`(`batch`\|`final`)를 인자로 받는다** — batch 셋 / final 일곱 · 웜스타트는 final 과 같은 일곱(실제 잠금은 매 제출의 `-c`)」 |
| §10 API 표면 MCP 도구 행 | 「7개 · 전부 조회」 | 「(**회의 중 배치에는 뒤의 셋만 연다** — MF-71)」 |
| **§12 테스트 6** | 「잘못된 JSON → 전체 폐기」 | 「+ **`humanAgendaId` 가 실려 와도 폐기하지 않는다** — 무시하고 null 저장」 |
| §12 테스트 7 | 「사후 검사 강등 · payload 미저장」 | 「+ **회의 중 참조 검사는 업무뿐**」 |
| §12 | — | **7-b 신설** — ① `source_agenda_id` 전부 NULL ② 배치 프롬프트에 안건 도구 0건 ③ `phase="batch"` 옵션 셋 / `"final"` 일곱 |
| §13 BE-17 | 「도구 7개 · allow list · 토큰」 | 「+ **`enabled_tools` 는 단계별 두 벌**(빌더가 `phase` 를 받는다)」 (근거에 71 추가) |

---

## 4. `40-architecture/database/domains/meeting.md`

| 절 | 전 | 후 |
|---|---|---|
| frontmatter | `updated_at: 2026-09-07` | `2026-09-08` |
| 서두 | 09-07 저녁 추가까지 | **2026-09-08 개정 블록 신설** — 「스키마는 그대로. 바뀐 것은 `source_agenda_id` 가 채워지는 자리」 + 걸린 규칙 6개 + WORK-015 |
| 컬럼 변경 표 `source_agenda_id` | 「`track='ai'`·`merged` 안건이 미러하는 사람 안건」 | 「**`merged` 안건이 가리키는 사람 안건. `ai` 는 항상 NULL**(MF-71). 원래는 미러용이었고 지금 쓰는 자리는 최종뿐」 |
| **M-5-a** | 「두 축은 최종에서 합쳐진다」 | 「+ **회의 중에는 둘이 서로를 모른다** — 제목이 겹쳐도 상관없다」 |
| **M-5-b** | 「AI 안건은 `source_agenda_id` 로 사람 안건을 가리킨다 — `humanAgendaId` 를 참조하면 미러 안건(제목 복사)을 만든다」 | 「**채우는 것은 최종 회의록뿐.** 회의 중 AI 안건은 전부 신설 · `humanAgendaId` 는 서버가 무시 · **미러 갈래는 코드에 없어야 한다.** `human`·`ai` 는 항상 NULL」 (+ 폐기 이력 명기) |
| **M-5-c** | 「AI·`merged` 안건의 `state` 는 원본에서 복사한 표시값(AI 신설은 NULL)」 | 「`merged` 만 복사. **`ai` 의 `state` 는 항상 NULL** — 복사할 원본이 없다. AI 탭은 캡션만」 |
| **M-6** | 「읽기는 도구로 한다 — `list_agendas()`·`get_agenda(id)` 로 그 순간 조회」 | 「**사람 것을 읽지도 않는다** — 그 둘이 회의 중 `enabled_tools` 에 없다. 열리는 것은 업무 셋. 사람 것을 보는 것은 **최종 한 번**」 (+ 문구 3단 이력) |
| M-7 | 「검증 전에 지우지 않는다」 | 「+ **INSERT 하는 안건은 전부 `source_agenda_id = NULL`** — 갈라지는 자리가 없다」 |
| M-8 | 최종은 AI 가 한 번에 쓴다 | 「+ **두 트랙이 만나는 자리는 여기뿐이고, 도구 일곱이 다 열리는 자리도 여기뿐**」 |
| Related Specs | 「SPEC-007 … `source_agenda_id` · 도구 7개」 | 「… **회의 중 도구 셋**」 + **WORK-015 행 추가** |

---

## 5. `reference/2026-09-06-task-management-app/ai-prompt-draft.md`

| 절 | 무엇 |
|---|---|
| §B | 코디가 넣어 둔 **정정(2026-09-07 · MF-53)** 블록 **바로 아래**에 **「⚠ 정정 2(2026-09-08 · MF-71)」 한 줄 추가** — 「## 줄을 만들기 전에 — 순서대로 조회한다」 절(①·②)과 「안건이 발화 구간마다 늘어나면 잘못하고 있는 것이다」 **폐기**. 남는 조회는 ③ 업무 셋뿐. 구현은 WORK-015 |

초안 본문은 **기록용이라 그대로 뒀다**(§B 머리말이 「이 절은 기록용으로만 남긴다」).

---

## 6. WORK-015 (신규) — `30-work/work-015-meeting-batch-solo.md`

- 제목: **중간 배치는 AI 혼자 쓴다 — 도구 셋 · 미러 안건 폐기 · 조회 순서 절 삭제**
- 형식: WORK-011 과 동일(frontmatter · Meta · Work Summary · Role · Scope · Code Surface · Domain/Schema · Dependency · **Internal Interface Contract** · Execution(Phase) · Pre-deploy · Rollback · Done Criteria · Open Issues · Related)
- **백엔드만 · 프론트 0 · 마이그레이션 0.** Depends: WORK-011 · 012(둘 다 done)

| Phase | 무엇 | 핵심 검증 |
|---|---|---|
| **1** | `build_codex_options(…, phase: "batch"\|"final")` — `enabled_tools` 와 툴별 `approval_mode` 줄만 갈린다. 호출부 셋에 phase(웜스타트 final · 배치 batch · 최종 final). **WORK-009 의 14줄 옵션 표를 두 벌로** | `batch` = **10줄**(내장4+url+headers+enabled_tools+approval 3) · 안건 도구 문자열 0건 / `final` = **14줄 문자열·순서 동일**(회귀) · `phase` 기본값 없음(누락 시 실패) · 옵션 빌더 단일 함수 정적 검사 유지 |
| **2** | `build_batch_prompt` 에서 「조회 순서」 절 · 「안건이 늘어나면 잘못」 삭제 → 「발화만 보고 네가 가른다」 · `_parse_output(fill_final=False)` 이 `humanAgendaId` 무시(null 강제 · **폐기 아님**) · `_persist` **중간 미러 갈래 삭제**(최종 불변) | 프롬프트 grep 0 · BE §12 **6 확장**(humanAgendaId 실려도 폐기 안 됨) · **7-b 신설**(`source_agenda_id`·`state` 전부 NULL · 제목 미복사) · 7 · 7-a 회귀 · **WORK-012 최종 테스트 무수정 통과** |

`30-work/README.md` — 회의록 재작업 그룹 표에 **WORK-015 행(todo)** 추가, 그룹 제목에 「+ 2026-09-08 MF-71」, 발주 순서 문단 아래에 **「009~014 가 들어간 뒤(HEAD `5c72c25`) 다음에 발주 · `meeting_batch_service.py`·`agent.py` 를 만지므로 다른 코드 워커와 동시 금지」** 문장 추가. 「최종 수정」 09-08.

---

## 7. 닿지 않는다고 확인한 것

| 문서 | 확인 |
|---|---|
| `40-architecture/frontend/README.md` | grep 「미러」 3건 전부 **`types/api.ts` 가 백엔드 schema 의 미러**라는 뜻 — 안건과 무관. **손대지 않았다** |
| `20-spec/spec-008-meeting-close.md` | `humanAgendaId`(L698·712) · `source_agenda_id`(L530) · 도구 일곱(L766·787) · `list_agendas`(L679·787·866) 는 **전부 최종 경로**라 MF-71 이 그대로 살려 둔다. **손대지 않았다** — 단 **L168 한 곳은 아래 §8-1** |

---

## 8. 새로 드러난 것 — 코디 판단 필요

### 8-1. `spec-008` L168 「미러 안건 배지」 — 유일하게 낡은 한 줄 (브리프 범위 밖)

```
현재  「AI 요약 탭 = agendas.ai — SPEC-007 U-4 규격 그대로(트리 · 「AI 안건」 캡션 · 펼침 · 미러 안건 배지 · 줄 시각 없음)」
문제  U-4 에서 미러 배지 갈래를 지웠으므로 이 열거가 없는 규격을 가리킨다.
      가리키는 대상(agendas.ai)이 종료 후에도 회의 중 그대로라 실제로 미러 배지가 뜰 일이 없다 — 표현만 낡았다
제안  「미러 안건 배지 · 」 여섯 글자 삭제. 계약 변화 0
```
브리프가 「`spec-008` 는 확인만 하고 손대지 마라」였으므로 **고치지 않았다.** 승인하면 한 줄이다.

### 8-2. 웜스타트에 어느 phase 를 주나 — **WORK-015 가 `"final"` 로 가정** ⚠

MF-71 본문은 「**중간 배치**의 `enabled_tools` 는 업무 셋 · **최종 제출**은 일곱」만 말하고 **웜스타트를 말하지 않았다.** WORK-015 는 `"final"`(일곱)로 두고 그 근거를 Open Issues 에 적었다 — 웜스타트는 도구 **목록을 알려 주는** 자리이고 그때 요청이 없으므로, 실제 잠금은 매 제출의 `-c` 가 한다(「`-c` 는 resume 에도 산다」 — MF-71 본문). **틀렸다면 한 줄 바꾸면 되고 다른 코드는 그대로다.** 사용자 확인 항목.

### 8-3. 웜스타트 프롬프트의 「쓸 수 있는 도구」 문구 (관찰 항목)

WORK-010 이 심은 웜스타트 프롬프트에 도구 일곱이 적혀 있다면, 회의 중에는 그중 넷이 열리지 않는다. **도구가 없으면 codex 는 못 부르므로 동작은 안전**하지만 문구는 어긋난다. WORK-015 는 웜스타트 프롬프트를 건드리지 않는다(WORK-010 소관). 실물에서 AI 가 「도구를 못 찾겠다」를 내면 그때 좁힌다.

### 8-4. MF-71 밖이라 손대지 않은 기존 어긋남 — `backend/README.md` §5-2 「해시만 저장」

§5-2 단명 토큰 불릿에 「`auth_session(…)` 행을 INSERT 하고(**해시만 저장**)」이라고 있는데, **MF-69 본문은 「원문을 그 행의 컬럼에 둔다(해시가 아니다 — 2026-09-07 저녁 사용자 확정)」**이고 WORK-009 §Internal Interface 도 「`find_meeting_token(token)` **원문 일치**」다. `database/domains/account.md` A-13 이 정본으로 보인다. **MF-71 범위 밖이라 고치지 않았다** — 별건으로 잡을 것.

---

## 9. 남긴 것 · 추측하지 않은 것

- **새 결정 0건.** MF-71 본문에 없는 것(웜스타트 phase · `get_meeting`·`get_account` 를 중간에 열지 여부의 재량)은 전부 WORK-015 **Open Issues** 로 올렸다. 본문의 「중간 = 셋」을 글자 그대로 따랐다.
- `decisions-pending.md` · `walkthrough-fixes.md` 를 근거로 쓰지 않았다.
- 코드 워크트리 · `orchestration/config` 미변경.

## 변경 파일

```
para/projects/summer-star/task-management/10-decision/decision-003-meeting-notes.md
para/projects/summer-star/task-management/20-spec/spec-007-meeting-live.md
para/projects/summer-star/task-management/40-architecture/backend/README.md
para/projects/summer-star/task-management/40-architecture/database/domains/meeting.md
para/projects/summer-star/task-management/30-work/work-015-meeting-batch-solo.md   (신규)
para/projects/summer-star/task-management/30-work/README.md
reference/2026-09-06-task-management-app/ai-prompt-draft.md
orchestration/work/docs-v1/docs-v1-meeting-reflow4-report.md                        (신규 · 이 문서)
```
