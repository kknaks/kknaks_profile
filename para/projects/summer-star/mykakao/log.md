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
| 2026-09-02 | spike | — | Windows 키유도 탐색 3회(poc-windows-key-derivation/-re/-recover): (1)macOS 모델 이식불가 C+D → (2)passive read 로 대화 로컬 존재 확증(D 정정) → (3)메모리 SQLCipher raw key 회수 + chatLogs 실복호(1455행). 파생식 미회수. PR 없음(spike) | orchestration/work/ |
| 2026-09-02 | baseline-add | BASE-003 | Windows V2 아이디어 등록 — 트레이 앱 + 방 선택 + 과거 복호 + 실시간 파일감시 축적(SQLite) + 대화 패턴 추출. 키=메모리 회수. status draft | baseline-003 |
| 2026-09-02 | baseline-add | BASE-004 | 오프라인 키 파생식 회수(RE) 백로그 등록 — spike3 관찰(가설 전수 불일치) + 남은 경로(Ghidra 언패킹 / WinDbg). status deferred | baseline-004 |
| 2026-09-02 | decision-add | DEC-003 | Windows V2 방식 4결정: 키=실행중 메모리 회수 / 저장=로컬 SQLite / 실시간=파일감시(-wal)→델타복호→append→SSE / UI=트레이+localhost HTML. status accepted | decision-003 |
| 2026-09-02 | decision-change | DEC-003 | 결정5 추가 = 구현 Rust(axum·rusqlite bundled-sqlcipher·notify·windows·tray-icon), 같은 레포 win_app/ 디렉토리. spike 코드는 참조 포팅. SAC는 언어 무관(서명 문제) | decision-003 |
| 2026-09-02 | spec-add | SPEC-003 | Windows V2 기능 계약(UX 3섹션+2pane / axum API 6개 / BE 메커니즘: 메모리 키회수·rusqlite 복호·notify 파일감시 / SQLite 스키마 / P1~3 / win_app 레이아웃). status draft | spec-003 |
| 2026-09-02 | baseline-change | BASE-003 | UX 구조 확정(트레이→설정 3섹션, 2pane) + Rust/win_app 반영 + status accepted, links→DEC/SPEC-003 | baseline-003 |
| 2026-09-03 | spike | — | spike4/4b 파생식 RE: 메커니즘 규명(SQLCipher+PBKDF2, passphrase=%s%s+DPAPI) but 정적·WinDbg(anti-debug 자폭) 모두 막힘 → (C). 파생식 셸빙, 속도는 세션 캐싱으로. BASE-004 기록 | orchestration/work/ |
| 2026-09-03 | baseline-add | BASE-005 | 로그인 상태 트래킹 + 자동 재조정(등록방 최신유지) 아이디어. 3상태 모델 + 재조정 루프. status accepted | baseline-005 |
| 2026-09-03 | decision-add | DEC-004 | 감지=계정 파일감시+프로세스wait(무거운 harvest는 이벤트 트리거만) / 속도=세션 키 캐싱 / 상태표시=트레이 메뉴+본인닉네임 / 영속=기존 room.selected. status accepted | decision-004 |
| 2026-09-03 | spec-add | SPEC-004 | 로그인 상태 트래킹 기능계약(3상태 감지/재조정 루프/세션캐싱/트레이 상태메뉴/api state 확장). status draft → WORK-006 | spec-004 |
| 2026-09-03 | work-add | WORK-006 | 로그인 상태 트래킹 코드 완료·커밋(ff79ba2): state.rs 3상태·이벤트 재조정·세션캐시·트레이 상태메뉴·/api/state. cargo test 18. | work-006 |
| 2026-09-03 | baseline-add | BASE-006 | 설정 UI 리디자인(카톡 transfer 2탭) + 백그라운드 수집 큐 + 트레이 정비. 목업 승인(artifact 7340ba99). status accepted | baseline-006 |
| 2026-09-03 | decision-add | DEC-005 | transfer UI / DB 백그라운드 수집 큐(상태 폴링, 대기중→트래커 자동수집) / 트레이 오너드로우(까만글씨·초록빨강 점·비선택) / 본인닉네임 조사. status accepted | decision-005 |
| 2026-09-03 | spec-add | SPEC-005 | 설정 UI 리디자인 기능계약(transfer 2탭/수집 큐/api rooms 상태/트레이 오너드로우). status draft → WORK-007 | spec-005 |
| 2026-09-04 | spike | — | 사진 획득 조사 2회: attachment=talkmedia/url_image_v2 매핑 규명 / .cng 복호는 키 힙에 없어 실패(C, Ghidra RE 필요→백로그). 반전: URL 생존=사진 나이(최근 200/오래됨 410), 실시간은 URL 다운로드로 성립 | orchestration/work/ |
| 2026-09-04 | baseline-add | BASE-007 | 사진 수집(실시간 URL 다운로드+로컬 저장+미디어 서빙). 커버 경계: 수집 전 만료=유실 표시(복구 안 함). status accepted | baseline-007 |
| 2026-09-04 | baseline-add | BASE-008 | 오래된 사진 .cng 복호 백로그(키 힙에 없음, Ghidra RE 필요). status deferred | baseline-008 |
| 2026-09-04 | decision-add | DEC-006 | 사진=talkmedia URL 다운로드(.cng 아님)+로컬 저장(바이트 보유)+/api/media 서빙+탭2 img. 유실은 정직 표시. status accepted | decision-006 |
| 2026-09-04 | spec-add | SPEC-006 | 사진 수집 기능계약(파이프에 사진 처리+media 스토어+/api/media+img/유실 렌더). status draft → WORK-008 | spec-006 |
