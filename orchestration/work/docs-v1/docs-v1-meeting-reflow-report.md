# [architect] 회의록 계약 ↔ 흐름 결정 31건 — 반영 보고

발주: `docs-v1-meeting-reflow-brief.md` · 정본: `reference/2026-09-06-task-management-app/Meeting flow.md`(MF-1 ~ MF-63) · 2026-09-07

## 0. 한 줄

**31건 전부 반영했다.** 고친 문서 13개 — DEC-003(전체 재작성) · DEC-001 §3·§4 · SPEC-002 · SPEC-003 · SPEC-004 · SPEC-006 · SPEC-007 · SPEC-008(전체 재작성) · `40-architecture/` 5개(database README · `domains/meeting.md` 재작성 · `domains/account.md` · backend · system · frontend). 옛 설계 흔적 grep(「최종 배치」·「통합 단계」·「600자」·「도구 6개」) **0건**. 새 결정은 만들지 않았고, 정말 못 정한 것 다섯을 **근거와 함께 OQ** 로 올렸다(§3). 계약을 잇느라 내가 읽은 자리 넷은 §4 에 따로 적었다 — 사용자가 다르게 보면 그 자리만 바꾸면 된다.

## 1. MF 별 반영 표

| MF | 무엇 | 어느 문서 어느 절 | 어떻게 |
|---|---|---|---|
| **MF-1** | `/start` 전이만 · 웜스타트 큐 · 즉시 응답 | DEC-003 §4 「회의 시작」 · §7 「웜스타트 미완료·실패」 · §STT · SPEC-006 §4 `POST /start` · §5 · U-4 CTA · Flow · S-7 · AC · SPEC-007 §4 웜스타트 표 · 검증 0 · Case Matrix · §5 · AC · backend §5-2 · §5-3 · §7(W-1 해소) · §8-3 · §12 테스트 8-a · BE-14 · system 흐름 ③ · 불변식 6 · SYS-14 · ERD `ai_session_id` 주석 · meeting.md M-12 | `/start` = 한 UPDATE + 즉시 응답. 웜스타트는 commit 뒤 백그라운드 태스크가 큐에 넣고 `session_id` 를 새 세션에서 UPDATE. `ai_session_id NULL` 인 동안 배치는 평가만 하고 제출 안 함. service commit 불필요 → W-1 닫힘 |
| **MF-2** | AI 도구 = API 래퍼 7개 | DEC-003 §2 「AI 의 데이터 접근」 · §8 「AI 도구 연결」 표 · SPEC-007 §4 「AI 도구 7개」 표 · backend §1 · §5-2 · §10 「MCP 도구」 행 · system 개요 그림 · Components · External Integrations · SYS-12 | 7개 목록 · 전부 조회 · DB 직결 아님 · 권한은 백엔드 |
| **MF-3** | codex allow list | DEC-003 §2 · §8 · system **§codex 설정**(신설 — 실측 표 · 함정 셋) · backend §5-2 빌더 · SPEC-007 §4 · AC | `enabled_tools` 7개 · 내장 스위치 전부 off · 툴별 `approval_mode` · deny list 없음 |
| **MF-4** | 회의별 단명 토큰 | DEC-003 §2 · §8 · system §codex 설정 · 흐름 ③ · backend §5-2 · SPEC-007 §4 · SPEC-008 Flow(폐기) | 발급 → MCP 헤더 주입 → ② 종결 후 best-effort 폐기. 인프라는 OQ-9 |
| **MF-55** | 용어 다섯을 웜스타트로 | DEC-003 §8 「AI 도구 연결」 웜스타트 행(용어 다섯 본문) · SPEC-007 §4 웜스타트 「주는 것」 · backend §5-2 | 안건이 뼈대 · 넷은 파생 · 액션/업무 경계. 프롬프트 초안 §A 참조 |
| **MF-49** | 배치 트리거 1000자 | DEC-003 §STT · SPEC-007 Business Req · §5 · Flow · S-4 · AC · §7-A · §8 | 600 → 1000. 나머지 수치 그대로 |
| **MF-50** | 배치 입력 = 발화만 | DEC-003 §4 「배치 입력」 · §7 「없는 업무 참조」(사후 검사) · §8 In 내 업무 · SPEC-007 §4 배치 입력 표(취소선) · 검증 3 · §5 · Flow · §7-D D-1 · backend §5-2 · §8-3 · system 흐름 ③ · 불변식 4 · meeting.md M-6 · M-15 | payload 에 안건·줄·AI 안건·화이트리스트를 싣지 않는다. **사후 검사는 남긴다** — 기준 목록은 검사 시점 조회 |
| **MF-51** | `list_agendas()` = 사람 + AI | DEC-003 §4 「AI 트랙 안건 축」 · §8 표 · SPEC-007 §4 도구 표 · meeting.md M-5-a | |
| **MF-53** | AI 트랙 전량 교체 | DEC-003 §4 「배치 갱신 방식」 · §6 AI 탭 · §7 스키마 위반 · SPEC-007 U-4 · WS `ai.batch`(전체) · 검증 5 · State/Lifecycle · §5 · AC(3건) · SPEC-006 §4 트랙 설명 · backend §5-1 · §5-2 · §12 테스트 7-a · BE-15 · system 흐름 ③ · 불변식 5 · frontend §8 · FE-15 · meeting.md M-5-b · M-7 · M-16 · DB README 인덱스 행 | DELETE + INSERT 한 트랜잭션, 검증 통과분으로만. WS 프레임은 트리 전체, 화면은 통째로 교체 |
| **MF-9** | 줄 시각 없음 | SPEC-007 U-2 · U-4 · Data Contract · §5 · AC · SPEC-008 U-3 · Data Contract · SPEC-006 §4 필드 표(`createdAt` 표시 안 함) · frontend §8 · meeting.md M-11 | 안건 헤더 시각·안내 바·프롬프트 바 시각은 그대로 |
| **MF-10** | 슬래시 명령어 5개 | SPEC-007 **U-3 재작성** · S-2 · §5 · AC(2건) · §7-A | 팝오버 유지 + `/논의 /결정 /업무 /액션 /새안건`. 스페이스에서 칩. 그 밖은 텍스트. 서버는 모른다 |
| **MF-37** | async 재전사 | DEC-003 §1 In · §3 transcript · §4 종료 파이프라인 · §6 트랜스크립트 · §7 · §STT 「재전사 모델」 행 · SPEC-008 U-1 ① · §4 파이프라인 ① · 수치 · Case Matrix · Flow · AC · system External Integrations(신설 행) · 개요 그림 · 불변식 2·3 · backend §1 · integrations/soniox.py · meeting.md M-9-a · DB README transcript 주석 | `stt-async-v5` · files → transcriptions → 폴링 → 블록 → 전량 교체. 「확인 필요」(헤더 없는 webm)는 system SYS-OQ-5 |
| **MF-56** | 종료 시 배치·통합 없음 | DEC-003 전체(개정 머리 · §1 표 · §4 · §6 · OQ-7 폐기) · SPEC-008 전체 · SPEC-007 Out · U-4 푸터 문구 · §7-D D-6 · SPEC-006 §4 State · `finalBatchState` 삭제 · backend §5-3 · §6 · §8-3 · system 흐름 ③ · 불변식 7·9 · SYS-13 · meeting.md M-6-a · M-7 · M-8 · `batch_run.phase` | 호출 한 번. AI 탭은 종료 후 그대로(「종결」 없음). `/integrate` → `/finalize` |
| **MF-57** | 최종은 AI 가 쓴다 | DEC-003 §4 「최종 회의록 작성」 · OQ-7 · SPEC-008 Business Req · §4 파이프라인 ② · 「서버 검증」 머리 · meeting.md M-8 · **`source_*_line_id` 삭제** · DB README ERD · 인덱스 | 「사람 문장 복사」 폐기. **참조 존재 검증의 새 자리** = 안건 참조 · 업무 참조(사후) · 페이로드 참조 · 근거 범위(SPEC-008 §4 표) |
| **MF-58** | 재전사 실패 fallback 없음 | DEC-003 §4 「재시도」 · §7 「재전사 실패」 · SPEC-008 U-2 · §4 `/finalize` · Case Matrix ① 행 · 구현 규칙 · AC · backend §8-1 · §8-3 · §12 테스트 8 · system 불변식 11 · meeting.md M-4 · M-9-a · M-13 | 「다시 시도」 하나, ①부터. 실시간 결과로 ② 를 부르는 코드가 없어야 한다(검수 항목) |
| **MF-59** | 액션·업무 줄 페이로드 | DEC-003 §3 `lines[].payload` · §4 「업무 갱신 허용 필드」(일곱 · `done` 없음) · SPEC-008 U-6 · U-9 · U-10 · §4 `payload` 두 모양 · `POST/PATCH …/task` 본문 · Validation · Case Matrix · SPEC-006 §4 필드 표 · backend §8-3 · §12 테스트 8-c · meeting.md **`pending_change` → `payload`** · M-14 · M-14-a · DB README | 액션 = 생성분(시작일~기한 · 할일 포함) · 업무 = 변경분 일곱. `done` 은 스키마 층 422 |
| **MF-52** | 출력 스키마 한 벌 | DEC-003 §3 · §7 「회의 중 페이로드」 · §STT · SPEC-007 §4 배치 출력 JSON(`headline`·`termCorrections`·`payload` null) · 검증 4 · SPEC-008 §4 ② · backend §5-2 · `ai_schemas/meeting_notes.json` 하나 · system 불변식 12 · meeting.md M-8-a | `payload` 뿐 아니라 `headline` · `termCorrections` 도 같은 방식(§4 ③) |
| **MF-54** | STT 용어 보정 두 겹 | DEC-003 §2 화자 · §3 「용어 보정 표」 · §6 「STT 용어 보정」 · SPEC-008 §4 `context` 표 · `termCorrections` · 「용어 보정 적용」 · AC · system External Integrations · meeting.md **`term_corrections` 신설** · M-9-b | ① `context.general`·`text`, `terms` 는 OQ-10 ② 표 → `auto` 만 스크립트 치환 · 화자 라벨 불변 · 화면 없음 |
| **MF-60** | 줄 종류 못 바꿈 | DEC-003 §1 표 ④ · §5 수정(U) · SPEC-008 U-7(셀렉터 제거) · U-8 · §4 `PATCH lines`(`kind` 거부) · Validation · Case Matrix · 구현 규칙 · AC · §7 제외 · meeting.md M-20 | |
| **MF-61** | 사람 줄은 빈 드로어 | DEC-003 §3 · §5 · SPEC-008 U-6 · U-9 · U-10 프리필 표 · S-7 · S-9 · AC · meeting.md `payload` 근거 | 액션 줄 → 제목·프로젝트만. 업무 줄 → §4 ② |
| **MF-62** | 안건 제목만 · 삭제 없음 | DEC-003 §1 표 ③ · §5 · SPEC-008 U-7 · §4 안건 참조 검증(「모든 사람 안건이 정확히 한 번」) · AC · meeting.md M-5-d · M-5-e | |
| **MF-13** | 업무 생성 = 새 업무 드로어 + 안건 | DEC-003 §5 · §8 Out · SPEC-008 U-10 재작성 · U-6 · S-6 · S-7 · AC · **SPEC-003 U-1**(슬롯·프리필·제출처 문단) · frontend §2 규칙 8 · FE-18 | 회의록 전용 드로어(시안 L2600~2882) 폐기 |
| **MF-14** | 업무 갱신 = 업무 상세 드로어 | DEC-003 §5 · SPEC-008 U-9 재작성 · U-6 · S-8 · S-9 · AC · **SPEC-003 U-3**(「넣기」 모드) · **U-8**(0건 폴백) · frontend §2 규칙 8 | 회의록 전용 드로어(시안 L2306~2599) 폐기. 후보 고르기는 업무 것 |
| **MF-21** | `work_type.description` | **DEC-001 §3**(유형.설명 행) · §4(기본 3종 색·설명 편집) · **SPEC-002** U-2 · U-3 · §4 GET/POST/PATCH · Validation · Data Contract · DEC-003 §8 In 인증·설정 · SPEC-007 도구 표 · SPEC-008 U-10 · **`account.md` A-4 · A-12** · DB README ERD · 표 · meeting.md 컬럼 표 | 시드 문구 둘. 「미팅·회의」는 OQ-11 |
| **MF-25** | 카운트 다섯 | DEC-003 §1 표 「AI 한 줄 요약 바」 · SPEC-006 U-8 · §4 `mergedSummary` · AC · SPEC-008 U-3 · U-4 · §4 출처 표 · Data Contract · AC | `discussionCount` · `taskCount` 추가. 화면에 그리는 그것을 센다 |
| **MF-36** | 지운 자리 유지 | DEC-003 §1 표 ⑤ · SPEC-008 U-7 · §4 `DELETE` · `POST lines` orderIndex · 구현 규칙 · S-5 · AC · SPEC-006 §4 트랙 설명 · backend §12 테스트 8-b · meeting.md M-20 · DB README `order_index` 주석 | 코드가 당기고 있던 것 — SPEC-008 옛 문장(「뒤 줄이 당겨진다」 3곳) 정정 |
| **MF-63** | 확인 모달 420 | DEC-003 §1 표 「확인 모달 크기」 · **frontend §6**(모달 두 크기 · `openConfirm size`) · FE-17 · SPEC-008 U-7 · AC · §7 제외 | `ConfirmModal` 하나. 420 은 `warning` 슬롯 없음 |
| **MF-5** | 미리보기 CTA 상태별 | SPEC-006 U-8 헤더 CTA 표 · U-2 CTA · S-1 · S-7 · AC · §7 | |
| **MF-6** | 미리보기 패널 고정·스크롤 | SPEC-006 U-6 · U-8 · AC · §7 · **frontend §2 규칙 7**(밀도 prop) · FE-18 | compact 밀도 prop 하나 |
| **MF-7** | breadcrumb 링크 + 「←」 | **frontend §6-3**(신설) · FE-16 · SPEC-006 U-1 · U-4 · AC · SPEC-007 Placement · U-1 · AC · SPEC-008 Placement · U-3 · AC · **SPEC-003 U-4** · **SPEC-004** 헤더 주석 | 전 화면 공통 — `PageHeader`/`Breadcrumb` 한 곳 |
| **MF-8** | 헤더 순서 배지 줄 → 제목 | frontend §6-3 · SPEC-008 Placement · U-3 헤더 ①~④ · U-4 · §7 제외(L1436~1443) · SPEC-006 U-4 헤더 · SPEC-007 U-1(§4 ④) · SPEC-003 U-4(업무가 정본) | |

