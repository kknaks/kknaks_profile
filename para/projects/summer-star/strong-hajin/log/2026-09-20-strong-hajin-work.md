# 작업 요약 — strong-hajin-work (strong-hajin)

기간: `2026-09-15` ~ `2026-09-20`
결과: 업무·요청 생성 프레임과 요청 자료 계약을 구현·검수하고, 다음 세션 재개용 코드 스냅샷을 보존한 뒤 작업 문서를 아카이브한다.

## 1. 무엇을 했나

업무/요청 생성 모달을 공통 탭 프레임과 갈래별 기본정보로 정리했다.
참조 읽음 처리, 상위·선행 업무, 결재자, 요청 자료 REST 계약과 요청 자료의 수락 시 업무 바인딩을 구현했다.
프론트는 요청 자료 파일·링크를 생성 후 반환된 request_id로 연결하도록 맞췄다.
계약 검수와 병렬 테스트 실패 원인 조사를 마쳤고, 회의 승격 자료 전파는 후속 범위로 남겼다.

## 2. 적용한 기술·개념

- **2단계 자료 바인딩** — 요청 생성과 자료 업로드를 분리하고 `work_request` 바인딩을 수락 시 `task`에 추가했다.
  - 왜 이걸 골랐나: 생성 payload에 임의 자료 필드를 넣으면 `extra=forbid` 계약을 깨므로 기존 attachments 계약을 확장했다.
  - 무엇이 어려웠나: 요청은 수락 전 활성 담당자가 없어 업무 자료 endpoint를 재사용할 수 없었다.
  - 근거: `backend/src/ax_workspace/modules/work/requests.py` · `backend/src/ax_workspace/modules/work/materials.py` · `work003-request-materials-be-report.md`
- **선행 업무 finish-to-start 게이트** — 프로젝트 범위의 predecessor 관계와 순환·미완료 검사를 한 전이 판정에 통합했다.
  - 왜 이걸 골랐나: 시작과 완료 우회 경로 모두 같은 계약으로 차단해야 했다.
  - 근거: `backend/src/ax_workspace/modules/work/lifecycle.py` · `backend/tests/unit/test_task_predecessor_gate.py`
- **참조 읽음 영수증** — `(work_request_id, member_id)` 멱등 영수증으로 수신함 reference 항목만 숨겼다.
  - 근거: `backend/tests/contract/test_reference_read_receipt.py` · `_RESUME-v3.md`
- **보존 스냅샷** — 커밋 `69b27c48f4e3213b04d9c2d7747e0cd68f7762e0`을 태그/브랜치 `archive/strong-hajin-work-2026-09-20`으로 보존했다.
  - 왜 이걸 골랐나: dirty 워크트리를 폐기하지 않고 아카이브 안전검사를 통과시키기 위해서다.

## 3. 막혔던 것 / 사고

- 요청 자료 endpoint가 없다는 사실을 뒤늦게 확인해 댓글 첨부 우회안을 폐기하고 정식 REST 5종으로 전환했다.
- 계약 테스트 4건은 코드 결함이 아니라 `-n auto` CPU 과다구독으로 재현됐고, 낮은 병렬도에서는 통과했다.
- 코드 워크트리 dirty 상태로 archive script가 중단됐으나, 로컬 보존 커밋과 별도 태그를 만든 뒤 기준 브랜치로 되돌려 안전하게 아카이브했다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-19 | 업무·요청은 공통 생성 탭 프레임을 사용 | 사용자 확정 와이어프레임 |
| 2026-09-20 | 요청 자료는 별도 REST 5종과 2단계 업로드로 구현 | 기존 자료 저장 모델과 `extra=forbid` 입력 계약 보존 |
| 2026-09-20 | 회의 승격 자료 전파는 후속 범위로 둠 | 회의록 기능을 나중에 추가하기로 한 사용자 지시 |
| 2026-09-20 | 코드 변경은 로컬 보존 태그만 만들고 push하지 않음 | 다음 세션 재개를 위해 변경 보존 |

## 5. 날짜별 로그

- `2026-09-15~19` 문서·스펙·업무 생성 프레임과 BE/FE 구현·검수
- `2026-09-20` 요청 자료 API, FE 연결, 병렬 테스트 원인 조사, 워커 종료 및 아카이브 준비

## 6. 산출물

- spec PR: 없음
- code PR: 없음
- 보존 커밋: `69b27c4` (push 없음)
- 리포트: `_RESUME-v3.md` · `review-be-api-gap-report.md` · `review-be-fix-report.md` · `review-fe-materials-report.md` · `be-contract-failure-audit.md`

## 7. 잔여

- 회의 승격 경로의 시작일·참조자·결재자·자료 전파는 회의록 기능 착수 때 구현한다.
- 병렬도 과다구독 테스트 안정화는 별도 테스트 인프라 작업으로 분리한다.
- 다음 세션에서 `archive/strong-hajin-work-2026-09-20` 태그 또는 브랜치로 코드 워크트리를 재생성한다.

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/strong-hajin/strong-hajin-work/README|strong-hajin-work]]
<!-- work-links:end -->
