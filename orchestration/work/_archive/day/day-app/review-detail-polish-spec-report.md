# 리뷰 리포트 — day-app 룸 상세 다듬기(SPEC-003 개정 ④ · WP v5) / doc · 좁은 검수 (2026-11-10)

- 대상:
  - 스펙 트리 `d6d961e9` 위 미커밋 `products/day/20-spec/spec-003-mobile-app.md`(+32/−12 · 파일 1개)
  - profile `delivery-request-v5.json`
  - 최신 ASCII = `detail-polish-spec-layout-fix-report.md`(준비중 · 호출 중 · 수락 뒤 [시작]도 둘째 줄 오른쪽 — 모든 조작이 아래 줄 오른쪽)
- 원천:
  - `detail-polish-spec-brief.md`(사용자 「응 호출중도 시작 비활성화 로 두자 / 시술 목록에는 시술경과가 메인이야 / 와이어프레임 수정안 다 그려바」 · 승인 「ㅇ으 그렇게 해서 이거까지 발주하자」)
  - `_RESUME.md` :3 · :300
  - `delivery-request-v4.json` · `delivery-v4-apply-result.json`(contract `775e4f0a…` · plan_digest `60de61f5…`)
  - 코드 read-only: day-app `47be2cb0` `app/lib/ui/format.dart` · 옆 backend `a1c90b9d` `board_rules.py:260-272 start_block`
- 방법:
  - diff 직접 대조 · `git diff --check`
  - v4 ↔ v5 JSON 경로 diff · harness 모델 1회
  - lint · schema는 planner 로그(0 error · 0 errors)를 확인하고 반복하지 않았다
  - 수정 · 하위 위임 없음

## 판정: PASS (FAIL 0 · WARN 0)

## 의미 · 범위 · 권한 정합

| 확인 | SPEC 근거 | 원천 대조 | 결과 |
|---|---|---|---|
| 룸 머리 정가운데 | U-4 `:227` 「헤더 전체 폭 기준 정가운데(왼쪽 버튼을 뺀 영역 아님) · 긴 이름 말줄임 · 뒤로 영역 · 접근성 그대로 · 다른 머리 무변경」 · Wireframe `:113` · A-31 · OQ-A31 머리 부분만 취소선(상세 마취 칸은 남음) | 브리프 ① | PASS |
| 호출 상자 = 미수락 남은 호출만 | U-4 1번 `:231` 「`called` 줄이 하나라도 남은 호출만 · 전부 수락된 큰 상자 숨김 · 부분 수락 · 여러 호출 중 미수락 남은 상자 그대로」 · 상자 내용 · 버튼 · 재호출 문장은 무변경 | 브리프 ② | PASS — 새 집계 정책 없음 |
| 시술 행 5상태 ASCII | U-7 ASCII: 준비중 · 호출 중 · 수락 뒤 = 1줄 시술명 / 2줄 담당의 + 오른쪽 [시작] · 진행중 = 1줄 시술명 + 큰 mm:ss / 2줄 담당의 · HH:MM 시작 + [종료] [⋮] · 완료 = 1줄 시술명 + 「완료 N분」 / 2줄 담당의 + [⋮] — **모든 조작이 둘째 줄 오른쪽**(layout-fix와 일치) | 브리프 ③ · layout-fix | PASS |
| 배지 · 행 수락 제거 | U-7 「상태 배지(진행중 · 수락 · 호출) 그리지 않음 · 그 행 값만」 · 호출 중 「행 [수락] · 호출 배지 · 호출 대상 · 경과 글자 없음」 · 버튼 목록에서 [수락] 제거 · U-6 들어오는 곳에서 「시술 카드 [수락]」 제거 + 「상단 호출 강조 상자로 모음」. 옛 「시술 카드 [수락]」 · 「호출 = 지금 − 처음 호출」 문장 잔존 0(grep) | 브리프 ③ | PASS |
| 수락 경로 · 정책 보존 | U-6 분기(원장 즉시 · 간호 대리) · 목록 카드 호출 줄 · 호출 탭 · 상단 상자 · 푸시 무변경 · A-39 회귀 | 브리프 ② | PASS — 수락이 사라진 자리 없음 |
| [시작] 활성 = 서버 값 | 「기본 비활성은 예시 · 활성은 서버 `canStart` 그대로 · 준비중 KOS 담당의면 true 가능 — 막지 않음 · 수락 뒤 false면 비활성 · 호출 중 = 서버 false 그대로」 | `start_block`: 호출 미수락 → `call_not_accepted`(false) · accepted → None(true) · 호출 없고 `kos_doctor` 있으면 None(true) · doing/done → false | PASS — 원천 코드와 일치 · 새 판정 없음 |
| 진행 경과 · 완료 N분 | 진행중 = 지금 − 그 행 `startedAt` mm:ss(개정 ③ 형식 · 기존 1초 갱신 · 새 타이머 없음) · 완료 = 「기존 끝 − 시작 분 표시 변환 그대로 · 새 반올림 정책 없음 · 시각 하나라도 없으면 「완료」만」 | `format.dart:48-52` `spanMin` = 둘 중 null이면 '' · 반올림 · 최소 1분 → 빈 값이면 「완료」로 연결 가능 | PASS |
| ⋮ · 확인 창 · 권한 | ⋮ = 진행중 「시작 취소」(`canUndoStart`) · 완료 「완료 취소」(`canUndoFinish`) · 확인 창 원문 · `/me` `board` edit일 때만 · 보기만 직무 새 조작 없음 | 개정 ② 그대로 | PASS |
| 범위 밖 무변경 | 개정 ④ 머리 · A-39: 목록 카드(상태 박스 2줄) · 4메뉴 · 통역 · 토스트 · 세션 · API · needs · canRecall · 상세 마취 칸. diff hunk도 머리 · Wireframe · U-4 · U-6 · U-7 · A-31 · A-39 · OQ-A31뿐 | — | PASS |
| 문구 발명 | 새 글자 = 「완료 {N}분」 · 「완료」 · 「{HH:MM} 시작」 — 모두 사용자 승인 와이어 · 기존 앱 글자. 그 밖 새 문구 없음 | — | PASS |

