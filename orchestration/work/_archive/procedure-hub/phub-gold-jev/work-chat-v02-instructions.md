# WORK-012(앱) 작성 지시서 — SPEC-005 0.1.0 상담 객체(상담 채팅 0.2) 구현 계획

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더)의 역할 · 제약 · 검증 · 완료 보고 꼴 그대로(핸들은 preamble 값). allowed_paths = **`WORK-012-consult-state.md` 새 파일 하나만**. Procedure Hub 데이터 · medikit 은 공개(비밀값 · 키 · 내부 URL 금지 그대로).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · **지금 0.1 수정 1 이 진행 중이라 흔들림** — 0.1 구현 + 수정 1 지시서를 기준으로 읽어라)

## 읽을 것

1. `$W/_RESUME.md` §2 11-17 행 전부 — 특히 맨 위 「0.2 까지 진행 — U5-1~U5-5 = 추천(U5-4 (a1) 표지만)」 · 「SPEC-005 검수 뒤 코디 W-1~W-9」 · 「얼굴 SVG = 사용자가 직접」
2. `$W/SPEC-005-consult-state.md` 전체 ← 계약 · `$W/review-spec-005.md`(WARN 9 · NOTE 10)
3. 0.1: `$W/SPEC-004-consult-chat.md` · `$W/WORK-011-consult-chat.md` · `$W/impl-chat-app-report.md` · `$W/review-code-chat-app.md` · `$W/app-chat-fix1-instructions.md`(지금 고치는 것 — UI · 단계 · `/c/<id>`)
4. 앱 코드 `$A/clinic_chat/consult/` · `$A/prompts/consult.json`

## 쓸 것

- SPEC-005 절 ↔ WP 대응(미대응 0) · 시험 S5-T1~T16 · 실물 E5-1~E5-5.
- U5-1~U5-5 = 추천 반영(U5-4 (a1): 보완 줄에 「같은 날 제약 있음」 표지만 · 회피/불가 행 내용은 물을 때 — 표지를 세우는 데 필요한 조회 하나를 어디에 둘지 · 안전 본문 먼저 싣기 0).
- 코디 W-1~W-9 한 줄씩(_RESUME 행 그대로) · NOTE 10 처리.
- `CHAT_STATE` 끈 상태 = 0.1 그대로(T1~T18 · 수정 1 시험 통과) · 켠 상태에서 달라지는 것 목록.
- 첫 WP = 수정 1 이 끝난 코드 위에서 시작(그 전에는 시작하지 않음 — 코디가 발주 때 알림).
- 얼굴 SVG · `face_coords.py` 는 **사용자가 직접 바꾼다** — 이 WORK 는 그 파일을 고치지 않는다(좌표표 꼴 · 키만 쓴다).
- 허브 부위 칸(SPEC-001 0.7)이 없으면 점 0 으로 도는 것 그대로.
- 실물: 워커 18223 · 코디 18222 · 18105 읽기만.

## 검증

대응표 · WARN/NOTE 반영 줄 · 경로 실재 · 공개 grep.
