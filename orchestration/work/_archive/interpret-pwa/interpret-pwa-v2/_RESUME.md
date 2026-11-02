
# 재개 노트 — interpret-pwa-v2 (interpret-pwa)

**지금**: DEC-001 D-39 ~ D-41 기록 · 조사 3갈래 진행(r1 zh 검증+새 시술 · r2 ja/en/zh-Hant · r3 th/vi/yue)
**다음**: 조사 합쳐 시드 반영 범위 확정(사용자) → planner SPEC 0.6(시드 추가 · 통역 기록 D-41) → backend(시드 · 기록 JSONL · 7일 삭제) + infra(PVC) → 배포 → 마감(ignored 파일 확인)

세팅: `scripts/new-work.sh interpret-pwa interpret-pwa-v2` · 설정 SSOT `config/projects/interpret-pwa.json`
코디handle: `<코디handle — stale 이라 미치환. 직접 확인해 채울 것>`

## 워크트리



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
