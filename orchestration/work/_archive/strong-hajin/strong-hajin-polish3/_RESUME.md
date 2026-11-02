# 재개 노트 — strong-hajin-polish3 (strong-hajin)

**지금**: 사용자 E2E 진행 중 · 2루프 E2E-1·2 커밋(코드 `53c9c20` · 문서 `ba3ca7e` SPEC-007 v0.5.2) · 다음 지적 대기
**다음**: 사용자 E2E 피드백 모아서 2루프 한 브리프 → 검수 → 코드 PR + 문서 PR → 운영 반영(front 이미지 + medi-ax dmg 재빌드) → archive-work.sh

세팅: `scripts/new-work.sh strong-hajin strong-hajin-polish3 --workers backend,frontend` · 설정 SSOT `config/projects/strong-hajin.json`
코디handle: `term_0ad6d618-af6c-4707-b594-389c33e240c1` (env `ORCA_TERMINAL_HANDLE` 은 stale — terminal list 로 확인)

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` (branch `kknaksss/strong-hajin-polish3`, base `origin/main` = `d1b5137` → PR `main`)

## 1. 지금

요청 = 계약. 사용자가 말한 것만 받아 적고 범위를 넓히지 않는다.

- [~] R1 (로그인) 브랜드 h1 → 「메디솔브 AX 프로젝트」, 설명 문장 삭제. 워드마크 유지
- [~] R2 (회의 상세) 「내보내기」 단추 크기를 옆 단추와 맞춤 · Tauri 다운로드 동작 확인·수정
- [~] R3 (회의 상세) 제목 인라인 수정(클릭 → 입력 → blur/Enter 저장, Esc 취소, 빈 값 되돌림) · 제목 없을 때만 「제목 후보: … [적용]」
- [~] R4 (업무 상세 모달 개편) §2 R4 결정대로
- [~] R5 (업무 상세) 선행업무 안내 박스·푸터 문구 삭제, 규칙 유지 + 상태 변경 시 토스트
- [~] R6 (업무 상세) 헤더 아래 여백 축소 — R4 개편 후 헤더→메타 정보 간격
- [x] 완료 확인창 — 이미 있음(「남은 단계가 있습니다」 ConfirmModal) 그대로
- [x] 출처 링크 = 원 AX 초안(ActionItem 판단 상세), 제안 주인만 보임
- [x] 인라인 저장 버전 — 매 저장 +1, 어긋나면 422 → FE 직렬 저장(응답 version 이어받기)
- [ ] E2E 2루프 후보: 회의 제목 편집 가능할 때만 긴 제목이 두 줄(InlineText pre-wrap vs 제목 nowrap) — review-fe-p1 W4
- [ ] 실기 필수 판정: 회의 자료 서랍 PDF 미리보기(`<object>`)가 셸 가로채기로 빈칸이 되지 않나 (review-fe-p3 W4)
- [?] `⋯`(취소 제안·조건 변경 제안)는 요청자가 거의 못 본다 — 요청자는 「보낸 업무」에서 읽기 전용으로 연다(지금 푸터도 같았다). 사용자 E2E 때 알리고 묻는다
- [?] 회의 자료 서랍 「내려받기」의 inline 형식(PDF·이미지)이 데스크톱 앱에서 「아무 일 없음」(Phase 3 X) — 사용자 E2E 때 파일 저장으로 바꿀지 묻는다
- [ ] 다음 작업 후보(사용자 10-05): **설정(Settings)·수신함 페이지** — 시안 claude design 프로젝트 `7e839512`(= 코드 `.design-sync/`) `Settings.html` + `_ds_bundle.css/js`, 수신함 시안. DesignSync 는 orca 워커로 읽힌다(코디 직접 X). 이 slug 범위 아님
- [ ] 다음 세션 후보(사용자 10-05): Slack·Gmail(회사 Workspace)·카카오톡 수집 — 카톡은 mykakao 재사용(로컬 DB 복호화+폴링, Mac 호스트 전용, config canonical 경로가 Windows 로 낡음). 이 slug 범위 아님
- [!] kknaks_profile 은 PUBLIC — 실명·메일·비밀값 커밋 금지
- [!] 로컬 스택은 사용자가 볼 때만. 백엔드 커밋 뒤 스택 재시작

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-05 | **E2E-1** 메타 정보 한 줄 두 항목: 진행 상태|버전 · 담당|출처 · 시작 예정일|실제 시작일 · 마감일|실제 종료일 · 결재·참조(있을 때) · 날짜칸 축소 · 좁은 폭 1열 · SPEC-007 「라벨·값 2열」 문구 동기 필요 | 사용자 「응 그렇게 가자 발주 해줘」 |
| 2026-10-04 | Phase 2b 검수 WARN 4 코디 답: W1 version 올리는 나머지 명령(제안·자료·완료 보고·연결 편집)도 직렬 대기열 · W2 담당 후보 한 번 조회·대상 이름은 후보/assignment 에서 · W3 죽은 `.scax-chat__context*` 삭제 · W4 `⋯`·danger tone DS-gaps | review-fe-p2b · 코디 |
| 2026-10-04 | Phase 2a 검수 WARN 6 코디 답: W1 전이·담당·체크리스트도 인라인 저장 직렬 대기열로 · W2 죽은 AX 참고 자료 경로 삭제(불필요 조회·토스트 제거, 다운로드 수신부 제외) · W3 내용 p→textarea 글자 뜀·캐럿 · W4 저장 중 표시 · W5 성공 시 전역 오류 걷기 — 전부 2b 에 합침 · W6 그대로 | review-fe-p2a · 코디 |
| 2026-10-04 | Phase 3 검수 WARN 7 코디 답: W1 quarantine 속성 · W2 /api/ 비2xx = 실패 토스트 · W3 가로채기 origin = 운영 origin 하나 · W4 `<object>` PDF 미리보기 취소 가능성은 macOS 실기 판정(깨지면 재발주) · W5 Windows 예약 이름·양방향 문자 · W6 on_download 실패 알림·키 충돌 · W7 읽기 타임아웃 | review-fe-p3 · 코디 |
| 2026-10-04 | Phase 3 방식 B(코디): wry 0.55.1 은 text/html 첨부에 download handler 를 안 부르고 응답 헤더도 못 봄 → 셸이 같은 origin `/api/` 최상위 이동·`_blank`(GET)를 가로채 Rust 가 `cookies_for_url` 로 직접 받아 응답 헤더로 판정, attachment = Downloads 저장, inline = 지금 동작 · `on_download` 도 걸기 · 새 crate `ureq`(native-tls) 1개 · 웹 알림 eval+CustomEvent(capabilities 변경 0) · 문구 「다운로드 폴더에 저장했습니다: {파일 이름}」/「파일을 저장하지 못했습니다.」 labels.ts 키 추가만 | `fe-p3-decision.md` · 코디 |
| 2026-10-04 | 검수 WARN 코디 답: W3 422 = 다시 읽은 서버 값 · W7 완료(확인 대기) = 셀렉트 없음·글자만 · W8 R5 = 업무 상세만(목록 행 TaskQuickActions 그대로) · OQ-T12 알림 = 셸이 웹에 사건 → 웹 공통 토스트(셸 문구 없음) | review-spec-report · 코디 |
| 2026-10-04 | writer OQ 닫음(코디 기본값): OQ-711 마감일 초과 배지 = 마감일 행 값 옆 · 뒤로 단추 = 헤더 제목 왼쪽 유지 / OQ-712 날짜 순서 E2E-5 / OQ-709 화면 사전 차단 없음·409 토스트만 / OQ-T12 첨부 = OS 다운로드 폴더 무대화 저장·성공/실패 알림·이름 겹치면 번호 / OQ-T13 인라인 `_blank` 범위 밖 — 실기에서 앱 화면 덮으면 사용자에게 / R3·R2a·R1 은 SPEC 없이 WP 에만 | writer 보고 · 코디 |
| 2026-10-04 | 진행 계획 승인: SPEC(007·006·회의·로그인) → 검수 → WP WORK-010(Phase 1 FE 작은 것 R1·R2a·R3 / Phase 2 FE 업무 상세 R4·R5·R6 / Phase 3 Tauri 다운로드) → Phase별 코드 검수 → 사용자 E2E 목록 보고. 서버 변경 없음. 끝까지 자율 | 사용자 「응 진행하자」 |
| 2026-10-04 | **a** 「진행과 판단」 구역 제목·담당자 변경 단추 삭제. 걸린 일(막힘 사유·완료 확인 대기+인정/보완 요청·보완 필요·담당 변경 대기·제안 응답·미완 하위)은 있을 때만 메타 정보 아래 상자로 | 사용자 「응 그렇게 가자」 |
| 2026-10-04 | **b** 상태 셀렉트 = 상태 전이만. 사유 필요 전이(막힘·취소·완료에서 재개)는 작은 모달(본문 인라인 막힘 입력도 모달로). 요청 업무 완료 = 완료 보고 모달. 취소 제안·조건 변경 제안은 헤더 `⋯` 메뉴 → 작은 모달 | 사용자 「권고안 · 작은 모달로」 |
| 2026-10-04 | **c** 담당 셀렉트 → 사유(선택) 작은 모달 → `/reassign` 제안, 담당 칸에 「변경 제안 중」. `task.assign` 없으면 읽기 전용 | 사용자 「권고안」 |
| 2026-10-04 | **d** 「AX에게 이 업무 묻기」 삭제 — 대체 입구 없음. `⋯` 메뉴는 요청자 제안 두 개만 | 사용자 「채팅에 묻기 일단 뺄거야」 |
| 2026-10-04 | **e** 출처 행 「AX 제안 · 판단 보기」(링크 = 원 ActionItem 판단 상세). onOpenSource 없는 화면은 글자만 | 사용자 「권고안」 |
| 2026-10-04 | **f** R6 여백은 업무 상세 스코프만. 공용 `.scax-modal__head/__body` 유지 | 사용자 「권고안」 |
| 2026-10-04 | **g** Tauri 다운로드 수정 포함 — 내보내기 = `.html` 첨부파일 저장, 앱 화면 유지. 완료 조건 macOS 실기 1회. `_blank` 첨부 링크도 같은 경로 확인. Windows 는 pending | 사용자 「화면이 렌더링되고 뒤로 갈 방법이 없어」 |
| 2026-10-04 | 완료 시 미완 체크리스트 확인창 = 기존 ConfirmModal 「남은 단계가 있습니다」 유지 | FE 조사 · 코디 |
| 2026-10-04 | **R4 업무 상세 모달**: 헤더 = 제목(클릭 인라인 수정, blur/Enter 저장, Esc 취소) + `×` 만. 「업무 상세」 머리글·상태 칩·버전 배지·편집·AX 단추는 헤더에서 뺀다 | 사용자 「헤더에 그냥 제목만」 · 「ax 버튼은 빼고 x 만」 |
| 2026-10-04 | **R4 메타 정보 구역** 신설 — 「업무 정보」와 같은 계층, 라벨·값 2열 격자: 진행 상태(셀렉트, 갈 수 있는 상태만 · 맨 아래 빨강 「업무 취소」+확인창) · 버전(읽기 전용, 코디 기본값) · 담당(셀렉트 즉시 저장) · 실제 시작일(읽기 전용) · 시작 예정일·마감일(날짜 선택 즉시 저장, 예정>마감 막음) · 출처(읽기 전용, 없으면 숨김) | 사용자 「메타 정보 구역을 넣자 · 담당자 셀렉트 · 진행 상태도 넣자」 · 출처 행 코디 기본값 |
| 2026-10-04 | **R4 편집 모드 폐지** — 모든 값은 그 자리 인라인 수정·즉시 저장. 값이 안 바뀌면 요청 안 함, 실패 시 원래 값 복원 + 필드 옆 표시. 업무 내용 = 인라인 여러 줄, blur 저장 | 사용자 「인라인으로 편집 · 다른 데 가면 자동 저장 · 굳이 편집을 나눠야 해?」 |
| 2026-10-04 | **R4 푸터 삭제** — 상태 전이는 메타 정보 진행 상태 셀렉트로만. 「진행과 판단」 구역 삭제. 「자료」「이력」은 범위 밖(그대로) | 사용자 「푸터에 완료 처리가 있으니 조회하고 닫을 때 계속 완료 처리」 |
| 2026-10-04 | **R5** 「시작할 수 없습니다」 박스·`.scax-blocked-note` 삭제. 막는 규칙 유지, 상태 변경 거부 시 토스트 「선행 업무 '○○'가 끝나지 않았습니다」 + 셀렉트 원복 | 사용자 「상태값 변경할 때 토스트만」 |
| 2026-10-04 | **R3** 회의 제목도 R4 와 같은 인라인 방식. 제목 후보는 「제목 없는 회의」일 때만 `[적용]` 과 함께 표시(코디 기본값) | 사용자 「회의 제목 수정도 마찬가지로」 |
| 2026-10-04 | 진행 순서: 요청 수집 → 코드 워커 읽기 전용 조사 → 계약(SPEC·WP) → 승인 → 구현 발주 | 사용자 세션 시작 지시 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend | `term_9ad99a8d-a800-4a0d-b525-869d033e347a` | `task_bd0ecf855f2d` | `ctx_682d7028aa28` | `strong-hajin-polish3-be-survey-brief.md` | 조사 완료 |
| writer | `term_c7a9e68e-fdc1-4bc0-ae65-59397967658b` | `task_ec44a10a619b` | `ctx_7fd720c2b236` | `strong-hajin-polish3-write-brief.md` | 완료 |
| reviewer | `term_5925682b-6b4f-4310-b511-e0c5ff7b8347` | `task_30e0aa95338f` | `ctx_7a7d1ba20fa0` | `strong-hajin-polish3-review-fe-p3-brief.md` (task_18d145cf13a2 · ctx_058772cde2f3 · 앞 P1 검수 WARN 4 완료) | **Phase 3 코드 검수 중** |
| frontend | `term_d91937b0-1fb8-48aa-b80a-fc23e2be573f` | `task_8f728b5e762a` | `ctx_279c43a7e103` | `strong-hajin-polish3-fe-p2b-brief.md` (task_9b4a8073d8ac · ctx_11068722e5ae) | Phase 2b 커밋 `58e591a` (검수 WARN 4 → fix1) |
| frontend(셸) | `term_9f7eadc0-4685-4ba7-b860-f5df3d66b22a` | `task_59598b7967c9` | `ctx_da3b77a44d56` | `strong-hajin-polish3-fe-p3-brief.md` | Phase 3 커밋 `9c15934` (실기 pending) |

## 4. 산출물

- spec PR: —
- code PR: —
- 리포트: `be-survey-report.md` · `fe-survey-report.md` (예정)

## 5. 이력 (최신이 위)

- `2026-10-04` P2a·P2b 커밋 · 로컬 스택(ax_demo_polish3 새 데모) + `make tauri-local` 기동 · E2E 체크리스트 전달
- `2026-10-04` Phase 1 커밋 `7f01c5b`(labels.ts 는 Phase 1 hunk 만 — Phase 3 다운로드 키는 미커밋) · Phase 2a 발주
- `2026-10-04` SPEC 검수 WARN 12 → fix1 · 문서 커밋 `eaeb24b`(SPEC·WORK-010) · FE 기준선 5건(`flaky-baseline-evidence.md`) · Phase 1·3 병렬 발주
- `2026-10-04` BE 조사 완료 — PATCH 8칸(담당·상태 불가) · 모든 명령 version+1·422 stale · reassign=제안·task.assign(구성원 없음) · 전이 활성 담당자만·허용 목록 응답 없음 · 회의 제목 PATCH(참석자·예정/완료, 잠금 없음) · Tauri on_download 0 → wry 가 text/html Allow(추정). 서버 변경 불요 판단
- `2026-10-04` FE 조사 완료 — R2 `--sm` 누락·Tauri 다운로드 처리 0(실물 확인 필요) · R3 InlineText 있음 · R4 진행과 판단 8구획·푸터 11종·담당 변경=제안·AX 입구 유일 · R5 드롭다운은 이미 409 토스트 · R6 41px 공용 13표면
- `2026-10-04` 세팅 · 사용자 요청 6건 수집 · 업무 상세 개편 방향 확정 · BE·FE 읽기 전용 조사 발주
