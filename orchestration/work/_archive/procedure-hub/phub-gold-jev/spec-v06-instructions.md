# SPEC-002(+ 필요하면 SPEC-001) 0.6 — 37 batch 결과로 B 원인 4 · 키 범위 · 되적기

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · allowed_paths(이번엔 **SPEC-001 · SPEC-002 두 파일만**) · 제약(공개 레포 · 외부 API · .env · 코드 레포 변경 금지) · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값). **디스크 여유 2~3GB — 큰 파일 만들지 마라.**

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만)

## 읽을 것

1. `$W/_RESUME.md` §2 맨 위 행 「테스트 답은 빠짐없이」 부터 11-17 행 전부 ← 정본
2. `$W/batch-v052-summary.md` 전체 · 보고서 `$A/runs/reports/20261117-115258-v052-37-a7df.md` · 각 문항 trace(`$A/runs/runs.jsonl` 의 batch `20261117-115258-v052-37-a7df` 줄) · 채점 `$A/runs/quality.jsonl`
3. 0.6 되적기 후보: `$W/app-v052-report.md` 「코디 확인 · 되적기 후보」 · `$W/app-v052-fix1-report.md` · `$W/review-code-v052-app.md` · `$W/impl-v052-hub-report.md` 미결(W-2 수 129 · 1,700 등)

## 할 것

**A. B 원인 넷 — 일반 규칙으로(문항 맞춤 금지)**. 원인마다 trace 근거(run id · 수) · 규칙 · 시험 기준(T/E 번호):
- **A1 답이 목록을 줄임**(Q01 · Q08 · Q10 · Q11 · Q35 — 다 읽었는데 답에서 빠짐 · 재료 70~250KB): 사용자 결정 「테스트 답은 빠짐없이 — 계열별로 묶어 이름만이라도 전부」 를 답 프롬프트 원칙 · 재료 꼴(§3-2a 묶음 · 이름 목록)로. LLM 입력을 늘리지 않는 쪽 우선(이름 목록만 · 칸은 정한 대로). 검사: 답에 안 나온 키 코드(D3) 기준. 프롬프트 문구 자체는 사용자 확인 C-1 그대로(원칙만).
- **A2 종류가 offered 에서 멈춤**(Q03 · Q05 · Q18): KD 규칙 어디서 read 로 안 넘어가는지 · 기대 종류가 빠지지 않는 규칙.
- **A3 combo 깊이 · required 미충족 → 후보 소진 / 원천 미확정 잘못 닫음**(Q15 · Q18 · Q37).
- **A4 입구 놓침**(Q13 · Q33).
- Q24 · Q21(종료 상태를 ② 가 미확정으로 읽음)도 원인 한 줄.

**B. 키 범위**: Q03 · Q05 · Q12 는 세 열 모두 빠짐 90% 안팎 — 키가 기대하는 「답에 나와야 할 코드」 의 범위가 답 꼴(「테스트 답은 빠짐없이」)로도 닿을 수 있는지. 닿을 수 없으면 D3 의 셈 단위(예: 이름 목록 수준 · 계열 묶음)를 어떻게 둘지 제안 + 사용자 결정 목록으로.

**C. 되적기**: 위 3 의 후보 전부(expected_kinds_by_entry · 덮인 조각 규칙 · W-1 필터 입구 매칭 · W-3 · W-4 · end_state counted_rows · HG1 「한 단 9 · 두 단 4」 셈 · Q12 키 +4 · 수 129/1,700).

version 0.6.0 · 변경 기록 · 열린 것 표 상태 칸 · **WORK 전 사용자 결정 목록**(추천 붙임 — 최소로).

## 검증

- 원인 넷 각각 trace 근거 표(run id · 수 — 회사 데이터 본문 0) · 결정 행 → 문서:줄 표 · 공개 grep.
