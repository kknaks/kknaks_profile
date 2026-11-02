# [researcher] 예약 현황 조회 — HAR 내부 API ↔ KOS 공개 API 대조 (read-only 조사)

너는 **cc-prototype `researcher` 워커**다. 먼저 역할 문서를 읽어라: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`). 완료 보고는 아래 §7. **앞 판(디자인 분석)의 맥락은 아래 파일로만 이어받는다.**

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 지정한 리포트 밖은 건드리지 마라)

## 1. 무엇을 하나

시안의 「현황 › 예약 현황」 화면을 **KOS 에서 읽어 올 수 있는지** 확인한다. 이번 판은 **조회만** — 쓰기(등록 · 이동 · 취소 · 접수 · 방 배정)는 다음 판.

사용자가 KOS 웹 「예약 현황」 화면을 열고 뜬 HAR 이 하나 있다. 그 안의 내부 API 와 KOS 공개 API 를 대조해, **시안의 조회 필드마다 어디서 가져오는지**를 적는다.

## 2. 읽을 것 (절대경로 · read-only)

- HAR: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/예약현황_조회.har` (gitignore — 고객 정보 · 토큰 · 테넌트 id 포함)
  - KOS 요청 15건 · 내부 API 11종: `get-schedules-for-reservation` · `get-reservation-groups` · `get-reservation-group-days-offs` · `get-occupied-times` · `get-default-operation-timetable` · `get-default-days-off` · `get-rooms` · `get-accounts` · `get-accounts-last-update-date-time-utc` · `get-roles` · `get-notices`. **이 목록으로 끝내지 말고 HAR 의 KOS 요청을 직접 전부 세어 대조하라**
- 시안 조회 필드: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/design-analysis-report.md` §3(예약 현황 전체) · **§7.2(필드 목록 — 이게 대조의 행)**
- KOS 공개 API: `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` · 호출 예 `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py`
- 이미 아는 것: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-12-cc-prototype/kos-demo-api.md` · `workflow-v2.md`(「KOS 반영 표」 · 「인증 · 계정」) · `workflow-v1.md`(1 · 2절 — `visitor.isNew` 등)

## 3. 할 일

1. **HAR 인벤토리**: KOS 요청마다 메서드 · 경로(테넌트 id 는 `{tenantId}`로) · 요청 본문 키 · 응답 최상위 구조 · 화면에서 무슨 용도로 보이는지.
2. **공개 API 짝 찾기**: 내부 API 마다 같은 정보를 주는 공개 API 가 있나(이름 · 필드 차이). 없으면 「공개 API 없음」.
3. **시안 필드 대조표**(§7.2 의 행 전부 + 범례 상태 7개 · 권역 5칸 · 「원내 현황」 탭 카드 · 공지): 필드마다
   - `공개 API`(API · 필드 경로) / `내부 API`(HAR 경로 · 필드 경로) / `KOS 에 없음` 중 하나. 둘 다 있으면 둘 다
   - KOS 값 ↔ 시안 값의 모양 차이(예: 상태 = `flowStep` 8개 ↔ 시안 7개, 권역 = KOS 의 무엇?)
   - **값을 다른 필드로 추정해 채우지 마라.** 「국적으로 권역을 계산할 수 있다」 같은 건 `KOS 에 없음` + 「정할 것」에 적는다
4. **데모 지점 실제 조회**: 대조표에서 쓰는 **공개 API 는 데모 키(`scripts/.env` 의 `KOS_API_tenent_dev`)로 한 번씩** 호출해 필드가 실제로 오는지 확인. 내부 API 는 `workflow-v2.md` 「인증 · 계정」 방식(시스템 계정 sign-in → Bearer)으로 **조회 API 만** 한 번씩. 계정 값은 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/.env` 를 읽기만(출력 · 리포트에 값 금지). 날짜는 오늘(2026-10-26 KST) 하루.
   - 호출마다: 경로 · 결과 코드 · 건수 · 확인한 필드. 실패하면 응답 그대로(값 가려서)
5. 「정할 것」: KOS 에 없는 필드 · 모양이 안 맞는 자리 · 권역 같은 결정 거리. **결정하지 마라.**

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-read-report.md` — 리포트 1개. 임시 스크립트 · 응답 덤프는 네 스크래치 디렉터리에(레포 밖).

## 5. 하지 말 것

- **KOS 쓰기 호출 금지**(command · change · cancel · create 류 전부). 조회(queries · get)만
- **운영 명동점 키(`KOS_API_tenent`) 사용 금지** — 데모(`KOS_API_tenent_dev`)만
- public 레포: 리포트에 **실명 · 연락처 · 여권번호 · KOS id(테넌트 · 고객 · 일정 · 계정) · 키 · 토큰** 금지. 예시값은 모양만(`SURNAME, GIVEN` · `{scheduleId}`)
- 코드 레포 · para/ · ax-clinic-project 수정 금지. 커밋 · push · PR 금지

## 6. 검증

```
필드마다 답 + 근거(HAR 요청 번호 · 응답 필드 경로 / 공개 API 문서 위치). 없는 것은 「KOS 에 없음」. 결정하지 않고 「정할 것」으로 모은다
```

- HAR 의 KOS 요청 수를 직접 세어 리포트 머리에 적고 인벤토리 행 수와 맞춘다
- 대조표 행 수 = §7.2 행 수(+ 위에 더한 것). 빠진 행이 없는지 리포트 끝에 적는다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 과 preamble 이 다르면 preamble 쪽으로만 보낸다.
> 같은 워크트리에 다른 코디 세션(`term_ef44ce2a…` · 시술 현황 되돌리기)이 있다 — **그쪽으로 보내지 마라.**

- 커밋 · push · PR 하지 마라. 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --from <네 handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "리포트 경로 / 요약 / 실호출 결과(수치) / 정할 것 개수"

orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 \
  --text "[worker_done] researcher 예약 조회 대조 완료 — <한 줄>. 상세는 reservation-read-report.md" --enter
```

- 막히면 30분 이상 헤매지 말고: `orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --text "[질문] researcher: <질문>" --enter`
