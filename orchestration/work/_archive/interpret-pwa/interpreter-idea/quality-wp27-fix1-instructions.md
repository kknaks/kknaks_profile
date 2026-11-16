# WP27 수정 1 — D-63 · 처분 §16 반영 후 7차 다시 (코디 · 2026-11-15)

1. 코드(`back/app/service/interpret/correct.py`): 바로잡기 ② — 대상 언어가 ja · zh · zh-Hant · yue 면, 다른 한자 언어 이름 · 별칭 중 한자가 든 꼴은 후보 제외(처분 §16 끝 줄) · 시험 1건(7차 ja S01 꼴: 다른 언어 한자 이름이 맞는 번역에 있어도 안 바꿈 — 지어낸 문장으로)
2. 시드 `.10`(`version` = `2026-11-15.10`): 처분 §16 표의 틀린 꼴 더하기 · 검사 8 · 긴 꼴 먼저 잡히는지
3. `ruff` · `pytest` · ㉒(거절 0 · 줄이기는 D-62 그대로)
4. **7차 196행 다시**(같은 음성 · 같은 목록 · 규칙은 시드 `.10` 에서 다시 만듦) → `quality-run/test7b-local.json` · 레포용 `test7b-result.json` · 결과 페이지 `quality-run/test7b-result.html`(같은 틀 · 사람 판정은 `test7b-human.js` — 빈 칸)
5. 보고 `wp27-be-report.md` 「수정 1 · 7차 다시」 절 — 언어별 기계 pass · 바로잡기 수 · 앞 판과 다른 행 번호
