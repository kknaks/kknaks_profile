# [researcher] 4차 — KOS → DAY 동기화 조사 (API · 백필 · 변경 감지) — 테스트 계정 실호출

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터와 같은 워크트리다. 리포트 파일 1개 말고 레포 안에 아무 파일도 만들거나 고치지 마라. 호출 스크립트 · 응답 원문은 scratchpad(레포 밖)에만 둔다. 너는 맥락이 없다 — 아래 파일이 전부다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec/products/day/20-spec/spec-000-data-model.md` §4(새 테이블 칸 표 · 「외부(KOS)」 열 = 각 칸의 KOS 필드) · §6 OQ-00-2 · 00-3(원장 전환 · 백필) ← **동기화 대상의 SoT**(PR #951).
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report.md` · `-2.md` · `-3.md` — HAR 에서 이미 본 경로 · 요청 · 응답 모양. 다시 하지 말고 출발점으로.
- 원본 HAR: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/har/*.har` (개인정보 — 값 옮기지 마라).
- 지금 DAY 동기화 코드(읽기만): `git -C /Users/kknaks/git/CENTURION_DAY show origin/prod:backend/day/tasks/emr.py` · `backend/day/emr/sync.py` · `backend/day/emr/kos/client.py`(sign-in · 내부 헤더 · `web_user_agent(tag)` · `list_active_sign_ins` · `revoke_active_sign_in`) · `backend/day/emr/kos/mapper.py`.
- KOS 공개 API 문서: `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` · 원본 `https://developers.kos-solution.com/openapi.yaml`(읽기만).

## 2. 배경

PR #951 로 메뉴 · 구매 · 시술권 · 선불카드 · 처방 테이블이 정해졌다. 원장 전환(예약 구현) 전까지는 이 테이블을 **KOS → DAY 동기화 + 지난 이력 백필**로 채운다. 동기화 스펙(SPEC-002 개정)을 쓰기 전에 「무엇을 · 어느 API 로 · 얼마나 자주 · 변경을 어떻게 알아채나 · 지난 이력을 어떻게 다 가져오나」를 실물로 확인한다.

조건(사용자 11-18): 상용 서비스가 이미 돈다 · 나중에 KOS 를 뗀다 — 그래서 동기화는 지금 10초/1시간 루프에 **더하는** 모양이어야 하고, 내부 API 의존(브라우저 UA 필수 · 언제든 막힐 수 있음)은 공개 API 로 되는 게 있으면 그쪽을 우선한다.

## 3. 계정 · 호출 규칙 — 반드시 지킨다

- **계정: 테스트 계정만.** 값은 `~/.config/day/kos-test-account.env`(`KOS_TEST_EMAIL` · `KOS_TEST_PASSWORD`). **값을 출력 · 로그 · 리포트 · 스크립트 파일에 쓰지 마라** — 실행 때 env 로 읽기만.
- **쓰면 안 되는 계정 · 키**: `KOS_SYSTEM_EMAIL/PASSWORD`(데모 지점 시스템 계정 — DAY 서버가 실사용 중) · `KOS_API_tenent`(명동점) — **절대 금지.** 공개 API 가 필요하면 `KOS_API_tenent_dev`(데모 지점 open-api 키 — 로그인 세션을 안 쓴다) 만.
- **테넌트 확인 먼저**: 테스트 계정으로 sign-in → `get-user-account` → 접근 테넌트가 **데모 지점(`KOS_API_tenent_dev` 의 테넌트)인지** 확인. 아니면(명동점 등 실 데이터) **고객 데이터 조회 전에 멈추고** 코디에게 물어라.
- **헤더**: 내부 API 는 KOS 웹과 같은 User-Agent · Origin · `kos-client-uri`(본: CENTURION_DAY `client.py` 의 내부 헤더). UA 끝에 ` (research)` 표시.
- **기기 5대 제한**: sign-in 이 401 `SignInLimitExceeded` 면 `get-active-sign-ins` → **UA 끝이 ` (research)` 인 네 세션만** 가장 오래된 것 하나 `revoke-active-sign-in` → sign-in 한 번 더. 네 표시가 아닌 세션(사람 · DAY 서버)은 **해제하지 말고 멈춰서 물어라.** 토큰은 한 번 받아 재사용 — sign-in 을 반복하지 마라(세션이 쌓인다).
- **호출은 조회(queries)만.** commands 는 위 `revoke-active-sign-in`(네 세션) **하나만** 예외. 생성 · 수정 · 삭제 · 결제 · 단계 변경 금지.
- 부하: 호출 사이 간격을 두고(≥ 0.3초) · 백필 가능성 확인은 페이지 몇 장까지만(전체를 긁지 마라).

## 4. 입력

위 §1 · 테스트 계정 실호출.

## 5. allowed_paths

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/kos-sync-research-report.md`
- 스크립트 · 응답 원문: 세션 scratchpad(레포 밖)만. 끝나면 응답 원문 파일은 지운다.

## 6. 할 일

- **Q1 테이블별 원천 API 표** — SPEC-000 §4 새 테이블 각각(메뉴 16 · 구매 5 · 시술권 3 · 선불카드 3 · 처방 1): 경로 · 공개/내부 · 요청 키(필터 · 페이지) · 응답 키가 칸 표 「외부(KOS)」 열과 맞는지 · 단위(병원 전체 / 고객별 / 구매별). HAR 에 있던 경로는 실호출로 확인, HAR 에 없는 것(예: `get-procedure-categories` · 약품 · 기기 목록 · 시술권 조회 경로)은 openapi · HAR 경로 이름으로 찾되 **경로를 지어내지 마라** — 못 찾으면 「확인 안 됨 + 필요한 HAR(화면 동작)」.
- **Q2 백필** — 고객 전체 이력을 가져오는 길: 날짜 범위 · 커서로 구매 · 시술권 · 선불카드를 **병원 전체** 로 나열하는 API 가 있나. 없으면 고객별(`visitorId`)로만 되는지 · 고객 목록을 다 도는 비용(고객 수 · 호출 수 추정). 일정(방문) 백필 경로(지난 일정 조회)도 — `purchase.visit_id` NOT NULL 이라 방문 먼저.
- **Q3 변경 감지** — 각 API 의 `lastUpdatedDateTimeUtc` · 커서 · `includeDeleted` · 삭제 표시. 「바뀐 것만」 받을 길이 있나 · 지운 것을 어떻게 알아채나.
- **Q4 지금 루프에 붙이기** — `tasks/emr.py` 10초(오늘 일정) · 1시간(기준 정보) 루프에 어떤 호출을 더하면 되나: 오늘 일정의 `purchaseIds` → 구매 · 오늘 고객 → 시술권 · 선불카드 · 메뉴 → 1시간. 호출 수 추정(오늘 일정 N 일 때).
- **Q5 공개 API 대체** — 위 중 공개 API(open-api · 키 방식 · 세션 없음)로 되는 것. 되면 내부 API 의존을 줄인다.
- 리포트 끝: 「동기화 스펙에서 정할 것」(결정 금지) · 「확인 안 됨 — 필요한 HAR」 표 · 개인정보 점검(grep 결과).

## 7. 범위 제약

- 결정하지 마라 — 정할 것으로 모은다. DAY 코드 · 문서 수정 금지. 커밋 금지.
- 리포트에 고객 이름 · 전화 · 차트번호 · 메모 · 직원 실명 · 토큰 · 계정 값 · 테넌트 id · KOS 문서 id 를 쓰지 마라 — 경로 · 키 이름 · 타입 · 건수만.

## 8. 검증

- 실호출마다 경로 · HTTP 상태 · 건수를 리포트 표에.
- `grep -nE '01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}|Bearer|@medisolveai' kos-sync-research-report.md` 0 건(명령 줄 자신 제외).
- 끝에 네가 만든 KOS 세션을 남겨도 되는지 · 해제했는지 한 줄.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from term_62a00765-d9eb-4449-b881-bbf998990151 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
