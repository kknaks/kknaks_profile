---
type: career
period: "2026.02 — present"
display_order: 1
is_current: true
title:
  ko: "백엔드 개발자"
  en: "Backend Developer"
org:
  ko: "메디솔브 AI"
  en: "Medisolve AI"
location:
  ko: "서울"
  en: "Seoul"
summary:
  ko: "피부과 전용 CRM, MSO 제작, 사내 하네스 엔지니어링"
  en: "Dermatology-focused CRM, MSO development, in-house harness engineering"
stack:
  - Python
  - FastAPI
  - Postgres
  - Vite
  - LangChain
# 이력서 PDF — 비면 PDF 미표시 (planning-02 §3.2).
bullets:
  ko:
    - "피부과 전용 CRM 백엔드 — Python/FastAPI/Postgres 기반 도메인 모델 설계 및 API 구현"
    - "MSO (Multi-Site Operation) 백엔드 — 다중 의원 데이터 격리·권한·운영 기능"
    - "사내 하네스 엔지니어링 — Claude Code 환경 설계, 자동화 룰·프리커밋·skill 정착"
    - "LangChain 기반 의료 도메인 AI 기능 통합 — 차트 요약·문서 검색"
  en:
    - "Backend for a derm-focused CRM — domain modelling and API on Python/FastAPI/Postgres"
    - "MSO (Multi-Site Operation) backend — multi-clinic data isolation, RBAC, ops features"
    - "In-house harness engineering — Claude Code environment, automation rules, pre-commit, skills"
    - "LangChain integration for medical-domain AI — chart summarisation, document retrieval"
---

## 무슨 일 하는지

피부과 전용 CRM과 MSO(Multi-Site Operation) 백엔드를 맡고 있으며, 레거시 의사결정 흐름을 Action Runtime의 정식 도메인으로 이식하는 워크플로 엔진(스테이지·엣지·Action·권한·알림 축)과 그 워크플로가 노출하는 MCP tool 표면(조회/쓰기 tool 인벤토리와 인증 정책)의 스펙·구현을 함께 주도하고 있다.

## 담당 영역

backend 중심으로 도메인 모델과 API를 설계하고, 제품 스펙(SPEC)과 작업계획(WP) 문서로 워크플로·MCP tool 계약을 먼저 정의한 뒤 별도 구현 레포의 실제 구현과 짝을 맞추는 방식으로 일한다. 그 과정에서 알림·권한·태스크 라이프사이클뿐 아니라, 어떤 tool을 세션에 노출할지(노출 축)와 그 tool 호출에 사람 인증을 요구할지(인증 축) 같은 크로스커팅 관심사를 스펙 레벨에서 조율한다.

## 챌린지

- 스펙을 구현 전에 완벽하게 쓰기보다, 구현 중 드러난 괴리(배정 알림 종수, round_no 축 오류, DnD 삽입선 좌표계 불일치 등)를 스펙에 계속 환류하는 방식으로 운영한다.
- 레거시 데이터와 신규 workflow 데이터를 한 대시보드에 합류시키는 문제처럼 스코프를 유보했다가 다시 정식 계약으로 끌어오는 판단을 반복하며, 레거시 의사결정 원장은 결국 tool 표면에서 완전히 은퇴시키고 신규 workflow로 이관을 마무리했다.
- 레거시 미종결 건의 이관처럼 원칙만 먼저 합의하고 실행 시점은 배포 시점으로 명시적으로 유보해 리스크를 관리한다.
- 세션이 참조할 tool 목록을 짤 때 "후보에 넣을지"와 "호출에 인증을 요구할지"를 다른 층의 통제로 나눠, 민감한 write 경로는 아예 후보 목록에서 빼는 방식으로 위험을 설계 단계에서 차단한다.

## 배운 점

- 승인 같은 행위 자체가 추적 가능한 태스크로 남아야 한다는 설계(부트스트랩 태스크)가 여러 워크플로에서 재사용 가능한 패턴임을 확인했다.
- 설계 초안의 축 오류나 좌표계 불일치는 스펙 선행만으로는 안 잡히고, 구현·실기동과의 짧은 피드백 루프를 거쳐야 드러나는 경우가 많다.
- tool 노출 여부(노출 축)와 사람 인증 요구 여부(인증 축)를 분리해서 설계하면, 같은 통제 패턴을 다른 세션·에이전트 표면에도 그대로 재사용할 수 있다.

## 대표 작업

- 사내 비공개 레포에서 진행 — 이 프로필 저장소에는 연결할 work 문서가 아직 없다.
