# DAY 모바일 배포 문서 표현 수정

작업지 /Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec. planner. AGENTS.md 필수 문서를 읽고 기존 문서 흐름을 지킨다. 사용자 요청은 iOS·Android 환경과 비공개 배포 구조를 메디니스에 기록, 회사 medisolveai, iOS부터. 이번은 검수에서 지적된 문장만 고치는 작업이다. 커밋/push/PR/계정 변경/코드 변경 금지. 다른 코디네이터가 이미 문서를 05b9a195에 커밋했으니 되돌리지 않는다.

읽을 것: products/day/40-architecture/mobile-deployment.md와 /Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/mobile-deployment-review-report.md. 완전한 재조사나 새로운 설계 금지.

allowed_paths: products/day/40-architecture/mobile-deployment.md 하나. 보고서는 profile orchestration/work/day-data-architecture/mobile-deployment-fix-report.md 한 개.

수정 요구:
1. WARN 1: 앱에서 KOS와 푸시 발송 API를 직접 부르지 않는다는 뜻으로 한정. 앱은 OS/SDK로 APNs/FCM 등록 및 기기 토큰 취득→DAY 서버 전달은 한다고 명시. Mermaid에도 token registration 연결 추가 가능. 앱에 서버 발송 자격증명 금지와 클라이언트 SDK 설정 구분.
2. WARN 2: 기존 코드 규칙의 Team ID 금지와 Xcode DEVELOPMENT_TEAM 필요 사이를 미결로 표시. Team ID는 비밀키가 아님, 저장소에 기록하는 범위는 기존 규칙 해석/개정 전 미결. 로컬 비추적 xcconfig/CI env 방식은 후보로만 적고 M-16 추가. AGENTS 변경하지 말 것.
3. WARN 3: iOS 순서 3번에서 Android productFlavors 제거, Android 후속 안내로 이동.
4. WARN 4: Android 출시 시점 확정 표현 제거, 문서에 함께 포함·실제 설정은 iOS 우선만 확정. Android 착수/출시 시점 미결.
5. WARN 5: Apple이 무단 사용 방지 장치를 요구→권고.
6. WARN 6: prod는 실제 병원 연결 포함 가능, demo 배제 정책은 미정으로 표현(기존 서버 dev 데모만 제약 유지).
7. WARN 7: 출처 표 Flutter iOS 배포 항목에서 TestFlight 심사 직접 확인처럼 보이는 표현 제거. 미검증 안내 유지. APNs TestFlight production은 정확한 공식 근거 https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/APNsOverview.html 에서 TestFlight 문장을 짧게 확인하고 출처 추가 가능(안 되면 배포 프로파일 기준 설명만 유지).
8. 빌드 mode와 flavor는 독립, 서명 키 앱 포함 금지(서명 자체는 당연 필요) 구분 유지. 기존 과도한 확정 문구만 정밀화.

log.md WARN8은 이번 scope 밖, 변경하지 않는다. 필수 로그 요건인지 보고서에서 확인만 하고, 필요하다면 코디에게 보고. lint --strict 결과 DAY 오류 0, diff --check 확인 후 보고. 완료 후 idle. lifecycle는 live preamble 따른다.
