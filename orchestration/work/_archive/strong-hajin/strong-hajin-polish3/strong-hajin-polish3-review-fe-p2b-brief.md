# [reviewer] WORK-010 Phase 2b 코드 검수

같은 reviewer 다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only** — 리포트 한 장만.

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` — Phase 2a 커밋 `cc64d18` 이후의 미커밋 diff 전부(`frontend/src/`)
⚠ Phase 3(셸)는 커밋됐다(`9c15934`). `App.tsx` 다운로드 수신부(`onShellDownload`)가 이번 diff 에서 바뀌었으면 **FAIL**.

## 2. 기준
- **SPEC-007 v0.5.1** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` — §2.10.1(`⋯`) · §2.10.3 · §2.10.5(상태×역할 표) · §2.10.6 · §2.10.9(전수) · §5 동시성 · §6 「고도화 3차」 AC. SPEC 이 정본
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md` 해당 Phase 체크박스
- 워커 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-p2b-worker-report.md`
- 조사 `fe-survey-report.md` §4·§5·§6 · `be-survey-report.md` §4 · 기준선 `flaky-baseline-evidence.md`

## 3. 볼 것
1. SPEC 절·WP 체크박스마다 PASS/FAIL(파일:줄)
2. **진행 상태 셀렉트 옵션**을 SPEC §2.10.5 표와 **칸마다** 대조(상태 × 역할 × 요청/일반) · 확인 대기 = 글자만 · 서버 허용표(be-survey §4-5)를 화면이 앞지르거나 새 규칙을 만들지 않나
3. 사유 모달(막힘·취소 필수 / 재개 선택) · 완료 보고 모달 · 남은 단계 확인창 · 409 = 서버 문장 토스트 + 셀렉트 원래 값 · 모달 닫으면 원복
4. `⋯` = 요청자만 · 담당 셀렉트 = `canAssign && !readOnly` · 제안 중 표시 · 대기 제안 시 재열림 없음
5. **걸린 일 상자** — fe-survey §4-3 구획 1~5·7 이 조건대로 서고 안의 단추 조건이 그대로인가
6. **푸터 없음**(빈 줄도 없음) · 「진행과 판단」 없음 · SPEC §2.10.9 대조표가 맞나 · 목록 행 `TaskQuickActions`·공용 `.scax-blocked-note` 는 그대로(W8)
7. **2a WARN 합친 것** — W1 전이·담당·체크리스트가 인라인 저장과 같은 직렬 대기열인가 · W2 죽은 AX 참고 자료 경로가 정말 다 지워졌고 남은 채팅 기능(현재 화면 맥락 등)을 깨지 않았나 · W3 글자 뜀·캐럿 · W4 저장 중 표시 · W5 성공 시 전역 오류 걷기
8. 회귀 — 내 업무 목록 상태 칸·프로젝트 우 패널(상태 셀렉트 부품을 나눴다면)
- **쓰는 곳 전수** — 워커가 센 grep 표를 직접 다시 세어 빠진 자리가 없나
- **조용히 통과하는 자리** — 빈 단언·개명·폴백·지운 테스트(계약이 「없다」로 바뀐 것은 뒤집었어야 한다)
- **사용자가 실물에서 만날 자리** 목록 — 이번이 마지막 페이지다. **사용자 E2E 체크리스트 초안**(상태별 업무 하나씩 무엇을 눌러 무엇이 보여야 하나)을 리포트 끝에 붙여라
- 테스트를 돌려도 된다(`frontend` 에서 `npx vitest run --no-file-parallelism`, 기준선 5건 분리) — 서버·프론트는 띄우지 마라

## 4. 판정
FAIL · WARN · PASS. 각 지적에 `파일:줄` + 근거.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/review-fe-p2b-report.md` 하나

## 6. 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-010 Phase 2b <PASS|WARN|FAIL>" --body "판정 / FAIL·WARN(파일:줄) / 실물 자리 / 리포트 경로"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] reviewer 완료 — Phase 2b <판정>. 리포트 review-fe-p2b-report.md" --enter
```
