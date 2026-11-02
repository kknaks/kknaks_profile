# WP-006 Phase 3 — 「진행 중」 회의 화면(스트림) 프론트 결과 보고

## 상태: done

## 1. 수행 내용

**새 파일**

| 파일 | 무엇 |
|---|---|
| `frontend/src/meetings/stream.ts` | 회의 스트림 클라이언트. **`WebSocket` 을 만드는 유일한 자리**(`api.ts` 와 같은 규약) + `useMeetingStream` 훅 |
| `frontend/src/meetings/microphone.ts` | 마이크 캡처 → 청크. 오디오 형식 선언 상수를 여기서 소유한다 |
| `frontend/src/meetings/LiveScript.tsx` | 「스크립트」 탭 실시간 원문 (확정 추가 · 잠정 교체 · 메모 섞임) |
| `frontend/src/meetings/MemoComposer.tsx` | `E80`·`E81` 메모 입력 (안건 드롭다운 + 한 줄 칸, 저장 단추 없음) |
| `frontend/src/Composer.tsx` · `src/GutterList.tsx` · `src/StatusNote.tsx` | **DS 에 없어 새로 세운 부품 셋** — D25 에 따라 화면 전용이 아니라 최상위 부품으로 분리 (§4) |
| `frontend/src/meetings/MeetingLive.test.tsx` | Phase 3 테스트 13건 (WS·마이크 모킹) |

**고친 파일** — `MeetingDetailPage.tsx`(스트림 연결·진행 표시·두 탭·스크립트·메모 자리) · `api.ts`(`addMeetingMemoLine` 추가, 옛 회의 함수 일괄 제거) · `viewModels.ts`(옛 회의 타입 제거) · `labels.ts`(스트림 임시 문구) · `styles.css`(부품 셋 + 진행 중) · `App.tsx`(`personaId`·`onSessionLost` 배선) · `chat/ResourcePeek.tsx`(새 회의 계약으로).

**삭제** — `liveTranscription.ts` · `liveTranscription.test.ts` · `MeetingDrawer.tsx` · `MeetingDrawer.test.tsx`. `CalendarMeetings.test.tsx` 와 캘린더 회의 탭은 Phase 1·2 에서 이미 뗐다. `api.ts` 의 옛 회의 함수 11개(달력 목록 · 노트 · 녹음 · **realtime credential · realtime segments** · 요약 채택 · 승격)와 `viewModels.ts` 의 옛 회의 타입 13개를 함께 지웠다 — **브라우저가 STT provider 를 아는 경로가 이제 없다** (SPEC §5.2-2).

## 2. 오디오 형식 선언

**`{ format: "webm/opus", sampleRate: 16000, channels: 1 }`** — `MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" })` · `start(250)`.

- `AudioWorklet` 로 16k PCM 을 뜨는 길도 있으나 worklet 모듈을 따로 실어야 한다. 데모에 필요한 것은 「끊기지 않고 250ms 안쪽으로 올라간다」뿐이라 `MediaRecorder` 로 갔다.
- **주의**: webm/opus 청크는 첫 조각 뒤로는 홀로 서지 못한다 — 서버가 **받은 순서대로 이어 붙여** provider 에 흘려야 한다. PCM 이 필요하면 `microphone.ts` 의 상수 한 줄과 `mimeType` 만 바뀐다.
- 64KB 를 넘는 청크는 잘라 보낸다(계약 한도). `ready` 전에는 아예 보내지 않는다.

## 3. 계약 준수

| 계약 | 구현 |
|---|---|
| 첫 프레임 | `{"type":"auth","role":"upstream"\|"subscribe","audio":{…}}` — `audio` 는 업스트림만. 주소에 토큰을 붙이지 않는다(같은 오리진 · 쿠키) |
| 역할 | `meeting.created_by === personaId` 면 `upstream`, 그 밖의 참석자는 `subscribe`(오디오 전송 0) |
| `transcript.partial` | **교체** — 이전 잠정을 통째로 갈고 저장하지 않는다. 확정이 서면 그 잠정은 사라진다 |
| `transcript.final` | **추가** |
| `ai.batch` | **AI 탭 통째 교체.** 줄 id 를 붙들지 않는다. 읽던 스크롤 자리를 지키고, 바닥에 붙어 있었으면 바닥을 지킨다 |
| `error` → 닫힘 | 사유를 상태 줄에 그대로 낸다 |
| close `4401` | `onSessionLost()` → 로그인 화면 |
| close `4404` | 「볼 수 없는 회의입니다.」 |
| close `4409` `invalid_meeting_status` | 상세 재조회 |
| close `4409` `meeting_stream_active` | 「다른 창에서 진행 중입니다.」 |
| close `1000` | 상세 재조회 → 「정리 중」 화면 |
| 재연결 | **없다.** 소켓 인스턴스가 하나로 끝나는 것을 테스트가 고정한다 |
| pause/resume | 없다 |
| 메모 | 응답으로 돌아온 줄만 붙인다(**낙관 렌더 0**). 실패하면 `T34` 를 내고 친 것은 칸에 남긴다 |

