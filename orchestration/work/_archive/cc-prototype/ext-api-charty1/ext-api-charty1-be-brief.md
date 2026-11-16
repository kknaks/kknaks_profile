# [backend] charty 1차 외부 연동 API — KOS0 확인 + BE1 ~ BE6 (SPEC-008 0.4.2)

너는 **cc-prototype `backend` 워커**다. **너는 이 작업의 앞 맥락이 하나도 없다** — 아래 파일이 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-charty1` (브랜치 `kknaksss/ext-api-charty1`)
base 브랜치: `origin/main`(`0a58aba`) → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)
기능 폴더 = **`procedure/`**(back = `procedure/back/`). 이 워크트리를 쓰는 다른 워커는 없다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype/30-work/work-014-ext-api-charty1.md` ← **작업 순서 · WP 표 · 계약 고정점 · 주의.** 이 파일이 실행 계획이다
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` (0.4.2) ← 계약의 SoT. **여기 없는 건 발명하지 마라.** 0.4.0 ~ 0.4.2 절 · §9 T48 ~ T73 · 「실물 확인(0.4.0)」 · 부록 F · G
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md` (D-01 ~ D-41) · `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md`(기존 ext 결정)
- 조사 리포트(근거 · 내부 API 모양): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/research-charty1-sources.md` · `research-clinic-staff.md` · `research-har-history-hospital.md`
- 문서 검수 리포트(왜 이렇게 정했나): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/review-doc-r1.md` · `review-doc-r2.md` · `review-doc-r3.md`
- 코드 레포 `AGENTS.md`(있으면)

**기대는 개념** — 이 작업이 따를 판단 기준:

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/areas/concept/back/minimal-api-surface.md` — 외부 경로는 계약에 적힌 칸만 낸다 · 경로 목록 고정 시험은 넓힐 뿐 지우지 않는다
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/areas/concept/back/api-documentation.md` — 새 경로 · 칸 전부 Swagger `summary` · `description` (BE6)
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/areas/concept/back/empirical-limit-probing.md` — KOS0 은 추측 대신 데모 실호출로 모양을 본다

## 2. 배경 / 무엇을 바꾸나

cc-prototype `procedure/back` 은 KOS(병원 관리 SaaS) → CC → 연동처(linky · charty) 구조의 가운데다. 지금 외부 API 는 여섯(`GET /menu` · `POST /customers/lookup` · `POST /reservations` · `GET /availability` · `POST /customers/visits` · `POST /customers/reservations`)이다. charty 요청으로 **lookup 을 고치고 새 일곱 경로**(board · 예약 상세 · 언어 · 오더 메모 · 상담 메모 · 병원 · 직원)를 더한다. 프로토라 연동처별 권한 분기는 없다(DEC-012 D-01).

## 3. 계약

연동처 ↔ CC 계약 = SPEC-008 0.4.2 전부 · WORK-014 「계약 고정점」 표. **고정점이 바뀌어야 할 것 같으면 멈추고 코디에게 묻는다.** 프론트 작업 없음.

## 4. 먼저 읽을 핵심 파일 (`procedure/back/` 아래)

- `app/api/ext.py` · `app/service/ext.py` · `app/schemas/ext.py`(`:24-30` `ExtLookupRequest` · `:157-158` `ExtCustomerRequest` 상속 — 끊는다) — 기존 외부 API
- `app/service/reservations.py`(`_flow` `:530-531` · `_detail_reads` `:581-619` · `personal` · `kos_write` `:710-721` · `_event` `:478-480`) — 손대는 곳은 셋뿐
- `app/kos/client.py`(내부 API · UA · 토큰) · `app/kos/reservation_sync.py` · `app/kos/sync.py` · `app/kos/runtime.py`
- `app/repository/db.py` · `app/repository/repo.py` · `app/domain/reservation_rules.py` · `app/main.py:120-124`
- `tests/fake_kos.py` · `tests/test_ext_*.py` · `tests/test_resv_*.py`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `procedure/back/`
- `procedure/docker-compose.yml` · `procedure/.env.example`(필요할 때만)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/kos0-report.md` 1개(레포 밖 · 코디 작업 폴더)

## 6. 구현 단계

