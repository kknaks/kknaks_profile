# [winapp] spike — 사진(이미지) 획득 경로 규명 (attachment / .cng / URL)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. **탐색(spike) — PR·커밋 없음.** 조사만.

## 배경
현재 사진 메시지가 화면에 "사진" 텍스트로만 뜬다(우린 message 텍스트 컬럼만 읽음). 실제 이미지를 표시하려면 attachment/캐시를 알아야 한다. 카톡 실행 중(키 회수 가능).

## 조사할 것 (값은 마스킹 — 원본 URL/토큰/이미지 비노출, 구조·필드명·존재여부만)

1. **사진 메시지의 전체 컬럼**: `chatLogs_<chatId>.edb` 복호(기존 decrypt 경로) 후, **type 이 사진인 행**의 모든 컬럼을 본다 — 특히 `attachment`(JSON), `v`, `referer`, `supplement` 등. 사진 메시지의 attachment JSON 에 **뭐가 들었나**: 이미지 URL(호스트/스킴만)·썸네일 URL·width/height·캐시키·파일명. (김태우 방에 사진 메시지 3개 있음 — 그 방 chatId 로.)
2. **로컬 캐시 매핑**: `chat_data\url_image_v2.edb`·`talkmedia.edb`(SQLCipher) 를 복호해 스키마 확인 — attachment/URL → 로컬 `.cng` 파일 매핑이 어떻게 되나(테이블·컬럼명만).
3. **.cng 포맷**: `chat_data\url_image_v2\*.cng` 파일 매직바이트·크기·엔트로피로 암호화 방식 추정. SQLCipher 계열인가, 별도 스킴인가(복호 가능성 판단만, 실제 복호는 하지 마라).
4. **URL 접근성**: attachment 에 이미지 URL 이 있으면, 그게 **직접 열리는지**(HEAD 요청 status 코드만 확인 — 이미지 저장 금지, 토큰/URL 원문 로그 금지) 또는 만료/인증 필요한지. curl 로 status 만.

## 판정
- **(A) URL 경로** — attachment URL 이 직접 접근 가능 → 쉬움. 어떤 필드에 어떻게.
- **(B) 로컬 .cng 복호** — URL 이 안 되거나(만료/인증) 오프라인이 나음 → .cng 복호 필요. 방식·난이도.
- **(C) 하이브리드** — 썸네일은 캐시/URL, 원본은 다른 경로 등.
→ 각 경로의 **구현 난이도 + 다음 스텝**을 근거와 함께.

## 안전 (불변)
- 카톡 무변조·원본 읽기만·SAC 미변경·키 RAM only. 복호 사본 RAII.
- **이미지 원본·URL 원문(토큰 포함)·본문·키를 로그·리포트·커밋·출력에 남기지 마라.** 구조/필드명/status/개수/지문만. 실제 이미지 파일 저장·커밋 금지.
- 새 crate 함부로 추가 금지(HEAD 요청은 std/기존으로, 부득이하면 보고). `win_app/` 밖·문서 SoT 수정 금지.

## 검증
탐색이라 통상 검증 없음. 조사 스크립트는 재현 명령을 리포트에 적고, 값은 마스킹. cargo 쓰면 build 만.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "사진 획득경로 spike: <판정 A/B/C 한 줄>" --body "attachment 구조/캐시 매핑/.cng 포맷/URL 접근성/판정+난이도+다음스텝"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 사진 spike <판정> — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`
