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
