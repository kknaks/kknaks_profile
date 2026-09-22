# [reviewer] SPEC-004 검수 — 계약이 DEC-003 과 실제 코드를 견디는가

너는 **strong-hajin `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar` (코드 — **읽기 전용 검증용**)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

> ⚠ **read-only.** 코드도 문서도 한 줄 고치지 마라. 산출물은 리포트 하나뿐이다.
> ⚠ 고칠 것을 발견해도 **고치지 마라.** 판정과 근거만 낸다. 수정은 원 워커에게 재발주된다.

## 1. 검수 대상

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-004-calendar-scheduling.md` (1209줄) ← **이것을 검수한다**
- `…/20-spec/README.md` 의 SPEC-004 추가분

### 기준 문서 (이것들이 옳다. SPEC 이 이것들을 어겼는지를 본다)

- `…/10-decision/decision-003-calendar.md` ← **계약의 SoT.** 채택 A~J · **증보 K1~K4** · 기각 · 보류
- `…/00-baseline/baseline-003-calendar.md` ← 입력·관측. R1~R9 와 「조사가 뒤집은 전제 둘」
- `…/20-spec/README.md` § **Data / Domain Boundary** ← spec 에 둘 것과 두지 않을 것의 경계
- `…/20-spec/spec-003-task-lifecycle-v2.md` ← 형식의 본보기
- `orchestration/work/strong-hajin-calendar/be-survey-report.md` · `fe-survey-report.md` ← 조사 사실

**전제 정정을 놓치지 마라** (DEC-003 머리말): 시안은 **레이아웃 정본**이고 **기능·모달 항목·
데이터·상태 어휘는 우리 것**이 정본이다. 디자이너가 없어 DS-gaps 는 우리가 만든다.

## 2. 무엇을 보나 — 여섯

### 2-1. DEC-003 채택 A~J · 증보 K1~K4 가 **전부** 내려왔나

빠진 항목이 있나. **뜻이 바뀐 채로** 내려온 항목이 있나. 특히:

- **§B 두 소멸 경로** — 기간 밖은 **쓰기**(`released_at`, 되돌릴 수 없음), 업무 종료는 **읽기**
  (조회 필터, 되돌아옴). 이 둘이 **섞이지 않았는지**를 본다. 섞이면 계약이 무너진다
- **§C** `COMPLETION_SUBMITTED` 는 **미완**이다 — 배정이 산다
- **§D** 가시성 「내 것만」
- **K1** 같은 날 재배정 = **시각 변경(같은 행 갱신)**. 닫는 사유는 **둘 그대로**
- **K2** `from`/`to` 가 오면 **구획도 커서도 없다**. 없으면 기존 동작 보존
- **K3** 닫힌 건수를 응답이 낸다
- **K4** 합본 조회가 조인해서 주최자 이름을 낸다. `/api/meetings` 는 안 건드린다

### 2-2. **SPEC 이 코드에 대해 한 주장이 참인가** — 이게 네가 코드 워크트리를 받은 이유다

SPEC 과 조사 리포트가 `파일:줄` 로 짚은 주장을 **직접 열어 확인하라.** 최소 이 넷:

- `policy.py:277` — 공유받은 회의가 무조건 `past` 로 가는가
- `application.py:1870-1883` — 회의 커서가 DB 커서가 아니라 **매 호출 전체 목록 재생성 + 선형탐색**인가
- `lifecycle.py:93-104` · `application.py:1296` · `work_tasks.py:1855`·`:2658`·`:2715` —
  상태 변경 경로가 조사가 적은 그대로인가
- `persistence.py:1015-1022` · `:1506-1515` — `released_at` + 부분 unique 선례가 그 모양인가

**틀린 주장이 하나라도 있으면 FAIL 이다.** 계약이 거짓 위에 서면 구현이 거기서 갈린다.

### 2-3. 경계 위반 — spec 에 두지 말아야 할 것이 들어왔나

`20-spec/README.md` § Data / Domain Boundary 기준. column·index·FK·ORM 모델·repository 구조·
lock 구현 상세가 본문에 있으면 **WORK 로 내려야 한다.**

### 2-4. **조용히 통과하는 자리** — 네 역할의 핵심

읽으면 말이 되는데 **구현자가 갈릴** 자리를 찾아라.

- **한 문장이 두 가지로 읽히는 곳.** 어느 쪽으로 구현해도 이 SPEC 을 안 어기는 곳
- **`(제안)` 표기의 오용** — §1 이 「확정을 구현 가능하게 만든 기술 표현」으로 정의했다.
  **확정이어야 할 것에 `(제안)` 이 붙어 있으면** 구현자가 바꿔도 된다고 읽는다. 그 반대도 본다
- **인수조건이 없는 계약 문장** — §6 이 그 문장을 어떻게 증명하는지 짚지 못하면 그 문장은 안 선다
- **에러 코드가 있는데 언제 나는지가 없는 것**, 또는 그 반대

### 2-5. 내부 모순

§2 UX Contract · §3 User Scenario · §4 Interface Contract · §5 Implementation Rules · §6 Verification
이 **서로 어긋나는 자리.** 특히 K1~K4 반영이 §2·§3·§4·§5·§6 다섯 곳에 걸쳐 들어갔으니
한 곳만 옛말인 자리가 있는지 본다.

### 2-6. 형식

`spec-003` 과 같은 절 구성·frontmatter 인가. links 에 BASE-003·DEC-003 이 있나.
`20-spec/README.md` 갱신이 맞나.

## 3. 판정

**FAIL** — 계약과 다른 것이 서 있다. 이대로 구현하면 틀린 것이 나온다
**WARN** — 물어야 할 만큼 모호하다. 구현자가 갈린다
**PASS** — 이대로 WP·구현으로 내려도 된다

지적마다 **`파일:줄` + 근거**. **근거 없는 지적은 쓰지 마라.** 취향은 지적이 아니다.
FAIL 과 WARN 은 **무엇을 어떻게 고쳐야 하는지**까지 적어라 — 원 워커에게 그대로 재발주된다.

## 4. allowed_paths

- **(read-only)** 코드도 문서도 수정·생성·삭제하지 않는다
- 쓰기가 허용된 파일은 **하나뿐**:
  `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-calendar/review-spec-004-report.md`

## 5. 범위 제약 — 하지 말 것

- **DEC-003 을 검수하지 마라.** 그것은 사용자·코디가 닫은 결정이다. SPEC 이 **그것을 따랐는지**만 본다.
  DEC-003 자체가 틀렸다고 보이면 지적이 아니라 **「코디 확인 필요」로 따로 모아라**
- **더 좋은 설계를 제안하지 마라.** 계약이 서는지만 본다
- 코드를 고치지 마라. 테스트를 돌리지 마라 (고친 게 없다)
- 시안을 기능 기준으로 쓰지 마라 — **레이아웃 정본일 뿐이다**

## 6. 검증

- 2-1 ~ 2-6 **여섯 항목이 모두** 답을 갖는다
- A~J · K1~K4 **전 항목 전수 대조표**가 리포트에 있다 (내려왔나 / 뜻이 맞나)
- 2-2 의 코드 주장 **넷을 실제로 열어 확인**했고 그 결과가 적혀 있다
- 모든 지적에 `파일:줄` 근거
- 판정이 **FAIL / WARN / PASS** 중 하나로 명확하다
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short` 가 비어 있다.
  출력을 리포트 끝에 붙여라

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a9d49810-1ce8-4885-8c5f-b93200c501ac --from term_a881668d-7491-4cca-b8a2-7dbdc04d6372 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
