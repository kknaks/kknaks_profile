# [app] 상담 채팅 0.2 구현 — WORK-012(SPEC-005 0.1.0 상담 객체)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만 써라(핸들은 preamble 값 · 그 브리프의 WORK-002 · 3열 시험 문구는 옛 판). 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(0.1 + 수정 1 미커밋 위에 이어서 · 커밋 금지 · 공개 레포). Procedure Hub 데이터 · medikit 은 공개. 키 · 홈 절대 경로 · 내부 URL 은 커밋될 파일에 넣지 마라.

**이번 일 = `WORK-012-consult-state.md`(같은 폴더) WP-0 ~ WP-8 전부.** 계약 = `SPEC-005-consult-state.md` 0.1.0(+ 0.1 의 `SPEC-004`). `_RESUME.md` §2 11-17 행(U5 추천 · U5-4 (a1) · SPEC-005 검수 뒤 코디 W-1~W-9 · **WORK-012 B 코디 답** · 사용자 테스트는 0.2 뒤) · 검수 `review-spec-005.md` · `review-work-012.md` 반영. 0.1 쪽은 `impl-chat-app-report.md` · `app-chat-fix1-instructions.md` 로 파악.

## 손대지 마라

- `clinic_chat/consult/templates/_face.svg` · `clinic_chat/consult/face_coords.py` — 사용자 지시로 다른 세션이 바꿨다(좌표표 꼴 · 키만 쓴다).
- 기존 `tests/test_*.py` · `tests/conftest.py`(더하기만은 새 파일로).

## 검수 WARN — 이렇게 닫아라(코디 값)

- **W-1 부위만 대상인 턴**: (가) — 리스트를 곧바로 짓지 않고, 그 부위의 고민(`concern_site`)을 선택지로 빈 칸 질문(자연스러운 질문 하나)을 낸다. 시술 · 제품 · 계열 대상은 묶음 ①(WP-6)대로. 리포트 §3-2 의 WP-1 · WP-4 · WP-6 줄을 그대로 넣어라.
- **W-2 같은 이름 고민 · 부위**(실물: 「팔자주름」 = `CON-009` · `SITE-046` 둘 다 `target`): 그 부위는 `sites[]` 에 넣되 `source` 에 짝 고민 코드를 단다 · QY1 · QY5 의 부위 거르개는 **그 짝 고민이 `focus` 일 때만**. §13 표 ② 턴 1 고침.
- **W-3**: 코드 기본값 `CHAT_STATE=off` · 켜는 값은 **프로세스 env 로만**(`.env` 에 두지 마라) · `.env.example` · README · WP-0 설정 칸을 그렇게 · 새 시험은 설정에서 `on` 명시 · **WP-8 `--e5` 와 18223 서버는 `CHAT_STATE=on` 을 붙인다** · E5 보고에 장부 시작 줄 `consult_state: "on"` 확인.
- **W-4**: 앞 턴 `ask` 의 `options[]` 의 (표, 코드)가 이번 턴 대상으로 확정되면(걸린 선택지 yes **또는 이번 글의 `target`**) 답한 것 · `how=text` · `from_ask` 채움. S5-T3 · T9 에 그 꼴 하나.
- **W-5**: 서버로 확인할 때 `curl --data-urlencode "text=…"` · 보낸 뒤 장부 시작 줄 `question` 이 보낸 글과 같은지 본다.
- **W-6**: WP-3 · WP-5 첫 걸음에 허브 18105 GET 한 건씩(`scope` · `facets` indication · `pair`)으로 응답 키 확인 · 보고에 적기(Jev · CLI 실물은 WP-8 뿐).
- **W-7**: `plan` 은 걷기의 `Call` 을 그대로 지어 `key()` 로 견준다(부위 거르개 값도 걷기와 같은 꼴 — 이름 글자) · E5-1 에 「걷기와 겹친 조회의 `skipped` 수」.
- **W-8**: E5-1 보고 값에 「턴마다 QY1 의 `site` 값 · 리스트 행 수」 · W-1 꼴(부위만 대상) 한 문장 · W-2 꼴(같은 이름 뒤 `focus` 이동) 한 문장을 `e5.py` 에.
- NOTE 9 는 리포트대로.

## 포트 · 프로세스 · 보고

- 네 확인 서버 = **18223**(`CHAT_STATE=on` · 끝나면 내림 · `lsof` 0). 18222(사용자 화면 · 코디가 0.2 뒤 재시작) · 18105(읽기만) · 18220 · 18210 · 18005 · 18432 건드리지 마라.
- 단계 보고: WP-0 끝 · WP-5 첫 걸음(pair 키) 때 `[진행] app: …` 한 줄씩, 이어서 진행.
- 완료 조건: WORK 의 워커 몫 전부 · ruff · pytest(env 없이 = 끈 상태 전체 · 새 시험) · E5-1~E5-5 실물 · 공개 grep 0 · 「코디: 18222 를 `CHAT_STATE=on` 으로 재시작 필요」 한 줄.
