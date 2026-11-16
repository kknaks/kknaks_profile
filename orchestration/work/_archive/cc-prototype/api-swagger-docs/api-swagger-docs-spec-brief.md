# [planner] SPEC-008 · WORK-012 — 시술 · 상품 메뉴 저장 + 외부 연동 API(DEC-010)

너는 **cc-prototype `planner` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2` (코디 워크트리 탑승 — 코디와 같은 트리. 브리프가 지정한 파일만 쓴다)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- **`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md`** ← 계약의 SoT(accepted · D-01 ~ D-34 · 열린 것 0). **여기 없는 정책은 발명하지 마라.** DEC 에 없는데 SPEC 에 꼭 필요한 값이 나오면 지어 넣지 말고 §9 (2) 로 코디에게 물어라
- 결정 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/_RESUME.md` §2
- KOS 사실(조사 리포트 4개 — 같은 폴더):
  - `research-procedure-menu.md` — 메뉴 작업별 키 트리 · 관계 · 가격 · 상태 · 크기 · 스펙과 실제 차이(§1 ~ §7)
  - `research-purchase-snapshot.md` — 고객 → 수납 → 시술권 → 작업 연결 키 · `getTicketBundlesQuery` 모양 · 상태
  - `research-har-product-edit.md` — 가격 수정 뒤 산 값 유지 · 옵션 id 유지
  - `research-name-email-lookup.md` — 내부 `get-visitors` 이름 검색 성질 · email 칸 · 페이징(`count` · `countInPage`) · 호출 순서 · 비용
- KOS 참고: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/reference/2026-10-12-cc-prototype/kos-demo-api.md`
- 형식 모범: 같은 폴더 `20-spec/spec-005-reservation-board.md`(back 계약 · KOS 연동 · 데이터 모델 절 구성) · `30-work/work-011-internal-chat.md`(WORK 모양)

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

협업자의 외부 시스템(링키 · 차티)이 상담 중에 상품 가격과 기존 고객의 남은 시술권을 보고, **고객 이름 + 이메일**로 조회 · 예약해야 한다. 지금 `procedure/back` 에는 메뉴(시술 · 상품) API 가 없다. 고객 검색은 직원 로그인 전용이고, 이름 · 전화 · 생년월일 · 차트번호로만 찾는다. DEC-010 이 정한 것은 셋이다. ① KOS 메뉴 전부를 DB 에 저장, ② 외부 연동 API `/api/ext/…`(메뉴 · 고객 조회 · 예약), ③ 연동처별 API 키 인증. 이 셋을 back 이 구현할 수 있는 계약(SPEC-008)과 작업 순서(WORK-012)로 만든다.

## 3. 계약 (다른 워커와 합의됨)

해당 없음 — 이번 산출물이 계약이다. 화면(front · app)은 범위 밖이다(D-01).

## 4. 먼저 읽을 핵심 파일 (코드 레포 canonical — **읽기만**, `/Users/kknaks/git/toy_pr2/cc-prototype` = main `c9f30ac`)

- `procedure/back/app/repository/db.py` — SQLite `SCHEMA`(D-04 저장 모양이 따를 규약: 시각 UTC ISO 문자열 · json 열 = 문자열 · `kos_id` UNIQUE · `synced_at` · `present`)
- `procedure/back/app/kos/sync.py` · `app/kos/runtime.py` — 마스터 루프 `sync_master` · `master_once` · `kos_poll_master_sec`(D-06 이 얹을 자리)
- `procedure/back/app/kos/client.py` — `open()` · `internal()` 호출 방식 · 토큰
- `procedure/back/app/service/reservations.py` — `PATH_VISITORS`(약 78줄) · `search()`(약 437 ~ 469줄 · `countInPage:20` = D-16 이 고칠 곳) · `personal_of()` · 예약 생성(약 780 ~ 890줄 · `_check_identifiable`)
- `procedure/back/app/schemas/reservations.py` — `NewCustomer` · `CreateReservationRequest`(약 470 ~ 506줄)
- `procedure/back/app/domain/reservation_rules.py` — `identifiable()`(약 249줄 · D-32 근거) · 기본 구역 규칙
- `procedure/back/app/api/deps.py` — `require_login` · `require_real_board`(D-10 직원 인증과 외부 키를 섞지 않는 근거)
- `procedure/back/app/config.py` — 설정 · env 이름 규약(D-23 키 · D-33 기본 그룹이 들어갈 자리)
- `procedure/back/app/openapi_docs.py` · `tests/test_openapi_docs.py` — Swagger 규약(새 엔드포인트도 설명 · 오류 표 · security 표시를 따라야 한다. 외부 키는 별도 securityScheme)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/cc-prototype/20-spec/` — 새 `spec-008-product-ext-api.md` + `README.md` 인덱스 행
- `para/projects/summer-star/cc-prototype/30-work/` — 새 `work-012-product-ext-api.md` + `README.md` 인덱스 행
- DEC-010 의 frontmatter `links.specs` · `links.works` 와 `10-decision/README.md` 의 DEC-010 행 Spec 칸 — **링크만** (본문 수정 금지)

