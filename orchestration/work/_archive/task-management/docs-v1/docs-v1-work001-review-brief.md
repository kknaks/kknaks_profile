
# [reviewer] WORK-001 검수 — 스캐폴딩 Phase 1~4 (백 + 프론트 + Tauri)

너는 **task-management `reviewer` 워커**다. **read-only.** 먼저 역할 문서를 읽어라 (**문서 레포 절대경로**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/work-001-scaffold`
base 브랜치: `origin/main`

**이 제품의 첫 코드 검수다.** 여기서 잡히는 어긋남과 문서 공백이 이후 모든 work 에 그대로 복제된다 — 지금 짚어야 싸게 고친다.

## 1. 검수 대상

이 워크트리의 커밋 **2건**(`origin/main` 이후 전부):

- `2a4d29a` — **Phase 1·2**(backend): 기동·헬스체크·Alembic·account 스키마·시드
- `84882c0` — **Phase 3·4**(frontend): Next 정적 골격·토큰·연결 확인 화면·Tauri 셸

범위 산정: `git diff origin/main...HEAD --stat` + `git log origin/main..HEAD`.
**작업 트리는 clean 하다** — 커밋된 것이 전부다.

## 2. SSOT — 판정 기준 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

| 층 | 문서 |
|---|---|
| **정책** | `10-decision/decision-001-auth-settings.md` (계정=DB 시드만·비밀번호 규칙·기본 유형 3종·**v2 스코프**·저장 실패 표시) |
| **아키텍처** | `40-architecture/backend/README.md` · `frontend/README.md` · `database/README.md`(+`domains/account.md`) · `system/README.md` |
| **SPEC** | `20-spec/spec-000-scaffold.md` |
| **WP** | `30-work/work-001-scaffold.md` — **Phase 1~4 의 작업·검증 체크리스트** |

**판정은 문서 기준이다.** 취향으로 지적하지 마라.

## 3. 이 검수에서 특히 볼 것

**아키텍처 — 백엔드**
- 계층: router → service → repository. **ORM 모델이 repository 를 넘지 않는가**(주의: 규약 원문은 「ORM **모델**」이다. `AsyncSession` 같은 세션 핸들은 별개 — 그게 층을 타는 게 바람직한지는 **의견이 아니라 규약에 근거가 있을 때만** 적어라)
- `schema`(FE 계약) / `dto`(내부)를 섞지 않았는가
- **`except Exception` 이 없는가.** 포착이 전부 구체 타입이고 재전파하는가. **임의 재시도·조용한 기본값이 없는가**
- 설정이 env → `Settings` 하나인가. **비밀값 기본값이 없는가**(없으면 기동 실패)
- CORS 가 명시 목록이고 `allow_credentials=False` 인가

**아키텍처 — 프론트**
- 정적 빌드 제약: **동적 세그먼트 0**, 모든 `page` 에 `'use client'`, Route Handler·미들웨어·Server Action 미사용
- 서버 상태는 TanStack Query, **전역 상태 라이브러리 없음**, `retry:false`
- **컴포넌트에 hex 리터럴이 없는가**(토큰 변수만)
- **토큰 저장소 격리** — `tokenStore` 밖에서 키체인·localStorage 를 부르지 않는가
- 오버레이 3종 규격·「드로어 위 모달 금지」의 **구조적 준비**가 규약대로인가

**SPEC**
- `spec-000` 의 **환경변수 표·헬스 응답 형태·시드 계약**이 그대로 구현됐는가
- **Case Matrix 의 에러가 코드에 있는가.** 반대로 **거기 없는 에러가 코드에 있는가**(있다면 문서 공백)
- Acceptance 항목이 실제로 성립하는가(코드를 읽어 판단. 실행하지 마라)

**WP**
- Phase 1~4 의 **작업 체크리스트가 실제로 다 됐는가**
- **범위 밖을 건드리지 않았는가** — 백 워커가 `app/front` 를, 프론트 워커가 `app/back` 을 만지지 않았는가
- WORK-002·003 의 기능(로그인 API·유형/프로젝트 CRUD 화면)을 **미리 만들지 않았는가**

**정책**
- 계정 생성 경로가 **시드뿐**인가(회원가입 API·화면이 없는가)
- 비밀번호가 **해시로만** 저장되는가, 규칙(8자+문자·숫자·특수문자)이 강제되는가
- 기본 유형 3종이 시드되고 **`is_default`** 가 붙는가

## 4. 문서 공백 — 별도 절로 모아라

코드 워커들이 이미 올린 것들이 있다. **네가 판정하고, 놓친 것을 더해라**:

| 워커가 올린 것 | 성격 |
|---|---|
| `APP_VERSION`·`TEST_DATABASE_URL` 이 SPEC-000 §5 환경변수 표에 없음 | SPEC 공백 |
| `DatabaseUnavailableError`(503)를 AppError 5종 외에 신설 | 아키텍처 §8 공백 |
| **시드가 기본 유형 `color_token` 을 재실행 때 덮어쓰지 않게 함** — SPEC-000 §5 「값이 다르면 맞춘다」 vs 정정 A-4 「기본 유형은 색만 편집 가능」이 **충돌** | **문서 간 모순** |
| CSP `script-src` 에 `'unsafe-inline'` 필요(정적 export·미들웨어 불가로 nonce 자리 없음), `connect-src` 의 API 주소가 빌드 시점 고정 | 아키텍처 공백 |
| 프론트 버전 핀(Next·Tailwind)을 이 work 가 정함. Tailwind 는 FE-OQ-2(브라우저 하한) 미정이라 v3 유지 | 결정 미기록 |
| 루트 `README.md` 가 어느 워커의 allowed_paths 에도 없어 기동 절차가 `app/front/README.md` 에만 있음 | 문서 배치 |

각 항목에 **어느 문서 어느 절에 무엇이 필요한지**를 적어라. 코디네이터가 그걸로 문서를 고친다.

## 5. allowed_paths — 이 밖은 건드리지 마라

산출물은 **이 파일 1개뿐**:

`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/work-001-scaffold/work-001-review-report.md`

**코드를 고치지 마라. 문서를 고치지 마라. 테스트·빌드를 돌리지 마라.** 커밋·push 금지.
(실행이 필요하다고 판단되면 리포트에 「코디 실행 요청」으로 적어라.)

## 6. 리포트 구조

```
# WORK-001 검수 리포트

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
- WORK-002 이후의 미구현을 FAIL 로 잡지 마라(이번 범위가 아니다).

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
