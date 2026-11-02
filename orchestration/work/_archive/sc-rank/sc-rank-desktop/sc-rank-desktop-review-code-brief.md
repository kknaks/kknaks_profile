
# [reviewer] SC Rank desktop/ 코드 검수 — WORK-001 P1~P5 (read-only)

너는 **sc-rank `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/roles/sc-rank/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리는 desktop 워커의 작업 트리다(워커는 끝나 있다). **아무것도 고치지 마라.** 테스트도 돌리지 않는다 — 수치는 워커 리포트를 인용한다. 너는 앞 맥락이 없다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/20-spec/spec-001-desktop-app.md` (v0.2.0) — 계약 SoT
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/10-decision/decision-001-desktop-app.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/30-work/work-001-desktop-port.md`
- 워커 리포트 셋: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p1-p2.md` · `report-desktop-p3.md` · `report-desktop-p4-p5.md`
- PoC 정본(read-only): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/server/` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/src/` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/tests/`

**기대는 개념** — 해당 없음.

## 2. 배경

웹 PoC 를 Tauri 2 + Rust 로 옮긴 코드 전체(`/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/desktop/`, 미추적 새 폴더)를 PR 전에 검수한다.
사용자는 macOS 앱에서 플레이스 3 · 블로그 19 조회와 엑셀 저장을 이미 해 봤고 오류는 없었다. 코디 대조로 플레이스 1건은 PoC 와 같은 시각 결과가 완전히 같았다.

## 3. 계약

해당 없음 (검수만). 역할 `rules.md` 「코드 검수」 체크리스트 전수.

## 4. 먼저 읽을 핵심 파일 / 따로 볼 것

- `desktop/src-tauri/src/` 전부 · `desktop/src-tauri/js/` · `desktop/src/bridge.js` 와 진입부 · `desktop/src/main.jsx` 의 PoC 대비 diff(`diff /Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/src/main.jsx /Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop/reference/2026-09-09-sc-prototype/desktop/src/main.jsx`)
- **따로 볼 것 (코디 요청)**
  1. 사용자 조회에서 `강남성형외과`·`신논현역성형외과` 가 **확인 업체 228 · 광고 18 로 똑같이** 나왔다(각 3페이지). 페이지 누적·광고 집계·타겟 발견 시 종료 로직이 PoC `place.mjs:71-101` 과 같은지 — 우연인지 버그인지 코드로 판정.
  2. 브라우저 기동 인자에 `--lang=en_US` 가 보인다(실행 중 프로세스 관측). SPEC §3 `ko-KR` 과의 관계(컨텍스트 locale 로 덮이는지).
  3. 워커 이슈 4: `main.jsx` 에 `import` 1줄 추가 — SPEC §5 「셋뿐」 범위 안인지.
  4. rustls 암호 제공자로 `aws-lc-rs` 를 써서 Windows 빌드에 NASM 우회(`AWS_LC_SYS_PREBUILT_NASM=1`)가 필요해졌다 — `ring` 으로 바꿀 여지와 Windows 빌드 위험을 WARN 으로 평가.
  5. 180초 화면 상한과 Rust 쪽 잠금·브라우저 기동 180초가 겹칠 때 사용자가 만날 동작.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/review-code-report.md` (리포트 1개만 생성)

## 6. 구현 단계

1. `git -C /Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop status` 로 범위 확인 — `desktop/` 밖 변경이 있으면 FAIL.
2. 체크리스트 전수 + §4 따로 볼 것 다섯.
3. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/review-code-report.md` 에 역할 형식으로. 「사용자가 실물에서 만날 자리」 절 필수.

## 7. 범위 제약 — 하지 말 것

- 파일 수정·테스트 실행·네이버 요청·앱 실행 금지.

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 또는 PoC 파일:줄). 판정은 FAIL(계약·PoC 와 다른 것이 돈다) · WARN(물어야 할 만큼 모호) · PASS. 「조용히 통과하는 자리」를 따로 본다 — 빈 단언·폴백·문구/제한값 변경
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
  --to term_4d2a12b8-e3cf-45de-a097-daa193cfd908 --from term_474e9b40-427f-4e01-98bd-fc77cef81d05 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d2a12b8-e3cf-45de-a097-daa193cfd908 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d2a12b8-e3cf-45de-a097-daa193cfd908 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
