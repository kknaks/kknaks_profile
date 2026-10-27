---
type: work
id: WORK-001
title: "통역 PWA 구현 — back 로그인 · 용어집 · 통역 WS · front 화면 · PWA · 로컬 E2E · 배포"
status: in-progress
product: interpret-pwa
work_type: new-feature
owner: kknaks
progress: 90
created_at: 2026-10-26
updated_at: 2026-10-27
tags:
  - product/interpret-pwa
  - doc/work
  - status/in-progress
links:
  baselines:
    - "[[baseline-001-interpret-pwa|BASE-001]]"
  decisions:
    - "[[decision-001-interpret-pwa|DEC-001]]"
  specs:
    - "[[spec-001-interpret-pwa|SPEC-001]]"
  works: []
  releases: []
  related: []
---

# 통역 PWA 구현

SPEC-001 을 빈 레포 `kknaksss/interpret-pwa` 에 세운다. 순서는 DEC-001 D-12 —
**back 뼈대 · 로그인 · 용어집 → 통역 WS(실물 호출) ↔ front 뼈대 · 화면(병렬) → 로컬 E2E(사용자) → 배포(마지막)**.

> 2026-10-26 fix1 — SPEC-001 0.2.0(문서 리뷰 FAIL 2 · WARN 6)에 맞춰 WP1 ~ WP5 내용 · 완료 조건과 「열린 것」 표를 고쳤다.
>
> 2026-10-26 fix2 — SPEC-001 0.3.0(DEC D-18 ~ D-21 · 확정 시안 · Soniox 실물 ① ~ ⑦ · 코드 리뷰 FAIL-1 · WARN 1 ~ 6 · 사용자 화면 피드백 `e2e-feedback-batch-1.md`)에 맞춰 **WP6 을 backend(WP6-BE) · frontend(WP6-FE) 두 행으로 구체화**하고 WP1 ~ WP5 상태 · 「열린 것」을 고쳤다.
>
> 2026-10-27 fix3 — SPEC-001 0.4.0(DEC D-22 ~ D-33)에 맞춰 WP6 ~ WP8 상태를 실제(배포 main d0a91a7)로 고치고, 폰 피드백 1 ~ 3(D-27 ~ D-32 — WORK 표 밖에서 발주 · 재배포)을 기록하고, **D-33 용어집 시드 전환을 WP9(backend) · WP10(frontend) · WP11(재배포 · 폰 확인)** 으로 더했다.
>
> 2026-10-27 fix4 — SPEC-001 0.4.1 에 맞춰 WP7(건너뜀) · WP8 · WP-P · WP9 · WP10 · WP11 상태를 실제(배포 main 9befd18 · PR 번호)로 고치고 **WP12(D-34 시작 오버레이 언어 단추)** 를 더했다.
>
> 1 파일 = 1 work = **빌드 계획**. 계약은 SPEC-001 만 참조한다 — 여기서 계약을 새로 정하지 않는다.

## Meta

- Covers spec: SPEC-001
- 코드 레포: `kknaksss/interpret-pwa`(로컬 `/Users/kknaks/git/toy_pr2/interpret-pwa`) — 범위 `back/` · `front/` · 루트 `docker-compose.yml` · `.env.example`. 배포 WP 는 infra 레포 `k8s_infra_mac`(`charts/interpret-pwa` 등 — config `interpret-pwa.json`)
- 워커: backend · frontend · reviewer · infra (config `orchestration/config/projects/interpret-pwa.json`)
- 통역 원형: cc-prototype `origin/main:procedure/back`(back) · `origin/main:_archive/cc/front/lib/interpret.ts`(브라우저 오디오) — read-only, **복사**(import 금지)
- 순서 원칙: WP1 이 **로그인 응답 · 토큰 · 오류 본문 모양을 먼저 고정**(SPEC-001 §3) → front 는 그 모양으로 붙는다. 통역 WS 모양은 원형 그대로라(SPEC-001 §5.3) WP2 와 WP3 은 처음부터 병렬
- 검증은 WP 마다 **그 범위의 시험만**. 전체(`uv run pytest -q` 전체 · `npm run build` · compose)는 WP7 에서 한 번
- 키(`SONIOX_API_KEY`) · 로그인 값은 사용자가 레포 루트 `.env` 에 넣는다(D-11). 워커 · 코디는 `.env.example` 만. 키가 없으면 실물 확인은 pending 으로 보고
- 워커는 사용자 포트(3600 · 8600 · 3700 · 8700)의 프로세스를 건드리지 않는다. 이 레포는 8800 · 3800(SPEC-001 §2.2)

## Work Packages