## WP v5 (`delivery-request-v5.json`)

| 점검 | 결과 |
|---|---|
| 모델 | `DeliveryRequest.model_validate` OK(contract_version 5 · L3) · JSON 파싱 OK · schema 0 errors(planner 로그) |
| 버전 · 결속 | #235 현재 v4(`delivery-v4-apply-result.json` contract `775e4f0a…` · plan_digest `60de61f5…`)를 scope_delta가 정확히 인용 · 코드 head `47be2cb0` · 사용자 원문 2개와 승인 「ㅇ으 그렇게 해서 이거까지 발주하자」 결속 |
| 같은 Delivery | `day/day-app` · baseline `3f57c1af…` pending · app/만 · PR #237 하나 · 사용자 마지막 merge · backend 수정 없음 |
| 최소 diff(v4 → v5) | 바뀐 키 = title · scope_delta · contract_version · acceptance[0] · A19 · A27(추가) · target_delta[16](추가) · review_surface[0] · [11](추가) · phases[4] · verification[0] · open_questions[0]. 그 밖(A2 수락 분기 · A16 · A17 · A18 · A20 ~ A26 · non_goals · dependencies · rollback)은 동일 |
| 원천 SHA | 「d6d961e9 + 개정 ④ 미커밋 — 코디 커밋 head로 결속」 정직 표기 |
| 승인 | receipt · 승인 주장 없음(L3 새 plan_digest 승인은 코디 몫) |

## 검증

- `git diff --check` → 출력 없음 · exit 0 · `git status` M 1개(spec-003). 타 SPEC · `20-spec.md` · 코드 무변경.
- planner 로그: lint `--strict` 0 error / 263 warning · `products/day` 0 · v5 schema 0 errors.

## 참고 (결함 아님)

- v5 `target_delta[11]`([v2 ⑧⑨⑩] 원래 항목)은 「< 시술현황 · {방}」 · 「시술 카드형」 옛 서술 그대로다. v5 A19 · target_delta[16]이 대체를 명시해 실제 약속은 충돌하지 않는다. 다음 버전에서 「v5에서 대체」 꼬리표를 달면 읽기 쉽다.
- 「완료 N분」의 분 산정은 SPEC이 「기존 표시 변환 그대로」로만 적고 규칙을 풀어 쓰지 않았다. 지금 코드 `spanMin`은 반올림 · 최소 1분이다(마취 완료 `lastSeconds ÷ 60` 내림과 다른 기존 규칙). 구현 리뷰 때 이 기존 함수 재사용 여부만 확인하면 된다.

## 남은 것

- 코디: 개정 ④ 커밋(exact head) → v5 plan(origin/main 재 fetch) → L3 승인 → #235 apply → mobile 코드 발주(룸 상세 머리 · 호출 상자 · 시술 행만).
- 상세 마취 칸 글자(OQ-A31 남은 부분)는 지금 그대로다.
