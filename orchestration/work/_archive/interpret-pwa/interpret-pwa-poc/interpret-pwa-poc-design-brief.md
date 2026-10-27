# [designer] interpret-pwa 시안 — Claude Design 전용 프로젝트 새로 · 로그인 · 통역 화면(상태 전부)

너는 **interpret-pwa `designer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/designer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리의 `front/` · `back/` · `.env` 는 건드리지 마라(`.env` 에 사용자 실키 — 열지 마라). 네 자리는 레포 루트 `design/` 뿐.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **§6 · §7 · §8** ← 화면 · 상태 · 문구의 정본(0.2.0)
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-07 ~ D-10 · D-16 ← 화면 결정
- **스타일 기준(읽기만)**: Claude Design 프로젝트 `dda9a931-097f-4780-9301-972d5ac1fc23`(ccc) 의 「Ceramique 의사 모바일」 — 스타일 · 컴포넌트 · 색. 로컬 사본: `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:_archive/cc/design/README.md` (+ 같은 폴더 `_ds/medikit-*/` · `.dc.html`) — medikit · `data-product="ceramique"` · `ceramique-theme.css` · `medikit-patches.css`
- 테마 원본: `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/front/app/styles/ceramique-theme.css`
- 지금 구현 화면(참고 — 디자인이 빠져 있다는 사용자 지적을 받은 상태): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp3-fe-shots/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp4-fe-shots/`

## 2. 배경 / 무엇을 바꾸나

1차 구현 화면에 디자인이 하나도 안 들어갔다(사용자: 「디자인이 하나도 안들어갓잖아」). 사용자는 **Claude Design 에 이 PWA 전용 프로젝트를 따로 만들고, 거기서 직접 고치겠다**고 했다.
네 일은 그 출발점 시안을 만드는 것 — ccc 세라믹 스타일 그대로, SPEC §7 의 화면 · 상태를 전부 담는다. 확정되면 시안이 화면 정본이 되고 frontend 가 맞춘다.

사용자 피드백(반영할 것):
- 색은 **세라믹 ccc 테마와 같은 색**(primary `#2498bd` 청록 계열). medikit 기본 파랑 아님
- 외국어 영역의 화면 전환 아이콘은 **화면을 돌리는 회전 화살표 아이콘**(지금의 ⇅ 아님)

## 3. 계약

해당 없음(시안이 확정된 뒤 SPEC 화면 절을 시안에 맞춘다).

## 4. 먼저 읽을 핵심 파일

- 위 §1 의 ccc 시안 사본 README · 「Ceramique 의사 모바일」 `.dc.html`

## 5. allowed_paths — 이 밖은 건드리지 마라

- Claude Design: **새 프로젝트 「Interpret PWA」**(이름 그대로) — 여기에만 쓴다. ccc 프로젝트는 읽기만
- 코드 레포 `design/` — 프로젝트 로컬 사본 + `README.md`(프로젝트 id · 테마 연결법 · 화면 목록)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/design-report.md`

## 6. 구현 단계

모바일 390px 기준(태블릿에서 깨지지 않게). 한 화면 = 한 파일(또는 한 프레임) — 사용자가 하나씩 고칠 수 있게.

1. **로그인** — 기본 · 오류(「아이디 또는 비밀번호가 맞지 않아요」) · 잠금(429 문구)
2. **통역 화면** — SPEC §7.2 배치(헤더 햄버거 · 외국어 영역[드롭다운 · 회전 아이콘 · 자막] · 가운데 원 · 한국어 영역[자막]). 외국어 영역 **뒤집힘(기본) · 바로 보기** 두 벌
3. **가운데 원 상태 8개**(SPEC §7.3 표 #1~#8) — 시작 전 오버레이 · 오류 · 연결 중 · 〈언어〉로 출력 중 · 멈춤 · 한국어 듣는 중 · 외국어 듣는 중 · 대기. 각 상태의 원 색 · 안내 문구 · 외국어 영역 문구. 한국어 = 테마 primary, 외국어 = 대비되는 색(테마 안에서 고르고 리포트에 근거)
4. **자막 배치**(SPEC §7.5 · D-16) — 대화가 몇 줄 쌓인 상태 한 장
5. **햄버거 메뉴**(로그아웃 · 용어집) · **용어집 모달**(카테고리 · 한국어 · 고른 언어 표, 158행 중 몇 줄 가짜 아닌 실제 용어 예 가능 — 용어집은 공개 데이터)
6. `design/` 사본 + README · 리포트(프로젝트 id · URL · 화면 목록 · SPEC §7 대조 · 제안)

## 7. 범위 제약 — 하지 말 것

- 코드 수정 금지 · ccc 프로젝트 수정 금지 · 새 디자인 언어 금지
- 사람 이름 · 키 · 계정값을 시안에 넣지 않는다

## 8. 검증

```
Claude Design 프로젝트에 브리프의 화면 목록이 전부 있다(화면별 이름 표) · 로컬 design/ 사본이 프로젝트와 같다 · medikit + ceramique 테마 토큰만 쓴다 · 가짜 값만(실명·키 0) · 기존 ccc 프로젝트는 읽기만
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
  --subject "designer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 \
  --text "[worker_done] designer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --text "[질문] designer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
