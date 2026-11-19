# [backend] 2단계 — KOS → DAY 동기화(메뉴 1시간 · 오늘 10초 · 5분 회차 · upsert/소프트 딜리트)

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

너는 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. base = origin/dev `bbd9220a`(코디가 발주 직전 fetch 한 최신). **시작 전에 `git fetch origin dev && git log -1 origin/dev` 로 dev 가 더 나아갔는지 보고, 나아갔으면 rebase 한 뒤 시작해라**(사용자 규칙: 코드 작업 전 dev 최신).

## 1. SSOT — 먼저 읽을 것

- **계약**: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉔ 「KOS 읽기 — 새 테이블 동기화」 전부(루프 표 · 원천 표 · 바뀐 것만 · upsert/사라짐/삭제 · 매핑 표 · entity_type · 환경 · 번들 순서) + §5 OQ-69~75(기본값). 칸은 `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec/products/day/20-spec/spec-000-data-model.md` §4. **여기 없는 경로 · 필드 · 정책을 만들지 마라.**
- **사실 원천**: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/kos-sync-research-report.md`(실호출 경로 · 요청 키 · 응답 키 · 건수) · `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report{,-2,-3}.md`(응답 모양).
- Delivery Issue `gh issue view 259 -R MediSolveAIDev/CENTURION_DAY` — 이번 몫 D-2(매핑) · D-3 · D-4 · D-5 · D-6 · A3 · A4 · A5 · A6 · A7.
- 앞 단계: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/be-1-report.md`(모델 · enum · entity_type) · `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-code-1-report.md` · `review-code-2-report.md`(있으면).
- 지금 동기화 코드: `backend/day/emr/`(base · normalized · factory · kos/client · kos/mapper · sync) · `backend/day/tasks/emr.py` — **이 구조와 관례를 그대로 따른다**(새 계층 금지).
- 결정 원장: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/_RESUME.md` §2.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

1단계에서 테이블을 만들었다. 이제 **KOS → DAY 동기화**로 채운다(원장 전환 전). 백필 · DAY → KOS 쓰기 · 화면은 범위 밖.

**지킬 것 (사용자 · 모든 줄의 기준)**
1. **상용 서비스 중** — 지금 10초 일정 동기화 · 1시간 기준 정보 동기화가 prod 에서 돈다. **새 동기화가 실패해도 기존 동기화(시술현황 판)가 멈추면 안 된다** — 새 부분은 기존 회차와 실패가 격리되게(예외 · 트랜잭션 · 타임아웃) 붙인다. 기존 함수의 동작 · 반환 · 호출 수를 바꾸지 마라(더하기만).
2. **KOS 뗄 것** — KOS id 는 `external_ref` 에만. KOS 문자열 → DAY enum 은 매핑 한 곳에서.
3. **삭제는 소프트 딜리트만** — 물리 DELETE 금지. 별도 삭제 로그 없음(사용자).
4. 호출 간격 · 묶음 크기는 조사 리포트 수준. KOS 부하를 늘리는 「매 회차 전체 재조회」 금지(바뀐 것만 — ㉔).

## 3. 계약

SPEC-002 ㉔ 그대로. 요약(틀리면 SPEC 이 이긴다):
- 메뉴 1시간: 카테고리 · 상품(옵션 · 가격 · 구성 · 진료항목 연결 — **내부** `get-products`) · 시술 · 진료항목 · 약품 · 기기(공개 메뉴 API) · 선불카드 상품 · 시술 외 품목 · 기타 작업(내부).
- 오늘 10초: 이미 받는 일정 목록의 `purchaseIds` → 내부 `get-purchase-summaries` 묶음(`includeDeleted`) · 구매 · 항목 · 거래 · 담당 · 조정 · 처방(`prescriptionIds`) · `visit_task.ticket_id`(`ticketConfiguration.ticketId`) · `treatment_item_id` · `machines`. 시술권(`get-ticket-bundles`) · 카드(`get-prepaid-card-summaries` · 이벤트 · 공유 고객)는 **바뀐 고객만**.
- 5분: 공개 통계(거래 · 카드 이벤트 · 구매 항목) 「지난 회차 이후」 → id 모으기 → 내부 원장 API 로 다시 받기. 「지난 회차 시각」을 어디에 둘지는 기존 관례(Redis · 서버 상태)를 따른다 — 새 테이블 금지(마이그레이션 0010 은 칸 보강 외 변경 금지).
- upsert · 사라짐: 기존 `external_ref` · `mark_absent(within=…)` 관례. 번들은 「옛 번들 삭제 표시 → 새 번들 생성」 순서(유일 제약).

## 4. 먼저 읽을 핵심 파일

- `backend/day/tasks/emr.py`(회차 · 스케줄 등록) · `backend/day/emr/sync.py`(`_apply_*` · `mark_absent` · `lock_visits`) · `backend/day/emr/kos/client.py`(내부 · 공개 호출 · 헤더) · `mapper.py` · `normalized.py` · `base.py`(어댑터 인터페이스 · 지원 여부) · 기존 동기화 테스트(`backend/tests/day/emr/…` 등 — 찾아서 관례 따라).
- 테스트용 KOS 응답 모양: HAR 리포트의 키 구조로 **가짜 값** 픽스처를 만든다(실제 이름 · 전화 · id 금지).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)`

