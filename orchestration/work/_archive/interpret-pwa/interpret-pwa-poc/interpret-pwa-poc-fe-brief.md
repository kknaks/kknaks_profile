# [frontend] interpret-pwa WORK-001 WP3 → WP4 — front 뼈대 · 화면 · PWA → 통역
# [frontend] <한 줄 제목>

너는 **interpret-pwa `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ backend 워커가 같은 워크트리의 `back/` 에서 병렬 작업 중 — `back/` 와 루트 `docker-compose.yml` · `.env.example` 는 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` ← **계약의 SoT.** 여기 없는 건 발명하지 마라. 비면 질문 채널로
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` ← WP 표 · 순서 · 완료 조건 · 주의
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` ← 결정(D-01~D-17)
- 통역 원형(read-only · **복사**, import 금지): 레포 `/Users/kknaks/git/toy_pr2/cc-prototype` 의 **`origin/main`** — canonical 체크아웃은 낡았을 수 있으니 `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<경로>` 로 읽어라. checkout · pull 금지

**기대는 개념**

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/areas/concept/back/websocket-relay.md` — 통역 중계(STT · TTS 두 WS)
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/areas/concept/front/half-duplex-echo-suppression.md` — 반이중
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/areas/concept/design/design-system.md` — medikit 클래스는 실재 대조(빌드 CSS 전수)

## 2. 배경 / 무엇을 바꾸나

빈 레포에 PWA front 를 세운다. WP3(뼈대 · 로그인 · 통역 화면 배치 · 용어집 패널 · PWA · 원 상태 가짜 렌더)을 끝내면 **이어서** WP4(원형 `lib/interpret.ts` 복사 · WS · 자막 배치 · 원 상태 · 음량 반응 · 반이중)로 간다. 사용자가 「코드까지 1차로 다 짜서 로컬 E2E」를 원한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

SPEC-001 §3.3(로그인) · §4.6(용어집 API) · §5.2~§5.4(통역 WS) 의 모양 그대로 소비한다. back 이 아직 없으면 그 모양으로 목업해 두고, back 이 뜨면(WP1 · WP2) 실 back 으로 확인한다. 모양이 안 맞으면 `[질문]`.

## 4. 먼저 읽을 핵심 파일

- 원형 medikit 연결: `procedure/front/package.json` · `procedure/front/tailwind.config.ts` · `procedure/front/app/globals.css` · `procedure/front/app/styles/medikit-patches.css` · `procedure/front/app/layout.tsx` (모두 `origin/main`)
- 원형 브라우저 오디오: `_archive/cc/front/lib/interpret.ts` (`origin/main`)
- medikit 컴포넌트 · 토큰: `_archive/cc/design/_ds/medikit-*/README.md` (`origin/main`)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `front/`

## 6. 구현 단계

1. **WP3** — WORK-001 WP3 행 그대로. 실 back 확인 · 스크린샷은 back WP1 이 떠 있을 때(없으면 목업으로 하고 pending)
2. WP3 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp3-fe-report.md` → **§9 (2) 직접 주입으로만** 중간 보고 한 줄(「WP3 끝, WP4 진행」)
3. **WP4** — WORK-001 WP4 행 그대로. 실발화 1회는 키가 있고 back WP2 가 떠 있을 때만(없으면 pending)
4. WP4 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp4-fe-report.md` → §9 두 채널 완료 보고

## 7. 범위 제약 — 하지 말 것

- 키 · 로그인 아이디 · 비밀번호 · 세션 비밀값을 코드 · 시험 · 리포트 · 로그에 쓰지 마라. 시험의 외부 응답은 모양만 맞춘 가짜
- 사용자 포트(3600 · 8600 · 3700 · 8700)의 프로세스를 건드리지 마라. 이 레포는 8800 · 3800 만. 띄운 프로세스는 끝나면 네가 내린다
- 커밋 · push · PR 금지
- 실물 호출에 키가 필요한데 레포 루트 `.env` 에 값이 없으면 **우회하지 말고 pending** 으로 보고(코드는 다 짜 둔다)
- `back/` · 루트 compose · env 예시 수정 금지. 원형 레포 수정 금지

## 8. 검증

```
front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 사용자 포트·프로세스를 건드리지 않는다. 실기기(마이크 · PWA 설치) 확인은 pending 으로 보고
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
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
