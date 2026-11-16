# [reviewer_doc] 서류 마감 검수 — 짧은 읽기 전용 검수

역할은 /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/reviewer_doc/role.md 및 같은폴더 규칙. code나서류 수정 금지. 읽을 최신 원천은 spec worktree /Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/60-release/app-store-preparation.md, profile work/prod-deploy-re1/mobile-paperwork-report.md와 mobile-description-final.txt, code worktree app/README.md와 필요한 최소 코드만이다. 사용자 제품정체성은 기존 병원EMR 조회/상태변경 직원앱, 새 업무콘텐츠는 채팅. DAY 동기사본과 세션/푸시기술정보는 별도로 정확히 기록.

사용자는 지원메일 및 심사연락처 제공, 데모자격은 직접입력, 운영주체/보관삭제는 권장안으로 서류준비 위임. 오늘 추가빌드/업로드/테스터배포/심사제출금지. 현재 ASC 연락처(App Review/Beta Review)·TestFlight 앱설명/지원피드백메일/한국어테스트안내는 코디가 API반영·GET확인. 개인심사 이름/폰/메일을 공개문서에 복사하면 안 됨. 값은 ~/.config/day/apple/store-contact.local.json 읽어 일치 여부만 확인할 수 있고 보고에 값출력금지. 공개지원메일만 허용.

검수 초점:
1. 기존EMR원본/동기사본/새채팅/기술정보구분, 신규진료수집앱·서버저장0 같은과장0.
2. 보관·파기권장운영방침과현재softdelete 실제동작 구분, 자동파기/법무완료허위주장0.
3. 공개지원메일반영, 심사개인연락처노출0, 데모자격빈칸유지, 시행예정일은미래계획으로명시.
4. 5-3심사노트의 데모로그인성공서술은 조건부템플릿이고 확인전제출금지가명확한지.
5. 남은T1-T6공개전확인은고지돼있는지. 오늘목표서류준비를전체공개/심사준비완료로혼동하지않는지.
6. 코디의 좁은문안검토: 'DAY는 비밀번호를 저장하지 않는다'는 일반로그인입력비밀번호로범위를좁히는편이정확(서버의KOS시스템자격보관과혼동방지). 최종앱설명의 '새진료기록앱이나환자용앱이아닙니다'같은부정대비문은제거해도정체성이앞문장에충분히드러남. 실제문제/보강권고로판정.

필요한최소확인만하고법률/공급자대규모조사·추가워커·테스트재실행금지. 이미근거있는초안인지검수, 실제파기구현미완이라고서류자체를FAIL로판정하지말고은폐여부로판정.

산출물 딱1개: /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-paperwork-review.md. PASS/WARN/FAIL과근거파일:줄. 서류수정불가. commit/push/PR/API변경금지. 완료는dispatchpreamble worker_done --outcome succeeded, 코디terminal알림. 한국어 간결하게.
