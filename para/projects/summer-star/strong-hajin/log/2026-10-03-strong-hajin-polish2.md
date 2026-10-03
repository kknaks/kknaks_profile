# 작업 요약 — strong-hajin-polish2 (strong-hajin)

기간: `2026-10-02` ~ `2026-10-03`
결과: 코드 kknaks/Strong_hajin#10 · 문서 kknaks/kknaks_profile#73 · 인프라 MediSolveAIDev/k8s_infra_mac#8 머지, **2026-10-03 운영 반영**(`d1b5137-arm64`, Argo Synced/Healthy 8/8)

## 1. 무엇을 했나

1차(WORK-008) 운영 반영 뒤 사용자가 운영에서 AX 로 업무를 만들어 보며 낸 지적 다섯(체크리스트가 비어 옴 · 수정 창이 바로 등록됨 · 「등록 중」 파랑 · 상세 헤더 줄 붙음 · 날짜 순서·종류)과 로컬 E2E 에서 더한 하나(AX 가 회의·업무 내용을 안 봄)를 한 판(WORK-009)으로 처리했다.
「다른 것들도 다 논의」라는 사용자 말대로 **코드 워커 읽기 전용 조사 → 사용자와 계약 → SPEC(검수) → WP → 페이지별 구현·검수·재수정 → 실물 확인 → PR → 운영** 순으로 갔다.
착지: AX 초안 「저장」 명령(`save_draft`) · AI 가 체크리스트·내용을 관련 기록 근거로 제안 · 채팅 서랍 단추 상태 · 업무 상세 날짜 넷과 완료 시 마감일 채움 · 「마감일」·`2026/10/06` 통일.

## 2. 적용한 기술·개념

- **확정 없는 저장 = 회차만 올리는 두 번째 명령** [[optimistic-lock]] · [[idempotency]] · [[human-in-the-loop]] — 「수정은 저장, 확정은 카드에서」
  - 왜 이걸 골랐나: 기존 `revise` 는 업무 요청의 재상신(차례를 상대에게 넘김)이라 같은 이름이면 봉투가 다른 두 계약을 한 id 로 내린다. 새 id `save_draft` 로 내고, 회차를 여는 기록 코드만 confirm 과 공유(`_open_revised_round`)해 기록이 갈라지지 않게 했다
  - 무엇이 어려웠나: 검수가 낡음·경합 구멍을 연달아 짚었다 — 다른 화면에서 먼저 저장하면 낡음 422 뒤 영영 막힘(최신 회차 재조회로), 저장 중 Esc → 바로 등록하면 **고치기 전 값으로 업무가 생김**(저장 중 창 닫힘·카드 단추 잠금), 자료 ID 순서·생략으로 등록이 회차를 또 올림(서버 정렬·생략 시 최신 스냅샷). 「같은 값이면 같은 회차, 같은 재전송이면 영수증」을 서버가 보장해야 화면 경합이 데이터로 새지 않는다
  - 근거: SPEC-002 §4 「초안 저장」 · `review-fe-p2a1-report.md` · `review-be-p1-report.md` · `review-be-p1b-report.md` · `6efdac1` · `4789647`
- **AI 에게 「제안할 것」과 「근거만 쓸 것」을 칸별로 나눈다** [[evidence-binding]] · [[prompt-engineering]] — 체크리스트가 비어 오던 원인
  - 왜 이걸 골랐나: 서버는 체크리스트를 어디서도 버리지 않았다(조사로 단계별 확인). 원인은 1차에서 넣은 「대화가 준 것만, 지어내느니 비워라」가 **모든 칸**에 걸린 것. 사람이 카드에서 검토하는 초안이므로 내용·체크리스트는 제안, ID 는 대화·조회 근거, **날짜·사람은 대화가 준 것만**으로 칸마다 기준을 달리했다
  - 무엇이 어려웠나: 탐색을 열자 기준이 다시 섞였다 — 「ID 와 날짜는 대화·조회 근거」 문장이 남아, 회의 할 일의 마감 후보가 마감일로 옮겨 갈 틈이 생겼다(검수 W1). ID 문장과 날짜 문장을 물리적으로 나눴다
  - 근거: SPEC-001 S-9 7·8 · `be-survey-report.md` §1-2 · `review-be-p3-report.md` · `1d4cd1f`
