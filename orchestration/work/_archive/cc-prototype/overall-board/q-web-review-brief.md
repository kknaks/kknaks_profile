# [reviewer] 고객 문진 웹 코드 리뷰 — WORK-010 (back WP-BE · front WP-FE · app WP-APP)

너는 **cc-prototype `reviewer` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라.

- **대상** = `/Users/kknaks/orca/workspaces/cc-prototype/overall-board`(branch `kknaksss/overall-board-6`)의 **커밋 안 된 변경 전체**(`git diff` + 새 파일 · 지운 파일) — **read-only**. 이미 커밋된 `7e39bd3`(여권 분류)은 배포됨 — 대상 아님
- **기준** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-006-customer-questionnaire-web.md` 0.1.0 · `10-decision/decision-008-customer-questionnaire-web.md` · `30-work/work-010-customer-questionnaire-web.md` WP-REVIEW 줄 · SPEC-004 0.4.2 · SPEC-005 0.4.1 · `_RESUME.md` §2 10-28 「고객 문진 웹 OQ 사용자 몫 = 추천대로」
- **워커 보고** = `app-backend-report.md`(WORK-010 WP-BE) · `app-fe-report.md`(WORK-010 · 실제 back 붙이기) · `app-mobile-report.md`(WORK-010 WP-APP · 실제 back 확인)

## 볼 것 (WP-REVIEW 줄 그대로 + 아래)
1. **보안**: 토큰이 로그 · DB 원문 · 푸시 · URL 쿼리(서버 로그)에 0 · 공개 응답 허용 키만(다른 고객 · 직원 정보 0) · 직원 세션과 공개 경로 분리 · 한 번 제출 · 시한(10분 열기 · 60분 쓰기) · 속도 제한 · 클라이언트 IP 헤더(CF-Connecting-IP) 처리
2. back ↔ front ↔ app 계약 일치(`qrUrl` · 공개 GET/POST · 오류 코드 · 데스크 상자 단계 · 앱 QR 화면)
3. 지운 것 회귀: 앱 문진 화면 · unlock · 직원 문진 경로 — 남은 참조 0 · 경로 49
4. 법적 검토 주석 3곳 · 실명 · KOS id · 토큰 grep 0
5. 지금 backend 가 「제출 뒤 데스크 상세 건강 정보 안 바뀜」을 고치는 중 — 그 부분은 판정 밖(메모만)
직접 `cd procedure/back && uv run pytest -q` · `cd procedure/front && npx tsc --noEmit && npm run lint` · `cd procedure/app && /Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze && /Users/kknaks/fvm/versions/3.44.8/bin/flutter test` 수치. 사용자 포트 · 파일 수정 금지. **FAIL 은 운영 배포 · 고객 폰 E2E 를 막는 것만 · 짧게.**

산출물: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/q-web-review-code-r1.md`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_1651dd24-029a-4cb4-9c8b-1ef3faa0e1f4 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer 완료: 문진 웹 코드 <판정 한 줄>" --body "리포트 경로 / FAIL n · WARN n / FAIL 목록 · 고칠 사람"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] reviewer 문진 웹 코드 — <판정>. 상세는 q-web-review-code-r1.md" --enter
```
