# day-data-architecture — 40-architecture 런타임 · 코드 구조 결과 보고

## 상태: done

## 수행 내용

워크트리 `mediness-mediness/day-data-architecture-spec`(PR #909 커밋 `974caeac` 위) · `products/day/` 만 수정. 커밋 없음. SPEC-000 · 10-decision · 20-spec.md · 30-work.md 는 손대지 않았다.

| 파일 | 내용 |
|---|---|
| `40-architecture/system.md` (수정) | 머리 — 원천 2개(erd · system README) 명시 · code-structure 링크. **토폴로지 그림을 원천 런타임으로 교체**(VM 안 caddy · api · worker · scheduler · Redis / VM 밖 관리형 PostgreSQL · Blob · APNs · KOS, `api` → KOS 는 로그인 · 바로 조회만 점선). 새 절: 런타임 구성(프로세스 · 자원별 하는 일 · 근거) · 버튼 하나의 흐름(sequence) · 폴링 방식 · 중복 막기(taskiq `interval` 10 / 3600, taskiq 0.12.6 `scheduled_task/v2.py` 확인 · 병원별 Redis 잠금 · 10초 넘기면 건너뜀) · 서버(VM 2/4 + 관리형 PG + Blob · 예상 메모리 ≈1.9GB · centurion 비교) · 기본값 표 6행(원천 그대로). 기존 절은 그대로 두고 쓰기 큐 그림의 참가자를 `DAY(api · worker)` 로, 「적재는 api · 발송 · 확인은 worker」 한 줄, transaction 문장에 출처(AGENTS.md) — 검수 참고 항목, 「KOS 를 뗄 때」의 `emr/` 행을 `backend/day/emr/` + 링크로 |
| `40-architecture/code-structure.md` (신규 · `DAY-CODE-STRUCTURE`) | CENTURION_DAY `v2-dev` `AGENTS.md`(기준 `b2ef2c06`) 요약: 레포 · 브랜치 · 모양(centurion) · 최상위 배치 표 · `backend/day` 층 표(화면 = admin 방식 / JSON API / 업무 = crm · catalog 방식 · repository 없음 / tasks / `public.py` 만 밖으로 / `emr/` 업체 어댑터) · 웹(Jinja2 + HTMX) · 앱(Flutter · iOS 축소판) · 「정본으로 가는 곳」 표(AGENTS.md 절 이름) |
| `40-architecture/README.md` | 진입에 system.md 설명 갱신 · code-structure.md 추가. 핵심 도메인 표 머리에 「도메인 코드가 들어갈 자리 → code-structure.md」 |
| `log.md` | 2026-11-03 `arch-change` · PR `#909` 한 줄 |

### 자리 선택 — 코드 구조를 새 파일로 둔 이유

system.md 는 런타임 · KOS 연동 흐름이고, 코드 배치는 읽는 사람(코드에 손대는 워커)과 바뀌는 때(레포 AGENTS.md 개정)가 다르다. 한 파일에 두면 system.md 가 정본 AGENTS.md 의 사본처럼 커진다. `rules/document-pipeline.md` 40-architecture 「쓰지 않는 것」(schema 전문 · column 목록 · repository 함수 목록 · migration 전문)에 맞게 — 디렉터리 · 층 단위까지만 쓰고 파일 · 함수 목록, API 본문은 쓰지 않았다(그건 정본 링크). 선례: nexus 40-architecture 의 `operations.md`(표준 3개 밖 파일).

## 검증

```
python3 scripts/lint-pipeline.py --strict → 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 WARN 은 전부 타 제품 기존 — 무관)
```

원천 대조(손 대조): system README 「이미 정한 것」 5 · 「정한 것」 6행 · 버튼 흐름 · 서버 3단락 · 기본값 6행 → 전부 system.md 에 있다. 원천에 없는 기술 · 버전 · 수치 추가 없음(taskiq 0.12.6 · 메모리 수치 · VM 사양은 원천 그대로).

## 미결·주의점

1. **caddy 의 역할 · 위치는 원천에 없다** — 원천은 예상 메모리 표에 `caddy ~50MB` 이름만 있다. 그림에서 클라이언트 → caddy → api 로 일반적인 앞단 배치를 그렸고, system.md 에 그렇게 그렸다고 적었다. 맞는지 코디 · 사용자 확인.
2. **CENTURION_DAY `AGENTS.md` 「아직 정하지 않은 것」에 「로그인 · 계정 방식」 · 「배포(Azure 서버 할당 예정)」가 남아 있다** — 그런데 erd 원천(04)은 로그인 = KOS sign-in 으로, system 원천은 서버 사양 · 런타임을 정했다. 정본 AGENTS.md 를 갱신할지 코디 판단(이 작업 범위 밖 · 코드 레포).
3. AGENTS.md 의 최상위 표기는 `backend/runtime` · `backend/common` · `backend/day` · `backend/migrations` · `backend/tests` 이고 `app/` · `deploy/` 는 최상위다. 브리프의 「runtime · common · migrations · tests」는 `backend/` 아래로 적었다(정본대로).
4. AGENTS.md 는 v2 를 centurion 처럼 `backend/admin` · `crm` · `catalog` 로 나누지 않고 `backend/day` 한 패키지에 둔다 — 「화면 = admin 방식 / 업무 = crm · catalog 방식」은 **방식**을 따른다는 뜻으로 적었다.
5. 원천 기본값 표의 SSE · Blob · APNs · Key Vault · JSON 로그는 「코디 추천 — 바꿀 때만 말하기」 — system.md 에도 「코디 추천 기본값」으로 표시.
