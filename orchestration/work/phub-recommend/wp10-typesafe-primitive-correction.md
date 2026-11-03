# WP-10 긴급 정정: TypeSafe 공식 primitive

사용자가 [TypeSafe Jev with coding agents](https://docs.typesafe.ai/introduction/coding-agents.md)를 제공해 공식 문서를 대조했다. [Primitives](https://docs.typesafe.ai/primitives)는 한 요청의 질문들이 같은 state를 **독립 평가**한다고 명시한다. 동일 후보 목록으로 `pick_1..pick_k` Choice를 반복하면 여러 노드 선택을 보장하지 않는다. [Noul](https://docs.typesafe.ai/primitives/noul)은 yes 확률을 반환하고 [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out), [Classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages)는 여러 관련성 질문을 한 요청에 배치하는 패턴이다.

정본 `SPEC-006.md` 0.3.13 §3-4-1-7 마지막 문단과 `WORK-012.md` 0.3.13 WP-10 마지막 문단으로 교체됐다. **노드 후보마다 관련성 Noul 하나 + 답 준비 Noul 하나를 같은 `system_one`에 보내고**, 앱이 여러 후보를 선택/보류한다. 안전·명시 target·부재 검증은 앱의 hard gate다. Jev는 page마다 호출하지 않는다. 후보별 결과와 threshold/불확실 구간을 trace로 남긴다. 동일 Choice 슬롯 반복 구현은 사용하지 않는다. 현재 작업 중이면 이 정정을 적용하고, 범위/시간상 어려우면 잘못된 설계로 실물 Q002를 돌리지 말고 원인과 남은 작업을 보고한다.
