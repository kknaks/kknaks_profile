# 코드 검수 — WORK-012 WP1 (BE + FE)

- 검수자: reviewer(read-only) · 2026-10-07
- 대상: 코드 워크트리 `strong-hajin-enhance`(base `f0ad522`)의 **미커밋 변경 전부**
  - 수정 42파일(+924/−136) · 새 파일 4(`test_meeting_agenda_source.py` · `test_meeting_due_dates.py` · `test_user_event_hub.py` · `InboxAttachments.test.tsx`)
- 계약: WORK-012 「Phase WP1-BE」·「Phase WP1-FE」 · Code Surface WP1 표 · SPEC-010 §2.1·§2.3·§4.2·§4.3(참석자)·§4.8 · SPEC-008 §2.2·§4.4·§5 · SH-IMP-020
- 워커 리포트: `be-wp1-report.md` · `fe-wp1-report.md`
- 한 일: `git diff` 전부 읽음 · 호출자·쓰는 곳을 `rg` 로 다시 셈. **시험·빌드·서버는 돌리지 않았다** — 수치는 워커 리포트 값이다.
- 약어: `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/` · `T/` = `backend/tests/`

---

## 0. 판정 — **WARN**

계약 체크박스는 BE 7/7 · FE 5/5 · SH-IMP-020 1/1 모두 구현됐다. Code Surface WP1 표의 자리도 빠짐없이 닿았다.
BE↔FE 계약(안건 `source` · `download=1` · 받기/원본 주소 · `integration.changed`)도 서로 맞는다. **FAIL 은 없다.**

남는 것은 WARN 7건이다. 둘이 앱 E2E 전에 결정이 필요하다.

1. **받기 링크가 같은 탭이 됐다** — 첨부 중계가 실패하면(상류 502 · 남의 것 404) 웹 메시지함 화면이 **JSON 오류 페이지로 넘어간다.**
2. **AX 로 만든 「다음 회의」 의 안건이 더는 자동으로 `carried` 가 되지 않는다** — AX 정책에 출처 지시가 없다.

---

## 1. 계약 체크박스 — 구현 위치

### WP1-BE (7/7)

| 계약 | 구현 | 판정 |
|---|---|---|
| 005 안건 출처(안건별 · `carried` 단독 = 422 · 추가 입구는 `carried` 불가 · AX `meeting_create` 같은 모양) | 생성 전용 모델 `B/modules/meetings/commands.py:138-142`(`source: Literal["manual","carried"] = "manual"`)<br>옛 `MeetingAgendaDraftInput` 은 제목만(`:130-132` — 추가 입구 `mcp.py:905,1779` · `http.py:87` · `bootstrap/application.py:3889` 가 그대로 씀)<br>규칙 `domain.py:155-170` · 예외 `:58-65`<br>생성 `application.py:415-419` · 저장 `:330-332`<br>HTTP `http.py:560-565`(422 `{code,message}`) · `:930`<br>AX 제안 동결 `platform/actions.py:316-324` | PASS — 회의 단위 판정 줄(`source = "carried" if carried …`)이 지워졌다 |
| 002 수정 참석자 합치기 | `commands.py:207-210`(`MeetingInfoPatch.validate_times` 안 · 생성 `:165-166` 과 같은 식) | PASS |
| 006 기한(이월만 · 취소 제외 · 뒤에 시작 · KST · 하한 · 프롬프트·스키마) | 쿼리 `platform/meetings.py:786-800`<br>`_office_day` `application.py:2001-2003`(이미 import 된 `rooms.OFFICE_TIMEZONE`)<br>재료 `:819,821,839,840`<br>`floor_due`·`resolve_due` `finalize.py:205-230`<br>서비스 `finalize_service.py:262`<br>배치 잠정 `application.py:1528,1555`<br>프롬프트 `finalize.py:350-351,396`<br>스키마 설명 `ai_final_output.json:130` · `ai_batch_output.json:103` | PASS |
| 014 받기 `?download=1` → 언제나 `attachment` | `B/entrypoints/http_inbox.py:121-138`(`force_attachment`) · 메일 `:243-254` · 방 `:256-270` | PASS |
| 018 원격 SVG(바이트 판정 · HTML 거절 · docstring 셋) | `sniff_svg` `B/platform/external_inbox_upstream.py:70-87` · 판정 `:383`<br>docstring `:9-12` · `:54` · `inbox_html.py:8-10` · 라우트 `http_inbox.py:276-277` | PASS |
| 018 원격 이미지 응답 `inline` | `_remote_image` `http_inbox.py:141-156` · 라우트 `:282` | PASS — `_download` 를 더는 지나지 않는다 |
| 010 `integration.changed` 저장마다 · 1초 묶기 | 실시간 저장 `sync_store.py:217-222`(옛 `return` 제거)<br>진행 칸 `:40-42,258-264,276-282`<br>카톡 `kakao_ingest.py:266-267`<br>묶기 `platform/user_event_hub.py:88-116` | PASS(§4 주의 하나) |

