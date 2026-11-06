# [researcher] 운영 명동점 KOS — 에이전시 유입 · 결제가 어디에 찍히나 (조회만)

너는 **cc-prototype `researcher` 워커**다. **맥락이 하나도 없다고 가정하고** 아래를 먼저 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` (코디 워크트리 — 리포트 1개 외에 건드리지 마라)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/reference/2026-10-12-cc-prototype/kos-demo-api.md` — KOS OpenAPI 작업 전수표 · 응답 모양(§3.3 일정 · §3.4 수납/통계). **데모 테넌트 기록이다.** 이번엔 운영이다
- `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` — 인증 · 호스트 · 오류
- `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py` — 조회 전용 수집기(허용 경로 + `/queries/` 만 통과). **운영 키 `KOS_API_tenent` 를 쓴다**
- 기존 운영 수집본(gitignore · 개인정보 포함): `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/sources/internal-data/` 의 `kos-raw/` · `kos-silver/` · `kos-gold/`. 그리고 이를 만든 스크립트 `scripts/kos_silver.py` · `kos_gold.py` · `kos_analyze.py` · `kos_relationships.py`(funnel 을 이미 다룬다)
- 공식 문서: `https://developers.kos-solution.com/docs/openapi`

기대는 개념:
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/areas/concept/cs/no-inference-from-free-text.md` — 메모 같은 자유 텍스트에서 에이전시를 「추정」해 세지 마라. 구조화된 필드만 근거. 자유 텍스트에만 있으면 「자유 텍스트에만 있음」으로 보고

## 2. 배경 / 무엇을 바꾸나

병원(운영 명동점)이 **에이전시가 데려온 손님에 대한 수수료 정산** PoC 를 원한다. 용도는 병원과 에이전시가 **「너는 이 기간에 N명을 데려왔고, 그중 M명이 결제해서 결제액이 X다」를 서로 확인**하는 것이다.

만들기 전에 사실 하나를 먼저 확인한다: **운영 KOS 데이터에서 「이 손님은 에이전시 A 가 데려왔다」가 어디에, 어떤 모양으로, 얼마나 빠짐없이 찍혀 있나.** 그리고 그 손님에게서 **결제까지 이어지는 연결**이 끊김 없이 되나. 이번 작업은 **조사뿐**이다. 코드도 설계도 만들지 않는다.

## 3. 계약

해당 없음 (조사 리포트). 산출물 = 리포트 1개:
`/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/research-agency-attribution.md`

## 4. 답할 질문 (리포트 절 = 질문 번호)

각 답에 **근거**(필드 경로 · 건수 · 어느 수집본/호출인지 · 공식 문서 URL)를 붙인다. 모르면 「미확인」, 문서에 없으면 「문서에 없음」.

- **Q1 에이전시 표시 위치** — 에이전시를 가리킬 수 있는 구조화 필드 후보를 전부 센다: `reservation.funnel{…}`(유입 코드), `reservation.connectedChannel`, `visitor.visitorType`, `visitor.categories[]`, `visitor.snsInfo`, 수납의 `assignee` 등. 각 후보의 **값 종류(코드 목록)와 값별 건수**. 에이전시 이름처럼 보이는 값이 어느 필드에 있나
- **Q2 유입 코드 목록** — funnel 코드 전체(id · name · 사용 여부). 공개 OpenAPI 로 받을 수 있나, 내부 API(`meta/codes`)로만 되나
- **Q3 채움률** — 최근 기간 일정/손님 중 Q1 후보 필드가 비어 있는 비율. **에이전시 손님이 필드 없이 빠지는 구멍**이 보이나
- **Q4 단위** — 에이전시는 손님(visitor)에 붙나, 예약(schedule)마다 붙나. 같은 손님이 예약마다 다른 유입을 갖는 경우가 있나(건수)
- **Q5 결제 연결** — 에이전시 손님 → 일정 `purchaseIds` → `getPurchaseSummaries`(품목 · `transactions[]` · 환불) 또는 `getTransactionStatistics`(기간 결제). 끊기는 곳 · 비율. 데모에서 본 「id 21개 중 7건만 조회」가 운영에서도 나오나
- **Q6 기간 매출 뽑기** — 「기간 안의 결제 전부」를 빠짐없이 받는 경로가 뭔가(`getTransactionStatistics` 페이지 · `totalCount`). 환불 · 취소가 어떻게 보이나(status 값별 건수)
- **Q7 확인용 표 시험 집계** — Q1 에서 가장 유력한 필드 기준으로 **지난 한 달** 「에이전시(값)별 · 손님 수 · 결제한 손님 수 · 결제액 합 · 환불액 합」을 **집계 숫자로만** 낸다. 에이전시 값이 내부 코드명이면 그대로 써도 된다(사람 이름 아님)
- **정할 것** — 조사 중 나온, 코디·사용자가 결정할 것 목록 (예: 에이전시 판정 필드 · 매출 기준 · 손님 식별을 에이전시에 어떻게 보여 줄지)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 6. 단계

1. 기존 수집본과 그 스크립트를 먼저 본다. 최신 실행(`kos-raw/2026-10-28T…`)에 funnel · 수납 · 결제가 있으면 **그걸로 답한다**
2. 부족한 것만 운영 API 로 **조회**한다. `kos_collect.py` 를 쓰거나 같은 가드(허용 경로 + `/queries/` 만)를 지키는 일회성 스크립트를 scratchpad 에 둔다. 새로 받은 원본은 `kos_collect.py` 기본 출력(위 gitignore 폴더)이나 scratchpad 에만 둔다
3. 호출은 `--request-budget` 같은 상한을 걸고 간격(`--interval` 0.3 이상)을 둔다. 먼저 `--execute` 없이 계획을 보고 돈다
4. 리포트를 쓴다. 머리에 조사 날짜 · 쓴 수집본(실행 폴더 이름) · 새로 부른 작업 목록과 호출 수

## 7. 범위 제약 — 하지 말 것

- **KOS 쓰기 호출 절대 금지.** `/commands/` 경로를 부르지 마라. 인증(`exchange-token`) 외 전부 `/queries/`
- **개인정보를 리포트에 쓰지 마라.** 이름 · 전화 · 생년월일 · 차트번호 · 여권 · SNS 계정 · 메모 원문 금지. 건수 · 비율 · 코드명 · 필드 경로만. 예시가 필요하면 값을 가린다(`홍**`, id 끝 4자리 정도까지)
- API 키 · 토큰 · 비밀번호를 리포트 · 터미널 출력 · 파일에 쓰지 마라
- ax-clinic-project 레포의 추적 파일 · `kos-silver/` · `kos-gold/` 를 고치지 마라(읽기만). 새 원본은 위 2번 자리에만
- 수수료 규칙 · 화면 · 코드 설계를 하지 마라. 「정할 것」으로만 모은다
- 커밋 · push · PR 금지

## 8. 검증

```
Q1~Q7 각각 답 + 근거(필드 경로 · 건수 · 출처). 모르면 「미확인」.
리포트에 개인정보 0 — 끝내기 전에 리포트를 직접 다시 읽어 이름·전화·생년월일 패턴이 없는지 확인
/commands/ 호출 0 — 새로 부른 경로 목록을 리포트 머리에 적는다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_54222257-b51f-4f06-9268-dea87de55c5a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
