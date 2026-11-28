# [mobile] 코드 검수 고침 1 — F-2 그리기 · W-1

같은 터미널이면 앞 맥락 그대로 · 같은 워크트리 · `app/` 만. **커밋 · push 하지 마라.**

검수: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-code-1-report.md`

## 정한 것(코디 기본값 · `_RESUME.md` §2 맨 위 행 · 다시 열지 마라)
- **F-2 / R45 고침 — 행 넘는 첫 줄 카드 = 두 조각**: 시작 행에서는 카드 시작 분 위치부터 **그 행 첫 줄(`line` 0) 띠 끝**까지 그리고 자른다. 다음 행에서는 **그 행 첫 줄 띠 안에서 행 시작부터 끝 분까지** 이어 그린다. 시작 행의 아래 줄 띠는 덮지 않는다(아래 줄 자리 셈에서 찬 자리로 두지 않음). 다음 행 첫 줄 자리 셈에는 그대로 넣는다. → 어떤 경우에도 카드 겹침 0. `lines` = 1 인 행은 두 조각이 붙어 지금처럼 한 장으로 보인다. 띠(`bands`)도 같은 규칙.
- **W-1 — y 매핑 하나**: 분 → y 는 카드와 같은 식(각 줄 띠 안 분 비례 · 줄 띠 높이 = 기본 높이). 회색 면은 그 행 **모든 줄 띠**에 같은 분 구간으로 칠한다. 현재 시각 선은 그 행 모든 줄 띠를 가로지르는 선들(각 띠 안 같은 분 위치). [+] 칸 · 빈 칸 누르기의 y → 시각도 같은 식(누른 줄 띠 안 분).

## 할 것
1. **F-2 그리기**: `reservation_table.dart` `span`(카드 · 띠)을 두 조각 규칙으로 — 누르기는 한 카드처럼.
2. **W-1**: `y()` · 회색 면 · 현재 시각 선 · 처음 스크롤 y 를 위 매핑으로(웹과 같은 식).
3. 테스트: F-2 경우(12:30 ~ 13:30 × 6 + 12:40 ~ 12:50, 겹침 0) · W-1(lines 2 행).

## 검증
`flutter analyze` · `flutter test` 각 1회(빌드는 생략 가능 · 하면 1회).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