**순서 = KOS0 → BE1 → BE2 → BE4 → (코디 「BE3 · BE5 가도 됨」 신호) → BE3 → BE5 → BE6.** 각 WP 의 내용 · 대상 파일 · 완료 조건 · 검증 명령은 WORK-014 WP 표 그대로.

1. **WP-KOS0 (조회만 · 쓰기 0 · 코드 변경 0)** — WORK-014 KOS0 행의 ① ~ ④.
   - 키: `/Users/kknaks/git/ax-clinic-project/scripts/.env` 의 **`KOS_API_tenent_dev` 만**(데모 테넌트). **`KOS_API_tenent`(실제 지점)는 절대 쓰지 않는다.** 그 레포는 read-only · 키를 어디에도 복사하지 않는다. 호출 예시는 같은 레포 `scripts/kos_collect.py` · `para/resources/technology/2026-09-18-kos-developers-api-guide.md`. 내부 API 는 지금 `KosClient` 방식(시스템 계정 토큰 · 브라우저 UA) 그대로.
   - 조회 스크립트 · 원 응답은 **레포 밖 네 scratchpad** 에만.
   - 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/kos0-report.md` — ① ~ ④ 의 **키 트리 · 꼴 · 건수만**(값 · id · 이름 금지) + **판정 한 줄**(「D-16 그대로」 또는 「D-17 대안」) + `flowStep` ↔ `CONSULTATION_WAITING` 대응 근거 + 휴무 낼 칸 후보.
   - 끝나면 완료 보고가 아니라 **중간 보고**만 하고 바로 BE1 로 간다:
     `orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 --text "[중간] backend KOS0 끝 — 판정 <한 줄>. kos0-report.md. BE1 진행." --enter`
2. **BE1 → BE2 → BE4** — 판정과 상관없다. 각 WP 끝에 그 WP 의 부분 검증 명령만 1번.
3. **BE3 · BE5 는 코디 신호를 기다린다.** 코디가 KOS0 판정으로 SPEC · DEC 에 고침 줄을 넣고 신호를 보낸다. BE4 까지 끝났는데 신호가 없으면 `[질문]` 으로 묻고 기다린다.
4. **BE6** — 마지막에 전체 `uv run pytest -q` 한 번 · 수치 보고.

## 7. 범위 제약 — 하지 말 것

- **KOS 쓰기 0**(KOS0 포함 전부). 쓰기 실물 확인은 코디의 WP-E2E-LOCAL 몫이다
- 커밋 · push · PR 금지. 사용자 포트(8700 · 3000) · 사용자 프로세스 · 사용자 docker compose 건드리지 않는다. 서버를 띄워야 하면 다른 포트 · 다른 compose 프로젝트 이름
- **직원 API 동작 무변경** · **기존 외부 여섯 계약 무변경**(lookup 은 칸 추가 + SPEC 변경 이력 0.4.0 ~ 0.4.2 에 적힌 행동 변화만)
- WORK-014 「주의」 절 전부(KOS 먼저 · `personal()` 그대로 · 판정 함수 하나 · visit UPDATE 만 · 헤더 다섯 경로만 · `ext_call` 무변경 · 병원 칸 다섯 · 휴무 원소 그대로 금지 · 시도 예약 `BEGIN IMMEDIATE` 안에 `await` 없음)
- **public 레포**: 코드 · 시험 · 리포트에 키 · KOS id · 테넌트 id · 실명 · 실제 이메일 · 전화 · 병원 이름 0. 시험 값은 `<이름>` · `a@example.com` 꼴
- SPEC 에 없는 칸 · 오류 code · 정책을 만들지 않는다. 막히면 묻는다

## 8. 검증

```
procedure/back 에서 — 착수 전 기준선 uv run pytest -q 1번(수치) · WP 마다 WORK-014 「검증 명령(부분)」 1번 · BE6 끝에 전체 uv run pytest -q 1번 · ruff 는 레포 설정이 있으면 BE6 에서.
기능 폴더 밖 import 없음 확인. 사용자 포트 · 프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 완료 보고 body 에 **T 번호별 시험 이름 표** · **WP 별 부분 검증 수치** · **public grep 결과**를 넣는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aad33590-4323-443d-9c17-3541475ee5f5 --from term_0729bfce-b08e-41e2-9218-165f550e86ed \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
