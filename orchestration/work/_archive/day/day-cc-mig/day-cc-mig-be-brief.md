# [backend] #264 KOS 키 전부 담는 테이블 보충 — 마이그레이션 0012 · 매퍼 · 기존 행 업데이트

너는 **day `backend` 워커**다. **맥락이 없다고 가정하라.** 먼저 읽을 것:

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 루트 `AGENTS.md`(이 워크트리)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-cc-mig` (브랜치 `kknaksss/day-cc-mig` · base `origin/dev` = `844eace4` — 시작 때 `git fetch` 해서 dev 가 더 새로우면 멈추고 질문)
최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- **계약**: SPEC-000 §4A 「KOS 키 보충」 — `/Users/kknaks/orca/workspaces/mediness-mediness/day-cc-mig-spec/products/day/20-spec/spec-000-data-model.md` (mediness PR #954 · 커밋 1944f922 · 문서 검수 PASS). §4A 공통 규칙 · §4A.1 ~ §4A.10 대조표 · §6 OQ-4A-1 ~ 15. **여기 없는 칸 · 값은 발명하지 마라.**
- **Delivery**: `MediSolveAIDev/CENTURION_DAY#264` — target_delta D-1 ~ D-5 · acceptance A1 ~ A7 · non_goals (`gh issue view 264 --repo MediSolveAIDev/CENTURION_DAY`)
- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/_RESUME.md` §2(2026-11-20 행)
- KOS 키 · 모양 · HAR 근거: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-report.md`(2차 K2 경로별 키 표) · `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-3-report.md`(3차 N3 · N4) — 매퍼가 읽을 키 경로는 여기서 확인
- 앞 사례(같은 꼴 작업): `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/_archive/day/customer-erd/customer-erd-be-2-brief.md` · `customer-erd-be-3-brief.md` · `be-2-report.md` · `be-3-report.md`(마이그레이션 0010 · 동기화 · 백필 · DEMO 실물 방식)

기대는 개념: 해당 없음.

## 2. 배경

DAY 는 cc-prototype 의 ext 외부 연동 API 를 옮긴다(2단계). 그 전에 **KOS 가 주는 키를 전부 담는 테이블을 먼저 만든다** — 나중에 기능 붙일 때 마이그레이션을 줄이려고(사용자). 화면 · 입력 기능은 만들지 않는다. 값은 **이미 도는 KOS 동기화 회차**에서 채우고, 이미 들어 있는 행은 수동 업데이트 경로로 채운다.

## 3. 계약

해당 없음(외부 API 없음). DB 계약 = SPEC-000 §4A.

## 4. 먼저 읽을 핵심 파일

- `backend/day/models/*.py` · `_columns.py` · `__init__.py` · `backend/migrations/versions/20261119_0011_visit_reserved_index.py`(head)
- `backend/day/emr/kos/*`(client · mapper · mapper_menu · mapper_purchase · mapper_sale_values · mapper_values · sale_reads · staff_client) · `backend/day/emr/sync_*.py` · `backend/day/services/emr_sync.py` · `emr_sale_sync.py` · `emr_backfill.py` · `backend/day/tasks/emr.py`
- `backend/runtime/backfill.py`(`--dry-run` · `--resume` · KOS 1초 1회 — 업데이트 경로로 재사용 · 확장)
- `backend/tests/migrations/` · `backend/tests/day/emr/`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/models/` · `backend/migrations/versions/` · `backend/day/enums/` · `backend/day/emr/` · `backend/day/services/emr_*.py` · `backend/day/tasks/emr.py` · `backend/runtime/backfill.py` · `backend/tests/`
- (frontend 몫 — `backend/day/routers/`(api 제외) · `templates/` · `static/` · `styles/` — 제외)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/be-1-report.md`

## 6. 구현 단계

