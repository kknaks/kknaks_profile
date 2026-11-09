# 리뷰 리포트 — day-data-architecture / doc · 40-architecture 런타임 · 코드 구조 (2026-11-03)

대상: `mediness-mediness/day-data-architecture-spec` 의 미커밋 변경. `PR #909` 커밋 `974caeac` 위에 다음이 올라와 있다.
- 수정: `products/day/40-architecture/system.md` · `40-architecture/README.md` · `log.md`
- 새 파일: `40-architecture/code-structure.md`

SPEC-000 등 나머지는 이미 PASS 했으므로 이번에는 보지 않았다.

원천:
1. 런타임: `kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` (줄 번호는 이 파일 기준).
2. 코드 구조: `CENTURION_DAY` `origin/v2-dev:AGENTS.md`. fetch 후 HEAD 는 `b2ef2c06` 이고, code-structure.md 가 적은 기준 커밋과 같다.

방법: 원천 문장 · 수치를 하나씩 대응시켜 대조했다. 그림의 노드 · 화살표는 원천 근거가 있는지 따로 봤다. 문서 규칙과 기존 절과의 충돌도 확인했다. 링크는 전수 검사했고 lint 는 1회 돌렸다.

## 판정: WARN

원천의 결정은 빠짐없이 옮겨졌고, 원천에 없는 기술 · 버전 · 수치는 0이다. caddy 위치는 「일반 앞단으로 그렸다」고 표시돼 있다. 걸리는 것은 하나다. code-structure.md 가 정본 AGENTS.md 의 「아직 정하지 않은 것」으로 독자를 보내는데, 그 절이 로그인 · 배포를 아직 미정이라고 한다. system.md · SPEC-000 은 이 둘을 정해 둔 상태라 문서끼리 어긋나 보인다(W1).

## FAIL

없음.

## WARN

### W1. code-structure.md 가 보내는 「아직 정하지 않은 것」이 system.md · SPEC-000 과 어긋난다

- 위치: `products/day/40-architecture/code-structure.md:74` (「아직 정하지 않은 것 → 「아직 정하지 않은 것」」)
- 근거:
  - 정본 `AGENTS.md:126-131` 은 「로그인 · 계정 방식」 · 「배포(Azure 서버 할당 예정)」를 미정으로 둔다.
  - 런타임 원천은 다르다. `system/README.md:10` 은 「로그인 = KOS sign-in」을 「이미 정한 것」으로, `:11` 과 `:27-32` 는 배포 · 서버 사양을 정한 것으로 둔다.
  - mediness 안에서도 `system.md:100-109`(서버), `system.md:167-169`(로그인), DAY-SPEC-000 §3 04 가 이 둘을 정해 두었다.
- 문제: mediness 독자는 같은 폴더 안에서 「정함」과 「미정」을 동시에 보게 된다. 원인은 코드 레포 정본이 갱신되지 않은 것이다(원천 쪽 지연). planner 도 미결 2 로 보고했다.
- 방향 (둘 중 하나):
  - (a) 코드 레포 `AGENTS.md` 「아직 정하지 않은 것」에서 로그인 · 배포를 빼거나 갱신한다. 코드 레포 일이라 코디 판단이다.
  - (b) 그 전까지 `code-structure.md:74` 행에 「로그인(KOS sign-in) · 서버 사양은 system.md 기준으로 정해졌다 — 정본 갱신 대기」를 한 줄 덧붙인다.

---

## 원천 1 (런타임) → system.md 대조

