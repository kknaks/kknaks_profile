# [frontend] 회의록 v3 후속 2건 — 텍스트 입력 포커스 파란 링(항목 5 미해소) · AX 플로팅 버튼이 패널 푸터를 가림

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = v3 커밋). `frontend/` 만, 회의록 페이지 범위. 커밋 금지.

## 코디 실물(1919×936) 확인 결과

1. **항목 5 미해소**: 예약 모달의 텍스트 입력(주제·목적·안건·참석자 검색·장소)이 포커스되면 여전히 **파란 테두리**가 선다(모달을 열면 주제 칸이 자동 포커스돼 파랗게 보임). 네이티브 select 가 사라진 것과 별개로 `input[type=text]` 의 focus 스타일이다. 사용자 요구: **파란 링 안 뜨게** — DS 의 조용한 포커스(테두리 `--border-strong` 정도)로 통일. 회의록 페이지의 입력 부품 범위에서(공용 부품이면 부품 단위 OK), 전역 outline 제거는 금지(접근성).
2. **AX 플로팅 버튼(우하단 FAB)이 오른쪽 패널 푸터의 [회의록 열기] 버튼을 가린다** — 패널이 화면 높이를 다 쓰게 되면서 겹침. 회의록 페이지에서는 패널 푸터가 FAB 와 겹치지 않게(패널 우측/하단 여백 또는 푸터 버튼 묶음을 FAB 폭만큼 안쪽으로). 다른 페이지 불변.

## 검증
```
cd frontend && npx tsc --noEmit + npx vitest run src/meetings/. 테스트 1(포커스 시 파란 링 클래스/outline 없음 — 가능한 범위에서).
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 회의록 v3 후속(포커스 링·FAB 겹침)" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 회의록 v3 후속. 상세는 인박스." --enter
```
