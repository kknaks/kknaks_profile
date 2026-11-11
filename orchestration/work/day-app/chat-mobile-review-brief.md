# 최종 앱 독립검수 추가 지시(아래 옛 브리프보다 우선)
너는 backend 작성자였지만 app 작성에는 참여하지 않았다. 이번에는 read-only 앱 독립 리뷰 역할이다. chat-mobile-completion-fix-report.md와 evidence/pairs-same 및 day-v2부터 읽고 첫 보고도 대조한다. SPEC 현재 b0f71ec312548a8dd60c70e51ac68374b84fb906의 003/004 권한 명확화가 우선: /me200 board없음은 셸/채팅/설정 유지, board API/SSE/고객/통역0. /me 자체403은 기존 전역차단. 직원 비활성/멤버십 상실이어도 실제 /me는200일 수 있고 채팅 API/SSE403은 토스트+목록 비움이다. 서버 auth를 새로 고치는 것 아님. 채팅 독립 연결줄, 같은 viewport 원형 비교, SPM lock2개/README 포함해서 누락/회귀 확인. 앱 미커밋 변경 전체가 검수 대상. backend는 별도 리뷰어가 DB검수 중이므로 DB 테스트/서버 설정/기동은 금지, app 테스트는 독립 수행 가능. 사용자의 시뮬레이터는 조작하지 마라. 최종 보고 chat-mobile-review.md. 너의 backend 수정 재개 금지. 아래 완료 명령에 --outcome succeeded/failed 와 --report-path 실제 경로 추가하고 preamble IDs 우선.

# [reviewer] DAY 채팅 앱 독립검수

mobile완료뒤발주. read-only·하위위임·commit/push/GitHub/서버/실기기계정조작0, profile보고 chat-mobile-review.md 하나. 코드tree /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app AGENTS·역할day/reviewer, mobile-code-brief/report/evidence·최종WPv7·SPEC53adbd49 004/003/000/001 대조. backend변경도dirty이나이검수는app/만(이후별도통합), 원천cc-prototype77173cf8 gitshowread-only.
원형디자인/문구·폰/iPad4메뉴·목록·1:1/그룹/초대/읽음/나감·hide/mute/수정삭제/전달/검색/첨부선택·사진·동영상·모아보기/배지배너/푸시이동 전기능매핑. SDK/native코드실체·키문구PHPhotoLibrarykey·사진제한접근·카메라취소·압축/변환한도·재생RangeBearer/redirect유출0·임시/OS파일·disposed/취소·실패재시도clientId유지. 화면캡처와원형대조,가로/긴문자/키보드/필수버튼잘림·접근성·레이아웃오버플로우검사,테스트기대값만확인하지말고실화면대표증거.
세션이바뀐뒤늦은401/2xx/SSE/APNs/픽커/변환후업로드가새세션삭제·전송·배너·토스트·메모리혼합0. active.sessionorigin/token/environment/hospital로격리·다기기읽음/tombstone/since서버시간/from_seq재가입경계. header종과chat tab별도, muted/openroom/foreground/background조건·SSE+APNs동일message중복0. **native willPresent/notification tap도environment와hospital 검증가능한실제context가있는지**(기존SessionBundle병원필드부재가능, Dartme.hospitalId만지켜nativeOSbanner에누출하지않는지),기존원장수락native category/Keychain/통역오디오회귀0. serverunreadRooms정본·유실복구/모든HTTP계약맞춤.
검증은unit/widget/contract/native·analyze·unsignedbuild 실제보고대조·중요집중테스트재현,원천기능누락0. 사용자의orca-mobile-iphone 실세션/데이터/route를리뷰어가조작하지않고허용fixture이미지/기존캡처로시각검수(필요하면코디에게mobile재캡처요청). 실서버키/실기기성공주장정직. 위협가정만WARN늘리지말고실제증거/프로토/스펙기준FAIL/WARN/PASS, fileline·최소정정. app/변경파일hash/테스트수치·새오류·제한을기록. 이후backend와API샘플·에러·SSE조립은별도통합,계약차이는발견즉시코디질문. exactpreamblecheckack/outcome/report worker_done1회후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_bdc96429-0e21-4311-bca9-622e97ece387 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
