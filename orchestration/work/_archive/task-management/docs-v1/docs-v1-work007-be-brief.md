# [backend] WORK-007 Phase 1~4 — WS 2단 중계 · 녹음 · AI 배치

너는 **task-management `backend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

**이 work 가 제품에서 기술 난도가 가장 높다**(BASE-003 L53). WS 2단 중계 · 배치 세션 유지 · 화자 분리 · 실패 처리가 얽힌다.

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
**코드 워커는 한 번에 하나만 돈다** — 이 트리에서 직접 작업한다. **WORK-006 이 이미 들어와 있다**(`a7e1bd4` be · `2d6319e` fe).

**문서는 코디 워크트리 절대경로로 읽는다(읽기 전용).**

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-007-meeting-live.md            ← 네 빌드 계획. Phase 1~4 만
  20-spec/spec-007-meeting-live.md            ← 외부 계약(§4)·Case Matrix·Acceptance(§6)
  10-decision/decision-003-meeting-notes.md   ← 정책. §4·§7·§STT
  00-baseline/baseline-003-meeting-notes.md   ← 기획 §Raw
  40-architecture/backend/README.md §5-1·§5-2·§8-2·§8-3·§12 · system/README.md 흐름 ③
  40-architecture/database/domains/meeting.md
orchestration/work/docs-v1/soniox-study.md    ← STT 조사
```

## 1. 범위 — Phase 1 · 2 · 3 · 4

```
Phase 1  스키마 보강 · env · 외부 어댑터 뼈대
Phase 2  REST 3표면 · /start 확장 · 웜스타트
Phase 3  WS 2단 중계 · 녹음 적재 · 일시정지
Phase 4  배치 파이프라인 · 검증 4단 · 즉시 push
```

**Phase 5~6 은 프론트다. 건드리지 마라.**

## ⛔ 2. WORK-006 이 이미 만든 것 — 다시 만들지 마라

| 무엇 | 어디 | 규칙 |
|---|---|---|
| **`build_detail()`** | `service/meeting_service.py` **함수 하나** | **여기에 `agendas.ai` · `latestBatchSeq` 를 채운다.** 새 빌더·표면별 조립 금지 |
| **`_assert_allowed` 상태 표** | `meeting_service` 한 곳 | 여기에 행을 더한다. 두 번째 가드 금지 |
| `meeting_router` | `api/meeting_router.py` | 여기에 표면을 **더한다**. 새 라우터는 **WS 전용**(`meeting_stream_router.py`)만 |
| 안건 표면 | `POST …/agendas { title }` | **회의 중에도 같은 것**을 쓴다. `PATCH …/agendas/{id}` 에 `state` 를 **더한다** |
| 6 테이블 · 리비전 `0005` | `models/meeting.py` | **컬럼이 이미 다 있다.** 대조하고 **없는 것만** 새 리비전으로 |
| `schedule_service` | 소비만 | 두 번째 겹침·파생 구현 금지 |

**Phase 1 첫 작업은 「`0005` 와 대조해서 없는 것만 판다」다.** 같은 컬럼을 두 리비전에 넣으면 `upgrade` 가 깨진다.

## ⛔ 3. 정본 이름 — SPEC 문서와 같다. 바꾸지 마라

```
agendas.{human, ai, merged}     tracks.* 아님
latestBatchSeq                  aiBatchSeq 아님
invalid_meeting_status          meeting_not_recording 만들지 마라 — 폐기됐다
meeting_stream_active           WS close 4409 (이 work 신설)
meeting_stream_disconnected     409 는 오디오 요청만. /end 는 이 상태에서도 받는다
자식 쓰기 응답                   MeetingDetail 전체 · 삭제만 204 · 없는 자식 404
안건 next 배지                   회의 중 「대기」 (문구는 프론트 몫 — 백엔드는 enum 만 저장)
```

**한국어 라벨을 DB 에 저장하지 마라**(G-4).

## ⛔ 4. 정책이 못박은 것 — 뒤집지 마라

**수치는 DEC-003 §STT L164 가 확정했다. 그대로 쓰고 env 로 뺀다.**

