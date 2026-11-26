
# [reviewer_doc] 앱 차트 스펙 검수 — DAY-SPEC-003 개정 ㉑ · DAY-SPEC-002 개정 ㉚

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

planner 는 끝났다(release). 이 워크트리는 읽기만 한다 — 아무도 쓰지 않는다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/_RESUME.md` §2 결정(범위 = 차트만 · D1 ~ D11) ← **대조 기준. 결정을 다시 열지 마라**
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/research-1-report.md` — 현황 조사 · §2 웹 기능 전수표 28행 · 근거 파일:줄 @CENTURION_DAY `55e60aa4`
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/planner-1-report.md` — planner 가 한 일 · 28행 처분 · OQ
- 웹 차트 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/_archive/day/day-chart-photo/_RESUME.md` §2 + 거기서 가리키는 `chart-photo-decisions.md`(C1 ~ C36) — 앱이 웹과 같아야 하는 기준

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

직원 앱 차트를 「읽기 전용」에서 「웹과 같은 기능」으로 올리는 스펙 개정을 검수한다. 산출물 = `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` 의 변경(커밋 안 됨 — `git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec diff origin/main` 으로 본다): `products/day/20-spec/spec-003-mobile-app.md`(개정 ㉑ · U-23 · A-51 ~ A-60 · OQ-A63 ~ A78) · `spec-002-procedure-board.md`(개정 ㉚ · 앱 /api JSON 짝 6) · `20-spec.md` · `10-decision.md` · `log.md`.

## 3. 계약

해당 없음(검수).

## 4. 먼저 읽을 핵심 파일

- `git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec diff origin/main -- products/day/` 전체
- 위 두 SPEC 본문 전체(개정 머리글 · 취소선 관례 · 앞 판과 맞는지)
- 코드 근거 확인용(read-only): `git -C /Users/kknaks/git/CENTURION_DAY show 55e60aa4:<path>` — 스펙이 기대는 사실(서비스 재사용 · 인증 · 오류 코드 · 앱 위젯 이름)이 실제와 맞는지

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 구현 단계

1. 결정 D1 ~ D11 · 범위가 하나씩 SPEC 에 반영됐는지 표(결정 → SPEC 절:줄 → 반영 / 누락 / 어긋남)
2. research-1 §2 웹 기능 28행이 SPEC-003 에 빠짐없이 처분됐는지(넣음 / 웹 전용 + 근거). 웹 전용으로 뺀 것이 결정과 맞는지
3. **「읽기 전용」 잔재 전수** — SPEC-003 · 002 전체에서 「읽기 전용」 · 「읽기만」 · 「차트 API 를 부르지 않」 · 「앱 경로 없음」 · 「웹만」 류를 grep 으로 전부 세고, 살아 있는 문장(취소선 아님)이 남았는지
4. 발명 검사 — 결정 · 웹 SPEC · 코드에 근거 없는 정책 · **화면 글자 · iOS 권한 문구**가 계약으로 들어갔는지(OQ · 「기본값(코디 제안)」 표시면 허용)
5. 범위 검사 — 여권 스캐너 · 문진 QR · 예약 탭 · 사진 대상 규칙 확장 · 웹 동작 / 권한 변경 · migration 이 들어갔는지(들어가면 FAIL)
6. 구현 가능성 — 앱 /api 짝(요청 · 응답 · 인증 · 오류)이 backend · mobile 워커가 되묻지 않을 만큼 닫혔는지 · 착수를 막는 OQ 에 기본값이 있는지 · 웹 경로와 같은 서비스를 쓴다는 말이 코드 사실과 맞는지
7. 인수 조건 A-51 ~ A-60 이 실기기 · TestFlight 에서 확인 가능한 문장인지 · 미저장 닫기 경로(✕ · 뒤로 가기 제스처 · 끌어 내림 · 바깥 누름)가 D6 과 맞는지
8. 지도(`20-spec.md`) · `10-decision.md` · `log.md` · 개정 번호가 서로 맞는지 · lint

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/review-doc-1-report.md` — 판정(PASS / WARN / FAIL) · 지적마다 파일:줄 + 근거 + 고칠 방향 · 「사용자 확인 필요」는 따로 묶는다.

## 7. 범위 제약 — 하지 말 것

- 레포 파일을 고치지 않는다(리포트 1개만) · 커밋 · push 금지
- 결정 D1 ~ D11 · 웹 결정 C1 ~ C36 자체를 다시 열지 않는다 — 이상해 보이면 「사용자 확인 필요」로 따로 적는다

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **(코디 추가 · 2026-11-25)** 이번 발주는 orca Run(`worker-start`)으로 나간다. **dispatch preamble 에 적힌 `worker_done` 명령(Task · Dispatch ID · `--outcome` · `--report-path`)이 아래 (1)보다 우선**이다. (2) 직접 주입은 그대로 해도 된다.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_414d6113-407d-486b-ab54-10a4a6b455cb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
