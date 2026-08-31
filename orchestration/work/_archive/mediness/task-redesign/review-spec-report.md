# 리뷰 리포트 — task-redesign / planner 리뷰 (2026-08-31)

## 판정: FAIL

**FAIL 사유 요약** — 개정된 6 SPEC + 신설 도메인 문서 2건 + WP-124 자체는 결정 SoT 와 정확히 맞고 품질이 높다(§확인한 것). 그런데 이번 재정비가 **폐기한 개념(수락·거절·`accept_pending`·`/decline`·`/slack/complete`)이 planner 가 손대지 않은 4개 SPEC 에 «활성 계약» 으로 그대로 살아 있다** — 그중 하나(`spec-155:847`)는 결정 SoT 3번(재배정 = `todo` 리셋)을 **정면으로 반대로** 서술한다. 게다가 이번 개정이 spec-152 §개정 절차로 **강제하겠다고 선언한 규칙**(「개정 = 추가 + 구 서술 grep 삭제」, `spec-152:68`)이 개정 대상 파일 안(`spec-154`)에서도 두 곳 지켜지지 않았다.

이는 문체 지적이 아니라 **계약 모순 + 죽은 계약 잔존**이며, 브리프 §3-2·§3-8 의 FAIL 조건에 직접 해당한다. 해소는 grep 스윕 1회 + 잔존 5곳 정정으로 끝나는 범위다.

---

## 검수 범위

- diff: `origin/mediness` 기준 워킹트리 — **수정 13 파일 + untracked 3 파일 = 16 파일**, `+672 / −538`
  - 수정: `20-spec.md` · `20-spec/spec-{031,110,125,152,153,154}` · `30-work.md` · `30-work/work-074` · `40-architecture/{README.md,erd.md,domains/decision_execution_task.md}` · `log.md`
  - 신규: `30-work/work-124-task-ledger-unification.md` · `40-architecture/domains/{runtime_task.md,version_wbs_task.md}`
- **allowed_paths 준수 ✅** — 16 파일 전부 `products/mediness/` 내부. 이탈 0. 코드 레포 무변경.
- 실행한 검사:
  - `python3 scripts/lint-pipeline.py --strict` → **0 error / 255 warning (exit 0)**. mediness 범위 = **0 ERROR · 1 WARN**(아래 §기존 부채)
  - 죽은 계약 D-1~D-27 키워드 26종 grep 스윕 (`products/mediness/**`, `90-archive/` 제외, `work-074` 별도 취급)
  - `accept_pending` / `수락 대기` / `task_declined` / `accepted_at` / `task_accepted` / `거부됨` / `decline` 전수 grep
  - 결정 SoT(`_RESUME.md` §2 11행) · 발주 브리프 §3 계약 대조
  - 30-work.md 3표(Status Board / WP List / Spec Coverage) ↔ WP frontmatter 대조

---

## 위반 (FAIL 사유)

### V-1. `/decline` 엔드포인트가 SPEC-150 API 인덱스에 활성 계약으로 남았다

- `products/mediness/20-spec/spec-150-action-runtime-workflow.md:578` — `| POST | /incidents/{run_id}/tasks/{task_id}/decline | action.runtime.basic | assignee OR system_admin + **사유 필수** | [152] |`
- **무엇이 어긋났나**: 같은 라운드에서 `spec-152:62 ⑩` 이 `/decline` 을 **죽은 계약으로 삭제**했다고 선언하고, `spec-152:261`·`spec-154:2141`·`runtime_task.md:82` 가 거절 개념 폐기를 계약화했다. 그런데 **그 endpoint 를 소유·색인하는 SPEC-150 의 표는 그대로**라, 지금 이 제품의 계약은 "거절 endpoint 는 있다(150) / 없다(152·154)" 두 가지를 동시에 말한다. 이 행이 링크로 가리키는 대상(152)에는 그 endpoint 가 이미 없다 — **매달린 계약**이다.
- 근거: 결정 SoT `_RESUME.md` §2 2026-08-31 「수락·거절 개념 완전 폐기 — decline 엔드포인트 3곳 … 제거」 / 브리프 §3-2 / `rules/document-pipeline.md` §한 곳 원칙(계약 SoT 1곳)
- 권장 수정: `spec-150:578` 행을 삭제하거나 `~~취소선~~ + 폐기(2026-08-31)` 로 명시 전환하고, `spec-150` 개정 노트에 1줄 남긴다.

### V-2. SPEC-155 가 「재배정 → 수락 대기」를 활성 계약으로 서술한다 — 결정 SoT 3번과 정반대

- `products/mediness/20-spec/spec-155-ax-task-draft-workflow.md:847` — `| 수신자 쪽 | **기존 수락 대기 플로우 재사용** — 재배정된 task 는 **수신자의 수락 대기**로 선다([SPEC-154 §4.8]) |`
- 같은 파일 `:795` — `기존 ax_task.start 가 … 「시작할게」 한 마디가 **수락 대기 → 진행**을 한 번에 지난다`
- **무엇이 어긋났나**: 결정 SoT 는 **재배정 = `todo` 리셋 + `started_at` 클리어**이고 수락 게이트 자체가 없다. 이 두 줄은 없어진 상태값(`accept_pending`)을 경유하는 플로우를 계약으로 유지하며, **근거로 인용하는 대상(`SPEC-154 §4.8`)이 바로 그 게이트를 폐기한 절**이다 — 인용이 인용 대상과 반대를 말한다.
- 이 SPEC 은 planner 가 신설한 `runtime_task.md:13`(`used_by: MEDINESS-SPEC-155`)·`:241` 에서 **정본 소비자로 명시**돼 있다 — 인지 밖 문서가 아니다.
- 근거: 결정 SoT `_RESUME.md` §2 2026-08-31 「재배정 = `todo` 리셋 + `started_at` 클리어」 / 브리프 §3-3
- 권장 수정: `§6.11d` 표의 「수신자 쪽」·「수락 게이트 리셋」 두 행을 `todo` 리셋 계약으로 교체. `:795` 는 「시작 전이 1회」로 문장 정정.

