# WP-125 backend 착지 보고 — 예약 승인 실행 성공 → 회의 자동 등록 체인 (P0~P5)

- 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow` (브랜치 `meeting-room-workflow`, base `origin/dev`)
- 커밋·push·PR **하지 않음** — 워크트리에 변경만 남김
- 검증: **1회** 실행, 지목 범위 green (아래 §5)

---

## 1. P0 착수 실사 3건 — 결과

### ① 초대 확정 목록의 실제 필드 형태 — **이메일 배열이 맞다**

| 필드 | 형태 | 근거 |
|---|---|---|
| `payload.attendees` | **입력 축** = 발화 라벨(이름 문자열) 배열 | `app/schemas/action_runtime.py:500` |
| `payload.participants` | **결과 축** = 해소된 초대 **이메일** 배열(requester 자동 포함) | `:501`, `workflow/orgref/people.py` `ResolvedParticipants.participants` |
| `payload.participant_names` | `participants` 와 **같은 순서**의 표시용 이름 | `:502` |
| `payload.unmatched` | 미매칭 **라벨**(초대 제외 표기용) | `:503` |

⇒ 표시용 이름 축이 **함께 있다**(`participant_names`). 체인은 `participants`(이메일)를 역해소하고
`participant_names` 를 제외 사유 표기의 라벨로 쓴다. **계약 방향 무변경.**

### ② 정방향 해소가 실제로 읽는 사람 원천·이메일 컬럼 — ⚠ **SPEC-151 §7.2 문면과 어긋난다**

| | SPEC-151 §7.2 문면 | 실측 코드 (SoT) |
|---|---|---|
| 사람 원천 | `organization_member` | `organization_member` **로 좁히되** 행은 `users` 에서 읽는다 |
| 이름 | `organization_member.display_name` | **`users.name`** |
| 메일 | `organization_member.work_email` | **`users.email`** |

근거: `workflow/meeting/workflow.py` `MeetingDomain.org_members()` (변경 전 `:544-564`) —
`select(User.name, User.email).join(OrganizationMember, OrganizationMember.user_id == User.id)`.
즉 **조인 방향은 조직 명부이지만 이름·메일 컬럼은 계정 축**이다.

**처분** — WP §Domain/Schema 의 SPEC 환류 규율대로 **코드에서 정하지 않았다.**
`SPEC-151 §7.9.3` 이 「실제로 어느 컬럼을 읽는지는 **코드가 SoT** 이고 이 절은 발명하지 않고 그
술어를 부른다」라고 명시하므로, 역해소는 **현행 술어를 그대로 되쓴다**(`users.email` 소문자 정규화).
👉 **§7.2 문면 정정은 SPEC 환류 몫**이다 — 아래 §6 «코디네이터 판단 필요» 참조.

부수 확인: 회의 모달 셀렉터(`meeting_v2_participants`)는 `OrganizationDirectory` 를 쓰고
`display_name` 으로 표시한다. 즉 **표시 이름의 원천이 이미 두 축**이다(예약 = `users.name`,
회의 = `display_name`). 이번 체인은 그 축을 건드리지 않았다.

### ③ 「예약 건당 회의 최대 1」 보증 수단 — **부분 유니크 인덱스 + 생성 직전 조회 (2겹)**

| 안 | 동시 재진입(재시도 · reconcile 이 겹치는 순간) |
|---|---|
| ① 생성 직전 조회만 | ⚠ **막지 못한다** — 두 트랜잭션이 같은 순간 「없다」를 읽으면 둘 다 INSERT |
| ② 부분 유니크 인덱스 | **막는다** — 나중 INSERT 가 제약 위반 → 체인이 «회의 생성 실패» 로 받아 보상(조합표 C) |

**②를 골랐다** → **migration 1건이 범위에 들어왔다**(`0135_meeting_v2_reservation_unique.py`).
조회는 첫 겹으로 **남긴다**(정상 재진입에서 헛된 INSERT·헛된 보상을 만들지 않는다).
인덱스 조건 = `reservation_run_id IS NOT NULL AND deleted_at IS NULL` — 조회 술어
(`by_reservation_run`)와 **같은 조건**이라야 「조회는 없다는데 INSERT 는 걸리는」 자리가 안 생긴다.

⚠ **배포 주의** — 기존 데이터에 중복 `reservation_run_id` 가 있으면 migration 이 **멈춘다**(의도).
`reservation_run_id` 를 채우는 경로는 지금까지 모달 발 생성 하나이고 run 당 회의 하나라 구조상
중복이 없지만, 배포 창에서 다시 세는 것이 맞다.

---

## 2. 변경 파일

### 신규 (3)

| 파일 | 무엇 |
|---|---|
| `back/app/services/action_runtime/workflow/meeting/meeting_chain.py` | **체인 어댑터** — source 게이트 · 멱등 · 역해소 · 회의 저장 · 취소/변경 파급 · 카드 facts |
| `back/alembic/versions/0135_meeting_v2_reservation_unique.py` | 부분 유니크 인덱스 `uq_meeting_v2_reservation_run_live` (P0-③) |
| `back/tests/services/engine_v2/test_wp125_reservation_meeting_chain.py` | 계약 고정 테스트 34건 |

### 수정 (7)

| 파일 | 무엇 |
|---|---|
| `workflow/meeting/definitions.py` | `_execute_reserve` 체인 훅 + 보상 + **실행 축 기록을 체인 뒤로** · `_execute_cancel`/`_execute_update` 파급 훅 |
| `workflow/meeting/workflow.py` | `active_org_member_query()` 추출(정·역 공유 술어) + `MeetingDomain.members_for_emails()` |
| `workflow/meeting/const.py` | `MEETING_MODAL_SOURCE` 이관 · 체인 fact/문안/감사 event_type |
| `app/services/meeting_v2_service.py` | 예약 발 진입 seam `create_from_reservation()` 신설 + 상수 재export |
| `app/repositories/meeting_v2_repo.py` | `by_reservation_run` · `unlink_reservation` · `soft_delete` · `reschedule` |
| `app/models/meeting_v2.py` | 주석만(인덱스 소재 명시). 스키마 변경 0 |
| `tests/.../test_meeting_definitions.py` | `_action()` 기본 `source` = 모달 발로 고정 + 사유 주석 |

**allowed_paths 준수** — 전부 `back/` 안. `mcp/`·`docker-compose*.yml` 무변경.

---

## 3. 구현 요약 (Phase 별)

### P1 — 발동 · 역해소 · 한 트랜잭션 저장

- **source 게이트** — `chain.chain_applies(source)` **한 함수**. 발동(§7.9.1)과 파급 가드(§7.9.5)가
  같은 것을 부른다. 값의 정의는 `const.MEETING_MODAL_SOURCE` **한 자리**(회의 서비스는 그 이름을 되쓴다).
- **멱등** — `by_reservation_run(run_id)` 로 이미 연결된 회의가 있으면 `skipped=already_linked`.
- **역해소** — `members_for_emails()` 가 **정방향과 같은 select**(`active_org_member_query`)를 돈다.
  거기에 회의 도메인의 `invitable_member_ids` 를 **교집합**으로 얹어 계정 미연결자를 제외한다
  (회의 판정을 예약이 우회하지 않는다).
- **제외 + 표기** — 3사유(정방향 미매칭 / 조직 구성원 미해소 / 계정 미연결)를 카드 facts
  `회의 참석 제외` 한 축에 사유와 함께 싣는다. **회의 생성을 실패시키지 않는다.**
- **host 미해소만 생성 실패** — `action.requester_member_id` 가 없으면 보상을 탄다.
- **파생 매핑** — 제목·일시는 plan 그대로 · host = requester · 참석자는 host 제외 · 공개 범위
  `private` · `product_tags=[]` · 상태 회의 도메인 기본(`waiting`). `headcount` 미저장.
- **슬롯 검증 미적용** — seam 이 `MeetingV2CreateRequest` 를 지나지 않는다. `:15`·`:40` 그대로 앉는다.
- **한 트랜잭션** — `session.begin_nested()`(SAVEPOINT). ⚠ 세션 전체 rollback 을 쓰지 않은 이유는
  바깥 트랜잭션에 **이번 외부 write 의 감사·실행 원장**이 들어 있기 때문(그것까지 지우면 일어난 일이
  원장에서 사라진다).

### P2 — 보상 원자성 · 실행 축 기록 시점

- **`complete_execution` 을 체인 뒤로 옮겼다** — 외부 예약 성공 «시점» 에 «성공» 을 적지 않는다.
  실행 축의 값은 `_close_reserve_chain` 에서 **한 번** 정해진다.
- **보상** = `room.cancel` **bound tool** 경유(`_run_write_step` 재사용 — gateway 직접 호출 0).
  대상은 **실행 결과의 external_id 하나** — 조건 재조회 0. **재시도 없음.**
- **C** — 보상 성공 → `fail_execution(retryable=False)` = 실행 축 실패(종료) · 카드 최종 실패.
  판단 축은 **승인**에 머문다(반려 아님).
- **D** — 보상 실패 → `complete_execution` 로 실행 축 **성공 유지** + 회의 미등록 사실 별도 표기.
  관측 로그 `log.error("WP-125 조합표 D … action_id/external_id/meeting_error/compensation_error")`
  — **OQ-9 판단의 입력**.
- **A 무변경** — 선점·대안 0 경로는 손대지 않았다(WP-119 의 「실패(종료) + 합법 edge」 수리 보존).

### P3 — 수정·취소 파급

- **가드 2겹** — `target_meeting()`: ① `by_reservation_run` 로 연결 확인 → ② `chain_applies(origin.source)`.
  판정 대상은 **amendment 카드가 아니라 원 예약 카드의 `source`**(amendment 는 항상 `api` 로 생성됨).
- **취소** — `waiting` → `soft_delete` / `live·paused·ended` → `unlink_reservation`(연결만 끊기).
- **변경** — `waiting` → `reschedule`(날짜·시작·종료) / 시작된 회의 → **그대로**. 회의실·참석자 무변경.
- **파급 실패는 예약을 되돌리지 않는다** — try/except → 감사 `reservation_meeting_sync_failed` +
  카드 fact `회의 반영`. 여기에 보상을 만들지 않았다.

### P4 — 표면

- 완료 카드 `review_surface.facts` 에 `등록된 회의`(제목 + 회의 id) 1건. 미등록이면 `회의 미등록` +
  사유(C = 「예약도 회의도 만들어지지 않았다」 / D = 「방은 잡혔지만…」). 파급 결과는 `회의 반영`.
- **카드 명령 증가 0 · state enum 0 · choice kind 0 · REQUIRED_FACTS 0** (테스트로 고정).
- **FE 몫 판정 = FE diff 0.** `front/components/chat/CardFacts.tsx` 가 `{label, value}` 배열을
  **generic 하게** 렌더한다(`facts.map` — 라벨 화이트리스트 없음). 새 컴포넌트 불필요.
- ⚠ **채팅 완료 안내는 별도로 만들지 않았다** — §6 «주의점» 참조.

### P5 — 테스트 34건

조합표 A~D · 실행 축 1회 기록(«성공 → 실패» 전이 부재) · source 게이트(이중 생성 0) ·
멱등 재진입 · P0-③ 인덱스(중복 거절 / soft-deleted 는 재등록 허용) · 파생값 전수 · 슬롯 밖 시각 ·
역해소 4경계 · 술어 이중화 금지(AST 대신 소스 검사) · 동기화 8분기(변경/취소 × 대기/시작됨 ·
연결 없는 run × 2 · **모달 발 음성 단언 × 2**) · 파급 실패 · 표면 5건.

---

## 4. 계약 준수 체크

| 계약 | 상태 |
|---|---|
| P0 실사 3건 선행 | ✅ (§1) |
| 발동·파급 판정 = 같은 source 축 하나 | ✅ `chain.chain_applies` 단일 · 값 정의 `const` 단일 (테스트 고정) |
| P3 진입 가드 2겹(연결 + source) | ✅ `target_meeting()` · 모달 발 음성 단언 2건 |
| 실행 축 기록은 체인이 끝난 뒤 | ✅ `_close_reserve_chain` · `terminal` 길이 1 단언 |
| 보상은 bound tool 경유 · gateway 직접 호출 금지 | ✅ `_bound_tool("room.cancel")` + `_run_write_step` |
| 보상 대상 = 그 external_id 하나 (조건 재조회 0) | ✅ 테스트 `cancel.calls == [{"external_id": "ext-1"}]` |
| 새 endpoint·leaf·state enum·카드 명령·DELETE 표면 0 | ✅ |
| 모달 발 경로 diff 0 | ✅ 제거된 줄은 상수 정의 1줄(같은 문자열로 재export). 소비처 테스트 32건 green |
| migration = 0 또는 인덱스 1건 | ✅ 인덱스 1건 (P0-③ 결과) |
| spec 레포 무수정 | ✅ read-only 참조만 |
| 커밋·push·PR 금지 | ✅ |

---

## 5. 검증 결과 (1회)

```
uv run pytest tests/services/engine_v2/test_wp125_reservation_meeting_chain.py \
              tests/services/engine_v2/test_meeting_definitions.py \
              tests/services/engine_v2/test_meeting_workflow.py \
              tests/services/engine_v2/test_meeting_surface.py -q
