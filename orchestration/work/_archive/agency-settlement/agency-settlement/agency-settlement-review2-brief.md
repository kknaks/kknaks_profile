# [reviewer] WP-REVIEW2 — back/ · front/ 2판을 SPEC-001 0.3.1 에 대조

너는 **agency-settlement `reviewer` 워커**다. 맥락이 없다고 가정하고 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/reviewer/role.md` (+ `rules.md`)
- 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` **0.3.1** · 작업 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` 2판(WP-REVIEW2 행 = 볼 것)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` D-01 ~ D-17 · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2
- 앞 판 코드 리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r1-report.md` · 문서 리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-doc-r4-report.md`
- 워커 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/wp-fe2-report.md` · backend 보고는 아래 판단 목록
- 시안 v2 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v2.dc.html` · 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/shots-fe2/`

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` — **read-only**(코드 커밋 전). ⚠ 코디가 띄운 8800 · 3800 서버 · `back/.env`(운영 키) 건드리지 마라. 운영 KOS 호출 금지.

backend 가 스스로 적은 판단(판정할 것): ① 증분 ② 범위를 「이번 증분에서 다시 판정한 수납」으로 좁힘(#26 과 충돌 회피 · 옛 itemsMissing 은 전체 다시 받기로만) ② r4 W-2 「바뀜」 = 그 수납의 이 달 ① 행 갈아 끼움 · 셈은 new 1 · missing 1 · 응답 필드 없음(로그만) ③ KOS 설정 없어도 저장본 요청은 200 ④ closedAt = 확정한 받기의 시작 ⑤ newPurchases 정의.

## 볼 것 (특히)
1. **돈** — 저장 · 증분 · 확정 · 전체 다시 받기 · 동시 요청에서 결제 · 품목이 빠지거나 두 번 들어가는 길(시험은 초록인데 운영에서 터질 자리 따로)
2. **확정 달 KOS 0** — 조용히 다시 부르는 길
3. **SQLite 개인정보** — 지정 밖 필드 · 원본 JSON · 권한(WAL/SHM) · gitignore · 로그
4. 엑셀 — 칸 차례 D-14 · 수식 셀 0 · 숫자/날짜 셀 · 이름 그대로 D-17 · 화면 범위와 같음
5. 손님 셈 D-15 · 결제 손님 D-16 · 에이전시 판정 · 탭
6. back `schemas` ↔ front `lib/types.ts` 필드 하나하나 · 시안 v2 와 다른 곳(FE 보고 12곳)이 SPEC 과 맞나
7. 「사용자가 실물에서 만날 자리」

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r2-report.md` 하나 · 판정 PASS/WARN/FAIL · 지적마다 `파일:줄` + 근거. 파일 수정 · 커밋 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_b19a3776-0bcd-4f25-992e-ba7af21fc8b5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: code r2" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] reviewer: <질문>" --enter`
