
# [frontend] WORK-002 검수 FAIL 수정 — F-3 로그아웃 결함 · F-2 프론트 테스트

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**네가 만든 WORK-002 Phase 2·3(`c49ae72`)이 검수에서 FAIL 을 받았다.** 그 두 건을 고친다.
**F-1(.env.example 자격증명)은 코디가 이미 되돌렸다** — 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

**검수 리포트 — 이번 작업의 출발점**
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work-002-review-report.md`
  — **F-2 · F-3 행을 그대로 읽어라.** 무엇이 어긋났고 어떻게 고치라는지가 거기 있다

**계약**
- `para/projects/summer-star/task-management/20-spec/spec-001-auth-session.md` — §4 API·Flow · §5 로그아웃 · §6 Acceptance
- `.../40-architecture/frontend/README.md` — **§11 반드시 있어야 하는 테스트** · §4-1 토큰 저장소(**2026-09-05 개정 — 브라우저 폴백 폐기**) · §4-2 요청 파이프라인
- `.../30-work/work-002-auth-session.md` — Phase 2·3 · Done Criteria

## 2. 무엇을 고치나

### F-3 — 로그아웃이 서버 세션을 끊지 못한다 **(먼저 고쳐라)**

`session.ts:83` 이 요청을 만들기 **전에** `tokenStore.get()` 으로 refresh(`R1`)를 캡처한다.
그 뒤 `apiFetch("/api/auth/logout")` 가 access 만료를 만나면 **파이프라인이 먼저 갱신을 태워 `R1 → R2` 로 회전**시킨다(`client.ts:211`).
본문에는 여전히 `R1` 이 실려 나가고, 서버는 `R1.revoked_at` 이 이미 찍혀 있어 **아무것도 하지 않고 204** 를 준다.

**결과: 사용자는 「로그아웃 완료」로 보이지만 `R2` 세션이 서버에 7일간 살아 있다.**
access 가 없는 경로(`client.ts:194`)도 같다. SPEC-001 S-5 「앱을 1시간 이상 켜 둔 뒤 조작」이 바로 이 상태다.

**고치는 방향** — 「보낼 refresh 를 **파이프라인이 갱신을 끝낸 뒤에** 읽는다」로 순서를 뒤집는다.
최소 수정은 `client.ts` 가 유효 access 를 확보하는 지점을 함수로 빼서(`ensureAccessToken()`),
`session.logout()` 이 그것을 **먼저 `await` 한 다음** `tokenStore.get()` 을 읽는 것이다.
대안은 `apiFetch` 에 「본문을 요청 직전에 만드는 콜백」을 허용하는 것.

> **서버를 고쳐 무효 토큰의 후속 회전 사슬까지 끊는 방식은 쓰지 마라** — A-7 재사용 감지와 구분이 안 되고,
> 로그아웃이 「이 세션만」이라는 SPEC-001 §5 계약을 넘는다. **`app/back` 을 건드리지 마라.**

### F-2 — 프론트 테스트가 하나도 없다

러너·라이브러리조차 없다(Vitest·RTL·MSW 어느 것도 `devDependencies` 에 없고 `test` 스크립트도 없다).
`frontend/README.md` §11 이 「없으면 리뷰 반려」로 못박은 필수 테스트 중 **WORK-002 범위 4건이 전부 빠졌다**:

| # | 무엇을 검증하나 |
|---|---|
| ④ | **401 갱신** — refresh 1회 → 재시도 → 두 번째 401 이면 로그인 화면. **루프가 없다** |
| ⑤ | **토큰 저장소 격리** — `persist=false` 로 로그인하면 저장소에 **아무것도 남지 않는다** |
| ⑦ | **v2 게이트** — 조작해도 **네트워크 요청이 나가지 않는다** |
| ⑧ | **정적 빌드 산출** — `out/` 에 Route Handler·미들웨어·`[…]` 없음 |

**Vitest + RTL + MSW** 를 붙인다(§11 이 지정한 조합). `tokenStore` 가 `invoke` 를 직접 물고 있으므로
`@tauri-apps/api/core` 는 **모듈 목**으로 세운다. ⑦ 은 `V2Gate` 로 감싼 버튼 클릭 시 MSW 핸들러가
**호출되지 않음**을 단언한다. ⑧ 은 `next build` 후 `out/` 트리 검사 스크립트로도 성립한다.

**F-3 을 고친 뒤 ④ 에 「로그아웃이 회전 뒤에도 서버 세션을 끊는다」를 추가하라** — 같은 결함이 다시 나면 테스트가 잡게.

## 3. 함께 고칠 것 — WARN 2건

검수 리포트의 WARN 표를 보고 아래 둘만 고친다(나머지 2건은 코디가 처리):

- **타이포에 임의 크기를 쓴 곳** → 토큰으로
- **카드 `radius` 가 12** → SPEC 은 **16**

## 4. allowed_paths — 이 밖은 건드리지 마라

- `app/front/` — 전부(`package.json`·테스트 설정 포함)

**`app/back/` 을 건드리지 마라.** 문서 레포도 **읽기 전용**이다 — 틀렸으면 보고한다.
**커밋·push·PR 하지 마라.**

## 5. 구현 단계

1. 역할 문서 → **검수 리포트 F-2·F-3 행** → SPEC-001 §4·§5 → `frontend/README.md` §11·§4-1·§4-2.
2. **F-3 을 먼저 고치고 재현으로 확인한다**(§6).
3. 테스트 러너를 붙이고 ④⑤⑦⑧ 을 쓴다. ④ 에 로그아웃 케이스를 포함한다.
4. WARN 2건 정정.
5. 검증(§6) → 완료 보고(§7).

## 6. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러) + npm test (네가 쓴 테스트만). 정적 빌드 제약 자기점검 — 동적 세그먼트 0 · 모든 page 에 'use client' · 컴포넌트 hex 리터럴 0 · tokenStore 밖에서 키체인/localStorage 호출 0. 전체 빌드 금지, 검증은 1회만
```

**F-3 은 반드시 실물로 재현·확인해라** — 리포트 §코디 실행 요청 3번이 방법을 적어놨다:

1. `ACCESS_TOKEN_TTL_MIN=1` 로 백엔드를 띄운다(`make up`·`migrate`·`seed` — 시드 값은 **네 `.env` 에** 채운다. `.env.example` 은 비어 있는 게 맞다)
2. 앱에서 로그인 → **1분 이상 기다려 access 를 만료시킨다** → 로그아웃
3. 그 과정에서 회전된 **refresh 로 `POST /api/auth/refresh`** 를 부른다
4. **401 이면 고쳐진 것이다. 200 이 오면 아직 새는 것이다** — 고칠 때까지 반복한다

보고에 **고치기 전 200 → 고친 뒤 401** 을 수치로 적어라.

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
