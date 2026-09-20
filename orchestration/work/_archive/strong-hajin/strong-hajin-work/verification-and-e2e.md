# W1 검증 및 사용자 E2E 인계

## 현재 상태

제품 구현 및 자동 검증 완료. 코드 최종 재검수2차 PASS. R1~4 해소, 마지막 R1a 문구는 코디가 실제 권한 분기와 대조하여 정정했다. E2E는 2026-09-16 사용자 지시에 따라 실행하지 않았다. 커밋·push·PR·배포 없음.

코드: /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work
브랜치: kknaksss/strong-hajin-work

## 실제 실행 증거

| 실행 주체 | 명령 | 결과 | 증거 |
|---|---|---|---|
| 코디 | PYTEST_XDIST_AUTO_NUM_WORKERS=4 make verify 중 test | 1297 passed | verify-r1-2026-09-16.log |
| 코디 | 같은 실행의 test-scale / test-release | 13 / 1 passed | 같은 로그 |
| 코디 | make test-postgres, ax_test_w1 | 65 passed, exit0 | postgres-r1-2026-09-16.log |
| 코디 | Node20.20.0 make frontend-test frontend-assets frontend-build | 645 passed, 자산9개 확인, 타입검사·빌드 통과, exit0 | frontend-final-node20-2026-09-16.log |
| BE 워커 | 마지막 문서/테스트 수정 관련 scoped contract | 84 passed, exit0 | backend-review-fix2-report.md |

단일 make verify 명령 전체가 exit0인 것은 아니다. 첫 실행은 자료 worker2 실패, 두 번째는 BE/scale/release 통과 후 Node25.5 localStorage 오류로 FE 실패. Node20.20.0에서 남은 FE/자산/빌드 타겟을 이어 실행해 전부 통과했다. 제품 코드·테스트 단언 변경 없이 환경을 맞춘 결과다.

## E2E 확인 목록 (사용자 수행)

1. 일반 구성원 → 업무 만들기 → 동료 담당 지정. 상대 내 업무에 즉시 표시·시작 가능, 상대 판단함에 수락 카드 없음.
2. 본인 업무 생성과 관리자 배정도 정상 생성. 보낸 목록 갱신과 assigned의 '즉시 배정됨' 표시.
3. 본인 시작일 입력 후 동료로 담당 전환: 시작일 입력 숨김·미전송 안내, 생성 성공. 본인으로 돌아오면 날짜 복원. 관리자 배정은 시작일 사용 가능.
4. 후보가 없는 계정은 담당 선택 숨김. 조직/권한 밖 재배정·수정은 거부.
5. 생성 중 연타·응답 유실 후 재시도는 한 건. 성공 후 같은 내용 새 생성은 별도 한 건.
6. 회의 후속 후보를 담당 지정 승격: 즉시 업무 생성, 원본 회의 출처 유지, 같은 후보 재승격은 중복 없음.
7. 요청 출신 업무 완료 보고→기존 요청자 확인 흐름 유지. AX 제안은 사용자 확인 전 생성 없음, 확인 후 한 건과 생성 출처 유지.

## 실행 환경 / 제한

- Node20.20.0 경로: /Users/kknaks/.nvm/versions/node/v20.20.0/bin. Node25.5에서는 현 테스트 환경 localStorage 오류가 재현됐다.
- 자료 worker의 3초 lease 시간 의존 테스트는 높은 CPU 부하에서 불안정. 병렬4는 이번 검증의 완화이며 영구 해결이 아니다.
- 새 DB 제약은 신규 격리 ax_test_w1에서 검증했다. 사용자 ax_demo는 변경하지 않았다. 기존 DB에서 바로 최신 스키마가 작동한다고 보장하지 않는다. E2E용 스택은 최신 코드·별도 DB로 준비해야 한다.
- W1만 구현. W2 완료 상태 개편·문의·전체 업무 페이지 재배치는 미구현.
- 기존 부채: meeting.followup.* 옛 AX 경로 오류(현재 todo 승격과 별개), 요청 판단 API의 제3자422/역량없음403/없는ID404 차이. 이번 W1에서 수정하지 않았다.
