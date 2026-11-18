# SPEC-006 0.1.0 검수 지시서(상담 채팅 0.3 · A1~A8)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-doc-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값). Procedure Hub 데이터 · medikit 은 공개(비밀값 · 키 · 내부 URL · 홈 경로는 그대로 본다). 외부 API · CLI 호출 금지. 같은 폴더에서 다른 워커가 다른 파일을 검수 중 — 네 리포트 외에는 손대지 마라.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · HEAD 68a31b1) · 장부 `$A/runs/consult/turns.jsonl`

읽을 것: `$W/spec-chat-v03-instructions.md`(지시 · 「정해진 것」) · `$W/_RESUME.md` §1 수정 2 목록 · §2 11-17 맨 위 행들(A8 화면 구조 · U7 (a) · 얼굴 점 · 메뉴는 시술 아님 · 내려가기) · `$W/SPEC-006-consult-v03.md` · 대조 `$W/SPEC-004-consult-chat.md` · `$W/SPEC-005-consult-state.md` · `$W/SPEC-001-hub-gold-mcp.md` 0.7.0(descended · sites · matched.how) · `$W/review-code-chat-v02.md`.

할 것:
1. 지시 A1~A7 + 코디 보충 A8 이 문서:줄로 닫혔나 · 「정해진 것」 위반 0 — 특히 **되물음 · 불만 턴은 검색 없이** · 화면 답에서 출처 · 층 · 「읽었어요」 빠짐(기록에는 남음) · 메뉴가 시술로 새는 길 0 · 하위 일반화 금지 · 안전은 물을 때만 · 지어냄 0.
2. 실물 대화 셋 12턴 기대표가 장부 실물(conv · 턴)과 맞나 · (가정) 표시.
3. 계약 구멍: 턴 종류 실패 · talk 턴의 객체 · 점 누르기(viewing) · 드로어 대화 목록(장부 읽기 · 대화 많을 때) · 객체 패널 env · SPEC-004/005 위에 얹는 표가 0.1/0.2 를 깨지 않나 · SPEC-001 0.7.0 칸 이름 일치.
4. 함께 쓰는 코드 선택 인자 셋(C6-1 entry_pick 추가) 등 코디 기본값 C6-1~13 이 결정을 넘지 않나.
5. U6-1 ~ U6-4 추천이 원칙과 맞나 · 숨은 사용자 결정 0.
6. **최종**: PASS 면 「U6-1 ~ U6-4 정해지면 WORK 진행 가능」 명시.

산출: `$W/review-spec-006.md` 1개만.
