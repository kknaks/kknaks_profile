# 카톡 Mac — 첨부(사진·파일) 조회 구조 조사 (read-only)

> architect(kakao) · 2026-10-06 · 앞 판 `kakao-survey.md` 의 K-9(첨부) 후속.
> 질문: 이번 카톡 범위 = **조회만 · 사용자가 고른 방만 · 첨부도 조회 가능한 구조**.
> Rust 앱이 로컬 DB 를 읽어 서버로 올리고 메시지함이 그린다. 첨부 파일 실체는 서버에 저장 안 함이 원칙
> (메일·슬랙 = 클릭하면 그때 받아 중계). → Mac 카톡 첨부를 어떻게 「볼 수 있게」 하나?
>
> ⚠ 경계: DB 복호·열기 안 함 · 캐시 파일 안 엶(`ls` 로 디렉터리/이름만) · 카톡 조작 안 함 · CDN 네트워크 접속 안 함.
> 근거 표기: `spec-001:NN` 등 = 우리 mykakao 문서 · `kakaocli/...:NN` = 외부 clone(읽기 전용) · `ls` = 이 Mac 실측 구조.

---

## §1. 결론

**첨부 "구분"은 된다. 첨부 "실물을 보이게" 하는 건 메일·슬랙만큼 깔끔하지 않다 — Mac 엔 logId 로 집을 수 있는
로컬 첨부 저장소가 없고, 실체는 시간제한 CDN URL 에 묶여 있다.**

1. **구분(식별)**: Mac 카톡 메시지 행(`NTChatMessage`)에 `type`(1=텍스트, 2=사진, 3=동영상…)과 **`attachment`/
   `extra` = 첨부·부가 데이터 JSON** 컬럼이 있다(우리 문서 `spec-001:177-203`). 즉 어떤 메시지가 사진/파일이고
   첨부 메타가 어디 있는지는 **같은 DB 한 테이블에서** 판별된다. (단 그 JSON **내용**은 우리가 아직 안 열어 봤다 —
   `spec-001:203` "비텍스트 type/attachment 분포 조사는 다음 단계, 이번 범위 밖".)

2. **실체 위치 — Windows 와 다르다**: Windows 판은 **별도 DB `talkmedia.edb`**(logId→token→url·fileSize·checkSum)로
   첨부를 깔끔히 매핑했다(`decision-006`, `baseline-007`). **이 Mac 컨테이너엔 그런 분리 미디어 DB 가 안 보인다**
   (`ls` 결과 §2) — 첨부 메타는 위 `attachment` JSON 안에 있고, 바이트 실체는 ① 카카오 CDN URL(JSON 안, 시간제한
   추정) ② macOS 시스템 URL 캐시(`Caches/fsCachedData`, 불투명·자동 삭제) 둘로 흩어져 있다.

3. **"클릭하면 보이는 길"**: 제일 현실적인 건 **(가) 서버가 attachment JSON 의 CDN URL 로 직접 받아 중계**다.
   단 **카톡 CDN URL 은 시간제한**이다 — Windows 에서 실증됨(최근=HTTP 200 생존 / 오래됨=410 Gone, `baseline-007`).
   → **메일·슬랙의 "안 저장하고 클릭할 때 받기" 원칙이 카톡엔 그대로 안 통한다.** 메일(Gmail 첨부 ID)·슬랙
   (`url_private`+사용자 토큰)은 **언제든 재조회되는 영속 API** 가 있지만, 카톡은 공식 재조회 API 가 없고 URL 이
   만료되면 끝이다. 그래서 카톡 첨부는 **best-effort** — 수집이 돌 때 신선하면 보이고, 오래 지난 건 "유실"로
   정직하게 표시하거나(mykakao Windows 가 택한 길, `decision-006` 결정4), 아니면 **수집 시점에 받아 우리가
   보관**해야 확실하다(= "서버에 첨부 저장 안 함" 원칙과 충돌 — 사용자 판단 필요, §4).

**한 줄**: 첨부 식별 ✅ · 썸네일/원본 노출은 "신선한 동안 CDN URL 로" ✅(제한적) · 메일·슬랙식 "영구 재조회" ❌
(카톡엔 영속 토큰 API 없음) · 깔끔한 로컬 파일 중계 ❌(Mac 로컬 캐시는 logId 로 주소 못 매김).

---

## §2. 근거

### (A) 첨부 식별 — 메시지 행 안에서
- `NTChatMessage`: `type`(메시지 종류, 1=텍스트), `message`(평문 본문), **`attachment`/`extra`(첨부·부가 JSON,
  비텍스트 type 해석에 사용)** — 우리 Mac spec 이 직접 적어 둠(`spec-001:177-203`, 특히 `:184-187`).
