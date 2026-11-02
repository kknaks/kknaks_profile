
# 재개 노트 — sc-meeting-room (sc-ax)

**지금**: 사용자 시안 리뷰 1~5번을 frontend Claude에 정식 발주. API는 backend read-only 확인, 미지원은 보고.
**다음**: frontend 완료 보고 후 시안·기능·전체 테스트 결과와 backend 무변경 검수. 커밋·push 금지.

세팅: `scripts/new-work.sh sc-ax sc-meeting-room` · 설정 SSOT `config/projects/sc-ax.json`
코디handle: `term_18011a51-e9ec-4cad-9370-1836d3ee8d2d`

## 워크트리

- `app`: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room` (branch `kknaksss/sc-meeting-room`, base `origin/main` → PR `main`)
- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-room-spec` (branch `kknaksss/sc-meeting-room-spec`, base `origin/main` → PR `main`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] <진행 중 — 누가 · 무엇을>
- [ ] <다음 할 일>
- [!] <막힌 것 · 사용자 게이트 · 주의>

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| <YYYY-MM-DD> | <무엇을 정했나> | <사용자 지시 · 조사 리포트 · 리뷰 판정> |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| frontend 시안 반영 | `term_08a8813a-da42-428b-9fff-52586fe9614f` | `task_de9c3f345a04` | `ctx_c29548503a5c` | `sc-meeting-room-fe-brief.md` | 워커 완료·코디 검수 대기 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- 2026-09-14: 현재 Codex 코디 `term_fa9914b3-124d-43d2-81ec-10417df53069`가 사용자 확정 시안 변경을 발주. 비교 이미지 16장 visual-review-2026-09-14/ 보존. 기존 DS sync 변경 보존. 별도 frontend Claude terminal 사용.

- `<YYYY-MM-DD>` <무슨 일이 있었나 — 한 줄>

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.

## 추가 리뷰 대기 — 2026-09-14

- 회의 종료 스크립트 가독성·후속 요청 모달 고정 메타 제거·첨부 500 오류: `meeting-ended-review-pending.md`. 추가 발주 전.
- 사용자는 실제 회의에서 회의 중 기능 테스트 중. 돌아오면 결과를 합쳐 발주 여부를 따른다.

- FE 완료 보고 수신: tsc 0, vitest 직렬 532 통과. 기본 병렬 실행 간헐 타임아웃 보고. 시각 검증 미실시. 완료 회의 정보 편집 진입점 소실 미결. 후속 리뷰 4·5 및 처리 워커 미기동 정정 기록함.

## 회의 중 후속 발주

- frontend: `term_08a8813a-da42-428b-9fff-52586fe9614f` · `task_5ff644180405` · `ctx_d6e0c4c78c96` · `sc-meeting-room-fe-live-brief.md` · 발주.
- 회의 중 5항목만. 종료 후 스피너/업무 요청 메타 제거 보류. 첨부 업로드는 사용자 수정 보존.

- 사용자 최신 정정: 회의 종료 버튼은 빨간 solid 유지. 후속 브리프 5번 정정 및 워커 직접 통보.

## 중복 생성 버그 긴급 후속

- 회의 중 FE 완료 보고: tsc 0/직렬 543 통과. 진행 중 첨부는 현재 SPEC/API 금지여서 미변경. 스크립트 공용 변경은 종료에도 영향.
- 사용자 보고 quick-start 2회 생성: `task_38de68a375e6` / `ctx_8409c07ebec7` / `term_08a8813a-da42-428b-9fff-52586fe9614f` / `sc-meeting-room-fe-duplicate-start-brief.md` 발주. backend 사용자 수정·재기동 완료, 수정 금지.

## 종료 후 발주

- 사용자 승인: 스피너+최종 회의록 생성 안내, 회의 후속 요청 모달 상태/요청자 제거. `task_0afebd651ed9` / `ctx_d08aae3409b8` / `term_08a8813a-da42-428b-9fff-52586fe9614f` / `sc-meeting-room-fe-ended-brief.md`.
- 직전 중복 생성 수정 완료 보고: tsc 0, 직렬 547. 실제 Network 사용자 검증 남음.

## 가독성 후속 발주

- `task_9dbcc966b6ca` / `ctx_61fe6a63e7e5` / `term_08a8813a-da42-428b-9fff-52586fe9614f` / `sc-meeting-room-fe-contrast-brief.md`. 사용자 요청대로 결과 회수까지 진행. 이전 종료 작업 완료 보고 tsc 0·직렬 555.

## 프론트 바퀴 발주처 (사용자 지정 2026-09-14)

`term_08a8813a-da42-428b-9fff-52586fe9614f` — 「✳ 회의 화면 시안 정합 및 기능 복구」
워크트리 `ax-workspace/sc-meeting-room` · 브랜치 `kknaksss/sc-meeting-room`.
**백엔드 → 리뷰 → 수정 이 닫힌 뒤** 이 터미널로 발주한다. 새 터미널을 만들지 마라.

프론트가 고칠 것 8건(코디가 코드에서 확인, 2026-09-14) — 백엔드 리뷰 보고와 대조해 확정한다:
1. **탭마다 안건 목록이 갈린다** (§4.2-6) — 지금 `MeetingDetailPage:862` 가 `shownAgendas.map` 한 벌만 돈다
2. `track: "memo"` → `"human"` — `viewModels.ts:851` · `MeetingDetailPage:74,139,376,555,822,825,883`
3. `can_edit_agendas` 불리언 → 벌별 `{human,ai,final}` — `viewModels.ts:917` · `MeetingDetailPage:293`
4. 종료 후 원본 두 벌을 여는 자리 — **`OQ-319` 미결**(탭/드로어/접힘)
5. 결론 표시는 최종 벌에만 (§4.0-5) — 지금 `:890` 이 벌 구분 없이 붙인다
6. 「안건 1. 안건 1」 라벨 (R-50)
7. 계보(`merged_from`·`from_lines`) 표면 — 프론트에 grep 0건, 스펙이 화면을 아직 안 정함
8. 저장 페이로드에 줄 id — `api.ts:958` 이 지금 `lines?: string[]`

사용자 결정: 「백엔드 완료하고 프론트 발주」 — 6번만 따로 빼지 않는다.
같은 파일을 두 번 여는 것이 되고, 나머지 7건이 어차피 그 파일을 크게 고친다.

## 사이드바 상단 발주

- `task_172cbbffe22c` / `ctx_de9190f9eefb` / `term_08a8813a-da42-428b-9fff-52586fe9614f` / `sc-meeting-room-fe-sidebar-top-brief.md`. 알림 disabled, 기존 설정 이동, 실제 프로필·접기 버튼·구분선. 하단 메뉴 제외. 이번 변경 커밋 금지.
- 이전 프론트 변경은 사용자 요청으로 5e7a41d 커밋 완료, push 없음.
