# WP-006 Phase 5 — 자료·공유 실계약 배선 결과 보고

## 상태: done

## 1. 변경 파일

| 파일 | 무엇 |
|---|---|
| `frontend/src/viewModels.ts` | `MeetingMaterial` · `MeetingMaterialFailure` · `MeetingMaterialUpload` · `MeetingViewer` |
| `frontend/src/api.ts` | 자료 다섯(`readMeetingMaterials`·`attachMeetingMaterials`·`detachMeetingMaterial`·`meetingMaterialContentUrl`·`readMeetingMaterialText`) · 공유 셋(`readMeetingShares`·`shareMeetingWith`·`revokeMeetingShare`) |
| `frontend/src/meetings/AttachModal.tsx` | **실계약으로 다시 씀** — 다중 업로드 · 부분 성공 · 422 전부 실패 |
| `frontend/src/meetings/ShareModal.tsx` | **실계약으로 다시 씀** — `basis` 목록 · `member_ids` 다중 공유 · 거두기 |
| `frontend/src/meetings/MaterialDrawer.tsx` | **신규** — PDF 는 `object`, Markdown 은 글자로 (시안대로 드로어 하나) |
| `frontend/src/DropZone.tsx` · `src/FileList.tsx` | **신규 범용 부품** (D25) |
| `frontend/src/meetings/MeetingDetailPage.tsx` | 자료 목록 서버 읽기 · 올린 사람만 × · 드로어 · `personaId` 복귀 |
| `frontend/src/styles.css` | `.drop-zone` · `.file-*` · `.material-frame` |
| `frontend/src/App.tsx` | `personaId` 다시 넘김 |
| `frontend/src/meetings/MeetingMaterials.test.tsx` | **신규 9건** |
| 기존 테스트 4개 | 새 api 모킹 + 드로어 테스트 재작성 |

## 2. 계약 준수 — 경로별

| 경로 | 화면이 하는 것 |
|---|---|
| `GET …/materials` | 탭이 서는 사람(참석·공유)만 읽는다. 목록은 `FileList` 한 줄씩 |
| `POST …/materials` | multipart 필드 이름 **`files`**, 여러 파일 한 번에. `Content-Type` 을 손으로 정하지 않는다(경계는 브라우저가 붙인다) |
| 부분 성공 201 | **붙은 것은 목록에서 빠지고 못 붙은 것만 사유와 함께 남는다.** `T04` 를 내고 **모달을 닫지 않는다** — 남은 것을 보여야 한다 |
| 전부 실패 422 | `detail.failed` 의 사유를 같은 자리에 낸다. `too_large`→`T01` · `unsupported_type`→`T02` (확정 문구 그대로 · M15) |
| 진행 중 409 | 화면이 먼저 막는다 — [자료 첨부]도 `×` 도 서지 않는다(서버 409 와 짝) |
| `DELETE …/materials/{mid}` | **`uploaded_by === personaId` 인 줄에만 ×.** 확인 뒤 떼고 목록을 다시 읽는다 |
| `GET …/materials/{mid}/content` | 드로어 본문. PDF 는 `<object data>`, Markdown 은 글자로 받아 `AssistantMarkdown` 으로 읽는다. [내려받기]는 같은 주소의 `<a>` |
| `GET …/shares` | 「볼 수 있는 사람」 표 — `basis` 가 참석/열람 배지를 가른다 |
| `POST …/shares` | **`{member_ids: […]}` 다중** (P1·2 의 한 명씩 호출을 고쳤다). 응답이 갱신된 목록이라 그대로 갈아 끼운다 |
| `DELETE …/shares/{id}` | `basis === "share"` 인 줄에만 [삭제]. 응답 본문(회의 한 줄)은 쓰지 않고 **목록을 다시 읽는다** |
| 이미 볼 수 있는 사람 | 검색·조직도 결과에서 뺀다 — 참석이든 열람이든 같다 |
| 알림 | 성공 문구는 「공유했습니다.」 하나. 「알림」이라는 말이 나가지 않는다 (§2.2) |

## 3. 검증

```
npx tsc --noEmit                            → 0 에러
npx vitest run src/meetings/                → 5 files · 61 tests 통과 (신규 9)
npx vitest run src/App.test.tsx
        src/chat/ResourcePeek.test.tsx      → 30 tests 통과 (프롭 변경 무영향 확인)
```

