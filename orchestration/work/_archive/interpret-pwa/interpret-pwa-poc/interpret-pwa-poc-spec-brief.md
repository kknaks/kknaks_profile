
# [planner] interpret-pwa SPEC-001 · WORK-001 — 통역 PWA 계약과 구현 순서

너는 **interpret-pwa `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 코디네이터 세션이 같이 쓴다 — allowed_paths 밖 파일을 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` ← **결정의 SoT(accepted).** D-01~D-17. 여기 없는 정책은 발명하지 마라.
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md` ← 사용자 원문 · 확인한 사실(용어집 API · Soniox 설정 · ccc 통역 구조)
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/README.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/README.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/README.md` ← 인덱스(갱신 대상)
- Soniox 공식 문서 `https://soniox.com/docs/llms.txt` 에서 필요한 페이지(실시간 번역 · context · TTS) — 다른 자료와 다르면 **공식 문서가 맞다**
- 용어집 실물: `GET https://stg-procedure-hub.medisolveai.com/api/v1/glossary/matrix` (인증 없음 — 직접 호출해 shape 를 확인해도 된다)

**기대는 개념** — 이 작업이 따를 판단 기준.

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/areas/concept/back/websocket-relay.md` — 통역은 back 이 두 WS(STT · TTS)를 중계한다. 그 계약 모양을 이대로
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/areas/concept/front/half-duplex-echo-suppression.md` — TTS 재생 중 마이크를 멈추는 반이중. 원 상태(D-09)의 「출력 중」이 이 구간이다
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/areas/concept/ai/nondeterministic-stt-output.md` — 발화 확정 · 자막 갱신 규칙을 정할 때
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/areas/concept/design/design-system.md` — medikit 토큰 이름은 실재를 대조한다(없는 클래스는 조용히 무시된다)

## 2. 배경 / 무엇을 바꾸나

빈 레포 `kknaksss/interpret-pwa`(루트에 `front/` · `back/` 빈 폴더)에 실시간 통역 PWA 를 세운다. ccc(cc-prototype)의
통역을 떼어 오되, 피부과 시술 용어 직역을 막으려고 Procedure Hub 용어집을 Soniox `context` 로 넣는다(DEC-001).
이번 작업은 **문서만** — SPEC-001(계약)과 WORK-001(구현 순서 · WP)을 쓴다. 코드는 그다음 발주다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 이번 산출물(SPEC-001)이 BE↔FE 계약을 **정한다.** 단, 통역 WS 는 원형(§4)의 계약 모양을 기본으로 하고,
바꾸는 자리는 바꾸는 이유(DEC 근거)를 적는다.

## 4. 먼저 읽을 핵심 파일 (read-only)

통역 원형 — 레포 `/Users/kknaks/git/toy_pr2/cc-prototype` 의 **`origin/main`** (canonical 체크아웃은 낡았을 수 있으니 `git -C <레포> show origin/main:<경로>` 로 읽어라. checkout · pull 금지):

- `procedure/back/app/api/interpret.py` — `WS /api/interpret` 입구 · 메시지 종류
- `procedure/back/app/service/interpret/session.py` · `soniox.py` · `assembler.py` · `chinese.py` — Soniox 연결 · 발화 묶기 · 번체 처리
- `procedure/back/app/config.py` · `procedure/back/tests/test_interpret.py` — env · 시험
- `procedure/front/app/globals.css` · `procedure/front/app/styles/medikit-patches.css` · `procedure/front/tailwind.config.ts` — medikit 을 Next.js 에 붙인 방식
- `_archive/cc/design/_ds/medikit-*/README.md` — medikit 컴포넌트 · 토큰
- 원형 통역 계약 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/_archive/cc-prototype/sts-prototype/interpret-ws-contract.md`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/interpret-pwa/20-spec/`
- `para/projects/summer-star/interpret-pwa/30-work/`

## 6. 구현 단계

