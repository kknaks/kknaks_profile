# [researcher] cc 시안(현황판 v3 · 의사 모바일)을 실제 운영 데이터로 채울 수 있는지 조사

너는 **cc-prototype `researcher` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype` (코디 워크트리에 직접 탄다)
리포트 파일 1개 말고는 아무것도 만들지도 고치지도 마라.

## 1. SSOT — 먼저 읽을 것

- **시안 (화면의 정본)** — 코드 레포 `/Users/kknaks/git/toy_pr2/cc-prototype/cc/design/`
  - `README.md` 먼저. 시안 두 장: `Ceramique 현황판 v3.dc.html`(관리자 현황판 · 데스크톱) · `Ceramique 의사 모바일.dc.html`(의사 개인 화면)
  - 시안 안의 환자·방·직원 값은 전부 샘플이다. **화면에 어떤 정보 칸이 있는지**를 읽는다(HTML 소스·인라인 데이터)
  - 시안 원본은 claude.ai/design 프로젝트 `dda9a931-097f-4780-9301-972d5ac1fc23` — 사본으로 부족할 때만 참고. 접근 못 하면 사본만으로 한다
- **실제 데이터** — `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/`
  - `manifest.json` — 운영(production) 병원 CRM API 캡처, 기간 2026-10-01~10-11(KST), 그룹·건수
  - `raw/<API 이름>/*.json` — API 별 응답. 핵심 후보: `getScheduleDetail`(177건 — visitor · flowStep · reservation · consultation · tasks[room·assignees·doctors·status·ready/completed 시각]), `getZones` · `getMachines` · `getProcedures` · `getMedicalServices` · `getReservationGroups` · `getScheduleStatistics` · `getProcedureTaskStatistics` 등
- 제품 맥락: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/00-baseline/baseline-003-cc-idea.md`(현황판 아이디어 · 도면) · `10-decision/decision-001-feature-lab.md`(스택·D-06)

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 알고 싶나

2026-10-16(금) 지점 방문 시연용으로 cc 현황판을 만든다. 시안은 나왔고, 병원 CRM 의 실제 운영 데이터 열흘치를 캡처해 왔다.
코디·사용자가 알고 싶은 것은 **「이 시안을 이 데이터로 구현할 수 있나 — 어느 칸은 데이터로 바로 되고, 어느 칸은 가공이 필요하고, 어느 칸은 데이터에 없나」**다.
이 답으로 cc 의 DEC(데이터 원천 · 시연 범위)를 정한다. 코드는 아직 없다.

## 3. 계약

해당 없음.

## 4. 조사할 질문 — 전부 답한다(답이 없으면 「데이터에 없음」·「시안에 없음」)

**A. 시안이 요구하는 정보**
1. 시안 두 장의 화면 구성 — 영역(패널·카드·목록·도면 등)별로 보여 주는 정보 칸 전부를 목록으로. 상태값·색 구분·숫자 집계·시간 표시 포함
2. 시안이 전제하는 **도메인 개념** — 환자 진행 단계, 방, 직원 역할(의사·상담사·관리사 등), 대기 시간 등. 각 개념이 시안에서 어떤 값들을 갖나(예: 단계 목록)

**B. 데이터가 가진 정보**
3. API 별로 무엇이 들어 있나 — 한 줄 설명 · 건수 · 핵심 필드. 특히 `getScheduleDetail` 의 구조(필드 트리)와 열거값 실측: `flowStep` 값 분포, `tasks[].type`·`status` 값 분포, `reservation.status`, 방(`tasks[].room`) 목록과 개수, 직원 이름 칸이 몇 종류(assignees · doctors · counselor · reservationAssignee)
4. 시각 정보 — 어떤 시각 필드가 있고(예약 시작·끝, flowStepUpdated, task ready/completed, doctorCall) 얼마나 채워져 있나(빈 값 비율). 「지금 누가 어디 있나」를 시각으로 재구성할 수 있나
5. 방·구역 — `getZones`·`tasks[].room` 의 방 목록이 BASE-003 도면(관리실 01–16 · 수면시술실 · 상담실 등)과 어떻게 대응하나

**C. 맞춰 보기 — 이 리포트의 본체**
6. **매핑표**: 시안의 정보 칸 하나하나 × 데이터 출처(API · 필드 경로) × 판정 `바로 됨` / `가공 필요(어떻게)` / `데이터에 없음`. 시안 두 장 모두
7. 「데이터에 없음」 칸마다 메우는 방법 후보(모의값 · 다른 API 추가 캡처 · 사람 입력 등)를 나열만 — 고르지 마라
8. **시연 재생 가능성**: 캡처는 과거 열흘치 스냅샷이다. 하루치를 골라 시각 순으로 재생하면 현황판이 「실시간처럼」 움직이나 — 어느 날이 건수·필드 충실도로 가장 좋은지, 상태 변화 이력이 남아 있는지(아니면 최종 상태만 있는지)
9. 의사 모바일 화면 — 「의사 한 명」 기준으로 데이터를 잘라 시안 칸을 채울 수 있나(의사 식별 칸이 일관된가)

**D. 위험**
10. 개인정보 — 어떤 필드가 개인정보인가(이름 · 전화 · 생년월일 · 국적 · 메모 · SNS 등). 시연 화면에 그대로 띄우면 안 될 것 목록. **값은 적지 말고 필드 경로만**
11. 데이터 품질 — 빈 값 · 일관성 깨짐 · 테스트로 보이는 행 등 구현에 걸릴 것

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 6. 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-cc-data-fit-report.md`

```markdown
# cc 시안 × 운영 데이터 적합성 조사 (<조사일>)
## 결론 한 장 — 시안 두 장 각각: 바로 됨 N칸 / 가공 M칸 / 없음 K칸, 구현 가능 판단의 근거, 가장 큰 구멍 3개
## A. 시안이 요구하는 정보 (질문 1~2)
## B. 데이터가 가진 정보 (질문 3~5) — 열거값 분포는 표로
## C. 매핑표 · 메우는 방법 후보 · 시연 재생 (질문 6~9)
## D. 개인정보 · 데이터 품질 (질문 10~11)
## 정할 것 — 코디·사용자가 결정할 항목 목록 (결정하지 말 것)
## 출처 목록 — 시안 파일:줄 · 데이터 파일 경로
```

## 7. 범위 제약 — 하지 말 것

- **⚠ 실제 운영 데이터다. 리포트에 개인 식별 값(환자·직원 이름, 전화번호, 생년월일, 차트번호, 메모 본문, SNS 계정)을 한 글자도 옮기지 마라.** 필드 경로·건수·분포·열거값(코드값)만 쓴다. 예시가 필요하면 `<이름>` 처럼 자리표시자로. 이 리포트는 나중에 공개 레포에 커밋된다. 방 이름·기기 이름·시술 이름 같은 병원 운영 값은 써도 된다
- 데이터 파일을 복사·가공 저장하지 마라. 분석용 임시 스크립트는 실행만 하고 파일로 남기지 마라(필요하면 `python3 -c` · `jq`). 외부 전송 금지
- 코드 작성(앱)·패키지 설치·API 호출 금지. 리포트 외 파일 생성·수정 금지. 커밋·push·PR 금지
- 구현 방식·데이터 원천을 고르지 마라 — 비교와 근거까지. 결정은 「정할 것」에

## 8. 검증

```
매핑표의 모든 시안 칸에 판정 + 근거(시안 파일:줄 · 데이터 필드 경로·건수). 개인 식별 값 0건(리포트를 이름·전화번호 패턴으로 스스로 grep 해 확인하고 결과를 보고). 결정하지 않고 「정할 것」으로 모은다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령의 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_ccbeb5ee-150a-49ac-ac88-da0dd51c4f01 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치 · 개인정보 grep 결과) / 미결·주의점"

# (2) 직접 주입 — 코디네이터를 깨운다
orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 (2) 방식으로 물어라:
  `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] researcher: <질문>" --enter`
