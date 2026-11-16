
# [docs] 초소수정 — SPEC-001 AC-3 문언 사실화

너는 **ontology-demo `docs` 워커**다. 한 가지만 (WORK-002 fix 잔여, 코디 확정 — (b)안):

SPEC-001 의 AC-3(마스킹 뷰) 문언을 실구현 계약으로 개정 — 마스킹 뷰는 PII 컬럼명
(patientName·phone·birthday·authorName)을 유지하되 **값이 마스킹본**이므로 어떤 조회·필터로도
원값이 나올 수 없다(노출 0건 보증의 주체는 뷰의 SELECT 목록 + AC-8 게이트). 「필터에서
차단된다」류의 문언이 있으면 「필터는 마스킹값 기준으로 동작한다」로 교체.
version patch·updated_at·README Spec List·log 1줄. 그 밖 수정 금지. 커밋·push 금지.
완료 보고 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "docs 완료: AC-3".
