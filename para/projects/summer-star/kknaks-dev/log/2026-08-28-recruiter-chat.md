
# 작업 요약 — recruiter-chat (kknaks-dev)

기간: `2026-08-28` ~ `2026-08-28`
결과: **머지(#23 코드 · #24 문서)·홈서버 배포·운영 e2e 검증까지 하루에 완주.** 채팅이 kknaks.dev 에 라이브다.

## 1. 무엇을 했나

포트폴리오 홈을 채팅 퍼스트로 전면 재구성했다 — 로그인 없는 채용담당자가 질문하면
codex 가 MCP tool 로 공개 이력 데이터(career·problem·개인/회사 제품)를 읽고 1인칭으로
대답한다. 설계(baseline→결정 3→spec, owner 문답으로 OQ 전부 닫음) → BE·FE 워커 병렬
발주 → 리뷰어 검수(WARN 10건) → 실사용 피드백까지 수정 8라운드(spec v0.0.14) →
로컬 compose e2e → 머지·배포·운영 e2e. 이 레포 **첫 오케스트레이션 발주**였고,
kknaks-dev 프로젝트 config·roles·단일 레포형 규약을 이번에 세웠다.

## 2. 적용한 기술·개념

- **tool calling 경계 설계 (MCP + 표면 축소)** — 익명 입력이 들어오는 에이전트의 손을 「정의한 tool」로만 한정
  - 왜 이걸 골랐나: 공개 번들 export(물리 격리)는 어드민 실시간 제어가 안 되고, 프롬프트 지시는 경계가 아니다. HTTP MCP + 제출 단위 `-c` 오버라이드(url·turn 토큰·allowlist·툴별 approval_mode) + `features.shell_tool=false`·`sandbox=read-only` 로 쉘 자체를 껐다 — 인젝션이 부릴 손이 tool 뿐
  - 무엇이 어려웠나: 노출 판정이 두 축임을 뒤늦게 확정 — 「공개 표면 조건(visible) ∧ chat_exposed(옵트인)」. 어드민 kind 축(표 이름)과 문서 유형 축(company_product)이 우연히 같은 이름이라 상수 하나가 두 축을 겸하다 갈라냈다
  - 근거: `app/back/service/chat/submission.py` · `app/mcp/` · spec-017 §4 · PR #23
- **상주 소비자 + 이벤트 폴딩 (스트리밍 없는 실시간)** — text 부분 누적·tool_use_id 멱등 upsert 를 DB 에 폴딩하고 프론트는 2초 폴링만
  - 왜 이걸 골랐나: WS 인프라 이식 없이 폴딩된 DB 를 읽는 것만으로 「자라나는 답변 + 쌓이는 tool 단계」가 된다. 사내 검증 구현(mediness landing-chat)의 실측 계약을 채택 — 중복 수신을 정상 경로로 두는 멱등 설계까지
  - 무엇이 어려웠나: 레퍼런스 없이는 「client.result() 완료 대기뿐」이라는 틀린 전제로 D6(스트리밍 없음)을 확정할 뻔했다 — 레퍼런스 정독이 결정 두 개(D5·D6)를 뒤집었다
  - 근거: `app/back/service/chat/consumer.py` · DEC-027 D5/D6 개정 이력
- **FastAPI BackgroundTasks 와 트랜잭션 커밋 순서** — 제출 배선을 teardown 커밋에 기대다 커밋 전 조회로 스킵 → 대화 영구 pending
  - 왜 이걸 골랐나(수정): 순서를 프레임워크 동작에 기대지 않고 세 경로 전부 명시 커밋 뒤 큐잉으로 고정 — 레퍼런스가 같은 사고 뒤 박은 계약과 동일 지점
  - 무엇이 어려웠나: 단위 테스트 124개가 전부 통과한 채로 뚫렸다 — conftest 가 start_turn 을 통째로 스텁해 「그 시점에 row 가 보이는가」를 아무도 안 쟀다. 로컬 e2e 첫 질문에서 발각. 수정 후 「독립 세션으로 실제 조회」하는 테스트로 불변식 자체를 잠갔다
  - 근거: `app/back/service/chat/runtime.py` · fix2 보고(RED→GREEN→재RED 역검증)
- **codex resume 세션의 선례 관성** — stale 세션이 예전 스탠스(「회사 상세 비공개」)를 따라 새 tool 을 무시
  - 왜 이걸 골랐나(수정): 프롬프트는 resume 에도 매 턴 다시 실린다 — 거절 범위를 「미공개」로 좁히고 「이전 턴에서 사렸더라도 이 지침이 우선」 한 문장으로 선례를 뒤집었다
  - 무엇이 어려웠나: 새 대화는 정상이고 옛 대화만 사려서 원인이 프롬프트인지 세션인지 갈랐어야 했다 — 같은 문구를 새 대화에 재현해 격리
  - 근거: `app/back/service/chat/prompt.py` 머리 주석 · fix6 보고
- **CSS 컨테이닝 블록 함정 (`animation-fill-mode: forwards` + transform)** — keyframe 의 transform 이 남아 `position: fixed` 가 뷰포트가 아니라 조상 기준이 됨 → 오버레이가 화면을 61px 이탈
  - 무엇이 어려웠나: 값은 맞는데 위치가 밀리는 증상 — FE 워커가 Playwright 계산값 실측으로 원인을 특정하고 absolute+relative 로 구조 수정
  - 근거: `app/front/app/globals.css` · fix5 보고
- **mono vs sans 시각 크기 차** — 같은 px 라도 mono 가 커 보인다. 컴포저(15px mono)가 본문(15.5px sans)보다 커 보이던 원인 — 수치가 아니라 시각 급으로 맞춰야 한다(14px 로)
  - 근거: fix6 보고
- **오케스트레이션 단일 레포형** — 문서(para)와 코드(app)가 한 레포인 프로젝트의 첫 발주 규약: 워커 SSOT 는 코디 워크트리 절대경로, allowed_paths 로 문서 보호, PR 은 브랜치로 분리, 회고는 config `summary_dest` 로 para log/ 착지
  - 근거: `orchestration/runbook.md` 「프로젝트 유형」 절 · `config/projects/kknaks-dev.json`

## 3. 막혔던 것 / 사고

- **제출-커밋 순서 실결함** (위 §2) — 단위 테스트가 못 잡는 층위가 있다. e2e 를 스택 다 세우고 한 바퀴 돌린 것이 하루 안에 이걸 꺼냈다 → 앞으로도 「한 바퀴 완주」를 머지 전 관문으로.
- **mock 화면 오인 사건** — owner 가 본 404 카드의 원인을 BE 구멍으로 추정해 fix8 을 발주했는데, 워커가 재현 실패 + 저장 카드 전수 조회로 반증했고, 실제로는 **FE 워커 검증용 mock 서버(:3100)의 닫힌 탭**이었다(픽스처 문구·카드가 화면과 글자 단위 일치, 실 DB 에 해당 질문 없음). 헛발주였지만 회귀 5건·판정식 문서화가 남았다 → 검증 서버는 내릴 때 「탭 잔상」까지 보고하기로 규약화.
- **서버 미커밋 착지 데이터와 배포 reset 충돌** — 잔디 착지 잡이 써둔 `ax-lead.md`(이력서 알맹이 2건)가 미커밋 상태로 남아 deploy 의 checkout 이 안전 정지. `rescue/ax-lead-20260828` 로컬 브랜치 + /tmp 백업으로 보존 후 진행. 서버에 push 자격증명이 없어 원격 push 는 미완 — 후속 판단 필요.
- **agent 브랜치의 squash 드리프트** — 문서 PR 을 agent 통째로 올리면 옛 커밋이 딸려 온다. main 에서 새 브랜치를 파 이번 세션 범위만 추출했고, 범위 밖 드리프트 14파일이 미동기로 남아 있음을 확인했다(후속).

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-08-28 | 홈 전면 재구성 — 채팅 히어로 + /chat (DEC-025) | 채팅 자체가 포트폴리오 — 숨기면 의미 없음. 시안 확인으로 확정 |
| 2026-08-28 | 익명 세션 = 서버 발급 httpOnly 쿠키, IP 는 식별자 기각 (DEC-026) | NAT·모바일. 해시만 저장 |
| 2026-08-28 | 실행 = 기존 open-kknaks 워커 + 전용 chat 큐, 데이터 = MCP tool (DEC-027) | 검증된 것 재사용, 새 설계력은 tool 경계에. owner 의 tool calling 학습 목적 |
| 2026-08-28 | 레퍼런스(mediness landing-chat) 계약 채택 — ~~stdio 브릿지·스트리밍 없음~~ → HTTP MCP·소비자 폴딩으로 D5·D6 개정 | 사내 실측이 원안의 전제를 반증 |
| 2026-08-28 | 근거 카드: product·career·problem 은 우측 문서 패널, project·note 는 이동 (~~모달~~ → ~~전부 패널~~ → owner 가 B 안 선택) | 전용 페이지 유무가 경계. 채팅 흐름 유지 |
| 2026-08-28 | retry 는 failed 를 pending 으로 되살림(새 줄 없음) — 리뷰 W6 환류 | 같은 질문 두 줄 UX 기각 |
| 2026-08-28 | 노출 판정식 = 공개 표면 조건 ∧ chat_exposed | 공개 API 가 보여주는 것이 tool 의 상한(D3) |
| 2026-08-28 | 근거 카드 스냅샷 404 위험 v1 수용 (spec OQ-5) | 발생 조건 드묾, 렌더마다 생존 확인은 폴링 비용 |

## 5. 날짜별 로그

- `2026-08-28` 설계(BL-008·DEC-025/026/027·SPEC-017) → kknaks-dev 오케스트레이션 신설 → BE·FE 병렬 발주 → 리뷰 WARN → 수정 8라운드(워커 발주 총 16건: BE 8·FE 7·리뷰 1) → 로컬 e2e(실결함 1 적발·수정) → PR #23·#24 머지 → 홈서버 배포 + 운영 e2e → 노출 옵트인 ON. back 169 · mcp 24 · tsc 0

## 6. 산출물

- code PR: https://github.com/kknaks/kknaks_profile/pull/23
- docs PR: https://github.com/kknaks/kknaks_profile/pull/24
- 커밋(main, squash): `6c296f9` feat(chat) #23 · `b40d23b` docs(chat) #24
- 리포트: `review-code-report.md`(8축 검수) · 워커 완료 보고 16건(인박스)

## 7. 잔여

- **레이트리밋 (DEC-026 OQ-1) — 최우선.** 채팅이 이미 공개라 익명 LLM 호출이 열려 있다. 세션+IP 이중 제한 별도 발주
- 서버 rescue 브랜치(`rescue/ax-lead-20260828`) 처리 — main 반영 vs 파이프라인 재생성
- agent 브랜치의 범위 밖 문서 드리프트 14파일 동기화
- 어드민 대화 열람 화면 · WS/SSE 승격 · mcp SDK 2.x — 후속 백로그 (spec §7)
