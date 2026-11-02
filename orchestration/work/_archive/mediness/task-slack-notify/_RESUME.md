# 재개 노트 — task-slack-notify (mediness)

**지금**: 코드까지 완료 — spec PR #686 + code PR #145 둘 다 오픈, 사용자 리뷰·머지 대기.
**다음**: dev→main 릴리스(회의 후 사용자 승인) → 내일 09:00 prod 첫 리포트 확인. env·봇 초대·테스트 발송(17명, C레벨 제외)은 완료.

세팅: `scripts/new-work.sh mediness task-slack-notify` · 설정 SSOT `config/projects/mediness.json`
코디handle: `term_d5bec05e-881f-4a29-a144-fd73be7e23c4`

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/task-slack-notify-spec` (branch `kknaksss/task-slack-notify-spec`, base `origin/mediness` → PR `mediness`)
- `app`: `/Users/kknaks/orca/workspaces/mediness-app/task-slack-notify` (branch `kknaksss/task-slack-notify`, base `origin/dev` → PR `dev`) — 아직 미사용

## 1. 지금

- [!] spec PR [#686](https://github.com/MediSolveAIDev/mediness/pull/686) 사용자 리뷰 게이트
- [ ] 머지 후: 코드 착수 승인 → WP-132 P1(DM 수렴 + 시드 5명) → P2(데일리 리포트 job)
- [ ] dev 배포 후 실기동: 채널 env(dev 값) 주입 → 다음날 09:00 스레드 확인 + 워크플로 배정 DM 1건 확인

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-02 | 데일리 리포트 채널 = `C0APPU6UG4X`(#009--업무일지). **ID 로만 계약**(이름 가변) | 사용자 확정 |
| 2026-09-02 | 집계 = **담당자 축**, 전날 KST 창(생성/진행/완료) + **열린 태스크 스냅샷**(마감 유무) | 사용자 확정(추천 채택) |
| 2026-09-02 | 생성 DM = **남이 세운 배정 전부**(워크플로·시스템 포함, 자기 배정 제외). 요청 술어 불변 | 사용자 확정(추천 채택) |
| 2026-09-02 | 스펙·WP 는 코디가 직접 작성(워커 발주 없음), 어렵지 않은 태스크 | 사용자 지시 |
| 2026-09-02 | WP 번호 = **132** (131 은 09-01 실기동 수리분 등재용 예약 — task-improve 문서 환류 목록) | 코디, 충돌 회피 |
| 2026-09-02 | 채팅 MCP 는 **중단·완료(요약 입력) 툴을 열지 않는다** — 둘 다 사람이 웹에서 직접. task_done 은 현행(근거 없으면 422 안내) 유지 | 사용자 확정 (MCP 점검 후) |
| 2026-09-02 | 데일리 리포트 **C레벨 제외** — org_role(ceo·coo·cto·cmo) 유효 부여 기준 | 사용자 확정 |
| 2026-09-02 | 채팅 조회(runtime_task_my) **내 것만** — 구 «관리자는 all»(WP-108) 폐기 | 사용자 확정 (754건 실기동) |
| 2026-09-02 | `users.slack_id` 미매핑 5명(구지윤·최원·김사라·박신아·원영진) **prod 백필 완료**(NULL-only 멱등). 시드 동기화는 WP-132 P1 | 사용자 버그 리포트(구지윤 요청 DM 미발송)의 원인 — 판정 정상, 매핑 공백 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend | `term_b8ed8262-30ef-48a9-8e1f-2c793bb6a731` | `task_82ca2269e96c` | `ctx_0974e05a53e9` | `task-slack-notify-be-brief.md` | 완료 (34 tests·코디 재검증 통과 → PR #145) |

※ `task_3f1d4a2e9fb6` 는 중복 생성분 — failed 처리(무효). spec-brief 는 미사용(코디 직접 작성).

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/686 (커밋 amend 됨 — 최신은 브랜치 HEAD)
  - 신설: `20-spec/spec-120-task-slack-notify.md`(SPEC-120 · DOC-252) · `30-work/work-132-task-slack-notify.md`(WP-132 · DOC-253, planned)
  - 정정: SPEC-154 §4.8 전달 절 → SPEC-120 위임 1줄 · 20-spec/30-work 맵 갱신
  - lint --strict: mediness 신규 ERROR/WARN 0 (30-work.md:243 SPEC-030 WARN 은 기존분)
- code PR: https://github.com/MediSolveAIDev/mediness-app/pull/145 (dev 대상, 리뷰 대기)

## 5. 이력 (최신이 위)

- `2026-09-02` 스펙·WP 작성 → spec PR #686 오픈. 직전에 prod slack_id 5명 백필(§2)
- `2026-09-02` 사용자 요건 접수(데일리 리포트 + 생성 DM) → 4문 확정 → new-work.sh 세팅
