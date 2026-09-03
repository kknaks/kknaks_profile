# 리뷰 리포트 — mcp-library-publish / planner 리뷰 (2026-08-28)

## 판정: PASS

사용자 확정 요구 2건이 모두 diff 로 성립하고, allowed_paths 이탈 0, mediness 범위 lint ERROR 0.
아래 «경미» 2건은 **위반이 아니라 판단 요청**이며 진행을 막지 않는다.

---

## 검수 범위

- **diff 산정 주의** — 이 워크트리의 `HEAD`(`5ab09c2aa`)는 **`origin/mediness`(`15459cd04`)보다 1 커밋 뒤**다(`rev-list --left-right --count` = `1 0`). 워커 산출물은 **커밋되지 않은 working-tree 변경**이므로, 브리프의 `git diff origin/mediness...HEAD` 는 base 이동분(#652 회의 WP 마감)까지 끌어와 노이즈가 된다. 실제 검수 범위는 **merge-base `5ab09c2aa` 위의 `git diff HEAD`** 로 산정했다.
- 파일 **5개** (untracked 0):

  | 파일 | 변경량 |
  |---|---|
  | `products/mediness/20-spec/spec-013-baseline-publish.md` | +123 / −4 |
  | `products/mediness/20-spec/spec-060-mcp-surface.md` | +22 / −3 |
  | `products/mediness/20-spec/spec-003-capability-rbac.md` | +4 / −2 |
  | `products/mediness/20-spec.md` | +1 / −1 |
  | `products/mediness/log.md` | +2 / −1 |

- **allowed_paths(브리프 §5 = `products/mediness/`, `context/`) 이탈 0.** 5파일 전부 `products/mediness/` 아래.
- **브리프 §7 금지 항목 4건 전부 미위반** — `30-work/`·`30-work.md` 무변경(WP 작성 0) · `spec-230-landing-agent-chat.md` 무변경(참조만) · `baseline.publish.basic` 축소 0 · 타 제품 문서 무변경.

### 실행한 검사

```
git diff --stat HEAD / git status --porcelain / git rev-list --left-right --count
python3 scripts/lint-pipeline.py --strict          → 0 error, 255 warning (exit 0)
grep 대조: OQ-10 · MEDINESS-OPEN-060-C · «호출자 밖으로 나가는 쓰기» 원문 · SPEC-003 §0.1/§0.2/§3.2/§3.3/§3.4/§3.7 ·
           SPEC-050/SPEC-129 실재 · mediness.product_list 인벤토리 행 · SPEC-013 §2 S-3 ·
           landing_chat.usage.read / prompt.version.* / voice.profile.* 선례 · write/health 카운트 · doc_no 4건
코드 대조(read-only): mediness-app/mcp/app/tools/read_file.py:28 · back/app/routers/baseline_publish.py:54-58
```

---

## 위반 (FAIL 사유)

**없음.**

---

## 경미 (WARN — 판정에 넣지 않음, 코디네이터 판단 요청)

### W-1. SPEC-003 §3.2 leaf index — `baseline` 도메인이 **행 2개**로 갈렸다 (같은 소유 SPEC인데)

- `products/mediness/20-spec/spec-003-capability-rbac.md:247-248`
- 이 표에서 **같은 소유 SPEC 의 leaf 여러 개는 한 행의 leaf 칸에 나열**하는 것이 8건 선례다 — `action`(`action.runtime.basic` `action.runtime.read_all`, 바로 위 행) · `landing_chat`(`room.basic` `usage.read`) · `mcp_tool` · `prompt` · `voice` · `weekly_report` · `department_space` · `decision`. `library` 가 3행인 것은 **소유 SPEC 이 각각 다르기 때문**(010/012/040)이라 이 경우와 다르다. 신규 행은 `baseline` + `SPEC-013` 으로 **위 행과 도메인·소유 SPEC 이 동일**하다.
- **근거 불충분 — 위반으로 단정하지 않는다.** 이 표에 「도메인당 1행」을 명문화한 규칙은 없고, 같은 §3.2 하단 bullet 은 「이 index 에 **행을 추가한다**」고만 적는다. 또 ⏳ 초안분을 **별행으로 격리**하면 사용자 리뷰에서 되돌리기가 쉽다는 실용 이점이 있다(의도적 선택일 수 있음).
- 권장(택일): ⓐ 현행 유지 + 확정 시 위 행에 병합 ⓑ 지금 `baseline.publish.basic` 행의 leaf 칸에 병합하고 비고에 ⏳ 표기.

### W-2. SPEC-013 §6 신규 OQ 절의 「§6 머리 규약 그대로」 지시자가 가리키는 대상이 없다

- `products/mediness/20-spec/spec-013-baseline-publish.md:202`
- `## 6. Open Questions` 바로 아래에는 머리 규약 문단이 없다. prose-ID 규약("OPEN-* ID 체계는 동결 레거시…신규 ID 를 발급하지 않고 prose 로 둔다")은 **§6 안의 「양식 개정 신규 OQ (2026-06-17)」 하위 절 머리**에 있다(`:214`).
- **규약 자체는 정확히 지켰다** — `OQ-a/b/c` 는 `MEDINESS-OPEN-013-*` ID 를 발급하지 않은 prose 라벨이고, lint 의 ID_RE(`-(DEC|SPEC|WP|OPEN|BL|QA|ESC)-NNN`) 밖이라 undefined-ID-ref 를 만들지 않는다(lint ERROR 0 로 실증). 지시자 문구만 부정확하다.
- 권장: 「§6 의 2026-06-17 절 머리 규약 그대로」로 한 단어 정정.

---

## 특별 검수 항목 (브리프 §2) — 항목별 결과

### ① 사용자 확정 요구 1 — 「기존 REST 의 thin wrapper, 새 정책 발명 없음」 ✅ 성립

- SPEC-013 §4 Functional Rule 신규 bullet(`:174`)이 **같은 서비스 계층 경유**를 명문화했다 — `prepare_upload`(양식 검증 + path 조립 + slug + frontmatter 주입) → `BaselinePublisher.publish`(화이트리스트 재검증 → `publish_lock` → fetch/reset → 존재 검증 → write → commit/push → `baseline_publishes` INSERT). **분기점은 ② 입력 어댑터 + capability 의존 둘뿐**으로 못 박았고, 「복제하면 두 문의 동작이 갈리고 그것이 이 라우트를 «다른 정책» 으로 만든다」로 근거까지 달았다.
- 실제 코드와 정합 — `back/app/services/publish/baseline_publisher.py` 의 화이트리스트·lock·로그 계약을 재사용하는 서술이고, 새 화이트리스트/새 로그/새 git 규약은 **한 줄도 신설되지 않았다**(diff 전수 확인).
- 신설된 것은 **입력 계약 3건뿐**(`format`·`content`·body `operation`) — 전부 「MCP 툴 인자에 파일이 없다」는 표면 차이의 직접 귀결이고, §3 Validation 표에 `(agent 경로)` 로 격리 등재됐다(`:155-157`).

### ② 사용자 확정 요구 2 — 「MCP 발행 = 시스템 관리자 전용, 두 층 모두 / 웹은 안 좁힌다」 ✅ 성립

- **툴 선언층** — SPEC-013 §3 `### MCP 계약` 툴 정의 표: `요구 leaf (requires(...)) = baseline.publish.agent`. SPEC-060 인벤토리 ⏳ 주석 ③ 에도 같은 값.
- **back 재판정층** — §API 계약 신규 행(`:49`)이 `POST /api/v1/library/baseline/agent-publishes` 의 요구 leaf 를 `baseline.publish.agent` · **`system_admin` 전용**으로 박았고, §4 Functional Rule bullet 이 `require_capability("baseline.publish.agent")` 를 명시.
- **두 층 모두 검증 가능** — §5 AC 신규 항목(`:184`)이 「ⓐ `tools/list` 에 안 실림 ⓑ 그럼에도 직접 호출하면 back 이 403 `CAPABILITY_REQUIRED` + leaf 로 거부 — **두 층 모두에서 막힌다(툴 선언만으로 통과되지 않는다)**」를 별도 체크로 세웠다. 요구를 그대로 검증 항목으로 옮긴 것.
- **웹 불변 — diff 로 실증.** SPEC-013 의 기존 3 endpoint 행(`:46-48`)·`baseline.publish.basic` leaf 행·역할 매트릭스 `basic` 행 전부 **무변경**(diff 에 `-` 라인 0, 추가만 있음). SPEC-003 도 `baseline.publish.basic` 행 무변경. 별도 AC(`:185`)로 「`member` 만 가진 활성 구성원이 upload/update/delete 를 그대로 수행」을 못 박았다.
- **코드 구조상으로도 웹이 조여질 경로가 없다** — `back/app/routers/baseline_publish.py:56-58` 의 `_Capability` 는 **per-route Annotated alias**(라우터 레벨 `dependencies=` 가 아님)라, 같은 라우터에 다른 capability 의 신규 route 를 붙여도 기존 3 endpoint 의 의존이 변하지 않는다. 초안의 「기존 3 endpoint 의 함수·의존은 손대지 않는다」는 구조적으로 정확하다.

### ③ 전용 라우트 + 신규 leaf 설계가 SPEC-060 §4 원칙과 정합한가 ✅ 정합 (원문 대조 완료)

- SPEC-060 §4 원문(`:369`, 이번 diff 이전부터 존재): 「선언 값은 그 tool 이 감싸는 **back REST endpoint 의 leaf 를 그대로** 쓴다… **tool 전용 leaf 를 새로 만들면 같은 행동에 권한 키가 둘 생긴다**」.
- 초안의 논거는 이 원문을 **왜곡 없이** 쓴다 — 「전용 라우트를 세우면 leaf 는 «툴 전용» 이 아니라 **그 endpoint 의 leaf**」이므로 원칙이 문자 그대로 성립. 「툴은 두 번째 게이트가 아니다」도 유지된다(판정은 back 한 자리).
- **반대 안의 기각 사유도 원문 근거를 댄다** — 같은 라우트 내 호출자별 분기를 배제한 이유로 ⓐ 한 endpoint 가 호출자에 따라 두 답을 냄 ⓑ 사람 축(누구인가) 판정에 표면 축(어디서 왔나)이 섞임 ⓒ 웹 코드에 손이 닿아 넓은 쪽이 조여질 위험. 신설 규범 bullet(SPEC-060 §4 `:371-374`)이 **비용(endpoint 1개 증가)까지 정직하게 적고**, 「발행 로직·화이트리스트·lock·로그를 복제하지 않는 것이 조건」을 성립 조건으로 걸었다.
- **자리 배치도 맞다** — 이 신설 규범은 「선언 규약 자체는 본 SPEC 이 owns」(SPEC-060 §4 소비처 bullet) 영역이므로 SPEC-060 에 두는 것이 정본 위치다.
- **OQ-10 인용 정확** — 초안은 `[SPEC-230 §5 OQ-10]` 로 인용한다. 실제로 OQ-10 은 **SPEC-230 §5**(`spec-230-landing-agent-chat.md:1100`)에 있고 SPEC-060 에는 없다 — **브리프 §1/§4 의 «SPEC-060 §5 OQ-10» 표기가 틀렸고 워커가 실물을 확인해 정정한 것**. 인용구 「leaf 분해가 필요한 것은 **사람마다 다르게** 회수해야 할 때뿐」도 원문과 **축자 일치**. 「툴 단위 회수(카탈로그 `enabled`)와 다른 축」도 원문(D11)과 일치.

### ④ 즉시형 예외 처리 — 원문 왜곡 없는가 / OQ 규약대로인가 ✅ 정합

- 원문(`spec-060-mcp-surface.md:346`): 「«호출자 밖으로 나가는 쓰기» 는 즉시형으로 둘 수 없다 (2026-08-25 신설)」 — 초안이 **인용부호까지 그대로** 옮겼고, 「정면으로 맞물린다」로 **긴장을 숨기지 않고 명시**했다.
- **오염 등급 어휘 정확** — §4 원문(`:44`)의 3등급은 「읽기=허용 / 본인 원장 내 쓰기=허용 / **호출자 밖 쓰기=차단 또는 카드 승격**」. 초안은 등급을 «호출자 밖 쓰기» 로 선언하고 「오염된 turn 의 호출은 back 이 거부」라 적었다 — 원문의 «차단» 갈래를 택한 것이라 왜곡 아님.
- **위계 오독 방지 장치가 양쪽에 박혔다** — SPEC-013 §3 ▸ 형태(`:140`)와 SPEC-060 §4(`:357`) 둘 다 「①~④ 는 «좁히고 관측한다» 2층이지 «경로를 없앤다» 1층이 아니다 · 이 예외를 「오염 게이트가 있으니 즉시형이어도 된다」의 선례로 읽으면 안 된다」를 적었다. 2026-08-25 처분표 3종(1층 처리)과 **다른 층임을 명시**해 선례 오용을 차단한다.
- **소유 분리 정확** — 형태(즉시형/카드형) 계약은 도메인 SPEC 소유라는 §4 규율대로, 판단·근거·미결은 SPEC-013 이 owns 하고 SPEC-060 은 「예외가 섰다는 사실과 위계」만 기록한다.
- **OQ 규약 준수** — 신규 OQ 3건(a 즉시형/카드형 · b 감사 표기 · c leaf 부여 범위)은 **신규 `MEDINESS-OPEN-013-*` ID 를 발급하지 않고 prose 라벨**로 뒀다. 이는 §6 의 2026-06-17 절이 세운 「OPEN-* 는 동결 레거시 → prose」 규약 그대로이며, lint ERROR 0 이 매달린 참조가 없음을 실증한다. OQ-a 는 ⓐⓑⓒ 선택지에 **각각 «감수(무엇을 잃는가)»** 를 붙이고 판단 축까지 제시해 사용자 리뷰에 바로 올릴 형태다. (지시자 문구만 W-2)

### ⑤ SPEC-003 수정이 최소인가 ✅ 최소 — 본문 2행 + `last_updated`

- 전수: ⓐ `last_updated` 2026-08-12→2026-08-28 ⓑ §3.2 leaf index **1행 추가**(`:248`) ⓒ §3.3 cutover 전환 영향표 **1행 추가**(`:333`). 그 외 본문·계약 변경 **0**.
- ⓒ 는 scope creep 이 아니다 — 그 표는 「동형/비동형」 분류표이고, 특정 역할에만 부여되는 신규 leaf 는 **비동형**이라 등재 대상이다. 선례 2건이 같은 형식으로 이미 있다: `action.runtime.read_all`(「비동형 · 신규 leaf」) · `task.delete`(「비동형 · 신규 leaf」). 신규 행도 같은 라벨·같은 서술 구조를 쓰고, 「**누구의 권한도 «줄지» 않는다** — `basic` 은 불변, 새로 여는 문에만 붙는다」로 웹 불변을 이 표에서도 재확인한다.
- **한 곳 원칙 준수** — 두 행 모두 「역할 구성 정의는 소유 SPEC」이라 명시하고 실제 역할 매트릭스는 SPEC-013 §3 권한에만 둔다. SPEC-003 은 index(키 존재 + 소유 위치)만 갖는다는 §3.2 하단 bullet 그대로.
- 다만 ⓑ 의 **행 분리 형태**는 W-1 참조.

### ⑥ frontmatter `status: stable` 유지 + ⏳ 라벨 처리가 lint 게이트상 타당한가 ✅ 타당 — 사실상 **유일한 lint-legal 선택**

- `scripts/lint-pipeline.py` 의 **생명주기 5→6 게이트는 ERROR(block)** 다: 「Spec Coverage derive 값이 `in_dev`/`done` 인데 SPEC frontmatter `status` 가 `draft` 면 ERROR」(`rules/document-pipeline.md` §자동 검증).
- 실측 — `30-work.md` §Spec Coverage: **SPEC-013 = `done`**(WP-052·WP-090) · **SPEC-060 = `done`**(WP-057·075·096·097) · **SPEC-003 = `in_dev`**(WP-085·WP-104). ⇒ 세 SPEC 중 어느 하나라도 `status: draft` 로 내리면 **즉시 blocking ERROR** 가 난다.
- 의미상으로도 맞다 — frontmatter `status` 는 **문서 전체의 계약 성숙도**이지 절 단위 플래그가 아니다. 이미 구현·운영 중인 계약 전체를 미확정으로 표시하면 거짓이 된다. 신설 절만 ⏳ + 「사용자 리뷰 전 — 확정 아님」으로 격리한 처리가 정확하다.
- 브리프 §6.5 「개정은 draft 상태로 둔다 — accepted 단정 금지」의 **취지(확정 단정 금지)는 충족**됐다: 신규 계약면 전부(⏳ 머리 블록 · API 표 행 · leaf 표 행 · Validation 3행 · 케이스 매트릭스 2행 · AC 8항목 · SPEC-060 §4 신설 규범 · SPEC-003 2행)에 ⏳/「초안」 표기가 붙어 있고, 확정 표현은 한 곳도 쓰지 않았다.

### ⑦ 추가 대조 — 초안이 인용한 외부 사실의 실재 확인 (전건 통과)

| 초안의 주장 | 대조 결과 |
|---|---|
| `MEDINESS-OPEN-060-C` = 공통 에러 enum 에 권한 거부 코드 없음 | ✅ `spec-060-mcp-surface.md:481` 실재. 인용 내용(403 이 `NOT_FOUND`/`UPSTREAM_ERROR` 로 뭉개짐 → 둘 다 틀린 행동) **원문 그대로**. 「이 초안이 그 OQ 를 해결하지 않는다」로 소관 분리도 정확 |
| `requires_tools = product_list` 의 대상 툴 실재 | ✅ `mediness.product_list`(domain product-catalog, SPEC-050) 인벤토리 `:195` 실재. `spec-050-product-catalog.md` 파일 실재 |
| 「조용히 포기」 실측 사고 = SPEC-230 §3 | ✅ 동일 근거로 이미 `task_update_request` 등재 개정(`:67`)이 쓰던 선례. 재사용 정확 |
| `delete` 미개방 근거 ① 「[삭제] + 부서 스페이스 `[발행 취소]` 두 경로가 있다」 | ✅ `spec-129-department-space.md` 실재 + `[발행 취소]` CTA 실재(`:252`, W-7 확인 다이얼로그) |
| `delete` 미개방 근거 ② 「restore endpoint 없음(§2 S-3)」 | ✅ SPEC-013 `:44` 가 「본 SPEC 에 **restore endpoint 가 없다는 점**(§2 S-3 — 복원 = 같은 path 로 다시 upload)」을 이미 명문화 |
| 256 KiB 근거 ③ 「`read_file` 1회 반환 상한 50 KiB(`CONTENT_MAX_BYTES`, 코드 SoT)」 | ✅ `mediness-app/mcp/app/tools/read_file.py:28` = `CONTENT_MAX_BYTES = 50 * 1024`. **코드와 일치** |
| leaf 부여 선례 「`landing_chat.usage.read` · `prompt.version.*` · `voice.profile.*` = `system_admin` only」 | ✅ SPEC-003 `:255`(usage.read = system_admin only) · `:328-329`(prompt/voice = `system_admin` 전용 유지). 3건 전부 실재 |
| 착지 시 갱신 수치 「write **18→19** · `/health` **57→58**」 | ✅ 현행 정본과 일치 — §Tool 인벤토리 헤딩 `:173` = 「(read 39 + **write 18**)」, §5 AC `:443` = 「write tool **18**개」, `:445` = 「`/health` 카운트 **57**」 |
| 「인벤토리 표의 행·카운트는 이번에 바뀌지 않는다(2026-08-13 실측 일치 규약)」 | ✅ diff 상 인벤토리 write 표에 행 추가 0, 헤딩 카운트 변경 0. 기존 ⏳ 예고 주석에 ③ 으로만 편입 — **선례(① 회의 재배선 · ② 샤라웃 2종)와 동일 처리** |
| SPEC-003 §3.7 = 권한 부족 오류 계약 | ✅ `:378` 실재 (`403 CAPABILITY_REQUIRED` 계약 자리) |

---

## 확인한 것 (PASS 근거 — planner 체크리스트 전항)

- **린트** ✅ `python3 scripts/lint-pipeline.py --strict` → **0 error**, 255 warning, exit 0. **mediness 범위 ERROR 0.**
  - mediness WARN 은 **1건뿐이고 이번 diff 와 무관**: `products/mediness/30-work.md:227` — SPEC-030 Spec Coverage 구현 상태 `in_dev` ≠ derive `done`(WP-045/089/090/113 전부 done). 이번 diff 는 `30-work.md`·SPEC-030 을 건드리지 않았다 ⇒ **선재 부채**.
  - 나머지 254 WARN 은 **전부 타 제품**(`procedure-hub`·`selly` 의 frontmatter `version`/`doc_no` 누락, 20-spec.md/30-work.md frontmatter 부재) — **무관**.
- **WP 갱신** ✅ **해당 없음 — 정상.** 이번 태스크는 스펙 개정 초안까지이고(브리프 §7 「WP·코드 작성 금지」), diff 에 `30-work/`·`30-work.md` 가 없다. 새 WP 가 없으므로 WP List·Status Board·Spec Coverage 갱신 의무가 발생하지 않으며, lint 의 3자 일치·map 동기 검사도 ERROR 0 로 통과.
  - ⚠ 뒤집어 말하면 **이 계약을 구현할 WP 는 아직 없다** — 사용자 리뷰 통과 후 WP 발주가 남았다(생명주기 5→6 게이트: 세 SPEC 모두 이미 `stable` 이라 WP 생성 전제는 충족).
- **spec↔WP 정합** ✅ 신규 WP 참조 0. 기존 WP 본문과 어긋나는 서술 없음 — 초안은 기존 WP(WP-052/090/116 등)의 착지 사실을 **바꾸지 않고 인용만** 한다.
- **frontmatter** ✅ 4개 SPEC/맵 문서 전부 `doc_no` 보유·**무변경**(`20-spec.md`=DOC-85 · SPEC-003=DOC-198 · SPEC-013=DOC-90 · SPEC-060=DOC-100). `id`/`type`/`title`/`status`/`owner`/`version` 무변경, `last_updated` 만 2026-08-28 로 갱신(3파일). doc_no 전역 유일성 ERROR 0.
  - `sources` 추가 1건 — SPEC-013 에 `20-spec/spec-060-mcp-surface.md` 추가. 실제 lineage 가 생겼으므로 타당(D4 lineage 규약 방향과 일치).
- **coverage 상태 규칙** ✅ Spec Coverage 표 무변경. 커버 WP 상태가 안 바뀌었으므로 derive 값도 불변이며, lint 의 derive 검증이 mediness 에서 SPEC-030(선재 부채) 외 WARN 을 내지 않는다.
- **인덱스 동기** ✅ 신규/삭제/rename SPEC 파일 0 ⇒ `20-spec.md` SPEC List 변경 불필요. `20-spec.md` 는 「최종 수정」 헤더 1줄만 갱신했고, 그 서술이 diff 내용과 일치(툴 이름·라우트·leaf·`delete` 미개방까지 정확).
- **`log.md` 규약** ✅ 표 최상단에 `2026-08-28 | spec-change | MEDINESS-SPEC-013, MEDINESS-SPEC-060, MEDINESS-SPEC-003 | — | …` **1행 prepend**(역시간순 유지). `종류` enum 적법(`spec-change`), `영향 ID` 3건이 콤마+공백으로 나열되고 세 파일과 정확히 대응.
  - `PR` 칸 `—` 은 **기존 관행과 일치** — 미머지 문서 라운드 행이 같은 표에 다수 있다(`:21`·`:23`·`:26`). 규칙이 금지한 것은 「`proposal` 같은 모호한 단어 단독」이지 미머지 표시가 아니다.
  - 요약 깊이도 규약대로 — `spec-change` 는 1줄 원칙이나 이 행은 설계 판단(전용 라우트 vs 툴 leaf)의 근거를 담아 다소 길다. 결정 성격의 근거 기술이라 허용 범위로 본다.
- **한 곳 원칙** ✅ 계약 본문은 SPEC-013 `### MCP 계약` 한 곳이 owns 하고, SPEC-060 은 「공통 surface 쪽 귀결만」·SPEC-003 은 「index 만」으로 각각 자기 자리 것만 갖는다. 파라미터 표·형태 근거·보상 통제표가 **SPEC-060 에 복제되지 않았다**(SPEC-060 은 「owns 는 SPEC-013」이라 링크만).

---

## 기존 부채 (이번 판정 제외)

1. **SPEC-060 내부 write 카운트 모순 (선재).** §Tool 인벤토리 헤딩 `:173` 은 「read 39 + **write 18**」, §5 AC `:443` 도 18 인데, 같은 절 리드 문단 `:176` 과 §4 read/write 경계 `:345` 는 여전히 「**write tool 19개**」다. 2026-08-25 `decision_register` 등록 해제(19→18) 때 두 자리가 안 따라온 잔재로 보인다. **이번 diff 는 이 4자리 중 어느 것도 건드리지 않았고**(초안은 정본인 18 을 기준으로 18→19 를 적어 올바르다), 별도 라운드에서 정리 대상.
2. **`30-work.md:227` SPEC-030 Spec Coverage derive 불일치 (선재 WARN).** 위 린트 항목 참조.
3. **워크트리가 `origin/mediness` 보다 1 커밋 뒤.** PR 전에 코디네이터가 `origin/mediness`(`15459cd04`, #652 회의 WP 마감) 를 반영해야 한다. 다만 #652 의 변경 파일(`30-work.md`·`30-work/work-120·121`·`spec-031`·`00-baseline/BL-003`)과 이번 diff 5파일은 **교집합 0** 이라 충돌 위험은 없다.

---

## 코디네이터에게 남기는 판단 포인트

1. **W-1 (SPEC-003 index 행 분리)** — 지금 병합할지, ⏳ 격리를 유지하다 확정 시 병합할지.
2. **사용자 리뷰에 올릴 미결 3건이 SPEC-013 §6 에 정리돼 있다** — OQ-a(즉시형 예외 확정 vs 카드형 승격)가 가장 무겁다. 초안은 ⓐ(즉시형 + 예외 명시)를 제안하며 감수 사항까지 적었으므로, 사용자에게는 **「관리자 세션이 오염됐을 때 문서 1건이 baseline 3영역에 승인 없이 올라가는 것을 감당할 수 있는가」** 한 문장으로 물으면 된다(초안이 제시한 판단 축).
3. **다음 단계는 WP 발주** — 세 SPEC 모두 `stable` 이라 생명주기 5→6 게이트는 이미 충족. 단, 이번 개정분이 ⏳ 초안이므로 **사용자 확정 후** 발주가 순서다.

---

# 재검수 (2차, 2026-08-28)

## 판정: PASS

1차 경미 2건(W-1·W-2)이 **둘 다 해소**됐고, 증분(수정 6 + 신규 1)에 **새 위반 0**.
`--strict` lint 는 여전히 **mediness 범위 ERROR 0**, mediness WARN 은 선재 1건뿐이다.
아래 «참고» 3건은 위반이 아니라 코디네이터가 알고 있으면 되는 사실이다.

---

## 검수 범위 (증분)

- 1차와 같은 산정 — 워커 산출물은 **커밋되지 않은 working-tree 변경**이고 `HEAD`(`5ab09c2aa`)는 여전히 `origin/mediness` 보다 1 커밋 뒤(`rev-list --left-right --count` = `1 0`). 실제 범위는 `git diff HEAD` + untracked.
- 파일 **7개** (tracked 6 + untracked 1):

  | 파일 | 변경량 | 1차 대비 |
  |---|---|---|
  | `products/mediness/20-spec/spec-013-baseline-publish.md` | +121 / −4 | 개정 (⏳→확정 전환 · OQ-a 해소 · 승격 재검토 조건 신설) |
  | `products/mediness/20-spec/spec-060-mcp-surface.md` | +22 / −3 | 개정 (동일 전환) |
  | `products/mediness/20-spec/spec-003-capability-rbac.md` | +5 / −2 | **W-1 해소** (2행 → 1행 병합) |
  | `products/mediness/20-spec.md` | +1 / −1 | 헤더 1줄 재작성 |
  | `products/mediness/30-work.md` | +10 / −4 | 🆕 Board·WP List·Spec Coverage 3행 |
  | `products/mediness/log.md` | +3 / −1 | 헤더 + entry 1행 (`spec-change, wp-add`) |
  | `products/mediness/30-work/work-123-mcp-baseline-publish.md` | 신규 239행 | 🆕 |

- **allowed_paths 이탈 0.** 7파일 전부 `products/mediness/` 아래.

### 실행한 검사

```
git diff --stat HEAD / git status --porcelain / git rev-list --left-right --count
python3 scripts/lint-pipeline.py --strict          → 0 error, 255 warning (exit 0)
doc_no: grep -rhoE "MEDINESS-DOC-[0-9]+" → max = 243, 중복 0
코드 대조(read-only, origin/dev @ mediness-app/user-dashboard):
  git ls-tree / git grep 로 Code Surface 12행의 파일·심볼·선례 전건 확인
```

---

## 위반 (FAIL 사유)

**없음.**

---

## ① 1차 경미 2건 — **둘 다 해소**

### W-1 (SPEC-003 §3.2 index 행 분리) ✅ 해소 — 권장 ⓑ 채택

- `spec-003-capability-rbac.md:247` — 별행이 사라지고 **기존 `baseline` 행의 leaf 칸에 병합**됐다: `` `baseline.publish.basic` `baseline.publish.agent` ``. 1차에서 근거로 든 **선례 8건과 동형**(`action` 행 등 — 같은 소유 SPEC 의 다중 leaf 는 한 칸에 나열).
- 비고 칸에 신규분만 구분되게 서술이 붙었고(`agent` = … 2026-08-28 확정 · 구현 WP-123 착지 시 발효 · `system_admin` only), **「`basic` 은 좁혀지지 않는다」 경고가 이 칸에도 남았다.**
- §3.5 비동형 표 행(`:332`)은 그대로 별행 — 그 표는 애초에 **leaf 1개 = 1행** 구조라 병합 대상이 아니다. 처리가 두 표에서 각각 맞다.

### W-2 (§6 지시자 문구) ✅ 해소 — 대상이 실재한다

- `spec-013-baseline-publish.md:588` — 「§6 머리 규약 그대로」가 **「아래 «양식 개정 신규 OQ» 절이 2026-06-17 에 세운 처리 그대로다」** 로 정정됐다.
- **위치 관계까지 맞다** — 신규 절 `### MCP 경유 발행 OQ` = **:586**, 참조 대상 `### 양식 개정 신규 OQ (2026-06-17…)` = **:594**. 「아래」가 사실이다.

---

## ② OQ-a 닫힘 — 사용자 결정 그대로인가 ✅ **그대로. 결정 밖 내용 추가 0**

요구 3요소를 하나씩 대조했다.

| 사용자 결정 | 반영 자리 | 판정 |
|---|---|---|
| **즉시형 예외 확정** | `spec-013:588` OQ-a 가 `~~취소선~~` + **「해소 (2026-08-28 사용자 확정) — ⓐ 즉시형 유지 + «예외» 명시」**. §3 ▸ 형태 리드(`:332` 부근)도 「⇒ 즉시형으로 열되 «예외» 로 명시」로 확정형 전환 | ✅ |
| **보상 통제 4건 유지** | §3 ▸ 형태의 4행 표 그대로 — ① 노출 인구 `system_admin` ② 화이트리스트 파급 고정 ③ 전건 추적·revert ④ 오염 turn 차단. **1차 검수 때와 항목·문구 동일**(추가·삭제 0) | ✅ |
| **「Action Runtime 배선이 baseline 도메인에 닿으면 카드형 승격 재검토」 명문화** | §3 ▸ 형태에 **`**승격 재검토 조건 (계약)**`** 문단 신설. 「이 예외는 «영구» 가 아니라 «지금 배선이 없어서» 성립 … 그 전제가 사라지면 근거도 사라진다 ⇒ **Action Runtime 배선이 baseline 도메인에 닿는 시점**에 카드형 승격을 재검토한다」 | ✅ |

- **소유·전파도 규율대로다.** 조건의 **owns 는 SPEC-013**(형태 계약 = 도메인 SPEC 소유, SPEC-060 §4 규율)이고, `spec-060:358` 은 「상세와 **승격 재검토 조건**은 [SPEC-013 §3 ▸ 형태] 에 있다」로 **링크만** 건다. WP-123 §배포 후 확인 축(`:214`)도 「닿으면 그 조건이 발동한다」로 참조만. **복제 0.**
- **결정에 없는 내용이 붙지 않았는지** — 새로 늘어난 것은 ⓐ 재검토 시 **판단 축 2줄**(① 카드형이 더 이상 «신설» 이 아니라 기존 배선 재사용인가 ② 승인자와 호출자가 갈리는가) ⓑ **「재검토를 «해야 한다» 는 것이 계약이고, 결과가 반드시 승격이라는 뜻은 아니다」** 한 줄. 둘 다 **1차 초안의 OQ-a ⓑ 기각 사유에 이미 있던 문장의 재배치**이며(초안 원문: 「승인자가 곧 호출자(`system_admin`)라 게이트가 「사람이 봤다」를 얼마나 보증하는지 불확실」), **새 정책·새 의무를 만들지 않는다.** ⓑ 는 오히려 조건의 범위를 좁히는 방향이라 과잉 확정이 아니다.
- **OQ-b·OQ-c 는 열린 채 유지** ✅ — prose 라벨, 신규 `MEDINESS-OPEN-013-*` ID 발급 0(lint ERROR 0 로 실증). §메타 `Open Questions` 줄(`:55`)도 「MCP 경유 발행 OQ 2건 … 형태 OQ 는 «즉시형 예외» 로 해소」로 동기됐다.

---

## ③ ⏳ 라벨 정리 ✅ 일관 + 인벤토리 예고 주석 유지

- **「사용자 리뷰 전 — 확정 아님」 계열 표기 잔존 0** — 4개 문서(`spec-013`·`spec-060`·`spec-003`·`20-spec.md`)에 `사용자 리뷰 전` / `확정 아님` / `(초안)` grep **전건 0 hit**. 전부 **「2026-08-28 사용자 확정」** 으로 전환됐다.
- **남은 ⏳ 는 전부 «구현 미착지» 의미로만 쓰인다** — 의미가 갈리지 않는다:
  - `spec-013:303` 「구현 착지 전까지 인벤토리 표에 행으로 세지 않는다 … ⏳ 예고 주석으로만」
  - `spec-013:312` 툴 정의 표 «대응 REST … (⏳ 신설)»
  - `spec-060:177` 인벤토리 ⏳ 블록
  - `spec-060:246` DEC-010 컨벤션 나열의 「⏳ `publish`(… 착지 시 등재)」
  - `work-123:83`·`:180` 인벤토리 착지 갱신
- 🔑 **SPEC-060 인벤토리 예고 주석 유지 ✅** — `:177` 이 **「⏳ … 3건」**(2건 → 3건)으로 늘고 ③ 이 추가됐다. **표의 행·카운트 변경 0**(write 표 행 추가 0, 머리 카운트 무변경) — 1차에서 확인한 2026-08-13 「실측 일치 표」 규약 그대로이며, 선례 ①②(회의 재배선 · 샤라웃 2종)와 **동일 처리**다.
- 계약 확정과 구현 미착지가 **두 축으로 분리돼 표기된다** — 계약면은 「확정」, 인벤토리·라우트는 「⏳ 미착지」. `20-spec.md` 헤더도 「**SPEC List Status 변경 없음** — 세 SPEC 다 `stable` 유지[계약 확정 · 구현 미착지는 Spec Coverage 축이 소유한다]」로 축 분리를 명시했다. 1차 ⑥ 의 lint 게이트 논리와 정합.

---

## ④ WP-123 — WP 규약 ✅ 전항 통과

### 형식·frontmatter

- **1 파일 = 1 WP** ✅. `## Scope` / `## Code Surface` / `## Domain / Schema` / `## Execution`(Phase별 Status·설명·작업·검증·완료 증거) / `## Pre-deploy Check` / `## Rollback` / `## Open Issues` / `## Related` — `rules/document-pipeline.md` §Work Tracking 의 기본 본문 전항 존재. **`PR Plan`·`Dev Plan` 별도 절 없음** ✅.
- 추가 절 2개(`## ⚠ 비동형 예고` · `## 배포 후 확인 축`)는 **선례 7건씩** 존재(`work-099`·`109`·`110`·`112`·`120`·`121`·`122`) — 신설 형식이 아니다.
- **frontmatter 필수 필드 전건** ✅ `id: MEDINESS-WP-123` · `type: work` · `title` · `status: proposed` · `owner: TBD` · `last_updated: 2026-08-28` · `covers`(3) · `depends_on: []`.
- **`doc_no: MEDINESS-DOC-243` — 중복 0 · 발번 규칙대로** ✅. 현행 + `90-archive/` 전체 스캔 결과 max = **243**(직전 242) ⇒ **max+1**. lint 의 doc_no 전역 유일성 ERROR 0.
- **파일명 NNN ↔ 본문 ID 일치** ✅ (`work-123-*` ↔ `MEDINESS-WP-123`, lint 통과).
- **SPEC 본문 복제 0** ✅ — 파라미터 표·보상 통제 표·케이스 매트릭스·AC 어느 것도 옮겨오지 않고 **전부 `[SPEC-013 §3 …](../20-spec/…)` link**. 본문 첫 줄이 「계약은 SPEC-013 §3 이 소유하며 **본 WP 는 그 빌드 계획**」으로 역할을 선언한다.
- **문서 링크 대상 실재** ✅ — `work-092`·`work-102`·`work-116`·`spec-050`·`spec-129`·`spec-150`·`spec-230` 7건 전부 파일 존재.

### `covers` 3건 타당성 ✅

| covers | 이 WP 가 그 SPEC 의 무엇을 구현하나 | 판정 |
|---|---|---|
| `MEDINESS-SPEC-013` | `### MCP 계약` 본문 전체 + API 계약 `agent-publishes` 행 + 권한 leaf + Validation 3행 + AC 9항목 | ✅ 주 계약 |
| `MEDINESS-SPEC-060` | §4 신설 규범(«전용 라우트» 처방)의 **첫 사례** + 즉시형 예외 + **인벤토리 착지 갱신**(P4 작업 항목에 실제로 있음 `:180`) | ✅ 착지 의무가 WP 안에 있음 |
| `MEDINESS-SPEC-003` | §3.2 index leaf 의 **카탈로그 구현**(migration `capability` 1행 + `access_role_capability` 1행) + §3.5 비동형 | ✅ P1 이 그 몫 |

`covers` 에 넣지 않은 SPEC(`spec-230`·`spec-050`·`spec-129`)은 **참조만** 하며 `## Related` 에 있다 — 규약대로.

### Code Surface 12행 — 실코드 spot-check ✅ **12/12 정합** (`origin/dev` 기준)

전수 아닌 파일·심볼 존재 확인 수준으로 대조했고 **어긋난 행이 없다**.

| WP 가 지목한 것 | 실측 |
|---|---|
| `back/app/routers/baseline_publish.py` — `_publish_form` · `_last_publish_row` | ✅ 파일 존재 · `_publish_form` 존재 · `_last_publish_row` `:61` |
| `back/app/schemas/baseline_publish.py` — 응답 모델 `BaselinePublishResponse` **재사용** | ✅ `class BaselinePublishResponse` **`schemas/baseline_publish.py:14`** (WP 서술과 자리 일치) |
| `back/app/services/publish/baseline_form.py` — `prepare_upload` · `AppError` 서브클래스 패턴 | ✅ `def prepare_upload` 존재 · `from app.core.errors import AppError` `:17` |
| `BaselinePublisher.publish` · `publish_lock` · `GitClient` **무변경 재사용** | ✅ `services/publish/baseline_publisher.py` · `publish_lock` · `services/publish/git_client.py` 전건 실재 |
| `mcp/app/server.py` — `_wrap_write_tool` 경유 | ✅ `mcp/app/server.py:558` |
| `access(capability=…, needs=(…), taint_policy=TAINT_BEYOND_CALLER)` | ✅ `TAINT_BEYOND_CALLER`·`assert_write_tools_declare_taint` = `mcp/app/tool_access.py`+`server.py`. `needs=("…_tool",)` 튜플 컨벤션 = 기존 8건 이상 동형(`needs=("list_dir_tool", "repo_search_tool",)` 등) |
| `needs=("product_list_tool",)` 의 대상 함수 | ✅ `async def product_list_tool(...)` `mcp/app/server.py:788` — **이름까지 정확** |
| `mcp/app/server.py` — `_health` 하드코딩 카운트 | ✅ `async def _health` `:1770`, 바로 아래 `:1777` 주석이 「`test_health_constant_matches_registration` 이 실 등록 수와 대조한다」 |
| `mcp/tests/test_tool_inventory.py` — `EXPECTED_WRITE`·`EXPECTED_WRITE_TOOLS` | ✅ `:29-31` `EXPECTED_READ = 40` / `EXPECTED_WRITE = 20` · `EXPECTED_WRITE_TOOLS` 존재 · `test_health_constant_matches_registration` `:135` |
| `mcp/tests/test_tool_access_declaration.py` | ✅ 존재 |
| migration 선례 `0095_landing_chat_usage_read.py` / 테스트 선례 `test_0086_landing_chat_usage_read.py` | ✅ 둘 다 실재 |
| 「착수 시점 최신 = `0133_landing_turn_taint`」 | ✅ `origin/dev` 최신 = **`0133_landing_turn_taint.py`** (그다음이 없음) — **실측 정확** |
| P4 지목 테스트 범위(웹 발행 무회귀 · 발행 서비스 · capability 축) | ✅ `back/tests/api/test_baseline_publish.py` · `back/tests/services/test_baseline_form.py`·`test_baseline_publisher.py` · `back/tests/api/test_capability_catalog.py`·`test_capability_resolver.py`·`test_me_capabilities.py` 전건 실재 |

### 비목표 ↔ 계약 모순 ✅ **없음** (7항목 전건 대조)

| 비목표 | 계약 쪽 근거 | 모순? |
|---|---|---|
| `delete` operation 개방 | SPEC-013 §3 ▸ operation 범위 「`delete` 는 이번에 열지 않는다」 | 없음 |
| 카드형(Action Runtime) 배선 | §3 ▸ 형태 = 즉시형 예외 확정 | 없음 |
| `baseline_publishes` 스키마·commit message 포맷 변경 | §3 ▸ 감사 「컬럼을 더하지 않는다 · 포맷 불변」 | 없음 |
| binary/이미지 첨부 | §4 스코프 외 (기존 계약) | 없음 |
| 웹 발행 UI·endpoint·leaf 변경 | §3 API 계약 주석 「웹 3 endpoint 는 영향받지 않는다」 | 없음 |
| 공통 에러 enum 에 권한 거부 코드 추가 | §3 ▸ 출력 「이 툴이 그 OQ 를 해결하지 않는다 — 공통 enum 은 SPEC-060 소관」 | 없음 |
| `agent` leaf 를 `system_admin` 밖으로 확대 | §6 OQ-c 열림 「선제적으로 넓히지 않는다」 | 없음 |

- **비목표가 계약을 «축소» 하지도 않는다** — 계약이 여는 것(upload·update 2종 · 256 KiB · JSON body · 두 층 차단)은 전부 Scope 포함에 있고 Phase 로 배치됐다.
- **Phase 순서에 근거가 있다** ✅ — 「P1(leaf)이 P2(라우트)보다 먼저 — 라우트가 존재하지 않는 leaf 를 요구하면 `system_admin` 도 403 이라 «좁게 열었다» 와 «잘못 만들었다» 가 구분되지 않는다」. Pre-deploy Check `:201` 이 같은 순서를 배포 축에서 다시 건다.
- **`Status:` 라인 형식** ✅ — 4 phase 전부 `- **Status**: TODO` (enum만, 뒤에 텍스트 0). lint 의 형식 위반 검사 통과. phase 전부 미완 + frontmatter `proposed` ⇒ 7→8 게이트 정합.

---

## ⑤ `30-work.md` 3자 일치 ✅ + SPEC-013 derive 타당 ✅ + 5→6 게이트 통과 ✅

- **세 곳 모두 반영** ✅
  - `## Status Board` `:111` — `MCP 도서관 발행 | MEDINESS-WP-123 | … | proposed | TBD | 2~3d | TBD | — | — | — | 사용자 리뷰 후 구현 발주`. 표준 컬럼 배열 준수.
  - `## WP List` `:194` — `MEDINESS-WP-123 | … | proposed | TBD | [work-123-…] | MEDINESS-SPEC-013, MEDINESS-SPEC-060, MEDINESS-SPEC-003`. **Covers 3건이 frontmatter `covers` 와 일치.**
  - `## Spec Coverage` — **3행 동기** (`:226` SPEC-013 · `:234` SPEC-060 · `:255` SPEC-003) 전부 covering WP 칸에 `MEDINESS-WP-123` 추가.
- **3자 Status 일치** ✅ frontmatter `proposed` = Status Board `proposed` = WP List `proposed`. lint 의 ERROR 급 3자 일치 검사 통과(0 error).
- **SPEC-013 derive `done`→`in_dev` 타당** ✅ — covering = WP-052(`done`)·WP-090(`done`)·**WP-123(`proposed`)**. 전부 `done` 이 아니게 됐으므로 `done` 유지는 거짓이 된다. lint 의 derive 검증이 **SPEC-013 에 WARN 을 내지 않는다**(유일한 mediness WARN 은 선재 SPEC-030 건) ⇒ 표 값과 lint 의 derive 가 일치함이 기계적으로 실증됐다.
  - SPEC-060·SPEC-003 은 **원래 `in_dev`** 였고 `proposed` WP 하나가 더해져도 derive 가 안 바뀌므로 유지가 맞다. ✅
  - ⚠ **1차 리포트 ⑥ 의 «SPEC-060 = `done`» 은 부정확했다** — diff 의 `-` 라인 실측 결과 그 행은 이번 변경 **이전에도 `in_dev`** 였다. 다만 ⑥ 의 결론(세 SPEC 다 `status: stable` 유지가 lint-legal 유일해)은 **`in_dev` 여도 5→6 게이트가 동일하게 걸리므로 그대로 성립**한다.
- **생명주기 5→6 게이트 통과** ✅ — WP 생성 전제 = covering SPEC 전부 `stable`. 실측: SPEC-013 `stable` · SPEC-060 `stable` · SPEC-003 `stable`. `draft` 0 ⇒ 에이전트 행동 규칙·lint backstop 둘 다 충족.
- **인덱스 동기** ✅ — 신규/삭제/rename SPEC 파일 0 ⇒ `20-spec.md` SPEC List 무변경(헤더 1줄만 갱신, 그 서술이 diff 내용과 정확히 대응). WP 파일 ↔ WP List 동기 ERROR 0.
- **`log.md` 규약** ✅ — 표 최상단 1행 prepend(역시간순 유지). `종류` = **`spec-change, wp-add`**(복합 결합 적법, `version-cut` 아님) · `영향 ID` = SPEC-013, SPEC-060, SPEC-003, **WP-123** 4건 콤마+공백 · `PR` = `—`(미머지 문서 라운드 선례 다수). 결정 성격 entry 라 요약이 길지만 §요약 규약이 결정 entry 에 허용하는 깊이다.

---

## ⑥ 선재 드리프트 기장 ✅ **WP Open Issues 에 있음** (이번 판정 제외 — 기존 부채)

- `work-123-…:225` 첫 Open Issue 가 정확히 그것이다 — 「계약 문서는 `read 39 + write 18 = 57` 로 적는데 **2026-08-28 `origin/dev` 실측은 `read 40 + write 20 = 60`**(WP-113 착지분이 표에 아직 안 실린 것으로 보인다). 착지 갱신은 «57→58» 을 박는 것이 아니라 **«그 시점 실측 +1»**. **드리프트 해소는 SPEC-060 소관의 별건이고 이 WP 가 떠맡지 않는다.」
- **실측 대조 결과 이 기장이 맞다** ✅ — `origin/dev:mcp/tests/test_tool_inventory.py:29-30` = `EXPECTED_READ = 40` · `EXPECTED_WRITE = 20` (합 60). WP 가 적은 숫자가 코드와 일치한다.
- **소관 분리도 정확** — 드리프트의 정본은 SPEC-060 인벤토리이고, 이번 라운드는 그 표를 건드리지 않는다(⏳ 예고 주석에만 편입). P4 작업 항목(`:180`)도 「⚠ 숫자는 «그 시점 실측» 이 정본」으로 잠갔다.
- 브리프 지시대로 **이번 판정에 넣지 않는다** — 1차 «기존 부채 1» 과 같은 건이며, 이제 **추적 자리가 생겼다**는 점이 개선이다.

---

## 참고 (위반 아님 — 코디네이터 인지용)

1. **로컬 app 워크트리가 `origin/dev` 보다 뒤처져 있다.** `mediness-app/user-dashboard` 는 브랜치 `kknaksss/user-dashboard`, alembic 최신이 `0114_merge_ax_chat_task_wbs_heads.py` 다. WP 가 기준으로 삼은 `0133_landing_turn_taint` 는 **`origin/dev` 에만** 있다 — 그래서 코드 대조를 전부 `git grep origin/dev` 로 했다. **WP 의 결함이 아니라 로컬 체크아웃의 문제**이고, 구현 워커가 착수할 때 fetch/rebase 가 선행돼야 한다는 뜻이다(WP `:76`·`:172` 가 이미 「착수 시 재실사」를 두 자리에 걸어 뒀다).
2. **`owner: TBD`** — WP frontmatter·Status Board·WP List 세 곳 모두 `TBD` 로 **일관**돼 규약 위반은 아니다(`30-work/` 69개 WP 가 같은 상태). 규칙이 정한 대로 **「다음 review 의 open item」** 이라는 것만 남긴다.
3. **워크트리가 `origin/mediness` 보다 1 커밋 뒤 (1차와 동일).** PR 전 코디네이터가 `origin/mediness` 를 반영해야 한다. 이번 증분은 `30-work.md` 를 **건드리므로 1차 때와 달리 교집합이 생긴다** — #652 도 `30-work.md` 를 바꿨다. ⚠ **머지 충돌 가능 자리 = `30-work.md` 의 헤더 「최종 수정」 줄 · Status Board · WP List**(WP-120·121·122 행 근처). 충돌 자체는 정상 병합으로 풀리지만, **병합 후 `python3 scripts/lint-pipeline.py --strict` 재실행**으로 3자 일치를 재확인할 것을 권한다.

---

## 기존 부채 (이번 판정 제외 — 1차에서 이월)

1. **SPEC-060 내부 write 카운트 모순 (선재).** §Tool 인벤토리 헤딩·§5 AC 는 18, 리드 문단·§4 read/write 경계는 19. **이번 diff 도 이 4자리를 건드리지 않았다.** 위 ⑥ 의 실측 드리프트(코드 = 20)와 함께 SPEC-060 소관 별건.
2. **`30-work.md:229` SPEC-030 Spec Coverage derive 불일치 (선재 WARN).** 이번 diff 는 SPEC-030 행을 건드리지 않았다 — **mediness 범위의 유일한 WARN**.

---

## 확인한 것 (PASS 근거 — planner 체크리스트 전항, 2차)

- **린트** ✅ `python3 scripts/lint-pipeline.py --strict` → **0 error**, 255 warning, exit 0. **mediness 범위 ERROR 0**, mediness WARN **1건**(선재 SPEC-030). 나머지 254 WARN 은 전부 `procedure-hub`·`selly` — **무관**. (1차와 동일 수치 = 신규 WARN 0.)
- **WP 갱신** ✅ WP-123 이 `30-work/` 파일 + WP List + Status Board + Spec Coverage **네 자리 모두**에 있고, 세 Status 가 `proposed` 로 일치. 내용 정합도 눈으로 대조(Covers 3건 = frontmatter `covers`, 파일 링크 실재, Scope 요약이 WP 본문과 일치).
- **spec↔WP 정합** ✅ WP 가 참조하는 SPEC 조항(SPEC-013 §3 `### MCP 계약`·§3 API 계약·§4 Functional Rule·§5 AC · SPEC-060 §4 · SPEC-003 §3.2·§3.5)이 **전부 이번 diff 로 실재**하고, WP 본문과 어긋나는 서술 없음. **역방향도 확인** — SPEC 쪽 5자리(`spec-013` 개정 머리·API 표·leaf 표·AC · `spec-060` 개정 머리·⏳ ③ · `spec-003` §3.2·§3.5)가 전부 `WP-123` 을 정확한 상대경로로 가리킨다.
- **frontmatter** ✅ 신규 WP 필수 필드 전건 + `doc_no: MEDINESS-DOC-243`(max+1·중복 0). 수정 4문서는 `last_updated` 만 2026-08-28 로 갱신(+ SPEC-013 `sources` 1건 추가 — 1차에서 타당 확인). `id`/`type`/`status`/`owner`/`version`/`doc_no` 무변경.
- **coverage 상태 규칙** ✅ 「커버 WP 가 전부 done 일 때만 `done`」 — SPEC-013 이 `proposed` WP 를 얻어 `done`→`in_dev` 로 내려간 것이 **이 규칙의 정확한 적용**이다. lint derive 검증이 세 행 모두 WARN 없이 통과.
- **한 곳 원칙** ✅ 계약 본문 = SPEC-013 `### MCP 계약` 단독 owns · SPEC-060 = 공통 surface 귀결 + 위계만 · SPEC-003 = index 만 · **WP-123 = 빌드 계획만**(계약 복제 0, Status Board 복제 0). 승격 재검토 조건도 SPEC-013 1곳 + 링크 2곳.
- **read-only 준수** ✅ 대상 리포 파일 수정·생성·삭제 **0**. 산출물은 이 리포트 1개. git 상태 변경 명령·테스트 실행 **0**.

---

## 코디네이터에게 남기는 판단 포인트 (2차)

1. **막는 것 없음 — 사용자 리뷰 / PR 로 진행 가능.** 1차 경미 2건이 해소됐고 신규 위반 0.
2. **병합 순서만 챙기면 된다** — `origin/mediness`(#652) 반영 시 `30-work.md` 가 **이번엔 교집합**이다(위 참고 3). 병합 후 lint 재실행 권장.
3. **WP-123 은 `proposed` 이고 사용자 리뷰 후 구현 발주가 순서** — WP 자체가 Status Board `다음` 칸에 「사용자 리뷰 후 구현 발주」로 그 순서를 박아 뒀다.
