# [reviewer] interpret-pwa WORK-001 WP5 — back · front 코드 검수(SPEC-001 대조)
# [reviewer] <한 줄 제목>

너는 **interpret-pwa `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

read-only. 코드 · 설정 · `.env` 를 고치지 마라. `.env` 에는 사용자 실키가 있다 — **열지도 출력하지도 마라.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` (0.2.0) ← 계약의 SoT
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` ← WP5 행(리뷰 항목 목록) · 주의
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` ← D-01~D-17
- 워커 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp1-be-report.md` · `wp2-be-report.md` · `wp3-fe-report.md` · `wp4-fe-report.md`

## 2. 배경 / 무엇을 바꾸나

backend(WP1 · WP2) · frontend(WP3 · WP4) 1루프가 끝났다. 사용자 로컬 E2E 전에 SPEC 대조로 계약 위반 · 조용히 통과하는 자리를 잡는다.

## 3. 계약

SPEC-001 §3 · §4.6 · §5(BE↔FE). 양쪽 코드가 같은 모양인지 직접 대조한다.

## 4. 먼저 읽을 핵심 파일

- 범위: 워크트리 전체 `git status` · `git diff origin/main` + untracked(`back/` · `front/` · `docker-compose.yml` · `.env.example`). `node_modules` · `.next` · `.venv` 제외

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/review-code-report.md`

## 6. 구현 단계

1. WORK-001 WP5 행의 항목을 전수로: 로그인 같은 401 · 잠금 · 토큰 검증 · 용어집 실패 동작 · context 조립 · 줄이기 순서 · `yue` 매핑 · 번체 자막 / TTS 간체 · WS accept 전 인증 · Soniox 두 연결 정리 · 영역 배치 D-16 · 반이중 · §7.3 상태 판정 순서(멈춤 중 출력) · 비밀값 · 「조용히 통과하는 자리」(용어집 없이 몰래 연결 · 없는 medikit 클래스 · 빈 단언) · OQ-006(외국어 문구 6×7 — 명백한 오역 · 빈칸만)
2. BE↔FE 대조: 메시지 이름 · 필드 · 오류 코드 · 토큰 전달(`?token=`) · Origin · 401/429 응답 모양
3. compose 로 둘이 같이 뜨는 구성인지(포트 8800 · 3800 · `NEXT_PUBLIC_API_BASE_URL` build arg · env_file) — 읽기로만
4. 「사용자가 실물에서 만날 자리」를 따로 모은다

## 7. 범위 제약 — 하지 말 것

- 수정 · 시험 실행 · 서버 기동 금지(결과가 필요하면 워커 리포트 인용). `.env` 열람 금지
- 취향 지적 금지 · 커밋 금지

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
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
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
