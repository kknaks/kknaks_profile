# Delivery 다섯 건 닫기 — 진행 기록

근거 = 사용자 2026-11-11 「아 그럼 스테이블에 올리고 다 닫자」 · 「이제 다 한 거잖아. 검증은 다음에 하자니까. 닫는 데 문제가 있어?」. baseline = mediness `origin/main` `19f7e40183e9cdb673db89190b831094507901a4`(DAY SPEC 000 ~ 005 stable).

## 공통 막힘 — 도구로 마감(spec-sync → complete-delivery) 불가

`spec-sync` 는 Delivery Issue 와 sync 문서 PR 을 **같은 `--github-repo`** 에서 찾는다(`tools/harness/src/mediness_harness/workflow.py` `spec_sync` → `fixture.pr_revision(spec_pr)` · `upsert_pr_comment(spec_pr, …)`). 대장 = CENTURION_DAY · sync PR = mediness 라 찾지 못한다 — harness README 「알려진 제약 1」 · **mediness#749 (OPEN)**. README 는 `--github-repo mediness` 우회를 금지한다(같은 번호의 다른 이슈 · PR 을 덮어씀). → 코디에게 방향을 물음(A · B · C · D).

## #241 — 진행 중(review 까지 · 마감 막힘)

| 항목 | 값 |
|---|---|
| contract_version | **7**(scope delta) · risk L3 그대로 · Target Delta 그대로 |
| contract_digest | `sha256:169aae2fb2c7da82b5e21f6f697670f714a7f9820d6be7e3250a5dec9af2a568` |
| plan_digest | `sha256:5438f95df42407aede9abd152ae69efad4555946b81859d6823b5cbd9e661639` — 승인 적용(human · kknaksss · 근거 사용자 결정) |
| baseline | ready @ `19f7e401` · missing `[]` |
| review-delivery | **recorded** — implementation `conformant` · merged · code PR #242 head `87cf2dec9e62db937cdcb6cc9c52f010baed8357` · merge `7b099e8f2973003f4d5203d082ca2a81ced23ec8` |
| per_spec | DAY-SPEC-003 `update-required`(§ API 표 :509 · D-3 :829 「통역 서버 없음 · 구현 전」 — #242 로 구현됨) · DAY-SPEC-004 `update-required`(C-1 :577 「#22 · 전체 알림 서버 없음 · 다음 WP」 · C-3 :579 「연결 문자열 방식 → WP-BE-4」 — #242 로 구현됨) · DAY-SPEC-005 `none` · DAY-SPEC-000 `none` |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` · `implementation:conformant` · `spec-sync:pending` |
| next_action | `run-spec-sync` |
| sync PR | 아직 없음(공통 막힘 — 코디 답 대기) |
| 상태 | **열림 — 마감 막힘** |

**뺀 수용 항목(그대로 · 다음 작업 검증으로 넘김 — Non-Goals 에 기록):**

1. A7 (사용자 실기기 · dev 배포 + TestFlight 다음 빌드 뒤) DAY-SPEC-003 A-46(통역 자막 양쪽 · 번역 음성 · 언어 바꾸기 · 종료 · 듣는 상태 누적 약 3분 20초 이상 긴 세션) · A-41 ~ A-43 · DAY-SPEC-004 C-A19 · C-A20 · C-A21(두 기기) · DAY-SPEC-005 N-A13 — wp-plan §7 목록
2. A11 (사용자 실기기) DAY-SPEC-004 C-A22(그림 8 재현 안 됨) · C-A23 · C-A25(두 계정 이상) — wp-plan §7 8 ~ 10
3. A14 (사용자 실기기) DAY-SPEC-004 C-A27 ② — TestFlight 사진 · 동영상 보내기 · 받기 · 크게 보기 · 재생 · 모아보기
4. A2 의 「BE-1 뒤 로컬」 실물(앱 ↔ 실제 서버 로컬 day-local — DAY-SPEC-004 C-A20 · C-A21) — 근거: `app-2-report.md:87` 하지 않음
5. A10 의 「BE-3 뒤 로컬 두 계정」 실물(DAY-SPEC-004 C-A25 — 두 계정 읽음 숫자) — 근거: `app-3-report.md:111` 하지 않음

**남긴 항목과 근거(전부 pass — 경로는 `day-r3/orchestration/work/fix/`):** 도구의 수용 id 는 순번이라 원래 라벨과 어긋난다(괄호가 원래 라벨).

| 도구 id | 원래 | 근거 |
|---|---|---|
| A1 | A1 앱 시술현황 | `app-1-report.md:24-31 · :43-44`(analyze 0 · +95) · `review-app-fix1-report.md:5 · :57-58` · `review-app-fix3-report.md:5 · :52-53`(+343) |
| A2 | A2 채팅 앱(테스트 더블) | `app-2-report.md:29-33 · :60` · `review-app-fix1-report.md:5-7 · :57-58` |
| A3 (…) | A3 서버 #22 · 전체 알림 | `be-1-report.md:22-28 · :48-52 · :16` · `review-be-report.md:129` · `review-be-2-report.md:5` |
| A4 | A4 통역 서버 단위 | `be-2-report.md:43-57 · :91-93` · `be-fix1-report.md:49-52` · `review-be-2-report.md:5 · :15` |
| A5 | A5 실제 Soniox | `be-2-report.md:98-112` · `fix-delivery-close-all-brief.md:18` |
| A6 | A6 로컬 키 비움 | `be-2-report.md:115-120` |
| A8 (코디) … | A8 시드 로그 · 코드 PR 하나 | `fix-delivery-close-all-brief.md:18` · PR #242 → dev `7b099e8f` |
| A8 | A9 읽음 서버 | `be-3-report.md:33-38 · :56-64` · `review-be-2-report.md:5` |
| A9 | A10 앱 채팅 화면(테스트 더블) | `app-3-report.md:64-69 · :87` · `app-fix3-report.md:50-52` · `review-app-fix3-report.md:5-7 · :52-53` |
| A10 | A12 저장소 서버 단위 | `be-4-report.md:42-59 · :93-96` · `review-be-3-report.md:6 · :18-20 · :49-50` |
| A11 | A13 저장소 dev 실물 | `fix-delivery-close-all-brief.md:18` · `review-be-3-report.md:24-28` |

파일: `…/work/fix/delivery/241/`(`fix.v7.*` · `review.*` · 이전 판 사본).

(경로 `pb2/` = `day-r3/orchestration/work/_archive/day/day-procedure-board-2/`. 코드 PR #238 하나에 #234 · #236 · #239 · #235 가 같이 들어가 있어 도구의 PR 쪽 review 댓글(marker 하나)은 마지막 review 로 덮인다 — Issue 쪽 closeout 기록 · 이 리포트 · `…/delivery/<번호>/review.request.json` 이 Delivery 별 근거다.)

## #234 — review 까지 기록 · 마감 대기(sync 문서 → 직접 닫기)

| 항목 | 값 |
|---|---|
| contract_version | **4** · risk L3 그대로 · Target Delta 그대로 |
| contract_digest | `sha256:5540b104de4ba88dea32fb214b23b958b2d6c04a658118d72fe49ee5786e79f2` |
| plan_digest | `sha256:9c74ce555f387afddc8fe094433bc07143dd5b9e21db1577219ad04bf1b83116` — **v3 승인과 같음 → 승인 유지**(범위 변경 없음 · 재결속만 · 새 receipt 없음) |
| baseline | ready @ `19f7e401` · missing `[]` |
| review-delivery | **recorded** — `conformant` · merged · 코드 PR #238 head `b8a59cc38f88f3cbb2a3f631d78bd10c1f5daf0d` · merge `aa7853cda2ded28042ebd693810d31b945f773b6` |
| per_spec | DAY-SPEC-000 `none` · DAY-SPEC-001 `none` · DAY-SPEC-002 `none` |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` · `implementation:conformant` · `spec-sync:pending` |
| next_action | `run-spec-sync` |

**뺀 수용 항목(그대로):**

- 없음 — 남은 실물 항목이 이미 근거가 있다(아래)

**남긴 항목과 근거(전부 pass):**

| id | 근거 |
|---|---|
| A1 | pb2/review-234-report.md:34-69(다른 not-supported 경로 PASS) · :71-76(A1 — test_kos_board_contract.py CC 5개 trial 없이 계획 · write_open 경로+값 · 다른 not-supported 경로 테스트 그대로) · pb2/review-236v3-report.md:12(격리 스택 scripts/test.sh -q 680 passed · infra 포함) · pb2/review-239b-report.md:61-62(같은 브랜치 전체 946 passed · ruff 통과 — PR #238 머지 전 마지막) |
| A2 | pb2/review-234-report.md:77-82(A2 — test_board_api.py 데모 · 실제 병원 픽스처 같은 op · not_supported 0) · pb2/_RESUME.md:115(be-234-fix1 — W2 귀가 대기 1 cancel-flow-tasks 단언 보강) · pb2/review-236v3-report.md:12(격리 스택 scripts/test.sh -q 680 passed · infra 포함) · pb2/review-239b-report.md:61-62(같은 브랜치 전체 946 passed · ruff 통과 — PR #238 머지 전 마지막) |
| A3 | pb2/review-234-report.md:83-88(A3 — test_emr_rules 구조 · test_emr_sync_service · test_auth_api) · pb2/review-236v3-report.md:12(격리 스택 scripts/test.sh -q 680 passed · infra 포함) · pb2/review-239b-report.md:61-62(같은 브랜치 전체 946 passed · ruff 통과 — PR #238 머지 전 마지막) |
| A4 | pb2/review-234-report.md:17-29(is_demo 동작 분기 0 · 칸 유지 · migration 없음) · pb2/_RESUME.md:115(be-234-fix1 — W3 is_demo 경계 tests/architecture 추가 · architecture 28 통과) · pb2/review-236v3-report.md:12(격리 스택 scripts/test.sh -q 680 passed · infra 포함) · pb2/review-239b-report.md:61-62(같은 브랜치 전체 946 passed · ruff 통과 — PR #238 머지 전 마지막) |
| A5 | pb2/review-234-report.md:29(trial · TRIAL_STEPS · kos_trial_writes_on_live · KOS_TRIAL_WRITES_ON_LIVE git grep 0) · :6-7(ruff 통과) · pb2/review-236v3-report.md:12(격리 스택 scripts/test.sh -q 680 passed · infra 포함) · pb2/review-239b-report.md:61-62(같은 브랜치 전체 946 passed · ruff 통과 — PR #238 머지 전 마지막) |
| A6 | pb2/_RESUME.md:89(사용자 2026-11-09 #234 A6 데모 실물 — 시작 취소 · 완료 취소 · 귀가 대기 1 · 2 · 재호출 모두 ✅) · :91(완료 취소 사용자 확인) |

- A6(데모 실물)은 빼지 않았다 — 사용자 2026-11-09 데모 확인 5개 모두 ✅ 가 기록돼 있다(`pb2/_RESUME.md:89 · :91`).

## #236 — review 까지 기록 · 마감 대기(sync 문서 → 직접 닫기)

| 항목 | 값 |
|---|---|
| contract_version | **4** · risk L3 그대로 · Target Delta 그대로 |
| contract_digest | `sha256:fd53bc590819f5a894038e83ecbd43d9660c75bec8328eae58134767c60b768d` |
| plan_digest | `sha256:1e4c9526094c4fe7a794a3b04e04f683d51bebdf64f6db770e144ced5d3bf24a` — 새 digest — 승인 적용(human · kknaksss · 근거 사용자 결정) |
| baseline | ready @ `19f7e401` · missing `[]` |
| review-delivery | **recorded** — `conformant` · merged · 코드 PR #238 head `b8a59cc38f88f3cbb2a3f631d78bd10c1f5daf0d` · merge `aa7853cda2ded28042ebd693810d31b945f773b6` |
| per_spec | DAY-SPEC-002 `none` |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` · `implementation:conformant` · `spec-sync:pending` |
| next_action | `run-spec-sync` |

**뺀 수용 항목(그대로):**

1. A1(①) 의 「화면 — 체크박스 켜짐/꺼짐 · 전체/부분 선택 스크린샷.」
2. A2(② · ③ · ④ · ⑤ · ⑦) 의 「화면 테스트(스크린샷 · 수동) — 고객 이름 누르기 없음 · 시술 이름 → 차트 모달(읽기 전용) · 「⋯」 호버 없이 보임 · 카드 안 스크롤이 끝/없으면 판 스크롤 · 상단 검색 칸(E06) 없음 · 판 카드에 경고 아이콘(E35) · 빨강 테두리 없음.」
3. A4(⑧ · ⑨ · ⑩) 의 「화면 — 판 카드 시술 줄에 [재호출] 없음 · 인박스 확인 필요 · 시술 대기 · 호출 탭 카드에 [재호출](5분 전 포함) · 누르면 창 없이 바로 · 글자 검정 · 확인 필요 카드 빨강 · 마취 초과 칩 빨강 · 팝업 없음.」
4. A5(⑪ · ⑫) 의 「화면 — 마취 자리 세 상태 스크린샷.」
5. A7(⑭) 의 「**데모 실물** — DAY dev(KOS 데모 지점)에서 원장을 바꾸면 KOS 집도의가 새 원장 1명으로 바뀌고 다음 조회가 그 값을 준다(실제 병원에는 쓰지 않음).」

**남긴 항목과 근거(전부 pass):**

| id | 근거 |
|---|---|
| A1(①) | pb2/review-236v3-report.md:60(A1 규칙 · API 테스트 이름) · pb2/review-236-be-report.md:46 · pb2/review-236-fe-report.md:51(전체 선택 렌더 테스트) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A2(② · ③ · ④ · ⑤ · ⑦) | pb2/review-236-be-report.md:47(A2 ③ API — 차트 라우트 · 그 밖 404) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A3(⑥) | pb2/review-236-be-report.md:48(A3 ⑥ 검색 infra 테스트) · pb2/review-236-fe-report.md:54(검색 화면 · 차트) · pb2/review-236v3-report.md:67(검색 칸 글자 「고객 · 원장 · 관리실」 copy 테스트) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A4(⑧ · ⑨ · ⑩) | pb2/review-236-be-report.md:49(A4 ⑧ ⑨ 확인 필요 단위 테스트) · pb2/review-236v3-report.md:61(A4 ⑩ 재호출 규칙 · API 테스트) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A5(⑪ · ⑫) | pb2/review-236-be-report.md:50(A5 마취 회차 · 귀가 대기 API) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A6(⑬) | pb2/review-236-be-report.md:51(값) · pb2/review-236-fe-report.md:58(줄 글자 렌더 테스트 test_수락_진행_완료_줄의_원장_글자) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A7(⑭) | pb2/review-236-be-report.md:52(A7 원장 바꾸기 API · outbox · event_log) · pb2/review-236v3-report.md:62(글자 「원장 변경」 · 거절 토스트 · 호버 테스트) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A8(⑮) | pb2/review-236-be-report.md:53(동시 수락 409) · pb2/review-236-fe-report.md:60(토스트 글자 · infra 웹 테스트) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A9(⑯) | pb2/review-236v3-report.md:63(test_확인_창은_medikit_ConfirmModal_모양) · pb2/review-236-fe-report.md:61(확인 창 · 닫기 · 되돌리기) · pb2/review-236-be-report.md:54(API 회귀) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A11(⑰) | pb2/review-236v3-report.md:64(카드 순서 규칙 · API 테스트) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A12(⑱) | pb2/review-236v3-report.md:65(반영 중 canUndoStart · 409 · web 테스트 — 더보기 같은 조각) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A13(⑲) | pb2/review-236v3-report.md:66(조작 응답 조각 · OOB · version 신호 web 테스트) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |
| A10 | SPEC-002 @ 19f7e401 에 「원장 변경」 · 「원장을 변경할 수 없습니다.」 · 「고객 · 원장 · 관리실」 있음(review-236-fe W1 · W4 글자는 사용자 결정 뒤 스펙 반영 — pb2/_RESUME.md:27) · pb2/review-236v3-report.md:12-13(격리 스택 scripts/test.sh -q 680 passed · 실패 0 · ruff 통과) · pb2/review-239b-report.md:61-62(PR #238 머지 전 같은 브랜치 전체 946 passed · ruff 통과) |

## #239 — review 까지 기록 · 마감 대기(sync 문서 → 직접 닫기)

| 항목 | 값 |
|---|---|
| contract_version | **2** · risk L3 그대로 · Target Delta 그대로 |
| contract_digest | `sha256:84933e3b7cbd4d8ec69c57eb3ae579921c799b6727052281d61f297f11226aa2` |
| plan_digest | `sha256:61f08a79e07935b9ac21bf12b1756242c38ccb471d7a18ad21ddb6df1aec9903` — 새 digest — 승인 적용(human · kknaksss · 근거 사용자 결정) |
| baseline | ready @ `19f7e401` · missing `[]` |
| review-delivery | **recorded** — `conformant` · merged · 코드 PR #238 head `b8a59cc38f88f3cbb2a3f631d78bd10c1f5daf0d` · merge `aa7853cda2ded28042ebd693810d31b945f773b6` |
| per_spec | DAY-SPEC-002 `none` · DAY-SPEC-000 `none` |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` · `implementation:conformant` · `spec-sync:pending` |
| next_action | `run-spec-sync` |

**뺀 수용 항목(그대로):**

1. A8(⑦) 의 「로컬 · dev DB 에 들어감 · 넣은 뒤 다음 동기화에서 판에 기타 작업이 보이고 「방 배정/」만 숨음」(로컬 DB 에는 2026-11-11 코디가 넣음 · dev 서버 DB 는 아직 · 판 관찰 기록 없음)
2. A9 **데모 실물**(DAY dev · KOS 데모 지점 — 실제 병원 쓰지 않음 · SPEC-002 OQ-38 · 39): ① 점유 이동 KOS 반영(작업 방 · 카드 방 · roomAssignedDateTimeUtc 가 새로 찍히는지) ② 복귀(「방 배정」 취소 · 원래 방) ③ 이동 ④ 「방 배정」 새로 만들기(add-flow-tasks → 다음 조회 sequence → change-tasks-room) ⑤ 진행 중 작업 이동 ⑥ change-tasks-room sequences 여러 개 한 요청 ⑦ 차트 메모(간호 · 의사) KOS 반영 ⑧ 의사차트 집도의 KOS 반영(수락 뒤) ⑨ KOS 웹 메모 수정 → DAY 반영 · 이력 「KOS」 ⑩ 담당자 빈 작업 메모 — 결과표(요청 2xx · 다음 조회 값 · outbox 상태)를 Issue 에 기록 → 결과는 spec-sync 로 SPEC-002 KOS 쓰기 표 · OQ-38 · 39.
3. A3 · A7 의 브라우저 실물 — 차트 자동 저장(blur · 2초) 타이밍 · 방 이름 팝오버 동작(review-239 W5 — 화면 테스트 · 정적 스크린샷까지만 됨)

**남긴 항목과 근거(전부 pass):**

| id | 근거 |
|---|---|
| A1(①) | pb2/code-239-report.md:59(A1 테스트 이름) · pb2/review-239-report.md:9(A1 ~ A8 · A10 서버 계약 스펙대로) · pb2/screens-239/a1-a7-board-etc-line-hold-band.png(기타 작업 줄 스크린샷) · pb2/code-239-report.md:12-13(test.sh 941 · not infra 658 passed) · pb2/review-239b-report.md:6(PASS) · :61-62(재리뷰 뒤 전체 946 passed · ruff 통과) |
| A2(②) | pb2/code-239-report.md:60(migration 테스트 · test_column_snapshot · 차트 이력 지우는 길 없음 · started_room_id) · pb2/code-239-report.md:12-13(test.sh 941 · not infra 658 passed) · pb2/review-239b-report.md:6(PASS) · :61-62(재리뷰 뒤 전체 946 passed · ruff 통과) |
| A3(③ · ④ 화면) | pb2/code-239-report.md:61(차트 화면 테스트) · pb2/screens-239/a3-chart-doctor-tab.png · pb2/screens-239/a3-chart-nurse-tab.png(두 탭 스크린샷) · pb2/code-239-report.md:12-13(test.sh 941 · not infra 658 passed) · pb2/review-239b-report.md:6(PASS) · :61-62(재리뷰 뒤 전체 946 passed · ruff 통과) |
| A4(④ API) | pb2/code-239-report.md:62(차트 저장 API 테스트) · pb2/code-239-report.md:12-13(test.sh 941 · not infra 658 passed) · pb2/review-239b-report.md:6(PASS) · :61-62(재리뷰 뒤 전체 946 passed · ruff 통과) |
| A5(④ 시술 전 · 동기화) | pb2/code-239-report.md:63(시술 전 의사차트 · 동기화 infra 테스트) · pb2/code-239-report.md:12-13(test.sh 941 · not infra 658 passed) · pb2/review-239b-report.md:6(PASS) · :61-62(재리뷰 뒤 전체 946 passed · ruff 통과) |
| A6(⑤ API) | pb2/code-239-report.md:64(점유 이동 · 이동 · 복귀 API 테스트) · pb2/review-239b-report.md:17-30(W1 「방 배정」 없는 점유 이동 순서 · 카드 방 — 닫힘) · pb2/code-239-report.md:12-13(test.sh 941 · not infra 658 passed) · pb2/review-239b-report.md:6(PASS) · :61-62(재리뷰 뒤 전체 946 passed · ruff 통과) |
| A7(⑤ · ⑥ 화면) | pb2/code-239-report.md:65(방 이동 팝오버 · 시술 완료 탭 원래 방 묶음 화면 테스트) · pb2/screens-239/a7-room-popover.png · pb2/screens-239/a1-a7-board-etc-line-hold-band.png(팝오버 · 파란 띠 스크린샷) · pb2/code-239-report.md:12-13(test.sh 941 · not infra 658 passed) · pb2/review-239b-report.md:6(PASS) · :61-62(재리뷰 뒤 전체 946 passed · ruff 통과) |
| A8(⑦) | pb2/code-239-report.md:27(scripts/seed_demo_connection.py env DAY_SEED_KOS_ROOM_ASSIGN_ETC_TASK_ID · 비면 안 넣음) · :66(test_room_assign_setting.py 3) · pb2/_RESUME.md:76(로컬 DB 에 env 값으로 넣음 — 코드 하드코딩 없음) |
| A10 | pb2/code-239-report.md:68 · pb2/code-239-report.md:12-13(test.sh 941 · not infra 658 passed) · pb2/review-239b-report.md:6(PASS) · :61-62(재리뷰 뒤 전체 946 passed · ruff 통과) |

- 판단 한 줄: A8 은 「값을 env 로 넣는 길(코드 하드코딩 없음)」만 남기고 dev DB 값 넣기 · 판 관찰은 넘겼다(dev 서버 DB 아직 · 관찰 기록 없음 — `pb2/_RESUME.md:76`). 빼지 않으면 근거 없는 pass 가 된다.

## #235 — 막힘(닫지 않음 · 아무것도 쓰지 않음)

| 항목 | 값 |
|---|---|
| 상태 | OPEN · `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending`(@ `9692e1fb`) · contract v8 · L3 — **그대로**(재결속 · scope delta · review 0) |
| 이유 | 브리프의 멈춤 조건 그대로 — 수용 53 개가 #241 이 뒤에 바꾼 계약과 부딪혀 판단이 갈린다. 예: A33 「채팅 이벤트 6종」(지금 7종 — `chat_member_read`, #241) · A45 · A50 「설정 = 원장 목록이면 [doctor_call] · 칸 = 「원장 호출」」(지금 채팅 활성 직원 = `chat` · 「채팅」 스위치, #241) · A14 「하단 메뉴 4개 」(지금 폰 대화 화면에서 숨김, #241) · A15 「배지 없음 · v7 까지 기준」. 또 첫 줄 「완료 정의」가 **코드 PR #237 의 새 head** 를 기준으로 잡는데 #237 은 #238 에 합쳐져 머지됐다(`pb2` 커밋 「merge: #237 채팅·알림·앱을 #238 최신 board 위에 합침」). 어느 항목을 #241 계약으로 갈음할지 · 낡은 항목을 뺄지 · 완료 정의를 #238 로 바꿀지는 결과 계약을 다시 쓰는 판단이라 사람 몫. |
| 사용자가 정할 것 | (가) #235 를 「#241 이 뒤 계약을 소유」로 보고 겹치는 항목(A14 · A15 · A33 · A45 · A50 등)을 #241 로 갈음 · 실물 항목은 다음 작업으로 넘기는 scope delta 를 승인해 닫기 / (나) #235 를 지금 계약 그대로 열어 두고 다음 작업에서 정리 / (다) 범위가 옛 계약이라 닫기만(도구 밖 · 마감 댓글에 사유) |
| 함께 남는 낡은 문장 | #235 마감 sync 몫이라 이번에 고치지 않음: SPEC-005 :26 「알림 API … 없다」 · N-1 · N-2 · SPEC-003 D-2 · D-5 · API 표 「푸시 기기 · 알림 목록 없음」 · SPEC-004 「지금 상태 — 정직 표기: 채팅 테이블만」 · C-1 「지금」 칸 · SPEC-001 「앱 환경 연결 — 구현 전」(:237 · :328 · :397) — 전부 #238 로 구현된 것 |

## 문서 sync 준비 (네 건 한 PR)

- 스펙 워크트리 `mediness-mediness/fix-spec` · 로컬 브랜치 **`kknaksss/day-delivery-close-sync`**(= `origin/main` `19f7e401` 에서 만듦 · 커밋 0)
- 바꾼 것:
  - `products/day/20-spec/spec-003-mobile-app.md` — 머리 한 줄(:55) · API 표 「통역」(**있음** — #242) · 서버 의존 D-3 「지금」 · 「통합 검증」(A-44 · A-45 · A-47 확인 · A-46 다음 작업)
  - `products/day/20-spec/spec-004-internal-chat.md` — 머리 한 줄(:34) · C-1 「서버 없음 · 다음 WP」 → 구현됨(#242) · C-3 「연결 문자열 방식이라 붙지 못함 → WP-BE-4」 → 관리 ID 연결 구현됨 · C-A27 ① 확인 · ② 다음 작업
  - `products/day/30-work.md` — Delivery 대시보드(도구 `sync_dashboard` 로 다시 그림 · 실제 ledger 에서 **#241 · #234 · #236 · #239 의 Issue 상태만 closed 로** 두고 그림 = 직접 닫은 뒤 ledger 와 같아 다음 fresh 실행이 `changed: false` · content_digest `sha256:2c504960fb5d32243377c52d575e2f259c0ae656e86ec47669f2d2c23077555a`) · Spec Coverage(covering Delivery · 상태: SPEC-002 done · 나머지 in_dev — #235 열림)
  - `products/day/log.md` — 1줄
- per_spec: #241 = SPEC-003 · 004 updated · 005 · 000 unchanged / #234 · #236 · #239 = 전부 unchanged(대시보드만)
- lint `--strict` → 0 error · `products/day` 줄 0
- 다음: 코디 커밋 · PR · 머지 → `[머지됨]` 받으면 네 Issue 에 마감 댓글 · `gh issue close --reason completed`

## 마감 (2026-11-11 · 코디 「[머지됨] mediness#932 7f7319ec…」 뒤)

| Delivery | 결과 | 마감 댓글 | 넘긴 검증 항목 |
|---|---|---|---|
| #241 | **CLOSED · completed** | https://github.com/MediSolveAIDev/CENTURION_DAY/issues/241#issuecomment-6790824297 | 5 |
| #234 | **CLOSED · completed** | https://github.com/MediSolveAIDev/CENTURION_DAY/issues/234#issuecomment-6790825175 | 0 |
| #236 | **CLOSED · completed** | https://github.com/MediSolveAIDev/CENTURION_DAY/issues/236#issuecomment-6790826040 | 5 |
| #239 | **CLOSED · completed** | https://github.com/MediSolveAIDev/CENTURION_DAY/issues/239#issuecomment-6790827056 | 3 |
| #235 | CLOSED · completed — **내가 닫지 않음** | 2026-11-11T08:18:39Z 「## 마감」 댓글 + 08:18:41Z closed(같은 GitHub 계정 · 다른 세션 — 댓글: 겹치는 수용 항목(A14 · A15 · A33 · A45 · A50 등)은 #241 · #242 가 소유) | — |

- 문서 sync PR = MediSolveAIDev/mediness#932 · 머지 `7f7319ec299c7ef4b904a6e66476c9d0e4997069`(head `e2aee21f…`).
- 라벨은 도구가 붙인 그대로(`implementation:conformant` · `spec-sync:pending`) — `spec-sync` · `complete-delivery` 는 mediness#749 로 실행 못 함(댓글에 한 줄).
- 마감 댓글 원문: `…/work/fix/delivery/<번호>/close-comment.md`.
- **다음 작업의 검증 목록 = 13 항목**(#241 5 · #236 5 · #239 3 — 각 Issue Non-Goals 와 마감 댓글에 그대로). #235 쪽 실물 항목(실기기 · TestFlight · APNs 수신 등)은 #235 마감 댓글이 정한 대로(내가 정리하지 않음).
- 남은 낡은 스펙 문장(#235 몫 — 이번 sync 에 안 넣음): SPEC-005 :26 · N-1 · N-2 · SPEC-003 D-2 · D-5 · API 표 「푸시 기기 · 알림 목록 없음」 · SPEC-004 「지금 상태 — 채팅 테이블만」 · C-1 「지금」 · SPEC-001 「앱 환경 연결 — 구현 전」 → 다음 작업 「문서 정리」 거리.
