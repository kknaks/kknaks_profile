# [mobile] 실기기 · 아이패드 피드백 T1~T5 수정

같은 cc-prototype `mobile` 워커 · 같은 코드 워크트리 · `procedure/app/` 만.

## SSOT
- 피드백: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/e2e-device-feedback-batch-1.md` **T1 ~ T5 전부**(원인 · 처분 줄 포함)
- 화면 정본(모양): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-mobile/Ceramique 시술실 태블릿.dc.html`(room · list scene) · `Ceramique 간호사 모바일.dc.html`
- 로직은 지금처럼 스냅샷 값만

## 할 일 요약
- **T1** 태블릿 룸 상세 두 열이 화면 아래(통역 바 위)까지 — 열 = Column · 왼쪽 오더 메모 카드 Expanded(안 스크롤) + 마취(· 주의) 아래 · 오른쪽 호출/완료 상자 + 시술 카드 Expanded(시술 목록 안 스크롤) + [의사 호출] 카드 바닥 고정
- **T2** 태블릿 머리 한 줄([← 현황] │ 방(크게) │ 고객 · 국적 · 첫/재내원 · 입실 │ … 상태 · 시각) · 모바일은 두 줄 그대로 · [간호사 요청] 없음
- **T3 · T4** 글자 크기 **반응형 비율** — 태블릿 글자 단계(시안 태블릿 값) 또는 화면 짧은 변 기준 배율을 Typo 전체에 · 오더 메모 본문 시안 크기 · 하드코딩 px 줄이기 · 모바일은 지금 크기(오더 메모만 한 단계)
- **T5** 목록 필터 = 맞는 카드만 · 격자 **왼쪽 위부터**(Wrap 폭 전체 · start) · **「귀가」 칩 추가**(전체 = 칩 합)

## 검증
- **아이패드 시뮬레이터(orca-mobile-ipad · 가로 + 세로)** 와 iPhone 시뮬레이터 각각 · **배포 서버 https://ccc.medisolveai.xyz** 로 — 목록(필터 1장 · 전체) · 룸 상세(내용 적은 카드 · 긴 카드) 스크린샷 경로를 보고에
- 사용자가 아이패드 시뮬레이터를 쓰고 있었다 — 시작 전에 '[시뮬레이터 씀] mobile' terminal send 하고 진행 · 끝나면 **아이패드 시뮬레이터에 고친 앱을 배포 서버로 띄워 둔 채** 보고(렉: 시뮬레이터 동시에 둘 금지 — 하나씩)
- analyze · 바뀐 시험 · 마지막 test 전체 1회 · **업로드(빌드 3)는 하지 마라**(사용자 확인 뒤) · 커밋 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
