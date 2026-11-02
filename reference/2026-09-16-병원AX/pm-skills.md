# PM 스킬 전체 목록

> 조사 일자 2026-09-17 · 출처 `/Users/kknaks/.claude/plugins/marketplaces/pm-skills/` (동일 내용이 `~/.claude/plugins/cache/pm-skills/<plugin>/2.1.0/` 에도 있음) · 총 102개 (미확인 0)
>
> 각 플러그인은 `commands/*.md`(슬래시 커맨드 · 여러 skill 을 엮는 라우터)와 `skills/*/SKILL.md`(실제 절차·템플릿) 두 층으로 되어 있다. 아래 표는 두 층을 모두 포함한다.
> 이름이 같은 커맨드/스킬 쌍 7건(`draft-nda`·`privacy-policy`·`pre-mortem`·`stakeholder-map`·`test-scenarios`·`business-model`·`value-proposition`)은 설명이 달라 두 행으로 나눴다. 그래서 표의 행은 109개, 고유 스킬 이름은 102개다.

## pm-toolkit

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-toolkit:draft-nda` | 두 당사자 간 비밀유지계약서를 관할지에 맞는 조항으로 작성 | 병원 시스템 현장 관찰·인터뷰 전에 클리닉 측과 맺을 NDA 초안 | 커맨드. 짝 = `draft-nda` skill. 입력: 당사자·맥락. 지금 사용 가능 |
| `pm-toolkit:draft-nda` (skill) | 정보 유형·관할·법률검토 필요 조항까지 포함한 상세 NDA 작성 | 위와 같음(커맨드가 호출하는 실제 템플릿) | 커맨드 `draft-nda` 의 실체. 단독 호출 불필요 |
| `pm-toolkit:privacy-policy` | 데이터 수집·이용·보관·컴플라이언스를 다루는 개인정보처리방침 작성 | AX 제품이 환자 예약·상담 데이터를 다룰 때의 처리방침 초안 | 커맨드. 짝 = `privacy-policy` skill. 한국 의료법·개인정보보호법은 별도 확인 필요. 제품 범위 확정 후 |
| `pm-toolkit:privacy-policy` (skill) | 데이터 유형·관할·GDPR 등 컴플라이언스 고려사항과 법률검토 조항 포함 | 위와 같음 | 커맨드의 실체. GDPR 기준이라 국내 적용 시 보정 필요 |
| `pm-toolkit:proofread` | 문법·논리·흐름 오류를 전체 재작성 없이 짚어 고침 | 완성된 사업 계획서 최종 교정 | 짝 = `grammar-check` skill. 영어 기준. 한국어는 `korean-humanizer` 가 나음. 7단계에서 |
| `pm-toolkit:grammar-check` | 문법·논리·흐름 오류를 찾아 부분 수정만 제안 | 위와 같음 | `proofread` 커맨드의 실체 |
| `pm-toolkit:review-resume` | PM 이력서를 10가지 베스트프랙티스로 검토 | 해당 없음 | 이력서 전용. 이 프로젝트와 무관 |
| `pm-toolkit:tailor-resume` | PM 이력서를 특정 JD 에 맞춰 키워드·경험 재구성 | 해당 없음 | 이력서 전용. 가진 자료 중 COO 직무기술서가 있지만 이건 채용용이 아니라 직무 분석용이라 용도가 다름 |

## pm-ai-shipping

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-ai-shipping:derive-tests` | 문서화된 의도에서 테스트 커버리지 맵을 뽑고 기존/제안/미검증 갭을 분리, CI 게이트 권고 | 직영 병원에 AX 도구를 실제로 붙일 때(1단계) 그 코드의 테스트 맵 | 코드가 있어야 씀. 문서 단계에서는 해당 없음 |
| `pm-ai-shipping:document-app` | AI 가 만든 코드베이스를 역공학해 아키텍처·플로우·권한·변수 문서로 | 직영 병원 AX 시범 구축물의 인수인계 문서 | 코드 필요. 지금 단계 아님 |
| `pm-ai-shipping:performance-audit-static` | 정적 성능 감사 — N+1·워터폴·과다조회·인덱스 누락·캐싱 기회 | 해당 없음(코드 없음) | 코드 필요 |
| `pm-ai-shipping:security-audit-static` | 정적 보안 감사 — 신뢰 경계 매핑 후 근거 있는 위험만 보고 | 환자 개인정보를 다루는 AX 도구 배포 전 감사 | 코드 필요. 의료 데이터라 실제 구축 시엔 중요 |
| `pm-ai-shipping:ship-check` | 위 4개를 묶어 리뷰 가능한 출시 패킷 생성 | 해당 없음(코드 없음) | 위 4개의 라우터. 코드 필요 |
| `pm-ai-shipping:intended-vs-implemented` | 「하기로 한 것」과 「코드가 실제로 하는 것」의 격차를 찾는 방법론 | 병원 업무 매뉴얼(문서상 절차)과 실제 현장 운영의 격차 분석에 방법론만 차용 가능 | 레퍼런스 문서. 원래는 코드용이지만 3~4단계 병목 식별의 사고틀로 전용 가능 |
| `pm-ai-shipping:shipping-artifacts` | 출시 전 필요한 문서 세트의 정의(아키텍처·권한·변수·테스트 맵 등) | 해당 없음 | 레퍼런스 문서. 코드 단계용 |