- 메시지 타입 열거: 텍스트1·**사진2·동영상3·음성4·스티커(이모티콘)5·파일6**·위치7 (`kakaocli/Sources/KakaoCore/Database/Models/Message.swift:14-21`).
- ⚠ **kakaocli 는 첨부를 안 읽는다.** 쿼리가 `m.message, m.type, m.sentAt` 만 뽑고 `attachment` 컬럼을
  건드리지 않음(`kakaocli/Sources/KakaoCore/Database/DatabaseReader.swift:133-137,159-166`). README 도 "미디어는 DB 에
  보이지만 렌더 안 함"이라 명시(`kakaocli/README.md:272,281`). → 첨부 JSON 의 **실제 필드 구조는 kakaocli 로는
  확인 불가**, 우리가 DB 를 1건 열어 봐야 확정(이번 금지).

### (B) 첨부 실체 위치 — 이 Mac `ls` 실측 (파일 안 엶, 디렉터리/이름만)
App Support 루트에 **분리 미디어 DB 없음** — 78-hex 암호 DB 2개(+`-wal`/`-shm`) · hex 디렉터리 · `Emoticon` ·
`com.crashlytics` 뿐. `talkmedia`·`media`·`attach` 류 파일명 **0건**:
```
Application Support/com.kakao.KakaoTalkMac/
  1196e147…a9d00 (+ -shm/-wal)      ← 78-hex 암호 DB (메시지·attachment 여기)
  b0bae659…e4049 (+ -shm/-wal)      ← 두 번째 78-hex DB
  97ea…/ 0e82…/  (hex 리소스 디렉터리)  Emoticon/  com.crashlytics/
```
미디어로 보이는 캐시 디렉터리(Data/Library 하위):
| 경로 | 무엇으로 보이나 | logId 로 주소 가능? |
|---|---|---|
| `Caches/fsCachedData` | **macOS 표준 URLCache 디스크 저장소** — UUID 이름 230개(`00422310-…`). HTTP 로 받은 것(이미지 포함)이 시스템 캐시로 떨어진 것 | ❌ 불투명·UUID·OS eviction. 메시지 logId→파일 매핑 없음 |
| `Caches/Items/<hash>/mr22·mr23·mr24` | 카톡 미디어 리소스 캐시(`.mr22` 66 · `.mr23` 49개) — 이모티콘/미디어 리소스 추정 | ❌ 이름이 chatId/logId 아님 |
| `Library/Images/People` | 프로필 이미지 | — (채팅 첨부 아님) |
| `Caches/ProfileResource` | 프로필 리소스 | — |
| `Caches/WebKit`·`HTTPStorages`·`Cookies` | 내장 웹뷰 저장소 | — |
> 요지: Mac 로컬엔 **채팅 첨부를 logId 로 꺼낼 수 있는 깔끔한 저장소가 안 보인다.** fsCachedData 는 있지만
> 시스템 URLCache 라 불투명하고 언제든 비워진다. (Windows 의 `.cng` 암호 캐시 같은 것도 이 Mac 에선 이름상
> 안 보임 — Mac 미디어 캐시 체계는 Windows 와 다름. 확정하려면 디렉터리 더 파야 하나 파일 열기 금지라 보류.)

### (C) mykakao Windows 방식 — Mac 에 통하는 것 / 안 통하는 것
| Windows 판(`baseline-007`·`008`·`decision-006`·`spec-006`) | Mac 적용 |
|---|---|
| 사진 메시지 식별 = type 코드 | ✅ 통함 — Mac 도 `type`+`attachment`(`spec-001`) |
| `talkmedia.edb` (chatMsgTokenJunction logId→token / tokenInfo token→url,fileSize,checkSum) | ❌/❓ **Mac 엔 그 분리 DB 안 보임**(§2 B). Mac 은 `attachment` JSON 안에 URL 이 들어 있을 것으로 **추정**(미확인) |
| **URL 다운로드(talk.kakaocdn.net, 최근 200 / 오래됨 410)** | ✅ **원리 통함** — CDN URL 시간제한은 플랫폼 공통. Mac 도 신선할 때 받으면 될 것(URL 이 JSON 에 있다는 전제) |
| 받은 바이트 **로컬 미디어 저장**(만료돼도 보유) | ⚠ 통하나 "서버에 첨부 저장 안 함" 원칙과 충돌 |
| 커버 경계 = **best-effort, 못 받은 건 "유실" 표시** | ✅ 사고방식 그대로 Mac 에 유효 |
| `.cng` 오프라인 복호(오래된 사진) | ❌ 범위 밖 — Windows 도 셸빙(`baseline-008`: 키 힙에 없음·Ghidra 필요). Mac 대응물 미확인 |
| 실체 저장을 **메모리 harvest 키로 talkmedia 복호** | ❌ Mac 무관 — Mac 은 오프라인 키 유도라 harvest 자체가 없음(앞 판 `kakao-survey.md` §2) |

---

## §3. "클릭하면 보이는 길" — 길별 비교 (결정 아님)

