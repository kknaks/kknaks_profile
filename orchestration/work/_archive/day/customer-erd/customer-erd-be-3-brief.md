# [backend] 3단계 — 지난 이력 백필 스크립트(내부 API · KOS 1초 1회 · 수동 실행)

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

너는 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. base = origin/dev `bbd9220a`(코디가 발주 직전 fetch 한 최신). **시작 전에 `git fetch origin dev && git log -1 origin/dev` 로 dev 가 더 나아갔는지 보고, 나아갔으면 rebase 한 뒤 시작해라**(사용자 규칙: 코드 작업 전 dev 최신).

## 0. 먼저 — 검수 4 WARN 정리 (`review-code-4-report.md`)

- **WARN-A**: 5분 회차 삭제로 남은 죽은 코드 · 낡은 주석을 지운다(리포트에 적힌 곳 · `sale_reads.py` stat 속성 · `_utc` 등).
- **WARN-B**: 오늘 구매 태스크 메시지에 발행 시각을 싣는다. 같은 병원에서 이미 더 새로운 메시지를 처리했으면 오래된 메시지는 버린다(세고 넘어감). `sales_from_payload` 를 `_isolated` 안으로 옮긴다.
- **WARN-D**: 진료항목 · 기기 · 약물은 「옵션에서 빠짐 ≠ 삭제」가 맞다. 다만 KOS 가 **명시적으로 `deleted:true`** 를 준 진료항목은 소프트 딜리트한다(SPEC-002 ㉔ 「삭제」 규칙). 테스트를 단다.
- WARN-C(구역 내부 응답은 데모로만 확인)는 코드 변경이 없다. 리포트의 「prod 첫 기준 정보 때 구역 수 확인」에 남긴다.

## 1. SSOT — 먼저 읽을 것

