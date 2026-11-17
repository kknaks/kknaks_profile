# [reviewer_doc] SPEC-001 · SPEC-002 초안 검수

너는 **procedure-hub `reviewer_doc` 워커**다(read-only). **앞 판의 맥락이 하나도 없다** — 아래 「읽을 것」만으로 일한다.
먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리(코디 워크트리 · 공유): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온`
**리포트 파일 1개 외에는 아무것도 만들거나 고치지 마라.**

## 1. SSOT — 먼저 읽을 것

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev` · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터)

- 검수 대상: `$W/SPEC-001-hub-gold-mcp.md` · `$W/SPEC-002-chat-eval.md`
- 정본: `$W/_RESUME.md` §2 결정 표 · `$W/phub-gold-jev-write-brief.md` §2(D 표 결정 상태) · §3(쓸 절)
- 근거: `$W/research-gold-connect.md` · `$P/para/resources/note/ai/llms.txt` · `$SM/gold/README.md` · `$SM/gold/semantic-map.md` · `$SM/gold/gold-build.py` · `$SM/gold/gold-check.py` · `$SM/gold/g_*.csv`(헤더 · 셈)
- 옛 코드(인용 확인용 · 읽기만): `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(`git show HEAD:`) · `~/git/PROCEDURE-HUB`(`git show origin/release/v1.2.0:`) · `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`

**기대는 개념**
- `$P/para/areas/concept/cs/artifact-traceability.md` — 응답 행이 gid → g_evidence → silver → source_ref 로 되짚히는 계약인지

## 2. 무엇을 보나

1. **결정 일치** — `_RESUME §2` · 브리프 §2 의 결정과 어긋나는 곳(특히 DB 없음 · repository 교체 경계 · CLI 구독 · Sonnet/Haiku · 3열 · stg 는 로컬 시험까지 · 37 은 표본 · 범위 밖 종료).
2. **근거 없는 정책** — 근거(결정 · 리포트 절 · 파일:줄) 없이 정한 것. 「제안」 · 「열린 것」 으로 표시됐으면 정상.
3. **인용 실물 확인** — 파일:줄 인용 중 **표본 15개 이상**을 실제로 열어 맞는지. 숫자(행 수 · 셈)는 표본 5개 이상 직접 다시 센다.
4. **계약 완결성** — SPEC-001 도구 8 이 SPEC-002 B · C 열 걷기와 37 문항 경로를 닫는지(조사 §5-2 「읽을 gold 표」 열 대조). 도구 출력 필드가 CSV 헤더와 같은지(부록 A 를 스크립트로 다시 대조).
5. **llms.txt 일치** — SPEC-002 Jev 요청 꼴(후보마다 Noul · answer_ready · Choice 는 하나 고를 때만 · 후보는 허용 관계에서만 · 종료는 앱 검증).
6. **채점 공정성** — 답 키 · 「원장 오류 따라감」 · 점수 두 벌 · 가리기가 3열에 같은 조건인지.
7. **열린 것 목록** — SPEC-001 O-1~O-11 · SPEC-002 O-1~O-14 가 실제로 결정 안 된 것만인지, 빠진 열린 것은 없는지. 특히 SPEC-001 O-1(gold 15표만으로 3단 계층 펼침이 안 닫힘) 주장을 gold 데이터로 확인.
8. **공개 레포** — 회사 데이터 본문(시술 설명 · 원장 문장 · 답 원문 · 가격 값 · 질문 문장) · 비밀값 · 내부 호스트/URL · 실명 0(grep 명령과 결과).

## 3. 계약

해당 없음(검수).

## 4. 산출

- `$W/review-spec-001-002.md` 1개: 머리에 **판정(PASS / WARN / FAIL) 문서별** + 지적 표(번호 · 문서:줄 · 심각도 FAIL/WARN/NOTE · 무엇 · 근거 파일:줄 · 고칠 방향). 확인한 인용 표본 목록과 결과. 다시 센 숫자 목록.

## 5. allowed_paths — 이 밖은 건드리지 마라

- 쓰기: `$W/review-spec-001-002.md` **1개만.** 그 밖은 읽기 전용. 임시 파일은 네 세션 scratchpad 에만.

## 6. 진행

1. 읽을 것 → 2. §2 의 1~8 순서로 대조 · 셈 → 3. 리포트.

## 7. 범위 제약 — 하지 말 것

- SPEC 을 고치지 마라(지적만). 결정을 새로 만들지 마라.
- 외부 API 호출 · `.env` 열기 · 서버/docker 띄우기 · 코드 레포 작업 트리 변경 · fetch 금지.
- 리포트에도 회사 데이터 본문을 싣지 마라(코드 · 칸 이름 · 셈 · 질문 id 까지).
- 「더 좋게 하려면」 수준의 취향 지적은 NOTE 로만. FAIL 은 결정 위반 · 근거 없음 · 인용 틀림 · 계약 구멍 · 공개 레포 위반.

## 8. 검증

```
DEC · SPEC · WORK 를 _RESUME 결정 · 조사 리포트 · 코드에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 끝내기 전 `git -C $P status --porcelain` 로 네 변경이 리포트 1개뿐인지 확인(폴더가 미추적이면 `ls -la $W` 로 새 파일 확인).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_95e86b96-831a-4d31-aa96-58649a80d244 --from term_9791c1ee-940d-4044-b82c-7b1c706b7887 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