신규 9건: 올린 사람만 × · 진행 중 첨부·삭제 없음 · 부분 실패 표시 · 전부 실패 422 표시 · 고르는 시점 판정 · `basis` 별 [삭제] · 이미 있는 사람 제외 · 다중 공유와 알림 문구 없음 · 공유받은 사람 조작 0. 드로어(인라인 아님)는 `MeetingDetail.test.tsx` 의 기존 테스트를 실계약으로 다시 써서 덮었다.

자기점검: `api.ts`·`stream.ts` 밖 `fetch`/`WebSocket` **0** · hex **0** · `TODO(WP-005)` **0**(마지막 하나까지 걷었다).

## 4. DS 추가 후보 (D25)

| 이름 | 자리 | 쓰인 곳 | props · 상태 | 로컬 클래스 |
|---|---|---|---|---|
| **`DropZone`** (신규) | `src/DropZone.tsx` | `AttachModal`. 파일을 받는 화면이 이 제품에 여럿인데(회의 자료 · 업무 자료 · 요청 증빙) 저마다 다르게 생겨 있었다 | `hint` · `pickLabel` · `accept?` · `onFiles` · `disabled?` · `children?` / 기본 · **끌어다 놓는 중**(`over`) · 비활성. **받는 것을 스스로 판단하지 않는다** | `.drop-zone(.over)` |
| **`FileList`** (신규) | `src/FileList.tsx` | `AttachModal`(고른 파일) · 자료 탭(붙은 자료) | `label` · `rows[{key, name, size?, reason?, onOpen?, onRemove?, removeLabel?, active?}]` / 기본 · **`reason`**(못 붙은 줄 — 이름이 흐려지고 사유가 옆에) · `active`(지금 열린 줄) | `.file-list` · `.file-row(.active)` · `.file-open` · `.file-name(.muted)` |
| `Composer` · `GutterList` · `StatusNote` | `src/` | (P3·P4 그대로) | — | `.composer*` · `.gutter-*` · `.status-note` |
| `MaterialDrawer` | `meetings/` **유지** | 자료 미리보기 | 회의 자료 계약(`content_type` · `material_id`)이 붙은 도메인 부품이다. 안쪽은 DS 의 `Drawer` 를 그대로 쓴다 | `.material-frame`(문서 뷰 틀) |

## 5. 임시 문구

**이번 라운드에 새로 지은 문구는 없다.** 자료·공유는 시안이 확정 문구를 다 갖고 있다 — `T01`·`T02`·`T03`·`T04`(첨부) · `T01`~`T03`(공유) · `T29`/`T30`(자료 삭제) 전부 원문 그대로다. 앞서 올린 임시 문구(`OQ-311` 스트림 여섯 + `savedElsewhere`·`alreadyRequested`·`titleCandidate`)는 그대로 남는다.

## 6. 미결 · 주의점

1. **`MOD-104-T02` 가 데모 범위보다 넓게 말한다** — 「문서 · 이미지 · 압축 파일을 올려 주세요」인데 실제로 받는 것은 PDF · Markdown 둘이다. 확정 문구라 고치지 않았다 (시안 리포트 `M15`). 형식이 굳으면 함께 고쳐야 한다.
2. **`can_detach` 필드가 없다.** 「올린 사람만 뗀다」를 화면이 `uploaded_by === personaId` 로 맞춰 본다 — 서버가 말해 주면 그것으로 바꾸는 게 옳다(권한은 서버가 정한다는 규칙). 그래서 `personaId` 프롭이 다시 들어왔다.
3. **`DELETE /shares/{id}` 의 응답이 목록이 아니라 회의 한 줄이다** (브리프는 「200 목록」이라 했다). 본문을 쓰지 않고 목록을 다시 읽어 우회했다 — BE 가 목록으로 맞추면 왕복 한 번이 준다.
4. **고르는 시점의 판정을 남겨 두었다** — 24MB 짜리를 다 올리고 나서 「크다」는 말을 듣지 않게 한다. **판정의 정본은 서버**이고 통과한 것도 서버가 되돌릴 수 있으며 그 사유가 같은 자리에 선다. 규칙이 두 곳에 있는 셈이라, 한도·형식이 바뀌면 `AttachModal` 의 상수도 함께 고쳐야 한다.
5. **PDF 뷰는 브라우저에 맡긴다** — `<object data>`. 렌더러를 싣지 않았다(번들·범위 밖). 브라우저가 못 열면 그 자리에 빈 상태가 선다.
