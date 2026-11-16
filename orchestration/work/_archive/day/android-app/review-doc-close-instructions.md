# [reviewer_doc] 마감 — spec-sync · Delivery #251 마감 sync 검수

같은 역할 · 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec`(브랜치 `kknaksss/android-app-close` · 미커밋 7파일). 읽기만 — 수정 · 커밋 금지.
맥락(이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`): `spec-close-instructions.md`(발주) · `spec-close-report.md`(planner) · `_RESUME.md` §2 · §5 · `app-1~6-report.md` · `review-code-4-report.md`. 코드 = CENTURION_DAY `origin/dev` `4f8316a7`(#253 squash).

## 볼 것
1. **사실 맞음** — 바뀐 줄마다 근거(리포트 · 코드 · 사용자 결정)와 대조. 특히 정식 앱 id · 프로덕션 출시 진행 · 업로드 키 공유 · 3단 주입 · 세션 저장 · minSdk/targetSdk · F1 · play_upload 짝 · A-48/A-49.
2. **누락** — planner 전수 표를 믿지 말고 `grep -rn -i "android\|play\|aab\|keystore\|업로드 키\|day.medisolveai\|\[미결\]" products/day/` 를 직접 돌려 낡은 줄이 남았는지.
3. **과잉** — 결정 안 된 것을 [확정]으로 쓰지 않았는지(FCM · 동영상 · 업로드 키 백업 · KOS 세션 14시간은 범위 밖 · 미결). 값(계정 · 키 · 서비스 계정 이메일 · 개발자 id) 0 · 화면 문구 발명 0.
4. **Delivery 마감 sync** — `30-work.md` · `log.md` 가 mediness#936 꼴과 맞는지 · conformant 판정 근거(A 마다) · 범위 밖 3건(F1 · 정식 앱 · 프로덕션)이 정직하게 적혔는지.
5. lint `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0.

## 산출물
`review-doc-close-report.md`(같은 폴더) — PASS/WARN/FAIL · 근거(파일:줄). 완료 보고는 1회차 리뷰 브리프(`android-app-review-doc-brief.md`)의 두 명령(새 preamble 값).
