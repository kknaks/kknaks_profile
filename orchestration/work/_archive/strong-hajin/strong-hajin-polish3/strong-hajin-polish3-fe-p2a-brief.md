# [frontend] WORK-010 Phase 2a — 업무 상세 헤더 · 메타 정보 · 인라인 즉시 저장

너는 이 워크트리를 조사하고 Phase 1 을 끝낸 **strong-hajin `frontend` 워커**다. 맥락이 끊겼으면 아래 파일만으로 이어 갈 수 있다. 역할 문서:
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 rules·skills·tools·workflow) · 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3/AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` (base `origin/main` `d1b5137` · Phase 1 은 코디가 커밋했다 — `git log` 로 확인)
⚠ **Phase 3(셸) 워커가 같은 워크트리에서 `frontend/src-tauri/`·`lib/shell.ts`·`App.tsx`·`labels.ts`(다운로드 문구 키) 를 만지고 있을 수 있다.** 너는 `lib/shell.ts` 를 건드리지 마라. `App.tsx` 는 **AX 단추 삭제에 따른 `askAboutTask`·`onAskAboutTask` 정리만** 허용 — 다운로드 수신부 근처는 손대지 말고, 겹치면 코디에게. `labels.ts` 는 정확한 위치 편집만(전체 덮어쓰기 금지).

## 1. SSOT
- **SPEC-007 v0.5.1** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` — **§2.10.1 · §2.10.2 · §2.10.4 · §2.10.7 · §2.10.8 · §2.10.9(이 페이지 몫)** · §3 S-1·S-2·S-9 · §6 「고도화 3차」 AC. **SPEC 이 정본** — WP 와 다르면 SPEC
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md` — **Phase 2a(2a-1 ~ 2a-4)** 체크박스 = 계약. 원칙 P-1~P-5
- 너의 조사 `fe-survey-report.md` §4(구조 1:1 · 편집 흐름 · 출처 · 입구 16곳 · 부품) · §5 · §6 / 서버 사실 `be-survey-report.md` §4-2·4-3(PATCH 8칸 · version · 422) · §4-7·4-8
- 기준선 `flaky-baseline-evidence.md`(FE 기존 실패 5건)

## 2. 이 페이지의 범위 (상세는 WP 2a)
1. **헤더** = (겹일 때) 뒤로 · 제목(클릭 인라인) · × — kicker·상태 칩·버전·편집·AX 삭제. AX 묻기는 끝까지 걷어낸다(쓰는 곳 0 이 되면 `askAboutTask` 까지). 공용 `Modal` 을 바꿔야 하면 업무 상세 전용 prop/className 으로만
2. **메타 정보 구역**(2열 격자, 행 순서 SPEC §2.10.2) — 이 페이지에서 **진행 상태·담당은 읽기 글자**(셀렉트는 2b). 시작 예정일·마감일 = DateField 즉시 저장(빈 행도 선다 · 예정>마감 막음). 마감일 초과 = 마감일 행 옆 danger 배지. 출처 = 「AX 제안 · 판단 보기」(`onOpenSource` 없는 화면은 글자만)
3. **업무 내용** 인라인 여러 줄(blur 저장, Enter 줄바꿈) · 칸 머리 하나만
4. **인라인 즉시 저장** — 편집 모드(`metaEditing`·편집/편집 끝내기·「변경 저장」·`dirty`) 삭제 · 필드 하나 = PATCH 하나 · 안 바뀌면 안 보냄 · **직렬 대기열 + 앞 응답 version 이어받기** · 실패 = 원래 값 + 필드 옆 표시 · **422 stale = 다시 읽고 서버 값 + 필드 옆 표시**(자동 재전송 없음) · 호출부 3곳(내 업무·홈·캘린더) `onUpdate` 가 새 version 을 돌려주게
5. **읽기 전용 입구**(canManage=false·read_only·cancelled)에서 전부 글자만
6. **「시작할 수 없습니다」 배너 삭제**(본문). 푸터·`scax-blocked-note`·목록 행은 **이 페이지에서 건드리지 않는다**(2b 와 W8)
7. **여백** — 머리 아래~메타 정보 간격을 업무 상세 스코프에서만 줄인다(공용 `.scax-modal__head/__body` 불변)
- **푸터는 이 페이지에서 그대로 둔다**(상태 단추들). 단 「변경 저장」만 지운다. 「진행과 판단」도 2b 몫 — 그대로

**쓰는 곳을 전부 센다** — `metaEditing`(읽는 자리 6) · `onAskAx`/`askAboutTask`/`onAskAboutTask` · `blockedBanner` · `onUpdate`/`updateTask` 호출부 · 공용 Modal 변경 시 사용 13표면 · `origin-chip` · 바꾼 CSS 선택자를 grep 으로 세고 **바꾼 자리 / 유지한 자리(이유)** 표를 보고에 낸다. SPEC §2.10.9 의 이 페이지 몫과 1:1 대조.

## 3. allowed_paths
- `frontend/src/` (테스트 포함) — 단 `lib/shell.ts` 금지 · `App.tsx` 는 AX 정리만. `frontend/src-tauri/` 금지

## 4. 하지 말 것
- 커밋·push 금지. **서버·프론트를 띄우지 마라. 사용자 포트(8001·5176·54329)를 건드리지 마라**
- 새 모양을 만들지 마라 — DS 부품(`InlineText`·`DateField`·`Badge`·`Button`)·토큰만. 2열 격자처럼 시안이 없는 자리는 기존 토큰으로 짜고 DS-gaps 에 적는다
- 서버 코드 수정 금지. 서버 응답이 모자라면 우회 조립하지 말고 코디에게

## 5. 검증
```
frontend 에서 npx vitest run --no-file-parallelism (기준선 5건 분리) · npx tsc --noEmit · make frontend-build. 같은 검증 중복 실행 금지. api.ts 밖 fetch 금지, 기존 부품/viewModels/labels 재사용.
```
- 새/고친 테스트(WP Phase 2a 검증 목록): 헤더에 kicker·상태·버전·편집·AX **없음** · 인라인 저장(안 바뀜=요청 없음 · 직렬 · version 이어받기 · 422 → 다시 읽기+서버 값) · 날짜 즉시 저장·뒤집힘 막음 · 읽기 전용 입구 안 열림 · 배너 없음 · 출처 「판단 보기」/글자만 · 마감일 초과 배지 자리
- 기존 테스트가 편집 모드·AX·배너를 단언하고 있으면 **계약이 바뀐 것**이니 고친다(지우는 대신 「없다」로 뒤집을 수 있으면 뒤집는다)
- 회귀: 프로젝트 우 패널(`ProjectTaskPanel`)·목록 등 바꾼 공용 심볼을 쓰는 곳

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다.

- **커밋·push·PR 하지 마라.** 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-p2a-worker-report.md` 에 파일로도 남긴다.
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-010 Phase 2a" \
  --body "변경 파일 / 계약 체크 결과 / grep 으로 센 자리 표 / 기준선 vs 결과 / DS-gaps / 미결"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] frontend 완료 — WORK-010 Phase 2a. 리포트 fe-p2a-worker-report.md" --enter
```
막히면: `orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[질문] frontend: <질문>" --enter`
