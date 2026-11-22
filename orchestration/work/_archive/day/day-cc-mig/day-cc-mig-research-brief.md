# [researcher] cc-prototype ext API 현황 · DAY 이관 가능성 조사

너는 **day `researcher` 워커**다. **너는 이 작업의 맥락이 없다** — 아래 파일이 전부다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- `/Users/kknaks/git/CENTURION_DAY/AGENTS.md` (git ref `origin/dev` 기준 — `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:AGENTS.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig` (코디네이터와 공유 — 리포트 파일 1개 외에는 아무것도 만들거나 고치지 마라)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**읽는 레포는 전부 read-only · git ref 로 읽는다.** canonical 체크아웃은 사용자 것이다 — checkout · pull · 수정 금지, `git fetch` 와 `git show <ref>:<path>` · `git ls-tree` · `git grep <ref>` 만.

| 레포 | 경로 | 기준 ref |
|---|---|---|
| cc-prototype (이관 원천) | `/Users/kknaks/git/toy_pr2/cc-prototype` | `origin/main` = `0553173` |
| DAY (이관 대상 · CENTURION_DAY) | `/Users/kknaks/git/CENTURION_DAY` | `origin/dev` = `844eace4` |
| mediness (DAY 문서 원천) | `/Users/kknaks/git/harness_works/mediness-mediness` | `origin/main` — `products/day/` |

## 1. SSOT — 먼저 읽을 것

- cc ext 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` (0.4.7)
- cc ext 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md` · `decision-011-ext-api-add1.md` · `decision-012-ext-api-charty1.md`
- cc ext 작업 · 회고: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/para/projects/summer-star/cc-prototype/30-work/work-012 ~ work-015-*.md` · `log/2026-11-12-api-swagger-docs.md` · `log/2026-11-16-ext-api-charty1.md` · `log/2026-11-17-ext-api-staff-fields.md`
- DAY 데이터 정본: `/Users/kknaks/git/harness_works/mediness-mediness` `origin/main:products/day/40-architecture/erd.md` · `products/day/20-spec/spec-000-data-model.md` · `products/day/10-decision.md` · `products/day/40-architecture/system.md` · `deployment.md`
- DAY 데이터 기본 규칙: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/config/projects/day.json` 의 `data_rules`
- 직전 DAY 작업(고객 ERD · 동기화 · 백필): `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/_archive/day/customer-erd/`

기대는 개념: 해당 없음 (조사 — 판단은 「정할 것」으로 올린다).

## 2. 배경 / 무엇을 바꾸나

cc-prototype `procedure/back` 에 외부 연동처(서비스)용 ext API(`/api/ext`, 연동처 키)를 만들어 데모 테넌트로 시험했다. 이제 이것을 **DAY 로 옮기고 고도화**한다. 연동 담당자에게는 도메인 `day.medisolveai.com` 을 안내할 예정이다.

**사용자가 정한 목표 구조 (2026-11-20 — 이 방향이 되는지를 판정하라, 다시 설계하지 마라):**

- **KOS 와의 통신은 DAY 만 한다.** 각 서비스(ext API 를 쓰는 연동처)는 KOS 를 직접 부르지 않는다.
- 흐름 = **KOS → DAY → 각 서비스 API**. 각 서비스는 DAY 가 가진 값을 받는다.
- 각 서비스가 자기 역할을 끝내면 **결과를 DAY 에 준다** → DAY 는 **자기 DB 를 갱신**하고 → **KOS 와 동기화**한다.

cc-prototype 은 DB 없이(또는 얇게) KOS 를 그때그때 호출해 넘기는 구조였을 수 있다 — 그 차이가 이번 조사의 핵심이다.

## 3. 계약

해당 없음 (조사). 산출물은 리포트 1개.

## 4. 먼저 읽을 핵심 파일 (cc `origin/main`)

- `procedure/back/app/api/ext.py` (551줄) — 엔드포인트 13개: `GET /menu` · `POST /customers/lookup` · `POST /reservations` · `GET /availability` · `POST /customers/visits` · `POST /customers/reservations` · `GET /reservations/board` · `GET /reservations/{reservationId}` · `PUT /customers/{customerId}/language` · `PUT /reservations/{reservationId}/order-memo` · `PUT /reservations/{reservationId}/consultation-memo` · `GET /clinic` · `GET /clinics/{clinicId}/staff` — **이 목록을 믿지 말고 직접 다시 세라**(router prefix · include 위치 포함, ext 외 연동처가 쓰는 다른 경로가 있으면 같이)
- `procedure/back/app/schemas/ext.py` (511줄) — 응답 · 요청 필드
- `procedure/back/app/service/ext.py` (902줄) — 각 값을 어디서 가져오나(KOS 공개 · 내부 API / cc DB / 계산)
- `procedure/back/app/kos/client.py` — KOS 호출(공개 · 내부 두 토큰)
- 연동처 키 인증 코드 · 설정(키 저장 위치 · 연동처 구분) — grep 으로 찾아라
- `procedure/back/tests/test_ext_*.py` — 시험된 동작

DAY `origin/dev`:
- `backend/day/models/*.py` — 테이블 (customer · visit · reception · task · staff · hospital · menu · purchase · ticket · prepaid_card · prescription · room …)
- `backend/day/emr/kos/*` — KOS 클라이언트 · mapper · `writes.py`(DAY → KOS 쓰기) · `sale_reads.py` · `staff_client.py`
- `backend/day/tasks/` · `services/` — 동기화 · 백필 경로
- `backend/day/routers/api/*` — 지금 있는 API(외부용이 이미 있는지)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-cc-ext-report.md` (이 파일 1개만 만든다)

## 6. 조사 질문

### A. 현황 (cc-prototype)

- **A1. API 목록** — 엔드포인트 전수 표: 메서드 · 경로 · 요약 · 읽기/쓰기 · 추가된 판(SPEC-008 버전 · DEC/D-번호 · work) · 테스트 파일.
- **A2. 넘기는 값** — 엔드포인트마다 요청 필드와 응답 필드 **전수**(중첩 포함): 필드명 · 타입 · 뜻 · **값의 출처**(KOS 공개 API 경로 / KOS 내부 API 경로 / cc DB 테이블.칼럼 / 계산 · 설정값). 쓰기 API 는 KOS 의 어디에 무엇을 쓰는지.
- **A2-1. 같은 이름 · 다른 출처 구분 (사용자 2026-11-20 — 「API 에 맞지 않는 데이터를 주는 곳이 있다」)** — 사용자가 이 리포트로 API 를 하나씩 점검한다. 그래서 A2 의 출처 칸은 「KOS」 수준이 아니라 **KOS 의 어느 기록(어느 API 경로 · 어느 필드 · 어느 업무 시점)인지**까지 적어라. 특히 **사람 · 역할 필드**(상담사 · 원장 · 담당자 · 작성자 등)와 **상태 · 시각 필드**는 같은 이름이 여러 시점에 있다.
  - 예: `visit` 의 상담사 · 원장 — 응답이 주는 값이 **상담 차트에 기록된 상담사 · 원장**인가, 아니면 **예약 · 접수할 때 지정한 상담사 · 원장**인가. 사용자가 기대하는 것은 상담 차트 쪽이다.
  - 필드마다 `출처 시점`(예약 · 접수 · 상담 차트 · 시술 · 수납 …)을 적고, SPEC-008 · DEC 의 필드 설명이 말하는 뜻과 코드가 실제로 꺼내는 값이 **다르거나 애매한 곳**을 별도 표 「뜻 불일치 후보」로 모아라(필드 · 문서상 뜻 · 코드상 출처 · 근거 파일:줄). 판정은 하지 말고 후보로만.
  - DAY 쪽(B1)도 같은 기준 — DAY 테이블에 같은 이름의 칼럼이 있어도 **어느 시점의 값을 담는지**가 같아야 `있음` 이다. 다르면 `없음(시점 다름)` 으로 적어라.
- **A3. 인증 · 연동처** — 연동처 키 방식(헤더 · 저장 · 발급 · 지점 범위), 지금 등록된 연동처(이름만 — **키 값 · 비밀값 절대 리포트에 쓰지 마라**), 에러 형식 · Swagger 문서 노출 방식.
- **A4. 실제 사용처** — 어떤 서비스가 어떤 엔드포인트를 쓰는지 문서 · 회고에 근거가 있는 만큼만(charty 등). 없으면 「확인 안 됨」.

### B. 이관 (DAY)

- **B1. 값이 DAY DB 에 있나** — A2 의 응답 필드 하나하나를 DAY `origin/dev` 의 테이블.칼럼에 대응시켜라. 판정: `있음`(그대로) · `가공`(있는 칼럼에서 계산 — 계산식) · `없음`. `없음` 이면 KOS 의 어디에 있는지 · DAY 가 그걸 이미 동기화로 받고 있는지 · 받으려면 무엇이 필요한지(사실만).
- **B2. 쓰기 값** — 쓰기 API(예약 생성 · 언어 · 오더 메모 · 상담 메모 등)가 바꾸는 값이 DAY DB 의 어디에 들어가야 하는지, DAY 가 그 값을 KOS 에 쓰는 경로(`emr/kos/writes.py` 등)가 이미 있는지.
- **B3. KOS → DAY → 서비스 방향이 되나** — 엔드포인트별로: DAY DB 만으로 응답 가능 / KOS 실시간 조회가 여전히 필요(이유 — 예: 예약 가능 시간 · 메뉴) / 불가. 현재 DAY 의 KOS 동기화 주기 · 트리거(근거 파일:줄)로 신선도가 어떤지.
- **B4. 서비스 → DAY → KOS 방향이 되나** — 서비스가 결과를 DAY 에 주면 DAY 가 DB 갱신 후 KOS 동기화하는 경로: 지금 DAY 에 있는 것(쓰기 큐 · 실패 처리 · 재시도 · 충돌) / 없는 것. cc 의 쓰기 API 는 KOS 에 바로 썼는지, 실패 시 어떻게 했는지.
- **B5. DAY 쪽 그릇** — DAY `origin/dev` 에 외부 API 를 받을 자리(라우터 계층 · 인증 · AGENTS.md 의 규칙상 어디에 놓이는지)와 cc 코드와 구조 차이(cc 는 service 직접 호출 · DAY 는 repository 없음 · 모델 감추기 등). 그대로 옮길 수 없는 지점 목록.
- **B6. 도메인** — `day.medisolveai.com` 이 DAY 배포 설정 · 문서(`deployment.md` · DAY 레포 `deploy/` · 프록시 설정)에 이미 있는지. 있으면 어디로 붙어 있는지, 없으면 「없음」. **DNS 조회 같은 외부 호출은 하지 않는다 — 레포 근거만.**

### C. 정할 것

조사 중 사용자 판단이 필요한 것을 표로 모아라(질문 · 선택지 · 각 선택의 근거). **결정하지 마라.**

## 7. 범위 제약 — 하지 말 것

- 어떤 레포도 수정 · 커밋 · 브랜치 생성 · checkout · pull 금지. 리포트 파일 1개만 쓴다.
- **KOS · DAY 서버 · 연동처에 실제 호출 금지**(DB 접속 · ssh · curl 포함). 레포 · 문서 근거만.
- 키 · 토큰 · 비밀번호 · 실명 환자 정보를 리포트에 쓰지 마라. `.env` 값은 키 이름만.
- 새 설계 · 스펙 초안을 쓰지 마라. 설계 제안은 C 「정할 것」의 선택지로만.
- 근거 없는 추정으로 칸을 채우지 마라 — 「확인 안 됨」으로 둔다.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · 문서 URL). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- A1 의 엔드포인트 수는 `git grep -n "@router\." origin/main -- procedure/back/app/api/` 등으로 직접 센 수와 맞아야 한다(센 명령을 리포트에 적어라).
- A2 · B1 은 필드 누락 0 — 스키마 클래스의 필드 수와 표의 행 수를 엔드포인트마다 적어 대조하라.
- 리포트 맨 위에 요약(엔드포인트 수 · B1 판정 집계 있음/가공/없음/없음(시점 다름) · B3 판정 집계 · 뜻 불일치 후보 수 · 정할 것 개수).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --from term_1b6a31fd-37a4-451d-904f-7a3ee6cfc348 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
