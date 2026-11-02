# [frontend] WORK-007 Phase 5~6 — 회의 중 화면 · 스트림 훅 · 2트랙

너는 **task-management `frontend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
**코드 워커는 한 번에 하나만 돈다.** WORK-006 전부(`a7e1bd4` · `2d6319e` · `618d5bb`)와 WORK-007 백엔드가 이미 들어와 있다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-007-meeting-live.md            ← 네 빌드 계획. Phase 5·6 만
  20-spec/spec-007-meeting-live.md            ← UX(§2 U-1~U-8) · §4 WS·API · §6 Acceptance
  00-design/회의록.dc.html                     ← 시각 정본. L761~1047 · L1048~1197 · L1198~1402
  00-design/디자인 시스템.dc.html               ← [09] MEETING NOTE(L649~755) + 05·06·07·10
  10-decision/decision-003-meeting-notes.md   ← 정책
  40-architecture/frontend/README.md          ← 구조 규약. 리뷰어 판정 기준
```

**`00-design/*.md` 요약본을 열지 마라.**

## 1. 범위 — Phase 5 · 6

```
Phase 5  프론트 공용 부품 · 스트림 훅   ← 화면보다 먼저 만든다
Phase 6  회의 중 화면 조립 · 실패 경로 · 첨부 · 반응형
```

**Phase 1~4(백엔드)는 끝났다. `app/back/` 을 건드리지 마라.**

## ⛔ 2. 공용 부품을 먼저 만든다 — WORK-008 이 그대로 쓴다

**화면부터 만들면 다음 work 가 복제한다.** WP Phase 5 가 그래서 앞에 있다.

| 부품 | 누가 또 쓰나 | 규칙 |
|---|---|---|
| **`AgendaLineTree`** | **회의록 탭 · AI 탭 · WORK-008 통합본 탭 셋** | **컴포넌트 안에 `track ===` 비교 0건.** 차이는 **props 로만**(근거 칩 · AI 안건 칩 · 편집 가능 여부 · 배지 문구). grep 으로 증명해라 |
| `MeetingStatusBar` | 회의 생애 전체의 상단 바 **한 자리** | WORK-006 `MeetingTopBar` 와의 관계를 정해라 — **두 파일이 같은 자리를 다투면 안 된다** |
| `TranscriptPanel` | WORK-008 상세의 스크립트 | `scrollToRange` + 하이라이트 + `Esc` 해제 |
| `PromptBar` · `LineKindPopover` | WORK-008 편집 모드 | `/` 팝오버 **4종**(논의·결정·**업무**·액션) + 새 안건 + 이동 |
| `lib/api/ws.ts` | — | **`new WebSocket(` 은 이 파일 밖에 0건** |

**WORK-006 이 만든 것을 다시 만들지 마라** — 첨부 탭·추가 팝오버·파일 드로어·`DrawerFrame`·`Selector`·`ItemRow`·`V2Gate`·`EmptyState`.
**`lib/` 로 올라간 것을 써라** — `useRowFailures` · `useWorkSettings` · `inlineErrorMessage`(`618d5bb` 에서 옮겼다).
**`features/*` 사이 import 는 0이어야 한다** — `static.test.ts` 가 이미 고정하고 있다.

## ⛔ 3. 정본 — 문서보다 이게 우선

```
agendas.{human, ai, merged}     tracks.* 아님
latestBatchSeq                  aiBatchSeq 아님
invalid_meeting_status          meeting_not_recording 없다
안건 배지                        active 「논의 중」 · done 「완료」 · next 「대기」   ← 회의 중이다
                                「다음 논의로」는 종료 후(WORK-008)다
AI 안건                          「AI 안건」 칩. track='ai' 에만 있고 회의록 탭에 안 보인다
경과 시간                        now − recordingStartedAt  (start_at 아님)
근거 칩 벽시계                    recordingStartedAt + fromMs
```

## ⛔ 4. 그리지 마라 — 기획·정책에 없다 (SPEC-007 §7-B)

```
L813~829        상태 바 파형 15개 막대       오디오 분석이 캡처 경로에 없다
L830·1101·1251  상태 바의 「자동 저장 · 09:42」  상태 바는 문구 + 경과 시간만
L795·1082·1232  부제의 「회의실 A」            장소는 v1 에 없다
L956~958        프롬프트 바 「+」 버튼
L1111~1152      AI 요약 카드(요약 문단 · 카운트 · 펼침)  → 안건>줄 트리로 그린다
L1172·1322·1354 「회의 중 작성」 · 「· 안건 1」 캡션
L1176~1187      PNG · PDF 첨부 행
L1036           잠정 발화의 시각
```

**시안에 없어 디자인 시스템으로 조립할 것** — `/` 팝오버의 **「업무」 항목**(L925~936 이 3종만 그린 것은 누락 · [09] L668~672) · AI 탭 트리 · 사유 상태 바 4종 · 「재개」 버튼 · 「안건 선택」 상태 · 빈 상태 2종.

## ⛔ 5. 정책 — 뒤집지 마라