### WP1-FE (5/5 + SH-IMP-020)

| 계약 | 구현 | 판정 |
|---|---|---|
| 002/004 일정 칸 | `F/styles/meetings.css:148-157`<br>— 날짜 `flex: 0 1 200px; min-width: 0`<br>— 수정 모달 안에서만 시각 한 쌍 축소 | PASS(실측 아님 — §6) |
| 002 중복 | `addPersonOnce` `F/features/meetings/PeoplePicker.tsx:12-19` → `MeetingEditModal.tsx:231` · `ShareModal.tsx:109,123` | PASS |
| 005 불러오기 시간 유지 · 안건별 `source` · 문구 | `BookingModal.tsx:199-208`(`setDate/From/To` 삭제)<br>제출 `:249-250` · API 타입 `lib/api.ts:1228-1229`<br>`labels.ts:750` 「새로 추가된 안건」 | PASS |
| 014 받기 주소 · 원본 보기 앱/웹 | 받기 함수 `api.ts:1682-1694`<br>`InboxAttachments.tsx`: `DownloadLink` `:45-52` · `downloadAll` `:87-99` · `Linked` `:101-105` · 조립 `:292` · `Thumb` `:175-205`(`hasShell()` `:189`)<br>방 `RoomView.tsx:547` + prop 길 전부<br>메일 `MailView.tsx:391-416` | PASS |
| 010 설정 화면(확인만) | 코드 변경 없음 · 시험 `SettingsPage.test.tsx` | PASS |
| SH-IMP-020 「빠른 회의」 | 새 상수 `labels.ts` `meetingScreen.quickStart` → `MeetingListPage.tsx:190`<br>상세 `MeetingDetailPage.tsx:1040` 은 `start`(「회의 시작」) 그대로 — 다시 셈: `meetingScreen.start` 쓰임 1 · `quickStart` 쓰임 1 | PASS — 공유 상수를 갈랐다 |

---

## 2. Code Surface 전수 — 다시 센 것

