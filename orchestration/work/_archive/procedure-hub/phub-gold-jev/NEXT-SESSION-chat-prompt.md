# 다음 세션 — Procedure Hub 채팅(상담) 만들기 · 조사부터

연결 시험(phub-gold-jev)은 v06-37 batch 를 마지막으로 끝났다. 이번 세션부터는 **채팅(상담)** 을 만든다. **같은 작업(slug `phub-gold-jev`) · 같은 브랜치에서 이어 간다.** 먼저 아래 정본을 읽고 작업 위치부터 확인해라.

## 정본 · 먼저 읽을 것

- 진행 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/_RESUME.md`(§2 결정 표가 SoT — 정한 것을 다시 묻지 마라)
- 시험 결과: 같은 폴더 `batch-v052-summary.md` · `batch-v06-summary.md`(마지막 판 · 0.5.2 대비)
- 계약: 같은 폴더 `SPEC-001-hub-gold-mcp.md` · `SPEC-002-chat-eval.md`(0.6.0)
- Jev 사용법: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/para/resources/note/ai/llms.txt`(Noul fan-out · Choice 는 하나 고를 때만 · instructions 영어 · 종류 이름 직접)

## 작업 위치(이어서 — 새 브랜치 만들지 않음)

| 무엇 | 경로 | 브랜치 |
|---|---|---|
| 코디 · 문서(프로필 · 공개 레포) | `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` | `kknaksss/프로시저허브-데이터-메달리온` |
| 허브(회사 레포) | `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev` | `kknaksss/phub-gold-jev`(base `release/v1.2.0`) |
| 앱(공개 레포) | `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev` | `kknaksss/phub-gold-jev`(base `main`) |
| silver · gold 데이터(gitignore · 로컬) | `…/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/` | — |

- **세 레포 모두 로컬 커밋까지 됨(11-17 — 앱 `6303e18` · 허브 `85c28af` · 프로필 `b0a3fbad`) · push · PR 은 아직.** 이번 세션 첫 일로 push · PR(분리 — 허브 · 앱 · 프로필 문서)을 올리고 그 위에서 이어 간다. 회사 레포 머지 · stg 는 별도 승인.
- 허브 실행(18105) · 시험 화면(18220) 명령은 앱 README 「실행 안내(e2e)」.

## 이번에 할 것

1. **silver · gold DB 화** — 허브는 지금 CSV 를 메모리로 읽는다(router → service → repository). repository 만 DB 로 바꾸게 지어 두었다. 어떤 DB · 적재 방식 · 해시/빌드 추적(gold_hash · aux_hash)을 어떻게 옮길지.
2. **채팅 — 이전 대화 기억 두 방식 비교**
   - **CLI**: `claude -p --resume`(세션 내부 저장으로 기억) — 지금 구독(Sonnet / Haiku)
   - **SDK**: Anthropic SDK + **프롬프트 캐싱**으로 이전 대화 기억(DB 화와 함께 SDK 로 간다는 결정)
   - 기억 · 비용 · 첫 답 속도 · 캐시 적중 · 재료(gold 묶음)를 대화 사이에 어떻게 들고 가나
3. **상담 프롬프트** — 시험 프롬프트(`앱 prompts/common.md` · `col_b.md` · `judge.md`)와 SPEC-002 §3-2a(LLM 에 싣는 칸) · §3-7(P11 · 이름 목록 FT8)을 참고해 새로 다듬는다. 원칙:
   - 상담은 **짧게 → 필요할 때 깊게**(고민 · 비교 단계는 개요 · 상세가 필요하면 더 깊게) — 시험의 「빠짐없이」 와 다르다(테스트 ≠ 상담)
   - 안전 정보를 처음부터 붙이지 않는다 · 묻지 않은 것 안 붙임 · 우열 판정 안 함(차이를 물으면 각각)
   - 층을 밝힘(물려받음 · 하위) · 앱이 답 문장을 짓지 않음 · 지어낸 숫자 0
   - B(gold + Jev 가 맨 앞에서 판단 · 필요한 것만 LLM 에) 흐름 위에서
4. **조사 먼저** — 1 ~ 3 을 read-only 조사 워커로 시작한다(SDK 는 claude-api 스킬 · 공식 문서 기준 · 추측 금지). 조사 → 결정 → SPEC → WORK → 구현 순서.
5. **화면은 이번에 정하지 않는다** — 사용자가 따로 지시한다.

## 지켜야 할 것

- 오케스트레이션: 조사 · 문서는 orca 워커(fable) · 코드는 opus · 단계 끝나면 리뷰 워커 자동 · 발주 전 사용자 승인 · e2e 지적은 모아서 한 번에.
- 회사 데이터(원장 · silver · gold · 질문 · 답)는 공개 레포(kknaks_profile · clinic_chat)에 커밋하지 않는다. 키 값 출력 금지 · 워커는 .env 를 열지 않는다.
- 사용자 포트 18210 · 18005 금지 · canonical 체크아웃은 pull/checkout 금지(fetch 만).
- 디스크 여유가 2 ~ 3GB 였다(11-17) — 큰 파일 주의.
- 답은 한국어 · 짧게 · 결정은 추천을 붙여 묻는다 · 정한 건 되묻지 않는다.
