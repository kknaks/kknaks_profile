
# 재개 노트 — ext-api-staff-fields (cc-prototype)

**지금**: 운영 배포 · 운영 실호출 확인 끝(코드 #25 `0553173` · infra #62 · 2026-11-17 15:15 KST) → 마감 남음
**다음**: 마감 — WORK-015 상태 · deploy 기록 → profile PR → archive-work.sh(회고 · 개념) · 워커 터미널 3 · infra 워크트리 정리

세팅: `scripts/new-work.sh cc-prototype ext-api-staff-fields` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_94d17da5-ee50-4f74-ade5-221f35a1ea02`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-staff-fields` (branch `kknaksss/ext-api-staff-fields`, base `origin/main` → PR `main`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [ ] 마감
- [!] 데모 KOS 시스템 계정 동시 로그인 5기기 한도 — 로컬 e2e 를 막았다(사용자 결정: 로컬 건너뛰고 운영 확인). 워크트리 `procedure/.env` 사본은 지움
- [ ] reviewer_doc → backend(WP-BE1) → reviewer → 로컬 데모 e2e → 배포(back.imageTag) → 운영 실호출 → 마감
- [!] W2(email · realName · roleName 이 문자열 아니면 500) — 기존 roleName 과 같은 동작 · SPEC 에 갈래 없음 → 이번엔 안 고침 · 회고 §7 후보
- [!] public 레포 — 이메일 · 실명 · KOS id 실값을 문서 · 시험 · 리포트에 넣지 않는다

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-17 | ext 직원 목록에 `email` · `realName` · `kosAccountId` 추가 — DEC-012 D-48(D-15 고침) · 필드 추가만 | 사용자 「이메일 실명 코스 id 다 받아야」 · 필드 이름 제안 승인 · 「발주해줘」 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner(fable) | `term_db02145b-6732-492e-bb39-120ba5de14a5` | — | — | 대기(터미널 살림) | 대기 |
| reviewer_doc(fable) | `term_e070a23e-f818-4e25-aef9-6879c05d58cb` | — | — | 끝(r2 PASS) | 대기 |
| backend(opus) | `term_2b24ee55-2fac-4c06-804a-14401d958071` | — | — | 끝(수정 r1) | 대기 |
| reviewer(opus) | `term_4f9e8603-2a4c-442e-b8c4-d20f9fe6c741` | — | — | 끝(r1 PASS) | 대기 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec 커밋: `5dd09a3f`(코디 브랜치 · PR 은 마감 때)
- code 커밋: `8fbd307`(브랜치 `kknaksss/ext-api-staff-fields` · 미push)
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-17` 코드 PR #25 스쿼시(`0553173`) · back 이미지 success · infra #62 · ArgoCD sync Synced Healthy · 운영 실호출 200(직원 78 · 키 여덟 · kosAccountId 78/78 · email 78/78 · realName 64/78 · Swagger 옛 문장 0) — 값은 기록 안 함
- `2026-11-17` 수정 r1 확인(24 passed · ruff) · 코드 커밋 `8fbd307` · 로컬 e2e 시도 → 데모 KOS sign-in 401 SignInLimitExceeded → 서버 내림
- `2026-11-17` 코드 검수 r1 PASS · WARN 2 → W1 SPEC §8 행 코디 추가 · backend 수정 r1 발주 / W2 보류
- `2026-11-17` BE1 완료(767 passed · ruff OK · 코디 관문 24 passed) → reviewer 발주
- `2026-11-17` 문서 검수 r2 PASS · 참고 2 코디 반영 · 문서 커밋 `5dd09a3f`(work/ 제외) · backend 발주
- `2026-11-17` planner 수정 r1 완료 → reviewer_doc r2 발주
- `2026-11-17` 문서 검수 r1 WARN 5 · FAIL 0(`review-doc-r1.md`) → planner 수정 r1 발주 · DEC-012 D-48 null 규칙 W3 반영(코디)
- `2026-11-17` planner 완료(release) · reviewer_doc r1 발주
- `2026-11-17` 착수 · DEC-012 D-48 코디 작성 · planner 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
