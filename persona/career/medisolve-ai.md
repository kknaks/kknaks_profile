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

피부과 전용 CRM과 MSO(Multi-Site Operation) 백엔드를 맡고 있으며, 레거시 의사결정 흐름을 Action Runtime의 정식 도메인으로 이식하는 워크플로 엔진(스테이지·엣지·Action·권한·알림 축)과 그 워크플로가 노출하는 MCP tool 표면(조회/쓰기 tool 인벤토리와 인증·의존 정책)의 스펙·구현을 함께 주도하고 있다. 최근에는 조직 데이터 모델에서 사람 참조를 `users`에서 `organization_member`로 전환하는 cutover를 도메인별로 확장하고, 랜딩 에이전트 챗의 표시 계약과 회의 요약 파이프라인처럼 사용자 대면 품질 이슈도 함께 다루고 있다.

## 담당 영역

backend 중심으로 도메인 모델과 API를 설계하고, 제품 스펙(SPEC)과 작업계획(WP) 문서로 워크플로·MCP tool 계약을 먼저 정의한 뒤 별도 구현 레포의 실제 구현과 짝을 맞추는 방식으로 일한다. 그 과정에서 알림·권한·태스크 라이프사이클뿐 아니라, 어떤 tool을 세션에 노출할지(노출 축)·그 tool 호출에 사람 인증을 요구할지(인증 축)·tool 간 실행 의존 관계 같은 크로스커팅 관심사를 스펙 레벨에서 조율하고, 사람 참조 축이나 토큰 사용량 집계처럼 여러 도메인에 걸친 데이터 모델·관측성 설계도 함께 맡는다.

## 챌린지

- 스펙을 구현 전에 완벽하게 쓰기보다, 구현·실측 중 드러난 괴리(배정 알림 종수, round_no 축 오류, DnD 삽입선 좌표계 불일치, MCP 토큰 만료·스트림 유실 위험, 챗 UI 표시 계약 부재 등)를 스펙에 계속 환류한다.
- 레거시 데이터와 신규 workflow 데이터를 한 대시보드에 합류시키는 문제처럼 스코프를 유보했다가 다시 정식 계약으로 끌어오는 판단을 반복하며, 레거시 의사결정 원장은 결국 tool 표면에서 완전히 은퇴시키고 신규 workflow로 이관을 마무리했다.
- 레거시 미종결 건의 이관처럼 원칙만 먼저 합의하고 실행 시점은 배포 시점으로 명시적으로 유보해 리스크를 관리한다.
- 세션이 참조할 tool 목록을 짤 때 노출 여부와 인증 요구를 다른 층의 통제로 나누고, MCP tool 카탈로그를 확대할 때는 tool 간 의존 관계까지 계약(관리자 화면 양방향 경고)으로 선언해 필요한 동반 tool이 꺼진 채로 방치돼 에이전트가 조용히 포기하는 사고를 막는다. 범용 「승인 요청 tool 1개」 안은 tool 1개=권한 선언 1개 원칙이 깨져 기각한다.
- 설계상 있어야 할 흐름(발화→승인 게이트, 예약 수정 API)이 실제로는 이미 존재하지만 노출·연결만 빠진 경우를 「신규 기능」이 아니라 「계약됐지만 구현·노출이 빠진 조각」으로 규정해 처리 범위를 좁힌다 — 단 서로 다른 ID 축을 쓰는 API 간 정합은 과제로 남겼다.
- 사람 참조 축 전환처럼 도메인을 확장할 때는 배정 자리만이 아니라 감사·결재선 자리까지 전수조사해, 부분 전환으로 인한 도메인 내부 불일치를 미리 차단한다.
- 토큰 사용량처럼 「양」을 노출하는 관측성 지표와 방 제목처럼 「내용」을 드러내는 정보를 구분해, 내용에 해당하는 것은 별도 권한으로도 노출하지 않는 프라이버시 경계를 세운다.

## 배운 점

- 승인 같은 행위 자체가 추적 가능한 태스크로 남아야 한다는 설계(부트스트랩 태스크)가 여러 워크플로에서 재사용 가능한 패턴임을 확인했다.
- 설계 초안의 가정(축 오류·좌표계·위험 지점)은 스펙 선행만으로는 안 잡히고 구현·실측과의 짧은 피드백 루프에서 뒤집히며 드러난다 — 답만 채우지 않고 질문과 계약 자체를 다시 쓴다.
- tool 노출 여부(노출 축)와 사람 인증 요구 여부(인증 축)를 분리해서 설계하면, 같은 통제 패턴을 다른 세션·에이전트 표면에도 그대로 재사용할 수 있다.
- 기능이 없어 보이는 사고가 실제로는 백엔드·계약엔 이미 있고 노출(MCP 등재, UI 연결)만 빠진 경우가 반복돼, 「신설 vs 등재」를 먼저 구분하는 것이 조사 초기 판단 비용을 크게 줄인다는 것을 확인했다.
- 성격이 다른 입력(회의 유형별 발화 패턴, 음성인식 오인식)을 하나의 균질한 프롬프트로 처리하면 오류가 결과물에 그대로 섞여 들어간다 — 배경 주입→정정→정형화처럼 단계를 분리하는 편이 더 안정적이다.

## 대표 작업

- 사내 비공개 레포에서 진행 — 이 프로필 저장소에는 연결할 work 문서가 아직 없다.
