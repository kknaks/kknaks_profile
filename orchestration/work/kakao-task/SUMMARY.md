# WORK-003 win_app — 완료 요약 (2026-09-04)

Windows 카톡 대화 로컬 수집 앱(Rust). mykakao 레포 `win_app/` 디렉토리, 브랜치 `feat/win-app`.

## 무엇을 만들었나 (기능)
- **방 선택·추적**: 카톡 방 목록(transfer UI) → 선택 저장(영속, room.selected). 검색.
- **과거 수집**: 선택 방 chatLogs(main+WAL) 복호 → 로컬 SQLite. 클릭 시 즉시 수집(POST /api/collect).
- **실시간 축적**: 파일감시(notify) + 3s 델타 폴링(WAL in-place 쓰기 보정) → SSE. 상태 히스테리시스로 진동 제거.
- **이름 해석**: chatListInfo(방 제목/종류) + TalkUserDB(닉네임). 본인 = 계정 이메일 fallback.
- **사진**: talkmedia URL 다운로드(WinHTTP, 신선하면 200) → SHA1 검증 → 로컬 저장 → /api/media 서빙 → 탭2 <img>. 만료=유실 표시.
- **트레이 앱**: windows crate 오너드로우 메뉴(까만 글씨·초록/빨강 상태점), 클릭 시 브라우저로 설정 열기.
- **UI**: 카톡 스타일 2탭(설정/채팅), vanilla HTML, axum 정적 서빙.

## 핵심 기술·판단 (막혔다 푼 것)
- **키 회수**: 파생식 회수 실패(anti-debug+DPAPI 벽, spike1~4b) → **실행 중 카톡 메모리 passive VM_READ 로 SQLCipher raw key 회수**. 세션 키캐시로 반복 harvest 회피. (BASE-004: 오프라인 파생식은 셸빙)
- **WAL 누락**: 활발한 방은 대화가 -wal 에 있어 main 만 읽으면 0행 → main+WAL 병합 복호.
- **chat_id 정밀도**: 큰 chatId JSON number 직렬화 시 JS 2^53 손실 → 문자열 직렬화.
- **실시간**: notify 가 WAL in-place 쓰기 놓침 → 3s 델타 폴링 병행. SSE 를 사진 다운로드보다 먼저 push.
- **SAC**: Smart App Control 이 MS 정책 업데이트(9/2~3) 후 rustc/cargo 하드 차단 → SAC OFF(사용자 승인, 되돌리기=클린설치).
- **사진 .cng**: 오래된 사진 URL 만료(410) → 로컬 .cng 복호 필요하나 키 힙에 없음(Ghidra RE, BASE-008 백로그). 최근 사진은 URL 다운로드로 해결.

## 산출
- 코드: mykakao 레포 `feat/win-app` (15커밋). PR 대기(계정 권한: kknaksss 소유 — 인증 필요).
- 배포본: mykakao.exe + ui/ zip (본인 기기·본인 카톡 전용, 서명없음→SAC/SmartScreen 안내).
- 문서: BASE/DEC/SPEC-003·005·006·007, BASE-004·008(백로그).

## 남은 것
- main PR (계정 권한 해결 후).
- 대화 패턴 추출(원래 목적, 미착수).
- 첫 로드 이름 지연(수십초 harvest) → 이름 캐싱 개선 여지.
- 사진 checkSum 일부 불일치 재시도.