→ 157 passed in 77.18s

uv run pytest tests/api/test_meetings_v2_room_reservation.py \
              tests/api/test_meetings_v2_rest.py \
              tests/api/test_meetings_v2_list_room_badge.py -q      # 모달 발 무영향 확인
→ 32 passed in 24.13s

uv run ruff check <변경 파일 전부>
→ 신규 error 0 (기존 `UP042` 2건은 `models/meeting_v2.py` 의 **선재** 지적 — 무관)
```

- **기존 실패 없음.** 전체 스위트는 사용자 방침대로 **돌리지 않았다.**
- 테스트 DB 는 pytest 플러그인(`tests/test_infra/plugin.py:97`)이 워커별 일회용 DB 를
  `alembic upgrade head` 로 올린다 — **0135 가 그 경로로 적용되어 green** 임을 확인했다.

---

## 6. ⚠ 코디네이터 판단 필요 — SPEC 환류 1건 (P0-②)

**SPEC-151 §7.2 의 「참석자 원천 = 조직 명부(이름 = `display_name`, 메일 = `work_email`)」 문면이
코드와 어긋난다.** 코드는 조직 명부로 **범위만** 좁히고 이름·메일은 **계정(`users.name`/`users.email`)**
에서 읽는다.

- 이 WP 는 §7.9.3 의 「코드가 SoT · 발명 금지」에 따라 **그 술어를 그대로 되썼고**, 코드에서
  임의로 정하지 않았다. 기능적으로 정·역이 어긋나지 않는다(같은 select 를 공유).
- **필요한 것은 SPEC 문면 정정 PR** 이다(문서 레포 · planning 몫). 방향 후보 둘:
  - (a) §7.2 문면을 실측대로 고친다 — 「조직 명부로 범위를 정하고 이름·메일은 계정 축에서 읽는다」
  - (b) 코드를 문면대로 `display_name`/`work_email` 로 옮긴다 — ⚠ **이건 별건**이다.
    정방향 해소·THE CONNECT 조인·카드 표기가 전부 걸리고 **이 WP 범위 밖**이다.
- 부수 사실: 회의 모달 셀렉터는 이미 `display_name` 을 쓴다 ⇒ **표시 이름 원천이 두 축**이다.
  (b) 를 고르면 그 어긋남도 함께 정리된다.

---

## 7. 미결·주의점

1. **채팅 완료 안내 「한 줄」을 신설하지 않았다** (§7.9.6). BE 에 예약 완료용 **고정 문자열 템플릿이
   존재하지 않는다** — 채팅은 카드를 `{action_id}` **참조로만** 남기고 상태·facts·버튼을 항상 서버에서
   되읽는다(`front/components/landing-chat/ApprovalCard.tsx`). 승인 자체도 REST 카드 경로라 채팅 턴이
   아니다. ⇒ 회의 등록 사실은 **카드 facts 로 채팅에 그대로 도달**하며, 별도 문구 자리를 만드는 것은
   「새 표면 0」 계약과 충돌한다. **새 안내 문자열이 필요하다는 판단이면 별건**으로 발주 필요.
2. **Pre-deploy Check 는 수행하지 않았다**(WP §Pre-deploy Check) — THE CONNECT 취소 API 실측,
   첫 실사용 회의 확인, 관측 로그 조회 경로 확인은 dev 환경 작업이다. ⚠ 특히 **취소 API 가 막히면
   조합표 C 가 전부 D 가 된다.**
3. **migration 배포 시 중복 검사** — §1-③ 참조. 위반이 있으면 멈추는 것이 의도다.
4. **보상 tool 미바인딩도 D 행으로 처리**했다(`MSG_MEETING_TOOL_UNBOUND`). 되돌릴 수단이 없으므로
   「보상 실패」와 같은 결말이 맞다고 판단했다 — 계약에 명시적 언급이 없는 자리라 표기해 둔다.
5. **동시 재진입의 실제 위험도는 관측이 없다**(WP §Open Issues 그대로). P0-③ 선택이 과한지는
   배포 후 확인 축에서 다시 볼 일이다.
6. **`review_surface` 를 실행 tail 에서 재대입**한다(facts 추가). 승인 지문 대조
   (`_assert_approved_content`)는 **재시도 경로**에서만 무는데, 체인이 facts 를 붙이는 것은 종결
   상태(C = FAILED_TERMINAL / D·B = DONE) 직전이라 재시도 창이 없다. 다만 향후 「체인 실패를
   retryable 로」 바꾸면 이 자리가 문제가 된다 — 그때 지문 축을 함께 봐야 한다.