```
일시정지        헤더에 [일시정지]/[재개] · [회의 종료]. 종료는 connecting 빼고 항상 활성
                — paused/stream 에서도 누를 수 있다(동작은 WORK-008)
마이크·스트림 실패  일시정지 상태 + 사유 배너. 별도 「다시 연결」 버튼 만들지 마라
자동 재연결      금지. setInterval/setTimeout 재연결 코드 0건
                resume() 을 사용자가 부를 때만 새 연결
잠정 토큰        화면 표시용. 확정 토큰만 서버가 적재한다
AI 증분          오는 대로 즉시 반영 + 「배치 n회 반영」. 버퍼링 금지
화자             익명 라벨(화자 1/2)까지만. 이름 입력 자리 없음
캡처            내 마이크만(getUserMedia). 트랙 ended → paused/mic
첨부            자료함 md · URL 두 갈래만 실동작. 로컬 업로드는 V2Gate — 요청 0
자동 재시도      없다. 낙관적 갱신 없다
```

## 6. 지킬 것 — 아키텍처

```
정적 빌드     동적 세그먼트 0 · 모든 page 에 'use client' · 상태는 쿼리스트링
색            컴포넌트 hex 리터럴 0. 토큰만
글꼴 크기      text-[NNpx] 0. 프리셋만 — 필요하면 tailwind.config 에 계단을 더하고
              **lib/utils.ts twMerge 에 등록**(빠뜨리면 조용히 버려진다)
날짜          new Date() 직접 포맷 0 — lib/datetime 을 쓴다
오버레이      Sheet/Dialog 직접 import 0 — DrawerFrame·lib/overlay 경유
영역 사이 import  0. 공유는 lib/ 나 components/shared/ 로
IME           isEnterSubmit() 를 쓴다 — 새 가드 만들지 마라
토큰 저장소    tokenStore 밖에서 저장소 호출 0
WS 인증        첫 프레임 토큰 · 4401 시 refresh 1회 → 재연결 1회 → 또 4401 이면 로그인
```

## ⛔ 7. 검증 — **앱 창 E2E 는 하지 마라**

**WP Phase 6 이 「Tauri 앱 창에서 실제 마이크로 회의를 기록한다」로 적혀 있다. 이번 발주는 그것을 하지 않는다.**

```bash
cd app/front && npx tsc --noEmit
cd app/front && npx vitest run
```

**대역(fake) WS 서버와 목 `getUserMedia` 로 옮겨라.**

```
error{upstream} 수신    → paused/stream · 재연결 시도 0건 (WebSocket 생성 스파이)
마이크 트랙 stop()      → paused/mic · pause{mic} 프레임 송신
resume()                → 새 연결 1회
잠정 교체 · 확정 append  → 프레임 분배 테스트
ai.batch 병합            → latestBatchSeq 증가 · 「배치 n회 반영」
scrollToRange            → 겹치는 블록 하이라이트 · Esc 해제
AgendaLineTree           → 같은 컴포넌트에 human/ai 데이터를 넣어 분기 없이 두 모양
/ 팝오버 4종             → 「업무」 항목 존재
상태 바                  → 파형·「자동 저장」 없음 · 경과 시간이 recordingStartedAt 기준
```

**정적 검사 — `grep` 결과를 완료 증거에**

```
new WebSocket( 이 lib/api/ws.ts 밖에 0
setInterval/setTimeout 재연결 0
AgendaLineTree 안에 track === 비교 0
hex 리터럴 0 · text-[NNpx] 0 · new Date( 포맷 0
features 사이 import 0 · Sheet/Dialog 직접 import 0
```

**테스트로 못 덮은 것은 「실물 확인 필요」 목록으로 보고에 남겨라.** 마이크·Tauri·반응형 실측이 거기 들어간다. **임의로 통과 처리하면 리뷰에서 FAIL 이다.**

## 8. 지킬 것 — 일반

1. **`app/front/` 밖을 건드리지 마라**
2. **문서를 고치지 마라**
3. **커밋·push 하지 마라**
4. **WP 범위 밖을 하지 마라.** 발견하면 보고에 적어라
5. **기획·정책에 없는 기능을 만들지 마라.** 시안에 있어도 — §4 목록
6. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 9. Done Criteria

- [ ] Phase 5·6 의 WP 작업 항목이 전부 구현됐다
- [ ] **`AgendaLineTree` 안에 `track ===` 비교 0건** — grep 증거
- [ ] **`new WebSocket(` 이 `lib/api/ws.ts` 밖에 0건** · 재연결 타이머 0건
- [ ] `MeetingStatusBar` 와 WORK-006 `MeetingTopBar` 의 관계가 정리됐다(같은 자리를 두 파일이 다투지 않는다)
- [ ] §4 「그리지 마라」 8항목이 화면에 **0건**
- [ ] 안건 배지가 **「대기」**(회의 중이다)
- [ ] `tsc` 0 에러 · `vitest` 통과 · **WORK-006 화면 회귀 없음**
- [ ] 정적 검사 grep 결과가 완료 증거에 있다
- [ ] 「실물 확인 필요」 목록이 정직하다
- [ ] `app/front/` 밖 변경 0 · 커밋 없음

## 10. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_106d427d-3614-40e0-a2c2-cea9d95c852e \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-007 Phase 5~6 완료" \
  --body "만든 공용 부품과 WORK-008 이 쓸 props 계약 / AgendaLineTree track 분기 0 증거 / WS 훅 상태 기계와 실패 3종 테스트 / MeetingStatusBar↔MeetingTopBar 정리 / 재사용한 WORK-006 부품 / tsc·vitest 결과 / **실물 확인 필요 목록** / 정적 검사 grep / 시안에 있으나 안 그린 것 / 범위 밖이라 안 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-007 Phase 5~6 완료. 상세는 인박스." --enter
```
