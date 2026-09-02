
# 재개 노트 — poc-windows-key-derivation (mykakao)

**지금**: <한 줄 — 어디까지 왔고 무엇을 기다리나>
**다음**: <재개하면 바로 할 것 하나>

세팅: `scripts/new-work.sh mykakao poc-windows-key-derivation` · 설정 SSOT `config/projects/mykakao.json`
코디handle: `term_eda12742-b6d9-434d-8eb8-f534be92dcc3`

## 워크트리

- `app`: `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation` (branch `poc-windows-key-derivation`, base `origin/main` → PR `main`)

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

---
## §3 발주 상태 (2026-09-02 세팅)
- Run: `run_562b2ec38263`  · 목적: Windows 카톡 키유도 spike
- Task: `task_056580856b93`  · status: dispatched
- Dispatch: `ctx_f62ed5eee8b9` (dispatch-show 의 두 번째 id)
- 코디handle: `term_eda12742-b6d9-434d-8eb8-f534be92dcc3`
- 워커handle(backend): `term_0f75ed4f-440d-43ef-a670-523b7b65aef7`
- 성격: **spike** — PR 없음. 산출물 = 조사 리포트 + 실증 코드. 결과가 baseline/decision 입력.
- 완료 캐치: 워커가 2채널로 깨움. 폴링 금지.

## §4 종료 (2026-09-02) — spike done
- 판정: **(C) 구조 상이 + 부분 (D) 로컬 미영속.** macOS 키유도 모델 Windows 이식 불가.
- 코디 정찰의 ESE 가설은 **틀림** — .edb 는 SQLCipher(WAL). 단 macOS 78-hex 메시지 DB 는 디스크에 없음.
- 산출물(워크트리, 비커밋): backend/probe_windows.py · tests/test_probe_windows.py(8 passed) · PROBE_REPORT.md
- 검증(코디, 실물): pytest 8 passed / 실값유출 0 / 원본 DB 미수정(mtime 17:45<조사 17:57) / mask()·합성픽스처 확인
- 열린 결정(사용자): ①KakaoTalk.exe 키파생 RE(범위밖·큰비용) vs ②Windows 미지원 전제(mykakao=macOS 전용)
- Task completed / worker released(retained). PR 없음.
