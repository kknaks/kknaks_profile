## 한눈에 보기

- **해결하려는 문제:** dev에 Flutter 앱이 없어, DAY 기준 시술현황 앱과 데모 계정의 환경 연결 계약을 구현 기준으로 확정해야 한다.
- **이번 PR에서 바뀌는 것:** 직원 앱 SPEC-003 신설, SPEC-001 로그인 환경 연결 추가, 두 SPEC stable 상태 및 배포 문서·인덱스·Delivery 연결 정합.
- **리뷰 후 다음 단계:** 문서 PR을 사람이 머지하면 새 main SHA로 Delivery를 재결속하고 앱 구현·코드 검수를 진행한다. 코드 PR은 별도 하나로 dev에 올린다.

## 배경

Delivery [CENTURION_DAY #235](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235)의 결과 계약은 사용자 승인을 받았다. 프로토타입은 동작 참고로만 사용하고 로그인·브랜드·권한·API는 DAY를 따른다.

## 변경 내용

1. 시술현황·룸 상세·기존 API 조작·간호사 대리 수락·SSE·앱 푸시 및 통역 소비 계약을 정의한다. 통역 권한은 해당 고객정보 보기 권한, 푸시 수신자는 기존 호출 대상이다. 사전은 서버 컨텍스트로 소비한다.
2. 정식 앱 한 개가 고정 prod 로그인 진입점을 사용한다. 서버가 데모 계정을 dev에서 인증하고 환경과 API origin을 반환하며, 앱은 /me 확인 후 세션과 연결 대상을 함께 저장한다. dev 장애는 실패로 처리하고 prod 우회를 허용하지 않는다.
3. APNs·통역 서버 전체 구현은 이번 Delivery 범위에 넣지 않는다. 앱 더블 검증과 실제 통합 검증을 구분하고, Apple 서명·TestFlight·실제 서버 설정은 사용자가 맡는다.

## 리뷰 포커스

main에 새로 올라온 기획 원문(v1.0.0)은 모바일 조작 축소, 근무 원장 기준 전체 호출, charty 통역 연동으로 서술한다. 이 PR은 현재 대화에서 사용자가 직접 확정하고 #235에서 승인한 1차 범위(간호사 대리 수락·고객정보 보기 직원의 통역·기존 병원 원장 호출 대상)를 유지한다. 차이 근거는 검수 보고에서 확인했고, 머지 판단 때 함께 확인해야 한다.

OQ-A1 카드 이동·A9 국적 기반 언어·A11 일부 빠른 문구는 기존 보류를 유지한다. 출처 없는 화면 문구는 추가하지 않았다. 방 이동·차트 작성 등 옆 세션 기능은 그 SPEC과 머지를 기다려 소비한다.

## 확인 방법과 결과

- SPEC 및 WP 독립리뷰 PASS. stable 기준선 최종 독립 검수 PASS(차단 없음·승인 결과계약 의미 변화 0).
- 코디네이터 `python3 scripts/lint-pipeline.py --strict`: 0 error / 기존 타제품 warning 263건. DAY warning 0건.
- `git diff --check`: 통과.
- 앱·서버 코드는 이 PR에서 구현하거나 실행 검증하지 않았다.

## ⚠ 배포 주의

문서 변경이며 실행 배포는 없다. 환경 연결은 구현 전 계약이다. 실제 코드 PR과 서버 설정 반영 후 통합 검증이 별도로 필요하다.

<details>
<summary>문서·운영 체크리스트</summary>

- [x] 범위·계획·검증·복구 방법은 Delivery Issue #235가 관리한다.
- [x] 사용자 동작·API 계약을 SPEC-001/003에 반영했다.
- [x] 새 Legacy WP를 만들지 않았다.
- [x] Spec Coverage에 GitHub Delivery를 연결했다.
- [x] archive 변경 없음.

</details>

<details>
<summary>Delivery 추적 정보</summary>

- Delivery: https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235
- Target SPEC: DAY-SPEC-003 · DAY-SPEC-001
- 현재 v1 baseline: b4cd1a004cd99c8e57761ad8cccd434d5e237b38 (pending)
- 승인 plan_digest: sha256:c4f70ae3f97540fbe9b54c2b9d8698395e58cd9a509e393308a52d59cca5c75e
- Contract v1 digest: sha256:f3d03f99835bfaa232d08bd27203c6022741d872dcbb931cbc56985aeb210eb8
- 문서 PR 머지 후 같은 결과계약의 v2를 새 exact main에 결속한다.
- Code PR / review-delivery: 구현 전

</details>

🤖 Generated with an AI coding agent