### V-3. SPEC-155 · SPEC-060 이 `decline` write 표면(REST·MCP 툴·채팅 intent)을 활성 계약으로 유지한다

- `spec-155-ax-task-draft-workflow.md:537` (`POST /api/v1/action-runtime/task-declines` 신설 계약) · `:609` (`mediness.task_decline` write 툴) · `:670` (`ax_task.decline` 채팅 intent) · `:834-841` (§6.11c **거절 사유 «확정»** 절) · `:860` (매핑표)
- `spec-060-mcp-surface.md:56` · `:240` (`mediness.task_decline` = **write · ⚡즉시형(확정)**) · `:445` (등록 tool 수 **57** 카운트에 포함)
- **무엇이 어긋났나**: `work-124` §Scope 와 P5 는 **MCP `task_decline` 툴 제거**를 작업으로 박아 두었는데(`work-124:47`·`:218`), 그 툴을 소유·선언하는 SPEC 두 곳은 그대로다. 파이프라인 방향은 **SPEC → WP → code** 이므로(`rules/document-pipeline.md` §핵심 모델), **SPEC 이 살아 있는 표면을 WP 가 지우는 계획**은 역방향이다. 구현자가 SPEC-060 을 열면 지우지 말아야 할 툴로 읽힌다.
- 근거: 결정 SoT 2번(`MCP task_decline 제거`) / `rules/document-pipeline.md` §변경 라우팅 「API endpoint·외부 계약이 바뀌면 SPEC 을 수정한다」
- 권장 수정: SPEC-060 툴 표 2행 + `/health` 카운트, SPEC-155 §6.11b~e 를 폐기 표기로 정리하고 두 SPEC 을 `work-124` `covers:` 에 추가.

### V-4. SPEC-230 이 `수락 대기` 상태 필터 칩과 「여섯 상태」를 활성 UX 계약으로 유지한다

- `spec-230-landing-agent-chat.md:95` · `:316` · `:319` — 필터 칩 `전체 / 수락 대기 / 진행 중 / 완료`
- `:318` — `카드 뱃지가 **여섯 상태**를 제 이름으로 보여 주므로`
- **무엇이 어긋났나**: 상태는 5값이고 `accept_pending` 은 없다. 「여섯 상태」 뱃지와 「수락 대기」 칩은 렌더 불가능한 값을 계약한다. `spec-152:260`·`spec-154:1816` 은 같은 축에서 **4열/5값**으로 정정됐는데 이 화면만 남았다.
- 근거: 결정 SoT 1번(5값) / 브리프 §3-1
- 권장 수정: 칩 3개(`전체/진행 중/완료`) 또는 5값 기준으로 정정하고 「여섯 상태」→「다섯 상태」.

### V-5. SPEC-154 내부 모순 — `accepted_at` 이 같은 파일에서 «활성 필드» 이자 «폐기» 다

- `spec-154-decision-workflow.md:715` — `| accepted_at·started_at·completed_at·canceled_at | **실제 수락**·시작·완료·취소 시각 | 생성 입력 아님. 생명주기 이벤트가 자동 기록 |` (§4.8 필드 계약표, 활성)
- `spec-154-decision-workflow.md:2357` — `lifecycle stamp(**accepted_at**·started_at·completed_at·canceled_at)도 바뀌지 않는다` (§4.20.1 삭제 축 계약표, 활성)
- vs `spec-154:754` — `~~accepted_at 스탬프~~ | **폐기**`
- **무엇이 어긋났나**: 이번 개정이 스스로 **절차로 강제**한 규칙 — `spec-152:68` 「**개정 = 추가 + 구 서술 grep 삭제** 이고, 개정 노트는 실제 변경과 1:1」 — 이 개정 대상 파일 안에서 지켜지지 않았다. 이 SPEC 이 8회 개정 동안 겪은 실패 패턴(같은 계약이 3~4곳에 다른 버전으로 존재)이 이번 라운드에서 재발한 형태다.
- 근거: `spec-152:68`(이번 개정이 세운 절차) / `rules/document-pipeline.md` §한 곳 원칙
- 권장 수정: `:715` 에서 `accepted_at` 제거(3종 스탬프로), `:2357` 도 동일. `runtime_task.md:155` 스탬프 표가 이미 3종이므로 그것과 맞춘다.

### V-6. D-13 `/slack/complete` 가 SPEC-150 에 활성 endpoint 로 잔존 (브리프 §3-8 직접 위반)

