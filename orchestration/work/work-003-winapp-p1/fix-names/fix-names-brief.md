# [winapp] Windows V2 수정 — 방/작성자 실이름 해석 + import 대상·UX

너는 **mykakao `winapp` 워커**다. **P1~P3 를 네가 만들었다** — 같은 워크트리·크레이트를 수정한다. 안전·자원 규칙 그대로.

워크트리: `C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1` (P3 커밋 `3583361` 위에)
브랜치: `work-003-winapp-p1`. PR 은 코디. **커밋 금지.**

> 사용자가 실기동해서 두 결함을 찾았다. 실제 데이터로 검증하며 고쳐라 — 단위테스트만으로 "됐다" 하지 마라.

## 1. 사용자가 발견한 결함 (코디 실측 확인)

**(A) 방/작성자 이름이 전부 난수(chatId·userId)로 뜬다.**
- 코디 진단: `/api/rooms` **51개 방 중 실이름 해석 = 0개** (전부 "대화방 <chatId>" fallback). 네가 P3 에서 넣은 닉네임 조인·enrich_titles 가 **실경로에서 작동 안 함**.
- **데이터는 있다**: `TalkUserDB.edb`(닉네임)·`chat_data/chatListInfo.edb`(방 목록/제목) 둘 다 **카톡이 열고 있어(잠김) 복호 가능**. 즉 못 고칠 문제가 아니라 **코드/스키마 버그**다.
- 사용자 요구: 방 이름이 **단체방인지 1:1인지** 구분되고 실제 이름이 보여야 한다. 1:1 이면 상대 이름, 단체면 방 제목/멤버.

**(B) "과거 가져오기" 가 0행 + 엉뚱한 방을 가져온다.**
- 사용자가 방 `15034819498347`(체크)를 골랐는데 결과는 `#906847525:0`(③에서 보던 방). 즉 **import 가 체크된 방이 아니라 ③ 뷰어의 방을 가져왔다.** 게다가 그 방은 "닫힘"이라 키가 없어 0행.
- 근본 제약: **키는 그 방이 카톡에서 "열림"일 때만 메모리에 있다.** 지금 열린 방은 소수(3개). 닫힌 방은 import 불가.

## 2. 고칠 것

### (A) 실이름 해석 — 최우선
1. `chatListInfo.edb` + `TalkUserDB.edb` 를 **실제 복호해 스키마를 직접 확인**하라(테이블·컬럼). P3 의 가정이 틀렸으니 **실 데이터로 재확인**. (복호는 P1 decrypt 파이프 재사용. 사본·읽기전용·임시본 RAII.)
2. **방 제목 해석**: 단체방 → 제목(subject/title). 1:1 → 상대 userId 의 nickName. **방 타입(group/direct) + 멤버수**를 산출.
3. **작성자 해석**: TalkUserDB userId→nickName 로 `/api/messages`·SSE 의 `author_name` 채움(지금 0개 해석 → 실제 이름).
4. `/api/rooms` 응답에 `title`(실이름) + `kind`("group"/"direct") + `member_count` 추가. UI ②③ 에서 "단체/개인" 과 실이름 표시.

### (B) import 대상 + UX
5. **"과거 가져오기" 는 ② 체크된 방들을 가져온다**(③ 뷰어 방 아님). 여러 개면 각각.
6. **열림 방만 import**. 닫힌 방을 고르면 스킵하고 명확히 안내: "이 방은 닫혀 있음 — 카톡에서 방을 열고 다시 시도". ①/② 에 열림/닫힘을 정확히 표시(이미 badge 있음 — 정확성 확인).
7. (선택) import 버튼 옆 안내: "열린 방만 가져올 수 있어요. 카톡에서 방을 여세요."

## 3. 안전 (불변)

- 실 방제목·닉네임·본문은 **UI 응답에만**. **로그·리포트·커밋·진단출력에 절대 남기지 마라**(마스킹/카운트만). applog 규율 유지.
- 원본 read-only, 복호 사본 RAII 삭제, 키 비상주, 카톡 무변조, SAC 미변경.
- 스키마 확인용 복호 출력도 **컬럼명·행수만**, 값(이름/본문) 미출력.

## 4. allowed_paths / 범위

- `win_app/` 만. 새 crate 추가 금지(SAC — proc-macro/build-script 새로 끌면 또 막힌다). 부득이하면 보고.
- 계약 변경(응답에 필드 추가는 OK, 기존 키 의미 변경은 보고).

## 5. 검증

```
cd win_app && cargo build --release(SAC 통과 필수, 차단0) + cargo test. cargo=~/.cargo/bin.
- **실 데이터 검증**: 열린 방 하나로 /api/rooms 가 실제 방이름·kind·member_count 를 주는지, /api/messages author_name 이 실제 닉네임인지 **개수/유무만** 확인(이름 원값 미출력).
- 닫힌 방 import 시 스킵+안내 동작 확인.
- 검증 1회. 못 한 건 못 했다고.
```

## 6. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령 모두** 실행.

```bash
orca orchestration send   --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle>   --type worker_done   --task-id <preamble taskId> --dispatch-id <preamble dispatchId>   --subject "winapp 이름해석 수정 완료: <한 줄>"   --body "chatListInfo/TalkUserDB 실스키마 / 방이름·kind·author 해석 결과(개수) / import 대상·UX / cargo 수치 / 미결"

orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed   --text "[worker_done] winapp 이름해석 수정 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`