| 표의 행 | 다시 센 것 | 판정 |
|---|---|---|
| 005 ② 안건 입력 모델 | `MeetingAgendaDraftInput` 쓰임 7줄<br>— 생성만 새 모델로<br>— 추가 입구 넷(`mcp.py:90,905,1779` · `http.py:87` · `bootstrap/application.py:140,3889`)은 옛 모델 그대로 | PASS |
| 005 ② `manual` 을 정하는 자리(F-4) | `application.py:467,564,1225` · `BookingModal.tsx:443` — 값은 그대로, 문구만 `labels.ts:750` 하나로 바뀐다 | PASS |
| 006 기한 | `next_meeting_after` 호출자 **하나**(`application.py:793`)<br>`resolve_due`/`finalize_notes` 호출자 하나(`finalize_service.py:253`)<br>`due_candidate` 를 쓰는 곳 = 배치 잠정 `:1555`(하한 걸림) · 최종 적재 `:937`(이미 `finalize_notes` 가 하한을 걸고 온 값) · 승격 `bootstrap/application.py:2015,3867`(그대로 — 맞음) | PASS |
| 006 KST | `OFFICE_TIMEZONE =` 셋 그대로 · 새 상수 없음 | PASS |
| 014 받기 링크 · 주소 · F-3 | `<Thumb` 3 · `<AttachmentList` 1 · `<FileCard` 5 — 받기 주소를 받아야 하는 것은 모두 받는다<br>`MailView.tsx:222` · `RoomView.tsx:350` 의 `FileCard` 는 보낸 답장·로컬 줄이라 주소 없음 — 맞음<br>`AttachmentList` 의 `downloadOf` 는 필수 prop 이라 빠진 호출자가 있으면 빌드가 깨진다 | PASS |
| 014 서버 disposition | `_download` 쓰는 곳 셋 → 메일·방 첨부는 `force_attachment`, 원격 이미지는 `_remote_image`<br>`http.py` 회의 자료·업무 첨부 disposition 은 diff 없음 | PASS |
| 018 SVG | `REMOTE_IMAGE_TYPES`(`external_inbox_upstream.py:91`)에 SVG 를 더했지만 **쓰는 곳이 0**(죽은 상수) — 무해 | PASS(참고) |
| 010 사건 | 사건을 내는 여섯 자리 중 바뀐 셋(실시간 저장 · `update_integration`/`update_room` · 카톡)<br>`_changed` 를 부르는 나머지(`set_room_access` · `mark_disconnected`)는 그대로 · 묶기 대상 | PASS |
| 운영 인벤토리 | `docs/unified-operations-inventory.json` 3항목만 패치 — WORK-012 · `AGENTS.md` 가 정한 처리 | PASS(allowed_paths 밖이지만 계약이 시킨 파일) |

---

## 3. BE↔FE 계약 일치

| 계약 | BE | FE | 판정 |
|---|---|---|---|
| 안건 `source` | `Literal["manual","carried"]` · 기본 `manual` · `carried`+이어온 회의 없음 = 422 `{code:"AGENDA_SOURCE_INVALID"}` | 불러온 미결 = `carried` + `setCarried`(`BookingModal.tsx:224-227`) · 손 = `manual` · [다음 회의 예약] = 초안 `carried` + `carriedFrom` | PASS — FE 는 이어온 회의 없이 `carried` 를 보낼 길이 없다 |
| 422 의 `detail` 모양 | `detail` = **객체** `{code, message}` | `api.ts` 는 `typeof detail === "string"` 만 메시지로 쓴다(`:123,167` 등) → 화면 문구는 `Unprocessable Entity` | WARN(경미) — 위 대로 FE 가 낼 일이 없어 실해는 없다. 생길 경우를 대비해 `bookMeeting` 이 `detail.code` 를 읽게 하는 것은 2루프 |
| `download=1` | 메일·방 라우트 `download: bool = Query(False)` · 원격 이미지·썸네일(`variant=thumb`)엔 없음 | `…/attachments/{aid}?download=1` — 원본 주소에 `?` 가 없어 붙는 모양이 맞다. 썸네일 주소엔 붙이지 않는다 | PASS |
| 받기/원본 주소 | 같은 라우트 · 쿼리로 가름 | `href`(원본) · `downloadHref`(받기) · `thumb`(미리보기) 셋 | PASS |
| `integration.changed` | `{member, integration_id, room_id?, source_kind, data}` — 묶일 때 방이 여럿이면 `room_id=None` | `SettingsPage.tsx:184` · `InboxPage.tsx:143` 은 `type` 만 보고 다시 읽는다 — `room_id`·`data` 에 기대지 않는다 | PASS |

---

## 4. 회귀 위험

