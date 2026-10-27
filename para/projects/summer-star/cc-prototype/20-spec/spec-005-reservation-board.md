---
type: spec
id: SPEC-005
title: "전체현황판 「현황 › 예약 현황」 — 스케줄 표 · 예약 등록 · 예약 상세(접수 묶음 · 실장 호출 · 귀가 정산) · KOS 데모 지점 계약"
version: 0.3.0
status: draft
product: cc-prototype
feature: procedure
created_at: 2026-10-26
updated_at: 2026-10-27
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-009-reservation-board|BASE-009]]"
  decisions:
    - "[[decision-006-reservation-board|DEC-006]]"
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-003-procedure-board|SPEC-003]]"
    - "[[spec-004-procedure-app|SPEC-004]]"
  works:
    - "[[work-007-reservation-board|WORK-007]]"
  releases: []
  related: []
sources:
  - "orchestration/work/overall-board/_RESUME.md §2 (2026-10-26 줄) · §1 (2026-10-26 메모)"
  - "reference/2026-10-26-cc-reservation/workflow-v3.md (r2)"
  - "orchestration/work/overall-board/reservation-*-report.md (15건 · 2026-10-26)"
  - "reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html (M:93-715) · design-analysis-report.md"
  - "reference/2026-10-12-cc-prototype/kos-demo-api.md (공개 API 경로)"
  - "cc-prototype overall-board procedure/ (d05cd88 — 읽기만)"
  - "orchestration/work/overall-board/reservation-review-doc-r1.md (r1 · FAIL 3 · WARN 9)"
  - "orchestration/work/overall-board/reservation-kos-probe-report.md (WP-KOS · 2026-10-26)"
  - "orchestration/work/overall-board/reservation-e2e-feedback.md (E2E batch 1 · 23건 · 2026-10-27)"
  - "orchestration/work/overall-board/_RESUME.md §2 (2026-10-27 줄) · §1 (2026-10-27 메모)"
  - "orchestration/work/overall-board/reservation-e2e-batch1-brief.md (BE · FE 몫)"
---

# 전체현황판 「현황 › 예약 현황」 계약

> `procedure/back`(FastAPI) · `procedure/front`(Next.js) 가 **시술 현황(SPEC-003)에 더해** 지킬 계약. 정책의 원천은 DEC-006(D-01 ~ D-57),
> 업무 흐름은 `reference/2026-10-26-cc-reservation/workflow-v3.md`, 화면 정본은 전체현황판 시안 「예약 현황」(`M:93-715`).
> 시안과 DEC-006 이 다르면 DEC-006 이 맞다(§6.8). DEC-006 과 `_RESUME` 가 다르면 `_RESUME` 가 맞다.
> **웹 계약이 정본이다**(D-02) — 앱은 이 문서를 따라 나중에 맞춘다.
> SPEC-003(시술 현황) · SPEC-004(계정 · 역할)의 계약은 **바꾸지 않는다** — 이 문서가 더하는 것은 §1.1 표에만 있고, 겹치는 곳(계정 역할 · 헤더 메뉴 · 경로 수)은 이 문서가 「더한다」고 적은 것만 더해진다.
>
> 근거 표기: `D-nn` = DEC-006 · `DEC-005 D-nn` · `R§` · `Q§` · `U§` · `C§` · `RM§` · `RT§` · `MT§` · `MC§` · `CS§` · `PD§` · `PP§` · `PC§` · `TA§` · `RX§` · `RXD§` = 리포트 15건(약호는 workflow-v3 머리말 표) · `M:n` = 시안 줄 · `DA§` = `design-analysis-report.md` 절 · `KDA` = `kos-demo-api.md` · `v3 n` = workflow-v3 절 · **`기본값`** = 결정에 없어 이 문서가 고른 구현값(§10 에 「planner 기본값 — 사용자 확인 대기」로 같이 올린다).
> **이 레포는 public** — 키 · 토큰 · 비밀번호 · 계정 이메일 · 실명 · 연락처 · KOS id 값 · 실제 금액을 쓰지 않는다. env 는 이름만. **시안 실명 치환 규칙**: 시안의 공지 예시 · 직원 · 상담사 · 고객 이름은 코드 · 가짜 데이터 · 스크린샷 · 시험에 옮기지 않는다 — 필요하면 「고객 A」 · 「상담사 1」 · 「공지 예시입니다」 같은 지어낸 값으로 바꾼다(디자인 Q-22).

## 0.3.0 변경 (2026-10-27 r3 — E2E batch 1)

원천 = 사용자 로컬 E2E batch 1(`reservation-e2e-feedback.md` 23건 · 코드 `3c3c6ad`) · 사용자 결정 = `_RESUME` 2026-10-27 줄(DEC-006 **D-51 ~ D-57**). 구현(backend · frontend)이 같은 원천으로 병렬로 고친다(`reservation-e2e-batch1-brief.md`) — **이 문서와 그 결과가 다르면 batch 1 보고로 맞춘다**(planner 가 고친다). 23건 → 절 전부는 **부록 F**. 뒤집힌 줄은 지우지 않고 ~~취소선~~ + 「(0.3.0 바뀜)」.

| 바뀐 것 | 절 |
|---|---|
| **세로축 = 06:00 ~ 22:00 고정**(D-57) · 운영 시간은 칸마다 회색 · 첫 렌더 지금 시각 자동 스크롤 · `axis` 는 늘 06–22 | §5.2 · §6.3 · §7.2 |
| **진행 경로 = 접수 때 고르는 ccc 값**(D-51) — 초진 · 재진 모두 · 기본 상담 필요 · KOS `consultationRequired` 안 읽음 · 안 씀 · `PUT …/route` 없앰 · [접수 완료] 요청에 `route` | §3.2 · §5.6 · §5.8 · §5.14 · §6.6 · §7.3 · §7.5 · §8 |
| **[접수 완료] 신분 조건 없음**(D-54) — 방만 고르면 켜짐 · `identity_incomplete` 없앰 · 신분 칸 줄 · 꺼짐 이유 뺌 | §5.6 · §5.12 · §5.14 · §6.6 · §7.3 · §7.5 |
| **[+ 상담 추가]**(D-55) — 「내원 현황」 머리 · KOS 공개 `changeFlowStep(CONSULTATION_WAITING)`(batch 1 데모 시험 결과로 확정) · 새 경로 1 | §5.8 · §5.14 · §6.6 · §7.5 · §8 |
| **등록 모달에서 당일 지정 의사 · 상담 필요 · 수면마취 뺌**(D-53) · **이름 같은 고객 경고 뺌**(D-56) · 고객 검색 = 조건 없이 첫 페이지 · SNS 종류 = KOS enum 드롭다운 | §5.5 · §6.5 · §7.4 · §7.5 · §8 |
| **상세 모달 열린 동안 5초 폴링**(D-52 · 수납 반영) · [귀가 완료] 성공 → 모달 닫기 + 토스트 · 「수납 필요 N건이 남아…」 문구 뺌 · 접수 성공 뒤 즉시 낙관 표시 | §4.2 · §5.10 · §6.6 · §6.7 |
| 화면 고침(사용자 지적 — 결정 아님): 예약 현황 전체 select · date · time = DS 컴포넌트 · 날짜 글자 → 달력 · 칸 폭 = 시안 식 · 카드 = 2줄 콤팩트 · [+] · 미리보기 · 카드가 줄 경계 안 · 칸 머리 정원 한 꼴 · 공지 높이 반응형 고정 비율 · 공지 시각 뺌 · 상세 제목 타이포 = 시안 | §5.2 · §6 머리 · §6.2 ~ §6.6 |
| §9 E2E — #3 · #7 · #8 · #9 · #14 · #19 · #21 · #28 · #30 · #33 고침 · **#36 ~ #41 더함** · 대조표 | §9 |
| §10 — OQ-719 · OQ-723 · OQ-750 · OQ-759 다시 처분 · OQ-704 · OQ-706 · OQ-744 · OQ-757 · OQ-758 고침 · **OQ-761 ~ OQ-767 새로** | §10 |

## 0.2.0 변경 (2026-10-26 r2)

원천 = reviewer_doc r1(`reservation-review-doc-r1.md` — FAIL 3 · WARN 9) · 사용자 결정 U1 ~ U7(DEC-006 D-44 ~ D-50) · WP-KOS 결과(`reservation-kos-probe-report.md` — 「안 받음」 0 · 모양 다름 5). 처분 전부는 부록 C · D · E.

| 바뀐 것 | 절 |
|---|---|
| **구역 두 개 전부**(U1) — 구역 사본 `zone` · 그룹 정원 구역별 · 하루 조회 `zoneIds` = 전 구역 · 슬롯 `full` = (그룹 · 구역 · 시각) · 방 목록 · 「사용 중」 = 그 예약의 구역 · 원내 현황 구역별 묶음 · 등록 「구역」 칸 | §3.2 · §4.2 · §5.2 · §5.4 · §5.5 · §5.7 · §6.4 · §6.5 · §7.2 ~ §7.5 |
| **[접수 완료] 켜짐 = KOS 신분 칸 다 채움**(U2) · ccc 「확인 완료」는 표시만 · 409 `identity_unconfirmed` → `identity_incomplete` | §5.6 · §5.12 · §5.14 · §6.6 · §7.3 · §7.5 |
| **부도 접수 허용**(U4) · **이어 하기 규칙 다시 씀**(U5 · F1) — 이어 하기 = `RECEPTION`(방 유무 무관) · 붙은 방 고정 · 신분 조건 없음 · 끝 단계 이상이면 그대로 성공 | §5.6 · §5.14 · §7.3 · §9 #23 |
| **헤더 「현황」 = 시술 현황 그대로**(U6 · W9) · 활성 판정 두 경로 | §6.1 · §9 #1 |
| **예약 카드 「수납 필요」 Badge**(U7 · W5) — 빨간 점 대신 시술 현황 카드와 같은 꼴 | §5.9 · §6.3 · §6.8 |
| 「방 배정」 판정 잇는 키(W3) · 오늘 사본 갱신(W7) · 내부 오류 이름 · `errorProperties`(W1) · 정원 초과 동시 조작(W2) · 경로 수 내역(W6) · 코디 수락(F2) | §5.9 · §4.2 · §4.4 · §5.4 · §7.6 · §3.4 |
| WP-KOS — §4 · §8 「미확인」 → 「(2026-10-26 데모 확인)」 · 문진 제출본 최상위 · 없음 = 400 + `errorProperties` · 방 없음 = `room.id` 빈 값 · `change-tasks-room` 약 1초 뒤 · 시각 밀리초 없음 · `funnel` 모양 확정 · 귀가 거절 400 | §4.2 · §5.6 · §5.10 · §5.11 · §8 |
| §10 — OQ-701 · 703 · 716 · 718 · 719(사용자 결정) · 728 · 739 · 753 ~ 756(WP-KOS) 닫음 · OQ-757(작은 기본값 묶음 · W4) ~ OQ-760 새로 | §10 |
| 시안 대조 — §6.8 #10 · #12 고침 · #23 ~ #29 더함(W5) · 「n / N 입력」 되살림 · 국기 title = 국가명 | §6.3 · §6.6 · §6.8 |

## 1. 범위

### 1.1 In (이번 판 = 웹 + back · D-01)

| 무엇 | 근거 |
|---|---|
| 헤더 「현황」 드롭다운에 **「예약 현황」** 하위 화면 추가 — 시술 현황은 그대로(「현황」 글자 · 첫 화면 = 시술 현황 — D-49) · 같은 `procedure/` 안 · 새 기능 폴더 없음 | D-01 · D-49 · `M:70-78` |
| **스케줄 표** — 날짜 이동 · [오늘] · **구역 두 개 전부**(D-44) · 칸 = KOS 예약 그룹 전부(order 순) · 시간축(**06:00 ~ 22:00 고정** — D-57 · 칸마다 자기 간격 · 1시간 높이 같음 · 운영 밖 회색 · 칸 머리 「{정원}명 / {간격}분」 · 첫 렌더 지금 시각 스크롤) · 카드(성별 · 이름 · 발음 · 초진/재진 · 국기 · 주 상태 색 + 부상태 뱃지 · **수납 필요** — D-50) · 범례 7 · 「총 예약 N건」(취소 · 부도 뺌) · 칸 [+] → 예약 등록 · **드래그 이동**(정원 꽉 찬 칸 미리 막기 · 거절이면 원위치 + 토스트 · 길이 유지) | D-10 ~ D-14 · D-19 · D-20 · D-44 · D-50 · D-57 |
| **오른쪽 패널** — 「예약 요청」 탭 = 그 날짜 KOS 공지(읽기) + 예약 요청 목록 **자리만**(빈 상태) / 「원내 현황」 탭 = 필터 · 카드 · 수납 필요 | D-07 · D-15 · D-39 |
| **예약 등록 모달** — 고객 검색(내부 `get-visitors` · 열면 첫 페이지 목록) · 결과 표 · ~~이름 같은 고객 경고~~(0.3.0 바뀜 — D-56) · 신규/기존 · KOS 예약 칸 그대로(**당일 지정 의사 · 상담 필요 · 수면마취 뺌** — D-53) · 신규 구분 규칙 · 내부 `find-duplicated-visitor` → `create-visitor` → `reserve` | D-16 ~ D-18 · D-53 · D-56 |
| **예약 상세 모달** — 고객 기본 정보(KOS 값 먼저 → 고쳐 저장 = 읽은 묶음 전체) · 신분 확인(KOS 신분 칸 채움 상태 + ccc **웹 수동 [확인 완료] — 표시만**) · 유입 · 예약 메모 · 건강 정보(KOS 문진 읽기 · 「확인 필요」) · 특이사항(읽기 · 쓰기) · 이전 방문(오늘 뺌) · 진행 경로(**접수 때 고르는 ccc 값** — D-51) · [시술실 선택] → **[접수 완료] 묶음**(~~켜짐 = KOS 신분 칸 다 채움~~ **방만 고르면 켜짐** — D-54 · 부도도 접수 · 중간 실패는 이어 하기) · [예약 취소](취소 \| 부도) · 접수 뒤 「내원 현황」(**[+ 상담 추가]** — D-55 · 상담 카드 [상담사 선택] → [실장 호출] · 단계 카드 2계층) · 「귀가 대기」 정산(전체 · 결제 · 수납 필요 N건 · [수납하기 ›] · [처방전 출력] · [귀가 완료]) | D-21 ~ D-42 · D-45 · D-47 · D-48 · D-51 · D-52 · D-54 · D-55 |
| **계정 역할 「코디」(`coordinator`) 추가** — 권한 제한 없음(SPEC-004 §3.1 · §3.4 에 더한다 · §3.4) | D-29 · D-30 |
| ccc DB — 예약 사본(예약 · 예약 그룹 · 슬롯 · 공지 · 유입 코드 · 기타 작업 목록) + ccc 만의 것(신분 확인 · 문진 방문별 이력 · 조작 이벤트 로그 — 취소 되돌리기는 로그만) | D-03 · D-20 · D-24 · D-25 |
| 시험 = 사용자 **로컬 E2E**(데모 지점 · §9) | `_RESUME 10-26 #49` |

### 1.2 Out (「하지 않는 것」)

| 무엇 | 근거 |
|---|---|
| 앱 전부 — 고객 QR 문진 입력 · 태블릿 띄우기 · 신분증 스캐너 · 신분증 이미지 업로드 · 상담사 푸시 알림 · 상담사(실장) 계정 연결 · 동시 로그인 기기 토큰 | D-01 · D-23 · D-26 · D-29 · D-38 |
| 본사 예약 요청(Linky) 동작 · 가안 카드 · 승인/반려 모달 — 자리만(빈 목록) | D-07 |
| 취소 되돌리기 버튼(로그만 쌓는다) | D-20 |
| KOS 소켓 실시간 — 조회로 간다(상세 모달은 5초 폴링 — §6.7). 소켓은 **따로 검토**(시술 현황 포함 — D-52) | v3 「보류」 · PC§3 · D-52 |
| 시술 현황판 상태 2계층 맞추기 — SPEC-003 그대로 | D-43 |
| 여정 리포트 · 처방전 내용 · 수납 · 상담 기록 · 시술 추가 화면(상담사가 KOS 에서) | D-05 · D-42 |
| 공지 쓰기 · 예약 그룹 · 운영 시간 설정 · 휴무 칠하기(응답 모양 미확인 — §10 OQ-713) · 「희망 시술」(`requestedProcedures`) | D-15 · D-16 · §10 |
| 원내 현황(평면도 · 시안 하위 화면 C) · 그 밖 상단 메뉴 | `_RESUME` 10-23 |
| 운영 명동점 키 · 운영 지점 쓰기 | D-06 |

## 2. 폴더 · 실행

### 2.1 폴더 — `procedure/` 안에 더한다 (코드 레포 `kknaksss/cc-prototype` · 브랜치 `kknaksss/overall-board`)

SPEC-003 §2.1 구조 · 계층 규약(router → service → repository · 도메인 예외 · `{error:{code,message}}`)을 그대로 쓴다. 더하는 자리(파일 이름은 워커가 정해도 되고, 계층만 지킨다):

```text
procedure/back/app/
  api/reservations.py          # §7 — HTTP 만
  service/reservations.py      # 조회 조립 · 조작(§5 규칙 · §8 KOS 호출 순서)
  service/reception.py         # [접수 완료] 묶음(§5.6)
  service/fake_reservations.py # PROC_FAKE_BOARD 때 가짜 응답(지어낸 값 · §7.1)
  domain/reservation_rules.py  # 2계층 상태 · 버튼 켜짐 · 정원 · 신규 구분 · 확인 필요 — HTTP 모름
  kos/reservation_sync.py      # 날짜별 조회 · 1시간 목록 조회(구역 · 그룹 · 다른 구역 방 …) → 사본(§4.2)
  kos/client.py                # KosError 에 errorProperties(key · reason)만 더함(§4.4) — 기존 동작 그대로
  repository/                  # db.py SCHEMA · MIGRATIONS 에 §3.2 표 · 열 더함, repo.py 에 읽기/쓰기
  schemas/reservations.py      # §7 응답 · 요청 모양(front 계약)
procedure/front/
  app/(main)/reservations/live/page.tsx · app/(main)/reservations/page.tsx(→ live)
  components/reservations/     # 스케줄 표 · 카드 · 오른쪽 패널 · 등록 모달 · 상세 모달 · 팝오버
  components/common/AppHeader.tsx   # 드롭다운 항목 하나 더함(§6.1)
  lib/api.ts · lib/types.ts · lib/session.ts   # 예약 API · 타입 · 역할 coordinator
```

- `procedure/app/`(시술실 앱)은 건드리지 않는다(D-02 · §1.2)
- 시술 현황 코드(`live/page.tsx` · `components/procedures/*` · 시술 스냅샷 · SSE)는 바꾸지 않는다 — 헤더 항목 한 줄 · 공통 lib 의 타입 추가 · 코디 수락 분기(`service/actions.py` — §3.4)만

### 2.2 실행

SPEC-003 §2.2 그대로(`cd procedure && docker compose up --build` · back 8700 · front 3700 · SQLite 한 파일). 서버 시작 순서에 **예약 목록 조회 1회**(§4.2 「1시간」 줄 — 구역 · 예약 그룹 · 유입 코드 · 기타 작업 목록 · 다른 구역 방)를 직원 · 방 조회와 같이 더한다.

### 2.3 env 더함 (`procedure/.env.example` — **이름만**)

| 이름 | 뜻 | 근거 |
|---|---|---|
| `CCC_COORD_ID` · `CCC_COORD_PASSWORD` · `CCC_COORD_NAME` | 코디 계정 아이디 · 비밀번호 · 표시 이름(비면 「코디」). 비면 그 계정을 만들지 않는다(SPEC-004 §3.1 간호사와 같은 규칙) | D-29 · §3.4 |
| `KOS_WEB_BASE` | KOS 웹 주소(딥링크 [수납하기 ›] · [처방전 출력] — `{KOS_WEB_BASE}/{tenantId}/reservation/schedule/?…`). 비면 두 버튼을 끈다(글자 「KOS 웹 주소가 설정되지 않았어요」 title) | D-40 · D-42 · PD§2 · RXD§0 · 기본값 |
| `KOS_ROOM_TASK_ID` | (선택) 「방 배정」 기타 작업 id. 비면 `get-etcetera-tasks` 에서 제목 「방 배정」 · `deleted=false` 인 것 | RM§2.2 · RM Q-71 · 기본값 |
| `KOS_RESV_CACHE_SEC` | 날짜별 조회 캐시(기본 10) — §4.2 | 기본값 |
| (뜻 더함) `KOS_ZONE_ID` | 지금 env 그대로(새 env 아님). 예약 현황에서는 **기본 구역** — 등록 모달 「구역」 기본값(§5.5) · 시술 현황(SPEC-003)은 지금처럼 이 구역만 | D-44 · SPEC-003 §4 |

front: 더하는 env 없음. 국기 그림은 npm **`flag-icons`**(SVG · MIT) 의존성 하나를 더한다(§6.3 · 기본값 · OQ-734).

## 3. 데이터 모델 (D-03 · DEC-005 D-12 ~ D-15)

### 3.1 원칙

- 모든 행 = ccc id(정수 PK) + `kos_id`(있으면). KOS 에서 오는 행은 `kos_id` 로 맞춰 **덮어쓴다**(DEC-005 D-09) · ccc 만의 행은 ccc 가 만든다 — D-03
- **시술 현황 표(`visit` · `procedure` · `customer`)의 뜻을 바꾸지 않는다.** 예약 사본은 새 표 `reservation`(일정 1건 = 예약 1건)에 둔다. 같은 KOS 일정이 `visit`(시술 카드 관점)과 `reservation`(예약 관점)에 각각 사본으로 있다 — 둘 다 KOS 가 기준이라 같은 데이터다. 합치기(조회 하나로)는 §10 OQ-701 (기본값)
- `customer` 는 **같이 쓴다**(같은 KOS 고객) — 예약 조회도 `customer` 를 `kos_id` 로 덮어쓴다. 열 하나 더함: `gender`
- **저장하는 개인정보 = 카드 · 목록에 쓰는 것만**(이름 · 발음 · 성별 · 국적 · 신규 여부 · 차트번호). 상세 모달의 생년월일 · 연락처 · 여권 · 주소 · 이메일 · SNS · 특이사항 · 문진 답 · 수납은 **열 때 KOS 에서 바로 읽고 저장하지 않는다**(예외: 문진 방문별 이력 — D-24 · §3.2) — **D-46(사용자 확정 · OQ-703 닫음)**. KOS 신분 칸(§5.12)도 저장하지 않고 상세 · 접수 때 읽어 계산한다
- 조작은 `event_log` 에 추가만(DEC-005 D-13). 예약 조작의 `event_log.visit_id` 는 비우고 `payload.reservationId`(ccc id)에 둔다 — 새 열 없음
- 시각 저장 = UTC ISO 문자열(SPEC-003 §3 와 같다) · 하루 단위 = KST 날짜 `YYYY-MM-DD`

### 3.2 테이블

**KOS 사본(조회 때 덮어씀)**

| 테이블 | 필드 | 원천 · 주기 |
|---|---|---|
| `zone`(r2 — D-44) | `id` · `kos_id` · `title` · `order` · `is_default` · `present` · `synced_at` | 공개 `get-zones` · 1시간 + 서버 시작 · KDA 278행 `data[{id, title, order, isDefault}]`(데모 2 — 「4층」 기본 · 「미사용」) |
| `reservation_group` | `id` · `kos_id` · `title` · `order` · `interval_minutes` · `capacities`(json — `intervalCapacities[]` 중 **`enabled` 인 것만** `[{zoneKosId, capacity}]` · 구역별(D-44) · 하나도 없으면 `[]`) · `timetable`(json — 요일 7개 `{enabled, start "HH:MM", end "HH:MM", breakStart, breakEnd}` KST 로 바꿔 둠) · `close_buffer_min`(`sameDayCloseBufferMinutes` — 저장만) · `present` · `synced_at` | 내부 `get-reservation-groups` · 1시간 + 서버 시작 · TA§2 |
| `reservation`(일정 1건) | `id` · `kos_id`(scheduleId) · `customer_id` · `day`(KST 날짜 — 첫 묶음 시작 기준) · `zone_kos_id` · `status`(`reservation.status`) · `flow_step` · `flow_step_at` · `reception_at` · `resources`(json — `occupiedResources[]` 그대로 줄인 것 `[{kosId, groupKosId, zoneKosId, startAt, endAt, doctors:[{id,name}]}]`) · `consultation_required`(**사본만 — 화면 · 규칙에 쓰지 않는다** · 0.3.0 · D-51) · `sedation_required`(상세 읽기만 · 등록 칸 없음 — D-53) · `counselor`(json `{id,name}` \| null) · `assignee`(json \| null) · `memo`(`reservationMemo`) · `funnel`(json — 일정 응답 모양 그대로) · `connected_channel` · `desired_discharge_at` · `purchase_ids`(json) · `prescription_ids`(json) · `tasks`(json — `[{type, sequence, title, status, paymentRequired, roomKosId, roomTitle, roomAssignedAt}]` · **`room.id` 가 빈 문자열이면 `roomKosId = null`** — KOS 는 방 없는 작업도 `room:{id:""…}` 객체를 준다 · WP-KOS 주의 3) · `room_kos_id` · `room_title`(카드 방 — SPEC-003 §3.3 `_card_room_task` 와 같은 규칙) · `kos_updated_at` · `present` · `synced_at` | 내부 `get-schedules-for-reservation` · 날짜별(§4.2) · R§1.1 · 구역 = 전 구역(D-44) |
| `reservation_slot` | PK(`group_kos_id`, `zone_kos_id`, `start_at`) · `end_at` · `capacity` · `reservation_count` · `synced_at` | 공개 `getReservationSlotsByGroupsV2` · 날짜별 · C§4 |
| `notice` | `id` · `kos_id` · `content` · `released_at` · `deleted` · `synced_at` | 내부 `get-notices` · 날짜별 · R§1 #15 |
| `funnel_code` | `id` · `kos_id` · `name` · `order` · `closed` · `is_default` · `synced_at` | 내부 `get-codes{FUNNEL}` · 1시간 · C§1.1 #7 |
| `etc_task_def` | `id` · `kos_id` · `title` · `deleted` · `synced_at` | 내부 `get-etcetera-tasks` · 1시간 · RM§1 P4 |
| `customer`(같이 씀) | **열 더함** `gender`(`MALE` · `FEMALE` · `GENDER_UNSPECIFIED`) — MIGRATIONS 에 한 줄 | 일정 `visitor.gender` · R§3.1 8행 |

`staff`(상담사 = `role_tags` 에 `COUNSELOR` · 원장 = `is_doctor`) · `room` 은 SPEC-003 §3.2 표를 그대로 쓴다(D-34 · D-36).

**ccc 만의 것(KOS 에 없음)**

| 테이블 | 필드 | 근거 |
|---|---|---|
| `identity_check`(신분 확인 · 추가만 · **표시만 — 접수 조건 아님 · D-45**) | `id` · `customer_id` · `status`(`confirmed` \| `unconfirmed`) · `method`(`web_manual` — 이번 판 · 나중 `scanner`) · `device`(null — 스캐너 판) · `checked_at` · `actor` · `event_id`. **고객의 지금 상태 = 그 고객의 마지막 줄**(없으면 미확인) | D-25 · 기본값(고객 단위 — 시안 「이전 방문 때 등록된 신분 정보」 `M:333`) · OQ-733 |
| `questionnaire_history`(문진 방문별 이력 · 추가만) | `id` · `customer_id` · `reservation_id`(그때 연 예약 · null 가능) · `kos_submitted_at`(KOS 제출본 `createdDateTimeUtc`) · `answers`(json — KOS `answers[]` 그대로) · `fetched_at`. UNIQUE(`customer_id`, `kos_submitted_at`) | D-24 · 기본값(읽기 때 쌓기 — §5.11 · OQ-732) |
| `event_log`(그대로) | 새 `type` — 아래 | DEC-005 D-13 |
| `account`(그대로) | `role` 값 하나 더함 `coordinator` — §3.4 | D-29 |

`event_log.type` 더함(payload 는 ccc id 만 · KOS id · 개인정보 값 없음):