- `spec-150-action-runtime-workflow.md:567` — `| POST | /incidents/slack/complete | — (전환 제외) | Slack callback … | [152] |` · `:650` 본문 서술
- vs `spec-152:407` — `**POST /slack/complete** — API 표에 등재돼 있었으나 **끝내 신설되지 않았다**(죽은 계약). 실경로는 공용 POST /api/v1/slack/interactions`
- **무엇이 어긋났나**: 브리프 §3-8 은 「D-1~D-27 이 products/mediness/ 에 **활성 서술**로 잔존하면 FAIL」로 판정 기준을 명시했다. D-13 은 spec-152 에서는 제거됐으나 **SPEC-150 의 endpoint 인덱스와 §capability 서술에는 살아 있고**, 그 행이 링크로 가리키는 152 에는 이제 그 endpoint 가 없다.
- 근거: `research-incident.md` §A-7 D-13 / 브리프 §3-8
- 권장 수정: `spec-150:567` 행 삭제 또는 폐기 표기 + `:650` 문단 정정. 실경로(`/slack/interactions`)로 대체 표기.

---

## 경미 (WARN)

- **W-1. `20-spec.md` 의 SPEC-152 제목이 갱신되지 않았다.**
  `20-spec.md:133`(SPEC Bundle) · `:200`(SPEC List) = `Incident Response Workflow — **이슈라이징 기반** 대응·…` ↔ `spec-152:5` frontmatter = `… **에러 트리거 기반** …`.
  인덱스는 본문의 단방향 derived view 인데(`rules/document-pipeline.md` §핵심 모델) 제목만 미러링이 빠졌다. lint 는 ID 만 대조하므로 잡지 못한다.

- **W-2. WP-124 `covers:` 가 SPEC-031·110/113 을 빠뜨렸다 — Spec Coverage 표도 미동기.**
  `work-124:9-13` `covers: 125·152·153·154`. 그런데 P6(`:226-238`)이 **SPEC-031 회의록 어휘 통일**을, P7(`:240-256`)이 **SPEC-110/113 레거시 원장 이관·폐기**를 구현한다. `30-work.md:242`(SPEC-031)·`:246`(SPEC-110)·`:249`(SPEC-113) covering WP 칸에 WP-124 가 없다.
  `rules/document-pipeline.md` §한 곳 원칙 — Spec↔Work 매핑 SoT = WP `covers` + Spec Coverage 표. 두 SPEC 이 이번 라운드에 개정됐는데(`spec-031`·`spec-110` diff 존재) 그것을 구현하는 WP 가 coverage 에 안 보인다.
  (V-3 해소 시 SPEC-060·155 도 같이 들어가야 한다.)

- **W-3. `21-html/Action Runtime Workflow Console.html:302,327,359,395` 에 `manual_incident`(D-14) 잔존.**
  planner 가 자체 보고에서 예외로 신고한 항목이고, 소유 SPEC(`spec-153:258`)은 폐기를 명시했다. `21-html` 은 선택 시안이라 lint 대상도 아니다 — **판정 제외**하되, 후속 incident WP 의 정리 목록에 넣을 것.

- **W-4. `40-architecture/decision-tracking-engine.md`(:31·:45·:67·:109) 와 `spec-113:66·136·140` 이 `is_required` 완료 자동 게이트를 활성 계약으로 유지한다.**
  `decision_execution_task.md:112` 는 `is_required` 를 **폐기**로 확정했고, `work-124:251` 이 「이 게이트가 SPEC-154 §4.9 run 전이와 중복인지 확인하고 중복이면 함께 소멸」을 **WP 검증 항목으로** 남겨 두었다 — 즉 계획상 열려 있는 자리다. 지금 단계에서 계약 모순으로 단정하기엔 근거가 부족해 WARN 으로 둔다. 코디네이터 판단 요청.

- **W-5. `spec-125:616` 이 5값 enum 목록을 본문에 복제한다.**
  브리프 §3-9(도메인 문서 = enum 정본, SPEC 은 링크) 관점의 미미한 중복. 다만 같은 줄이 `domains/runtime_task.md` 를 명시 링크하고, 이것은 `version_wbs_task_status`(별개 PG enum)의 「값 동형」 계약을 말하는 자리라 **의도된 서술로 읽힌다.** 지적하되 수정 요구는 하지 않는다.

---

## 기존 부채 (이번 판정 제외)

- `products/mediness/30-work.md:231` — `MEDINESS-SPEC-030 Spec Coverage 구현 상태 'in_dev' ≠ derive 한 'done'` (lint WARN 1건).
  이번 diff 가 건드리지 않은 행이고(covering WP-045/089/090/113 도 무변경), 이번 작업 이전부터 있던 drift다.
- 타 제품(`procedure-hub` · `selly` · `linky` 등) frontmatter WARN 254건 — **무관**. 전부 `doc_no`/`version` 누락 계열이고 mediness 와 무관하다.

---

## 확인한 것 (PASS 근거)

