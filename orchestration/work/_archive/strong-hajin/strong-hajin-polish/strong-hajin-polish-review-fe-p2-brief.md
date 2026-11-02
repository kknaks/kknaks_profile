# [reviewer] WORK-008 Phase 2 코드 검수 — frontend 리뷰 모드 (B-01 깜박임)

너는 **strong-hajin `reviewer` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only.**

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` 의 **`frontend/` 미커밋 변경만** (`git diff -- frontend/` + 새 파일 `frontend/src/lib/screenCache.ts`·`.test.tsx`).
⚠ 같은 워크트리 `backend/` 에서 backend 워커가 Phase 3a 를 하고 있다 — `backend/` diff 는 대상이 아니다.

## 2. 기준
- WP `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 2** · 원칙 P-2·P-3
- 발주서 `…/orchestration/work/strong-hajin-polish/strong-hajin-polish-fe-p2-brief.md`
- 조사 `fe-survey-report.md` §7 · 기준선 `flaky-baseline-evidence.md`
- 워커 보고 요약: 공용 `screenCache`(모듈 Map + 주인 personaId) · 화면 7 적용(홈·업무·캘린더·프로젝트·조직·보고·회의 목록), 제외(회의 상세·자료함·관계 탐색·AX) · 직렬 vitest 1133 중 기준선 5 실패만 · tsc 0 · build 성공

## 3. 볼 것
1. **계약** — 재진입 즉시 이전 데이터·뒤에서 갱신 · 스켈레톤은 첫 진입만 · 화면 전부(실제 메뉴를 다시 센다) · 쓰기 뒤 갱신 · envelope 는 갱신된 응답 기준 · 로그아웃/사용자 전환 때 폐기
2. **누설** — 다른 사람 데이터가 비칠 경로가 하나라도 있나: 주인 설정 타이밍(렌더 중 scope), 세션 만료·다른 사람 로그인·같은 탭 재로그인, 비동기 응답이 주인이 바뀐 뒤 도착해 옛 주인 값을 기억하는 경쟁
3. **옛 데이터가 남는 자리** — 쓰기 뒤 refresh 를 안 거치는 경로(모달 저장·AX 등록·판단 명령·드래그 이동 등)를 grep 으로 전부 세고, 그 뒤 다른 탭 재진입 때 옛 값이 보이는지
4. **키 설계** — 캘린더 구간·조직별·날짜별 키가 섞이거나 무한히 쌓이는지(메모리)
5. **조용히 통과하는 자리** — 테스트가 주인 없는 경로만 타서 실제 App 경로를 안 보는 것, 이름만 바뀐 단언
6. P-2 · 프론트 규율(api.ts 밖 fetch 0, 새 라이브러리 0)
7. **사용자가 실물에서 만날 자리** — 코디 화면 확인 목록

## 4. 판정
FAIL · WARN · PASS. 각 지적에 파일:줄 + 근거. 테스트는 직렬로만(`npx vitest run --no-file-parallelism <파일>`), 서버·브라우저 금지.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p2-report.md` 하나만

## 6. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-008 Phase 2 코드 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN(파일:줄) / 화면 확인 목록 / 리포트 경로"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] reviewer 완료 — Phase 2 코드 검수 <판정>. 리포트 review-fe-p2-report.md" --enter
```
