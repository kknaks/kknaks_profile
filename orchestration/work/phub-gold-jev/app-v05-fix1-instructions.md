# [app] v05 앱 수정 1

**너는 앞 판의 맥락이 없다.** /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/phub-gold-jev-app-brief.md 의 역할 · allowed_paths · 공개 레포 제약 · §9 완료 보고 그대로. 문서는 전부 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev 에 있다. 워크트리 /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev(미커밋 위에 이어서).

읽을 것: /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-code-v05-app.md(WARN 4 · NOTE 9 · §6) · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/WORK-006-app-v05.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md(0.5.1).

할 것:
- **W-1**: 읽을 종류가 0 이 되면(적용 가능한 종류가 하나도 없음) **KD6 기본 묶음**으로 읽는다(리뷰 추천 · 실행 중단 대신). 재현 시험.
- **W-2**: 부위 입구가 둘 이상이면 **부위마다 조회를 나눈다**(사건 · 조건과 같은 식 · concern_candidates 의 site 도) · unused 까닭 바로잡기. 시험.
- **W-3**: 37 문항 세트 칸 `expected_entries` 를 명세 `calls/<id>.json` 의 entries 로 결정론 채움(그 밖 빈 문항은 리뷰 고칠 방향대로) · 보고서 대상 일치가 37 에서 잡히는지.
- **W-4**: README 세 자리.
- **코디 발견 — C 열 토큰 0**: 화면 속도 탭으로 돌린 C 열 기록의 `tokens.llm` 합이 0 · 입력 KB 0(run 3271c805eb65 · c817dcce3fd4 · 02c3ea42989b). C(와 A)의 토큰 · 입력 크기를 stream-json 의 usage 로 채운다(도구 왕복 합). 속도 표 · 카드에 C 토큰이 나오게.
- **N-5**: 묶음 머리의 `table`(gold 표 이름)을 LLM 에 보내지 말고 기록에만(「LLM 에는 필요한 칸만」). **N-2**: 입구 고르기 `entry.by` 값 이름을 SPEC 대로 `noul`. 나머지 NOTE 는 안 고침 · 이유.
- 실물: 18221 속도 탭 API(effort low · 동시 · 허브는 18105 — 코디가 새 코드로 띄워 둠)로 「써마지 효과가 뭐야?」 「팔자주름에 뭐 해?」 B · C 1회씩 → C 토큰 · 입력 KB 가 0 이 아닌지 · B 결과 같은지. 18220 · 18105 · 18106 은 코디 것.
- ruff · pytest · 커밋 후보 grep.
