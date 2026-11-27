# [backend · e2e 1] 로컬 스택 + KOS 데모 지점 실물 — 링키 요청 → 생성 → 수정 → 취소

같은 터미널 · 같은 맥락. 코디가 스택을 띄웠다: `http://127.0.0.1:11140`(`--kos-demo --scheduler` · migration 0031 · seed-demo 완료 · 병원 `82dafd66…`). **스택 시작 · 멈춤 · 재시작 금지 · 코드 고치지 마라**(파일을 바꾸면 API 가 리로드에서 멈춘다 — 버그는 원인 file:line 만). 다른 작업 스택 · 포트 금지.
- ext 키(로컬 시험용) = 파일 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-reservation3/98891b4e-7a3d-4d78-bb3e-726656353895/scratchpad/ext-local-key`(헤더 `X-Api-Key` · 값 출력 금지)
- 웹 로그인 = `~/.config/day/kos-test-account.env`(값 출력 금지 · KOS 동시 로그인 5기기 한도 — 세션 하나만 쓰고 끝나면 로그아웃)
- KOS 반영 확인 = DAY 로그 · DB 사본(SELECT) · 필요하면 KOS 다시 읽기(`get-schedule-detail`)
- 시험 고객 = 이름에 「(시험)」 · 가짜 번호 · `example.com` · 실제 고객 건드리지 마라 · 예약은 **앞날**(모레 이후 빈 칸)

## 시험

1. ext E7 · E8 · 직원 목록으로 예약 그룹 · 유입 · 원장 · 상담사 id 를 고른다
2. **초진(이메일만 있는 새 고객)** E1 → 웹 목록 SSE `reservation_request` · 알림 행(ADMIN · COORDINATOR) · 창 1 · 2 · 3열 조각 → [예약 생성] → W1(이메일만 — **review W3: KOS 같은 고객 찾기가 이름만으로 어떻게 답하나**) → W2(email) · W3(counselor · 메모 합친 글 · 유입) 확인 · `reservation_applied` · E5 로 링키가 보는 값 · E4 `updated_since`
3. **재진**(1 에서 만든 고객 또는 데모 재진 시험 고객) E1 → 판정 = 재진(구분 값 하나 같음) → 생성
4. 같은 스레드에 링키 E2 `change`(시간 · 메모 · 희망 시술 · 상담사 **비움(null)** — review W4: KOS 「당일 지정 상담사」가 지워지나 · 남나 기록) → 웹 [예약 수정] → W4(+메모 · 유입) 확인
5. 웹 변경 요청(칩 2개) → 링키 E5 로 보임 → 링키 E2 새 버전 → 「대체됨」 · 버튼 돌아옴 · [철회] 한 번
6. 다른 고객 `change` → 400 `customer_changed` · 구분 값 하나도 없는 E1 → 400
7. 링키 E2 `cancel` → 웹 [예약 취소] → W5 · 스레드 취소됨 · `reservation_applied`
8. **review N5**: 새 스레드 하나 생성 뒤 예약 현황에서 먼저 그 예약 취소 → 링키 `cancel` → 스레드 취소됨 + `reservation_applied` 자동 확인
9. 실패 한 건(가능하면 — 잘못된 그룹 id 를 DB 로 만들지 말고, 안 되면 건너뜀) → 「KOS 등록 실패」 · [다시 시도]
10. 정리 — 만든 예약 전부 취소 확인 · 로그아웃

## 리포트
`e2e-1-report.md`(이 폴더) — 맨 위 표(시험 × O/X · SSE 초 · 비고) · W3 · W4 실물 결과 · 버그 목록(원인 file:line · fe/be). 완료 보고 두 명령(subject 「backend 완료: e2e 1」).
