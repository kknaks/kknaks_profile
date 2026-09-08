# [architect] 회의록 계약을 흐름 결정 31건에 맞춘다

너는 **task-management `architect` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (문서 레포 · 코디 워크트리)

---

## ⛔ 0. 정본은 하나다

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md
```

**이 문서가 정본이다.** 사용자가 흐름을 단계별로 짚으며 닫은 결정 31건이 `MF-1 ~ MF-63` 번호로
들어 있고, `§0 결정 번호표` 가 목록이다. 본문은 `§1 회의 시작` · `§2 회의 중` · `§3 회의 종료` 에 있다.

**지금 SPEC·DEC·ERD 는 옛 설계 그대로다.** 네 일은 **계약을 이 결정에 맞추는 것**이다.

### 판정 규칙

| 무엇 | 정본 |
|---|---|
| **흐름·동작** — 무엇이 언제 일어나나 | **`Meeting flow.md` (MF-n)** |
| **기능** — 어떤 화면·필드·상태가 있나 | 기획 BASE-003 + 정책 DEC-003 |
| **시각** — 색·크기·간격 | 디자인 시스템 + 시안 |

**`Meeting flow.md` 와 기존 SPEC 이 부딪히면 `Meeting flow.md` 가 이긴다.** 그게 나중 것이다.

### 하지 마라

- **결정을 새로 만들지 마라.** MF 번호에 없는 것을 네 판단으로 정하지 않는다
- **시안을 판정에 넣지 마라.** 시안에 있는데 MF·기획·정책에 없으면 만들지 않는다
- **「나중에 정한다」로 남기지 마라.** 정말 못 정하는 것만 OQ 로 올린다 —
  **OQ 마다 「어디를 찾았는데 없었나」를 근거로 달아라.** 근거 없는 OQ 는 반려한다
- **수치를 사용자에게 묻지 마라.** DEC-003 L141 이 「수치는 spec 에서 정한다」로 이미 위임했다

---

## 1. 산출물

**고칠 문서 (새로 만들지 않는다)**

```
para/projects/summer-star/task-management/10-decision/decision-003-meeting-notes.md
para/projects/summer-star/task-management/20-spec/spec-006-meeting-setup.md
para/projects/summer-star/task-management/20-spec/spec-007-meeting-live.md
para/projects/summer-star/task-management/20-spec/spec-008-meeting-close.md
para/projects/summer-star/task-management/40-architecture/  (ERD · backend · frontend 중 해당분)
```

**끝나면 `orchestration/work/docs-v1/docs-v1-meeting-reflow-report.md` 에 보고한다.**
MF 번호마다 「어느 문서 어느 절을 어떻게 고쳤는지」를 표로. 안 고친 것이 있으면 이유를 적어라.

---

## 2. 반영할 결정 31건

`Meeting flow.md` 를 **직접 읽어라.** 아래는 어느 문서가 걸리는지의 지도일 뿐이다.

### 회의 시작

| MF | 무엇 | 걸리는 문서 |
|---|---|---|
| MF-1 | `/start` 는 전이만. 웜스타트는 **큐에 넣고 즉시 응답** | DEC-003 §STT · SPEC-006 §4 · backend README §7(W-1 해소) |
| MF-2 | AI 도구는 **API 래퍼 7개**. DB 직결 아님 | DEC-003 §8 · SPEC-007 §4 |
| MF-3 | 못 쓰게 하는 것은 **codex 설정 allow list** 로 잠근다 | DEC-003 §8 · architecture/system |
| MF-4 | 회의마다 **단명 토큰** 발급 → 헤더 주입 → 마감 시 폐기 | architecture/system · SPEC-007 §4 |
| MF-55 | **용어 다섯의 뜻**(안건이 뼈대 · 넷이 파생)을 웜스타트로 준다 | DEC-003 §8 · SPEC-007 §4 |

### 회의 중

| MF | 무엇 | 걸리는 문서 |
|---|---|---|
| MF-49 | 배치 트리거 **확정 발화 1000자** (600 에서 올림) | DEC-003 §STT · SPEC-007 §4 |
| MF-50 | 배치는 **발화만** 넘긴다. 안건·줄·업무·유형은 **툴로 조회** | DEC-003 §4 · SPEC-007 §4 |
| MF-51 | `list_agendas()` 는 **사람 안건 + AI 안건**을 다 준다 | SPEC-007 §4 |
| MF-53 | 배치는 **증분만 넣고 AI 트랙 전체를 다시 낸다** (세션이 앞 발화를 기억한다) | DEC-003 §4 · SPEC-007 §4 · ERD |
| MF-9 | 줄에 시각을 안 붙인다 — **안건에만** | SPEC-007 U-2·U-4 · SPEC-008 U-3 |
| MF-10 | 슬래시 명령어 **5개**(`/논의 /결정 /업무 /액션 /새안건`). **그 밖은 전부 그냥 텍스트** | SPEC-007 U-3 |

### 회의 종료

| MF | 무엇 | 걸리는 문서 |
|---|---|---|
| MF-37 | 종료 후 **async 재전사**(`stt-async-v5`) — 화자 분리를 바로잡는다 | DEC-003 §4·§6 · SPEC-008 §4 · integrations |
| MF-56 | **최종 배치와 통합 단계를 없앤다.** 호출 한 번으로 최종 회의록을 만든다 | DEC-003 §1·§4 · SPEC-008 §4 |
| MF-57 | 최종 회의록은 **AI 가 쓴다** — 사람이 적은 줄도 다듬는다(오타 교정) | DEC-003 §1 · SPEC-008 §4 |
| MF-58 | 재전사 실패에 **fallback 없음** — 「다시 시도」 하나 | DEC-003 §7 · SPEC-008 |
| MF-59 | 최종 회의록의 액션·업무 줄에 **DB 에 바로 넣을 페이로드**를 담는다 | SPEC-008 §4 · ai_schemas · ERD |
| MF-52 | 출력 스키마는 **한 벌**. 페이로드만 nullable — 증분은 null | SPEC-007·008 §4 · ai_schemas |
| MF-54 | **STT 용어 보정** — ① Soniox `context` 로 미리 주고 ② 최종에서 AI 가 **매핑표**를 만든다 | DEC-003 §6 · SPEC-008 · ERD |

### 편집 · 정리

| MF | 무엇 | 걸리는 문서 |
|---|---|---|
| MF-60 | **줄 종류는 편집에서 못 바꾼다** | DEC-003 §5 · SPEC-008 U-6·U-7 |
| MF-61 | 사람이 적은 액션·업무 줄은 **빈 드로어**로 연다 | SPEC-008 U-10 |
| MF-62 | 안건은 **제목만 고친다. 삭제는 없다** | SPEC-008 U-7 |
| MF-13 | 「업무 생성」 = **업무 탭의 새 업무 드로어** + 안건 셀렉터 | SPEC-008 U-10 · SPEC-003 U-1 |
| MF-14 | 「업무 갱신」 = **업무 상세 드로어**. AI 변경분이 반영된 채로 뜬다 | SPEC-008 U-9 · SPEC-003 U-8 |
| MF-21 | `work_type.description` **추가** — 업무 설정에서 등록할 때 적는다 | DEC-001 §3 · SPEC-002 · ERD |
| MF-25 | 카운트는 **최종 회의록 기준** — 안건·논의·결정·액션·업무 | SPEC-008 U-1 |
| MF-36 | 줄을 지운 자리는 **그대로 둔다** (뒤 줄을 당기지 않는다) | ERD M-20 · SPEC-008 §4 |
| MF-63 | 확인 모달 **420 폭 · 한 문장**. 600 은 무거운 것에만 | frontend README §6 |

### 목록 · 상세

| MF | 무엇 | 걸리는 문서 |
|---|---|---|
| MF-5 | 미리보기 CTA 를 **상태별로** — scheduled·recording 「회의 입장」 | SPEC-006 U-8 |
| MF-6 | 미리보기 패널은 **빈 상태 크기에 고정** · 넘치면 패널 안 스크롤 | SPEC-006 U-6·U-8 |
| MF-7 | breadcrumb 은 **링크** + 상세에 「←」 — **전 화면 공통** | frontend README · SPEC-003·004·006·008 |
| MF-8 | 상세 헤더를 **업무 헤더 순서**(배지 줄 → 제목)로 | SPEC-008 U-3·U-4 · SPEC-006 U-4 |

---

## 3. ⛔ 크게 바뀌는 것 넷 — 여기를 놓치면 전부 틀린다

```
① 최종 배치와 통합이 사라진다 (MF-56)
   전   /end job = ① 마지막 배치 → ② 통합(참조 id 만 내고 서버가 본문 복사) → ended
   후   /end job = ① async 재전사 → ② **최종 회의록 한 번** → ended

   「모델은 구조만 내고 본문은 서버가 복사한다」는 통합 규칙이 **없어진다**(MF-57).
   그 규칙에 딸린 검증(참조 존재 확인)도 자리가 바뀐다 — 어디로 가는지 네가 정해서 적어라

