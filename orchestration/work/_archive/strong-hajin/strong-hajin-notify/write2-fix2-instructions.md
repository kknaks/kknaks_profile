# [writer] 알림 2판 수정 2 — 재검수 r2 FAIL 1 · WARN 6

정본: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-spec-work-r2-report.md` §11(줄 번호까지 있다). 사용자 결정 필요 없음 — 아래 택일은 코디가 정했다.

## allowed_paths
SPEC-011 · SPEC-006 · SPEC-008 · WORK-013 · DEC-010(머리 blockquote 의 판 표시 한 줄만)

## 고칠 것
- **R-F1**: 권장안 (a) — **연결의 둘째 이후 `ready` = 다시 읽기(resync 와 같은 효과)**. 순번이 있든 없든 재연결이면 메시지함·설정 연동이 다시 읽는다(지금 WS 동작과 같거나 낫게). 검수표의 줄 전부 + AC-02·02b · SPEC-008 §4.4 · WORK WP1-FE·시험
- **R-W1**: 기준 줄을 못 찾으면 **「그 순번 이하 가운데 가장 큰 순번 줄의 `updated_at` − 60초」**, 그것도 없으면 resync(= 다시 읽기)로
- **R-W2**: P-8 의 직접 호출을 Makefile 타겟으로 — `make test-contract-serial FILES="…"` · `PYTEST_ADDOPTS='-k …' make test-contract` · `PYTEST_ADDOPTS=… make test-postgres` (검수표 근거 `Makefile:76-91`)
- **R-W3**: 남은 수·판 정정 전부(W13 :49 · :98 · :264 · :379 · S11 :39 · DEC 머리 「2판 수정 1·2」)
- **R-W4**: OQ-1102 제안을 「거부면 다시 묻지 않는다 — 안내 줄은 2루프 후보(I-8)」 로
- **R-W5**: 묶음 알림 = `notification_id: null` · 클릭하면 읽음 없이 **알림 목록 화면만** · `target = {surface: "notifications"}` 를 SPEC-011 §4.6 · §4.5-2-3 · SPEC-006 :468 에
- **R-W6**: 연속 **10회** 실패면 재연결을 멈추고 다음 화면 활성·포커스 때 다시 시작

## 끝나면
- WORK 부록 3 에 r2 대응 행 추가 · 다른 파일 금지 · 커밋 금지
- 완료 보고는 앞 브리프 §7 두 명령. subject 「writer 완료: 알림 2판 수정 2」 · text 「[worker_done] writer 알림 2판 수정 2 완료 — <한 줄>」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
