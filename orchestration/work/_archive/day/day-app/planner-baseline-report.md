# day-app planner — 승인된 SPEC 기준선 확정(stable) 보고

## 상태: done — 문서 상태만 바꿈 · **main baseline ready · 구현 착수를 선언하지 않는다**

- task `task_f9169c05267b` · dispatch `ctx_664875b4e747` · 워크트리 `mediness-mediness/day-app-spec`(HEAD b4cd1a00 · origin/main 3f57c1af) · 커밋 · rebase · push · PR 없음
- 근거: 사용자 Delivery #235 결과 계약 승인(2026-11-09 「응 진행하자 !」 · digest `sha256:c4f70ae3…5e`) · review-policy-report PASS · review-wp2-report PASS

## 이번 변경 (이전 로컬 변경 보존 · 통째 재작성 없음)

| 파일 | 줄 | 변경 |
|---|---|---|
| `products/day/20-spec/spec-001-login-session.md` | frontmatter `status` | `draft` → `stable` |
| `products/day/20-spec/spec-003-mobile-app.md` | frontmatter `status` | `draft` → `stable` |
| `products/day/20-spec.md` | SPEC List DAY-SPEC-001 · 003 | Status `draft` → `stable` |
| `products/day/30-work.md` | Spec Coverage DAY-SPEC-001 · 003 | `— (WP · Delivery Issue 미발주)` → `[Delivery #235](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235)` · 구현 상태 `proposed` 그대로(형식 = 다른 제품 `[Delivery #N](url) \| proposed` 선례) |

- `mobile-deployment.md` · `delivery-request.json` · SPEC-000/002 · 다른 SPEC 상태 손대지 않음. WP 파일 · 원장 생성 없음.
- SPEC-001 은 #235 의 target 이라 SPEC-003 과 같이 coverage 를 바로잡았다(같은 「미발주」 오래된 표현).

## 의미 변화

- **없음** — 본문(앱 동작 · 권한 · 라우팅 · 푸시 · 통역 · 보류 · OQ) 한 글자도 바꾸지 않았다. 바뀐 것은 status 2줄 · 인덱스 Status 2칸 · coverage 2칸.
- 승인 결과계약(Delivery #235 · `delivery-request.json`)은 수정하지 않았다. target(DAY-SPEC-003 · 001) · Acceptance · Non-Goals 대상 문장 그대로.

## 검증

- `python3 scripts/lint-pipeline.py --strict`(레포 규칙 lint · `mediness` CLI 바이너리는 이 환경 PATH 에 없음) → exit 0 · `0 error, 263 warning` · **products/day ERROR 0 · WARN 0** · 263건은 전부 다른 제품(무관)
- `git diff --check` → 출력 없음(exit 0)
- 정합: frontmatter 001 · 003 = stable · 000 · 002 = draft 그대로 / 20-spec.md SPEC List 같은 값 / 30-work.md coverage 001 · 003 = Delivery #235 · 000 · 002 그대로

## ⚠ 보고 — 최신 main 기획 원문과 승인 계약의 의미 차이 (SPEC 은 바꾸지 않았다)

origin/main 3f57c1af 에 2026-11-09 08:10–08:13 UTC 로 올라온 `products/day/00-baseline/planning/데이(CC)-*.md`(v1.0.0) 가 직원 앱 범위 · 수락 · 통역 · 푸시를 다르게 적는다. 승인 결정을 임의로 바꾸지 않고 근거만 남긴다 — 사용자 · 코디 판단 필요.

| 주제 | 기획 원문(main) | 승인 SPEC-003 / SPEC-002 |
|---|---|---|
| 모바일 범위 | 「데이(CC)-기획안-·-모바일」 L67: 「CC 모바일에서는 보기 · 호출 수락 · 관리실 통역 · 알림 받기만 한다. 마취 · 시작 · 종료 · 차팅 · 관리실 이동 · 귀가 대기는 시술 현황(CC-06)에서」 · 예약 내역 · 대기 고객 보기(CC-24-2) · 사진(CC-25 · 1차 밖) | 앱에서 마취 · 호출 · 재호출 · 시작 · 종료 · 취소 · 귀가 대기까지 조작(U-4 ~ U-9) · 예약 화면 없음 |
| 수락 | 「시술-현황」 3-2: 원장이 CC 모바일에서 수락 · 간호사는 수락 없이 「시작」(실제 온 원장 고름) · 담당 원장을 간호사가 바꿈 | 간호사 대리 수락(사용자 결정 · SPEC-002 U-6 · SPEC-003 U-6) |
| 전체 호출 받는 원장 | 「그날 근무가 있는 원장」(근무 스케줄 기반 · 「시술-현황」 L409 · 3-2 표) | 「그 병원 원장 목록 전체」(사용자 2026-11-09 「응 맞아」 · OQ-A17 닫음) |
| 통역 | 「모바일」 CC-24-1: 원장 · 간호사 · charty 통역 기능을 연다(CC 가 모델 운영 안 함) · 켠 계정/고객/언어/시각 저장 | 시술 현황 고객 정보를 보는 사람 모두(사용자 OQ-A15) · DAY 서버 WS + interpret-pwa 사전(D-3) · 기록 저장 없음 |
| 기타 | 「다시 알림」(수락 뒤 미시작 원장에게 푸시 재발송) · 재호출 기본 = 처음 호출 그대로 | SPEC 에 없음 · 재호출 창 기본 = 처음 대상(SPEC-002 OQ-04) |

- 기획 원문은 CC 전체 v1.0.0(상위기획 · 근무 스케줄 · charty 연동 전제)이라 1차 범위와 시점이 다를 수 있다. 판단은 하지 않았다.
- 권장: PR 전에 사용자에게 「#235 승인 범위(1차) 유지 vs 기획 원문 v1.0.0 정렬」을 확인. 유지면 이 stable 그대로, 정렬이면 SPEC 개정 + #235 scope_delta 재승인.

## 남은 것

- 코디 독립 리뷰 → commit · rebase(3f57c1af — planning 추가분과 교집합 없음) · push · SPEC PR. 머지 뒤 #235 를 같은 key · version 2 · 새 main SHA 로 재결속해야 baseline ready.
