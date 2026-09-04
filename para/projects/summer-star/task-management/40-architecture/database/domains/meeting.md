---
type: architecture
id: DOMAIN-003
title: "meeting — 2트랙 회의록과 통합본"
status: draft
product: "task-management"
created_at: 2026-09-04
updated_at: 2026-09-04
tags:
  - product/task-management
  - doc/architecture
  - architecture/database
links:
  baselines: [BASE-003]
  decisions: [DEC-003, DEC-001, DEC-002, DEC-004, DEC-005]
  specs: []
  works: []
  related: []
---

# meeting

**사람과 AI 가 각자 회의록을 쓰고, 종료 후 통합한다.** 이 도메인의 설계 축은 그 2트랙이다(BASE-003).

## Purpose

DEC-003 의 2트랙 모델·배치 파이프라인·실패 정책을 스키마로 옮긴다. 12-meeting-notes 의 「줄 하나에 배치가 `detail`·`evidence` 를 채운다」 단일 트랙 모델은 폐기됐다(§A-5).

## Entities / Tables

| Entity/Table | Purpose | Notes |
|---|---|---|
| `meeting` | 회의록 본체 | 소프트 딜리트. **시간 컬럼 없음** |
| `meeting_agenda` | 안건 | 사람·AI 공유 축. `origin` 으로 누가 만들었는지 표시 |
| `meeting_line` | **줄 — 3트랙** | `track ∈ {human, ai, merged}` |
| `meeting_transcript` | 확정 발화 블록 | 근거 칩의 원천 |
| `meeting_attachment` | 첨부 | v1 은 자료함 md 만 |
| `meeting_batch_run` | 배치 실행 이력 | 실패 구간을 다음 배치로 넘기는 커서 |

### 왜 줄이 세 테이블이 아니라 한 테이블 + `track` 인가

세 집합의 컬럼이 사실상 같고(안건·종류·본문·순서·근거·업무 참조), **통합본이 AI 줄의 타임스탬프를 물려받으므로** 같은 모양이어야 한다(DEC-003 §4). 테이블을 셋으로 가르면 같은 컬럼 정의를 세 번 쓰고 통합 로직이 세 모델을 오간다. 트랙별 조회는 `(meeting_id, track, agenda_id, order_index)` 인덱스 하나로 끝난다.

## Invariants

- **M-1** **`meeting` 에 시간 컬럼이 없다.** `startAt`/`endAt` 은 `schedule` 로 이관됐다(DEC-005 §3 · §A-4).
- **M-2** `work_type_id` 는 **`kind='meeting'` 인 유형만** 받는다. 디자인의 `미팅·회의|반복|개인` 3종 enum 은 폐기됐고 **반복 회의는 v1 제외**다(DEC-003 §3 · §A-7).
- **M-3** `status` 는 **4종** — `scheduled → recording → generating → ended`. **`generating` 은 신설**이다(DEC-003 §3 · §A-6).
- **M-4** 통합 결과는 `integration_state` 가 든다. **`status='ended'` + `integration_state='failed'`** 가 「통합 정리 실패 · 다시 생성」 배너의 조건이다. **「다시 생성」은 이 조합에서만 노출**되고, 정상 생성분의 재생성은 없다(DEC-003 §4).
- **M-5** **줄은 항상 어떤 안건에 속한다** — `agenda_id` 는 NOT NULL 이다(12-meeting-notes).
- **M-6** 회의 중 AI 는 **`track='ai'` 에만 INSERT 한다.** 사람 줄을 읽지도 고치지도 않고, 줄 제안도 하지 않는다(DEC-003 §4).
- **M-7** 회의 중 배치는 **증분 추가만** — 기존 `track='ai'` 줄을 UPDATE 하지 않는다. 전체 재정리(DELETE + INSERT)는 **종료 후 최종 배치 한 번**뿐이다(DEC-003 §4).
- **M-8** 통합본(`track='merged'`)의 본문은 **사람이 쓴 문장 그대로**다. AI 에서 가져오는 것은 `evidence` 와, AI 트랙에만 있는 내용의 추가분뿐이다(DEC-003 §4).
- **M-9** `meeting_transcript` 에는 **확정 토큰만** 들어간다. 잠정 토큰은 화면 표시용으로 흘려보내고 저장하지 않는다(DEC-003 §3).
- **M-10** `speaker_label` 은 **익명**(`화자 1`/`화자 2`)이다. 참석자·발언자 이름 컬럼을 두지 않는다(DEC-003 §2). Soniox 는 **세션당 최대 15명**을 라벨링한다(soniox).
- **M-11** `at_ms` 는 **회의 시작 기준 오프셋**이다. 근거 칩의 `evidence` 도 같은 기준이라 벽시계 시각과 섞지 않는다.
- **M-12** `ai_session_id` 는 **회의 하나에 하나**다. 매 배치가 이 세션을 `resume` 한다 — 배치마다 새 세션을 만들지 않는다(DEC-003 §STT).
- **M-13** **`recording_path` 는 영구 보관**이다. 회의록을 소프트 딜리트해도 녹음 파일을 지우지 않는다. 보존 기간·자동 삭제 정책이 없다(DEC-003 §4·§6).
- **M-14** `meeting_line.task_id` 는 **버튼을 눌러 업무가 실제로 생기거나 연결됐을 때만** 채워진다. 줄을 적는 것만으로는 안 생긴다(DEC-003 §5).
- **M-15** 배치 결과의 `task_id` 는 **웜스타트로 준 업무 ID 화이트리스트** 안에 있어야 한다. 밖이면 `task_id` 를 떼고 `kind='action'` 으로 강등하되 **본문은 살린다**(DEC-003 §7).
- **M-16** JSON 스키마를 위반한 배치 결과는 **행 하나도 넣지 않고 통째로 폐기**한다. 부분 파싱 금지 — `meeting_batch_run.status='discarded'` 로 남기고 그 구간을 다음 배치에 합친다(DEC-003 §7).
- **M-17** 첨부는 자료함 문서 참조뿐이다. **회의 중 md 작성(`source=local`·`agendaId`)은 v2** — v1 에 문서 생성 경로가 없다(DEC-004 §8 · §A-11).
- **M-18** **300분 초과 회의를 다루지 않는다** — 세션 경계·재연결 컬럼을 만들지 않는다(DEC-003 §4).

## Related Specs / Works

- SPEC-00x 회의록 (DEC-003 Resulting Spec)
- 참조: `domains/account.md`(유형·프로젝트) · `domains/task.md`(업무 생성·갱신) · `domains/calendar.md`(시간) · `domains/library.md`(첨부)
