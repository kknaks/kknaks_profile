# 발주서 — 실패 문항 재실행(허브 v3 빌드 d3a1abd52f70afe9) · 전후 비교 보고

## 배경
허브가 SPEC-005 v3.1 로 바뀌었고 18005 가 새 빌드(health build_hash `d3a1abd52f70afe9`)로 떠 있다. 도구들이 `intent`(I-01~I-12 · 선택) 를 받아 의도별 섹션 묶음 · 동봉을 기본으로 붙인다. check_conditions 는 family/product id 를 펼친다(10-30 오류 15 원인). 10-30 전체 실행 기록(gold `e9d30ace`)은 **그대로 두고** 그 위에 재실행을 쌓아 전후를 비교한다.

## 1. 앱 최소 변경(코드 · 로컬 커밋 · push 금지)
- case3: 허브 호출마다 Jev 의도 id 를 `intent` 로 넘긴다(recommend · procedure_card · pair_check · check_conditions · compare · combos — 쓰는 곳 전부 grep). Jev 의 sections 선택은 그대로(허브 기본 묶음과 합집합).
- case2: MCP 도구 스키마에 `intent` 가 노출되는지 확인만(앱 변경 없음 · Claude 가 쓰든 말든 기록).
- 기록의 `gold` 칸이 서버 health 의 build_hash 를 그대로 담는지 확인(e9d30ace → d3a1abd5).
- 화면 「질문 기록」: limit 100 → 전체 + 번호(Qnnn) 검색 칸(사용자 지적 10-31). 작게.
- 시험 · ruff · 18210 재시작(일괄 시작 전).

## 2. 재실행
- 대상 `reference/2026-10-30-hub-evals/build-out/rerun-questions.txt`(182문항 = 10-30 에 case2·case3 채점 실패 있던 문항 + 오류 15 합집합).
- 조건은 10-30 과 같게: claude-cli Sonnet effort medium · 세 케이스 · Opus 열마다 절대 채점 자동 · 순차 · 간격 15초 · 재시도 2 · caffeinate · 30분마다 진행 줄.
- 일괄 라벨 `rerun-v3` · 기록 그대로 추가(아카이브 금지).

## 3. 보고서 `build-out/rerun-report.md`(+json · 레포 밖)
- 문항 × 케이스 전후 표(채점 항목별 통과/실패 · 통과 수 전후 · Δ) — 전 = 10-30 기록(gold e9d30ace) · 후 = rerun-v3
- 케이스별 항목 통과율 전후(분모는 182문항 · 239 환산도 같이) · 「정보 없음」류 답 수 전후 · 오류 수 전후
- 시간(첫 글자 · 전체 중앙값) 전후 · 허브 결과 바이트 중앙값 전후(trace)
- **나빠진 문항**(전 통과 → 후 실패) 따로 · Opus 주장 인용
- 남은 실패를 fail-triage 사유(A/B/C)로 다시 묶기는 하지 말 것(코디가 recheck 와 맞춰 봄) — Opus 주장 · 근거 경로만 그대로 표에
- 결론 · 고칠 안 쓰지 말 것 — 숫자와 예만

## 제약
공개 레포: 키 · 원장 · 골드 · runs · 사용자 홈 경로 커밋 금지 · 허브 18005 손대지 말 것(죽어 있으면 멈추고 ask) · 사용자 포트 · procedure-* 컨테이너 손대지 않음. 끝나면 worker_done(보고서 경로 + 전후 통과율 표).
