# [writer] 고도화 1판 — BASE-008(입력 눕히기) · DEC-009(결정) 작성

너는 **strong-hajin `writer` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 문서 규칙: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/project.md` · 각 폴더 `README.md`(`00-baseline/` · `10-decision/`)
- **모양의 본보기**(바로 앞 판): `para/projects/summer-star/strong-hajin/00-baseline/baseline-006-external-channels.md` · `10-decision/decision-008-external-channels.md` — 머리(frontmatter)·읽는 규칙·표기·절 구성을 이대로 따른다

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2` (코디 워크트리에 직접 탄다)
경로 약어: `P/` = `para/projects/summer-star/strong-hajin/` · `W/` = `orchestration/work/strong-hajin-enhance/`

⚠ **코디와 같은 트리다.** 아래 allowed_paths 의 파일만 만든다. 다른 파일(특히 `improvements/` · `_RESUME.md` · index·log)은 **읽기만** 한다.

## 1. SSOT — 원료 (여기 없는 것은 발명하지 마라)

| 원료 | 무엇 | 경로 |
|---|---|---|
| 개선 목록 | 항목 19건(SH-IMP-001~019)의 문제 · **사용자 정리 · 결정 · 조사 결과** — 이 판의 정본 | `P/improvements/README.md` · `P/improvements/SH-IMP-0NN-*.md` |
| 결정 요지 표 | 날짜별 사용자 결정 한 줄씩 | `W/_RESUME.md` §2 |
| BE 조사 | 서버 코드 현재 동작 · 메디니스 대조(§5.7) | `W/be-survey-report.md` |
| FE 조사 | 화면·셸 현재 동작 · 다운로드 입구 표 · 메일 이미지 규칙 | `W/fe-survey-report.md` · 추가 지시 `W/fe-survey-add1-instructions.md` |
| 이전 입력 | 회의 생성·편집 피드백 4건(이 판이 넓힌다) | `P/00-baseline/baseline-007-meeting-creation-improvements.md` |
| 뒤집을 결정 | 「메시지함 = 조회·읽음, hover 행동 막대 없음」 · 2단계(AX 판단) 미룸 | `P/10-decision/decision-008-external-channels.md` |

**기대는 개념** — 해당 없음(이 판은 결정 기록이다).

## 2. 배경

운영(`https://ax.medisolveai.xyz`)과 데스크톱 앱(medi-ax)을 쓰며 나온 개선 19건을 사용자와 하나씩 논의해 방향을 정했고, BE·FE 조사와 코디의 운영 DB·로그 확인으로 원인을 확정했다. 이 판은 그것을 **BASE(입력) → DEC(결정)** 두 문서로 굳힌다. 다음 판이 SPEC(SPEC-008 개정 · 새 SPEC-010)과 WORK-012 를 쓴다 — **이 판에서는 SPEC·WORK 를 쓰지 않는다.**

**범위**: SH-IMP-001~018. **019(화자 분리)는 보류** — BASE 에 관찰만 남기고 DEC 에서 「이번 범위 밖」 으로 적는다. 009 는 완료(운영에서 해결) — 관찰만. 013② ③ 은 사용자 Mac GUI 확인(결정 아님). 013 ① 이름 없는 방은 **사용자가 정하지 않았다 → 이번 범위에서 뺀다**.

## 3. 만들 것

### 3-1. `P/00-baseline/baseline-008-enhance-improvements.md` — BASE-008

- **판단하지 않는다.** 항목별로 (사용자) 관찰 · (조사) 현재 코드 동작 · (운영) DB·로그 확인을 눕힌다. 근거 표기는 BASE-006 의 「읽는 규칙」 방식(표기 표 + 리포트 목록과 한계)
- 항목은 SH-IMP 번호로 묶는다. 각 항목: 문제 · 화면/운영 근거 · 조사가 확인한 현재 동작(리포트 절 번호로 인용) · 메디니스 대조(006·019)
- BASE-007 과의 관계: BASE-007 의 네 건(001~004)을 이 판이 이어받는다고 적는다(BASE-007 파일은 고치지 마라)
- 가린 것: 사람 실명·메일·토큰 금지(「팀원 A」·「사용자」). 운영 회의는 제목 대신 「10-07 주간 회의(id 앞 8자리)」 정도로

### 3-2. `P/10-decision/decision-009-enhance.md` — DEC-009

