# SPEC-004 0.1.0 검수 지시서(상담 채팅 1판)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-doc-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값). 11-17 사용자 결정: Procedure Hub 데이터는 공개 정보 — 「회사 데이터 본문 0」 은 이 데이터에 걸지 않는다(비밀값 · 키 · 내부 URL · 홈 경로는 그대로 본다). 외부 API · CLI 호출 금지(`claude --help` 는 됨).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만)

읽을 것: `$W/spec-chat-instructions.md`(지시 · 「정해진 것」) · `$W/_RESUME.md` §2 11-17 행 · `$W/research-chat.md` · `$W/SPEC-004-consult-chat.md` · 대조 `$W/SPEC-001-hub-gold-mcp.md`(concern_candidates) · `$W/SPEC-002-chat-eval.md` §3-2a · 앱 코드(`$A/clinic_chat/`).

할 것:
1. 지시 「할 것」 1~8 이 문서:줄로 닫혔나 · 「정해진 것」 위반 0(특히 CLI 직접 · open_kknaks 안 씀 · 옵션 표 · 리스트 결정론 · 고민 부위 점 · 얼굴 밖 라벨 · 근거 꼬리 화면에서만 숨김 · 문구 안 지음 · 플로우는 0.2).
2. 인용 표본(앱 파일:줄 20 이상) 맞나 · 부위 60 분류 재셈(point 17 · pair 27 · area 8 · line 4 · none 4).
3. 계약 구멍: CLI 세션 수명 · 실패 · 동시 한도 · 고정 cwd · 이벤트 순서(list · sites 가 첫 delta 앞) · 장부 꼴 · 이어 묻기 · 재료 덧붙이기가 캐시에 맞나 · SDK 경계.
4. F6(`--max-turns` · `--system-prompt-file` 이 로컬 2.1.322 에서 받히나 — `claude --help` 로 다시 보고, CL8 의 「E1 에서 확인 · 안 되면 코디에게」 가 충분한가) · F7 snapshot 이 프롬프트 바꿀 때 걸리는 곳.
5. 시험 T · 실물 E 가 실물(CLI 3턴 · 화면 18222)을 요구하나.
6. U-11 ~ U-13 추천이 결정 · 원칙과 맞나 · 숨은 사용자 결정 0 · 코디 기본값 C-10~C-18 이 결정을 넘지 않나.
7. **최종**: PASS 면 「U-11 ~ U-13 정해지면 WORK 진행 가능」 명시.

산출: `$W/review-spec-004.md` 1개만.
