# WORK-001 WP1 결과 보고 — cc/back 뼈대 · 시드 · 상태 · API · SSE · 로그인

## 상태: done

## 수행 — 파일·모듈 목록

워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype`(브랜치 `kknaksss/sts-prototype`). 커밋 없음.

- **`sts/` 삭제**(D-30) — `git rm` 으로 `sts/back/.gitkeep` · `sts/front/.gitkeep` 삭제가 index 에 올라가 있다
- `cc/back/` 새로 만듦(`.gitkeep` 삭제)
  - `pyproject.toml` · `uv.lock` · `.python-version`(3.12) · `.env.example`(SPEC §8 키 5개, `SONIOX_API_KEY=` 포함) · `.gitignore`(`.env` · `data/`) · `README.md`(설치 · 시드 · 실행 · 포트 8600)
  - `app/main.py` — FastAPI, CORS 는 `CC_FRONT_ORIGIN` 하나만, 오류는 `{error:{code,message}}` + 4xx(검증 오류도 400)
  - `app/config.py` — env(.env) 설정. `CC_DB_PATH` 상대경로는 `cc/back` 기준, 시드는 같은 폴더 `seed.json`
  - `app/api/` — router: `board` · `staff`(로그인 · 첫 화면 · 진료 시작/완료) · `patients` · `admin`(reset) · `events`(SSE)
  - `app/service/` — `board_service`(조작 · undo · version · reset · snapshot) · `staff_service` · `patient_service` · `memo_parse`(양식 파싱) · `events`(SSE 버스) · `snapshot`(시각 ↔ 오프셋)
  - `app/domain/` — `board.py`(시안 `custIn` · `presentIn` · `waitLabel` · `statusOf` · `commit` · `assign` · `complete` · `removeStaff` · `place` · `checkIn` 이식) · `rooms.py`(시안 `LAYOUT` · `capOf` · `isSleep` · `roomName` + 방 대응표 상수) · `errors.py`
  - `app/repository/` — SQLite(`reference` · `customer` · `staff` · `resv` · `history` · `meta`). ORM 없음, 요청 하나 = 트랜잭션 하나
  - `app/seed/` — `__main__.py`(CLI `build` · `save`) · `build.py`(재구성) · `names.py`(가짜 이름 · 메모 치환) · `capture.py`(캡처 읽기)
  - `tests/` — 5개 파일 20개 시험
- `cc/back/data/seed.json` · `cc.db` — `seed build --date 2026-10-09 --at 14:45` 로 한 번 만들어 둠(gitignore). front 가 바로 띄울 수 있다

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `CC_CAPTURE_DIR=<캡처> uv run pytest` (cc/back) | **20 passed** (1.0s) |
| `uv run ruff check .` | **All checks passed** |
| `uv run python -m app.seed build --date 2026-10-09 --at 14:45` | 일정 27 · 지금 내원 5 · 귀가 6 · 직원 17(의사 4 · 상담사 3 · 코디 10) · 완료 기록 30 |
| 실제 서버(임시 포트 18611, 끝나고 그 프로세스만 종료) | `GET /api/events` 연결 → `version 2` → `POST assign` → `version 3` 이벤트 수신. CORS: `localhost:3600` 허용 · 다른 출처 헤더 없음 |
| 기능 폴더 밖 import | 없음(`app.*` · 표준 · 서드파티만) |

브리프 §8 최소 항목 대조:
- 시드 build 10-09 — `test_build_1009`
- **이름 대조 0건** — `test_no_real_customer_names_in_any_response`: 캡처 `visitor.name` 177건(고유 173) + `phoneticName` + 상담 `visitor.name` + 메모 전체의 「이름 :」 값 = **331개 이름**을 응답 전체(board · staff · 모든 직원 home · 27명 환자 상세)와 원문 · 정규화(공백 · 쉼표 · 하이픈 · 점 · 접두 제거, 대문자) 둘 다로 대조 → 고객 자리 0건. 걸리는 3개는 **직원 이름**(강도윤 · 송지호 = 시술 담당, 차예린 = 예약 담당)이 다른 날 고객 이름과 같은 경우라 D-09 · design-r2 이슈 3 대로 예외 처리(시험에서 직원 · 유입처 이름은 대조 제외). 전화 · 생년월일 · 차트번호 키 · 값 0건(`test_no_phone_chart_birth_in_responses`)
- assign · complete · place · checkIn(예약 + 현장) · undo · 진료 시작/완료 각 1개 이상 — `test_api.py`
- reset 이 시드로 돌아감(경과도 같게) · `seed save` 뒤 reset 이 저장 상태로 — `test_reset_returns_to_seed` · `test_seed_save_then_reset`
- 환자 상세 ⚠ 주의가 오더 · 상담 사본 양쪽에서 모임 — `test_cautions_gathered_from_both_memos`(출처 「오더 메모 · 상담 메모 사본」 합침 · 「상담 메모 사본」만 있는 것(design-r2 SUN LI NA 예의 임플란트) · 「고객 메모」 맨 위)
- SSE 가 변경 때 version 을 보냄 — `test_sse_sends_version_on_change` + 위 실제 서버 확인

## 계약 대조 — SPEC 항목별 같음/다름

기준: SPEC-001 + `wp1-wp3-contract-addendum.md`(→ `cc/front/lib/types.ts`).

| 항목 | 판정 | 비고 |
|---|---|---|
| §4.1 build CLI · 입력(KST 날짜, 취소 포함) · seed.json + DB | 같음 | |
| §4.1-2 이름 치환 | 같음 | 아래 「치환 규칙」 |
| §4.1-3 직원(의사 · 상담사 · 코디, 마취용 제외) | 같음 | 의사∩코디 겹치면 의사 우선 |
| §4.1-4 상태 재구성 · since 오프셋(초) | 같음(근사) | 아래 「근사」 |
| §4.2 reset — since 를 지금 − 오프셋 · SSE | 같음 | history 시각 · 귀가 시각도 같은 방식으로 다시 계산 |
| §4.3 seed save — 이전 것 `seed.<시각>.json` | 같음 | build 도 같은 방식으로 이전 것을 남긴다 |
| §5.1 모델 · 계산 규칙(시안 그대로) | 같음 + 1건 | 시안에 없는 「단계 다 끝났는데 귀가 전」 고객: 그 방 queue[0] 직원이 complete 하면 귀가(아래 이슈 2) |
| §5.2 GET board · home · patients · staff · events | 같음 | board 에 `rooms`(id · name · col · row · cs · cap · kosRooms) · `corridors` · `now` 추가. customers 에 `nationality` 추가 |
| §5.3 조작 · 성공 시 `{version}` + SSE | 같음 | undo 는 마지막 변경만(아니면 409). 의사가 아니면 start/finish 400 |
| addendum since = epoch ms | 같음 | 모든 since · 시각 숫자 |
| addendum 현장 접수 `{scheduleId:null, name, order}` → `walkin-<n>` | 같음 | 환자 상세는 이름 · 오더(동선)만 |
| addendum patients `tickets[]` | 같음 | `getTicketBundlesQuery` AVAILABLE. 만료 · 담당 직군 · 수면은 KOS 에 없어 `""` · `의사` · `false` |
| check-in `order` 생략 | 추가 | 예약 고객은 order 를 안 보내면 KOS 작업으로 재구성한 오더를 쓴다 |
| §5.5 환자 상세 칸 | 같음 | types.ts 모양. `board.room` 은 칸 id, `route[].room` 은 칸 이름 |
| §6 로그인 | 같음 | 데스크 계정 = `{staffId:"desk", name:"데스크", role:"데스크"}`, home `/desk` · 직원 `/staff` |
| §8 env · CORS · 포트 | 같음 | |
| §7 통역 · WS | 안 함(WP2) | |

## 시드 재구성 — 어색한 곳(근사)

KOS 에는 최종 시각만 있어 아래처럼 정했다. 사용자가 앱을 움직여 고친 뒤 `seed save` 로 갈아 끼우면 된다.

1. **단계 끝 시각을 추정했다.** 상담 끝 = 첫 시술 작업 `ready`(시술 작업은 상담 뒤 한꺼번에 생김) · 원장 진료 끝 = 첫 의사 호출(`doctorCall`) · 시술 끝 = 그 작업들의 `completed`. 원장 상담 작업(ETCETERA)의 `completed` 는 방 점유 끝이라 쓰지 않았다.
2. **시술 단계를 묶었다.** 연달아 있고 방 · 의사 · 담당자가 같은 PROCEDURE 작업은 한 단계로(라벨 「첫 작업 외 n」). 안 묶으면 한 고객이 시술 9단계가 되어 데스크가 [완료]를 9번 눌러야 한다. 순서는 `sequence` 순이라, 실제로는 뒤 단계가 먼저 끝난 일정(예: 10:00 TW 고객 9작업)은 「완료 안 된 첫 단계」가 앞쪽에 남는다.
3. **진정 단계가 없다.** 10-09 에 「진정」 작업이 없어 오더 끝에 진정이 붙지 않는다(시안은 늘 붙임). 그래서 시술이 다 끝난 고객은 「마무리 대기」(step = 오더 길이)로 남는다 → 이슈 2.
4. **수면 단계가 없다.** `anesthesiaType` 이 CREAM/UNSPECIFIED 뿐이라 `sleep` 은 0건. `A_시술실1/2`(수면실 01/02)에서 시술 중인 고객은 그냥 그 방에 있고 `prev`(복귀 방)는 두지 않았다.
5. **위치.** 열린 작업 중 「호출된 시술 → 원장 상담(방 점유) → 그 밖」 순으로 방을 골랐다. 열린 작업이 없으면 라운지인데, **이미 작업을 마친 고객은 마지막 방에 둔다**(SPEC 「없으면 lounge」와 다름 — 14:45 의 KR 고객이 시술 끝 · 귀가 전이라 라운지에 두면 시안 로직으로는 귀가시킬 방법이 없다. design-r2 도 「관리실 03 · 마무리 대기」로 그렸다).
6. **직원 큐.** 그 방에 열린 작업의 담당자(원장 상담 작업 담당 포함)와 호출된 의사, 진행 중 상담의 상담사를 넣었다. 여러 방이면 가장 최근에 시작한 방이 queue[0]. **호출 전 의사는 큐에 넣지 않았다**(넣으면 queue[0] = 「방에 있음」이 되어 버림). 그래서 14:45 에 권태윤 원장 큐가 비어 있다 — 데스크가 배정해야 의사 화면에 뜬다.
7. **원장 상담 작업 담당 코디가 방에 계속 있다.** 그 작업이 접수부터 끝까지 열려 있어서, 의사가 [진료 완료] 해도 그 방에 코디가 「방에 있음」이라 시안 statusOf 로는 「시술」(파랑)로 보인다(SPEC §5.3 의 「마무리 대기」가 아님). 데스크가 그 코디를 빼면 「원장 대기 · …」/「코디 대기 · …」로 바뀐다.
8. **14:45 장면은 5명뿐**(동시 체류 최대 16명은 17시). 현황판이 한산하다 — 더 붐비는 장면이 필요하면 `--at 17:00`.
9. **2인관리실 01 겹침 없음**(14:45). 다른 시각엔 트윈1-1/1-2 가 한 칸이라 정원 2 를 넘으면 build 가 경고를 찍는다.
10. 귀가 시각 · 완료 기록 시각도 reset 때 「지금 − 오프셋」으로 바뀐다 → 환자 동선의 시각은 시연 시계 기준(실제 10-09 시각이 아님).
11. 예약 목록의 「시술」 · 「원장」은 예약값이 비어 있어(data-fit Q1) 실제 받은 작업에서 채웠다(「첫 시술 외 n」, 마취용 뺀 첫 의사, 없으면 「미정」). 테스트 행(취소 · 작업 0)도 취소로 들어가 있다(가짜 이름).

## 치환 규칙(D-09)

- 가짜 이름: 캡처 전체 고객 173명에게 id 로 결정적으로(KR 한글 3자 · 중화권 로마자 · JP · TH · 그 밖 영어식). 실제 이름 331개(정규화)와 겹치면 다시 고름
- 메모: 모든 고객의 로마자 이름(낱말 사이 공백 · 쉼표 · 하이픈 무시) · **그날 고객의** 한글 이름 · 음역 → 가짜 이름. 「이름 :」 줄 값 → 그 메모 주인 가짜 이름. 남은 대문자 로마자 연속이 고객 이름 낱말로만 되어 있으면 동행인으로 보고 치환(예: 예약 메모의 「HUANG CHENG」 → 그 고객 가짜 이름). 전화번호 꼴 → `010-****-****`
- 직원 · 유입처 이름은 그대로(다른 날 고객 한글 이름은 치환하지 않는다 — 직원 이름 오치환 방지)
- 참조 문서에서 전화 · 차트번호 · 생년월일 · SNS id 는 비우고, 나이는 시드 날 기준 계산값만 둔다

## 이슈 · 코디가 확인할 것

1. **이름 대조 예외 3건** — 강도윤 · 송지호(시술 담당 코디) · 차예린(예약 담당)가 다른 날 고객 이름과 같다. 직원 자리라 D-09 대로 두었다. 시험은 직원 · 유입처 이름을 대조에서 뺀다.
2. **시안 로직 확장 1건** — `complete` 때 그 방 고객의 현재 단계가 없으면(단계는 다 끝났고 귀가 전) 귀가 처리한다. 시안에선 생기지 않는 상태(진정 단계가 늘 붙음)라 시드에서만 필요하다. 싫으면 「진정 관리」를 모든 시술 고객 오더 끝에 붙이는 쪽으로 바꿀 수 있다(SPEC 「진정 작업이 있으면」과 다름) — 판단 필요.
3. **AC §9-2 「배정 → 의사 화면 「다음」」** — 의사 큐가 비어 있으면 첫 배정은 「다음」이 아니라 「지금(current)」에 뜬다(SPEC §5.2 current = queue[0]). 14:45 시드에서 권태윤 원장은 큐가 비어 있다(근사 6). 시연 때 두 번 배정하거나 시드를 손본 뒤 `seed save`.
4. 시술권 `expires`·`role`·`sleep` 는 KOS 에 값이 없어 빈 값 · `의사` · `false` 로 채웠다(addendum 의 필드는 다 있음).
5. `data/` 에 실데이터가 든 `seed.json` · `cc.db` 가 있다(gitignore 확인). `CC_CAPTURE_DIR` 은 `.env` 에 넣지 않았다 — 사용자가 `.env` 를 만들거나 명령 앞에 env 로 준다.
6. 레포 루트 `README.md` 에 `sts/` 언급이 있으면 고쳐야 할 수 있다(범위 밖이라 안 봄 · 안 고침).
