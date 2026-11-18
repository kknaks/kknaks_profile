# WORK-011(앱) 작성 지시서 — SPEC-004 0.1.0 상담 채팅 1판 구현 계획

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더)의 역할 · 제약 · 검증 · 완료 보고 꼴 그대로(핸들은 preamble 값). allowed_paths = **`WORK-011-consult-chat.md` 새 파일 하나만**. 11-17 사용자 결정: Procedure Hub 데이터는 공개 정보 — 「회사 데이터 본문 0」 은 이 데이터에 걸지 않는다(비밀값 · 키 · 내부 URL 금지 그대로).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · 구현은 여기서 이어서 · 공개 레포)

## 읽을 것

1. `$W/_RESUME.md` §2 11-17 행 전부 — 특히 맨 위 세 행: **U-11~U-13 = (a)** · **상담 프롬프트 = JSON(`prompts/consult.json`)** · **SPEC-004 검수 뒤 코디 W-1~W-8**
2. `$W/SPEC-004-consult-chat.md` 전체 ← 계약
3. `$W/review-spec-004.md` WARN 8 · NOTE 7
4. `$W/research-chat.md`(근거) · 앞 WORK 꼴 `$W/WORK-009-v06.md`
5. 앱 코드 `$A/clinic_chat/` · `$A/prompts/` · `$A/README.md` · `$A/pyproject.toml`

## 쓸 것

- SPEC-004 절 ↔ WP 대응표(미대응 0) · 시험 T1~T18 · 실물 E0~E4.
- **프롬프트 JSON 반영(SPEC 과 다른 곳)**: CL2 의 `--system-prompt-file` → 앱이 `prompts/consult.json` 을 읽어 `system` 절을 이어 붙인 글을 `--system-prompt "<글>"` 로(지금 `cli.py:80` 꼴). JSON 꼴 = `version` · `system`(절 배열) · `jev_front` · `turn_headers` · `tail_marker` 등 앱 쪽 상담 프롬프트 전부 키로 · 장부 sha 는 JSON 전체(대화 시작 · 이 턴 둘 — W-4) · SDK 때 같은 JSON 의 `system` 을 쓰는 경계. 초안 표지는 `version` 칸으로. SPEC 되적기 후보로 §끝에 한 줄.
- 검수 반영 한 줄씩(W-1~W-8 · `_RESUME` 코디 행 그대로) · NOTE 7 처리.
- **첫 WP = E1 CLI 3턴 실측**(구독 · 회사 자료 없는 짧은 글 · `--max-turns 1` 받나 · 기억 이어짐 · 첫 글자 · cache 토큰 · 세션 파일 자리 · 다른 cwd 에서 resume(W-5) · 프롬프트 바꿔도 첫 턴 기록 유지(F7)) — 안 되면 멈추고 코디에게.
- 얼굴 SVG · 좌표표 WP: 손 SVG(밑그림 PNG 는 참고만 · 레포에 안 둠) · 부위 60 분류 · 좌표 초안은 워커 · **사용자 눈 확인은 코디가 화면으로**.
- 허브 의존: 고민 부위 코드는 SPEC-001 0.7(허브 · 별도 발주)이 낸다 — 그 전까지 앱은 그 칸이 없으면 점 없이 동작(라벨도 없음) · 허브 칸이 오면 켜지는 꼴로. 허브 몫은 WP 로 쓰지 않는다(필요한 계약만 한 줄).
- 실물: 코디 몫(18222 띄움 · 18105 는 지금 DB 판 · 사용자 e2e)과 워커 몫(18223 등 빈 포트에서 확인 후 내림) 갈라 적기. 18210 · 18005 · 18105 · 18220 금지.
- 완료 조건 · 검증 명령(ruff · pytest · grep) · 단계마다 그 WP 시험만 · 전체는 끝에 한 번.

## 검증

대응표 · WARN/NOTE 반영 줄 · 경로 실재 · 공개 grep(비밀값 · 키 0).
