# [planner 재기동] charty1 — 6차만 한다

너는 이전 planner 터미널이 죽어 새로 뜬 planner 다. **앞 맥락이 없다.** 원 브리프(아래 전문)의 제약 · 완료 보고 형식을 그대로 따르고, **이번 일은 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/spec-fix-e2e1-instructions.md` 하나뿐**이다. DEC-012 · SPEC-008(0.4.4) · WORK-014 는 이미 여러 판 고쳐졌다 — 지금 파일을 읽고 그 위에 더한다. 네 워커handle = `term_623737c8-c73b-4d48-a30c-244d3c8521de`.

---


# [planner] charty 1차 — 외부 API 8개: DEC-012 · SPEC-008 0.4.0 · WORK-014

너는 **cc-prototype `planner` 워커**다. **앞 맥락은 하나도 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2` (코디 워크트리 · 코디와 공유 — 아래 산출 파일 말고는 건드리지 마라)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

`P = /Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype` · `W = /Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1`

- **조사 3개(이번 작업의 사실 근거)**: `W/research-charty1-sources.md`(1차 · 항목 1-1 ~ 4) · `W/research-clinic-staff.md`(2차 · 병원 · 직원) · `W/research-har-history-hospital.md`(3차 · 이력 조회 · get-hospital)
- `W/_RESUME.md` §2 — 사용자 결정 표(이 브리프 §2 와 같다)
- 앞 결정 · 계약: `P/10-decision/decision-010-product-ext-api.md` · `P/10-decision/decision-011-ext-api-add1.md` · `P/20-spec/spec-008-product-ext-api.md`(0.3.3) · `P/30-work/work-013-ext-api-add1.md`(WORK 모양 · 부분 검증 명령 관례) · `P/log/2026-11-12-api-swagger-docs.md`(함정)
- 코드(read-only): kknaksss/cc-prototype `origin/main` `0a58aba`. canonical `/Users/kknaks/git/toy_pr2/cc-prototype` 는 **예전 커밋에 서 있다** — 반드시 `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/<경로>` 로 읽어라(checkout · pull 금지). 주로 `api/ext.py` · `service/ext.py` · `schemas/ext.py` · `service/reservations.py`(board · detail · memo · personal) · `kos/sync.py` · `kos/reservation_sync.py` · `repository/db.py`
- HAR(로컬 · gitignore · 값 옮기지 않음): `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-11-16-cc-charty1/har/` — `병원정보.har`(get-hospital) · `상담대기2.har`(운영 시간 `get-default-operation-timetable` · `get-default-days-off` 응답 모양은 여기서)

**기대는 개념** — DEC 는 사용자 결정 · 코디 기본값을 구분해 적는다. SPEC 의 모든 칸은 조사 리포트 · 코드 · DEC 중 하나를 근거로 가리킨다. 근거 없는 정책 0.

## 2. 배경 · 결정 (사용자 승인 · 2026-11-16) → DEC-012 로 쓴다

charty(협업자)가 1차 상담 화면용으로 요청했고, linky 도 같이 쓴다. 구조는 KOS → CC → 연동처. **프로토타입이라 권한 분기 없음 · 원하는 데이터만 준다.** 권한 · 「KOS = 저장소 / CC = 원본」 전환은 별도 고도화 작업(이번 범위 밖).

사용자 결정:

- **D-01 공통** — 아래 API 전부 연동처 공통(linky · charty 같은 키 체계 · DEC-010 인증 · 호출 제한 · `ext_call` · `no-store` · Swagger tag 「외부 연동」 · 오류 모양 그대로). 연동처별 권한 분기 없음.
- **D-02 D-03 해제** — DEC-011 D-03(메모 · 의사 이름 미노출)과 「이름 + 이메일 둘 다」 규칙은 **이번에 추가하는 경로에는 걸지 않는다**(기존 6개 경로의 계약은 그대로 · 깨지 않는다). 사유: 프로토 · 사용자 결정.
- **D-04 쓰기 = KOS 먼저** — 지금 직원 API 와 같은 순서: CC 사본에서 찾고 → KOS 에 쓰고 → 성공하면 `event_log` → 사본 갱신. CC 에 먼저 쌓았다가 보내지 않는다. KOS 실패 = 연동처에 오류 그대로.
- **D-05 「차트 메모」 = 상담 메모** — 쓰기는 오더 메모 · 상담 메모 둘.
- **D-06 외주 직원 = KOS 계정**(역할 「CS팀(콜센터)」). CC 별도 저장 없음. 직원 목록 하나에서 역할로 구분.
- **D-07 제외** — 시술권 차감 · 예산 · 동행자 · 통역 필요 · 피부 진단(KOS · CC 원천 없음 · 연동처에 「없음」 회신). 시술권 만료일 칸은 KOS 에 없다 → 칸을 만들지 않는다(발행일만).