## 4. DS 추가 후보 (D25)

디자인 시스템 v2(`docs/design` · `styles.css`)에 없어 이번에 새로 세운 것들이다. 범용인 셋은 `meetings/` 밖 최상위로 뺐고, 스타일은 전부 `styles.css` 에 **DS 토큰만으로** 뒀다(하드코딩 색 0 · 새 그림자 0).

| 이름 | 자리 | 쓰인 곳 | props · 상태 | 로컬 클래스 |
|---|---|---|---|---|
| **`Composer`** | `src/Composer.tsx` | `MemoComposer`(회의 메모). 저장 단추 없이 던지는 한 줄 칸이 필요한 모든 자리 | `leading?` · `value` · `onChange` · `onSubmit` · `placeholder` · `sendLabel` · `disabled?` · `error?` / 상태: 기본 · 포커스(`:focus-within` 테두리) · 비활성 · 오류 | `.composer` · `.composer-divider` |
| **`GutterList`** | `src/GutterList.tsx` | `LiveScript`(원문·메모). 「같은 시각 축에 종류가 다른 줄이 섞이는」 목록(활동 기록 등) | `label` · `rows[{key, gutter, body, muted?}]` · `gutterWidth?` / 상태: 기본 · `muted`(아직 굳지 않은 줄) | `.gutter-list` · `.gutter-row` · `.gutter-meta` · `.gutter-body(.muted)` |
| **`StatusNote`** | `src/StatusNote.tsx` | 진행 표시 띠의 스트림 상태·마이크 상태 | `tone?: "muted"\|"danger"` · `children` / `role="status"` — 읽던 자리를 끊지 않는다 | `.status-note(.danger)` |
| `MemoComposer` | `meetings/` **유지** | 회의 메모 한 줄 | 회의 API·`T34`·안건 드롭다운이 붙은 **도메인 부품**이라 최상위로 올리지 않았다. 범용 껍데기만 `Composer` 로 뺐다 | `.meeting-composer-foot`(패널 푸터 여백) |
| `LiveScript` | `meetings/` **유지** | 「스크립트」 탭 | `ScriptRow`(화자 라벨·경과 시각·메모 표시)가 회의 계약이라 도메인 부품이다. 줄 모양만 `GutterList` 로 뺐다 | — (전부 `GutterList` 클래스) |
| 진행 표시 띠 | `meetings/` **유지** | 「진행 중」 상단 | 경과 시간 + 시작한 사람 + `StatusNote` 들. 회의 전용 배치라 그대로 뒀다 | `.meeting-live-bar` |

**DS 에 이미 있어 새로 만들지 않은 것** — 탭(`.meeting-tabs`) · 배지·상태점(`.badge`·`.status`) · 빈 상태(`Empty`) · 로딩(`Skeleton`) · 드롭다운(`Select`) · 아이콘(`Icon`) · 오류 문장(`.field-error`).

## 5. 임시 문구 (SPEC §13 `OQ-311` — 확정 문구 없음)

기획 정본의 확정 문구 집합에 스트림 거절·끊김 문구가 없다. 아래 여섯은 **임시다.** 확정 문구가 오면 `labels.ts` 의 이 자리만 바뀐다.

| 키 | 임시 문구 | 언제 |
|---|---|---|
| `streamConnecting` | 연결하는 중 | 첫 프레임 보낸 뒤 `ready` 전 |
| `streamDisconnected` | 연결이 끊겼습니다. `{사유}` | `error` 프레임 · 그 밖의 비정상 닫힘 |
| `streamTaken` | 다른 창에서 진행 중입니다. | `4409 meeting_stream_active` |
| `streamNotFound` | 볼 수 없는 회의입니다. | `4404` |
| `streamUnauthorized` | 다시 로그인해 주세요. | `4401` |
| `micDenied` | 마이크를 쓸 수 없습니다. 스크립트와 AI 요약은 계속 받습니다. | `getUserMedia` 거부 |

