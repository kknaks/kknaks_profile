# backend WP-BE5 — SPEC-001 0.5.2 (묶음 구성 · 0원 줄 · PDF 줄 맞춤)

SSOT: SPEC-001 **0.5.2** · WORK-001 4판 **WP-BE5** 행 · 사용자 수정 `feedback-2026-11-02-b.md`(1 ~ 6). 맥락: 너는 BE4 를 만든 워커다.
- ⑤ `optionConfiguration.compositions` 에서 시술 이름 · 횟수 · 단위만 꺼내 저장(마이그레이션 0003) · 응답 `lines[].composition`(SPEC 꼴)
- 0원 품목 차례 = ② 차례 그대로(앞 유료 아래로 옮기기 없앰)
- PDF 명세서: 상자 · 요약 · 표 좌우 끝 같은 선 · 요약 칸 테두리 같은 굵기 · 「기간」 한 줄 · 묶음 줄 아래 작게 「구성」
- 저장된 9 · 10 · 11월은 ⑤ compositions 가 없다 → 다시 받기 없이 채울 길이 없으면 SPEC 대로 비워 두고 보고(코디가 전체 다시 받기)
- 운영 PG(5434) · 8800 · back/.env 건드리지 마라 · dev PG · testcontainers · ruff · pytest
- 완료 보고: WP-BE4 브리프 §9 두 채널(같은 task/dispatch) · subject 「backend WP-BE5 완료」
