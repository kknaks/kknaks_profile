
# [desktop] WORK-001 P6 — 코드 레포 분리 정리 (kknaksss/sc-rank)

너는 **sc-rank `desktop` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/roles/sc-rank/desktop/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/sc-rank/sc-rank-desktop`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. **이번 판은 P6 만.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/30-work/work-001-desktop-port.md` — P6 행
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/20-spec/spec-001-desktop-app.md` (v0.2.2) §1 위치·구성
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/10-decision/decision-001-desktop-app.md` D-07 (10-01 개정)
- 앞 판 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-fix-review.md`
- PoC 원본(read-only, 다른 레포): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/server/`

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

앱 코드가 kknaks_profile `reference/2026-09-09-sc-prototype/desktop/` 에 있다가 이 레포(`kknaksss/sc-rank`) 루트로
**이력째 옮겨졌다**(첫 커밋 `20ef3b7`, subtree split). Windows PC 에서 clone 해 빌드하기 위해서다.
옛 자리에서는 PoC 가 `../` 에 있었는데 이 레포에는 없다 — 그 가정으로 깨지는 곳을 정리한다.

## 3. 계약

- 동작·판정·문구 변경 **0**. 이번 판은 경로·자료 정리뿐이다.
- 주입 JS 동일성 테스트(`src-tauri/tests/collect_offline.rs` — `../../server/*.mjs` 를 읽음)는 **레포 안 `poc/` 의 PoC 원본 사본**을 읽게 바꾼다. `poc/` 에는 그 테스트가 읽는 PoC 파일만 **바이트 그대로** 복사하고, `poc/README.md` 한 장에 출처(kknaks_profile 경로·커밋 `d6954f0`)와 「수정 금지 — 동일성 검사용」을 적는다.
- `README.md`: `../server/`·`cd reference/…/desktop`·`desktop/` 같은 옛 경로를 레포 루트 기준으로. Windows 절차는 `git clone https://github.com/kknaksss/sc-rank.git` 부터 시작.
- 그 밖에 레포 밖을 가리키는 곳이 있으면 **전부 grep 으로 찾아** 같은 원칙으로 정리하고 목록을 보고한다.

## 4. 먼저 읽을 핵심 파일

- `src-tauri/tests/collect_offline.rs` · `README.md` · `grep -rn -E '\.\./\.\./|reference/2026|desktop/' --exclude-dir=node_modules --exclude-dir=target .`

## 5. allowed_paths — 이 밖은 건드리지 마라

- 이 레포 전부(브리프 상단 워크트리)
- 리포트 파일 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p6.md`

## 6. 구현 단계

1. grep 전수 → 정리.
2. `npm ci` → `cd src-tauri && cargo test && cargo clippy --all-targets -- -D warnings` → 루트 `npm run build` (1회씩).
3. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-p6.md` — 바꾼 곳 목록 · 명령 출력 수치.

## 7. 범위 제약 — 하지 말 것

- 동작 변경 · 네이버 요청 · 앱 실행 · GUI 자동화 금지. kknaks_profile 레포 수정 금지. 커밋·push·PR 금지.

## 8. 검증

```
src-tauri 에서 cargo test · cargo clippy --all-targets -- -D warnings, 루트에서 npm run build. Phase 범위에 맞게 1회씩 — 통과하면 반복하지 마라. 실수집(네이버 요청)은 Phase 끝에 1회만, 요청 간격 규칙을 지킨다. 사용자 포트·프로세스·브라우저 프로필을 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
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
  --to term_4d2a12b8-e3cf-45de-a097-daa193cfd908 --from term_7546f553-e9fa-47fb-b58b-1d35fecc8522 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "desktop 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d2a12b8-e3cf-45de-a097-daa193cfd908 \
  --text "[worker_done] desktop 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d2a12b8-e3cf-45de-a097-daa193cfd908 --text "[질문] desktop: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
