
# 재개 노트 — interview1-update (sc-ax)

**지금**: **폐기 (2026-09-03)** — mediness 반영 취소. 사용자 결정: sc-ax baseline 갱신은 하지 않고, 인터뷰 원료는 프로필 레포 `references/2026-08-28-sc인터뷰-경영관리부/` 로만 보존
**다음**: 없음. 워크트리·브랜치(`interview1-update-spec`) 삭제 완료 — 미커밋 수정 13파일 폐기

세팅: `scripts/new-work.sh sc-ax interview1-update` · 설정 SSOT `config/projects/sc-ax.json`
코디handle: `term_915b3ecb-68dd-4d26-98f7-ef3f645318fb`

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec` (branch `interview1-update-spec`, base `origin/sc-ax` → PR `sc-ax`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

(없음 — 2026-09-03 폐기로 전부 닫힘. ①baseline 산출물 미커밋 폐기, ②planning·③보고서 미착수 종료)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-08-28 | 작업 순서 ①baseline 업데이트 ②planning 업데이트 ③회의결과 보고서 | 사용자 지시 |
| 2026-08-28 | 실작업 전 사전 조사 2건을 read-only 병렬 발주 | 사용자 지시 |
| 2026-08-28 | 인터뷰 원료 SoT = `references/2026-08-28-sc인터뷰-경영관리부/` (발견지도·회의록·트랜스크립트) | 사용자 제공 + prod DB 추출 |
| 2026-08-28 | ③ 보고서 = 고객사용 덱, `00-baseline/present/interview-1-report/` (kickoff-report 패턴) | 사용자 선택 (조사 B Q1 후보 A) |
| 2026-08-28 | 기능 공백 5건 = ②에서 새 FTR 추가 (범위 확대 승인) | 사용자 선택 (조사 B Q6) |
| 2026-08-28 | 돌발유입(AS-010) = baseline 2.3 신규 대분류 PR-7 승격, 전파 갱신 포함 | 사용자 선택 (조사 A 미결5) |
| 2026-08-28 | M-11/12 차수 재배치 = 이번엔 기록만, 재배치는 고객사 협의 사안 | 사용자 선택 (조사 A 미결6) |
| 2026-08-28 | 발주 방식 = 한 번에 묶지 않고 baseline 정의서부터 결정 하나씩 사용자 검토 후 진행 | 사용자 지시 |
| 2026-08-28 | baseline 결정 1 = 질문지가 D-4 원장. `00-baseline/interview/` 신설(README=회차 대장 + 01-questions-mgmt-1.md), html→md 반입이 첫 작업. 실명→역할명 치환 | 사용자 승인 |
| 2026-09-03 | **작업 폐기** — mediness sc-ax baseline 반영 취소, 워크트리·브랜치 삭제. 프로필 레포에는 references 원료만 보존 | 사용자 지시 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner(조사A) | `term_56ddde23-9bda-4d15-b749-d98bd2c88703` | `task_6ea315e970fb` | `ctx_7566cccba204` | `interview1-update-survey-baseline-brief.md` | 완료 (diff 0 검증) |
| planner(T1 질문지 반입) | `term_56ddde23-9bda-4d15-b749-d98bd2c88703` | `task_70a4cd418bb5` | `ctx_f03a5663767d` | `interview1-update-baseline-t1-questions-brief.md` | 완료 (코디 검증 통과 — 사용자 리뷰 대기) |
| planner(T2 결과 등재) | `term_56ddde23-9bda-4d15-b749-d98bd2c88703` | `task_2ec54e0153c0` | `ctx_4aedac743ce7` | `interview1-update-baseline-t2-register-brief.md` | 완료 (코디 검증 통과) |
| planner(T3 본문 반영) | `term_56ddde23-9bda-4d15-b749-d98bd2c88703` | `task_97a19653eca2` | `ctx_42b9d6a4a4cf` | `interview1-update-baseline-t3-apply-brief.md` | 완료 (코디 검증 통과 — PR 43→61·PR-7 신설) |
| planner(T4 요약 동기) | `term_56ddde23-9bda-4d15-b749-d98bd2c88703` | `task_e46216901d6e` | `ctx_6e2b73dfad8b` | `interview1-update-baseline-t4-summary-brief.md` | 완료 (코디 검증 통과) |
| planner(조사B) | `term_103bfd52-e1c5-432d-8c8f-b6bf090616b3` | `task_9e60697cb957` | `ctx_a78263997291` | `interview1-update-survey-planning-brief.md` | 완료 (diff 0 검증) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- 리포트: `survey-baseline-report.md` · `survey-planning-report.md` (완료 — 갱신지점 a8/b6/c10 · 파생 대조표 · 보고서 착지 3안)
- spec PR: 없음 (조사 단계)

## 5. 이력 (최신이 위)

- `2026-08-28` 조사 A·B 병렬 발주 (터미널 2개, 같은 워크트리 read-only 공유)
- `2026-08-28` sc-ax 프로젝트 세팅 — config·roles 신설, 원격 `sc-ax` 브랜치 생성(main 동형), 워크트리 생성
