# [designer] 회의록 내보내기 HTML 템플릿 — 「주제 스레드형」 · 페이지 단위(A4 인쇄)

너는 **sc-ax designer 워커**다(회의록 시안 세션). 이번 산출물은 dc.html 시안이 아니라 **BE 가 그대로 옮길 인쇄용 HTML 템플릿 하나**다.

## 사용자 결정 (2026-09-11)
- 내보내기는 **HTML 유지**, 조판은 **페이지 단위**(A4, 머리/꼬리, `@page` + page-break, 화면에서도 페이지 경계가 보이게).
- 양식은 mediness 「회의록 PDF 내보내기」의 **주제 스레드형** — 참고 이미지 `design/ref-export-thread-style.png`(우리 데이터로 다시 그린다):
  - 머리: 회의명(굵게) · 우측 일시(날짜·요일·시작~종료) · 참석자 한 줄
  - 요약 문단(우리는 「제목 후보/요약」이 없으면 생략)
  - **스레드 축**: 왼쪽 세로 점선 + 안건마다 점. 안건 제목(굵게) + 상태 칩(결론 남/안 남) + **발화 시각 칩**(그 안건 줄들의 근거 시각, 벽시계 HH:MM, 최대 3개 + 「+N」)
  - 안건 본문 = 최종 줄들(문장 나열, 줄마다 우측에 시각 하나 작게)
  - 「다음 할 일」 = 「액션」 칩 + 제목 + 기한 + 근거 시각 칩 / 근거 없으면 「근거 없음」 표기 · 승격된 것은 「요청됨」
  - 꼬리: 페이지 번호 · 「SCAX · 회의록」 · 내보낸 시각
- 자료 미리보기·업무 링크 없음. 색·타이포는 DS 토큰 값(인쇄용이라 CSS 는 파일 안에 인라인 — 외부 번들 참조 금지).

## 산출물
- `design/export-thread-template.html` — **정적 샘플 데이터**로 완성된 한 파일(CSS 인라인, 폰트는 시스템 폰트 스택). 안건 3개·줄 8개·할 일 4개 정도의 예시. 두 페이지 이상 나오게.
- `design/REPORT-export-template.md` — 자리별 규격(여백·폰트 크기·색 토큰값)·BE 가 치환할 자리(`{{meeting.title}}` 식 주석 표시)·인쇄 검증(Chrome 인쇄 미리보기 A4 에서 잘림 없음).

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_70f0f1a7-c2ca-4699-b77a-c168e2c2f4c8 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "designer 완료: 내보내기 스레드형 템플릿" \
  --body "파일 / 규격 요약 / 치환 자리 / 검증 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] designer 완료 — 내보내기 템플릿. 상세는 인박스." --enter
```
