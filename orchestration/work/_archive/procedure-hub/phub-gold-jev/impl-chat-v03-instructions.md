# [app] 상담 채팅 0.3 구현 — WORK-014(SPEC-006 · 허브 SPEC-001 0.7.2 칸)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만 써라(핸들은 preamble 값 · 그 브리프의 WORK-002 · 3열 시험 문구는 옛 판). 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(HEAD 68a31b1 위 · 커밋 금지 · 공개 레포). Procedure Hub 데이터 · medikit 공개. 키 · 홈 절대 경로 · 내부 URL 커밋 금지.

**이번 일 = `WORK-014-consult-v03.md`(같은 폴더) WP-0 ~ WP-8.** 계약 = `SPEC-006-consult-v03.md` + 앱이 읽는 허브 칸은 `SPEC-001-hub-gold-mcp.md` **0.7.2**. `_RESUME.md` §2 11-17 맨 위 행들 · `review-spec-006.md` · `review-work-014.md` 반영.

## ⚠ 시험 — 사용자 지시(11-17)

**WP 마다 그 WP 시험 파일만 돌린다. 전체 pytest 금지.** 돌린 파일 목록 · 통과 수를 WP 별로 보고. 끝에도 전체를 돌리지 않는다(코디가 정한다).

## 손대지 마라

`clinic_chat/consult/templates/_face.svg` · `clinic_chat/consult/face_coords.py` · 허브 레포. 18105 · 18222 · 18220 · 18210 · 18005 · 18432 프로세스(18105 는 GET 만).

## 검수 WARN · B — 코디 답(이대로)

- **W-1(0.7.2)**: SP 판정은 허브가 한다 — 앱은 응답의 `site_applied` · `site_prefer` 만 읽는다(묶음마다). 한 턴에 고민이 여럿이라 filter 묶음 · prefer 묶음이 섞이면 **묶음마다 자기 값대로** 그린다. SP-6 · SP-T3 을 0.7.2 판정(물은 부위가 고민 부위 안일 때만 filter)으로 읽어라.
- **W-2**: `test_consult_page.py` T24 의 `data-slot` 수 8 은 **A8(사용자 결정 — 드로어 · 객체 패널) 때문에 바뀌는 예외로 고쳐도 된다** — 고친 줄과 까닭을 보고에. 그 밖 기존 시험은 그대로.
- **W-3 · B-10**: WP 별 시험 목록에 빠진 것을 넣는다 — `test_state_examples.py`(S5-T15)는 WP-7 · tail 은 WP-4 · state/plan 은 WP-7 · ledger 는 WP-1. 표에 없는 기존 시험은 **그 WP 가 건드린 파일의 시험**을 그 WP 에서 돈다.
- **W-5**: S6-T2 를 두 꼴로(앞 `ask` 없음 = `resolve` 뿐 / 있음 = 걷기 끝까지 돌고 재료만 버림) · E6-3 에 그 턴 조회 수를 따로.
- **W-9**: EM6 시험 꼴은 WP-6(descended) 뒤로 옮긴다.
- **B-2**: 하위 고민을 누르면(viewing) 객체에 **`said` 가 아니라 WORK 가 정한 `how=view`** 로 든다(손님이 말한 것이 아니다).
- **B-5**: `rev_changed` 로 거절한 턴은 장부 줄을 쓰지 않는다 — WORK 대로(보고에 한 줄).
- **B-9**: 시험 앱 걷기 · 답 키 쪽 SP 는 이번 일 밖.
- 나머지 WARN · NOTE 는 리포트 「고칠 방향」 대로.

## 실물 · 보고

- 네 확인 서버 = **18223**(CHAT_STATE=on · CHAT_DEBUG_PANEL=on · 끝나면 내림 · `lsof` 0). 허브 0.7.2 칸은 **아직 18105 에 없다**(허브 구현이 병행 중) — 실물 E6 은 0.7.2 칸 없이 도는 꼴까지 · 0.7.2 칸이 드는 E 는 「허브 대기」 로 보고(코디가 허브 재시작 뒤 돌린다).
- `curl` 은 `--data-urlencode`.
- 단계 보고: WP-0 · WP-4 · WP-8 끝에 `[진행] app: …` 한 줄.
