# [reviewer_code] 앱 코드 검수 — WORK-002 구현(clinic_chat)

너는 **reviewer_code 워커**다(read-only). **앞 판의 맥락이 없다.** 역할 문서(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/reviewer/role.md`(+ 같은 폴더 파일).

검수 워크트리: `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(branch `kknaksss/phub-gold-jev` · base `origin/main` · **공개 레포** · 커밋 없음 — 변경은 작업 트리에만). **파일을 고치지 마라 · stash · checkout 금지 · `.env` 열지 마라.**

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev`

## 읽을 것

- 계약: `$W/SPEC-002-chat-eval.md`(0.4.1) · `$W/SPEC-001-hub-gold-mcp.md` §4 · `$W/WORK-002-app.md`(0.2.0) · `$W/_RESUME.md` §2 · `$P/para/resources/note/ai/llms.txt`
- 구현 보고: `$W/app-report.md`

## 볼 것

1. 범위 · **공개 레포** — `git status --porcelain --ignored` 로 커밋될 것 / gitignore 된 것. 커밋될 파일에 키 · 회사 데이터 본문(질문 문장 · 답 · 원장 · gold 값 · 시술 이름) · 홈 절대 경로 0(grep 명령 · 결과). 세트 · 답 키 · runs 가 gitignore 자리에만.
2. **원칙** — B 걷기에서 폭이 Jev 점수 · 상한 · 상위 N · 잘라 내기 · 칸 빼기로 줄어드는 자리 0 · 종료 = 폭 다 읽음 + 깊이 판단 끝 + 검사 · answer_ready 단독 종료 없음 · **묻지 않은 안전 정보를 붙이는 자리 0** · Jev 는 앱이 펼친 선택지 안에서만(Choice 는 하나 고를 때만 · 후보 관련성 = Noul fan-out).
3. **SPEC-002 대조** — RG1~RG8 · 입구 고르기 · FT1~FT5 · K1~K5 · 종료 상태 6 · 세 상태에도 단계 ⑤ · 세 열 같은 조건(질문 · 모델 · 답 지시) · 채점 D1~D9 · 가리기 · 미확인 키 채점 금지 · 합성 키 배관.
4. 구현 보고 미결 ①~⑤ 판정: ① 추론 끔 불가 → `--effort low` 기본(O-23 (b))이 SPEC · 결정과 맞나 ② Q10 「상태 안 맞음」 원인이 SPEC 구멍인지 구현 문제인지(facets package 상위 고민 펼침 · SPEC-001 · SPEC-002 해당 절) ③ Q25 표본 3/6 ④ **resolve 짧은 조각이 긴 조각 안이면 뺌 — SPEC 에 없는 동작 = 폭을 줄이는가**(입구가 빠지면 원칙 위반) · 패키지 이름 raw_ledger ⑤ draft 문항.
5. 시험 — 직접 한 번: `uv sync` · `uv run ruff check .` · `uv run pytest -q`(실호출 없음). **실호출 금지**(Jev · claude 를 부르지 마라 — 실물은 코디 몫). 허브 18105 는 코디가 띄워 둔 것 — 띄우거나 내리지 마라(GET 몇 번은 됨).
6. 「사용자가 e2e 에서 만날 자리」(README 실행 안내가 실제로 따라 할 수 있나 · 결과를 어디서 보나 · 헷갈릴 출력)를 따로 모아라.

## 산출

`$W/review-code-app.md` 1개만. 판정 PASS/WARN/FAIL + 지적 표(파일:줄 · 심각도 · 근거 SPEC 절 · 고칠 방향).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from term_a6fd24aa-4db0-4914-803d-0bf77d4e7678 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_code 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] reviewer_code 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 --text "[질문] reviewer_code: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
