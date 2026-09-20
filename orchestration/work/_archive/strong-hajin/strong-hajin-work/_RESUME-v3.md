# strong-hajin-work — 다음 세션 재개점

작성: 2026-09-20

## 현재 기준

- 문서/코디 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin`
- 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
- 이번 세션은 커밋·push·PR 없이 종료했다.
- 작업 워커와 검수 워커 터미널은 모두 종료했다. 로컬 Vite/API 터미널과 코디네이터 터미널만 유지한다.

## 완료된 기능

### 백엔드

- 요청 자료 REST 5종을 `request_id` 기반 2단계 계약으로 구현했다.
- 기존 `attachments`/`attachment_bindings`를 `context_type=work_request`로 재사용한다.
- 요청 수락 시 요청 binding을 보존하고 같은 attachment에 task binding을 추가한다.
- 요청 projection, 회의 승격 공통 필드, CC 후보 capability를 구현했다.
- AX가 요청 자료를 evidence로 잘못 보내던 inventory 매핑은 E2 `excluded`로 정정했다.
- 링크 자료가 레거시 다운로드에서 500이 되던 경로는 기존 422 오류로 정정했다.

### 프론트

- 일반 업무 요청 생성 후 반환된 `request_id`로 파일·링크 자료를 업로드한다.
- 성공한 자료는 중복 업로드하지 않고 실패한 항목만 재시도한다.
- 생성 payload에 `material_ids`, `attachments`, `material_draft_ids`를 추가하지 않았다.
- `REQUEST_MATERIALS_SAVED=false`의 일반 요청 경고를 제거했다.
- 회의록 승격은 응답에 `request_id`가 없어 자료 연결을 보류한다. 사용자 결정으로 다음 범위에서 처리한다.

## 검증 결과

- FE: `CreateWorkAttach` 13 passed, `CreateWorkLayout` 29 passed, `npx tsc --noEmit` exit 0.
- BE 자료 수정: 집중 회귀 2 passed, inventory drift guard 4 passed.
- BE contract 감사: 단독 4/4, 두 파일 순차 20/20 통과.
- `-n auto --dist worksteal` 5회는 3·4·4·3·5 failed. `-n 2/-n 4`는 20/20, `-n 8`은 2 failed.
  실패는 CPU 과다 병렬로 추출 워커가 lease/time budget을 놓치는 현상으로 좁혀졌다. 해당 테스트 setup에는 work request가 없어 요청 자료 코드가 실행되지 않는다.
- 기준 브랜치 baseline 비교는 하지 않았으므로 “기존부터 동일했다”고 단정하지 않는다.
- 전체 `make verify`, 브라우저 E2E, 회의록 승격 자료 연결은 미실행/미완료다.

## 다음 세션에서 할 일

1. 사용자가 요청할 때만 contract 실행 병렬도(`-n 4` 등)를 CI/Makefile에 반영할지 결정한다. 테스트 코드 임의 수정 금지.
2. 회의록 승격 자료가 필요해질 때 promote 응답에 `request_id`를 추가하고 FE 자료 연결을 별도 발주한다.
3. 그 외 범위는 새 사용자 지시 없이는 확장하지 않는다.

## 주요 보고서

- `orchestration/work/strong-hajin-work/be-contract-failure-audit.md`
- `orchestration/work/strong-hajin-work/review-fe-materials-report.md`
- `orchestration/work/strong-hajin-work/review-be-fix-report.md`
