# [reviewer_doc] 2회차 재검수 — planner 2회차 반영 확인

1회차 브리프 `android-app-review-doc-brief.md` 와 같은 역할 · read-only · 리포트 1개. 맥락이 없으면 이 폴더(`/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`)의 `review-doc-1-report.md` · `spec-2-instructions.md` · `spec-2-report.md` 를 읽어라.

## 새 사용자 결정 (2026-11-13)
- **Android 통역도 범위 안 · 완료 조건(A-48)** — 마이크 권한 · 녹음 · 결과 표시 · 소리 출력. Dart 변경 필요하면 코디 확인(스펙에 정하지 않음).
- Delivery 승인 경로 = (b) 스펙 PR 머지 → v2 재결속 → 승인. v2 는 아직 안 함 — spec-2-report §4 목록이 맞는지만 본다.

## 볼 것
1. W-1~W-4 가 리뷰 1의 고칠 방향대로 반영됐나(파일:줄).
2. 통역 범위 안이 스펙 전체에서 일관한가 — `grep -rn "통역" products/day/` 로 「Android 밖」 「iOS 만」 류 낡은 줄이 남았나. A-48 통역 항목이 에뮬레이터에서 확인 가능하고 화면 문구를 지어 넣지 않았나(U-15 와 대조).
3. W-2 정리 뒤에도 [미결]이 [확정]으로 올라간 곳 0.
4. spec-2-report §4(v2 목록) · §5(title 그대로) · §7(에뮬레이터 마이크 · TTS 언어) 판단에 의견.
5. lint `--strict` products/day ERROR 0 (직접 1회).

## 산출물
`review-doc-2-report.md`(같은 폴더) — 판정 PASS/WARN/FAIL · 지적마다 파일:줄 + 근거.
완료 보고는 1회차 브리프 §9 두 명령(새 dispatch preamble 의 taskId · dispatchId).
