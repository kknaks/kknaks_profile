# 리뷰 리포트 — day-reservation / doc 2차 (2026-11-23)

- 대상: 워크트리 `mediness-mediness/day-reservation-spec` 미커밋 변경(planner 고침 1 뒤) — `spec-006-reservation-board.md`(420줄) · `20-spec.md` · `30-work.md` · `10-decision.md` · `log.md`
- 기준: 결정 파일(갱신 — R1 보충 · 「데이터」 머리 · R17 ~ R20) · 1차 리포트 `review-doc-1-report.md` · 고침 지시서 `planner-fix-1-instructions.md` · CENTURION_DAY `origin/dev` `5ece25ea` · cc `origin/main`
- 코디 정정 반영: 「조회 때 KOS 호출 · DB 최신화」는 R17 이다. FAIL 로 보지 않는다.
- 줄 번호 `S6:L` = spec-006 줄. 리포 파일은 고치지 않았다.

## 판정: FAIL

1차의 F-1 · W-1 ~ W-9 는 모두 닫혔다(W-4 는 일부만). R17 ~ R20 은 본문 전체에 대체로 일관되게 반영됐다.
그런데 새 「조회 흐름」에 **새 FAIL 1건**이 있다. 흐름에 적힌 경로대로만 구현하면, 다른 날짜의 방문에 **예약 그룹이 비어** 열에 놓을 수 없다. R20 은 그런 방문이 없다는 전제로 따로 처리하지 않기로 했으니, 카드가 조용히 사라진다.

### lint

`python3 scripts/lint-pipeline.py --strict` → **exit 0 · 0 error · 263 warning** · `products/day/` 범위 0건. 263건은 다른 제품의 `doc_no` · frontmatter 건으로 이번 변경과 **무관**하다. `doc_no` 중복은 없다.

---

## FAIL

### F2-1. 조회 흐름이 `visit.reservation_group_id` 를 채우는 단계를 빠뜨렸다

- **어디**: S6:L265(흐름 3단계 = `fetch_schedules` → `apply_schedules` 만) ↔ S6:L234(같은 SPEC 의 칸 표는 `reservation_group_id` = 「KOS 키 보충(`mapper_kos_keys.py:286`)」이라고 바르게 적었다) · S6:L130 · L311 · L397(R20 — 그룹 없는 방문은 없다 · 따로 처리하지 않음)
- **코드 사실**:
  - `apply_schedules` 는 `visit.reservation_group_id` 를 쓰지 않는다. `emr/sync_schedules.py:506` 의 `reservation_group_id` 는 **`visit_occupied_resource` 행**의 칸이다(`:495-510` `VISITOCCUPIEDRESOURCE.write`). 방문 행에 쓰는 칸(`:318-342`)에는 그룹이 없다.
  - `visit.reservation_group_id` 는 KOS 키 보충만 채운다. `emr/kos/mapper_kos_keys.py:281-286` `visit_extra` → `extra.ref("reservation_group_id", …, "reservationGroupId", reservation)`.
  - 이 보충은 **회차 밖**에서 돈다. `tasks/emr.py:111` `await _kos_keys("schedules", hospital, result)`가 `run_schedules` 가 끝난 뒤, 태스크 안에서 따로 부른다(`:71-80` 「회차가 끝난 뒤 그 응답의 더할 칸을 따로 반영」).
- **결과**: 오늘이 아닌 날짜를 볼 때 S6:L265 대로 `fetch_schedules` → `apply_schedules` 만 부르면 이렇게 된다. 처음 들어온 방문은 `reservation_group_id` = null 이다. 이미 있던 방문은 예전 값 그대로다. 그러면 R9 의 열 원천이 비어 카드를 놓을 열이 없다. R20 이 별도 처리를 없앴으므로 카드는 **조용히 빠진다**. 「그룹 없는 방문은 없다」는 KOS 원본에 대한 사실이다. 이 흐름에서 DAY 사본까지 그렇다는 보장은 없다.
- **고칠 것**: 흐름 3단계에 KOS 키 보충을 넣는다. 「그 응답의 `kos_keys` 를 `emr_kos_keys.apply_isolated`(지금 `tasks/emr.py:71-80` 과 같은 것)로 반영한 **뒤** DB 를 읽는다」. 아니면 「기존 일정 동기화 경로」의 범위가 `run_schedules` + 태스크 뒤 보충(`_kos_keys`)까지라고 밝힌다. 순서도 정해야 한다. 지금 오늘 회차는 보충을 판 반영 · 신호가 끝난 뒤에 따로, 실패해도 로그만 남기고 돈다. 화면은 보충이 끝나야 그룹을 안다. 보충이 실패하면 그 카드들을 어떻게 보일지는 OQ-R23 에 한 줄로 넣는다.
- 같은 이유로 S6:L276 의 사실 표에 「KOS 키 보충은 회차 밖 태스크 단계(`tasks/emr.py:111`)」 한 줄을 넣는다.

