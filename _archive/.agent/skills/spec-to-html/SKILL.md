---
name: spec-to-html
description: products/<product>/20-spec/ 의 SPEC 문서를 baseline HTML 시안 1 파일로 변환. output mode (ui-mockup/workflow/data-model) 와 다중 SPEC 입력 지원. FE 코드 루트가 주어지면 같은 테마로 통일, 없으면 claude_design/ 최신 디자인 시스템 톤 차용. products/<product>/21-html/ 에 저장하고 product-doc-pipeline hook 을 수행한다. 트리거 "spec-NNN html 만들어" / "MRT-SPEC-003 시안 그려줘" / "/spec-to-html".
allowed_tools: [Read, Glob, Grep, Write, AskUserQuestion, Bash]
runs_scripts:
  - "../../scripts/product_doc_pipeline.py"
---

# spec-to-html — SPEC → baseline HTML 시안

## When to invoke

사용자가 SPEC 본문을 시각적 시안 HTML 로 보고 싶을 때 호출.

**호출 예시:**
- "MRT-SPEC-003 시안 html 그려줘"
- "open-kknaks spec-011 참고해서 html 만들어줘"
- `/spec-to-html OKK-SPEC-005 mode=ui-mockup`
- `/spec-to-html STL-SPEC-001,002 mode=ui-mockup`
- `/spec-to-html AXKG-SPEC-001..003`
- "이 spec 어떻게 보이는지 baseline html 만들어"

**호출하면 안 되는 경우:**
- SPEC 작성·정정·코드 대조 — `/code-compare-spec` 등 별도 skill
- 실제 FE 코드 생성 — 코드는 별도 레포. 이 skill 산출물은 문서 SoT 안의 *시안*이다
- 회의록·log HTML 변환 — 별도 도구

## Output Mode

HTML 산출물의 성격을 결정하는 세 가지 mode:

| mode | 용도 | 대상 독자 |
|---|---|---|
| `ui-mockup` | end-user/운영자가 보는 실제 화면. dashboard, 카드, chip, badge, form, status indicator. **SPEC 에 `## 3. User Scenario` (S-N) 절이 있으면 Interactive Demo Player 자동 활성 (Step 5 참조).** | 나(제품 결정), 포트폴리오 열람자 |
| `workflow` | pipeline 단계 다이어그램. state machine / 데이터 handoff / 화살표 흐름 | 개발자 관점 검토 |
| `data-model` | 도메인 ERD / 필드 카드. 데이터 구조 시각화 | 개발자 관점 검토 |

mode 생략 시 → Step 2 에서 SPEC 본문 시그널로 자동 추론, 모호하면 AskUserQuestion.

## Procedure

### Step 1 — 호출 파싱, SPEC/제품 해석

**SPEC ID 추출 — 단일 또는 다중:**
- 단일: `MRT-SPEC-003`, `spec-011` (+ product slug)
- 다중 명시: `SPEC-NNN,NNN,NNN`
- 범위: `SPEC-NNN..NNN` (예: `AXKG-SPEC-001..003` → 001, 002, 003)

**product 해석 — prefix 테이블을 하드코딩하지 않는다.** 제품이 계속 늘어나므로 런타임에 해석한다:

1. prefix 가 있으면 (`MRT-SPEC-*` 등) → `Grep` 으로 `products/*/20-spec/spec-*.md` frontmatter 의 `id: <PREFIX>-SPEC-` 매치를 찾아 product 디렉토리 확정
2. product slug 가 인자로 오면 (`open-kknaks spec-011`) → 그대로 사용
3. prefix 없는 bare `SPEC-NNN` 이 여러 제품에 매치되면 → AskUserQuestion 으로 제품 선택. 임의 결정 금지

**mode / references 인자 (선택):**
- `mode=ui-mockup` / `mode=workflow` / `mode=data-model`
- `fe_root=<절대경로>` — 스타일을 차용할 FE 코드 루트 (Step 3 참조)
- `references=<경로>` — 명시적 reference 시안 경로

### Step 2 — SPEC read + mode 추론

`products/<product>/20-spec/spec-NNN-*.md` 를 Glob 으로 찾아 Read. 다중 SPEC 이면 전부 Read.

**output_mode 자동 추론 (mode= 미지정 시)** — 이 레포 spec 템플릿(`templates/product/20-spec/spec.md`) 섹션을 시그널로 쓴다:

