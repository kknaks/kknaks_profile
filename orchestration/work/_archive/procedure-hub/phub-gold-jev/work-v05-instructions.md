# WORK-005(허브) · WORK-006(앱) 작성 지시서 — SPEC 0.5.1 길 찾기 재설계 구현 계획

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더 — 앞 WORK-001/002 때 지시)의 역할 · 제약 · 검증 · 완료 보고 꼴을 그대로 따른다. allowed_paths = **`WORK-005-hub-v05.md` · `WORK-006-app-v05.md` 두 새 파일만**.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev`

## 읽을 것

1. `$W/SPEC-001-hub-gold-mcp.md` · `$W/SPEC-002-chat-eval.md`(0.5.1 · 재검수 PASS) — 변경 기록 0.5.0 · 0.5.1 이 무엇이 바뀌었는지 요약
2. `$W/review-spec-v051.md` §7 NOTE 6 — WORK 에 한 줄씩
3. `$W/_RESUME.md` §2(맨 위 「끝까지 진행」 부터)
4. 지금 코드(이어서 고치는 것 — 새로 쓰지 않는다): 허브 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev/backend/app/modules/gold/` · 앱 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev/clinic_chat/`(walk · columns · select · web · speed). 앞 계획 `$W/WORK-001-hub.md` · `WORK-002-app.md` · `WORK-003-web.md` · `WORK-004-speed-tab.md` · 구현 보고 `$W/app-report.md`
5. KD8 결과: `$W/kd8-jev-check-report.md` — **지금 다른 워커가 쓰는 중**. 있으면 읽고 KD2/KD3 의 WP 를 그에 맞추고, 없으면 그 WP 를 「KD8 결과로 정함 — 대안 둘(본문 그대로 / 사이 값 상위 n)」 로 적어라

## 쓸 것

- **WORK-005 허브**: resolve 확장(부분 일치 · 조사 무관 · covered_by) · `coverage` 도구(14 종류 × 자기/하위/물려받음 · 칸 값 정의) · 하위 role · 도구 설명(W-4) · 시험(T16 등). 진행 중인 서버 · 앞 시험을 깨지 않게.
- **WORK-006 앱**: 단계 ① 맨 앞 판단(TG · KD · RG · CD) · ② 고른 대상 × 종류 읽기(하위 층 · RQ1 네 줄) · §3-2a 싣는 칸 · verified_lines / answer_lines · 답 프롬프트(P2 · P9 · P10 — 초안 · 사용자 확인 C-1) · b_slim 을 새 B 로 합침(O-26) · 속도 탭 · 화면 · 기록 · 답 키 스크립트(37 다시 뽑기 · N-2) · 실물 확인(E: 「써마지 효과」 「써마지의 원리」 「팔자주름에 뭐 해?」 「인모드가 뭐야」 Q22 → 종료 상태 · 입력 KB · 첫 답 글자)
- NOTE 6 한 줄씩 · 순서 · 병행(허브 WP 와 앱 WP 를 나란히 — 앱은 coverage 응답 꼴만 모의로) · 완료 조건 · 검증 명령(앞 WORK 와 같은 꼴).

## 검증

SPEC 0.5.0 · 0.5.1 변경 절 ↔ WP 대응표(미대응 0) · 파일 경로 실재 · 공개 grep.
