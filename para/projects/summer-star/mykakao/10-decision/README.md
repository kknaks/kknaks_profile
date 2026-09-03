# Decision Index

규칙: `para/projects/project.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| DEC-001 | 메시지 추출 방식 — 로컬 SQLCipher DB 복호화 (kakaocli) | accepted | BASE-001 | B 채택 (로컬 복호화) | SPEC-001 |
| DEC-002 | AI 요약 방식 — open_kknaks(codex) + 단일 방·단일 날짜 + SSE + 2뷰 | accepted | BASE-002 | 확정 5개 채택 | SPEC-002 |
| DEC-003 | Windows V2 방식 — 메모리 키 회수 + SQLite 축적 + 파일감시 실시간 + Rust/트레이/HTML | accepted | BASE-003 | 4결정 채택(Rust·axum·win_app) | SPEC-003 |
| DEC-004 | 로그인 상태 감지·재조정 — 파일감시/프로세스wait + 세션캐싱 + 트레이메뉴 | accepted | BASE-005 | 5결정 채택 | SPEC-004 |
| DEC-005 | 설정 리디자인 — transfer UI + 백그라운드 수집 큐 + 트레이 오너드로우 | accepted | BASE-006 | 4결정 채택 | SPEC-005 |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 카톡 버전 업데이트 시 키 유도 깨짐 대응 | kknaks | 추출 안정화 후 |
| OQ-2 | 신규 메시지 증분 수집(sync) 여부 | kknaks | 출력 플로우 결정 시 |

> DEC-002 OQ-1~4는 PLAN-002-T-002에서 **모두 closed** (SPEC-002 반영). 상세는 [[decision-002-ai-summary-approach]] §Open Questions.
