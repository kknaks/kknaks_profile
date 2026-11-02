# @sc-ax-fe — 규칙

## 계약은 서버가 준다
- 권한·가능한 행동은 envelope(`allowed_commands`·`requires_reason`·`waiting_on`·`preview`)로만 판단한다.
  kind 나 status 로 command·필드·권한을 추론하는 코드를 쓰지 않는다
- 서버 호출은 `src/api.ts` 를 거친다. 컴포넌트에서 직접 `fetch` 하지 않는다
- 재전송은 영수증이다 — 같은 command 를 다시 보내는 UI 는 두 번째 effect 를 기대하지 않는다 (`idempotency.ts`)

## 재사용
- 새 컴포넌트 전에 `src/` 의 기존 것(Modal · DateField · Checklist · WorkViews · WorkModals · ActionPreview)과 `viewModels.ts`·`labels.ts` 를 먼저 찾는다. 중복 구현은 리뷰 FAIL 사유
- 라벨·한국어 카피는 `labels.ts` 에 모은다. 컴포넌트에 문자열을 흩뿌리지 않는다
- 스타일은 `styles.css` + 디자인 시스템 토큰. 컴포넌트에 임의 hex 리터럴을 두지 않는다

## 테스트
- 훅·viewModel·critical 컴포넌트는 옆자리 `*.test.tsx`(vitest + Testing Library, jsdom) 에 먼저 RED
- e2e(`scripts/*-e2e.mjs`)는 떠 있는 스택(8001/5176)이 필요하다 — 브리프가 지정할 때만, 데이터 reset 없이

## 스코프 규칙
- 작업 전 영향 파일 전수 나열 (페이지 → 컴포넌트 → viewModels → api.ts → 테스트)
- SPEC 에 없는 화면·행동이 필요하면 만들지 말고 코디네이터에게 묻는다
- BE 응답이 부족하면 프론트에서 우회 조립하지 않는다 — 보고한다

## 리포트 형식

```markdown
# <slug> 결과 보고

## 상태: done / in-progress / blocked

## 수행 내용
- {추가/수정한 파일 목록}
- {화면·컴포넌트·viewModel 변경}

## 테스트 결과
- tsc 결과 (만진 파일 0 에러) · vitest 결과 (통과/실패 수, 실행한 파일)

## 다른 팀 영향
- BE 에 필요한 envelope·응답 변경
- SPEC·디자인 시스템과 어긋난 지점 (planner 보고 필요)

## 이슈/블로커
- {막힌 부분, 합의 필요 항목}
```