## 2. 크게 바뀐 넷 — 어디에 어떻게

| # | 바뀐 것 | 갔던 자리 |
|---|---|---|
| ① | 종료 시 배치·통합 호출 폐지 | 파이프라인 = ① 재전사 → ② 최종 회의록(SPEC-008 §4). `/integrate` → `/finalize`(①부터). `finalBatchState` · 「종결」 · 「통합본」 어휘 삭제. **참조 존재 검증** → 안건 참조(모든 사람 안건 정확히 한 번 · AI 안건 id 참조 금지) · 업무 참조(사후 · 강등) · 페이로드 참조(틀린 키만 뗀다) · 근거 범위. `source_*_line_id` + 부분 UNIQUE + CHECK 삭제(ERD) |
| ② | 배치 컨텍스트 없음 | SPEC-007 §4 배치 입력 표 취소선 · 도구 7개 표 · 검증 3 「사후 검사」 — 기준 목록은 회의 프로젝트 업무(무소속은 무소속) **검사 시점 조회**. 웜스타트도 컨텍스트 없음 |
| ③ | AI 트랙 전량 교체 | M-7 재작성 · SPEC-007 검증 5 · WS 프레임 전체 · frontend 「통째로 교체」 · 「검증 전에 지우지 않는다」 테스트 7-a |
| ④ | 편집 다섯 · 종류 전환 없음 | DEC-003 §1 표 ①~⑤ · SPEC-008 U-7 · `PATCH lines` 에 `kind` 없음(스키마 층) · M-20 「줄 종류는 못 바꾼다」 |