- 상태 `accepted` (사용자가 항목별로 이미 결정했다). 결정마다 **D-01, D-02 …** 번호 · 근거(사용자 날짜 · 조사 절) · 「기본값(코디 제안)」 인 것은 그렇게 표시 — 아래가 그 목록이다
  - 005 「불러오기는 시간을 안 가져온다」 · 006 「취소된 업무도 맥락 목록에서 뺀다」 · 006 「보정 표를 회의록 화면 끝에」 · 003 「기존 회의실을 새 조건에서 못 쓰면 비활성 + 이유」 · 015 「스레드 답글이면 스레드 전체, 100줄 미만이면 있는 만큼」(이건 사용자 확인됨 — 기본값 아님) · 008 「단추 위치 [업무 생성][요약] 이 [답장] 앞」
- **뒤집는 결정**은 DEC-008 의 해당 줄을 인용하고 「~~DEC-008 D-n~~ → DEC-009 D-m」 로 적는다(DEC-008 파일은 고치지 마라): hover 행동 막대 없음 → 있음(015) · 2단계 AX 판단 미룸 → 메일만 수동 먼저(008) · 원격 이미지 처리(018 — SPEC-008 원격 이미지 절과 사용자 결정 10-06 「자동·프록시」 위에 SVG 허용)
- **계약 조문(필드·엔드포인트·테이블)은 쓰지 않는다** — DEC-008 머리말과 같은 선을 지킨다. 「무엇을 채택·버리나」 까지
- 끝에 **「이번 범위 밖」** 절: 019 · 013 ① · 013② ③(GUI 확인은 결정 아님) · 008 자동 추천(다음 단계) · 업무 「업데이트」 추천 · 012 은 범위 안(나간 방 이벤트)
- 끝에 **「WP 묶음(제안)」** 절 — 사용자 승인됨: WP1 운영 버그(002/004 · 005 · 006 기한 · 014 · 018 · 010) → WP2 회의록 생성 고도화(006) → WP3 AX 흐름(017 · 001 · 003/016) → WP4 메시지함→AX(015 · 008 · 012) · 셸 dmg 묶음(011 + 013② ③ 확인). 순서만 적고 Phase 상세는 WORK 몫
- Open Questions: 남은 미결이 있으면 OQ-901~ 로. **추측으로 메우지 마라** — 원료에 결정이 없으면 OQ 다

## 4. 먼저 읽을 핵심

- `P/improvements/` 의 각 항목 「사용자 정리」·「결정」·「동작」·「조사 결과」·「원인 확정」 절 — 결정의 정본
- `W/be-survey-report.md` §0 · `W/fe-survey-report.md` §0 — 한 줄 요약

## 5. allowed_paths — 이 밖은 건드리지 마라

- `P/00-baseline/baseline-008-enhance-improvements.md` (새로 만든다)
- `P/10-decision/decision-009-enhance.md` (새로 만든다)

index(`README.md`)·`log.md`·`improvements/`·`_RESUME.md` 는 **고치지 마라** — 코디가 한다. 커밋·push 금지.

## 6. 단계

1. 원료 전부 읽기 → 2. BASE-008 → 3. DEC-009 → 4. 자체 점검(아래 §8)

## 7. 하지 말 것

- SPEC·WORK 를 쓰지 마라. 코드 레포를 고치지 마라(읽기는 된다)
- 원료에 없는 결정·수치를 만들지 마라. 원료끼리 어긋나면 OQ 로 올리고 보고에 적어라
- 운영 서버·DB 에 접속하지 마라

## 8. 검증

- 두 파일이 있다 · frontmatter 가 본보기와 같은 키를 갖는다 · `links` 가 서로를 가리킨다(BASE-008 ↔ DEC-009 · DEC-008 · BASE-007)
- SH-IMP-001~018 이 BASE·DEC 둘 다에 빠짐없이 나온다(019 는 범위 밖으로) — **개수를 세어 보고에 적어라**
- 위 §3-2 의 기본값 여섯이 「기본값」 으로 표시됐다
- `git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2 status --short` 에 두 파일만 새로 생겼다(코디의 다른 변경은 원래 있던 것)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디handle 은 세션 재연결로 바뀐다 — 확실하지 않으면 코디에게 [질문] 으로 묻지 말고 preamble 값을 따르라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_367ca23a-f846-44c0-afc7-07b6655df214 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: BASE-008 · DEC-009" \
  --body "파일 경로 / 결정 개수 · 뒤집은 결정 · 기본값 표시 / 항목 개수 대조 / OQ"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 \
  --text "[worker_done] writer BASE-008 · DEC-009 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
