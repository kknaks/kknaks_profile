# [planner] 스펙 마무리 — 새 main 위로 rebase · 구현 사실 동기화 · 남은 문장 3

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec` · 브랜치 `kknaksss/day-mobile-v2-spec`(PR MediSolveAIDev/mediness#955 · 커밋 7d198317 · base ccede286). 이번에는 **git 쓰기 허용**(rebase · commit) · **push 금지**(코디가 force push).

## 1. rebase
`git fetch origin && git rebase origin/main`(= `07aaa6d2` · #954 KOS 키 테이블 SPEC-000 §4A · ERD · #957 prod 반영 절차 들어옴). 겹침 예상: `products/day/20-spec/spec-000-data-model.md` · `log.md` · `20-spec.md` · `40-architecture/` — **양쪽 내용 모두 살려** 푼다. migration 번호 표기가 있으면 실제대로: dev 는 `0012_kos_keys` → 우리 `0013_doctor_call_cancel_kind` · `0014_device_platform_android`.

## 2. 구현 사실 동기화 (코드 CENTURION_DAY dev `5ece25ea` · PR #266 · dev 배포됨)
코드가 스펙과 다르거나 스펙이 열어 둔 것을 코드가 정한 곳을 스펙에 반영(정본 = 코드 · 결정 근거 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/_RESUME.md` §2):
- 바로 시작 앱 화면 = 룸 상세 [의사 호출] 옆 [바로 시작] → 의사 호출 드로어 재사용(원장 고르기 없음) · 체크 가능 = `canQuickStart` · 거절 코드마다 토스트 차례로(OQ-A54 바로 시작 몫 닫음 · 사용자)
- 시안 없음(사용자) — 앱 화면은 기존 컴포넌트 + 웹 배치 · 글자(OQ-A52 · A54 닫음)
- 통역 동시 상한 3(`DAY_INTERPRET_MAX_SESSIONS=3` · Soniox 조직 TTS 3 · I-1 닫음)
- 푸시 묶음: iOS `apns-collapse-id`=callId · Android 알림 tag = data.callId · 새 칸 없음
- `/api/auth/device` client=web → 400 `invalid_request`
- migration 0013 · 0014(위)
- 통역 드로어 재생 중 안내 「번역 음성이 나오는 동안은 듣지 않아요」 지움 · 「번역 읽는 중」 그대로 · 대리 수락 창 「호출할 시술 · N개」 그대로(사용자)
- release Android 빌드는 Firebase 설정 없으면 실패(`-PDAY_ALLOW_NO_PUSH=true` 예외)
- 각 리포트(파일:줄)는 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-*-report.md` · `mobile-*-report.md` · `review-code-*-report.md`. 확인 못 한 것은 「실기기 확인 전」으로.

## 3. 남은 문장 3
- U-21 「복귀」 → 웹 실제 글자 「복귀하기」(검수 M1 W-1)
- SPEC-002 `canChangeDoctor` 문장(:672 근처)을 개정 ㉕ ③ 과 맞춤(검수 P2 WARN)
- 위 2의 바로 시작 드로어 결정

## 검증 · 보고
`python3 scripts/lint-pipeline.py --strict` products/day ERROR 0. 커밋은 rebase 뒤 **새 커밋 하나**(`docs(day): 0.2.0 구현 사실 동기화 — …`). 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-6-report.md`: 새 HEAD sha · 충돌 파일과 푼 방법 · 바꾼 곳(파일:줄) · Delivery #262 · #263 v2 재결속 때 넣을 문구 갱신(spec-5-report 목록 + 위 구현 사실). 완료 보고는 dispatch preamble 의 worker_done 그대로.
