# [planner] 제출 자료 원천의 실행 현황·통역 공급자 근거 최종 반영

같은 spec 워크트리, 네 문서 products/day/60-release/app-store-preparation.md 및 리포트 /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-policy-report.md만 수정. 다른 파일·코드·issue·Delivery·커밋/push/PR 금지.

할 일은 좁게 3개:
1. 앱/버전/한국어 메타데이터·URL 2개 등록과 screenshot10장 API COMPLETE 사실을 /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-asc-report.md, mobile-screenshot-report.md에서 확인해 현황 행 갱신. iPhone1320x2868×5/iPad2064x2752×5, RGB·manifest·코디 시각승인·SHAallowlist. 원천 main은 lib/main.dart, 촬영은 tool/store_capture/main.dart. 정책이 아닌 실행 상태는 보고서를 가리키고 문서 전체에 복제하지 않는다. binary 업로드는 아직 진행중이므로 완료라 적지 않는다.
2. 문안 원천 §5-2를 실제 등록된 설명(207자)과 일치시키고, 별도 후보문구를 제거하거나 명확히 참고로 분리해 SSOT 혼동 없앤다. 사용자에게 이미 등록된 문안과 별개 선택을 새로 요구하지 않는다. 등록문안 바꾸는 remote action 금지.
3. Soniox공식 https://soniox.com/policies/privacy-policy §1·4·5, https://docs.soniox.com/security-and-privacy 를 직접 확인. 공개정책상 실시간 API CustomerContent는 transient processing/no retention, 모델학습/평가/개선에 쓰지 않음, content-free usage/운영 metadata는 별도 보관을 구분. DAY code는 real-time STT/TTS WS, Async저장호출 없음과 대조하여 공개정책 근거로 문안에 반영. 우리가 해당 회사의 별도 계약/프로젝트설정을 검증했다고 주장하지 않음. 'Soniox전체 정책이전혀미확인'이라는 stale서술은 공개정책확인/개별설정미확인으로 고친다. 단순 통역에 개인정보가 무조건 포함/동의팝업필수 단정 금지. Apple label에서 실시간전송=항상수집이라는 단정도 금지. 계정/푸시/채팅서버저장 항목은 유지.

운영주체/지원연락처/책임자/서버보관파기/시행일은 여전히 사용자 미응답. 이 값들은 추측해서 채우거나 페이지바로발행가능이라고 쓰지 않는다. 문안초안을 완성해 두되 미정분리.

문서lint 네 문서 관련 오류만 체크. 새 대규모 조사/추가워커 금지. 완료는 preamble worker_done 및 코디terminal 알림2채널. 한국어 간결리포트.
