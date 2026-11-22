# [planner] 스펙 2차 — 검수 1차 FAIL 반영 + 사용자 답

작업 워크트리 그대로: `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec` (네 1차 미커밋 변경 위에서 이어서). 브리프 `day-mobile-v2-spec-brief.md` 의 범위 · 제약 · 검증 그대로.

## 1. 검수 리포트 — 전부 반영

`/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-1-report.md`

- **FAIL 5(F-1 ~ F-5) 전부 고친다.** 옛 판 문장은 지우지 말고 취소선 + 「→ 2026-11-20 개정 …」.
- **WARN 17(W-1 ~ W-17) 전부 반영**하거나, 반영 안 하는 것은 리포트에 이유 한 줄. 특히:
  - W-1 `can*` 판정 = 한 갈래로 못박기(서비스 거절 규칙이 정본 · 웹 템플릿 조건이 더 좁으면 그 차이를 적고 #262 A2 문구도 맞춤)
  - W-2 방 목록 재묶음 규칙(지금 방 빼기 · 자기 자신 takenBy 에서 빼기 · 빈 방 먼저)
  - W-9 ~ W-14 통역 세부(통키 `56e43a0` 코드 대조 — TokenGate · ECHO_TAIL · 빈 final caption · context `text` 키 · stop 큐 비움 · TTS cancel · `audio_end` 응답 · PCM 버리기 범위 · `playback_stopped` 보내는 조작 = 통키 front 사실대로 · 시드 `.11` 로더 검사 · `wrong_key`)
  - W-15 #262 단계 시작 조건을 의존 표대로(통역 P1 → P5 를 앞당길 수 있게) — v2 재결속 때 반영할 내용으로 리포트에 적어라(지금 Issue 수정 금지)
  - W-16 출시 순서 「prod 서버 배포 먼저 → 정식 0.2.0 앱」을 SPEC-003 ⑲ ① · mobile-deployment 에 명시 · 되돌리기에 통역 되울림 추가

## 2. 사용자 답 (2026-11-20 · 결정 표에 더함)

| # | 결정 |
|---|---|
| M-4 보강 | **방 복귀도 앱에 넣는다**(OQ-A55 닫음 · 기존 `/api/visits/{id}/room-return`). 점유 이동 뒤 점유 띠(웹 `holdRoom` 표시)도 앱 카드 · 룸 상세에 보인다(복귀할 자리가 보여야 하므로 — W-3 · 글자는 웹 글자) |
| M-6 정정 | 웹에는 알림 목록 · 종 화면이 없다 → **웹은 OS 알림만**(OQ-N19 기본값 그대로 닫음). 결정 표 「웹 알림 목록 · 종 배지」 글자는 이 뜻으로 고친다 |
| OQ-N15 | 새 알림 종류 이름 = **`doctor_call_cancel`** (사용자 확정) |
| OQ-N16 | {N} 뜻 — **사용자 답 대기**. 지금은 기본값 「이번 취소로 빠진 시술 수」로 두고 OQ 로 열어 둔다(W-6 예시 — 3줄 호출을 하나씩 취소하면 알림 3번 — 를 OQ 행에 적어라) |

## 3. 검증 · 보고

- `python3 scripts/lint-pipeline.py --strict` → products/day ERROR 0
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-2-report.md` — F/W 번호별 반영 위치(파일:줄) · 반영 안 한 것과 이유 · 남은 막는 OQ 표
- 커밋 · push · PR · Issue 수정 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
