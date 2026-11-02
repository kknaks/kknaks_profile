# [frontend] WP-FE4 — SPEC-001 0.5.1 (유입채널 · 수수료율 · 설정 · PDF · 반응형 · PG)

너는 **agency-settlement `frontend` 워커**다. 맥락이 없다고 가정하고 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/frontend/role.md` 를 먼저 읽어라.
⚠ 같은 워크트리 `back/` 에서 다른 워커가 병렬 작업 중 — 건드리지 마라. ⚠ 코디 · 사용자가 보는 8800 · 3800 · `back/.env`(운영 키) · `back/data/` 건드리지 마라 · 운영 KOS 호출 금지(가짜 transport · 가짜 응답).
화면 = 시안 v3 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v3.dc.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-v3-report.md` 그대로(반응형 1600 · 1024(1280/768 경계는 SPEC) · 390) · 가짜 응답으로 시안 장면마다 스크린샷 → `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/shots-fe4/`(데스크톱 · 태블릿 · 폰)

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` (main 위 브랜치 `kknaksss/agency-settlement` · 코드 PR #1 이후 이어서)

## SSOT
- 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` **0.5.1** · 작업 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` 4판 **WP-FE4** 행 + BE4 ∥ FE4 계약 고정점 표
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` D-01 ~ **D-23** · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2(2026-11-02 줄)
- 사용자 피드백 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/feedback-2026-11-02.md` · 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-doc-r7-report.md`

## 할 것
WP-FE4 행 전부 + 아래 「구현 때 지킬 것」 전부(해당하는 것).

## 구현 때 지킬 것 (doc r7) (막지 않음 · BE4 · FE4 브리프로)

### 수수료 · 돈 경로
1. 수수료는 **정수로만** 계산한다: `(amount * rate_bp + 5000) // 10000`(금액은 음수 없음 · §6.3). float 은 쓰지 않는다. #76 에 1,005 × 12.5% = 126 과 0.5 경계를 넣는다
2. **판정 함수 하나**: `/api/sales` · `channels[]` · `channelTotal` · PDF · zip · 엑셀 「정보」를 모두 같은 `build_month()` 결과에서 만든다(PDF 가 다시 계산하지 않는다). 시험으로 「PDF 합계 = `/api/sales` 그 채널 `netTotal` · `feeTotal`」 · 「zip PDF 합계들의 합 = `channelTotal`(손님 0 채널은 0 이라 같음)」을 확인한다
3. 스냅샷 복사(W-1 을 어느 쪽으로 정하든)는 **쓰기 잠금 안에서 `INSERT … ON CONFLICT DO NOTHING`** 으로 한다 · 응답 읽기용 `REPEATABLE READ READ ONLY` 트랜잭션보다 먼저
4. `PUT` · `lock` · `unlock` 의 `month_locked` · `cannot_lock` 검사는 **쓰기 잠금을 잡은 트랜잭션 안에서** 한다(검사와 쓰기 사이에 다른 요청이 끼면 안 됨)
5. `priorFee` 는 늘 `null` 이고 수납 `feeTotal` 은 줄 합만 쓴다. front 의 「—」 조건 = `itemsHere = false` 이고 `netTotal ≠ 0`(W-5 셋째와 같은 조건)
6. 0원 품목: 화면에서는 흐리게 보이고 `fee 0`, PDF 에서는 빠지고, `unsetItems` 에는 세지 않는다. 0 % 로 설정한 줄은 미설정이 아니다

