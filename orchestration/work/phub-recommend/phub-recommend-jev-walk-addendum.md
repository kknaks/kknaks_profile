# 보충(사용자 결정 11-01) — case3 = Jev 재귀 탐색으로 바꾼다(추가 아님 · 교체)

지금 case3(Jev 슬롯 1회 → 허브 경로 1회 → 의도 묶음 · 동봉 전부 → Claude)는 잘못된 설계다. 허브가 「뭐가 필요할지 몰라 다 주는」 구조라 46KB · C 10%. 바꾼다:

```
질문 → Jev(의도 · 시작 노드 후보: resolve)
  → 허브 peek(node): 노드 요약(slim) + 이웃 목록(종류 · 한 줄 라벨 · id) + 섹션 목록(이름 · fact 수 · 바이트) ≤ 2KB
  → Jev Choice: 펼칠 것(섹션 · 이웃 ≤255) · 「충분한가」(신뢰도)
  → 허브 expand(node, sections | neighbor ids): 고른 것만
  → … 걸음 상한 N · 바이트 예산 B 안에서 반복
→ Claude: 모은 fact(id · 원문) + claude_contract
```

## SPEC-005 v3.2(허브)에 더할 것
- **peek · expand 응답 꼴**(결정론 · LLM 없음): `peek` = slim 카드 + `neighbors[]{id, kind, edge, label}` + `sections[]{name, n_facts, bytes}` + 안전 요약(G13 유지) · `expand` = 요청한 섹션 fact 원문 · 요청한 이웃의 slim. 기존 도구(T3 procedure_card `sections=` · T8 neighbors) 위에 모양을 정하는 것 — 새 도구를 만들지 같은 도구의 모드로 할지 실물 보고 정함.
- A-1 다이어트는 **case2(Claude 가 부르는 MCP) 쪽 기본 응답**에 그대로 적용 · case3 는 peek/expand 로 크기를 Jev 가 정하므로 의도 묶음 · 동봉 자동 첨부는 case3 경로에서 안 쓴다(선택 가능 유지).
- 끝 조건에 peek 크기(≤ 2KB 중앙) · expand 1회 크기 · 걸음 4 안에 2차 분류 B 186 의 fact 에 **도달 가능한 비율**(그래프 경로 길이 셈 · 결정론) 추가.

## SPEC-006 v2(앱)에 더할 것
- case3 정의 교체: Jev 재귀 탐색 — 걸음 상한(기본 4) · 바이트 예산(기본 20KB) · 「충분」 신뢰도 문턱 · 못 찾으면 **되돌아가기** = 의도 기본 묶음 1회(지금 case3) · 걸음마다 기록(고른 노드 · 섹션 · Jev 신뢰도 · 바이트 · ms) · 첫 글자 영향 측정.
- 비교 기준: 전 case3(10-31 rerun-v3 기록)과 같은 182문항 · 같은 채점.
- Jev 호출 수 · 시간은 trace 에(0.3초 × 걸음).
