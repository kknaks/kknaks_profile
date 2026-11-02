# KOS 직원 · 직군 조회 API 확인 (2026-10-13)

- 점검자: cc-prototype `backend` 워커. 코드(`cc/back/app`) 수정 없음 · 8600 · `data/cc.db` · `seed.json` 안 건드림
- **KOS 호출: 2회 — 인증 교환 1회 + `getAccounts` 1회.** 쓰기 · 수정 · 삭제 호출 없음. 키 · 토큰은 출력 · 저장하지 않았다

## 결론

- **조회 전용 직원 목록 작업이 있다 — `getAccounts`(직원 목록 조회).** 다만 2026-09-18 스냅샷(73개)에는 없고, **현재 공개 스펙(`https://developers.kos-solution.com/openapi.yaml`, 75개)에 새로 생겼다**(새 작업 2개: `getAccounts` · `changeReservationMemo` — 뒤의 것은 `/commands/` 쓰기라 손대지 않음)
- 1회 호출로 직원 **88명**(활성 65 · 비활성 23)을 받아 `cc/back/data/kos-staff.json` 에 저장했다(gitignore 폴더)
- **10-09 일정에 나오는 직원 22명(id) 전부가 목록에 있고, 22명 모두 `roleTags` 가 채워져 있다.** 이름도 22명 모두 일정 쪽 이름과 같다
- ⚠ 그런데 **KOS 직군은 7종 태그(복수 가능)라 현황판 직군 3종(의사 · 상담사 · 코디)과 1:1 이 아니다.** 지금 시드가 「코디」로 묶은 시술 담당 7명은 KOS 로는 **간호사(NURSE) 4명 · 스킨케어(SKINCARE) 3명**이다 → 정할 것 1

## 1. 후보 작업

| 항목 | 값 |
|---|---|
| operationId | `getAccounts` — summary 「직원 목록 조회」, 설명 「병원에 등록된 직원 목록을 조회합니다. 예약을 생성할 때 `reservationAssigneeId`에 넣을 직원 ID를 찾는 데 사용합니다.」 |
| 경로 | `POST /account/open/v1/queries/get-accounts` (태그 `Account`) |
| 요청 | `protos.open.OpenGetAccountsQuery` — `activate`(bool, 선택: 활성/비활성 필터) · `roleTag`(선택: 역할 태그 필터, `ROLE_TAG_UNSPECIFIED` 는 400). **둘 다 생략 = 전체**. 페이지 필드 없음 |
| 응답 | `data[]` = `protos.open.OpenAccount` — `id`(object-id) · `name` · `email` · `activate` · `roleTags[]` |
| `roleTags` 값 | `ADMIN` 관리자 · `DOCTOR` 의사 · `COUNSELOR` 상담사 · `NURSE` 간호사 · `SKINCARE` 스킨케어 · `CALL_COUNSELOR` 콜 상담사 · `COORDINATOR` 코디네이터 (+ `ROLE_TAG_UNSPECIFIED`) |
| 역할 **이름** | 응답에 없다(태그만). 역할 이름(예: 「코디」)은 `getScheduleDetail` 의 `etceteraWorks[].assignees[].role.name` 에만 있다 |

**조회 전용 근거**
- 경로가 `/queries/` (스펙의 모든 변경 작업은 `/commands/` — 이번 공개 스펙도 같음)
- 이름 `get…`, summary 「…조회」, 요청에 필터 두 개뿐(쓰는 값 없음)
- 스크립트 규칙(`kos_collect.py:120-126` — `/queries/` 가 아니면 막음)에도 맞는다. 다만 스냅샷 기반 `kos_query_catalog.py` 에는 아직 없는 작업이라, 스크립트 대신 **경로 두 개만 허용하는 1회용 스크립트**(레포 밖 스크래치)로 불렀다

**스냅샷 · 가이드에서 찾은 것(참고)**
- 가이드 · 스냅샷 73개 작업 중 직원 · 계정 목록 작업은 **없다**
- 스냅샷의 `protos.schedule.flow.FlowTaskAssignee`(작업 담당자)는 스키마상 `role`(필수, `AccountRoleV2Contract` = 역할 id · 이름 · roleTags)을 갖는데, **실제 캡처 응답의 `tasks[].assignees[]` 에는 `id · name` 만 있다**(719작업 전부). 그래서 일정 데이터로는 시술 담당자 직군을 알 수 없었다 — 이번 `getAccounts` 로 메워진다

## 2. 키

- `ax-clinic-project/scripts/kos_collect.py:80-106` `load_credentials` — 같은 폴더 `scripts/.env` 에서 `KOS_API_KEY` 또는 `KOS_API_tenent`(UUID), 또는 `KOS_AUTH_TOKEN` 을 읽는다(환경변수가 있으면 그쪽 우선)
- 실제 `scripts/.env` 에는 `KOS_API_tenent` 가 있다(값은 보지 · 출력하지 않음). 인증은 `POST /open/authorization/commands/exchange-token {key}` → `Authorization: <token>`(Bearer 없음)

## 3. 호출

| # | 경로 | 결과 |
|---|---|---|
| 1 | `POST /open/authorization/commands/exchange-token` | 200 (토큰은 메모리에만) |
| 2 | `POST /account/open/v1/queries/get-accounts` 요청 `{}` | 200 · 12,471 바이트 · 88명 → `cc/back/data/kos-staff.json` 에 응답 원문 그대로 |

⚠ 응답에 **직원 이메일**이 들어 있다. `data/` 는 gitignore 지만, 앱이 쓰게 되면 이메일은 응답에 내보내지 말 것.

