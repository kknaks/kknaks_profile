
# [researcher] charty 1차 상담 — 요청 항목별 「어디서 가져오나」 조사

너는 **cc-prototype `researcher` 워커**다. **앞 맥락은 하나도 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2` (코디 워크트리 · 코디와 공유 — 리포트 1개 말고는 건드리지 마라)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

문서(코디 워크트리 · read-only) — `P = /Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype`

- `P/log/2026-11-12-api-swagger-docs.md` — 지금 외부 API 6개 · 연동처 키 · 제한 · 기록 · 함정
- `P/10-decision/decision-010-product-ext-api.md` · `P/10-decision/decision-011-ext-api-add1.md` (특히 D-03 메모 미노출)
- `P/20-spec/spec-008-product-ext-api.md` (0.3.3) · `P/30-work/work-012-product-ext-api.md` · `P/30-work/work-013-ext-api-add1.md` · `P/deploy.md`
- 앞 조사들: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/_archive/cc-prototype/api-swagger-docs/research-*.md` (표기 방식 · 조사 깊이를 이대로)
- DAY 조사(차트 메모 · 집도의 KOS 쓰기 사실): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/_archive/day/day-procedure-board-2/research-har-room-chart-report.md`
- KOS 데모 조사: `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-12-cc-prototype/kos-demo-api.md` — §1 접속 · 쓸 키 · 쓰지 말 키

KOS(private · read-only)

- 사용법: `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` §3
- 호출 코드(참고): `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py`
- 키: `/Users/kknaks/git/ax-clinic-project/scripts/.env` 의 **`KOS_API_tenent_dev` 만**(운영 호스트의 데모 테넌트). **`KOS_API_tenent` 는 실제 지점 키 — 절대 쓰지 않는다**
- 공식 스펙: `https://developers.kos-solution.com/openapi.yaml`
- 내부 API 는 브라우저 UA 필수(2026-11-03~) — 기존 코드의 내부 호출부를 보고 같은 헤더로

HAR(로컬 · gitignore · **값을 리포트에 옮기지 않는다** — 경로 · 메서드 · 키 모양만)

- `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-11-16-cc-charty1/har/상담대기.har` — **2-3 의 원천 후보**(KOS 단계 변경 이력 · 상담 대기 시각). 사용자가 이번에 준 것
- `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-11-09-cc-day/har/` — `차트작성.har` · `차트작성2.har` · `차트작성3.har`(차트 메모) · `고객예약접수시술.har` · `방이동.har` · `집도의변경.har` · `삭제후의사호출.har`
- `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-11-11-cc-product/har/상품 수납.har` — 수납 · 시술권 · 선불카드 후보
- **오더 메모 HAR 은 없다.** 다른 HAR 에서 오더 메모 호출이 보이면 적고, 없으면 「HAR 필요」로 둔다. 짐작으로 경로를 만들지 마라

코드(read-only) — kknaksss/cc-prototype `origin/main` `0a58aba`. canonical 체크아웃 `/Users/kknaks/git/toy_pr2/cc-prototype` 는 **예전 커밋에 서 있다** — 파일은 반드시 `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<경로>` 로 읽어라(checkout · pull 금지).

**기대는 개념** — 확인(데모 실호출) · 스펙(openapi) · HAR · 추정을 구분해 적는다(앞 조사와 같은 표기). 정할 것은 정하지 않고 모은다.

## 2. 배경 / 무엇을 알아내나

charty(외부 연동처)가 1차 상담 화면용으로 API 를 요청했다. 구조는 **KOS → CC(우리 back) → 서비스들**이다. charty 는 CC 의 `/api/ext/*` 를 X-Api-Key(연동처 charty) 하나로 부르고, CC 가 KOS 에서 값을 가져와 넘긴다. 직원 정보는 centurion 통합 계정.