**결정 SoT 대조 (브리프 §3-1~7)**

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | 상태 5값 · `accept_pending` 부재 | ✅ | `runtime_task.md:69-74`(enum) · `:93-99`(5×5 전이표) · `version_wbs_task.md:51-53` · `erd.md:143` · `spec-152:1648` · `spec-125:616` · `spec-153:497` — 전부 5값 일치 |
| 2 | 수락·거절 폐기 (decline·`task_declined`·`accepted_at`) | ⚠ **부분** | 개정 대상 문서에서는 완전 제거 (`runtime_task.md:82-83,189-190` · `spec-152:261,1537` · `spec-154:752-754` · `spec-125:396`). **미개정 SPEC 4곳 잔존 → V-1·V-3·V-4·V-5** |
| 3 | 재배정 = `todo` 리셋 + `started_at` 클리어 · terminal 가드 | ⚠ **부분** | `runtime_task.md:142-151`(전이 아님·terminal 가드 «첫 쓰기 앞·기계 안»·**담당자 본인 요청 가능** 명시) · `spec-152:558` · `spec-154:2526` — 정확. **`spec-155:847` 이 정반대 → V-2** |
| 4 | 착수 = 명시 시작만 (자동전환 강등 · 시스템도 todo 후 전이) | ✅ | `runtime_task.md:121-132`(옛 경로 3개 표로 전부 닫음 · 「시스템도 예외가 아니다」 · 이벤트 2건) · `version_wbs_task.md:77-81`(overdue DM 유지 명시) · `spec-125:229` · `spec-154:752`(부트스트랩) |
| 5 | incident 정본 흐름 = 브리프 §3 코드블록 | ✅ | `spec-152:38-39`(흐름 재선언) · is_lead 게이트 `:800-806` · Slack fail-loud `:211-219`·`:1718`·`:1744`(`SLACK_NOT_CONFIGURED` 503) · cc=버전 참여자 `:1396` + **OQ-13 로 해소 규칙 표기** `:2068` · 완료 표면 슬랙만 `:202,210` · 피드백 게이트 유지 `:1492-1505` · 라운드 판정 «활성 라운드(최대 round_no)» 1벌 `:1506-1517` + 판정 자리를 전이 seam 안쪽으로 · run 감사 `:1545-1553`(TaskEvent→run 이벤트 이관) · 종결 시 추적 테스크 정리 `:1556-1568` |
| 6 | 범위 제외가 본문 계약에 침입하지 않음 | ✅ | 알림/DM·게이트 방치 에스컬레이션 = **OQ-2**(`:2055`) · 슬랙 인바운드 어댑터 = **OQ-15**(`:2070`) · GitHub/Jira mirror = **OQ-1/OQ-5**. 본문 계약 절에는 없음. `work-124:52-56` 제외 목록과도 일치 |
| 7 | WP-124 가 새 스펙만 SoT 로 참조 · WP2 미작성 | ✅ | `work-124:34` — 조사 문서를 «스냅샷이고 계약이 아니다» 로 명시하고 **링크·경로를 두지 않음**. `§Related:314-324` 전부 SPEC/도메인 문서. WP2(incident) 미작성 ✅, `work-074` 는 폐기 표시만 ✅ |

**교차 정합 (브리프 §3-8~11)**

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| 8 | D-1~D-27 grep 스윕 | ⚠ | D-5·D-11·D-19·D-23·D-24·D-25·D-8·D-6 = **폐기 표기로 정리 확인**(`spec-152:62,155,1629-1635,1759-1760` · `spec-153:863`). D-14 = spec-153 정정 ✅ / html 잔존(W-3). **D-13 = spec-150 잔존 → V-6.** work-074 인용분은 «동결» 명시로 허용 처리 |
| 9 | 도메인 ↔ SPEC 층위 (enum·전이표 복제) | ✅ | `spec-152:1650` 「어휘·전이표는 domains/runtime_task.md 가 정본 — incident 축 영향만」 · `spec-152:1531` TaskEvent 도 동일 · `spec-154:2157` · `spec-125:25` 링크 전환. 전이표 실체는 도메인 문서 1벌뿐 (W-5 만 미미) |
| 10 | ERD ↔ 도메인 ↔ SPEC 상호 링크·테이블 정합 | ✅ | `erd.md` 전면 재작성 — 인벤토리+축별 관계도 분리 · `:143-145`(5값·phase 전용 각각 도메인 링크) · `:255-271` 마이그레이션 좌표(`0028~0112` + 예정행이 WP-124 링크) · `40-architecture/README.md:46-49` 표에 신규 2건 등재 + 레거시 2건 🔴 표기. `runtime_task.md ↔ version_wbs_task.md ↔ decision_execution_task.md` 3자 상호 링크 성립 |
| 11 | planner 자체 보고 예외 6건 문서 명시 | ✅(5/6) | ① html `manual_incident` → 문서 명시 없음, 소유 SPEC 은 정정됨(W-3) ② §4.19 와이어프레임 → **`spec-154:1825` 에 ⚠ 명시** + 재도해를 WP-124 P5 로 위임 ③ WP-114 충돌 → `work-124:30`·**OI-1** ④ `accepted_at` drop → **OI-6** + `Rollback:297` 「값은 복구되지 않는다」 ⑤ `task_unblocked` 신설 → **OI-5** + `runtime_task.md:164` 「제안 목록에 있던 값의 승격, 새 축 아님」 ⑥ WP2 미작성 → `work-124:21`·`:32`·`work-074` 폐기 노트 |

**planner 리뷰 공통 체크리스트 (`roles/mediness/reviewer/rules.md`)**

- [x] **린트** — mediness 범위 **0 ERROR**. WARN 1건은 기존 부채(§기존 부채).
- [x] **WP 갱신 3자** — WP-124 가 `30-work/work-124-*.md`(신규) · `30-work.md:112`(Status Board) · `:196`(WP List) · `:264,274,275,276`(Spec Coverage 4행) 전부 반영. frontmatter `status: proposed` ↔ Board ↔ WP List **3자 일치**(lint ERROR 0 으로도 확인). WP-074 는 board/WP List 양쪽에 폐기 사유 기재 + frontmatter 의도적 동결(`work-074:15-33` 에 근거 명시).
- [x] **spec↔WP 정합** — WP-124 가 인용하는 조항이 전부 실재: `SPEC-154 §4.19.6`(칸반 4열, `spec-154:1816`) · `SPEC-154 §4.8`(`:745-757`) · `SPEC-152 §라운드 판정`(`:1506`) · `SPEC-125 §U-13`(overdue) · `SPEC-153 task_status`(`:497`). 개정된 spec 내용과 WP 본문 간 모순 없음. **단 covers 누락 2건 → W-2.**
- [x] **frontmatter** — `work-124` `doc_no: MEDINESS-DOC-244`(전역 유일, lint 통과) · `covers`/`depends_on: []` 존재. 신규 도메인 문서 2건 `type: architecture` + `used_by` 존재(도메인 문서는 `doc_no` surface 아님 — 정상). `decision_execution_task.md` `status: draft → deprecated` 전환 적절.
- [x] **coverage 상태 규칙** — WP-124 는 `proposed` 이므로 SPEC-125/152/153/154 의 구현 상태를 `done` 으로 올리지 않았다. 4행 모두 `in_dev` 유지 ✅ (lint derive 검증 통과).

