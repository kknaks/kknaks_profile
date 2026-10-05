# [reviewer] WORK-010 Phase 2a 코드 검수

같은 reviewer 다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only** — 리포트 한 장만.

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` — Phase 1 커밋 `7f01c5b` 이후의 미커밋 diff 중 업무 상세 관련(`features/work/`·`MyWorkPage`·`TodayPage`·`CalendarPage`·`styles/task-detail.css`·`ds/` 변경·`App.tsx` 의 AX 정리·테스트)
⚠ 같은 워크트리에 Phase 3(셸) 미커밋 변경(`frontend/src-tauri/`·`lib/shell.ts`·`App.tsx` 다운로드 수신부·`labels.ts` `shellDownload`)이 있을 수 있다 — **대상 아님.**

## 2. 기준
- **SPEC-007 v0.5.1** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` — §2.10.1 · §2.10.2 · §2.10.4 · §2.10.7 · §2.10.8 · §2.10.9(2a 몫) · §6 「고도화 3차」 AC. SPEC 이 정본
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md` 해당 Phase 체크박스
- 워커 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-p2a-worker-report.md`
- 조사 `fe-survey-report.md` §4·§5·§6 · `be-survey-report.md` §4 · 기준선 `flaky-baseline-evidence.md`

## 3. 볼 것
1. SPEC 절·WP 체크박스마다 PASS/FAIL(파일:줄)
2. **인라인 저장** — 직렬 대기열이 정말 직렬인가(두 필드를 빠르게 연달아 고칠 때) · 앞 응답 version 이어받기 · 422 stale = 다시 읽고 서버 값 · 실패 원복 · 안 바뀜=요청 없음 · IME · 호출부 3곳(내 업무·홈·캘린더)이 모두 새 version 을 돌려주나
3. **헤더** — kicker·상태·버전·편집·AX 가 정말 없나 · AX 묻기 심볼이 남아 있지 않나(`askAboutTask`·`onAskAboutTask`) · 공용 `Modal` 변경이 다른 12 표면에 번지지 않았나
4. **메타 정보** — 행·순서·읽기/편집 구분·빈 행 규칙·마감일 초과 배지·출처 「판단 보기」/글자만
5. **읽기 전용 입구 10곳**에서 편집 요소가 하나도 안 열리나
6. **2a 범위 밖을 건드리지 않았나** — 푸터 상태 단추·「진행과 판단」·`scax-blocked-note`·목록 행은 이 페이지에서 그대로여야 한다(2b 몫). 「변경 저장」만 사라져야 한다
7. 여백이 업무 상세 스코프에서만 바뀌었나
8. 워커 미결 「`askAboutTask` 삭제로 채팅 참고 자료 칩·`loadContextOptions` 조회가 죽은 경로」 — 정말 죽었나(다른 진입 0인지) 판정하고, 지울 범위를 파일:줄로 적어라(2b 에서 정리할지 코디가 정한다)
9. `ds/Modal.tsx`(title ReactNode)·`ds/InlineText.tsx`(Esc 전파 끊기) 공용 부품 변경이 다른 사용처를 깨지 않나
- **쓰는 곳 전수** — 워커가 센 grep 표를 직접 다시 세어 빠진 자리가 없나(입구 16곳 · 호출부 3곳 · 공용 부품 사용처)
- **조용히 통과하는 자리** — 빈 단언·개명·폴백·지운 테스트(계약이 「없다」로 바뀐 것은 지우지 말고 뒤집었어야 한다)
- **사용자가 실물에서 만날 자리** 목록(눈으로 이상해 보일 곳)
- 테스트를 돌려도 된다(`frontend` 에서 `npx vitest run --no-file-parallelism`, 기준선 5건 분리) — 서버·프론트는 띄우지 마라

## 4. 판정
FAIL · WARN · PASS. 각 지적에 `파일:줄` + 근거.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/review-fe-p2a-report.md` 하나

## 6. 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-010 Phase 2a <PASS|WARN|FAIL>" --body "판정 / FAIL·WARN(파일:줄) / 실물 자리 / 리포트 경로"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] reviewer 완료 — Phase 2a <판정>. 리포트 review-fe-p2a-report.md" --enter
```
