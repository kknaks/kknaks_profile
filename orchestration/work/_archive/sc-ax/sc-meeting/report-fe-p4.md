# WP-006 Phase 4 — 회의 뒤 화면 실계약 배선 결과 보고

## 상태: done

## 1. 변경 파일

| 파일 | 무엇 |
|---|---|
| `frontend/src/viewModels.ts` | 실계약 필드 반영 — `MeetingLine.at_ms` · `MeetingAgenda.last_saved_at` · `MeetingInfo.{can_write_memo, started_at, title_candidate, failure_reason}` · `MeetingTodo.{description: string, reference: 객체}` · 새 타입 `MeetingTranscript` |
| `frontend/src/api.ts` | `readMeetingTranscript` · `promoteMeetingTodo` · `removeMeetingTodo` · `retryMeetingFinalize` · `meetingExportUrl` 추가. `updateMeetingAgenda` 에 `expected_last_saved_at`. **`ApiError` 가 `detail` 을 들고 온다**(409 가 「지금 있는 것」을 함께 낸다) |
| `frontend/src/meetings/MeetingDetailPage.tsx` | 원문 읽기 · 근거 칩 점프 · 승격 · 후보 삭제 · 다시 시도 · 내보내기 · 제목 후보 · 409 충돌 · 작성자 표시 이름 |
| `frontend/src/WorkModals.tsx` | `CreateWorkDrawer` 에 `onSubmitRequest?` 하나 — **주지 않으면 지금까지대로** `createWorkRequest` 로 간다(다른 화면 무변경) |
| `frontend/src/GutterList.tsx` · `styles.css` | `GutterRow.active` + 가리켜진 줄로 스크롤 (범용 확장) |
| `frontend/src/meetings/LiveScript.tsx` | `ScriptRow.active` 를 나른다 |
| `frontend/src/labels.ts` | `savedElsewhere` · `titleCandidate` · `promoted` · `alreadyRequested` |
| `frontend/src/App.tsx` | `personaId` 프롭 제거 — 권한을 화면이 추론하지 않는다 |
| `frontend/src/meetings/MeetingAfter.test.tsx` | **신규 10건** |
| `MeetingDetail.test.tsx` · `MeetingLive.test.tsx` · `MeetingList.test.tsx` | 실계약 픽스처로 갱신 + 바뀐 동작 4건 재작성 |

## 2. 계약 준수 — 경로별

| 경로 | 화면이 하는 것 |
|---|---|
| `GET …/transcript` | 「정리 중·완료·실패」의 스크립트 탭이 읽는다. 발화와 메모를 **`atMs` 한 축**으로 정렬해 `GutterList` 로 그린다. 예정·취소됨엔 탭이 없어 읽지 않는다 |
| `PATCH …/agendas/{aid}` | `{lines: string[], expected_last_saved_at}` — **줄별 저장 없음**, 안건 하나를 통째로 덮어쓴다. 빈 줄은 보내기 전에 버린다 |
| 409 `meeting_agenda_stale` | 덮어쓰지 않는다. `detail.current.lines`(track final)로 편집 칸을 갈아 끼우고 임시 문구를 낸 뒤 재조회 |
| `POST …/todos/{id}/promote` | `CreateWorkDrawer` 는 그대로 열되(prefill 유지·담당 비움) 제출만 promote 로 간다. `createWorkRequest` 는 이 경로에서 호출되지 않는다. 409 면 재조회 후 「이미 …」 |
| `DELETE …/todos/{id}` | × 는 확인 없이 서버로. 승격된 줄엔 × 가 없다 |
| `POST …/finalize` | [다시 시도]가 부른다(전에는 `endMeeting` 을 부르고 있었다 — **버그 수정**). `failure_reason` 을 안내 옆에 붙인다 |
| `GET …/export?format=html` | `<a href>` 하나. **형식 고르는 자리 없음**, pdf·docx 문자열 0 |
| `title_candidate` | 제목이 비면 머리에 흐리게. 연필을 열면 칸에 차 있고, 저장하면 그것이 제목이 된다 |
| `can_write_memo` | 메모 입력 칸과 **WS 업스트림 역할**의 유일한 근거. `created_by === personaId` 판별을 걷어냈다 |
| `started_at` · `Line.at_ms` | 경과 시간 기준점과 메모 시각을 서버 값으로. `Date.now()` 자체 계산은 째깍이는 경과 표시에만 남는다 (검수 4 W-a) |
| `Line.author` | `member_id` 다 — `meeting.attendees` 명부로 표시 이름을 찾고 **없으면 이름 자리를 비운다**(id 를 그리지 않는다). W9 미결 해소 |

## 3. 검증

```
npx tsc --noEmit                                         → 0 에러
npx vitest run src/meetings/                             → 4 files · 51 tests 통과 (신규 10)
npx vitest run src/App.test.tsx src/CreateWork.test.tsx
    src/MyWorkPage.test.tsx src/WorkModals.test.tsx
    src/chat/ResourcePeek.test.tsx                       → 5 files · 52 tests 통과 (드로어 변경 무영향 확인)
```

