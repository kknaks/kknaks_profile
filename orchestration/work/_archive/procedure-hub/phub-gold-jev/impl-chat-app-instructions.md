# [app] 상담 채팅 1판 구현 — WORK-011(SPEC-004 0.1.0)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만 그대로 써라(핸들은 preamble 값). **그 브리프의 WORK-002 · 3열 시험 · 32 문항 · 「허브 준비」 문구는 옛 판이다 — 이번 일은 아래가 앞선다.** 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(HEAD 6303e18 위에 이어서 · 커밋하지 마라 · 공개 레포).

11-17 사용자 결정: Procedure Hub 데이터 · medikit 은 공개 — 이 둘의 본문은 공개 레포에 둬도 된다. **키 · 비밀값 · 사용자 홈 절대 경로 · 내부 URL 은 커밋될 파일에 넣지 마라(그대로).** 원본 얼굴 PNG(`/Users/kknaks/Downloads/…`)는 밑그림 참고만 — 레포에 넣지 마라.

**이번 일 = `WORK-011-consult-chat.md`(같은 폴더) WP-0 ~ WP-10 전부.** 계약 = `SPEC-004-consult-chat.md` 0.1.0. `_RESUME.md` §2 11-17 행(프롬프트 JSON · 디자인 킷 · medikit 공개 · U-11~13 (a) · SPEC-004 검수 뒤 코디 W-1~W-8 · **WORK-011 B 코디 답**) · 검수 `review-spec-004.md` · `review-work-011.md` 반영.

## 검수 WARN — 이렇게 닫아라(구현 전)

- **W-1**: 든 후보(앞 턴 대상)는 `concepts` 와 **따로** 든다 — 겹침 묶음(TG3 범위 규칙) · 상품 이름 덮임(EN1) · 입구 고르기 재료에 넣지 않는다. T12 에 「든 후보 둘(표가 다름)이 둘 다 yes → 둘 다 대상 · `overlap` 0」. G7 이 든 대상에 안 걸리는 것은 받아들임(gate 동결). 함께 쓰는 코드에 손대는 줄이 늘면 보고.
- **W-2**: WP-7 은 `walk(question, deps)` 로 짓고 `sites` 는 빈 조각 자리만 → WP-8 이 `sites` 를 채움 → WP-9 가 `carry` · `instr` 를 건다. T6 은 WP-9 끝에 한 번 더.
- **W-3**: ① 오류 이벤트 이름 `turn_error` · 닫기 `close`(본문의 `error` 를 그렇게 읽어라) ② `close` 는 `data:` 줄을 가진다(빈 값이어도) ③ 빈 `sites` 는 빈 글자가 아니라 **빈 요소**(받는 자리 통째) ④ 가짜 턴에 `turn_error` 로 끝나는 꼴 하나 ⑤ T6 · T10 에 「조각 글자 길이 > 0」.
- **W-4**: 기존 `tests/test_*.py` 24 · `conftest.py` · `fake_hub.py` · `fake_jev.py` 는 **고치지 않는다**(가짜는 더하기만). WP-10 에 `git diff --stat tests/` — 기존 시험 파일 변경 0.
- **W-5**: `consult.css` 에 `@font-face` 한 블록(본 `CENTURION_DAY/backend/day/static/day.css:108-113` 꼴 · 같은 폴더 상대 주소).
- NOTE 11 은 WORK · 리포트대로(절 번호 어긋남은 리포트 표 기준으로 읽어라).

## 포트 · 프로세스

- 네 확인 서버 = **18223**(띄우기 전 `lsof` · WP 끝에 스스로 내림 · `lsof` 0 줄 보고). 18222 는 코디가 띄운다.
- 허브 **18105 는 지금 DB 판** — HTTP 읽기(도구 호출)만. 띄우기 · 내리기 · 다시 띄우기 금지. 18106 · 18220 · 18221 · 18210 · 18005 · 18432 건드리지 마라.
- Jev · CLI 구독 실물 호출은 WORK 의 E 걸음만(E1 CLI 3턴 · 짧은 글 · 회사 자료 없이 시작). 구독이 네 세션에서 안 잡히면 「못 돌림」 보고(코디가 돌린다).

## 단계 보고

- **WP-0(E1 · E2 실측) 끝나면** 결과(`--max-turns 1` 받나 · 기억 이어짐 · 턴별 첫 글자 ms · cache_read/creation · 세션 파일 자리 · 다른 cwd resume · F7 스냅숏)를 `[진행] app: WP-0 …` 한 줄로 코디에게 보내고 **이어서 진행**. `--max-turns` 를 안 받으면 멈추고 `[질문]`.
- 얼굴 좌표 초안 · 화면이 서면 `[진행] app: 화면 준비 — 18223 …` 한 줄(코디가 사용자 눈 확인을 받는다).
- 완료 조건: WORK 의 워커 몫 전부 · ruff · pytest(단계마다 그 WP 시험 · 전체는 끝에 한 번) · 공개 grep 0.
