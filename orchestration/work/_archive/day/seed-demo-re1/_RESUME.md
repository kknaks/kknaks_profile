
# 재개 노트 — seed-demo-re1 (day)

**지금**: <한 줄 — 어디까지 왔고 무엇을 기다리나>
**다음**: <재개하면 바로 할 것 하나>

세팅: `scripts/new-work.sh day seed-demo-re1` · 설정 SSOT `config/projects/day.json`
코디handle: `term_e62e850f-aae8-4092-a945-6f9406c2af07`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/seed-demo-re1` (branch `kknaksss/seed-demo-re1`, base `origin/dev` → PR `dev`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] <진행 중 — 누가 · 무엇을>
- [ ] <다음 할 일>
- [!] <막힌 것 · 사용자 게이트 · 주의>

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| <YYYY-MM-DD> | <무엇을 정했나> | <사용자 지시 · 조사 리포트 · 리뷰 판정> |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| <planner> | `<term_…>` | `<task_…>` | `<ctx_…>` | `<…-spec-brief.md>` | <발주 · 진행 · 완료 · 검수중> |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `<YYYY-MM-DD>` <무슨 일이 있었나 — 한 줄>

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.

## 코디 기록 (2026-11-12)

- 목표(사용자): 데모 지점 테스트 데이터 시드 = 「방 배정」 기본 · 한국어 이름 · 상담 양식 오더 메모 · 시술 4개 이상 — `scripts/seed_demo_board.py` 고침(「코드는 고쳐 놔야 할 거 아니야」)
- Delivery 없음(개발용 스크립트 · 제품 기능 · 계약 변화 없음)
- 발주: backend `term_3aae8b41-becd-44cb-ac22-b88605bfdfbb` · `task_a9cc8c6e7437` · `ctx_b6e9c071ba7f` · 브리프 `seed-demo-re1-be-brief.md`
- 다음: worker_done → reviewer 자동 → 코디가 데모 지점 1회 실물 → 코드 PR(→ dev) · 머지는 사용자
