# [planner] 알림SPEC005 WARN 정정

notification-spec-brief.md/notification-spec-report.md/notification-spec-review.md/currentdiff읽기. 동일spec tree53adbd49위. 허용005+20-specindex+30-workcoverage만(003/004/000/001/002동결5개지킴), 보고profile notification-spec-fix-report.md. 코드/WP/GitHub/commit/push/merge/하위위임0.
W1정정: 관찰결과(호출id,받는계정)한번보장유지, 기존테이블로기본수단=호출단위잠금안조회후쓰기(같은tx)명확히. 'migration 필요없다'절대단정과OQ3모순제거. 유일색인선택은SPEC000/migration후속필요하므로지금기본아님, 단계와동결범위구분. 실제재호출은새callid생성(currentday/services/board.pyrecall)이라새알림이며이전행유지되는점명확히. 프로토에는이dedup없다는DAY적응표기.
W2정정: ids=[]는0건, 모두읽음은ids/callId둘다칸없음만. 두필드동시주어지면원천처리우선순위확인/명세로모호없게. 모두읽음은내병원+내계정의안읽은전체날짜(오늘목록만으로축소X) 원천그대로한구절. 읽음후SSE다기기종맞춤은DAY적응으로유지/차이표명시(신규문구/정책아님, 데이터동기화보완). 빈ids0건/읽음동시/다기기AC 정합.
SPEC005 status stable로정리·index동기, 검수대상새파일만닫음. 아직코드미구현/제안계약·키/실기기pending유지. 003연결패치목록은지금수정0; v8알림코드착수전에적용/독립검수필요를선행조건으로명시(동결해제후). 새로운OQ/사용자확인양산0. lintstrict최종1회DAY0/무관분리, gitdiffcheck·동결5blob확인, before/after/원천/AC매핑보고. 정확ID outcome/report worker_done1회/checkack후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_3333de45-6039-44ec-b7af-76bbd3afdb0c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