| 원천 | system.md | 결과 |
|---|---|---|
| `:7` 레포 · centurion 모양(`backend/day/` + `runtime/`) · 구조 = AGENTS.md | `:12` · code-structure.md | 있음 |
| `:8` 웹 Jinja2 + HTMX · 앱 Flutter(iOS · 축소판) | code-structure.md `:55-61` · 그림 `:22` | 있음 |
| `:9` DB PostgreSQL `day` · SQLAlchemy 2 async · alembic | `:54` | 있음 |
| `:10` 폴링 10초 / 1시간 · 쓰기 큐 · 로그인 KOS sign-in | `:95` · `:133-138` · `:145-` · `:167-169` | 있음 |
| `:11` 배포 DAY 전용 Azure(나중) · `APP_ENV` | `:109` · `:173` | 있음 |
| `:17` #1 api / worker 분리 · api 는 KOS 를 부르지 않음(로그인 · 잔여 시술권 바로 조회 예외) · 근거 | `:61-62` · 그림 점선 `:49` | 있음 · 근거 그대로 |
| `:18` #2 taskiq · worker + scheduler(`LabelScheduleSource`) | `:62-63` · 그림 `:27-28` | 있음 |
| `:19` #3 Redis — 브로커 · 결과 · 화면 알림 · 잠금 | `:64` · 그림 `:29` | 있음 |
| `:20` #4 `taskiq-redis` · RabbitMQ 없음 · 메모리 | `:64` | 있음 |
| `:21` #5 `interval` 10 / 3600 · taskiq 0.12.6 · `scheduled_task/v2.py` | `:95-96` | 있음 · 수치 · 버전 그대로 |
| `:22` #6 병원별 Redis 잠금 · 10초 넘기면 건너뜀 · 코디 기본값 | `:98` | 있음 · 「코디 기본값」 표시 유지 |
| `:24-25` 버튼 하나의 흐름 | `:69-91` sequence | 있음 · 순서 같음 |
| `:29` 예상 메모리 5항목 ≈ 1.9GB | `:105` | 있음 · 수치 그대로 |
| `:30` 조건 · centurion 비교 | `:106-107` | 있음 |
| `:32` 요청할 것 | `:104` · 그림 `:24` 「예정」 | 있음 |
| `:34-43` 기본값 6행 (코디 추천 — 바꿀 때만 말하기) | `:111-122` | 6행 모두 같음 · 「코디 추천 기본값」 표시 유지 |

- 원천에 없는 기술 · 버전 · 수치는 **0**이다. system.md 의 수치(2코어 / 4GB · 768 / 384 / 384 / 256 / ~50MB · 1.9GB · 0.12.6 · 10 / 3600)는 전부 원천 `:21, 29` 에 있다.
- caddy: 원천에는 메모리 표(`:29`)에 이름만 있다. system.md 는 이를 두 곳에 표시했다. `:55` 「일반적인 앞단 배치로 그렸다」와 `:67` 「원천 메모리 표에 이름만」이다. 「VM 안」은 원천 메모리 표(VM 기준)에서 나온 것이라 근거가 있다. **표시됨**.

## 원천 2 (AGENTS.md) → code-structure.md 대조

| code-structure.md | AGENTS.md | 결과 |
|---|---|---|
| `:20-22` 레포 · `v2-dev` · 이전 코드 `stg` · `main` 참고만 · centurion 모양 · 통합은 나중 | `:6-12` | 같음 |
| `:28-35` 최상위 8행 | `:16-53` 트리 | 같음. `common` 에서 cors 를 생략했다(요약) |
| `:39` centurion 은 admin / crm · catalog / crm/emr, DAY 는 `backend/day` 한 패키지 | `:10-11` · `:22-44` | 같음 |
| `:43-48` 층 6행(화면 · JSON API · 업무 · 백그라운드 · public · emr) | `:23-44` · `:61-66` | 같음. repository 없음 · `day.public` 만 · DTO · 튜플 · 도메인 예외도 같다 |
| `:50-53` router HTTP 만 · `day` → `common` · `day` 스키마 · 같은 파일 이름 · `tests/architecture/` · mapper 흡수 · outbox | `:55-57` · `:61-68` · `:72-74` | 같음 |
| `:57` 웹 — Jinja2 + HTMX + 바닐라 JS · HX-Request 분기 · medikit 토큰 · 세부는 정본 | `:80-87` | 같음 |
| `:61` 앱 — iOS · 폰 · 아이패드 · 축소판 · 스펙이 범위 · 서버 계산값 | `:50` · `:91-92` | 같음 |
| `:65-74` 정본 절 안내 8행 | `:14` · `:59` · `:70` · `:78` · `:89` · `:105-107` · `:115-117` · `:126` | 절 이름이 모두 실재한다 |

