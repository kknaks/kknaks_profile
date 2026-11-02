# 소재 — 슬랙 에러 채널 → incident 어댑터 (후속 작업 입력, 2026-08-31 확보)

> OQ-10(실전 error event 스키마)·OQ-15(인바운드 어댑터)의 실물 소재. 사용자 제공 샘플 3건 기준.

## 채널

- **#900-prod-error-alerts** — prod. **어댑터 대상 (확정)**
- #901-stg-error-alerts — stg. **제외 (확정)**
- 발신자: "Error Alert" 봇 앱 (Block Kit 필드 게시)
- 참고: 사이드바에 `incident-9fedb85e` 채널 존재 — 구 채널명 형식(uuid8) 잔재로 보임 (현행 규칙 = `incident-{label}-{yyyymmdd-HHmm}`)

## 메시지 형식 2종 (실측)

### A. HTTP 에러
- 헤더: `🚨 {제품} {ENV} 에러 발생` (예: WATCH PROD, CHARTY STG)
- 필드: 상태(`500 (Unhandled Exception)`) · 시간(KST) · `request_id` · 엔드포인트(`POST /api/v1/...`) · 에러 본문 · IP/UA
- 제품별 추가 필드: CHARTY 는 tenant·user_id·role 추가 — **필드 집합이 제품마다 가변**
- 꼬리: `💡 로그 검색:` + grep 명령(키 = request_id). CHARTY 는 traces 쿼리 형식 — **꼬리도 가변**

### B. 워커(TASKIQ) 에러
- 헤더: `🚨 {제품} {ENV} · TASKIQ`
- 필드: Queue · Task(경로) · `task_id` · Exception(클래스) · Retry class · Attempt(`1/1`) · Duration(ms) · 에러 본문
- 꼬리: 로그 검색(키 = task_id)

## 확정 결정 (2026-08-31)

1. **승격 = 전건 자동.** #900 에 메시지가 쌓이면 그대로 `POST /incidents/raise` → AI 수집 → is_lead 승인 게이트. **게이트가 사람 필터다** — 그 앞에 이모지 지목 등 사전 필터를 두지 않는다
2. **환경 = prod(#900)만.** stg 는 개발 이슈로 별도
3. 수신 방식 = 봇을 #900 에 초대 + Events API `message.channels` 구독 (기존 `/slack/events` 라우터·서명검증 인프라 재사용). 제품별 에러 리포터 수정 없이 채널 하나 구독으로 전 제품 커버
4. 진입 = `source=slack_error_channel` (raise 의 source 확장 축 — 계약 이미 open)

## 어댑터 설계 시 열린 것 (스펙 단계 OQ 후보)

- 파싱: 헤더에서 제품·환경 추출, 필드 라벨 기반 파싱(가변 필드는 raw 로 보존해 AI 수집 입력으로). 파싱 실패 시에도 **raw 본문으로 raise** (유실 금지)
- 중복: `request_id`/`task_id` 가 자연 dedupe 키 — 같은 키 재게시 처리 규칙(스펙에서)
- Error Alert 봇 메시지만 필터(사람 잡담 제외) — bot_id/앱 식별
- scope 매핑: 제품명(WATCH·CHARTY·…) → scope_slug 매핑 표 필요 (mediness 외 제품 에러도 이 채널에 온다 — mediness 것만? 전 제품? **미정**)
