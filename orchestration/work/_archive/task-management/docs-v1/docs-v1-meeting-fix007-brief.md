# [architect] SPEC-007 · WORK-007 정정 — 이름 정합

너는 **task-management `architect` 워커**다. 네가 방금 쓴 `spec-007-meeting-live.md` · `work-007-meeting-live.md` 두 파일만 고친다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`

## 0. 왜 정정하나 — **네 잘못이 아니다**

코디가 브리프에 이렇게 적었다.

```
「MeetingDetail 의 정본은 SPEC-006 이다.
 SPEC-006 워커가 tracks.human/ai · aiBatchSeq 로 맞춘다」
```

**이건 코디의 오류다.** SPEC-006 브리프에는 이름을 지정하지 않고 「하나로 맞춰라」만 적었고,
SPEC-006 워커는 자기 이름(`agendas.*` · `latestBatchSeq`)을 유지했다. **너만 `tracks.*` 를 썼다.**

그리고 네 `§7-D D-4` 의 「코디 결정은 `tracks.*`」 문장을 **SPEC-008 워커가 읽고 자기 문서까지 바꾸려 했다.**
그 문장이 오염원이다 — **반드시 지워야 한다.**

## ⛔ 1. 확정 이름 — 이게 정본이다

| 항목 | 정본 | 네 문서의 현재 값 |
|---|---|---|
| `MeetingDetail` 트랙 필드 | **`agendas.{human, ai, merged}`** | `tracks.*` |
| 배치 회차 필드 | **`latestBatchSeq`** | `aiBatchSeq` |
| 상태 가드 에러코드 | **`invalid_meeting_status`** 하나 | 일치(정정 불필요) |
| 자식 쓰기 응답 | **`MeetingDetail` 전체** (삭제만 `204`) | `PATCH …/agendas/{id}` 가 「사람 안건 전량」 |
| 안건 `next` 배지 문구 | **회의 중 「대기」** / 종료 후 「다음 논의로」 | 「다음으로」로 통일해 놓음 |

**배지 근거** — `DEC-003` §1 표 2026-09-06: `state='next'` 는 하나인데 뜻이 둘이다.
회의 중 = 「아직 안 다룸」 → **「대기」**, 종료 후 = 「다음 회의로」 → **「다음 논의로」**.
시안도 그렇게 갈라 그렸다 — 회의 중 L909·L1149·L1299 「대기」 / 상세·편집 L1525·L1740·L1960.
**네 담당은 회의 중이므로 전부 「대기」다.**

`agendas.*` 형태 — 안건 배열이고 줄은 안건 안 `lines[]` 에 중첩된다(SPEC-006 §4 필드 소유 표).

## 2. 할 일

1. **`spec-007-meeting-live.md`**
   - `tracks.*` → `agendas.{human, ai, merged}` (grep 1건)
   - `aiBatchSeq` → `latestBatchSeq` (grep 4건)
   - 「다음으로」 → 「대기」 (grep 11건 — **배지 문구인 것만**. 다른 뜻으로 쓰인 자리는 두어라)
   - `PATCH …/agendas/{id}` 응답을 **`MeetingDetail` 전체**로
   - **`§7-D D-4` 에서 「코디 결정은 `tracks.*`·`aiBatchSeq`」 문장을 지운다.**
     대신 「`MeetingDetail` 정본은 SPEC-006 의 `agendas.*`·`latestBatchSeq` 이고 이 spec 이 그것을 따른다」로 바꾼다
2. **`work-007-meeting-live.md`**
   - Open Issues 의 **「코드는 `tracks.*`·`aiBatchSeq` 로 만든다」 항목을 지운다.** 이름은 확정됐으므로 이슈가 아니다
   - 본문에 `tracks.*`·`aiBatchSeq`·배지 문구가 있으면 위 정본으로
3. **`S007-OQ-1`(재개 영구 실패)을 닫는다**
   - 화면에는 일시정지 상태에도 **[재개] [회의 종료] 둘 다** 있다(시안 L804·L1085·L1235).
     재개가 실패하면 **다시 일시정지로 돌아올 뿐**이고 그 자리에 종료가 항상 있다. **막다른 길이 아니다**
   - `backend/README.md` §8-2 이 이미 정정됐다 — **끊긴 상태에서 409 로 막는 것은 오디오뿐이고 `/end` 는 받는다**
   - OQ 를 **닫힘으로 옮기고** 근거를 적어라. 새 처리·새 분기를 만들지 마라

## 3. 하지 마라

1. **SPEC-006 · SPEC-008 · WORK-006 · WORK-008 을 건드리지 마라.** 지금 다른 워커가 잡고 있다
2. **기획·정책·아키텍처·시안을 고치지 마라**
3. **위 5건 밖의 내용을 바꾸지 마라.** 재작성이 아니라 정정이다
4. **커밋·push 하지 마라**

## 4. Done Criteria

- [ ] `grep -c "tracks\."` = 0 · `grep -c "aiBatchSeq"` = 0 (두 파일 모두)
- [ ] 배지 문구가 회의 중 화면 전부 「대기」
- [ ] `PATCH …/agendas/{id}` 응답이 `MeetingDetail` 전체
- [ ] **`§7-D D-4` 의 `tracks.*` 문장이 사라졌다**
- [ ] WORK-007 Open Issues 에서 이름 항목이 사라졌다
- [ ] `S007-OQ-1` 이 닫혔고 새 분기가 안 생겼다
- [ ] 네 파일 2개 외 변경 0건

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_95f47648-153b-4ec8-a4e4-97e9d0bebae3 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "SPEC-007 · WORK-007 정정 완료" \
  --body "치환 건수(tracks·aiBatchSeq·배지) / D-4 문장 전후 / PATCH agendas 응답 변경 / S007-OQ-1 닫은 근거 / grep 검증 결과 / 손대지 않은 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] SPEC-007 · WORK-007 정정 완료. 상세는 인박스." --enter
```
