# planner — 앱 계약 r2 (코디 · 2026-10-27) — review-doc r1 FAIL 6 · WARN 14 · U1~U6 · WP-KOS 결과

원천: `app-review-doc-r1.md`(FAIL · WARN 줄마다) · `app-wp-kos-report.md`(K1 ~ K4) · `_RESUME` §2 10-27(WP-KOS 기본값 Q-154 ~ 157). allowed_paths · 금지 · 보고는 앞 판 그대로(보고서 `app-spec-r2-report.md` — 처분 줄 → 고친 곳 대조표).

## FAIL 은 전부 고친다
- F1 `push_log.call_id` NOT NULL — 새 표 또는 마이그레이션 방식(표 다시 만들기)을 계약에 · 운영 DB 기준 시험 조건
- F2 사진 열람 = Bearer(쿠키 없음) — 웹 썸네일은 back 이 내려준 **짧은 서명 URL**(또는 fetch + blob) 중 지금 인증 구조에 맞는 것 하나로
- F3 기기 식별 — pending · claim · 문진 이력 · 스트림에 `deviceId` 계약(같은 코디 계정의 태블릿 / 폰 구분)
- F4 · F5 WP-KOS 결과 반영 — K4 경로 `get-visitor-images` · ④-c 본문(category 안 보냄 · fileName · visitorId · source · shootingDateTimeUtc · 장비 코드 = `get-codes` 에서 이름으로 찾기) · ④-a K2 만료일 · §8.0 #8 · #21 · #22 게이트 = 통과 · OQ-619 · OQ-622 닫음 · WORK WP-KOS = 완료(산출 `app-wp-kos-report.md`)
- F6 AP-41 암호화 — 아래 U2

## WARN — 리뷰 제안대로 고친다(W1 ~ W14). SPEC-005 낡은 줄(W4)은 SPEC-005 에서 그 줄만(취소선 + 「SPEC-004 0.4.0 로」)

## 사용자 결정 U1 ~ U6 — 코디 기본값(사용자 통보)
- U1 띄우기 = 보이는 알림 · 소리 없음 · 알림 목록 · 배지 · 설정에 넣지 않음(「알림 둘만」과 별개 — 화면 열기 신호)
- U2 사진 볼륨 암호화 = **클러스터가 지원하면 켬 · 안 되면 없음 + 법적 검토 주석** — WP-INFRA 에 「암호화 가능 여부 확인 · 보고」 한 줄
- U3 알림 목록 = 계정 행(기기 없어도 쌓음)
- U4 설정에 「이 기기 이름」 칸 넣음
- U5 문진 잠금 해제 실패는 **코디 아이디를 잠그지 않는다** — 그 기기에서만 5번 틀리면 1분 기다림(로그인 잠금과 별개 카운터)
- U6 앱 예약 상세 = 이 기기 [여권 스캔]만(다른 기기로 보내기는 웹에서)