| 물음 | 본 것 | 판정 |
|---|---|---|
| 기한 규칙이 다른 호출자에 새나 | `next_meeting_after` 호출자 하나 · 재료의 `next_meeting_on` 은 최종 프롬프트에만 쓰인다<br>상태 조건이 `== scheduled` → `!= cancelled` 로 바뀌어 **진행 중·끝난 이월 회의도 「다음 회의」 가 된다** — SPEC §4.8 과 맞음<br>`meeting_starts_on` 은 기본값 `None` 이라 옛 경로·대역에선 하한이 걸리지 않는다(워커 리포트 §7-3) | PASS |
| `download=1` 이 미리보기 경로에 새나 | 썸네일(`thumbOf`) · 메일 `src` · 원격 이미지는 받기 주소를 쓰지 않는다 · 서버도 기본값 `False` | PASS |
| SVG 허용이 첨부(`_download`) 경로에 새나 | `_download` 는 바뀌지 않았다 — `INLINE_IMAGE_TYPES` 넷 + `inline_media_type`(PDF·Markdown)만 `inline`, SVG 첨부는 여전히 `attachment`<br>SVG 판정은 `SafeImageFetcher`(원격 이미지) 안에만 있다 | PASS |
| 공유 상수 분리(「빠른 회의」) | `start` 는 상세 단추 한 곳이 계속 쓰고, 목록 머리만 `quickStart` | PASS |
| **AX 회의 생성의 출처** | 옛 서버는 `carried_from_meeting_id` 가 있으면 **안건 전부를 `carried`** 로 적었다. 이제는 안건마다 `source` 를 받고, 안 주면 `manual` 이다.<br>그런데 AX 회의 생성 정책·도구 설명(`codex_cli.py` `MEETING_CREATION_POLICY` · `tool_catalog.py`)에 `source` 지시가 **0**(`rg carried` 결과 없음).<br>→ AX 로 「지난 회의 이어서 다음 회의 잡아 줘」 를 하면 넘어온 안건도 「새로 추가된 안건」 으로 선다 | **WARN(BE)** — SPEC-010 §4.2 「출처를 안 주면 `manual`」 과는 맞지만, 사용자에겐 10-07 이전보다 나빠진 표시다. AX 정책에 「이어온 회의의 미결 안건은 `source:"carried"`」 한 줄(WP3 의 AX 회의 생성 작업과 묶어도 된다) |
| 1초 묶기의 타이머 | 운영 기본값은 `threading.Timer`(데몬) · 듣는 쪽 한 곳에만 있다<br>계약 시험(SQLite)에서도 앱이 만든 허브가 진짜 타이머를 띄운다(`bootstrap/external_inbox.py:83`) — 라이브러리 스레드라 `conftest` 걸개 대상이 아니고 워커 수치상 통과<br>창 안 둘째 사건이 최대 1초 늦게 온다 — **같은 연동의 `integration.changed` 를 연달아 단언하는 시험이 생기면 흔들릴 수 있다** | WARN(경미 · BE) — 지금 시험엔 해당 없음. 시험용 앱 공장에서 `coalesce_seconds=0` 을 넘기는 것을 권장 |
| 실시간 1건마다 연동 재읽기 | 이제 메시지 한 건마다 `integration.changed` 도 나간다 → `InboxPage.tsx:143` 이 **연동 목록을 다시 GET**(초당 최대 1회/연동) | WARN(경미) — SPEC 이 받아들인 비용이다. 운영 부하 관찰만 |

---

## 5. 시험이 계약을 잡나

