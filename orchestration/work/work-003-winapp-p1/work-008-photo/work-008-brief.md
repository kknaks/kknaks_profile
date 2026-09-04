# [winapp] WORK-008 — 사진 수집 (URL 다운로드·로컬 저장·미디어 서빙·<img>)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋·PR 코디.

## 1. SSOT (read-only 절대경로)
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-006-photo-collection.md` ← **계약 SoT.**
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/10-decision/decision-006-photo-collection.md` / `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/00-baseline/baseline-007-photo-collection.md`
- 기존 코드: import.rs(델타 수집)·watch.rs(폴링)·server.rs(API/AppState/키캐시)·store.rs·ui/index.html(탭2 렌더).
- 직전 사진 spike 결과(네가 함): talkmedia.edb(chatMsgTokenJunction logId→token, tokenInfo token→url,fileSize,checkSum[SHA1]) memory harvest 키로 복호됨. 채팅사진 URL=talk.kakaocdn.net, **최근=200/오래됨=410**. .cng 복호는 범위 밖(BASE-008 백로그).

## 2. 구현 (SPEC-006)
1. **사진 수집 파이프**: 델타 수집(import_room/폴링)에서 **사진 타입 메시지** 식별(type 코드 — 실데이터로 확인). 그 logId → talkmedia.edb 조회(token→url,fileSize,checkSum). talkmedia 복호는 기존 harvest 키 재사용.
2. **다운로드·저장**: URL GET → 200 이면 바이트 확보 → **checkSum(SHA1)·fileSize 검증** → 로컬 미디어 스토어 저장(예 `%LOCALAPPDATA%\mykakao\media\<chatId>\<logId>.<ext>` 또는 DB blob, 택1). 상태=`saved`. **410/404=`lost`(유실, 재시도 안 함)**. 실패=`pending`(다음 델타에 재시도 가능).
3. **미디어 상태 DB**: `media(chat_id,log_id,mime,status,path/blob)` 또는 message 확장. 우리 SQLite.
4. **서빙**: `GET /api/media/<chatId>/<logId>` → 저장 이미지 바이트(Content-Type mime), 없으면 404.
5. **메시지 표식**: `/api/messages` 사진 메시지에 `kind:"photo"` + `media_status`(saved|lost|pending).
6. **탭2 렌더**(ui/index.html): 사진 메시지 → saved면 `<img src="/api/media/<chatId>/<logId>" loading="lazy" style="max-width">`, pending=로딩, lost="유실됨" placeholder+아이콘. "사진" 텍스트 대체.

## 3. 안전 (불변)
- **URL·토큰·checkSum 원값·이미지 내용을 로그·리포트·커밋에 남기지 마라** — host·status·크기·일치여부·개수만. 이미지는 **로컬 저장·외부 전송 0**(다운로드는 카카오 CDN 에서 GET 만).
- 원본 DB 읽기만·카톡 무변조·SAC 미변경·키 RAM only·복호 임시본 RAII. 미디어 스토어는 우리 것.
- HTTP 다운로드에 새 crate 가 필요하면(reqwest 등) **먼저 보고**(SAC — proc-macro/build-script 리스크; 가능하면 기존/std 로). `win_app/` 밖·문서 SoT 수정 금지.

## 4. 검증 (개수/유무만, 이미지·URL 원값 미출력)
```
cargo build --release(SAC 통과·새 crate 보고) + cargo test. 실기동: 최근 사진 있는 방 수집 → talkmedia URL 200 다운로드 → 로컬 저장 → checkSum 일치 → /api/media 200 image 확인. 탭2 <img> 표시(육안). 만료 사진 → lost "유실됨". 값 미출력. 검증 1회.
```

## 5. 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "WORK-008 사진 수집 완료: <한 줄>" --body "수집 파이프/다운로드·checkSum/미디어 스토어//api/media/탭2 img·유실/새 crate 여부/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] WORK-008 사진 수집 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히거나 crate 필요하면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`
