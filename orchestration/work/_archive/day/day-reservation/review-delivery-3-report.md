# review-delivery-3 — review-delivery --apply + spec-sync (마감)

- 기준: Code PR #272 exact head `85836b300cb729fb9b4923d05ae9d8bf14bd66f8` · dev 스쿼시 머지 `4bf0b4a12f3238b610150eb052a6964ab2438ff2`(= 지금 `origin/dev`) · baseline Mediness `32b83390` · contract v3 · Mediness `origin/main` = `c43633be`(#959 머지).
- 코드 · 문서는 고치지 않았다. 커밋 · push · PR 없음. harness 가 쓴 것 = Issue 라벨 · closeout 마커 · PR #272 review 댓글뿐.

## 결과 요약

| 단계 | #267 ① | #268 ② | #269 ③ |
|---|---|---|---|
| review `--plan`(head · unmerged) | planned · `await-human-merge` | 같음 | 같음 |
| review `--apply`(head · unmerged) | recorded | recorded | recorded |
| review `--plan` / `--apply`(merged · `4bf0b4a1`) | recorded · next = **`run-spec-sync`** | 같음 | 같음 |
| Issue 라벨(지금) | execution-plan:ready · delivery-plan:approved · spec-baseline:ready · **implementation:conformant · spec-sync:pending** · OPEN | 같음 | 같음 |
| `check-evidence --kind review` | **fresh: false**(review 링크 · contract digest · Acceptance 링크 stale) | **fresh: false**(같음) | **fresh: true** |
| spec-sync | **막힘**(아래 ①·②) | 막힘 | 막힘(②) |

## review 입력

- Acceptance 전부 `pass`. e2e(#267 A5 · #268 A6 · #269 A4) evidence = 코디가 남긴 Issue 댓글(#267 `issuecomment-7121402449` · #268 `-7121402807` · #269 `-7121403210`) + 「사용자 직접 확인 2026-11-24 · 로그 sync 18 · done 18 · 오늘 날짜 최신화 0 · 폴링 낸 최신화 0」. 나머지 Acceptance = `review-delivery-2-report.md` 의 테스트 경로:줄 그대로.
- 직원 토큰 공지 KOS 실호출: 따로 된 Acceptance 가 없다(#267 A7 = 가짜 어댑터 테스트). 그래서 남은 위험으로만 적는다(dev 배포 뒤 확인 — 댓글에 적힘).
- **사실대로 적어 둘 것**: e2e Acceptance 문장의 「같은 날짜를 두 창에서 동시에 열기 = KOS 일정 조회 1회」는 댓글에 따로 적혀 있지 않다(댓글은 「같은 날짜 반복 = Redis 10초 캐시 건너뜀」). 코디 지시(「댓글을 e2e evidence 로」 · 사용자 「내가 다 확인했다」)대로 pass 로 넣었다. 동시 요청 1회는 #268 A5 테스트(`test_date_sync.py:336`)가 덮는다.
- per_spec: DAY-SPEC-006 · 000 · 002 모두 `none`(baseline 이 이미 구현을 담음 — 앞 보고와 같음).
- 파일: `delivery/review-v3-final-*.json`(head) · `review-v3-merged-*.json`(merged) · `*-plan-*.json` · `*-apply-*.json`.

## 막힘 ① — 한 Code PR 에 Delivery 셋: review evidence 마커가 PR 에 하나뿐

- harness 는 PR 댓글 마커 `mediness:delivery-review-evidence:v1` 를 **PR 마다 하나** upsert 한다(`workflow.py:18` · `upsert_pr_comment`). 세 Issue 를 차례로 apply 하니 PR #272 댓글(`issuecomment-7121416466`)에는 **마지막 #269 evidence 만** 남았다.
- 그래서 `check-evidence --kind review` = #269 fresh · #267 · #268 stale. 다시 돌리면 마지막 것만 fresh 로 바뀔 뿐이라 셋을 동시에 fresh 로 만들 수 없다.
- 원인 = 규칙 「1 Delivery Issue = 1 Code PR」(delivery-workflow 「원장과 evidence」)과 다르게 세 Delivery 가 #272 하나를 쓴 것(delivery-4 review_surface 에 적힌 구조). Issue 쪽 closeout 마커 · 라벨은 셋 다 제대로 있다.
- 우회(마커 손으로 고치기 · 반복 apply)는 하지 않았다. **사람 판단 필요**: (a) #267 · #268 을 #269 로 합치거나 supersede 하는 Scope Delta(`start-delivery`) (b) harness 에 PR 하나 · Delivery 여럿 지원을 넣기 (c) #269 만 정본 evidence 로 마감하고 #267 · #268 은 사람이 「#269 evidence 로 덮음」 기록 뒤 닫기.

## 막힘 ② — sync worktree 를 못 만든다(로컬 브랜치 이름 충돌)

- `spec-worktree --plan` = 세 Issue planned(base `c43633be` · 브랜치 `mediness/delivery-{N}-spec`).
- `--apply`(#267) = conflict: `fatal: 'refs/heads/mediness' exists; cannot create 'refs/heads/mediness/delivery-267-spec'`.
- 문서 레포에 옛 로컬 브랜치 **`mediness`**(`8995dece` · 2026-07-28 · origin 보다 646 뒤 · 어느 worktree 에도 안 걸림)가 있어 `mediness/…` 이름을 못 쓴다. 남의 브랜치라 지우거나 이름을 바꾸지 않았다. → 그 브랜치를 정리(지우기 · 이름 바꾸기)할지는 사람이 정한다. 정리하면 같은 명령으로 이어 갈 수 있다.

## dashboard 미리 보기 (쓰기 없음)

- `origin/main` 의 `products/day/30-work.md` 사본(scratchpad)에 `dashboard-sync --view delivery --project-delivery-issue N --project-spec-sync synced --repo-url https://github.com/MediSolveAIDev/CENTURION_DAY --plan`: 셋 다 exit 0 · `changed: true` · projection = `issue_state: closed` · `spec-sync:synced`.
  - #267 `sha256:68a7096d…2273` · #268 `sha256:baa815ad…a6ceb` · #269 `sha256:13cdfc99…bd55`.
- Issue 마다 projection 이 따로라 sync PR 도 Issue 마다(최대 하나씩) 된다.
- Spec Coverage(손으로 쓰는 표 — DAY-SPEC-006 `in_dev` · DAY-SPEC-002 `in_dev`)는 dashboard-sync 가 건드리지 않는다. 머지 뒤 `done` 으로 돌리는 것은 sync PR 에 사람 · planner 가 넣을 문서 변경이다(이번엔 문서 고치기 금지라 하지 않음).

## 남은 순서 (막힘이 풀린 뒤)

1. 막힘 ① 판단 → (a) 면 `start-delivery` Scope Delta 뒤 `review-delivery` 를 다시(새 digest) · (c) 면 #269 로 진행.
2. 막힘 ② 정리 → `spec-worktree --apply` → 그 worktree 에서 `dashboard-sync --plan` / `--apply`(+ Spec Coverage `done` 손질) → 문서 PR 하나 → **사람 머지**.
3. 머지된 sync PR head 로 같은 projection 다시 돌려 `current · changed:false · 같은 digest` 확인 → `spec-sync --apply`(code_merge_sha `4bf0b4a1` · current_code_head · spec_pr · spec_pr_head_sha · per_spec all `unchanged`) → `complete-delivery` → `check-evidence --kind spec-sync` fresh → Issue close.
4. 남은 위험: 직원 토큰 공지 KOS 실호출 — dev 배포 뒤 확인.