| 시험 | 판정 | 비고 |
|---|---|---|
| `T/contract/test_meeting_agenda_source.py`(10) | 강함 | 출처별 저장 · 422 코드 · 추가 입구 거절 · AX 동결 거절까지 응답 본문으로 단언 |
| `T/contract/test_meeting_due_dates.py`(5) + `test_meeting_finalize.py`·`test_meeting_memo_batch.py` 추가분 | 강함 | 경로 (a)(b)(c)(d)를 KST 날짜로 계산해 비교. 10-07 모양(같은 owner 같은 날 오후) = `null` |
| `T/unit/test_user_event_hub.py`(2) | 강함 | 타이머 대역으로 창 열림·밀림·방 합치기·다음 창을 순서대로 단언 |
| `T/contract/test_external_inbox.py` 추가분 | 강함 | `download=1` × 이미지·PDF·기타의 disposition · 머리 셋 유지 · 원격 SVG `inline`+CSP |
| `T/integration/postgres/…` 추가분 | 강함 | NOTIFY 페이로드로 실시간 1건·커서만·무관 칸 |
| `F/features/meetings/MeetingEditModal.test.tsx` 「CSS」 | **약함** | `meetings.css` 를 글자로 읽어 규칙 문자열이 있는지만 본다 — 규칙을 같은 뜻으로 고쳐 써도 깨지고, 넘침 여부는 증명하지 못한다(jsdom 한계 — 워커도 명시). 완료 판정은 앱 E2E 에 기대야 한다 |
| `F/features/inbox/InboxAttachments.test.tsx`(10) | 강함 | 앱/웹 갈래를 셸 전역 대역으로 나눠 `href`·`target` 을 단언 · 받을 수 없는 첨부에 링크 없음 |
| `F/features/meetings/MeetingList.test.tsx` · `MeetingAfter.test.tsx` | 강함 | 제출 페이로드 `agendas` 를 `toEqual` 로 단언 — 두 입구 모두 |
| `F/features/settings/SettingsPage.test.tsx` | 보통 | 화면 쪽 절반(사건 → 다시 읽기)만. 숫자가 실제로 느는지는 BE+앱 E2E 몫 |
| **빠진 시험** | WARN | ① AX `meeting_create` 에 `carried_from` 만 주고 `source` 없이 → 안건이 `manual` 이 되는 것(§4)을 **의도로 고정**하거나 정책을 바꾸는 시험 ② 받기 링크 실패 응답 때 화면 동작(§6-1) |

**프론트 실패 8건**은 두 워커 모두 기준선(`fe-baseline.md` 9건) 안이라고 했다(`CreateWork` · `CreateWorkLayout` · `TaskDetailDates`). 내가 돌려 보지는 않았다 — 코디 확인.

---

## 6. 사람 눈에 이상해 보일 자리(앱 E2E)

| # | 자리 | 무엇이 걸리나 |
|---|---|---|
| H-1 | **받기 실패가 화면을 날린다(웹)** | 받기 링크가 `target="_blank"` 없는 **같은 탭** 링크가 됐다(`InboxAttachments.tsx:45-52` · `MailView.tsx:404`). 성공(`attachment`)이면 화면에 머물지만, 상류 실패 `502` · 슬랙 토큰 만료 · `404` 면 브라우저가 **메시지함을 떠나 JSON 오류 본문 페이지로 이동한다.** 예전엔 새 탭에 떴다. 앱은 셸이 가로채므로 셸의 실패 토스트가 뜨는지 확인 필요 |
| H-2 | **웹 「모두 다운로드」** | 같은 탭 이동을 300ms 간격으로 연달아 누른다. 느린 중계(첫 응답 머리 전)면 다음 이동이 앞 이동을 취소할 수 있다 — 여러 파일 중 일부만 받아질 수 있다(FE 워커도 미측정이라 적음) |
| H-3 | **불러오기 뒤 회의실이 조용히 빈다** | 시간을 더는 가져오지 않으므로, 지난 회의 방(`rooms.find(name)` · `BookingModal.tsx:207`)이 **새 시간의 가용 목록에 없으면 「예약 없음」 으로** 남는다. 예전엔 같은 요일·같은 시각을 넣어 대개 잡혔다. 아무 안내가 없다 |
| H-4 | **AX 로 이어 잡은 회의의 안건 표시** | §4 — 넘어온 안건이 「새로 추가된 안건」 으로 보인다 |
| H-5 | **빠른 회의의 자리표시 안건 · 메모 폴백 안건** | 「새로 추가된 안건」 배지(SPEC H-4 · E2E 확인 항목) — 코드가 계약대로 그렇게 한다 |
| H-6 | **앱에서 썸네일 클릭 = 저장** | 계약(OQ-812 · H-8)대로. 메일 이미지 썸네일도 같다(`MailView.tsx:397`) |
| H-7 | **수정 모달 시각 칸에 시계 아이콘이 없다** | `meetings.css` `.meeting-meta-edit … svg { display:none }`. 생성 모달엔 있다 — 두 모달이 미세하게 다르다(AX 카드와는 같음). 앱 기본 창에서 세 칸이 한 줄에 드는지는 실측 전 |
| H-8 | **기한이 비는 경우가 는다** | 이월 회의가 없으면 「다음 회의 전날」 기한이 더는 생기지 않는다. 같은 owner 의 다른 예약으로 잡히던 기한이 이제 `null` 이 된다 — 맞는 변경이지만 사용자는 「기한이 줄었다」 로 본다 |