| 길 | 어떻게 | 전제 조건 | 실패 모습 | 원칙("저장 안 함") 부합 |
|---|---|---|---|---|
| **(가) 서버가 CDN URL 로 직접 받아 중계** | Rust 앱이 `attachment` JSON 에서 URL 추출→서버로 올림. 사용자가 클릭하면 **서버가 그 URL 을 그때 fetch** 해 바이트 중계 | URL 이 JSON 에 있어야 함(미확인) · **URL 이 아직 안 만료** · (public 토큰 URL 이면) 추가 인증 불필요 | URL 만료 시 **410 Gone** → 못 봄. 카톡·앱 꺼짐과 **무관**(서버가 직접 감) | ✅ 가장 부합 — 단 **신선한 동안만** 성립. 메일·슬랙과 달리 영구 보장 ❌ |
| **(나) 서버→Rust 앱→로컬 파일 중계** | 클릭 시 서버가 Rust 앱에 요청→앱이 로컬 캐시에서 파일 찾아 업로드 중계 | 로컬에 그 첨부가 있어야 함. **그러나 Mac 로컬 캐시(fsCachedData)는 logId 로 주소 못 매김**(§2 B)·OS 가 비움 · 앱·카톡이 켜져 접근 가능해야 | 캐시에 없음/삭제됨 → 못 찾음. 매핑 불가라 **신뢰도 낮음** | ✅ 부합하나 **실현성 의문**(Mac 매핑 수단 없음) |
| **(다) 수집 시점 즉시 다운로드+우리 보관** (mykakao Windows 길) | 수집 파이프가 사진 메시지 만나면 **그 자리에서** CDN URL 다운로드→우리 저장. 클릭은 우리 저장본 서빙 | 수집이 **신선한 동안** 돌아야(실시간/근접) | 수집 전 만료 → "유실" 표시, 복구 안 함(`decision-006` 결정4) | ❌ **원칙과 충돌** — 첨부 바이트를 우리가 보관 |

> (가)가 원칙에 가장 맞지만 **카톡 CDN 의 시간제한 탓에 "클릭할 때쯤 이미 만료"가 흔할 수 있다.** 확실히 보이려면
> 사실상 (다)로 기운다. 이 긴장(원칙 vs 실현)이 이번 범위의 핵심 결정거리다(§4).

---

## §4. 열린 질문 (결정하지 않음)

- **AT-1 (attachment JSON 실제 필드)**: `NTChatMessage.attachment` JSON 안에 무엇이 있나 — 원본 URL? 썸네일 URL?
  만료시각? 로컬 경로? fileSize·checkSum? **확정하려면 DB 1건을 열어 봐야 함**(이번 복호·열기 금지로 보류).
  이게 닫혀야 (가)/(나) 실현성이 확정된다. → 별도 read 승인 필요.
- **AT-2 (CDN URL 유효기간·인증)**: Mac 카톡 첨부 URL 이 얼마나 사나(Windows 는 분 단위 관찰, `baseline-007`),
  public tokenized 라 서버가 바로 받나 아니면 쿠키/헤더 인증이 필요하나. (네트워크 접속 금지로 이번 미측정.)
- **AT-3 (저장 원칙 예외)**: 메일·슬랙은 "안 저장·클릭 때 재조회"가 영속 API 로 가능하지만 **카톡은 불가**.
  카톡만 **best-effort + 수집 시 보관**(길 다)을 예외로 허용할지, 아니면 "신선한 것만 보임·나머지 유실 표시"로
  갈지(원칙 유지). 사용자 결정거리.
- **AT-4 (썸네일 목록 노출)**: 메시지함 목록에 사진 미리보기를 바로 보이려면 썸네일이 필요한데, 썸네일도 CDN·
  같은 만료 체계일 공산 → 목록 썸네일도 (다)처럼 수집 시 받아 둬야 안정적. 인라인 소형 썸네일이 JSON 에
  base64 로 들어오는 경우가 있는지 AT-1 에서 함께 확인.
- **AT-5 (미디어 종류 범위)**: 1차 범위를 사진만으로 볼지, 동영상(용량 큼)·파일·이모티콘/스티커까지 볼지.
  Windows 도 사진만 하고 동영상·파일은 후속으로 뺐다(`spec-006` Out).
- **AT-6 (오래된 첨부 = Mac `.cng` 대응물)**: URL 만료된 오래된 사진의 오프라인 복원 경로가 Mac 에 있나.
  Windows 는 `.cng` 복호가 막혀 셸빙(`baseline-008`). Mac 캐시 체계가 달라 재조사 필요(이번 ls 로는 `.cng` 미발견).
- **AT-7 (Rust 가 attachment JSON 파싱)**: 식별·URL 추출은 Rust 가 DB 읽을 때 `attachment` 컬럼을 같이 뽑으면 됨
  (kakaocli 는 안 하므로 우리가 추가). 컬럼명·JSON 스키마 확정은 AT-1 에 의존.

---

## 부록 — 조사 경계(무엇을 안 했나)
- DB **복호·열기 안 함.** `attachment` 컬럼 존재는 우리 문서(`spec-001:187`) 근거이고, **JSON 내용은 미확인.**
- 캐시/미디어 파일 **안 엶** — `ls` 로 디렉터리 구조·파일명·확장자 분포만 봄.
- CDN URL **네트워크 접속 안 함** — 유효기간·인증은 Windows 실증(`baseline-007`)과 구조 추론으로만 기술.
- kakaocli 는 scratchpad 얕은 clone **소스 읽기만.**
