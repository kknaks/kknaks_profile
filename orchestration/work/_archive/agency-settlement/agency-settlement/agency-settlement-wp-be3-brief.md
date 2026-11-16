# [backend] WP-BE3 — SPEC-001 0.4.2 (D-18 최종 결제만)

너는 **agency-settlement `backend` 워커**다. 맥락이 없으면 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/backend/role.md` 를 먼저 읽어라.
⚠ 같은 워크트리 `front/` 에서 다른 워커가 병렬 작업 중 — 건드리지 마라. ⚠ 코디 · 사용자가 보는 8800 · 3800 서버 · `back/.env`(운영 키) · `back/data/`(운영 저장본) 건드리지 마라 · 운영 KOS 호출 금지(가짜 transport · 가짜 응답 · 임시 DB 만).

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` (2판 코드가 커밋 안 된 채 있다 — 이어서 고친다)

## SSOT
- 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` **0.4.2** · 작업 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` 3판 **WP-BE3** 행(완료 조건 · 시험)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` D-01 ~ **D-18** · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2
- 사용자 말(10-29 실물 화면): **「손님이 최종적으로 어떤 상품을 얼마 병원에 냈나가 중요 · 최종적으로 취소된 건 필요 없다」**
- 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-doc-r6-report.md`(마지막) · 앞 판 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/wp-fe2-report.md`

## 할 것
WORK 3판 **WP-BE3** 행 전부 + 아래 「구현 때 지킬 것」 10 전부(해당하는 것).

## 구현 때 지킬 것 (WP-BE3 · FE3 · REVIEW3 브리프로)

1. **schema 1 → 2 빈 칸 채우기**는 그 달 잠금 + 쓰기 잠금 안에서, 한 트랜잭션으로 한다. 읽기 응답은 채운 뒤 다시 읽은 저장본으로 만든다(§4.4 「읽기 트랜잭션 하나」)
2. `netTotal` · 「앞 달 결제 취소」 · 숨김 · `excludedItems` 판정은 **함수 하나**에 둔다. 응답 · 엑셀 · 에이전시 합이 그 함수 결과만 쓴다. 엑셀 합 = 화면 합(#57)은 이 함수를 두 번 계산하지 않는 것으로 지킨다
3. 증분 5 (ii)의 ② 갈아 끼우기 대상 = 「**이 달** `items_here = true` + 이번 증분 새 행」. 품목이 다른 달인 수납 · `pinned_elsewhere` 수납은 대상이 아니다(#56 끝 줄)
4. 「살아 있는 승인」 저장값(`paid_at_utc` · `payment_types`)은 그 달 받기 · 그 달 증분(새 행 수납)에서만 쓴다. 다른 달 받기에서는 쓰지 않는다(#59)
5. 엑셀 「앞 달 결제 취소」 행: 품목 종류 · 상태 글자(`앞 달 결제 취소` · `취소`)를 back `labels.py` 와 front `labels.ts` **두 표에 같이** 넣는다(#39 두 표 같음 시험이 깨지지 않게). 글자 셀(`data_type "s"`) 규칙도 그대로
6. 숨긴 수납 수는 월별 건수 줄만. 에이전트별은 back 이 에이전시별 숨긴 수를 주지 않으므로 front 가 만들어 내지 않는다(`:210`)
7. `⚠ 통화 섞임` = `netTotal === null`. `paymentsNet` 의 null 여부로 가르지 않는다(§6.7)
8. 옛 필드 grep 0: `approvedTotal` · `paymentLines` · `reversalLines` · `lines[].paymentType` · `kind` ≠ `item`(WORK BE3 완료 조건). front `types.ts` 도
9. F-1 규칙을 넣으면 `transactions.at_utc`(취소 시각)와 `items.fetched_at` 비교는 **파싱한 시각**으로 한다(문자열 비교 금지 — r2 NOTE 1 과 같은 규칙)
10. 로그 · 오류에 `netTotal` · `paymentsNet` 값을 싣지 않는다 — 수(`hiddenPurchases` · `excludedItems` · 다시 부른 ② 수납 수)만

---


## 검증
```
cd back && uv run ruff check . && uv run pytest -q   # 옛 필드 grep 0 · commands/ 1줄
```
보고에 WP-BE3 완료 조건 · 지킬 것 1 ~ 10 을 한 줄씩 「충족 / 해당 없음 / 미충족(사유)」.


## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_c299b474-0715-4348-9ac5-d608f7e3c1b8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WP-BE3" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] backend: <질문>" --enter`
