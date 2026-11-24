# planner-fix-6 결과 보고 — KOS 사진 가져오기 (결정 C23) + 저장소 폴더 이름 `beforeAfter`(코디 추가)

## 상태: done

워크트리 `mediness-mediness/day-chart-photo-spec` · fix-5 미커밋 변경 위 · 미커밋. 바꾼 파일 = `products/day/20-spec/spec-002-procedure-board.md` · `20-spec/spec-000-data-model.md` · `40-architecture/deployment.md` · `10-decision.md` · `log.md`.

## 1. C23 — 사진 탭을 열 때 KOS 사진 가져오기

| 자리(spec-002) | 반영 |
|---|---|
| :45 머리글 | 「보충 6」 ⑰ |
| U-16 | 「DAY 행만 · KOS 웹 사진 안 보임」 두 bullet ~~취소선~~ + 사유 → 탭 열기 = 작업 넣기 · DAY 행만 그림 · 끝남 최대 3초 기다림 · 안 끝나면 한 번 더 읽기 · 순서 = `shot_at` |
| §3 API 사진 목록 행 | `poll` 없으면 작업 1회 넣기 + 3초 기다림 · `poll=1` = 다시 읽기(작업 안 넣음 · SPEC-006 R45 꼴) |
| 매트릭스 | 새 줄 셋 — 가져오기 실패 = 200 조용히 지금 DAY 목록 · 같은 방문 도는 중 = 새로 안 돎 · KOS 에서 지운 사진 = DAY 그대로 |
| §3 「KOS 사진」 :1115 | 목록 행 = 화면 요청은 안 부름 · 가져오기 작업이 1회 · 새 「가져오기(C23)」 행 = 원본 서명(`query` 없음) 1회 → GET · 「동기화 없음(C22)」 ~~취소선~~ → 10초 동기화 밖 · 탭 열 때만 |
| :1212 규칙 39 | ① ~~C22-기본값 ③ 문장~~ → DAY 행만 읽기 + 작업 넣기 · **새 ⑪** ⓐ 잠금(같은 방문 · `try_lock` 꼴 · 끝남/실패 표시) ⓑ KOS 1회 · 「DAY 에 없음」 = `external_ref` · DAY 가 올린 미반영 행(fileName uuid = DAY 행 id)은 `external_ref` 만 닮 · 두 묶음 밖 분류는 안 들임 ⓒ 저장 = 사진마다 짧은 커밋 · `source = kos` · `shot_at` = KOS 찍은 시각 · 5MB 안 걺 ⓓ 토큰 ⓔ 실패 조용히 · `event_log` `photo.import` ⓕ KOS 에서 지운 사진 = DAY 그대로 ⓖ 10초 동기화 · 차트 열기에는 안 넣음 ⓗ 앱 밖 |
| §4 | C23 결정 짝 행 · 「시술전후사진」 차이 행 보충 |
| DB 절 | `source` · `shot_at` · `photo.import` |
| OQ | **OQ-93 닫음(C23)** · 새 **OQ-96**(지운 사진 · 5MB · 분류 밖 · KOS 수정 맞출지) · **OQ-97**(다시 그리기 횟수 · 「최근 N초」 표시) · **OQ-98**(실패 · 가져오는 중 · 구분 표시) |

**작업 안 토큰 — 시스템 계정을 쓰지 않고 탭을 연 직원 토큰**(작업 인자 `staff_id` → 그 직원의 만료 안 된 `external_session` · 규칙 24 고르기 · 코드 `emr/outbox_delivery.py` `staff_token`). 근거: ① 사진 읽기 = 직원 토큰(OQ-92 기본값 · C10 과 같은 축 · KOS 웹이 직원 세션으로 부르는 경로) ② worker 도 직원 토큰을 고를 수 있다(쓰기 큐 선례) ③ 토큰이 없으면 다른 토큰으로 대신하지 않고 건너뜀(규칙 24). 작업 안 KOS 401 = 그 작업만 멈춤 · 세션은 끝내지 않음(기본값).

**다시 그리기** = 끝남 최대 3초 기다림(SPEC-006 R43 값) → 안 끝나면 지금 DAY 목록 + 몇 초 뒤 `poll=1` 1번 다시 읽기(기본값 · OQ-97).

**SPEC-000 `visit_photo`** — `source`(day · kos) · `shot_at` 칸 · `created_by_staff_id` 는 `kos` 면 비어도 됨(✓ 취소선) · `created_at` 설명 바로잡음 · 인덱스 (`visit_id`, `shot_at`) · 「DAY 에 없음」 판정 = `external_ref` 유일 제약. migration 필요(fix-5 와 같은 migration).

## 2. 코디 추가 — 저장소 폴더 이름 `beforeAfter`

- fix-5 · 6 의 `before-after/…` 키를 전부 **`beforeAfter/{병원 id}/…`** 로(앞 값은 ~~취소선~~): spec-002 머리글 ⑯ · 규칙 39(키 · ⑪ ⓒ) · §4 C22 행 · DB 절 / spec-000 머리글 · `visit_photo.file_key` / 10-decision · fix-5 log 행.
- **코드 예약 이름과 다르다**고 적음: 코드 `adapters/storage/blob.py:11` 주석 · 40-architecture/deployment.md 용도 표는 `before-after` — Azure dev 컨테이너의 실제 폴더는 `beforeAfter` → 코드 상수 · 용도 표를 맞춘다(spec-002 DB 절 · 규칙 39 · spec-000).
- `40-architecture/deployment.md` 용도 표 「고객 전후 사진」 행도 ~~`before-after` · 이름만 예약~~ → `beforeAfter` · 씀으로 고침(파일 저장소 정본이 어긋나지 않게 — products/day 안).
- 그대로 둔 것: `log.md` 2026-11-11 이력 두 줄(이력) · **DAY-SPEC-004 :425** 「전후 사진(`before-after`) 폴더와 섞지 않음」(채팅 SPEC 의 참조 한 줄 — 이번 범위 밖이라 손대지 않음 · 코디 판단 필요).

## 검증

`python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning** · `products/day/` 0건(전부 타 제품 — 무관). 바꾼 표 열 수 점검 통과.

## 미결 · 주의

- DAY-SPEC-004 :425 의 `before-after` 참조를 고칠지(코디).
- Delivery request 의 사진 계약(K4 · 「DAY 저장 0」)은 fix-5 · 6 과 어긋난다 — 다시 발행 때 고칠 것.

## 3. 코디 추가 2 — 결정 C18 고침(글만 비교)

- 규칙 31 ⓑ C18 문장(:1192 근처): 「마지막 이력의 글 ~~(+ 의사는 집도의)~~ 이 요청 `baseBody` ~~(+ `baseDoctorStaffId`)~~ 와 같으면」 → **글만 비교하고 집도의는 비교하지 않는다** + 날짜 · 사유(review-code-2 N1 — 동기화 이력 집도의는 「한 명일 때만」 규칙을 안 따라 다시 저장이 또 걸림 · 집도의 차이는 KOS 쪽 판정이 이미 봄).
- 같은 내용 맞춤: 개정 ㉘ 머리글 보충 3 ⑫ · 매트릭스 C18 줄. `log.md` 1행.
- 검증: lint `--strict` 다시 — 0 error · `products/day/` 0건.
- 이 추가는 worker_done 을 보낸 뒤 받아 반영했다(코디에게 터미널로 따로 알림).
