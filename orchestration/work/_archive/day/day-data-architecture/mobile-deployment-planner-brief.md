
# [planner] <한 줄 제목>

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

<같은 워크트리를 다른 워커와 공유하면 여기에 경고를 적는다. 예: "BE 워커가 `back/` 에서 병렬 작업 중 — 건드리지 마라.">

## 1. SSOT — 먼저 읽을 것

- `<spec/WP 절대경로>` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `<추가 참조 절대경로>`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- `<…/para/areas/concept/<영역>/<stem>.md>` — <이 작업에서 무엇을 이대로 하라는 건지 한 줄>

## 2. 배경 / 무엇을 바꾸나

<현재 상태 → 바꿀 것. 왜 하는지 1~2문단.>

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

<BE↔FE 계약이 있으면 필드명·shape·에러코드까지 명시. 없으면 "해당 없음".>

## 4. 먼저 읽을 핵심 파일

- `<파일:줄>` — <왜 봐야 하는지>

## 5. allowed_paths — 이 밖은 건드리지 마라

products/day/40-architecture/ 만 — 한국어로 작성

## 6. 구현 단계

1. <…>

## 7. 범위 제약 — 하지 말 것

- <…>

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9bbbcec2-6de7-453d-9504-3e548904046b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9bbbcec2-6de7-453d-9504-3e548904046b \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9bbbcec2-6de7-453d-9504-3e548904046b --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

## 이번 발주의 완결 지시 (위 일반 자리표시자보다 우선)

너는 맥락이 없다. 위 일반 템플릿의 미기입 항목은 이 절로 모두 대체된다. 완료 채널은 live dispatch preamble이 정본이다. 오래된 template의 terminal 직접 주입은 필요 없다.

사용자 요청: "기록은 메디니스에 하고 아이폰, 안드로이드 다 적어줘. 아직 내가 처음 이제 앱을 만드는거야 medisolveai 가 회사 이름이야". 앞 대화에서 iOS 먼저 구축, 최종 배포는 비공개라고 했고 회사 Apple Developer Team 사용 가능 여부에 "응"이라고 답했다. 설치 대상이 회사 직원/고객 병원 직원인지, 개인 폰/관리 기기인지는 미답이다.

읽기: AGENTS.md가 요구하는 context/manifest.yaml, context/index.md, context/current-state.md, rules/document-pipeline.md; products/day/README.md,20-spec.md,30-work.md 및 40-architecture/README.md,system.md,code-structure.md; SPEC-001 로그인. profile의 reference/2026-11-03-cc-day/system/README.md도 참고. 코드 레포 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture/AGENTS.md는 읽기 전용.

변경: products/day/40-architecture/mobile-deployment.md 신설하고 architecture README 및 system에 필요한 짧은 링크만 추가한다. 문서 위치는 규칙상 허용되는지 먼저 확인. 아키텍처 문서이며 코드 구현, SPEC, Delivery, decision 생성은 안 한다. 배포/설정 실행은 안 한다. 다른 제품, archive 수정 금지. 커밋/push/PR 금지.

한국어로 처음 앱 만드는 사람이 이해할 수 있게 작성. 확정 사실 / 제안 / 미결 / 실제 설정 완료를 구분. 회사 이름 medisolveai는 확정이지만 도메인 소유는 미확인. com.medisolveai.day 및 com.medisolveai.day.dev는 두 플랫폼 식별자 후보로만 쓰며 등록 완료나 확정으로 쓰지 않는다. dev/prod 두 flavor는 추천안이다. Android도 문서에는 함께 다루되 실제 진행은 iOS 우선. 별도 staging 필수 도입 안 함.

담을 내용:
- 공통 Flutter 코드, iOS/Android 개별 서명/식별자. 앱→HTTPS 환경별 API→기존 DB schema day_dev/day_prod 및 KOS demo/live. 서버 경유만, 앱에 KOS/서명/푸시 비밀키 넣지 않음. API hostname 미정. 기존 auth Bearer 및 공용 service 유지. 기존 서버 설계와 모순 금지.
- 앱명 DAY Dev/DAY, dev/prod 식별자 분리와 동시 설치, flavor와 debug/release 차이, local API override는 dev에서만 제안.
- iOS 회사 Team/App ID/Bundle ID/Xcode scheme·config/인증서·provisioning/iPhone+iPad 및 최소 OS 미정/Keychain/권한은 기능별 최소 설정. 자동 서명은 로컬 시작 추천, CI 서명/비밀 저장은 향후. TestFlight는 검증 수단이지 정식 상시 배포 경로 아님.
- iOS Custom Apps(지정 조직 Apple Business 경유·심사), Unlisted(검색 비노출·링크 가진 누구나 다운로드 가능·로그인 필요·심사), Enterprise(100인 이상 등 자격·자사 직원 내부용·고객 병원 배포 대안으로 확정 금지), Ad Hoc(등록 기기 소규모 검증 및 한도, 정식 대규모 운영 추천 아님). 비공개 배포 != Apple 심사 생략. 현재 배포 방식은 미정.
- Android 회사 계정/Application ID/flavors/keystore 및 키 보관·백업/APK 직접 배포 또는 managed Google Play private 앱 후보/직접 배포의 설치 허용·업데이트 책임. Google Play 등록이 직접 APK 배포의 필수라는 식으로 쓰지 않음. 최신 외부 배포 개발자 인증 조건은 공식 출처로 검증하되 국가·시점 추정 금지.
- 푸시 iOS APNs, Android FCM 후보; 기존 APNs 직접 설계 유지. FCM Android 도입 미결. APNs sandbox/production은 flavor나 backend dev/prod와 같은 축이 아님: signing entitlement 기준, TestFlight production. 앱별 device token을 계정/기기/플랫폼/앱ID/푸시 환경으로 구분 필요(향후 계약, 테이블 변경 아님). foreground SSE와 background push 구분.
- 환경별 구성표, 배포 구조 작은 Mermaid, 미결 목록, iOS부터 하는 순서(계정 권한 확인→식별자 확정→flavor→실기기 로그인→푸시→비공개 경로→자동화). 완료 체크처럼 꾸미지 말 것. 버전/build, crash logs 환자정보 금지, release 검증 항목 간단히.

공식 문서 링크 및 확인일 2026-11-08 포함. 직접 browse하여 기술 조건 확인(가능하지 않으면 링크 검증 안 됨 표시). 참고 URL:
https://docs.flutter.dev/deployment/flavors-ios
https://docs.flutter.dev/deployment/flavors
https://docs.flutter.dev/deployment/ios
https://developer.apple.com/support/unlisted-app-distribution
https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/set-distribution-methods
https://developer.apple.com/programs/enterprise/
https://developer.android.com/distribute/marketing-tools/alternative-distribution
https://developer.android.com/developer-verification
https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns

검증: lint-pipeline --strict 실행 후 products/day 범위 오류와 기존 무관 오류 분리. diff --check 및 링크 실재 검사. 변경 파일/검증/미결 요약을 /Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/mobile-deployment-planner-report.md 에 남긴다(이 보고서만 profile 쓰기 허용). 완료 보고 후 idle.
