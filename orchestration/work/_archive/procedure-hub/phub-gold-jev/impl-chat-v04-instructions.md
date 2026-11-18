# [app] 상담 0.4 구현 — WORK-017(SPEC-008 0.2.0 · 소넷 입구)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만 써라(핸들은 preamble 값 · 그 브리프의 WORK-002 · 3열 시험 문구는 옛 판). 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(HEAD be1c622 · **커밋 금지 · 공개 레포**). Procedure Hub 데이터 · medikit 공개. 키 · 홈 절대 경로 · 내부 URL 커밋 금지.

**이번 일 = `WORK-017-consult-v04.md` WP-0 ~ WP-12.** 계약 = `SPEC-008-consult-entry.md` 0.2.0. 결정 = `_RESUME.md` §2 맨 위 11-18 행 전부. 검수 `review-work-016-017.md` 의 앱 몫(R-2 · R-3 · R-4 · R-5)을 아래대로.

## 검수 반영(코디 답 · 이대로)

- **R-2**: §15-4 에 끈 대화 시험 넷(`test_v03_prompt` s6_t8 · s6_t9 · `test_v03_frame` s6_t29 · `test_state_blanks:119`) — 리포트 처분 제안대로(끈 대화 0.1 동작을 보는 부분은 「장부에 off 시작 줄을 둔 옛 대화 = 열기만 · 턴 막힘」 으로 고치고, s6_t8 앞 반(켠 대화 = v3)은 그대로). 까닭 = CP1 · CP7.
- **R-3**: 채점기 차례 — ⓐ 고치기 **전에** `research-input-space/` 의 다섯 산출물(now-turns · pick-*-turns · fail-by-tag · summary · fan-*)을 네 scratchpad 에 복사(「고치기 전 실행」 금지) ⓑ `INPUT_SPACE_OUT` 은 **쓰는 자리만** 바꾼다(표 · RUN 읽기 그대로) ⓒ 끝 조건 = 고친 score.py 를 `INPUT_SPACE_OUT=<임시>` 로 옛 장부에 돌려 ⓐ summary 와 견줌(기준 차이는 보고). **조사 산출물을 덮지 마라.** 0.4 결과는 `research-input-space/runs/v04*` · `INPUT_SPACE_OUT` 자리로만.
- **R-4**: X-28 — `turn.py:479` viewing 의 `source` 를 OU12 꼴로 · `sure` = `null`(손님 말이 아님 · how=view). `e3.py` · `e5.py` 는 B-8 과 함께 안 고침.
- **R-5**: `pick` 프롬프트의 머리 글자 = 답 요약 줄 「앞 답 요약:」 · 리스트 줄 「보여 준 리스트:」 · `marks.same_list` = 「(앞과 같음)」 — 손님에게 안 보이는 글 · **초안 · 사용자 확인 대상**(version `-draft`).
- B 표 · 열린 것은 WORK 대로 · U8-3 막는 화면 문구는 빈칸(`data-slot` 만).

## ⚠ 시험 — 사용자 지시

**WP 마다 그 WP 시험 파일만 · 전체 pytest 금지.** 돌린 파일 · 통과 수 WP 별 보고 · 끝에도 전체 금지. 바뀌는 기대값은 계약에서(시험이 낸 수를 옮기지 마라).

## 허브 · 포트 · 실물

- 허브 0.8.1 은 다른 워커가 같은 때 18107 에서 만든다 — **너는 18105(0.7.2 DB 판)를 GET/조회로만 쓴다.** 상담 0.4 켠 상태는 목록 꼴 · concern_candidates 등만 써서 0.7.2 허브로 돈다(SPEC-001 0.8.1 영향 표). 18105 재시작 금지.
- 네 서버 = **18224**(CHAT_STATE=on · CHAT_DEBUG_PANEL=on · 끝나면 내림 · `lsof` 0). 18222 · 18223 · 18105 · 18107 · 18432 프로세스 건드리지 마라.
- 소넷 CLI 는 앱과 같은 격리 인자 · thinking 끔(WP-0 실측 — `llm/cli.py:11-12` 꼴 먼저).
- **E8 표 실행(WP-12)**: 356 턴 전부 · `ref.to=answer` 5 대화는 답 LLM 실제 호출 · D-14 8 검사 90%↑ · 3 검사 95%↑ · 정보 종류 90% · E8-6b ⓐ 90% ⓑⓒ 100% — 수 · 꼴별 실패 표 · 지연 중앙/p90 를 보고. 문턱 미달이면 **멈추지 말고** 실패 턴 원인 층(이해 호출 · 검증 · 객체 · 조회 · 데이터)을 갈라 보고하고, 프롬프트 · 규칙을 고칠 수 있으면 계약 안에서 한 번 고쳐 다시 잰다(고친 것 · 전/후 수).
- `curl` 은 `--data-urlencode`.

## 보고

WP-0 · WP-5 · WP-9 · WP-12 끝에 `[진행] app: …` 한 줄.
