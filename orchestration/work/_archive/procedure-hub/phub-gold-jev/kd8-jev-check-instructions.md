# [app] KD8 — Jev 정보 종류 판단 확인 (WORK 첫 WP · 작은 시험)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더)의 역할 · allowed_paths · 공개 레포 제약 · §9 완료 보고 그대로. 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(미커밋 위에 이어서 — 다른 워커 없음).

읽을 것: `SPEC-002-chat-eval.md`(0.5.1) §3-1 KD1 ~ KD8 · §3-2a(정보 종류 14 · 영어 이름 · 설명) · §9-3c 「정보 종류 하나만」 묶음 · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/para/resources/note/ai/llms.txt` · 기존 `clinic_chat/walk/select.py`(묶음 Noul 꼴 — 참고만).

## 할 것

- **허브 · LLM 없이 Jev 만** 부르는 스크립트(`clinic_chat/experiments/kd8_kind_check.py` 처럼 — 앱 본 코드는 바꾸지 마라).
- 질문 셋(로컬 파일 · gitignore 자리 — 문장 커밋 금지): (a) §9-3c 「정보 종류 하나만」 5 꼴(원리만 · 효과만 · 회복만 · 하위 목록만 · 상품만) (b) 종류 둘을 함께 묻는 꼴 5 (c) 종류를 짚지 않는 질문 3(「…뭐야」 · 「…뭐 해」 꼴) — 각 문항에 **기대 종류**를 함께 적는다. 문장은 일반 시술 이름으로 네가 초안(사용자 확정 대상 아님 — 실험용).
- 문항마다 Jev 한 요청: 14 종류 `kind_{k}` Noul(SPEC §3-2a 영어 이름 · 설명 · instructions 영어) + 대상 1 개는 state 에 고정(대상 판단은 이번 범위 밖).
- 재는 것: 물은 종류의 Noul 값 · 순위 · 1위인가 · yes(≥0.7)인가 · 묻지 않은 종류 가운데 yes 수 · 사이(0.3~0.7) 수 · 문항당 ms. **두 판**으로: ① state = 한국어 질문 그대로 ② state 에 영어 한 줄 풀이를 덧붙임 — 한국어 약점이 원인인지 가른다.
- 결과 표(문항 × 판)와 결론 한 줄: KD2 · KD3 본문 그대로 / KD3 을 「사이 값 상위 n」 으로(그 n 추천) / 둘 다 안 됨.
- 실물 Jev 호출은 이 시험 범위만(26 요청 안팎). ruff · 커밋 후보 grep. 결과 리포트는 `$W/kd8-jev-check-report.md`(W = 프로필 work 폴더 — 질문 문장은 넣지 말고 꼴 · 기대 종류 · 수치만).