---

## WARN

### W2-1. OQ-R22 기본안 ⓐ(오늘은 가져오지 않음)가 본문 문장과 범위가 어긋난다
- 본문은 날짜 구분 없이 「그 날짜 최신화 뒤 전체 페이지」라고 쓴다(S6:L250 · L251 · L80 · L299 · Rule 7 L340). R17 문장도 「어떤 날짜를 보면」이다. 그런데 OQ-R22 기본안 ⓐ는 오늘을 뺀다(S6:L403). 1차 F-1 과 같은 꼴이지만, 10초 회차가 오늘을 덮으므로 동작 차이는 작다 → WARN.
- 고칠 것: 본문의 「그 날짜 최신화」에 「(오늘은 OQ-R22)」 표시를 붙인다. 기본안 ⓐ가 R17 문장을 좁히는 것이니 사용자 확인 대상이라고 OQ 에 밝힌다.

### W2-2. 갱신 방식(OQ-R10)과 요청 때 가져오기가 맞물리는 것을 적지 않았다
- OQ-R10 기본안 ⓑ = 조각 폴링 10초(S6:L396). R17 대로면 다른 날짜 화면을 열어 둔 PC 마다 **10초에 한 번 KOS 하루 일정 조회**가 생긴다. 운영 동기화에는 호출 간격 제한이 없다(S6:L283 · `emr/pacing.py:1-4` 「운영 동기화에는 붙이지 않는다」). 그래서 KOS 부하 · 기기 제한과 맞물리는데 OQ-R10 · R22 · R24 어디에도 적혀 있지 않다.
- 고칠 것: OQ-R10 에 「폴링이 R17 요청 때 가져오기를 다시 부르는지(→ OQ-R22 ⓒ 캐시와 함께)」 한 줄을 넣는다. R18(선동기화 안 함)과는 부딪히지 않는다.

### W2-3. 사실 표 한 줄이 코드와 조금 다르다
- S6:L279 「KOS 오류 · 형식 오류 = `error`(예외 이름만 남김)」. 실제 `emr_sync.py:170-174` 는 `EmrError` 면 **메시지**(`str(exc)`)를, 그 밖(`ValueError` · `OSError`)이면 예외 이름을 남긴다. `error_kind` 는 늘 예외 이름이다.
- 고칠 것: 「`error` — KOS 오류는 메시지 · 그 밖은 예외 이름 · `error_kind` = 예외 이름」으로 고친다.

### W2-4. 1차 W-4 의 OQ-R07 쪽이 빠졌다
- 병원 운영 시간표 · 휴무 사실은 OQ-R08 에만 들어갔다(S6:L394). 1차 W-4 는 OQ-R07(왼쪽 시간 칸 회색 기준 · S6:L412)에도 넣으라고 했다. 시안의 단일 `OPEN`(L1489)에 더 가까운 후보가 병원 운영 시간표다.
- 고칠 것: OQ-R07 기본안 옆에 「후보: `hospital_operation_timetable`(동기화 있음 — OQ-R08 사실 참고)」을 덧붙인다.

### W2-5. 남은 옛 표현
- S6:L181 「(이 SPEC 은 새 동기화 회차를 넣지 않는다)」. 개정 ① 뒤에는 요청 때 일정 경로를 부르므로 읽는 사람이 헷갈린다. → 「공지 동기화는 넣지 않는다(R17 흐름도 공지는 안 가져옴)」로 범위를 좁힌다.
- S6:L372 cc 와 다른 곳: cc 는 날짜를 볼 때 **정원 · 공지 · (오늘이면) 금액도** 다시 읽는다(cc `kos/reservation_sync.py:4` · `api/reservations.py:66-67`). DAY 는 일정만이다(S6:L270). 「다른 곳」에 이 차이도 한 줄 넣는다.