## 3. OQ — 정말 못 정한 것 (DEC-003 Open Questions 에 근거와 함께)

| OQ | 무엇 | 어디를 찾았는데 없었나 | 계약이 취한 자리 |
|---|---|---|---|
| **OQ-8** | 웜스타트 실패의 기록·재시도 · 세션 없는 회의의 ② | `Meeting flow.md` §1-5 ③ 「**확정 안 함**」 · `decisions-pending.md` ① 「배치 실패와 같은 경로」는 코디 제안 · MF-58 은 ② 재시도 이야기 | 회의는 시작 · 세션 없으면 배치 안 돎(확정분만). `/end` 는 세션 없이도 받고 ② 는 「세션 없음」으로 `final_failed` |
| **OQ-9** | MCP 서버 배치 · 단명 토큰 인프라 | `Meeting flow.md` §1-5 ① 「별도 work」 · ② 「토큰 인프라 확인 안 했다」 · SPEC-001 §4(access 는 무상태 JWT — 폐기 표면 없음) · `account.md` A-7 | 도구 7개 · allow list · 헤더 토큰만 계약. 배치·발급 축은 MCP work |
| **OQ-10** | 재전사 `context.terms` 원천 | MF-54 ① 「사내 고유명사·제품명」 · DEC-001 §1·§3 · `database/README.md` §2 · `grep 용어|term decision-001` 0건. 보정 표는 회의 1건 단위라 다음 회의로 안 넘어간다 | `context.terms` 비움. `general` · `text` 만 |
| **OQ-11** | 「미팅·회의」 시드 설명 문구 | MF-21 「기본 3종에도」인데 Meeting flow 에 둘만 있다 · DEC-001 §4 | 빈 값 시드. 동작 영향 없음(AI 는 종류=업무만 고른다) |
| **OQ-12** | 유형 「기본값」(MF-59 「못 고르면 기본값」) | DEC-002 §3 type 기본값 「—」 · SPEC-003 U-1 기본 없음 · DEC-001 §4 종류=업무 기본이 둘 · `grep 기본값 spec-003` 0건 | `payload.workTypeId` `null` 허용 → 드로어가 유형을 비운다(제출 조건이 사람에게 고르게) |