- 결정(사용자 2026-11-19 · `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/_RESUME.md` §2): 백필은 **수동 실행 스크립트** · KOS **1초에 1회** · **내부 API 만** · 어제까지 · 로컬 테스트 → dev 서버 드라이런 → 실행 · **dev 데이터 초기화 없음**.
- SPEC-000 OQ-00-3 메모(`/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec/products/day/20-spec/spec-000-data-model.md`) — 판은 오늘 창만 · 사라짐 처리는 창 안 · 동기화 알림 없음 · 창은 어제까지 · S-8 세션 · flow_log 마지막 단계 · visit 날짜 인덱스 없음 · 내부 고객 목록 `visitor/v2/queries/get-visitors`.
- SPEC-002 ㉔ — 원천 경로 · 매핑 · upsert · 소프트 딜리트 · 번들 순서(백필도 같은 규칙).
- 사실 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/kos-sync-research-report.md` Q2(일정 월 단위 · 구매 묶음 87개 · 시술권 고객별 · 카드) · 고객 목록 = 메인 `reference/2026-10-23-cc-overall-board/har/고객정보 수정.har` 등(`visitor/v2/queries/get-visitors` — 요청 `indexOfPage · countInPage · sort{by:lastVisitedDateTimeUtc}` · 응답 `count · data[]`) — HAR 위치 `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-23-cc-overall-board/har/` (개인정보 — 값 옮기지 마라).
- 앞 단계 코드: 2단계 동기화(`be-2-report.md` · 리뷰 3 · 4) — **같은 upsert · 매핑 함수를 재사용**한다(새 쓰기 경로 금지).

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

새 테이블은 오늘 데이터 · 메뉴만 동기화로 채워진다. 지난 구매 · 시술권 · 카드 이력을 한 번에 채우는 백필을 만든다. 이걸로 2단계의 「출처 구매 항목 없어 건너뛴 지난 시술권」도 풀린다.

**지킬 것**
1. **상용 서비스 중** — 백필은 운영 동기화와 **같은 프로세스 · 스케줄에 붙이지 않는다**(수동 실행). 오늘 창(10초 루프 몫)은 건드리지 않는다 — **어제까지만**. 기존 판 · 동기화 결과가 같아야 한다.
2. **KOS 1초 1회** — 모든 KOS 호출 사이 ≥ 1.0초(재시도 포함). 429 · 5xx 는 기다렸다 재시도(상한). 공개 API 0.
3. **KOS 세션** — `KOS_CLIENT_TAG=backfill`(운영과 다른 표시). 기기 제한이면 **이 표시 세션만** 가장 오래된 것 해제. 끝나면 자기 세션 해제. 운영 · 사람 세션 해제 금지.
4. **소프트 딜리트만** · 물리 DELETE 금지 · 다시 돌려도 결과 같음(멱등).
5. 개인정보 — 로그 · 출력에 이름 · 전화 · 차트번호 · 메모 · KOS id · 토큰 금지(건수 · 단계 · 진행 위치만).

## 3. 계약

- 순서: ① 일정 **월 단위** `get-schedules-grouped-by-zone`(구역 = 내부 get-zones) → 방문 · 작업 · 처방(기존 일정 반영 함수 — 지난 창으로) ② 모은 `purchaseIds` → `get-purchase-summaries` 묶음(`includeDeleted:true`) → 구매 · 항목(items + pendingItems) · 거래 · 담당 · 조정 ③ 구매가 있는 고객 → `get-ticket-bundles` ④ 고객 목록 `get-visitors` 전체 페이지 → 고객마다 `get-prepaid-card-summaries` → 카드마다 이벤트 · 공유 고객. (고객 자체 upsert 는 기존 고객 동기화 규칙대로 — 새 칸 · 새 규칙 금지.)
- 인자: `--hospital <id>` · `--from YYYY-MM` · `--to YYYY-MM-DD`(기본 어제 · 오늘 이상 거부) · `--stage schedules|purchases|tickets|cards|all` · `--dry-run`(KOS 는 읽고 DB 는 안 씀 · 건수만) · `--resume`(진행 위치부터).
- 진행 위치: 단계 · 월 · 페이지 · 고객 커서를 저장(기존 관례 — Redis 또는 파일; 새 테이블 금지). 끝에 요약(단계별 받은 · 쓴 · 건너뛴 · 소요).
- 마이그레이션: `visit (hospital_id, reserved_start_at)` 인덱스(부분 `deleted_at IS NULL` 관례 따름) — **0010 에 넣는다**(아직 어디에도 적용 안 됨). 기존 테이블 인덱스 추가는 이것 하나만(SPEC-000 OQ-00-3 메모 근거).

## 4. 먼저 읽을 핵심 파일

- 2단계 동기화 코드 전부(`backend/day/emr/sync_*` · `services/emr_sale_sync.py` · `emr/kos/sale_reads.py` · `tasks/emr.py`) · 기존 일정 반영(`sync_schedules.py` — 창 · `mark_absent(within=…)`).
- KOS client(1초 간격을 어디서 강제할지 — 백필 전용 래퍼 권장 · 운영 client 동작은 바꾸지 마라).
- `scripts/` · 기존 관리 명령 관례 · `docs/development/deployment.md`(dev VM 에서 1회 실행하는 방법을 리포트에 적기 — 실행은 하지 마라).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)` — **이번엔 지정한다**: 백필 실행 진입점을 `scripts/` 관례(또는 `backend/day/…` 명령 모듈 — 관례를 보고 고른다)에 둔다

## 6. 구현 단계

1. `git fetch origin dev` — 나아갔으면 rebase.
2. 백필 모듈 + 실행 진입점 + 1초 간격 래퍼 + 진행 위치 + 인자.
3. 0010 에 `visit` 날짜 인덱스.
4. 테스트 — 1초 간격(가짜 시계) · 어제까지(오늘 거부) · dry-run 은 DB 쓰기 0 · resume · 멱등(두 번 돌려 쓴 행 0) · 세션 표시 · 소프트 딜리트 · 기존 판 결과 같음.
5. **로컬 실물(DEMO)** — 버리는 컨테이너 · 테스트 계정 · DEMO 테넌트만(이전과 같은 방식) · `--dry-run` 한 번 → 실제 한 번 → 다시 한 번(쓴 행 0 확인) · 2단계에서 건너뛴 지난 시술권이 풀리는지 · 소요 시간 · 호출 수. 세션 해제.
6. dev 서버 드라이런 · 실행 **방법만** 리포트에(명령 · 환경 · 예상 시간) — 서버 실행은 코디 · 사용자가 한다.
7. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/be-3-report.md`.

## 7. 범위 제약 — 하지 말 것

- 운영 스케줄에 백필 붙이기 · 오늘 창 쓰기 · 공개 API · 새 테이블(진행 위치용 포함) · 기존 동작 변경.
- dev · prod 서버 접속 · 실행 · 공유 DB.
- 커밋 · push · PR.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from term_bbe79944-22d5-4480-8435-1776c9ea2198 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