**추가로 확인한 문서 품질(지적 없음 — 기록만)**

- `log.md:19-27` — 이번 라운드 entry **8행** 추가. 종류 enum(`arch-change`/`domain-add`/`spec-change`/`wp-add`/`wp-change`) 정확, 역시간순, 영향 ID 콤마+공백 규약 준수. 결정 성격 entry 의 요약이 「무엇을·왜·대안」을 담아 규약(§log.md `요약` 규약)을 충족.
- `runtime_task.md` — 전이표(5×5) · 스탬프표 · TaskEvent 확정 1벌 + **폐기 어휘 표** · 합성 전이 · 재배정 · `task_type` allowlist · Invariant · 마이그레이션 4단계까지 SoT 로서 빠짐없다. 「왜 그렇게까지 하는가」 근거를 각 계약에 붙인 서술이 특히 좋다(`:132`).
- `work-124` — 10 phase 전부 `Status: TODO`(형식 규칙 준수 — enum 만) · `설명/작업/검증/완료 증거` 4칸 구조 준수 · P1~P3 배포 단위 명시 · Rollback 이 phase 별로 갈려 있고 `accepted_at` 비복구를 명시 · OI 6건이 전부 실제 미결. **PR Plan/Dev Plan 중복 절 없음** ✅.

---

## 재검수 시 확인할 것 (수정 재발주용 체크리스트)

1. `spec-150:567`(D-13) · `:578`(decline) 2행 정리 + 개정 노트
2. `spec-155:537,609,670,795,834-841,847,860` decline·수락 대기 계약 정리 (§847 이 최우선 — 결정 SoT 정면 위반)
3. `spec-060:56,240,445` MCP `task_decline` 툴 + 카운트 정리
4. `spec-230:95,316,318,319` 필터 칩·「여섯 상태」 정정
5. `spec-154:715,2357` `accepted_at` 제거
6. `20-spec.md:133,200` SPEC-152 제목 동기 (W-1)
7. `work-124` `covers` + `30-work.md` Spec Coverage 에 SPEC-031·110(+정리 후 060·155) 추가 (W-2)
8. 재검수 시 재실행: `python3 scripts/lint-pipeline.py --strict` + `grep -rn "decline\|수락 대기\|accept_pending\|accepted_at\|task_declined\|slack/complete" products/mediness/20-spec products/mediness/40-architecture`

---
---

# 재검수 (R2, 2026-08-31)

## 최종 판정: WARN — 진행 가능

**FAIL 6건 전부 해소 · WARN 2건 해소 · W-4 코디 지침대로 처리 · 활성 계약 잔존 0 · lint mediness 0 ERROR.** 원 리포트의 재검수 8항목이 **8/8 통과**했고, 차단 사유는 남지 않았다. WARN 으로 두는 이유는 **수치 오기 3건**(계약 축이 아니라 «착지 시 움직일 숫자» 와 «후보 개수»)이 R2 정정 과정에서 새로 또는 그대로 남았기 때문이고, 이 셋은 **PR 진행을 막을 근거가 아니다** — 정본 표(`spec-060:180` = write 18 · `:452` = `/health` 57)는 정확하고 WP-124 작업 항목도 옳은 값을 들고 있다.

## 재검수 범위

- diff: `origin/mediness` 기준 워킹트리 — **수정 19 파일 + untracked 3 = 22**, `+790 / −601` (R1 대비 **+6 파일 · +118/−63**)
- R2 가 새로 손댄 6 파일: `spec-060`(17) · `spec-113`(4) · `spec-150`(20) · `spec-155`(81) · `spec-230`(17) · `40-architecture/decision-tracking-engine.md`(5)
- **allowed_paths 준수 ✅** — 22 파일 전부 `products/mediness/`. 코드 레포 무변경. WP2 미작성 유지.
- 실행: `python3 scripts/lint-pipeline.py --strict` · 폐기 키워드 6종 전수 grep(`20-spec/`·`40-architecture/`) · `scripts/lint-pipeline.py:664` `_derive_coverage_status` 소스 대조 · MCP 툴 카운트 사실 추적(2026-08-12 → 08-25 → 현행)

## ① FAIL V-1~V-6 해소 판정

