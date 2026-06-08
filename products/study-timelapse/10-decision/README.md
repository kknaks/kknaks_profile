# Decision Index

규칙: `rules/product-doc-pipeline.md`

> study-timelapse 의 결정 로그. 원본 `study_timelapse/medi_docs/current/adr/` 의 ADR 21건(adr-01~22, **adr-03 결번**)을 큐레이션 이관한 것이다. 각 decision 의 `구현 현황` 섹션에 실제 코드 grounding 을 남겼다.
> 이관 범위: 10-decision 만 (baseline/spec/work 는 미이관). baseline/spec 연결은 후속 스테이지에서 채운다.

## 결정 로그

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| STL-DEC-001 | 비율 4:5 통일 — 백엔드 VALID_ASPECT_RATIOS 수정 | accepted | (미이관) | 4:5 채택, 4:3 제거 | (예정) |
| STL-DEC-002 | 세션 업데이트 단일화 — saving 에서만 completed | accepted | (미이관) | saving 단일 호출 | (예정) |
| STL-DEC-004 | 녹화 패러다임 — 프레임 샘플링(무음) + Native 재작성 | accepted | (미이관) | 프레임 샘플링 채택 | (예정) |
| STL-DEC-005 | 캡처 스케줄 함수 — Sqrt 스케줄 | accepted | (미이관) | Sqrt 채택 | (예정) |
| STL-DEC-006 | 백그라운드 녹화 정책 — keep-awake + 자동 정지 | accepted | (미이관) | C+A 채택 | (예정) |
| STL-DEC-007 | 정지 확인 UX — 인디케이터 + 모달 | accepted | (미이관) | A+B 채택 | (예정) |
| STL-DEC-008 | 캐시 생명주기 — stitch 즉시 삭제 + 캡처 5분 TTL | accepted | (미이관) | D 채택 | (예정) |
| STL-DEC-009 | 카메라 통합 — VisionCamera frame processor plugin | accepted | (미이관) | B-3 채택 | (예정) |
| STL-DEC-010 | 구독 상태 모델 — 5상태 머신 + timezone | accepted | (미이관) | 5-state 채택 | (예정) |
| STL-DEC-011 | 월 only $1.99 — 연 플랜 폐기 | accepted | (미이관) | 월 only 채택 | (예정) |
| STL-DEC-012 | mock-purchase API + 이벤트 소싱 | accepted | (미이관) | 전용 API + append-only | (예정) |
| STL-DEC-013 | Anonymous paywall + 약관 양쪽 노출 | accepted | (미이관) | 로그인 유도 + 양쪽 | (예정) |
| STL-DEC-014 | Phase 1 실행 전략 — 1a 후 1b/1c 병렬 | accepted | (미이관) | 병렬 + 단일 디바이스 DoD | (N/A 프로세스) |
| STL-DEC-015 | 영수증 검증 이중 경로 — verify + webhook | accepted | (미이관) | 이중 경로(webhook=SoT) | (예정) |
| STL-DEC-016 | 트라이얼 — introductory offer 7일 + 자동 갱신 | accepted | (미이관) | B+A, 가입=free | (예정) |
| STL-DEC-017 | 환불 정책 — 스토어 위임 | accepted | (미이관) | Apple/Google 위임 | (예정) |
| STL-DEC-018 | RevenueCat app_user_id 매핑 — 가입 즉시 logIn | accepted | (미이관) | 가입 즉시 logIn | (예정) |
| STL-DEC-019 | Grace Period — pro 유지 + grace_until 컬럼 | accepted | (미이관) | 옵션 B 채택 | (예정) |
| STL-DEC-020 | RevenueCat Webhook 인증 — Bearer | accepted | (미이관) | Bearer 채택 | (예정) |
| STL-DEC-021 | 취소 vs 환불 상태 전환 | accepted | (미이관) | 환불=즉시 / 취소=만료까지 | (예정) |
| STL-DEC-022 | subscription_status 신뢰원 — backend 캐시 + sync | accepted | (미이관) | B + 강제 sync endpoint | (예정) |

> **adr-03 결번**: 원본 `adr/` 디렉토리에 `adr-03` 파일이 존재하지 않는다. 번호는 원본 ADR 과 1:1 lineage 유지를 위해 그대로 보존(STL-DEC-003 미발급).

## 미결 사항

| ID | Question | Owner | Next |
|---|---|---|---|
| STL-DEC-008 | 캡처 프레임 5분 TTL 적정값(1분/10분) | 사용자/admin | 운영 피드백 |
| STL-DEC-013 | 약관/개인정보/환불정책 planner 초안 + Phase 2 전 법무 | — | 별도 task / Phase 2 게이트 |
| STL-DEC-017 | `policy-05-subscription-refund` 일할→스토어 위임 갱신 | — | P2.1 task |
| 다수 | 각 decision 의 정밀 전이·계약 명세 | — | 20-spec 스테이지(후속) |
