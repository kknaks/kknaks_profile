# SPEC-001 · SPEC-002 0.5.2 — 되적기 + 허브 구멍 3 규칙

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · allowed_paths(이번엔 **SPEC-001 · SPEC-002 두 파일만**) · 제약(공개 레포 · 외부 API · .env · 코드 레포 변경 금지) · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev` · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(읽기만)

## 읽을 것

1. `$W/_RESUME.md` §1 e2e 4 · 5 · 「허브 묶음 발주」 줄 · §2 맨 위 두 행(2026-11-17 답 키 검토 · v05 앱 검수 뒤 W-1~W-4) ← 정본
2. `$W/app-key-fix1-report.md` 전체(특히 「코디 요청 셈」 · 미결 2 · 3 · 4)
3. `$W/review-code-v05-hub.md` · `$W/review-code-v05-app.md` · `$W/WORK-005-hub-v05.md` · `$W/WORK-006-app-v05.md`(구현에서 정해진 것)
4. 허브 코드(읽기만): `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev/backend/app/modules/gold/` — `concern.py` · `core.py` · `coverage/` · `resolve.py`
5. silver: `$SM/silver/concern.csv`(parent_code) · `concern_site.csv`(95행) · gold `g_indication.csv` · `g_scope.csv`

## 할 것

**A. 허브 구멍 3 규칙(SPEC-001 도구 계약 · SPEC-002 B 흐름에 닿는 곳)** — 사용자 원칙 「질문이 가리키는 대상 × 필요한 정보 안에서는 빠짐없이」 · 일반 규칙(한 문항만 고치지 않음):
- **H1 고민 → 윗고민 물려받음**: 고민 자기 적응 행 0 이고 silver `concern.parent_code` 윗고민에 있으면 그 행을 `물려받음` 층으로 준다(예 Q10 볼 주름 → 깊은 주름 · 대상 54 고민). 층 표시 · RQ1 은 기존 물려받음 규칙대로. 여러 단 위로 올라갈지(가장 가까운 윗고민 하나 vs 끝까지) — 제안 + 근거.
- **H2 계열 → 자손 전부 펼침**: SPEC 「하위 = 자손 전부」 를 허브가 어김 — 계열 `scope` 가 하위 시술 아래 케이스를 안 편다(18 계열 전부 · 케이스 합 268). 어느 도구 · 칸이 자손 전부를 내야 하는지 계약을 못 박고 시험 기준(T 번호).
- **H3 고민 + 부위 → concern_site**: 「이마에 주름」 이 주름 CON-001 + 부위 이마로 잡히면 `concern_candidates(CON-001, site=이마)` 가 행의 site 글자만 걸러 2행 — silver `concern_site`(CSI-0001 이마주름 CON-005 ↔ 이마 SITE-014)로 **그 부위의 하위 고민 행까지** 넣는다(이마주름 직접 54행). resolve 단계에서 하위 고민 CON-005 를 대상으로 바꿀지 / concern_candidates 안에서 합칠지 — 제안 + 열린 것. concern_site 가 gold 에 없으면 gold 표를 늘릴지 허브가 silver 를 읽을지도 결정 행으로(gold 는 silver 값 그대로 원칙).
- 세 규칙마다: 영향 셈(코드 · 수) · 기존 37 문항 중 바뀌는 것 · 시험 세트 묶음 제안(문장 쓰지 마라).

**B. 되적기(구현에서 정해졌는데 SPEC 에 없는 것 → 결정됨)**: v05 앱 검수 뒤 W-1(읽을 종류 0 → KD6 기본 묶음) · W-2(부위마다 조회) · W-3 · N-2 · N-5 · 상품 셈 식(coverage 계열 17 · 시술 0 vs §4-9 15 · 11 — 정해서 적음) · 제품 offer inherited=0 · purpose=label · A-1 covered_by · app-key-fix1 미결 4 전부(G13 · G14 · D11 · `lineup_rows[]` · `kinds_met` · scope 가 명세에 듦 · 세트 칸 `key_upper_entries` · `key_lower_entries` · `key_fix1` · 세트 확정값이 초안을 이김 · ② 채점 입력 `kinds_met`) · 화면 말 「적응」 → 「어디에 쓰나」.

**C. 사용자 결정 목록(열린 것)**: app-key-fix1 미결 3(Q03 · Q05 lineup — 케이스 아래 하위 0) 처럼 사용자가 정할 것만 따로 표(추천 붙임). 그 밖은 WORK 전 사용자 결정 0 이 목표.

version 0.5.2 · 변경 기록 · 열린 것 표 상태 칸.

## 검증

- 결정 행 → 문서:줄 표 · H1~H3 각각 근거 셈(네가 직접 CSV 로 다시 센 수 — app 보고 수와 대조)
- 부록 A 헤더 대조 다시 · 공개 grep(회사 데이터 본문 0 — 코드 · 수만)