- **생성 턴만 제동을 푸는 예외 꼬리** [[knowledge-graph-assisted-retrieval]] · [[retrieval-augmented-generation]] — AX 가 회의·업무를 안 보던 원인
  - 왜 이걸 골랐나: 실물 도구 호출이 목록 둘뿐이었다. 지시문이 회의·자료·업무 상세를 한 번도 이름으로 들지 않았고, 「묻지 않으면 graph 를 걷지 않는다」 류 제동 5문장이 생성 턴에도 실렸다. 제동 원문은 다른 질문 턴의 속도를 지키므로 지우지 않고 「업무 초안 턴은 예외」 꼬리만 달았다
  - 무엇이 어려웠나: 꼬리가 금지 문장(「넓힌 목록으로 내 업무를 답하지 않는다」) 뒤에 붙어 금지까지 풀리는 듯 읽혔다(검수 W3). 그리고 턴 제한 90초에 첫 실물이 67초 — 「검색은 도구마다 한 번, 상세 최대 3건」 상한을 문장으로 못 박자 45초로 줄었다
  - 근거: `be-survey2-report.md` · `review-be-p3-report.md` · 실물 2회(45초/25초)
- **CSS 명시도 동률이면 뒤가 이긴다** [[design-system]] — 「등록 중…」이 파랗던 원인
  - 왜 이걸 골랐나: 1차의 검정 덮어쓰기가 `:not(:disabled)` 에만 걸려, 진행 중 비활성 + 포인터 위에서 DS `.scax-button:disabled`(0,2,0)와 `--solid-primary:hover`(0,2,0, `:not(:disabled)` 없음)가 동률 → 후순위 hover 가 이겼다. DS 원본을 고치면 앱 전체가 바뀌므로 서랍 스코프(0,3,0)로만 덮고 DS 결함은 OQ-901 로 남겼다
  - 무엇이 어려웠나: jsdom 은 CSS 를 적용하지 않는다 — 테스트는 규칙 원문·명시도 계산·렌더 클래스로 단언했고, 실제 색은 Playwright 로 `getComputedStyle` 을 찍어 확인했다
  - 근거: `fe-survey-report.md` §3 · `review-fe-p2a2-report.md` · `d1bb87d`
- **날짜 문자열과 시각을 다르게 포맷한다** [[date-time]] — 「처리일」이 하루 밀리던 것
  - 왜 이걸 골랐나: 포맷터가 넷이었고 시각(`completed_at`)을 UTC 로 잘라 서울 새벽 완료가 전날로 보였다. 날짜 전용 문자열은 `Date` 없이, 시각만 `Intl`(Asia/Seoul)로 옮기는 포맷터 하나로 모았다. 검수가 LA 시간대로 돌려 하루 안 밀림을 확인
  - 근거: `review-fe-p2b-report.md` · `c64cddf`

## 3. 막혔던 것 / 사고

- **워커가 API 오류(ENOTFOUND)로 조용히 멈췄다** — Phase 3 fix1 을 받자마자 끊겼고 완료 신호가 없어 사용자가 「멈춘 거 같은데」로 짚었다 → `orca terminal read` 로 화면을 보고 재개 지시. 같은 때 세션 재연결로 워커 핸들 넷이 바뀌어 있었다. **보고가 조용하면 화면부터** 를 또 늦게 했다
- **코디 핸들이 세션 도중 바뀌었다**(시작 때 env 의 stale 값을 피해 `c0a5…` 를 골랐는데, 이후 다시 `b2ea…` 로 돌아옴) → 브리프 전부와 `_RESUME` 을 일괄 치환하고 살아 있는 워커에게 정정 전송
- **셸 heredoc 안의 백틱이 실행됐다** — PR 본문을 따옴표 없는 heredoc 으로 고치다 `` `graph_search` `` 등이 명령으로 실행돼 본문이 깨졌다 → 파일 편집으로 다시 쓰고 GitHub 본문을 재확인. 본문은 따옴표 heredoc 또는 파일로만
- **원격 kubectl `custom-columns` 의 대괄호를 medi-me zsh 가 glob 으로 먹었다** → `jsonpath` 를 따옴표로(RUNBOOK-002 §6 에 기록)
- **데모 DB 에 회의가 없다** — E2E-6 의 회의 쪽은 실물로 확인하지 못했다(업무 쪽만). 운영에서 사용자 확인이 남는다
- 워커가 「내부 이름」으로 분류해 남긴 pydantic `title='기한'` 이 실제로는 채팅 확인 폼 칸 라벨이었다(검수 FAIL). **화면에 닿는 문자열은 「서버가 화면용으로 내는 것 전부」 로 세야** 한다

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-02 | E2E 지적은 전부 논의 대상 — 코드 워커 읽기 전용 조사 먼저 | 사용자 「다른 것들도 다 논의잖아」 |
| 2026-10-02 | ~~수정 창 등록 = confirm+draft(1차)~~ → 수정 창 「저장」(파랑), 확정은 카드 「등록」만 | 사용자 E2E-2 · 「파랑으로 가자」 |
| 2026-10-02 | 상세에 날짜 넷, 목록·캘린더·간트는 예정~마감 그대로 | 사용자 「업무 상세에서 일단」 |
| 2026-10-02 | 빈 예정 칸은 실제 값으로 — 시작일(유지) · 마감일은 완료 때(신규), 되돌리지 않음 | 사용자 「마감예정일도 마찬가지」 |
| 2026-10-02 | 실제 종료일 = 완료 보고 시각 · 「마감일」 · `2026/10/06` · 계획/실제 기한 두 값 SPEC 정리 | 코디 권고 · 사용자 「나머지는 권고안으로」 |
| 2026-10-02 | 저장 명령은 새 id `save_draft`(revise 미재사용) · 낡음은 기존 confirm 관례 422 · Case Matrix 정정 | 워커 판단 · 검수 동의 |
| 2026-10-02 | E2E-6: 초안 전 회의·업무·자료 탐색을 근거로 · 상세 최대 3 · 사람은 대화가 이름 댄 사람만 · 날짜는 대화만 | 사용자 「2번은 안 할거야 · 1번만」 · 검수 W1 |
| 2026-10-02 | 채팅 단추 상태는 서랍 스코프만 — DS 원본 hover 결함은 OQ-901 | 앱 전체 영향 |
| 2026-10-03 | 운영 반영 후 아카이브 | 사용자 |

