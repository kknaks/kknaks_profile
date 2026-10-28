# [backend] WP-KOS — 예약 현황 KOS 데모 실호출 확인 (코드 변경 없음)

너는 **cc-prototype `backend` 워커**다. **앞 판의 맥락이 없다.** 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리(코드): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` (branch `kknaksss/overall-board`) — **이번 판은 코드 변경 · 커밋 없음**

## 1. 무엇을 하나

`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-007-reservation-board.md` 의 **WP-KOS 행 그대로**(K1 ~ K10). 기준 계약은 같은 폴더 `../20-spec/spec-005-reservation-board.md`(§3.3 · §4 · §5.6 · §8 「미확인」 줄 · §10 OQ-728 · OQ-739 · OQ-753 ~ OQ-756). KOS 근거 리포트는 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-*-report.md`(특히 create · move-cancel · reception-test · visitor-update · room). HAR 은 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/`(gitignore · **`처방전*.har` 은 실제 지점 — 읽지 마라**)

⚠ SPEC-005 는 지금 reviewer_doc 검수 중이다(r1). 본문은 바뀔 수 있다 — WP-KOS 는 **KOS 가 무엇을 받는지**를 확인하는 판이라 SPEC 문구에 매이지 말고 KOS 사실을 적어라.

## 2. 데모 쓰기 허가 범위

사용자(2026-10-26): 「데모 지점은 테스트 해봐도 돼」. **데모 테넌트에 한해** K1 ~ K10 의 호출만. 호출 전 테넌트 assert(procedure `.env` 의 데모 값 · 운영 명동점 키 `KOS_API_tenent` 금지). 각 쓰기 1회 · 재시도 금지(실패는 응답 그대로 · 값 가려서). 시험용 고객 · 예약은 만들어도 된다(리포트에 「시험용으로 만듦」 · 지우지 않음). 시술 대기로 둔 일정은 K9 에서 귀가까지 진행해 끝내 둔다(시술 현황 E2E 를 어지럽히지 않게). **사용자 스택(3700 · 8700) · 사용자 프로세스 건드리지 않음** · env 값 출력 금지 · 호출은 일회성 스크립트(레포에 남기지 않음 · back `KosClient` import 가능)

## 3. 산출물

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-kos-probe-report.md` — WORK-007 WP-KOS 완료 조건 그대로(K1 ~ K10 표 · 판정 한 줄씩 · `funnel` 요청 모양 · 남긴 데모 데이터 목록). **public — KOS id · 키 · 토큰 · 실명 · 고객 값 0**(완료 조건의 grep = 0)

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 같은 워크트리 · 코드 워크트리의 다른 코디 세션으로 보내지 마라.

```bash
orca orchestration send \
  --to term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --from <네 handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "backend WP-KOS 완료: <판정 요약 한 줄>" \
  --body "리포트 경로 / K1~K10 판정 / 안 받음 · 모양 다름 목록 / 쓰기 수 · 운영 키 0 / 남긴 데모 데이터"

orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 \
  --text "[worker_done] backend WP-KOS 완료 — <한 줄>. 상세는 reservation-kos-probe-report.md" --enter
```
