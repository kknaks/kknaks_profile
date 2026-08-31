
# [backend] 조사 — 회의 생성 요청이 FE→BE→DB 로 어떻게 흐르나 (read-only)

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow`
base 브랜치: `origin/dev`

**이번 태스크는 조사(read-only)다. 리포 파일을 수정·생성하지 않는다.** 산출물은 아래 §6 이 지정한 리포트 파일 1개뿐이다.

## 1. SSOT — 먼저 읽을 것

- 해당 없음 — 이번 발주가 spec 작성 **전 단계**의 현행 코드 조사다. 코드가 곧 사실이다. 추측으로 메우지 말고 파일:줄 근거로만 적어라.

## 2. 배경 / 무엇을 조사하나

회의실 예약 워크플로우를 고치려 한다. 요구는 두 가지다:

1. **스케줄 테이블** — 회의가 잡히면 어떤 시간대에 누가 어느 회의실에 들어가는지 보이는 뷰
2. **회의실 자동 배정** — 지금은 회의 생성 모달에서 태그·시간 입력 후 조회해 수동 선택(기본값 "예약 안 함")인데, 제품–멤버 연결을 활용해 회의 생성 시 회의실이 자동으로 잡히게

스펙을 쓰기 전에 **현행 회의 생성 요청의 전체 흐름**을 정확히 알아야 한다. 그걸 네가 조사한다.

## 3. 조사 질문 — 리포트가 답해야 하는 것

1. **요청 경로**: 회의 생성 모달 제출 → front API route → back router → service → repository → DB 까지, 각 단계의 파일:줄과 함수명. 요청/응답 payload shape 포함.
2. **회의실 조회·예약**: 모달의 회의실 목록("태그·시간 입력 후 조회", 정원·모니터·N명 가능)이 어디서 오나. `front/app/api/meetings-v2/rooms/availability/route.ts` 부터 back 까지. 예약이 회의 생성과 한 트랜잭션인가, 별도 요청인가. 충돌(동시간 중복 예약) 방지는 어디서 하나.
3. **DB 모델**: 회의·회의실·예약·참석자에 해당하는 테이블/모델 전부 (`back/app/models/meeting_v2.py` 중심). 컬럼·FK·유니크 제약. 회의실 점유(시간대별 누가 어디) 를 조회하려면 지금 스키마로 무엇이 되고 무엇이 안 되나.
4. **태그와 제품–멤버 연결**: 모달의 태그(전사/제품/부서 + 제품 슬러그들)가 DB 어디에 사는가. 제품–멤버(어떤 멤버가 어떤 제품 소속인지) 매핑 테이블이 있는가 — 있으면 어디, 없으면 가장 가까운 것. **회의실 자동 배정이 이 연결을 쓸 수 있는지가 핵심이다.**
5. **참석자**: 선택된 참석자·HOST 가 어떻게 저장되나. 참석자 수 ↔ 회의실 정원 검증이 지금 있나.
6. **기존 스케줄/점유 뷰**: 시간대별 회의실 점유를 보여주는 화면·API 가 이미 있나 (일정/캘린더류 포함). 있으면 어디까지 되나.

## 4. 먼저 읽을 핵심 파일

- `front/components/meeting-v2/MtgV2CreateModal.tsx` — 회의 생성 모달 (제출 payload 의 출발점)
- `front/app/api/meetings-v2/rooms/availability/route.ts` — 회의실 가용성 조회 프록시
- `front/app/api/meetings/route.ts` — 회의 생성 프록시로 추정
- `back/app/routers/meetings_v2.py` — 회의 v2 라우터
- `back/app/services/meeting_v2_service.py` → `back/app/repositories/meeting_v2_repo.py` → `back/app/models/meeting_v2.py`
- `back/app/clients/the_connect.py` — "회의실" 문자열이 있다. 외부 연동 여부 확인

v1(`meetings.py`·`meeting_service.py`)과 v2 가 공존한다 — **실제로 모달이 쏘는 쪽**을 기준으로 삼고, 다른 쪽은 한 줄로만 언급하라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포 파일 수정·생성 **금지** (read-only 조사)
- 산출물은 §6 의 리포트 파일 1개뿐 (워크트리 밖 절대경로)

## 6. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/research-meeting-create-flow.md`

- §3 의 질문 순서대로 답한다. 모든 주장에 `파일:줄` 근거를 단다.
- 요청 흐름은 단계 나열(FE 컴포넌트 → route → router → service → repo → 테이블)로, 스키마는 테이블·컬럼 표로.
- 마지막 절에 「스펙 작성 전에 정해야 할 것」— 조사하다 발견한 열린 질문·리스크를 적는다. 없으면 "없음".

## 7. 범위 제약 — 하지 말 것

- 코드 수정·생성·삭제 금지. 테스트 실행 금지. docker 기동 금지. DB 접속 금지 — **코드 리딩만으로** 답한다.
- 개선안 설계를 하지 마라 — 이번 발주는 현행 파악이다. 개선 아이디어가 떠오르면 리포트 마지막 절에 한 줄씩만.
- 30분 이상 막히면 §9 방식으로 물어라.

## 8. 검증

```
해당 없음 (read-only 조사) — 리포트의 파일:줄 인용이 실제 코드와 일치하는지 스스로 재확인 1회
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "리포트 경로 / 조사 요약 / §3 질문별 답 유무 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