| # | 원 위반 | 판정 | 근거 (파일:줄) |
|---|---|:--:|---|
| **V-1** | `spec-150` `/decline` 활성 행 | ✅ **해소** | `spec-150:584` 취소선 + 「**폐기 (2026-08-31)**」 + 「대체 = 아래 `/reassign` 행」 · `:20-23` 변경 노트 ① 신설(어휘 정본 `runtime_task.md` 링크) |
| **V-2** | `spec-155:847` 「재배정 → 수락 대기」 (결정 SoT 3번 정면 위반) | ✅ **해소** | `spec-155:869` → **「재배정된 task 는 수신자의 `todo` 로 선다 — 수락 대기가 아니다」** + 「근거로 인용하던 SPEC-154 §4.8 이 바로 그 게이트를 폐기한 절」 각주 · `:871` 「수락 게이트 리셋」 → **「`todo` 리셋 + `started_at` 클리어, 전이가 아니라 담당자 축의 변경」** · **행 2개 신설** = terminal 가드(`:872`, `system_admin` 예외 없음) · 담당자 본인 요청(`:873`) · `:813` 「`ax_task.start` 가 수락 대기 → 진행을 한 번에」 → **「`todo → in_progress` 시작 전이 1회」**(결론 유지·근거 교체) |
| **V-3** | decline write 표면 3벌 (`spec-155` · `spec-060`) | ✅ **해소** | `spec-155:545`(REST) · `:617`(MCP) · `:678`(leaf) · `:884`(§6.11e 매핑) · `:702`(§6.10 분류표) 전부 취소선 + 폐기 표기 · `§6.11:163-173` 처분 표 배너(거절 폐기 / 재배정 존치·지위 상승 / ⓐⓑ 불변) · `spec-060:247`·`:63` 🔴 계약 폐기 · 등록 해제 대기 + `:40-45` 개정 노트. **spec-152 잔존 3곳도 함께**(`:86`·`:1766`·`:1805` write 후보에서 「거부」 제거 · `:1811→` §MCP ④ `/slack/complete` 폐기) |
| **V-4** | `spec-230` `수락 대기` 칩 · 「여섯 상태」 | ✅ **해소** | `:323` 칩 `전체 / **대기** / 진행 중 / 완료` · `:325` **「다섯 상태」** + 칩 밖 상태를 `blocked`·`canceled` 로 정정 · `:326` 문구 행 동기 · `:24-29` 개정 노트 · `:101` 구 기록은 각주로 이음(이력 미개변) |
| **V-5** | `spec-154` `accepted_at` 내부 모순 | ✅ **해소** | `:716` 스탬프 **3종**(`started_at`·`completed_at`·`canceled_at`) + 정본 링크 · `:2358` 동일 · `:37` 개정 노트 **㉖-a** — 「스스로 강제 선언한 절차가 개정 대상 파일 안에서 안 지켜졌다」를 **감추지 않고 기장** |
| **V-6** | D-13 `/slack/complete` (브리프 §3-8) | ✅ **해소** | `spec-150:573` 취소선 + 「계약으로 신설된 적이 없다(죽은 계약 D-13)」 + 실경로 `POST /api/v1/slack/interact` 명시 · `:656` §범위 제외 항 폐기(「전환 제외 대상이라는 자리 자체가 없어진다」) · `:588` 집계 **35/35 → 33/33 전부 capability**(「의도적 전환 제외 1개」 축 소멸 명시) · 구 수치는 각주로 이음 |

**V-6 집계 정정 검산** — 표에서 2행이 폐기됐으므로 35 − 2 = 33 ✅. 「capability 34 + Slack callback 1」 중 그 callback 1 이 곧 폐기 대상이었으므로 「전환 제외 축 소멸 → 33 전부 capability」도 산술·의미 양쪽으로 맞다.

## ② WARN W-1 · W-2 · W-4

| # | 판정 | 근거 |
|---|:--:|---|
| **W-1** | ✅ **해소** | `20-spec.md:133`(SPEC Bundle) · `:200`(SPEC List) 둘 다 **「에러 트리거 기반」**. 구 문자열 잔존 0 |
| **W-2** | ✅ **해소** | `work-124` `covers:` **4 → 11**(`:9-19` = 031·060·110·113·125·150·152·153·154·155·230) · `30-work.md:196` WP List Covers 열 **11개 동일 문자열** · Spec Coverage **11행**에 WP-124 등재(`:236,242,246,249,264,273,274,275,276,277,281`). Status Board 는 WP-124 1행이라 무변경이 정상. **WP 본문에 추적 가능한 작업도 박혔다** — `:186`·`:198`(P3 `/slack/complete` 구현 변형 폐쇄 + 검증) · `:228`·`:234`(P5 SPEC-060 인벤토리 동기 + `/health` 56 3자 일치) · `:229`(랜딩 칩) · `§Related:332-335` 4줄 |
| **W-4** | ✅ **코디 지침대로** | `spec-113:134` · `decision-tracking-engine.md:35` 각각 **인용 블록 1줄** 추가 — 「A축 폐기 예정 · `is_required` 는 `decision_execution_task.md` 에서 폐기 확정 · **지금 지우지 않는 이유** = SPEC-154 §4.9 run 전이와 중복인지 확인 전이고 그 확인이 WP-124 P7 검증 항목 · 현행 동작의 기록이지 존속 약속이 아니다」. **`is_required` 자체는 미삭제** — 지침(「폐기 예정 노트만」) 정확히 준수. 두 파일 diff 가 각 +2/+3 줄뿐이라 **범위 밖 변경 0** |
| W-3 · W-5 | — | 지시대로 미수정 확인 (`21-html` 시안 · `spec-125:616` 의도된 동형 서술) |

## ③ 폐기 키워드 grep 스윕 재실행 — **활성 계약 잔존 0**

`grep -rn` (`20-spec/` + `40-architecture/`), 히트 전량을 허용 범주로 분류:

