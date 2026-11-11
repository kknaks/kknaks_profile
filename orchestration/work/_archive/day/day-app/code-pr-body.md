## 배경

DAY에는 직원용 Flutter 앱이 없어, 폰·아이패드에서 시술현황을 보고 조작할 수 없었다. 승인된 [Delivery #235](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235)와 [SPEC PR mediness#921](https://github.com/MediSolveAIDev/mediness/pull/921)을 기준으로 iOS 1차 앱을 만든다.

사용자 지시대로 문서·코드 PR 모두 마지막까지 미머지로 둔다. 구현 기준은 리뷰 PASS인 SPEC commit `78f3ee59c8a10e0abb1bde8896302873a46d0732`다. canonical main baseline은 아직 pending이며 ready로 바꾸지 않았다.

## 변경 내용

### 1. DAY 직원 앱

DAY 테마·로그인·병원 선택·세션 복원과 시술현황을 구성했다. 폰은 한 열·바텀시트, 아이패드는 격자·두 열·팝오버를 사용한다. 호출·재호출·간호사 대리 수락·시작/종료·취소·마취·귀가 대기·읽기 차트를 현재 API에 연결한다. 권한·상태·카드 순서는 서버가 내려준 값을 사용한다.

### 2. 인증 대상과 세션 일관성

정식 앱의 고정 로그인 진입점에서 서버가 데모 이메일을 판별해 dev로 인증을 전달한다. 일반 계정은 해당 서버에 남는다. 전체 60초·리다이렉트 및 재시도 없음·동시 상한 4·dev 장애 시 503으로 처리한다. prod 경로에서 데모 계정의 KOS 호출이나 DB 행 생성이 없음을 로컬 테스트 DB로 확인했다.

앱은 받은 HTTPS origin을 허용 목록과 대조하고 병원 선택·/me 환경을 확인한 뒤 세션 대상·토큰·만료·직원 ID를 Keychain 레코드 하나에 저장한다. 이후 HTTP·SSE·WS·푸시 수락은 그 대상만 사용한다. release는 환경 정보가 빠진 응답을 거절한다. 명시한 로컬 origin의 개발 debug 예외를 둔다.

### 3. 실시간·알림·통역 클라이언트

SSE 갱신·재연결·생명주기 처리, APNs 토큰 등록/해제·알림 이동·Swift 네이티브 본인 수락, 통역 WS·마이크·PCM 재생·기기 TTS를 구성했다. 통역은 시술현황 보기 권한을 따르며 7개 언어를 구분한다. 빠른 문구는 원천이 있는 5개 언어만 사용한다.

D2 기기/APNs 발송 서버와 D3 통역/사전 서버 전체는 이번 변경에 포함하지 않는다. 서버가 없는 경로는 앱 테스트 대역으로 검증했고 실제 통합은 pending이다.

## 검증

- backend: 코디 `DAY_ENV_FILE=<기존 local.env> scripts/test.sh -q` → **663 passed**, 1 warning(로컬 PostgreSQL·Redis, scratch `day_test`, 신규 D1 infra 6건 포함).
- backend 독립 재검수 **PASS**: local Compose 환경변수 전달, 비정상 JSON, 동시 상한·취소 복구, 설정 오류 로그 값 숨김을 확인했다.
- 앱 수정본 검증: Flutter analyze 0 issue / Flutter test **155 passed** / Swift 판단 검사 **47 passed** / unsigned iOS build 성공(17.6MB).
- 앱 독립 재검수 **PASS, 차단 없음**. 이전 세션의 늦은 401 경합, Keychain 저장 실패, 전체 75초 제한, 통역 마이크 정리와 실제 WS 핸드셰이크를 수정·재검증했다. 코디도 수정본 analyze 0 issue · native 47건을 독립 재실행했다.
- 실서버·실기기·시뮬레이터 화면·실제 Keychain/알림 액션·APNs·Soniox·prod 데모 연결은 미실행이다.

비차단 참고: 이전 세션의 로그아웃 처리가 남아 있을 때 새 세션의 로그아웃은 최대 약 40초 동안 무시될 수 있다. 깨진 Keychain 레코드는 사용하지 않고 다음 로그인 때 덮어쓴다. 실제 Keychain 경합과 wss/TLS 경로는 실물 검증이 남았다.

## 리뷰 포커스

- 구현 범위는 이번 대화에서 확정한 1차 SPEC이다. 신규 기획 원문과 범위 차이는 SPEC PR에 기록했다.
- 서버 업무 규칙 재계산과 원천 없는 화면 문구·번역을 추가하지 않았다. 카드 이동·국적 기반 언어 자동 선택·vi/yue 빠른 문구는 기존 보류를 유지한다.
- 방 이동·차트 작성·시드 등 옆 세션의 기능은 그 SPEC·머지를 기다려 소비한다.
- 공식 main baseline pending은 사용자 지정 구현 순서 때문이다. 독립 코드 리뷰와 검증은 현재 SPEC commit을 기준으로 수행했다. `review-delivery --plan`은 `delivery review requires a ready stable SPEC baseline`으로 공식 evidence 기록을 거절했다. 문서 PR을 선머지하거나 ready를 위조하지 않았으며, 마지막 머지 단계에서 baseline 재결속 후 공식 evidence를 기록한다.

## ⚠ 배포 주의

머지·배포·서명·TestFlight는 실행하지 않았다. 실제 값은 사용자가 나중에 설정한다.

- 서버: `DAY_PUBLIC_API_BASE`, prod `DAY_DEMO_LOGIN_EMAILS`·`DAY_DEMO_API_BASE`. dev 공개 origin과 prod 데모 대상이 같아야 한다. 로컬 Compose와 서버 일반 설정에는 변수 전달 구조·빈 이름만 추가했다.
- 데모 연결을 중단할 때는 **데모 이메일 목록을 유지하고 대상 주소만 비워** 503으로 막는다. 이메일 목록을 비우면 일반 prod 인증으로 가므로 복구 수단으로 사용하지 않는다.
- 앱: Bundle ID는 예제 placeholder이며 사용자 로컬 xcconfig로 확정한다. Apple Team/서명값은 저장소에 없다. DAY 아이콘 자산은 미제공 상태로 App Store 제출 전에 필요하다.
- D2/D3 서버 및 APNs·Soniox 설정 후 실제 연결을 검증해야 한다.

Refs #235
Spec: MediSolveAIDev/mediness#921

🤖 Generated with an AI coding agent
