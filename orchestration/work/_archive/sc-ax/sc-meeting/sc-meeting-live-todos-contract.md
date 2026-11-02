# 계약(코디 확정) — 회의 중 「다음 할 일」(D46, 사용자 2026-09-11)

회의 중 AI 배치가 안건별 후속 업무 후보를 낸다. **읽기 전용** — 회의 중에는 [업무 생성]·[×] 없음. 승격은 종료 뒤 최종에서만(지금대로).

- **배치 스키마** `modules/meetings/schemas/ai_batch_output.json`: `agendas[].todos` 를 **required** 로 추가(빈 배열 허용, maxItems 10). 항목 = 최종 스키마의 todo 와 같은 모양 `{title(1~100), description, due_candidate: string|null(YYYY-MM-DD), checklist_candidate: [string], line_ids: [string]}`. strict 규칙 그대로(모든 키 required, 선택은 nullable).
- **적재**: `meeting_todos.provisional BOOLEAN NOT NULL DEFAULT false` 열 추가(additive → sync-demo-schema). 배치마다 그 회의의 **provisional=true 전량 삭제 후 이번 회차 것으로 교체**(AI 트랙 줄과 같은 결, 같은 트랜잭션). 담당자 없음·description 항상은 §8.2 그대로 적용하되 회의 중이라 **checklist 는 비어도 된다**. 기존 업무 중복 제외(`task_list`)도 회의 중엔 생략 가능(최종에서 한다).
- **최종 합성**: 시작할 때 provisional 전량 삭제, 최종 todos 는 지금대로 provisional=false 로 전량 교체(승격된 것 유지).
- **응답**: `Todo` 에 `provisional: bool` 필드 추가(MeetingDetail `agendas[].todos`, ai.batch 프레임 안 todos 모두). `ai.batch{seq, agendas:[{…기존 Agenda 모양(lines 는 track ai), todos:[Todo]}]}`.
- **게이트**: provisional 인 todo 에 promote/delete → 409 `todo_provisional`. 회의 상태 in_progress 에서 promote 는 어차피 409(기존).
- **FE**: 「AI 요약」 탭(in_progress) 안건 블록 밑 「다음 할 일」 = 배치가 온 뒤엔 `stream.batch.agendas[].todos`, 배치 전엔 상세 `agenda.todos.filter(provisional)`(늦게 들어온 참여자). 항목 = 제목 + 기한 후보(있을 때만). 버튼 없음. 없으면 「후속업무 후보가 없습니다」 그대로. 메모 탭엔 안 보임. done/failed 화면은 지금 그대로(provisional 은 최종이 지우므로 안 온다).
