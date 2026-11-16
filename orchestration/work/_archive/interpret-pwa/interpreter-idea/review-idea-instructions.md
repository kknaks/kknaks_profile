# reviewer_doc 검수 — 아이디어 목업 `idea.md` (2026-11-12)

대상: `reference/2026-11-12-interpreter-idea/idea.md` + 같은 폴더 `idea-*.svg` 11장 + `orchestration/work/interpreter-idea/idea-src/make_svgs.py`.
**계약 = 작성 브리프** `orchestration/work/interpreter-idea/interpreter-idea-idea-brief.md` §0 ~ §3 · §8.

볼 것:
1. 단계 정의가 브리프 §2(사용자 말) 그대로인가 — 특히 **QR = 고객 화면**. 늘리거나 바꾼 곳.
2. 결정 문장 0 · 미정인 곳은 선택지 목업으로 그렸는가 · 열린 것 목록이 빠짐없는가.
3. 0단계 목업이 지금 통키 화면(`/Users/kknaks/git/toy_pr2/interpret-pwa/front/` main `17c26b5`)과 맞는가 — 인용한 컴포넌트 · 구성 대조.
4. 제안서 아이디어 표 — 쪽 번호가 맞는가(pdftotext 쪽별 대조) · 문구 복사 0(20자 겹침).
5. 숫자(원가 · 병원) 0 · 병원/지점 데이터 0 · 예시 문장이 실제 기록 · 실명이 아닌가 · 키 0.
6. SVG — 전부 열리는가(xmllint) · 글자 잘림 · 겹침(가능하면 `qlmanage -t` 나 브라우저 렌더로 눈 확인) · md 참조 경로.
7. 「새로 필요한 것」이 설계 · ERD 수준으로 넘어가지 않았는가.

리포트: `orchestration/work/interpreter-idea/review-idea-report.md` 1개 — PASS/WARN/FAIL, 지적마다 파일:줄 · 근거 · 고칠 방향. 수정 금지 · Soniox/운영 서버 호출 금지. 보고는 원 브리프(`interpreter-idea-review-doc-brief.md`) §9 두 채널.
