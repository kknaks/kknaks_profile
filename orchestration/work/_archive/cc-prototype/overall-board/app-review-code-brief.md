# [reviewer] 앱 판 코드 리뷰 — WORK-009 (back BE1~BE5 · app APP1~APP6 · front WP-FE · infra 볼륨)

너는 **cc-prototype `reviewer` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라.

- **대상** = `/Users/kknaks/orca/workspaces/cc-prototype/overall-board`(branch `kknaksss/overall-board-2`)의 **커밋 안 된 변경 전체**(`95c64bc` 이후 · `git status` · `git diff` · 새 파일) — **read-only**. infra 변경은 `/Users/kknaks/orca/workspaces/k8s_infra_mac/overall-board`(branch `kknaksss/cc-prototype-app-photo`) diff 만 훑어라
- **기준** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` 0.4.1 · `10-decision/decision-007-app-v2.md` · `30-work/work-009-app-v2.md` · 구현 중 정한 모양 `orchestration/work/overall-board/app-spec-followups.md`(#1~#7) · `_RESUME.md` §2 10-27 앱 줄
- **워커 보고** = `app-backend-report.md` · `app-mobile-report.md` · `app-fe-report.md` · `app-infra-report.md` · 스크린샷 `app-shots/` · `fe-shots-reservation/app-fe-*`
- **알아 둘 것**: 문진은 다음 판에 **고객 웹 페이지**로 바뀐다(10-27) — APP5 앱 문진 화면 · BE4 는 **보류 코드**. 판정에서 FAIL 로 잡지 말고 「다음 판 정리 목록」으로만

## 볼 것
1. back ↔ app ↔ front 계약 일치(경로 50 · 요청 · 응답 · SSE · 푸시 payload · followups #1~#7)
2. **회귀**: 시술 현황 · 예약 현황 웹 · 기존 원장 호출 푸시 · `push_log` 다시 만들기(운영 DB 데이터 보존)
3. 보안 · 개인정보: 사진 열람 인증 · 사진첩 저장 0 · 주민번호 0 · 법적 검토 주석 · 띄우기 claim 1회 · 10분 · 다른 기기 · 다른 계정 차단 · 로그 · 리포트에 실값 0
4. 앱 상태 이름 · 색 = 웹 2계층 · 알림 둘만 · 수납 · 처방전 버튼 없음
5. infra: PVC · env · compose · Dockerfile `/photos` 권한
직접 `cd procedure/back && uv run pytest -q` · `cd procedure/app && /Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze && /Users/kknaks/fvm/versions/3.44.8/bin/flutter test` · `cd procedure/front && npx tsc --noEmit && npm run lint` 수치를 적어라. 사용자 포트 · 시뮬레이터 창 · 파일 수정 금지. **FAIL 은 시뮬레이터 E2E 를 막는 것만 · 짧게.**

산출물: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-review-code-r1.md`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_146f0bc4-7592-4d84-a000-aaca4c743aa1 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer 완료: 앱 코드 <판정 한 줄>" --body "리포트 경로 / FAIL n · WARN n / FAIL 목록 · 고칠 사람"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] reviewer 앱 코드 — <판정>. 상세는 app-review-code-r1.md" --enter
```
