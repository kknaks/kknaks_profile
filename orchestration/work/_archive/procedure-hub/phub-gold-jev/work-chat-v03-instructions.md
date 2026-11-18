# WORK-014(앱) 작성 지시서 — SPEC-006 0.1.0 상담 채팅 0.3 구현 계획(A1~A8)

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더)의 역할 · 제약 · 검증 · 완료 보고 꼴 그대로(핸들은 preamble 값). allowed_paths = **`WORK-014-consult-v03.md` 새 파일 하나만**. 다른 writer 가 같은 폴더에 `WORK-013-hub-v07.md` 를 동시에 쓴다 — 손대지 마라. Procedure Hub 데이터 · medikit 공개.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · HEAD 68a31b1)

읽을 것: `$W/SPEC-006-consult-v03.md` · `$W/review-spec-006.md`(WARN 12 · NOTE 9) · `$W/_RESUME.md` §2 11-17 맨 위 행들(**SPEC-006 검수 뒤 코디 값 W-1~W-8 · W-11 · W-12** · **W-9 = (a) · W-10 = 「○○ 계열 시술」** · U6-1~3 (a) · **U6-4 보류(열린 것으로)** · A8 화면 · **시험은 구현한 것만 · 전체 안 돌림**) · `$W/SPEC-001-hub-gold-mcp.md` 0.7.1(앱이 읽는 칸: descended[] · sites[] · matched.how · **site_mode · site_applied · site_prefer · n_site_prefer** — SP 규칙: 부위 없는 고민 + 부위 = 거르지 않고 표지 행을 앞에 · 표지 0 일 때 화면(review-spec-001-v071 N-4)) · `$W/review-spec-001-v071.md` N-4 · 앞 WORK 꼴 `$W/WORK-012-consult-state.md` · 앱 코드.

쓸 것: SPEC-006 절 ↔ WP(미대응 0) · 코디 값 반영 줄 · SPEC-001 0.7.1 칸 이름 일치 · 시험 S6-T1~T29 + SP 꼴(부위 없는 고민 + 부위 · 표지 0 일 때) · 실물 E6-0~E6-6(워커 18223 · 코디 18222 · 18105 는 허브 0.7.1 구현 뒤 코디가 재시작 — 그 전 실물은 0.7.1 칸 없이 도는 꼴) · 얼굴 SVG · face_coords 안 고침 · 함께 쓰는 코드 선택 인자(C6-1 · W-4 상담 쪽만) · **WP 마다 「그 WP 시험 파일만 돌림 · 전체 pytest 금지 · 돌린 파일 목록 보고」**(사용자 11-17) · 완료 조건.

검증: 대응표 · 경로 실재 · 공개 grep.
