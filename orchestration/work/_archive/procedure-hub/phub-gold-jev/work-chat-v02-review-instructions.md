# WORK-012 검수 지시서 (짧게)

**너는 앞 판의 맥락이 없다.** `work-review-instructions.md`(같은 폴더)의 역할 · 볼 것 · 제약 · 완료 보고 꼴 그대로(핸들은 preamble 값). Procedure Hub 데이터 · medikit 은 공개(비밀값 · 키 · 홈 경로 금지 그대로). 외부 API · CLI 호출 금지.

앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · 0.1 + 수정 1 미커밋 · `_face.svg` · `face_coords.py` 는 다른 세션 소유 — 이 WORK 가 고치지 않는지 본다).

읽을 것: `WORK-012-consult-state.md` · 계약 `SPEC-005-consult-state.md` · `review-spec-005.md` · `_RESUME.md` §2 11-17 행(맨 위 **WORK-012 B 코디 답 + 추가(대상이 부위 · 시술 · 제품이어도 리스트)** · U5 추천 · SPEC-005 검수 뒤 코디 W-1~W-9 · 사용자 테스트는 0.2 뒤) · `impl-chat-app-report.md` · 수정 1 보고(인박스 요약은 _RESUME §5) · 앱 코드.

볼 것: ① SPEC-005 ↔ WP 대응(미대응 0) · 지어낸 동작 0 ② U5 · W-1~W-9 · B 답 반영 — 특히 **추가 항목(부위 · 시술 · 제품 대상 리스트 · 같은 이름 고민/부위)이 WORK 에 없으면 어느 WP 에 넣을지 구체 제안**(코디 실물: 「팔자주름이 고민이에요」 → 대상 SITE · list 0 — 앱 `runs/consult/turns.jsonl` 마지막 줄) ③ 실행 가능성(수정 1 코드 위 · 함께 쓰는 코드 줄 수 · 기존 시험 무변경 · CHAT_STATE 기본 off) ④ 실물 E5 가 실물(구독 CLI · 18105 · 18223)을 요구 ⑤ 공개 grep.

산출: `review-work-012.md` 1개 · 판정 PASS/WARN/FAIL. FAIL 이 없으면 「구현 진행 가능」 명시.
