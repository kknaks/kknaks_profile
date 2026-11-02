
# 재개 노트 — work-001-data-foundation (ontology-demo)

**지금**: WORK-001~005 전건 완료·커밋(8커밋)·**코드 PR #33** + 문서 PR #32 오픈. 최종 413 passed/5 skipped. 사용자 아침 E2E 대기.
**다음**: 사용자 로컬 E2E(README 「로컬 E2E」 7단계 — .env 비번 → 빌드 → redis+워커 → MCP·API → front dev → 게이트 → 채팅 R-1·R-2+하이라이트 육안 4항) → 통과 시 PR #32·#33 머지 → 홈서버 배포(README 「배포」) → archive-work.sh(SUMMARY).
**코디 핸들**: `term_9b07d036-3622-4fc7-9d9e-a5fda263b871` (구 45e793be stale — 워커들은 preamble 규약으로 정상 보고).

세팅: `scripts/new-work.sh ontology-demo work-001-data-foundation --workers backend` · 설정 SSOT `config/projects/ontology-demo.json`
코디handle: `term_45e793be-0adb-44c7-9d9a-eb35c4f48320`

## 워크트리

- `app`: `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation` (branch `kknaksss/work-001-data-foundation`, base `origin/ontology-demo` → PR `ontology-demo`)

## 1. 지금

- [x] WORK-001 완료 — 1차 검수 FAIL(차단3) → fix(97 passed·실패주입 7본) → **재검수 PASS** → 커밋(BE 24파일)
- [x] WORK-002 완료 — 검수 FAIL(차단1·경고8)→fix→코디 직접 검증(257 passed·AC-8 54, 재검수 갈음)→커밋
- [x] WORK-004 완료+fix 커밋 (검수 PASS)
- [x] WORK-003 완료 — 검수 WARN→fix→코디 검증(383 passed)→커밋. 게이트 4·5 라이브 통과
- [~] **backend WORK-005 진행** — task_f4da2df3c086, **새 핸들 `term_3fb7e8e1-146c-49ea-b990-1e0b3b35be77`** (구 term_7d777e3b 터미널 사망·재생성). 통합 검증·PII 스캔·배포 구성·아침 E2E 절차서
- [~] frontend 계약 동기 소태스크 — task(is_error·RETRY_NOT_ALLOWED·주석 정리·픽스처 대조)
- [ ] 전건 완료 → 최종 커밋 → 코드 PR 1건 + 문서 PR #32 → 아침 브리핑
- [x] frontend WORK-004 완료 — 검수 PASS·커밋. 후속 픽스(task_2e362fb1ba8e: W2 hex 단일화·W3 window_days·◀ has_prev_period·sign U+2212·error_code 대비) 진행
- [ ] docs 대기열: 현재 태스크(sign·status) 완료 후 → SPEC-003 에 source_group(tables 응답)·error_code(채팅 실패) 등재 발주
- [ ] WORK-002 완료 → 검수 → 커밋 → WORK-003(에이전트·채팅, 조사 §5.5·§5.6 확정값) 발주
- [ ] 코드 PR 은 전 WP 완료 후 1건 (사용자 지시)
- [!] FE 산출물은 미커밋 유지(WORK-004 완료·검수 후 커밋). promo v2 는 silver source_id 로 해소됨
- [!] 문서 SSOT 는 docs-baseline 워크트리 절대경로 (문서 PR #32 미머지 — 머지되면 base 에 들어옴)
- [!] WORK-004(프론트)는 디자인 조정 대기 20건 해결 전 발주 금지 — 사용자가 DESIGN_FEEDBACK.md 들고 디자인 세션 예정

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-02 | WP 5건·22 phase (10건 분할 축소 — 태스크는 WP 안 phase) | 사용자 지시 |
| 2026-09-02 | BE 순차(001→002→003) 진행 중 디자인 세션 병행, WORK-004 는 그 뒤 | 사용자 합의 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| frontend | `term_72270375-ebd6-4edf-935a-cd20e899d44f` | `task_855048fe5fc8` | `ctx_462527f158e6` | `work-004-frontend-fe-brief.md` | 진행 — WORK-004 P1~P4, mock 선행(env 스위치), app/front 만 |
| reviewer | `term_d753f8ab-5db6-4d08-8ce3-b2285fc2e34d` | `task_ac815760f528` | `ctx_5b50b396df8a` | `review-work-001-brief.md` | 진행 — WORK-001 검수 |
| backend | `term_7d777e3b-6ab5-4373-8bad-9ccaeea377d1` | `task_ab19b4399636` | `ctx_86e01000f4db` | `work-001-data-foundation-be-brief.md` | 완료 — P1~P5·게이트 전항. 검수 PASS 후 커밋 → WORK-002 이어 발주 |

(참고: `term_d673441f…` 는 같은 워크트리의 빈 셸 — 발주 대상 아님)

## 4. 산출물

- 문서 PR: https://github.com/kknaks/kknaks_profile/pull/32 (baseline→decision→spec→work 전체, 병합 대기)
- 코드 PR: <완료 후>

## 5. 이력 (최신이 위)

- `2026-09-02` WP 5건 승인 → work 커밋·푸시(f40bfcf, PR#32 갱신) → WORK-001 발주(task_ab19b4399636)
