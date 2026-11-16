# 게이트 6 페이지 재생성 발주 — 8차 게이트 기준 71자리 (2026-11-06 · 사용자 「오퍼스로 발주 · 페이지 부터」)

## 입력
- `silver-v3/out/gate/batch6.json`·`.md`(8차 게이트 · 묶음: ledger-nodes 182 · dup-strong 38 · sentence-b 11 · ambiguous 13 · occlusion-embolism 3 · r30-candidates 2 · batch3 15 · r1-candidates 20 · mxx-prefix 34)
- `decisions-batch6b-dup-classification.json`(사용자가 승인한 ⑦ 분류 · verdict user_pending 5 만 남김)
- 참고 구현(3차 드라이런 기준 이전 페이지): `silver-v3/dryrun3/_ref_gen_gate6_dryrun3.py`(생성기) · `_ref_silver-gate-6.html`(결과). **화면 꼴·db 저장 방식(answers/<docId> · docId = encodeURIComponent(id) 의 % → _)·내보내기 상자·스크립트 구조는 그대로 따른다.** 데이터 부분만 8차로 바꾼다.

## 자리(정확히 71 · 생성기가 묶음별로 세어 출력)
| 묶음 | 자리 | 만드는 법 |
|---|---|---|
| 질문 | 2 | Q-prefix(아래 문구 바꿈) · Q-synonym(이전 페이지 그대로) |
| ⑦ 접기 | 5 | dup-strong 38 중 사용자 승인 분류의 user_pending 5 쌍만. 승인 31쌍 + 「처짐 ↔ 밑 처짐」(분석기가 턱밑을 쪼갠 빌더 버그 — 9차에서 고침)은 자리로 올리지 않는다. 선택지 셋: 같은 사건(짧은 쪽 · 붙은 말은 속성으로 분해) / 다른 사건(둘 다 노드) / 긴 쪽이 사건. 쌍마다 「왜 사람이 보나」 힌트(이전 페이지에 있음) |
| 애매 | 13 | ambiguous 13 그대로(문구 1 · 노드 12). 선택지: 노드로 둔다 / 다른 노드와 같다(이름 적기) / 부작용 아님(메모·설명문). 문구 자리는 원문 · 왜 애매 · locator |
| 문장꼴 | 11 | sentence-b 11. 선택지: 설명문으로 둔다 / 타임라인 줄로 / 사건 지정(이름 적기) |
| 폐색/색전 | 3 | occlusion-embolism 3. 선택지: 두 사건 모두 / 폐색만 / 색전만 |
| R30 연결 | 2 | r30-candidates 2. 선택지: 연결한다(edge_create) / 안 한다. 원문 근거 표시 |
| 묶음3 | 15 | batch3 15 그대로(선택지·근거·추천은 게이트 파일 것) |
| R1 수식어 후보 | 20 | r1-candidates 20. 선택지: 수식어로 둔다(사건에서 떼어 속성으로) / 사건 이름의 일부(떼지 않음). 말 · 원장 횟수 · 붙어 있던 노드 · 원문 예 |
| 합계 | 71 | |
mxx-prefix 34 는 자리로 올리지 않는다(사용자 결정 11-06: 원장 꼴 「계열코드-이름」 유지 · 4판에서 3판이 뗀 18종에 접두를 되붙임). Q-prefix 질문 문구는 「synergy 「계열코드-이름」 꼴 유지(사용자 결정) — 확인만」이 아니라 **빼고**, 질문은 Q-synonym 하나 + 아래 새 질문 하나로 2:
- Q-timeline-co2: post-procedure-timeline 의 타임라인 이름 「프락셔널 CO2 레이저」(1곳)도 4판에서 「CO2프락셔널 레이저」로 고칠까? 선택지: 고친다 / 그대로(타임라인 이름은 설명이라 둔다). 근거: 4판에서 시술 라벨 4곳(procedure-comparison 「CO2 프랙셔널 레이저」 · treatment-optimization 「프락셔널 CO2(피부결)」 · treatment-sequence 「프락셔널 CO2」×2)은 사용자 결정으로 「CO2프락셔널」 로 고친다.

## 규칙
- 자리·문구·원문은 게이트 파일과 원장에서만. 추천은 게이트 파일에 있을 때만(지어내지 않음). 원문은 브론즈 3판 locator 로 읽기.
- 페이지 맨 위에 「사용자 승인으로 닫힌 ⑦ 31쌍」 펼치기 요약(이전 페이지와 같은 꼴 · 분류 파일에서).
- 머리 제목 「실버 결정 묶음 6 — 남은 71자리」 · 묶음 이동 탭 · 진행 바.
- 산출: 생성기 `silver-v3/lib/gate6page.py`(또는 tools/) 와 HTML `silver-v3/out/gate/batch6-page.html` · 자리 목록 `batch6-page-slots.json`. 커밋·게시 금지(게시는 코디).
- 끝에 생성기가 묶음별 자리 수를 출력하고, HTML 스크립트를 `node --check` 로 문법 확인.

## 보고(20줄 안)
묶음별 자리 표(합 71 여부) · 빠진·남은 차이(있으면 왜) · node --check 결과 · 파일 경로.
