# 카톡 Mac DB — 첨부·방·메시지 필드 확인 (읽기 전용 · 사용자 승인)

> architect(kakao) · 2026-10-06 · 앞 조사 `kakao-attach-survey.md` 미결 **AT-1**(attachment JSON 실제 필드)을 닫는다.
>
> **방법**: 사용자 승인("읽기 전용으로 확인") 하에, 본인 Mac 카톡 로컬 DB(`<78hex>`, 카톡 26.1.1)를 scratchpad 로
> **복사**해 그 **사본만** `sqlcipher` CLI 로 열었다. 쓰기·스키마 변경·카톡 조작·발송·CDN 네트워크 접속 없음.
> 키는 kakaocli 방식(기기 UUID + userId → PBKDF2-SHA256) 재현. **SQLCipher compatibility 3** 에서 열림(v26.1.1).
> 사본·키는 조사 뒤 삭제했다.
>
> ⚠ **개인정보 마스킹**: 아래 어디에도 대화 본문·실명·전화번호·실제 URL·실제 파일명을 쓰지 않았다. **키 이름 ·
> 값의 모양 · 호스트 도메인 · 파라미터 이름 · 집계값(개수·TTL)** 만 적는다.
> 근거 표기: `테이블.컬럼` · `type N` = NTChatMessage.type 값 · (집계) = 사본 질의 결과.

---

## §0. 핵심 결론 (결정 아님)

1. **복호 됨 → AT-1 닫힘.** attachment 는 `NTChatMessage.attachment`(TEXT, JSON)에 들어 있고, **사진·동영상·파일은
   JSON 안에 `url`·`thumbnailUrl`(둘 다 서명·만료 CDN 링크)·`expire`·크기·체크섬·MIME 을 갖는다**(§2·§3).
