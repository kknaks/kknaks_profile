"""채용담당자 채팅 서비스 — SPEC-017.

    session_service   익명 세션 발급·검증 (쿠키의 반대편)
    chat_service      대화·메시지 (공개 API 4종이 딛는 곳)
    exposure_service  chat_exposed 판정 + chat-tool 조회 (MCP 의 반대편)
    prompt            시스템 프롬프트 조립 (§5 프롬프트 계약)
    submission        codex 제출 계약 (-c 오버라이드)
    turn_token        turn 전용 MCP Bearer 토큰 발급·검증·폐기
    consumer          이벤트 폴딩 — 부분 텍스트 · steps · sources
    runtime           제출과 소비자 기동의 배선 (커밋 뒤에 돈다)
"""