### 상품 키
7. 상품 키 다듬기는 **한 함수**로 한다(앞뒤 공백만 뗌 · Python `str.strip()`). ⑦ `title` 과 ② 이름 양쪽에 같은 함수를 쓴다. 정규화(NFC)는 하지 않는다(§5.5 「그대로」) — L27 수로 판단
8. `PurchaseItemType_UNSPECIFIED` · `productNameFrom = none` 줄은 키가 없어 늘 미설정이다. 설정 `rows` 에도 없다(#73)

### PG · 옮기기
9. 달 잠금은 `try/finally` 로 푼다. KOS 를 받는 동안 트랜잭션을 열어 두지 않는다(`idle in transaction` 0). 쓰기는 잠금을 쥔 연결에서 한다(W-2)
10. `migrate_sqlite` 의 시각 파싱은 `app.domain.clock.parse` 를 그대로 쓴다. 3판 `_db` 는 `+00:00` 로 쓰고, KOS 원문 칸(`approved_utc` · `last_updated_utc` 등)은 `Z` · 소수 자릿수가 섞일 수 있다. 0/1 → boolean, `visit_date` → date 로 바꾼다. 「PG 3판 표 중 하나라도 행이 있으면 멈춤」
11. **새 back(PG)을 옮기기 전에 띄우지 않는다.** 빈 PG 에서 9 · 10월을 열면 J2 전체 받기로 KOS 를 부르고(확정 달 KOS 0 이 깨짐), 그다음 옮기기도 「비어 있지 않음」으로 멈춘다. WORK `:223` 「한 번에 바꾸기」 앞에 M2 를 둔다
12. M1 숫자는 scratchpad 에 숫자로만 적는다. M3 에 「9 · 10월 수납별 `paidAt` · `paymentTypes` 가 같음(저장값 · 수만)」을 더하면 W-2(r5) 고정이 옮겨졌는지도 확인된다
13. alembic `0001` 의 GRANT 에 **시퀀스 `USAGE`**(`fee_rate_changes.id` · `catalog_fetches` 의 identity/serial)도 넣는다. 빠지면 앱 계정 `INSERT` 가 권한 오류로 실패한다. 또 `fee_rate_changes` 에는 앱 계정 `UPDATE` · `DELETE` 를 주지 않는다(「지우지 않음」을 DB 가 막게 · #80)
14. `DATABASE_URL` 의 호스트 검사(로컬만)는 `TEST_DATABASE_URL` · testcontainers 호스트(보통 `localhost`)에서도 통과해야 한다. docker 환경에 따라 다른 IP 가 오면 시험만 막히니 확인한다

### 채널 · ⚠ · 쓰기 막기
15. `priorCancels` 는 「이 달 ① `APPROVED` 행과 이어진 `tx_id` 집합」에 `canceledRefId` 가 **없는** 취소다. 같은 달 승인이 ⑤ 와 못 이어진 경우에는 그 승인의 취소가 「앞 달」로 잡혀 ⚠ 가 뜬다. 이것은 드러내는 쪽이라 그대로 두고, 시험 #71 에 이 꼴을 하나 더한다
16. §7.4 Host 검사: `TestClient` 기본 Host(`testserver`)가 403 에 걸리므로 시험에서 Host 를 넣는다. `127.0.0.1:3800` 으로 연 화면은 `Origin` 이 달라 쓰기가 403 이 된다(code r1 CORS 실물 자리와 같음) → README · 오류 문구에 「localhost:3800 으로 여세요」
17. F-1 을 고치면 다른 사이트 GET(`refresh=full`)이 잠긴 달을 바꾸지 못한다. 남은 GET 쓰기(잠기지 않은 달 다시 받기 · W-1 (b) 를 고르면 스냅샷)는 `Sec-Fetch-Site: cross-site` 이면 막는 것을 권장한다(선택)

### front
18. 율 입력은 **문자열로** 만분율로 바꾼다(`"12.35"` → 1235). `12.35 * 100` = 1234.999… 같은 float 오차를 막는다. 셋째 자리는 front 가 먼저 막는다
19. ⚠ 는 `mismatch` 만 본다 · 합 칸 ⚠ = `netTotal === null` / `feeTotal === null` · PDF 미리보기는 ≥ 1024 에서만 · 가로 페이지 스크롤 0(`scrollWidth ≤ innerWidth`) · [이 달 확정]은 저장 안 한 변경이 있으면 꺼짐 · F-1 을 고치면 잠긴 달 [전체 다시 받기]도 꺼짐
20. 지점 · 병원 이름은 한 곳에서만 온다(W-5 둘째). LIVE4 L28 에서 실험한 비율은 끝나고 빈 칸으로 되돌리고, 기록 행은 남는다는 것을 사용자에게 알린다

---


## 검증
```
cd front && npx tsc --noEmit && npm run lint   # build 는 코디가(3800 이 production)
```
보고에 WP-FE4 완료 조건 · 지킬 것을 한 줄씩 「충족 / 해당 없음 / 미충족(사유)」.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_3aef3682-39a2-4fb9-9cff-543b2ea5ce0d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WP-FE4" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] frontend: <질문>" --enter`
