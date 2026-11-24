# [planner · 고침 2] 2차 검수 WARN 8 닫기 + D54 ~ D56

같은 터미널 · 같은 규칙(브리프 `day-reservation2-spec-brief.md`). 앞의 「[코디 중지]」는 풀린다 — 이 고침만 한다.

## 읽을 것
- `review-doc-2-report.md`(같은 폴더) — **W-N1 ~ W-N8 전부 「고칠 방향」대로**
- 결정 파일 맨 아래 **D54(SNS = DAY `SnsType` enum 6개 그대로 · KOS 같은 값) · D55([문진 QR] · [여권 스캔] = 시안 조건 · 비활성) · D56(빈 오더 메모 안 보냄)**

## 코디 답 (고칠 방향과 다르거나 비어 있는 것)
- **W-N4**: W13 ④ 의 시술 작업 seq = **「방 배정」 만들기와 같은 예외(SPEC-002 규칙 28 · `_chain_room_assign`)로 `add-flow-tasks` 2xx 뒤 바로 상세 조회해서 새 seq 를 찾고 이어서 방 지정**. 이건 기존 예외를 시술권 작업에 넓히는 것이고 D53(모든 쓰기 즉시 확인 일반화)은 아니다 — 그렇게 적어라
- **W-N5**: W7a / W7b 판정 = **쓰기 계획 단계(서버 중앙)에서 KOS 상세(`consultations[]`)를 읽어** 가른다. `consultationId` 는 쓰기 큐에 넣을 때 DAY 가 만든 uuid 를 그대로(다시 시도도 같은 id). RB-11 `get-visitor` 사본 = 저장 요청 안(R39 예외 W1 과 같은 자리)
- **W-N6 · W-N1 · W-N2 · W-N3 · W-N7 · W-N8**: 고칠 방향대로
- OQ-D22 · D23 = D55 · D56 으로 닫음 · OQ-D24 = 열린 것 아님(W-N8) · OQ-D07 = D54 로 SNS 닫음(국가번호 목록만 남김) · OQ-D25 그대로

## 검증 · 보고
lint --strict products/day 0 error. 보고에 W-N1 ~ W-N8 처리 자리 · 남은 OQ. 완료 보고 두 명령(subject 「planner 완료: 고침 2」 · 이번 dispatch 값).
