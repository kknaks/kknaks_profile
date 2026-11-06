# [reviewer_doc] r7 — SPEC-001 0.5.0 · WORK 4판 (구현 전 마지막)

너는 **agency-settlement `reviewer_doc` 워커**다. 맥락이 없다고 가정하고 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/reviewer/role.md` (+ `rules.md`) — 대상이 문서
- 대조 기준: DEC-001 **D-19 ~ D-23** · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2 2026-11-02 줄 전부 · 피드백 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/feedback-2026-11-02.md` · 시안 v3 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v3.dc.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-v3-report.md` · 앞 판 `review-doc-r6-report.md` · `review-code-r3-report.md`
- 지금 코드(정본) `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement/back` · `front` — 읽기만 · KOS 공식 스펙 `https://developers.kos-solution.com/openapi.yaml`

작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` — read-only · 리포트 1개.

## 대상
`/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` 0.5.0 · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` 4판

## 볼 것 (막는 것만 FAIL · 나머지는 「구현 때 지킬 것」으로)
1. **수수료 돈 경로** — 비율 스냅샷(그 달 비율) · 새 달 복사 · 확정 잠금/풀기 · 반올림 · 미설정 0 · 앞 달 결제 취소 「—」(D-21) · 결산 표 · PDF · zip · 화면 합이 같은 값(판정 함수 하나)
2. **상품 키 = (품목 종류, 이름)**(OQ-138 코디 채택) — 같은 이름 · 이름 바뀜 · 목록에 없는 팔린 상품(OQ-139)에서 비율이 틀리게 붙는 길
3. **PG 전환 · SQLite 옮기기** — 확정 달 KOS 0 유지 · 옮긴 뒤 숫자 같음(M1 ~ M5) · 잠금(advisory) · 개인정보 칸
4. 채널 일반화 · 9월 ⚠ 규칙 · 쓰기 API 막기(§7.4)
5. 반응형 · 화면 계약이 시안 v3 와 맞나 · BE4 ∥ FE4 계약 고정점이 닫혔나
6. public grep

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-doc-r7-report.md` · 판정 · 「구현 때 지킬 것」 목록.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_b19a3776-0bcd-4f25-992e-ba7af21fc8b5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: SPEC 0.5.0 검수 r7" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] reviewer_doc: <질문>" --enter`
