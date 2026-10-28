# [planner] 고객 문진 웹 페이지 — 계약 문서(SPEC · DEC · WORK)

너는 **cc-prototype `planner` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc`(공유).

## 무엇을 하나
문진을 **고객 자기 폰의 ccc 고객용 웹 페이지**로 바꾼다(사용자 10-27 · 10-28). 지금 앱 문진 화면(APP5)과 문진 API(BE4)는 「보류 코드」다.

## SSOT
- 결정: `orchestration/work/overall-board/_RESUME.md` §2 — **10-27 「문진 = 고객이 웹에서」 줄 · §1 「문진 다시 하기」 항목 · 10-28 「문진 다시 하기 착수」 줄** · 문진 언어 원천(KOS language → 국적표 → en) · 방문별 이력 · 주민번호 안 넣음 · 법적 검토 주석
- 지금 계약: `para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` 0.4.1(§5-3 띄우기 · §6.15 앱 문진 · §7) · `spec-005-reservation-board.md` 0.4.0(예약 상세 문진 · QR 상자) · `10-decision/decision-007-app-v2.md` · 구현 중 정한 모양 `orchestration/work/overall-board/app-spec-followups.md`
- KOS 근거: `orchestration/work/overall-board/app-kos-report.md`(공개 문진 제출 · 양식 번역 6개 · 언어) · `reservation-questionnaire-report.md`
- 지금 코드(읽기만): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/back/app/{service/questionnaire.py,api/questionnaire.py,service/display.py,domain/languages.py}` · `procedure/app/lib/screens/questionnaire*` · `procedure/front/components/reservations/Display.tsx` (branch main = 운영 `affac41`)

## 쓸 문서
- `para/projects/summer-star/cc-prototype/20-spec/spec-006-customer-questionnaire-web.md`(새) — 고객 문진 웹: 경로(`/q/<토큰>` 등 · front 의 로그인 없는 공개 페이지) · 토큰(만들기 · 유효 시간 · 한 번 제출 · 다시 열기 · 만료 화면) · 화면(언어 칩 · KOS 양식 그대로 · 동의 · 미리 채움 · 제출 · 끝) · 언어 고르기 · back API(BE4 재사용 · 로그인 대신 토큰) · 보안(다른 고객 정보 0 · 속도 제한 · 로그) · QR 이 뜨는 곳(데스크 웹 상세 · 직원 앱 띄우기 `kind`) · KOS 제출 · ccc 이력 · **나중에 KOS 없이**(문항 · 답 ccc 저장으로 바꿀 자리) · E2E(고객 폰 실물)
- SPEC-004 · SPEC-005 해당 줄(앱 문진 화면 뺌 · 띄우기 = QR 보여 주기) — 그 줄만 · DEC-008(새 — 이 결정들) · WORK-010(새 — back · front · app WP · 검증) · README · log
- 보고 `orchestration/work/overall-board/q-web-spec-report.md`

## 금지 · 검증
- 코드 수정 금지 · 실명 · KOS id · 키 · 토큰 금지(public) · 열린 것은 OQ(기본값 제안 붙여)
- 검증: 결정 줄 → 절 대조 빠짐 0 · grep 0

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 커밋·push 금지.
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_aebffa88-6963-4ab6-b345-c0704f98ab64 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 완료: <한 줄>" --body "산출 경로 / 요약 / 검증 수치 / 정할 것"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