| SPEC 본문 절 | 추론 mode |
|---|---|
| `## 2. UX Contract` / `### U-N` / `### Placement` | `ui-mockup` |
| `## 3. User Scenario` / `### S-N` | `ui-mockup` **+ Interactive Demo (S-N 을 step 으로 매핑)** |
| `### Flow` / `### State / Lifecycle` | `workflow` (단, ui-mockup 시그널 동시 존재 시 ui-mockup 우선) |
| `### Data Contract` / ERD / 테이블 정의 | `data-model` |

여러 시그널 동시 존재 시 우선순위: **ui-mockup > workflow > data-model**.
다중 SPEC 입력 시 — 모든 SPEC 의 시그널을 수집해 최빈 시그널 또는 우선순위로 결정.
추론 불가 (시그널 없음) → AskUserQuestion 으로 mode 선택.

### Step 3 — 스타일 소스 결정

이 레포는 문서 SoT 만 들고 코드는 별도 레포다. `fe_root` 인자가 없으면 AskUserQuestion 으로 확인:
- "이 제품의 FE 코드 루트 경로가 있나요? (스타일 통일용)"
- 옵션: "있음 (경로 답변)" / "없음 — 레포 디자인 시스템 톤 사용"

**3a — FE 코드 있음:** `fe_root` 를 Read/Grep. Tailwind config / 색 토큰 / 컴포넌트 패턴 / className 컨벤션 추출. 그 패턴으로 HTML 생성.

**3b — FE 코드 없음:** 레포 안의 reference 를 톤 SSOT 로 차용한다. 내용을 이 skill 에 베끼지 말고 런타임에 읽는다:

- `claude_design/kknaks_profile_v2.1.0/design-system.html` — 색/타이포/컴포넌트 토큰 (버전 폴더가 더 생기면 최신 버전 사용)
- `claude_design/kknaks_profile_v2.1.0/CLAUDE.md`, `SLOTS.md` — 디자인 규칙·슬롯 구조
- `products/<product>/00-baseline/` 안의 기존 `.html` — 해당 제품 시안이 이미 있으면 그 톤 우선
- 기존 `products/<product>/21-html/*.html` — 같은 제품의 이전 산출물과 톤 통일

기본 뼈대는 Tailwind CDN + Pretendard. reference 가 다른 스택이면 reference 를 따른다.

### Step 4 — cross-ref read

SPEC frontmatter `links` 의 wikilink 를 따라 Read:
- `links.decisions` — 결정 근거 (시안이 결정과 어긋나면 안 됨)
- `links.specs` / `links.related` — 의존 SPEC
- 본문 `[[...]]` wikilink 도 추출해서 Read
- 필요 시 `products/<product>/40-architecture/` (system/database 구조)

### Step 5 — HTML 생성

다음 컨벤션을 따르는 HTML 1 파일 생성.

**HTML 기본 뼈대:**
- `<!DOCTYPE html>` + `lang="ko"` + `meta viewport` (width=1440, ui-mockup 이 모바일 제품이면 390)
- Tailwind CDN `<script src="https://cdn.tailwindcss.com">` + inline `<script>` 에 `tailwind.config` (또는 Step 3 스타일 소스 스택)
- Pretendard `<link>` (font CDN)

**frontmatter 박기 (필수):**

`<!doctype html>` 바로 뒤, `<html>` 앞에 yaml-in-html-comment 형식으로 삽입 — doctype *앞*에 주석을 박으면 quirks mode 트리거되므로 금지. 필드는 이 레포 frontmatter 원칙(`rules/product-doc-pipeline.md`)을 따른다:

```html
<!doctype html>
<!--
---
type: spec-html
product: open-kknaks
output_mode: ui-mockup
spec_mode: multi-spec
spec_ids: [OKK-SPEC-005, OKK-SPEC-006]
title: "batch 실행 콘솔 시안"
summary: |
  batch 태스크 등록(005) → CLI/콘솔에서 진행 관찰(006) 흐름의 운영 화면 시안.
sections:
  - spec_id: OKK-SPEC-005
    anchor: "#section-spec-005"
    role: "batch 등록 폼 + 대기열"
  - spec_id: OKK-SPEC-006
    anchor: "#section-spec-006"
    role: "실행 진행 스트림 뷰"
references:
  - "claude_design/kknaks_profile_v2.1.0/design-system.html"
tags:
  - product/open-kknaks
  - doc/spec-html
generated_at: 2026-07-07
generated_by: spec-to-html
---
-->
<html lang="ko">
```