---

## 7. FAIL / WARN 목록(재발주용)

### FAIL — 없음

### WARN (7)

| # | 팀 | 자리 | 무엇 | 권장 |
|---|---|---|---|---|
| W-1 | FE(+코디 결정) | `InboxAttachments.tsx:45-52` · `:87-99` · `MailView.tsx:404,416` | 같은 탭 받기 링크 — 실패 응답이면 웹 화면이 오류 JSON 으로 넘어감(H-1) · 「모두 다운로드」 연속 이동 취소 가능(H-2) | 계약(같은 탭 링크)은 SPEC-008 §2.2 그대로라 코드 결함은 아니다 — 웹에서 실패 화면을 어떻게 할지(그대로 둘지 · 웹만 숨은 iframe 으로 받을지)는 코디 결정. 최소: 운영 웹 E2E 에서 실패 첨부 1건·여러 파일 「모두 다운로드」 1회 확인. 앱은 셸 실패 토스트 확인 |
| W-2 | BE | `B/platform/codex_cli.py` `MEETING_CREATION_POLICY` · 도구 설명 | AX 회의 생성에서 이어온 회의 안건이 `carried` 가 되지 않는다(정책에 `source` 지시 0) — 10-07 이전보다 표시가 나빠진다(H-4) | 「`carried_from_meeting_id` 를 줄 때 그 회의의 미결 안건은 `source:"carried"`」 한 줄 + 시험. WP3 AX 회의 생성과 묶어도 된다 |
| W-3 | FE | `BookingModal.tsx:207` | 불러오기 뒤 지난 회의 방이 새 시간에 없으면 조용히 「예약 없음」(H-3) | 안내 한 줄 또는 WP3 회의실 셀렉트에서 처리 — E2E 확인 항목으로 |
| W-4 | FE | `F/features/meetings/MeetingEditModal.test.tsx`(CSS 글자 단언) | 넘침을 증명하지 못하는 시험 — 규칙 문자열에만 묶임 | 앱 E2E 를 AC-01 의 완료 증거로 명시(코디). 시험은 두되 의미를 과신하지 않는다 |
| W-5 | BE | `B/platform/user_event_hub.py` + 시험용 앱 공장 | 계약 시험에서도 진짜 1초 타이머가 돈다 — 연속 `integration.changed` 를 단언하는 시험이 생기면 흔들린다 | 시험 앱에서 `coalesce_seconds=0` 주입 |
| W-6 | FE | `lib/api.ts`(`bookMeeting` 오류 처리) | 422 `detail` 이 객체라 문구가 `Unprocessable Entity` 로 뜬다 — 지금은 낼 길이 없어 실해 없음 | 2루프에서 `detail.code` 를 읽거나 그대로 둠(코디) |
| W-7 | BE | `B/platform/external_inbox_upstream.py:91` | `REMOTE_IMAGE_TYPES` 가 쓰는 곳 0 인 채 SVG 를 더했다(죽은 상수) | 지우거나 그대로(참고) |

### 확인한 것 / 확인 안 한 것

- **확인한 것**
  - diff 전부(BE 16 · FE 17 · 시험 · 인벤토리)
  - 호출자 재계수: `next_meeting_after` · `resolve_due` · `due_candidate` · `MeetingAgendaDraftInput` · `_download` · `Thumb`/`FileCard`/`AttachmentList` · `meetingScreen.start` · `integration.changed`
  - BE↔FE 페이로드 모양
- **확인 안 한 것**
  - 시험·빌드·앱 실물 — 금지 · 코디 몫
  - 데스크톱 셸이 `attachment` 실패 응답을 어떻게 알리는지(셸 코드 `download.rs` 는 이번 diff 밖)
  - 운영 슬랙·Gmail 실물
