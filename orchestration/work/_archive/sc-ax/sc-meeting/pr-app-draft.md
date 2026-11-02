# feat(meetings): 회의·미팅노트 1차 — 실시간 전사 중계 · 메모/AI 두 트랙 · 종료 합성 · 승격 · 자료·공유 · THE CONNECT 회의실 예약 (SCAX-SPEC-004 0.4.11)

## 무엇

회의를 「나(서기)와 AI 둘이 참석하는 자리」로 다시 세웠다. 브라우저가 STT 를 직접 부르던 경로를 걷어내고, 서버가 Soniox 세션을 소유하는 WS 중계 + **종료 시 원본 음원 2-pass 재전사(화자 분리, 폴백 없음)** 위에 **메모 트랙·AI 중간 요약 트랙·종료 합성·후속업무 승격(시스템이 보내는 업무 요청)·자료·공유·THE CONNECT 회의실 예약(자동 대체)·주제 스레드형 내보내기**를 올렸다. 문서 정본은 mediness `products/sc-ax/20-spec/spec-004-meeting-note.md` **0.4.11** 와 WP-001~007(PR MediSolveAIDev/mediness#719).

## 기능별 커밋

| 영역 | 커밋 | 내용 |
|---|---|---|
| 도메인·화면 골격 | 5751efa | 회의·안건·줄, 상태 6, 회의 API, 목록·상세 화면 |
| 실시간 전사 | 806f52c · 96d5312 | WS 중계(쿠키 인증, 4401/4404/4409/1000), 확정 블록(화자 변경·300자·2초), 원본 append, 종료 드레인, Soniox keepalive, 브라우저 직결 폐기 |
| 메모·AI 배치 | 80dd097 · 8397d8f | 메모 API, 웜스타트 세션 resume, MCP 도구 allowlist, strict `--output-schema`, 전량 교체·push, 업스트림 소유자 게이트 |
| 종료 합성·승격 | 8397d8f · 1925a76 · d939dae | durable job 합성(같은 세션·콜드 폴백·실패 전이), 제목 후보·다음 할 일·근거, 기준일 환산, **승격 = 시스템(회의)이 보내는 업무 요청**(promoted_by·cc, 조직 경계 없음), 안건 덮어쓰기 409 |
| 자료·공유·검색 | 59e1102 · cbb4799 | 다중 첨부(20MB·PDF/MD·부분 성공), 드로어 미리보기, 공유 목록(basis), 전사 검색 다리, `can_detach`(예정에서만) |
| 회의실 예약 | d0d5e32 · e297e1e | THE CONNECT 실제 목록·예약·동기화, **자동 대체(정원≥인원 최소 방)**, 대체 불가 시 409+가능 목록(회의 미생성), 시간대별 가능 조회 |
| 내보내기 | b0cf1b9 | HTML 주제 스레드형 A4 조판(템플릿 조각 렌더러·서버 장 나눔·쪽 번호) |
| 화면(디자인 라운드) | 9644e7c ~ ab8a8ef | 뷰포트 고정·투명 스크롤·3단 패널, 공용 부품(DateField inline·TimeRangeField·Select), 전역 포커스 링 제거, 상태 어휘 「종료」·「취소」, 줄 우측 발화 시각, 공유·떼기 시점, 안건 출처 다섯, 「회의명」 |
| 2차(실물 테스트 3회) | ada1aa9 · b440c6b · e252dee · c52f94a · cee9bca · 6004fb6 | **종료 합성 = 재료(메모·AI·전사)로 처음부터 새로 쓰기**(사람 안건 보존 검사 삭제, D42) · 실패 사유 사람 말(D43) · **종료 시 2-pass 재전사**(Soniox stt-async-v5, 화자 분리, 원문 전량 교체 후 합성, D44) · **재전사 폴백 없음 — 실패는 회의 「실패」+[다시 시도]**, 결과 GET 스트리밍·재시도, lease 1800 · 회의 중 안건 추가 + `agenda.added`(D45) · **회의 중 AI 요약에 「다음 할 일」 후보**(provisional, 읽기 전용, D46) · 배치 근거 검증 구간 = 회의 전체(D47) · 빠른 시작 자리표시 안건 제목을 AI 가 채움(D48) · 블록 경계 20초·150자·문장 끝(D51) |
| 2차 화면 | 57a4925 · b6fc76d · e7e0cfa · d9303b2 · cf60d06 · b941846 · 469c91f · 15d0cf5 | **참여자 = 같은 WS 읽기 전용 구독**(확정·잠정·AI·memo.line·안건 실시간, D41) · 스크립트 `시간|화자|내용` 한 줄 · 회의 중 「+ 새 안건」 · 상태 전이마다 원문 재조회 · 회의 중 AI 탭 다음 할 일 · **근거 칩 전부 + TimeChip**(겹치는 줄로 점프, D49) · **시각 표기 회의 경과 mm:ss**(D50) · DateField = 우리 DatePicker 하나(OS 달력 삭제, 전 화면) · Popover body 포털(카드·드로어 안 잘림 해소) · 승격 드로어 「업무 요청」(토글 없음) |
| main 머지 | 4212691 · ec9946b | #3 채팅 인터랙션 · #8 프로젝트 참여 이력 머지(충돌 24파일). 옛 회의 모델(MeetingNote·meeting_create/share 도구·MeetingDrawer·native 자료 다리) SPEC-004 로 정리, 채팅 회의 열기 → 회의 상세. **채팅 [확인] 의 meeting.create/share 는 새 모델 이관 전까지 안내 오류**(별도 작업) |
| 정책 반영 | 20723a7 · 여러 fix | quick-start 웜스타트·기본 안건, 정리 중 폴링, vite WS 프록시, 조직도 인원수·안건 번호·내보내기 링크 버그 |

## 결정(10-decision D1~D51 중 코드에 닿는 것)
- D1 두 트랙 유지 · D34 화면 상태 다섯(서버 여섯) · D35 승격 후보 「요청됨」 유지 · D36 회의실 자동 대체·대체 불가 시 생성 거절 · D37 드로어 미리보기 유지(4종·조작은 데모 밖) · D38 안건 출처 다섯 · D39 스레드형 조판 · D40 승격 요청자 = 시스템 · **D41 참여자 WS 구독 · D42 합성 재작성 · D43 실패 사유 사람 말 · D44 종료 2-pass 재전사(폴백 없음, D3 철회) · D45 회의 중 안건 추가 · D46 회의 중 다음 할 일 후보 · D47 근거 검증 구간 회의 전체 · D48 자리표시 안건 제목 · D49 근거 칩 전부 · D50 경과 mm:ss(D31·D34 철회) · D51 블록 20초·150자·문장 끝**.
- SCAX-SPEC-001 소유 변경: 팀장 `work_request.create`(D30), 요청자 시스템 행위자 `system:meeting`(D40) — §12 R-37·R-48 통보.

## 검증
- 계약 테스트(회의 6파일 + work·권한·검색 회귀 + architecture) 코디 재현 전부 통과. 코드 검수 6회(reviewer) — FAIL 전부 해소, 마지막 셋 PASS.
- **2차(09-11~12) 검증은 사용자 지시로 실물 e2e 우선** — 실제 회의 녹음(Charty 09-07, 1x)으로 3회 + 실제 사용자 회의 1회: 재전사 final 성공·칩 전부·회의 중 안건·참여자 실시간 확인. 2차 커밋들의 pytest/vitest 스위트는 워커 부분 실행 또는 미실행(tsc 0) — **머지 전 전체 스위트 1회 필요**.
- 실물: Soniox(합성 음성·브라우저 가짜 마이크 webm/opus), Codex 웜스타트·중간 배치·종료 합성, THE CONNECT 예약·자동 대체·거절·취소 동기, 승격→시스템 요청, 자료 부분 실패·검색, 내보내기 A4 렌더, 화면 playwright.

## 실행 주의
- env: `~/.config/soniox/env`(SONIOX_API_KEY) · `~/.config/theconnect/env`(TDL_EMAIL/TDL_PASSWORD) — Makefile 이 api·local-stack 에 source. Codex 는 CLI 로그인.
- 스키마: `make reset-demo` 또는 `make sync-demo-schema`(additive: meetings.room_reservation·transcript_source · work_requests.promoted_by_member_id · meeting_todos.provisional · meeting_agendas.title_placeholder + main 의 notifications 등). sync 는 NOT NULL/DEFAULT 를 붙이지 않으므로 provisional·title_placeholder 는 뒤에 `UPDATE … SET false WHERE NULL; ALTER … SET DEFAULT false, SET NOT NULL` 한 줄.
- `make local-stack` 의 API 는 --reload 없음.
- 잠정값(OQ): 배치 트리거 600자/80자/90초 · keepalive 10초 · 드레인 8초 · 합성 시도 3 · 정리 중 폴링 5초 · 재전사 폴링 5초/상한 1200초(lease 1800).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01EDgZPT3rYB6MDEKAL8Kxs6

