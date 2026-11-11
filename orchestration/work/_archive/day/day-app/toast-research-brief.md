# [mobile] 기존 프로토타입 상태 변경 토스트 정적 조사

## 1. 읽을 것·역할
너는 기존 DAY mobile 워커다. 앞 맥락에 의존하지 않는다. /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/mobile/의 역할 문서와 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app/AGENTS.md를 먼저 읽는다. 이번은 코드 구현 없이 읽기 전용 조사다. 하위 워커·내부 서브에이전트 금지.

## 2. 대상
프로토타입 /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app (read-only), 현재 앱 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app/app (read-only).

## 3. 사용자 요청
기존 앱처럼 상태 변경 시 토스트를 쓰는지, 기존 토스트가 무엇인지 조사. 참고 스크린샷은 상단의 검정 둥근 토스트 「A-룸1 · 써마지 FLX 300shot 종료」 + 「되돌리기」. 화면 문구를 만들지 않는다.

## 4. 조사 내용
프로토타입에서 toast/SnackBar/ScaffoldMessenger/Overlay 및 공통 알림 함수를 추적한다. 시술 시작·종료·각 취소·수락·호출·마취·귀가대기 등 실제 호출 지점별 문구 템플릿, 성공/실패 및 표시 조건, 위치·색·모양·시간·중복 처리, 되돌리기 제공 여부와 실제 호출 action/권한을 표로 정리. 통역/로그인 등 다른 토스트도 실제 존재하면 별도 표에 포함. 파일:줄 근거 필수. 사용자의 캡처와 일치하는 구현 위치를 특정. 현재 DAY 앱과 차이를 비교하되 정책을 결정하거나 코딩하지 않는다. 정적 확인과 실행 확인을 구분.

## 5. 경계
코드·스펙·백엔드·설정 수정, 실행/빌드/서버 접근/로그인/업무 조작, 커밋·push·PR 금지. 기존 사용자 데이터나 비밀값을 출력하지 않는다. 생성 허용 파일은 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/research-prototype-toasts.md 한 개.

## 6. 산출물·수락
위 표와 파일:줄 근거, 현재 앱 차이, 확인 못한 항목을 한국어 보고서에 남긴다. 원래 문구만 인용하며 코드 위치를 정확히 확인한다. 완료 요약은 주요 상태 변경 토스트와 되돌리기 목록을 간결히 보고.

## 7. 진행
새 live preamble의 Task/Dispatch/핸들이 옛 예시보다 우선한다. 마지막 메일 확인 후 worker_done --outcome succeeded 또는 failed를 정확히 한 번 보내고 idle한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_e8a8842c-a789-4862-93a5-7886d6bd1c61 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
