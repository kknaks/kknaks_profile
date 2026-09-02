---
target: 모두닥 주식회사 · Problem Solver (Engineering Based)
jd: https://modoodoc.career.greetinghr.com/ko/o/202796
based_on: 2026-08-28-modoodoc-jd-analysis.md §4 어필 전략
심사축: 엔지니어링 문제 해결 · 사업 전체 오너십 · 의료 도메인 · AI-Native 실행
정면: 처리량 3.2배 · 6개월 무장애 · 800GB 무중단 이관 · 의료 AI · 승인형 워크플로 재사용 / 경합: 개발 3년·매출·병원 영업·마케팅 / 침묵: Django·병원 계약·ROAS·제품 A/B 테스트
created: 2026-08-28
updated: 2026-08-28
---
# 이건학

백엔드 엔지니어 · AX 리더\
서울, 대한민국 ·\
email : [dh221009@naver.com](mailto:dh221009@naver.com)\
github : [https://github.com/kknaks](https://github.com/kknaks)\
blog : [https://kknaks.dev](https://kknaks.dev)

## 소개

개발 경력 1년의 백엔드 엔지니어이자 AX 리더입니다. 고부하 조회 처리량 3.2배, ETF 60종
실시간 시세 6개월 무장애, 800GB 데이터베이스 무중단 이관으로 운영 문제를 해결했습니다.

4인 팀에서 의료 AI 제품과 사내 AX 워크스페이스를 만들고 있습니다. AI가 초안을 만들고
사람이 승인하는 업무 흐름을 공통 구조로 묶었으며, 개인 제품 4개를 배포해 운영하고 있습니다.

## 기술


| 구분        | 사용 기술                                                                            |
| --------- | -------------------------------------------------------------------------------- |
| 서버        | Python · FastAPI · PostgreSQL · MySQL · Redis · RabbitMQ · Elasticsearch         |
| 프론트 · 모바일 | Next.js · React · TypeScript · Swift · SwiftUI                                   |
| AI        | Anthropic Claude API · Azure OpenAI · LangGraph · MCP                            |
| 인프라 · 데이터 | Docker Compose · Linux · AWS · Azure · Airflow · Logstash · Prometheus · Grafana |


## 경력

### 메디솔브 AI — AX 리더 · 2026.06 – 현재

4인 팀에서 사내 업무 자동화 제품과 의료 AI 솔루션의 설계·개발을 담당

- **Mediness — 개발·QA 기준 표준화** — 흩어진 문서·회의·의사결정·업무를 하나의 사내
  시스템으로 통합. 기능 명세 60여 건과 작업 단위 100여 건을 같은 양식으로 관리해 개발 범위와
  QA 기준을 일치시킴
- **반복 개발 제거 — 같은 승인 기능을 세 업무에 재사용** — AI가 초안을 작성하고 사람이 승인하면 실행하는
  공통 기능을 분리해 회의·장애 대응·의사결정에 적용. 새 업무를 추가할 때 공통 코드 수정 없이 재사용
- **안전한 AI 실행 — AI가 실패해도 승인 요청 생성** — AI가 도구를 직접 실행하지 못하게 막고,
  서버가 허용된 작업인지 확인한 뒤 사람의 승인을 받아 실행. AI 응답에 문제가 생겨도 실패 내용을
  남겨 담당자가 업무를 이어갈 수 있게 처리

### 메디솔브 AI — 백엔드 개발자 · 2026.02 – 2026.06

의료 클리닉용 상담 자동화 제품 2종의 백엔드 담당

- **Charty — 실시간 상담 음성을 구조화 차트로 전환** — 전사·언어 판별·번역을 세 단계로
분리해 한국어 번역 호출을 차단. 시술 용어 사전과 LLM 폴백으로 결과 흔들림과 세션 중단 방지
- **Linky — 6개 메신저를 한 인박스로 통합** — 수신·응답을 큐와 워커로 분리하고 위험 대화는
사람에게 인계. `(대화 ID, 대상 메시지 ID)` UNIQUE 제약으로 재시도 중복 답변 차단

### 퀀터스 — 백엔드 개발자 · 2025.08 – 2026.02

퀀트 트레이딩 앱의 실시간 시세와 뉴스·공시 데이터 파이프라인 담당

- **실시간 시세 파이프라인 — 6개월 무장애** — ETF 60종을 웹소켓으로 수집하고 장애 시
10초 폴링으로 자동 전환·복귀. RabbitMQ 전달과 Redis master/slave 저장으로 장 중 데이터 공백 0회
- **뉴스·공시 조회 — 처리량 3.2배** — MySQL 동기 조회를 Elasticsearch 비동기 검색으로
전환하고 호출을 3회→1회로 축소. k6 300 VU에서 RPS 25.7→81.2, 평균 응답 68% 단축,
P95 57% 개선
- **800GB 데이터베이스 — 무중단 이관** — dump/load·DMS·dual write를 중단 시간·손실·비용으로
비교해 DMS 선택. binlog CDC 실시간 복제 후 연결만 전환해 다운타임 0
- **뉴스·공시 수집·AI 요약 — 하루 약 4천 건** — Airflow 1시간 주기 수집과 LangGraph
종목 판별·요약·한↔영 번역 파이프라인 구축

### 도화엔지니어링 — 토목 설계 · 2020.01 – 2023.12

도로·인프라 설계 4년. 개발 경력과 분리해 기재

## 사이드 프로젝트 — 여름별컴퍼니

기획·개발부터 배포·운영까지 완주한 제품 4개

### Wine Log — App Store·Google Play 운영

라벨 촬영으로 와인 정보를 채우고 시음 기록에 맞춰 다음 와인을 추천하는 모바일 앱. 모바일·관리자
웹·FastAPI 백엔드·AI 워커 4개 컴포넌트를 구성해 iOS와 Android에 배포

→ [App Store](https://apps.apple.com/kr/app/wine-log/id6758934423) · [Google Play](https://play.google.com/store/apps/details?id=com.kknaks.winelog) · [GitHub](https://github.com/kknaks/wine_log)

### DeskDeck — App Store 출시 · v1.0.1

iPhone으로 Mac의 창을 전환하고 단축키를 실행하는 LAN 전용 리모컨 앱. 기능 명세 7건,
작업 단위 17건과 ADR 5건을 작성하고 iOS 앱·macOS 헬퍼를 구현해 App Store 1.0.1 출시

→ [App Store](https://apps.apple.com/kr/app/deskdeck/id6772868137)

### Summer Star — 사무실 NFC 출퇴근 운영

직원이 NFC 카드를 대면 출입을 기록하고 출퇴근으로 해석하는 사무실 시스템. Next.js 어드민·FastAPI
백엔드·PostgreSQL·Pi NFC 에이전트를 묶어 실제 사무실에 배포해 운영

→ [GitHub](https://github.com/kknaks/summer_star_company)

### open-kknaks — PyPI 배포 · v2.0.2

Claude Code와 Codex CLI 작업을 Redis 큐와 워커로 실행하는 Python 라이브러리. provider 2종을
같은 제출·결과·스트림 계약으로 묶고 미들웨어 6종, 인터페이스 3종, 테스트 232건을 갖춰 PyPI v2.0.2 배포

→ [PyPI](https://pypi.org/project/open-kknaks/) · [GitHub](https://github.com/kknaks/open_kknaks)

## 교육

- 멋쟁이사자처럼 백엔드 스쿨 플러스(심화) · 2024.12 – 2025.03
- 비트캠프 풀스택 과정 · 2024.06 – 2024.12