## pm-data-analytics

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-data-analytics:analyze-cohorts` | 사용자 데이터 코호트 분석 — 리텐션 곡선·기능 채택·인게이지먼트 추세 | 클리닉 신환 코호트별 재방문율 분석(병원 EMR 데이터 확보 후) | 짝 = `cohort-analysis` skill. 입력: 실데이터. 3단계 이후 |
| `pm-data-analytics:cohort-analysis` | 리텐션 곡선·기능 채택 추세·세그먼트 인사이트 산출 | 위와 같음 | `analyze-cohorts` 의 실체 |
| `pm-data-analytics:analyze-test` | A/B 테스트 결과 분석 — 유의성·표본 검증·ship/extend/stop 판단 | AX 도구 도입 전후 상담 전환율 비교(직영 병원 파일럿) | 짝 = `ab-test-analysis`. 입력: 실험 데이터. 1단계 파일럿 이후 |
| `pm-data-analytics:ab-test-analysis` | 통계적 유의성·표본 검증·신뢰구간과 ship/extend/stop 권고 | 위와 같음 | `analyze-test` 의 실체 |
| `pm-data-analytics:write-query` | 자연어를 SQL 로 — BigQuery·PostgreSQL·MySQL 등 | 병원 EMR/예약 DB 에서 병목 지표(대기시간·노쇼율) 추출 쿼리 | 짝 = `sql-queries`. 입력: DB 스키마. 병원 시스템 접근 확보 후 |
| `pm-data-analytics:sql-queries` | 업로드한 스키마 다이어그램·문서를 읽고 방언별 SQL 생성 | 위와 같음 | `write-query` 의 실체 |

## pm-execution

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-execution:meeting-notes` | 회의 전사를 결정·액션아이템·후속으로 구조화 | **가진 「사업 구상 대화 전사」에서 결정된 것과 미결(목적·고객·수익 구조)을 분리** | 짝 = `summarize-meeting`. 입력: 이미 있음. **지금 바로 가능** |
| `pm-execution:summarize-meeting` | 날짜·참석자·주제·결정·요약·액션아이템 구조로 전사 요약 | 위와 같음 | `meeting-notes` 의 실체 |
| `pm-execution:plan-okrs` | 회사 목표에 정렬된 팀 OKR 초안 | AX 전환 1년차 OKR (목적이 정해진 뒤) | 짝 = `brainstorm-okrs`. 전제: AX 목적 확정. 지금은 못 씀 |
| `pm-execution:brainstorm-okrs` | 정성적 Objective + 측정 가능한 Key Result | 위와 같음 | `plan-okrs` 의 실체 |
| `pm-execution:pre-mortem` | PRD·런치 플랜의 리스크를 사전 부검 | 직영 병원 AX 전환 착수 전 「6개월 뒤 실패했다면 왜?」 | 짝 = 동명 skill. 입력: 전환 계획 초안. 6단계 이후 |
| `pm-execution:pre-mortem` (skill) | 리스크를 Tiger·Paper Tiger·Elephant 로 분류하고 출시차단/후속/추적으로 판정 | 위와 같음 | 커맨드의 실체 |
| `pm-execution:red-team-prd` | PRD·로드맵·전략의 핵심 가정을 공격하고 가장 싼 검증법 제시 | 사업 계획서 초안의 「AI 로 인건비를 줄일 수 있다」 가정을 깨보기 | 짝 = `strategy-red-team`. 입력: 계획서 초안. 7단계 직전 |
| `pm-execution:strategy-red-team` | 스틸맨 후 공격, 실패모드를 영향×확률×검증비용으로 순위화, kill criteria 제시 | 위와 같음 | `red-team-prd` 의 실체 |
| `pm-execution:sprint` | 스프린트 라이프사이클 — 계획·회고·릴리스노트 | 직영 병원 전환 작업을 스프린트로 운영할 때 | 라우터(`sprint-plan`/`retro`/`release-notes`). 실행 단계용 |
| `pm-execution:sprint-plan` | 캐파 추정·스토리 선정·의존성 매핑·리스크 식별 | 위와 같음 | 전제: 백로그 존재. 6단계 이후 |
| `pm-execution:retro` | 스프린트 회고 — 잘된 것·아쉬운 것·담당자와 기한이 붙은 액션 | 직영 병원 1차 전환 후 회고 | 실행 단계용 |
| `pm-execution:release-notes` | 티켓·PRD·체인지로그에서 사용자용 릴리스 노트 생성 | 클리닉 직원에게 배포하는 「이번 주 바뀐 것」 안내문 | 실행 단계용 |
| `pm-execution:stakeholder-map` | 이해관계자를 Power × Interest 그리드에 배치하고 소통 계획 | **원장·총괄실장(COO)·상담실장·간호팀·데스크를 권력/관심으로 매핑** — 3단계 인터뷰 대상자 선정 근거 | 짝 = 동명 skill. 입력: COO 직무기술서로 일부 확보. **거의 지금 가능** |
| `pm-execution:stakeholder-map` (skill) | Power/Interest 그리드 + 사분면별 소통 전략과 커뮤니케이션 플랜 | 위와 같음 | 커맨드의 실체 |
| `pm-execution:test-scenarios` | 유저스토리·스펙에서 해피패스·엣지·에러 시나리오 생성 | AX 도구의 예약 변경·노쇼 처리 시나리오 QA | 짝 = 동명 skill. 입력: 스토리. 구현 단계 |
| `pm-execution:test-scenarios` (skill) | 테스트 목적·시작 조건·역할·단계별 행동·기대 결과 | 위와 같음 | 커맨드의 실체 |
| `pm-execution:transform-roadmap` | 기능 중심 로드맵을 성과 중심으로 전환 | 「챗봇 도입·CRM 연동」 식 기능 나열을 「상담 대기 30% 감소」로 바꾸기 — 사업 계획서 로드맵 장 | 짝 = `outcome-roadmap`. 입력: 기능 로드맵 초안. 6단계 |
| `pm-execution:outcome-roadmap` | 이니셔티브를 사용자·비즈니스 임팩트 문장으로 재작성 | 위와 같음 | `transform-roadmap` 의 실체 |
| `pm-execution:write-prd` | 기능 아이디어·문제 진술에서 PRD 작성 | 병목 하나(예: 상담 예약 전화 응대)를 푸는 AX 모듈의 PRD | 짝 = `create-prd`. 전제: 병목 식별(4단계) 완료 |
| `pm-execution:create-prd` | 문제·목표·세그먼트·가치제안·솔루션·릴리스 8섹션 PRD 템플릿 | 위와 같음 | `write-prd` 의 실체 |
| `pm-execution:write-stories` | 기능을 백로그 항목으로 — user/job/WWA 포맷 + 수용 기준 | 해당 없음(사업 계획서 단계) | 라우터(`user-stories`/`job-stories`/`wwas`). 구현 단계 |
| `pm-execution:user-stories` | 3C(Card·Conversation·Confirmation)와 INVEST 기준의 유저스토리 | 해당 없음 | 구현 단계 |
| `pm-execution:job-stories` | "When [상황], I want to [동기], so I can [결과]" 포맷 + 수용 기준 | 「상담실장이 마감 후 차트 정리할 때…」 식으로 병원 직무 상황을 기술 | JTBD 포맷이라 병원 업무 관찰 기록을 정리하는 데 전용 가능. 3단계 이후 |
| `pm-execution:wwas` | Why-What-Acceptance 포맷의 백로그 항목 | 해당 없음 | 구현 단계 |
| `pm-execution:prioritization-frameworks` | RICE·ICE·Kano·MoSCoW 등 9개 우선순위 프레임워크 레퍼런스 | **6단계 작업 우선순위 설계 시 어떤 프레임워크를 쓸지 고르는 기준** | 레퍼런스 문서(판단 없이 읽기만 해도 유용). 지금 읽어둘 수 있음 |
| `pm-execution:generate-data` | 테스트용 더미 데이터셋 생성 — CSV·JSON·SQL·Python | 병원 EMR 데이터를 못 받는 동안 쓸 가상 예약/시술 데이터 | 짝 = `dummy-dataset`. 실데이터 대체용. 가짜 데이터로 분석 결론 내면 안 됨 |
| `pm-execution:dummy-dataset` | 컬럼·제약·출력 포맷을 지정한 현실적 더미 데이터 생성 | 위와 같음 | `generate-data` 의 실체 |

