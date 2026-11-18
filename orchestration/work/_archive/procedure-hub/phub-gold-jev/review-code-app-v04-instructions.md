# [reviewer_code] 앱 코드 검수 — WORK-017 상담 0.4(소넷 입구)

**앞 판 맥락 없음.** `phub-gold-jev-review-code-app-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만(그 브리프의 옛 WORK · 「볼 것」 은 옛 판 — 아래가 앞선다 · 핸들은 preamble 값). 검수 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(HEAD be1c622 위 미커밋 변경 · **공개 레포**). **파일 고치지 마라 · stash · checkout 금지.**

## 읽을 것

계약 `SPEC-008-consult-entry.md` 0.2.0 · `WORK-017-consult-v04.md` · 지시서 `impl-chat-v04-instructions.md` · 검수 `review-work-016-017.md`(R-2~R-5) · `_RESUME.md` §2 맨 위 11-18 행 · 채점 `research-input-space/scripts/README.md` · 결과 `research-input-space/runs/v04-score` · `v04b-score`(summary.json · now-turns.jsonl).

구현 보고 요지: 켠 턴 = 목록 적재 → 소넷 이해 호출 하나 → 검증 → 객체 · 부위 거르개 → 조회 · 답 재료(걷기 결정론 함수 · Jev · resolve 맞춤 꼴 0) · 장부 consult.understand/site_filter · rev 4 · 옛 끈/rev3 대화 rev_changed · pick 0.4.0-draft · WORK 와 달리 받은 것(가짜 CLI 이해 길 조건 · VF11 을 VF6 앞 · offer_name 길 없음 · 거둠만 new 턴 화면 안 갱신 · site_index 캐시 키). E8 v04b: 3검사 93.8 · 8검사 86.9(문턱 95 · 90 미달) · 실패 44 = 이해 21 · 객체 13(sure=false → guess) · 조회 6 · 데이터 4.

## 볼 것

1. `git diff` + untracked 범위 — `walk/` · `columns/` 지운 줄 0 · 시험 앱 B 열 경로 동작 불변 주장 확인 · 켠 경로에 Jev · resolve 맞춤 꼴 부름 0(grep).
2. SPEC-008 0.2.0 계약 대조(LD · UC · VF · OU · QS · QM · DT · BQ · FL · 장부 · SSE · 프롬프트 적재기) — 특히 「WORK 와 달리 받은 것」 이 계약과 부딪히나.
3. **실패 44 턴 표본 15** 를 장부로 직접 보고 층 판정이 맞나 · 코드 결함(소넷 탓이 아닌 것)이 섞였나 — 「소넷 비결정 ±3.5%」 주장 근거 확인(v04 · v04b 같은 턴 비교).
4. 시험 — WORK §15 의 그 WP 시험 파일들만 직접 돌려라(전체 pytest 금지 · 외부 호출 0 파일만). 지운 시험이 계약 변경 몫인가 · 기대값이 계약에서 오나.
5. 실물: **18222 에 코디가 0.4 를 띄워 둠**(CHAT_STATE=on · DEBUG_PANEL=on · 허브 18105 = 0.8.1). 띄우거나 내리지 마라. 대화 2개만(조사 끼임 고민 「턱에 살이 너무 많아보여」 → 「사각턱인데?」 · 바꿔 말하기 「얼굴이 자꾸 빨개져요」) — curl 은 `--data-urlencode` · 대상 · 리스트 · 점 · 객체 패널을 보고.
6. 공개 레포 — 키 · 홈 절대 경로 · 내부 URL grep.

## 산출

`review-code-app-v04.md` 1개(같은 폴더). PASS/WARN/FAIL + 지적 표(파일:줄 · 심각도 · SPEC 절 · 고칠 방향) + 「문턱 미달 원인 가운데 코드로 고칠 것 / 프롬프트 몫 / 측정 몫」 3칸 표.