```
확정 발화 600자 · 안건 전환 즉시(미처리 80자 미만이면 생략) · 상한 180초
배치 타임아웃 120초 · 회의당 AI 세션 하나(동시 실행 금지)
stt-rt-v5 · language_hints ["ko"] · enable_speaker_diarization true
endpoint detection 미사용 (조기 파이널라이즈가 화자 분리를 깎는다)
```

**전송 경로** — 프론트 → 백엔드 → Soniox. **프론트는 키를 모른다.** 백엔드가 키를 갖고 원본 적재를 겸한다.

**오디오 청크는 ① 녹음 파일 append → ② Soniox 전달 순.** 파일 적재가 실패하면 **그 자리에서 끊는다**(BE §5-1).

**확정 토큰만 DB 적재.** 잠정 토큰은 화면 표시용이다(DEC-003 §3).

**AI 증분은 즉시 push + 배치 회차 표시.** 버퍼링 금지(§4 L97).

**AI 는 AI 탭만 채운다. 사람 트랙에 개입하지 않고 줄 제안도 하지 않는다**(§4 L95).
**AI 안건은 `track='ai'` 에만 존재**하고 회의 중 사람 탭에 보이지 않는다(§4 L96).

**웜스타트 컨텍스트** = 선택 프로젝트 + 그 프로젝트의 업무 + 미리 작성된 안건.
**무소속 회의는 무소속 업무**를 준다(§4 L98 · §8 L149). **화이트리스트도 같은 목록**이다.

**배치 입력에 사람 안건·사람 줄을 읽기 전용 컨텍스트로 넣는다** — ERD M-6 가 「고치지도 제안하지도 않는다. **읽기는 한다**」로 정정됐다(BASE-003 L36·L38).

### DEC-003 §7 이 열거한 실패만 처리한다 — **그 밖은 fallback 하지 말고 전파**

```
회의 중 배치 실패    조용히 넘기고 그 구간을 다음 배치에 합쳐 재시도. 사용자에게 표시 안 함
JSON 스키마 위반     그 배치 결과 전체 폐기. 부분 파싱 금지. 폐기 구간은 다음 배치로
없는 업무 참조       웜스타트 화이트리스트 밖 ID 는 거부.
                    참조 틀린 줄은 taskId 만 떼고 action 줄로 강등 — 내용은 살린다
마이크·스트림 실패   일시정지 상태 + 사유. 자동 재연결 금지. 재개는 사용자가 누른다
```

**「우리가 설계한 거 이외에 터지는 에러는 터지게 둬야 해」**(BASE-003 L43). `except Exception` 금지.

## ⛔ 4-b. WORK-006 검수에서 넘어온 백엔드 몫 1건 — 함께 닫아라

**`validation_error` 응답에 어느 필드가 틀렸는지가 없다.** 지금은 `{detail, code}` 만 나간다.

```
SPEC-006 §4 Case Matrix   「해당 컨트롤 실패 테두리 + 인라인 문구」
                          예: 「회의는 5분 이상 300분 이하여야 합니다」 → 일시 칸
                              「종료 시각은 시작보다 뒤여야 합니다」   → 일시 칸
실제 응답                  {detail, code} — 화면이 어느 칸인지 고를 수 없다
프론트 현재                ApiError 에 field 를 받을 준비가 돼 있고(618d5bb),
                          field 가 없으면 폼 전체에 붙인다
```

**`422 validation_error` 응답에 `field` 를 실어라.** 값은 요청 스키마의 필드 이름
(`title` · `workTypeId` · `projectId` · `startAt` · `endAt` · `agendas[n].title` …)이다.
여러 필드가 틀렸으면 **첫 번째 하나**를 싣는다(화면이 한 칸을 가리킨다).

**같은 규약을 업무·설정에도 적용해라** — `task_router` · `setting_router` 의 `validation_error` 도 같은 모양이어야 한다.
프론트가 영역마다 다른 처리를 두지 않게 한다. **다만 그쪽 화면은 고치지 마라**(프론트 몫).

`backend/README.md` §8-2 의 `validation_error` 행에 `field` 를 적는 것은 **코디 몫**이다 — 보고에만 남겨라.

## 5. 환경 변수

