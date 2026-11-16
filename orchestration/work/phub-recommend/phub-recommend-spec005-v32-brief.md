# 발주서 — SPEC-005 v3.2 · WORK-007: 응답 다이어트(A-1) · B 잔여 3종(A-2)

## 왜
rerun-v3(`build-out/rerun-report.md`) · 2차 분류(`build-out/fail-triage2.md`): case3 정확성 37→57% 올랐지만 허브 결과가 11.9KB→46.5KB(중앙 · p95 171KB · 최대 280KB)로 커졌고 C(허브가 줬는데 놓침)가 1.9%→6.6% · 크기 구간별 0%→10% 로 는다. B 는 186 남음 — 이웃 노드 안 펼침 51 · 기본 묶음 밖 섹션 33 · 섹션 매핑 밖 24 · 경로 안 닿음 13 · Jev 안 고름 12 · step8 메모 10 · 쌍 evidence 8 등(§3 표). 1차 재인용 점검(79%)과 실제 실행의 차이 = Claude · Jev 가 점검 때와 다른 도구 · 노드를 부름.

## 입력(읽기)
- `SPEC-005.md`(0.3.1) · `WORK-005.md` · `backend/build-out/work005-report.md`(SPEC 과 다른 곳 D-1~D-14 · 미닫힘 34 · 크기 손잡이) · `review-spec005-v3.1-report.md`
- `fail-triage2.md` §2 C 행 전부(응답 위치 · 크기) · §3 B 잔여 표 · §5 크기↔C · 부록 · `fail-triage2.json`
- `rerun-report.md` §2 바이트 · §3 나빠진 행 · `runs/runs.jsonl`(rerun-v3 trace: 실제 호출 패턴 — 어떤 도구 · 어떤 id · intent · sections)
- 허브 코드(읽기만) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`(c95b37a)

## SPEC-005 v3.2 에 넣을 것
1. **D-1~D-14 를 본문에 반영**(스펙 = 실물) · 미닫힘 34 처분 명시
2. **A-1 응답 다이어트**: 동봉(C1~C14)을 **질문의 부위 · 의도 · 요청 노드에 맞는 것만** — 부위 위험은 resolve 된 site 만 · 확인 조건은 질문 조건 · 의도 묶음 밖 섹션은 id 만 · 섹션별 fact 상한 · 「more_ids 로 더 받기」 규칙. 목표 **case3 경로 결과 중앙 ≤ 20KB · p95 ≤ 60KB** · 도구별 기본 응답 상한을 숫자로(2.5× 폐기 · 새 표). 어떤 fact 가 「바로 쓸 것」인지 `claude_contract` 에 우선순위 칸(질문 부위 · 의도 일치 순) — 허브에 LLM 없음 유지(규칙만)
3. **A-2 B 잔여**: 실제 호출 패턴(rerun-v3 trace) 기준으로 (a) 이웃 노드 51 — procedure_card · recommend 에서 금기 조건(check_condition) · 부위 위험 1-hop 을 어느 입력에 붙일지 규칙 (b) 기본 묶음 밖 섹션 33 + Jev 안 고름 12 — 의도 묶음 보강 또는 id 노출 (c) 섹션 매핑 밖 24 — fact id 전부 열거해 매핑 (d) step8 메모 10 · 쌍 evidence 8 · 엣지 속성 6 · 경로 안 닿음 13(허브 안 부름 10 제외) — 조항 또는 「닫지 않는 행」 명시. B 186 ↔ 조항 1:1 표 필수
4. **끝 조건**: (i) rerun-v3 실제 호출 묶음(676) 재실행 recheck — 조항이 닿는 행 ≥ 90% (ii) 크기 목표 (iii) C 행 18 중 C3(동봉 밖) 8 이 기본 응답에 들어옴 (iv) 품질 6/6 · 106/106 · 회귀 0 · 결정론 · 시험 — 그 뒤 실패 문항 재실행은 코디

## WORK-007
WP 로(다이어트 / 동봉 규칙 / 섹션 매핑 / 메모 · 쌍 / 측정) · WP 마다 시험 · 코드 표면 grep 전부.

## 제약
스펙 문서만 · 실버 · 시맨틱 수정 없음(A 54 는 9단계) · 원장 인용 본문 금지 · 열린 것 §7 · 끝나면 worker_done(바뀐 조항 · B 186 ↔ 조항 대응 수 · 아직 안 정한 것).