실물 확인 항목(OQ 가 아니라 확인): **헤더 없는 webm 을 `stt-async-v5` 가 받나** — system SYS-OQ-5 · DEC-003 §STT 「확인 필요」.

## 4. 새 결정이 아니라 「두 MF 를 이은 읽기」 — 사용자가 다르게 보면 여기만

| # | 읽기 | 근거 | 어디 |
|---|---|---|---|
| ① | **회의 중 헤더도 배지 줄 → 제목 순서.** MF-8 본문은 「회의록 상세」와 「시작 전 헤더도」만 적었고 회의 중을 안 적었다. 같은 라우트의 상태 변화라 같은 규약을 적용했다 | MF-8 · MF-7 「전 화면 공통」 | SPEC-007 U-1 · §7-A 표시 |
| ② | **사람이 적은 업무 줄(`taskId` 없음)** → 「업무 연결」 → 후보 고르기(업무 것) → 연결 → 업무 상세 드로어(평소 그대로). MF-61 「빈 드로어」에서 업무 줄은 `taskId` 없이 드로어를 열 수 없어 MF-14 「손으로 연결할 때만 후보 고르기」를 먼저 지나게 했다. `PATCH …/lines/{id} {taskId}` 표면 신설 | MF-61 + MF-14 | SPEC-008 U-6 · U-9 · §4 · §7 |
| ③ | **`headline` · `termCorrections` 도 nullable** — MF-52 는 「페이로드만 nullable」이라 했으나 이 둘도 최종 전용이라 같은 방식으로 뒀다(파일 하나 원칙) | MF-52 | SPEC-007 §4 · SPEC-008 §4 |
| ④ | **「다시 시도」는 ①부터** — ① 이 성공하고 ② 만 실패했어도 재전사부터 다시 돈다(부분 재시도 갈래를 안 만든다, $0.10/시간). **`/integrate` → `/finalize`** 이름 변경 — 통합이 없는데 이름만 남길 수 없었다. `integration_state` 컬럼·필드 이름은 ERD 그대로 두고 뜻만 「최종 회의록 생성 상태」(M-4) | MF-58 「재시도는 원본+안건+요약」 | SPEC-008 U-2 · §4 · §7 |
| ⑤ | **`context.text` = 같은 프로젝트의 직전 종료 회의 `ai_headline`** — MF-54 「직전 회의 요약」에서 회의록이 가진 요약은 그것뿐이다 | MF-54 ① | SPEC-008 §4 |
| ⑥ | **최종 호출 payload = 재전사 스크립트 하나** — MF-56 은 「재전사 스크립트 + 사람 줄 + AI 줄을 주고」라 했으나 MF-50·51 의 도구(`list_agendas` 가 둘 다 · `get_agenda` 가 줄)가 그것을 이미 주므로 payload 에 다시 싣지 않았다 | MF-50 · 51 · 56 | SPEC-008 §4 ② |
| ⑦ | 「+ 액션 아이템」 칩은 옛 설계대로 **곧장 업무 생성**(새 업무 드로어) — 액션 줄만 적는 갈래를 만들지 않았다. AI 탭 배치 0회 종료 시 안내 바 「AI 요약 없음」(빈 상태 문구) | 옛 SPEC-008 U-10 · MF-13 | SPEC-008 U-7 · U-3 |

