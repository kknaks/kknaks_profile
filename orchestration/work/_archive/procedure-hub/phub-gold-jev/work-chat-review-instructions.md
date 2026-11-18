# WORK-011 검수 지시서 (짧게)

**너는 앞 판의 맥락이 없다.** `work-review-instructions.md`(같은 폴더)의 역할 · 볼 것 · 제약 · 완료 보고 꼴 그대로(핸들은 preamble 값). 11-17 사용자 결정: Procedure Hub 데이터 · medikit 은 공개 — 「회사 데이터 본문 0」 은 이 둘에 걸지 않는다(비밀값 · 키 · 내부 URL · 홈 경로는 그대로). 외부 API · CLI 호출 금지(`claude --help` 됨).

앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · HEAD 6303e18) · 디자인 킷 본 `/Users/kknaks/git/CENTURION_DAY`(읽기만).

읽을 것: `WORK-011-consult-chat.md` · 계약 `SPEC-004-consult-chat.md` · `review-spec-004.md`(WARN 8 · NOTE 7) · `_RESUME.md` §2 11-17 행(**WORK-011 B 코디 답** · U-11~13 (a) · 프롬프트 JSON · 디자인 킷 · medikit 공개 · SPEC-004 검수 뒤 코디 W-1~W-8).

볼 것: ① SPEC-004 ↔ WP 대응(미대응 0) · 지어낸 동작 0 · SPEC 과 다르게 받은 곳(프롬프트 JSON · 디자인 킷 · B 답)이 결정 행과 맞나 ② W-1~W-8 · NOTE 7 반영 ③ 실행 가능성(앱 코드 이어서 · 경로 · 함께 쓰는 코드 손대는 곳이 carry · instr 둘뿐 · 기존 시험 무변경 · 포트 18223 워커 / 18222 코디 · 18105 읽기만) ④ WP-0 E1 이 실물 CLI 3턴(기억 · 첫 글자 · cache · `--max-turns` · 다른 cwd resume · F7)을 요구하고 안 되면 멈춤 ⑤ 화면 WP 가 DAY 규칙(HX-Request 조각 · JS 한 파일 · 인라인 스크립트 0 · htmx 벤더링 + 라이선스 · medikit 토큰만)과 맞나 · 화면 문구 지어 넣은 것 0 ⑥ 얼굴 SVG · 좌표표(부위 60 분류 · 짝 두 점 · 얼굴 밖 라벨 · 허브 부위 칸 없을 때 점 없이) ⑦ 공개 grep.

산출: `review-work-011.md` 1개 · 판정 PASS/WARN/FAIL. FAIL 이 없으면 「구현 진행 가능」 명시.
