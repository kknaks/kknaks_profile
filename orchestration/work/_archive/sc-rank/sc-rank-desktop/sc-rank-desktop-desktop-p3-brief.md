
# [desktop] WORK-001 P3 브라우저 수집 (CDP) + smoke

너는 **sc-rank `desktop` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/roles/sc-rank/desktop/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. **이번 판은 P3 만** 한다(화면 연결 P4 는 다음 판). P1·P2 는 끝나 있다 — 앞 판 리포트를 먼저 읽어라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/20-spec/spec-001-desktop-app.md` (v0.2.0) — §2.2 명령 실패 · **§3 브라우저** · §4 수집 행 · §6 A-4·A-5
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/30-work/work-001-desktop-port.md` — P3 행
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p1-p2.md` — **앞 판 리포트(네가 썼을 수도, 아닐 수도 있다)**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/review-doc-report.md` F-1 — 수집 쪽 PoC 줄 번호별 값

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

P2 까지 순수 로직이 섰다. 이번 판은 PoC 의 Playwright 수집(`place.mjs` `collectPlaceList` · `blog-browser.mjs` `blogBatches`)과
썸네일 다운로드(`blog.mjs` `curl`)를 CDP + reqwest 로 옮기고, 명령 `check_place`·`check_blog` 를 실제로 동작시킨다.
**WORK-001 에서 가장 위험한 판이다.**

## 3. 계약

- SPEC §3 전부: Edge→Chrome · 헤드리스 · 임시 프로필 `sc-rank-cdp-*` · 앱당 1개 공유·재사용·끊기면 재기동 · 조회마다 격리 컨텍스트 · `ko-KR` 1400×900 · UA(실제 UA 에서 `HeadlessChrome`→`Chrome`) · 종료 정리 + 다음 기동 때 잔여 정리 · CDP 는 `127.0.0.1` 또는 파이프.
- SPEC §2.2: 블로그·플레이스 공유 잠금, 끝난 시점부터 0.7초/2초, 문구 `index.mjs` 그대로. `check_place` 입력 검증은 잠금 앞.
- SPEC §4: 수집 함수 본문 전체, 페이지 안 JS(`place-dom.mjs` · `place.mjs:74-80`·`:94-99` · `blog-browser.mjs:25`·`:35-42`)는 **문자열 그대로 주입**.
- 로그: PoC `[place]`·`[blog]` 단계 로그를 같은 필드로(`log` 크레이트 → 앱은 파일, smoke 는 stdout).
- `examples/smoke.rs`: `place <키워드> <타겟>` · `blog <키워드> keyword <타겟>` · `blog <키워드> image <파일>` — 요약 JSON 출력, `status=="error"` 면 exit 1, 끝나면 브라우저 정리.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/place.mjs:36-109` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/place-dom.mjs` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/blog-browser.mjs` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/blog.mjs:52-58·80-113` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/index.mjs` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/scripts/smoke.mjs` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/smoke-result.txt`(PoC 실측 로그 모양)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `reference/2026-09-09-sc-prototype/desktop/`
- 리포트 파일 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p3.md`

## 6. 구현 단계

1. **스파이크 먼저**: CDP 로 지도 페이지를 열고 `searchIframe` 의 실행 맥락에서 `#_pcmap_list_scroll_container` 를 읽을 수 있는지, 블로그에서 `s.search.naver.com/p/review/` 응답 본문을 받을 수 있는지 확인한다. **막히면 우회로(직접 iframe URL 로 이동, 다른 수집 방식 등)를 만들지 말고 즉시 `[질문]` 으로 보고**한다 — 대안은 사용자 결정이다(DEC-001 Option C).
2. 브라우저 관리(§3) · 플레이스 수집 · 블로그 배치 · 썸네일 다운로드(reqwest rustls, 8초·6MB·비 2xx 실패·PoC UA) · 동시 8.
3. 명령 `check_place`·`check_blog` 연결 + 잠금·간격. 오류 문구 규칙(P2 의 `ScrapeError`).
4. `examples/smoke.rs`.
5. 실수집 — **각 1회만**, 사이에 2초 이상:
   - `cargo run --example smoke -- place 강남역성형외과 무이성형외과`
   - `cargo run --example smoke -- blog 구월동레이저제모 keyword 썸블리의원`
   - `cargo run --example smoke -- blog 구월동피부과 image tests/fixtures/1.png`
   `not_found` 는 실패가 아니다(순위는 고정값이 아님). `error` 면 원인을 로그로 보고.
6. smoke 후 `pgrep -f sc-rank-cdp-` 가 비고 임시 프로필이 없는지 확인(A-8 의 예제 쪽 확인).
7. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p3.md` 에 — SPEC §3 표·§4 수집 행마다 같음/다름, smoke 출력 원문.

## 7. 범위 제약 — 하지 말 것

- 화면(`src/`) 수정(P4) 금지.
- Chromium 다운로드·동봉 금지. 사용자 브라우저 프로필·실행 중 브라우저를 건드리지 마라.
- 실수집 반복 금지(위 3회 + 실패 원인 확인용 재시도 최대 1회씩).
- 판정·문구·타임아웃 「개선」 금지. 커밋·push·PR 금지.

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