## 5. 코디가 이어서 할 것

- **SPEC-003** — U-1 · U-3 · U-8 에 문단을 더했다(슬롯 · 「넣기」 모드 · 0건 폴백 · breadcrumb). §4 · AC 는 안 건드렸다 — SPEC-003 워커가 규격을 받아 마무리
- **WORK-006 · 007 · 008** — 옛 설계(`/integrate` · `pendingChange` · `source_*_line_id` · 마지막 배치 · 통합 규칙 · 종류 전환)를 그대로 담고 있다. 이 발주 범위 밖이라 손대지 않았다 — 재발주 전 갱신 필요
- **`ai-prompt-draft.md` §C** — 「최종 배치 프롬프트」가 옛 사상(「이전 배치 줄은 버려진다」 = 최종 배치)이다. 정본 폴더라 손대지 않았다. §「아직 안 정한 것」 ①(한 줄 요약 자리)은 MF-56 으로 구조상 닫혔고 ③(통합 프롬프트)은 사라졌다
- **DB 마이그레이션 영향** — `meeting_line.pending_change` → `payload` · `source_human_line_id` · `source_ai_line_id` + 부분 UNIQUE 2 + CHECK 삭제 · `meeting.term_corrections` 추가 · `meeting_batch_run.phase` CHECK(`integration` 제거) · `job.error_code` 값 · `work_type.description` 추가
- `_RESUME.md` 가 이 세션 중 바뀌어 있다(내 변경 아님) — 코디가 확인

## 6. 끝났다고 말하기 전에 (브리프 §6)

- [x] MF-1 ~ MF-63 31건 전부 반영 — §1 표
- [x] 옛 설계 흔적 grep 0건 — 「최종 배치」 · 「통합 단계」 · 「600자」 · 「도구 6개」(대상 9개 문서). 「통합본」 · 「다시 생성」 · `finalBatchState` · `pendingChange` · `source*LineId` 도 살아 있는 계약에서는 0건(해소된 OQ 이력 문장에만 남는다)
- [x] SPEC-007 ↔ 008 정합 — 출력 스키마 한 벌(007 §4 가 정본, 008 은 최종 전용 필드만) · `payload` · `mergedSummary` 다섯 · 줄 시각 없음 · 헤더 규약 · `/finalize` · AI 탭 종료 후 그대로
- [x] OQ 마다 「어디를 찾았는데 없었나」 — §3
- [x] 새 결정 없음 — 이은 읽기 일곱은 §4 에 표시
