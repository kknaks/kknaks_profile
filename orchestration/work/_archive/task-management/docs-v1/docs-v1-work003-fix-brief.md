
# [frontend] WORK-003 검수 FAIL 수정 — U-7 자동저장 실패 표시를 밖으로 끌어낸다

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**네가 만든 WORK-003 Phase 2·3(`8e17d0b`)이 검수에서 FAIL 1 · WARN 7 을 받았다.**
**선행 조건이던 문서 공백(G-12)은 코디가 방금 닫았다** — SPEC-002 U-7 에 팝오버형 컨트롤 규격이 생겼다(`4050912`).

## 1. SSOT — 먼저 읽을 것

**검수 리포트 — 이번 작업의 출발점**
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work-003-review-report.md`
  — **F-1 행과 WARN 표를 그대로 읽어라.** 무엇이 어긋났고 어떻게 고치라는지가 거기 있다

**계약**
- `para/projects/summer-star/task-management/20-spec/spec-002-work-settings.md` — **§2 U-7**(방금 팝오버 규격이 추가됐다) · U-3 · §4 Case Matrix 마지막 행 · U-8 반응형
- `.../40-architecture/frontend/README.md` — **§3-5 자동 저장 컴포넌트는 실패 상태 prop 을 공통으로 갖는다** · §5-3 색 렌더 · §11 테스트
- `.../30-work/work-003-work-settings.md` — §Internal Interface Contract 자동 저장 실패 표시 행 · Done Criteria

## 2. 무엇을 고치나

### F-1 — 자동 저장 실패 표시가 컴포넌트 안에 갇혔다

색 트리거는 U-3 이 「고르면 **즉시 저장**」으로 못박은 **자동 저장 컨트롤**인데,
`saveColor` 는 실패를 잡아 토스트만 띄우고 **재전파하지 않으며**(같은 자리의 `saveName` 은 `throw` 한다),
`ColorPickerPopover` 에는 실패 표시를 받을 자리가 없다.

**결과: 서버를 내린 채 색을 바꾸면 토스트가 4초 뒤 사라지고 화면에 아무 흔적이 없다 — 사용자는 색이 저장된 줄 안다.**

**뿌리는 그 위다.** 실패 상태가 `InlineEditText` 의 **내부 state**(`saveFailed`)라서 prop 으로 공유될 수 없고,
그래서 **두 번째 자동 저장 컨트롤이 생기자마자 규격이 새어 나갔다.**

**고치는 방향** — 실패 상태를 **컴포넌트 밖으로 끌어낸다**:

1. `InlineEditText` 의 `saveFailed` 를 **`saveFailed?: boolean` + `onRetry?: () => void` prop** 으로 바꾼다(내부 state 제거)
2. **같은 두 prop 을 `ColorPickerPopover` 도 받는다**
3. 실패 상태의 **소유자는 패널**이다(이미 `rowErrors` 를 들고 있다) — `rowFailures[id][field]` 로 **필드 단위** 관리

그러면 `saveColor` 의 재전파 유무가 규격을 좌우하지 않는다.

**표시 규격은 방금 SPEC-002 U-7 에 추가됐다** — 팝오버형 컨트롤은 **컨트롤 자신에 테두리 실패색**,
**캡션·「다시 저장」은 행 아래 인라인 자리 하나**에 모은다(행 높이 64 를 바꾸지 않는다). 그대로 따르라.

> **이 컴포넌트를 업무·회의·캘린더가 전부 복제한다.** 여기서 닫지 않으면 세 번 더 샌다.

## 3. 함께 고칠 것 — WARN

검수 리포트 WARN 표를 보고 **아래 다섯을 고친다**:

- **팔레트 토큰명이 5곳에 나열**돼 Done Criteria 「두 곳에만」 미충족 → **`tokens.css` 와 서버 두 곳만** 남기고 나머지는 그 하나를 참조하게
- **추가 행 컨트롤 높이가 36/34/32 로 갈림** → SPEC 대로 통일
- **카드 `radius` 12 → 16** (**WORK-002 W-2 재발이다** — 같은 값이 두 번 어긋났으니 토큰으로 고정해 다시 갈리지 않게)
- **추가 행 컴포넌트가 유형·프로젝트에 중복** → 하나로
- **필수 테스트 ③의 토스트 절반 미검증** → 마저 검증

나머지 둘(추가행 재클릭 포커스·저장중 진행표시)은 **판단이 필요하니 손대지 말고 보고만** 하라.

## 4. allowed_paths — 이 밖은 건드리지 마라

- `app/front/` — 전부(`package.json`·테스트 설정 포함)

**`app/back/` 을 건드리지 마라.** 문서 레포도 **읽기 전용**이다 — 틀렸으면 보고한다.
**커밋·push·PR 하지 마라.**

## 5. 구현 단계

1. 역할 문서 → **검수 리포트 F-1 행 + WARN 표** → **SPEC-002 U-7**(팝오버 규격 신설분) → `frontend/README.md` §3-5.
2. **F-1 을 먼저 고친다** — prop 화 → `ColorPickerPopover` 수용 → 소유자를 패널로.
3. **테스트를 추가한다** — 「색 저장 실패 시 화면에 표시가 남고 4초 뒤에도 사라지지 않는다」·「다시 저장이 정확히 1건 나간다」. 같은 결함이 다시 나면 테스트가 잡게.
4. WARN 5건 정정.
5. 검증(§6) → 완료 보고(§7).

## 6. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러) + npm test (네가 쓴 테스트만). 정적 빌드 제약 자기점검 — 동적 세그먼트 0 · 모든 page 에 'use client' · 컴포넌트 hex 리터럴 0 · tokenStore 밖에서 키체인/localStorage 호출 0. 전체 빌드 금지, 검증은 1회만
```

**F-1 은 반드시 앱 창에서 재현·확인해라**:

1. `make up`·`migrate`·`seed` 후 앱을 띄운다(시드 값은 **네 `.env` 에**)
2. **API 를 내린다**(`docker compose -f docker-compose.local.yml stop back`)
3. **색을 바꾼다** → 토스트가 뜨고, **4초가 지나도 화면에 표시가 남아 있어야 한다**(컨트롤 테두리 + 행 아래 캡션 + 「다시 저장」)
4. **이름도 바꿔** 같은 행에 두 필드가 실패하면 **줄이 늘어나는지** 본다
5. API 를 올리고 **「다시 저장」** → 저장되고 표시가 사라지는지, **요청이 정확히 1건**인지(네트워크 탭)
6. 그동안 **자동 재시도가 0건**인지

보고에 **4초 후 표시 잔존 여부**와 **「다시 저장」 요청 수**를 적어라.

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
