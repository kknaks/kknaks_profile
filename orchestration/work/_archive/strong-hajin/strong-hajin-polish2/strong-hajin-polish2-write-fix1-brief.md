# [writer] 고도화 2차 SPEC — 검수 FAIL·WARN 재수정 (fix1)

앞 판 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-write-brief.md` 의 규칙·allowed_paths·완료 보고가 그대로다.
검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-spec-report.md` — **전부 읽고** 아래대로 고친다.

## 고칠 것

1. **FAIL — SPEC-004 「날짜가 바뀌는 세 자리」**: `:373`·`:416` 과 리포트가 짚은 `:925`·`:1039-1040`·`:1420`·`:1429`·`:1625`·`:1659` — 넷째 자리(완료의 마감일 채움)를 더해 **넷**으로. 같은 개념의 다른 서술을 grep 으로 다시 전부 센다. AC 한 줄 추가. **OQ-405 는 닫는다**(코디 2026-10-02: 건다)
2. **WARN — SPEC-002 `:295`·`:234`** due_date 표기를 「마감일」로(U-17·OQ-Q①)
3. **WARN — SPEC-002 `:450`·`:681` 「변경 없으면 회차 안 오름」** — **유지한다**(코디 결정 2026-10-02). 근거를 「(코디 2026-10-02 — 고친 차이가 없는 회차는 기록할 것이 없다)」로 적는다
4. **WARN — SPEC-002 `:471`** 예외의 출처를 새 절(§4 「초안 저장」)로 고친다
5. **WARN — SPEC-001 `:376` U-7** 값 줄을 날짜 넷/마감일 결정과 맞춘다(리포트 근거대로)
6. **OQ 닫기** — SPEC-001 OQ-Q·OQ-R, SPEC-004 OQ-405 를 코디 답으로 닫고 본문에 반영:
   - OQ-Q: ① 「기한 지남」 칩·「기한 초과」 배지도 「마감일」 ③ DateField 입력 표기 `2026/10/06` ⑤ SPEC-004 거절 문구(`:300`·`:1048`) 날짜 형식 통일 · ② 만들기 창·캘린더 「시작일」 라벨 유지 ④ 캘린더 날 머리 유지
   - OQ-R: 서버 확인은 고친 초안을 계속 받는다(다른 카드·MCP 가 쓴다). 두 AX 초안 kind 의 화면만 저장 명령을 쓴다
7. **권장 반영** — SPEC-002 §6 의 「채팅 서랍 안 단추」 AC 열거에 「근거 N개 더 보기」(사람 행동 → 검정 계열) 추가 · 「포커스 링은 이번 범위 밖」 한 줄

고친 SPEC 은 이미 올린 버전 안에서 변경 이력 줄만 보탠다(버전 재상승 불필요).
완료 보고 subject 는 「writer 완료: 고도화 2차 SPEC fix1」.