---

## 1차 지적 행별 확인

| 1차 | 고친 곳 | 판정 |
|---|---|---|
| F-1 OQ-R02 ↔ 본문 | R17 · R18 로 닫음 — S6:L80 · L58 · L242 · L250 ~ 251 · §3 「조회 흐름」 L259 ~ 285 · L299 · OQ-R02 닫음 L389 · L418 | **닫힘**(흐름 안의 새 구멍은 F2-1) |
| W-1 카드 높이 출처 | S6:L131 cc `spanOf` 표시 + 시안과 다름 · §4 L366 | 닫힘 |
| W-2 그룹 없는 방문 | R20 — S6:L130 · L311 · L397 · L419 | 닫힘(단, F2-1 로 다시 생길 길이 있음) |
| W-3 동기화 멈춤 표시 | R19 → OQ-R21 · S6:L321 · L402 · `record_sync` 사실 | 닫힘 |
| W-4 병원 시간표 · 휴무 | OQ-R08 L394 에만 | 일부 — W2-4 |
| W-5 Spec Coverage 값 | `30-work.md` `proposed` | 닫힘 |
| W-6 필터 유지 문장 | S6:L175 | 닫힘 |
| W-7 OQ-R06 cc 문구 | S6:L393 | 닫힘 |
| W-8 기획안 「탭 옆 수납 필요 수」 | S6:L355 | 닫힘 |
| W-9 결번 · O2 근거 · `released_at` null | S6:L73 · L98 · L391 ⓔ | 닫힘 |
| OQ-R16 방식 차이 | S6:L401 | 닫힘 |

## R17 ~ R20 · R1 보충 — 본문 일관성

| 자리 | 판정 |
|---|---|
| 머리 · 개정 노트 L24 · L30 · L32 | 맞음 — 옛 문장은 취소선으로 남겼다 |
| Business Requirement L48 · L49(KOS 읽기만 · DB 최신화 · R1 보충) | 맞음 |
| 범위 표 L58 · RV-07 · 08 L80 | 맞음 |
| U-3 회색(지난 날 / 다음 날) L119 · 케이스 L299 | 맞음 |
| U-6 필터 유지 L175 | 맞음 |
| U-7 공지 L183(R17 흐름은 공지를 안 가져옴 → 늘 비어 보임) | 맞음. L181 표현은 W2-5 |
| 칸 표 L234 ~ 238 · L242 | 맞음 |
| API L250 ~ 251 | 맞음(오늘 범위는 W2-1) |
| 조회 흐름 L259 ~ 285 | 경로 누락 F2-1 |
| 케이스 L300 · L301 · L311 · L321 | 맞음 |
| Rule 7 L340 · cc 비교 L372 | 맞음(L372 보강 W2-5) |
| `20-spec.md` Scope In · `10-decision.md` 현재 결론 · `log.md` spec-change 행 | 맞음. 새 ESC 없음 — 맞음(팀 권한 안 OQ) |
| 취소선 처리한 옛 문장이 살아 있는 곳 | 그대로 살아 있는 「조회 부작용 없음」 · 「KOS 호출 없음」 문장은 없다. L181 만 모호하다(W2-5) |

## 「조회 흐름」 코드 사실 확인 (`origin/dev` 직접)

