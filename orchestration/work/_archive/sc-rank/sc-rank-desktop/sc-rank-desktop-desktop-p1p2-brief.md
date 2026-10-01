
# [desktop] WORK-001 P1 뼈대 + P2 순수 로직·테스트 이식

너는 **sc-rank `desktop` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/roles/sc-rank/desktop/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. **이번 판은 P1·P2 만** 한다(P3 브라우저 수집은 다음 판).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/20-spec/spec-001-desktop-app.md` (v0.2.0) ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/30-work/work-001-desktop-port.md` ← Phase 표. 이번은 P1·P2
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/10-decision/decision-001-desktop-app.md` ← 결정 14건
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/review-doc-report.md` ← 문서 검수. **F-1·W-5 에 PoC 줄 번호별 옮길 값 목록**이 있다
- PoC(동작 정본, read-only): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/src/` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/tests/` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/index.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/1.png`

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

웹 PoC(Express + React)를 서버 없는 Tauri 2 + Rust 앱으로 옮긴다. 이번 판은 앱 뼈대와,
네트워크·브라우저 없이 검증할 수 있는 순수 로직을 PoC 와 **같은 단언**으로 세운다.

## 3. 계약

SPEC-001 §1(앱 경계) · §2(명령 모양 — 이번 판은 빈 구현/`todo` 가 아니라 **컴파일되는 시그니처 + 미구현 오류 반환**) ·
§4(옮기는 방식·오류 문구 규칙) · §6 A-1·A-2·A-3·A-7.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/place.mjs:1-45` — `extractPlaceName`·`parsePlaceList`·`PLACE_SCOPE`
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/blog.mjs` 전부 — `parseBlogList`·`matchBlogKeyword`·`imageHash`·`hashDistance`·`decodeTargetImage`·`imageUrl`·`mapConcurrent`·검증 문구
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/workbook.mjs` 전부
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/tests/place.test.mjs` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/tests/blog.test.mjs` — 옮길 단언 12개
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/src/main.jsx` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/index.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/vite.config.js` — 화면 사본 대상

## 5. allowed_paths — 이 밖은 건드리지 마라

- `reference/2026-09-09-sc-prototype/desktop/`
- 리포트 파일 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p1-p2.md` (코디 워크트리 — 이 파일만 쓴다)

## 6. 구현 단계

**P1 뼈대**
1. `desktop/` 에 Tauri 2 + React + Vite 앱. PoC `index.html`(무변경)·`src/` 사본. `vite` dev 포트 13100 strictPort, 프록시 없음.
2. `tauri.conf.json`: productName `SC Rank` · identifier `com.summerstar.scrank` · 창 제목 `SC Rank` · `bundle.targets=["nsis"]`.
3. 명령 셋(`check_blog`·`check_place`·`export_xlsx`) 등록 — 평평한 인자, camelCase, `Option`→`null`(SPEC §2.1). 이번 판 본문은 미구현 오류.
4. `tauri-plugin-log`(파일) · `tauri-plugin-dialog` · `tauri-plugin-opener` 등록만.
5. 화면(`main.jsx`)은 **이번 판에 고치지 않는다** — P4 몫. `npm run tauri dev` 로 PoC 화면이 뜨는지만 본다.

**P2 순수 로직**
6. 플레이스 판정(`extractPlaceName`·`parsePlaceList`·`PLACE_SCOPE`), 블로그 파싱·키워드 일치(`scraper`), 이미지 해시(SPEC §4 전처리 순서 그대로), 목표 이미지 디코드·검증, 썸네일 URL 검사, 제한 동시 실행, 엑셀(`rust_xlsxwriter`, SPEC §4 엑셀 행 전부), 오류 문구 규칙(한글 도메인 오류 vs 폴백), 브라우저 탐색 함수(후보 경로 목록 인자 · 없으면 SPEC §3 문구).
7. 테스트: `place.test.mjs` 9개 · `blog.test.mjs` 3개를 같은 단언으로(A-1), 엑셀 열·타입(A-2), 빈 후보 탐색(A-7). 픽스처 `1.png` 는 `desktop/src-tauri/tests/fixtures/` 로 복사, 변형은 `image` 크레이트.
8. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p1-p2.md` 에 역할 `rules.md` 형식으로 — SPEC §4 표의 P2 해당 행마다 「같음/다름」.

## 7. 범위 제약 — 하지 말 것

- 브라우저 기동·CDP·네이버 요청(P3) · 화면 연결(P4) 하지 마라.
- PoC 파일을 고치지 마라(복사해서 쓴다). 판정·문구·제한값을 「개선」하지 마라.
- 테스트 단언을 약하게 옮기지 마라. 옮기기 어려운 단언은 그대로 두고 이유를 보고.
- 커밋·push·PR 금지.

## 8. 검증

```
desktop/src-tauri 에서 cargo test · cargo clippy --all-targets -- -D warnings, desktop 에서 npm run build. Phase 범위에 맞게 1회씩 — 통과하면 반복하지 마라. 실수집(네이버 요청)은 Phase 끝에 1회만, 요청 간격 규칙을 지킨다. 사용자 포트·프로세스·브라우저 프로필을 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
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
  --to term_7f81f426-1d1d-4036-983d-a48b8b469147 --from term_95308b9e-d8ad-46e1-ae6b-f40a81d9ae20 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "desktop 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_7f81f426-1d1d-4036-983d-a48b8b469147 \
  --text "[worker_done] desktop 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_7f81f426-1d1d-4036-983d-a48b8b469147 --text "[질문] desktop: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
