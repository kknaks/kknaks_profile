# SPEC-001 · SPEC-002 수정 4회차 지시서 (0.4.0 → 0.4.1 · 문구 고침)

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · allowed_paths(SPEC 두 파일만) · 제약 · 검증 · §9 완료 보고는 그대로. **결정은 새로 만들지 않는다 — 이번은 문구 고침만.**

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`

## 읽을 것

1. `$W/review-spec-001-002-r4.md` — 새 WARN 4(Y-1 ~ Y-4) · 새 NOTE(N-1 ~ N-6 — N-7 은 코디가 `_RESUME` §2 에 행을 더해 닫음)
2. `$W/_RESUME.md` §2 맨 위 행(「재검수 2(r3) §5 결정 = 추천」) — 이제 SPEC 의 근거를 `spec-fix3-instructions.md` 대신 이 행으로 바꿔 단다

## 할 것

- Y-1: RG8 이 보는 입구 = 「겹침을 가른 뒤(범위 규칙 · entity Choice) 남은 입구」. RG6 으로 두 개념을 다 둔 경우의 처리도 리포트 고칠 방향대로.
- Y-2: M1 ① · D3 ① — 후보가 케이스인 묶음은 `procedure_code` 로 센다(케이스 이름 금지 M6 · G10 · P7 과 맞춤).
- Y-3: 부위·고민(「무엇을 하나」) 꼴에서는 **깊이를 두지 않는다**(required 가 폭에서 다 참 · 모범 답에 효과 없음 — `_RESUME` §2 안전 행). §3-2 깊이 칸 · 키 명세 · 채점 입력을 맞춘다.
- Y-4: §3-2 부위·고민 행의 후보별 `facets` profile role = `자기` · `물려받음`(허브 기본값) · 호출 명세 §9-5 도 같은 값 · `mechanism_name` 빈칸이면 G4 층 표시와 함께 윗층 값임을 밝힌다.
- N-1 ~ N-6: 리포트 고칠 방향대로.
- 두 SPEC 의 근거 표기 「spec-fix3-instructions.md §…」 를 `_RESUME §2 11-16 「재검수 2(r3) §5 결정」` 로 바꿈(지시서는 보조 근거로 남겨도 됨).
- version 0.4.1 · 변경 기록.

## 검증

- Y · N 각 → 문서:줄 표 · 원칙 grep(폭 줄어드는 자리 0) · 안전 강제 첨부 grep(0) · 부록 A 헤더 대조 · 공개 grep — 결과를 보고 body 에.
