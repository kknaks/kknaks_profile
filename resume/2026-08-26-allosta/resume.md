---
target: 알로스타 ((주)바이오컴) · 풀스택 개발자
jd: https://allosta.career.greetinghr.com/ko/o/187008
based_on: 2026-08-26-allosta-jd-analysis.md §4 어필 전략
심사축: 문제를 스스로 정의 · end-to-end 완성 · AI 를 일하는 방식으로
정면: 성능(3.2배) · 비동기(6개월 무장애) · AI 방식 / 경합: 연차·K8s·고객관점 / 침묵: FaaS·NestJS
created: 2026-08-26
updated: 2026-08-26
---
# 이건학

백엔드 개발자 · AX 리더  
서울 ·   
email : [dh221009@naver.com](mailto:dh221009@naver.com) 
github : [https://github.com/kknaks](https://github.com/kknaks)
blog : [https://kknaks.dev](https://kknaks.dev)

## 소개

개발 경력은 짧지만 밀도로 일해 왔습니다. 헬스케어 AI 스타트업에 백엔드로 입사해
4개월 만에 AX 리더를 맡았고, 그 전 회사에서는 실시간 시세 파이프라인을 6개월 무장애로
운영하며 고부하 조회 성능을 3.2배로 올렸습니다. 문제를 받은 대로 구현하기보다 원인을
분해해 구조로 풀고, 개선은 주장 대신 측정으로 증명합니다.

개인사업자로 제품 네 개를 기획부터 출시·운영까지 혼자 완주해 양대 앱스토어와 PyPI,
홈서버에서 운영 중입니다. AI 를 코드 생성 도구가 아니라 팀의 일하는 방식으로 설계하는
일을 회사와 개인 양쪽에서 하고 있습니다.

## 기술


| 구분        | 사용 기술                                                                    |
| --------- | ------------------------------------------------------------------------ |
| 서버        | Python · FastAPI · PostgreSQL · MySQL · Redis · RabbitMQ · Elasticsearch |
| 프론트 · 모바일 | Next.js · React · React Native · Expo · TypeScript · Swift               |
| AI        | LangGraph · MCP · Claude/OpenAI API                                      |
| 인프라       | Docker · Linux · nginx · AWS · Azure · Airflow                           |


## 경력

### 메디솔브 AI — AX 리더 · 2026.06 – 현재

4인 팀에서 기술 전반을 맡아 회사의 AI 전환을 주도

- **사내 AX 워크스페이스(Mediness) 주도** — 흩어진 문서·회의·의사결정·업무를 한곳에
모아 개발자가 아닌 구성원도 AI 와 함께 일하게 하는 사내 제품. 기획 문서 작성부터
QA 까지 전체 개발 과정 표준화
- **AI 권한 경계 설계** — AI 에게 맡길 것과 사람 승인이 필요한 것의 기준 수립.
상태를 바꾸는 요청은 반드시 승인 화면을 거치도록 강제
- **팀 AI 개발 환경 구축** — 자동화 규칙·검사 장치 세팅, 문서와 코드가 어긋나면
걸러내는 정합 점검 절차 운영

### 메디솔브 AI — 백엔드 개발자 · 2026.02 – 2026.06

의료 클리닉용 상담 자동화 제품 2종의 백엔드 담당

- **Charty — 실시간 AI 진료 차트** — 상담 음성을 실시간 전사·통역하고 AI 가 구조화된
차트를 만드는 서비스. 실시간 스트림과 LLM 이 동시에 도는 async 파이프라인,
전사·번역 3단계 분리 설계. 한 덩어리로 엉켜 수정 범위를 알 수 없던 서버를
역할별로 분리하고 테스트 137건을 붙여 고쳐도 안전한 구조로 전환
- **Linky — 외국인 환자 다국어 상담 플랫폼** — 텔레그램·왓츠앱 등 6개 메신저 문의를
인박스 하나로 모으고 AI 가 번역·응답, 위험한 대화만 사람에게 인계하는 서비스.
수신·응답을 큐로 분리한 워커 상태 기계와 LLM 폴백 설계. 실제 대화 상황 9가지를
자동 검증하는 도구로 출시 점검 통과. 환자 개인정보 마스킹·암호화 규칙 정의 참여

### 퀀터스 — 백엔드 개발자 · 2025.08 – 2026.02

퀀트 트레이딩 앱에서 트레이딩의 입력이 되는 데이터 파이프라인 담당

- **실시간 시세 파이프라인 — 6개월 무장애** — 대표 ETF 60종 시세를 웹소켓으로 수집해
자동트레이딩 서버에 전달. 장 중 공급이 끊기면 낡은 가격으로 매매를 판단하게 되는
문제에 대비해 하트비트 헬스체크 + 서킷브레이커(장애 시 10초 폴링 자동 전환·복귀),
RabbitMQ 전달, Redis master/slave 저장으로 안전장치를 겹침. 실서비스 6개월,
장 중 데이터 공백 0회
- **뉴스·공시 조회 성능 — 처리량 3.2배** — 관심 종목 뉴스 화면이 고부하에서 worker
timeout 으로 무너지는 문제를 원인 분해(인덱스 부재·국가별 중복 쿼리·동기 블로킹)
후, MySQL 동기 접근을 Elasticsearch 비동기 검색으로 전환하고 호출을 3회→1회로
축소. k6 실측 처리량 3.2배(RPS 25.7→81.2)·평균 응답 68% 단축·P95 57% 개선
- **뉴스·공시 수집·AI 요약 파이프라인** — 한국·미국 뉴스·공시 하루 약 4천 건을
Airflow 1시간 주기로 수집, LangGraph 파이프라인이 종목 판별 → 요약 → 한↔영 번역
처리
- **800GB DB 무중단 이관** — 클라우드 계약 변경으로 AWS RDS → Azure MySQL 이관.
3개 방안을 중단 시간·손실·비용으로 비교해 DMS 선택, binlog CDC 실시간 복제 후
접속만 전환해 다운타임 0 으로 완료

## 사이드 프로젝트 — 여름별컴퍼니 (개인사업자)

기획·개발·출시·운영을 한 사람의 시야로 완주. 모두 지금 접속 가능

### Wine Log — App Store · Google Play 출시

마신 와인을 기록·관리하는 모바일 앱. 라벨 사진을 찍으면 AI 서버가 와인을 인식해
정보를 채우고, 관리자 웹에서 데이터 관리. 모바일(React Native)·관리자 웹(Next.js)·
AI 서버(FastAPI + pgvector + LangGraph)·인프라까지 한 제품의 전 층을 혼자 담당해
양대 스토어 출시

→ [App Store](https://apps.apple.com/kr/app/wine-log/id6758934423) · [Google Play](https://play.google.com/store/apps/details?id=com.kknaks.winelog) · [github](https://github.com/kknaks/wine_log)

### DeskDeck — App Store 출시 (v1.0.1)

iPhone 을 Mac 의 리모컨으로 쓰는 앱. 발표나 강의 중 노트북 앞을 떠나도 손 안의
폰으로 창 전환·단축키 실행, 같은 네트워크 안에서 실시간 동작. 기획부터 심사
대응·배포까지 혼자 완주

→ [App Store](https://apps.apple.com/kr/app/deskdeck/id6772868137)

### kknaks.dev — 홈서버 운영 중

포트폴리오이자 스스로 자라는 지식 파이프라인. 매일 커밋을 수집해 AI 가 활동을
요약하고, 유튜브·블로그 캡처 자료가 승인 게이트를 거쳐 공개 문서로 발행. 사람과
자동화가 같은 문서를 덮어쓰는 문제를 겪은 뒤 원천 데이터의 소유 정의(SSOT)와
사람 승인 게이트 설계로 해결. FastAPI + PostgreSQL + 워커 구성을 홈서버에 직접
배포·운영

→ [kknaks.dev](https://kknaks.dev) · [github](https://github.com/kknaks/kknaks_profile)

### open-kknaks — PyPI 배포

AI 코딩 도구(Claude Code CLI)를 사람이 아닌 프로그램이 호출할 수 있게 감싼 태스크 큐
라이브러리 + MCP 서버. AI 작업을 서비스 파이프라인의 한 단계로 편입. 회사
제품에서도 사용 중

→ [PyPI](https://pypi.org/project/open-kknaks/) · [github](https://github.com/kknaks/open_kknaks)

## 교육

- 멋쟁이사자처럼 백엔드 스쿨 플러스(심화) · 2024.12 – 2025.03
- 비트캠프 풀스택 과정 · 2024.06 – 2024.12

