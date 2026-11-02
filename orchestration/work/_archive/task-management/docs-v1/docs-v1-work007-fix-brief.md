# [backend+frontend] WORK-007 검수 수정 — FAIL 2 · WARN 3 · compose

너는 **task-management 코드 워커**다. **이번 건은 백엔드와 프론트를 한 워커가 함께 고친다** — F-1 이 두 층에 걸쳐 있다.

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
네 것은 `b09a16a`(be) · `ecb7f07`(fe) 다.

**검수 리포트** — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work007-review-report.md` **먼저 통째로 읽어라.**

## ⛔ 1. 닫을 것 — 6건

### F-1 (FAIL) — AI 업무 줄의 `task.workType` 이 응답에 없다 · **be + fe**

```
SPEC-007 §4 L378 LineItem(track=ai) · U-4 L161 · Data Contract L566
SPEC-008 §4 L450-451 · L484 · 디자인 시스템 [09] L671
  → task 요약에 workType 을 담기로 돼 있다
실제
  schemas/meeting.py:210-217 · dto/meeting.py:73-80
  repository/meeting_child_repository.py:190-213  ← 조인이 없다
결과
  LineRow.tsx:14 가 유형 배지를 못 그린다
```

**be** — dto 에 필드 1 · 조인 1 · schema 1. **fe** — `LineRow` 에 `TypeBadge` 1.
**WORK-008 이 같은 자리에 「업무 갱신」 버튼을 붙인다.**

### F-2 (FAIL) — `startCapture` 실패를 `catch {}` 로 삼킨다 · **fe**

```ts
// features/meetings/hooks/useMeetingStream.ts:170-175
try { captureRef.current = startCapture(mic, …); } catch { onTrackEnded(); }
```

**설계 밖 실패의 fallback 이다.** `MediaRecorder` 부재 · 후보 mime 전부 미지원(`audioCapture.ts:50-55` 의 `NotSupportedError`)이
**「일시정지 · 마이크 연결이 끊겼습니다」 + 서버로 `pause{mic}`** 로 나간다. 서버는 정상 일시정지로 보고 Soniox 세션을 유지하고,
사용자가 「재개」를 눌러도 같은 자리에서 또 접힌다. **어디서 깨졌는지가 가려진다.**

```
DEC-003 §7 L131-132   처리하는 실패는 열거한 것뿐. 광범위한 포착은 어디서 깨졌는지를 가린다
BASE-003 L43          설계한 거 이외에 터지는 에러는 터지게 둬야 해
Case Matrix 마이크 실패 행   권한 거부 · 장치 분리 · 트랙 ended **셋뿐**
```

**`catch` 를 걷어 전파해라.** 굳이 잡을 거면 **사유를 드러내는 별도 문구 + 토스트**로 — 마이크 실패로 접지 마라.
**`:153-157` 의 `getUserMedia` 실패 `catch` 는 그대로 둬라** — Case Matrix 행에 있다(토스트 「마이크를 사용할 수 없습니다」).

### D-8 — `docker-compose.local.yml` 에 Redis · open-kknaks worker 가 없다 · **be**

**이게 없으면 회의를 한 번도 시작할 수 없다.** `/start` 의 웜스타트가 브로커 연결에서 예외를 낸다.

```
docker-compose.local.yml:8-24   db · api 뿐
:3 주석                          「Redis · open-kknaks worker · 파일 저장소는 회의록 배치에서 여기에 합류한다」
config.py:46                     redis_url 기본값 redis://localhost:6379/0
```

**주석이 「여기서 합류한다」고 적어 둔 대로 이번에 넣는다.** WP L43 의 「WORK-001 이 넣었다」는 전제 오류다.

- `redis` 서비스 추가(healthcheck 포함) · `api` 가 `depends_on` 으로 기다리게
- **open-kknaks worker** — `40-architecture/system/README.md` 와 `backend/README.md` §5-2·§5-3 을 읽고 필요한 것을 넣어라.
  **open-kknaks 자체는 고치지 마라** — 설정은 우리 부팅부(compose·env)에서만 한다
- `STORAGE_ROOT` 볼륨도 함께(녹음 원본이 컨테이너와 함께 사라지면 안 된다)
- **넣을 수 없는 것이 있으면 만들지 말고 보고에 적어라**(이미지 이름·실행 커맨드를 모르면 그렇게 적어라)

### W-2 — 배치 태스크의 예외가 아무 데도 안 드러난다 · **be**

`service/meeting_batch_service.py:117-121` `schedule()` 이 `asyncio.create_task(evaluate(...))` 를 던지고
`_tasks.discard` 만 붙였다. **`task.result()` 를 아무도 읽지 않는다.**

배치는 요청 경계 밖이라 500 이 없다. 설계 밖 예외(`ai_session_id` 없음 `RuntimeError :234-236`, 브로커 도달 불가)가 **조용히 사라진다.**

**`_tasks.discard` 자리에서 `task.result()` 를 읽어 스택을 로그로 남겨라.** 삼키지 말고 드러내라.

### W-3 — WS `4404` 에 상태 바가 사실과 다른 문구를 그린다 · **fe**

`hooks/useMeetingStream.ts:262-266` 이 `NOT_FOUND` 에서 `paused/stream:upstream` 으로 간다.
최종 화면은 맞지만(재조회 404 → 「없는 회의록입니다」) **그 사이 「서버 연결이 끊겼습니다」가 뜬다. 서버는 살아 있다.**

SPEC-007 §4 close code 표 L305: `4404` → 「없는 회의록입니다」.
**`4404` 는 상태 바를 갈지 말고 재조회 결과로만 갈리게 해라.**

### W-4 — `kind≠task` 인 출력 줄의 `taskId` 를 조용히 뗀다 · **be**

`service/meeting_batch_service.py:397-400` 이 강등도 폐기도 아닌 **무음 정정**을 한다.
`ai_schemas/meeting_batch.json:42` 가 `taskId` 를 조건 없이 `integer|null` 로 둬서 스키마도 안 잡는다.

```
SPEC-007 §4 배치 출력 L421   taskId — kind=task 일 때만, 없으면 null
BE §8-1                      기본값으로 때우지 않는다
검증 표 2단·3단              이 경우를 적지 않았다 (문서 공백 D-5)
```

**폐기로 볼지 무시로 볼지는 문서가 정한다. 지금은 최소한 `reason` 로그를 남겨라** — 조용히 지나가지 않게.
**스키마도 `kind=task` 조건을 걸 수 있으면 걸어라**(`if/then` 또는 `oneOf`).

## 2. 손대지 마라

```
W-1  meeting_service.start() 의 session.commit()
     → BE §2「service commit 금지」와 §7「외부 호출 전에 커밋」이 서로 충돌한다.
       **문서를 먼저 정해야 한다. 코드는 그대로 둬라**(코디가 문서 정합 후 다시 발주한다)

