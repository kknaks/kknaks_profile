# [qa · 2차] 같은 시나리오 — **창 띄운 모드(headed) · 사용자가 화면을 보고 있다**

같은 터미널 · 같은 맥락(`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/qa-1-report.md`). 이번에는 **사용자가 이 Mac 화면에서 진행을 눈으로 본다.**

## 실행 방식(반드시)
- Playwright **`headless=False`** · **`slow_mo=600`** 정도 · 창 크기 1600×1000 · 브라우저 창 **하나**(탭은 필요할 때만) — 사용자가 따라 볼 수 있게.
- 시나리오마다 시작 전 페이지에 짧게 멈춤(2 ~ 3초) · 호버 · 팝오버 · 툴팁은 **3초 정도 띄워 둔 채** 스크린샷.
- 끝나면 창을 **바로 닫지 말고 10초** 두고 닫아라.
- 로그인 1회만(테스트 계정 · 끝나면 KOS 로그인 해제 · DAY 로그아웃).

## 바뀐 것(고침 뒤 다시 볼 것)
- FAIL-1 링크 복사/열기 고침 · WARN-1 CSP 콘솔 오류 고침 · W-a [+] 칸 · 빈 칸 누르기 = 그 그룹 간격 단위(60분 그룹 = 정각만 · 등록 창 시간 늘 골라짐) · 링크 진행 줄 = 「남은 시간 mm:ss」만(카메라 글자 · [QR 닫기] 없음).
- **6개월 경과 데이터**: 코디가 로컬 DB 에 고객 `b26e24e0` 의 7개월 전 문진 1행(`acb32d7a`)을 넣었다 → 방문 `def4cbab` 상세 「초진 문진」 줄 = 「6개월 경과」 · [문진 QR] 보임 이어야 함.

## 시나리오 (qa-1 과 같은 번호 · 방문 `def4cbab` 19:00 · `7511bbb0` 19:30)
1 F2 배치 · 2 F1 [+](정각 칸 · :30 칸 둘 다 — 60분 그룹 :30 은 어떻게 되는지) · 3 F3 팝오버 · 4 F5(기기 0대 — 빈 목록 그대로) · 5 F6 웹 진행 칸 · 6 링크 복사(클립보드 값 확인) · 링크 열기(새 탭이 그 링크 · 문진 첫 화면 · **제출 금지**) · 두 번 = 같은 링크 · 7 D45(가능한 범위) · 8 **6개월 경과** · 9 콘솔 오류 0.
KOS 쓰기 동작 금지(저장 · 옮기기 · 취소 · [다시 보내기] · 제출) 그대로.

## 산출물
- 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/qa-2/` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/qa-2-report.md`(맨 위 표 · qa-1 대비 바뀐 판정)

## 하지 말 것
코드 · 문서 · 스택 · DB 쓰기 · 비밀값 · PII 출력.

## 완료 보고 — 문구 변경 금지
⚠ 핸들은 dispatch preamble 값을 믿어라.
```bash
orca orchestration send --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "qa 완료: <한 줄>" --body "<요약>"
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[worker_done] qa 완료 — <한 줄>. 상세는 인박스." --enter
```