② 배치가 컨텍스트를 안 받는다 (MF-50)
   전   payload = transcript + humanAgendas + humanLines + aiAgendas + taskWhitelist
   후   payload = **transcript 하나**. 나머지는 AI 가 툴로 조회한다

   `taskWhitelist` 가 payload 에서 빠져도 **서버의 사후 검사는 남긴다** —
   목록 밖 업무를 가리키면 강등하는 그 로직이다

③ 배치가 매번 AI 트랙 전체를 낸다 (MF-53)
   전   INSERT 만. 앞 배치가 틀려도 못 고친다
   후   배치마다 AI 트랙을 **갈아끼운다**
   → ERD 의 AI 트랙 쓰기 규약(M-7 「INSERT 만」)이 바뀐다

④ 회의록 편집이 좁아진다 (MF-60)
   할 수 있는 것   줄 삭제 · 줄 추가 · 줄 수정 · 업무 넣기 · 안건 제목 수정
   못 하는 것      **줄 종류 바꾸기** · **안건 삭제**
   → `kind=task ↔ taskId` 불변식이 전환으로 깨질 일이 없어진다
```

---

## 4. 조사해 온 사실 — 다시 찾지 마라

**Soniox async** (2026-09-07 문서 확인)

```
모델      stt-async-v5   ← 전용. 화자 분리 재설계가 핵심 개선점(2026-06-11)
흐름      POST /v1/files → POST /v1/transcriptions → 폴링 또는 웹훅 → GET …/transcript
         인증 Authorization: Bearer
