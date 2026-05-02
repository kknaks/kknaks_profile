---
type: career
period: "2025.06 — present"
display_order: 1
is_current: true
title:
  ko: "Backend Engineer"
  en: "Backend Engineer"
org:
  ko: "Stealth AI Co."
  en: "Stealth AI Co."
location:
  ko: "서울 · 하이브리드"
  en: "Seoul · Hybrid"
summary:
  ko: "LLM 기반 B2B 제품의 백엔드. RAG 파이프라인 + 임베딩 캐싱 + 벡터 DB 운영까지 담당."
  en: "Backend for an LLM-based B2B product. RAG pipeline + embedding cache + vector DB ops."
stack:
  - Python
  - FastAPI
  - Postgres
  - Docker
  - Redis
---

# Stealth AI Co. — Backend Engineer

(mock 본문 — 추후 본인 회고로 교체)

## 무슨 일 하는지

LLM 기반 B2B SaaS 제품의 백엔드. 사용자 문서를 임베딩해서 벡터 DB에 적재하고, 사용자 질의에 대해 retrieval + LLM 응답을 만들어 내려주는 RAG 파이프라인이 핵심입니다.

## 챌린지

- 임베딩 호출 비용 — 캐싱 전략 + 배치 처리로 비용을 줄였습니다
- 벡터 DB 인덱스 — HNSW 파라미터 튜닝 (efConstruction, M)
- 응답 latency — 동기 호출을 비동기로 전환

## 배운 점

- 백엔드 엔지니어가 인프라까지 직접 다뤄야 LLM 제품을 만질 수 있다는 것
- 모델 선택보다 데이터 파이프라인의 정합성이 더 큰 영향
- 비용 관점에서의 아키텍처 결정 (모델 호출 비용 vs 인프라 운영 비용)
