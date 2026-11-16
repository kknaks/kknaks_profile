# [planner] 2차(add1) — 외부 API 3개 추가: DEC-011 · SPEC-008 0.3.0 · WORK-013

원 브리프(`api-swagger-docs-spec-brief.md`) 제약 그대로(public 레포 · 실명/이메일/KOS id/키 값 0 · 브리프가 지정한 파일만 · 커밋 금지). 완료 보고는 원 브리프 §9 두 채널.

## 배경 (협업자 요청 원문 요지)

링키 · 차티가 이미 배포된 `/api/ext/*`(메뉴 · 조회 · 예약)에 더해 세 개를 요청했다.

1. 특정일 예약 가능 시간대 — 보냄: 날짜 `YYYY-MM-DD` / 받음: 그날 예약 가능 시간대 목록
2. 고객 과거 시술 — 보냄: 이름 · 이메일 / 받음: 방문 목록, 최신 순
3. 예약 내역 — 보냄: 이름 · 이메일 / 받음: 그 고객의 예약 목록

## 사용자 승인된 결정 (2026-11-12 · 코디 추천 그대로) → DEC-011 로 쓴다

- **D-01** 셋 다 외부 연동 API(`/api/ext/*`). 인증(`X-Api-Key`) · 키당 호출 제한 · `ext_call` 기록 · `Cache-Control: no-store` · Swagger tag 「외부 연동」 · 오류 모양은 DEC-010 그대로 공유.
- **D-02** 가능 시간대 = **외부 예약 기본 그룹(DEC-010 env 그룹) 하나만**. 칸 = 그 그룹 시간 간격. 칸마다 시작 시각 · 남은 자리 수. 남은 자리 0 칸은 뺀다. 오늘이면 이미 지난 시각은 뺀다. 남은 자리 계산은 **예약 생성의 정원 검사와 같은 규칙**(이 목록의 시각으로 예약하면 정원 때문에 거절되지 않아야 한다 — 동시 요청 경합만 예외).
- **D-03** 과거 시술 = 지금보다 앞선 KOS 일정, 최신 순. 칸 = 날짜 · 시작 시각 · 결과(직원 「이전 방문」의 결과 분류 그대로) · 시술 이름 목록. **예약 메모 · 상담 메모 · 의사 이름은 내지 않는다.**
- **D-04** 예약 내역 = 오늘(KST) 이후 일정, 시각 오름차순, 상태(취소 포함). 지난 일정은 D-03 에서.
- **D-05** 고객 찾기 = DEC-010 조회 규칙 그대로(D-16 · D-17 · D-19 등). 고객 없음 · 틀린 입력 = 조회와 바이트까지 같은 404.
- **D-06** 이름 · 이메일은 URL 에 두지 않는다(본문 POST — 조회와 같은 이유).

## 코디 기본값 (DEC 에 「코디 기본값」으로 표시)

- 경로: `GET /api/ext/availability?date=YYYY-MM-DD` · `POST /api/ext/customers/visits` · `POST /api/ext/customers/reservations`. 더 나은 이름이 코드 관례상 있으면 질문으로.
- 날짜 범위: 오늘(KST) ~ 90일. 과거 · 범위 밖 · 형식 틀림 = 400(기존 오류 code 체계에서 고른다 — 없으면 질문).
- 과거 시술 개수: 최근 50건까지.
- 기본 그룹 env 빔 · 그룹 없음 · 켜진 구역 0 = 가능 시간대도 `503 ext_not_configured`(KOS 부르기 전).

## 사실 확인 — 코드에서 (지어 넣지 말 것)

코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs/procedure/back` (main `e0e4a16` · 읽기만)
- 정원 · 칸: `app/service/reservations.py` 예약표(`intervalMinutes` · `capacities` · `open` · `lines()` · `enabled_zones`) · 예약 생성 정원 검사(약 820 · 950줄 근처)
- 과거 방문: 같은 파일 `previous_visits()` · `PREV_RESULT` · 이것을 부르는 곳과 KOS 고객 일정 호출(어느 KOS 작업 · 호출 수)
- 예약 상태 값 · 우리 예약 id 와 KOS 일정의 관계(우리 DB 에 없는 KOS 예약을 어떻게 낼지) — 사실을 보고 칸을 정하되, 정책이 필요하면 질문
- 기존 외부 API: `app/api/ext.py` · `app/service/ext.py` · `app/schemas/ext.py` · SPEC-008 0.2.3

## 산출

- `para/projects/summer-star/cc-prototype/10-decision/decision-011-ext-api-add1.md` (accepted · 열린 것 0 · DEC-010 연결)
- `20-spec/spec-008-product-ext-api.md` → **0.3.0**: 세 경로 계약(요청 · 응답 칸 · 오류 표 · 시험 T 번호 이어서) · 변경 이력
- `30-work/work-013-ext-api-add1.md`: backend WP(부분 검증 명령 포함) · 끝 조건에 데모 KOS 실물 호출
- 세 README · `work-index.md` 행

KOS 호출 비용(요청 1번당 KOS 호출 수)을 경로마다 SPEC 에 적는다.