2. **단, kakaocli 로는 이 기기에서 못 연다.** kakaocli `auth` 는 "No candidate user ID produced a valid key" 로 실패
   (앞 조사 §6 이슈 #14·#16 그대로). 원인: **실제 userId 가 `AlertKakaoIDsList` 후보 4개 밖**이었다. 계정 해시
   (`DESIGNATEDFRIENDSREVISION:` 의 SHA-512 역상)를 brute-force 해 **진짜 userId 를 복구**하니 kakaocli 와 동일한
   파생식으로 파일명·키가 정확히 맞고 compat 3 로 열렸다. → **운영에선 userId 를 brute-force(또는 수동 입력)로
   보강해야 한다**(§5 미결).
3. **서버 중복 방지 키 = `(chatId, logId)`** — `logId` 단독은 전역 유일 아님(중복 존재), 조합은 전수 distinct(§6).

---

## §1. 스키마 (표)

**테이블 목록(집계)**: `NTChatMessage · NTChatRoom · NTUser · NTChatContext · NTChatMeta · NTChatThread ·
NTChatLogMeta · NTOpenLink · NTCalendar · NTEvent · NTBookmark · NTMultiProfile · NTSetting · NTChatFolder …`(19개)

### NTChatMessage (메시지) — `NTChatMessage.*`
| 컬럼 | 타입 | 쓰임(관찰) |
|---|---|---|
| `chatId` | INTEGER | 방 FK. **dedup 키 1/2** |
| `logId` | INTEGER | 메시지 번호. **dedup 키 2/2** (단독 유일성 ✗, §6) |
| `authorId` | INTEGER | 보낸 사람 = `NTUser.userId` FK. 0=시스템(§6) |
| `type` | INTEGER | 메시지 종류(§2) |
| `message` | TEXT | 본문(텍스트). 비텍스트는 캡션/빈 값 |
| **`attachment`** | **TEXT(JSON)** | **첨부 메타 — 핵심(§2·§3)** |
| `supplement` | TEXT | 부가(일부 type) |
| `extra` | TEXT | 부가 |
| `localFilePath` | TEXT | **사용자가 수동 저장한 파일 경로만**(§7) — 자동 캐시 아님 |
| `sentAt` | INTEGER | 보낸 시각(epoch **초**, 10자리, §6) |
| `readAt` | INTEGER | 읽은 시각 |
| `prevId`·`msgId`·`status`·`subType`·`scope`·`threadId`·`contentFlag`·`referer`·`revision` | INTEGER | 상태·스레드·기타 |

### NTChatRoom (방) — `NTChatRoom.*`
| 컬럼 | 타입 | 쓰임(관찰) |
|---|---|---|
| `chatId` | INTEGER | PK |
| `type` | INTEGER | 방 종류 코드(값 0·1·2·3·4·5 관찰, 의미 미해독 — §5) |
| `vtype` | INTEGER | (전부 0, 집계) |
| `directChatMemberUserId` | INTEGER | **>0 이면 1:1** 방(상대 `NTUser.userId`). §5 |
| `linkId` | INTEGER | **>0 이면 오픈채팅**(= `NTOpenLink`). §5 |
| `chatName` | TEXT | **거의 항상 비어 있음**(hasName 1 / noName 440, 집계) → 이름은 파생 필요 |
| `activeMembersCount` | INTEGER | 참여자 수(<=2: 369 · 3–10: 51 · 10+: 21) |
| `displayMemberIds` | BLOB | 표시용 멤버 id 목록(이름 조합용) |
| `imageUrl`·`fullImageUrl` | TEXT | 방 대표 이미지 |
| `inviterUserId`·`token`·`lastLogId`·`lastSeenLogId`·`extra` | — | 기타 |

### NTUser (사람) · NTChatContext (나)
- `NTUser`: `userId`(PK) · `displayName` · `nickName` · `friendNickName` · `profileImageUrl` · `phoneNumber` · `uuid` …
  → **1:1 방 이름 = `directChatMemberUserId` 로 이 테이블의 `displayName`/`nickName` 조회**(§5).
- `NTChatContext.userId` = **로그인한 내 userId**(이번 복구값과 일치).

---

## §2. 첨부 type 값별 JSON 구조 (표)

`NTChatMessage.type` 분포(집계, 상위): `1`(텍스트) 768,596 · `2` 11,602 · `3` 1,265 · `12` 8,085 · `26` 8,579 ·
`20` 7,681 · `71` 5,046 · `18` 2,283 · … (0=시스템 10,724)

| type | 뜻(관찰) | `attachment` JSON 주요 키 | 다운로드 URL | 썸네일 URL | 크기·이름·체크섬 |
|---|---|---|---|---|---|
| **2** | **사진** | `url`,`thumbnailUrl`,`thumbnailW/H`,`k`,`cs`,`s`,`w`,`h`,`expire`,`mt`,`cmt` | ✅ `url` | ✅ **별도** `thumbnailUrl` | `s`(크기)·`cs`(체크섬)·`mt`/`cmt`(MIME) |
| **3** | **동영상** | `url`,`tk`,`expire`,`cs`,`s`,`d`,`w`,`h`,`f` | ✅ `url` | ✗(원본만) | `s`·`d`(길이)·`cs` |
| **4** | 오디오/음성류 | `url`,`k`,`name`,`expire`,`rsc`,`hfac`,`rt` | ✅ `url` | ✗ | `name` |
| **5** | 오디오류 | `url`,`k`,`d`,`expire` | ✅ `url` | ✗ | `d` |
| **6** | 이모티콘/스티커 | `url`(짧음·CDN 아님),`name`,`sound`,`alt`,`thumbnailW/H` | 리소스 경로 | — | 미디어 아님 |
| **12** | 이모티콘 | `path`,`kid[]`,`name`,`alt` | 이모티콘 스토어(`path`/`kid`) | — | 미디어 아님 |
| **18** | **파일** | `url`,`k`,`name`,`size`,`cs`,`expire`,`s` | ✅ `url` | ✗ | **`name`(파일명)·`size`·`cs`** |
| **20** | 애니 스티커 | `type`,`path`,`name`,`sound`,`kid[]`,`width`,`height`… | 이모티콘 스토어 | — | 미디어 아님 |
| **26** | **답장(인용)** | `src_logId`,`src_userId`,`src_type`,`src_message` | — | — | 원본 메시지 참조(미디어 아님) |
| **27** | **여러 장 사진(앨범)** | `imageUrls[]`,`thumbnailUrls[]`,`kl[]`,`hl[]`,`wl[]`,`sl[]`,`csl[]`,`mtl[]`,`expire` | ✅ `imageUrls[]` | ✅ `thumbnailUrls[]` | 배열(장수만큼) |
| 16385~ | 피드/공지류 | `urls`(외부 host),`byHost`,`lastFeedId` | 외부 | — | 사용자 미디어 아님 |

> 요지: **사용자 미디어(사진 2 / 앨범 27 / 동영상 3 / 파일 18 / 음성 4·5)는 전부 `attachment` JSON 안에 CDN `url`
> 을 갖는다.** 이모티콘·스티커(6·12·20)는 CDN URL 이 아니라 이모티콘 스토어 경로(`path`/`kid`)라 **별도 취급**.
> 답장(26)은 원본 메시지 참조일 뿐 미디어가 아니다.

---

## §3. 다운로드 URL · 썸네일 · 만료 · 인증 (AT-2 상당 부분 닫힘)

| 항목 | 관찰 |
|---|---|
| URL 호스트 | **`talk.kakaocdn.net`** (사용자 미디어 공통) |
| URL 쿼리 파라미터 | **`credential`, `expires`, `signature`** (+썸네일은 `convert`,`w`,`h`) — **서명된 URL** |
| 인증 방식 | **쿼리 서명**(credential+signature). 즉 **별도 Authorization 헤더·쿠키 없이** URL 그대로 GET 하는 모양 (※ 실제로 받아보지는 않음) |
| **만료 — URL `expires` 파라미터**(epoch 초, 권위값) | **사진·동영상(type 2·3) ≈ 3일 · 파일(type 18) ≈ 14일** (사본 30건 중앙값, `sentAt` 대비) |
| 만료 — `attachment.expire` 필드 | 13자리 = **epoch 밀리초**, `sentAt` 대비 ≈ **14일**(모든 type). ※ URL `expires` 와 다를 수 있어 **실제 끊기는 시점은 URL `expires`(사진 3일)가 더 짧은 쪽** |
| 썸네일 | 사진(2)·앨범(27)은 **원본과 별개의 `thumbnailUrl`** 보유 → 목록 미리보기에 쓸 수 있으나 **같은 서명·만료 체계**(신선할 때만) |

> **AT-2 답**: URL 은 헤더 인증 없이 받는 서명 URL 로 보이고, **사진/동영상은 발행 후 ~3일**, 파일은 ~14일이면
> 만료된다(이 사본 기준 중앙값). "클릭할 때 받기"를 늦게 하면 특히 **사진은 3일 안**에 안 받으면 끊긴다.

---

## §4. 파일 이름·크기·MIME (JSON 안에 있나)

| 정보 | 어디 | type |
|---|---|---|
| 파일명 | `attachment.name` | 파일 18 · 음성 4 |
| 크기(바이트) | `attachment.size`(파일 18) / `attachment.s`(사진·동영상·앨범) | 2·3·18·27 |
| 체크섬 | `attachment.cs`(사진·파일·동영상) / 앨범 `csl[]` | 2·3·18·27 |
| MIME | `attachment.mt`·`cmt`(사진) | 2 (그 외 type 은 명시 MIME 키 없음 — 확장자/`name` 으로 유추) |
| 치수 | `w`/`h`(사진·동영상), `thumbnailWidth/Height`(썸네일), 앨범 `wl[]`/`hl[]` | 2·3·27 |

---

## §5. 방 1:1 / 단체 / 오픈채팅 구분 · 이름 (표)

| 구분 | 판별 필드(관찰) | 집계 | 이름 표시 |
|---|---|---|---|
| **1:1** | `NTChatRoom.directChatMemberUserId > 0` | 348 | **`chatName` 거의 없음** → `directChatMemberUserId` 로 `NTUser.displayName`(없으면 `nickName`) 조회 |
| **오픈채팅** | `NTChatRoom.linkId > 0` (= `NTOpenLink`, 13건) | 13 | `chatName` 또는 오픈링크 메타 |
| **단체(일반)** | 위 둘 다 아님 | 나머지(~93 중 오픈 제외) | `chatName` 비면 `displayMemberIds` 로 참여자 이름 조합(없으면 `(unknown)`) |
| 참여자 수 | `NTChatRoom.activeMembersCount` | <=2:369 / 3–10:51 / 10+:21 | — |

> **방 이름 없는 1:1 표시**: `chatName` 이 사실상 전부 비어 있어(hasName 1 / noName 440), **상대 userId(`directChatMemberUserId`)
> → `NTUser.displayName`** 로 그려야 한다. kakaocli README 의 "group 이름 `(unknown)`" 한계가 여기서 비롯(§2 앞 조사).
> `NTChatRoom.type`·`vtype` 코드값도 있으나 **의미 미해독**(직접 쓰지 말 것 — 미결).

---

## §6. 메시지 고유키 · 시각 · 보낸 사람 (서버 dedup 후보)

| 항목 | 관찰 | 서버 반영 |
|---|---|---|
| **중복 방지 키** | `logId` 단독 = **유일 아님**(중복 행 존재: 작은 값·일부 큰 값) · **`(chatId, logId)` = 전수 distinct**(830,838/830,838) | **PK = (chatId, logId)** 권장 후보 |
| 보낸 시각 | `sentAt` = epoch **초**(10자리) | 그대로 저장 |
| 보낸 사람 | `authorId` = `NTUser.userId`(>0 829,947 · =0 시스템 891) | FK |
| 메시지 종류 | `type`(§2) | 렌더 분기 |
| `msgId` | 자리수 들쭉날쭉·작은 값 많음 | 전역키로 **부적합** |

---

## §7. `localFilePath` — 자동 캐시가 아니다

- 비어 있지 않은 행: **type 2(사진) 30건 · type 18(파일) 43건** 뿐(전체 대비 극소).
- 값 모양(마스킹): 경로 디렉터리 = **`~/Downloads`**, 확장자 `.jpeg`/`.pdf` — 즉 **사용자가 카톡에서 직접 "저장"한
  파일**의 경로다. 컨테이너 내부 캐시(`~/Library/Containers/...`)도 `/tmp`도 아님.
- → 앞 조사 §2 의 "로컬에 logId 로 집을 수 있는 자동 저장소 없음"을 **재확인**. `localFilePath` 는 사용자가 수동
  저장한 소수만 가리키므로 **첨부 노출의 일반 경로로 못 쓴다**.

---

## §8. 열린 질문 (결정하지 않음)

- **DB-1 (userId 복구 운영화)**: 이 기기처럼 **진짜 userId 가 `AlertKakaoIDsList` 밖**이면 kakaocli 는 실패한다.
  운영 앱은 계정 해시(`DESIGNATEDFRIENDSREVISION` SHA-512 역상) brute-force 또는 수동 입력으로 userId 를 보강해야.
  계정이 둘(이 기기 DB 2개) → **어느 계정을 쓸지** 고르는 UX 필요.
- **DB-2 (만료 재확인 · 앞 조사 AT-3)**: 사진 URL ~3일이면 "안 저장·클릭 때 받기"가 **사실상 수집 즉시 받아 둬야**
  성립. "서버에 첨부 저장 안 함" 원칙을 카톡만 예외로 할지(= best-effort 보관). `expire` 필드(ms, 14일)와 URL
  `expires`(3일)가 **불일치** — 둘 중 짧은 URL `expires` 가 실제 한계인지 실측 필요(네트워크 금지로 이번 미검증).
- **DB-3 (썸네일 목록 · 앞 조사 AT-4)**: 목록 미리보기는 `thumbnailUrl`(사진·앨범)로 가능하나 **같은 3일 만료** →
  목록 썸네일도 수집 시 받아 둬야 안정적.
- **DB-4 (이모티콘·스티커 6/12/20)**: CDN URL 이 없고 이모티콘 스토어 경로(`path`/`kid`)라 **원본 복원 경로가 다름**.
  1차 범위에서 "스티커"는 어떻게 표시할지(텍스트 대체? 안 그림?).
- **DB-5 (앨범 type 27)**: 한 메시지에 사진 N장(`imageUrls[]`). 메시지함 렌더·수집에서 N장 처리 방식.
- **DB-6 (방 type/vtype 코드 의미)**: `NTChatRoom.type` 값(0~5)의 정확한 의미 미해독 — 1:1/오픈은 `directChatMemberUserId`/
  `linkId` 로 충분하나, 코드 의미가 필요하면 추가 조사.
- **DB-7 (음성 type 4·5 구분)**, **DB-8 (supplement/extra 컬럼 용도)** — 1차 범위 밖이면 보류.

---

## 부록 — 조사 경계(무엇을 했고 안 했나)
- 했음: 사본 1개를 `sqlcipher` 로 **읽기 전용** 열람 → 스키마·type 분포·attachment JSON **키 구조**·방/사람 필드·
  집계(개수·TTL) 확인.
- 안 함: 원본 수정·WAL 체크포인트(사본만 조작) · 대화 본문/실명/전화번호/실제 URL/실제 파일명 출력 ·
  **CDN 네트워크 접속**(만료는 URL `expires` 파라미터 − `sentAt` 산술로만) · 카톡 앱 조작·발송.
- 뒤처리: **사본(main.db·-wal·-shm)·복구 키 파일 삭제.** kakaocli 빌드 산출물은 scratchpad 에만.