## pm-go-to-market

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-go-to-market:battlecard` | 세일즈용 경쟁 배틀카드 — 포지셔닝·기능 비교·반론 대응 | 우리 AX 솔루션 vs 기존 병원 CRM·차트 벤더 비교표 | 짝 = `competitive-battlecard`. 전제: 「남에게 판다」 결정 + 경쟁사 조사. 지금 못 씀 |
| `pm-go-to-market:competitive-battlecard` | 특정 경쟁사 대비 포지셔닝·기능 비교·반론 대응·승패 패턴 | 위와 같음 | `battlecard` 의 실체. 경쟁사 1곳 지정 필요 |
| `pm-go-to-market:growth-strategy` | 성장 루프와 GTM 모션 설계 | 해당 없음(고객이 우리 병원만인지 미정) | 라우터(`growth-loops`+`gtm-motions`). 고객 정의 후 |
| `pm-go-to-market:growth-loops` | 바이럴·사용·협업·UGC·리퍼럴 5가지 루프 평가 | 클리닉 간 레퍼럴로 확산되는 구조가 가능한지 검토(제품화 택할 경우) | 전제: 제품화 방향 확정 |
| `pm-go-to-market:gtm-motions` | 인바운드·아웃바운드·유료·커뮤니티·파트너·ABM·PLG 7가지 모션 선택 | 미용 클리닉 대상 판매를 학회·장비사 파트너 채널로 갈지 검토 | 전제: 제품화 방향 확정 |
| `pm-go-to-market:gtm-strategy` | 채널·메시징·성공지표·출시 타임라인을 담은 GTM 전략 | 사업 계획서의 시장 진입 장 | 전제: ICP·가격 확정. 7단계 |
| `pm-go-to-market:plan-launch` | 비치헤드 세그먼트·ICP·메시징·채널·런치 플랜 전체 | 위와 같음 | 라우터(`beachhead-segment`+`ideal-customer-profile`+`gtm-strategy`) |
| `pm-go-to-market:beachhead-segment` | 첫 진입 시장을 절박한 고통·지불의사·점유 가능성·추천 가능성으로 평가 | **피부과 vs 성형외과, 1인 원장 vs 다지점 중 어디부터 칠지 판단** | 입력: 세그먼트 후보(2단계 데스크 조사 산출물). 3단계 직후 유력 |
| `pm-go-to-market:ideal-customer-profile` | 리서치 데이터에서 ICP 도출 — 인구통계·행동·JTBD·니즈 | 「어떤 클리닉이 우리 AX 를 살 것인가」 — 미결 항목 「고객이 누구인가」의 답 | 입력: 리서치 데이터 필요. 3단계 인터뷰 후 |

## pm-market-research

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-market-research:competitive-analysis` | 경쟁 지형 분석 — 경쟁사 식별·강약점 비교·차별화 기회 | **미용 클리닉용 기존 솔루션(EMR·CRM·예약·상담봇 벤더) 지형 조사** | 짝 = `competitor-analysis`. **지금 바로 가능**(데스크 조사 본체) |
| `pm-market-research:competitor-analysis` | 경쟁사의 강점·약점·차별화 기회 분석, 직접 경쟁사 식별 | 위와 같음 | `competitive-analysis` 의 실체 |
| `pm-market-research:market-sizing` | TAM·SAM·SOM 을 탑다운·바텀업으로 추정 | **국내 피부과·성형외과 수 × 시스템 지출로 시장 규모 산출** — 사업 계획서 필수 장 | 입력: 공개 통계(심평원·건보공단 기관 수). **지금 바로 가능** |
| `pm-market-research:market-segments` | 3~5개 고객 세그먼트를 인구통계·JTBD·제품적합성으로 도출 | 클리닉을 규모·진료과·체인 여부로 세분하고 각 세그먼트의 운영 고통 정리 | **지금 가능**(가설 수준). 3단계 인터뷰로 검증 필요 |
| `pm-market-research:research-users` | 페르소나 구축·세그먼트·고객 여정 매핑을 한 번에 | 병원 내부 사용자(원장·실장·데스크) 전체 리서치 | 라우터(`user-personas`+`user-segmentation`+`customer-journey-map`). 입력: 리서치 데이터. 3단계 이후 |
| `pm-market-research:user-personas` | 리서치 데이터에서 JTBD·페인·게인·의외의 통찰을 담은 페르소나 3종 | 총괄실장·상담실장·데스크 페르소나 | **COO 직무기술서 1건이 있어 부분 착수 가능**하나 나머지는 3단계 인터뷰 필요 |
| `pm-market-research:user-segmentation` | 피드백 데이터에서 행동·JTBD·니즈 기반 3개 이상 세그먼트 | 병원 직군별로 AX 수용도가 갈리는 지점 분류 | 입력: 피드백 데이터. 3단계 이후 |
| `pm-market-research:customer-journey-map` | 단계·터치포인트·감정·페인포인트·기회의 엔드투엔드 여정 지도 | **환자 여정(문의→상담→시술→사후관리)과 직원 여정을 그려 병목 후보 도출** — 4단계 병목 식별의 주 도구 | 입력: 현장 관찰(3단계). 4단계의 핵심 도구 |
| `pm-market-research:analyze-feedback` | 대량 사용자 피드백 분석 — 감정·테마 추출·세그먼트별 인사이트 | 클리닉 리뷰 사이트·환자 후기에서 운영 불만 테마 추출 | 짝 = `sentiment-analysis`+`user-segmentation`. 공개 리뷰를 모으면 지금도 가능 |
| `pm-market-research:sentiment-analysis` | 피드백 데이터에서 세그먼트별 감정 점수·JTBD·만족도 | 위와 같음 | `analyze-feedback` 의 실체. 입력: 피드백 원문 |