지금 ext 는 6개(`GET /menu` · `POST /customers/lookup` · `POST /reservations` · `GET /availability` · `POST /customers/visits` · `POST /customers/reservations`). 코디가 잡은 가안은 「기존 `lookup` 에 필드 추가 + 새 ext 5개(board · 예약 상세 · 고객 언어 · 오더 메모 · 차트 메모)」다. 이 가안이 맞는지는 네 조사로 정해진다 — 항목마다 **원천이 어디이고 KOS 를 몇 번 불러야 하는지**를 알아내라.

## 3. 알아낼 것 — 항목마다 분류 + 근거

분류는 다섯 중 하나: **A 지금 코드에 있음**(직원 API · ext 어디서 이미 KOS 에서 받고 있음 — 파일:줄) / **B KOS 공개 API 로 됨**(작업 이름 · openapi 근거 · 데모 실호출 결과) / **C 내부 API(HAR)로만 됨**(HAR 파일 · 경로 · 메서드) / **D CC 저장 필요**(KOS 에 원천 없음) / **E 없음 · HAR 필요**.
항목마다 추가로: KOS 호출 수(목록이면 1건당 · 전체), 데모 KOS 조회 실호출 결과(모양 · 건수만), 함정.

**1. 직원 API 를 ext 로**
- 1-1 `GET /api/reservations/board` 접수 목록(오늘 고객 · 내원 단계 · 접수 시각) — 직원 board 가 KOS 를 몇 번 부르나 · ext 로 낼 때 칸
- 1-2 `GET /api/reservations/{reservation_id}` 고객 정보(기본 정보 · 고객 언어 · 문진 · 이전 방문 · 예약 메모 · 귀가 희망 시각 · 유입 경로) — 칸마다 원천
- 1-3 `PUT /api/customers/{customer_id}/personal` — 고객 언어만 바꿀 때 KOS 쓰기 호출 모양(**실호출 금지 · 코드 · HAR 로만**). 다른 칸을 같이 덮어쓰는 위험이 있나

**2. 상세에만 있는 칸을 목록에** (목록에 넣으면 KOS 호출이 늘어나는지가 핵심)
- 2-1 담당 상담사(staffId · 이름) — 상세 `reservation.counselor` 원천
- 2-2 관리실 — 상세 `flow.roomTitle` 원천
- 2-3 **처음 상담 대기가 된 시각** — 이후 단계로 넘어가도 안 바뀌는 값. 지금 코드는 `flowStepUpdatedDateTimeUtc`(지금 단계가 된 시각)만 써서 바뀐다(`procedure/back/app/service/reservations.py` 내원 현황 함수). **사용자 말: KOS 는 단계 변경 이력을 쌓는다.** `상담대기.har` 에서 그 이력을 주는 호출을 찾고(공개 API 에도 있는지 openapi 대조), 데모 KOS 에서 실제로 첫 `CONSULTATION_WAITING` 시각을 뽑을 수 있는지 확인. 보조 근거: CC 이벤트 `reception`(`endStep = CONSULTATION_WAITING`)
- 2-4 접수 시각 — 귀가 마친 고객 포함(상세 `flow.receptionAt` 원천 · 지금 board 가 귀가 고객을 빼는지)

**3. 없는 칸 · API**
- 3-1 접수의 상담 여부(상담 · 시술만) — 지금 코드의 「상담 거침」 판정과 KOS `consultationRequired` 관계
- 3-2 customerId(ccc id)로 보유 시술권 조회 — 지금 lookup 의 시술권 조회 경로를 이름+이메일 없이 탈 수 있나
- 3-3 시술권 「사용 중」 장수 — 지금 `remainingCount` 계산 근거와, 사용 중을 구분하는 KOS 칸
- 3-4 시술권 만료일(없으면 발행일) — KOS 칸 유무. 그리고 **「charty 가 차감할 시술권을 골라 넘긴다」를 받으려면 시술권 차감(KOS 쓰기)이 필요한지** — 차감 호출 모양(HAR) 유무만
- 3-5 선불카드 잔액 · 만료일 — KOS 원천(공개 · 내부)
- 3-6 예약의 희망 시술 · 예산 · 동행자 · 원장 상담 지정 · 통역 필요 — KOS 예약 · 고객에 칸이 있나, CC 에만 있나(문진 · 예약 폼)
- 3-7 진단기 · 날짜(그날 피부 진단) — 원천 유무
- 3-8 열람 기록(연 직원 · 고객 · 시각) — CC 에 이미 있는 호출 기록 테이블 구조(파일:줄)와, 직원 id 를 받으면 어디에 붙일 수 있는지. **정책은 정하지 말고** 사실만
- 3-9 지난 방문의 상담자 — 지금 `previousVisits[]` · ext `visits` 원천 호출에 상담자 칸이 있나

