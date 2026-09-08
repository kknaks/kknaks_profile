
# [reviewer] WORK-002 검수 — 인증·세션 Phase 1~3 (백 + 프론트)

너는 **task-management `reviewer` 워커**다. **read-only.** 먼저 역할 문서를 읽어라 (**문서 레포 절대경로**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main`

**인증은 전 영역의 전제다.** 여기가 새면 뒤의 모든 work 가 그 위에 쌓인다.

## 1. 검수 대상

**WORK-002 커밋 3건만** 본다 (WORK-001 은 이미 검수했다 — `2a4d29a`·`84882c0` 은 대상 아님):

- `37a8ce1` — **Phase 1**(backend): 인증 4표면(로그인·갱신·로그아웃·세션) + W-3 주석 정정
- `c39d501` — `.env.example` 시드 기본값(WORK-001 잔여 결함 수정)
- `c49ae72` — **Phase 2·3**(frontend): 토큰 저장소·요청 파이프라인·로그인 화면·설정 셸·로그아웃 모달·V2Gate + W-2 gutter 정정

범위 산정: `git diff 84882c0...HEAD --stat` + `git log 84882c0..HEAD`.
**작업 트리는 clean 하다** — 커밋된 것이 전부다.

## 2. SSOT — 판정 기준 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

| 층 | 문서 |
|---|---|
| **정책** | `10-decision/decision-001-auth-settings.md` — **§4 세션**(Bearer·access 1h/refresh 7d·「유지」 체크 시 OS 키체인·**브라우저 저장소 폴백 없음**, 2026-09-05 개정) · §3 비밀번호 · **§v2 스코프** |
| **아키텍처** | `40-architecture/backend/README.md` · `frontend/README.md` · `database/README.md`(+`domains/account.md`) · `system/README.md` |
| **SPEC** | `20-spec/spec-001-auth-session.md` (§4 Case Matrix · §5 · §6 Acceptance) |
| **WP** | `30-work/work-002-auth-session.md` — **Phase 1~3 의 작업·검증 체크리스트** |

**판정은 문서 기준이다.** 취향으로 지적하지 마라.

## 3. 이 검수에서 특히 볼 것

**아키텍처 — 백엔드**
- 계층: router → service → repository. **ORM 모델이 repository 를 넘지 않는가**(주의: 규약 원문은 「ORM **모델**」이다. `AsyncSession` 은 별개 — **규약에 근거가 있을 때만** 적어라)
- `schema`(FE 계약) / `dto`(내부)를 섞지 않았는가 · **service·repository 에 `commit()` 이 없는가**
- **`except Exception` 이 없는가.** 포착이 전부 구체 타입이고 재전파하는가
- **`persist_changes` 예외가 규약대로인가**(§7 신설, 2026-09-05) — 기본 False, 켠 것은 「실패 응답 자체가 쓰기인」 예외뿐(`RefreshTokenReuseError` 하나), 구체 타입으로 받아 commit 후 **재전파**. 편의로 켠 곳이 없는가
- 설정이 env → `Settings` 하나인가. **비밀값 기본값이 없는가**
- CORS 명시 목록 · `allow_credentials=False`

**보안 — 이 검수의 핵심**
- **계정 존재가 새지 않는가** — 틀린 비밀번호와 없는 아이디의 응답이 **같은가**(내용·상태코드·시간)
- **refresh 가 평문으로 저장되지 않는가.** 회전·재사용 감지(A-7)가 실제로 성립하는가
- **응답·로그에 토큰 전문·비밀번호 해시가 새지 않는가**
- 401 사유(헤더없음·만료·위조)를 **구분해 알려주지 않는가**
- 「다른 기기 모두 로그아웃」 같은 **v2 기능을 구현하지 않았는가**

**아키텍처 — 프론트**
- 정적 빌드 제약: **동적 세그먼트 0**, 모든 `page` 에 `'use client'`, Route Handler·미들웨어·Server Action 미사용
- 서버 상태는 TanStack Query, **전역 상태 라이브러리 없음**, `retry:false`
- **컴포넌트에 hex 리터럴이 없는가**(토큰 변수만) · gutter 가 §7-1 표대로인가(W-2 정정 확인)
- **토큰 저장소 격리** — `tokenStore` 밖에서 키체인·localStorage 를 부르지 않는가
- **브라우저 저장소 폴백이 없는가** — 셸이 없을 때 `persist=true` 가 **조용히 다른 곳에 저장하지 않고 예외를 던지는가**(DEC-001 §4)
- **갱신이 1회로 끝나는가** — 401 에 무한 재시도하지 않고, **로그아웃 뒤 갱신을 재시도하지 않는가**(재사용 감지가 걸려 전 세션이 끊긴다)

**SPEC**
- `spec-001` 의 **API 표면·Validation·상태 전이**가 그대로 구현됐는가
- **Case Matrix 의 에러가 코드에 있는가.** 반대로 **거기 없는 에러가 코드에 있는가**(있다면 문서 공백)
- Acceptance 항목이 실제로 성립하는가(코드를 읽어 판단. 실행하지 마라)

**WP**
- Phase 1~4 의 **작업 체크리스트가 실제로 다 됐는가**
- **범위 밖을 건드리지 않았는가** — 백 워커가 `app/front` 를, 프론트 워커가 `app/back` 을 만지지 않았는가
- WORK-002·003 의 기능(로그인 API·유형/프로젝트 CRUD 화면)을 **미리 만들지 않았는가**

**정책**
- **회원가입·비밀번호 찾기·소셜 로그인**이 API·화면 어디에도 없는가
- 「로그인 상태 유지」가 **서버에 없는가**(클라이언트 보관 선택일 뿐)
- v2 항목(다른 기기 로그아웃·계정 삭제 등)이 **UI 는 있되 동작하지 않는가**

## 4. 문서 공백 — 별도 절로 모아라

코드 워커들이 이미 올린 것들이 있다. **네가 판정하고, 놓친 것을 더해라**:

| 워커가 올린 것 | 성격 |
|---|---|
| **조작·형식오류 access 에 쓸 코드가 §8-2 표에 없어** 헤더없음·만료·위조를 전부 `401 token_expired` 하나로 통일했다 | 아키텍처 공백 — 코드 신설 여부 판단 필요 |
| WP 테스트의 「남의 자원 404」가 Phase 1 에 해당 표면이 없어 「남의 refresh 로 로그아웃해도 그 세션이 안 죽는다」로 대체 | WP 공백 |
| `tokenStore` 에 `load()`·`isPersistent()`·`KeychainError` 를, `ConfirmRequest` 에 `confirmLabel`·`destructive` 를 추가 | 아키텍처 인터페이스 미기록 |
| `features/auth/api.ts` 대신 `lib/auth/session.ts` 에 호출을 모음 | 디렉토리 규약 해석 |
| macOS dev 는 ad-hoc 서명이라 `src-tauri` 재컴파일마다 키체인 ACL 알림 | 운영 메모 |
| 사이드바의 캘린더·회의록·자료함·메시지가 **404 로 빠지고 정적 export 라 돌아올 길이 없다** | 미구현 경로 처리 — **사용자 판단으로 후속 work 까지 보류** |

각 항목에 **어느 문서 어느 절에 무엇이 필요한지**를 적어라. 코디네이터가 그걸로 문서를 고친다.

## 5. allowed_paths — 이 밖은 건드리지 마라

산출물은 **이 파일 1개뿐**:

`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work-002-review-report.md`

**코드를 고치지 마라. 문서를 고치지 마라. 테스트·빌드를 돌리지 마라.** 커밋·push 금지.
(실행이 필요하다고 판단되면 리포트에 「코디 실행 요청」으로 적어라.)

## 6. 리포트 구조

```
# WORK-002 검수 리포트

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
- **WORK-003 이후의 미구현을 FAIL 로 잡지 마라**(유형·프로젝트 관리 화면 등). 사이드바 404 도 사용자 판단으로 보류된 사안이다.
- **WORK-001 커밋(`2a4d29a`·`84882c0`)은 이미 검수했다** — 다시 보지 마라.

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