## pm-marketing-growth

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-marketing-growth:market-product` | 마케팅 아이디어·포지셔닝·가치제안 문구·제품명을 묶은 창작 툴킷 | 해당 없음(제품 정의 전) | 라우터(아래 4개). 제품화 확정 후 |
| `pm-marketing-growth:marketing-ideas` | 채널·메시징·근거를 갖춘 저비용 마케팅 아이디어 5개 | 클리닉 대상 세미나·학회 부스 등 초기 영업 아이디어 | 제품화 확정 후 |
| `pm-marketing-growth:positioning-ideas` | 경쟁사와 차별화된 포지셔닝 문장과 근거 | 「차트 벤더가 아니라 운영 전환 파트너」 식 포지셔닝 후보 | 전제: 경쟁 지형 조사 완료 |
| `pm-marketing-growth:product-name` | 브랜드 가치·타깃에 맞는 제품명 5개 | AX 솔루션 제품명 | 가장 마지막. 지금 불필요 |
| `pm-marketing-growth:value-prop-statements` | 기존 가치제안에서 마케팅·세일즈·온보딩용 문구 생성 | 사업 계획서의 한 줄 가치 문장 | 입력: 확정된 가치제안. 7단계 |
| `pm-marketing-growth:north-star` | 노스스타 지표와 입력 지표 정의, 비즈니스 게임 분류 | AX 전환의 성공을 무엇으로 잴지 — 미결 항목 「목적」과 직결 | 짝 = `north-star-metric`. **목적(비용절감/매출증대/사람의존제거) 확정 직후 쓸 첫 스킬** |
| `pm-marketing-growth:north-star-metric` | 노스스타 1개 + 입력 지표 3~5개, 비즈니스 게임(Attention/Transaction/Productivity) 분류와 7기준 검증 | 위와 같음. 미용 클리닉은 Transaction·Productivity 중 어디인지가 쟁점 | `north-star` 의 실체 |

## pm-product-discovery

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-product-discovery:discover` | 아이디에이션→가정 매핑→실험 설계까지 디스커버리 전 과정 | 병목 하나를 골라 해결안까지 한 사이클 | 라우터(아래 다수). 전제: 병목 식별(4단계) |
| `pm-product-discovery:brainstorm` | PM·디자이너·엔지니어 관점의 아이디어/실험 브레인스토밍 | 병목별 해결안 발산 | 라우터(`brainstorm-ideas-*`/`brainstorm-experiments-*`) |
| `pm-product-discovery:brainstorm-ideas-new` | 신규 제품의 기능 아이디어를 3관점에서 발산 | AX 솔루션이 신제품이므로 이쪽. 병목 해결 기능 후보 도출 | 전제: 병목 목록(4단계) |
| `pm-product-discovery:brainstorm-ideas-existing` | 기존 제품의 기능 아이디어를 3관점에서 발산 | 직영 병원에 이미 깔린 시스템 위에 얹을 개선안 | 병원 기존 시스템 현황 조사 후 |
| `pm-product-discovery:brainstorm-experiments-new` | 신규 제품용 린스타트업 실험(프리토타입) — XYZ 가설·랜딩·사전예약 | 「클리닉이 월 N만원에 살 것이다」를 싸게 검증할 방법 설계 | 수익 구조 가설이 서면 사용 |
| `pm-product-discovery:brainstorm-experiments-existing` | 기존 제품 가정 검증용 실험 — 프로토타입·A/B·스파이크 | 직영 병원에서 돌릴 파일럿 설계 | 1단계 직영 전환과 맞물림 |
| `pm-product-discovery:identify-assumptions-new` | 신규 제품 아이디어의 리스크 가정을 GTM·전략·팀 포함 8개 범주로 | **미결 3건(목적·고객·수익)을 포함해 이 사업이 깔고 있는 가정 전부를 명시화** | 입력: 사업 구상 전사(이미 있음). **지금 바로 가능** |
| `pm-product-discovery:identify-assumptions-existing` | 기존 제품 기능의 리스크 가정을 Value·Usability·Viability·Feasibility 로 | 직영 병원 전환 항목별 리스크 | 1단계용 |
| `pm-product-discovery:prioritize-assumptions` | 가정을 Impact × Risk 매트릭스로 우선순위화하고 실험 제안 | 위에서 뽑은 가정 중 무엇부터 검증할지 — 3단계 인터뷰 질문의 근거 | 입력: `identify-assumptions-new` 산출물. 그 직후 |
| `pm-product-discovery:interview-script` | The Mom Test 원칙의 JTBD 인터뷰 대본(유도질문 금지·과거 행동 중심) | **3단계 병원 직원 인터뷰 대본** — 원장·실장·데스크별 | 입력: 주제·대상. **지금 준비 가능**(3단계 직전 필수) |
| `pm-product-discovery:summarize-interview` | 인터뷰 전사를 JTBD·만족 신호·액션아이템 구조로 요약 | 3단계 인터뷰 전사 정리 | 입력: 인터뷰 전사. 3단계 수행 후 |
| `pm-product-discovery:interview` | 인터뷰 대본 준비 또는 전사 요약 | 위 두 개를 한 커맨드로 | 라우터(`interview-script`+`summarize-interview`) |
| `pm-product-discovery:opportunity-solution-tree` | 성과→기회→솔루션→실험을 잇는 OST(Teresa Torres) | **4단계 병목을 기회로 놓고 5·6단계 우선순위까지 한 장에 잇기** | 입력: 성과 정의(= AX 목적) + 병목 목록. 4~6단계의 뼈대 |
| `pm-product-discovery:analyze-feature-requests` | 기능 요청을 테마·전략정합·임팩트·공수·리스크로 분석·우선순위화 | 병원 직원들이 쏟아낼 「이것 좀 자동화해달라」 목록 정리 | 입력: 요청 목록(3단계 부산물) |
| `pm-product-discovery:triage-requests` | 고객·이해관계자 기능 요청 묶음을 분류·우선순위화 | 위와 같음 | 라우터(`analyze-feature-requests`+`prioritize-features`) |
| `pm-product-discovery:prioritize-features` | 임팩트·공수·리스크·전략정합으로 백로그 순위와 상위 5개 추천 | **6단계 작업 우선순위 설계의 실행 도구** | 입력: 후보 목록 + 기회비용 산출(5단계) |
| `pm-product-discovery:metrics-dashboard` | 핵심 지표·데이터 소스·시각화·알림 임계값을 갖춘 대시보드 설계 | AX 전환 효과 추적 대시보드(대기시간·상담 전환·야근시간) | 짝 = `setup-metrics`. 전제: 노스스타 확정 |
| `pm-product-discovery:setup-metrics` | 노스스타·입력지표·헬스지표·알림 임계값 대시보드 설계 | 위와 같음 | `metrics-dashboard` 의 라우터 |

