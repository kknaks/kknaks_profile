# [reviewer] WP-REVIEW4 — back/ · front/ 를 SPEC-001 0.5.2 에 대조 (BE4 · BE5 · FE4 · FE5 한 번에)

너는 **agency-settlement `reviewer` 워커**다. 맥락이 없다고 가정하고 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/reviewer/role.md` (+ `rules.md`)
- 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` **0.5.2** · 작업 WORK-001 4판(REVIEW4 행) · 결정 DEC-001 D-01 ~ D-23 · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2(2026-11-02 줄)
- 사용자 피드백 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/feedback-2026-11-02.md` · `feedback-2026-11-02-b.md` · 시안 v3 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v3.dc.html`
- 문서 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-doc-r7-report.md`(「구현 때 지킬 것」 — 지켜졌나) · 앞 코드 검수 `review-code-r3-report.md`
- 지시서 `be4-add-product-id.md` · `be4-fix-1-instructions.md` · `fe4-fix-1-instructions.md` · `be5-instructions.md` · `fe5-instructions.md`

작업 워크트리 `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` — **read-only**(커밋 전). ⚠ 8800 · 3800 · `back/.env` · **운영 PG(127.0.0.1:5434 — 운영 개인정보)** 건드리지 마라 · 운영 KOS 호출 금지. 시험은 dev PG(5433) · testcontainers 로만.

**코디 실물(운영 · 숫자만)**: SQLite → PG 옮기기 대조 같음 · 9 · 10 · 11월 [전체 다시 받기] 뒤 수납 · 품목 · 실결제 합 옮기기 전과 같음 · ⚠ 0 · 상품 키: 9월 product 1,367 · option 914(지금 KOS 목록에 없는 삭제 상품 — 공개 API 한계) · product_title 88 · name 110 · 묶음 구성 채우기 9월 141 · 10월 126 · 11월 15줄 · 사용자가 10월 수수료율 152 개 저장함.

## 볼 것 (특히)
1. **수수료 돈 경로** — 그 달 비율 스냅샷 · 새 달 복사(GET 이 안 만듦) · 확정 잠금이면 전체 다시 받기 409 · 반올림 · 미설정 0 · 앞 달 결제 취소 「—」(D-21) · 화면 · 결산 표 · PDF · zip 합이 같은 값
2. **상품 id 키** — 옵션 짝짓기 · 목록 밖 옵션 · product_title 대체 · 같은 이름 다른 id · 키가 바뀔 때(상품 받기 전/뒤) 이미 넣은 비율이 다른 키로 새는 길
3. **PG** — 잠금(advisory · xact) · 풀 교착 · 권한(앱 계정) · 마이그레이션 0001 ~ 0003 왕복 · 개인정보 칸 · 로그
4. 쓰기 API 막기(Origin · Host · JSON) · 확정 달 KOS 0
5. 0원 줄 · 묶음 구성 · PDF 줄 맞춤 · 반응형 · 시안 v3 · `feedback-2026-11-02-b.md` 반영
6. back schemas ↔ front types 필드 하나하나 · 「사용자가 실물에서 만날 자리」

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r4-report.md` · 판정 PASS/WARN/FAIL · `파일:줄` + 근거.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_484ec91b-dc98-476e-bf33-eb653612c2c8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: code r4" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] reviewer: <질문>" --enter`