필수 필드: `type`, `product`, `output_mode`, `spec_mode`, `spec_ids`, `title`, `summary`, `tags`, `generated_at`, `generated_by`.
조건부 필드: `sections` (multi-spec 시만), `references` (차용 시안 있을 때만).

**multi-spec 시 sections anchor:**
- 본문 각 SPEC 구역에 `<section id="section-spec-NNN">` 부여, frontmatter `sections[].anchor` 와 1:1 대응
- 화면 요소는 하나의 화면 안에 융합하되 (별도 페이지 나열 금지), section 경계는 anchor 로 남긴다

**안정적 id 컨벤션 (권장):**
- 화면/최상위 섹션: `id="screen-<name>"` / `id="section-<name>"`
- 카드·리스트 아이템 (JS 렌더 포함): 데이터 키 기반, index 금지 (`id="task-row-${slug}"` ○ / `id="card-0"` ✕)
- JS `innerHTML` 템플릿 문자열에도 id 포함 — 재렌더 후 같은 id 유지
- 상태 표현(active/highlight)은 정적 class 가 아니라 JS 토글, 토글 클래스는 `demo-` prefix (`demo-active`, `demo-hidden`) — 기존 css 클래스 충돌 회피

**mode 별 생성 컨벤션:**

*ui-mockup:*
- 실제 화면처럼 보이는 시안 — chip, badge, status indicator, modal, form field
- SPEC 의 `### U-N` (UX Contract) 항목을 element 단위로 1:1 시각화
- 실제 데이터 sample 을 박아 mock (사용자명, 날짜, 상태값 등 — placeholder "TODO" 금지)
- 아이콘은 inline SVG 또는 lucide CDN (이모지 chrome 금지)
- 클릭 가능한 인터랙션처럼 보이는 디자인 (`cursor-pointer`, hover state)

*ui-mockup + Interactive Demo Player (`## 3. User Scenario` S-N 절 존재 시 자동 활성):*

S-N 시나리오의 단계를 step 으로 매핑해 viewer 가 단계별 화면 전개를 보는 demo 를 생성한다.

1. **step 매핑**: SPEC 단계를 1:1 시각화하지 말 것. viewer 에게 안 보이는 backend-only 단계(enqueue, webhook 수신 등)는 합친다. viewer 가 인지하는 이벤트 수 기준 자연스러운 **8~9 단계** 권장.
2. **attribute 컨벤션 (필수)**:
   - `data-step="N"` — N step 부터 show (미만이면 `demo-hidden`)
   - `data-tier="ok|caution|risk"` — 단계별 활성 tier (multi-state widget 용)
   - `data-action="first|prev|play|next"` — control 버튼
   - `data-speed="0.5|1|1.5|2"` — 속도 버튼
3. **JS player**: IIFE 로 감싸기. state = `currentStep`, `speed`, `playing`, `timer`. **default `currentStep = TOTAL`** (첫 진입 시 final state 전부 보임, "다시보기"가 step 1 reset + auto-play). autoPlay timer = `setTimeout(tick, 1500 / speed)`.
4. **widget UI**: 우하단 floating. progress bar + step counter (`N / TOTAL 단계`) + controls + speed buttons.
5. 정적 `class="... active"` / inline highlight 금지 — JS 토글로만.

*ui-mockup + Multi-Scenario Selector (S-N 시나리오 또는 Case Matrix 케이스가 3개 이상일 시 활성):*

1. 시나리오별 element 에 `data-scenario="ID"` 부여 (공통 element 에는 X)
2. selector chip 그룹 — 각 chip 에 `data-scenario-select="ID"`, 선택된 chip 에 `demo-active`
3. JS state 에 `currentScenario` + `TOTAL_STEPS[scenarioId]` map, swap 시 step reset + autoPlay
4. 모든 케이스를 박지 말고 viewer 가치 기준 **대표 3~5개** 선별

*workflow:*
- 단계 흐름 카드 + 화살표, state machine / branch / loop 명시
- SPEC 의 `### Flow` (mermaid) / `### State / Lifecycle` 를 시각 카드로 전개
- 데이터 handoff 표기 (어떤 필드가 어디로)
- multi-spec: SPEC 간 handoff 화살표로 E2E pipeline 시각화

