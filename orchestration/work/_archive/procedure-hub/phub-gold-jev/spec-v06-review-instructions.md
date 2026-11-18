# SPEC 0.6.0 검수 지시서

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-doc-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값). **디스크 여유 2~3GB — 큰 파일 만들지 마라.**

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만)

읽을 것: `$W/spec-v06-instructions.md`(지시) · `$W/_RESUME.md` §2 11-17 행 · `$W/batch-v052-summary.md` · 두 SPEC 0.6.0 변경 기록 · SPEC-002 §3-7(541행~) · §11 U-5 ~ U-8 · batch `20261117-115258-v052-37-a7df` trace(`$A/runs/runs.jsonl`) · 보고서 `$A/runs/reports/20261117-115258-v052-37-a7df.md`.

할 것:
1. 지시 A(A1~A4 · Q21 · Q24) · B · C 가 문서:줄로 닫혔나 표.
2. 원인 넷의 근거 수를 **네가 trace 로 다시 셈**(A1 62 · 32 · 20 · 59 · A2 56 중 38 · offered 10 · no 8 · U-5 (a) 56/56 · A3 짝 조회 0 행 꼴 · A4 Q13 · 키 갈래 입구 41 · 값 706 · 층 173 · BR5 464→34 등) — 다르면 세는 식까지.
3. 새 규칙이 **문항 맞춤이 아니라 일반 규칙**인지(37 밖 draft 48 꼴에서도 서나) · 「빠짐없이」 · 「묻지 않은 것 안 붙임」(KD10 · KD9 가 묻지 않은 정보를 붙이는 쪽으로 가지 않나 — asked_only) · 「LLM 에는 필요한 칸만」 · 「앱이 답 문장을 짓지 않음」 과 부딪치지 않나.
4. A3 원인 다시 읽음(깊이 → 짝 조회의 끝) · PR · BR6 · EN1 · SD1 · KD11 을 writer 가 끌어낸 것(변경 기록 0.6.0 끝 5 줄)이 결정 없이 들어간 동작인지 — U-5 에 묶은 것이 맞나.
5. U-5 ~ U-8 추천이 원칙과 맞나 · 그 밖에 숨은 사용자 결정 0.
6. 부록 A 헤더 대조 · 공개 grep.
7. **최종**: PASS 면 「U-5 ~ U-8 정해지면 구현 진행 가능」 명시.

산출: `$W/review-spec-v06.md` 1개만.