1. **SPEC-001** `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` — frontmatter(type spec · id SPEC-001 · version 0.1.0 · status draft · links.decisions DEC-001). 절은 최소 아래를 덮는다. 각 절 머리에 근거 D-번호:
   - **구성 · 실행**: `front/`(Next.js PWA) · `back/`(FastAPI uv) · 레포 루트 `docker-compose.yml` · 포트(기존 로컬 앱과 겹치지 않게 제안 — cc-prototype 은 8600/3600) · env 목록(이름만 — `SONIOX_API_KEY` · 로그인 아이디 · 비밀번호 · 용어집 URL · CORS 등). **값은 적지 않는다**(D-06 · D-11)
   - **로그인**(D-06): 단일 계정 env 대조 · 세션/토큰 방식 · 보호 대상(통역 WS 포함) · 로그아웃 · 실패 응답
   - **용어집**(D-05 · D-13 · D-14): 기동 때 matrix 를 읽어 캐시 · 실패 시 동작 · 언어별 `context` 조립 규칙(`terms` · `translation_terms` · `general`) · 8,000토큰 한도를 넘을 때 줄이는 규칙 · 용어집 메뉴가 쓰는 API(읽기 전용)
   - **통역 WS**(D-03 · D-04): 원형 계약을 기준으로 메시지 종류 · 필드 · 오류 코드 · 언어 코드 매핑(용어집 `langs` 6개 ↔ Soniox 언어 코드). ⚠ `yue`(광둥어)를 Soniox 가 별도 코드로 받는지 · `zh` 로 잡히는지는 원형 기록과 공식 문서로 확인하고, 문서로 확정 못 하면 **열린 것**으로 남겨라
   - **중국어 번체**(D-17): Soniox 는 간체만 낸다 → 원형 `chinese.py`(OpenCC `s2tw`) 방식으로 화면 자막만 번체 · TTS 는 간체. 어느 언어 선택이 번체 자막인지(최소 `yue` — 용어집 `yue` 표기가 번체다), 용어집 번체 표기를 `translation_terms` 에 넣을 때 간체로 바꿔 넣을지를 정한다
   - **화면**(D-07 · D-08 · D-09 · D-10 · D-16): 로그인 · 통역 화면의 영역 배치(와이어 텍스트) · 외국어 영역 180° 뒤집힘과 화면 전환 아이콘 · 가운데 원 상태표(대기 · 외국어 듣는 중 · 한국어 듣는 중 · 〈언어〉로 출력 중 — 색 · 음량 반응 · 안내 문구) · 자막 배치 · 햄버거(로그아웃 · 용어집)
   - **PWA**: manifest · 홈 화면 추가 · HTTPS 조건(로컬은 localhost) · 화면 꺼짐 방지 · 끊김 시 재연결
   - **실물 확인 항목**: 완료 조건이 될 실물 호출(Soniox 에 용어집 context 를 넣은 연결 1회 — 한도 안인지 · 시술명 번역이 용어집대로 나오는지)
   - **열린 것**: 근거로 닫을 수 없는 것 전부
2. **WORK-001** `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` — WP 표(담당 워커 · SPEC 절 · 선행 · 검증). 순서는 DEC D-12: back 뼈대·로그인·용어집 → 통역 WS(실물 호출) ↔ front 뼈대·화면(분담 병렬 가능) → 로컬 E2E(사용자) → 배포(infra, 마지막). WP 마다 검증은 관련 시험만, 전체는 마지막에 한 번
3. 인덱스 갱신: `20-spec/README.md` · `30-work/README.md`. (제품 `README.md` · `log.md` 는 코디가 갱신한다 — 건드리지 마라)

## 7. 범위 제약 — 하지 말 것

- 코드 작성 · 코드 레포 수정 금지(원형은 read-only)
- DEC 를 고치지 마라. DEC 와 다르게 가야 할 이유가 보이면 **열린 것**에 적고 보고에 올린다
- 이 레포는 public — Soniox 키 · 계정 비밀번호 · 실명을 문서에 넣지 않는다(로그인 아이디도 「env 값」으로만)
- 범위 밖(DEC Scope Out): 통역 기록 저장 · 여러 계정 · 자동 언어 맞추기 · ccc 변경

## 8. 검증

```
SPEC 의 모든 절이 DEC · 확정 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 계정값 · 실명 0(grep)
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
