# researcher 2차 — 병원 정보 · 직원 목록 원천

너는 cc-prototype `researcher` 워커다. 원 브리프(`ext-api-charty1-research-brief.md`)의 제약이 **그대로** 유효하다: 데모 키(`KOS_API_tenent_dev`)만 · 조회만(쓰기 0) · public 이라 이름 · 이메일 · id 값 · 키는 적지 않고 모양 · 건수만 · 리포트 1개만 · 코드는 `git show origin/main:`.

## 배경

연동처(linky · charty 공통)가 두 API 를 원한다. ① 병원 정보 ② 그 병원 직원 목록. 직원에는 병원 직원과 **외주 직원**이 같이 있다. 외주 직원은 KOS 계정으로 있고, KOS 웹 계정 화면에서 권한 칸이 「CS팀(콜센터)」로 보인다(사용자 확인).

## 알아낼 것

1. **병원 정보** — KOS 공개 스펙(openapi 1.0.1)에 병원 · 테넌트 · 지점 정보를 주는 조회가 있나. 있으면 작업 이름 · 칸 전체 키 트리 · 데모 실호출 모양. 없으면 내부 API(HAR 7+1개 · `상담대기.har` 의 그룹 · 코드 · 통화 · 부가세 조회 등)에 있나. 그것도 없으면 CC 설정(`config.py` · 구역 · 그룹)으로 낼 수 있는 칸이 무엇인가
2. **직원 목록** — 공개 `get-accounts` 응답 전체 키 트리(데모 실호출). 「CS팀(콜센터)」 같은 권한 · 역할이 `roleTags` 로 오나, 다른 칸으로 오나, 안 오나. 관찰된 역할 값 종류와 건수(값 이름은 KOS 역할 이름이면 적어도 됨 · 사람 이름 · 이메일 금지). 활성 · 비활성 건수
3. **지금 CC** — `staff` 사본 동기화(`kos/sync.py`)가 무엇을 버리는지(`kos_exclude_account_ids` 포함), 직원 API 중 직원 목록을 내는 곳이 있는지(파일:줄)

## 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/research-clinic-staff.md`
- 맨 위 요약: 질문 1~3 한 줄 답 + 분류(A~E · 1차와 같은 표기)
- 정할 것(결정하지 않고 모음)

완료 보고는 원 브리프 §9 의 두 채널 그대로.