## pm-product-strategy

| 스킬이름 | 스킬설명 | 적용예시 | 비고 |
|---|---|---|---|
| `pm-product-strategy:market-scan` | SWOT·PESTLE·Porter 5 Forces·Ansoff 를 한 번에 돌리는 거시 환경 분석 | **미용 의료 시장 거시 분석 — 비급여 규제·의료광고 심의·인건비 상승·AI 의료기기 규제** | 라우터(아래 4개). **지금 바로 가능**, 데스크 조사 핵심 |
| `pm-product-strategy:swot-analysis` | 강점·약점·기회·위협과 실행 권고 | 직영 병원을 가진 것이 강점인지(레퍼런스) 약점인지(경쟁 클리닉이 안 삼) 정리 | `market-scan` 구성요소. 단독 사용도 가능 |
| `pm-product-strategy:pestle-analysis` | 정치·경제·사회·기술·법률·환경 6요인 분석 | 의료법·개인정보보호법·비급여 고지 의무 등 법률 요인이 AX 범위를 어디서 막는지 | `market-scan` 구성요소. **지금 가능**, 의료업 특성상 Legal 비중 큼 |
| `pm-product-strategy:porters-five-forces` | 경쟁강도·공급자·구매자 교섭력·대체재·신규진입 위협 | 병원 SW 시장의 교섭력 구조(차트 벤더 락인, 원장의 구매력) | `market-scan` 구성요소. **지금 가능** |
| `pm-product-strategy:ansoff-matrix` | 시장침투·시장개발·제품개발·다각화 성장 경로 매핑 | **「우리 병원만」 vs 「남에게 판다」 — 미결 항목 「고객이 누구인가」를 성장 경로로 정리** | `market-scan` 구성요소. 미결 사항 정리에 직접 유용 |
| `pm-product-strategy:strategy` | 9섹션 Strategy Canvas 로 제품 전략 작성 | 사업 계획서의 전략 장 골격 | 짝 = `product-strategy`. 전제: 조사 완료. 7단계 |
| `pm-product-strategy:product-strategy` | 비전·세그먼트·비용·가치제안·트레이드오프·지표·성장·역량·방어력 9섹션 | 위와 같음 | `strategy` 의 실체 |
| `pm-product-strategy:product-vision` | 팀을 움직이는 제품 비전 문장 도출 | AX 전환의 비전 문장 — 미결 「목적」을 말로 굳히는 데 | 입력 가벼움. 목적 논의의 촉매로 지금도 가능 |
| `pm-product-strategy:business-model` | Lean Canvas·BMC·Startup Canvas·Value Proposition 중 골라 비즈니스 모델 탐색 | 사업 계획서의 비즈니스 모델 장 | 라우터(아래 3개 + `value-proposition`) |
| `pm-product-strategy:lean-canvas` | 문제·솔루션·지표·비용·UVP·불공정우위·채널·세그먼트·수익 1장 | **가진 자료 2건으로도 채울 수 있는 첫 한 장** — 빈칸이 곧 미결 목록 | **지금 가능**. 빈칸을 남기는 용도로 쓰면 조사 범위가 잡힘 |
| `pm-product-strategy:business-model` (skill) | Business Model Canvas 9블록 생성 | 직영 병원 + 외판 두 모델을 각각 그려 비교 | `business-model` 커맨드의 실체 중 하나 |
| `pm-product-strategy:startup-canvas` | 제품 전략 9섹션 + 비용·수익을 합친 캔버스(BMC·Lean 대안) | 신규 사업이므로 이쪽이 적합. 전략과 BM 을 분리해 볼 때 | 조사 후 7단계 |
| `pm-product-strategy:value-proposition` | Who·Why·What before·How·What after·Alternatives 6부 JTBD 가치제안 | 「총괄실장의 어떤 일을 없애주는가」를 6칸으로 | 짝 = 동명 skill. 입력: 대상 직무 이해. COO JD 로 부분 착수 가능 |
| `pm-product-strategy:value-proposition` (skill) | 6부 JTBD 템플릿 상세 가치제안 설계 | 위와 같음 | 커맨드의 실체 |
| `pm-product-strategy:pricing` | 가격 모델·경쟁 가격 분석·지불의사 추정·가격 실험 | 미결 항목 「수익 구조와 가격」 | 짝 = `pricing-strategy`. 전제: 고객·가치 확정. 지금 못 씀 |
| `pm-product-strategy:pricing-strategy` | 가격 모델·경쟁 가격·지불의사·가격 탄력성 분석 | 위와 같음 | `pricing` 의 실체 |
| `pm-product-strategy:monetization-strategy` | 수익 모델 3~5개를 대상 적합성·리스크·검증 실험과 함께 | **미결 「수익 구조」의 선택지를 펼치는 용도** — 구독·성과과금·내부원가절감 | 가격보다 먼저 옴. 고객 정의가 어느 정도 서면 사용 |

