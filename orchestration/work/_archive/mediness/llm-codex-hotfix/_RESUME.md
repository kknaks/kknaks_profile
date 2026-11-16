
# 재개 노트 — llm-codex-hotfix (mediness)

**지금**: 마감 — 운영 배포·D·B 실호출 성공 · dev 반영 #154 · C 백필·W47 재채움 안 함(사용자) · archive-work.sh 진행
**다음**: 없음 — 잔여는 SUMMARY §7

세팅: `scripts/new-work.sh mediness llm-codex-hotfix` · 설정 SSOT `config/projects/mediness.json`
코디handle: `term_4d39f44d-7335-41dc-bd4a-b274304b05d9`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `app_main`(핫픽스): `/Users/kknaks/orca/workspaces/mediness-app/llm-codex-hotfix-hotfix` (branch `kknaksss/llm-codex-hotfix-hotfix`, base `origin/main` → PR `main`)
- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/llm-codex-hotfix-spec` (PR #942 → `mediness`)
- `app`(조사용, 변경 없음): `/Users/kknaks/orca/workspaces/mediness-app/llm-codex-hotfix` (branch `kknaksss/llm-codex-hotfix`, base `origin/dev` → PR `dev`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [x] CI 복구 — 인프라가 ARC 를 GitHub App 으로 교체 + 코디가 stale listener 삭제(사용자 승인) → 재실행 3회차 빌드 성공 · ~~`arc-system/medisolve-arm64-…-listener` 403 `You must be an org admin or have the runners and runner groups fine-grained permission` (03:17 UTC 확인)~~
- [x] Phase 3 D 주간 1회: homepage v1.6.0 · bytes=5178 · parse OK(W·W+1)
- [x] Phase 3 B 게이트 1회: recommend_with_ai · bytes=68557 · fallback=False · title 있음
- [!] Phase 3 C 브리프 — 11-13 백필(publish=git 커밋) 여부 사용자 확인
- [x] 회고 SUMMARY 초안 · 개념 보강 3(argv-length-limit · tool-allowlist-by-phase · externalized-configuration)
- [ ] Phase 3 실물 확인: back 로그 `server_llm final_prompt … provider=codex` · 06:00 브리프 PUBLISHED+본문 첫 줄 · C bytes < ~120,000 · D 파드 내 1회 · B eval_decision_gate 1건
- [ ] 후속(별도): A AX 비서 — back 에 codex 마운트·인증(GitOps 차트) + DEPLOY §4-4 k8s 기준 개정
- [!] 이 워크트리는 base origin/dev — 핫픽스 코드는 main 기준(app_main 워크트리)이 필요할 수 있음

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-13 | 서버 LLM 호출을 claude → codex 로 핫픽스 | 사용자 지시 |
| 2026-11-13 | 사용자 PC 데몬 `agent/` 는 범위 밖(개인 로컬) | 사용자 |
| 2026-11-13 | 판단 기준은 코드 기본값이 아니라 운영 배포 env | 사용자 지시 |
| 2026-11-13 | codex 로 살린다 — 이번 범위 B·C·D(코드), A 는 인프라 후속 | 사용자(「코덱스로 살릴거야」「그렇게 가자」) · survey 리포트 |
| 2026-11-13 | 코드는 main 기준 핫픽스 → main→dev 반영 | 코디 기본값(운영=main) |
| 2026-11-13 | WP-133 승인. 테스트 작성·실행 생략(CI 가 테스트 안 돌림 확인) — 수용은 Phase 3 실물 호출로 | 사용자 |
| 2026-11-13 | 설정 키 = 공용 한 벌(Open ① ⓐ) | 코디 기본값(WP 권장) |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| infra | `term_dd2f12cb-195c-40ee-ae67-7cadfce68bf3` | `task_e6c0675bfacb` | `ctx_c4bbb1a04fe2` | `llm-codex-hotfix-infra-brief.md` | 완료·release (run `run_dafa8505e142`) |
| planner | `term_7c6d1054-c63d-4781-a69b-faa689f5bcfb` | `task_4c5bddea8ad9` | `ctx_d2eb13bf5e9c` | `llm-codex-hotfix-spec-brief.md` | 완료·release |
| reviewer_spec | `term_b9963c8b-5ebc-46cd-a18f-6897c9485cc2` | `task_66c1d1018ec5` | `ctx_319fb6d76c73` | `llm-codex-hotfix-review-spec-brief.md` | 완료 WARN·release |
| backend_hotfix | `term_ffb55a13-10b5-4db8-902e-149e4df17ee5` | `task_315e855f71b0` | `ctx_128d501775be` | `llm-codex-hotfix-be-hotfix-brief.md` | 완료·release |
| reviewer_code_hotfix | `term_d626f8c9-8298-4e5c-9a9f-a33f6c117839` | `task_37b1653cb22c` | `ctx_dd4b37771416` | `llm-codex-hotfix-review-code-hotfix-brief.md` | PASS·release |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/942
- code PR: https://github.com/MediSolveAIDev/mediness-app/pull/153
- 리포트: `review-spec-report.md`(WARN) · `survey-prod-claude-usage.md` — 코디 확인: worker 로그 차단 에러 8건(11-10~13), back codex:none · driver=claude 직접 재확인
- 커밋: `ebbb2e42` — fix(back) 서버 LLM claude→codex (WP-133) · spec `3f63221c`

## 5. 이력 (최신이 위)

- `2026-11-13` ARC 복구·배포 6f175d80 · 실물 D·B 성공
- `2026-11-13` #153·#942 머지 → CI queued: ARC 리스너 403 크래시 루프 발견 · 회고 초안·개념 보강
- `2026-11-13` reviewer_code PASS → code PR #153
- `2026-11-13` backend_hotfix 완료 — 공용 키 SERVER_LLM_PROVIDER/SERVER_CODEX_MODEL, 신규 server_llm_submission.py → reviewer_code_hotfix 발주(config 에 reviewer_code_hotfix 추가)
- `2026-11-13` 사용자 WP 승인·테스트 생략 → spec PR #942 · config 에 backend_hotfix 추가 · 코드 발주
- `2026-11-13` planner 수정 1차 완료(WARN 6 반영 확인) → 사용자 리뷰 요청
- `2026-11-13` reviewer_spec WARN 6 → planner 수정 재발주
- `2026-11-13` planner 완료 — WP-133 신설(Open 5) → reviewer_spec 발주
- `2026-11-13` 사용자 codex 전환 확정 → planner 발주(spec 워크트리 llm-codex-hotfix-spec)
- `2026-11-13` infra 실측 완료 — prod=main 67b6a7dc, A·C·D(+B) claude·이미 실패, E·F codex 정상
- `2026-11-13` 코드 grep 으로 서버 claude 경로 후보 6개 추림 → 운영 env 실측을 infra 워커에 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
