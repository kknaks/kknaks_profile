# [reviewer] WORK-008 Phase 1 코드 검수 — frontend 리뷰 모드

너는 **strong-hajin `reviewer` 워커**다(앞서 SPEC 을 검수한 그 워커). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md` (+ `rules.md`). **read-only.**

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` 의 미커밋 변경 (`git status` · `git diff` · 새 파일 `frontend/src/lib/weekWindow.ts`·`.test.ts`).

## 2. 기준
- 계약: WP `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 1(1-1~1-5)** + 원칙 P-2·P-3
- 정본 SPEC: SPEC-001 U-6-a·U-16 · SPEC-005 §2.4 · SPEC-007 §2.9 (같은 레포 `20-spec/`)
- 발주서: `…/orchestration/work/strong-hajin-polish/strong-hajin-polish-fe-p1-brief.md`
- 워커 보고(요약): 변경 14파일+신규 2 · vitest 1122 중 5 실패(기준선과 같은 날짜 의존 5 — `flaky-baseline-evidence.md`) · tsc 0 · build 성공

## 3. 볼 것
1. **계약 충실도** — WP 체크박스 하나하나가 코드로 맞나(파일:줄). 특히
   - B-02: 처음 열 때 두 갈래 모두 참조자 전원 · 요청 담당 선택 시 그 사람만 빠짐·바꾸면 돌아옴 · 참조자 체크 해제 · `initial` 있는 자리 불변
   - F-01: 작은 모달이 상세 **위**에, ESC/바깥은 작은 모달만, 성공 후 상세 재조회(낙관적 갱신 없음), 사유 선택
   - F-03/D-01: 범위 함수 **하나**를 둘이 공유 · 월요일 시작 5주 · 주 경계 넓힘 · 넓힘은 첫 화면만 · 1주 밀기 · 「오늘」
   - F-02: search 입력이 다른 입력칸과 같은 DS 규칙 · WebKit 꾸밈 제거
2. **전수조사가 맞나** — 워커가 센 개수를 직접 grep 으로 다시 센다(`assigneeId`·`CreateWorkModal` 여는 곳·`type="search"`·`search-input-box`·범위 계산). 빠진 자리
3. **조용히 통과하는 자리** — 테스트는 초록인데 계약이 깨진 곳: 빈 단언·이름만 바꾼 테스트·날짜를 고정해 경계를 안 보는 테스트·`today` 를 주입 못 해 오늘 의존이 생긴 곳
4. **P-2** — DS 토큰·부품 밖의 하드코딩 색/크기, 새 모양. CSS 변경(`components.css`·`ax.css`·`screens-a.css`)이 다른 입력칸·화면에 번지는 부작용
5. 프론트 규율 — envelope 로 권한 판단 · `api.ts` 밖 fetch 없음 · 기존 viewModel/부품 재사용
6. **사용자가 실물에서 만날 자리** — 코드로 보이는 「막히진 않는데 눈에 이상할」 곳을 모아 적는다(코디 화면 확인 목록으로 쓴다)

## 4. 판정
FAIL(계약과 다르게 돈다) · WARN · PASS. 각 지적에 파일:줄 + 근거.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p1-report.md` 하나만. 테스트를 직접 돌려도 되지만 **직렬로만**(`npx vitest run --no-file-parallelism <파일>`), 서버·브라우저는 띄우지 않는다

## 6. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-008 Phase 1 코드 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN(파일:줄) / 전수조사 재계수 / 화면 확인 목록 / 리포트 경로"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] reviewer 완료 — Phase 1 코드 검수 <판정>. 리포트 review-fe-p1-report.md" --enter
```
