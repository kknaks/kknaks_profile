
# 재개 노트 — admin-chat-insights (kknaks-dev)

**지금**: BE·FE 완료, 코디 검증 통과. **로컬 스택 가동 중**(:48000 back + :3000 dev,
DB 볼륨에 어제 대화 12건 실데이터) — owner 육안 확인 대기.
**다음**: owner 확인 → 커밋·PR(admin-chat-insights → main) → 배포 → 워크 마감.

세팅: `scripts/new-work.sh kknaks-dev admin-chat-insights` · 설정 SSOT `config/projects/kknaks-dev.json`
코디handle: `term_53806a6d-ced5-4948-88bd-4181b7ba4323`

## 워크트리

- `app`: `/Users/kknaks/orca/workspaces/kknaks_profile/admin-chat-insights` (branch `admin-chat-insights`, base `origin/main` → PR `main`)

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
| backend | `term_fea6be18-9b1e-4cd3-b6e0-c2d0822cf096` | `task_1fa387975bcf` | `ctx_6d213eac287d` | `admin-chat-insights-be-brief.md` | **완료** — API 3종+집계, jsonb 'null' 실버그 수정. 코디 재현 **186 passed** |
| frontend | `term_63f64d4e-318d-4eb5-8297-b64a40dea957` | `task_b67b6121139f` | `ctx_82ea84cbee32` | `admin-chat-insights-fe-brief.md` | **완료** — 「방문자 › 채팅」 탭+화면(신규 7·수정 3), tsc 0(코디 재현). sessionId 위치는 spec 확정(conversation 안) |

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
