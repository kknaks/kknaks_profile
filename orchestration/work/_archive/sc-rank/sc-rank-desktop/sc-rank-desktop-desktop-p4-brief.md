
# [desktop] WORK-001 P4 화면 연결 + P5 Windows 빌드 절차

너는 **sc-rank `desktop` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/roles/sc-rank/desktop/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. **이번 판은 P4·P5** 다. P1~P3 는 끝나 있다 — 앞 판 리포트 둘을 먼저 읽어라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/20-spec/spec-001-desktop-app.md` (v0.2.0) — **§5 화면 변경 셋** · §2 명령 모양 · §1 로그·배포물 · §6 A-6·A-8
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/30-work/work-001-desktop-port.md` — P4·P5 행
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p1-p2.md` · `report-desktop-p3.md` — 앞 판 리포트

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

수집·판정·엑셀은 Rust 명령으로 섰다(P3). 코디 대조 결과 플레이스 smoke 가 PoC 와 같은 시각 **완전히 같았다**
(rank 69 · organicRank 53 · total 88 · totalAds 18) — P3 리포트의 「광고 0건」은 그 시점 네이버 편성으로 판정했다. 추가 조치 없음.
이번 판은 화면을 명령에 잇고(P4), Windows 에서 사용자가 빌드·설치할 절차를 남긴다(P5).

## 3. 계약

- SPEC §5 **셋만**: (1) `desktop/src/bridge.js` — `invoke` reject 문자열 → `Error`, 조회 180초 `Promise.race`(문구 `main.jsx:66`), `check_place` Err 는 오류 행 (2) 저장 대화상자 — 기본 파일명 한국 날짜, `.xlsx` 필터, 취소 무메시지, 모든 실패는 `main.jsx:77` 문구 (3) 진입부에서 `a[target=_blank]` 클릭 가로채기 → `tauri-plugin-opener`. `main.jsx` 의 `<a>` 는 그대로.
- `main.jsx` 에서 바뀌는 줄은 `fetch` 호출부·다운로드부뿐이어야 한다. 그 밖의 줄 diff 0.
- 미구현 Err 문구 「아직 구현되지 않은 기능입니다.」가 코드에 남지 않는다.
- P5: `desktop/README.md` — macOS 개발(설치·dev·test·smoke) · **Windows 빌드**(사전 요건: Rust MSVC·VS Build Tools·Node·WebView2 — 버전 명시, 명령, NSIS 산출물 경로) · 설치 후 첫 실행 SmartScreen 안내 · Edge 원격 디버깅 정책(`RemoteDebuggingAllowed`)으로 막힐 수 있음 · 로그 파일 위치(OS별).

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/desktop/src/main.jsx:55-82` — 호출·저장 · `:115` 링크
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/desktop/src-tauri/src/commands.rs` · `lib.rs`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `reference/2026-09-09-sc-prototype/desktop/`
- 리포트 파일 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p4-p5.md`

## 6. 구현 단계

1. P4 셋 구현.
2. 앱 확인 1회(`npm run tauri dev`, 13100 비었는지 먼저): 플레이스 키워드 1개 조회 → 저장 대화상자로 저장 → 파일 경로·calamine 등으로 읽은 머리행을 리포트에. 저장 대화상자·링크 열기는 가능한 범위에서 확인하고 못 한 것은 pending 으로. 네이버 요청은 이 1건만.
3. 앱 창을 닫은 뒤 `pgrep -f sc-rank-cdp-` 없음 · 임시 프로필 없음(A-8 앱 쪽).
4. P5 README. `cargo check --target x86_64-pc-windows-msvc` 를 시도하고 안 되면 사유 보고(타깃 추가 `rustup target add` 는 해도 된다).
5. verify(test·clippy·build) 1회 → 리포트.

## 7. 범위 제약 — 하지 말 것

- §5 셋 밖의 화면 변경 금지(문구·스타일·기본 키워드 포함).
- 네이버 요청은 6-2 의 1건만. 띄운 프로세스는 네 것만 끈다. macOS 권한 대화상자는 누르지 않는다.
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
