
# 재개 노트 — kos-signin-limit (day)

**지금**: 마감 — #257 · #946 스쿼시 머지 · dev 배포 성공 · Delivery #256 v2 승인 · 닫음 · 회고 · 개념 · 아카이브. **남은 것 = 20시 prod 배포(`git push origin a6aa4ba5:prod`) · 배포 뒤 시스템 계정 표시 없는 옛 세션 정리**
**다음**: spec-1 → review-doc → (착수 막는 OQ 사용자 확인) → be · fe → review-code → 테스트 · day-local → 사용자 확인. 배포는 사용자가 정할 때(서버 env `KOS_CLIENT_TAG`)

세팅: `scripts/new-work.sh day kos-signin-limit` · 설정 SSOT `config/projects/day.json`
코디handle: `term_94fbe396-828d-4fa4-8bd8-829294f10614`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit` (branch `kknaksss/kos-signin-limit`, base `origin/dev` → PR `dev`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] 사용자 로컬 확인 중(day-local 17:31 재빌드 · 로컬 시스템 세션 `(local)` 표시 확인) · be-1 · fe-1 · review-code-1 PASS · 전체 1358 passed
- [ ] 스펙 맞추기(PR 전 planner): SPEC-002 차트 여는 영역(E6 → 시술명 영역) · 탭 글자 확정(OQ-59 ⓐ) — 이 작업 스펙 PR 에 같이
- [ ] **배포 때 코디가 서버 env 에 넣기(사용자 11-17)**: dev `KOS_CLIENT_TAG=dev` · prod `KOS_CLIENT_TAG=prod`(서버 app.env · 넣는 길은 config/day.json · deploy 문서 확인) · 배포 뒤 시스템 계정 표시 없는 옛 세션 한 번 정리(초기화 스크립트)
- [ ] 범위 밖: 로그아웃 때 KOS 해제(사용자 — 안 함) · 앱 화면(심사 중)
- [!] 11-17 fe-4 중복 발주 — 사용자가 끊은 줄 알았던 발주가 실제로 워커를 띄워 같은 파일을 둘이 고침 → 하나 남기고 다른 하나 Esc · 터미널 닫음 · 최종 상태 코디 검증(CSS 빌드 동기 · 전체 1359 passed). **발주 명령이 「거절」로 끝나도 워커가 떴는지 worker-list 로 확인할 것**
- [!] 이 작업은 fix-feedback 코디 세션에서 이어 띄움(사용자 지시) · 코디가 「코드 먼저」로 잘못 알아들어 backend 를 먼저 띄웠다가 중단

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-17 | 공통 = sign-in 401 SignInLimitExceeded → 목록 → 해제 → 재시도 | 사용자 · HAR 기기로그인 |
| 2026-11-17 | 시스템 계정 = UA 끝 환경 표시 (local/dev/prod · 새 env KOS_CLIENT_TAG) · **막혔을 때만** 같은 UA 세션 자동 해제(매번 아님) | 사용자 · 코디 실물 시험(UA 표시 200 · 같은 UA 재로그인해도 앞 세션 남음) |
| 2026-11-17 | ~~직원 = 안내만~~ → 직원 = **기기 선택 단계**(KOS 화면 구성 · 글자 그대로 · DS) · 로그아웃 때 해제 안 함 | 사용자 |
| 2026-11-17 | 기기 선택 단계는 **웹만** · 앱 로그인 API 는 지금처럼(깔린 앱이 unexpected_response 를 안 보게) · 앱은 다음 버전에서 같이 | 사용자(A) |
| 2026-11-17 | 시스템 계정 = 막혔을 때 **같은 환경(UA) 세션 중 가장 오래된 하나만** 해제 후 재시도 1회 | 사용자 · 검수 W-3 |
| 2026-11-17 | 앱 JSON 로그인 = 기기 제한이어도 지금과 같은 401 invalid_credentials(새 코드 안 씀 · OQ-K17) | 사용자 A 의 뜻(앱 화면 그대로) |
| 2026-11-17 | 기기 선택 화면 「처음으로」 링크 두지 않음(KOS 화면에 없음) | 검수 W-5 · 코디 기본값 |
| 2026-11-17 | 차트 여는 영역 = 시술명 영역 전체(1줄 이름 + 2줄 상태 · 원장 변경 버튼 · 체크 · 줄 버튼 · ⋮ 제외) · 호버 「차트 작성」 | 사용자 로컬 확인(fix-feedback E6 보강) |
| 2026-11-17 | 정렬 탭 글자 = 「시술대기 순」 · 「방별 순」(임시 이름 확정 · SPEC-002 OQ-59 ⓐ) | 사용자 |
| 2026-11-17 | 차트 영역 호버 · 포커스 모두 배경 · 테두리 없음 — 툴팁 「차트 작성」만 | 사용자 |
| 2026-11-17 | 순서 = 스펙 먼저 → 코드 구현까지 · 배포는 나중 | 사용자 정정 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend | `term_bff3b467-29df-483f-ac92-a9eef70ff0a5` | `task_40d11c130d04` | `ctx_359d9e31a2b9` | `kos-signin-limit-be-brief.md` | 발주 — `be-1-report.md` |
| frontend | `term_d5c97e95-d2bf-44f2-8ed9-9b51d0fb60f1` | `task_97be1900cb9c` | `ctx_f597dc5d5206` | `kos-signin-limit-fe-brief.md` | 발주 — `fe-1-report.md` |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `<YYYY-MM-DD>` <무슨 일이 있었나 — 한 줄>

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