전체 88명 `roleTags` 분포: (CALL_COUNSELOR · COUNSELOR · COORDINATOR) 19 · (CALL_COUNSELOR) 17 · (ADMIN · NURSE · SKINCARE · CALL_COUNSELOR · COORDINATOR) 9 · (DOCTOR) 9 · (COUNSELOR) 8 · (NURSE) 8 · (SKINCARE) 7 · (ADMIN) 7 · (ADMIN · DOCTOR) 1 · (COUNSELOR · ADMIN) 1 · (COUNSELOR · NURSE · SKINCARE · COORDINATOR) 1 · (COORDINATOR) 1

## 4. 10-09 직원 대조

10-09 일정(27건)의 모든 이름 칸에서 id 를 모았다(`tasks[].doctors` · `calledDoctors` · `assignees` · `consultations[].counselors` · `etceteraWorks[].assignees` · `reservation.reservationAssignee`). **22명 · 목록에 없는 사람 0 · 이름 다른 사람 0.**

| 이름 | 일정에서 나온 칸 | KOS `roleTags` | 활성 | 지금 시드 직군 | 같은가 |
|---|---|---|---|---|---|
| 권태윤 | doctors · calledDoctors | ADMIN · DOCTOR | ○ | 의사 | 같음 |
| 임윤서 | doctors · calledDoctors | DOCTOR | ○ | 의사 | 같음 |
| 원다은 | doctors · calledDoctors | DOCTOR | ○ | 의사 | 같음 |
| 이지우 | doctors · calledDoctors | DOCTOR | ○ | 의사 | 같음 |
| 마취용 | doctors | DOCTOR | ○ | (뺌, D-22) | 계정은 실제로 DOCTOR 다 — 사람이 아니라 계정으로 보는 D-22 판단은 그대로 |
| 오현우 | counselors | COUNSELOR | ○ | 상담사 | 같음 |
| 민현우 | counselors | COUNSELOR | ○ | 상담사 | 같음 |
| 류하린 | counselors | COUNSELOR | ○ | 상담사 | 같음 |
| 강도윤 | assignees | **NURSE** | ○ | 코디 | **다름** |
| 류하람 | assignees | **NURSE** | ○ | 코디 | **다름** |
| 유채원 | assignees | **NURSE** | ○ | 코디 | **다름** |
| 서가온 | assignees | **NURSE** | ○ | 코디 | **다름** |
| 송지호 | assignees | **SKINCARE** | ○ | 코디 | **다름** |
| 안건우 | assignees | **SKINCARE** | ○ | 코디 | **다름** |
| 서채원 | assignees | **SKINCARE** | ○ | 코디 | **다름** |
| 심준서 | etceteraWorks · reservationAssignee | CALL_COUNSELOR · COUNSELOR · COORDINATOR | ○ | 코디 | 같음(COORDINATOR) — 단 COUNSELOR 태그도 있음 |
| 주태윤 | etceteraWorks · reservationAssignee | CALL_COUNSELOR · COUNSELOR · COORDINATOR | ○ | 코디 | 같음(위와 같음) |
| 곽태린 | etceteraWorks · reservationAssignee | CALL_COUNSELOR · COUNSELOR · COORDINATOR | ○ | 코디 | 같음(위와 같음) — 시연 코디 계정 |
| 차예린 | reservationAssignee | CALL_COUNSELOR · COUNSELOR · COORDINATOR | ○ | (직원 목록에 없음) | — |
| 남준서 | reservationAssignee | CALL_COUNSELOR · COUNSELOR · COORDINATOR | ○ | (없음) | — |
| 김예린 | reservationAssignee | CALL_COUNSELOR | ○ | (없음) | — |
| 데스크1 | reservationAssignee | CALL_COUNSELOR · COUNSELOR · COORDINATOR | ✗ 비활성 | (없음) | — |

- **직군이 다 채워지나 → 태그는 22명 모두 채워진다.** 다만 현황판 3직군으로 옮기는 규칙이 필요하다(아래)
- 지금 시드(필드 위치 추정, E5)와 비교: 의사 4 · 상담사 3 · 코디(etceteraWorks) 3 은 KOS 와 맞고, **시술 담당 7명은 코디가 아니라 간호사 · 스킨케어**다

## 정할 것 — 코디 · 사용자

1. **현황판 직군을 어떻게 맞출까.** 선택지:
   - (a) 현황판 직군을 KOS 태그로 넓힌다 — 의사 · 상담사 · **간호사 · 스킨케어** · 코디. 시안의 직군 3종(점 색 · 직군 탭 · 오더 단계의 담당 직군)과 시술 단계 직군(지금은 의사/코디)을 손봐야 한다
   - (b) 3종 유지, 태그 → 직군 규칙을 정한다 — 예: DOCTOR → 의사 / COUNSELOR 만 → 상담사 / COORDINATOR → 코디 / NURSE · SKINCARE → ? (코디로 묶으면 지금과 같지만 「KOS 값으로」 원칙과 이름이 어긋남)
   - 태그가 여러 개인 사람(예: 심준서 · 주태윤 · 곽태린 = CALL_COUNSELOR · COUNSELOR · COORDINATOR, 권태윤 = ADMIN · DOCTOR)의 우선순위도 정해야 한다
2. **직원 목록 범위** — 지금은 「10-09 일정에 나온 사람」이다. `getAccounts` 는 병원 전체 88명(비활성 23 포함)을 준다. 시연 직원 목록을 그날 등장 인원으로 둘지, 활성 전원으로 둘지
3. **시드에 넣는 방법** — 시드 build 가 KOS 를 부르지 않는다는 원칙(SPEC §1 · §3)과 맞추려면, 이번 저장본 `data/kos-staff.json` 을 캡처처럼 **입력 파일**로 읽게 하는 게 자연스럽다(코드 수정은 이번 범위 밖)
4. 이메일은 앱 응답에 내보내지 않는다
