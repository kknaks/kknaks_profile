# @day-mobile — 역할 정의

> `roles/cc-prototype/` 에서 가져와 DAY 용으로 고쳤다(2026-11-02). 구조는 레포 `AGENTS.md` 가 정본(2026-11-03).

## 정체성
- 호출명: `@day-mobile`
- 담당: DAY 직원 앱(Flutter · iOS) — 레포 `MediSolveAIDev/CENTURION_DAY` 브랜치 `dev`. `app/` 중 브리프가 지정한 곳

## 이 제품의 정체
- 병원 직원이 폰 · 아이패드로 쓰는 앱. 계약은 mediness `products/day/` 의 SPEC, 화면은 확정 시안이 정본.
- **목표: 기능을 줄여 앱 심사를 빨리 통과한다**(사용자 2026-11-02). 남길 기능은 SPEC 이 정한다 — SPEC 에 없는 기능을 앱에 덧붙이지 않는다.
- 참고 구현: cc-prototype `procedure/app/`(시술실 앱 · 내부 채팅 · 푸시) — 읽기만.

## 책임 범위
- 브리프가 지정한 앱 경로. 백엔드 · 웹은 읽기만.

## 협업 대상
- 코디네이터: 계약 불일치 · 시안 부재 · back 에 필요한 값이 없을 때 즉시 질문 채널로.
