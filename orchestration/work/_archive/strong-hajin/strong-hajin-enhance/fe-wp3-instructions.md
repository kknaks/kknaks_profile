# [frontend] WORK-012 Phase WP3-FE

기존 구현 브리프(`strong-hajin-enhance-fe-impl-brief.md`)의 규칙 그대로(allowed_paths · 하지 말 것 · 커밋 금지 · 포트 금지). **WP1 `e51fe3b` · WP2 `e58fb25` 커밋됨** — 그 위에서.

- 할 일: `P/30-work/work-012-enhance.md` **「Phase WP3-FE」 절의 계약 체크박스 전부** + Code Surface WP3 표의 자리 전부(표 밖 같은 심볼도)
- 계약: SPEC-010(AX 회의 생성 · 회의실 셀렉트 · AX 수정 카드 편집 계약 · 옛 meeting.update 합침 · 업무 생성 맥락 목록) · DEC-009
- WP1 검수 **W-3**: 불러오기 뒤 지난 회의 방이 새 시간에 없으면 조용히 「예약 없음」 이 되지 않게 — 회의실 셀렉트(이번 판)에서 이유를 보인다
- AX 회의 생성 카드는 업무 생성 카드(`AxDraftCard`)와 **흐름·디자인만 같게, 내용은 회의 고유 필드**(OQ-901 · OQ-1001 쪽 구성)
- WP3-BE 와 병렬 — 서버 계약은 WORK-012 WP3-BE 절 · SPEC-010 에 고정, 그대로 소비
- **검증 = 바꾼 부분 관련 시험만**(전체 make test · make verify · 프론트 전체 vitest 금지 — 마지막에 코디가 한다). 돌린 시험 파일 목록과 수치를 리포트에
- 리포트: `W/fe-wp3-report.md` · 완료 보고: 기존 브리프 §7 두 명령(subject 「frontend 완료: WP3-FE」). **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
