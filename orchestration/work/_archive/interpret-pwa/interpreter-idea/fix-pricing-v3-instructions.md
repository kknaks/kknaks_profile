# writer_fable 수정 — 3판 WARN 3건 (2026-11-12)

`orchestration/work/interpreter-idea/review-pricing-v3-report.md` (a)(b)(c) 를 고칠 방향대로:
- (a) 결론 이유 3번에 「계정별 토큰 집계가 아직 안 됨(§7 #6)」 한 줄.
- (b) `corner()` 가 kmax < 1 일 때 k = 1 을 평가해 실현 불가 조건(41 × 87.6 + 60 > 3600)을 넣는 문제 — 실현 가능 조건 안에서만 평가하도록 고치고 재실행(토큰제 한꺼번에 최악 28.4% 예상 · 결론 불변이면 그대로).
- (c) pd2-D 표지가 가려지는 것 — 실제로 엇갈려 보이게 그리거나 본문 설명을 그림과 맞춘다.
숫자 · 그래프는 `calc2.py` 재실행으로만. 끝나면 재작성 브리프 §9 두 채널 — 반영 표.

앞 맥락이 없다면 먼저 읽을 것: `orchestration/work/interpreter-idea/rewrite-fable-brief.md`(규칙 · 완료 보고 §9 — --from term_d6650170-79a6-4a75-ac74-f269eee80776).
