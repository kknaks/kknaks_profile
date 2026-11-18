# SPEC-001 · SPEC-002 수정 1회차 지시서

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · allowed_paths(SPEC 두 파일만) · 제약 · 검증 · §9 완료 보고는 그대로 적용한다. 이번 일은 **새로 쓰기가 아니라 고치기**다.

경로: `W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`

## 읽을 것

1. `$W/review-spec-001-002.md` ← 검수 리포트(FAIL 1 · WARN 11 · NOTE 10). 지적마다 「고칠 방향」 이 있다
2. `$W/_RESUME.md` §2 맨 위 행(11-16 「검수 뒤 결정 4」) ← 사용자 결정. **이것이 고칠 방향의 선택을 정한다**
3. 고칠 대상: `$W/SPEC-001-hub-gold-mcp.md` · `$W/SPEC-002-chat-eval.md`

## 할 것

1. **사용자 결정 4 반영**(열린 것 → 본문 결정으로 옮기고, 열린 것 표에서는 「결정됨(11-16) → §n」 으로 남김)
   - ① F-1 답 키: SPEC-002 §8 · §9 — 답 키 = 37 문항을 허브 도구 길 전체 행으로 결정론 스크립트가 다시 뽑음(입력 · 출력 칸 · 놓일 자리(gitignore 로컬) · 사용자 확인 절차). `gold_pointers` · `answer` 는 표본임을 명시. D3 = 「빠진 코드」 전체 키 대조 · 「지어낸 코드」 gold 실재 여부. D5 G1 「전부」 도 전체 키로. ② 채점 입력도 전체 키
   - ② SPEC-001 O-1 → 보조 입력: silver `concern` · `adverse` · `condition` 의 `code` · `parent_code`. §2 입력 · 해시 · §3 색인 · 계층 펼침을 쓰는 도구(`concern_candidates` · `facets` · `pair`/패키지 등 실제로 쓰는 곳 전부 grep 으로 찾아) 계약에 반영. gold 는 불변
   - ③ SPEC-001 O-2 → 원장 확인 목록(ledger-check-list)의 id · 코드만 보조 입력 · 해당 응답에 `ledger_check[]`(꼴 정의). SPEC-002 W-1 의 「원천 미확정」 세 조건과 이어서
   - ④ SPEC-002 O-1 → A 열 = 앱 로컬 stdio MCP 3도구(목록 · 경로 읽기 · 검색) — 입력 · 출력 · 원장 폴더 env · trace(읽은 경로 — W-4 와 같이)
2. **추천대로 확정된 것**: SPEC-002 O-3(범위 Choice 에 「범위 밖」 옵션 · 9) · O-4(① 가장 낮은 값 ② required 미충족일 때만 높은 순 ③ 설정 · 넘으면 「실행 중단」) · O-6(batch 안 고정 · 실제 id 기록) · O-12(1회차는 재기만) · O-13(차례로 · 순서 섞음 · 기록) · O-14(batch 만) → 본문 반영 + 열린 것 표 「결정됨」
3. **검수 지적 전부**(W-1 ~ W-11 · N-1 ~ N-10)를 리포트의 「고칠 방향」 대로 고친다. 선택지가 여럿이면 리포트 첫 선택지. 그 밖은 열린 것으로
4. 남는 열린 것(SPEC-001 O-3 ~ O-11 중 남은 것 · SPEC-002 O-2 · O-5 · O-7 ~ O-11)은 그대로 두되 검수가 더하라고 한 항목(O-4 ④ · O-5 칸 단위 required · O-12 꼴 「제안 모음」)은 더한다
5. 두 문서 version `0.1.0 → 0.2.0` · updated_at · 맨 끝에 「변경 기록」 절(지적 번호 → 고친 곳 줄)

## 검증(브리프 §8 에 더해)

- 지적 21 + 결정 4 가 각각 어디서 고쳐졌는지 표(번호 · 문서:줄)를 보고 body 에
- 부록 A 헤더 대조 다시 실행(보조 입력 칸도 실제 silver CSV 헤더 · ledger-check-list 헤더와 대조)
- 공개 레포 grep 다시