| SPEC 줄 | 주장 | 코드 | 판정 |
|---|---|---|---|
| L264 | 창 계산 = `today_window` | `services/emr_sync.py:123-127` | 맞음 |
| L265 | `fetch_schedules(start, end)` | `emr_sync.py:225` · `emr/kos/__init__.py:170-185`(`startDateTimeUtc` · `endDateTimeUtc`) | 맞음 |
| L265 | `apply_schedules` · 창 안에서 사라진 것 `deleted_at` | `emr_sync.py:230` · `emr/sync_schedules.py:205` · `:391-400`(`in_window` · `within=`) | 맞음. 단, 그룹 칸은 쓰지 않는다 → F2-1 |
| L276 | 창이 `today_window` 로 고정 · 날짜 인자 없음 | `emr_sync.py:211` · `:224` | 맞음 |
| L277 | 잠금 키 · `skipped_locked` · 기다리지 않음 | `emr_sync.py:43` · `:97-98` · `:148-155` | 맞음 |
| L278 | 상한 60 − 5 = 55초 · 넘기면 `timeout` | `emr_sync.py:102-120` · `:156-169` · `backend/common/config.py:124`(TTL 60) · `:127`(여유 5) | 맞음 |
| L279 | 오류 = `error` · 예외 이름만 | `emr_sync.py:170-174` | 조금 다름 → W2-3 |
| L280 | 회차 안 `outbox.confirm` · 방 배정 잇기 | `emr_sync.py:238-242` | 맞음 |
| L281 | `record_sync` | `emr_sync.py:266-275` | 맞음 |
| L282 | 오늘 구매 · 시술권 · 카드 = 별도 태스크 | `tasks/emr.py:98-110` | 맞음 |
| L283 | `KosPacer` 는 백필 전용 | `emr/pacing.py:1-4` · `emr/factory.py:71` `build_backfill_adapter` | 맞음 |
| L394 | 병원 운영 시간표 · 휴무 동기화 | `emr/sync_kos_keys_hospital.py:110-165` | 맞음 |
| L131 | cc `spanOf` | cc `ScheduleTable.tsx:35-37` | 맞음 |
| L372 · L403 | cc `KOS_RESV_CACHE_SEC` · `sync.lastError` | cc `api/reservations.py:66-68` | 맞음 |
| (빠진 사실) | KOS 키 보충은 회차 뒤 따로 | `tasks/emr.py:71-80` · `:111` · `mapper_kos_keys.py:286` | **F2-1** |

## 새 OQ-R21 ~ R25 — 본문 섞임 · R18 충돌

| OQ | 기본안이 본문에 결정처럼 섞였나 | R18(선동기화 안 함)과 충돌 | 판정 |
|---|---|---|---|
| R21 동기화 멈춤 표시 | 아니다 — 본문 L321 「이번 판 표시 없음」 = R19 그대로 | 없음 | PASS |
| R22 오늘도 가져올지 | 본문은 「모든 날짜 최신화」, 기본안은 「오늘 빼기」 — 방향이 반대 | 없음(ⓒ 캐시는 선동기화가 아니다) | WARN W2-1 |
| R23 실패 · 느림 | 아니다 — 케이스 L300 은 (OQ-R23) + 지금 코드 사실만 | 없음 | PASS |
| R24 동시 요청 · 잠금 · 쓰기 큐 | 아니다 — 케이스 L301 은 (OQ-R24) + 사실만. 기본안 「날짜를 넣은 잠금」은 새 Redis 키 설계라 테이블 · migration 금지와는 무관하다 | 없음 | PASS |
| R25 그 날짜 구매 | 아니다 — 칸 표 L238 은 「= OQ-R25」 | 없음 | PASS. 메모: 기본안대로면 지난 날 귀가 대기 카드의 「수납 필요」는 백필이 있을 때만 맞는다. 귀가 대기가 지난 날에 남는 경우는 드물어 영향은 작다 |

## 직원이 실물에서 만날 자리

- (F2-1) 내일이나 어제를 처음 열면 예약이 표에 안 보이거나 일부만 보인다. 오늘 회차의 보충이 돌기 전 오늘 첫 방문도 잠깐 같은 일을 겪을 수 있다.
- (W2-2) 다른 날짜를 열어 둔 PC 가 늘면 KOS 조회가 늘어난다(간격 제한 없음).
- 같은 병원에서 오늘 10초 회차와 같은 잠금 키를 쓰면 서로 `skipped_locked` 를 내 화면 최신화가 빠질 수 있다 — 이건 OQ-R24 에 적혀 있다.

## 참고(무관)

- lint WARN 263건 = 다른 제품. 이번 변경과 무관.
- `visit.reservation_group_id` ↔ `visit_occupied_resource` 가 같은지(DAY-SPEC-000 OQ-4A-7)는 그대로 열려 있다. SPEC-006 은 R9 대로 앞의 칸을 쓴다(L397).
