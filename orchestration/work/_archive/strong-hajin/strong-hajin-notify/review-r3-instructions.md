# [reviewer] 알림 SPEC·WORK 재검수 r3 — 좁게

앞 판 `review-spec-work-r2-report.md` 의 FAIL 1(R-F1) · WARN 6(R-W1~W6)을 writer 가 고쳤다(지시서 `write2-fix2-instructions.md` · WORK 부록 3 r2 대응표). 같은 폴더.

## 볼 것 (이것만)
1. R-F1 · R-W1~W6 이 **본문에서** 닫혔나(부록 대응표를 믿지 말고)
2. 이번 수정이 고친 절 주변에 **회귀**가 없나 — 특히 §4.1 연결 수명(첫 ready · 둘째 ready · resync · 10회 멈춤)이 서로 모순 없이 한 줄로 읽히나 · SPEC-008 §4.4 와 맞나
3. R-W2 의 Makefile 타겟이 코드 레포 `Makefile` 에 실제로 있나

## 산출물
- `review-spec-work-r3-report.md`(같은 폴더) 하나 — §0 판정 · 항목별 · FAIL/WARN 목록 · 사용자에게 물을 것
- 완료 보고는 앞 브리프 §6 두 명령. subject 「reviewer 완료: SPEC·WORK 재검수 r3 <판정>」 · text 「[worker_done] reviewer 재검수 r3 <판정> — FAIL n · WARN n. 리포트 review-spec-work-r3-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