- 발명 0. 복제 수준도 아니다. 디렉터리 · 층 단위까지만 썼다. 파일 이름은 `public.py` · `emr/<업체>/mapper.py` 둘뿐이고 둘 다 규칙 설명에 필요하다. 「작업 규칙」 · 「백엔드 안전」 · 「테스트」 본문은 옮기지 않고 링크로 보낸다.
- 빠진 것 중 정본에 있는 것: 웹 세부(JS 하나 · CSP · 벤더링 · CSRF), 앱 `--dart-define`, 작업 규칙 전체. 모두 「정본으로 가는 곳」 표로 보낸다. 요약 의도와 맞는다.

## 문서 규칙 · 충돌 · 링크

- `rules/document-pipeline.md` 의 40-architecture 「쓰지 않는 것」(schema 전문 · column 목록 · repository 함수 목록 · migration 전문 · API endpoint 본문): **위반 0**. `system.md:95` 의 `schedule=[{"interval": 10}]` 는 원천 `:21` 의 설정값 한 줄이고 API 본문이 아니다.
- 기존 절 ↔ 새 절:
  - 「쓰기 — 외부 쓰기 큐」 그림의 참가자가 `DAY(api · worker)` 로 바뀌었고, `:162` 「적재는 `api`, 발송 · 확인은 `worker`」가 원천 `:17, 24` 와 맞는다.
  - 「읽기 — 폴링」 표(10초 / 1시간)와 `:95` interval 10 / 3600 이 일치한다.
  - 「외부 통합」 APNs(`:194`)와 그림 `Worker --> APNs`(원천 `:17` worker 푸시) · 기본값 「APNs 직접」이 일치한다.
  - 「KOS 를 뗄 때」 `backend/day/emr/`(`:186`)는 AGENTS.md `:39` 와 같다.
  - `:162` transaction 문장에 출처(AGENTS.md 「외부 CRM 연동」)가 붙었다. 1판 참고 항목이 해소됐다.
  - 충돌은 W1 하나뿐이다.
- `40-architecture/README.md` 진입 2행 · 핵심 도메인 머리 1문장은 내용과 맞다. `log.md` 의 `arch-change` · `#909` 한 줄은 형식에 맞다.
- 링크: `products/day/**/*.md` 상대 링크 전수 검사 결과 **깨진 링크 0**.
- lint `python3 scripts/lint-pipeline.py --strict` 1회 → **exit 0 · 0 error · 263 warning**. `products/day/` 범위는 ERROR 0 · WARN 0이다. 263 WARN 은 타 제품의 기존 경고라 **무관**하다.
- 보안 grep(이메일 · 토큰 · URL · Bearer): 0건. VM 사양 · 메모리 수치는 비밀값이 아니다.

## 직원이 실물에서 만날 자리

없음. 문서 변경뿐이다.

## 참고(설계 판정 아님)

- 그림 `system.md:39` 의 `API --> Blob`(파일을 쓰는 쪽이 api)는 원천이 정하지 않았다. 원천에는 「파일은 Azure Blob」(`:30, 40`)뿐이다. 업로드를 api 가 받는 것은 자연스러운 읽기라 지적하지 않는다. 다만 caddy 처럼 「일반적인 배치」로 표시하면 더 엄밀하다.
- 그림의 `Sched -- 주기 작업 --> Redis -- 태스크 --> Worker` 는 원천 #2 · #4(scheduler · Redis 브로커)에서 바로 나오는 흐름이라 근거가 충분하다.
