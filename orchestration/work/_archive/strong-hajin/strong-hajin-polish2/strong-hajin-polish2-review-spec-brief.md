# [reviewer] 고도화 2차 SPEC 반영 검수 — planner 리뷰 모드

너는 **strong-hajin `reviewer` 워커**다. **너는 이 작업의 맥락이 없다** — 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` 등)

이번 모드: **planner 리뷰**(문서). **read-only** — 문서·코드를 한 글자도 고치지 않는다. 산출물은 리포트 한 장.

## 1. 대상

문서 레포(코디 워크트리) `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3` 의 미커밋 diff:

```bash
git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3 diff -- para/projects/summer-star/strong-hajin/20-spec/
```

(`30-work/`·`orchestration/` 의 변경은 코디 것 — 대상 아님)

## 2. 기준 (SoT)

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/_RESUME.md` §1·§2 — 사용자와 닫은 결정(2026-10-02 행: E2E-1 ~ E2E-5 ③)과 원문
- writer 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-write-brief.md` §2 — 반영 지시
- 사실 근거(지금 코드): 같은 폴더 `be-survey-report.md` · `fe-survey-report.md`

## 3. 볼 것

1. **충실도** — E2E-1~5 결정이 **빠짐없이, 더하지 않고** 반영됐나. 결정별 반영 위치와 일치 여부. 결정에 없는 계약을 SPEC 이 새로 세웠으면 FAIL. 특히:
   - E2E-1: 체크리스트·내용 = AI 제안, ID·날짜는 근거가 있을 때만
   - E2E-2: 「초안 저장」(pending·회차 +1·diff) · 모달 단추 「저장」(파랑) · 확정은 카드 「등록」만 · 1차 「모달 등록 = confirm+draft」 문장이 **남아 있지 않은지**
   - E2E-5 ②: 마감일 없으면 완료 때 실제 종료일로(직접 완료·완료 보고), 보완·재개로 되돌리지 않음 · 시작 예정일 채움은 지금 동작 유지
   - E2E-5 ③: 계획/실제 기한 두 값(`due_planned`/`due_actual`) 문장이 전부 정리됐나
2. **충돌** — 고친 문장과 **고치지 않은 다른 절**이 서로 다른 말을 하지 않나(같은 SPEC 안, SPEC 사이 — SPEC-004 캘린더·SPEC-005 프로젝트 포함). grep 으로 같은 개념의 다른 서술을 전부 찾는다(예: 기한/마감일 라벨, `due_planned`, 시작일 자동 채움, AX confirm draft, 채팅 단추 색, 상세 메타 순서)
3. **인수조건** — 바뀐 계약마다 AC 줄이 있고, 검증 가능한 문장인가
4. **형식** — 버전·변경 이력·결정 근거 열·frontmatter. 실명·메일 0건
5. **writer 가 연 Open Questions — 코디가 기본값으로 닫았다(2026-10-02)**. 재수정 판에서 SPEC 에 반영한다. 아직 OQ 로 남아 있는 것은 FAIL 이 아니다. 대신 이 답과 **어긋나는 문장**이 있으면 지적한다:
   - SPEC-001 OQ-Q → ① 「기한 지남」 칩·「기한 초과」 배지도 「마감일」로 ③ DateField 입력 표기 `2026/10/06` 통일 ⑤ SPEC-004 거절 문구 날짜도 통일 · ② 만들기 창·캘린더의 「시작일」 라벨은 유지 ④ 캘린더 날 머리(「10월 6일 월요일」)는 유지
   - SPEC-001 OQ-R → 서버 confirm 은 고친 초안을 계속 받는다(다른 카드가 쓴다). 두 AX 초안 kind 의 화면만 저장 명령을 쓴다
   - SPEC-004 OQ-405 → 완료의 마감일 채움 자리에도 배정 검증 훅을 건다
   - 보고만 한 것: 포커스 링(파랑 계열)은 이번 범위 밖 · 「근거 N개 더 보기」는 E2E-3 규칙 대상(사람 행동)
6. **조용히 통과하는 자리** — 취소선으로 남긴 옛 문장이 여전히 유효한 것처럼 읽히는 곳, 참조 절 번호가 틀린 곳, 「마감일」 통일이 서버 필드명까지 바꾼 곳

## 4. 판정

FAIL(결정과 다른 것이 적혔다 · 충돌) · WARN(모호) · PASS. 각 지적에 `파일:줄` + 근거.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-spec-report.md` ← 이 파일 하나만

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다.

```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_f8b0a2d6-3e7b-41de-b8c1-2acef6635f48 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: 고도화 2차 SPEC 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN 목록(파일:줄) / OQ 의견 / 리포트 경로"

orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] reviewer 완료 — SPEC 검수 <판정>. 리포트 review-spec-report.md" --enter
```