신규 10건: 원문+메모 시각 축 · 근거 칩 구간 점프 · promote(담당 비움·참석자 우선·링크 없음) · 중복 승격 409 · 다시 시도 · 저장 충돌 409 · 제목 후보 · 내보내기 링크 하나 · 공유받은 사람 조작 0 · 정리 중 영역 로딩. 후보 삭제는 기존 테스트를 서버 호출 확인으로 고쳐 덮었다.

자기점검: `api.ts`·`stream.ts` 밖 `fetch`/`WebSocket` **0** · hex **0** · 회의록 업무 링크 **0** · 담당 자동 채움 **0** · 줄별 저장 **0**.

## 4. DS 추가 후보 (D25)

이번에 **새로 만든 부품은 없다.** 아래 셋은 P3 에서 세운 것이고, 이번 라운드는 `GutterList` 에 「가리켜진 줄」 하나를 더했다. 값은 전부 토큰이다.

| 이름 | 자리 | 쓰인 곳 | props · 상태 | 로컬 클래스 |
|---|---|---|---|---|
| `Composer` | `src/Composer.tsx` | `MemoComposer` | `leading?` · `value` · `onChange` · `onSubmit` · `placeholder` · `sendLabel` · `disabled?` · `error?` / 기본 · 포커스 · 비활성 · 오류 | `.composer` · `.composer-divider` |
| **`GutterList`** (이번 확장) | `src/GutterList.tsx` | `LiveScript` — 진행 중 스트림과 끝난 회의 원문 양쪽 | `label` · `rows[{key, gutter, body, muted?, **active?**}]` · `gutterWidth?` / 기본 · `muted`(잠정) · **`active`(다른 자리에서 가리킨 줄 — 켜지고 가운데로 스크롤)** | `.gutter-list` · `.gutter-row(.active)` · `.gutter-meta` · `.gutter-body(.muted)` |
| `StatusNote` | `src/StatusNote.tsx` | 진행 표시 띠 | `tone?: "muted"\|"danger"` · `children` / `role="status"` | `.status-note(.danger)` |

`CreateWorkDrawer.onSubmitRequest` 는 **부품이 아니라 이음매**다 — 드로어를 복제하지 않고 제출 자리만 갈아 끼운다. DS 후보가 아니라 앱 계층의 확장점이라 표에 올리지 않았다.

## 5. 임시 문구 (`OQ-311` — 확정 문구 없음)

| 키 | 임시 문구 | 언제 |
|---|---|---|
| `savedElsewhere` | 다른 곳에서 먼저 저장됐습니다. 지금 있는 내용으로 바꿔 두었습니다. | 안건 저장 409 (**이번 추가**) |
| `alreadyRequested` | 이미 업무 요청으로 보낸 후보입니다. | 승격 409 (**이번 추가**) |
| `titleCandidate` | 제목 후보 {후보} | 제목이 비고 후보가 있을 때 (**이번 추가**) |
| `streamConnecting` · `streamDisconnected` · `streamTaken` · `streamNotFound` · `streamUnauthorized` · `micDenied` | (P3 그대로) | 스트림 상태 줄 |
| `scriptEmpty` | 아직 원문이 없습니다. | 원문이 0건일 때 |

## 6. P3 리포트 §7 미결 처리

| 미결 | 결과 |
|---|---|
| 1. `TODO(WP-003)` 메모 API | **닫힘** — 서버에 실물이 있고 화면이 그대로 부른다 |
| 2. `ai.batch.agendas` 모양 | **남음** — WP-003 이 아직 배치를 밀지 않아 실물로 확인하지 못했다. REST `Agenda` 투영 가정 유지 |
| 3. 메모 줄에 시각이 없다 | **닫힘** — `Line.at_ms` 를 쓴다 |
| 4. 끝난 회의 원문 읽기 계약 없음 | **닫힘** — `GET …/transcript` |
| 5. 메모 권한을 서버가 말하지 않음 | **닫힘** — `can_write_memo` |
| W9 작성자 표시 | **닫힘** — 명부로 표시 이름을 찾고 없으면 비운다 |

## 7. 미결 · 주의점

1. **근거 칩과 스크립트 줄의 시각 눈금이 시안과 다르다.** 시안은 둘 다 **벽시계**(「15:32」)인데, 이 화면은 P3 브리프가 못박은 **경과 mm:ss**(「02:00」)로 통일돼 있다. 계약이 주는 값이 `at_ms`(경과)라 둘을 같은 눈금으로 두는 것이 칩→줄 점프의 전제다. 벽시계로 돌리려면 `started_at + atMs` 로 두 자리를 함께 바꾸면 된다 — **어느 쪽인지 확인이 필요하다.**
2. **승격의 422**(참석자 교차 조직)는 지금 오류 배너 한 줄로만 보인다. BE 후속 E4 가 열면 그대로 사라진다.
3. **`ai.batch` 실물 미확인** (위 §6-2).
4. **자료·공유는 손대지 않았다** — WP-005 범위. 자료 탭은 여전히 로컬 상태이고 `TODO(WP-005)` 가 그대로 있다.
5. `MeetingTodo.description` 을 `string` 으로 좁혔다(BE 는 빈 문자열을 낸다). null 을 낼 수 있으면 알려 달라 — 한 줄이다.