## 6. 구현 단계

1. `git fetch origin dev` — 나아갔으면 rebase.
2. normalized · mapper — 메뉴 · 구매 · 시술권 · 카드 · 처방 KOS 응답 → 우리 형식 + 매핑 표(KOS 값 → DAY enum · 매핑 밖 값 = 건너뛰고 셈 · OQ-70).
3. client — ㉔ 원천 표의 경로만(내부 · 공개 구분 · 요청 키 그대로).
4. sync — `_apply_menu` · `_apply_purchases` · `_apply_tickets` · `_apply_prepaid_cards` 류(이름은 관례대로) · external_ref 연결 · 사라짐 · 소프트 딜리트 · 번들 순서 · 방문 없는 구매 건너뜀(OQ-69).
5. tasks — 1시간 회차에 메뉴, 10초 회차에 오늘 구매 · 바뀐 고객 시술권 · 카드, 새 5분 회차. **기존 회차 실패 격리.**
6. FK 인덱스 — 2단계 조회(external_ref 연결 · 고객별 · 방문별)에 실제로 쓰는 FK 에만. 0010 에 넣는다(아직 어디에도 적용 안 됨). 넣은 것과 이유를 리포트에.
7. 테스트 — 매핑(값별) · upsert(새로 · 바뀜 · 사라짐 · 되살림) · 바뀐 고객만 · 번들 순서 · 기존 회차 격리(새 부분이 예외를 내도 일정 동기화 결과가 같음) · 물리 DELETE 0(grep).
8. **DEMO 실물 확인(A3 · A4)** — 로컬 스택만. KOS 연결은 **사용자 테스트 계정**(`~/.config/day/kos-test-account.env` · 값 출력 금지)으로 `hospitalName` 이 DEMO 인 테넌트만. **데모 시스템 계정 · 실 명동점 금지.** `KOS_CLIENT_TAG=local`. 메뉴 회차 1번 · 오늘 회차 1번 돌려 테이블 건수(메뉴 · 오늘 구매 · 시술권 · 카드)와 판 화면이 그대로인지 확인. 사용자 포트 · 프로세스는 건드리지 않는다(다른 포트로). 못 하면 이유와 함께 pending.
9. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/be-2-report.md` — 바꾼 파일 · ㉔ 줄 → 코드 대응 · 테스트 수치 · DEMO 건수 · 남은 위험.

## 7. 범위 제약 — 하지 말 것

- 백필 · DAY → KOS 쓰기 · 화면 · 라우터 · 감사 로그.
- 기존 동기화 함수의 동작 변경 · 기존 테이블 변경 · 0010 의 칸 변경(FK 인덱스 추가만 허용).
- SPEC 에 없는 경로 · 필드 · 정책(막히면 「[질문]」).
- 커밋 · push · PR · 공유 DB · dev/prod 서버.

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
