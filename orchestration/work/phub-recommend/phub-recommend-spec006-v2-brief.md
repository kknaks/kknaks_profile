# 발주서 — SPEC-006 v2 · WORK-006: 실험 앱 case2 공정성(B-1)

## 왜
2차 분류 `reference/2026-10-30-hub-evals/build-out/fail-triage2.md` §2 · §5: Claude CLI(`claude -p --tools ""`)가 MCP 도구 결과를 약 1.8~2.2KB 에서 잘라 모델에 넘긴다(614호출 중 100 · 허브 응답 중앙 88KB vs 모델이 받은 중앙 1.8KB). case2 실패 131행 중 56행이 잘린 호출 문항. 또 Claude 가 `intent` 를 넘긴 호출 14/662(2.1%). case2 수치가 허브 품질이 아니라 실험 장치 때문에 낮다.

## 입력(읽기)
- `SPEC-006.md` · `WORK-004.md` · `cli-provider-report.md`(「SPEC-006 과 다른 점」 목록 — 이번에 본문 반영) · `cli-research.md`
- 앱 코드 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`(읽기만 · 수정 금지) — `clinic_chat/llm/cli.py` · `cases/case2.py` · MCP 설정 · 기록 trace 필드
- 실물 확인(조사 포함): Claude CLI 가 큰 도구 결과를 자르는 규칙 · 한도를 올리는 설정(env · 플래그)이 있는지 · Codex CLI 도 같은지 — `claude --help` · 문서 · 실험 1회(실물 호출은 코디 승인 뒤 — 이번엔 **설정 조사까지만**, 호출은 WORK 에 「확인 시험」으로)
- `fail-triage2.md` §5 잘린 호출 도구별 분포(check_conditions 47 · procedure_card 23 · pair_check 17 · compare 7 · recommend 6)

## SPEC-006 v2 에 넣을 것
1. **도구 결과 전달 보장**: 모델이 허브 응답 전체를 받는다 — 후보 (a) CLI 한도 설정 (b) 앱 쪽 MCP 프록시가 결과를 모델이 읽을 수 있는 크기로 나누어 이어 주기(후속 호출 `page=`) (c) 모델에 Read 도구 허용(파일 미리보기 경로) — 실물 조사 결과로 하나 고르고 나머지는 「아직 안 정한 것」 아님(근거로 닫기). Codex 도 같은 보장. 기록에 `delivered_bytes` · `truncated` 칸(이미 있으면 정의만)
2. **intent 전달**: MCP 도구 설명 · 스키마에 `intent`(I-01~I-12) 를 「반드시 넘김 · 의도 표」로 · 시스템 프롬프트 한 줄 — case3 와 같은 조건이 되게. 넘긴 비율을 기록 · 보고서 칸으로
3. **공정성 원칙 조항**: 세 케이스가 받는 허브 바이트 상한 · 전달 보장은 같게(CLI 판 · SDK 판 둘 다) · 10-30 결정(입력 상한 CLI 판 셋 다 없음)을 이 원칙으로 정리
4. 「SPEC-006 과 다른 점」(provider 층 · effort medium · ttft_kind · 채점 열마다 절대 · 직렬 없음 · CLI 단계 정의 · 입력 상한) 을 v2 본문으로
5. **끝 조건**: case2 182문항(또는 실패 문항) 재실행에서 잘린 호출 0 · intent 전달 ≥ 95% · 기록 검증 스크립트(결정론) · 기존 시험 전부

## WORK-006
WP: 조사 확인 시험 → 전달 보장 구현 → intent → 기록 · 검증 스크립트 → case2 재실행(코디 발주). 코드 표면 = grep 전부.

## 제약
스펙 문서만 · 공개 레포라 원장 인용 본문 금지 · 열린 것은 §7 · 끝나면 worker_done(바뀐 조항 · 고른 전달 방식과 근거 · 아직 안 정한 것).
