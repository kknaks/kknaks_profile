
# 작업 요약 — phub-gold-jev (procedure-hub)

기간: `2026-11-16` ~ `2026-11-18`
결과: 허브 gold 조회 도구(REST · MCP · DB 76 표)를 stg 에 배포하고 데이터를 반입했다(PROCEDURE-HUB #32 · #34). 상담 채팅 앱 0.4 는 개인 레포 main 에 머지(clinic_chat #2). 고도화(SDK · 프롬프트 확정 · 그림 출력)는 다음 작업.

## 1. 무엇을 했나

11-16 에 확정한 새 gold 15표(메달리온)를 허브가 결정론 도구 9 개로 내주게 하고(REST · MCP), 같은 질문을 원장 · gold+Jev · gold MCP 세 길로 답하는 시험 앱으로 연결을 검증했다. 11-17 에 silver · gold 를 로컬 DB(76 표)로 옮기고, 그 위에 시술 상담 채팅(htmx · 얼굴 점 · 상담 객체)을 0.1 → 0.3 으로 쌓았다. 그런데 e2e 마다 새 구멍이 나서 11-18 에 패치를 멈추고 **입력 전수 표(78 대화 · 356 턴)** 로 실패를 층별로 셌고, 원인이 「글자 맞춤 resolve 가 후보 관문」 이라는 것을 수로 확인했다. 입구를 소넷 이해 호출 하나로 바꾸고(0.4) 허브 resolve 는 정확 이름 · 목록만 남겼다(0.8.1). 마지막으로 gold 를 기존 허브(`app.main`)에 「꺼져도 허브는 안 죽는」 꼴로 붙여 stg 에 배포하고 일회성 컨테이너로 데이터를 실었다.

## 2. 적용한 기술·개념

- **입력 전수 표 → 실패 층 → 설계 한 번(완료 = 표 통과율)** — 상담 입구 재설계의 근거 → [[input-space-enumeration]] · [[golden-set-regression]]
  - 왜 이걸 골랐나: 0.1~0.3 동안 e2e 에서 터진 문장 하나씩 규칙을 덧대(조사 · 줄임 · 겹침 · 부위 잇기) 매번 옆에서 새 구멍이 났다(사용자 「할 때마다 구멍이 왜 생기냐고」). 의도 꼴 × 말 꼴 × gold 실제 조합으로 대화 55 · 턴 255 를 먼저 짓고 지금 시스템에 그대로 돌리니 통과 115/239(48%) · 실패 층 = 후보 39 · Jev 43 · 앱 규칙 39 · 데이터 3 으로 갈렸다 — 데이터 보강이 아니라 구조 문제라는 것이 처음으로 수로 나왔다.
  - 무엇이 어려웠나: 정답 키 · 프롬프트 · 채점을 한 워커가 지어 소넷 97.1% 가 윗값이었다(검수: 엄격 92.5~94.1 · 프롬프트 예문 8 개가 표 턴과 같음). 앞 답을 가리키는 턴은 표의 가짜 앞 답 기준이라 실물 답과 어긋나 9 턴이 억울하게 떨어졌다 → 분모에서 따로 셈. 소넷은 같은 코드에서도 판마다 8검사 6% 가 흔들려 **같은 코드로 두 번** 재야 문턱 판정을 믿을 수 있었다.
  - 근거: `research-input-space.md` · `review-input-space.md` · `research-input-space/scripts/README.md` · `review-code-app-v04.md`(M-1 · L-8)

- **엔티티 해석을 글자 맞춤에서 LLM 고르기로(닫힌 목록 안에서만)** — 상담 0.4 입구 → [[entity-resolution]] · [[context-catalog-injection]]
  - 왜 이걸 골랐나: 같은 표 위에서 다섯 판을 쟀다 — 지금(resolve → Jev) 대상 정답 70.7% · **소넷+별칭 97.1%(2.9초)** · 소넷 후보를 Jev 로 확정 85.8% · 하이쿠 93.4% · Jev fan-out(목록 820 을 한 요청 · 표별 5 동시) 62.3%(층 접기 넣으면 83.7% · 0.34초). Jev 는 「보기 안에서 점수」 는 잘하지만 같은 줄기(필러 계열+시술)를 한꺼번에 yes 해 하나로 확정을 못 했고, 앞 대화 · 거둠 같은 맥락은 소넷이 강했다. MCP 도구 루프 · 임베딩은 지연 · 맥락 부족으로 뺐다. 지어냄은 「gold 목록 820 + 별칭을 프롬프트에 · 앱이 목록 밖 코드는 버림」 으로 막아 0/375.
  - 무엇이 어려웠나: 처음엔 Jev 사용법을 문서(llms.txt) 없이 앱 코드만 보고 「32 개 한도」 로 잘못 말했다 — 실제로는 질문 수 제한이 없고 32 개씩 **차례로** 보낸 우리 코드가 38 요청 · 10초의 원인이었다. CLI 로는 thinking 을 완전히 못 꺼(후보 5 개 모두 20 호출 중 4~5 번 켜짐) 그 턴만 5초대 · 10초 초과가 남았다 → SDK 판으로 넘김.
  - 근거: `research-input-space.md` §3 · `SPEC-008-consult-entry.md` · `para/resources/note/ai/llms.txt` · clinic_chat #2

- **허브는 결정론 · 해석은 부르는 쪽 — resolve 를 「정확 이름 → 코드 + 목록」 으로 줄임** → [[deterministic-first-ai-enrichment]]
  - 왜 이걸 골랐나: 0.5(부분 일치) · 0.7(줄임 일치)은 앱이 resolve 를 문장 이해 관문으로 쓰느라 허브 규칙을 덧댄 것이었다(사용자 「resolve 에 규칙을 추가하는 게 아니라 최소한의 목록 출력 꼴 · 입력 정리는 채팅 단」). 다른 서비스 · MCP 클라이언트에 필요한 것은 이름 → 코드와 목록뿐이다.
  - 무엇이 어려웠나: 줄이면 시험 앱(B 열)이 깨진다 → 시험 앱은 옛 허브 판(0.7.2)에 묶었다. 계약 표 밖에서 깨지는 시험(문장을 넣던 Q21 등)을 검수가 세 번에 걸쳐 더 찾았다.
  - 근거: `SPEC-001-hub-gold-mcp.md` 0.8.x · `review-code-hub-v081.md` · PROCEDURE-HUB fdc155b

- **선택적 하위 시스템은 꺼져도 본체는 뜬다(graceful degradation)** — stg 에 gold 를 `app.main` 에 붙임 → [[graceful-degradation]]
  - 왜 이걸 골랐나: stg 는 `app.main` 하나만 돈다. 별도 컨테이너 + Gateway 경로는 인프라 레포 일이고, 그냥 붙이면 새 표가 빈 첫 배포에서 gold 적재 실패(F2)가 허브 전체를 죽여 CD health 가 실패한다. 그래서 gold 의 모든 실패(빈 표 · 해시 · 접속 · 시간 한도 · 설정 · 예외)를 「gold 만 503 `unavailable`」 로 받고 본체 health · OpenAPI 는 한 글자도 안 바꿨다. 적재 시간 한도(데몬 스레드 + lifespan 안 한도)로 멈춤도 막았다.
  - 무엇이 어려웠나: 503 본문에 DB 호스트가 실릴 뻔했다(인증 없는 Gateway — 검수 R-1). 시험이 전역 앱을 다시 만들면서 다른 라우터 wiring 을 바꿔 glossary 시험 3 개가 깨졌다.
  - 근거: `SPEC-003-hub-gold-db.md` §11 · `review-spec-003-stg.md` · `review-code-hub-stg.md` · PROCEDURE-HUB d3d078c · #32

- **원천 CSV 는 레포 · 적재는 같은 이미지의 일회성 컨테이너** — stg 시드 → [[seed-data]]
  - 왜 이걸 골랐나: CSV 가 레포(`data/medallion/`)에 있으니 이미지에 데이터를 싣지 않고(ADR 「image 는 migration + API 만」), 배포가 스키마를 만든 뒤 VM 에서 `docker run --rm` 으로 dry-run → 한 트랜잭션 적재. 시작 시드 · 파이프라인 단계는 레포 ADR 이 기각한 꼴이었다.
  - 무엇이 어려웠나: 적재가 「배포 뒤」 에만 가능해(새 표는 컨테이너 시작 때 생김) 순서를 「env → 배포(gold 꺼짐) → 적재 → 재생성」 으로 짰다. `docker restart` 는 env 파일을 다시 안 읽어 env 는 배포 전에, 바꾼 뒤에는 Bastion 배포 스크립트로 재생성.
  - 근거: `research-stg-seed.md` · `stg-runbook.md`(실행 기록) · `data/medallion/README.md`

- **리버스 프록시가 Host 를 바꾸면 MCP DNS rebinding 보호가 막는다(421)** → [[reverse-proxy]]
  - 왜 이걸 골랐나: mcp SDK 기본은 Host 가 localhost 꼴일 때만 받는다. 보호를 끄지 않고 허용 목록 설정(`GOLD_MCP_ALLOWED_HOSTS`)을 더했다.
  - 무엇이 어려웠나: 공개 호스트를 넣었는데도 421 — 컨테이너 로그(`Invalid Host header: <내부 IP>:10000`)를 보고서야 Gateway 가 Host 를 백엔드 내부 주소로 넘긴다는 것을 알았다. 두 값을 다 넣어 풀었다.
  - 근거: `stg-runbook.md` 실행 기록 · `_RESUME.md` §2 11-18

## 3. 막혔던 것 / 사고

- 상담 e2e 마다 다른 문장이 실패 → 증상 패치를 0.1~0.3 세 판 되풀이 → 사용자 지적 · 「입력 전수 표부터」 로 바꿈. 처음부터 꼴 × 데이터 표를 짓고 시작했어야 했다(메모리 `feedback_input_space_before_rules`).
- 코디가 장부를 열지 않고 「구조를 통째로 바꾸자」 · 「Jev 는 대체로 맞다」 를 말했다가 장부 · 표 수로 두 번 정정했다. 제브 사용법도 공식 문서를 안 읽고 말해 정정 — 판단 전에 원천(장부 · 문서)부터 연다.
- 데이터 판 워커가 alembic downgrade 를 셸 따옴표 실수로 돌려 로컬 74 표를 내렸다 → 새 판 재적재로 회복(덤프 있었음). 이후 절차서에 「downgrade 쓰지 않음」.
- Docker 데몬이 꺼져 로컬 PG 가 내려가 있었다 → 다시 띄움(볼륨 그대로).
- 조사 워커가 코디 추가 지시(Jev fan-out 판)를 읽기 전에 완료 보고를 보냄 → 같은 터미널이 이어서 재고 표에 더함.
- 앱 0.4 구현에서 주석 한 줄이 `synergy_lines` 키를 삼켜 답 LLM 재료가 빠졌는데, 그 자리를 보던 시험 9 개가 어느 WP 「돌릴 파일」 에도 없어 아무도 안 돌렸다 → 코드 검수가 찾음.
- stg 승격 PR 이 우리와 무관한 문서(`prod-db-rename.md` — stg #28 ↔ release #30)에서 충돌 → 승격 브랜치로 release 쪽을 받아 다시 올림(#33 닫고 #34).
- stg MCP 421(위 §2) · VM 메모리 891MB · swap 0 에서 gold 가 +70MB(컨테이너 154 → 225MB) — 지금은 여유 210MB 지만 다음 판 주의.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-16 | 옛 gold(PR #31) 버리고 새 gold 15표로 허브 MCP · 3열 시험 다시 | 11-16 확정 gold |
| 2026-11-17 | silver · gold 를 DB(76 표)로 · 원장 JSON 은 DB 에 안 넣음 · 로컬 DB 먼저 | 사용자 「로컬 허브 DB 까지」 |
| 2026-11-17 | 상담 채팅 = CLI(`claude -p --resume`) · 소넷 · htmx SSR · medikit · 프롬프트 JSON | 사용자 |
| 2026-11-17 | 그림은 DB 까지 이번 판 · 출력은 다음 스펙 · 의료 검수 게이트 없음 · 한국어만 | 사용자 |
| 2026-11-18 | 패치 멈춤 — 입력 전수 표 → 실패 표 → 설계 한 번 | 사용자 「할 때마다 구멍」 |
| 2026-11-18 | 상담 판단은 소넷으로만(Jev 뺌) · resolve 는 최소 목록 꼴 · 입력 정리는 채팅 단 | 다섯 판 측정 · 사용자 |
| 2026-11-18 | 결정 표 D-1~D-15(정확 이름만 · 별칭 넣음 · 말 안 한 고민 안 붙임 · 부위 거르개 이번 턴만 · 점은 말한 고민만 · 애매 = guess + 되묻기 · 실패 = 대상 없이 되묻기 · 완료 = 8검사 90 · 3검사 95) | 사용자 「확정하고 코드 구현까지」 |
| 2026-11-18 | 워커 모델 = 앞으로 전부 opus(fable 은 데이터 메달리온 때 규칙) | 사용자 |
| 2026-11-18 | 상담 0.4 결과(8검사 88.7/90.9 · 3검사 94.3/95.3) 받음 · thinking 은 SDK 에서 끔(다음 작업) | 사용자 「이 정도면 괜찮은 거 같은데」 |
| 2026-11-18 | 이번 판은 배포로 닫음 · stg 시드 = 일회성 적재 · gold 는 `app.main` 에 붙임 · 단계 승인 없이 이어서(막힐 때만) | 사용자 |

전체 결정 행(사유 · 코디 답 포함)은 `_RESUME.md` §2 가 정본이다.

## 5. 날짜별 로그

- `2026-11-16` gold 연결 조사 → SPEC-001(허브 MCP) · SPEC-002(3열 시험) 0.4.1 → 0.6 · 허브 gold 모듈 · 시험 앱 · 화면 · 속도 탭 · 답 키 37 실행
- `2026-11-17` silver · gold DB 화(SPEC-003 · 76 표 · 적재기) · 허브 0.7.2(시술로 내려가기 · 고민 부위 · 줄임) · 상담 채팅 0.1~0.3 · 그림 데이터 · concern_site 보강 · e2e
- `2026-11-18` 입력 전수 표 · 다섯 판 측정 · 상담 0.4(소넷 입구) · 허브 resolve 0.8.1 · stg 판(gold 를 app.main 에) · PROCEDURE-HUB #32 · #34 stg 배포 · 데이터 반입 · clinic_chat #2 · gold API 안내서

## 6. 산출물

- code PR: PROCEDURE-HUB #32(release/v1.2.0 · aa46a86) · #34(stg 승격 · 60b2d57) · clinic_chat #2(main · 97d964e)
- 커밋(허브): 85c28af · daa54e3 · 3a5da4a · d97a9ad · fdc155b · d3d078c / (앱): 6303e18 · 68a31b1 · be1c622 · 296cb2c(스쿼시 머지)
- 안내서: `para/projects/company/procedure-hub/gold-api-guide.md`(stg 실물 응답 기준 REST · MCP 호출법)
- 리포트: `research-input-space.md` · `review-input-space.md` · `research-stg-seed.md` · `review-spec-008.md` · `review-work-016-017.md` · `review-code-hub-v081.md` · `review-code-app-v04.md` · `review-spec-003-stg.md` · `review-code-hub-stg.md` · `stg-runbook.md`
- 계약: SPEC-001 0.8.2 · SPEC-003 0.2.1 · SPEC-008 0.2.1 · SPEC-004~007 · WORK-001~018

## 7. 잔여

- 상담 이해 호출 SDK 판(thinking 끔 · ANTHROPIC_API_KEY 필요) — 그 뒤 시간 한도 · JSON 덧붙임(첫 객체만 읽기) 다시 판단
- 사용자 확인: `pick` 프롬프트 초안(규칙 10 · 머리 글자 9) · 거둠만 한 턴 = talk · 막힘 · 새 대화 화면 문구(빈칸) · 앞 답 가리킴 턴 사람 검수 · 애매 18 턴 정답
- 그림 출력 스펙(허브 도구 · 정적 서빙 · 화면) · 허브 Low 3(옛 줄임 주석) · 시험 앱은 허브 0.7.2 에 묶여 있음(로컬 재현 시 옛 판 워크트리 필요)
- stg VM 메모리 여유 약 210MB · swap 0 — 다음 판에서 gold 가 커지면 인프라 확인 · prod 승격은 범위 밖
- 상담 앱 워크트리 `clinic_chat/phub-gold-jev`(main 머지 · 브랜치 남음) — 다음 작업에서 이어 쓰거나 지움

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/procedure-hub/phub-gold-jev/README|phub-gold-jev]]
<!-- work-links:end -->
