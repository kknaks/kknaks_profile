# [backend] 읽기 전용 점검 — 화면에 나오는 모든 값의 KOS API 원천

사용자 원칙(2026-10-13): **「실제 존재하는 API(필드)로만 만든다.」** 데이터에 없는 것을 추정해 채우지 않는다.
계기: 환자 상세 「오늘 오더」 출처에 「상담실장 민현우」를 붙였는데 `orderMemo` 에는 작성자 칸이 없다(`app/service/patient_service.py:82` — `consultation.counselor` 를 작성자처럼 씀).

## 할 것 — 코드 수정 금지, 리포트 1개만

`cc/back` 의 모든 읽기 응답(`/api/staff` · `/api/board` · `/api/staff/{id}/home` · `/api/patients/{id}` · 접수 모달용 값 · 시드 build 가 만드는 상태)에서 **front 가 화면에 보여 주는 값 하나하나**를 표로:

| 화면 · 칸 | 응답 필드 | KOS 원천(API · 필드 경로) | 판정 |
|---|---|---|---|

판정은 셋 중 하나:
- **그대로** — KOS 필드 값을 그대로(형식 변환 · 고객명 치환만)
- **가공** — KOS 필드 값에서 계산 · 자르기(예: 메모 양식 줄 고르기, 생년월일→나이). 규칙 한 줄
- **추정** — KOS 에 그 정보가 없는데 다른 필드로 짐작(예: 작성자 = 상담 담당자, 직군 = 이름이 나온 칸). **왜 추정인지 한 줄**

시드 재구성(14:45 위치 · 단계 · 직원 큐 · since)과 현황판 계산(상태 라벨 · 대기 라벨)도 같은 표에. 고정 문구(시안 UI 글자)는 빼도 된다.

## 범위

- 읽기만. `cc/back` · `cc/front` 수정 금지. 서버를 띄운다면 임시 포트 · 별도 DB(사용자 E2E 중인 8600 · `data/cc.db` · `seed.json` 금지). 커밋 금지. KOS API 호출 금지
- front 가 무엇을 보여 주는지는 `cc/front/lib/types.ts` 와 화면 컴포넌트를 읽어서

## 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/api-source-audit-report.md` — 위 표 + 맨 위 요약(추정 N개 목록 · 가공 N개 목록)

완료 보고는 WP2 브리프 §5 두 명령 그대로(subject 「backend 완료: API 원천 점검 …」, taskId/dispatchId 는 WP2 것 task_edd69d808493 / ctx_8a10efa14b88).
