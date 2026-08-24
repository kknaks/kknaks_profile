# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Type | IDs | Summary | Links |
|---|---|---|---|---|
| 2026-06-12 | scaffold | — | 제품 문서 스캐폴딩 생성 (README, log, 00~30 index) | — |
| 2026-06-12 | baseline-add | BASE-001 | 카톡 대화 로컬 자동 추출(내보내기 없이) 아이디어 등록 | baseline-001 |
| 2026-06-12 | decision-add | DEC-001 | 추출 방식 = 로컬 SQLCipher DB 복호화(kakaocli) 채택 | decision-001 |
| 2026-06-12 | spec-add | SPEC-001 | 메시지 추출 기능 계약 + 키유도/user_id 복구 방법 상세. 추출 메커니즘 라이브 검증(631k msg/741 방) | spec-001 |
| 2026-06-12 | decision-change | DEC-001 | 복호화 내부화 명시(자체 키유도 + 표준 sqlcipher), kakaocli reference-only | decision-001 |
| 2026-06-12 | spec-change | SPEC-001 | 내부 복호화 레시피(compat3+passphrase) + 읽기모드(immutable vs mode=ro) 박음 | spec-001 |
| 2026-06-12 | work-add | WORK-001 | 추출 확인용 웹 데모(FastAPI+SQLAlchemy+sqlcipher3+바닐라JS) done. 4 REST + SSE 실시간 라이브 검증 | work-001 |
| 2026-06-15 | baseline-add | BASE-002 | 추출 대화 AI 요약(방·날짜 선택 + 사용자 프롬프트) 아이디어 등록 | baseline-002 |
| 2026-06-15 | decision-add | DEC-002 | AI 요약 방식 = open_kknaks(codex) + 단일 방·단일 날짜 + SSE 스트리밍 + 2뷰 데모 확정(5건). 구현 상세 OQ 4건은 spec 단계 | decision-002 |
| 2026-06-15 | spec-add | SPEC-002 | 추출 대화 AI 요약 기능 계약(2뷰 html/SSE 릴레이/codex gpt-5.5/조립 템플릿/cap+고지). status draft | spec-002 |
| 2026-06-15 | decision-change | DEC-002 | OQ-1~4 closed(SPEC-002 반영) + links.specs→SPEC-002 승격 | decision-002 |
| 2026-06-15 | mapping-change | DEC-002 / SPEC-002 | DEC-002 ↔ SPEC-002 양방향 연결 | spec-002 |
| 2026-06-15 | work-add | WORK-002 | AI 요약 작업 지시서(W-1 BE 2엔드포인트 / W-2 FE 2뷰 / W-3 redis+codex 기동) + acceptance/test. status todo | work-002 |
| 2026-06-15 | work-change | WORK-002 | 인프라 개정 = docker(redis 7-alpine + codex worker, open-kknaks examples 미러) + backend 호스트 스크립트(`redis://localhost:6379`) + 결과 저장(DB) 스킵. DEC/SPEC 본문 불변 | work-002 |
| 2026-06-15 | work-change | WORK-002 | docker codex 실측 메커니즘 3개 정정(T-006 E2E `c5d4b97`): node 런처 멀티스테이지 / cwd 상속 chdir / config.toml trust. `skip_git_repo_check`=submit-side·미사용 명시. 40-architecture 승격 후보 표기 | work-002 |