API 목록(경로는 가칭 · 코드 관례상 더 나은 이름이면 질문):

| # | API | 담는 것 | 원천(조사) |
|---|---|---|---|
| 1 | `POST /api/ext/customers/lookup` **수정** | ① `customerId`(ccc id)만으로도 조회(이름+이메일 갈래는 그대로) ② 시술권 조회를 공개 → **내부** `ticket/v1/queries/get-ticket-bundles` 로 바꿔 `tickets[].inUseCount` 추가 · 「사용 중만 남은 묶음」도 나오게(지금 통째로 빠지는 버그) ③ `prepaidCards[]`(카드별 잔액 · 포인트 · 만료일 — 공개 `getPrepaidCardSummaries`) | 1차 3-2 · 3-3 · 3-4 · 3-5 |
| 2 | `GET /api/ext/reservations/board` | 오늘 접수 목록(예약 단위) — 고객 · 내원 단계 · 접수 시각(귀가 포함) · 담당 상담사(`reservation.counselor` = KOS 「희망 상담사」, 직원 상세와 같은 값 · Swagger 에 뜻 명시) · 관리실 · 상담 여부(직원 상세와 같은 CC 판정) · **처음 상담 대기 시각** | 1차 1-1 · 2-1 ~ 2-4 · 3-1 · 3차 §1 |
| 3 | `GET /api/ext/reservations/{reservationId}` | 직원 상세의 고객 정보(기본 · 언어 · 문진 · 이전 방문 · 예약 메모 · 귀가 희망 · 유입) + 희망 시술(`requestedProcedures`) · 희망 의사 · 이전 방문의 상담자 | 1차 1-2 · 3-6 · 3-9 |
| 4 | `PUT /api/ext/customers/{customerId}/language` | 고객 언어만 — 직원 `personal` 과 같은 「다시 읽고 묶음 전체 보내기」 | 1차 1-3 |
| 5 | `PUT /api/ext/reservations/{reservationId}/order-memo` | 오더 메모 등록 · 수정(통째 교체) — 내부 `schedule/v1/commands/change-order-memo` | 1차 4-1 |
| 6 | `PUT /api/ext/reservations/{reservationId}/consultation-memo` | 상담 메모 — 공개 `updateScheduleConsultationInfo` | 1차 4-5 |
| 7 | `GET /api/ext/clinic` | 병원 정보 — 내부 `get-hospital`(17칸 중 연동처에 낼 칸) + 운영 시간(내부 `get-default-operation-timetable` · 휴무 `get-default-days-off` — 모양은 `상담대기2.har`) | 2차 §1 · 3차 §2 |
| 8 | `GET /api/ext/clinics/{clinicId}/staff` | 직원 목록 — `staffId`(ccc) · 이름 · 역할 이름(내부 `account/v2/queries/get-accounts` 의 `roleName`) · `roleTags` · 활성. 비활성 포함(`active` 로 구분). 이메일 없음 | 2차 §2 · §3 |

코디 기본값(DEC 에 「코디 기본값」으로 표시):

- **처음 상담 대기 시각 원천** = 내부 `schedule/v1/queries/get-schedule-event-logs {scheduleId}` 에서 `eventType=FlowStepChanged` · `flowStep=CONSULTATION_WAITING` 중 가장 이른 `raisedDateTimeUtc`. **실응답 미확인(JS 로만 봄)** → WORK 의 **첫 Phase 를 「데모 KOS 이 조회 1회 실호출로 모양 · flowStep 숫자 대응 확인」**으로 둔다. 일정마다 한 번 정해지면 안 바뀌므로 **CC 에 저장하고 다시 부르지 않는다**(상담 대기를 거친 일정만 · board 호출이 건수 비례로 늘지 않게). 응답이 예상과 다르면 대안 = CC 가 10초 조회 중 상담 대기로 바뀐 것을 본 시각 저장(최대 10초 늦음 · 켜기 전 값 없음). **API 칸 모양은 어느 쪽이든 같다**(null 허용).
- **열람 기록(요청 3-8)** = 요청 헤더로 연동처가 보내는 직원 id(centurion 통합 계정 · 헤더 이름은 planner 제안 · 선택 헤더)를 받아 **고객 데이터를 여는 경로**(3 예약 상세 · 1 lookup)에서 `event_log` 에 새 type 으로 남긴다(직원 id · 고객 · 예약 · 시각). `ext_call` 의 「고객 id 를 안 싣는다」 원칙은 그대로. 이 직원 id 는 **연동처가 신고한 값이고 CC 가 검증하지 않는다**고 DEC · SPEC 에 적는다. 쓰기(4 · 5 · 6)의 행위자 = `ext:<연동처>:<직원 id>`(헤더 없으면 `ext:<연동처>`).
- **clinicId** — CC 서버 하나는 KOS 병원 하나(`kos_tenant_id`)에만 붙는다. 7 의 응답에 `clinicId` 를 주고 8 은 그 값만 받는다(다른 값 404). 값을 무엇으로 할지(KOS 테넌트 id 를 그대로 낼지 · CC 고정 값) planner 제안 · 질문.
- **직원 목록의 시스템 계정** — `kos_exclude_account_ids`(시스템 계정)는 빼는 쪽 기본. 근거는 2차 §3.
- 병원 정보 17칸 중 낼 칸 — 연동처가 「병원 정보」로 쓸 기본 칸(이름 · 주소 · 전화 · 운영 시간)을 기본으로 하되, 나머지(대표자 · 사업자 번호 · 요양기관 번호 · 국적 · 언어 등)는 planner 가 표로 올리고 질문으로 모은다.
- board 신선도 · 부분 실패: 직원 화면과 같은 10초 사본 · 날짜 조회 실패 시 낡은 사본 + 표시(직원 board 관례) · 상세 일부 실패 시 칸 null + 오류 칸(직원 상세 관례) — 조사 1차 §6-13 근거로 SPEC 에 명시.

