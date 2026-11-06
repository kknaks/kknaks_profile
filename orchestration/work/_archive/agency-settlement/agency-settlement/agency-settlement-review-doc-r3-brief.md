# [reviewer_doc] SPEC-001 0.3.0 · WORK-001 2판 검수

너는 **agency-settlement `reviewer_doc` 워커**다. **맥락이 없다고 가정하고** 읽어라:
- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/reviewer/role.md` (+ `rules.md`) — 대상이 문서라는 점만 다르다
- 앞 판 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-spec-001-r2-report.md` · 코드 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r1-report.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` — **read-only**, 리포트 1개만.

## 대조 기준
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` — D-01 ~ **D-14**(D-10 ~ D-14 새로)
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2 — 2026-10-29 줄 전부(이기는 순서 1번)
- 시안 v2: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v2.dc.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-v2-report.md`
- 지금 코드(1판 · 운영 10월 조회 성공): `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement/back` · `front` — 읽기만
- KOS 공식 스펙 `https://developers.kos-solution.com/openapi.yaml`

## 대상
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md`(0.3.0) · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md`(2판) · 두 README

## 볼 것
1. D-10 ~ D-14 · _RESUME §2 새 줄이 빠짐없이 · 바뀌지 않고 들어갔나
2. **저장 · 증분(§4.4 ~ §4.6)에서 돈이 빠지거나 두 번 들어가는 길** — 증분 경계 · 겹침 · 중복 키 · 달 확정 순간 · 품목 달 고정 · 취소가 다음 달에 오는 경우 · [전체 다시 받기] 뒤 · 동시 요청
3. 확정 달이 정말 KOS 0 인가(조용히 다시 부르는 길)
4. 에이전시 판정 · 손님 셈(이름 기준 — 동명이인) · 탭 목록
5. 엑셀(§3.6 · §4.7) — 칸 차례 D-14 · 숫자 셀 · 개인정보
6. SQLite 에 원본 · 지정 밖 개인정보가 들어가는 길 · 파일 gitignore · 로그
7. code r1 W-1 · W-3 · W-5 · W-6 정리가 지금 코드와 맞나
8. WORK 2판 WP 완료 조건 · 시험이 위를 덮나 · public grep

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-spec-001-r3-report.md` — 판정 PASS/WARN/FAIL · 지적마다 `파일:줄` + 근거. 파일 수정 · KOS 호출 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_b19a3776-0bcd-4f25-992e-ba7af21fc8b5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: SPEC 0.3.0 검수" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] reviewer_doc: <질문>" --enter`
