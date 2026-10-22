# [backend] KOS 데모 지점에 오늘 날짜 환자 채우기 — 국적별 · 타임당 2명

같은 cc-prototype `backend` 워커. **코드 레포 수정 없음**(필요하면 일회용 스크립트는 scratchpad 에만).

## 사용자 요청
「오늘 날짜로 환자 여러 명 구성 — 데모에서 국적별로 타임당 2명씩」

## 기본값(코디가 정함 — 바꿀 근거가 생기면 질문)
- **대상: KOS 데모 테넌트만**(키 `KOS_API_tenent_dev` · 호스트 .com). 운영 명동점 키 `KOS_API_tenent` **절대 금지**
- 날짜: **오늘(KST)** · 시간: **KOS 예약 슬롯 그대로**(`getReservationSlotsByGroup` / `reserveByTimeSlot` 의 슬롯) · 운영 10:00~20:00 안 슬롯마다 **2명**
- 국적: 슬롯마다 돌려가며 — KR · CN · JP · TW · US · TH · VN (한 슬롯 안 2명은 서로 다른 국적) · 첫내원/재내원 섞기
- 이름: **가짜 이름**(실존 인물 · 직원 이름 금지 · 국적에 맞는 흔한 형태) · 연락처는 비우거나 KOS 가 요구하면 명백한 가짜(010-0000-xxxx)
- 그룹/구역: 시술 현황판이 보는 **4층 구역**(KOS_ZONE_ID)과 맞는 예약 그룹

## 할 일
1. **조사 먼저**: 공개 API(`reference/2026-10-12-cc-prototype/kos-demo-api.md` · developers.kos-solution.com 문서)로 국적까지 넣어 예약을 만들 수 있는지 — 내원객 생성(국적 필드) · `reserveByTimeSlot`(·WithVisitorId). 국적 필드가 없으면 내부 API(HAR · `orchestration/work/myeongdong-poc-v2/_RESUME.md` §2 사실 줄)에서 찾는다
2. 현황판에 카드로 뜨려면 **수납 · 시술(task)** 까지 있어야 한다(SPEC-003 카드 조건). API 로 접수 · 수납 · 시술권 생성까지 가능한지 확인 — **가능하면 일부(예: 슬롯마다 1명)만 수납까지**, 나머지는 예약 상태로 둔다. 불가능하면 예약만 만들고 「KOS 화면에서 사용자가 할 일」을 보고
3. 먼저 **1명 만들어 확인**(KOS 조회로 국적 · 시간 · 구역 확인 · 현황판 back 이 읽는지) → 그다음 전체
4. 만든 목록(시간 · 국적 · 가명 · scheduleId)을 `orchestration/work/myeongdong-poc-v2/demo-patients-2026-10-22.md` 에 — 지울 때 쓸 수 있게(취소 API 경로 포함)

## 하지 말 것
- 운영 테넌트 · 키/토큰/비밀번호 값 출력 · 실명 · 실제 연락처 · 코드 커밋 · 기존 일정 수정/취소

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
