
# 재개 노트 — day-data-architecture (day)

**지금**: Delivery #224 뼈대 구현 완료 · 코디 확인 통과 → 검수 WARN → fix1 반영 · 코디 확인 → **Code PR #228(CENTURION_DAY → v2-dev, 머지는 사용자 · 구현 뒤)** · **#225 구현 완료 · 코디 확인 → 검수 WARN → fix1 → **PR #228 커밋 `b6f23b42`** · SPEC-000 동기화 PR #909 `dcce1eea`**. **#226 완료 · PR #228 커밋 `8c85233a`** · **#227 로그인: v2 → 검수 WARN → v3(SPEC-001 CSRF · 빈 입력 개정 포함) → 검수 WARN 가벼움(kos-client-uri — HAR 로 답, SPEC-001 한 줄 planner) → backend 구현 발주**(Delivery 승인 라벨은 사용자 몫 · 미승인)(넘긴 것: W7 outbox 중복 발송 · SENT 정체 · 빈 expect + (visit_id, seq) 유일 migration = 첫 실제 쓰기 Delivery(SPEC-002) / W8 공용 계정 표시 위치 = 사용자 결정 — 정할 때까지 원장 목록에 공용 계정이 보일 수 있음)(코디 기본값: outbox 는 기반만 · 실제 KOS 쓰기 0 · 공개 API 이전 안 함 · 후보 목록만 · OQ-02-2 는 필드 확인만 · 실물 = 데모 지점 폴링 1회 필수 · 데모 접속값은 local.env 만). 열린 것(알림 · 채팅 때): account 에 달린 device · notification_setting · push_log · chat_member 는 병원 무관인지. #226 주의: 부분 유일이라 ON CONFLICT 에 WHERE deleted_at IS NULL 반복. 넘긴 것: prod 배포 = W7 키 canary / #226 = Redis timeout · 필수 bool 은 동기화가 전부 채움(진행 중 코디 허용: compose ENCRYPTION_KEY 1줄 · env.py import day.models · env.py autogenerate 비교 수정)(코디 기본값: product_option_id FK 없음 · 정해진 enum 은 DB 에서 막고 열린 enum 은 varchar · 07 그대로 · OQ-03-1 보류 칸 안 만듦 · 암호 키 없으면 기동 실패 · W6 timeout · day_test fixture). 넘긴 것: #225 브리프 = W6 쿼리 timeout · in-process 스키마 격리 / #226 브리프 = W5 Redis timeout 분리 · W9 worker migrate 의존 · 태스크 테스트 fixture / prod 배포 = W8 offline SQL · APP_ENV 필수 · 화면 단계 = 시안 DS gap 17종 · medikit 기준 HTMX 키트 1.3.0 추천 · 동작 규칙은 cc 구현 기준(마취 20 · 호출 5 · 카드/방 순서 · 탭)(CENTURION_DAY 워크트리 `day-data-architecture` · 브랜치 `kknaksss/day-data-architecture` · base `v2-dev`). PR #909 머지는 사용자가 구현 뒤에 한다 — 머지 요청하지 말 것. Delivery #224~#227(CENTURION_DAY) 생성 — 전부 `delivery-plan:review`(사용자 계약 승인 대기) · `spec-baseline:pending`(PR #909 머지 대기). PR #909 보정 커밋 `60fae27b`
**다음**: SPEC 먼저 닫는다(사용자 2026-11-05 — 「스펙도 없는데 wp를 만든거야?」): SPEC-001 로그인 · 세션(PR #909 에 같이) → 검수 → #909 머지 · SPEC 확정 → Delivery #224~#226 재결속 · 승인, #227 은 SPEC-001 기준으로 계약 다시 → backend 발주

세팅: `scripts/new-work.sh day day-data-architecture` · 설정 SSOT `config/projects/day.json`
코디handle: `term_70b6f193-86a2-4c1d-8965-4e2220cef9b3`

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` (branch `kknaksss/day-data-architecture-spec`, base `origin/main` → PR `main`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [!] mediness PR #909 — 사용자 리뷰 · 머지
- [ ] 워커 터미널 2개(planner · reviewer) 정리 — 머지 뒤
- [!] `reference/2026-11-03-cc-day/screen/시술현황_프로토타입.html`(3MB · 사용자 추가) — public 레포라 내용 확인 전 미커밋
- [!] planner 미결 13항(planner-report.md) — 사용자 판단 필요분 있음(product_option_id FK · ESC 기본값 · version · context/products.md 등)
- [!] 원천 문서가 `reference/2026-11-03-cc-day/erd/` 로 옮겨짐(사용자 · 내용 동일) + `screen/` 추가 — 프로필 미커밋
- [ ] PR — mediness `main`(spec 레포) · 원천 문서는 profile `kknaksss/day`(이미 push)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-06 | **medikit HTMX 기반 먼저**(시술 현황 화면 전) — 새 컴포넌트는 DAY 레포 안(ui.html · static · styles) · 키트 올릴 후보 목록 · CRM 브랜드색 · 상태 팔레트는 DAY 토큰 확장 · 별도 Delivery 로 #227 과 병렬(CSRF 연결만 #227 뒤) | 사용자 |
| 2026-11-06 | **CSRF = centurion admin 방식(403 csrf_failed · 로그인 전 미적용) · 빈 입력 = 400 invalid_request · 의사 호출 창 = 왼쪽 고르기(검색 · 모든 의사 · 원장+상태) / 오른쪽 선택된 시술**(원천 04-staff · procedure-board-decisions) | 사용자 |
| 2026-11-06 | **SPEC-002 사용자 OQ 닫음(추천대로)**: OQ-01 웹 = 화면 라우트 HTML 조각 · JSON 앱 전용 · OQ-04 재호출 = 시안처럼 고르는 창(모든 의사 | 원장 한 명 · 기본 = 처음 대상 — 처음 「모든 의사만」에서 바꿈) · OQ-07 실패 토스트만(KOS 에서 고치면 폴링이 맞춤) · 공용 계정 = 1차는 다 넣음(빼지 않음 · 처음 「뺄 id 목록」에서 바꿈) — 원천 procedure-board-decisions.md | 사용자 |
| 2026-11-06 | **단계마다 리뷰 자동** — 스펙 → WP → 코드 각 단계 done 이면 코디 확인 뒤 같은 턴에 reviewer 발주(묻지 않음) | 사용자 |
| 2026-11-06 | **시술 현황 화면 결정**(원천 `reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`): U1 담당의 있으면 호출 없이 시작 · U2 호출은 cc 팝오버 · U3 재호출 = 새 행 + 기존 호출 닫음 · U4 의사 본인 또는 간호사가 대신 · 남기는 건 수락한 의사만 · U7 cc 그대로(시술 3단계만 — 시술 준비 현황) · U6 빈 방 안 보임 · U8 · U10 cc 그대로 · U9 수납 필요 시안에 · U12 마취 · 호출만. U6 순서 = 카드 · 생성 순(먼저 생긴 게 앞) · D&D 로 바꿈 · U5 방 옮기기 · U11 차트 작성은 다음 스펙(HAR 뒤) | 사용자 |
| 2026-11-06 | 프론트 검수 먼저 — **시술 현황만**, 시안 ↔ 명동 업무 흐름(workflow-v2 · v3 경계) ↔ KOS HAR(main 체크아웃 · gitignore) ↔ cc-prototype 코드 ↔ SPEC-000 대조(reviewer) | 사용자 |
| 2026-11-05 | **유일(UNIQUE)은 살아 있는 행만**(부분 유일 WHERE deleted_at IS NULL) · **chat_room.direct_key 병원별 유일** — 원천 erd README · 07 반영 | 사용자 |
| 2026-11-05 | **코드 PR 은 #228 하나 — 시안(화면)까지 다 만들 때까지.** 백엔드 #224~#227 · 화면 전부 같은 브랜치 `kknaksss/day-data-architecture` 에 Issue 별 커밋으로 쌓는다. 묻지 말 것 | 사용자 |
| 2026-11-05 | 시술 현황 시안 = `screen/시술현황_프로토타입 (1).html` · medikit 에 없는 컴포넌트 있음 → frontend 워커 조사(있음/없음 목록) | 사용자 |
| 2026-11-05 | **구현 먼저 · 머지는 나중**(사용자: 「왜 자꾸 머지하라는 거야 일단 구현하고 머지할 건데」) — #224 계약 승인으로 보고 backend 발주 | 사용자 |
| 2026-11-05 | SPEC-001 로그인 · 세션 OQ 11개 전부 권장대로(경로 `/api/auth/*` · 웹 쿠키 `day_session` + 앱 Bearer · 세션 = KOS 토큰 만료 · 1차는 병원 직원만 · 2단계 인증 계정은 막고 안내(명동점 90개 중 0개) 등) | 사용자 |
| 2026-11-05 | ~~Delivery 를 SPEC 머지 전에 연다~~ → **SPEC 먼저 닫고 Delivery**. #227 은 대상 SPEC 없이 열린 것(코디 실수) — SPEC-001 뒤 계약 다시 | 사용자 지적 |
| 2026-11-05 | 백엔드 작업 계획은 mediness 새 규칙 — GitHub Delivery Issue(start-delivery). WP 파일 안 씀. 디자인 변동 가능 → 백엔드만, 로그인까지 4개 | 사용자 |
| 2026-11-05 | cc-prototype #20 — KOS 내부 API 브라우저 헤더 필수 → DAY 연동 · 로그인에 반영 | cc-prototype `77173cf` |
| 2026-11-03 | 테이블 설계 01~07 확정 — 원천 `reference/2026-11-03-cc-day/` | 사용자 칸 단위 검토(아티팩트 승인/반려) |
| 2026-11-03 | mediness 제품 slug `day` · ID prefix `DAY` | 코디(카탈로그 slug `day` · 스캐폴드 기본값) |
| 2026-11-03 | 검수 FAIL 대응: 원천 묶은 행 42개 분리(deleted_at NULL 허용) · `consultation_procedure` · `visit_occupied_resource_doctor` 칸 표 추가 · ESC-001 값 그대로 | 사용자 「둘 다 그대로 가고 재발주」 |
| 2026-11-03 | 컬럼 수준 계약은 SPEC-000(데이터 모델), architecture 는 관계 · invariant 만 | mediness `rules/document-pipeline.md` · selly SPEC-000 선례 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_256e3ec1a806` | `ctx_e497e1180940` | `day-data-architecture-spec-brief.md` | 완료(터미널 유지 — 수정 재발주용) |
| reviewer_doc | `term_441c2cdb-68e6-4463-b694-d8d6adfc7210` | `task_0fbf4462273f` | `ctx_6b32d164d0aa` | `day-data-architecture-review-doc-brief.md` | 1판 FAIL(터미널 유지) |
| planner SPEC-001 CSRF 개정 + #227 v3 | `term_33d8da4d-2ead-4828-bc2f-3316d4b4bbbe` | (task-list) | (dispatch) | `planner-spec001-csrf-delivery227-v3-instructions.md` | 발주 · 진행 → 끝나면 리뷰 자동 |
| planner #227 재계약 v2(SPEC-001) | `term_33d8da4d-2ead-4828-bc2f-3316d4b4bbbe` | (task-list) | (dispatch) | `planner-delivery227-v2-instructions.md` | 발주 · 진행 → 끝나면 reviewer 자동 |
| reviewer #226 fix2 재검수 | `term_93d7dafc-cadb-4d5c-b78f-2ebd18f0aafc` | `task_b99db8e4b21b` | `ctx_a79a0765ae1e` | `review-226-fix2-brief.md` | 완료 · PASS → **#226 커밋 `8c85233a`(PR #228)** |
| reviewer SPEC-002 fix1 재검수 | `term_75e030e5-a3f9-4ed9-96a9-489fef7ec748` | `task_a14f0d53b6df` | `ctx_124c805a9fda` | `review-spec002-fix1-brief.md` | 완료 · WARN · W1~W11 닫힘 · 새 N1(대리 수락 → 방문 뒤 쓰기 멈춤 서술) · N2(규칙 25 계정 — 코디 판정: sign-in 계정 하나 · OQ-11 다시 열림) → fix2 대기(planner 가 #227 재계약 끝난 뒤 발주) |
| backend #226 fix2(N1~N3) | `term_adbc21b4-456a-447f-8dc5-a3899532a4e5` | `task_f31756aff8ee` | `ctx_7600caad89ba` | `backend-226-fix2-instructions.md` | 완료 · 코디 확인(not infra 155 · 전체 222 · ruff) |
| planner SPEC-002 fix1(W1~W11 · 답 있는 OQ 닫기) | `term_33d8da4d-2ead-4828-bc2f-3316d4b4bbbe` | `task_5e5df92efb20` | `ctx_dc288a2290c5` | `planner-spec002-fix1-instructions.md` | 완료 · lint 0 · OQ 7 닫음 · 사용자 OQ 3(01 · 04 · 07) 대기 |
| reviewer #226 fix1 재검수 | `term_93d7dafc-cadb-4d5c-b78f-2ebd18f0aafc` | `task_a382c748f20f` | `ctx_fce434e5246b` | `review-226-fix1-brief.md` | 완료 · WARN · W1~W6 · 경계 닫힘 · 새 N1~N3 |
| backend #226 실물 확인 2(needs_master) | `term_adbc21b4-456a-447f-8dc5-a3899532a4e5` | `task_4840ee6b85b9` | `ctx_11b9e8fa45f7` | `backend-226-live2-instructions.md` | 완료 · needs_master 실물 1회 정상(잠금 skip 0 · 오류 0 · 로그 누출 0) |
| reviewer DAY-SPEC-002 문서 검수 | `term_75e030e5-a3f9-4ed9-96a9-489fef7ec748` | `task_a6d882be4de6` | `ctx_2d43268f7499` | `review-spec002-brief.md` | 완료 · WARN 11(FAIL 0) · 사용자 OQ 01 · 04 대상 · 07 복구 |
| backend #226 fix1(W1~W6 · 병원 경계) | `term_adbc21b4-456a-447f-8dc5-a3899532a4e5` | `task_42ebb6c6f004` | `ctx_89f641df77dd` | `backend-226-fix1-instructions.md` | 완료 · 코디 확인(not infra 153 · 전체 220 · ruff) |
| reviewer #226 코드 검수 | `term_93d7dafc-cadb-4d5c-b78f-2ebd18f0aafc` | `task_48ba455ecfc4` | `ctx_b25b91f03c06` | `review-226-brief.md` | 완료 · WARN(FAIL 0 · W1~W8) |
| planner DAY-SPEC-002 시술 현황 | `term_33d8da4d-2ead-4828-bc2f-3316d4b4bbbe` | `task_70c80e1f4154` | `ctx_7f6be83ad3f2` | `planner-spec002-instructions.md` | 완료 · 미커밋(lint 0) · 사용자 OQ 8 · HAR 요청 5 |
| reviewer 시술 현황 시안 검수(읽기 전용) | `term_e22da864-5b18-46cf-9db2-332b95aae73c` | `task_82e401a05433` | `ctx_75dfcc9a03ec` | `review-screen-procedure-brief.md` | 완료 · WARN · 결정 12 → 원천 `screen/procedure-board-decisions.md` |
| backend #226 KOS 연동 | `term_adbc21b4-456a-447f-8dc5-a3899532a4e5`(새 터미널 — 옛 `term_a35ac44d` 는 에이전트 없음) | `task_1fa1aed8d5fb` | `ctx_f04c9725151a` | `backend-226-brief.md` | 완료 · 코디 확인(203 passed · not infra 131/2.2s · KOS 쓰기 0) |
| backend #225 fix1(W1~W6 + 부분 유일 · direct_key) | `term_a35ac44d-5a0f-4901-9681-51c4c9b6de8f` | `task_e628c11fdab2` | `ctx_9302d3e803a7` | `backend-225-fix1-instructions.md` | 완료 · 코디 확인(153 passed · 부분 유일 8 · UNIQUE 제약 0 · 대조 51/51) — worker_done 없이 끝남 |
| planner SPEC-000 동기화(#225) | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_ab2374dfca48` | `ctx_382678641efc` | `planner-spec000-sync-instructions.md` | 완료 · PR #909 `dcce1eea` |
| reviewer #225 코드 검수 | `term_ad2a4487-a45e-4f07-bd10-b6fa67936898` | `task_94cd7c9fad9e` | `ctx_adf86ce0f990` | `review-225-brief.md` | 완료 · WARN(FAIL 0 · W1~W8) |
| backend #225 데이터 모델 | `term_a35ac44d-5a0f-4901-9681-51c4c9b6de8f` | `task_8a5467385cab` | `ctx_e467fd28fa38` | `backend-225-brief.md` | 완료 · 코디 확인(51 테이블 · enum 28 · 0002 · 80 passed · 대조 51/51) |
| backend #224 fix1(W1~W4 · W7 · 정리) | `term_a35ac44d-5a0f-4901-9681-51c4c9b6de8f` | `task_ce3aedaa6948` | `ctx_3cd0483672a2` | `backend-224-fix1-instructions.md` | 완료 · 코디 확인(37 passed · 무인프라 31/6 skip · ruff · compose ready 200 · day.ping) |
| reviewer #224 코드 검수 | `term_ad2a4487-a45e-4f07-bd10-b6fa67936898` | `task_7839c062a1d2` | `ctx_49ebc47c594f` | `day-data-architecture-review-brief.md` | 완료 · WARN(FAIL 0 · W1~W9) |
| frontend 조사(DS gap) | `term_8fb75a5f-ce60-4682-a22f-25481c9d3f39` | `task_e281fee9db7c` | `ctx_cef3e5796f11` | `frontend-ds-research-instructions.md` | 발주 · 진행(코디 워크트리 · 읽기 전용) |
| backend #224 | `term_a35ac44d-5a0f-4901-9681-51c4c9b6de8f` | `task_b55365041983` | `ctx_54b11e55fc04` | `day-data-architecture-be-brief.md` | 완료 · 코디 확인(compose · health 200 · 32 passed · ruff · day.ping) |
| planner SPEC-001 결정 반영 | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_23966603a026` | `ctx_f348cbceb7b3` | `planner-spec001-fix-instructions.md` | 발주 · 진행 |
| planner SPEC-001 | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_a536db100de3` | `ctx_34532b18e680` | `planner-spec001-instructions.md` | 완료(OQ 11) |
| planner delivery | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_226ed1ca2070` | `ctx_65b9ce7dbcbe` | `planner-delivery-instructions.md` | 완료(human gate) · request JSON → `delivery/` |
| planner arch | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_78d14ef22adb` | `ctx_51d128cdd28e` | `planner-arch-instructions.md` | 완료 · 검수 WARN → 해소 |
| planner 수정 1판 | `term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4` | `task_18d832312263` | `ctx_91b93dee59be` | `planner-fix-1-instructions.md` | 발주 · 진행 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/909 (`f92a8acb` · `974caeac` · `e71e3849` · `60fae27b` · SPEC-001 커밋)
- Delivery: CENTURION_DAY #224 뼈대(L2) · #225 데이터 모델(L3) · #226 KOS 연동(L3) · #227 로그인(L3) — plan_digest 는 `planner-delivery-report.md`
- 코드 레포: CENTURION_DAY v2-dev `8e4fb4b5` — AGENTS.md 「아직 정하지 않은 것」 로그인 · 배포 제거(사용자 2026-11-05)
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-05` 40-architecture 추가(planner) → 검수 WARN(정본 낡음) → AGENTS.md 갱신 · PR #909 커밋
- `2026-11-03` 수정 2판 → 재검수 PASS → mediness PR #909
- `2026-11-03` 검수 FAIL → 원천 수정 · planner 수정 1판 발주
- `2026-11-03` planner 완료 → reviewer_doc 발주
- `2026-11-03` 사용자 승인 → planner 발주(run `run_86b1e890ecc2`)
- `2026-11-03` new-work.sh · `products/day` 스캐폴드(`scaffold-product.sh day DAY DAY`) · planner 브리프 작성

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
