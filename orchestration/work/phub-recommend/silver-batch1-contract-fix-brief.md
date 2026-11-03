# 첫 이관 계약 CR-H1/H2/H3/M1 최소 보완

사용자승인 계획 단계4 구현선행 계약 보완이다. silver-batch1-contract-review/report.md의4 findings를 해결한다. DATA-001/WORK-013·silver-data-contract-batch1/field-contract.json과 input manifest를 실제 원천/문서에 일치시키고 재검증한다. 후보 이관 구현·정본데이터·임상판정은 이번범위아니다.

## 보완결정

1. CR-H1: 변경되는 _RESUME.md를 builder의 직접 물리입력에서 제거한다. 이전 manifest판을 별도immutable 증거로 보존한다. 현재 _RESUME의 정확한 bytes를 이번 허용폴더 frozen-inputs/에 복사하고 고정 locator/domain/logical key/hash로 새 manifest판을 발급한다. 이전원본bytes를 갖고있다고 허위주장하지 않는다. 이전expected hash·현재hash·미확보원본 사실, 실제 계약에서 인용하는 family.name_basis 등 문맥을 원천/결정/현재값에 대조한 reconciliation을 명시한다. **코디는 원문·데이터를 바꾸지 않는 현재판 진행기록 snapshot의 입력채택을 승인**하며 기록수정은 계속할수있지만 frozen입력은 불변이다. 이름·임상사실 변경근거로 로그를 단독사용하지 않는다. 실제 결정대조로 닫히지 않으면 ask한다.
2. CR-H2: design/coverage/HTML 등 감사전용 아티팩트는 데이터source collection과 다른 audit collection/domain으로 분리한다. semantic source snapshot ID에 감사파일hash가 전파되지 않게 한다. 감사manifest 자체의 hash보호와 basis링크는 유지한다. fixed membership·logical key·각collection 공식·필드transform을 명시한다. source자료 변경이면 ID변경, audit-only 변경이면 unchanged-data occurrence/normalized ID불변을 수식/메모리시험으로 확인한다. source_ref를 ID payload에서 몰래제거하지 않는다.
3. CR-H3: 모든 safety원문claim은 보존하지만 attachment는 검증된단일owner가 있을때만 생성한다. subject=null/후보/이번범위밖 entity는 attachment 미생성 사유와 mapping/source-row-index로 기록하며 분모를 별도계산한다. 새owner나 package/unit 적용을 발명하지않는다. 실제56candidate/ownerless rows의132safetyfield를 확인하여 이관기 정상positive와 zero-loss coverage규칙을 계약에 포함한다. 단일owner도 clinical승인과는별개이다.
4. CR-M1: collection snapshot의 source_kind는 collection역할이며 heterogeneous파일별원천종류/실제version은 files[] meta로 보존한다. collection source_version은 별도명시판이없으면 null+reason. file단위missing/null/type 원형보존을 정의한다. 임의파일하나version을 collection전체판으로쓰지않는다. 원문snapshot과generated/research/decision/audit를분리하고 membership을새manifest로명시한다.

## 작성·검증

허용 DATA-001.md/WORK-013.md/field-contract.json 및 silver-data-contract-batch1/ 아래 **새**contract-fix/ 디렉터리(구manifest복사·reconciliation·frozen-inputs·새manifest·검증script/results·report.md)만이다. 기존문서검수report/results와 기존input-manifest는 증거로보존하고 새manifest경로를 WORK/field-contract에서명시한다. 과거보고를새PASS로소급갱신하지않는다. 원장/실버/decisions/apply/스킬/semantic/HTML/design/pilot/기존리뷰/앱·Hub/env/DB/서버/네트워크/모델/설치/하위worker/commit/push/PR금지.

4finding별문서/field/manifest일치·전체member counts·실제input hashes·원문/계열name_basis근거·ownerlessfield coverage·ID공식 반례·file/source_version positive를독립검사한다. 84필드/247baseline을보존하고 scope밖실적0을유지한다. 다음worker가새manifest로P0통과가능한지확인하고CR4건의폐쇄근거와수정전후/한계/고정hash를report에쓴다. 임상unknown과needs_design은유지한다.

live Orca preamble의inbox/heartbeat처리, 완료시세문장요약·report-path/files-modified로worker_done한번후멈춘다.
