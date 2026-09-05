# [reviewer] WORK-004 검수 — 업무 생성·상세 Phase 1~6 (백 + 프론트)

너는 **task-management `reviewer` 워커**다. **read-only.** 먼저 역할 문서를 읽어라 (**문서 레포 절대경로**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main`

**여기서 만든 `DrawerFrame`·업무 도메인·후보 검색 표면을 회의·캘린더·문서함이 전부 쓴다.** 여기가 어긋나면 뒤가 복제한다.

## 1. 검수 대상

**WORK-004 커밋만** 본다 (WORK-001·002·003 은 이미 검수했다). `5bfe012` **다음부터 HEAD 까지**:

- `aec6222` — **Phase 1~3**(backend): 업무 도메인·본체 API·자식 컬렉션(할일·첨부·연관·메모·로그)
- `70924d7` — 연관업무 후보를 **컬렉션 표면**으로 전환(구현 중 드러난 공백)
- `7550e1b` — **Phase 4~6**(frontend): `DrawerFrame`·생성 드로어·상세 드로어·전체 페이지
- 그 뒤 커밋 — **`scope` 필터·`total`**(backend) + **필터 칩 3·카운트**(frontend)

범위 산정: `git diff 5bfe012...HEAD --stat` + `git log 5bfe012..HEAD`.
**작업 트리는 clean 하다** — 커밋된 것이 전부다.

## 2. SSOT — 판정 기준 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

| 층 | 문서 |
|---|---|
| **정책** | `10-decision/decision-002-tasks.md` — **완료 게이트**(결과자료 ≥1 **또는** 완료 결과) · **N:1 무소속 허용** · **소프트 딜리트**(복원 없음) · §6 메모는 로그가 아니다 |
| **아키텍처** | `40-architecture/backend/README.md`(**§3 규칙 7 쿼리 alias — 2026-09-06 신설** · §7 · §8) · `frontend/README.md`(**§6-2 오버레이 3종·드로어 폭**) · `database/README.md` + `domains/task.md` · `system/README.md` |
| **SPEC** | `20-spec/spec-003-tasks-crud.md` — §2 U-1~U-10 · **§4 API 표와 `GET /api/tasks/relations/candidates` 절(2026-09-06 갱신)** · Case Matrix · §6 Acceptance |
| **WP** | `30-work/work-004-tasks-crud.md` — Phase 1~6 체크리스트 + **§Internal Interface Contract** |

**판정은 문서 기준이다.** 취향으로 지적하지 마라.

## 3. 이 검수에서 특히 볼 것

### 드로어 규격 — 이 검수의 핵심

사용자가 **「드로어 폭은 다 통일해야 한다」**고 못박아 아키텍처 §6-2 에 올렸다. 코드가 그걸 **강제**하는지 본다.

- **폭이 한 곳에서만 정해지는가.** `DrawerFrame` 이 폭을 **`prop` 으로 받지 않는가** — 받는 순간 규칙이 무너진다
- **`Sheet`/`Dialog` 를 직접 import 한 곳이 없는가**(`DrawerFrame` 제외). 있으면 다음 영역이 그걸 따라한다
- **전체화면 전환 판정이 `DrawerFrame` 안에 있는가.** 호출부가 화면 폭을 재고 있으면 안 된다
- 헤더 72·푸터 76·Esc/×/스크림 닫기·`expandTo` 가 규격대로인가
- 생성 드로어 CTA 를 위해 **`DrawerFooter` 포털**을 뒀다고 워커가 보고했다 — **그게 폭·레이아웃 소유권을 우회하는 구멍인지** 판정해라

### 완료 게이트 — 아직 붙지 않았다

**WORK-004 는 게이트를 구현하지 않는다**(WORK-005 몫). 상태 드롭다운·「완료 처리」·⋯ 는 **비활성**이 정답이다.

- 비활성이 **화면만**이 아니라 **요청이 실제로 안 나가는가**(워커는 「요청 0건」을 실측했다고 보고했다 — 확인해라)
- **비활성 UI 를 숨기지 않았는가**(DEC 원칙: v2·미구현은 그리되 비활성)
- 서버에 **상태 전이 경로가 열려 있지 않은가** — `PATCH /api/tasks/{id}/status` 는 WORK-005 다. 본체 `PATCH` 로 상태가 바뀌면 **게이트를 우회하는 뒷문**이다. **이건 FAIL 후보다**

### 연관업무 후보 표면

- **표면이 하나뿐인가.** 옛 `/{task_id}/relations/candidates` 잔재가 없는가 — 둘이면 생성·상세가 다른 코드를 타고 정렬이 갈린다
- **라우트 선언 순서** — 고정 경로가 `/{task_id}`(int) 보다 **앞**인가. 뒤면 422 가 난다. 테스트로 고정돼 있는가
- **쿼리 파라미터에 `Query(alias=...)` 가 있는가**(§3 규칙 7). 빠지면 **조용히 무시되고 200 이 난다** — 실패가 안 보이는 종류다. **`scope`·`excludeId`·`projectId`·`dueDate` 전부 확인해라**
- `scope` 가 **정렬이 아니라 자르는 필터**인가. 세 값이 실제로 다른 결과를 내는가
- **기준 프로젝트가 없을 때 `scope=project` 가 `all` 처럼 답하는가** — 빈 목록을 주면 무소속 업무(DEC-002 허용)에서 팝오버가 비어버린다. **화면도 칩을 비활성으로 내리는가**(이중 방어)
- **`total` 이 `len(items)` 가 아닌가** — 20건을 넘으면 갈린다. count 쿼리로 세는가
- `excludeId` 가 **남의 것·없는 것이면 404** 인가(403 이면 존재가 샌다)

### 아키텍처 — 백엔드

- 계층: router → service → repository. **ORM 모델이 repository 를 넘지 않는가**(규약 원문은 「ORM **모델**」이다. `AsyncSession` 은 별개 — **규약에 근거가 있을 때만** 적어라)
- `schema`(FE 계약) / `dto`(내부)를 섞지 않았는가 · **service·repository 에 `commit()` 이 없는가**
- **`except Exception` 이 없는가.** 포착이 전부 구체 타입이고 재전파하는가
- **`persist_changes` 를 편의로 켠 곳이 없는가**(§7 — 「실패 응답 자체가 쓰기인」 경우만)
- **생성이 한 트랜잭션인가** — 자식(할일·첨부·연관)이 절반만 남는 경로가 없는가
- **소프트 딜리트**: 목록·후보에서 빠지되 **참조 경로로는 남는가**. 복원 API 가 없는가
- 남의 업무가 **404** 인가

### 아키텍처 — 프론트

- 정적 빌드 제약: **동적 세그먼트 0**(상세는 `/tasks/detail/?id=`), 모든 `page` 에 `'use client'`, Route Handler·미들웨어·Server Action 미사용
- 서버 상태는 TanStack Query, **전역 상태 라이브러리 없음**, `retry:false`
- **컴포넌트에 hex 리터럴이 없는가**(토큰 변수만)
- **드로어와 전체 페이지가 같은 본문(`TaskDetailBody`)을 쓰는가** — 두 벌이면 이후 수정이 한쪽만 간다
- **메모가 로그에 남지 않는가**(DEC-002 §6). 로그는 시스템 기록이다
- **연관업무가 양방향인가**(T-10) — A 에 B 를 걸면 B 에도 A 가 보이는가
- U-7 자동 저장 실패 표시가 **WORK-003 에서 만든 공통 규격을 쓰는가** — 업무에서 새로 만들었으면 정의가 둘이 된 것이다

## 4. 알려진 미결 — 여기에 시간을 쓰지 마라

1. **드로어 안 「할일 추가」는 화면 실측이 안 됐다.** 자동조작이 입력 포커스를 못 잡아 워커가 API 왕복과 컴포넌트 테스트로 덮었다. **코드로 판정할 수 있는 만큼만 보고, 사람 손 확인이 필요하면 그렇게 적어라.**
2. dev DB 에 검증용 업무·프로젝트가 남아 있다. **결함이 아니다.**

## 5. 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work-004-review-report.md` 에 쓴다.

- **네 층(정책·아키텍처·SPEC·WP) 각각 PASS/WARN/FAIL** 판정
- **FAIL 은 파일:줄 + 무엇이 어긋났는지 + 고치는 방향**까지. 재현 가능한 것은 재현 방법도
- **문서 공백**(코드 결함이 아니라 문서가 안 정한 것)은 **따로 분리**해라 — 코디가 닫는다
- 판정 못 한 것은 **「확인 못 함」으로 적어라.** 추측으로 PASS 주지 마라

**read-only 다 — 코드도 문서도 고치지 마라. 커밋하지 마라.**

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: WORK-004 검수 — FAIL n · WARN n · 공백 n" \
  --body "층별 판정 / FAIL 목록 / WARN 목록 / 문서 공백 / 확인 못 한 것"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] reviewer 완료 — WORK-004 검수 FAIL n · WARN n · 공백 n. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] reviewer: <질문>" --enter`
