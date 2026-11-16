# [reviewer_code] Hub·앱 격리 연결 관문 확인

너는 read-only 통합 검증 워커다. Orca dispatch preamble 완료 보고를 따른다. Hub worktree `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` 기준 HEAD `2edc190` + 현재 미커밋 코드, 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 기준 HEAD `078ac99` + 현재 미커밋 코드, 프로필 레포 `orchestration/work/phub-recommend/WORK-011-public-contract-handoff.md`와 `WORK-012.md`를 읽는다.

실물 Gold 입력을 격리 메모리/inprocess에서 로드해 공개 REST `pairs/selected`·`global-claims`의 build hash, status, cursor, 출처/인용 자격을 확인하고, 앱 REST client/관계 어댑터가 같은 응답을 해석하는지 연결 시험한다. 가능하면 기존 테스트 인프라의 ASGI transport를 사용한다. 앱 코드가 다른 워커에 의해 수정 중이므로 읽기 전용으로만 관찰하고 최종 HEAD/파일 시각을 기록한다. 실제 사용자 서버 `127.0.0.1:18005`, procedure-* 컨테이너·포트·DB를 조작하지 않는다. 새 서버가 필요하면 우선 inprocess로 하고, 별도 임시 포트 없이 해결할 수 없으면 사유만 보고한다.

Q018/R8-0163, Q064/R8-0075, Q139/R8-0218·0219와 전역 메모, Q173/R8-0111을 각 실제 확정 pair·source로 조회해 원문/ID와 앱 전달 가능 여부를 기록한다. 이는 모델 답 평가가 아니며 QID 원문을 찾을 수 없으면 추정하지 않는다. 같은 build hash 두 번의 ID·순서·본문·상태·직렬화 크기 결정을 대조한다.

보고 파일은 프로필 레포 `orchestration/work/phub-recommend/isolated-hub-app-integration-report.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 격리 시험·read-only 호출만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
