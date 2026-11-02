# [reviewer] 고도화 — SPEC-008 v0.6.0 · SPEC-010 · WORK-012 검수

너는 **strong-hajin `reviewer` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance/AGENTS.md`

경로 약어: `P/` = `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/summer-star/strong-hajin/` · `W/` = `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/work/strong-hajin-enhance/` · 코드 `C/` = `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance/`(origin/main `f0ad522`)

## 0. 이것은 검수다 — 읽기 전용

판정(PASS / WARN / FAIL)과 근거만 낸다. 문서·코드를 고치지 마라. 산출물은 리포트 한 장.

## 1. 검수 대상

- `P/20-spec/spec-008-external-channels.md` (v0.6.0 개정 — v0.5.1 대비 `git -C <docs 워크트리> diff` 로 바뀐 곳)
- `P/20-spec/spec-010-meeting-ax-enhance.md` (신설)
- `P/30-work/work-012-enhance.md` (신설)

근거: `P/10-decision/decision-009-enhance.md`(**결정 정본** · OQ 전부 닫힘) · `P/00-baseline/baseline-008-enhance-improvements.md` · `P/improvements/SH-IMP-0NN-*.md` · `W/be-survey-report.md` · `W/fe-survey-report.md` · 코드 `C/`

## 2. 물음

1. **결정 대응** — DEC-009 의 결정 D-n · 닫힌 OQ 가 SPEC 어느 절에 빠짐없이, **뒤틀림 없이** 들어갔나(문구·값·기본값 표시). 빠진 것·다르게 적힌 것을 표로
2. **발명** — SPEC·WORK 에 DEC/원료에 없는 결정·수치·필드가 들어갔나
3. **범위** — 범위 밖(019 · 013① · 008 자동 추천 · 업무 업데이트 추천)이 들어가지 않았나
4. **계약 충돌** — SPEC-008 의 바뀐 절이 남은 절(특히 원격 이미지 · 메시지함 조회 전용 · 첨부 받기 · 실시간 사건)과 모순되나. DEC-008 을 뒤집은 자리가 표시됐나
5. **WORK Code Surface 전수** — WORK 가 적은 「닿는 곳」 을 **네가 직접 grep 해 다시 세어라**(최소: AX 참고 자료 `resource_type` 나열 지점 · 메시지함 다운로드 입구 · `timeout_seconds` 를 쓰는 호출 · `next_meeting_after`·기한 계산 호출 · 안건 `source` 를 정하거나 그리는 곳 · `integration.changed` 를 내는 곳 · 회의 수정·Connect PUT 경로 · `meeting.info.update` 계약 나열 지점). 개수가 다르면 FAIL — 빠진 파일:줄을 적어라
6. **Phase 실행 가능성** — Phase 마다 선후(BE 계약 고정 → FE) · 검증 명령(코드 레포 Makefile 타겟) · 앱 기준 Done Criteria 가 있나. 사용자 E2E 체크리스트가 **데스크톱 앱** 기준인가
7. **사람 눈에 이상해 보일 자리** — 계약은 맞는데 실물에서 사용자가 걸릴 자리(예: 보정 표가 비었을 때 · 회의실 조회 실패 중 저장 · 맥락 100줄 경계가 날짜 구분선과 겹칠 때)를 모아라

## 3. allowed_paths

- `W/review-spec-work-report.md` ← **이 파일 하나만 만든다**

## 4. 하지 말 것

- 문서·코드 수정 · 테스트·빌드·서버 실행 · 운영 접속 금지
- 실명·메일 금지

## 5. 리포트 형식

```
# 검수 — SPEC-008 v0.6.0 · SPEC-010 · WORK-012
## 0. 판정 (PASS/WARN/FAIL) + 한 줄
## 1~7. 물음별 — 항목마다 판정 · 근거(파일:줄) · 고칠 것
## 8. FAIL 목록(writer 재발주용) · WARN 목록
```

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디handle 은 세션 재연결로 바뀐다 — 확실하지 않으면 코디에게 [질문] 으로 묻지 말고 preamble 값을 따르라.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_367ca23a-f846-44c0-afc7-07b6655df214 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: SPEC·WORK 검수 <판정>" \
  --body "리포트 경로 / 판정 / FAIL n · WARN n"

# (2) 직접 주입
orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 \
  --text "[worker_done] reviewer SPEC·WORK 검수 <판정> — FAIL n · WARN n. 리포트 review-spec-work-report.md" --enter
```

- 막히면: `orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 --text "[질문] reviewer: <질문>" --enter`
