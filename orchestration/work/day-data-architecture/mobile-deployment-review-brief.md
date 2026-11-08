# DAY 모바일 배포 아키텍처 문서 검수

역할: read-only reviewer. 작업지 /Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec. 먼저 AGENTS.md 및 필수 진입 문서, /Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/reviewer/role.md와 같은 폴더 규칙을 읽는다.

SSOT: /Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/mobile-deployment-planner-brief.md 의 마지막 완결 지시. 사용자 요구 = 메디니스에 iOS와 Android 개발·운영 및 비공개 배포 구조를 함께 기록, 회사 이름 medisolveai, 처음 앱 제작, iOS 먼저. 개발·운영 flavor와 com.medisolveai.day(.dev)는 제안이고 최종 배포 경로는 미정. Apple Team 사용 가능은 사용자 응답 기준이며 실제 계정 검사한 것 아님.

대상: products/day/40-architecture/mobile-deployment.md 및 README.md/system.md의 이번 diff. planner report는 profile 같은 폴더 mobile-deployment-planner-report.md.

검수: 사용자 결정과 제안/미결 구분, 회사 도메인 소유나 앱ID 등록 완료 오표시 없음, 기존 DAY auth/emr/DB/런타임과 모순 없음, iOS private 배포/Unlisted/Enterprise 자격·범위 및 심사 설명, Android 직접 APK와 managed Google Play 및 업데이트/키 관리, APNs 환경이 backend flavor와 독립임, FCM 미확정, 비밀정보 없음, 링크 정확성과 초보자 이해 가능성. 과잉 기능이나 업무 스펙을 추가하지 않았는지. 공식 출처만 근거로 보고하며 미확인은 분리.

허용 변경: /Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/mobile-deployment-review-report.md 보고서 한 개만. 제품 문서 수정/커밋/push/PR 금지. lint-pipeline --strict와 git diff --check 실행하고 products/day 오류와 무관 기존 오류 분리. PASS/WARN/FAIL, 파일:줄 근거, 수정 필수 여부, 다음 사용자가 실제 설정 시 알아야 할 미결을 짧게 남긴다. 완료는 live preamble worker_done으로 보고하고 idle.