값       $0.10/시간 (실시간 $0.12). **화자 분리 추가 요금 없음**
파라미터   language_hints:["ko"] · language_hints_strict · enable_speaker_diarization
         context { general[{key,value}] · text · terms[] }  ← 상한 8000 토큰
결과      tokens[] 에 text · start_ms · end_ms · confidence · speaker
         ⚠ **sub-word 단위**로 쪼개진다 — 화자·시간 기준으로 묶어야 한다
상한      파일 300분 · Soniox 보관 30일
소요 시간   **공식 수치 없음.** 「한 시간짜리가 몇 분 만에」 정도 — 즉시로 설계하지 마라

⚠ 미확인   우리 녹음은 실시간으로 흘려 써서 **duration 헤더가 비어 있다**
          webm 은 지원 목록에 있지만 헤더 없는 webm 을 받는지는 문서에 없다
          → 이건 **실물 확인 항목**이다. 계약에는 「확인 필요」로 적고 넘어가라
```

**용어 보정 등급 2종** (mediness 실측에서 가져온 것)

```
자동 치환   문맥이 확실한 제품명·시스템명 → **본문을 바꾸고** 표에 남긴다
추정       인명 · 숫자 · 금액 · 일정, 1회 등장 → **본문은 안 건드리고** 표에만
화자 라벨은 어떤 경우에도 안 바꾼다
표가 곧 백업이다 — 표에 없는 치환은 하지 않는다
회의 1건 단위. 다음 회의로 안 넘어간다
```

**codex 설정** (0.147.0 실측)

```
deny list 는 없다 — allow list 뿐이다
features.shell_tool=false · web_search="disabled" · features.image_generation=false
features.apps=false   ← 안 걸면 mcp__codex_apps__ 27종이 붙는다
sandbox="read-only"
enabled_tools = 우리 툴 7개만 (서버 id 접두 안 붙인다 — 틀리면 조용히 「툴 0개」)
tools.<툴>.approval_mode="approve"   ← 툴별로
approval_policy="never" 는 「안 묻고 실패 처리」다 — 이것만 걸면 툴 호출이 죽는다
reasoning_effort 하한은 low. none 은 툴 고르는 판단 자체를 죽인다
```

---

## 5. 지킬 것

```
계층 규약    router → service → repository. ORM 은 repository 를 넘지 않는다
            service 는 commit 하지 않는다 (MF-1 이 W-1 을 닫는다)
            schemas/ = front 계약(camelCase) · dto/ = 내부(snake_case)
            Query(alias="camelCase") 는 손으로 쓴다

완료 게이트   task.status 대입은 task_service.change_status() 안에서만
            **회의록은 done 을 안 보낸다** — 완료 결과만 채운다
            회의록 쪽에 판정 코드를 두지 않는다

SPEC 경계    SPEC 에 둘 것 — 사용자 용어 · API request/response · status/enum · acceptance criteria
            SPEC 에 두지 말 것 — table schema 전문 · column/index/FK · repository 구조
```

---

## 6. 끝났다고 말하기 전에

```
□ MF-1 ~ MF-63 **31건 전부**가 어느 문서엔가 반영됐다 (보고서 표로 증명)
□ 옛 설계 흔적이 안 남았다 — 「최종 배치」 · 「통합 단계」 · 「600자」 · 「도구 6개」 grep 0건
□ SPEC 끼리 안 부딪힌다 — 007 과 008 이 같은 것을 다르게 적지 않았다
□ OQ 마다 「어디를 찾았는데 없었나」 근거가 붙어 있다
□ 새 결정을 만들지 않았다 — MF 번호 밖의 것을 정하지 않았다
```

**모르면 멈추고 물어라. 짐작으로 메우면 이 문서가 또 폐기된다.**
