# 알림v8 승인·이슈반영

사용자 「응 진행하고 구현하는동안 우리 ios 개발용 푸쉬 알림 받을까 ?」로 v8 승인. delivery-v8-plan-approval.json에 current plan_digest4b1a7c2f 결속. CLI 승인결과 delivery-v8-approved-result.json = plan-approved / executionready / baselinepending.

자동 렌더 본문281795자로 GitHub GraphQL Body is too long 재현. 원래CLI scope-delta comment 생성은 됐지만 본문은v7에남아 approvalCLI가 contract_changed conflict를 반환했다. 코드/도구를 수정하지 않고 profile의 delivery-request-v8-execution.json으로 이미완료된v1~7과거실행서술만 정리했다(결과계약 필드/contractdigest/plan_digest완전동일). 기존 parser가 읽을수있게 metadata값의percentencodedUnicode를rawUnicode로만 표현하고 의미있는 %,>,--,newline만encode해 exactparser동일성assert. 인간본문은v8요약/Spec/PR링크로 간추림. delivery-v8-compact-body.md 52929자로 실제gh issue edit 성공. _issue_blocks(compactbody)==(검수받은동일contract,정리한execution) 검증. 이후 CLI로 실제 승인receipt댓글과approvedlabels생성 성공. 범위재승인없이format/Execution만정정. API작업실키사용0.

발주는 notification-backend-code-brief.md / notification-mobile-code-brief.md. 기존 sourcehead3aaa9780에서영역분담, 같은PR237, merge0. Apple API키발급과APNs키는별도임을공식문서근거로사용자안내, 아직실키경로/실서명승인정보없음. 코드구현은키와독립진행.
