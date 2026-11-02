# [frontend 셸] WORK-010 Phase 3 fix1 — 검수 WARN 처리

검수 `review-fe-p3-report.md`(같은 폴더) WARN 7. 코디 답(근거 「코디 2026-10-04」):
- **W1** 저장한 파일에 macOS **quarantine 속성**(`com.apple.quarantine`)을 붙인다 — 브라우저 다운로드와 같은 Gatekeeper 기준. 실패해도 저장은 성공으로 두고 로그만. Windows 는 해당 없음(보고에 Zone.Identifier 미처리로 적기)
- **W2** `/api/` 응답이 **2xx 가 아니면**(401·3xx·404·5xx) **실패 토스트**(「파일을 저장하지 못했습니다.」). 2xx + inline 만 「아무것도 안 함」
- **W3** 가로채기 origin 은 **운영(앱) origin 하나**로 좁힌다 — 인증용 허용 목록 전체가 아니라
- **W4** 하위 프레임(`<object>` PDF 미리보기) — **이번엔 코드로 고치지 않고 코디 macOS 실기에서 판정**한다. 실기에서 깨지면 그때 재발주한다. 대신 보고에 「깨질 때의 고침 후보 2개(주 프레임 판별 가능 여부 · 회의 자료 content 경로 예외)와 각자의 대가」를 적어 둔다
- **W5** 파일 이름에서 Windows 예약 이름(CON·PRN·AUX·NUL·COM1-9·LPT1-9)과 양방향 제어 문자(U+202A-202E·U+2066-2069)를 처리한다 + 시험
- **W6** `on_download` 경로의 실패도 실패 토스트 · URL 키 충돌(같은 URL 두 번 동시)을 해결 + 시험
- **W7** HTTP 읽기 타임아웃을 둔다(연결 30초 · 전체는 넉넉히 — 값과 근거 보고)
범위·allowed_paths·하지 말 것은 Phase 3 브리프 그대로(+ `fe-p3-decision.md`). 검증: `cargo test`·`cargo clippy -- -D warnings`(두 판) · 웹을 바꿨으면 해당 vitest + tsc. 보고 `fe-p3-worker-report.md` 끝에 「fix1」 절 + **§6 실기 절차 보강**(실패 토스트 재현 필수화 · PDF 미리보기 판정 · 세션 만료 · `xattr -l` 확인). 완료 보고는 같은 두 채널(subject 「frontend(셸) 완료: WORK-010 Phase 3 fix1」).
