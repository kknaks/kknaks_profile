# [writer] SPEC-002 · SPEC-003 수정 — 검수 FAIL 2 · WARN 반영

너는 SPEC-002 · SPEC-003 을 쓴 **procedure-hub `writer` 워커**다.

## 1. 읽을 것 (`orchestration/work/phub-recommend/`)

- `review-spec-002-003-report.md` — FAIL 2(SPEC-003) · WARN 13
- 수정 대상: `SPEC-002-mfds-mcp.md` · `SPEC-003-mfds-ingest.md`. 기준 DEC-003 · _RESUME §2

## 2. 할 일

1. **F-1 · F-2 를 닫는다.** F-1: 답 파일 ↔ 카드 해시 대조를 빌드 시점에도 다시 해서, 후보가 바뀐 카드의 옛 승인이 원장에 들어가지 않게. F-2: 대상 항목 파일에 결정론 연결 키를 두어 products.json 제품의 영문명 질의가 실제 대상 항목에 닿게(검수가 짚은 domain.py:230 실물 기준)
2. **W-13(키 누출)은 반드시** — httpx 로그 · 예외 메시지 · 캐시 파일 이름에 serviceKey 가 남지 않게(public 레포)
3. W-1 · W-2 · W-4 ~ W-12 반영. 실물 확인이 필요하면 키로 엔드포인트당 몇 번만(키 값 미기록). OQ-M03 은 검수가 답을 찾았으니(W-8) 닫는다
4. **W-3(정규화 일치 = 자동 확정)은 고치지 말고 OQ 로 남긴다** — 코디가 사용자에게 묻는 중
5. 두 문서 변경 이력에 「검수 반영 — F-1 · F-2 · WARN」 한 줄

## 3. allowed_paths

- 두 SPEC 파일 수정만

## 4. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: SPEC-002·003 검수 반영" \
  --body "F-1 · F-2 처리 / WARN 반영 · 미반영 / 다시 호출해 확인한 것"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] writer 완료 — SPEC-002·003 검수 반영. 상세는 인박스." --enter
```
