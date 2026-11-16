# WP-11 C→고정선택→H 실제 실행기 준비

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`와 준비 artifacts를 읽기만 사용. `wp11-calibration-preflight-review.md`의 라벨/투영 PASS와 P1/P2 실행 경계를 반영한 build-out 실행기 한 파일 및 offline 자가검사만 작성한다. 앱/정본/라벨/registry/서버/DB 변경 금지.
- 실행기는 기존 Settings/SDK로 실제 jev1.14.0 state/questions/model만 전송, retry0·최대72물리시도·동일사례 재호출없음·입력hash/wire대조/인증비노출을 강제한다. raw HTTP JSON→SDK parsed choices/nouls/model/usage 동일성, raw SHA/타임스탬프/유한nonnegative latency를 검증해 오류 응답은 C선정 근거가 될 수 없게 한다. fake/oracle은 실제실행 결과와 구분한다.
- C48 actual 증거를 exclusive 파일로 고정→cp.select로 재계산한 단일 tuple을 H 호출 전에 동결. H실행은 같은 메모리의 선택과 원래 C raw/hash 재계산 결과가 일치할 때만 허용한다. C증거 없는/재hash변경 selection 거부. exclusive stage ledger에 experiment/preflight/C/selection/H-started/H-completed hash·시각·시도수를 저장하며 같은 실험 H재실행/문턱재선택/다른출력명 우회 금지. 로컬 전체파일을 악의적으로 다시 쓰는 공격까지 방어하는 보안제품으로 확대하지 말고 정상 실행 경로의 순서/무결성을 증명한다.
- reviewer 메모리 위조선택·t변경재hash·C누락·raw다른모델/빈응답/잘못SHA/nullusage/음수latency·retry/상한·H재호출을 offline 자가검사로 거부한다. 기존6grid/tie/양성10/12/오승인0·candidate C실패시 H미개방을 유지한다. 정답은 scorer전용, model payload에 넣지 않는다.
- **실제 API를 아직 호출하지 말고**, 코드 경로·self-test 결과·실행manifest hashes를 만들어 Orca ask로 코디에게 점검 요청한다. 코디의 실행 답변 후에만 승인된 C48→조건충족시H24 실제 평가를 한 번 진행할 수 있다. 질문/정답/prompt/grid 변경·API 재시도/추가평가 금지. 실제 실행 후 immutable raw/score/ledger와 `reference/2026-10-30-hub-evals/build-out/wp11-calibration-execution-report.md`에 기록, policy등록/기능활성화/Q002실행은 하지 않는다.
