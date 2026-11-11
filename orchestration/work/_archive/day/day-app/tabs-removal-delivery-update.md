<!-- day-app:ui-verification-v6 -->
시술현황 상단 인박스 탭 제거를 구현하고 독립 검수를 완료해 기존 [PR #237](https://github.com/MediSolveAIDev/CENTURION_DAY/pull/237)에 반영했습니다. 코드 head `b6c034bfa239bd4f12f1a29c6e58c74d82c87de6`, 실행 SPEC [PR #921](https://github.com/MediSolveAIDev/mediness/pull/921) `06239a1c7d45e95a02e5aab61b9d29bea6b7aca3`입니다.

- 상단 「현황 / 호출 n / 시술 완료 n」 탭·선택 상태·별도 호출/완료 목록·검색을 제거했습니다. 본문은 연결 상태 줄·기존 4필터·서버 cards[] 카드 목록뿐입니다. 하단 4메뉴·카드/상세 직무별 수락·푸시 진입·룸 상세 개정④·모델 calls/doneTab 수신·KOS 실패 토스트·귀가 처리는 유지합니다. 완료 카드를 새로 합치거나 숨은 대체 메뉴를 만들지 않았습니다.
- 전체 Flutter 198 passed / 27 skipped(캡처 전용) / 0 failed. 지운 호출 탭 경로 2건만 제외했고 카드·상세 직무별 수락/정확 body와 세션/환경/푸시 회귀는 유지했습니다. 독립 관문 70 passed, 코드·시각 리뷰 PASS(FAIL0/WARN0), 코디 analyze0·diff-check/경로/비밀패턴검사0입니다.
- unsigned iOS build 17.4MB, 시뮬레이터 빌드 성공. fixture 캡처 27건/PNG82와 실제 시뮬레이터에서 탭 없이 필터→카드인 것을 확인했습니다. 기존 사용자 세션·데이터를 보존해 덮어 설치했고 현황 목록이 복원됐습니다(PID45830). 로그인 입력·업무 쓰기는 미실행입니다.
- 이번 후속은 app/3파일뿐이며 backend/env/native/서명은 바꾸지 않았습니다. SPEC·코드 PR 모두 OPEN, merge/배포/TestFlight는 하지 않았습니다.

latest main baseline은 `9692e1fb461bf8c4e52bf489e37ab8ff875f9918`(이전 baseline 이후 products/day 변경 없음)이며 SPEC003 부재·SPEC001 draft로 pending을 유지합니다. 새 exact head 공식 review plan도 ready stable baseline이 없다는 이유로 거절됐습니다. 위 독립 리뷰 근거를 harness fresh evidence로 주장하지 않으며 사용자가 정한 마지막 머지 순서에서 재결속합니다.