*data-model:*
- `### Data Contract` / `40-architecture/database/` 기반 ERD / 필드 카드 / 관계도
- 타입 + nullable + FK 명시

### Step 6 — 저장 + hook

**저장:** `products/<product>/21-html/spec-NNN[-NNN]-<slug>.html` 로 Write. slug 는 spec 파일명 slug 를 따른다 (예: `spec-011-slack-knowledge-capture.md` → `spec-011-slack-knowledge-capture.html`). `21-html/` 은 검증 대상 stage 디렉토리가 아니다 — README 강제 없음, 시안 산출물 전용.

파일이 이미 있으면 AskUserQuestion 으로 덮어쓸지 확인 후 진행.

**product doc pipeline hook (필수):** `products/**` 를 건드렸으므로 `agent.md` 의 응답 종료 전 hook 을 수행한다:

1. `products/<product>/log.md` 에 1줄 추가 (Type: `spec-html-add` 또는 `spec-html-change`, IDs: 대상 SPEC ID, Links: 산출물 경로)
2. `.agent/hooks/product-doc-pipeline.md` 체크리스트 확인
3. `python3 .agent/scripts/product_doc_pipeline.py` 실행
4. warnings/errors 를 최종 응답에 포함. 실패를 성공처럼 보고하지 않는다

## Checklist

- [ ] SPEC ID → product 를 런타임 Grep 으로 해석했는가 (prefix 테이블 하드코딩 X, 모호하면 AskUserQuestion)
- [ ] 다중 SPEC 모드: 모든 SPEC 파일 Glob + Read 했는가
- [ ] mode 미지정 시 spec 템플릿 섹션 시그널로 추론했는가, 불가 시 AskUserQuestion
- [ ] FE 코드 루트 유무를 확인했는가 (Step 3 생략 금지)
- [ ] 3b 에서 reference 를 런타임에 실제로 Read 했는가 (기억으로 톤 발명 금지)
- [ ] cross-ref 를 frontmatter `links` wikilink 로 모두 Read 했는가
- [ ] HTML frontmatter (yaml-in-html-comment) 를 `<!doctype html>` *뒤*에 박았는가
- [ ] frontmatter 필수 필드 10개 모두 채웠는가 (type, product, output_mode, spec_mode, spec_ids, title, summary, tags, generated_at, generated_by)
- [ ] multi-spec 시 `sections` 배열 + `<section id="section-spec-NNN">` anchor 를 넣었는가
- [ ] 안정적 id 컨벤션 (데이터 키 기반, index 금지) 을 따랐는가
- [ ] **(User Scenario S-N 존재 시)** Interactive Demo Player 를 박았는가 — `data-step`/`data-tier`/`data-action`/`data-speed`, `currentStep = TOTAL` default, 정적 active class 금지
- [ ] **(3+ 시나리오/케이스 시)** Multi-Scenario Selector — `data-scenario` + chip + JS swap, 대표 3~5개 선별
- [ ] 기존 파일 덮어쓰기 전 사용자 확인 받았는가
- [ ] 저장 위치가 `products/<product>/21-html/` 인가
- [ ] `log.md` 1줄 추가 + `product_doc_pipeline.py` 실행 + 결과를 최종 응답에 포함했는가

## Failure / Rollback

- SPEC 파일을 Glob 으로 못 찾으면 → 사용자에게 전체 경로 요청
- product 해석 불가 (bare SPEC-NNN 다중 매치) → AskUserQuestion 필수, 임의 결정 금지
- output_mode 추론 불가 → AskUserQuestion 으로 mode 선택
- `product_doc_pipeline.py` errors → 오류 내용 그대로 보고, 성공처럼 보고하지 않음
- 파일 저장 실패 → 오류 보고 후 중단

## Related

- spec 템플릿 (mode 추론 시그널의 SSOT): `templates/product/20-spec/spec.md`
- 문서 규칙: `rules/product-doc-pipeline.md`
- hook: `.agent/hooks/product-doc-pipeline.md`, `.agent/scripts/product_doc_pipeline.py`
- 디자인 레퍼런스: `claude_design/kknaks_profile_v2.1.0/` (design-system.html, CLAUDE.md, SLOTS.md)
- agent entry: `agent.md`