| type | payload | 언제 |
|---|---|---|
| `resv_create` | `{reservationId, customerId, newCustomer, groupId, start, end}` | 예약 등록 성공 |
| `resv_move` | `{reservationId, resourceIndex, from{groupId,start,end}, to{groupId,start,end}}` | 이동 성공 |
| `resv_cancel` | `{reservationId, reason, prevStatus}` — **취소 되돌리기의 원천**(D-20) | 취소 · 부도 성공 |
| `resv_memo` · ~~`resv_route`~~ | `{reservationId}` · ~~`{reservationId, consultationRequired}`~~ | 메모 · ~~진행 경로~~(0.3.0 바뀜 — 진행 경로는 KOS 쓰기가 없어 로그도 없다 · `reception.route` 에 남는다 · D-51) |
| `visitor_personal` · `visitor_remark` | `{customerId, fields:[바꾼 칸 이름]}` · `{customerId}` | 고객 정보 · 특이사항 |
| `identity` | `{customerId, status}` | 신분 확인 표시 |
| `reception` | `{reservationId, roomId, route, endStep, steps:[끝낸 단계 이름]}` — `route` = `consultation` \| `direct`(0.3.0 · D-51) | [접수 완료] 성공(또는 일부 — §5.6) |
| `consultation_add` | `{reservationId, fromStep}` | [+ 상담 추가] 성공(0.3.0 · D-55 · §5.8) |
| `counselor_call` | `{reservationId, counselorStaffId}` | [실장 호출] |
| `discharge` | `{reservationId}` | [귀가 완료] |
| `kos_rejected` | `{reservationId?, customerId?, op, httpStatus, kosError}` | 위 조작의 KOS 호출이 거절 · 실패(§4.4) |

새 표 · 열은 서버 시작 때 `CREATE TABLE IF NOT EXISTS` + `MIGRATIONS`(지금 `repository/db.py` 방식)로 생긴다 — 기존 DB 파일이 그대로 남는다.

### 3.3 KOS 필드 대응표

| ccc | KOS | 어디서 | 근거 |
|---|---|---|---|
| `reservation.kos_id` · `flow_step` · `flow_step_at` · `reception_at` · `kos_updated_at` · `zone_kos_id` | `id` · `flowStep` · `flowStepUpdatedDateTimeUtc` · `receptionDateTimeUtc` · `updatedDateTimeUtc` · `zone.id` | 일정(`get-schedules-for-reservation` `data[]`) | R§1.1 · WP-KOS K1 |

시각 읽기: `occupiedResources[].reservationTime` 은 밀리초 없는 `…:00Z`, `desiredDischargeDateTimeUtc` 는 `….000Z` 로 온다 — **문자열로 비교하지 않고 파싱해서 비교한다**(WP-KOS 주의 5). `desiredDischargeDateTimeUtc` 는 값이 있을 때만 키가 온다(K1).

| `reservation.status` · `consultation_required` · `sedation_required` · `counselor` · `assignee` · `memo` · `funnel` · `connected_channel` · `desired_discharge_at` | `reservation.status` · `consultationRequired` · `sedationRequired` · `counselor{id,name}` · `reservationAssignee{id,name}` · `reservationMemo` · `funnel` · `connectedChannel` · `desiredDischargeDateTimeUtc` | 같은 일정 | R§1.1 · C§2.2 |
| `reservation.resources[]` | `occupiedResources[]{id, reservationTime{startDateTimeUtc, endDateTimeUtc}, reservationGroup{reservationGroupId, zoneId, doctors[]}}` — **그룹 id 원천 = 이것**(없으면 `reservation.reservationGroupId`) | 같은 일정 | R§1.1 · R Q-21 · 기본값(OQ-702) |
| `reservation.purchase_ids` · `prescription_ids` | `purchaseIds[]` · `prescriptionIds[]` | 같은 일정 | PD§4 · RXD§0 |
| `reservation.tasks[]` | `tasks[]{type, sequence, title, status, paymentRequired, room{id,title}, roomAssignedDateTimeUtc}` — `room` 은 늘 객체 · 방 없음 = `room.id` 빈 값 | 같은 일정 | R§1.1 · PP§0 · WP-KOS K8(2026-10-26 데모 확인) |
| `customer.kos_id` · `name` · `phonetic_name` · `gender` · `nationality` · `is_new` · `chart_number` | `visitor.id` · `name` · `phoneticName` · `gender` · `nationality` · `isNew` · `chartNumber` | 같은 일정 · 고객 검색 결과 | R§3.1 6 ~ 11행 |
| `zone.*` | `id` · `title` · `order` · `isDefault` | 공개 `get-zones` `data[]` | KDA 278행 · R§4 233행 |
| `reservation_group.*` | `id` · `title` · `order` · `intervalMinutes` · `intervalCapacities[{zoneId, enabled, intervalCapacity}]`(→ `capacities` 구역별) · `operationTimetable{monday…sunday{enabled, startTime, endTime, breaktime{startTime,endTime}}}`(날짜 붙은 UTC — 시 · 분만 KST 로) · `sameDayCloseBufferMinutes` | `get-reservation-groups` `data[]` | TA§2 |
| `reservation_slot.*` | `data[{reservationGroupId, zoneId, slots[{startDateTimeUtc, endDateTimeUtc, capacity, reservationCount}]}]` | `getReservationSlotsByGroupsV2` | C§4 |
| `notice.*` | `data[{id, content, releaseDateTimeUtc, deleted}]` | `get-notices` | R§1 #15 |
| `funnel_code.*` | `data[{id, category, name, order, closed, default}]` | `get-codes{FUNNEL}` | C§1.1 #7 |
| `etc_task_def.*` | `data[{id, title, deleted}]` | `get-etcetera-tasks` | RM§1 P4 |

### 3.4 계정 역할 「코디」 — SPEC-004 §3 에 더한다 (D-29 · D-30)

| 항목 | 계약 |
|---|---|
| 값 | `account.role` = `admin` \| `doctor` \| `nurse` \| **`coordinator`** · back `schemas` `Role` · front `lib/types.ts` `Role` · `lib/session.ts` `ROLES` 에 더함 |
| 만드는 법 | 서버 시작 때 `CCC_COORD_ID` · `CCC_COORD_NAME`(비면 「코디」) 으로 1행 upsert · 비밀번호 `CCC_COORD_PASSWORD`(bcrypt) — 지금 `service/accounts.py` `_fixed` · `_passwords` 의 간호사 규칙과 같다 |
| 권한 | **제한 없음**(D-30) — 시술 현황 API(SPEC-004 §3.4 표)는 **관리자와 같다**(수락은 `doctorId` 필수 · 관리자 규칙). 이 문서의 예약 API(§7)는 **네 역할 모두 ○**(직무별 제한은 마지막 — D-30) |
| 역할 분기를 쓰는 곳(전수) | back `actor.role ==` = **`service/actions.py` `accept()` 한 곳** — `admin` 분기를 `admin` \| `coordinator` 로 넓힌다(안 넓히면 코디 수락 = 403 `role_forbidden` · r1 F2). front = `lib/types.ts` `Role` · `lib/session.ts` `ROLES`. 그 밖 역할 분기 없음(review-doc r1 F2 grep) |
| 로그인 · 헤더 | SPEC-004 §3.3 · §3.6 그대로(아이디 + 비밀번호 · 헤더 표시 = `name`) |
| 푸시 | 원장 호출 푸시(SPEC-004 §5-1) 대상이 아니다(지금 대상 계산 그대로) |
| 상담사(실장) 계정 | 이번 판 없음(D-38) |

## 4. KOS 연동

### 4.1 인증 · 토큰

SPEC-003 §4.1 그대로(공개 `exchange-token` · 내부 시스템 계정 `sign-in` · 401 재로그인 1회). 시스템 계정 id(`kos_token.account_kos_id`)는 **예약 담당자 기본값**에도 쓴다(§5.5 · OQ-710).

### 4.2 조회 — 무엇을 언제

내부 = `{KOS_INTERNAL_API_BASE}/tenants/{tenantId}/<경로>` · 공개 = `{KOS_OPEN_API_BASE}/<경로>`(지금 `KosClient.internal` · `.open`). 경로는 앞 `/` 없이 적는다.

| 무엇 | 종류 · 경로 | 본문 | 언제 | 근거 |
|---|---|---|---|---|
| 구역 | 공개 `schedule/open/zone/v1/queries/get-zones` | `{}` | **1시간 + 서버 시작**(직원 · 방과 같은 주기 · SPEC-003 §4.2) | KDA 123 · 278행 · R§4 233행 · D-44 |
| 예약 그룹 | 내부 `schedule/group/v1/queries/get-reservation-groups` | `{deleted:false, zoneIds:[zone 사본 전부]}` | 같음 | R§1 #9 · TA§1 #196(KOS 화면은 `zoneIds[2]`) · WP-KOS K1(2026-10-26 데모 확인) |
| 다른 구역 방 | 내부 `schedule/zone/room/v1/queries/get-rooms` | `{zoneId}` — `KOS_ZONE_ID` **밖** 구역마다 1번(4층은 SPEC-003 직원 · 방 조회가 이미 읽는다) → 같은 `room` 사본(`zone_kos_id` 로 구분) | 같음 | R§1 #1 · D-44. 시술 현황은 방을 id 로만 찾으므로(`rooms.get`) 행이 늘어도 바뀌지 않는다 |
| 유입 코드 | 내부 `meta/codes/v1/queries/get-codes` | `{category:"FUNNEL"}` | 같음 | C§1.1 #7 · WP-KOS K1 |
| 기타 작업 목록 | 내부 `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` | `{}` | 같음 | RM§1 P4 · RT§1 |
| 하루 예약 | 내부 `schedule/v2/queries/get-schedules-for-reservation` | `{baseDateUtc: <그 날짜 KST 00:00 의 UTC — "YYYY-MM-DDT15:00:00.000Z" 꼴(전날)>, reservationGroupIds:[present 그룹 kos_id 전부], zoneIds:[present 구역 kos_id 전부]}` | **날짜별 · 화면이 볼 때**(아래) | R§1 #10(KOS 화면 = `zoneIds[2]`) · §1.1 · §2 · **D-44**(두 구역) · OQ-701(닫음) · WP-KOS K1 |
| 칸 정원 · 예약 수 | 공개 `schedule/open/v2/queries/get-reservation-slots-by-groups` | `{reservationGroupIds:[…], startDateTimeUtc, endDateTimeUtc}` = 그 날짜 KST 하루 → `data[{reservationGroupId, zoneId, slots[…]}]` = **그룹 × 구역마다** | 같음 | C§4 · KDA 171행 · WP-KOS K1 |
| 공지 | 내부 `meta/notice/v1/queries/get-notices` | `{startDateTimeUtc, endDateTimeUtc, deleted:false}` = 그 날짜 KST 하루 | 같음 | R§1 #15 · §3.5 · D-15 · WP-KOS K1 |
| 원내 현황 금액 | 공개 `purchase/open/v1/queries/get-purchase-summaries` | `{purchaseIds:[오늘 원내 일정들의 purchaseIds 합]}` — 비면 부르지 않음 | 같음(오늘만) | PD§4 · KDA 74행 |

**날짜별 조회 규칙**(기본값 — OQ-704 · 하루 1번 · 시술 현황 조회와 합치지 않음 — OQ-701 닫음 · D-44):
- `GET /api/reservations/board?date=` 가 오면 back 이 그 날짜의 마지막 조회 시각을 본다. `KOS_RESV_CACHE_SEC`(기본 10초)보다 오래됐으면 위 「날짜별」 넷을 차례로 불러 사본에 덮어쓴 뒤 응답한다 · 아니면 사본으로 바로 응답. 같은 날짜 조회가 동시에 오면 한 번만 부른다(날짜별 잠금)
- front 는 화면이 열려 있는 동안 **10초마다** 그 날짜를 다시 부른다(§6.7). 그래서 「보고 있는 날짜만 10초」가 된다 — 백그라운드 루프를 더하지 않는다
- **오늘 사본이 쓰이는 계산**(방 「사용 중」 §5.7 · 상담사 지금 상태 §5.8 · 원내 현황)은 **오늘 날짜 캐시가 `KOS_RESV_CACHE_SEC` 보다 오래됐으면 계산 전에 오늘 날짜 조회를 먼저 1번 한다**(같은 날짜 잠금) — 데스크가 다른 날짜를 보다가 오늘 예약 상세를 열어도 낡지 않게(r1 W7). 상세 조회(§7.3) · 접수(§5.6 0단계) 때 이 확인을 한다
- **조회 시간(09:00 ~ 21:00 · DEC-005 D-08)은 예약 조회에 걸지 않는다** — 화면이 볼 때만 부르므로(데스크가 밤에 다음날 예약을 본다)
- 하루 예약 결과에 없는 그날 `reservation` 행은 `present = 0`(행은 남김 — 지운 예약 · 다른 날로 옮긴 예약). 다른 날로 옮겨진 예약은 그 날짜 조회 때 `day` 가 바뀐다
- 실패(네트워크 · 5xx · 401 재시도 뒤 · 2xx 인데 `data` 가 배열 아님)는 그 날짜 `sync.lastError` 로 응답하고 사본 그대로 — SPEC-003 §4.2 와 같은 규칙. 로그엔 예외 종류 · HTTP 상태만
- 슬롯 · 공지 · 금액 조회가 실패해도 예약은 보인다(그 칸만 빈 값 · `sync.lastError` 에 이름)

**상세 조회**(예약 상세 모달을 열 때 · 조작 뒤 · **열려 있는 동안 5초마다**(0.3.0 · D-52 — 수납 반영) · 캐시 없음 — §7.3):

| 무엇 | 종류 · 경로 | 본문 | 근거 |
|---|---|---|---|
| 고객(개인 · 관리 묶음 · 특이사항 · 신분 칸) | 내부 `visitor/v2/queries/get-visitor` | `{id: visitorId}` → `data{…}` — **빈 칸은 키 자체가 없다**(없음 = 빈 값으로 본다) | U§3 · MT§2 · C§1.3 · WP-KOS K1 |
| 문진 양식(질문 · 쪽) | 공개 `visitor/open/v1/queries/get-visitor-questionnaire` | `{visitorId}` — 응답 = 최상위 객체 · `pages[{id, title, questions[{questionId, title, sequence, answers[…]}]}]` | R§3.1 18행 · R§5.1 · KDA 143행 · WP-KOS K1(2026-10-26 데모 확인) |
| 문진 제출본 | 공개 `visitor/open/v1/queries/get-questionnaire-submit` | `{visitorId}` → **최상위 객체**(`data` 로 감싸지 않음) `{id, visitorId, createdDateTimeUtc, answers[{seq, questionId, questionTitle, answerId, answerTitle, memo}], agreements[…], …}` · **제출본 없음 = HTTP 400 `InvalidRequestException` + `errorProperties:[{key:"visitorId", reason:"NotFound"}]` → 「아직 입력되지 않았어요」**(오류 아님 — `className` 만으로는 못 가른다 · `errorProperties` 를 읽는다 · §4.4) | Q§4.1 · R§5.1 · **WP-KOS K1 주의 1 · 2(2026-10-26 데모 확인 — 0.1.0 의 `data{…}` 와 다름)** |
| 이전 방문 | 공개 `schedule/open/v1/queries/get-schedules-by-visitor` | `{visitorId}` → `data[]`(하루 예약과 같은 일정 모양) | R§3.1 20행 · D-28 · WP-KOS K1 |
| 수납(귀가 대기 · 완료만) | 공개 `get-purchase-summaries` | `{purchaseIds: 그 일정 purchaseIds}` | PD§4 |

### 4.3 덮어쓰기 · 기준 (D-03)

- KOS 에 칸이 있는 값(예약 · 상태 · 단계 · 그룹 · 시각 · 메모 · 유입 · 상담사 · 작업 · 방 · 수납 · 공지 · 그룹 설정)은 **KOS 가 기준** — 조회 때 덮어쓴다. 예약 조작은 대기열을 두지 않으므로(§4.4) 「반영 대기 중이면 덮어쓰지 않는다」 보호도 없다
- ccc 만의 것(신분 확인 · 문진 이력 · 이벤트 로그)은 조회가 건드리지 않는다
- **쓰기 뒤 반영 지연 0 ~ 3초**(RT§0 · WP-KOS: 모든 다시 읽기가 1초 첫 번째에 보였다 · `change-tasks-room` 은 0초엔 안 보이고 약 1초 뒤) — 조작이 성공하면 back 이 그 날짜 캐시를 비우고(다음 GET 이 KOS 를 다시 읽는다) front 는 응답 직후 한 번 · 2초 뒤 한 번 더 부른다(§6.7). 묶음 중간 확인은 §5.6

### 4.4 쓰기 방식 — 동기 (기본값 · OQ-705)

- 예약 조작(§7.5)은 **KOS 응답을 기다려** 성공 · 실패를 돌려준다. SPEC-003 의 `kos_op` 대기열 · 재전송은 쓰지 않는다. 근거: ① 이 조작들은 ccc 만의 상태가 없고 KOS 가 기준이라 먼저 바꿔 둘 ccc 값이 없다(D-03) ② 드래그 거절은 「카드 원위치 + 오류 토스트」(D-20)라 KOS 의 답이 바로 있어야 한다 ③ 예약 등록은 새 `scheduleId` 를 받아야 끝난다
- 성공 = KOS 2xx. 그때 `event_log` 1줄(§3.2) → 그 날짜 캐시 비움 → (단계 · 방이 바뀌는 조작이면) **시술 현황 일정 조회 1회**(`KosRuntime.tick()` — 시술 현황판 카드가 10초를 기다리지 않게 · SPEC-003 §4.4 의 빠른 확인과 같은 생각)
- KOS 4xx = **409 `kos_rejected`** · 메시지 = 한국어 한 줄 + KOS 오류 이름(`KosError` 와 같은 꼴 — 본문 · id 없음). `event_log(kos_rejected)` 1줄
- **`KosError` 에 `errorProperties` 를 더한다**(`kos/client.py` `_error_of` — `[{key, reason}]` 만 · 값 없음 · 지금 `className` 이름 문자열은 그대로). 지금은 버려서(WP-KOS K9b) 거절 이유를 못 가른다. 문구 고르기 = **`errorProperties` 의 `key reason` 먼저, 없으면 `className`**:

  | KOS 가 주는 것 | 어느 API | 문구 | 근거 |
  |---|---|---|---|
  | `startDateTime` · `NotAvailable` | 내부 `reserve` · `update-reservation`(JS `ALREADY_RESERVED`) | 「같은 고객의 예약이 그 시간에 있어요」 | C§2.2 · MC§2.2 |
  | `occupiedResources[n].startDateTimeUtc` · `NotAvailable` | 내부(JS `DIFFERENT_DATE…`) | 「묶음 날짜가 서로 달라요」 | C§2.2 |
  | `ReservationCapacityExceeded` | **공개** v2 스펙 예시 — 내부 JS 처리 목록에는 없다(받는지 미확인 · §5.4 · OQ-760) | 「그 시간은 정원이 찼어요」 | MC§2.2 · C§4 |
  | `status` · `NotAvailable` · `ReservationNotAllowedByPolicy` | 공개 `cancel-reservation` | 「지금 상태에서는 취소할 수 없어요」 · 「예약 정책상 바꿀 수 없어요」 | MC§3 |
  | `visitorId` · `NotFound` | 공개 문진 제출본 | 오류 아님 — 「아직 입력되지 않았어요」(§5.11) | WP-KOS K1 |
  | `InvalidRequestException`(그 밖) | 공개 `changeFlowStep(COMPLETED)` 거절 등 | 「KOS 가 거절했어요 ({이름})」 | WP-KOS K9b |

- KOS 네트워크 · 5xx · 401 재시도 뒤 실패 = **502 `kos_unavailable`** 「KOS 에 연결하지 못했어요」 · `event_log(kos_rejected)` 1줄
- 내부 단계 변경의 키는 **`id`**(공개는 `scheduleId`) — RM§2.3
- 키 · 토큰 · 고객 값은 로그 · 오류 메시지 · 응답에 싣지 않는다(SPEC-003 §4.1)

### 4.5 호출별 본문 → §8

## 5. 상태 · 규칙

규칙 계산은 **back 이 한다**(SPEC-003 §7.2 「규칙 한 곳」과 같다) — 상태 · 버튼 켜짐(`can*`) · 정원 꽉 참(`full`) · 「확인 필요」 · 「수납 필요」 · 「사용 중」을 front 가 다시 계산하지 않는다.

### 5.1 상태 = 2계층 (D-11)

① `reservation.status` 가 `CANCELED` · `NO_SHOW` 면 그것이 먼저 ② 아니면 `flowStep`.

| KOS | `main` | `sub` | 글자(주 · 부) |
|---|---|---|---|
| `status = CANCELED` | `canceled` | null | 취소 |
| `status = NO_SHOW` | `noshow` | null | 부도 |
| `flowStep = RESERVED` | `reserved` | null | 예약 |
| `RECEPTION` | `reception` | null | 접수 |
| `CONSULTATION_WAITING` | `consultation` | `waiting` | 상담 · 대기 |
| `CONSULTATION` | `consultation` | `doing` | 상담 · 진행 |
| `PROCEDURE_WAITING` | `procedure` | `waiting` | 시술 · 대기 |
| `PROCEDURE` | `procedure` | `doing` | 시술 · 진행 |
| `PROCEDURE_DONE` | `home` | `waiting` | 귀가 · 대기 |
| `COMPLETED` | `home` | `done` | 귀가 · 완료 |
| 그 밖(`FLOW_STATUS_UNSPECIFIED` 등) | `reserved` | null | 예약 — 기본값(KOS 값 그대로 title 에 · OQ-757) |