| 키워드 | 활성 잔존 | 남은 히트의 성격 |
|---|:--:|---|
| `task_declined` · `task_accepted` | **0** | 히트 자체가 0 |
| `accepted_at` | **0** | `work-124`(제거 작업 목록·downgrade·Rollback) · `work-104`/`work-103`(완료 WP 기록) · `work-074`(동결). **SPEC·도메인 문서 활성 잔존 0** |
| `accept_pending` | **0** | `spec-152:1408,1412`(폐기 **근거** 서술 — 과거형 진단) · `spec-125:935`·`runtime_task.md:229`(**마이그레이션 매핑** — 없으면 cutover 가 불가) |
| `수락 대기` | **0** | `spec-230:101`(그 시점 기록 + 정정 각주) · `spec-154:1624,1711,1835,1881,1904,1986,2057`(**ASCII 와이어프레임** — `:1825` 가 「이 시안 표기는 폐기됐다·정본은 위 표·재도해는 WP-124 FE」로 이미 봉인, R1 에서 예외 승인된 자리) |
| `거부됨` | **0** | `spec-154:2320` AC-18c — 「거부됨 배지가 **어디에도 없고**」를 단언하는 문장(폐기를 **강제**하는 쪽) |
| `/slack/complete` | **0** | `spec-152:62`(죽은 계약 삭제 목록) · `spec-150` 폐기 표기 2곳. **`work-089` 완료 WP 기록**은 그 시점 착지 기록이라 허용 |
| `decline` | **0** | 전부 취소선·🔴·폐기 표기. 예외 1 = `spec-154:2283` → **R2-W3** |

## ④ R2 신규 6파일의 범위 이탈 검사 — **이탈 0**

| 파일 | 변경량 | 손댄 곳 | 판정 |
|---|---:|---|:--:|
| `spec-113` | +2 | frontmatter date + §3.6 인용 블록 1개 | ✅ 범위 내 |
| `decision-tracking-engine.md` | +3 | frontmatter date + §기본 실행 모델 인용 블록 1개 | ✅ 범위 내 |
| `spec-150` | 20 | frontmatter + 변경 노트 + endpoint 2행 + 집계 1문장 + retry 각주 + §범위 제외 2줄. **커널 불변식·3요소·3층·§4.5·§5 조립·leaf 정의·Policy·projection 전부 무변경**(노트가 그 사실을 명시) | ✅ 범위 내 |
| `spec-230` | 17 | frontmatter + 개정 노트 + `:101` 각주 + §U-7 4줄. 사이드바 반응형·출처 칩·중단 계약·API 표면 무변경 | ✅ 범위 내 |
| `spec-060` | 17 | frontmatter + 개정 노트 + `task_decline` 행 2곳. **인벤토리 머리 카운트·§5 AC 수치 미변경**(의도 — ⑤ 참조) | ✅ 범위 내 |
| `spec-155` | 81 | 개정 노트 + §6.4 초기 상태 `todo` + §6.7/6.8/6.9/6.10/6.11 거절 축. 재배정 축·생성/수정/삭제 3종·§6.10d 5조건·§6.11f·§7 자격 축 무변경 | ✅ 범위 내 |

**기존 계약 파손 없음.** 특히 `spec-155` 는 「`ax_task.accept` 를 만들지 않는다」·「재배정 = 🗂확인 카드」·「§6.10d ⑤ 일반 규칙」 **세 결론을 전부 유지**하고 근거만 교체했다 — 폐기가 살아 있는 판단을 끌고 내려가지 않았다. `§6.11b`·`§6.11c` 를 삭제하지 않고 폐기 표기로 남긴 것도 「왜 그렇게 갔는지」 보존 원칙에 맞다.

## ⑤ 「write 19→18 오독」 정정 — planner 근거 **맞다** (spot 확인)

수치 이력을 문서에서 역추적해 검산했다:

| 시점 | 사건 | write | `/health` | 출처 |
|---|---|---:|---:|---|
| 2026-08-12 (4차) | 거절·재배정 2종 **등재** | 17 → **19** | 56 → **58** | `spec-060:59` |
| 2026-08-25 (②) | `decision_register` **등록 해제** | 19 → **18** | 58 → **57** | `spec-060:48` · `work-116:170` |
| **현행** | — | **18** | **57** | `spec-060:180`(「read 39 + write 18」) · `:452`(「`/health` … **57**」) |
| WP-124 P5 착지 시 | `task_decline` 등록 해제 | 18 → **17** | 57 → **56** | `spec-060:44` · `work-124:228,334` |

⇒ **planner 판정이 정확하다.** 원 리포트가 인용한 「19→18」은 *2026-08-25 `decision_register` 해제 때의 수치*였고, `task_decline` 제거 후 값은 **17 / 56** 이다. 방향(계약 폐기는 지금·인벤토리 수치는 등록 해제 착지 시)도 `spec-060:184-185` 가 등재 때 지킨 「실측 일치 표」 규율의 반대 방향으로 일관된다 — **정본 표를 실물보다 앞세우지 않는다**는 같은 규칙이다.

## ⑥ Spec Coverage 3행 `done → in_dev` 강등 — derive 규칙상 **맞다 (필수)**

`scripts/lint-pipeline.py:664` `_derive_coverage_status()` 실물 대조:

```python
if all(s == "done" for s in wp_statuses):        return "done"
if any(RANK[s] >= RANK["in_dev"] for s in wp_statuses): return "in_dev"
return "proposed"
```

