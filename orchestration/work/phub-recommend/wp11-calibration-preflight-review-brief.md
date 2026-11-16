# WP-11 실제 보정 실험 전 검수

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 읽기 전용. SPEC-006 실제all-hold 보정계약/WORK-012, `wp11-calibration-review.md` R1/R2/R3 및 `wp11-calibration-prep-report.md`와 수정 fixture/semantic_candidate/calibration_prep를 대조한다. 전체613tests 보고, 코디 신규16PASS.
- 수정48의 R1조건F/R2contradicts/R3각claim시간한정·keyed라벨을 독립 확인하고 동일입력 반대라벨/명백 오라클 오류가 없는지 검수한다. 원본48/기존17 보존, 원문·context·scope·의무 lossless 투영, baseline 불변, 런타임 기본off/registry빈 유지.
- C24×baseline/candidate48 요청→사전6tuple(공통t=.50/.60/.70/.80/.90/.95)→오승인0중양성최대/동률높은t→candidate양성10/12·유효응답 선행→단일 tuple 봉인→미관측H24를 실제도구가 강제하는지, H재선정·정답모델입력·누락분모·재시도/최대72 우회가 없는지 확인한다. 상세score/원응답hash/실제모델/전송무결성 경계도 본다.
- 새 요구로 범위를 늘리지 말고 실행차단 P1/P2 재현만 `reference/2026-10-30-hub-evals/build-out/wp11-calibration-preflight-review.md`에 기록한다. 코드/라벨/정본/DB/서비스 변경·실제API/batch 금지. Orca worker_done 보고.
