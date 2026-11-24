# [planner] Delivery #267 · #268 · #269 고침 — 검수 FAIL 4 · WARN 6

읽을 것: 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-delivery-1-report.md` · 네 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-1-report.md`(계약 원본 — 경로 · view model · task 입구) · `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-2-report.md` · request `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery/`
문서 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` · 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation` (AGENTS.md)

## 고칠 것 — 리포트의 「고칠 것」 그대로 Issue 본문 · 계약에 싣는다
- FD-1 폴링 구분 신호를 하나로 정해(제안 중 하나 · 이유 한 줄) #267 · #269 에 같은 문장 · #267 A2 시험에 그 신호
- FD-2 task 입구(이름 · 인자 · 「① 은 넣고 안 기다림 · 잠금 · 중복 제거는 ② · 오늘은 안 넣음」)를 #267 · #268 에 같은 문장
- FD-3 view model 표 + 조각 `#reservation-main` 범위를 #267(제공) · #269(소비)에 같은 표 · 판정 위치(정원 글자 · 취소 / 노쇼 · 툴팁 글자 — 서버가 상태 키만 · 문구는 템플릿이 시안대로 등)를 표에 명시
- FD-4 수정 후보 `repositories/` → `queries/` · `services/reservations.py`(AGENTS.md 이름 규칙)
- WD-1 ~ WD-5 리포트대로(e2e 기대 결과 · 순서 조건 · #268 A1 시술권 · 카드 · 필터 수 계산 위치 · 메뉴 링크 한 곳 · partials 이름)

## 재결속 · 승인
같은 key · version+1 로 `--plan` → `--apply`(baseline 은 지금 그대로 origin/main + pending · #958 머지 안 함). 바뀐 것은 검수 지적에 따른 계약 명시라 범위는 같다. harness 가 재승인을 요구하면 **승인 receipt 를 적용한다**(사용자가 이 Delivery 를 승인했고 이번 변경은 검수 반영 — 보고에 「재승인 적용」을 밝힌다). 규칙이 막으면 우회하지 말고 출력 그대로 보고.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-3-report.md` — Issue 마다 바뀐 절 · 새 digest · 승인 상태 · 계약 세 개(신호 · task 입구 · view model) 최종 문장. json 은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery/`. 코드 · 커밋 · push · 머지 금지(30-work.md 변경 없으면 그대로). 완료 보고는 preamble 의 worker_done.