SPEC-113·155·230 의 covering 집합은 **{기존 done WP…} + {WP-124 `proposed`}** 다. `all(done)` 이 깨지고 done WP 가 `RANK ≥ in_dev` 를 만족하므로 **derive = `in_dev`**. ⇒ **강등은 선택이 아니라 강제**이고, `done` 을 유지했으면 오히려 derive WARN 이 떴다. lint 가 그 3행에 WARN 을 내지 않는 것이 일치의 증거다. 「끝난 SPEC 에 새 일이 생겼다」를 표가 말하게 한다는 planner 의 해석도 규칙과 같은 방향이다.

## ⑦ lint

```
python3 scripts/lint-pipeline.py --strict  →  0 error, 255 warning (exit 0)
```

- **mediness 범위 = 0 ERROR · 1 WARN** — `30-work.md:231` SPEC-030 coverage derive. 이번 diff 가 건드리지 않은 행이고 covering WP(045/089/090/113)도 무변경 ⇒ **기존 부채**(R1 판정과 동일).
- 타 제품 254 WARN(`procedure-hub`·`selly` 등 `doc_no`/`version` 누락) — **무관**.
- WP status 3자 일치·doc_no 유일성·map 동기·phase Status 형식 = ERROR 0 으로 전부 통과.

## R2 경미 (WARN — 진행 차단 아님)

- **R2-W1. `spec-155:29` 개정 노트 ⑤ 가 「MCP write **19 → 18**」로 남았다.**
  같은 파일 `:890`(§6.11e)은 「write **18 → 17** · `/health` 57 → 56」, `spec-060:44`·`work-124:228`·`:334` 도 전부 18→17 이다. planner 가 **스스로 오독을 발견해 정정하고 「전 문서에서 통일했다」고 보고한 항목**인데 이 한 곳이 통일에서 빠졌다 — 같은 파일 안에서 두 수치가 다르게 말한다.
  영향: 구현자가 개정 노트만 보면 잘못된 목표치를 잡는다. 정본 표(`spec-060:180`)와 WP 작업 항목은 옳으므로 **계약 축 손상은 없다.**
  권장: `spec-155:29` 를 `18 → 17` 로 교체(1곳).

- **R2-W2. `spec-152:88` 이 「write 툴 **6종**(§6 OQ-12)」으로 남았다.**
  같은 파일 `:86`·`:1766`·`:2067` 은 「거부 1종 소멸 → **5종**」으로 정정됐다. `:2067` OQ-12 제목의 「6종」은 괄호 정정문이 붙어 **이력 보존**으로 읽히지만 `:88` 에는 그 단서가 없다.
  권장: `:88` 에 정정 각주를 달거나 5종으로 교체.

- **R2-W3. `spec-154:2283` 이 `decline_reason` 을 현재형 선례로 인용한다.**
  「`거절` 이벤트가 **이미 그렇게 하고 있고** `decline_reason` 이 거기서 파생한다」 — 그 이벤트는 이번에 폐기됐다. 다만 이 문장이 세우는 계약은 **`blocked_reason` 을 `중단` 전이 이벤트 payload 에서 파생**시키는 것이고 그 계약 자체는 무손상이다(`decline_reason` 은 **설계 판단의 선례**로만 인용됨 — `:2282` 「컬럼을 만들면 진실이 두 벌이 된다」의 근거).
  권장: 과거형(「그렇게 하고 있었고」)으로 한 단어 교체. **선례 인용 자체는 지우지 않는 편이 낫다.**

## 이월 (판정 제외 — 이번 범위 밖)

- **`work-114`(`in_dev`)가 「5열 보드 · 수락 대기 컬럼 · 수락 CTA」를 명시 계약한다**(planner 자체 보고 §남긴 것 1). **동의한다** — 이 자리는 `work-124` **OI-1**(FE 파일 충돌 — 착수 전 소유 조정)이 이미 소유하고, WP-114 스스로 「수락 대기 게이트 은퇴 — 별도 트랙」을 적어 두어 인지 밖이 아니다. WP 는 빌드 계획이고 계약 SoT 는 SPEC 이며 그쪽은 정정됐다. **착수 전 소유 조정 시 함께 정리**할 것.
- 완료 WP 기록(`work-107`·`work-103`·`work-104`·`work-089`)의 「수락 대기」·`accepted_at` 서술 — **그 시점 사실의 기록**이라 미개변이 옳다.
- `21-html` 시안 `manual_incident`(W-3) · `spec-125:616` enum 동형 서술(W-5) — 지시대로 미수정.
- SPEC-030 coverage derive WARN — 기존 부채.

## R2 재검수 8항목 대조

| # | 원 리포트 체크리스트 | 판정 |
|---|---|:--:|
| 1 | `spec-150` D-13·decline 2행 + 개정 노트 | ✅ |
| 2 | `spec-155` decline·수락 대기 (§847 최우선) | ✅ |
| 3 | `spec-060` MCP `task_decline` + 카운트 | ✅ (수치 이동 시점 규율 근거 타당) |
| 4 | `spec-230` 칩·「여섯 상태」 | ✅ |
| 5 | `spec-154` `accepted_at` 2곳 | ✅ |
| 6 | `20-spec.md` SPEC-152 제목 | ✅ |
| 7 | `work-124` `covers` + Spec Coverage | ✅ (4→11 · 3표 동기 · derive 검산 통과) |
| 8 | lint + grep 재실행 | ✅ (0 ERROR · 활성 잔존 0) |

**8/8 통과. 차단 사유 없음 — 코디네이터 판단으로 PR 진행 가능하며, R2-W1~W3 은 3곳 한 줄씩 고치면 닫힌다.**
