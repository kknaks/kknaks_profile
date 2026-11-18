# [app] 답 키 고치기 1 — 사용자 답 키 검토 결정 반영 · 다시 뽑기

**너는 앞 판의 맥락이 없다.** /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/phub-gold-jev-app-brief.md 의 역할 · allowed_paths · 공개 레포 제약 · §9 완료 보고 그대로(핸들은 preamble 값). 문서는 전부 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev 에 있다. 워크트리 /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev(미커밋 위에 이어서).

`SM=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gold · silver · 원장 체크 · 읽기만)

읽을 것: `_RESUME.md` §2 맨 위 「2026-11-17 답 키 검토」 행(← 정본) · `SPEC-002-chat-eval.md`(0.5.1 — 답 키 · RQ1 · 틀린 말 검사 절) · 앱 `clinic_chat/evalset/{answer_key,key_calls,loader}.py` · `clinic_chat/walk/gate.py` · `data/eval-set/key-summary.md`.

## 할 것

사용자가 답 키 37 을 사람이 읽는 표로 보고 정했다. 그대로 반영하고 **37 키를 다시 뽑는다**.

- **K1 · Q35**(보톡스 회복): 기대 종류 = **회복만**(부작용 뺌 — 묻지 않은 안전 정보 안 붙임).
- **K2 · Q03**(스킨보톡스 vs 보톡스): 기대 대상에 **보톡스(modality M1) 추가** — 비교 질문은 양쪽.
- **K3 · 윗층만**(Q02 · Q04 원리 · Q18 · Q21 · Q22 · Q36 · Q26 · Q37): 물려받은 윗층으로 채우고 **층을 밝히면 정답** — 이미 RQ1 규칙과 같은지 확인만(키 · 채점이 이걸 충족으로 세는지 · 다르면 맞춤).
- **K4 · 자료 없음**(Q10 · Q12 · Q33): 「자료 없음 / 원장 확인」 을 밝히면 정답.
  - **Q10 볼 주름**: 원장 LCK-010 — 「깊은 주름(팔자주름, 볼 주름 등)」 의 적응 행이 윗고민 **깊은 주름 CON-008** 에 붙어 있다. 기대 = **CON-008 의 적응(어디에 쓰나) 행을 「깊은 주름 기준」 층 밝혀 답함**(기대 상태 근거 충족 · 「원장 확인」 아님). 고민 → 윗고민 물려받음이 허브 도구로 이미 오는지 먼저 확인 — **허브 코드 변경이 필요하면 고치지 말고 코디에게 [질문]**.
  - **Q12 필러 혈관 폐색 시간**: 기대 대상 = **필러(modality M2) 전체 + 하위**(지금 히알루론산 필러 PRC-100 만 → 넓힘) · 혈관 폐색. 기대 = 부작용 행 · 세부(자리 · 비율 · 임계량 · 징후 · 즉시 내원) 답함 + **onset · duration 칸 빈칸 → 「자료에 없음」 밝힘**. 원장에도 없음(코디 확인 — taxonomy.json 필러 `onset_duration` 은 **효과** 발현 · 지속).
  - **Q33 코그 실 리프팅**: 대상 0 — gold `g_entry` · `g_offer` · silver 에 코그 / 실 리프팅 상품이 정말 없는지 셈해 보고(이름 · 코드 · 행 수). 있으면 키 고치고, 없으면 그대로 + 근거.
- **K5 · 틀린 말 검사 추가**: 「효과 기간(outcome · 원장 `onset_duration`)을 부작용 발현 · 지속 시간으로 씀」 · 「다른 대상(예: 콜라겐부스터)의 부작용 시간을 물은 대상 것처럼 씀」 — 기존 「층 섞기」 와 같은 꼴로 결정론 검사 + 시험.
- **K6 · 하위 목록(lineup) 구멍**: Q01 ~ Q05 의 `expected_kinds` 에 `lineup` 이 있는데 키 `rows` 에 g_scope 행 0 · `kinds_met` 에 lineup 없음. 원인 찾아 고침(키가 lineup 을 g_scope 로 읽는지) · 시험.
- **K7 · 부위 둘 이상 문항**: 앱 수정 1 W-2(부위마다 조회)로 `plan_calls` 가 바뀐 문항의 키를 다시 뽑음 — 어느 문항이 바뀌었는지 전후 표.
- 다시 뽑은 뒤: `key-summary.md` 다시 쓰고, **사람이 읽는 표 `data/eval-set/key-table.md`**(gitignore 자리) — 열: id · 질문 · 기대 대상(이름) · 기대 정보(한국어: 개요 · 원리 · 어디에 쓰나 · 효과 · 하위 목록 · 부작용 · 회복 · 금기 · 같이 하면 안 됨 · 같이 하면 좋음 · 패키지 · 같은 날 · 순서·간격 · 상품·가격 — 충족 층이 자기가 아니면 괄호로 하위 / 윗층만 / 없음) · 기대 결과. 0.5.1 키 대비 바뀐 줄 표시.
- **`--confirm` 하지 마라**(사용자 확인 몫). 실물 LLM 호출 0. 허브 18105 는 코디 것 — 읽기 호출만 · 띄우거나 내리지 마라.
- ruff · pytest · 커밋 후보 grep(키 · 회사 데이터 · 홈 경로 0).

보고서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/app-key-fix1-report.md` — K1 ~ K7 각각 무엇을 바꿨나 · 전후 수 · Q33 셈 · 미결(회사 데이터 본문은 질문 id · 코드 · 수만).