## 6. 할 일

1. **SPEC-008** (`version 0.1.0 · status draft`) — 절 구성 제안(모범 SPEC-005 를 따르되 이 기능에 맞게):
   1. 범위 In / Out(D-01 · D-02 · D-12 의 「내주지 않는 것」)
   2. 데이터 모델 — 메뉴 표들(D-03 ~ D-05 · D-07): 표 · 칸 · 키 · 원본 JSON 열 · 「없음」 표시 · KOS 필드 대응표. 외부 호출 기록 표(D-24 — 원문 이름 · 이메일 없음)
   3. KOS 연동 — 메뉴 동기화(D-05 · D-06 · 작업 목록 · 호출 순서 · 실패 시 이전 값 유지 여부는 지금 `sync_master` 동작을 따른다) · 이름 검색 페이징(D-16) · 시술권 조회(D-12)
   4. 조회 규칙 — D-15 ~ D-22 를 단계 순서로(이름 다듬기 → 검색 → email 정규화 · 대조 → 0 / 1 / 2+ 갈래)
   5. 외부 API — 엔드포인트 셋(D-11 · D-27 ~ D-33): 경로 · 메서드 · 요청 · 응답 필드(이름 · 타입 · 뜻 · null 뜻) · 오류 표(없음 · 특정할 수 없음 · 인증 실패 · 429 · KOS 실패 · 정원 등 — 지금 back 오류 형식 `{"error":{code,message}}` 과 400 `invalid_request` 규약을 따른다)
   6. 인증 · 보안 — 연동처별 키 전달 방식(헤더 이름) · env 이름(**이름만**, 값 0) · 직원 API 와의 분리(D-10) · 호출 제한(D-34) · 기록(D-24) · admin 공유 회수는 사용자 몫(D-26)
   7. Swagger — 외부 API 를 문서에 싣는 방식(별도 tag · securityScheme)
   8. 시험 기준 — 계약마다 어떤 시험으로 고정하는지
   - 모든 절에 근거 DEC D-번호를 단다. DEC 에 없는 세부(헤더 이름 · 경로 이름 · 표 이름 · 오류 code 문자열)는 **지금 코드 규약에서 끌어와 정하고 근거를 「코드 규약: 파일:줄」로 적는다.** 규약으로도 안 정해지는 정책은 §9 (2) 로 묻는다
2. **WORK-012** — SPEC-008 을 구현할 WP 순서(예: 메뉴 저장 · 동기화 → 외부 인증 · 기록 · 제한 → 메뉴 API → 고객 조회 → 예약 → Swagger · 시험). WP 마다 범위 · 완료 조건 · 검증(관련 시험만 · 전체 `pytest` 는 마지막 한 번) · 실물 확인 1회(데모 KOS 로 이름+이메일 조회 · 예약이 실제로 되는지 — 실물 e2e 없이 done 금지)
3. 인덱스 · 링크 갱신(§5)

## 7. 범위 제약 — 하지 말 것

- 코드 수정 · 커밋 · push · PR 금지. 코드 레포는 읽기만
- KOS 호출 금지(이번 일은 문서다 — 사실은 조사 리포트에서 가져온다)
- DEC-010 본문 수정 금지 · 새 정책 발명 금지 · 「열린 것」 새로 만들지 않기(DEC 는 열린 것 0 으로 닫혔다. 필요하면 묻는다)
- public 레포 — 키 · 토큰 · 실명 · 이메일 · 연락처 · KOS id 값 0. 예시 값은 자리표시(`a@example.com` · `<이름>`)

## 8. 검증

```
SPEC 의 모든 절이 DEC · workflow · 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 실명 0(grep)
```

- DEC-010 D-01 ~ D-34 가 SPEC 어디에 반영됐는지 대조표(D 번호 → SPEC 절)를 SPEC 끝에 둔다. 빠진 D 0
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> \
  --dispatch-id <이 태스크의 dispatchId> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / DEC 대조 / 주의점"

# (2) 직접 주입
orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --text "[질문] planner: <질문>" --enter`