## 3. 계약 — 지킬 것

- **기존 ext 6개 계약을 깨지 않는다.** lookup 은 필드 **추가**만(이름 · 뜻이 바뀌는 칸 0). 「사용 중만 남은 묶음이 새로 나온다」는 행동 변화는 변경 이력과 Swagger 에 적는다.
- 직원 API 동작 무변경.
- 경로마다 **요청 1번당 KOS 호출 수**를 SPEC 에 적는다(조사 리포트 수치 그대로).
- 내부 API 의존이 늘어나는 곳(시술권 · 개인 묶음 · 오더 메모 · get-hospital · 계정 · 운영 시간 · 이력)을 SPEC 한 표로.

## 4. 산출 (이 파일들만)

- `P/10-decision/decision-012-ext-api-charty1.md` — accepted · D-번호 · 사용자 결정 / 코디 기본값 구분 · DEC-010 · DEC-011 연결(DEC-011 D-03 을 새 경로에서 푼다는 것을 명시) · 열린 것은 「열림」으로(이력 조회 실응답)
- `P/20-spec/spec-008-product-ext-api.md` → **0.4.0**: 8개 경로 계약(요청 · 응답 칸 · 오류 표 · 시험 T 번호 이어서) · KOS 호출 수 · 내부 의존 표 · 변경 이력
- `P/30-work/work-014-ext-api-charty1.md` — backend WP. Phase 0 = 이력 조회 데모 실호출 확인. Phase 마다 부분 검증 명령(`uv run pytest -k …` 등). 끝 조건에 **데모 KOS 실물 호출**(쓰기는 시험 고객 · 끝나면 되돌림) · 기존 6개 회귀
- 세 폴더 README · `P/work-index.md` 행

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/cc-prototype/10-decision/` (DEC-012 와 README 만)
- `para/projects/summer-star/cc-prototype/20-spec/`
- `para/projects/summer-star/cc-prototype/30-work/`
- `para/projects/summer-star/cc-prototype/work-index.md`

## 6. 진행 단계

1. §1 읽기(조사 3개 먼저) → 2. 코드 사실 확인(`git show origin/main:`) → 3. DEC-012 → 4. SPEC-008 0.4.0 → 5. WORK-014 → 6. README · 인덱스 → 7. public grep

## 7. 범위 제약 — 하지 말 것

- **public 레포다** — 키 · 토큰 · 테넌트 id · KOS id · 실명 · 실제 이메일 · 전화 · 병원 이름 원문 0. 협업자는 역할로(연동처 이름 linky · charty 는 써도 됨 · 기존 문서 관례).
- 코드 · 설정 수정 금지. KOS 호출 금지(문서 작업). 커밋 · push 금지.
- 정책을 새로 만들지 않는다 — §2 에 없는 것은 「질문」으로 모아 보고. 사용자 결정을 다시 묻지 않는다.

## 8. 검증

```
SPEC 의 모든 절이 DEC · workflow · 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 실명 0(grep)
```

- §2 API 8개 · D-01 ~ D-07 · 코디 기본값이 DEC · SPEC 에 빠짐없이 있다(대조표를 보고에)
- public grep(이메일 · 전화 · uuid · hex24 · 키 패턴 0) 결과를 보고에

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aad33590-4323-443d-9c17-3541475ee5f5 --from term_889ea549-2ad0-479e-a6ee-f17f460839e6 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