D-2  웜스타트 실패 뒤 회의 상태
     → 정책(DEC-003 §7)에 없다. **사용자 결정 대기.** 새 분기를 만들지 마라
```

## 3. 지킬 것

1. **위 6건 밖을 고치지 마라.** 리팩터 욕심 금지 — 발견하면 보고에 적어라
2. **문서를 고치지 마라**
3. **커밋·push 하지 마라**
4. **키를 커밋하지 마라.** `.env` 는 gitignore 돼 있다
5. **기획·정책에 없는 기능을 만들지 마라**
6. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 4. 검증 — **앱 창 E2E 는 하지 마라**

```bash
cd app/back  && uv run pytest -q <네가 만들거나 고친 테스트만>
cd app/front && npx tsc --noEmit
cd app/front && npx vitest run
```

**F-1·F-2·W-3·W-4 는 테스트로 고정해라.**

```
F-1   AI 업무 줄 응답에 workType 이 있고 LineRow 가 배지를 그린다
F-2   startCapture 가 던지면 **마이크 실패로 접히지 않는다**(pause{mic} 프레임 0)
W-3   4404 수신 시 상태 바가 「서버 연결이 끊겼습니다」로 가지 않는다
W-4   kind≠task 인데 taskId 가 온 경우 로그(또는 폐기)가 남는다
```

**compose 는 `docker compose config` 로 문법만 확인**하고 실제 기동은 하지 마라 — 실물 확인은 사용자 몫이다.

## 5. Done Criteria

- [ ] F-1 — 응답에 `workType` 이 있고 `LineRow` 가 배지를 그린다. 테스트 고정
- [ ] F-2 — `catch {}` 가 사라졌다. 설계 밖 실패가 마이크 실패로 접히지 않는다
- [ ] D-8 — compose 에 `redis` · worker · `STORAGE_ROOT` 볼륨. 못 넣은 것은 보고에 명시
- [ ] W-2 — 배치 태스크 예외가 스택 로그로 드러난다
- [ ] W-3 — `4404` 가 상태 바를 갈지 않는다
- [ ] W-4 — 무음 정정이 사라졌다(로그 또는 폐기)
- [ ] W-1 · D-2 를 **건드리지 않았다**
- [ ] `pytest` · `tsc` 0 · `vitest` 전부 통과 (WORK-006 회귀 없음)
- [ ] 커밋 없음 · 키 미커밋

## 6. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_55ac2876-0839-42aa-b7a5-c820f9abfb69 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-007 검수 수정 완료" \
  --body "6건 각각 어디를 어떻게 고쳤나(파일:줄) / compose 에 넣은 것과 **못 넣은 것** / 새로 고정한 테스트 / pytest·tsc·vitest 결과 / W-1·D-2 를 안 건드렸다는 확인 / 고치다 발견했지만 범위 밖이라 안 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-007 검수 수정 완료. 상세는 인박스." --enter
```
