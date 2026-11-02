# frontend — 시술 현황 코드 리뷰 W1 · W2 (코디 · 2026-10-27) — 작게

리뷰 `procedure-review-code-r3.md`(PASS · WARN 2).
- **W1(코디 기본값)**: 끄는 중 **자기 카드 위로 돌아오면 미리보기를 지운다**(= 원래 자리 · 놓으면 저장 없음). 지금은 마지막 대상이 남아 그 순서로 저장된다. `live/page.tsx:178` `onOver`
- **W2**: `live/page.tsx:173` 낡은 주석(귀가 대기 카드 위 drop 도 이제 판이 받음) 고침
- `tsc` · `lint` · 커밋 금지 · 보고서 `procedure-fe-v2-report.md` 「리뷰 W1 · W2」 절 + 앞과 같은 두 명령
