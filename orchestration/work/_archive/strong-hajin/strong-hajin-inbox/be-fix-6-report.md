# BE 수정 판 6 결과 보고 — 슬랙 방 목록 · 메시지함 로딩

## 상태: done (커밋 안 함 · 코디 스택은 GET 만 · frontend/ 무접촉)

## 측정 (ms · 같은 DB `ax_demo_inbox` · jiho · 「전」= 코디 API(옛 코드) 또는 바꾸기 전 같은 함수 · 「후」= 내 프로세스 지금 코드)
| 엔드포인트 | 전 | 후 | 비고 |
|---|---|---|---|
| `GET /api/integrations/slack/available-rooms` 첫 쪽 | 11,457 (코디 API) · 20,200 (같은 토큰·콜드) | **831** (API) · 740~850 (콜드 3회) | 100방(채널 52·비공개 4·그룹 DM 35·DM 9) · 그룹 DM `mpdm-` 남은 것 0 |
| 같은 목록 다시 열기 | 10,889 | **25** | 목록 캐시 90초 |
| 둘째 쪽 | — | 1,860 → 같은 방식 | 이름표 캐시가 데워진 뒤 |
| `GET /api/inbox/messages?source=all` | 23 | 22 | 쿼리 25 — 원래 빠름 |
| `GET /api/inbox/messages?source=mail` | 19 | 21 | 쿼리 23 |
| `GET /api/inbox/messages?source=slack` | 11 | 12 | 쿼리 22 |
| `GET /api/inbox/rooms/{id}/messages`(3,577건 방) | 8 | 10 | 쿼리 16 — 방 크기와 무관(N+1 없음) · 응답 40KB/50건 |
| 방 첨부(파일) 받기 | 286~324 | 첫 301 → **다시 18~35** | 짧은 메모리 캐시 + 브라우저 캐시 |
| 방 첨부(이미지) 받기 | 792 | 첫 781 → **다시 30** · 썸네일 97KB(원본 276KB) | `?variant=thumb` |

→ 결론: 서버의 메시지함 목록·방 열기 응답은 원래 수십 ms 로 병목이 아니었다. 사용자가 느낀 「방 로딩」은 ① 방 고르기 목록(10~20초) ② 방 안 첨부 이미지를 열 때마다 슬랙에서 원본 크기로 새로 받는 것(하나 0.3~0.8초 · 이미지가 여러 개면 누적)이다. 둘 다 고쳤다.

## 고친 것
1. **이름표 한 번에**(`platform/external_slack.py` `SlackUserCache`): `users.list` 몇 쪽으로 워크스페이스 사용자 id→이름·handle·봇·아바타 맵, 10분 캐시(토큰 지문별 · 프로세스 하나에 하나 `SLACK_USERS`). 캐시에 없는 id 만 `users.info` 하나씩 메우고, 「없는 사람」도 기억. **연동 워커의 방 이름·보낸 사람 이름표(`user_name`·`user_tag`)도 같은 캐시**
2. **그룹 DM**: `mpdm-a--b--c-1` 에서 handle 을 뽑아 맵으로 실명 — `conversations.members` 는 형식이 다르거나 모르는 사람이 있을 때만(이 계정 35개 중 1개)
3. **목록 응답 캐시**: 회원 토큰·커서별 90초
4. **나란히**: 방 목록(`users.conversations`)과 이름표(`users.list`)를 동시에 · 대체 호출도 최대 6개 동시
5. **429**: Retry-After 가 3초 이하면 기다렸다 한 번 더 · 길면 묵은 이름표를 쓰고, 묵은 것도 없으면 502(화면이 다시 시도)
6. **메시지함 첨부**: 중계 응답 `Cache-Control: private, max-age=600`(내용이 aid 로 고정) · 프로세스 메모리 캐시 10분(연동·aid 키 · 파일당 5MB·전체 64MB 상한 · **디스크·DB 저장 없음 — D-29 그대로**) · 연결 끊김·소유 검사는 캐시보다 앞이라 끊긴 연동·남의 회원에게 캐시가 새지 않음 · 슬랙 이미지 `?variant=thumb`(thumb_720/480/360/160 중 있는 것)

## 응답·경로 변화 (FE 영향)
- `GET /api/inbox/rooms/{room_id}/attachments/{aid}?variant=thumb` 추가(선택) — 대화 안 이미지 미리보기에 쓰면 더 작고 빠르다. 큰 보기·받기는 그대로(variant 없이)
- 첨부 응답 `Cache-Control` 이 `private, no-store` → `private, max-age=600`
- available-rooms 모양 변화 없음

## 검증
- make test-unit 477 · make test-contract 1243 + serial 128 통과 · architecture 45(inventory 는 첨부 라우트 서명 한 줄만)
- 새 시험: `tests/unit/test_slack_directory.py`(users.list 한 번·mpdm 실명·대체 호출 1·다시 열기 0호출 · 워커가 같은 캐시 · 429 짧으면 대기/길면 묵은 이름표/없으면 502 · handle 파싱) · contract(첨부 캐시·썸네일·남의 회원 404·잘못된 variant 422 · RelayCache 상한)
- BE-3 기존 시험 2개에 캐시 비우기 한 줄(상류 실패 경로를 그대로 재려고)

## 주의
- 메모리 캐시라 프로세스가 여럿이면 각자 데운다(운영 back 1~2개라 문제 없음)
- 첨부 메모리 캐시는 「저장 안 함」(D-29)을 디스크·DB 기준으로 지킨다 — 10분 메모리 보관이 정책상 불편하면 `RelayCache` 를 끄고 브라우저 캐시만 남기면 된다(한 줄)
