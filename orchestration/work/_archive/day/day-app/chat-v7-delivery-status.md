채팅 v7 코드와 독립검수를 기존 PR #237에 반영했습니다. 코드 head `3aaa97806684b8cea7f7fb777adbcdcff7ae0de6`(서버 `1dc1ec3d` + 앱 `3aaa9780`), 대상 dev, 미머지입니다.

- 서버 전체765 pass(작성자), 독립 실PG/Redis96·스트림7×3·구조/배포121 pass. 이전 WARN3 해소, 배포스크립트 주석 E501도 정정 후 코디 ruff backend scripts 통과.
- 앱245 pass/analyze0/native54 독립검수 후, 키보드 이식누락·긴직무명 overflow2건을 최소수정했습니다. 제품후속 독립검수 PASS·관련120 pass, 추가 키보드매트릭스 포함 레이아웃7은 코디 직접 재현해 통과했습니다.
- 로컬11040 채팅API 미반영(404)이므로 실제 직원 간 송수신 통합은 pending입니다. 실기기 카메라/사진제한접근/영상/APNs, 실제 키·Blob·서명/TestFlight는 사용자 설정 뒤 확인합니다.
- SPEC PR #921은 `b0f71ec3` 검수본으로 미머지입니다. 공식 review-delivery --plan은 `delivery review requires a ready stable SPEC baseline`(conflict)로, 사용자 지시대로 문서 선머지를 하지 않아 완료 판정으로 닫지 않았습니다.
- 알림 SPEC005·WP v8은 문서검수 PASS이며 v8 결과 계약의 현재 plan_digest 승인은 아직 회신 대기입니다. 이 코드에 알림목록·종배지·원장호출 발송을 완료했다고 포함하지 않습니다.

머지·배포·실업무DB migration·실키 사용은 실행하지 않았습니다.