`scriptEmpty`(「아직 원문이 없습니다.」)는 Phase 1·2 에서 올린 그대로 남아 있다 — 이제 **끝난 회의**의 원문 자리에만 선다.

## 6. 검증

```
npx tsc --noEmit                                        → 0 에러
npx vitest run src/meetings/ src/App.test.tsx
        src/chat/ResourcePeek.test.tsx src/labels.test.ts → 6 files · 75 tests 전부 통과
```

Phase 3 신규 13건이 WP 검증 4항목 + 계약 항목을 덮는다:

| 검증 | 테스트 |
|---|---|
| 비소유 참석자에게 메모 입력 칸 없음 | 「메모 입력 칸은 회의를 만든 사람에게만 선다」 |
| `ai.batch` 통째 교체 · 스크롤 유지 | 「ai.batch 는 AI 트랙을 통째로 갈아 끼우고 읽던 자리를 지킨다」 |
| 회의 종료 시 연결 닫히고 「정리 중」 | 「[회의 종료]는 연결을 닫고 「정리 중」 화면으로 넘긴다」 |
| 상단에 AI 채팅·알림 없음 | 「상단에 AI 채팅 입력도 알림도 없다」(진행 중 [자료 첨부] 숨김도 함께) |
| 첫 프레임 형식 · 역할 | 「첫 프레임이 역할을 선언한다」 · 「그 밖의 참석자는 구독 전용으로 붙는다」 |
| partial 교체 / final 추가 | 「잠정 발화는 교체되고 확정 발화는 쌓인다」 |
| `4409 meeting_stream_active` | 「두 번째 업스트림은 거절된다」 |
| 끊김 표시 · 재연결 없음 | 「끊기면 사유를 그대로 내고 다시 붙지 않는다」 |
| `ready` 전 오디오 없음 · 청크 업스트림 | 「마이크는 ready 뒤에 열리고 청크가 그 연결로 올라간다」 |
| 마이크 거부 | 「마이크를 거부해도 화면이 멈추지 않고 상태 줄로 알린다」 |
| `4401` | 「인증이 죽으면 로그인으로 돌려보낸다」 |
| 메모 낙관 렌더 없음 · `T34` | 「메모는 돌아온 줄만 붙는다 — 실패하면 친 것을 그대로 두고 알린다」 |

자기점검: `api.ts`·`stream.ts` 밖에서 `fetch`·`new WebSocket` **0** · hex 리터럴 **0** · 금지어(일시정지·재개·녹음·다시 연결) **0**(테스트의 부재 확인 한 줄 제외) · `backend/` 무수정 · dev 서버 안 띄움.

## 7. TODO · 미결

1. **`TODO(WP-003)` 메모 쓰기 API** — `POST /api/meetings/{id}/agendas/{agendaId}/lines {text}` → `Line`. 계약대로 먼저 부르고 있고 테스트는 모킹이다.
2. **`ai.batch.agendas` 의 모양을 REST 의 `Agenda` 투영과 같다고 가정**했다(`_agenda_view`). 화면은 `order`·`title`·`lines[].text` 만 읽으므로 남는 칸이 있어도 무해하지만, 다르면 `stream.ts` 의 타입 한 줄이다.
3. **메모 줄에 시각이 없다.** `Line` 계약에 `created_at`·`at_ms` 가 없어, 스크립트 탭의 메모 행은 **이 세션에서 던진 순간의 경과 시간**을 쓴다. 새로고침하면 그 시각이 사라진다 — 줄에 시각을 실어 주면 그대로 해결된다(계약 요청).
4. **끝난 회의의 원문을 다시 읽는 계약이 없다.** 「스크립트」 탭은 진행 중에만 값이 있고, 그 밖에는 `scriptEmpty` 자리만 선다.
5. **메모를 쓸 수 있는지를 서버가 말해 주지 않는다.** `created_by === personaId` 로 갈랐다 — `can_write_memo` 같은 필드가 오면 그것으로 바꾸는 게 옳다(권한은 서버가 정한다는 규칙에 맞다).
6. **`OQ-305`(업스트림 승계)** — 시작한 사람이 나가면 오디오가 멈춘다. 승계 갈래를 만들지 않았다(계약에 없다).
