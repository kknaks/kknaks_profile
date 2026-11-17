# SPEC-001 · SPEC-002 0.5.0 — 길 찾기 재설계 지시서

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · allowed_paths(이번엔 **SPEC-001 · SPEC-002 두 파일만**) · 제약(공개 레포 · 외부 API · .env · 코드 레포 변경 금지) · §8 검증 · §9 완료 보고 그대로.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev` · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`

## 읽을 것

1. `$W/_RESUME.md` §2 **맨 위 행 「길 찾기 재설계 진행」 부터 아래로 11-16 행 전부**(특히 안전 강제 첨부 폐기 · 흐름 · 원칙 · 허브/앱 검수 뒤 결정 · 속도 탭 · 화면 동시 실행) ← 정본
2. `$W/_RESUME.md` §1 「e2e 피드백」 1~3 + 아래 4 ← 이번 재설계가 풀어야 할 실패들(run id 있음 — 앱 `~/orca/workspaces/clinic_chat/phub-gold-jev/runs/runs.jsonl` 에서 trace 를 읽어 근거로)
   - 4: 「써마지의 원리가 머야」 → 허브 resolve 조사 목록에 「의」 없음(`~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev/backend/app/modules/gold/resolve.py:20`) → 후보 0 → Jev 입구 고르기가 에이전(PRD-425) 오선택 → 범위 못 정해 K2 실행 중단(run 9612b0ddc5e6)
   - 속도 탭 실측: B 선별 묶음 Noul 대부분 0.3~0.7 → 거의 다 넘김(run f0060a0fff0d · 7deeab3778dd · `trace.selection`)
   - 상위 제품 29 중 자기 행 0 · 하위에만 3(써마지 · 리쥬란 · 더마펜) · 대부분 하위에 다른 행 더 있음 — 코디 셈(gold `g_scope` role 하위 제품 · silver `product.parent_code`)
3. 두 SPEC(0.4.1) + 그 뒤 구현에서 결정됐지만 SPEC 에 아직 없는 것(「SPEC 0.4.2 때 되적기」 — `_RESUME` §2 의 N1-1 · 허브 W-1 제품 offer role · 앱 F-1 · W-1 속성 시작 폭 · Q10 · Q25 · W-3 · R2-F1 · 화면(WORK-003) · 속도 탭(WORK-004) · effort · 동시 실행)
4. `$P/para/resources/note/ai/llms.txt` · `$W/research-gold-connect.md` §1 · `$SM/gold/semantic-map.md` §5(물려받기 · 「하위는 표시만」)

## 할 것

**A. 길 찾기 재설계(SPEC-002 B 열 흐름 · SPEC-001 도구)** — 결정 행 그대로:
- ① **허브가 후보를 넓게**: 질문 글을 정규화한 뒤 그 안에 **들어 있는 모든 입구 이름**(g_entry norm 부분 일치 · 조사 · 띄어쓰기 무관 · 긴 것 우선이되 짧은 것도 남김 — 폭 원칙)을 후보로 · 후보마다 정보 종류별 **자기 / 하위 / 물려받음 행 수** 셈을 같이(새 도구 또는 resolve 확장 — 제안 + 열린 것). 오타 등 0 이면 기존 입구 고르기로.
- ② **Jev 가 처음에 한 요청으로 판단**: (a) 후보마다 「질문이 이것을 가리키나」 Noul (b) 정보 종류(개요 · 원리 · 효과 · 적응 · 부작용 · 금기 · 회복 · 같은 날/간격/순서 · 상품 · 패키지 · 제품 목록 …) 마다 「이 질문에 필요한가」 Noul (c) 범위는 (a)(b) 에서 결정론으로 끌어냄(Choice 를 줄일 수 있으면 줄임 — 제안). instructions 영어 · 후보 설명에 행 수 셈.
- ③ 허브는 **고른 대상 × 필요한 정보 종류만** 읽되 그 안에서는 빠짐없이(쪽 끝까지) · **하위 층 자기 행도 넣고 층 표시**(「하위는 표시만」 → 「하위도 읽고 층을 밝힘 · 상위 이름으로 일반화 금지」 — semantic-map §5 를 바꾸는 결정 · SPEC 에 근거 행 인용). 필수 항목은 「자기 또는 하위 자기 행」 으로만 충족 · 물려받은 윗층만으로는 충족 아님(보여 주기만).
- ④ 애매한 Noul(0.3~0.7) 처리: 대상은 넘김 쪽 · 정보 종류는 범위 기본 묶음과 합집합 — 제안 + 1회차 trace 뒤.
- ⑤ 깊이(재귀) · 틀린 말 검사 · 종료 상태는 유지하되 새 흐름에 맞춰 번호 · 이름 정리.
- ⑥ 답 프롬프트 원칙에 「답에 id 인용을 줄마다 넣지 않음(기록에만) · 모범 답 꼴(계열 · 시술 · 원리 한 줄 · 되묻기)」 — e2e 지적 1(문구 자체는 사용자 확인 C-1).
- 원칙 문구를 「질문이 가리키는 대상 × 필요한 정보 안에서는 빠짐없이」 로 다시 적고, 그 판단을 Jev(+규칙)가 맨 앞에서 한다는 것을 §1 에.

**B. 되적기**: 위 3 의 구현 결정을 두 SPEC 본문에 반영(열린 것 → 결정됨).

**C. 속도 · 화면**: 화면 · 속도 탭 · effort · 동시 실행 · 첫 답 글자(`click_to_first_answer_ms` — C 측정 보정, 지금 구현 중)를 SPEC-002 에 짧게(측정 정의 중심).

**D. 시험 세트**: e2e 실패 꼴(상위 이름 · 하위에 데이터 / 「…의」 등 조사 / 입구 겹침 / 정보 종류 하나만 묻는 질문)을 묶음으로 추가 제안(문장 쓰지 마라 — 묶음 · 셈 근거만).

version 0.5.0 · 변경 기록 · 열린 것 표 상태 칸. **WORK 전 사용자 결정 = 0** 이 목표 — 남으면 따로 목록.

## 검증

- 결정 행 → 문서:줄 표 · e2e 실패 4 각각이 새 흐름에서 어디서 막히는지(run 의 trace 근거) 표
- 부록 A 헤더 대조 다시(새 도구 · 칸) · 공개 grep
