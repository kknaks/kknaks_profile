
# [reviewer] WORK-003 검수 — 업무 설정 Phase 1~3 (백 + 프론트)

너는 **task-management `reviewer` 워커**다. **read-only.** 먼저 역할 문서를 읽어라 (**문서 레포 절대경로**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main`

**여기서 만든 팔레트·배지/dot·자동 저장 실패 규격을 업무·회의·캘린더가 전부 쓴다.** 여기가 어긋나면 뒤가 복제한다.

## 1. 검수 대상

**WORK-003 커밋 2건만** 본다 (WORK-001·002 는 이미 검수했다):

- `ffc544d` — **Phase 1**(backend): 유형·프로젝트 8표면(목록·생성·부분수정·소프트딜리트)
- `8e17d0b` — **Phase 2·3**(frontend): 팔레트 8종·TypeBadge/ColorDot/ColorPickerPopover·업무 설정 화면·U-7 자동저장 실패 규격

범위 산정: `git diff 533843e...HEAD --stat` + `git log 533843e..HEAD`.
**작업 트리는 clean 하다** — 커밋된 것이 전부다.

## 2. SSOT — 판정 기준 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

| 층 | 문서 |
|---|---|
| **정책** | `10-decision/decision-001-auth-settings.md` — **§3 필드**(유형: 종류·이름·색 / **slug 없음**) · **§4 기본 3종 잠금**(이름·종류 고정, 색만) · **소프트 딜리트**(복원 없음) · §7 저장 실패 표시 |
| **아키텍처** | `40-architecture/backend/README.md` · `frontend/README.md` · `database/README.md`(+`domains/account.md`) · `system/README.md` |
| **SPEC** | `20-spec/spec-002-work-settings.md` (§2 U-1~U-8 · §4 Case Matrix · **팔레트 8종 Data Contract** · §6 Acceptance) |
| **WP** | `30-work/work-003-work-settings.md` — Phase 1~3 체크리스트 + **§Internal Interface Contract**(후속 work 가 의존하는 접점) |

**판정은 문서 기준이다.** 취향으로 지적하지 마라.

## 3. 이 검수에서 특히 볼 것

**아키텍처 — 백엔드**
- 계층: router → service → repository. **ORM 모델이 repository 를 넘지 않는가**(주의: 규약 원문은 「ORM **모델**」이다. `AsyncSession` 은 별개 — **규약에 근거가 있을 때만** 적어라)
- `schema`(FE 계약) / `dto`(내부)를 섞지 않았는가 · **service·repository 에 `commit()` 이 없는가**
- **`except Exception` 이 없는가.** 포착이 전부 구체 타입이고 재전파하는가
- **`persist_changes` 예외가 규약대로인가**(§7 신설, 2026-09-05) — 기본 False, 켠 것은 「실패 응답 자체가 쓰기인」 예외뿐(`RefreshTokenReuseError` 하나), 구체 타입으로 받아 commit 후 **재전파**. 편의로 켠 곳이 없는가
- 설정이 env → `Settings` 하나인가. **비밀값 기본값이 없는가**
- CORS 명시 목록 · `allow_credentials=False`

**단일 정의 — 이 검수의 핵심**
- **팔레트 8종이 서버 1곳·프론트 1곳뿐인가.** 세 번째 정의가 없는가(WP Done Criteria 「중복 정의 없음」)
- **색이 전부 `data-color-token` 으로 그려지는가** — 컴포넌트에 hex·인라인 `style` 이 없는가(FE §5-3)
- 팔레트에 **없는 토큰명이 오면 중립 색으로 떨어뜨리고 항목을 숨기지 않는가**
- **자동 저장 실패 표시가 「전 영역 공통」으로 쓸 수 있게** 만들어졌는가(한 화면에 갇히지 않았는가). 해제 조건이 「다시 저장 성공」·「재편집 후 저장 성공」 **둘뿐**이고 시간 경과로 사라지지 않는가

**규칙의 이중 방어**
- **기본 유형 잠금**이 화면과 서버 **두 겹**인가 — 화면이 컨트롤을 감춰도 서버가 `work_type_locked` 로 막는가
- **소프트 딜리트**: 목록·선택지에서 빠지되 **참조 경로로는 이름·색이 그대로** 나오는가(A-6). **복원 API·UI 가 없는가**
- 남의 유형·프로젝트가 **404** 인가(403 이면 존재가 샌다)

**아키텍처 — 프론트**
- 정적 빌드 제약: **동적 세그먼트 0**, 모든 `page` 에 `'use client'`, Route Handler·미들웨어·Server Action 미사용
- 서버 상태는 TanStack Query, **전역 상태 라이브러리 없음**, `retry:false`
- **컴포넌트에 hex 리터럴이 없는가**(토큰 변수만) · gutter 가 §7-1 표대로인가(W-2 정정 확인)
- **토큰 저장소 격리** — `tokenStore` 밖에서 키체인·localStorage 를 부르지 않는가
- **`items` 를 꺼내는 것이 `api.ts` 까지인가**(훅 위로는 배열)
- 캐시 무효화가 `['workTypes']`·`['projects']` 에 걸리고, `['tasks']`·`['meetings']` 키가 **등록만** 돼 있는가(지금은 읽는 화면이 없다 — no-op 이 정상)
- **자동 재시도가 없는가** — 저장 실패 후 요청이 저절로 다시 나가지 않는가

**SPEC**
- `spec-001` 의 **API 표면·Validation·상태 전이**가 그대로 구현됐는가
- **Case Matrix 의 에러가 코드에 있는가.** 반대로 **거기 없는 에러가 코드에 있는가**(있다면 문서 공백)
- Acceptance 항목이 실제로 성립하는가(코드를 읽어 판단. 실행하지 마라)

**WP**
- Phase 1~4 의 **작업 체크리스트가 실제로 다 됐는가**
- **범위 밖을 건드리지 않았는가** — 백 워커가 `app/front` 를, 프론트 워커가 `app/back` 을 만지지 않았는가
- WORK-002·003 의 기능(로그인 API·유형/프로젝트 CRUD 화면)을 **미리 만들지 않았는가**

**정책**
- **slug·영문명 필드가 없는가**(DEC-001 §3 — 자동 키로 충분하다는 결정)
- **집계 카운트(「이번 달 8건」)를 만들지 않았는가**(v1 제외 — S002-OQ-3)
- **복원 UI 가 없는가**

## 4. 문서 공백 — 별도 절로 모아라

코드 워커들이 이미 올린 것들이 있다. **네가 판정하고, 놓친 것을 더해라**:

| 워커가 올린 것 | 성격 |
|---|---|
| **에러 코드 3종**(`duplicate_name`·`invalid_color_token`·`not_found`)이 §8-2 표에 없다. 발명하지 않고 SPEC-002 Case Matrix 문구를 그대로 썼다 | 아키텍처 공백(S002-OQ-2) |
| **`extra="forbid"` 를 이번 요청 스키마에만** 걸었다 — 계약에 없는 필드를 조용히 무시하면 「바뀐 줄 알았는데 안 바뀐」 상태가 된다. 기존 auth 스키마는 범위 밖이라 안 건드렸다 | 전 영역 통일 여부 결정 필요 |
| 빈 `PATCH({})` 는 200 + 현재 값이다 — Case Matrix 에 「바꿀 것 없음」 실패가 없어 에러를 발명하지 않았다 | SPEC 공백 |
| 이미 삭제된 항목의 PATCH·DELETE 는 404(§4 State 에 삭제됨에서 나가는 전이가 없다) | SPEC 해석 |
| `tests/setting_fixtures.py` 가 `conftest.py` 가 아니라 자동 수집되지 않는다(모듈이 import) — WORK-001 의 conftest 를 안 건드리려는 선택 | 테스트 구조 |
| A-6 「참조 중인 곳에 이름·색 그대로」는 task·meeting 테이블이 아직 없어 **소비 경로로만 검증**했다 — 화면 확인은 WORK-004 몫 | 검증 이월 |
| `['tasks']`·`['meetings']` 무효화가 읽는 화면이 없어 **지금은 no-op** | 정상(설계대로) |

각 항목에 **어느 문서 어느 절에 무엇이 필요한지**를 적어라. 코디네이터가 그걸로 문서를 고친다.

## 5. allowed_paths — 이 밖은 건드리지 마라

산출물은 **이 파일 1개뿐**:

`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work-003-review-report.md`

**코드를 고치지 마라. 문서를 고치지 마라. 테스트·빌드를 돌리지 마라.** 커밋·push 금지.
(실행이 필요하다고 판단되면 리포트에 「코디 실행 요청」으로 적어라.)

## 6. 리포트 구조

```
# WORK-003 검수 리포트

## 판정 요약
| 층 | 판정 | 근거 |
(정책 / 아키텍처-백 / 아키텍처-프론트 / SPEC / WP 각각 PASS·WARN·FAIL)

## FAIL — 반드시 고쳐야 하는 것
| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |

## WARN — 규약에서 벗어났으나 동작하는 것
(같은 형식)

## 문서 공백 — 코드가 아니라 문서를 고쳐야 하는 것
| # | 무엇이 비었나 | 어느 문서 어느 절 | 무엇을 적어야 하나 |

## 확인한 것 (PASS 근거)
간단히 — 무엇을 어떻게 확인했는지

## 코디 실행 요청 (있으면)
```

## 7. 범위 제약

- **코드·문서 수정 금지.** 판정과 근거만.
- **근거를 댈 수 없으면 싣지 마라.** 추측 지적 금지.
- 취향·선호로 지적하지 마라 — **문서에 근거가 있는 것만**.
- **WORK-004 이후의 미구현을 FAIL 로 잡지 마라**(업무 화면·집계 카운트 등). 사이드바 404 도 사용자 판단으로 보류된 사안이다.
- **WORK-001·002 커밋은 이미 검수했다** — 다시 보지 마라.

## 8. 검증

```
리뷰는 read-only — 코드를 고치지 않고 테스트도 돌리지 않는다. git diff <base>...HEAD + untracked 로 범위를 산정하고, 네 층(정책·아키텍처·SPEC·WP)별로 PASS/WARN/FAIL 과 위반 목록(파일:줄 + 어긋난 문서 절)을 남긴다. 문서가 빈 것은 지적이 아니라 「문서 공백」 절로 분리한다
```

자기점검 — 보고에 적어라:

- 네 층 **전부**에 판정을 냈나
- 모든 FAIL·WARN 에 **파일:줄 + 문서 절**이 붙었나
- 문서 공백이 지적과 **분리**됐나
- 코드·문서를 하나도 고치지 않았나(`git status` 로 확인)

## 9. 완료 보고 — **문구 변경 금지**

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
  --subject "reviewer 완료: <한 줄>" \
  --body "판정 요약(층별) / FAIL·WARN 건수 / 문서 공백 건수 / 주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
