
# [docs] 소수정 2건 — CORS·쿠키 계약 등재 + chart_no 마스킹 확장

너는 **ontology-demo `docs` 워커**다. 2건 (WORK-005 실측, 코디 확정):
1. SPEC-003(v0.0.10→0.0.11): 배포 토폴로지(Vercel↔홈서버 교차 오리진) 계약 등재 — CORS 는 명시 오리진 목록(env ONTOLOGY_ALLOWED_ORIGINS, credentials 라 와일드카드 불가·미설정 시 기동 거부), 세션 쿠키 SameSite 는 secure 에서 파생(https=None+Secure / http=Lax). 근거: 이게 없으면 게이트 화면부터 브라우저가 막는다(WORK-005 실측).
2. SPEC-001(v0.0.8→0.0.9): 마스킹 뷰 절에 chart_no 방어 한 줄 — 「chart_no 는 추적용으로 유지하되, 숫자 패턴이 아닌 값(원천 오염으로 이름이 앉은 1건 실측)은 뷰에서 마스킹 표기로 치환한다」. DEC-002 의 노출 0건 게이트 연장.
version·updated_at·README 동기·log 1줄. 그 밖 수정 금지. 커밋·push 금지. 보고 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "docs 완료: CORS·chart_no".