## 5. 날짜별 로그

- `2026-10-02` 세팅 · 운영 E2E 지적 5건 기록 · BE/FE 읽기 전용 조사 · 계약 확정 · SPEC 반영(FAIL→fix1→재검수 WARN) · WP · Phase 1(BE)·2b(FE) 병렬 · 2a-2·2a-1 · 페이지별 검수·재수정 · 로컬 실물(AX 초안·save_draft·마감일 채움·화면 캡처) · make verify · 사용자 E2E 중 E2E-6 추가 → 조사·SPEC·Phase 3
- `2026-10-03` Phase 3 재수정(워커 API 오류로 멈춤 → 재개) · 실물 45초/25초 · 코드 PR #10 · arm64 이미지 · 인프라 PR #8 · Argo sync · 문서 PR #73

## 6. 산출물

- spec PR: https://github.com/kknaks/kknaks_profile/pull/73
- code PR: https://github.com/kknaks/Strong_hajin/pull/10 (squash `d1b5137`)
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/8

- `kknaksss/strong-hajin-polish2` → `main`
  - `1d4cd1f` feat(backend): AX 초안 전 관련 회의·업무·자료 탐색을 근거로 (WORK-009 Phase 3 · E2E-6)
  - `6efdac1` feat(backend): AX 초안 저장(save_draft) · AI 체크리스트·내용 제안 · 완료 시 마감일 채움 (WORK-009 Phase 1)
  - `4789647` feat(frontend): AX 초안 「수정」 모달 = 저장(save_draft), 확정은 카드 「등록」만 (WORK-009 Phase 2a-1)
  - `d1bb87d` feat(frontend): 채팅 서랍 안 사람 행동 단추 — 진행 중·비활성까지 검정 계열 (WORK-009 Phase 2a-2)
  - `c64cddf` feat(frontend): 업무 상세 날짜 넷 · 출처 줄 간격 · 「마감일」·2026/10/06 통일 (WORK-009 Phase 2b)
- 리포트: `be-survey-report.md` · `fe-survey-report.md` · `be-survey2-report.md` · `review-spec-report.md` · `review-spec2-report.md` · `review-spec3-report.md` · `review-fe-p2b-report.md` · `review-fe-p2a2-report.md` · `review-fe-p2a1-report.md` · `review-be-p1-report.md` · `review-be-p1b-report.md` · `review-be-p3-report.md` · `flaky-baseline-evidence.md`

## 7. 잔여

- **운영 확인(사용자)**: AX 업무 생성 — 체크리스트·내용이 관련 기록 근거로 채워지고, **회의가 있는 주제**에서 회의 내용이 반영되는지(데모 DB 에 회의가 없어 미확인) · 턴 시간(90초 제한, 로컬 45초)
- **실패 회의 `ac0e41…`** — 아직 failed(다시 시도 안 누름). 다른 하나는 콜드스타트로 done 확인
- **OQ-901 DS hover 결함** — `solid/outlined/text/danger:hover` 에 `:not(:disabled)` 없음, 앱 전체에서 비활성+hover 가 활성처럼 보임(이번엔 채팅 서랍만 덮음) · IconButton 비활성 규칙 없음
- **기존 부채**: confirm 낡음 422 뒤 재조회 없음(저장 경로만 고침) · 낡음 오류 영문 문장 그대로 · `submitted_at`·`valid_until` UTC 자름 · 「AX 제안 N」 칩이 채팅에서 초안을 만든 직후 갱신되지 않는 것(화면 재진입 전, 확인 필요)
- **기준선 날짜 의존 테스트 5건**(CreateWork 시작일 4 · CreateWorkLayout 1) — 1차 회고에서 넘어온 채 그대로
- 1차 회고 §7 에서 넘어온 것: 서버 성능 · 「AX 제안」 칩 대상 확대 · DS-gaps 올릴지 · 남은 OQ(SPEC-001 OQ-K · DEC-007)