**4. 오더 메모 · 차트 메모 등록 · 수정** — 각각 KOS 쓰기 호출(공개 · 내부 · HAR 파일), 요청 모양, 수정 시 id 를 어디서 얻나, 지금 CC 코드에 같은 쓰기가 있나(직원 API `PUT /reservations/{id}/memo` · `/customers/{id}/remark` 와의 관계). **실호출 금지**

**5. 묶어 보기** — 위 결과로 「기존 ext 수정 / 새 ext」 가안을 다시 그려라(엔드포인트별 담을 칸 · KOS 호출 수). 결정이 아니라 사실 정리다.

## 4. 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/research-charty1-sources.md`

- 맨 위 요약표: 항목(1-1 ~ 4) × 분류(A~E) · 원천 한 줄 · KOS 호출 수 · 실호출 확인 여부
- 항목별 절: 근거(파일:줄 · openapi 작업 · HAR 파일 + 경로) · 데모 결과(모양 · 건수) · 함정
- §5 묶어 보기
- 「정할 것」 — 결정하지 않고 모음(정책 질문 · 원천이 둘인 칸 등)

## 5. allowed_paths — 이 밖은 건드리지 마라

- 위 리포트 1개만 생성. 원 응답 덤프 · HAR 발췌가 필요하면 네 scratchpad 에만(레포에 두지 마라)

## 6. 진행 단계

1. §1 문서 · 앞 조사 읽기 → 2. 코드(`git show origin/main:`)에서 A 분류 · 호출 수 → 3. HAR 분석(값 말고 모양) → 4. openapi 대조 → 5. 데모 KOS **조회만** 실호출(작업당 한두 번) → 6. 리포트

## 7. 범위 제약 — 하지 말 것

- **public 레포다** — 키 · 토큰 · 테넌트 id · KOS id · 사람 이름 · 연락처 · 이메일 · 전화를 리포트에 쓰지 않는다. 협업자 이름도 역할로. HAR 값 원문 금지(경로 · 키 이름 · 모양만)
- **KOS 쓰기 호출(`/commands/` · 내부 쓰기) 0건.** 실제 지점 키 금지. 우리 운영 서버(ccc) · 클러스터 무접촉
- 사용자 포트(8700 · 3000) · 프로세스 무접촉. 로컬 서버를 띄우지 마라
- canonical 체크아웃 checkout · pull · 수정 금지
- 코드 · 설계 · 정책을 정하지 않는다. 커밋 · push 금지

## 8. 검증

```
질문마다 답 + 공식 문서 URL. 문서에 없는 것은 「문서에 없음」. 결정하지 않고 「정할 것」으로 모은다
```

- 요청 항목 1-1 ~ 4 가 요약표에 **빠짐없이** 있다(항목 수 세어 보고에 적기)
- 리포트를 public 기준으로 grep(키 · 이메일 · 전화 패턴 · KOS id 모양 0) — 결과를 보고에 적기
- 못 한 확인은 사유와 함께 「미확인」으로 보고한다

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aad33590-4323-443d-9c17-3541475ee5f5 --from term_d5888b4b-3ae9-4524-8fc9-263519993e8c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
