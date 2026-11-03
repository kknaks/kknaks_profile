# 발주서 — hub-evals 실패 전수 분류(읽기 전용 조사 · 코드 · 데이터 수정 금지)

## 목적
239문항 실행에서 골드(case2 · case3)가 실패한 건을 **「왜 놓쳤나」로 결정론 분류**한다. 결과로 고칠 곳(허브 응답 설계 / 실버·골드 데이터 / 답변 프롬프트)을 나눈다.

## 입력(모두 읽기만)
- 채점 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-30-hub-evals/runs/quality.jsonl`
  — 행마다 `run_id · case · question_no · judge.failures[]{item, claim, evidence{file, path, quote}, status}` (status valid 만 센다)
- 답 기록 `…/runs/runs.jsonl` — `cases.<case>.trace`(case2 도구 호출 · 결과, case3 hub 경로 · jev 슬롯 · 허브 결과) · `answer`
- 보고서 `…/reference/2026-10-30-hub-evals/build-out/fullrun-report.md`(사유 키워드 분류는 참고만 · 정본 아님)
- 골드 내보내기 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json` + 허브 REST(18005 떠 있음 · 호출만 · 서버 손대지 말 것)
- 원장(RAW_DIR) · 실버 json — evidence.path 가 가리키는 원문 확인용

## 분류(실패 건 1개 = 행 1개 · 전부)
evidence.quote(원장 원문)를 기준으로:
- **A 골드에 없음** — gold-export 에 그 사실(노드 · fact · 엣지 속성)이 없다. → 원장 파일 · 필드 경로(`extracted.M9.contraindications.relative`, `complications.*.management` 등) 단위로 묶어 센다 — 어느 원천 영역이 실버에 안 올라왔는지
- **B 골드에 있는데 허브 응답에 없음** — 골드엔 있지만 그 질문에서 허브가 실제로 돌려준 결과(trace 의 도구 결과)에 없다. → 어느 칸이라 빠졌나(slim 카드 밖 섹션 / recommend 상한 / pair_check 안 부름 / 의도 경로가 그 도구를 안 탐)로 다시 나눔
- **C 허브 응답에 있는데 답이 놓침** — trace 결과엔 있는데 Claude 답이 「정보 없음」이라 함 → 프롬프트 · 모델 문제
- **D 채점 오류** — evidence 가 원장과 안 맞거나 claim 이 틀림(있으면)
- case3 는 B 안에서 「Jev 가 섹션을 안 골라서(상위 4 밖)」를 따로 센다.
판정은 **문자열 · 구조 대조**로(정규화 뒤 포함 여부 · fact id 대조). LLM 판단 금지. 애매하면 「미분류」로 두고 사유 적기.

## 산출 `…/reference/2026-10-30-hub-evals/build-out/fail-triage.md` + `fail-triage.json`
1. 전체 표: 케이스 × 항목 × A/B/C/D 건수 · 문항 수
2. A: 원장 파일 · 필드별 건수 내림차순 + 예 1개씩
3. B: 빠진 칸별 건수 + 의도(I-xx)별 분포 + 예
4. C: 문항 번호 목록 + 예
5. 「빠진 연결」 · 「엉뚱한 시술」 사유(보고서 3절)는 A/B 와 별도로 **그래프 문제** 칸: 어느 엣지 · 계열이 틀렸거나 없는지 노드 id 로
6. 오류 15건(case3 family id → checks 400)은 집계만
7. 결론 금지 — 고칠 안은 쓰지 말 것. 숫자와 예만.
전부 레포 밖(build-out · gitignore 됨) · 커밋 없음 · 원장 인용은 파일 안에만. 끝나면 worker_done(경로 + 표 1 요약).
