# 재개 노트 — cc-nav-resv (cc-prototype)

**지금**: 배포 완료(2026-10-15) — 코드 kknaksss/cc-prototype#2(main 339293e) · infra MediSolveAIDev/k8s_infra_mac#20 · 시나리오 Secret seed.json 갱신 · 배포 DB 재시드 · 운영 확인 OK. 문서 PR kknaks/kknaks_profile#95 OPEN
**다음**: 문서 PR #95 머지 → 10-16 시연 → archive-work.sh(회고 · 개념 · 잔디)

세팅: `scripts/new-work.sh cc-prototype cc-nav-resv` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_aa31d360-73a0-4b4d-bc7b-a073df3ab46e`
문서: BASE-006 · DEC-004 · SPEC-002 0.1.0 · WORK-002 (`para/projects/summer-star/cc-prototype/`) — 아직 커밋 안 함

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv` (branch `kknaksss/cc-nav-resv`, base `origin/main` → PR `main`) — 두 워커 공유, 시안 워커는 리포 파일 무수정

## 1. 지금

- [x] frontend(WP1) 완료 보고(tsc · lint · build 통과) · 코디 화면 확인(3610/8610 로컬, 데스크 · 의사 · 1440 · 390 햄버거) OK — 미커밋. 미결: 현황판 왼쪽 medikit Menu 사이드바(헤더와 중복) 처분
- [x] frontend(시안 WP3) 완료 — claude design 「Ceramique 예약관리 v1」(scene 9) · 「Ceramique 현황판 폰 v1」 업로드 · design-report.md. **사용자 시안 검토 대기**
- [x] WP2 완료 · 코디 화면 확인(390 Aside · 접수 모달 · 1024 1차 그대로) OK — 미커밋
- [x] WP4-BE 완료(pytest 65 · ruff) · 리포트 `wp4-be-report.md` · 8610 재기동 · smoke OK — 미커밋. 주의: 예약 조작도 version 을 올려 그 직후 현황판 [되돌리기]는 400(의도된 동작으로 둠) · KOS operationId 미확인
- [x] WP4-FE 완료(tsc · lint · build) · 코디 E2E(3610/8610, 데스크 1440): 요청 → 등록 미리보기 → 확정 → 스크린샷 → 변경 요청(사유) → 수정 요청 → 수정 미리보기 → 수정 확정 · 콘솔 에러 0 · API 로 고객 시간 변경 갈래 · 409/400 · reset OK — 미커밋
- [!] 10-16(금) 시연에 들어가야 함 · 스크린샷 원본: 사용자가 준 KOS 예약 카드 캡처 `reference/2026-10-12-cc-prototype/kos-screenshot/`(실제 고객 정보 · gitignore) — 모양만, 값은 가짜

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-14 | DEC-004 D-01 ~ D-18 | 사용자 대화(BASE-006) |
| 2026-10-14 | 데스크 계정 헤더 = `현황판 \| 예약관리`(내 스케쥴 없음) · 폰 경계 760px | 코디 기본값 통보 |
| 2026-10-14 | 폰 현황판 = 1차 Aside 그대로(새 폰 시안 안 씀) · 예약관리 = 시안 v1 그대로 · 기존 디자인 무변경(사이드바 유지) | 사용자 — DEC-004 D-19 ~ D-21 |
| 2026-10-14 | 시안 워커 + 코드 워커 병렬 | 사용자 「시안 작업 워커랑 코드 작업 워커로」 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| frontend(WP1→WP2) | `term_d5b9a7c3-f61a-48d1-ac69-e9ad27be8c9c` | `task_be8a1f042f0e` | `ctx_697d7a8ea683` | `wp4-fe-brief.md` (`task_f82151d85d8b` · `ctx_214364686a31`) | 완료 (WP1 · WP2 · WP4-FE 검수 OK) |
| backend(WP4) | `term_288dbb43-d8f8-4ae8-af87-a78d977d4052` | `task_8480e27a6412` | `ctx_54fab98e1c60` | `wp4-be-brief.md` | 완료 |
| frontend(시안) | `term_cf31eb74-73ab-48d9-a1d5-39963a681edc` | `task_4a3c1833a7ef` | `ctx_5535a6cc7310` | `cc-nav-resv-design-brief.md` | 완료 · 사용자 검토 대기 |

## 4. 산출물

- spec PR: kknaks/kknaks_profile#95
- code PR: kknaksss/cc-prototype#2 (squash 339293e) · infra MediSolveAIDev/k8s_infra_mac#20 (c3c8d64)

## 5. 이력 (최신이 위)

- `2026-10-15` 배포: 코드 #2 · infra #20 · Secret · 재시드 · 운영 확인 · 문서 PR #95 · 로그인 실명 4개 교체(이력은 남김 — 사용자 「괜찮아」)
- `2026-10-15` fix5 완료 · 코디 확인 OK
- `2026-10-15` batch-5 → SPEC 0.3.3 → fix5-FE 발주
- `2026-10-15` fix4 완료 · 코디 E2E OK
- `2026-10-15` fix3 완료 · batch-4 → SPEC 0.3.2 → fix4-FE 발주
- `2026-10-15` batch-3 → SPEC 0.3.1 §5.3 → fix3-FE 발주
- `2026-10-15` fix2-FE 완료(+memo.tsx addendum) · 코디 E2E OK
- `2026-10-15` fix2-BE 완료(pytest 75) · 리포트 `fix2-be-report.md` · 8610 재시드
- `2026-10-15` 기획자 피드백 BASE-007 판단 정리 → D-23~35 · SPEC-002 0.3.0 → fix2 BE · FE 발주 · 코디handle term_aa31d360 으로 바뀜
- `2026-10-14` fix1 완료 · 코디 확인 OK · 코디handle 이 term_a8da76a5 로 바뀜(덮어씀)
- `2026-10-14` WP4 완료 · 코디 E2E OK · 사용자 피드백 batch-1 → fix1 발주
- `2026-10-14` 시안 검토 → D-19~21 · SPEC-002 0.2.0 · WP2 · WP4-BE 발주
- `2026-10-14` slug 생성 · 문서 4종 작성 · WP1 · 시안 발주