1. **D-1 마이그레이션 0012**(0011 에 이어짐) — §4A 새 표 12 · 기존 표 nullable 칸 · 새 DAY enum 타입 · `external_ref.entity_type` 새 값 `hospital`. **기존 표 · 칸 이름 · 타입 변경 0.** 새 표 `deleted_at` · 유일 제약은 살아 있는 행만. 모델 동기.
2. **D-2 매퍼** — §4A 「동기화로 채움」 칸 전부. 상태 · 종류 = DAY enum · **목록 밖 KOS 값 = 행 유지 · 그 칸 null + 동기화 경고(KOS 원래 문자열 남김)** — 지금 `MappingError` 로 행째 빼는 곳(CARD 사례 `mapper_purchase.py:165-168 · 192-204`)도 이 규칙으로. CARD 매핑 추가. `created_at` ← KOS `createdDateTimeUtc`. 금액마다 통화. 번역 jsonb.
3. **D-3 병원** — 기준 정보(1시간) 회차에 `get-hospital` · `get-default-operation-timetable` · `get-default-days-off` · 예약 그룹 휴무 · 예약 규칙 조회를 더한다. KOS `hospitalId` → `external_ref(hospital)`. 휴무 모양은 키 미관찰(OQ-4A-2) — 빈 배열이면 아무것도 안 쓰고, 값이 오면 SPEC 모양대로 · 모르는 모양이면 경고.
4. **D-4 고객 칸** — SPEC 기본값(OQ-4A-14) 대로.
5. **상용 서비스 중**: 새 동기화 부분이 실패해도 **기존 회차(시술현황 판)가 멈추면 안 된다** — 실패 격리(예외 · 트랜잭션 · 타임아웃). 기존 함수 동작 · 반환 · 호출 수 변경 0(더하기만).
6. **D-5 기존 행 업데이트** — 이미 있는 행의 새 칸을 채우는 수동 실행 경로(`runtime/backfill.py` 확장 또는 새 stage). `--dry-run`(KOS 읽고 DB 쓰기 0 · 건수만) · `--resume` · KOS 1초 1회 · 자기 세션만 해제(`KOS_CLIENT_TAG`).
7. **테스트** — 마이그레이션 왕복 · 매핑(값별 · 목록 밖 값) · upsert · 병원 · 기존 회차 격리 · 업데이트 dry-run DB 쓰기 0 · 멱등 · 물리 DELETE 0(grep).
8. **로컬 실물(DEMO · A3 · A5)** — customer-erd be-2 · be-3 과 같은 방식: 버리는 컨테이너 · 사용자 테스트 계정(`~/.config/day/kos-test-account.env` · 값 출력 금지) · `hospitalName` 이 DEMO 인 테넌트만 · 데모 시스템 계정 · 실 명동점 금지 · `KOS_CLIENT_TAG=local` · 사용자 포트 · 프로세스 금지(다른 포트). 순서: 동기화 한 회차(새 칸 · 병원 표 채워짐 건수) → **업데이트 `--dry-run`(건수만 · DB 쓰기 0 확인) → 실제 업데이트(새 칸 채워짐) → 한 번 더(쓴 행 0)**. 세션 해제. 못 하면 이유와 함께 pending.
9. **dev 서버 실제 업데이트 방법만** 리포트에(명령 · 환경 · 예상 시간 · 호출 수) — 서버 실행은 코디가 한다.
10. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/be-1-report.md` — 바꾼 파일 · §4A 칸 → 코드 대응(표별 칸 수 대조 · 빠진 칸 0) · 기존 칸 변경 0 증거 · 테스트 수치 · DEMO 건수(드라이런 · 실제 · 재실행) · 남은 위험 · OQ 처리.

## 7. 범위 제약 — 하지 말 것

- ext API · 화면 · 수납 · 문진 · 타이머 · 리액션 · 예약 칸/점유 표 · DAY → KOS 쓰기(non_goals)
- 기존 칸 이름 · 타입 변경 · 물리 DELETE
- 커밋 · push · PR. 사용자 포트 · 프로세스 · 공유 DB(STG · PROD) · dev 서버 접속 금지.
- 비밀값 · 토큰 · 테넌트 id · 환자 정보를 리포트 · 로그 · 테스트 고정값에 쓰지 마라.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 시술현황 판 기존 테스트(관련 파일) 통과(A6).
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다. 기존에 깨져 있던 무관한 실패는 「무관」으로.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --from term_19c73ecd-4bec-48fa-8d75-eb86935ec90d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: #264 테이블 보충 <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
