
# [reviewer_doc] DAY 앱 SPEC 독립 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

planner가 쓴 SPEC 단계 산출물만 검수한다. planner 완료 후 실행되는 태스크다. 너는 앞 대화 맥락이 없으며 원천은 아래 최종 발주 브리프다. WP·코드 작성 금지. 모든 소스는 읽기 전용이다.

## 1. SSOT — 이번 사용자 확정 결정

- /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/_RESUME.md 최신 결정 세 줄
- 같은 폴더 planner-policy-report.md · review-spec2-report.md · planner-spec-fix2-report.md
- 검수 대상 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec/products/day/20-spec/spec-003-mobile-app.md
- 기존 DAY-SPEC-002 권한·호출·수락 계약과 dev 91728737는 읽기 전용 참고

## 2. 이번 태스크

앞 태스크는 완료됐다. 새 preamble id로만 보고한다. 최종 사용자 답 ①통역은 시술현황에서 해당 고객 정보를 보는 사람 모두 ②푸시는 기존 호출대상 그대로(all=해당 병원 원장 목록 전체·one=지정원장), 관리자 추가/호출자 제외를 새 정책으로 만들지 않음 ③향후 코디→상담사 호출을 추가할 수 있으나 이번 1차에는 추가하지 않음. 이 세 결정 반영만 좁게 검수한다.

## 3. 검수 계약

통역 노출·WS권한·AC가 기존 해당 병원 고객정보 열람권한을 따르고 별도 interpret/edit 권한을 요구하지 않아야 한다. 푸시 수신자와 간호사 대리 수락 권한을 혼동하지 않는다. 알림 본인수락은 기존 board.accept 서버 판정을 따른다. OQ-A15/A17은 닫혔고 다른 미결까지 닫은 것으로 쓰면 안 된다. 현재 doctor_call의 규칙을 미래 모든 직무 호출에 영구 고정하지 않는다. 상담사 API·UI·데이터모델 변경을 1차에 추가하면 안 된다.

## 4. 파일

SPEC-003 U-14·U-15·§3 푸시/통역·AC A-14b/A-16b·§5 닫은 것·향후 요구 행을 확인한다. N1~N3 문서정정도 고쳐졌는지만 확인한다. 이미 해소된 F1/W1~W9의 대규모 원천을 다시 전수 조사할 필요 없다. 새 변경이 모순을 만들었을 때만 근거와 함께 지적한다.

## 5. allowed_paths

- /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/review-policy-report.md 한 파일만 작성. 그 밖 전부 읽기 전용.

## 6. 검증

세 결정 일치 여부·남은 미결 구분·diff 범위·SPEC 내부 문장 정합을 확인한다. 문서 lint는 planner가 변경 뒤 0 error 확인했고 코디가 핵심 diff를 대조한다. 이번 좁은 리뷰에서 내용이 바뀌지 않았다면 lint를 다시 돌릴 필요 없다. 보고서는 1쪽 이내로 판정 PASS/WARN/FAIL과 근거·남은 것만 쓴다.

## 7. 금지

수정·커밋·push·PR·서버조작·새 정책·문구 결정 금지. WP·코드 미착수 유지.

## 8. 완료

지정 보고서 한 파일과 최신 preamble의 worker_done --outcome succeeded로 완료 보고. 검수 PASS와 구현완료/실연동완료는 다르다. 현재 앱/서버 코드는 아직 없음.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_bfb1afc9-97a0-4d5b-bcab-aa5b6b982f00 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