## 지금 단계(2단계 데스크 조사)에서 바로 쓸 수 있는 스킬

가진 자료 두 건(사업 구상 대화 전사, COO 직무기술서)과 공개 자료만으로 결과가 나오는 것만 골랐다. 인터뷰·현장 관찰 결과가 있어야 하는 스킬은 뺐다.

1. **`pm-execution:meeting-notes`** — 사업 구상 전사에서 이미 정해진 것과 미결(목적·고객·수익)을 문서로 분리한다. 입력이 이미 손에 있는 유일한 스킬이고, 나머지 조사의 범위를 여기서 정한다.
2. **`pm-product-discovery:identify-assumptions-new`** — 1번에서 나온 미결을 8개 범주의 가정으로 명시화한다. 「AI 로 사람 의존을 없앨 수 있다」처럼 말해지지 않은 전제를 끄집어내야 데스크 조사가 무엇을 확인하러 가는지 정해진다.
3. **`pm-product-strategy:market-scan`** (특히 `pestle-analysis`·`ansoff-matrix`) — 미용 의료 시장의 규제·경제 요인을 훑는다. 비급여·의료광고 심의 같은 법률 제약이 AX 범위를 어디서 자르는지가 먼저 나와야 이후 설계가 헛돌지 않는다. Ansoff 는 「우리 병원만 vs 외판」 미결을 성장 경로로 정리해준다.
4. **`pm-market-research:market-sizing`** — 국내 피부과·성형외과 기관 수와 시스템 지출로 TAM/SAM/SOM 을 낸다. 사업 계획서에 반드시 들어가고, 공개 통계만으로 산출 가능하다.
5. **`pm-market-research:competitor-analysis`** — 미용 클리닉용 기존 EMR·CRM·예약·상담 솔루션 지형을 그린다. 「병원 시스템 현황」 조사의 절반은 이미 파는 사람들이 무엇을 파는지 보는 일이다.

3단계 인터뷰에 들어가기 직전 준비물로 `pm-product-discovery:interview-script` 와 `pm-execution:stakeholder-map` 을 붙여 쓰면 되지만, 산출물이 아니라 준비물이라 위 목록에는 넣지 않았다.
