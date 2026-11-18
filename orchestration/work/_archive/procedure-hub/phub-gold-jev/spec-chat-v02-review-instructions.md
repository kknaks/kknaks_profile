# SPEC-005 0.1.0 검수 지시서(상담 객체 · 상담 채팅 0.2)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-doc-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값). 11-17 사용자 결정: Procedure Hub 데이터 · medikit 은 공개 — 「회사 데이터 본문 0」 은 이 둘에 걸지 않는다(비밀값 · 키 · 내부 URL · 홈 경로는 그대로). 외부 API · CLI 호출 금지.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · 0.1 구현 중) · `SM=$W/../_archive/procedure-hub/phub-ledger-redesign/silver-model`

읽을 것: `$W/spec-chat-v02-instructions.md`(지시 · 「정해진 것」) · `$W/_RESUME.md` §2 11-17 행 · `$W/SPEC-005-consult-state.md` · 대조 `$W/SPEC-004-consult-chat.md` · `$W/SPEC-001-hub-gold-mcp.md` · gold CSV.

할 것:
1. 지시 「할 것」 1~8 이 문서:줄로 닫혔나 · 「정해진 것」 위반 0(단계 밀어붙이기 0 · 객체 값 = 데이터 코드만 · 지어낸 고민 0 · 시너지 먼저 · 안전은 물을 때만 · 우열 0 · 담기 · 가격 범위 밖 · SPEC-004 안 흔듦).
2. 예시 대화 셋의 코드 · 행 수 재셈(gold CSV) · 「Jev 값은 가정」 표시가 지켜졌나 · 보완 89 중 5 짝(SY6) 재셈.
3. 계약 구멍: 갱신 규칙 UP · 되돌림 RV · 빈 칸 · 질문 규칙 NQ 가 서로 부딪히지 않나 · 「자연스럽게」 가 사실상 고정 순서가 되지 않나 · 객체와 걷기(0.1 · 동결 부분)가 어긋나는 곳(O5-2) 처리 · 「볼(SITE-051) 우연 일치」 같은 오매핑을 막는 규칙.
4. SPEC-004 위에 얹는 것 표가 0.1 계약을 깨지 않나(이벤트 · 장부 · 프롬프트 JSON · CLI).
5. U5-1 ~ U5-5 추천이 결정 · 원칙과 맞나(특히 U5-4 가 「안전은 물을 때만」 의 예외를 여는 범위) · 숨은 사용자 결정 0.
6. **최종**: PASS 면 「U5-1 ~ U5-5 정해지면 WORK 진행 가능(0.1 구현 끝난 뒤)」 명시.

산출: `$W/review-spec-005.md` 1개만.
