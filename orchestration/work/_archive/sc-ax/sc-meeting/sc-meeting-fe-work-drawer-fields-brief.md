# [frontend] 업무 생성 드로어 — 달력을 우리 DatePicker 로(전 화면 기본값) · 담당자 Select 팝오버 위치·후보(DS-17·DS-18)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. `frontend/` 만. 커밋 금지. dev 서버·5176 금지. **vitest 스위트 돌리지 마라(사용자 지시, e2e 로 본다) — `npx tsc --noEmit` 만.** **칩 작업(task_4f87ab1bb0c2) 완료 보고 뒤에 이어서.**

## 실물(09-11, 회의록 「다음 할 일」→[업무 생성] 드로어) — 사용자
1. **달력이 크롬 기본 달력**이다. `DateField` 기본값이 `calendar="platform"`(OS showPicker)이고 우리 `DatePicker` 는 `inline` 을 준 화면(회의 목록)만 쓴다. **고침(DS-17)**: `DateField` 기본값을 우리 DatePicker 팝오버로 바꾸고, `platform` 갈래와 숨은 `input[type=date]`·`showPicker` 경로를 지운다. 프롭은 남기지 말고 하나로. 전 화면(업무 생성·업무 요청·수정 요청·업무 상세 시작일/기한·회의 예약)이 같은 달력을 쓰게 된다. 아이콘은 칸 안쪽(회의 목록과 같은 모양).
2. **담당자 Select 팝오버가 칸에서 떨어져** 아래·오른쪽으로 뜬다(표 행/스크롤 컨테이너 안). **고침(DS-18)**: `Popover` 앵커 계산을 컨테이너 스크롤·표 안에서도 맞게(anchor 의 getBoundingClientRect 기준, 열릴 때와 스크롤/리사이즈 때 재계산, 화면 밖이면 위로 뒤집기). 다른 Select 도 같은 부품이니 같이 맞는다.
3. 그 Select 에 **유나만** 보인다 — 후보가 어디서 오는지 확인해서 리포트에 적어라(회의 참석자만인지, 조직 전체인지). 계약을 바꾸지는 말고 지금 규칙을 적어라. 규칙이 「참석자만」이면 그대로.

## 검증
`cd frontend && npx tsc --noEmit` 0. 테스트 파일은 새 모양에 맞게 고치되 실행하지 마라. Storybook 스토리(DateField·Popover) 갱신.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 업무 생성 드로어 달력·Select(DS-17·18)" \
  --body "변경 파일 / 달력 일괄 범위 / 팝오버 고침 / 담당자 후보 규칙 / tsc / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — DS-17·18. 상세는 인박스." --enter
```
