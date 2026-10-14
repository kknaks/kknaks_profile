# [researcher] KOS 웹앱 HAR 2차 분석 (DEMO)

1차와 같은 규칙 · 같은 형식이다 — `kos-har-research-brief.md` §4 범위 제약(토큰 · 쿠키 값 기록 금지 · 재전송 금지 · 복사 저장 금지 · 고객 이름 `<고객>`)을 그대로 지킨다.

- 입력: `/Users/kknaks/Downloads/app.kos-solution.com2.har` (사용자가 DEMO 에서 1차에 없던 동작을 눌러 저장)
- 목표: 1차에서 「HAR 에 없음」이던 동작의 내부 API — **담당자 · 집도의 · 방 · 우선순위 · 시술 완료하기 · 단건 시술 취소 · 상담사 지정 · 시술 추가** (+ 녹화된 그 밖의 쓰기 전부). 특히 **시술 완료하기**(시술권 차감)
- 동작마다: 내부 경로 · 요청 본문 필드(값 모양) · 응답 모양 · 공개 OpenAPI 대응 유무 · 작업을 무엇으로 가리키나(`sequence`? task id? `ticketId`?)
- 1차 리포트 `research-kos-har-report.md` 는 **수정하지 말고**, 새 리포트 `research-kos-har2-report.md` 에 쓰고 맨 위에 「1차 + 2차 합친 동작 ↔ 내부 API 대응표」를 둔다
- 검증: 쓰기 요청 수 = 표 행 수 · 리포트에 토큰 · 쿠키 값 0건 · 재전송 0
- 완료 보고는 1차 브리프 §7 두 명령 그대로(subject 「researcher 완료: HAR 2차 …」, taskId/dispatchId 는 1차 것 task_b140c10eb08f / ctx_266d4b492e3e)
