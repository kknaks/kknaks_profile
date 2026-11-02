# 야간 코드 구현 목표 — 사용자 승인 2026-09-22

총10 Phase를 순차 구현→독립 검수→수정→다음 단계로 진행한다. 오늘 밤 코드 구현과 자동 검증 우선, 사용자 앱 설치·최종 E2E는 내일이다. 미실측을 통과로 기록하지 않는다. 물리기기 미확인 gate는 해당 증거를 pending으로 남기고 독립 구현을 진행할 수 있다. 실제 기능 불성립을 관측하면 수정/구조 판단 없이 통과하지 않는다. 운영 배포·Release 발행 완료는 오늘 코드완료와 별개로 기록한다.

Phase1 Claude 구현 발주. Phase별 코드 완료/자동검증/실측 상태를 분리해 남긴다. 기존 코드 워크트리 사용, 같은 파일 동시작업 금지. 문서 계획 재작성 루프 없이 실물 구현 검수를 우선한다.

도구 확인: cargo/rustc, Node20, OpenSSL, Xcode clang 가용. 전역 설치 불필요. P4 frontend Rust 검증 설정 추가 완료. Phase1 구현 진행 중.

P5 준비 완료: strong-hajin config에 infra repo/worker 및 roles/strong-hajin/infra 정의. 전용 차트/Application/AppProject만 허용, 로컬 Helm 검증과 실제 배포 구분. 인프라 구현은 Phase6에서 직렬 발주할 예정이며 아직 외부 레포 수정0.
