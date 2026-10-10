# [reviewer] 알림 SPEC·WORK 재검수 r2

앞 판 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-spec-work-report.md` 의 FAIL 3 · WARN 11 을 writer 가 고쳤다. 지시서 `write2-fix1-instructions.md`(같은 폴더) · 사용자 결정 원장 `_RESUME.md` §2 「검수(FAIL 3·WARN 11) 뒤 사용자 결정」 행.

## 볼 것
1. FAIL 3 · WARN 11 이 **각각 실제로 닫혔나**(WORK 부록 3 대응표를 믿지 말고 본문에서 확인) — 특히 F-1 재연결 계약이 `EventSource` 동작과 맞나(새 인스턴스 · `?last_event_id=` · 세션 확인으로 가르기 · 회복 시험)
2. 새 결정 DEC-010 D-36~D-41 이 원장 행과 맞고 SPEC 에 대응하나 · 뒤집은 줄 취소선
3. **회귀** — 이번 수정이 앞 판에서 PASS 였던 대응(67행 · 35건 · 16항목 · 꼬리표 · kind)을 깨지 않았나
4. 새로 들어간 수치(겹침 창 60초 · OS 묶음 10초/셋 등)가 근거를 갖나
5. Code Surface 빠짐 5 를 네가 다시 grep 해 확인

## 산출물
- `review-spec-work-r2-report.md`(같은 폴더) 하나 — 형식은 앞 판과 같게(§0 판정 · 항목별 · FAIL/WARN 목록 · 사용자에게 물을 것)
- 완료 보고는 앞 브리프 §6 두 명령. subject 「reviewer 완료: SPEC·WORK 재검수 <판정>」 · text 「[worker_done] reviewer 재검수 <판정> — FAIL n · WARN n. 리포트 review-spec-work-r2-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
