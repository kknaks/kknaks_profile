# [researcher] 환자 상세 — 직원이 환자 보러 갈 때 필요한 정보가 실제 데이터에 무엇이 있나 (메모 다섯 종 · 차트 · 시술 이력)

너는 **cc-prototype `researcher` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype` (코디 워크트리에 직접 탄다)
리포트 파일 1개 말고는 아무것도 만들지도 고치지도 마라. 너는 앞 맥락이 없다 — 아래 파일에만 있다.

## 1. SSOT — 먼저 읽을 것

- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-002-cc-poc.md` — 특히 D-04 · D-05 · D-09(**가짜는 고객명뿐. 시술 · 메모 · 이력 · 직원은 실데이터**) · D-10(시술 이력은 KOS API 로 보강, **KOS 는 운영 DB — 읽기만**)
- 시안 피드백: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-feedback-batch-1.md` — #3 · #4 가 이번 조사의 이유
- 현재 시안 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-staff-report.md` — 「시안이 쓰는 데이터 칸」표(지금 환자 상세가 무엇을 어디에 두었나)
- 앞 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-cc-data-fit-report.md` §B(필드 트리)
- **실제 데이터**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/raw/` — `getScheduleDetail`(일정 상세 177) · `getTicketBundlesQuery` · `getVisitorPrepaidCardBalance` · `getPrepaidCardSummaries` · `getPurchaseSummaries` · `getProcedureTaskStatistics` 등. **값을 실제로 읽어라**
- **KOS API**(시술 이력 보강 가능성): 가이드 `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` · 수집 스크립트 `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py` · `kos_collect_extra.py` · `kos_query_catalog.py` (읽기만)

**기대는 개념** — 해당 없음.

## 2. 배경

직원 페이지의 환자 상세(D-05)는 의사·코디가 **환자를 보러 가기 직전에** 보는 화면이다. 지금 시안은 실제 값을 보지 않고 필드 이름만으로 지어서
(1) 상단 카드와 「환자 차트」가 같은 정보(성별·나이·차트번호·국적·오늘 시술)를 두 번 보여 주고,
(2) 메모 다섯 종 중 둘만 넣었다. 메모는 환자 보러 갈 때 가장 중요한 정보다.
**실제 데이터를 읽고**, 환자 상세를 중복 없이 다시 짤 재료를 가져와라.

## 3. 계약

해당 없음.

## 4. 조사할 질문 — 전부 답한다(답이 없으면 「데이터에 없음」)

**A. 메모 다섯 종 — 실제 내용**
1. `visitor.memo` · `consultation`/`consultations[]` 상담 메모 · `reservation.reservationMemo` · 오더 메모(`orderMemo` — 경로 확인) · `tasks[].assigneeMemo` (+ `doctorMemo` · `memo` 등 다른 메모 칸이 있으면 전부) 각각:
   - 누가 언제 쓰나(필드 위치로 추정) · 채워진 비율(전체 · 10-09) · 길이 분포
   - **무슨 내용인가** — 실제 값을 읽고 내용 유형으로 분류(예: 주의사항·건강 · 시술 요청·부위·샷수 · 결제·패키지 · 일정·동선 · 언어·통역 · 기타). 유형별 건수와 **대표 예시 2~3개를 원문 그대로**(고객 이름만 `<고객>` 으로)
   - 같은 내용이 여러 메모에 중복되나
2. 직원이 환자를 보러 갈 때 **메모마다 쓸모** — 의사 관점 · 코디 관점으로 한 줄씩

**B. 차트 — 상단 카드와 겹치지 않는 정보**
3. `getScheduleDetail` 및 다른 API 에서 **고객 한 명에 대해 알 수 있는 것 전부**를 실제 값 기준으로 목록화: visitor(성별·나이·국적·신규·visitorType·categories·funnel·SNS 등) · 오늘 시술(tasks · 기기 · 마취 · 회차) · 구매·결제(purchases · 시술권 잔여 · 선불 잔액) · 상담 · 예약 그룹 등. 각 항목의 실제 값 예시(고객명 제외)와 채움 비율
4. 그중 **환자 보러 갈 때 필요한 것**과 아닌 것을 구분하고 근거 한 줄

**C. 시술 이력 — KOS API 로 받을 수 있나**
5. 가이드·OpenAPI 스펙·스크립트에서 **고객(visitor) 단위 과거 시술·방문 이력을 조회하는 작업**이 있나 — 작업 이름 · 요청 필드 · 응답 필드 · 기간 제한. 스크립트가 이미 쓰는 호출이면 그 함수 위치
6. ⚠ 가이드상 **73개 작업이 전부 `POST`**(조회·삭제 동일) — 5번 작업이 **조회 전용인지**(쓰기·삭제와 이름·스펙으로 구분되는지) 확인. 읽기 전용 호출 목록을 따로 적는다

**D. 제안 — 결정하지 말고 안(案)으로**
7. 환자 상세를 **중복 없이** 다시 짠 안 1~2개: 상단 카드 / 환자 차트 / 환자 메모 / 시술 이력 / 오늘 고객 동선 각 칸에 무엇을 넣나(필드 경로). 의사·코디가 다르게 봐야 할 칸이 있으면 표시
8. 메모를 종류별로 따로 보일지, 내용 유형(주의·요청·결제…)으로 묶어 보일지 — 각 안의 장단

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 6. 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-patient-detail-report.md`

```markdown
# 환자 상세 — 실제 데이터 조사 (<조사일>)
## 결론 한 장 — 메모 다섯 종이 각각 무엇인가 · 차트에 넣을 것 · 시술 이력 보강 가능 여부 · 중복 없는 환자 상세 안
## A. 메모 (질문 1~2) — 메모별 표 + 대표 예시
## B. 고객 정보 전체 (질문 3~4)
## C. 시술 이력 · KOS 읽기 전용 호출 (질문 5~6)
## D. 환자 상세 재구성 안 (질문 7~8)
## 정할 것 — 코디·사용자가 결정할 항목 (결정하지 말 것)
## 출처 목록 — 데이터 파일 경로 · 가이드/스크립트 줄
```

## 7. 범위 제약 — 하지 말 것

- **고객 이름만 가린다**(`<고객>`). 그 밖의 값(메모 원문·시술·직원 이름 등)은 실제 그대로 써도 된다. 전화번호가 메모에 섞여 있으면 그 번호만 `<전화>` 로
- **KOS API 를 호출하지 마라** — 읽기 전용이라도 이번 판은 문서·스펙·스크립트만 읽는다. 운영 DB 다
- 데이터 파일 복사·가공 저장 금지(분석은 `python3 -c` · `jq` 로 실행만). 리포트 외 파일 생성·수정 금지. 커밋·push·PR 금지
- 재구성 안을 확정하지 마라 — 안과 근거까지. 결정은 「정할 것」에

## 8. 검증

```
메모 다섯 종(+ 발견한 다른 메모 칸) 전부에 채움 비율 · 내용 유형 분류 · 원문 예시. 고객 정보 목록 각 항목에 실제 값 예시와 비율. 시술 이력 조회 작업이 있으면 이름·필드·조회 전용 근거, 없으면 「없음」과 찾아본 범위. 리포트에 고객 이름 0건(데이터의 visitor.name 값 전부와 대조해 확인하고 결과 보고)
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령의 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_4e46377b-beeb-4892-8fb8-70517fb63683 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(고객 이름 대조 결과) / 미결·주의점"

# (2) 직접 주입 — 코디네이터를 깨운다
orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 (2) 방식으로 물어라:
  `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] researcher: <질문>" --enter`