| WP | 내용 | 계약 | 담당 | 선행 | 범위(경로) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|---|
| WP1 | **back 뼈대 · 로그인 · 용어집** — uv 프로젝트(Python 3.12 · 원형 의존성 중 fastapi · uvicorn · pydantic-settings · httpx · websockets · opencc · ruff · pytest) · `config.py`(SPEC §2.4 env 전부 · 루트 `.env` → `back/.env`) · `container.py` · `main.py`(CORS = `INTERPRET_FRONT_ORIGIN` · 오류 처리기 `{error:{code,message}}` · 접근 로그 쿼리 지움) · `domain/errors.py` · **로그인**(env 대조 · 상수 시간 · 5회/1분 잠금 · HMAC 토큰 · `/api/auth/login` · `/api/auth/me`) · **용어집**(기동 때 한 번 읽기 · 실패면 빈 용어집 · 중복 `ko` 첫 행 · `GET /api/glossary?lang=`) · `GET /api/health` · `build_context()`(§4.3 · §4.4 줄이기 — 순수 함수) · `Dockerfile`(CMD `--port 8800` 고정) · 루트 `docker-compose.yml`(ports 8800 · 3800 고정 · front `build.args` 는 `${NEXT_PUBLIC_API_BASE_URL:-http://localhost:8800}` 치환) · 루트 `.env.example`(이름만 · `INTERPRET_BACK_PORT` 없음) | SPEC-001 §2 · §3 · §4 | backend | — | `back/**` · `docker-compose.yml` · `.env.example` | §9.1 「로그인」 · 「용어집」 · 「context」(재연결 제외) 시험 통과 · `.env.example` 값 0 · 실물 1회: 기동 로그에 용어집 `version` · `count 158`(또는 그날 값) · `/api/glossary?lang=yue` 가 번체 | `cd back && uv run ruff check . && uv run pytest -q tests/test_auth.py tests/test_glossary.py tests/test_context.py` · 실물 matrix 1회 | 완료(2026-10-26 · 결과는 WP6 로) |
| WP2 | **back 통역 WS** — 원형 `service/interpret/{session,soniox,assembler,chinese}.py` · `api/interpret.py` · `tests/test_interpret.py` 복사 · `langs.py`(SPEC §5.5 매핑 한 곳) · `parse_start` 의 `lang` 6개 · `traditional` · `scheduleId` 무시 · `yue` → Soniox `zh` + 번체 자막 · STT 설정에 `context`(WP1 `build_context`) · **`ready` 앞 STT 설정 확인**(최대 2초 · `SonioxError.error_type` · `invalid_request` 만 `terms` 빼고 STT 1회 재연결 · 그 뒤 TTS 열기 · 같은 브라우저 WS 유지 · `ready` 뒤 거절은 재연결 없음 — SPEC §4.4.1) · WS 인증(Origin → 토큰 · accept 전) · 오류 문구 env 위치 | SPEC-001 §5 · §4.4 · §4.4.1 | backend | WP1 | `back/app/service/interpret/**` · `back/app/api/interpret.py` · `back/app/container.py` · `back/app/main.py`(router) · `back/tests/test_interpret.py` · `back/tests/test_context.py`(재연결 추가) | §9.1 「통역」 · 「context」(§4.4.1 가짜 Soniox 5건) · 「비밀값」 통과 · **실물 §9.3 ① ~ ④ · ⑥ · ⑦** — 6개 언어 각각 context 연결 수치 · 용어집 target 대로 번역된 용어 수 · ⑦ 거절까지 걸린 시간(2초 확인 창 확정) · **결과 기록 → 사용자 결정 2건**: ② 를 외국어 발화로도 돌린 결과(역방향 용어 필요 여부 — SPEC OQ-003) · ⑤ 괄호 병기 target 이 번역 · TTS 에 나온 모양(SPEC OQ-009) | `uv run pytest -q tests/test_interpret.py tests/test_context.py` · 실물 스크립트(PCM 파일 → WS · 키는 사용자 `.env`) | 완료(2026-10-26 · 결과는 WP6 로) |
| WP3 | **front 뼈대 · 화면 · PWA** — Next.js 16 · React 19 · Tailwind 3 · `@medisolve-ai/medikit@1.4.0`(원형 `procedure/front` 방식 — preset · styles · pretendard) · 포트 3800 · `lib/api.ts`(`NEXT_PUBLIC_API_BASE_URL` · 401 → 로그인) · `lib/session.ts`(`localStorage`) · **로그인 화면** · **통역 화면 배치**(헤더 햄버거 = medikit `Popover` + `Button` · 외국어 영역 180° · 전환 아이콘(인라인 SVG) · 언어 고르기 = medikit `ComboBox` 6개 · 가운데 원 자리 · 한국어 영역) · 「탭해서 통역 시작」 오버레이 · 용어집 패널 = medikit `BaseModal` + `Table` · 로그아웃 · `front/.env.example`(`NEXT_PUBLIC_API_BASE_URL` 이름만 · 개발은 `.env.local`) · **PWA**(manifest · 아이콘 · 서비스 워커 — `/api` · WS 캐시 안 함 · wake lock) · `Dockerfile`. 원 상태 8개 · 자막은 **가짜 상태로 그려 보기까지**(WS 는 WP4) | SPEC-001 §2.3 · §6 · §7.1 · §7.2 · §7.3(색 · 문구 · 외국어 영역 문구 7개 × 6개 언어) · §7.6 · §8 | frontend | WP1 의 §3 응답 모양(문서로 이미 고정 — 코드 완료를 기다리지 않아도 된다) | `front/**` | `tsc` · `lint` · `build` 통과 · 쓴 medikit 클래스 **빌드 산출 CSS 전수 대조 빠진 것 0** · 로컬 실 back(WP1)으로 로그인 → 통역 화면 → 용어집 패널(6개 언어) → 로그아웃 · 뒤집힘 ↔ 바로 보기 스크린샷(뒤집힌 상태에서 `ComboBox` 펼친 목록 방향 포함 — SPEC OQ-010) · 상태 8개 + 오버레이 가짜 렌더 스크린샷 | `cd front && npx tsc --noEmit && npm run lint && npm run build` · 클래스 대조 스크립트 | 완료(2026-10-26 · 결과는 WP6 로) |
| WP4 | **front 통역** — `lib/interpret.ts`(원형 복사 — AudioWorklet 16 kHz 640샘플 · 24 kHz 재생 · 반이중 400 ms) · WS `?token=` · **오버레이 탭 안에서 `AudioContext` 깨우기 · 마이크 · WS**(자동 시작 없음 · `ready` 전 PCM 없음) · `start{lang}` · `pause`/`resume`(원 누름 · `pause` 때 지금 재생 멈춤) · `stop`(언어 바꿈 · 로그아웃 · 백그라운드 → 복귀 때 「시작 전」 오버레이) · caption → 영역 배치(§7.5 · D-16) · 원 상태 판정(§7.3 #1 ~ #8 순서 — **멈춤 중 TTS 는 「출력 중」**) · 음량 반응(AnalyserNode) · 「〈언어〉로 출력 중」 · 오류 + [다시 연결] · 자동 재연결 없음 | SPEC-001 §4.4.1(클라 쪽) · §5.2 · §5.3 · §7.3 · §7.4 · §7.5 · §8 「끊김 · 재연결」 | frontend | WP2 · WP3 | `front/lib/interpret.ts` · `front/components/**`(통역 화면) | `tsc` · `lint` · `build` 통과 · 단위 시험(있으면 — 영역 배치 · 상태 판정(멈춤 중 `audio_start` → 출력 중 → 재생 끝 + 400 ms → 멈춤 · 백그라운드 복귀 → 시작 전) · 반이중 타이머) · §9.2 「시작 전」 오버레이 확인(새로고침 진입) · **맥 브라우저 `localhost:3800` + 실 back 로 실발화 1회** — 한국어 · 외국어 각 1문장 · 자막이 각 영역에 자기 언어로 · TTS 재생 · 재생 중 송신 0 B | `npx tsc --noEmit && npm run lint && npm run build` · 실발화 1회(키 없으면 pending) | 완료(2026-10-26 · 결과는 WP6 로) |
| WP5 | **리뷰** — WP1 ~ WP4 를 SPEC-001 대조(로그인 같은 401 · 잠금 · 토큰 검증 · 용어집 실패 동작 · context 조립 · 줄이기 순서 · `yue` 매핑 · 번체 자막 / TTS 간체 · WS accept 전 인증 · Soniox 두 연결 정리 · 영역 배치 D-16 · 반이중 · 비밀값 · public 값 · 「조용히 통과하는 자리」 — 용어집 없이 몰래 연결 · `ready` 뒤 거절에 몰래 재연결 · 없는 medikit 클래스 · 컴포넌트) · **외국어 영역 안내 문구 6개 언어 × 7개 값 검토(SPEC OQ-006 — 기계 번역 수준이면 PoC 범위로 표시)** | SPEC-001 전부 | reviewer | WP4 | read-only | FAIL / WARN / PASS 목록(파일:줄 + SPEC 절) · 처분은 코디가 사용자와 | — | 완료(2026-10-26 · 결과는 WP6 로) |
| WP6-BE | **back 수정 묶음** — ① **역방향 용어(D-18)**: `build_context` 에 역방향 짝(정방향 뒤 · 같은 행 · `yue` source `t2s` · 역방향 source 중복은 처음 짝) · 줄이기 순서 `terms` 뒤부터 → 역방향 뒤부터 · 정방향 · `general` 유지 · `forward_only()` · `invalid_request` 재연결 = **정방향만**으로 STT 1회(처음부터 정방향만이면 재연결 없음) · 로그 칸 수(정방향 · 역방향 · 뺀 수) ② **TTS 괄호 제거(D-19)**: `strip_parens()` 를 TTS 보내기 직전 한 곳 · 반각 · 전각 · 섞은 짝 · 겹침 · 앞 공백 · 짝 없는 괄호 그대로 · 비면 TTS 안 보냄 · caption 은 그대로 ③ **WARN-1** 용어집 읽기 어떤 예외든 빈 용어집(URL 모양 오류 포함 · 이유 = 예외 종류 이름) ④ **WARN-6** 용어집 10초 = 전체 시간(`asyncio.wait_for`) ⑤ **WARN-2** 망가진 토큰(ASCII 아님 등) → HTTP 401 · WS 1008(bytes 비교) ⑥ **WARN-5** 로그인 env 빈 채 기동 → 경고 1줄(이름만) · 응답은 같은 401 ⑦ **실물 재확인 §9.3 ⑧ ~ ⑪** — 6개 언어 역방향 포함 통과 최대치 실측 → `GLOSSARY_CONTEXT_MAX_CHARS` 기본값(가장 작은 통과치 − 10%)을 `config.py` 기본값으로(`.env.example` 은 이름만 그대로) · 그 값으로 6개 언어 거절 0 · 역방향 적중 · 괄호 TTS · URL 모양 오류 기동 | SPEC-001 §3.1 · §3.2 · §4.2 · §4.3 · §4.4 · §4.4.1 · §4.5 · §5.7 · §9.1 · §9.3 ⑧ ~ ⑪ | backend | WP5 처분(코디 · 사용자 — `e2e-feedback-batch-1.md`) | `back/app/service/glossary.py` · `back/app/service/auth.py` · `back/app/service/interpret/{session,assembler}.py`(TTS 입력 · 재연결) · `back/app/config.py`(기본값) · `back/app/main.py`(기동 경고) · `back/tests/test_{context,glossary,auth,interpret}.py` · 실물 스크립트 | §9.1 「로그인」 · 「용어집」 · 「context」 · 「통역」 중 0.3.0 항목 시험 추가 · 통과 · **실물 ⑧ 언어별 통과 최대치 · 정한 기본값 · 그 값으로 거절 0 · 뺀 쌍 수** · ⑨ 역방향 적중 수(en · zh · ja 3개씩 — D-18 전과 비교) · ⑩ ja TTS 입력 괄호 0 · caption 괄호 그대로 · ⑪ 기동 · `ready` — 결과 JSON(키 · 토큰 0) · SPEC §4.4 · §2.4 기본값 갱신은 코디 → planner | `cd back && uv run ruff check . && uv run pytest -q tests/test_context.py tests/test_glossary.py tests/test_auth.py tests/test_interpret.py` · 실물 스크립트(⑧ ~ ⑪) | 완료(2026-10-26 · 168 passed · ⑧ ~ ⑪ 통과 · 기본값 **18832** → SPEC 0.4.0 §4.6 · OQ-002 닫음) |
| WP6-FE | **front 수정 묶음** — ① **시안 맞춤(D-20)**: 화면 17개를 `design/project/*.dc.html` 값으로(SPEC §6 · §7 표의 시안 파일 · 클래스 · 크기 — 로그인 카드 · 말풍선 · 부제 · 눈 단추 · 401 테두리 · 429 박스 / 헤더 56 · 카드 · 가운데 줄 196 · 상자 144 / 원 크기 96 · 88 · 100 · 96 ~ 144 · 글리프 · 링 · 외국어 안내 색 점 · 오류 박스 / 자막 `text-typo-title-sm-500` · `final:false` **gray-600** / 메뉴 196 · 로그아웃 red / 용어집 모달 부제 「N개 · 읽기 전용」 · 칸 폭) ② **테마**: `app/styles/ceramique-theme.css` 복사(cc-prototype `origin/main:procedure/front/app/styles/ceramique-theme.css`) · `<html data-product="ceramique">` ③ **아이콘**: 화면 전환 = 회전 화살표 SVG(⇅ 삭제) · 바로 보기일 때 `bg-primary-100 border-primary-500 text-primary` ④ **이름(D-21)**: 헤더 워드마크 「Tongky」 · 로그인 제목 · `metadata.title` 「통키」 · **PWA manifest `name` 「통키」 · `short_name` 「Tongky」** ⑤ **오버레이가 헤더까지 덮음**(리뷰 WARN-3 — 시안 `State-1-Start`) ⑥ **FAIL-1**: 재생 큐를 비울 때 「버림」 표시 → 다음 `audio_start` 까지 바이너리 버림 · 게이트 그대로 ⑦ **WARN-4**: 출력 언어 · 원 색 · 점 색 바꾸는 시점 = 그 발화 첫 조각 재생 시작 시각(마이크 막음은 `audio_start` 즉시) | SPEC-001 §6 · §7.1 ~ §7.6 · §8 manifest · §9.2 | frontend | WP5 처분 · (⑥ ⑦ 은 WP6-BE 와 무관 — 병렬) | `front/app/**`(layout · manifest · styles · login) · `front/components/**` · `front/lib/interpret.ts` · `front/lib/halfDuplex.ts` · `front/lib/view.ts` · `front/tests/**` | `tsc` · `lint` · `build` 통과 · 클래스 대조 빠진 것 0(시안에서 옮긴 클래스 포함) · 단위 시험 추가(FAIL-1 「pause 뒤 같은 id 조각 → 재생 0 · 게이트 그대로 · 다음 `audio_start` 뒤 재생」 · WARN-4 「앞 발화 재생 중 다음 `audio_start` → 표시는 앞 발화 끝에」) · **시안 대조 스크린샷 17장**(390 × 844 · 시안 파일과 같은 상태 · primary 계산값 `#2498bd` · 오버레이 위 햄버거 안 눌림) · manifest 응답의 `name` · `short_name` | `cd front && npx tsc --noEmit && npm run lint && npm run build && npx vitest run` · 클래스 대조 스크립트 · 스크린샷 | 완료(2026-10-26 · D-22 ~ D-25 범위 추가 반영 · 23 통과 · 클래스 166 누락 0 · 스크린샷 17 + D-22 · D-24 · D-25) |
| WP7 | **로컬 E2E** — `docker compose up --build`(8800 · 3800) · SPEC-001 §9.4(0.3.0 — 시안 모양 · 멈춤 뒤 무음 · 역방향 용어 · 괄호 TTS 포함) · 코디가 먼저 한 번 → 사용자. **전체 검증은 여기서 한 번**. 피드백은 모아서 한 번에 수정 발주 | SPEC-001 §9.4 | 코디(진행) · 사용자 · 수정은 해당 워커 | WP6-BE · WP6-FE | 레포 전체 | 사용자 로컬 E2E 통과 · SPEC-001 §10 OQ-001 · OQ-005 · OQ-007 사용자 확인 기록 | `cd back && uv run ruff check . && uv run pytest -q` · `cd front && npm run build` · `docker compose up --build` | 건너뜀(2026-10-26) — 사용자가 로컬 E2E 를 건너뛰고 배포 주소 폰 테스트로 감(WP8 · WP-P). 코디 compose 확인만 함 · OQ-001 · 005 · 007 은 폰 확인으로 |
| WP8 | **배포**(맨 뒤 · 별도) — **들어가기 전에 도메인 · 경로 결정(D-15 · SPEC-001 OQ-011)** · 이미지 빌드(arm64) · infra 차트 `charts/interpret-pwa` · ArgoCD 앱 · Ingress(`/api` → back · **WS `/api/interpret` 업그레이드 · 버퍼링 끔 · 시간 초과 늘림** · `/` → front) · Secret(`SONIOX_API_KEY` · 로그인 아이디 · 비밀번호 · 세션 비밀값 — 값은 클러스터에만) · front 빌드 `NEXT_PUBLIC_API_BASE_URL` = 배포 주소 · SPEC-001 §9.5 확인 · **휴대폰 실기기**(홈 화면 추가 · 마이크 · 화면 꺼짐 방지 · `wss` 실발화) | SPEC-001 §8 · §9.5 · D-12 · D-15 | infra · backend · frontend(이미지 · Dockerfile) · 코디 · 사용자(기기) | WP7 · 도메인 결정 | infra 레포 `charts/interpret-pwa/` · `argocd/applications/interpret-pwa*.yaml` · `provisioning/secrets/interpret-pwa*.env.example` · 코드 레포 이미지 빌드 설정 | 배포 주소(HTTPS)에서 §9.5 전부 · 휴대폰 standalone 실발화 1회 · 유휴 2분 안 끊김 · 레포 · 차트 비밀값 0 | `helm lint charts/interpret-pwa` · `helm template … -f values-prod.yaml` · `kubectl apply --dry-run=client` · 배포 주소 확인 | 완료(2026-10-26 첫 배포 `https://tongky.medisolveai.xyz` · 코드 PR #1(046eabe) · infra PR #25 · ns `interpret-pwa-prod` · Argo 수동 sync · Secret `interpret-pwa-secret` · `ghcr-pull` · DNS CNAME `tongky`) |
| WP-P | **폰 피드백 1 ~ 3**(기록 — 표 밖 발주 · 완료) — ① D-27 로그인 입력 16px · D-28 zh-Hant(lang 7개 · Soniox zh · 자막 번체 · 메뉴 번체) ② D-28 개정(목록 표시 이름 · 중국어/대만어) · D-29 초기화 · D-30 데모 로그인(`/api/auth/config` · `/api/auth/demo` · `INTERPRET_DEMO_LOGIN`) ③ D-31 언어 목록 자체 목록(카드 안 · 180°) · D-32 zh-Hant `s2twp` | SPEC-001 0.4.0 §2.4 · §3.3 · §3.4 · §5.5 · §5.6 · §7.1 ~ §7.3 | backend · frontend · designer | WP8 | `back/**` · `front/**` · 시안 | 각 보고(`fix-phone{1,2,3}-*-report.md`) | back ruff · pytest(190 passed) · front tsc · lint · build · vitest(28) · 클래스 대조(191 누락 0) | 완료(2026-10-26 · 코드 PR #2(4ccf905) · #3(d0a91a7) · infra PR #26 · #27 · 재배포) |
| WP9 | **back 용어집 시드(D-33)** — ① **시드 스키마 · 검사**: `back/seed/glossary.json` 위치 · §4.2 머리 · term · entry 필드 · 검사 1 ~ 5 를 한 함수(`validate_seed`)로 · `SeedError`(경로 · id · 규칙 이름) ② **가져오기 스크립트** `back/scripts/import_glossary.py`(§4.8 — `--url` · `--from-file` · `--out` · 출력 파일이 있으면 안 씀 · 같은 `ko` 행 합치기 · 괄호 분해 다섯 모양 · zh-Hant = zh 의 `s2twp` 초안 `reviewed:false` · 결정적 출력 · 끝에 검사) → **실행 1회로 첫 시드를 만들어 커밋**(matrix `2026-07-01-reviewed-v5` 또는 그날 판 · 요약 수치를 보고에) ③ **로더**: lifespan 에서 `load_seed` · 실패면 기동 실패(§4.4) · 성공 로그 1줄 · `Dockerfile` 이 `seed/` 복사 ④ **context**: `build_context` 를 시드 term 기반 · `ContextParts`(네 묶음 · 구조로) · `to_soniox` · 줄이기 순서 넷 · `forward_only` = 정방향 기본만 · `yue` · `zh-Hant` `t2s` · zh-Hant 는 zh-Hant entry(§4.5 · OQ-013) · `GLOSSARY_COLUMN` 삭제 · 로그 칸 수 ⑤ **메뉴 API** `rows: [{id, category, ko, koAliases, term, aliases, reviewed}]` · `count` = 그 언어 행 수 · 런타임 `s2twp` 메뉴 변환 삭제(§4.7) · `/api/health` 시드 판 ⑥ **Procedure Hub 런타임 호출 제거**(§4.9 — `load_glossary` · `parse_matrix` · `_fetch` · `split_translation_terms` · `GLOSSARY_MATRIX_URL`(config · `.env.example`)) ⑦ **시험**(§9.1 「시드」 · 「context」 · 「메뉴」 · 「가져오기 스크립트」 — matrix 기반 용어집 시험은 시드 기반으로 바꾸거나 지운다) ⑧ **실물 §9.3 ⑫ ~ ⑯**(7개 언어 거절 0 · zh-Hant 한도 · 써마지 · 울쎄라 정방향/역방향 · 기동 실패) — ⑬ 이 기본값을 바꾸면 `config.py` · `.env.example` 주석 · 보고(SPEC 반영은 코디 → planner) | SPEC-001 0.4.0 §2.1 · §2.4 · §3.3(health) · §4 전부 · §5.5 · §5.6 · §9.1 · §9.3 ⑫ ~ ⑯ | backend | WP-P(배포본 위) | `back/seed/**`(새) · `back/scripts/import_glossary.py`(새) · `back/scripts/live_check.py` · `back/app/service/glossary.py` · `back/app/service/interpret/{langs,session}.py` · `back/app/api/glossary.py` · `back/app/schemas/glossary.py` · `back/app/config.py` · `back/app/container.py` · `back/app/main.py` · `back/Dockerfile` · `back/tests/test_{seed,context,glossary,import_glossary,interpret}.py` · 루트 `.env.example` | §9.1 해당 묶음 통과 · **레포 시드가 검사 통과(시험 ①)** · `grep -rn "stg-procedure-hub\|GLOSSARY_MATRIX_URL\|glossary/matrix" back/app` 0 · 가져오기 요약(term 수 · 언어별 entry 수 · 합친 행 · 분해 종류별 수 · `reviewed:false` 수) · 실물 ⑫ ~ ⑯ 수치(JSON · 키 · 토큰 0) · 깨진 시드로 `docker compose up` 시 back 이 안 뜸 1회 | `cd back && uv run ruff check . && uv run pytest -q tests/test_seed.py tests/test_context.py tests/test_glossary.py tests/test_import_glossary.py tests/test_interpret.py` · `uv run python scripts/import_glossary.py`(1회) · 실물 스크립트(⑫ ~ ⑯) | 완료(2026-10-27 · 코드 PR #4(9befd18) · 183/239 passed · 첫 시드 157 term `2026-10-27.2` · 실물 ⑫ ~ ⑯ · 한도 **20251**(코디 처분 — SPEC 0.4.1 §4.6)) |
| WP10 | **front 용어집 메뉴 — 별칭 · 검수 표시(필요한 만큼만)** — `GlossaryModal` 이 새 응답 필드(`koAliases` · `aliases` · `reviewed`)를 읽어 §7.6 표대로: 한국어 칸 아래 ko 별칭 줄 · 고른 언어 칸 아래 별칭 줄 · `reviewed:false` 면 현지명 뒤 「검수 전」 꼬리표 · 칸 수 · 폭 · 부제(그 언어 `count`)는 그대로 · `lib/api.ts` 응답 타입. `loaded=false` 문구는 지우거나 둠(닿지 않음 · 계약 영향 없음). **그 밖 화면은 건드리지 않는다** | SPEC-001 0.4.0 §4.7 · §7.6 · §9.2 | frontend | WP9 의 §4.7 응답 모양(문서로 고정 — 코드 완료를 기다리지 않아도 된다 · 실 back 확인만 WP9 뒤) | `front/components/interpret/GlossaryModal.tsx` · `front/lib/api.ts` · `front/tests/**` | `tsc` · `lint` · `build` · `vitest`(메뉴 행 — 별칭 줄 · 꼬리표는 `reviewed:false` 에서만) 통과 · 클래스 대조 누락 0(꼬리표 클래스 포함) · 실 back(WP9 시드)으로 모달 스크린샷 3장(en · zh-Hant(「검수 전」 다수) · ja(「그 밖」 괄호 → 「검수 전」)) | `cd front && npx tsc --noEmit && npm run lint && npm run build && npx vitest run` · 클래스 대조 · 스크린샷 | 완료(2026-10-27 · 코드 PR #4 · vitest 30 · 클래스 197 누락 0 · 스크린샷은 목업 — 실 시드 화면은 WP11 폰) |
| WP11 | **재배포 · 폰 확인** — WP9 · WP10 머지 → main 이미지(Actions · sha) → infra `values-prod` 태그 + **ConfigMap · Secret 이름 목록에서 `GLOSSARY_MATRIX_URL` 삭제**(§9.5 · infra PR) → 머지 → ArgoCD sync → 배포 주소에서 ① `/api/health` 시드 `version` · `count` ② 폰 실발화: 대만어(zh-Hant)로 써마지FLX · 울쎄라 — TTS 가 현지명으로 읽음 · 대만어 자막 대만식 ③ 용어집 메뉴 별칭 · 「검수 전」 ④ 시드 PR 흐름 1회(사용자가 별칭 하나 고침 → 재배포 → 메뉴 반영 — OQ-012 · OQ-014 처리의 시작) | SPEC-001 0.4.0 §9.5 · §9.4 | 코디(진행) · infra · 사용자(폰) | WP9 · WP10 | infra 레포 `charts/interpret-pwa/` · `provisioning/secrets/interpret-pwa*.env.example` · `values-prod.yaml` | 배포 주소에서 ① ~ ③ · 사용자 폰 확인 · 레포 · 차트 비밀값 0 | `helm template … -f values-prod.yaml` · 배포 주소 확인 · 폰 | 재배포 완료(2026-10-27 · main 9befd18 · infra PR #28 · 코디 확인: health · login · manifest · wss ready · demo) · **폰 확인 진행 중**(사용자) |
| WP12 | **시작 오버레이 = 언어 단추 7개(D-34)** — 「탭해서 통역 시작」 대신 언어 단추 7개(§5.5 순서 · 목록 표시 이름 · 크게) · **누르는 것이 시작**(그 언어로 AudioContext 깨우기 · 마이크 · WS · `start{lang}`) · 마지막 언어는 표시만(자동 선택 · 자동 시작 없음) · 오버레이는 상담사 방향(바로 · 회전 상태 무관) · 헤더까지 덮음 그대로 · 백그라운드 복귀도 같은 오버레이 · 시작 뒤 언어 바꿈은 드롭다운 그대로 | SPEC-001 0.4.1 §7.3 #1 · §7.4 · §8 | designer(시안 `State-1-Start` D-34 판) · frontend | WP11 | 시안 `design/project/State-1-Start.dc.html` · `front/components/interpret/InterpretScreen.tsx` · `front/lib/**` · `front/tests/**` | `tsc` · `lint` · `build` · `vitest`(단추 7개 · 누르면 그 lang 으로 start · 마지막 언어 표시만 · 자동 시작 0) · 클래스 대조 누락 0 · 스크린샷(오버레이 · 뒤집힘 상태에서도 바로) · 재배포 뒤 폰 확인(iOS AudioContext 가 단추 누름으로 깨어남) | `cd front && npx tsc --noEmit && npm run lint && npm run build && npx vitest run` · 클래스 대조 · 스크린샷 | **진행 중**(2026-10-27 · designer · frontend) |

## 병렬

```text
WP1(back 뼈대 · 로그인 · 용어집) ──┬── WP2(back 통역 WS · 실물) ──┐
                                   │                              ├── WP4(front 통역) ── WP5 리뷰 ── WP6 수정 ── WP7 로컬 E2E ── WP8 배포(마지막)
WP3(front 뼈대 · 화면 · PWA) ──────┴──────────────────────────────┘

WP6 = WP6-BE(back 묶음 · 실물 ⑧ ~ ⑪) ∥ WP6-FE(시안 맞춤 · FAIL-1 · WARN-4) → WP7

(0.4.0) WP8 배포 ── WP-P 폰 피드백 1 ~ 3 ── WP9(back 시드 · 가져오기 · 실물 ⑫ ~ ⑯) ∥ WP10(front 메뉴 별칭 · 검수) ── WP11 재배포 · 폰
(0.4.1) WP11 ── WP12(D-34 시작 오버레이 — designer → frontend) ── 재배포 · 폰
```

- back 순서(한 워커): WP1 → WP2. front 순서(한 워커): WP3 → WP4.
- WP3 은 WP1 과 **동시에** 시작해도 된다 — 로그인 · 용어집 응답 모양은 SPEC-001 §3.3 · §4.6 으로 고정돼 있다. 실 back 확인(완료 조건)만 WP1 뒤.
- 로그인 응답 · 오류 본문 · WS 메시지 모양을 바꿔야 하면 SPEC-001 을 먼저 고친다(코디 → planner) → 양쪽 다시 맞춤.
- WP2 실물 확인(§9.3 ①)이 한도를 넘는 언어를 보이면 SPEC-001 §4.4 · OQ-002 를 사용자 결정으로 닫고 나서 WP4 로 간다. (2026-10-26 ① 통과 — 정방향만)
- **WP9 와 WP10 은 서로 기다리지 않는다** — 메뉴 응답 모양은 SPEC 0.4.0 §4.7 로 고정돼 있다(`term` 이름은 그대로 · 필드만 더함). 통역 WS 메시지 모양은 바뀌지 않는다. WP10 의 실 back 스크린샷만 WP9 뒤.
- WP9 의 첫 시드는 **가져오기 스크립트를 한 번 돌린 결과**를 그대로 커밋한다 — 워커가 시드 값을 손으로 고치지 않는다(현지명 · 별칭 검수는 사용자 · OQ-012 · OQ-014). WP9 실물 ⑬ 이 한도 기본값을 바꾸면 코디가 planner 에게 넘겨 SPEC §2.4 · §4.6 에 적는다.
- WP6-BE 와 WP6-FE 는 서로 기다리지 않는다 — WS 메시지 모양은 0.3.0 에서도 그대로다(TTS 입력 · context 는 back 안쪽). WP6-BE 실측(⑧)이 정한 기본값은 코디가 planner 에게 넘겨 SPEC §2.4 · §4.4 에 적는다.

## 주의

- public 레포(문서) · private 레포(코드)지만 둘 다 키 · 로그인 아이디 · 비밀번호 · 세션 비밀값 · 실명을 코드 · 시험 데이터 · 커밋 · 보고에 넣지 않는다. 시험의 Soniox · Procedure Hub 응답은 모양만 맞춘 가짜 값.
- Soniox TTS 동시 한도가 있다(원형 주석 「3」) — 실물 스크립트도 세션마다 두 연결을 닫는다.
- 휴대폰 마이크는 HTTPS 에서만 된다 — 로컬 E2E(WP7)는 맥 브라우저 기준, 기기 확인은 WP8(SPEC-001 OQ-007).
- 백엔드 커밋 뒤 compose 를 다시 올리고 E2E(옛 코드가 떠 있는 채로 확인 금지).
- 완료 = 사용자가 **실제로 통역해 본 것**(WP7 · WP8 기기). 웹 빌드 통과로 완료 처리하지 않는다.

## 열린 것

SPEC-001 §10 이 정본이다. 이 작업 순서에 닿는 것만:

| ID | 닿는 WP | 언제 닫나 |
|---|---|---|
| ~~OQ-002~~ | — | 닫음 — 시드 실측 20,251(SPEC 0.4.1 §4.6 · WP9 ⑬ · ja 22,502 × 0.9) |
| ~~OQ-003 · OQ-009~~ | — | 닫음 — D-18 · D-19 |
| ~~OQ-004 · OQ-010 · OQ-011~~ | — | 닫음(0.4.0) — D-28 · D-31 · D-26 |
| OQ-006 | — | PoC 범위(원어민 검수 없음) |
| OQ-001 · OQ-005 · OQ-007 | WP11 · WP12 | 사용자 폰 확인으로 닫는다(OQ-005 의 시작 조작은 D-34 로 정해짐 · 원 = 멈춤만 남음) |
| OQ-013 | — | 배포됨(zh-Hant entry · ⑬ zh 와 22짝 다름) — 사용자 확인 |
| OQ-014 | — | 1건 처리(써마지FLX `ko_aliases` 「써마지」) · 더 필요한 호칭은 사용자 시드 PR |
| **OQ-012 · OQ-015 — 시드 PR 숙제(사용자)** | WP 밖 · 고치면 재배포(SPEC §9.5) | ① **zh-Hant 현지명**(美國音波 · 鳳凰電波 등 — 지금 157개 전부 zh 의 s2twp 초안 `reviewed:false`) ② **구어 별칭 美版/韩版** — 「超声刀」 · 「热玛吉」 단독을 울쎄라 ↔ 슈링크유니버스 · 써마지FLX ↔ 올리지오 중 어디에 둘지(⑮ 역방향 오답 원인) ③ 「그 밖」 괄호 60개 검수. 워커는 값을 짓지 않는다 |
