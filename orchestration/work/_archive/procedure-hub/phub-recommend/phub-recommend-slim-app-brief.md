# [backend] 실험 앱 비용 · 속도 줄이기 — Jev 가 필요한 정보 고르기 · 채점 버튼 · 캐시 · 비용 표시 (사용자 10-30)

(앞 작업 WORK-004 이어서 · 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` · 로컬 커밋만 · push 금지)

## 왜(사용자)
실물 4질문에 $10 소진 — 답변 입력만 질문당 10만~20만 토큰(허브 recommend 145KB · case1 도구 결과 누적 재전송) + Opus 채점 2번(토큰 기록 없음). 「질문 한 번에 2달러는 너무 비싸」 · 「그래프에서 몇 단계를 할지 Jev 가 판단하면 안 돼? 모든 단계를 다 받아야 해?」
**허브는 다른 워커가 동시에 고침**: 도구 기본 응답 = 짧은 카드(안전 요약은 늘) · `sections` 입력(SPEC-005 §4-3 이름: overview · method · recovery · aftercare · timeline · emergency · disclosure · safety.side_effects · safety.complications · safety.pih · checks · site_caution · dose · products · evidence · ops · market · all). 허브가 끝나기 전엔 모의로 · 끝나면 실물 대조(코디가 18005 재시작 후 알림)

## 할 일
1. **case3 — Jev 가 필요한 정보 고르기**: 같은 Jev 요청에 「필요한 정보」 질문 추가(section 마다 Noul 또는 Choice — 한 요청 · 병렬이라 시간 거의 같음) → 허브 호출에 `sections=` 로 그 항목만. 안전 요약은 허브가 늘 줌. 질문 꼴별 예시를 시험으로(추천 → 기본만 · 「임신 중 …」 → checks · 「부작용」 → safety.side_effects/complications · 「회복」 → recovery/aftercare)
2. **case2 — 도구 설명**에 「기본은 짧은 카드 · 필요하면 sections 로 다시 요청」(공통 프롬프트는 같게 · 데이터 · 도구 설명만 다르게 — R-5)
3. **case1 — 원장 도구 결과 누적**: raw_list 기본 depth 를 낮추거나 크기 상한 · 도구 결과가 커지면 잘림 표시(SPEC §5-12 크기 한도) — case1 이 허수아비가 되지 않게 원장 접근 능력은 유지
4. **프롬프트 캐시**(Anthropic cache_control — 시스템 프롬프트 · 도구 설명 · 도구 루프 앞부분) · 세 케이스 같게
5. **Opus ① 이름 뽑기 · ② 채점은 자동으로 돌리지 않고 버튼**(열 아래 「채점」 · 기록 표에서도) — 자동 끄기는 설정값(기본 끔)
6. **비용 기록 · 표시**: 모든 LLM 호출(Sonnet · Opus · Jev) 토큰을 기록(채점 포함 — 지금 빠짐) · 캐시 읽기/쓰기 토큰 · 모델별 단가표(설정 · 출처 날짜 주석)로 질문당 예상 $ 를 열마다 · 합계로 화면에 · 기록에
7. **목표**: 채점 없이 질문 1개 ≤ $0.20(세 열 합) · case2 · case3 첫 글자 · 전체 시간 줄어듦을 모의로 확인 · 실물 1질문은 코디 알림 뒤(사용자 크레딧 충전 뒤)
- 시험 · ruff · 18210 재시작 · 실물 호출 없음(크레딧 소진) · 기록 RUNS_DIR 그대로
## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_56c4278e-4761-44d7-8d67-87ca697be965 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: 실험 앱 비용 줄이기" --body "예상 $/질문 N(모의) · 시험 N passed · 커밋"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] backend 완료 — 실험 앱 비용 줄이기. 상세는 인박스." --enter
```
