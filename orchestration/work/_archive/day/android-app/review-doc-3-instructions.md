# [reviewer_doc] 3회차 검수 — Play 내부 테스트 범위 확장

1·2회차와 같은 역할 · read-only · 리포트 1개. 맥락이 없으면 이 폴더(`/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`)의 `spec-3-instructions.md`(사용자 결정 표 = 기준) · `spec-3-report.md` · `review-doc-2-report.md` 를 읽어라.

대상: 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec` 의 **미커밋 변경**(`git diff` — 커밋 `cb14f570` 이후분).

## 볼 것
1. 결정 표 일치 — 개발 앱만 Play 내부 테스트 · Play 앱 서명 · 업로드 키 로컬 · API 업로드(첫 빌드 수동). [미결]이어야 할 것(정식 앱 id · 정식 배포 방식 · FCM · 업로드 키 백업 위치 · CI · minSdk)이 [확정]으로 오른 곳 0.
2. M-3 · M-11 · M-12 · M-17 닫힘 범위 — §13 표와 본문(§1 · §1-1 · §7 · §9 · §12)이 같은 말.
3. §7-3-1 공식 문서 표 — 링크를 직접 열어(가능하면) 답이 문서와 맞는지 표본 3개 이상. 「확인 안 됨」을 확인된 것처럼 쓴 곳.
4. §7-3-2 사용자 손 단계 — 빠진 단계 · 순서 오류(예: 첫 AAB 전에 업로드 키 필요 · 앱 서명 등록 시점).
5. A-49 확인 가능성 · A-48 과 겹침 · 화면 문구 발명 0.
6. 값(이메일 · 키 · 서비스 계정 · 개발자 id) 0 · 전수조사 누락(`grep -rn -i "android\|play\|fcm\|keystore" products/day/`).
7. spec-3-report §6 v2 목록 · risk L3 상향 판단에 의견.
8. lint `--strict` products/day ERROR 0 (직접 1회).

## 산출물
`review-doc-3-report.md`(같은 폴더) — 판정 PASS/WARN/FAIL · 지적마다 파일:줄 + 근거. 완료 보고는 1회차 브리프 §9 두 명령(새 dispatch preamble 의 taskId · dispatchId).
