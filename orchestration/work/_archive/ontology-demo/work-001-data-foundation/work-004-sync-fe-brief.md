
# [frontend] WORK-004 계약 동기 소태스크

너는 **ontology-demo `frontend` 워커**다. WORK-004 이어서, app/front/ 만, git 조작 금지. 4건:
1. error_code·source_group 의 "SPEC-003 개정 대기" 주석 제거 — v0.0.8 에서 공식 등재됐다(AC-18/19).
2. steps[].is_error 를 타입·렌더에 반영(도구 실패 스텝 시각 구분 — 기존 토큰 안에서).
3. retry 는 failed 메시지에만 — done 메시지에 retry UI 가 노출되지 않는지 확인(400 RETRY_NOT_ALLOWED 계약 신설).
4. 픽스처가 최신 계약(v0.0.10 예정: is_error 포함)과 일치하는지 자체 대조 후 보고에 명시.
검증: tsc + build 1회. 보고 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "frontend 완료: 계약 동기".
