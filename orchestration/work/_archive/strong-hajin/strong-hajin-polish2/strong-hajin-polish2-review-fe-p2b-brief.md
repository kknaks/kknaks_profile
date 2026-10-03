# [reviewer] WORK-009 Phase 2b 코드 검수 — frontend 리뷰 모드

너는 **strong-hajin `reviewer` 워커**다(앞서 SPEC 을 검수한 그 워커). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/reviewer/role.md` (+ `rules.md`). **read-only.**

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` 의 **`frontend/` 미커밋 변경만** (`git status -- frontend` · `git diff -- frontend` · 새 파일 `frontend/src/features/work/TaskDetailDates.test.tsx`·`frontend/src/lib/taskDates.test.ts`).
⚠ 같은 워크트리 `backend/` 는 backend 워커가 Phase 1 을 하는 중이다 — **대상 아님, 건드리지 마라.**

## 2. 기준
- 계약: WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` **Phase 2b(2b-1 · 2b-2)** + 원칙 P-4·P-5
- 정본 SPEC: SPEC-007 §2.2 「날짜 넷」·「출처 줄」·§6 · SPEC-001 U-17·§6·OQ-Q(닫힘) · SPEC-003 「업무 날짜」 (`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/20-spec/`)
- 발주서: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-fe-p2b-brief.md` · 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-survey-report.md` §4·§5
- 워커 보고 요약: 24파일 수정+새 테스트 2 · `formatDate`(labels.ts) 하나로(시각이면 서울 날짜로) · `labels.taskDateLabel` 상수 36곳 · formatDate 호출 73곳 · vitest 기준선 5 실패/1182 → 5 실패/1196(같은 날짜 의존 5) · tsc 0 · build 성공 · 유지한 자리 ①~⑩(① 만들기 창·캘린더 「시작일」 ② 캘린더 날 머리 ③ 목록 「… 시작」 ④ 축 눈금 ⑤ 기간 잇는 기호 ⑥ 회의·프로젝트 DateField 「.」 ⑦ 「처리일」 머리 ⑧ submitted_at·valid_until slice ⑨ 서버 오류 매칭 정규식 「기한」 ⑩ 시각 표시). 서버 라벨 「기한」 10자리는 BE 몫으로 넘겼다(코디가 Phase 1 에 추가)
- 코디 판단: ⑤ 유지 · ⑥ 유지(업무 날짜 아님)

## 3. 볼 것
1. **계약 충실도** — WP 체크박스마다 코드(파일:줄). 날짜 넷 순서·이름·값 없는 칸 · 편집 라벨 · 출처 줄 간격·글자 계층 · 「마감일」 라벨·`2026/10/06` 형식 · 유지 자리(OQ-Q ②④)
2. **전수조사가 맞나** — 직접 grep 으로 다시 센다: 「기한」·「희망 기한」·「… 마감」 남은 자리(화면에 나가는 것), `toLocale*`·`slice(0, 10)`·`split("T")`·`replace` 같은 날짜 자르기, 날짜 포맷 함수 사본. 빠진 자리
3. **시간대** — `formatDate` 가 날짜 전용 문자열(`2026-10-06`)을 **하루 밀지 않는지**(브라우저 TZ 가 서울이 아닐 때 포함) · 시각을 서울 날짜로 옮기는 방식이 `Intl`/고정 오프셋 어느 쪽이고 경계 테스트가 실제 경계를 보는지
4. **조용히 통과하는 자리** — 문자열만 바꾼 테스트 · 빈 단언 · 오늘 의존 · 라벨 상수로 옮기며 의미가 바뀐 곳(예: 「시작」이 시작 예정일 뜻에서 다른 뜻으로)
5. **P-5** — DS 토큰 밖 하드코딩 · CSS 가 다른 화면으로 번지는 부작용(`.origin-chip` 전역 규칙)
6. **사용자가 실물에서 만날 자리** — 「막히진 않는데 눈에 이상할」 곳(긴 날짜 줄 줄바꿈, 칩 폭, 표 머리 폭 등) 목록

## 4. 판정
FAIL(계약과 다르게 돈다) · WARN · PASS. 각 지적에 파일:줄 + 근거.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-fe-p2b-report.md` 하나만. 테스트를 직접 돌려도 되지만 **직렬로만**(`npx vitest run --no-file-parallelism <파일>`), 서버·브라우저는 띄우지 않는다

## 6. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_f8b0a2d6-3e7b-41de-b8c1-2acef6635f48 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-009 Phase 2b 코드 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN(파일:줄) / 전수조사 재계수 / 화면 확인 목록 / 리포트 경로"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] reviewer 완료 — Phase 2b 코드 검수 <판정>. 리포트 review-fe-p2b-report.md" --enter
```
