# [backend] case3 WP-4 관계 어댑터 구현

너는 앱 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 기존 미커밋 coverage 코드를 이어간다. 기준 HEAD `078ac99`.

## 계약

- 프로필 레포 `orchestration/work/phub-recommend/WORK-011-public-contract-handoff.md`, `WORK-012.md` WP-4, `SPEC-006.md` 0.3.10 §3-4-1-5와 `SPEC-005.md` §5-5·§6-9를 읽는다. Hub 구현은 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`의 현재 미커밋 코드·시험을 읽기 전용으로 참조한다.
- 관계 facet I-06/07/08/11은 확정 단위 시술 pair와 Q139 전역 scope를 별도 frontier로 유지한다. `POST /procedure-hub/gold/pairs/selected`, `/procedure-hub/gold/global-claims`의 `cursor/more/complete/status`를 끝까지 수집한다. Hub 호출별 64/32 KiB 상한은 전체 그래프 탐색 중단 조건이 아니다.
- claim/resolved/대안별 fact ID, 원문, source file/path, applies_to의 pair·방향·조건, `quotable`을 원장에 보존한다. 선택 pair/조건과 출처가 맞지 않거나 `quotable=false`이면 지원 사실로 세지 않는다. `truncated/error` 또는 cursor 모순은 해당 범위 incomplete이며 `empty`는 범위 완료 증거가 있을 때만 부재로 판단한다. 전역 메모는 R8 edge fact를 대체하지 않는다.
- REST 오류를 미수신 상태로 정규화하고, 앱/Hub build hash가 다르면 지원·부재 완료를 막는다. 현재 사용자 서버는 새 경로 404이므로 실물 서버를 호출하거나 갱신하지 않는다. Hub 격리 fixture·mock 응답으로 코드를 시험한다.
- 기존 WP-1~3/5 PASS 경로, `walk_coverage_mode=False` 기본값, 근거 선별과 부분 답/안전 검증을 유지한다.

## 검증/보고

- Q018.1/R8-0163, Q064.1/R8-0075, Q139.1/2/R8-0218/0219, Q173.1/R8-0111과 전역 Q139 scope의 접근 회귀를 fixture로 검증한다. 선택 관계의 방향·조건·공유 claim·대안·페이지 2+·빈/오류/불일치 빌드를 음성 시험한다. 모델/서버·DB·50/239×3 평가는 실행하지 않는다.
- 관련 및 전체 pytest, ruff, diff check. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-wp4-relation-report.md`. 완료 시 `worker_done` 한 번.
