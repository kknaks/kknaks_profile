# 발주서 — phub-recommend 회고(SUMMARY) + 개념 소화

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (브랜치 kknaksss/phub-recommend-archive).

## 1. 배경

`orchestration/work/phub-recommend/`(Procedure Hub 추천 · 골드 그래프 허브 · 실버 1~9단계 · ERD v1~v3.3 · hub-evals · 상담 앱 · 10-26 ~ 11-08)는 11-08 「ERD 설계 바탕 틀림」 판정으로 멈췄고, 이어진 작업 `phub-ledger-redesign` 은 11-16 마감 · 아카이브됐다. 사용자 지시(11-16): **phub-recommend 도 이전 작업이라 아카이브 · 회고 · 개념까지 다 쌓는다.** 코드 PR(PROCEDURE-HUB #31)은 머지하지 않고 참고용으로만 남는다.
**이 레포(kknaks_profile)는 PUBLIC** — 키 · 토큰 · 실명 · 내부 URL 0. 회사 데이터 원문(원장 문장 · 시술 설명)은 회고 · 개념에 옮기지 않는다(숫자 · id · 결정 · 방법만).

## 2. 읽을 것

- 꼴: `templates/orchestration/work-summary.md`(규칙 전부) · 같은 프로젝트 선례 `para/projects/company/procedure-hub/log/2026-11-16-phub-ledger-redesign.md`
- 정본: `orchestration/work/phub-recommend/_RESUME.md` 전부 · `HANDOFF-2026-11-05.md` · `HANDOFF-2026-11-08.md`(있으면) · DEC-001~003 · DATA-001 · ERD-FROZEN.md · erd-v*-review · app-*-report · 그 밖 리포트(필요한 만큼)
- **이미 있는 단계 기록**(같은 작업의 중간 기록 — 회고는 이것들을 링크하고 반복하지 않는다): `para/projects/company/procedure-hub/log/2026-10-30-gold-decisions.md` · `2026-10-30-quality-eval.md` · `2026-10-30-semantic.md` · `2026-10-30-silver-step7-site-rules.md` · `2026-11-01-silver-step9-explanations.md`
- 코드 쪽 사실(읽기만): PROCEDURE-HUB PR #31(`gh pr view 31 --repo MediSolveAIDev/PROCEDURE-HUB`) · 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` 의 `git log origin/release/v1.2.0..HEAD --oneline`
- 개념: `orchestration/runbook.md` 240~250줄(개념 소화 절차) · `para/areas/area.md` §3 · §3.4 맵 · 최근 개념 소화 커밋 꼴(`git log --oneline -10 -- para/areas/concept`)

## 3. 쓸 것

1. **`orchestration/work/phub-recommend/SUMMARY.md`** — 템플릿 꼴(맨 위 `---` 아래부터). 작업 전체(10-26 ~ 11-08)를 덮는다:
   - 결과 줄: 「11-08 ERD 설계 바탕 틀림 판정으로 중단 → phub-ledger-redesign 으로 재설계(11-09 ~ 11-16) · 코드 PR #31 머지 안 함(참고용)」.
   - §2 · §3 은 **가장 오래 막힌 구간**과 판단이 갈린 곳(ERD 를 키 · 트리로 먼저 그린 것이 왜 세 번 실패했나 · 실버 단계 순서 · hub-evals 결과 · 골드 그래프 허브 · 상담 앱 구조(Jev 슬롯 · LLM 은 앱 쪽) · 사고 기록 등) — _RESUME · 리포트로 확인한 사실만.
   - §4 결정 표(큰 결정) · §5 날짜별 로그(하루 한 줄 이상) · 단계 기록 5개 링크.
   - archive-work.sh 가 이 SUMMARY.md 를 `para/projects/company/procedure-hub/log/<날짜>-phub-recommend.md` 로 옮긴다(파일 이름은 스크립트가 정함 — 네가 그 자리에 따로 만들지 않는다).
2. **개념 소화** — SUMMARY §2 각 항목을 `para/areas/area.md` §3.4 맵에서 찾아 기존 개념 노트 보강(없을 때만 신규 + 맵 등재) · SUMMARY §2 항목에 `[[개념]]` 역링크. phub-ledger-redesign 소화(11-16 커밋 96f98201)에서 이미 보강한 노트는 겹치지 않게 이 작업 몫만 덧붙인다.

## 4. 규칙 · 금지

- 바꾸는 파일: `orchestration/work/phub-recommend/SUMMARY.md`(새) · `para/areas/concept/**` · `para/areas/area.md`(맵 등재가 필요할 때만). 그 밖 변경 금지. 커밋 · push 금지. PROCEDURE-HUB 워크트리 변경 금지(읽기만).
- 지어 쓰지 않는다. 끝나면 grep 으로 원문 인용 · 비밀값 · 내부 URL 0 확인 — 결과를 완료 보고에.

## 5. 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-recommend/SUMMARY.md`) — 보고에 보강 · 신규 개념 · 역링크 목록.
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "phub-recommend 회고 · 개념 완료" --enter`