- 「시술 완료」 · 「상담 완료」 상태는 없다(D-11 · D-35)
- 색(범례 · 카드 막대 · 상세 머리) — 시안 `BK_BAR` 의 색을 주 상태로 다시 붙인다: 예약 `purple` · 접수 `yellow`(Badge warning) · 상담 `cons`(#15803d · 시안 인라인 클래스 그대로 복사) · 시술 `primary` · 귀가 `gray-600`(대기) / `gray-300`(완료) · 취소 `red` · **부도 `red` 외곽선**(시안에 없음 — 기본값 · Badge danger outline 느낌의 `border-red text-red bg-white` · OQ-757 · §6.8 #23) — `M:1189` · DA§3.2
- 부상태 뱃지 = 카드 이름 줄 끝 작은 글자 칩(「대기」 · 「진행」 · 「완료」) — 기본값(시안에 없음 · §6.8 #20 · OQ-757)

### 5.2 칸 · 시간축 · 카드 배치 (D-10 · D-12)

- **구역 = 두 개 전부**(D-44) — 칸은 구역으로 나누지 않는다(KOS 화면처럼 그룹 칸 하나에 두 구역 카드가 같이 놓인다 · R§1 #10). 카드마다 자기 구역(`reservation.zone_kos_id`)을 갖고, 정원 · 「사용 중」 · 원내 현황이 그 구역으로 갈린다
- **칸** = `reservation_group` 중 `present` 인 것 전부, `order` 오름차순. 칸 머리 = 「{title}」 · 「{N}건」(그 칸 카드 중 취소 · 부도 뺀 수 — D-14 · 구역 합) · 「{정원}명 / {interval_minutes}분」 — ~~{정원} = 켜진 구역이 하나면 그 수 · 둘 이상이면 「{구역} {n} · {구역} {n}명」~~ (0.3.0 바뀜 — 사용자 「칸마다 표기가 다름」 · 피드백 #7) → **켜진 구역 수와 상관없이 한 꼴: 「{구역} {n}명」을 구역 `order` 순으로 「 · 」로 잇는다**(하나면 「4층 3명 / 15분」 · 둘이면 「4층 3 · 미사용 3명 / 15분」 — 「명」은 끝에 한 번) · 하나도 없으면 「- 명」 — 기본값(OQ-758 · **frontend batch 1 결과와 다르면 그 꼴로 고친다**)
- ~~**세로축** = 그날 요일의 그룹 운영 시간의 합(데모 = 10:00 ~ 20:00) · 모두 꺼졌으면 축 없음~~ (0.3.0 바뀜 — D-57) → **세로축 = 06:00 ~ 22:00 고정**(모든 날 · 모든 칸 같은 축). 운영 시간은 칸마다 회색으로 보인다(아래). 그룹이 모두 쉬는 요일(휴무 요일)도 축은 그대로이고 모든 칸이 회색 + 판 위 「운영하지 않는 날이에요」 글자 한 줄 — 기본값(TA Q-124 — 그룹 시간표가 빈 요일은 운영 안 함으로 본다 · OQ-757 ⑦ · §6.8 #25)
- **시각 라벨 = 30분**(축 시작부터) · **칸마다 자기 간격으로 줄**(15 · 30 · 60) · **1시간 높이는 모든 칸이 같다**(기본 1시간 = 144px — 시안 30분 줄 최소 72px 와 같은 높이 · 기본값 · OQ-757)
- **운영 밖 = 회색**(`bg-ms-gray-100`) — 칸마다 그 요일 `enabled` · `start` ~ `end` 밖, 그리고 `breakStart` ~ `breakEnd`. 휴무(`get-*-days-off`)는 이번 판에 칠하지 않는다(응답 모양 미확인 · 데모 0건 — OQ-713)
- **카드** = `reservation.resources[]` **한 묶음당 한 장** — 그 묶음의 그룹 칸 · **위 = 그 묶음 시작 시각의 줄 경계**. 한 예약이 그룹 여럿을 차지하면 칸마다 한 장씩(`resourceIndex` 로 구분) — 기본값(OQ-702 · R§3.3 「일정 하나가 그룹 여러 개」)
- ~~카드 높이 = 길이(분) ÷ 60 × 1시간 높이(최소 한 줄)~~ (0.3.0 바뀜 — 사용자 「2줄로 표시하라고 했는데 왜 3줄짜리 뚱뚱이 칸이 됐지」 · 피드백 #10) → **카드 높이 = 내용 2줄 콤팩트**(시안 `M:130-149`) — 예약 길이로 늘리지 않는다. 1시간 = 144px 는 **줄(격자) 높이 규칙**이고 카드 높이와 따로다. **카드는 그 칸의 한 줄 경계를 넘지 않는다**(피드백 #7): 2줄 높이가 그 칸 한 줄보다 크면(15분 칸 = 36px) 한 줄 높이로 줄이고 2줄을 숨긴다(§6.3 「한 줄이면 2줄 숨김」) — 기본값(OQ-765)
- 같은 칸에서 **같은 시각에 겹치는** 카드는 왼쪽부터 나란히. **칸 폭 = `13 + mx·196 + (mx−1)·6`px**(시안 `M:1721-1727` 식 그대로) — `mx` = 그 칸에서 한 시각에 겹치는 카드 최대 수(최소 1) · 상한 화면 폭 1600 이상 5 · 1100 이상 3 · 그 밖 1(시안 `perRow`), 넘치면 칸 안 가로 스크롤. 사용자 「3명이 한 열에 들어가야 하는데 … 시안이랑 많이 다름」(피드백 #3) — 겹침이 3이면 3장 나란히. **정원만큼 늘 자리를 잡을지(`mx = max(겹침, 정원)`)는 열림**(OQ-763)
- 묶음 시각이 축 밖(06:00 전 · 22:00 뒤)이면 축을 그 시각까지 늘린다(카드가 잘리지 않게 · 기본값 · OQ-757 ⑤ · §6.8 #24)
- 그룹이 사본에 없는 예약(그룹이 지워짐 등) = 맨 끝 「그룹 없음」 칸 하나에 모은다(기본값 — R§3.3 옛 그룹 이름 · OQ-757 · §6.8 #24). §7.2 `columns[]` 의 그 칸 = `groupId: null` · `title: "그룹 없음"` · `intervalMinutes: 30` · `capacities: []` · `open: []`(전부 회색 아님 — 축 전체 흰색) · [+] 없음 · 드롭 금지

### 5.3 건수

- 「총 예약 N건」 = 그날 `present` 예약 중 `main ∉ {canceled, noshow}` 의 **예약 수**(묶음 수가 아니다) — D-14
- 범례 7개 옆 수 = 주 상태별 예약 수(취소 · 부도 포함 — 범례는 그 상태의 수) — 시안 「예약 N」 `M:1885`

### 5.4 정원 · [+] · 드래그 (D-20)

- 슬롯 = `reservation_slot` 의 **`(group, zone, start)` 행 — 구역별**(D-44). 행마다 **`full` = `reservation_count ≥ capacity`**(행이 없으면 `full = false` — KOS 가 거른다) — C§4
- **카드 하나의 「그 줄 꽉 참」 = 그 카드 구역의 슬롯 `full`**(드래그). **[+] 의 「그 줄 꽉 참」 = 그 줄의 켜진 구역 슬롯이 모두 `full`**(하나라도 자리가 있으면 [+] — 등록 모달에서 자리 있는 구역을 고른다 · §5.5) — 기본값(OQ-758)
- **[+]** = 운영 시간 안팎 상관없이 줄마다 호버로 보인다(시안 `M:151-156`). **그 줄의 켜진 구역 슬롯이 모두 `full` 이면 [+] 를 그리지 않는다**(§7.2 `rows[].plusAllowed = false` · 「그룹 없음」 칸도 없음). 운영 밖 · 휴무 · 시간 점유 · 당일 마감 버퍼로는 막지 않는다 — KOS 가 거르면 409 토스트(OQ-713)
- **새 예약 길이 = 그 칸 `interval_minutes`**(기본값 — OQ-712 · KOS HAR 예약은 30분 칸에 30분)
- **드래그**: 끄는 동안 놓을 칸 줄을 primary 점선 outline · 카드 미리보기 점선(시안 `M:1708-1717`). **놓을 줄의 (그 칸 그룹 · 끄는 카드의 구역) 슬롯이 `full` 이면 그 줄은 놓기 금지 표시(`cursor: not-allowed` · 빨간 점선)이고 놓아도 아무 일 없다**(D-20 「미리 막기」). 단 자기 자신이 원래 있던 줄은 `full` 이어도 놓을 수 있다(제자리). 이동은 구역을 바꾸지 않는다(`occupiedResources[].reservationGroup.zoneId` 그대로 — K3)
- 놓으면 새 시작 = 놓은 줄의 시작(그 칸 간격에 맞춤) · **길이 = 원래 길이 그대로**(D-20) · 같은 날짜 안에서만(다른 날짜로 끌 수 없다)
- 놓은 직후 카드는 새 자리로 미리 옮겨 보인다(낙관 표시) → API 실패(409 · 502)면 **원위치 + 오류 토스트**(back `message`) — D-20
- **동시 조작의 정원**(r1 W2): 내부 `reserve` · `update-reservation` 이 정원 초과를 거르는지는 **확인되지 않았다**(내부 JS 오류 처리에 정원 초과가 없다 — C§2.2 · MC§2.2 · KOS 직원 화면은 정책을 무시한다 — C Q-55 · WP-KOS 는 정원 시험을 하지 않았다). 그래서 두 데스크가 같은 줄 마지막 자리에 거의 같이 놓으면 **둘 다 들어가 정원을 넘을 수 있다** — ccc 미리 막기는 사본(10초) 기준이다. 이번 판은 받아들이고(KOS 직원 화면과 같은 수준) E2E #12 에서 KOS 가 어떻게 하는지 기록한다(OQ-760). 「같은 고객 겹침」(`startDateTime NotAvailable`)은 KOS 가 거절한다(JS `ALREADY_RESERVED`)
- 드래그할 수 있는 카드 = `main ∈ {reserved, reception}`(MC§0 접수된 일정도 이동) — 기본값(OQ-714). 그 밖 카드는 끌리지 않는다. 「그룹 없음」 칸 카드도 다른 칸으로 끌 수 있다(KOS 이동 본문은 같다)

### 5.5 예약 등록 규칙 (D-16 ~ D-18)

- **기존 고객**: 내부 `reserve` 1번(§8). **신규 고객**: 신규 구분 검사 → 내부 `find-duplicated-visitor` → (없으면) `create-visitor` → `reserve` — 전부 **2026-10-26 데모 확인**(WP-KOS K2)
- **구역**(D-44 · KOS `reserve.zoneId` · `occupiedResources[].reservationGroup.zoneId` 칸 — D-04 「KOS 에 있으면 칸」): 그 그룹에서 켜진 구역 중 그 줄 자리가 있는 것. 기본 = `KOS_ZONE_ID`(켜져 있고 자리 있으면) · 아니면 구역 `order` 첫 번째. 켜진 구역이 하나면 칸을 보이지 않고 그 구역으로 보낸다 — 기본값(OQ-758)
- **신규 구분 규칙**(D-17) = 이름(앞뒤 공백 뺀 1자 이상) **+** (메인 연락처(국가번호 + 번호) · SNS(종류 + ID) · 이메일 · 여권번호 · 생년월일 중 하나 이상). **front 가 [예약 등록]을 끄고, back 도 같은 검사**(어기면 409 `not_identifiable` 「고객을 구분할 수 있는 정보가 부족합니다」 — KOS 문구) — 기본값(OQ-707 · C§3.3)
- ~~**이름 같은 고객 경고**(D-18) = 신규 고객 이름을 입력하면 front 가 내부 검색을 부르고, 이름이 같은 고객이 있으면 빨간 줄 「이름이 같은 기존 고객이 있어요 · 같은 사람이면 선택하세요」~~ (0.3.0 바뀜 — D-56 · 동명이인) → **경고 없음** — 문구 · 아래 고객 버튼 둘 다 그리지 않는다. 같은 고객인지는 아래 KOS 중복 확인만
- **등록 직전 KOS 중복 확인**(D-18): `find-duplicated-visitor` 가 고객을 돌려주면 **만들지 않고 409 `duplicated_visitor`**(본문 `error.candidate = {customerId, name, chartNumber, dateOfBirth}` — 그 고객을 사본에 넣고 ccc id 로) → front 는 「KOS 에 같은 고객이 있어요 · 이 고객으로 예약할까요?」 + [이 고객으로](기존 고객 길로 다시 보냄) — 기본값(OQ-708)
- **예약 담당자** = 모달 칸(활성 직원 목록) · **기본 = 시스템 계정**(`kos_token.account_kos_id` 의 staff · 이름) — 기본값(OQ-710 · C Q-60 · RT Q-75)
- ~~**당일 지정 의사** = 원장 목록 중 여럿 → `occupiedResources[].reservationGroup.doctors[]`~~ (0.3.0 바뀜 — D-53 · 칸 없음 · 보내지 않음) · **희망 상담사** = 상담사 목록(D-36) 중 하나 → `counselor` · **유입** = `funnel_code`(`closed = false`, `order` 순) 중 하나 + 상세 글자 → `funnel{funnel:<그 코드 행 전체>, funnelDetail}`(§8 · OQ-754 닫음) · ~~**수면마취** → `sedationRequired` · **상담 필요** → `consultationRequired`~~ (0.3.0 바뀜 — D-53 · 칸 없음 · 보내지 않음 — 상담 필요는 예약 상세 진행 경로 · D-51) · **귀가 희망 시각**(그날 시각) → `desiredDischargeDateTimeUtc` · **예약 메모** → `reservationMemo` — C§2.2
- **SNS 종류** = KOS `snsInfo.snsType` enum 그대로 `etc · kakaotalk · line · instagram · whatsapp · wechat`(R§3.1 13i) — 드롭다운 · 화면 글자 = 「기타 · 카카오톡 · 라인 · 인스타그램 · 왓츠앱 · 위챗」(기본값 · OQ-766) · 보내는 값 = enum(0.3.0 · 피드백 #23)
- `occupiedResources[].id` = **ccc 가 uuid4 를 만든다** — 기본값(OQ-711 · C Q-62)
- 신규 고객 Badge = 「신규 고객」(차트번호 없음) · 기존 = 「기존 고객 · No.{chartNumber}」 — 기본값(OQ-709)
- 고른 구역의 슬롯이 `full` 이면 409 `slot_full`(KOS 를 부르지 않는다)
- 신규 고객 동의 플래그는 보내지 않는다 — KOS 기본값으로 저장된다: 개인정보 · 광고 동의 = false · **정보성 알림 동의 = true**(보내지 않았는데 참 · WP-KOS K2-2 · OQ-753 닫음 — 사용자 알림거리)

### 5.6 [접수 완료] 묶음 (D-31 ~ D-33 · D-47 · D-48 · D-51 · D-54)

**두 갈래**(back `can.receive` · `receiveMode` — §7.3):

| 갈래 | 켜짐(사본 기준) | 신분 조건 | 방 |
|---|---|---|---|
| 새 접수 `new` | `main ∈ {reserved, noshow}` — 취소는 꺼짐 · **부도는 접수한다**(D-47 · KOS `recept` 가 부도 일정을 받아 `IN_PROGRESS` 로 바꾼다 — CS§2.1 ①) | ~~KOS 신분 칸이 다 채워짐(§5.12 · D-45)~~ (0.3.0 바뀜 — D-54) → **걸지 않는다** — 방만 고르면 켜진다. ccc 「확인 완료」도 보지 않는다 | 데스크가 [시술실 선택]에서 고른다(그 예약 구역의 빈 방 — §5.7) |
| 이어 하기 `resume` | `flow_step = RECEPTION` — **방 유무와 상관없이**(끝 단계에 못 간 묶음 · KOS 에서 접수만 한 예약 — D-48 · r1 F1) | **걸지 않는다** — KOS 가 이미 접수를 받았고, 여기서 막으면 ccc 에서 끝 단계로 갈 길이 없다 | 그 일정의 「방 배정」 작업(아래 「제목 판정」)에 **방이 이미 붙어 있으면 그 방으로 고정**(`rooms[]` 에서 그 방 `selected` · `roomLocked = true` · 다른 방은 못 고른다 · 5 건너뜀). 안 붙었으면 새 접수처럼 고른다 |

그 밖(`CANCELED` · 상담 대기 이후 단계) = 꺼짐. front 는 [시술실 선택](잠기지 않았을 때) → [접수 완료] 순서만 그린다 — 두 갈래의 버튼 모양은 같다.

**진행 경로 `route`**(0.3.0 · D-51): [접수 완료] 요청에 데스크가 고른 진행 경로를 싣는다 — `consultation`(상담 필요 · **기본**) \| `direct`(바로 시술). 초진 · 재진 모두 고를 수 있다. 이 값은 6단계 끝 단계로만 쓰고 KOS `consultationRequired` 에는 쓰지 않는다(읽지도 않는다). 생략 = `consultation`.

**순서**(RT§1 데모 확인 순서 그대로 — D-31 · WP-KOS K8 이 바로 시술 끝 단계까지 2026-10-26 데모 확인):

| # | 무엇 | KOS | 건너뛰기(다시 눌렀을 때) |
|---|---|---|---|
| 0 | 미리 확인 | 내부 `get-schedule-detail{scheduleId}` 로 **지금 KOS 단계 · 작업**을 읽고 갈래를 다시 정한다(사본은 10초 늦을 수 있다): `status = CANCELED` → 409 `not_receivable` · `flowStep = RESERVED` → 새 접수(~~내부 `get-visitor` 를 다시 읽어 §5.12 판정 — 안 채움이면 409 `identity_incomplete`~~ 0.3.0 바뀜 — D-54 · 신분 판정 없음) · `flowStep = RECEPTION` → 이어 하기 · **`flowStep` 이 끝 단계 이후(`CONSULTATION_WAITING` ~ `COMPLETED`)면 아무것도 보내지 않고 `{ok:true, flowStep}`**(반영 지연 · 두 번 누름). 「방 배정」 기타 작업 id = `KOS_ROOM_TASK_ID` 또는 `etc_task_def` 의 「방 배정」(없으면 409 `room_task_missing` — OQ-721). 방: 붙은 방이 있으면 요청 `roomId` 가 그 방이어야 한다(다르면 409 `room_locked`) · 없으면 고른 방이 그 예약 구역의 방이어야 하고(아니면 400) 「사용 중」(§5.7 — 오늘 사본 먼저 갱신 · §4.2)이면 409 `room_busy` | — |
| 1 | 접수 | 내부 `recept{scheduleId}` | KOS `flowStep ≠ RESERVED` 면 건너뜀 |
| 2 | 반영 기다림 | `get-schedule-detail` 를 **1초 간격 최대 5번** — `flowStep = RECEPTION` 이 보이면 다음 | 1 을 건너뛰면 없음 |
| 3 | 「방 배정」 작업 추가 | 내부 `add-flow-tasks`(§8) | 안 취소된 「방 배정」 작업이 이미 있으면 건너뜀(방 유무 무관 · 그 작업을 쓴다) |
| 4 | sequence 읽기 | (3 을 보냈으면) `get-schedule-detail` 1초 간격 최대 5번 — 새 「방 배정」 작업(**`room.id` 빈 값** · `CANCELED` 아님)이 보이면. 쓸 작업 = 안 취소된 「방 배정」 중 가장 큰 `sequence` | — |
| 5 | 방 지정 | 내부 `change-tasks-room{scheduleId, sequences:[그 sequence], roomId}` → `get-schedule-detail` 1초 간격 최대 5번 — 그 작업에 방이 보이면 다음(**약 1초 뒤 보인다** — K8 주의 4) | 그 작업에 이미 방이 있으면 건너뜀(0 에서 같은 방인지 확인함) |
| 6 | 끝 단계 | 내부 `change-flow-step{id, step}` — ~~`consultationRequired = true` → `CONSULTATION_WAITING` · `false` → `PROCEDURE_WAITING`~~ (0.3.0 바뀜) → **요청 `route = consultation` → `CONSULTATION_WAITING` · `direct` → `PROCEDURE_WAITING`**(D-32 · D-33 · D-51) | 이미 끝 단계 이후면 0 에서 끝남 |

- 각 단계 KOS 4xx · 5xx 면 **거기서 멈추고 되돌리지 않는다**(`cancel-reception` · `cancel-flow-tasks` 를 부르지 않는다 — D-48) → 409 `kos_rejected` 또는 502 `kos_unavailable` + `error.step`(위 번호의 이름: `recept` · `add_task` · `read_sequence` · `assign_room` · `flow_step`) · `event_log(reception)`(`steps` = 끝낸 단계) + `event_log(kos_rejected)`. 2 · 4 · 5 의 다섯 번 안에 안 보이면 409 `kos_slow` 「KOS 반영이 늦어요 · 잠시 뒤 다시 눌러 주세요」 — 기본값(RM Q-64 · Q-65 · RT Q-74)
- **다시 누르면 0 이 지금 KOS 상태를 읽고 남은 단계만 간다** — 1 이 끝났으면 이어 하기(`RECEPTION`), 5 까지 끝났으면 방 고정 + 6 만. 이 길로 E2E #23 두 갈래를 본다
- 성공 응답 `{ok:true, flowStep}` · 그 뒤 시술 현황 일정 조회 1회(§4.4) — 바로 시술이면 시술 현황 카드가 생긴다(SPEC-003 §5.1)
- **접수 → 「시술 대기」 + 방이 보이기까지 느림**(사용자 「오래 걸리는데 확인 필요」 · 피드백 #14 · 0.3.0): back 은 6단계 200 이면 **바로 응답**한다(6 뒤 다시 읽기를 기다리지 않는다) · front 는 성공 응답의 `flowStep` 과 고른 방으로 **즉시 낙관 표시** 뒤 다시 부른다(§6.7). 2 · 4 · 5 의 다시 읽기 횟수 · 간격은 **backend batch 1 단계별 측정 수치로 정한다** — 그 전엔 1초 × 최대 5번 그대로(OQ-764)
- **「제목 판정」 — 이 절의 「방 배정」 작업 = `type = ETCETERA` · `title = 「방 배정」` · `CANCELED` 아님**(묶음이 만든 · 쓸 작업을 찾는 데만). 수납 필요(§5.9)에서 빼는 「방 배정」은 **SPEC-003 판정**, 방 「사용 중」(§5.7)은 type · 제목 무관 「방 붙은 작업」 — 셋은 자리가 다르다(r1 W3)
- 이 「방 배정」 작업은 ccc 가 의사 호출에 쓴 적 없는 방 붙은 ETCETERA → 시술 현황에서 숨는 줄이다(SPEC-003 §5.1 판정 그대로 · `_RESUME` 10-25)

### 5.7 방 목록 · 「사용 중」 (D-34)

- 목록 = `room` 사본 중 **그 예약의 구역(`reservation.zone_kos_id`) 방 전부**(4층 = SPEC-003 사본 · 다른 구역 = §4.2 「다른 구역 방」), `order` → `title` 순 — 시안 A-룸1~10 으로 줄이지 않는다 · D-44
- **「사용 중」** = 오늘 **그 구역** 예약 사본(오늘 사본 먼저 갱신 — §4.2) 중 `flow_step ∈ {RECEPTION, CONSULTATION_WAITING, CONSULTATION, PROCEDURE_WAITING, PROCEDURE}` 이고 `main ∉ {canceled, noshow}` 인 일정의 **`CANCELED` 아닌 작업에 붙은 방**(`roomKosId` 가 null 아닌 것 · type 무관). 귀가 대기(`PROCEDURE_DONE`) · 귀가 · 예약 단계 일정의 방은 치지 않는다(귀가 대기 = 라운지 · DEC-005 D-33) — 기본값(OQ-720 · RT Q-77). 「사용 중」 방은 누를 수 없다(시안 `M:1826-1832`). 지금 연 예약 자신의 방은 「선택됨」(이어 하기 고정이면 그 방만 — §5.6)

### 5.8 상담 카드 · 상담사 지금 상태 (D-35 ~ D-37)

- ~~상담 카드는 접수 뒤 · `consultationRequired = true` 인 예약에만.~~ (0.3.0 바뀜 — D-51 · KOS 체크를 읽지 않는다) → **상담 카드는 접수 뒤 · 상담을 거치는 예약에만** = 지금 `flow_step ∈ {CONSULTATION_WAITING, CONSULTATION}` 이거나, ccc 이벤트에 `reception.route = consultation` · `consultation_add` 가 있는 예약(기본값 · OQ-767 — KOS 에서 접수한 예약도 상담 단계면 보인다). 상태 = `CONSULTATION_WAITING` → 「상담 대기」 · `CONSULTATION` → 「상담 진행 중 · HH:MM」(시각 = `flowStepUpdatedDateTimeUtc` — 기본값 OQ-724) · 그 뒤 단계(`PROCEDURE_*` · `PROCEDURE_DONE` · `COMPLETED`) → 「상담 완료」(다음 단계로 넘어감 = 완료 — D-35). 상담사 = `reservation.counselor`(없으면 노랑 카드 「상담사를 선택하세요」 — 시안)
- **상담사 목록** = `staff` 중 `role_tags` 에 `COUNSELOR` · `active`(D-36) · 시스템 계정 뺌
- **상담사 지금 상태**(D-37) = 오늘 예약 사본(**두 구역 전부** — 상담사는 사람 단위라 구역으로 나누지 않는다 · 오늘 사본 먼저 갱신 §4.2) 중 `flow_step = CONSULTATION` 이고 `counselor.id = 그 상담사 kos_id` 인 일정이 있으면 「{그 일정 카드 방} 상담 중」 · 없으면 「비어있음」. 여러 건이면 `flow_step_at` 가장 늦은 것
- **[실장 호출]** 켜짐 = `flow_step ∈ {CONSULTATION_WAITING, CONSULTATION}` + 상담사 하나 고름 — 기본값(OQ-725). 누르면 KOS `update-reservation{scheduleId, counselor}`(단독 수정 — `RESERVED` 에서 다른 칸 안 지움 2026-10-26 데모 확인 · K5. 접수 뒤 단계에서는 미시험 → E2E #25) → `event_log(counselor_call)`. 상담 카드에 「{이름} 실장 호출됨 · HH:MM」(마지막 `counselor_call` 이벤트 — ccc 만). **앱 알림은 이번 판 없음**(D-38)
- [상담 시작] · 상담 기록은 KOS 에서(D-35) — ccc 에 버튼 없음
- **[+ 상담 추가]**(0.3.0 · D-55 · 시안 `M:415-521`): 「내원 현황」 머리 오른쪽 버튼. 켜짐 = 접수 뒤 · `flow_step ∈ {CONSULTATION, PROCEDURE_WAITING, PROCEDURE, PROCEDURE_DONE}` · `main ∉ {canceled, noshow}`(이미 상담 대기 · 접수 묶음 중(`RECEPTION`) · 귀가 완료면 꺼짐) — 기본값(OQ-767). 누르면 KOS **공개 `changeFlowStep{scheduleId, step:"CONSULTATION_WAITING"}`**(뒤로 가는 단계 변경 · 공개 스펙상 받음 — **batch 1 backend 데모 1회 시험 결과로 확정**, 안 받으면 이 줄은 멈추고 사용자 질문) → `event_log(consultation_add)` · 상세 · 판 다시 부름. **상담 기록은 만들지 않는다**(KOS [상담 시작]이 만든다 — D-35). 그 뒤 상담 카드는 다시 「상담 대기」 · [상담사 선택] → [실장 호출] 길 그대로

### 5.9 수납 필요 · 금액 (D-39 · D-40)

- **「수납 필요 N건」** = 그 일정 `tasks[]` 중 `paymentRequired = true` 이고 `status ≠ CANCELED` 이며 **「방 배정」이 아닌**(SPEC-003 §5.1 판정 — 방 붙은 ETCETERA · ccc 호출 기록 없음) 작업 수 — 시술 현황 「수납 필요」와 같은 원천 · 같은 규칙(PP§5 · D-50 · 기본값 OQ-727)
- **SPEC-003 판정을 예약 사본에 잇는 키**(r1 W3): 작업 `t` 가 「방 배정」 = `t.type = ETCETERA` **이고** `t.roomKosId ≠ null` **이고** 호출 기록 없음. 호출 기록 = 시술 현황 사본에서 `visit.kos_id = reservation.kos_id` 인 visit 의 `procedure` 중 `kos_sequence = t.sequence` 인 행이 ccc 호출(`Rules._called`)에 들어 있음. **그 visit · procedure 행이 없으면 호출 0**(다른 구역 · 다른 날 · 아직 동기화 전). 코드는 `domain/rules.py` `is_room_task` 와 같은 식을 쓴다(새 기준을 만들지 않는다)
- **스케줄 표 카드 · 원내 현황 · 정산 상자 셋 다 이 값**(D-50) — 카드는 §6.3 Badge
- **금액**(기본값 — OQ-726): 「전체」 = `getPurchaseSummaries` `items[].priceV2.amount.value` 합 · 「결제」 = `transactions[]` 중 `status = APPROVED` 이고 `canceledRefId` 없는 것의 `price.value` 합 · 수납이 여럿이면 다 더함 · 통화 = 첫 수납 `currency`(KRW 는 「₩」 + 천 단위 쉼표 꼴). 수납 id 가 없으면 금액 = null(「-」). **「후납 금액」 칸은 만들지 않는다** — KOS 값이 없다(D-04 · PD§0) → 그 자리에 「수납 필요 N건」
- 원내 현황 카드 · 정산 상자 모두 같은 값

### 5.10 [귀가 완료] (D-40 · D-41)

- 켜짐 = `flow_step = PROCEDURE_DONE`(귀가 · 대기) **+ 수납 필요 0건**(D-41). 수납 필요가 남으면 꺼짐(~~+ 「수납 필요 N건이 남아 귀가 완료를 할 수 없어요」~~ 0.3.0 바뀜 — 사용자 「이거 문구 빼」 · 피드백 #16 → **이유 글자 없음** · 정산 상자 「수납 필요 N건」만) — back 도 409 `payment_required`
- KOS = 공개 `changeFlowStep{scheduleId, step:"COMPLETED"}` — **2026-10-26 데모 확인**(K9: `PROCEDURE_DONE` → `COMPLETED` 200 · `reservation.status` 도 `COMPLETED` · OQ-728 닫음). 남은 작업을 ccc 가 취소하지 않는다. **KOS 도 거절한다**: 수납 필요 + 시작 안 한 시술이 남은 일정에서 HTTP 400 `InvalidRequestException`(K9b — 이유가 수납 필요인지 안 끝난 시술인지는 못 가름) → 409 `kos_rejected` 토스트(§4.4 표 마지막 줄). ccc 는 수납 필요 ≥ 1 이면 보내지 않으므로 이 거절은 「수납 필요 0 · 안 끝난 시술 남음」에서만 난다
- 성공하면 카드 「귀가 · 완료」 · 시술 현황 카드가 사라진다(SPEC-003 §5.1 조건 2) — 시술 현황 일정 조회 1회(§4.4). **front 는 성공하면 상세 모달을 닫고 토스트 「{이름} 귀가 완료」**(0.3.0 · 피드백 #18)
- 수납 반영: KOS 에서 수납 확정 → `paymentRequired` 꺼짐은 **상세 모달이 열려 있는 동안 5초 폴링**으로 들어온다(D-52 · §6.7) — 닫았다 열지 않아도 [귀가 완료]가 켜진다

### 5.11 건강 정보 · 「확인 필요」 · 문진 이력 (D-24 · D-27)

- 질문 = 문진 양식 `pages[]` 중 제목 「건강 정보」 쪽의 `questions[]`(데모 7개 = 시안 7개와 같은 이름 — R§3.1 18행). 답 = 제출본(**최상위 객체** · §4.2) `answers[]` 중 `questionId` 가 그 질문인 것(`seq` 순)(여러 답이면 `answerTitle` 을 「 · 」로 · `memo` 가 있으면 뒤에 괄호)
- **「확인 필요」** = 답이 있고, 그 답 `answerTitle` 들(앞뒤 공백 뺌)이 **모두 「없음」 또는 「아니오」 인 것이 아닌** 질문(D-27). 답 없는 질문 = 「미입력」(확인 필요 아님). 빨강 글자 · 머리 Badge 「확인 필요 N」 — 기본값(OQ-731 — 다국어 답 글자는 미확인)
- 제출본 없음(400 + `errorProperties` `visitorId NotFound` — §4.2 · §4.4) = 「아직 입력되지 않았어요 · 고객이 문진을 작성하면 채워집니다」(시안 문구에서 「QR로」를 뺌 — 앱 판 전 · §6.8)
- **문진 방문별 이력**(D-24) = 상세 조회 때 제출본을 받으면, 그 고객의 `questionnaire_history` 마지막 `kos_submitted_at` 과 다르면 한 줄 쌓는다(`reservation_id` = 지금 연 예약). 이번 판은 **쌓기만** — 화면에 이력을 보이지 않는다 — 기본값(OQ-732)

### 5.12 신분 확인 — ccc 표시만 (D-25 · ~~D-45~~ D-54)

~~**① KOS 신분 칸 채움(접수 조건 — D-45)**~~ (0.3.0 바뀜 — D-54 · **접수 조건이 아니다**). 아래 칸 계산은 **화면 · 규칙에 쓰지 않는다** — 「신분 칸 n / N」 줄 · 「신분 칸을 채워 주세요」 꺼짐 이유를 그리지 않고, 409 `identity_incomplete` 도 없다. 빈 칸은 「고객 기본 정보」의 노랑 빈칸으로만 보인다. back 이 §7.3 `identity.fields` · `complete` 를 계속 실어도 되지만 front 는 쓰지 않는다(기록용 — 옛 판정): **빈 값 = 키가 없거나 앞뒤 공백 뺀 빈 문자열**(get-visitor 는 빈 칸 키를 안 준다 — K1).

| 고객 | 칸(모두 채워져야) | KOS 키 | 근거 |
|---|---|---|---|
| 외국인 — `nationality ≠ "KR"`(빈 값 포함) | 여권 영문명 · 생년월일 · 여권번호 | 영문명 = `passportSurname` · `passportGivenNames` **중 하나 이상** · `dateOfBirth` · `passportNumber` | D-45 · 시안 `ID_F` 외국인 `M:2178` · U§2 |
| 내국인 — `nationality = "KR"` | 생년월일 · 주민등록번호 | `dateOfBirth` · `registrationNumber` | D-45(「SPEC 이 정한 칸」) · 시안 `ID_F` 내국인 `M:2179`(생년월일 · 주민등록번호) |

- ~~영문명 「하나 이상」 · 국적 빈 값 = 외국인 · 칸 묶음 = 기본값(OQ-759)~~ · ~~상세 「신분 확인」 줄 = 칸마다 채움 · 빔 + 「신분 칸 n / N」 · [접수 완료] 옆 「신분 칸을 채워 주세요 · {빈 칸 이름}」~~ (0.3.0 바뀜 — D-54 · 피드백 #12 · OQ-759 닫음)

**② ccc 「확인 완료」 표시(표시만 — D-25 · D-45)**:

- 상태 = 그 고객 `identity_check` 마지막 줄(없으면 미확인). 상세 「신분 확인」 Badge(확인 완료 primary / 미확인 warning — 시안 `M:308`) · 「신분 확인」 제목 타이포 = 시안 `M:308` 그대로(§6.6 · 피드백 #11)
- **[확인 완료]**(미확인일 때) · **[미확인으로]**(확인 완료일 때 · 접수 전만) — 데스크가 여권 · 신분증을 눈으로 보고 누른다. 한 줄 추가(`method = web_manual` · `device = null`) + `event_log(identity)`. KOS 호출 없음. **[접수 완료] 켜짐에 쓰지 않는다**
- 확인 완료 글자 = 「확인 완료 · {actor 이름} · HH:MM」(날짜가 오늘이 아니면 「M/D」 붙임). 시안의 스캔 단계(기기 · QR · 대기 · 썸네일)는 그리지 않는다(앱 판 · §6.8)

### 5.13 이전 방문 · 고객 정보 · 특이사항 (D-22 · D-28)

- **이전 방문** = `getSchedulesByVisitor` 결과 중 **시작 시각의 KST 날짜가 그 예약의 날짜와 같은 일정을 뺀 것**, 최신 순. 결과 Badge = `reservation.status` `COMPLETED` 「방문 완료」(neutral) · `NO_SHOW` 「노쇼」(danger) · `CANCELED` 「취소」(neutral) · 그 밖은 KOS 값 그대로 회색(`IN_PROGRESS` 로 남은 지난 일정 등) — 기본값(OQ-738). 펼치면 「예약 HH:MM · {zone.title} / {그룹 제목}」 · 예약 메모 · 상담 메모(`consultation.consultationMemo`) · 시술 내역(`tasks[].title · status · doctors[].name`) — 시안 `M:393-413`
- **고객 기본 정보**: 상세 조회의 내부 `get-visitor` 값을 먼저 채워 보인다 → 데스크가 고침 → [저장] = back 이 **저장 직전 `get-visitor` 를 다시 읽어** 개인 정보 묶음 전체에 바꾼 칸만 덮어 `update-visitor-personal-information` 으로 보낸다(D-22 · U§2.2). 빈 칸으로 고치면 빈 문자열을 보낸다(KOS 웹앱과 같다 — U§2.2)
- **특이사항** = 상세의 `get-visitor.memo`(공개로는 일정 `visitor.memo` — 같은 값 · MT§3) · [저장] = back 이 저장 직전 `get-visitor` 를 다시 읽어 관리 묶음 그대로 + `memo` 만 바꿔 `update-visitor-management-information`(MT§4 · 기본값 OQ-740 「직전 다시 읽기」)
- 고객 정보 · 특이사항은 **접수 뒤에도 고칠 수 있다**(KOS 칸이다) — 단 시안처럼 접수 뒤 기본 정보 칸은 회색 읽기 전용 + [수정] 하나로 풀기(기본값 · `M:2067`)

### 5.14 버튼 켜짐 표 (back `can.*` · 상세 응답)

| 버튼 | 켜짐 | 409 코드(어기고 부르면) |
|---|---|---|
| [예약 취소](취소 · 부도) | `main = reserved` — 접수 전만(시안 · OQ-715). 부도 카드는 [예약 취소] 없음(이미 부도 · 되돌리기 없음 — D-20) · [접수 완료]만(D-47) | `not_cancelable` |
| 진행 경로 라디오 | ~~`main = reserved` + 재진 · 초진은 값만~~ (0.3.0 바뀜 — D-51) → **접수 전(`receiveMode = new` — `main ∈ {reserved, noshow}`)이면 초진 · 재진 모두 켜짐 · 기본 = 상담 필요**. 이어 하기(`resume`)도 끝 단계 전이라 켜짐. 바꿔도 **API 호출 없음**(front 상태 — [접수 완료] 요청 `route` 로만 간다) | (호출 없음 — ~~`route_locked`~~ 없앰) |
| [시술실 선택] · [접수 완료] | §5.6 두 갈래(`receive` · `receiveMode`) — 새 접수 = `main ∈ {reserved, noshow}`(~~+ KOS 신분 칸 다 채움~~ 0.3.0 바뀜 — D-54) · 이어 하기 = `flow_step = RECEPTION`(방 유무 무관). 둘 다 신분 조건 없음 — **방만 고르면 켜짐**. [시술실 선택]은 `roomLocked` 면 잠김 | `not_receivable` · ~~`identity_incomplete`~~ · `room_busy` · `room_locked` · `room_task_missing` · `kos_slow` |
| [실장 호출] | §5.8 | `not_consultation` · `not_counselor` |
| [+ 상담 추가] | §5.8(0.3.0 · D-55) | `not_consultation_addable` |
| [수납하기 ›] | `main = home` · 수납 필요 ≥ 1 · `KOS_WEB_BASE` 있음 | (호출 없음 — 딥링크) |
| [처방전 출력] | `main = home` · `prescriptionIds` ≥ 1 · `KOS_WEB_BASE` 있음 — 0 이면 「오늘 처방전 없음」 글자만(버튼 없음 · OQ-729) | (호출 없음) |
| [귀가 완료] | §5.10 | `not_home_waiting` · `payment_required` |
| 예약 메모 [저장] | `main ∉ {canceled, noshow}` 이고 `flow_step ≠ COMPLETED` | `reservation_closed` |
| 고객 정보 · 특이사항 [저장] · 신분 확인 표시 | 늘(신분 [미확인으로]만 접수 전) | `identity_locked` |
| 드래그 · 이동 | §5.4 | `not_movable` · `slot_full` |

## 6. 화면 (시안 기준)

화면 정본 = 시안 「현황 › 예약 현황」 `M:93-715`(DA§3). 시안과 다르게 가는 곳은 §6.8 표에만 있다 — 표에 없으면 시안대로(`_RESUME` 10-23 「시안이 정본」 · D-04 가 고친 곳 제외).

**입력 컨트롤 = 디자인 시스템 컴포넌트**(0.3.0 · 사용자 「셀렉터들이 우리 셀렉터가 아님」 「달력이 기본 캘린더인데 우리 메디킷에 달력 없나?」 · 피드백 #2 · #6 · #9): 예약 현황 화면 **전체**(등록 모달 · 상세 모달 · 오른쪽 패널 · 제목 줄)의 select · 날짜 · 시각 입력은 브라우저 기본 `<select>` · `<input type="date|time">` 를 쓰지 않고 **medikit · Ceramique DS 컴포넌트**(Select · DatePicker/Calendar · TimePicker)로 그린다. `procedure/front` 에 이미 있는 DS 컴포넌트를 먼저 쓰고, **없으면 만들지 않고 질문**(batch 1 frontend 몫 — 있는지는 그 보고로 확정 · OQ-762). 값 꼴(`yyyy-MM-dd` · `HH:MM` · KOS enum)은 그대로.

### 6.1 경로 · 헤더

| 경로 | 화면 |
|---|---|
| `/reservations/live` | **예약 현황**(새) — 헤더 「현황 › 예약 현황」 |
| `/reservations` | `/reservations/live` 로 보낸다 |
| `/procedures/live` | 시술 현황(그대로 · SPEC-003 §6.1) |

- 경로 이름은 시술 현황(`/procedures/live`)과 짝을 맞춘 기본값(OQ-752 · SPEC-003 OQ-524 의 예약 쪽)
- 헤더 「현황」 드롭다운 항목 = **「시술 현황」 → `/procedures/live` · 「예약 현황」 → `/reservations/live`** 순서 — **지금 항목 뒤에 하나 더하기만**(D-49 · U6). 「현황」 글자를 누르면 지금처럼 첫 항목(시술 현황 — `AppHeader.tsx` `items[0].href` 그대로). 지금 화면 항목은 `text-primary bg-primary-100`(SPEC-003 §6.2 그대로)
- 「현황」 부모 활성 = 경로가 **`/procedures/*` 또는 `/reservations/*`**(지금 `NAVS.base: '/procedures'` 하나 → 두 경로를 보게 · r1 W9). 시술 현황 쪽에서 바뀌는 것은 드롭다운 항목 하나 · 활성 판정 하나뿐(SPEC-003 §6.2 「바꾸지 않는다」의 예외 — D-49)
- 로그인 뒤 첫 화면 · `/` 는 지금 그대로 `/procedures/live`(SPEC-003 §6.1 — 바꾸지 않는다 · D-49). 역할별 첫 화면은 직무별 제한과 함께 마지막에

### 6.2 제목 줄 (`M:96-110`)

- 왼쪽: 「예약 현황」(title-md-600) · [‹] 날짜 [›](32×32) · 날짜 글자 「YYYY. M. D. (요일)」(최소 폭 140 · **누르면 DS 달력이 떠서 날짜를 고른다** — 0.3.0 · 피드백 #6) · [오늘](Button outlined sm · 오늘이면 꺼짐) · 「총 예약 N건」(§5.3)
- 오른쪽: 범례 Badge sm dot **7개** — 예약 · 접수 · 상담 · 시술 · 귀가 · 취소 · 부도(+ 수 · §5.3 · D-11)
- 그 아래(또는 날짜 옆) 동기화 글자: 「마지막 KOS 조회 HH:MM:SS」 · 실패면 「조회 실패」(caption red · title = 실패 이름) — 시술 현황 제목 줄과 같은 꼴(기본값 · 디자인 Q-7 · OQ-757)

### 6.3 스케줄 표 (`M:113-162`)

- 흰 판 · 반경 12 · 가로 · 세로 스크롤 · 칸 머리 sticky top · 시각 라벨(64px) sticky left — 시안
- 칸 · 축(06:00 ~ 22:00) · 회색 · 카드 위치 · 칸 폭 = §5.2. **지금 시각 줄**(오늘만) = 그 30분 라벨 `text-primary` + 가는 primary 가로선(시안의 「지난 시각 회색」 바탕은 쓰지 않는다 — 회색은 운영 밖 뜻 · D-12 · §6.8)
- **첫 렌더 때**(오늘) 지금 시각 줄이 보이게 자동 스크롤(위 64px 여유 — 시안 `M:1313-1323` · D-57). 사용자 「화면이 렌더링될 때 현재 시간으로 가야 함」 — 0.2.0 에도 있던 줄인데 3c3c6ad 에서 안 됨(피드백 #4 — 원인은 frontend batch 1). 다른 날짜로 옮기면 그날 칸 중 가장 이른 운영 시작 줄로(기본값 · OQ-757 ⑰). 10초 폴링 다시 그리기에서는 스크롤을 옮기지 않는다
- **카드**(폭 196 · 반경 6 · 왼쪽 막대 4px = 주 상태 색) — 1줄: 성별 아이콘(♂ `text-primary` / ♀ `text-red` / 미지정은 아이콘 없음 — OQ-735) · 이름(KOS `name` 그대로 · 한 줄 줄임 · D-13) · 방문 칩(초진 `bg-purple-100 text-purple` / 재진 `bg-ms-gray-100`) · 부상태 칩(§5.1) / 2줄: 국기(18×12 · `flag-icons` · title = **국가 이름**(front 고정 ISO 표 · 시안 `M:139` — r1 W5) · 모르는 코드면 코드) · 한글 발음(비면 빈칸) · **「수납 필요」 Badge**(아래). 카드 높이 = 2줄 콤팩트 · 그 칸 한 줄이 2줄보다 낮으면 한 줄 높이로 2줄을 숨긴다(§5.2 · 0.3.0). 취소 · 부도 = 불투명 0.5 + 이름 취소선(시안 · OQ-736)
- **「수납 필요」**(D-50 · U7) = `paymentRequiredCount ≥ 1` 이면 **medikit `Badge` `variant="warning"` `size="sm"` 「수납 필요」** — 시술 현황 카드(`components/procedures/OrderCard.tsx` · SPEC-003 §6.7 #7 · 시안 `M:825-827`)와 같은 꼴 · 같은 글자. 자리 = 2줄 오른쪽 끝(발음이 줄어든다) · 카드가 한 줄 높이면 1줄 끝(이름이 줄어든다). 원천 · 판정 = §5.9(시술 현황과 같은 규칙). 수는 적지 않는다(N건은 상세 · 원내 현황)
- 국기: ISO alpha-2 → `fi fi-{소문자 코드}` · 모르는 코드 · 빈 값 = 회색 상자 + 코드 글자(없으면 「-」) — 기본값(OQ-734)
- 카드 누르기 → 예약 상세 모달(§6.6) · 끌기 → §5.4
- 빈 칸 호버 [+](점선 상자 196 · ~~최소 높이 50~~ **높이 = 그 칸 한 줄 높이 그대로 — 줄 경계에 딱 맞고 다음 줄로 넘지 않는다**(0.3.0 · 사용자 「15분이 왜 시간 끝에 안 걸려」 · 피드백 #7 · 줄 높이 = 간격 × 1시간 높이 ÷ 60) · 끌어 놓기 미리보기도 같은 규칙 · 위 검은 툴팁 「{그룹} | HH:MM ~ HH:MM」) → 예약 등록 모달(그 날짜 · 그룹 · 시각) — 시안 `M:151-156` · `rows[].plusAllowed = false` 면 없음
- 예약 0건인 날 = 격자만(시안에 빈 상태 없음 · DA§9) · 불러오는 중 = 판 위 「불러오는 중…」 글자 한 줄 · 조회 실패 = §6.2 글자 + 마지막 사본(기본값 · 디자인 Q-8)

### 6.4 오른쪽 패널 (폭 340 · 넓은 화면만 · `M:164-243`)

- 탭 = 「예약 요청」(기본) · 「원내 현황」(medikit `Tabs` · 패치 Tabs-1 · Tabs-2)
- **「예약 요청」 탭**
  - 위: 「공지사항」 — **그 날짜 KOS 공지 목록**(D-15): 줄마다 ~~게시 시각 「HH:MM」(caption gray) +~~ 내용(pre-wrap) — **게시 시각 글자는 뺀다**(0.3.0 · 사용자 「이게 왜 있어 빼」 · 피드백 #19). **공지 영역 높이 = 패널 안 화면 높이에 비례한 고정 비율**(지금 420 상한보다 크게 · 공지가 없어도 자리 유지 · 넘치면 영역 안에서 스크롤 — 0.3.0 · 사용자 「항상 화면에서 고정 비율로」 「이거보다 크게 반응형으로」 · 피드백 #5 · #20). 비율 값 = frontend batch 1 구현값(기본값 · OQ-757 ⑱). 없으면 「이 날짜 공지가 없어요」. **[수정하기] 없음**(읽기만 — OQ-737)
  - 아래: 「예약 요청」 「대기 0건」 + 빈 상태 「들어온 예약 요청이 없어요」 — **자리만**(D-07 · 요청 카드 · [반려] · [승인] · 가안 카드 없음)
- **「원내 현황」 탭**(오늘만 · 다른 날짜면 「오늘만 볼 수 있어요」 — 기본값 · OQ-757 · §6.8 #26)
  - 원내 = 오늘 예약(**두 구역 전부**) 중 `flow_step ∈ {RECEPTION, CONSULTATION_WAITING, CONSULTATION, PROCEDURE_WAITING, PROCEDURE, PROCEDURE_DONE}` · `main ∉ {canceled, noshow}` — 기본값(귀가 완료 · 예약 단계 뺌 · OQ-757)
  - **구역별로 묶는다**(D-44): 구역 `order` 순 · 묶음 머리 「{구역} N명」(caption 600) · 원내 0 명인 구역은 묶음을 그리지 않는다. 필터 수는 두 구역 합 — 기본값(OQ-758)
  - 필터 칸 = **전체 · 접수 · 상담 · 시술 · 귀가 대기**(+ 수) — 시안 5개 이름(전체 · 귀가 대기 · 시술 중 · 상담 중 · 접수 완료)을 2계층 주 상태로 고침(D-11 · §6.8). 3칸 + 2칸 두 줄 · 같은 칸 다시 눌러도 안 풀림 · 탭 옮기면 「전체」로(시안)
  - 카드: 이름 · 한글 발음 · 국기 | Badge(수납 필요 ≥ 1 → danger 「수납 필요」 먼저 · 아니면 주 상태 · 부상태 글자) / 금액 3칸 = **전체 · 결제 · 수납 필요**(§5.9 · 후납 금액 대신 「N건」 · 0 이면 「-」 · ≥ 1 이면 빨강 + `bg-red-100`). 누르면 그 예약 상세 모달 + 스케줄 표에서 그 카드로 스크롤(시안 `M:1960`)
  - 정렬 = 구역 안에서 접수 시각 순(기본값 · OQ-757)

### 6.5 예약 등록 모달 (`M:572-652` · D-16 ~ D-18)

- 머리 「예약 등록 · M/D (요일) HH:MM ~ HH:MM · {그룹}」 · 바깥 누르면 닫힘 · 폭 `min(1200px, 92vw)`(시안 비율)
- **왼쪽 「고객 검색」** [↻ 초기화]: 입력 4개(이름 · 연락처 · 생년월일(DS 달력) · 차트번호) + [검색] → 결과 표(차트번호 · 이름 (발음) · 생년월일 · 국적) · 20건씩 페이지 · 줄 누르면 기존 고객으로 고름. **모달을 열면 조건 없이 첫 페이지 목록**을 보이고, **조건 없이 [검색]도 된다**(0.3.0 · 사용자 「고객 리스트 안뜸」 · 피드백 #1 — ~~검색 전 = 「고객을 검색하세요」~~ · ~~「검색 조건을 하나 이상」~~ 없앰). 결과 0 = 「일치하는 고객이 없어요 · 신규 고객으로 등록됩니다」
- **오른쪽 「예약 초안」** Badge(§5.5) · 칸(KOS 예약 칸 그대로 — D-16):

| 칸 | KOS | 필수 | 메모 |
|---|---|---|---|
| 예약일 · 시간 · 그룹 | `occupiedResources[0]` | ○(읽기 — [+] 에서 정해짐) | 끝 = 시작 + 그룹 간격(§5.5) |
| 구역 | `zoneId` · `occupiedResources[0].reservationGroup.zoneId` | ○ | 그 그룹 · 그 줄에 자리 있는 켜진 구역 select · 기본 `KOS_ZONE_ID` · 하나뿐이면 칸 숨김(§5.5 · D-44) |
| 이름 | (신규) `create-visitor.name` | ○ | 기존이면 읽기 |
| 한글 발음 | (신규) `phoneticName` | | 히라가나면 front 가 「가타카나로 입력해 주세요」(C§3.3) |
| 성별 | (신규) `gender` | | 남 · 여 · 선택 안 함(DS Select) |
| 생년월일 | (신규) `dateOfBirth` | 구분 정보 중 하나 | `yyyy-MM-dd` · DS 달력 |
| 국적 | (신규) `nationality` | | ISO alpha-2 목록(front 고정 표 — U Q-48 · 기본값) |
| 연락처(국가번호 + 번호) · 이메일 · SNS(종류 + ID) · 여권번호 | (신규) `phoneNumber` · `email` · `snsInfo` · `passportNumber` | 구분 정보 중 하나 | §5.5 신규 구분 규칙 · **SNS 종류 = DS 드롭다운**(KOS enum · 한글 글자 — §5.5 · 피드백 #23) |
| ~~상담 필요~~ | ~~`consultationRequired`~~ | | **뺌**(0.3.0 · D-53 · 피드백 #22 — 예약 상세 진행 경로에서 · D-51) |
| ~~수면마취~~ | ~~`sedationRequired`~~ | | **뺌**(0.3.0 · D-53 · 피드백 #22) |
| 예약 담당자 | `reservationAssignee` | | 기본 = 시스템 계정(§5.5) · DS Select |
| ~~당일 지정 의사~~ | ~~`reservationGroup.doctors[]`~~ | | **뺌**(0.3.0 · D-53 · 피드백 #21) |
| 희망 상담사 | `counselor` | | 하나 · DS Select |
| 유입 채널 · 상세 | `funnel` | | KOS 코드 select + 글자 |
| 귀가 희망 시각 | `desiredDischargeDateTimeUtc` | | HH:MM(그날) · DS 시각 입력 |
| 예약 메모 | `reservationMemo` | | 자리 글자 「날짜/지점/희망 시술/통역/특이사항」 |

- 통역 · 예산 · 희망 시술 칸 없음(D-16)
- 바닥 [취소] [예약 등록] — 꺼짐: 고객 안 고름 + 신규 구분 규칙 어김. 누르면 버튼 「등록 중…」 → 성공 = 모달 닫고 토스트 「{그룹} HH:MM 예약 등록」 + 스케줄 표 다시 부름 / 409 `duplicated_visitor` = §5.5 / 그 밖 실패 = 모달 안 빨간 줄(back `message`)
- ~~이름 같은 고객 경고(§5.5) = 신규 고객 이름 칸 아래 빨간 줄 · 그 줄의 고객을 누르면 기존 고객으로 고름~~ (0.3.0 바뀜 — D-56 · 피드백 #8) → **없음**. 같은 고객 안내는 [예약 등록] 뒤 409 `duplicated_visitor` → 「KOS 에 같은 고객이 있어요 · 이 고객으로 예약할까요?」 + [이 고객으로]만(§5.5)

### 6.6 예약 상세 모달 (`M:245-571` · DA§3.4)

- **제목류 타이포 = 시안 그대로**(「고객 기본 정보」 · 「신분 확인」 · 「유입 채널」 · 「예약 메모」 · 「건강 정보」 · 「주의사항」 · 「이전 방문」 · 「내원 현황」 — 시안 해당 줄과 하나씩 대조 · 0.3.0 · 사용자 「시안이랑 글자 크기 다른 거 같은데」 · 피드백 #11). 성별 · SNS 종류 등 입력 = DS 컴포넌트(§6 머리)
- 바깥 오버레이 `rgba(0,0,0,.32)` · 창 `min(1440px, 92vw) × 88vh` · 머리 = 주 상태 색 + 제목(예약 「접수 전」 · 접수 「접수 완료」 · 상담 「상담 대기/진행」 · 시술 「시술 대기/진행」 · 귀가 「귀가 대기/완료」 · 취소 「예약 취소」 · 부도 「예약 부도」) + [×]
- **왼쪽 칸**
  - 고객 머리: 성별 · 이름(title-md-600) · 발음 · 초진/재진 Badge / 「국기 {국가 이름} · {남성/여성} · 만 N세 · No.{차트}」(시안 「{국가}」 · 생년월일 없으면 나이 뺌 — OQ-735) · 머리 오른쪽 caption 「{구역} / {그룹}」
  - 「고객 기본 정보」 3칸 격자(시안 칸 순서): 이름 · 한글 발음 · 성별 · 생년월일 · 주민등록번호/여권번호(국적 `KR` 이면 주민 · 아니면 여권 — 기본값) · 국적 · 휴대폰(국가번호 + 번호) · 이메일 · SNS 종류 · SNS 아이디 · 주소(국적 `KR` 이면 「주소」 · 아니면 「주소 (자국)」 — KOS 칸 하나) + **여권 영문 성 · 이름 칸**(KOS `passportSurname` · `passportGivenNames` — 시안에 없음 · OQ-741). 빈칸 = `bg-yellow-100 border-yellow-500` · 채움 = 흰색(시안 `M:2067`). [저장](바뀐 칸이 있을 때만 켜짐) · 상세 조회 실패면 칸 대신 「KOS 에서 고객 정보를 읽지 못했어요」 + [다시]
  - 「고객 기본 정보」 제목 옆 **「n / N 입력」**(시안대로 — 위 칸 중 채운 수 / 칸 수 · front 계산 · r1 W5) · [QR로 고객 입력 요청]만 없음(앱 판 · §6.8 #10)
  - 「신분 확인」(§5.12) — ~~① KOS 신분 칸 줄(칸마다 채움/빔 · 「신분 칸 n / N」)~~(0.3.0 바뀜 — D-54) · ccc Badge + [확인 완료]/[미확인으로](표시만)
  - 「유입 채널」 = KOS 값 글자(코드 이름 · 상세) — **읽기만**(이번 판 · 등록 때 넣는다 · §6.8)
  - 「예약 메모」 textarea + [저장](§5.14)
- **오른쪽 칸**
  - 「건강 정보」 + Badge 「확인 필요 N」(§5.11) · 7줄 「{질문} · {답}」(확인 필요 = `text-red`)
  - 「주의사항」 = KOS **특이사항** textarea(높이 110 · 자리 글자 「고객 공통 메모 (모든 방문에 표시)」) + [저장](§5.13)
  - 접수 전: 「이전 방문 N건」 아코디언(§5.13) · 없으면 「이전 방문 내역이 없습니다 (초진)」
  - 접수 뒤: 「내원 현황」 — 머리 오른쪽 **[+ 상담 추가]**(§5.8 · D-55 · 시안 `M:415-521` · 꺼지면 숨기지 않고 꺼짐)
    1. 「접수 완료 · HH:MM · {방} 배정 · 데스크 {이름}」(접수 시각 = `reception_at` · 방 = 카드 방 · 데스크 = 마지막 `reception` 이벤트의 actor 계정 이름 · ccc 가 안 했으면 「데스크 {…}」 뺌 — OQ-722)
    2. 상담 카드(§5.8 · 상담을 거치는 예약만 — OQ-767) — [상담사 선택/변경] 팝오버 「상담사 호출」: 상담사 줄마다 이름 · 「비어있음」/「{방} 상담 중」 → 고르면 바닥 [{이름} 실장 호출]
    3. 단계 카드 2개 — 「시술」(시술 대기 · 시술 진행 · 완료 = 귀가 단계로 넘어감) · 「귀가」(귀가 대기 · 귀가 완료). 지금 단계 `border-primary bg-primary-100`(시안 `bkStages`) — 2계층 이름(D-11)
    4. 「귀가 대기」 단계(`main = home`)의 **정산 상자**: 금액 3칸 「전체 금액 · 결제 금액 · 수납 필요」(§5.9) · [수납하기 ›](§5.14 — 새 탭으로 KOS 수납 딥링크) · 「처방전」 줄(`prescriptionIds` N 이면 「처방전 N건」 + [처방전 출력](새 탭 KOS 일정 상세 `tab=etceteraWork`) · 0 이면 「오늘 처방전 없음」) · **여정 리포트 줄 없음**(D-42) · [귀가 완료](§5.10 · ~~꺼지면 이유 글자~~ 꺼지면 이유 글자 없음 — 0.3.0 · 피드백 #16 · 성공하면 모달 닫기 + 토스트 — 피드백 #18)
- **바닥 줄**: [예약 취소](빨간 외곽선 · 접수 전만 → 작은 팝오버 「예약 취소 / 예약 부도」 두 버튼 + [닫기] · 고르면 바로 KOS — 기본값 · OQ-757) · 진행 경로 라디오 「상담 필요 · 바로 시술」(§5.14 — **접수 때 고르는 값 · 초진 · 재진 모두 · 기본 상담 필요 · 바꿔도 호출 없음** · D-51 · 피드백 #13) · [시술실 선택 / 시술실 · {방}](고르기 전 빨간 테두리 · 위로 열리는 팝오버 「시술실 배정 · {그 예약 구역} · 빈 방 N개」 + 방 목록 §5.7 · **`roomLocked` 면 「시술실 · {방}」 고정 · 팝오버 안 열림 · title 「이미 배정된 방이에요」**) · [접수 완료/접수됨/취소됨](§5.6 — 이어 하기도 같은 버튼 · 고른 진행 경로를 요청 `route` 로 · 꺼지면 이유 글자: ~~신분 칸 ·~~ 방 — 0.3.0 · D-54 · 성공 직후 응답 `flowStep` · 고른 방으로 즉시 낙관 표시 — §5.6 · 피드백 #14) · [닫기](접수 뒤)
- 조작 중 그 버튼 「…중」 · 끝나면 상세 다시 부름 + 스케줄 표 다시 부름(§6.7)

### 6.7 갱신 · 토스트

- 스케줄 표 = 열려 있는 동안 **10초마다** `GET board?date=` · 조작 성공 직후 1번 + 2초 뒤 1번(반영 지연 · §4.3) — 기본값(OQ-704 · SSE 를 쓰지 않는다)
- 상세 모달 = 열 때 · 조작 뒤 · 그리고 ~~스케줄 표 폴링에서 그 예약의 `state` · `flow_step` 이 바뀌었을 때 다시 부른다(10초마다 상세를 부르지 않는다 — KOS 호출 수)~~ (0.3.0 바뀜 — D-52) → **열려 있는 동안 5초마다** `GET /api/reservations/{id}`(수납 반영 — 사용자 「수납했는데 반영 안 되는데」 · 피드백 #17). 닫으면 멈춘다 · 조작 중(버튼 「…중」)에는 건너뛴다 · 입력 중인 칸(고객 기본 정보 · 메모 · 특이사항)의 값은 폴링이 덮지 않는다(기본값 · OQ-757 ⑲). KOS 소켓은 따로 검토(D-52 · OQ-744)
- 토스트 = 가운데 아래 · 2.6초 · 이 화면 안에(시안은 시술 현황 안에만 — 디자인 Q-9) · 성공 문구(기본값 · OQ-757): 「예약 등록」 · 「{이름} 예약 이동」 · 「예약 취소」/「예약 부도」 · 「접수 완료 · {방}」 · 「{이름} 실장 호출」 · 「{이름} 상담 추가」(0.3.0) · 「{이름} 귀가 완료」(0.3.0 — 모달 닫힘과 같이) · 「저장했어요」. 실패 = back `message`
- 좁은 화면(760 미만) = 오른쪽 패널 없음 · 스케줄 표만(시안 `narrow`)

### 6.8 시안과 다르게 가는 곳

| # | 시안 | 이 계약 | 근거 |
|---|---|---|---|
| 1 | 칸 = 권역 5개(국내 · 중화권 · 영미권 · 일본 · 기타) | KOS 예약 그룹 **전부**(order 순) | D-10 |
| 2 | 줄 08:00 ~ 20:00 · 30분 고정 · 지난 시각 회색 | ~~그룹 운영 시간~~ **06:00 ~ 22:00 고정**(0.3.0 · D-57) · 칸마다 자기 간격 · 1시간 높이 같음 · **운영 밖 회색**(지난 시각 회색 없음 · 지금 줄 primary 선) · 칸 머리 「{정원}명 / {간격}분」(한 꼴 — §5.2) | D-12 · D-57 |
| 3 | 범례 7(예약 · 접수 · 상담 중 · 시술 중 · 귀가 대기 · 귀가 · 취소) | 범례 7 = 주 상태(예약 · 접수 · 상담 · 시술 · 귀가 · 취소 · **부도**) · 부상태 = 카드 칩 | D-11 |
| 4 | 카드 이름 「SURNAME, GIVEN」 | KOS `name` 그대로 + 발음 | D-13 |
| 5 | 공지 Textarea 하나 + [수정하기/저장] | 그 날짜 KOS 공지 **목록 · 읽기만** | D-15 · OQ-737 |
| 6 | 예약 요청 카드 · 가안 카드 · 승인/반려 모달 | 빈 목록 자리만 | D-07 |
| 7 | 원내 현황 필터(전체 · 귀가 대기 · 시술 중 · 상담 중 · 접수 완료) · 금액 「후납」 | 필터 = 전체 · 접수 · 상담 · 시술 · 귀가 대기 · 금액 3칸 = 전체 · 결제 · **수납 필요 N건** | D-11 · D-04 · §5.9 |
| 8 | 등록 모달 칸 12개(통역 · 원장 상담 · 희망 시술/예산 포함) | KOS 예약 칸 그대로(§6.5 표) — 통역 · 예산 · 희망 시술 없음 · 예약 담당자 · 희망 상담사 · 귀가 희망 시각 더함 · ~~수면마취 · 당일 지정 의사 더함 · 「원장 상담」 → 「상담 필요」~~(0.3.0 바뀜 — 셋 다 뺌 · D-53) · **「원장 상담」 칸 없음** | D-16 · D-53 |
| 9 | 유입 채널 고정 6개 select(상세에서 고침) | KOS `FUNNEL` 코드 · 상세에서는 **읽기만** | D-16 · 기본값 |
| 10 | 고객 입력 QR 상자 · 태블릿 · 메신저 | 없음(앱 판). 「n / N 입력」은 시안대로 둔다(0.2.0 · r1 W5) | D-01 · D-29 |
| 11 | 신분 확인 = 기기 스캔 4단계 + 신분 칸(`ID_F`) | 스캔 없음 · ~~KOS 신분 칸 채움 줄(§5.12 ①)~~(0.3.0 바뀜 — D-54) · **웹 수동 [확인 완료] / [미확인으로](표시만)** | D-01 · D-25 · D-54 |
| 12 | [접수 완료] 켜짐 = 예약 + 방 + 신분 필드 모두 입력(`M:1840`) | 예약 **또는 부도** + 방 — ~~+ KOS 신분 칸 다 채움~~(0.3.0 바뀜 — **신분 조건 없음** · D-54). 더해 **이어 하기**(`RECEPTION` · 붙은 방 고정) | ~~D-45~~ · D-47 · D-48 · D-54 |
| 13 | 시술실 팝오버 「A구역 · A-룸1~10」 · 사용 중 하드코딩 | 그 예약 구역의 KOS 방 전부 · 사용 중 = §5.7 계산(구역별) | D-34 · D-44 |
| 14 | 상담사 팝오버 실장 4명 · 상태 하드코딩 | 직원 사본 `COUNSELOR` · 상태 = §5.8 계산 · [실장 호출] = KOS 상담사 지정(앱 알림 없음) | D-35 ~ D-38 |
| 15 | [+ 상담 추가] | ~~없음~~ (0.3.0 바뀜) → **있음**(§5.8 — KOS 공개 `changeFlowStep(CONSULTATION_WAITING)` · 상담 기록은 안 만듦) | D-55 · OQ-750 |
| 16 | 정산 상자 「후납 금액」 · 「오늘 여정 리포트 · [QR 전송]」 · 처방전 「항생제 · 연고 1건」 | 「수납 필요 N건」 · 여정 리포트 없음 · 처방전 = 「처방전 N건」(약 이름 없음) + KOS 딥링크 | D-41 · D-42 · OQ-729 |
| 17 | [예약 취소] = 바로 「취소」 | 「예약 취소 / 예약 부도」 고르기 | D-20 |
| 18 | 다른 날짜 상태 일괄 바꿈(데모 · `M:1684`) | KOS 값 그대로 | D-03 |
| 19 | 건강 빈 상태 「고객이 QR로 작성하면 채워집니다」 | 「고객이 문진을 작성하면 채워집니다」 | D-01(앱 판 전) |
| 20 | 부상태 표시 없음 | 카드 칩 · 상세 머리 제목 | D-11 |
| 21 | 동기화 표시 없음(예약 현황) | 「마지막 KOS 조회 · 조회 실패」 글자 | 기본값 · 디자인 Q-7 |
| 22 | 상세 기본 정보에 여권 영문 성 · 이름 없음 | 칸 둘 더함(KOS 칸) | D-04 · OQ-741 |
| 23 | 부도 상태 없음 · 카드 칩 없음 | 부도 = 빨강 외곽선 색(§5.1) | D-11 · OQ-757 |
| 24 | 칸 = 권역 고정 · 축 고정 | 「그룹 없음」 칸(사본에 없는 그룹) · 운영 밖 예약이면 축을 늘림(§5.2) | OQ-757 |
| 25 | 모든 날 같은 축 | 그룹이 모두 쉬는 요일 = 축 없음 + 「운영하지 않는 날이에요」(§5.2) | TA Q-124 · OQ-757 |
| 26 | 원내 현황 = 날짜와 무관(데모 데이터) | 오늘만 · 다른 날짜 「오늘만 볼 수 있어요」 · **구역별 묶음**(§6.4) | D-44 · OQ-757 · OQ-758 |
| 27 | 예약 카드에 수납 표시 없음(`M:130-149`) | **「수납 필요」 Badge warning sm**(시술 현황 카드와 같은 꼴 · §6.3) | D-50 |
| 28 | 국기 title · 상세 머리 = 국가 이름 | 같음(국가 이름) — 0.1.0 의 「국가 코드」를 시안대로 되돌림 | r1 W5 |
| 29 | 등록 모달에 구역 칸 없음 | 구역 select(켜진 구역이 둘 이상일 때만 · §6.5) | D-44 · D-04 |
| 30 | 등록 모달 이름 칸 아래 「이름이 같은 기존 고객이 있어요」 + 고객 버튼(`M:572-652`) | **없음**(0.3.0 · 동명이인) — KOS 중복 확인만 | D-56 |
| 31 | 진행 경로 = 재진만 고름(`M:1866`) | 초진 · 재진 모두 · 기본 상담 필요 · 접수 때 고르는 값(KOS 체크 아님) | D-51 |
| 32 | 공지 높이 420 고정 · 공지 시각 없음(`M:170-176`) | 패널 높이 비례 고정 비율(420 보다 크게) · 시각 없음(시안과 같음) | 피드백 #5 · #19 · #20 |

## 7. back ↔ front API

### 7.1 공통

- SPEC-003 §7 공통 그대로: JSON · 오류 `{error:{code, message}}`(+ 필요할 때 `step` · `candidate`) · `Authorization: Bearer <ccc 토큰>`(없거나 틀리면 401)
- 역할 = admin · doctor · nurse · **coordinator** 모두 ○(§3.4 · D-30). 검사 순서 = 401 → 403 `fake_board`(조작만) → 400 `invalid_request` → 404 `not_found` → 409 → 502
- `PROC_FAKE_BOARD` 가 켜지면 GET 넷(§7.2 ~ §7.4)은 `service/fake_reservations.py` 의 **지어낸 값**(이름 「고객 A」 꼴 · KOS id 없음 · 금액은 작은 가짜 숫자)을 돌려주고 조작은 403 `fake_board` — front 가 back 을 기다리지 않고 그리기 위한 것(SPEC-003 §2.3 와 같은 규칙)
- 시각 = ISO(KST 오프셋 `+09:00`) · 날짜 = `YYYY-MM-DD` · id = ccc 정수 id(KOS id 는 응답에 없다 — 딥링크 URL 안에만)

### 7.2 스케줄 표 — `GET /api/reservations/board?date=YYYY-MM-DD`

`date` 생략 = 오늘(KST). 형식 오류 = 400.

```text
{
  date, isToday, now,
  sync: { lastOkAt, lastError },                       // 그 날짜 조회(§4.2)
  axis: { start: "HH:MM", end: "HH:MM" },              // §5.2 — 0.3.0: 늘 06:00 ~ 22:00(축 밖 예약이면 늘림) · null 안 씀
  closedDay,                                            // 0.3.0 — 그룹이 모두 쉬는 요일이면 true(「운영하지 않는 날이에요」)
  zones: [{ zoneId, title, order, isDefault }],           // D-44 — 구역 사본(present)
  columns: [{ groupId, title, order, intervalMinutes, count,          // groupId null = 「그룹 없음」 칸(§5.2)
              capacities: [{ zoneId, capacity }],                    // 켜진 구역만 · 머리 글자는 §5.2
              open: [{ start: "HH:MM", end: "HH:MM" }] }],   // 운영 구간(쉬는 시간 뺀 조각)
  cards: [{ reservationId, resourceIndex, groupId, zoneId, start, end,
            customer: { customerId, name, phoneticName, gender, nationality, isNew },
            state: { main, sub }, paymentRequiredCount, draggable }],
  slots: [{ groupId, zoneId, start, end, capacity, count, full }],   // 구역별(§5.4)
  rows: [{ groupId, start, plusAllowed }],             // [+] 줄 — 켜진 구역 중 하나라도 자리 있음(§5.4)
  counts: { total, reserved, reception, consultation, procedure, home, canceled, noshow },
  notices: [{ id, content, releasedAt }],
  requests: [],                                        // D-07 자리만 — 늘 빈 배열
  clinic: { counts: { all, reception, consultation, procedure, home },   // 두 구역 합
            items: [{ reservationId, zoneId, customer: { name, phoneticName, nationality },
                      state: { main, sub }, receptionAt, paymentRequiredCount,
                      amount: { total, paid, currency } | null }] } | null   // 오늘만(§6.4)
}
```

- `cards[]` 순서 = 칸 order → 시작 → `reservationId` · `slots[]` = 칸 × 켜진 구역마다 그 날 운영 줄 전부(슬롯 사본이 없으면 `capacity = null` · `full = false`) · `rows[]` = 칸마다 운영 줄 전부(「그룹 없음」 칸 없음) · `clinic.items[]` 순서 = 구역 order → 접수 시각(front 가 `zoneId` 로 묶는다 · §6.4)
- `count`(칸) · `counts.total` = §5.3 · `main` · `sub` = §5.1 문자열

### 7.3 예약 상세 — `GET /api/reservations/{reservationId}`

```text
{
  reservationId, day, start, end, groupTitle, zoneId, zoneTitle,
  state: { main, sub },
  customer: {
    customerId, name, phoneticName, gender, nationality, isNew, chartNumber, age,      // age = 만 나이 | null
    personal: { name, phoneticName, gender, dateOfBirth, registrationNumber, passportNumber,
                passportSurname, passportGivenNames, passportExpiryDate, foreignRegistrationNumber,
                nationality, language, phone: { countryCode, number } | null, additionalPhone,
                email, sns: { type, accountId } | null,
                address: { address, detailed, zipCode } | null } | null,             // get-visitor 실패 = null
    personalError,                                                                    // null | "KOS 오류 이름"
    remark,                                                                           // 특이사항(visitor.memo)
    identity: { status: "confirmed"|"unconfirmed", checkedAt, checkedBy, method,     // ccc 표시(§5.12)
                kind?, fields?, complete? } },                    // 0.3.0: 접수 조건 아님(D-54) — 실어도 되나 front 가 쓰지 않는다
  reservation: { sedationRequired, memo,                  // 0.3.0: consultationRequired 뺌(D-51) · sedationRequired 는 KOS 값 읽기만으로 남음(구현 확정)
                 funnel: { name, detail } | null, connectedChannel,
                 counselor: { staffId, name } | null, assignee: { name } | null,
                 doctors: [{ name }], desiredDischargeAt },   // doctors = KOS 값 읽기만(등록 칸은 없음 — D-53)
  health: { state: "none"|"ok"|"error", submittedAt, needCount,
            items: [{ title, answer, memo, needsCheck, empty }] },
  previousVisits: [{ date, start, result: "completed"|"noshow"|"canceled"|"other", resultRaw,
                     zoneTitle, groupTitle, reservationMemo, consultationMemo,
                     procedures: [{ title, status, doctors: [string] }] }],
  flow: { receptionAt, roomTitle, receptionBy,
          consultation: { state: "none"|"waiting"|"doing"|"done", counselor: { staffId, name } | null,   // 0.3.0: 있음/없음 = ccc 접수 기록(route) · 지금 단계로 판정(§5.8)
                          since, calledAt, calledBy } | null,
          stages: { procedure: "none"|"waiting"|"doing"|"done", home: "none"|"waiting"|"done" } } | null,   // 접수 뒤만
  settlement: { paymentRequiredCount, amount: { total, paid, currency } | null,
                prescriptionCount, links: { purchase, prescription } | null } | null,   // main = home 만
  rooms: [{ roomId, title, busy, selected }],             // 그 예약 구역 방 · receiveMode 있을 때만(아니면 [])
  roomLocked,                                             // 이어 하기 + 방 붙음 = true(그 방만 selected)
  receiveMode: "new"|"resume"|null,                       // §5.6 두 갈래 · null = 접수 묶음 아님
  counselors: [{ staffId, name, busyRoom }],              // 상담 카드가 있을 때만(아니면 [])
  defaultRoute: "consultation",                           // 0.3.0 — 진행 경로 라디오 기본(D-51)
  can: { cancel, editRoute, receive, callCounselor, addConsultation, discharge, editMemo, editPersonal, editRemark,
         confirmIdentity, unconfirmIdentity }                 // editRoute = 접수 전(새 접수 · 이어 하기) · 초진 · 재진 모두
}
```

- `links.purchase` = `{KOS_WEB_BASE}/{tenantId}/reservation/schedule/?visitorId={…}&scheduleId={…}&tab=purchase` · `links.prescription` = 같은 꼴 `&tab=etceteraWork`(`historyMenu` 안 붙임 — OQ-729). `KOS_WEB_BASE` 가 비면 `links = null` — PD§2 · RXD§0
- 상세 조회 중 KOS 읽기 하나가 실패해도 응답은 온다(그 칸 null · `health.state = "error"` 등) — 기본값(OQ-757). ~~`get-visitor` 가 실패하면 신분 칸을 모르므로 새 접수 `can.receive = false`~~ (0.3.0 바뀜 — D-54 · 신분 조건이 없으므로 `get-visitor` 실패는 접수를 막지 않는다 · 그 칸만 null)
- `can.receive` = §5.6 갈래 조건(~~새 접수는 `identity.complete` 포함~~ 0.3.0 — 신분 조건 없음) — 방 고름은 front 몫이라 `can.receive` 에 넣지 않는다. 상세 조회 때 오늘 사본 갱신(§4.2)을 먼저 한다(`rooms[].busy` · `counselors[].busyRoom`)

### 7.4 등록 모달 · 고객 검색

| 메서드 · 경로 | 요청 | 응답 | 오류 |
|---|---|---|---|
| `GET /api/reservations/form` | `?date=&groupId=&start=`(그 줄의 구역 자리 · 없으면 구역 목록만) | `{ staff:[{staffId,name}], defaultAssigneeStaffId, ~~doctors~~, counselors:[{staffId,name}], funnels:[{funnelId,name}], zones:[{zoneId, title, available}], defaultZoneId, snsTypes: string[6] }` — 0.3.0: `doctors` 뺌(D-53) · `snsTypes` 더함(KOS enum 값 6개 그대로 · 한글 글자는 front 가 붙인다 — §5.5 · 구현 확정 2026-10-27) | 400 형식 |
| `GET /api/customers/search` | `?name=&phone=&birth=YYYY-MM-DD&chart=&page=1` — ~~넷 중 하나 이상~~ **조건 없어도 된다**(0.3.0 · 피드백 #1 — 빈 조건 = 내부 `get-visitors` 빈 조건 첫 페이지 · OQ-761) | `{ items:[{customerId, chartNumber, name, phoneticName, dateOfBirth, nationality, isNew}], total, page, pageSize:20 }` — 결과 고객은 `customer` 사본에 upsert(ccc id) | ~~400 조건 없음~~ · 400 형식 · 502 |

- `staff` = 활성 직원(시스템 계정 포함 · 「마취용」 등 `KOS_EXCLUDE_ACCOUNT_IDS` 뺌) · `defaultAssigneeStaffId` = 시스템 계정(§5.5)

### 7.5 조작

| 메서드 · 경로 | 요청 | 성공 | 409 코드(도메인) | 근거 |
|---|---|---|---|---|
| `POST /api/reservations` | `{ groupId, zoneId?, start, customer: {customerId} \| {new: {name, phoneticName?, gender?, dateOfBirth?, nationality?, phone?:{countryCode, number}, email?, sns?:{type, accountId}, passportNumber?}}, assigneeStaffId?, counselorStaffId?, funnelId?, funnelDetail?, memo?, desiredDischargeTime?:"HH:MM" }` — 0.3.0: ~~`consultationRequired` · `sedationRequired` · `doctorStaffIds`~~ 뺌(D-53 · **보내면 422** — 구현 확정 2026-10-27) · `sns.type` ∈ KOS enum 6(아니면 400) | `{reservationId, customerId}` | `not_identifiable` · `duplicated_visitor`(+`candidate`) · `slot_full` · `kos_rejected` | §5.5 · D-16 ~ D-18 · D-44(`zoneId` 생략 = §5.5 기본 구역) · D-53 |
| `POST /api/reservations/{id}/move` | `{ resourceIndex, groupId, start }` | `{ok:true}` | `not_movable` · `slot_full` · `kos_rejected` | §5.4 · D-19 · D-20 |
| `POST /api/reservations/{id}/cancel` | `{ reason: "CANCELED" \| "NO_SHOW" }` | `{ok:true}` | `not_cancelable` · `kos_rejected` | D-20 |
| `PUT /api/reservations/{id}/memo` | `{ memo }`(문자열 · 빈 문자열 = 비움) | `{ok:true}` | `reservation_closed` · `kos_rejected` | §5.14 |
| ~~`PUT /api/reservations/{id}/route`~~ | ~~`{ consultationRequired: bool }`~~ | — | — | **없앰**(0.3.0 · D-51 — 진행 경로는 KOS 쓰기가 없다 · [접수 완료] `route` 로) |
| `POST /api/reservations/{id}/reception` | `{ roomId, route? }`(이어 하기 + 방 고정이면 그 방 · `route` = `consultation`(기본 · 생략) \| `direct` — 0.3.0 · D-51) | `{ok:true, flowStep}` | `not_receivable` · ~~`identity_incomplete`~~(0.3.0 없앰 — D-54) · `room_busy` · `room_locked` · `room_task_missing` · `kos_slow` · `kos_rejected`(+`step`) | §5.6 · D-47 · D-48 · D-51 · D-54 |
| `POST /api/reservations/{id}/counselor-call` | `{ staffId }` | `{ok:true}` | `not_consultation` · `not_counselor` · `kos_rejected` | §5.8 |
| `POST /api/reservations/{id}/consultation-add` | — (본문 없음) | `{ok:true}` | `not_consultation_addable` · `kos_rejected` | §5.8 · D-55(0.3.0 · 경로 이름 = 구현 확정 2026-10-27 · KOS 동작은 backend 데모 1회 시험 중 · OQ-767) |
| `POST /api/reservations/{id}/discharge` | — | `{ok:true}` | `not_home_waiting` · `payment_required` · `kos_rejected` | §5.10 |
| `PUT /api/customers/{customerId}/personal` | `{ personal: {…§7.3 personal 와 같은 키 · 보낸 키만 바꿈} }` | `{ok:true}` | `kos_rejected` | §5.13 · D-22 |
| `PUT /api/customers/{customerId}/remark` | `{ memo }` | `{ok:true}` | `kos_rejected` | §5.13 · D-28 |
| `PUT /api/customers/{customerId}/identity` | `{ status: "confirmed" \| "unconfirmed" }` | `{ok:true}` | `identity_locked` | §5.12 · D-25 |

- 0.3.0: `POST /api/reservations` 에 뺀 칸(`consultationRequired` · `sedationRequired` · `doctorStaffIds`)을 보내면 **422**(구현 확정 2026-10-27 · 요청 모델 검증)
- 400 `invalid_request` = 모르는 필드 · 형식(시각 · 날짜 · 정수) · 빈 필수 · 그 그룹에서 꺼진 구역 · 그 예약 구역 밖 방. 없는 id = 404. 502 `kos_unavailable` = 모든 KOS 조작 공통(§4.4)
- 409 메시지(기본값 · 한국어 한 줄): `not_identifiable` 「고객을 구분할 수 있는 정보가 부족합니다」 · `duplicated_visitor` 「KOS 에 같은 고객이 있어요」 · `slot_full` 「그 시간은 정원이 찼어요」 · `not_movable` 「옮길 수 없는 예약이에요」 · `not_cancelable` 「접수 전 예약만 취소할 수 있어요」 · `reservation_closed` 「끝난 예약이에요」 · ~~`route_locked`~~ · `not_receivable` 「접수할 수 없는 예약이에요」 · ~~`identity_incomplete`~~(0.3.0 없앰) · `not_consultation_addable` 「지금은 상담을 추가할 수 없어요」(0.3.0) · `room_locked` 「이미 배정된 방이 있어요 · {방}」 · `room_busy` 「사용 중인 방이에요」 · `room_task_missing` · `kos_slow`(§5.6) · `not_consultation` 「상담 단계가 아니에요」 · `not_counselor` 「상담사가 아니에요」 · `not_home_waiting` 「귀가 대기가 아니에요」 · `payment_required` 「수납 필요가 남아 있어요」 · `identity_locked` 「접수 뒤에는 미확인으로 바꿀 수 없어요」
- 조작마다 `event_log` 1줄(`actor` = 로그인 아이디 · §3.2)
- `move` 의 `start` 는 그 칸 간격 경계여야 한다(아니면 400). 길이는 back 이 원래 묶음 길이로 계산(§5.4)

### 7.6 경로 수

지금 back 경로 19개 = **HTTP 18(router 17 + `GET /api/health`) + 통역 WS 1**(코드 `tests/test_order.py` `test_route_count_19` · `len(http) + len(ws) == 19`). 여기에 **이 문서 HTTP 15개**(§7.2 1 · §7.3 1 · §7.4 2 · §7.5 11 — 0.3.0: `PUT …/route` 하나 빼고 `POST …/consultation-add` 하나 더해 11 그대로)를 더해 **34개 = HTTP 33(router 32 + health) + WS 1**. 시험 이름 · 값을 `test_route_count_34` · `== 34` 로 바꾼다(r1 W6 · SPEC-003 §7.4 의 「router 18 + health」 내역은 그쪽 기존 부채 — 이 문서가 고치지 않는다)

## 8. KOS 반영 표

내부 = `{KOS_INTERNAL_API_BASE}/tenants/{tenantId}/…` · `Authorization: Bearer` / 공개 = `{KOS_OPEN_API_BASE}/…` · `Authorization: <token>`. 경로 · 본문은 HAR 에서 본 그대로(내부는 공식 계약이 아니다 — DEC-005 OQ-503). 0.1.0 의 「미확인」 줄은 WORK-007 WP-KOS 가 데모 지점에 1회씩 보내 **모두 받았다** — 「확인」 칸 **(2026-10-26 데모 확인)** = `reservation-kos-probe-report.md` K 번호(「안 받음」 0). 남은 실물 확인은 딥링크 2 · 접수 뒤 단계의 [실장 호출] · 정원 초과 동시 조작뿐(E2E).

| ccc 조작 | 순서 | 종류 · 경로 | 본문(모양) | 확인 | 근거 |
|---|---|---|---|---|---|
| [예약 등록] 기존 고객 | 1 | 내부 `schedule/reservation/v2/commands/reserve` | `{visitorId, zoneId: <고른 구역>, occupiedResources:[{id: <uuid4>, type:"RESERVATION_GROUP", reservationTime:{startDateTimeUtc, endDateTimeUtc}, reservationGroup:{reservationGroupId, zoneId}}](0.3.0 — `doctors` 보내지 않음 · D-53), reservationAssignee:{id,name}, ~~consultationRequired, sedationRequired~~(0.3.0 — 보내지 않음 · KOS 기본값 · D-53), counselor?:{id,name}, reservationMemo?, desiredDischargeDateTimeUtc?, funnel?:{funnel:<funnel_code 행 전체 {id, category:"FUNNEL", name, order, closed, default}>, funnelDetail:"<글 · 없으면 빈 문자열>"}}` → `{scheduleId}` · `funnelCategory` 는 보내지 않는다(데모 분류 0건) | **7칸 모두 (2026-10-26 데모 확인)**(K2-3 — 일정 상세에 보낸 그대로 · 지정 의사는 `occupiedResources…doctors` 에만 보이고 `reservation.doctor` 는 빈 값) · `funnel` 모양 확정(KOS 웹 JS 계약 + 실호출 — OQ-754 닫음) | C§2.1 · §2.2 · RT§2.1 · WP-KOS K2 · §0 `funnel` |
| [예약 등록] 신규 고객 | 1 | 내부 `visitor/v1/queries/find-duplicated-visitor` | `{name, phone?:{countryCode, phoneNumber}, passportNumber?, birthDateUtc?(KST 0시의 UTC ISO), snsInfo?, email?}` — 빈 값은 넣지 않는다 → 일치 `data{고객}` / 없음 `{}` | (2026-10-26 데모 확인)(이름 + 생년월일 · K2-1) | U§4 · C§1.8 · WP-KOS K2 |
| 〃 | 2 | 내부 `v1/visitor/commands/create-visitor` | `{name, phoneticName?, gender?, dateOfBirth?("yyyy-MM-dd 00:00:00.000Z"), nationality?, phoneNumber?, email?, snsInfo?, passportNumber?}` → `{data:{id}}` · 동의 플래그는 보내지 않는다 | (2026-10-26 데모 확인)(K2-2 · 동의 없이 200 · KOS 기본값 = 정보성 알림 동의 true · OQ-753 닫음) | C§3 · WP-KOS K2 |
| 〃 | 3 | `reserve`(위와 같음) | `visitorId` = 2 의 id | 〃 | C§1.11 |
| 드래그 이동 · [이동] | 1 | 내부 `schedule/reservation/v2/commands/update-reservation` | `{scheduleId, occupiedResources:{items:[사본의 묶음 전부 — 옮긴 묶음만 reservationTime · reservationGroup.reservationGroupId 바꿈 · id · zoneId · doctors 는 그대로]}}` | (2026-10-26 데모 확인)(K3 — `doctors` 를 실어 보낸 모양 · 바뀐 칸은 시각 · 그룹뿐 · 묶음 id · 지정 의사 · 메모 · 유입 · 상담사 · 수면 · 상담 필요 · 귀가 희망 · 담당자 남음). KOS HAR 두 건은 `doctors` 없이 보냈다(MC§1.1 #7) — **ccc 는 K3 모양(실어 보냄)으로 간다**. 길 = 내부(묶음 id 유지 · KOS [이동] 과 같은 길 — `_RESUME 10-26 #60`) — 기본값 OQ-714 | MC§1.1 #7 · §2.1 · WP-KOS K3 |
| [예약 취소] 취소 · 부도 | 1 | 공개 `schedule/open/v1/commands/cancel-reservation` | `{scheduleId, reason:"CANCELED"\|"NO_SHOW"}` | 데모 확인(C1 · N1) | MC§3 · KDA 150행 |
| (취소 되돌리기) | — | **이번엔 없음 — `event_log(resv_cancel)` 만**. 다음 판 = 내부 `schedule/reservation/v1/commands/revoke-canceled-reservation{scheduleId}`(데모 확인) | — | — | D-20 · MC§4 |
| 예약 메모 [저장] | 1 | 공개 `schedule/open/v1/commands/change-reservation-memo` | `{scheduleId, memo}`(통째로) | (2026-10-26 데모 확인)(K6 · 다른 칸 그대로) | KDA 62행 · Q§5 M18 · WP-KOS K6 |
| ~~진행 경로~~ | — | ~~내부 `update-reservation{scheduleId, consultationRequired}`~~ | — | **0.3.0 없앰 — KOS 호출 없음**(진행 경로는 ccc 값 · [접수 완료] 끝 단계로만 · D-51). K4 확인 결과는 남긴다 | D-51 |
| 고객 정보 [저장] | 1 | 내부 `visitor/v2/queries/get-visitor` | `{id}` | 조회 확인 | U§3 |
| 〃 | 2 | 내부 `visitor/v2/commands/update-visitor-personal-information` | `{id, name, phoneticName, phoneNumber, additionalPhoneNumber, email, dateOfBirth("yyyy-MM-dd 00:00:00.000Z"), gender, registrationNumber, foreignRegistrationNumber, passportNumber, passportSurname, passportGivenNames, passportExpiryDate("yyyy-MM-dd"), address{address, detailedAddress, zipCode}, nationality, language, snsInfo}` — 1 에서 읽은 묶음 전체 + 바꾼 칸. **1 에 키가 없던 칸은 보내지 않는다**(빈 문자열로 채우지 않음 · 데스크가 그 칸에 값을 넣었을 때만 보냄) | (2026-10-26 데모 확인)(K7 · 날짜 꼴 두 가지 받음 · 같은 꼴로 다시 읽힘 · 시스템 계정 권한 · 고치지 않은 칸 남음 · OQ-739 닫음) | U§2 · WP-KOS K7 |
| 특이사항 [저장] | 1 · 2 | 내부 `get-visitor` → `visitor/v2/commands/update-visitor-management-information` | `{id, memo, visitorFunnel, (visitor\|account\|unregistered), visitorType, visitorCategories, doctor, counselor, aggrementPersonalInformation, aggrementAdvertisements, agreementInformationalNotification, customAttributes?}` — 읽은 그대로 + `memo` 만 바꿈 · 빈 배열은 뺀다 | 데모 확인(MT§2) | MT§2 · §4 |
| 신분 확인 | — | 없음 — ccc DB | — | — | D-25 |
| [접수 완료] | 0 | 내부 `schedule/v1/queries/get-schedule-detail`(~~+ 새 접수면 `get-visitor` — 신분 칸~~ 0.3.0 — 신분 판정 없음 · D-54) | `{scheduleId}` | (2026-10-26 데모 확인)(K1 · K8) | RT§3 · WP-KOS K8 |
| 〃 | 1 | 내부 `schedule/v1/commands/recept` | `{scheduleId}` | 데모 확인(A1 · K8 · 부도 일정도 받음 — CS§2.1 ①) | RT§1 · RM§2.1 · D-47 |
| 〃 | 2 | 내부 `schedule/v1/commands/add-flow-tasks` | `{scheduleId, tasks:[{type:"ETCETERA", title:"방 배정", etceteraConfiguration:{etceteraTaskId, name:"방 배정", translsMap:{name:{}}}, translsMap:{title:{}}}]}` → 새 작업 `room:{id:""…}` | 데모 확인(A2 · K8) | RT§1 · RM§2.2 · WP-KOS 주의 3 |
| 〃 | 3 | 내부 `schedule/flow/v1/commands/change-tasks-room` | `{scheduleId, sequences:[「방 배정」 sequence], roomId}` | 데모 확인(A3 · K8 · `RECEPTION` 에서 받음 · **약 1초 뒤 보임**) | RT§1 · RM§2.4 · WP-KOS 주의 4 |
| 〃 | 4 | 내부 `schedule/v1/commands/change-flow-step` | `{id: scheduleId, step:"CONSULTATION_WAITING"}` — 요청 `route = consultation`(0.3.0 · D-51) | 데모 확인(A4) | RT§1 |
| ↳ 바로 시술 | 4 | 〃 | `{id, step:"PROCEDURE_WAITING"}` — 요청 `route = direct` | (2026-10-26 데모 확인)(K8 · 묶음 네 단계 모두 200 · OQ-756 닫음) | RM§2.3 · RM Q-67 · WP-KOS K8 |
| [실장 호출] | 1 | 내부 `update-reservation` | `{scheduleId, counselor:{id, name}}` + ccc 로그(앱 푸시 없음) | (2026-10-26 데모 확인)(K5 · `RESERVED` 에서 그 칸만 바뀜 · OQ-755 닫음). **접수 뒤 단계(상담 대기 · 진행)는 미시험 — E2E #25** | CS§2.3 · §6 · WP-KOS K5 |
| [+ 상담 추가](0.3.0 · D-55) | 1 | 공개 `schedule/open/v1/commands/change-flow-step` | `{scheduleId, step:"CONSULTATION_WAITING"}` + ccc `event_log(consultation_add)` · 상담 기록 없음 | **미확인 — batch 1 backend 데모 1회 시험**(받으면 이 줄 확정 · 안 받으면 멈추고 질문 · 다른 값이 바뀌는지 기록) | CS§2 · Q-95 · `reservation-e2e-batch1-brief.md` §3 |
| [수납하기 ›] | — | 호출 없음 — 딥링크 `…&tab=purchase` | — | 로그인 · 탭 미확인(OQ-730) | PD§2 |
| [처방전 출력] | — | 호출 없음 — 딥링크 `…&tab=etceteraWork` | — | 실물 미확인(데모 처방전 0건 · OQ-729) | RXD§0 · §1 |
| [귀가 완료] | 1 | 공개 `schedule/open/v1/commands/change-flow-step` | `{scheduleId, step:"COMPLETED"}` — 수납 필요 ≥ 1 이면 보내지 않는다 | (2026-10-26 데모 확인)(K9 200 · K9b 수납 필요 + 안 끝난 시술 = **400 `InvalidRequestException`** · OQ-728 닫음) | PD§5 · D-40 · D-41 · WP-KOS K9 |
| 상담 시작 · 상담 기록 · 수납 · 시술 추가 · 오더 메모 · 시술 대기 전환 | — | **ccc 없음** — 상담사가 KOS 웹에서 · ccc 는 사본만 | — | — | D-05 · CS§0 · PD§3 |
| 시술 구간 | — | SPEC-003 §8 그대로 | — | — | — |

- 「본문(모양)」의 `?` = 값이 있을 때만 넣는다
- 시각 → KOS: UTC `…Z`(밀리초 `.000Z` 꼴 — HAR 과 같게 · 지금 `kos_utc` · K2 받음). 생년월일만 `yyyy-MM-dd 00:00:00.000Z`(U§2.1 JS · K7) · 여권 만료일 `yyyy-MM-dd`. **KOS → ccc 는 밀리초가 없을 수 있다**(§3.3 — 파싱해 비교)
- 쓰기 뒤 반영 지연 0 ~ 3초 — §4.3 · §5.6

## 9. 검증 기준 — 로컬 E2E (데모 지점)

준비: `procedure/.env` 에 SPEC-003 §9 env + §2.3 새 env(`CCC_COORD_*` · `KOS_WEB_BASE`) → `docker compose up --build` → `http://localhost:3700` 에 **코디 계정**으로 로그인. 데모 KOS 웹 화면 또는 공개 `getScheduleDetail`(조회)로 KOS 쪽을 본다. **데모 지점만 · 쓰기 허가 범위**(D-06). 시험이 남긴 예약 · 상태는 끝에 목록으로 남겨 사용자에게 알린다(OQ-751). **WP-KOS 가 남긴 데모 데이터**(시험 고객 1 · 일정 2 — 귀가 완료 1 · **귀가 대기 + 수납 필요 1**, `reservation-kos-probe-report.md` §5)를 #28 · #34 에 쓴다.

| # | 단계 | ccc 에서 보는 것 | KOS 쪽 확인 | 근거 |
|---|---|---|---|---|
| 1 | 코디 로그인 · 헤더 | 코디 계정(아이디 + 비밀번호)으로 들어감 · 첫 화면 = **시술 현황** · 헤더 「현황」 호버 = 「시술 현황」 · 「예약 현황」 두 항목 · 「현황」 글자 = 시술 현황 · 「예약 현황」 → `/reservations/live` 에서도 「현황」 활성 · 시술 현황 화면 · 동작 그대로 · **코디로 의국 [수락](원장 고름) = 됨 · 원장 안 고르면 400** | — | §3.4 · §6.1 · D-49 · r1 F2 |
| 2 | 날짜 이동 | [‹] [›] 하루씩 · [오늘] = 오늘이면 꺼짐 · 날짜 글자 · 다른 날짜의 예약이 KOS 와 같다 | KOS 「예약 현황」 그 날짜와 카드 수 · 위치 같음(**두 구역 일정 전부** — 다른 구역 예약이 있는 날 포함 · #35) | §6.2 · D-10 · D-44 |
| 3 | 칸 · 시간축 | 칸 = KOS 예약 그룹 전부(order 순 · 데모 13) · 칸 머리 「{그룹} · N건 · {정원}명 / {간격}분」(**모든 칸이 같은 꼴** — 구역 하나 = 「4층 3명 / 30분」 · 둘 = 「4층 3 · 미사용 3명 / 15분」 — 데모 「제모」 · 0.3.0) · **축 = 06:00 ~ 22:00**(0.3.0) · 라벨 30분 · 60분 칸 줄 = 30분 칸 두 줄 높이 · 15분 칸 = 반 줄 · **운영 밖 회색 = 칸마다 06:00 ~ 10:00 · 20:00 ~ 22:00**(데모 운영 10–20) · 오늘이면 첫 화면이 지금 시각 줄로 스크롤돼 있음 · 칸 폭 = 겹침 수만큼 카드가 나란히(같은 시각 3건 = 3장 · `13 + mx·196 + (mx−1)·6`) | 그룹 설정과 같음 | §5.2 · D-12 · D-57 |
| 4 | 카드 | 성별 아이콘 · KOS 이름 그대로(국가 접두 포함 · 잘리지 않음) · 발음 · 초진/재진 · 국기 그림(코드 → 그림) · 주 상태 색 막대 · 부상태 칩 · 위치 = 그 그룹 칸 · 그 시각 · **높이 = 2줄 콤팩트**(30 · 60분 예약도 두껍지 않음 · 15분 칸은 줄 경계 안 — 0.3.0) | KOS 고객 · 예약 값과 같음 | §5.2 · §6.3 · D-11 · D-13 |
| 5 | 범례 · 총 건수 | 범례 7(예약 · 접수 · 상담 · 시술 · 귀가 · 취소 · 부도) + 수 · 「총 예약 N건」 = 취소 · 부도 뺀 수 · 칸 머리 N 도 같음 | — | §5.3 · D-14 |
| 6 | 공지 | 오른쪽 「예약 요청」 탭 위에 그 날짜 KOS 공지(있으면) · 날짜를 옮기면 같이 바뀜 · 수정 버튼 없음 · 아래 예약 요청 「대기 0건」 빈 상태 | KOS 공지 목록과 같음(데모 공지가 없으면 KOS 웹에서 하나 쓰고 확인 — 사용자) | §6.4 · D-15 · D-07 |
| 7 | 칸 [+] → 신규 고객 예약 | 빈 줄 호버 [+] · 툴팁 「{그룹} \| HH:MM ~ HH:MM」 (15분 칸 [+] 상자가 그 줄 경계 안 — 0.3.0) → 등록 모달 머리 날짜 · 시각 · 그룹(구역이 하나인 그룹 = 구역 칸 없음 · 「제모」 = 구역 select 기본 4층). **칸에 당일 지정 의사 · 상담 필요 · 수면마취 없음**(0.3.0) · 모든 select · 날짜 · 시각 = DS 컴포넌트. 이름만 넣으면 [예약 등록] 꺼짐 → 생년월일(DS 달력)을 넣으면 켜짐 → 담당자(기본 시스템 계정) · 희망 상담사 · 유입(KOS 코드) · SNS(종류 = 드롭다운) · 메모 · 귀가 희망 시각 넣고 등록 → 토스트 · 10초 안에 카드(초진) | 새 고객 생김(차트번호 KOS 가 붙임) · 일정 `RESERVED` · 넣은 칸이 KOS 예약 상세에 보임(상담사 · 유입 · 메모 · 귀가 희망 · SNS 종류) · 지정 의사 · 수면 · 상담 필요는 KOS 기본값 | §5.5 · §6.5 · D-16 · D-17 · D-53 |
| 8 | 기존 고객 예약 · 검색 | **모달을 열면 조건 없이 고객 목록 첫 페이지** · 조건 없이 [검색]도 목록(0.3.0) → 이름 하나로 검색 → 결과 표(차트 · 이름 (발음) · 생년월일 · 국적) · 20건 페이지 → 골라 등록 → 카드(재진이면 재진) | 그 고객에 일정 하나 더 | §6.5 · §7.4 · OQ-706 · OQ-761 |
| 9 | ~~이름 같은 고객 경고~~ · KOS 중복 | 신규 고객 이름을 기존 고객 이름과 같게 → **경고 · 고객 버튼 없음**(0.3.0 · D-56). 같은 이름 + **다른** 생년월일로 등록 → 새 고객으로 들어감(동명이인). 같은 이름 + 같은 생년월일로 등록 → 「KOS 에 같은 고객이 있어요」 + [이 고객으로] → 기존 고객으로 등록 | 동명이인 = 새 고객 생김 · 같은 고객 = 새 고객이 **생기지 않음** | §5.5 · D-18 · D-56 |
| 10 | 정원 꽉 찬 칸 | 한 칸 줄을 4층 정원(데모 3)만큼 채운 뒤 → 그 줄에 [+] 없음(켜진 구역이 4층 하나) · 다른 4층 카드를 끌어 그 줄에 놓으면 금지 표시 · 아무 일 없음 | 변화 없음 | §5.4 · D-20 · D-44 |
| 11 | 드래그 이동 | 카드를 다른 그룹 · 다른 시각으로 끌어 놓기 → 바로 새 자리 · 길이 그대로 · 토스트 · 새로고침해도 그 자리 | 일정 그룹 · 시각 바뀜 · 메모 · 유입 · 담당 · 상담사 · **지정 의사 그대로** | §5.4 · §8 · D-19 |
| 12 | 드래그 거절 | **(필수)** 같은 고객의 다른 예약과 겹치는 시각으로 끌어 놓기 → **원위치 + 토스트 「같은 고객의 예약이 그 시간에 있어요」** / **(관찰)** 두 브라우저에서 같은 줄 마지막 자리로 거의 같이 놓기 → KOS 가 늦은 쪽을 거절하면 원위치 + 토스트, **받으면 정원을 넘긴 채 둘 다 들어간다** — 어느 쪽인지 기록(OQ-760) | 필수: 변화 없음 · 관찰: 그 줄 `reservationCount` 와 정원 | §4.4 · §5.4 · D-20 · r1 W2 |
| 13 | 예약 상세 — 기본 정보 | 카드 → 상세 · KOS 고객 값이 먼저 채워짐(빈칸 노랑) · 여권 영문 성 · 여권번호 · 국적을 고쳐 [저장] → 토스트 · 다시 열어도 그 값 | KOS 고객 상세에 고친 값 · **고치지 않은 칸(연락처 · 주소 · 유입 등) 그대로** | §5.13 · D-22 |
| 14 | 신분 확인 | ~~① 신분 칸 줄~~(0.3.0 없음 — D-54) · ccc 「미확인」 Badge → [확인 완료] → 「확인 완료 · {이름} · HH:MM」 · [미확인으로](접수 전) — **바꿔도 [접수 완료] 켜짐은 그대로**(표시만) · 「신분 확인」 제목 글자 크기 = 시안 | 변화 없음(ccc 만) | §5.12 · D-25 · D-54 |
| 15 | 유입 · 예약 메모 | 유입 = 등록 때 고른 KOS 코드 글자(읽기) · 예약 메모 고쳐 [저장] | KOS 예약 메모 바뀜 | §6.6 · §8 |
| 16 | 건강 정보 | 문진 제출본이 있는 고객 = 7줄 + 「확인 필요 N」(「없음 / 아니오」 아닌 답 빨강) · 없는 고객 = 「아직 입력되지 않았어요」 | KOS 문진 답과 같음(데모에 제출본 있는 고객 1명 — Q§4.1) | §5.11 · D-27 |
| 17 | 특이사항 | KOS 특이사항이 보임 → 고쳐 [저장] | KOS 웹 「특이사항」에 보임 · 유입 · 분류 등 다른 관리 칸 그대로 | §5.13 · D-28 |
| 18 | 이전 방문 | 지난 일정 N건(오늘 것 없음) · 결과 Badge · 펼치면 예약 시각 · 메모 · 상담 메모 · 시술 | `getSchedulesByVisitor` 와 같음 | §5.13 · D-28 |
| 19 | 진행 경로 | **초진 · 재진 모두** 접수 전 라디오 「상담 필요 / 바로 시술」 켜짐 · **기본 = 상담 필요**(KOS 「상담 필요」 체크가 꺼진 예약도) · 바꿔도 토스트 · 호출 없음 → [접수 완료] 끝 단계가 고른 값대로(#21 · #22) | **KOS `consultationRequired` 그대로**(안 바뀜 — 0.3.0 · D-51) | §5.6 · §5.14 · D-51 |
| 20 | 시술실 선택 | [시술실 선택] 팝오버 = **그 예약 구역의** KOS 방 전부 · 같은 구역 다른 고객이 쓰는 방 「사용 중」(누를 수 없음) · 빈 방 수 · 다른 날짜를 보다가 오늘 예약을 열어도 「사용 중」이 맞음 | KOS 방 목록과 같음 | §5.7 · D-34 · D-44 · r1 W7 |
| 21 | [접수 완료] — 상담 필요 | **신분 칸(여권 · 주민등록번호 등)이 빈 고객도 방만 고르면 [접수 완료] 켜짐**(꺼짐 이유 글자 없음 · ccc 「확인 완료」 안 눌러도 — 0.3.0 · D-54) · 진행 경로 = 상담 필요(기본) → 방 고름 → 누름 → **곧바로**(낙관 표시) 머리 「상담 대기」 · 「내원 현황」 첫 줄 「접수 완료 · HH:MM · {방} 배정 · 데스크 {코디}」 · 상담 카드 노랑 | 일정 `CONSULTATION_WAITING` · 예약 상태 `IN_PROGRESS` · 접수 시각 · 「방 배정」 작업 `READY` + 그 방. **KOS 웹 고객 상세 · 시술 진행판이 KOS 우회 결과와 같아 보이나**(RT Q-78) | §5.6 · D-31 · D-33 · D-51 · D-54 |
| 22 | [접수 완료] — 바로 시술 | **초진 예약에서** 진행 경로 「바로 시술」을 골라 접수 → 상세 「시술 대기」 + 방이 **곧바로**(낙관 표시) · **시술 현황 화면에 그 고객 카드가 10초 안에 생김**(「방 배정」 줄은 안 보임) · 누름 → 「시술 대기」 + 방 보일 때까지 걸린 시간을 적는다(OQ-764 · backend 측정과 대조) | 일정 `PROCEDURE_WAITING` + 방 · `consultationRequired` 그대로 | §5.6 · D-51 · OQ-756 · OQ-764 · SPEC-003 §5.1 |
| 23 | [접수 완료] 이어 하기 — **두 갈래 필수** | **(a) 접수만**: KOS 웹에서 접수만 해 둔 예약(`RECEPTION` · 작업 없음) → ccc 상세 [시술실 선택] 열림 · 신분 칸 비어도 [접수 완료] 켜짐 → 누름 → 남은 단계(작업 추가 · 방 · 끝 단계)만. **(b) 방까지 붙음**: KOS 웹에서 접수 → 「방 배정」 작업 추가 → 시술 대기로 올려 방 지정 → 단계를 「접수」로 되돌린 예약(D-31 AS-IS 의 끝만 「접수」로) → ccc 상세 = 「시술실 · {그 방}」 고정(팝오버 안 열림) · [접수 완료] → 끝 단계만 | (a) 「방 배정」 작업 **하나만** · 고른 방 · 끝 단계 / (b) 작업 · 방 그대로(새 작업 0) · 끝 단계만 바뀜 | §5.6 · D-48 · r1 F1 |
| 24 | [예약 취소] — 취소 · 부도 | 접수 전 예약 [예약 취소] → 「예약 취소」 → 카드 흐림 + 취소선 · 「취소」 · 총 건수에서 빠짐. 다른 예약 「예약 부도」 → 「부도」 | 예약 상태 `CANCELED` / `NO_SHOW` · `flowStep` 그대로 · ccc `event_log(resv_cancel)` 2줄(`GET` 로는 안 보임 — back DB 확인) | D-20 · §8 |
| 25 | 상담사 선택 → [실장 호출] | 상담 대기 예약 상담 카드 [상담사 선택] = KOS 상담사 목록 · 상태 「비어있음 / {방} 상담 중」(KOS 에서 다른 예약을 상담 진행으로 바꿔 둔 상담사는 「{방} 상담 중」) → 골라 [{이름} 실장 호출] → 「{이름} 실장 호출됨 · HH:MM」 | 일정 `reservation.counselor` = 그 상담사 · 다른 칸 그대로 | §5.8 · D-35 ~ D-37 |
| 26 | 상담 진행 · 완료 · 단계 카드 | KOS 에서 [상담 시작](사용자) → 10초 안에 상담 카드 「상담 진행 중 · HH:MM」 · 카드 부상태 「진행」 → KOS 에서 시술 대기로 → 상담 카드 「상담 완료」 · 단계 카드 「시술 대기」 · 시술 현황 카드 생김 | (KOS 조작은 사용자) | §5.8 · D-35 · D-05 |
| 27 | 원내 현황 | 오늘 · 「원내 현황」 탭 = 접수 ~ 귀가 대기 고객만 · **구역별 묶음(머리 「{구역} N명」)** · 필터 5(수 · 두 구역 합) · 카드 Badge(수납 필요 먼저) · 금액 3칸(전체 · 결제 · 수납 필요) · 카드 누르면 상세 + 스케줄 표 스크롤 | 금액 = KOS 수납과 같음 | §6.4 · §5.9 |
| 28 | 귀가 대기 정산 — 수납 필요 | 시술 현황에서 [귀가 대기]한 고객(또는 KOS 에서 귀가 대기 + 수납 안 한 추가 시술) → 상세 정산 상자 「수납 필요 1건」 빨강 · [귀가 완료] 꺼짐(**이유 글자 없음** — 0.3.0) · [수납하기 ›] → 새 탭 KOS 수납 화면(그 고객 · 그 일정) | KOS 화면이 그 일정으로 열림(로그인 세션 · 탭 — OQ-730) | §5.9 · §5.10 · D-40 · D-41 |
| 29 | [처방전 출력] | 처방전 있는 일정 = 「처방전 N건」 + [처방전 출력] → 새 탭 KOS 일정 상세 「기타 업무」 탭 · 없으면 「오늘 처방전 없음」(데모 처방전 0건이면 KOS 에서 하나 만들어 확인 — 사용자 판단) | 그 탭이 열림 | §6.6 · D-42 · OQ-729 |
| 30 | [귀가 완료] | **상세 모달을 연 채로** KOS 에서 수납 확정(사용자) → **5초 안에** 정산 상자 「수납 필요」 0 · [귀가 완료] 켜짐(닫았다 열지 않음 — 0.3.0 · D-52) → 누름 → **모달 닫힘 + 토스트 「{이름} 귀가 완료」** · 카드 「귀가 · 완료」 · 시술 현황 카드 사라짐 | 일정 `COMPLETED` · 예약 상태 `COMPLETED` | §5.10 · §6.7 · D-52 · OQ-728 |
| 31 | 동기화 · 실패 | KOS 웹에서 예약 메모를 고치면 10초 안에 상세(다시 열면) · 카드 위치 이동은 10초 안에 판 · back 내부 API 주소를 틀리게 두면 「조회 실패」 글자 + 마지막 사본 그대로 · 조작은 502 토스트 | — | §4.2 · §4.4 · §6.7 |
| 32 | 좁은 화면 · 시안 대조 | 760 미만 = 패널 없음 · 시안 「예약 현황」 장면과 나란히 놓고 §6.8 표 밖 차이가 없는지 | — | §6.8 |
| 33 | 부도 고객 접수 | 부도 카드(빨강 외곽선 · 흐림) 상세 → [예약 취소] 없음 · 방 → [접수 완료] 켜짐(신분 조건 없음 — 0.3.0) → 누름 → 상담 대기/시술 대기 · 카드 흐림 풀림 | 일정 예약 상태 `NO_SHOW` → `IN_PROGRESS` · 단계 · 「방 배정」 + 방 | §5.6 · D-47 · CS§2.1 |
| 34 | 카드 「수납 필요」 | WP-KOS 가 남긴 「귀가 대기 + 수납 필요」 일정(오늘 · 「기타」 칸)과 #28 고객 카드 = 「수납 필요」 Badge(warning sm · 시술 현황 카드와 같은 꼴) · 「방 배정」만 있는 카드 · 수납 끝난 카드 = Badge 없음 · KOS 에서 수납 확정 → 10초 안에 Badge 사라짐 | 작업 `paymentRequired` 와 같음 | §5.9 · §6.3 · D-50 |
| 35 | 다른 구역 예약 | KOS 웹에서 「미사용」 구역 「제모」에 예약 하나(사용자 · 데모) → ccc 판 「제모」 칸에 카드 · 칸 머리 건수에 들어감 · 상세 머리 「미사용 / 제모」 · [시술실 선택] = 그 구역 방 · 원내 현황 = 「미사용」 묶음 · 4층 정원 줄 `full` 과 따로 | KOS 「예약 현황」과 같음 | §5.2 · §5.4 · §5.7 · D-44 |
| 36 | **[+ 상담 추가]**(0.3.0) | 상담 진행 또는 시술 대기 고객 상세 → 「내원 현황」 머리 [+ 상담 추가] 켜짐(상담 대기 · 접수 전 · 귀가 완료면 꺼짐) → 누름 → 토스트 · 머리 「상담 대기」 · 상담 카드 「상담 대기」 · [상담사 선택] → [실장 호출] 다시 됨 | 일정 `CONSULTATION_WAITING` · 상담 기록 새로 안 생김 · 다른 칸(작업 · 방 · 상담사) 무엇이 바뀌었는지 기록(backend 시험과 대조) | §5.8 · §8 · D-55 · OQ-767 |
| 37 | DS 컨트롤 · 달력(0.3.0) | 등록 모달 · 상세 모달 · 패널의 select · 날짜 · 시각이 모두 DS 모양(브라우저 기본 위젯 0) · 제목 줄 날짜 글자 누르면 DS 달력 → 고른 날짜로 판 이동 | — | §6 머리 · §6.2 · OQ-762 |
| 38 | 공지 영역(0.3.0) | 공지 없는 날도 공지 영역 높이 그대로 · 창 높이를 바꾸면 비율대로 커지고 줄어듦 · 긴 공지는 영역 안에서 스크롤 · 공지 줄에 시각 글자 없음 | — | §6.4 |
| 39 | 시간축 · 스크롤(0.3.0) | 오늘 첫 화면 = 지금 시각 줄이 위쪽에 보임 · 06:00 · 22:00 끝까지 스크롤 · 10초 폴링에도 스크롤 안 튐 · 다른 날짜 = 그날 운영 시작 줄 | — | §5.2 · §6.3 · D-57 |
| 40 | 상세 폴링(0.3.0) | 상세 모달을 연 채로 KOS 웹에서 예약 메모 · 단계를 바꾸면 5초 안에 모달에 보임 · 고객 기본 정보에 입력하던 값은 폴링이 덮지 않음 · 모달을 닫으면 상세 요청이 멈춤(back 로그) | — | §6.7 · D-52 |
| 41 | 등록 SNS · 상세 SNS(0.3.0) | 등록 모달 · 상세 「고객 기본 정보」 SNS 종류 = 드롭다운(기타 · 카카오톡 · 라인 · 인스타그램 · 왓츠앱 · 위챗) → 저장 | KOS 고객 `snsInfo.snsType` = 고른 enum 값 | §5.5 · §6.5 · §6.6 · OQ-766 |

**대조 — §1.1 「넣는다」 → §9 #**

| 넣는 것 | # |
|---|---|
| 헤더 「현황 › 예약 현황」(시술 현황 그대로 · 첫 화면 시술 현황) | 1 |
| 날짜 이동 · [오늘] · 두 구역 전부 | 2 · 35 |
| 칸 = 그룹 전부 · 시간축(06–22) · 칸 머리 · 칸 폭 | 3 · 39 |
| 카드(성별 · 이름 · 발음 · 초진/재진 · 국기 · 주 상태 색 · 부상태 · 수납 필요 · 2줄) | 4 · 34 |
| 범례 7 · 총 N건 | 5 · 24 |
| 칸 [+] → 예약 등록 | 7 |
| 드래그 이동 · 정원 미리 막기 · 거절 원위치 · 길이 유지 | 10 · 11 · 12 |
| 「예약 요청」 탭 = 공지(그 날짜 · 고정 비율 높이) + 요청 자리만 | 6 · 38 |
| 「원내 현황」 탭(필터 · 카드 · 수납 필요 · 구역별) | 27 · 35 |
| 등록 모달: 검색(첫 페이지 목록) · 결과 표 · 신규/기존 · KOS 칸(지정 의사 · 상담 필요 · 수면 뺌 · SNS 드롭다운) · 신규 구분 규칙 · 중복 → 생성 → 예약(이름 경고 없음) | 7 · 8 · 9 · 41 |
| 상세: 기본 정보(먼저 채움 → 고쳐 저장) | 13 |
| 신분 확인(웹 수동 표시만 · 접수 조건 아님) | 14 · 21 · 33 |
| 유입 · 예약 메모 | 15 |
| 건강 정보(확인 필요) | 16 |
| 특이사항 읽기 · 쓰기 | 17 |
| 이전 방문(오늘 뺌) | 18 |
| 진행 경로(접수 때 고르는 값 · 초진 · 재진) | 19 · 21 · 22 |
| [시술실 선택] → [접수 완료] 묶음(상담 대기 · 시술 대기 · 부도 접수 · 이어 하기) | 20 · 21 · 22 · 23 · 33 |
| [예약 취소](취소 \| 부도) · 취소 로그 | 24 |
| 내원 현황 · [+ 상담 추가] · 상담 카드 · [상담사 선택] → [실장 호출] · 단계 카드 2계층 | 21 · 25 · 26 · 36 |
| 귀가 대기 정산(전체 · 결제 · 수납 필요 · [수납하기 ›] · [처방전 출력] · [귀가 완료] 꺼짐 · 상세 5초 폴링 · 성공 닫힘) | 28 · 29 · 30 · 40 |
| 계정 역할 코디(코디 수락 포함) | 1 |
| ccc DB(신분 확인 · 조작 로그 · 문진 이력) | 14 · 24 · 16(문진 이력은 back DB 확인) |
| (0.3.0) 화면 전체 DS 컨트롤 · 날짜 달력 | 37 |

빠진 「넣는다」 항목 0.

**back 단위 시험**(pytest · KOS 는 가짜 클라이언트 — **가짜 응답 모양 = WP-KOS K1 실제 모양**: 문진 제출본 최상위 · 없음 400 + `errorProperties` · `room:{id:""}` · 밀리초 없는 시각 · 빈 칸 키 없음): §5.1 상태표 전부 · §5.2 축(합 · 휴무 요일 null · 축 밖 예약) · 카드 = 묶음당 1장 · 「그룹 없음」 칸 · 칸 머리 정원(구역 하나 · 둘 · 없음) · §5.3 건수(취소 · 부도 뺌) · §5.4 `full` 구역별(제자리 허용 · 카드 구역 · [+] = 모든 켜진 구역 꽉 참) · 이동 길이 유지 · 구역 그대로 · 간격 경계 400 · §5.5 신규 구분 규칙(다섯 갈래 각각 · 이름만 409) · 중복 409 + candidate · **등록 본문에 `doctors` · `consultationRequired` · `sedationRequired` 없음 · 요청에 넣으면 422 · `sns.type` enum**(0.3.0) · 고객 검색 빈 조건 = 첫 페이지(400 아님) · 담당자 기본 · 구역 기본 · `funnel` 본문 = 코드 행 전체 · §5.6 갈래(새 접수 = 예약 · 부도 / 이어 하기 = `RECEPTION` 방 유무 무관 · **둘 다 신분 조건 없음** — 0.3.0 · 신분 칸 빈 고객도 접수됨) · 0단계 KOS 단계로 갈래 다시 정함(끝 단계 이후 = 보내지 않고 ok) · ~~신분 칸 409 `identity_incomplete`~~ · **끝 단계 = 요청 `route`**(생략 = 상담 대기 · `consultationRequired` 를 읽지 않음 · `update-reservation` 호출 0) · 붙은 방 고정 · 다른 방 409 `room_locked` · 묶음 순서 · 건너뛰기(이미 접수 · 이미 「방 배정」 · 이미 방 · 이미 그 단계) · 단계 실패 멈춤 + `step` · 반영 기다림(2 · 4 · 5) 5번 → `kos_slow` · §5.7 사용 중(구역별 · 오늘 사본 갱신) · §5.8 상담사 상태(두 구역) · 호출 단계 · 상담 카드 보임 조건 · **[+ 상담 추가] 켜짐 · 공개 `changeFlowStep(CONSULTATION_WAITING)` 본문 · `event_log(consultation_add)`**(0.3.0) · §5.9 수납 필요(「방 배정」 = SPEC-003 판정 · visit 없음 = 호출 0 · 취소 뺌) · 금액 계산 · §5.10 귀가 막기 · KOS 400 → 409 `kos_rejected` · §5.11 확인 필요 · 제출본 없음(`errorProperties`) · 이력 쌓기(같은 제출본은 한 번) · ~~§5.12 신분 칸(외국인 · 내국인 · 국적 빈 값 · 영문명 하나)~~(0.3.0 — 접수 판정 아님) · ccc 표시 마지막 줄 · §5.13 이전 방문 오늘 뺌 · 고객 저장 = 다시 읽은 묶음 + 바꾼 칸(없던 키는 안 보냄) · 특이사항 = 관리 묶음 + memo · §5.14 `can.*` · `KosError.errorProperties` · §4.4 문구 표 · 날짜별 캐시(10초 · 동시 한 번) · 조회 실패 `sync.lastError` · 409 · 502 매핑 · `event_log` 줄 · `PROC_FAKE_BOARD`(GET 가짜 · 조작 403) · 역할 네 개 · 코디 계정 만들기 · **코디 수락(`doctorId` 필수 · 없으면 400)** · 경로 34(`test_route_count_34` — 0.3.0: `PUT …/route` 없음 · `POST …/consultation-add` 있음) · 축 = 06–22(휴무 요일 `closedDay`).

E2E 공통: 브라우저 두 개(데스크 PC 둘)를 열어 둔다 — 한쪽 조작이 다른 쪽에 10초 안에 보인다(#11 · #12 · #21). 시술 현황 화면을 다른 탭에 열어 두고 #22 · #26 · #30 에서 카드가 생기고 사라지는지 본다. 백엔드 커밋 뒤 compose 를 다시 올린다.

## 10. 열린 것

「planner 기본값 — 사용자 확인 대기」 = 결정에 없어 이 문서가 리포트 · 결정 · 시안 안에서 고른 구현값. 사용자가 바꾸면 바뀐다. 「이번 판 밖」 = 구현하지 않는다. **「닫음」** = 0.2.0 에서 사용자 결정(D-44 ~ D-50) 또는 WP-KOS 데모 확인으로 닫힌 것 — 줄은 지우지 않는다(번호 유지).

| ID | 질문 | 지금(기본값) | 상태 |
|---|---|---|---|
| OQ-701 | 하루 일정 조회 길 · 구역 범위 · 시술 현황 조회와 합치기(R Q-20 · Q-22) | 내부 `get-schedules-for-reservation` **1번** · **구역 = 두 개 전부**(D-44) · 화면이 볼 때 · 시술 현황(`get-schedules-grouped-by-zone` · 10초 · 4층)과 **합치지 않는다**(예약 사본 따로 · §3.1) — 근거: 공개 8번보다 1번 · 리포트가 결과 id 집합 같음 확인(R§2) · 시술 현황 E2E 중인 코드를 흔들지 않음 | **구역 = 닫음(U1 · D-44)** · 1번 · 합치지 않음 = planner 기본값 — 사용자 확인 대기 |
| OQ-702 | 예약 그룹 id 필드 · 그룹 여럿 차지한 일정(R Q-21 · Q-4 나머지) | `occupiedResources[].reservationGroup.reservationGroupId`(없으면 `reservation.reservationGroupId`) · 묶음 한 개당 카드 한 장 · 사본에 없는 그룹 = 「그룹 없음」 칸 | planner 기본값 — 사용자 확인 대기 |
| OQ-703 | ccc 사본에 둘 개인정보 범위(DEC-005 D-14) | 카드 값만 저장(이름 · 발음 · 성별 · 국적 · 신규 · 차트) · 상세 개인정보 · 특이사항 · 문진 답 · 수납 · 신분 칸은 열 때 KOS 에서 읽고 저장 안 함(문진 이력만 예외 — D-24) | **닫음 — U3 · D-46** |
| OQ-704 | 갱신 방식 · 수납 정보 조회 주기(PD Q-108 · 디자인 Q-7) | front 10초 폴링 · back 날짜별 10초 캐시 · SSE 안 씀 · 조회 시간 제한 없음 · 수납 = 판 조회(오늘 원내)와 상세 — **0.3.0: 상세는 열린 동안 5초 폴링**(D-52 · 사용자 지시 · 주기 5초는 코디 기본값) | planner 기본값 — 사용자 확인 대기 |
| OQ-705 | 예약 조작을 대기열(SPEC-003 `kos_op`)로 보내나 | **동기** — KOS 응답을 기다려 성공 · 실패(§4.4). 재전송 없음 | planner 기본값 — 사용자 확인 대기 |
| OQ-706 | 고객 검색 길(C Q-50) | 내부 `get-visitors`(이름 하나로 · 발음 · 전체 수) — 코디 기본값(브리프 §3) · 0.3.0: 빈 조건 = 첫 페이지 목록(OQ-761) | planner 기본값 — 사용자 확인 대기 |
| OQ-707 | 신규 구분 규칙 검사 위치(C Q-52) | front 버튼 끄기 + back 409 둘 다 | planner 기본값 — 사용자 확인 대기 |
| OQ-708 | KOS 중복 확인에서 기존 고객이 나오면 | 새로 만들지 않고 409 `duplicated_visitor` → [이 고객으로] | planner 기본값 — 사용자 확인 대기 |
| OQ-709 | 「신규 고객 / 기존 고객 · No.N」 표시(C Q-61) | 신규 = 「신규 고객」(차트번호 없음) | planner 기본값 — 사용자 확인 대기 |
| OQ-710 | 예약 담당자(C Q-60 · RT Q-75) | 칸 = 활성 직원 · 기본 = 시스템 계정(테넌트 계정 id) | planner 기본값 — 사용자 확인 대기 |
| OQ-711 | 내부 `reserve` 의 `occupiedResources[].id`(C Q-62) | ccc 가 uuid4 | planner 기본값 — 사용자 확인 대기 |
| OQ-712 | 예약 길이 ↔ 그룹 간격(TA Q-127) | 새 예약 = 그룹 간격 · 이동 = 원래 길이 · KOS `intervalExceeded` 경고는 그리지 않음 | planner 기본값 — 사용자 확인 대기 |
| OQ-713 | 정원 밖 검사 · 휴무 · 당일 마감 버퍼 · 시간 점유(C Q-55 · TA Q-124 · Q-128 · R Q-5 나머지) | 막는 것은 정원(슬롯 사본)뿐 · 운영 밖 회색 칸에도 [+] · 휴무 · 시간 점유는 조회 · 표시하지 않음(응답 모양 미확인 · 데모 0건) · 그룹 시간표가 빈 요일 = 운영 안 함 | planner 기본값 — 사용자 확인 대기 |
| OQ-714 | 이동 길(MC Q-89) · 옮길 수 있는 단계 | **내부 `update-reservation`**(묶음 id 유지 · KOS [이동] 과 같은 길 — `_RESUME 10-26 #60`) · 예약 · 접수만 · 구역 그대로. 지정 의사 · 메모 · 유입 등이 남는 것은 **K3 로 데모 확인**(`doctors` 를 실어 보낸 모양). 공개 `updateReservationV2` 는 묶음 id 를 새로 만들고(MC§2.3) 의사 값을 받지 않는다(C§5 — 지워지는지는 시험 안 함) — 브리프 예시(공개)와 다르게 골랐다 | planner 기본값 — 사용자 확인 대기 |
| OQ-715 | 접수 뒤 취소 · 부도 · 되돌리기(MC Q-86 · Q-87) | 시안대로 접수 전만 · 되돌리기 버튼 없음(로그만 — D-20) | planner 기본값 — 사용자 확인 대기 |
| OQ-716 | 부도 · 취소 일정의 접수(CS Q-99) | **부도 = 접수 허용**(KOS 그대로 · `recept` 가 받아 `IN_PROGRESS`) · 취소 = 막음 | **닫음 — U4 · D-47** |
| OQ-717 | 접수 길 · 끝 단계 길(RM Q-63 · RT Q-73 · RM Q-67) | 내부 `recept` · 내부 `change-flow-step`(데모 확인된 묶음 그대로) | planner 기본값 — 사용자 확인 대기 |
| OQ-718 | 묶음 중간 실패 · 반영 지연(RM Q-64 · Q-65 · RT Q-74) | 되돌리지 않음 · **이어 하기**(§5.6 — `RECEPTION` 이면 방 유무 무관 · 붙은 방 고정 · 신분 조건 없음 · 끝 단계 이후면 그대로 성공) · 다시 읽기 1초 × 최대 5번 → 409 `kos_slow` | **닫음 — U5 · D-48**(규칙은 r1 F1 고친 것) |
| OQ-719 | [접수 완료] 켜짐 조건(시안 「신분 필드 모두 입력」) | ~~예약(또는 부도) + 방 + KOS 신분 칸 다 채움~~ → **예약(또는 부도) + 방**(신분 조건 없음) · ccc 「확인 완료」는 표시만 | **닫음 — ~~U2 · D-45~~ → 2026-10-27 D-54**(사용자 E2E) |
| OQ-720 | 방 「사용 중」 범위(RT Q-77 · 디자인 Q-19) | 오늘 · **그 예약 구역**(D-44) · 접수 ~ 시술 진행 일정의 안 취소된 방 붙은 작업(귀가 대기 · 귀가 · 예약 단계 뺌) · 계산 전 오늘 사본 갱신 | planner 기본값 — 사용자 확인 대기 |
| OQ-721 | 「방 배정」 기타 작업이 없는 지점(RM Q-71) | 제목 「방 배정」으로 찾고 `KOS_ROOM_TASK_ID` 로 덮을 수 있음 · 없으면 409 | planner 기본값 — 사용자 확인 대기 |
| OQ-722 | 「데스크 {직원}」(R Q-14 · RM Q-69) | ccc `reception` 이벤트 actor 이름 · ccc 가 안 했으면 뺌 | planner 기본값 — 사용자 확인 대기 |
| OQ-723 | 진행 경로 라디오를 초진에도 여나 | ~~시안대로 접수 전 + 재진만 · 초진은 값만~~ → **초진 · 재진 모두 · 기본 상담 필요 · 접수 때 고르는 ccc 값** | **닫음 — D-51(2026-10-27 사용자 E2E)** |
| OQ-724 | 상담 카드 「진행 중 · {시각}」(CS Q-101) | `flowStepUpdatedDateTimeUtc` | planner 기본값 — 사용자 확인 대기 |
| OQ-725 | [실장 호출] 가능 단계 · 「호출됨」 원천 | 상담 대기 · 상담 진행 · 「호출됨」 = ccc `counselor_call` 마지막 이벤트 | planner 기본값 — 사용자 확인 대기 |
| OQ-726 | 금액 계산 범위(R Q-15 · PD Q-105 · PP Q-111 · Q-112) | 전체 = 항목 `priceV2.amount.value` 합 · 결제 = `APPROVED` 이고 `canceledRefId` 없는 거래 합 · 여러 수납 다 더함 · `ACCEPTED`/`PAID` 구분 안 함 · **후납 금액 칸 없음 → 「수납 필요 N건」**(v3 기본값) | planner 기본값 — 사용자 확인 대기 |
| OQ-727 | 「수납 필요」 판정(PD Q-106 · PP Q-113 ~ Q-115 · PC Q-118) | 시술 현황과 같게 — `paymentRequired` · 「방 배정」(SPEC-003 판정 · 잇는 키 §5.9) · 취소 뺌 · 같은 옵션 작업 둘은 둘로 셈. 카드 · 원내 현황 · 정산 상자 같은 값(D-50) | planner 기본값 — 사용자 확인 대기 |
| OQ-728 | [귀가 완료] 길 · 남은 작업(PD Q-110 · PP Q-116 나머지) | 공개 `changeFlowStep(COMPLETED)` · 남은 작업 취소 안 함 · KOS 가 거절(400 `InvalidRequestException`)하면 토스트 | **닫음 — WP-KOS K9 · K9b(2026-10-26 데모 확인)**. 거절 이유(수납 필요 / 안 끝난 시술)는 못 가름 — `errorProperties` 를 남기면(§4.4) E2E 에서 보인다 |
| OQ-729 | [처방전 출력] 남은 것(RX Q-131 ~ Q-134 · RXD Q-136 · Q-137) | `prescriptionIds` ≥ 1 이면 「처방전 N건」 + 버튼 · 0 이면 「오늘 처방전 없음」만 · `historyMenu` 안 붙임 · 약 이름 · 「출력됨」 표시 없음 · 데모 처방전으로 실물 확인은 사용자 판단 | planner 기본값 — 사용자 확인 대기 |
| OQ-730 | [수납하기 ›] — KOS 웹 세션 · 탭 · 결제 단말(PD Q-102 ~ Q-104) | 딥링크 `tab=purchase` · 새 탭 · 데스크 PC 브라우저에 KOS 로그인이 되어 있다고 본다 · 결제 단말은 KOS 쪽 | 열림 — E2E #28 에서 확인 |
| OQ-731 | 「확인 필요」 글자 비교 · 다국어 답 | 답 `answerTitle` 앞뒤 공백 뺀 값이 「없음」 · 「아니오」 가 아니면. 다른 언어 양식의 답 글자는 미확인 | planner 기본값 — 사용자 확인 대기 |
| OQ-732 | 문진 방문별 이력을 언제 쌓나 · 보이나 | 상세 조회 때 제출본이 새로우면 한 줄(읽기 때 쌓기) · 화면에 안 보임(앱 판에서 쓰는 길) | planner 기본값 — 사용자 확인 대기 |
| OQ-733 | 신분 확인 단위 · 되돌리기 | 고객 단위 · 마지막 줄 · [미확인으로]는 접수 전만 | planner 기본값 — 사용자 확인 대기 |
| OQ-734 | 국기 그림 출처 · 모르는 코드(R Q-8 은 닫힘) | npm `flag-icons` · 모르면 회색 상자 + 코드 | planner 기본값 — 사용자 확인 대기 |
| OQ-735 | 작은 표시(R Q-7 · Q-9 · Q Q-31 · U Q-48) | 성별 미지정 = 아이콘 없음 · 나이 = 생년월일 있을 때만 · 휴대폰 = KOS 값 그대로 · 국적 목록 = front 고정 ISO 표 | planner 기본값 — 사용자 확인 대기 |
| OQ-736 | 취소 · 부도 카드 흐리게(MC Q-90 나머지) | 시안대로 불투명 0.5 + 이름 취소선 | planner 기본값 — 사용자 확인 대기 |
| OQ-737 | 공지 모양 · 수정(R Q-17 나머지 · 디자인 Q-21) | 그 날짜 목록 · 읽기만 · 수정은 KOS 에서 | planner 기본값 — 사용자 확인 대기 |
| OQ-738 | 이전 방문 결과 글자(R Q-23 나머지) | 방문 완료 · 노쇼 · 취소 · 그 밖은 KOS 값 그대로 | planner 기본값 — 사용자 확인 대기 |
| OQ-739 | 기존 고객 수정 — 권한 · 날짜 꼴(U Q-41 · Q-47) | `dateOfBirth` = `yyyy-MM-dd 00:00:00.000Z` · `passportExpiryDate` = `yyyy-MM-dd` · 시스템 계정 · 읽은 묶음 + 바꾼 칸(없던 키는 안 보냄) | **닫음 — WP-KOS K7(2026-10-26 데모 확인)** |
| OQ-740 | 특이사항 동시 수정(MT Q-81) | 쓰기 직전 다시 읽기(그 사이 바뀐 관리 칸을 덮지 않게) | planner 기본값 — 사용자 확인 대기 |
| OQ-741 | 스캔 영문 이름 넣을 곳(U Q-42) | 이번 판 = 데스크가 손으로 「여권 영문 성 · 이름」 칸(`passportSurname` · `passportGivenNames`)에 · `name` 은 건드리지 않음(카드 이름 = `name` — D-13) | planner 기본값 — 사용자 확인 대기 |
| OQ-742 | 코디 역할의 시술 현황 권한 | 관리자와 같다(D-30 — 제한 없음) · 코드 `service/actions.py` `accept()` 의 `admin` 분기에 `coordinator`(§3.4) | planner 기본값 — 사용자 확인 대기 |
| OQ-743 | 시술 현황판 상태 2계층 맞추기 범위 · 시점(D-43) | **이번 판 밖** — 시술 현황 다음 판(SPEC-003 개정) | 이번 판 밖 |
| OQ-744 | KOS 소켓 실시간 · 놓친 이벤트(PC Q-119 · Q-120) | 다음 버전 — 조회로 · 0.3.0: **따로 검토**(시술 현황 포함 · 10초 조회 · 상세 5초 폴링을 대체할지 — D-52 · `_RESUME` §1 10-27) | 이번 판 밖(검토 열림) |
| OQ-745 | 취소 되돌리기 버튼 | 다음 버전 — `event_log(resv_cancel)` 이 원천 | 이번 판 밖 |
| OQ-746 | 상담사(실장) 계정 · 앱 푸시 · 동시 로그인 세부(`_RESUME` §1 메모 · #71) | 다음 판(앱) | 이번 판 밖 |
| OQ-747 | 문진 제출 길(공개 ↔ legacy) · 덮어쓰기 · 문진 → 시안 칸 · KOS 직원 화면 문진 위치(Q Q-28 · Q-30 · Q-32 ~ Q-34 · Q-38 · R Q-10) | 다음 판(앱 질문지) — 이번 판은 읽기만 | 이번 판 밖 |
| OQ-748 | 고객 입력 기기 연결 · 스캐너 · 신분증 이미지 업로드(Q Q-25 · U S16) | 다음 판(앱) | 이번 판 밖 |
| OQ-749 | 「수납 중」 표시 · 남은 시술권 · 수납 → 시술 목록(PC Q-122 · PP Q-117 · PD Q-107) | 표시 안 함 · 수납 → 작업은 v2 1 「상담사가 시술을 추가」로 고쳐 둠 | 이번 판 밖 |
| OQ-750 | [+ 상담 추가](CS Q-95) | ~~만들지 않음~~ → **넣는다**(§5.8 · 세부 OQ-767) | **닫음 — D-55(2026-10-27 사용자 E2E)** · KOS 동작은 OQ-767 |
| OQ-751 | 확인 작업 — KOS 웹 눈 확인 · 시험이 남긴 데모 상태 알림 · HAR 요청 수(RT Q-78 · MC Q-91 · R Q-24) | E2E #21 에서 눈 확인 · WP-KOS 가 남긴 데모 데이터(고객 1 · 일정 2 — 리포트 §5)는 사용자 통보 대상 · E2E 가 남긴 데모 예약 목록도 같이 · HAR 수는 다시 뜨지 않음 | 열림 — WP-E2E(WP-KOS 몫은 끝남) |
| OQ-752 | 예약 현황 경로(SPEC-003 OQ-524 의 예약 쪽) | `/reservations/live`(시술 현황과 짝) · 첫 화면 · 「현황」 글자 = 시술 현황 그대로(D-49) | planner 기본값 — 사용자 확인 대기(경로 이름만) |
| OQ-753 | `create-visitor` 동의 플래그(HAR = true 로 보냄) | 보내지 않음 — 받음. KOS 기본값: 개인정보 · 광고 = false · **정보성 알림 = true**(사용자 알림거리) | **닫음 — WP-KOS K2-2(2026-10-26 데모 확인)** |
| OQ-754 | `reserve` 의 `funnel` 본문 모양 | `funnel:{funnel:<FUNNEL 코드 행 전체>, funnelDetail}`(KOS 웹 JS 계약 + 실호출 · `funnelCategory` 안 보냄) | **닫음 — WP-KOS K2-3(2026-10-26 데모 확인)** |
| OQ-755 | 내부 `update-reservation` 부분 수정(진행 경로 · 상담사 · 이동)이 다른 칸을 지우지 않나 | 안 지운다(K3 · K4 · K5 — 전부 `RESERVED` 에서). 접수 뒤 단계의 상담사 지정은 E2E #25 | **닫음 — WP-KOS K3 ~ K5(2026-10-26 데모 확인)** |
| OQ-756 | 접수 묶음 끝 단계 `PROCEDURE_WAITING`(바로 시술) | 받음 · 방 없음 판정 = `room.id` 빈 값 · `change-tasks-room` 약 1초 뒤 보임 | **닫음 — WP-KOS K8(2026-10-26 데모 확인)** |
| OQ-757 | **작은 기본값 묶음**(r1 W4 — 본문에 「기본값」으로만 있던 화면 값 · 한 줄로 확인) | ① 모르는 `flowStep` = 예약(§5.1) ② 부도 색 = 빨강 외곽선(§5.1) ③ 부상태 칩 = 이름 줄 끝 작은 글자(§5.1) ④ 1시간 높이 = 144px(§5.2 · 줄 높이만 — 카드 높이는 2줄 · 0.3.0) ⑤ 축(06–22) 밖 예약이면 축을 늘림(§5.2) ⑥ 「그룹 없음」 칸(§5.2) ⑦ 휴무 요일 = 축 그대로 · 전 칸 회색 + 「운영하지 않는 날이에요」(§5.2 · 0.3.0 고침) ⑧ 접수 뒤 기본 정보 회색 잠금 + [수정](§5.13) ⑨ 동기화 글자 「마지막 KOS 조회 · 조회 실패」(§6.2) ⑩ 불러오는 중 · 조회 실패 표시(§6.3) ⑪ 원내 현황 = 오늘만 · 범위(접수 ~ 귀가 대기) · 정렬 = 구역 → 접수 시각(§6.4) ⑫ 국적 `KR` → 주민번호 · 「주소」 / 아니면 여권 · 「주소 (자국)」(§6.6) ⑬ 취소 팝오버는 고르면 바로 KOS(확인 없음 · §6.6) ⑭ 토스트 문구(§6.7) ⑮ 상세 부분 실패 = 그 칸만 null(§7.3) ⑯ `KOS_WEB_BASE` 비면 [수납하기 ›] · [처방전 출력] 끔(§2.3) ⑰ (0.3.0) 다른 날짜로 옮기면 그날 가장 이른 운영 시작 줄로 스크롤 · 폴링에는 스크롤 안 옮김(§6.3) ⑱ (0.3.0) 공지 영역 비율 = frontend 구현값(§6.4) ⑲ (0.3.0) 상세 5초 폴링이 입력 중인 칸 · 조작 중엔 건너뜀(§6.7) | planner 기본값 — 사용자 확인 대기(하나씩 바꿔도 다른 줄에 안 번짐) |
| OQ-758 | **구역 두 개의 세부**(U1 · D-44 가 정하지 않은 화면 값) | 칸은 구역으로 나누지 않음(KOS 처럼 한 칸에 두 구역) · 칸 머리 정원 = ~~하나면 「3명」, 둘이면 「4층 3 · 미사용 3명」~~ **0.3.0 한 꼴 — 늘 「{구역} {n}」을 잇고 끝에 「명」**(하나 = 「4층 3명」 · 둘 = 「4층 3 · 미사용 3명」 · 피드백 #7 · frontend 결과로 확정) · [+] = 켜진 구역 중 하나라도 자리 · 등록 「구역」 칸(기본 `KOS_ZONE_ID` · 하나면 숨김) · 이동은 구역 그대로 · 원내 현황 = 구역별 묶음(필터 수는 합) · 상담사 지금 상태 = 두 구역 합(사람 단위) · 다른 구역 방 = 1시간 `get-rooms` 로 같은 사본 · 시술 현황(SPEC-003)은 4층 그대로 | planner 기본값 — 사용자 확인 대기 |
| OQ-759 | **KOS 신분 칸의 세부**(U2 · D-45 「내국인 = SPEC 이 정한 칸」) | ~~내국인 = 생년월일 · 주민등록번호 · 외국인 = 여권 영문명 · 생년월일 · 여권번호 …~~ — 접수 조건이 없어져(D-54) 쓸 곳이 없다 | **닫음 — D-54(2026-10-27 · 피드백 #12 「주민등록번호 · KOS 에서 제약 없음」)** |
| OQ-761 | (0.3.0) 고객 검색 빈 조건 — 내부 `get-visitors` 가 조건 없는 조회를 받고 페이지를 주는지 | 받는다고 보고 빈 조건 = 첫 페이지(구현 확정 「빈 조건 = 목록(page)」) | 열림 — backend batch 1 보고 · E2E #8 |
| OQ-762 | (0.3.0) `procedure/front` 에 DS Select · DatePicker/Calendar · TimePicker 가 있나 | 있으면 그것 · 없으면 만들지 않고 질문(batch 1 frontend 브리프) | 열림 — frontend batch 1 보고 |
| OQ-763 | (0.3.0) 칸 폭 `mx` = 겹침 최대 수(시안 식) ↔ 정원만큼 늘 자리(사용자 「3명이 한 열에 들어가야 하는데」 · 피드백 #3) | 시안 식 그대로(겹침 최대 수 · `perRow` 상한) — 정원 3 · 겹침 3 이면 3장 | **planner 기본값 — 사용자 확인 대기**(사용자 원문은 정원 쪽으로도 읽힌다 — E2E #3 에서 눈 확인) |
| OQ-764 | (0.3.0) 접수 → 「시술 대기」 + 방이 보이기까지 시간 · 다시 읽기(2 · 4 · 5) 횟수 · 간격 | 1초 × 최대 5번 그대로 · back 즉시 응답 · front 낙관 표시 | 열림 — backend batch 1 단계별 측정 수치로 정한다(피드백 #14) |
| OQ-765 | (0.3.0) 카드 2줄 높이 ↔ 15분 칸 한 줄(36px) · 30분 줄 72px 안 카드 위치 | 카드 위 = 시작 줄 경계 · 높이 = 2줄 · 줄보다 크면 한 줄 높이 + 2줄 숨김 | planner 기본값 — 사용자 확인 대기(피드백 #7 · #10 을 같이 지키는 해석) |
| OQ-766 | (0.3.0) SNS 종류 한글 글자 | 기타 · 카카오톡 · 라인 · 인스타그램 · 왓츠앱 · 위챗(값 = KOS enum) | planner 기본값 — 사용자 확인 대기 |
| OQ-767 | (0.3.0) [+ 상담 추가] KOS 동작 · 켜짐 · 상담 카드 보임 | KOS = 공개 `changeFlowStep(CONSULTATION_WAITING)`(backend 데모 1회 시험 중 — 안 받으면 멈추고 질문) · 켜짐 = 상담 진행 · 시술 대기 · 시술 진행 · 귀가 대기 · 상담 카드 = ccc 접수 기록(`route = consultation`) · `consultation_add` · 지금 단계(상담 대기 · 진행)로 판정 · 경로 `POST …/consultation-add`(구현 확정) | KOS 동작 = 열림(batch 1 시험) · 켜짐 범위 = planner 기본값 — 사용자 확인 대기 |
| OQ-760 | 내부 `reserve` · `update-reservation` 이 **정원 초과를 거르나**(r1 W2 · C§2.2 · C Q-55) | 모름 — 내부 JS 에 정원 초과 처리가 없고 WP-KOS 는 정원 시험을 안 했다. ccc 는 사본(10초)으로 미리 막기만 · 동시 조작으로 넘치면 받아들임(KOS 직원 화면 수준) · E2E #12 관찰 갈래에서 KOS 동작을 기록 · 「`ReservationCapacityExceeded`」 문구는 공개 이름 그대로 둠 | 열림 — E2E #12 |

## 부록 A. DEC-006 대응표

| D | 이 문서 |
|---|---|
| D-01 범위 | §1.1 · §1.2 · §2.1 |
| D-02 웹 정본 | 머리말 · §2.1 |
| D-03 같은 데이터 · 사본 | §3.1 · §4.3 |
| D-04 KOS 칸 그대로 | §6.5 · §6.8 · §5.9 |
| D-05 상담사 KOS 직접 | §1.2 · §5.8 · §8 |
| D-06 데모 쓰기 | §1.2 · §9 머리 |
| D-07 예약 요청 자리만 | §6.4 · §7.2 `requests` |
| D-08 · D-09 순서 · 디자인 원천 | 머리말 · §6 |
| D-10 칸 = 그룹 전부 · 국기 | §5.2 · §6.3 |
| D-11 2계층 | §5.1 · §6.3 · §6.6 |
| D-12 시간축(세로축 → D-57) | §5.2 |
| D-13 카드 이름 | §6.3 |
| D-14 건수 | §5.3 |
| D-15 공지 | §4.2 · §6.4 |
| D-16 등록 모달 · 내부 reserve | §5.5 · §6.5 · §8 |
| D-17 신규 구분 · 차트번호 | §5.5 |
| D-18 ~~이름 경고~~(→ D-56) · 중복 확인 | §5.5 |
| D-19 이동 · 드래그 | §5.4 · §8 |
| D-20 취소 사유 · 로그 · 드래그 거절 | §5.4 · §6.6 · §3.2 `resv_cancel` · §8 |
| D-21 · D-23 · D-26 스캔 · 질문지 · 이미지 | §1.2(앱 판) |
| D-22 기존 고객 수정 | §5.13 · §8 |
| D-24 문진 이력 · 특이사항 확인 | §3.2 · §5.11 |
| D-25 신분 확인 ccc | §3.2 · §5.12 |
| D-27 확인 필요 | §5.11 |
| D-28 특이사항 · 이전 방문 | §5.13 · §8 |
| D-29 · D-30 코디 역할 · 권한 | §3.4 · §7.1 |
| D-31 접수 묶음 | §5.6 · §8 |
| D-32 · D-33 진행 경로(→ D-51) · 끝 단계 | §5.6 · §5.14 |
| D-34 방 목록 | §5.7 |
| D-35 상담 흐름 · [실장 호출] | §5.8 · §8 |
| D-36 상담사 목록 | §5.8 |
| D-37 상담사 지금 상태 | §5.8 |
| D-38 상담사 푸시 | §1.2 · OQ-746 |
| D-39 후납 · 수납 필요 | §5.9 |
| D-40 수납하기 · 수납 정보 · 귀가 완료 | §5.9 · §5.10 · §7.3 `links` |
| D-41 귀가 막기 | §5.10 |
| D-42 처방전 · 여정 리포트 뺌 | §6.6 · §7.3 · §8 |
| D-43 시술 현황판 2계층 | §1.2 · OQ-743 |
| D-44 구역 두 개 전부(U1) | §3.2 `zone` · §4.2 · §5.2 · §5.4 · §5.5 · §5.7 · §5.8 · §6.4 · §6.5 · §7.2 ~ §7.5 · §9 #2 · #35 · OQ-758 |
| ~~D-45 접수 신분 조건 = KOS 신분 칸(U2)~~ → D-54 | §5.6 · §5.12 · §5.14 · §6.6 · §7.3 `identity` · §7.5 · §9 #14 · #21 · OQ-759 |
| D-46 사본 = 카드 값만(U3) | §3.1 · OQ-703 |
| D-47 부도 접수 허용(U4) | §5.6 · §5.14 · §8 · §9 #33 · OQ-716 |
| D-48 이어 하기(U5) | §5.6 · §7.3 `receiveMode` · `roomLocked` · §9 #23 · OQ-718 |
| D-49 헤더 첫 화면 = 시술 현황(U6) | §6.1 · §9 #1 · OQ-752 |
| D-50 카드 「수납 필요」(U7) | §5.9 · §6.3 · §6.8 #27 · §9 #34 |
| D-51 진행 경로 ≠ KOS 체크(10-27) | §3.2 `reception.route` · §5.6 `route` · 6단계 · §5.8 상담 카드 · §5.14 · §6.6 · §6.8 #31 · §7.3 `defaultRoute` · §7.5(`PUT route` 없앰) · §8 · §9 #19 · #21 · #22 · OQ-723 |
| D-52 상세 5초 폴링 · 소켓 따로(10-27) | §1.2 · §4.2 · §5.10 · §6.7 · §9 #30 · #40 · OQ-704 · OQ-744 |
| D-53 등록 칸 셋 뺌(10-27) | §3.2 · §5.5 · §6.5 · §6.8 #8 · §7.3 · §7.4 · §7.5(422) · §8 reserve · §9 #7 |
| D-54 접수 신분 조건 없음(10-27) | §5.6 · §5.12 · §5.14 · §6.6 · §6.8 #12 · §7.3 · §7.5 · §9 #14 · #21 · #33 · OQ-719 · OQ-759 |
| D-55 [+ 상담 추가](10-27) | §3.2 `consultation_add` · §5.8 · §5.14 · §6.6 · §6.8 #15 · §7.3 `can.addConsultation` · §7.5 · §8 · §9 #36 · OQ-750 · OQ-767 |
| D-56 이름 같은 고객 경고 뺌(10-27) | §5.5 · §6.5 · §6.8 #30 · §9 #9 |
| D-57 시간축 06–22 · 첫 렌더 스크롤(10-27) | §5.2 · §6.3 · §6.8 #2 · §7.2 `axis` · `closedDay` · §9 #3 · #39 |

## 부록 B. workflow-v3 「정할 것」 → 처분

| v3 「정할 것」 줄 | 처분 |
|---|---|
| 하루 일정 조회 길 · 그룹 id 필드 · 구역 범위 | OQ-701 · OQ-702 |
| 시간축 남은 것(빈 요일 · 길이 · 마감 버퍼 · 시간 점유) | OQ-713 · OQ-712 |
| 스캔한 영문 이름 | OQ-741 |
| 카드 · 상세 작은 표시 | OQ-735 · OQ-734 |
| 취소 · 부도 흐리게 | OQ-736 |
| 공지 모양 · 수정 | OQ-737 |
| 고객 검색 | OQ-706 |
| 신규 구분 검사 위치 | OQ-707 |
| 신규 / 기존 표시 시점 | OQ-709 |
| 정원 외 검사 | OQ-713 |
| 예약 담당자 | OQ-710 |
| `occupiedResources[].id` | OQ-711 |
| 이동 길 | OQ-714 |
| 접수 뒤 취소 · 부도 되돌리기 | OQ-715 |
| 부도 일정의 접수 | OQ-716 |
| 접수 길 | OQ-717 |
| 접수 묶음 순서 · 실패 · 지연 | OQ-718 |
| 시술 대기로 바꿀 때 시술 목록 검사 | OQ-717 · OQ-756 |
| 방 「사용 중」 | OQ-720 |
| 「방 배정」 작업 없는 지점 | OQ-721 |
| 「데스크 {직원}」 | OQ-722 |
| 문진 제출 길 · 덮어쓰기 / 문진 → 시안 칸 / KOS 직원 화면 문진 위치 | OQ-747 |
| 고객 입력 기기 연결 | OQ-748 |
| 기존 고객 수정 권한 · 날짜 꼴 | OQ-739 |
| 특이사항 동시 수정 | OQ-740 |
| 사본 개인정보 범위 | OQ-703 |
| [+ 상담 추가] | OQ-750 |
| 상담 카드 진행 시각 | OQ-724 |
| 금액 | OQ-726 |
| 「수납 필요」 판정 | OQ-727 |
| 「수납 중」 · 남은 시술권 · 수납 → 시술 목록 | OQ-749 |
| [귀가 완료] | OQ-728 |
| [수납하기 ›] 세션 · 탭 · 단말 | OQ-730 |
| 수납 정보 조회 주기 | OQ-704 |
| [처방전 출력] 남은 것 | OQ-729 |
| 이전 방문 `IN_PROGRESS` | OQ-738 |
| 확인 작업 | OQ-751 |
| 상담사 계정 · 동시 로그인 | OQ-746 · OQ-742 |
| 시술 현황판 2계층 | OQ-743 |

빠진 줄 0(v3 「정할 것」 전부 → OQ). 이번 판에 새로 연 것: OQ-705 · OQ-719 · OQ-723 · OQ-725 · OQ-731 ~ OQ-733 · OQ-752 ~ OQ-756 · (0.2.0) OQ-757 ~ OQ-760.

## 부록 C. review-doc r1 처분 (FAIL 3 · WARN 9 — 빠짐 0)

| r1 | 지적 | 처분 | 고친 곳 |
|---|---|---|---|
| **F1** | [접수 완료] 이어 하기 켜짐이 「방 붙은 작업 없음」에 묶여 5 · 6 실패 뒤 막힘 · 이어 하기 신분 조건 · 붙은 방 처리 없음 · E2E #23 선택 | 고침 — 이어 하기 = `RECEPTION`(방 유무 무관) · 0단계가 KOS 단계로 갈래를 다시 정하고 끝 단계 이후면 그대로 성공 · 붙은 방 고정(`roomLocked` · 409 `room_locked` · 5 건너뜀) · 이어 하기 신분 조건 없음(한 줄) · E2E #23 두 갈래 필수 | §5.6 · §5.14 · §7.3 `rooms` · `roomLocked` · `receiveMode` · §7.5 · §9 #23 · D-48 |
| **F2** | WP-BE1 대상 파일에 `service/actions.py` 없음 → 코디 수락 403 | 고침 — §3.4 「역할 분기를 쓰는 곳(전수)」 줄 · WORK-007 BE1 대상 파일 · 완료 조건(코디 수락 · `doctorId` 없으면 400) · E2E #1 | §2.1 · §3.4 · §9 #1 · 단위 시험 · OQ-742 · WORK-007 BE1 |
| **F3** | 「4층만」이 D-10 과 어긋남 · E2E #2 기준과 반대 | 사용자 결정 U1(두 구역 전부 · D-44)로 고침 — 하루 조회 · 그룹 조회 `zoneIds` = 전 구역 · 정원 · 사용 중 · 원내 현황 구역별 · E2E #2 기준 「KOS 화면과 같음」 유지 · #35 더함 | §3.2 · §4.2 · §5.2 · §5.4 · §5.7 · §6.4 · §7.2 · §9 #2 · #35 · OQ-701 · OQ-758 |
| W1 | 이동 근거 「지정 의사 보존」이 리포트보다 셈 · `doctors` 실어 보냄은 HAR 밖 · 오류 이름이 공개 것 · 내부 4xx 본문 꼴 미확인 | 고침 — 근거를 K3 데모 확인(`doctors` 실어 보낸 모양으로 받음 · 남음)으로 바꾸고 HAR 은 `doctors` 없이 보냈다는 사실 적음 · OQ-714 문장 고침 · §4.4 오류 표(내부 `errorProperties` 먼저 · 공개 이름은 「공개」로 표시) · `KosError.errorProperties` 더함 | §4.4 · §8 이동 줄 · OQ-714 |
| W2 | 내부 API 가 정원을 거르는지 모름 · #12 전제 · K 에 정원 시험 없음 | 고침 — §5.4 「동시 조작의 정원」 줄(넘칠 수 있음 · 받아들임) · E2E #12 = 같은 고객 겹침 필수 + 정원 동시 조작 관찰 · OQ-760 열림. WP-KOS 는 이미 끝나 정원 시험을 E2E 로 옮김(데모 쓰기 허가 범위) | §4.4 · §5.4 · §9 #12 · OQ-760 |
| W3 | 「방 배정」 판정 두 가지 · 예약 사본에서 호출 기록 잇는 키 없음 | 고침 — §5.9 잇는 키(`reservation.kos_id` ↔ `visit.kos_id` · `tasks[].sequence` ↔ `procedure.kos_sequence` · visit 없음 = 호출 0 · `is_room_task` 같은 식) · §5.6 「제목 판정은 묶음 안에서만 · 수납 = SPEC-003 판정 · 사용 중 = type 무관」 한 줄 | §5.6 · §5.7 · §5.9 |
| W4 | 본문 기본값 다수가 §10 밖 | 고침 — **OQ-757 「작은 기본값 묶음」 한 줄**(16개 목록) · 본문 해당 자리에 `OQ-757` 표시. 「카드 수납 필요 빨간 점」은 U7(D-50)로 바뀌어 묶음에서 뺌 | §10 OQ-757 · §5.1 · §5.2 · §6.2 ~ §6.7 · §7.3 |
| W5 | §6.8 에 빠진 차이(빨간 점 · 그룹 없음 · 축 늘림 · 휴무 문구 · 오늘만 · 국기 title · 「n / N 입력」) | 고침 — 빨간 점 → U7 Badge(#27) · #23 ~ #29 더함 · 국기 title · 상세 머리 = 시안대로 국가 이름(#28) · 「n / N 입력」은 시안대로 되살림(#10 고침) | §6.3 · §6.6 · §6.8 |
| W6 | 경로 수 내역이 코드와 다름 · 시험 이름 | 고침 — 19 = HTTP 18(router 17 + health) + WS 1 → 34 = HTTP 33(router 32 + health) + WS 1 · `test_route_count_34` · SPEC-003 쪽 부채는 안 고침(적어 둠) | §7.6 · WORK-007 BE0 |
| W7 | 상담사 상태 · 사용 중이 오늘 사본에 기대는데 갱신 시점 없음 | 고침 — §4.2 「오늘 사본이 쓰이는 계산 전 오늘 캐시가 10초보다 오래면 오늘 조회 1번」 · 상세 · 접수 0단계에서 · E2E #20 | §4.2 · §5.6 · §5.7 · §5.8 · §7.3 · §9 #20 |
| W8 | DEC-006 D-38 근거 표기(SPEC-004 §5-1 ↔ A-14 · APNs) | 고침 — DEC-006 D-38 에 둘 다 적음(`_RESUME` §1 메모 인용) | DEC-006 D-38 |
| W9 | 헤더 「현황」 글자 = 예약 현황으로 시술 현황 동작이 바뀜 · 활성 판정 | 사용자 결정 U6(시술 현황 유지 · D-49)로 고침 — 항목 = 시술 → 예약 순 · 「현황」 글자 = 시술 현황 · 활성 = 두 경로 · 「바뀌는 것은 항목 하나 · 활성 판정 하나」 | §6.1 · §9 #1 · D-49 |
| (§5 빈칸 ③) | 「그룹 없음」 칸의 `columns[]` 모양 | 고침 — `groupId: null` 등 모양 한 줄 | §5.2 · §7.2 |

## 부록 D. 사용자 결정 U1 ~ U7 반영 (DEC-006 D-44 ~ D-50)

| U | 결정 | D | SPEC-005 반영 | 닫은 OQ |
|---|---|---|---|---|
| U1 | 두 구역 전부 · 정원 · 사용 중 · 원내 현황 구역별 · E2E #2 「KOS 화면과 같음」 유지 | D-44 | §3.2 `zone` · `capacities` · §4.2(구역 · 그룹 · 하루 · 다른 구역 방) · §5.2 칸 머리 · §5.4 `full` 구역별 · §5.5 구역 칸 · §5.7 · §5.8 · §6.4 구역 묶음 · §6.5 · §7.2 `zones` · `capacities` · `zoneId` · `rows` · §7.4 `zones` · §7.5 `zoneId` · §9 #2 · #3 · #10 · #20 · #27 · #35 | OQ-701(구역) · 세부 = OQ-758 |
| U2 | ~~[접수 완료] 켜짐 = KOS 신분 칸 다 채움~~ (2026-10-27 바뀜 → D-54 · 신분 조건 없음) · ccc 확인은 표시만 | D-45 | §5.6 새 접수 · 0단계 `get-visitor` · §5.12 ① 칸 표 · ② 표시만 · §5.14 · §6.6 신분 줄 · §6.8 #11 · #12 · §7.3 `identity.fields` · `complete` · §7.5 `identity_incomplete` · §9 #14 · #21 | OQ-719 · 세부 = OQ-759 |
| U3 | 카드 값만 | D-46 | §3.1(그대로 · 결정 표시) | OQ-703 |
| U4 | 부도 고객 접수 허용 | D-47 | §5.6 새 접수 `main ∈ {reserved, noshow}` · §5.14 · §6.8 #12 · §8 `recept` · §9 #33 | OQ-716 |
| U5 | 이어 하기 | D-48 | §5.6(F1 고친 규칙) · §7.3 · §9 #23 | OQ-718 |
| U6 | 헤더 「현황」 첫 화면 = 시술 현황 유지 | D-49 | §1.1 · §6.1 · §9 #1 | (OQ-752 는 경로 이름만 남김) |
| U7 | 예약 카드 「수납 필요」 표시 | D-50 | §5.9(카드 · 원내 · 정산 같은 값) · §6.3 Badge warning sm(시술 현황 카드와 같은 꼴) · §6.8 #27 · §9 #34 | — |

## 부록 E. WP-KOS 결과 반영 (`reservation-kos-probe-report.md` · 2026-10-26)

| WP-KOS | 판정 | SPEC-005 줄 | 닫은 OQ |
|---|---|---|---|
| K1 읽기 모양 | 같음(13 호출) · 문진 제출본만 다름 | §3.3 · §4.2 각 줄 「WP-KOS K1」 · 빈 칸 키 없음(§4.2 고객) · `desiredDischargeDateTimeUtc` 값 있을 때만(§3.3) | — |
| 주의 1 · 2 문진 제출본 최상위 · 없음 = 400 + `errorProperties` | 다름 → 고침 | §4.2 제출본 줄 · §4.4 `errorProperties` · §5.11 | — |
| K2 신규 생성 · 전 칸 예약 · `funnel` | 받음 · 모양 확정 | §5.5 · §8 등록 3줄 | OQ-753 · OQ-754 |
| K3 내부 이동 | 받음(`doctors` 실어 보냄 · 남음) | §5.4 · §8 이동 줄 · OQ-714 | — |
| K4 · K5 진행 경로 · 상담사 단독 | 받음 | §5.8 · §8 경로 · [실장 호출] 줄 | OQ-755 |
| K6 메모 | 받음 | §8 메모 줄 | — |
| K7 고객 수정 | 받음(날짜 꼴 · 권한 · 없던 키 안 보냄) | §8 고객 정보 줄 · §8 머리 아래 시각 줄 | OQ-739 |
| K8 바로 시술 · 주의 3 · 4 | 받음 · `room:{id:""}` · `change-tasks-room` 약 1초 | §3.2 `tasks` · §3.3 · §4.3 · §5.6 4 · 5 단계 · §8 접수 줄 | OQ-756 |
| K9 · K9b 귀가 · 거절 | 받음 · 400 `InvalidRequestException` | §4.4 표 · §5.10 · §8 귀가 줄 | OQ-728 |
| 주의 5 시각 밀리초 | 다름 → 고침 | §3.3 시각 읽기 · §8 시각 줄 | — |
| K10 남긴 데모 데이터 | 고객 1 · 일정 2 | §9 머리(#28 · #34 에 씀) · OQ-751 | — |
| 정원 초과 · 접수 뒤 실장 호출 | 시험 안 함 | §5.4 · §8 · §9 #12 · #25 · OQ-760 | — |

## 부록 F. E2E batch 1 반영표 (`reservation-e2e-feedback.md` #1 ~ #23 — 빠짐 0)

「처분」 = 피드백 표의 처분 칸(정해짐 = 사용자 결정 · DEC-006 D 번호 / 대기 = 사용자 지적을 고칠 것 · batch 1 BE · FE 몫). 구현 결과가 이 줄과 다르면 batch 1 보고로 맞춘다.

| # | 지적(짧게) | 처분 | SPEC-005 0.3.0 | §9 | OQ |
|---|---|---|---|---|---|
| 1 | 고객 리스트 안 뜸(조건 없이 목록 없음) | 대기 → 조건 없이 첫 페이지 | §6.5 · §7.4 | #8 | OQ-706 · OQ-761 |
| 2 | 셀렉터가 DS 가 아님(등록 · 상세 · 패널) | 대기 → 화면 전체 DS 컨트롤 | §6 머리 · §6.5 · §6.6 | #7 · #37 | OQ-762 |
| 3 | 칸에 3명이 나란히 안 들어감 | 대기 → 칸 폭 = 시안 식 `13 + mx·196 + (mx−1)·6` | §5.2 | #3 | OQ-763 |
| 4 | 시간축 06–22 · 운영 시간 표시 · 첫 렌더 지금 시각 | **정해짐 D-57** | §5.2 · §6.3 · §6.8 #2 · §7.2 | #3 · #39 | OQ-757 ⑦ ⑰ |
| 5 | 공지 영역 고정 비율 높이 | 대기 → 패널 높이 비례 · 자리 유지 · 안에서 스크롤 | §6.4 · §6.8 #32 | #38 | OQ-757 ⑱ |
| 6 | 날짜 글자 누르면 달력 | 대기 → DS 달력 | §6.2 | #37 | OQ-762 |
| 7 | 15분 칸 [+] 이 줄을 넘음 · 칸 머리 표기가 칸마다 다름 | 대기 → [+] · 미리보기 · 카드가 줄 경계 안 · 칸 머리 한 꼴 | §5.2 · §6.3 | #3 · #7 | OQ-758 · OQ-765 |
| 8 | 이름 같은 고객 경고 왜 넣나 · 동명이인 | **정해짐 D-56** | §5.5 · §6.5 · §6.8 #30 | #9 | — |
| 9 | 생년월일 기본 달력 | 대기 → DS 달력(#2 · #6 묶음) | §6 머리 · §6.5 | #7 · #37 | OQ-762 |
| 10 | 카드가 3줄짜리로 두꺼움 | 대기 → 카드 = 2줄 콤팩트 · 길이로 안 늘림 | §5.2 · §6.3 | #4 | OQ-765 |
| 11 | 「신분 확인」 글자 크기가 시안과 다름 | 대기 → 상세 제목류 시안 타이포 대조 | §5.12 ② · §6.6 | #14 | — |
| 12 | [접수 완료] 신분 칸 조건(주민등록번호) — KOS 에 제약 없음 | **정해짐 D-54** | §5.6 · §5.12 · §5.14 · §6.6 · §6.8 #12 · §7.3 · §7.5 | #14 · #21 · #33 | OQ-719 · OQ-759 |
| 13 | 상담 필요가 안 눌림 · 체크 ≠ 접수 때 상담 | **정해짐 D-51** | §3.2 · §5.6 · §5.8 · §5.14 · §6.6 · §6.8 #31 · §7.3 · §7.5 · §8 | #19 · #21 · #22 | OQ-723 |
| 14 | 접수 → 시술 대기 + 방이 오래 걸림 | 대기(측정) → back 즉시 응답 · front 낙관 표시 · 다시 읽기는 측정으로 | §5.6 · §6.6 | #22 | OQ-764 |
| 15 | 「내원 현황」 [+ 상담 추가]가 없음 | **정해짐 D-55** · KOS 확인 필요 | §3.2 · §5.8 · §5.14 · §6.6 · §6.8 #15 · §7.3 · §7.5 · §8 | #36 | OQ-750 · OQ-767 |
| 16 | 「수납 필요 N건이 남아…」 문구 빼 | 대기 → 문구 뺌 · 버튼 꺼짐 + 정산 상자만 | §5.10 · §6.6 | #28 | — |
| 17 | 수납했는데 반영 안 됨 · 웹소켓? | **정해짐 D-52** — 상세 열린 동안 5초 폴링 · 소켓 따로 검토 | §1.2 · §4.2 · §5.10 · §6.7 | #30 · #40 | OQ-704 · OQ-744 |
| 18 | 귀가 완료 뒤 모달이 안 닫힘 | 대기 → 성공하면 닫기 + 토스트 | §5.10 · §6.6 · §6.7 | #30 | — |
| 19 | 공지 위 「00:00」 빼 | 대기 → 게시 시각 뺌 | §6.4 · §6.8 #32 | #38 | — |
| 20 | 공지 높이 더 크게 반응형 | 대기 → #5 묶음 | §6.4 | #38 | OQ-757 ⑱ |
| 21 | 등록 「당일 지정 의사」 필요 없음 | **정해짐 D-53** | §5.5 · §6.5 · §6.8 #8 · §7.4 · §7.5 · §8 | #7 | — |
| 22 | 등록 「진행」(상담 필요 · 수면마취) 필요 없음 | **정해짐 D-53** | §5.5 · §6.5 · §6.8 #8 · §7.3 · §7.5 · §8 | #7 | — |
| 23 | SNS 종류가 드롭다운이 아님 | 대기 → KOS enum DS 드롭다운(등록 · 상세) | §5.5 · §6.5 · §7.4 · §7.5 | #41 | OQ-766 |

합계: 23건 → 정해짐 8(#4 · #8 · #12 · #13 · #15 · #17 · #21 · #22 = D-51 ~ D-57) · 대기 15(고칠 것). 빠진 # 0.