```
SONIOX_API_KEY        .env 에 실제 값이 이미 들어 있다. 읽어서 쓰되 **문서·로그·코드에 값을 남기지 마라**
.env.example          SONIOX_API_KEY= 자리가 이미 있다(빈 값). MEETING_BATCH_* 5수치를 여기에 더해라
```

**키를 커밋하지 마라.** `.env` 는 gitignore 돼 있다.

## 6. 지킬 것 — 아키텍처

```
계층        router → service → repository 한 방향
ORM 경계    모델은 repository 를 넘지 않는다
schema/dto  service 는 schemas/ 를 import 하지 않는다. dict 를 계층 계약으로 쓰지 마라
PATCH       T | Unset + model_dump(exclude_unset=True)
쿼리 파라미터 Query(alias="camelCase") 를 손으로 적는다 (§3-7 — WORK-004 에서 밟았다)
트랜잭션     요청 하나가 경계. service·repository 에서 commit() 금지
블로킹 금지  비동기 경로에서 동기 I/O 금지. 파일 적재는 anyio.to_thread
WS          업스트림은 클라이언트 연결 성립 후에 연다. 종료 처리는 finally
백프레셔     큐 상한 초과 시 잠정 토큰만 버린다. 확정 토큰·AI 증분은 안 버린다
AgentClient 싱글턴. resume={"mode":"session","session_id":...} 로 회의 하나의 세션 유지
            codex 실행 옵션은 빌더 함수 한 곳에서만 만든다
LLM SDK     Anthropic·OpenAI 직접 import 금지. open-kknaks 를 통해서만
```

## ⛔ 7. 검증 — **앱 창 E2E 는 하지 마라**

```bash
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만>
# 전체 스위트는 코디가 돌린다. 검증은 1회만
```

**WP 의 「앱 창에서 …」 항목을 테스트 코드로 옮겨라.** WS 는 `wscat` 대신 **테스트 클라이언트**로 닫는다.

**BE §12 필수 테스트 6·7 은 반드시 있어야 한다** — 스키마 위반 폐기 · 화이트리스트 밖 강등.

**테스트로 못 덮은 것은 「실물 확인 필요」 목록으로 보고에 남겨라.** 임의로 통과 처리하면 리뷰에서 FAIL 이다.

## 8. 지킬 것 — 일반

1. **`app/back/` 밖을 건드리지 마라**(`.env.example` 은 허용)
2. **프론트를 만들지 마라.** Phase 5~6 은 다른 워커다
3. **문서를 고치지 마라**
4. **커밋·push 하지 마라**
5. **WP 범위 밖을 하지 마라.** 필요해 보여도 하지 말고 보고에 적어라
6. **기획·정책에 없는 기능을 만들지 마라.** 시안에 있어도
7. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 9. Done Criteria

- [ ] Phase 1~4 의 WP 검증 항목이 전부 통과
- [ ] **`build_detail()` 이 여전히 1개**이고 거기에 `agendas.ai`·`latestBatchSeq` 를 채웠다
- [ ] **`_assert_allowed` 가 여전히 한 곳**이다
- [ ] 리비전은 `0005` 와 대조해 **없는 것만** 팠다(또는 안 팠다)
- [ ] 프론트로 Soniox 키가 내려가지 않는다 — grep 으로 확인
- [ ] 배치 수치 5종이 **env** 에 있고 DEC-003 §STT 값과 같다
- [ ] BE §12 필수 테스트 **6·7** 이 있다
- [ ] `except Exception` 0건 · 자동 재연결 0건
- [ ] 「실물 확인 필요」 목록이 정직하다
- [ ] `app/back/` 밖 변경 0건 · 커밋 없음 · 키 미커밋

## 10. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_a8f9b58c-82ab-4a7f-a5df-6e3aa63941ff \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-007 Phase 1~4 완료" \
  --body "리비전 판단(0005 대조 결과) / 만든 표면과 WS 계약 / build_detail 에 더한 필드 / 배치 트리거·검증 4단 구현 위치 / 실패 3종 테스트 / env 수치 5종 / pytest 결과 / **실물 확인 필요 목록** / 키 미커밋 확인 / 범위 밖이라 안 한 것 / SPEC·WP 와 어긋나 못 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-007 Phase 1~4 완료. 상세는 인박스." --enter
```
