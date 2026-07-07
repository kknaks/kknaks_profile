---
type: spec
id: AXKG-SPEC-012
title: "Source Collection Adapter: YouTube·웹 원문 수집 계약"
status: stable
product: ax-knowledge-graph
version: 0.0.1
created_at: 2026-07-07
updated_at: 2026-07-07
tags:
  - product/ax-knowledge-graph
  - doc/spec
  - status/stable
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works:
    - "[[work-001-mvp-pipeline-scaffold|AXKG-WORK-001]]"
  releases: []
  related: []
---

# Source Collection Adapter: YouTube·웹 원문 수집 계약

Source Inbox에 들어온 URL을 요약 AI가 읽을 수 있는 `SourceMaterial`로 변환하는 수집 adapter 계약을 정의한다. MVP에서는 YouTube, 정적 웹 article, 동적 렌더링 웹 페이지를 포함한다. PDF, RSS 등은 이 spec의 adapter 목록을 확장해 추가한다.

> 이 spec은 "원문을 어떻게 가져오는가"만 다룬다. URL 수신과 상태 관리는 AXKG-SPEC-003, 수집된 원문을 프롬프트·스키마와 조립해 AI task로 실행하는 흐름은 AXKG-SPEC-011 소관이다.

## 1. Context

### Meta

- Decision reference: AXKG-DEC-001, AXKG-DEC-005
- Baseline reference: AXKG-BL-001
- Domain note: `Source Collection Adapter`, `SourceMaterial`, `YouTube Adapter`, `Static Web Adapter`, `Dynamic Web Adapter`
- 호출 주체: `collect_source_summary` 실행 전 context builder 또는 그 하위 fetcher.
- 소비처: AXKG-SPEC-011 요약 스테이지의 입력 컨텍스트.

### Business Requirement

AX Knowledge Graph는 YouTube, 웹 문서, PDF처럼 서로 다른 원천을 같은 요약 파이프라인으로 보내야 한다. 수집 방식을 AI 실행 스펙에 직접 박으면 adapter가 늘어날수록 실행 계약이 비대해지고, 실패 코드·보안 정책·캐시 정책이 흩어진다. Source Collection Adapter는 source type별 수집 방식을 분리하고, 요약 AI에는 정규화된 `SourceMaterial`만 넘긴다.

### Scope

In scope:

- source URL의 type detection
- YouTube URL에서 video id 추출
- YouTube metadata와 transcript 수집
- 정적 HTML article의 제목·본문·작성자·게시일 추출
- 정적 수집 가능 여부 판단과 동적 렌더링 fallback
- Playwright/Chrome 기반 rendered visible text 추출
- `SourceMaterial` 정규화 출력
- 수집 실패 코드와 보안 제한
- 기존 profile YouTube 수집 코드 재사용 경로 기록

Out of scope:

- Source Inbox row 생성과 상태 UI (AXKG-SPEC-003)
- AI prompt 조립, output_schema 검증, ai_tasks lifecycle (AXKG-SPEC-011)
- PDF, RSS adapter 구현 계약 (후속 확장)
- 로그인·paywall·권한 필요한 source 수집
- 사이트별 비공개 API 커스텀 adapter. 공식 API/RSS는 후속 전용 adapter로만 추가한다.

## 2. Interface Contract

### Adapter Selection

| 입력 | adapter | MVP 처리 |
|---|---|---|
| `youtube.com/watch?v=...` | `youtube` | 지원 |
| `m.youtube.com/watch?v=...` | `youtube` | 지원 |
| `youtu.be/...` | `youtube` | 지원 |
| `youtube.com/shorts/...` | `youtube` | 지원 |
| 기타 HTTP(S) URL + `content-type: text/html` | `static_web` | 지원 |
| `static_web` 기준 미달 + public browser render 가능 | `dynamic_web` | 지원 |
| PDF, RSS, 기타 non-HTML URL | `unsupported` | 후속 adapter 전까지 `UNSUPPORTED_SOURCE_TYPE` |

Adapter 선택은 3단계로 한다.

1. URL host/path 기반으로 명확한 source type을 먼저 판정한다. YouTube URL은 HTTP content-type 확인 전에 `youtube` adapter로 보낸다.
2. 명확한 전용 adapter가 없으면 HTTP HEAD 또는 GET 응답의 content-type과 body를 보고 `static_web` 가능 여부를 판정한다.
3. `static_web`이 `DYNAMIC_RENDER_REQUIRED` 또는 본문 부족으로 실패하면 `dynamic_web` adapter를 시도한다.

구현 원칙:

- 사이트별 내부 JSON API를 발견해도 일반 adapter가 직접 커스텀 호출하지 않는다. 예: 특정 사이트의 `/bbs/listBbs.json` 같은 endpoint를 사이트별 규칙으로 박지 않는다.
- 동적 웹은 브라우저 렌더링 결과 DOM을 기준으로 수집한다.
- 공식 API, RSS, sitemap처럼 안정적인 공개 계약이 있는 경우에만 후속 전용 adapter로 분리한다.

### SourceMaterial

모든 adapter는 성공 시 아래 구조로 정규화된 자료를 반환한다.

```json
{
  "source_url": "https://example.com/article",
  "canonical_url": "https://example.com/article",
  "adapter": "youtube | static_web | dynamic_web",
  "title": "...",
  "author": "...",
  "published_at": "YYYY-MM-DD or null",
  "duration_seconds": 1234,
  "content_text": "... extracted body ...",
  "content_format": "transcript | article_text | rendered_visible_text",
  "fetch_method": "youtube_transcript_api | static_html | playwright_chrome",
  "fetched_at": "ISO-8601",
  "external_id": "youtube video id or null",
  "metadata": {
    "thumbnail": "...",
    "tags": [],
    "headings": [],
    "links": [],
    "images": [],
    "page_kind": "article | list | mixed | unknown"
  }
}
```

규칙:

- `content_text`는 요약 AI가 읽을 원문이다.
- `adapter`는 **수집 방식 식별자**다. 콘텐츠 유형 `source_type`(`article`/`video`/`document`/`unknown`, AXKG-SPEC-001/002 계약)과 다른 필드이며 어휘를 섞지 않는다. adapter는 요약 AI에 유형 힌트를 준다: `youtube→video`, `static_web`/`dynamic_web`→기본 `article`(요약 AI가 본문 기준으로 보정).
- `canonical_url`은 중복 source 판단과 trace에 사용한다. 수집 성공 시 `sources.normalized_url`을 canonical 기준으로 갱신하고 중복을 재검사한다(예: `youtu.be/X`와 `watch?v=X`는 canonical에서 합류). 갱신 결과 기존 source와 충돌하면 AXKG-SPEC-003 S-2 중복 규칙(기존 source에 연결)을 따른다.
- `duration_seconds`는 YouTube처럼 재생 시간이 있는 source에서만 값이 있고, 정적 웹에서는 null이다.
- `external_id`는 source provider의 안정 식별자다. YouTube는 video id, 정적 웹은 null이다.
- `fetch_method`는 운영 디버깅을 위해 저장 또는 `ai_tasks.payload`에 스냅샷한다.
- `metadata.page_kind=list`인 경우 `content_text`는 목록 페이지의 visible text이며, `metadata.links`에는 사용자가 선택할 수 있는 article 후보를 담는다.
- transcript 전문과 rendered visible text 전문은 application log에 남기지 않는다. 필요한 경우 DB payload 또는 material snapshot에만 저장한다.

### YouTube Adapter

입력:

- `source_id`
- `source_url`
- 선택 metadata: `submitted_by`, `source_channel`, `raw_text`

처리:

1. URL scheme이 `http` 또는 `https`인지 검증한다.
2. host와 path/query에서 YouTube video id를 추출한다.
3. canonical URL을 `https://www.youtube.com/watch?v=<video_id>`로 정규화한다.
4. metadata를 수집한다.
5. transcript를 수집한다.
6. transcript가 비어 있거나 너무 짧으면 실패 처리한다.
7. `SourceMaterial`을 반환한다.

기존 구현 참고:

- `app/back/service/jobs/content_enrich.py`
  - `extract_metadata(youtube_id)`
  - `extract_transcript(youtube_id)`
- `app/back/service/knowledge_capture/source.py`
  - `fetch_source(url)`
  - `_fetch_youtube(url)`
  - `_youtube_id(url)`

구현 시 위 코드를 직접 import할 수 있지만, AXKG 구현에서는 장기적으로 `service/source_collection/` 같은 공통 fetcher로 분리해 `persona/contents`, `knowledge_capture`, `ax-knowledge-graph`가 같은 adapter를 공유하는 편이 낫다.

### Static Web Adapter

정적 웹 adapter는 HTTP 응답 HTML 안에 본문이 이미 포함된 article/blog/documentation 페이지를 수집한다. JavaScript 실행 후에야 본문이 생기는 페이지는 이 adapter가 처리하지 않고 `DYNAMIC_RENDER_REQUIRED`로 분리한다.

입력:

- `source_id`
- `source_url`
- 선택 metadata: `submitted_by`, `source_channel`, `raw_text`

처리:

1. URL scheme이 `http` 또는 `https`인지 검증한다.
2. SSRF guard를 통과한 뒤 제한된 redirect를 따라간다.
3. 응답 `content-type`이 `text/html` 또는 HTML로 파싱 가능한 타입인지 확인한다.
4. `<script>`, `<style>`, nav, footer, 광고, 댓글, 관련글 영역을 제거한다.
5. title 후보를 우선순위로 추출한다: `og:title` → `<title>` → 첫 번째 `h1`.
6. canonical URL 후보를 우선순위로 추출한다: `<link rel="canonical">` → 최종 redirect URL.
7. author 후보를 추출한다: `article:author`, `author` meta, byline 영역, 없으면 null.
8. published_at 후보를 추출한다: `article:published_time`, `datePublished` JSON-LD, time tag, 없으면 null.
9. article 본문 후보를 추출한다: `<article>` → `main` → text density가 높은 container.
10. headings(`h1`~`h3`)와 본문 텍스트를 정규화한다.
11. 정적 수집 가능성 기준을 통과하면 `SourceMaterial`을 반환한다.

정적 수집 가능성 기준:

| 기준 | 통과 조건 | 실패 코드 |
|---|---|---|
| 본문 길이 | boilerplate 제거 후 `content_text`가 최소 500자 이상 | `CONTENT_EXTRACT_FAILED` |
| 텍스트 밀도 | 후보 container의 링크/메뉴 대비 본문 텍스트 비율이 충분함 | `CONTENT_EXTRACT_FAILED` |
| 제목 | title 후보가 존재함 | `CONTENT_EXTRACT_FAILED` |
| JS 의존 의심 | "enable javascript", root div만 존재, 본문 container 없음 | `DYNAMIC_RENDER_REQUIRED` |
| 접근 제한 | 로그인/paywall/권한 안내가 본문을 대체함 | `PAYWALL_OR_AUTH_REQUIRED` |

테스트 fixture 후보:

- `https://bums-life.tistory.com/entry/Graphify%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-AI%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%B4-%EC%BD%94%EB%93%9C%EC%99%80-%EB%AC%B8%EC%84%9C%EB%A5%BC-%EC%A7%80%EC%8B%9D-%EA%B7%B8%EB%9E%98%ED%94%84%EB%A1%9C-%EB%B0%94%EA%BE%B8%EB%8A%94-%EB%B0%A9%EB%B2%95`

이 fixture는 HTML 응답만으로 title, author, published_at, heading, body가 추출되는 정적 article 케이스다.

### Dynamic Web Adapter

동적 웹 adapter는 정적 HTML만으로는 본문을 얻기 어렵지만, 공개 브라우저 렌더링으로 화면 텍스트를 볼 수 있는 페이지를 수집한다. 사이트별 내부 API를 직접 커스텀하지 않고, Playwright/Chrome으로 렌더링된 DOM에서 visible text를 추출한다.

입력:

- `source_id`
- `source_url`
- 선택 metadata: `submitted_by`, `source_channel`, `raw_text`

처리:

1. URL scheme이 `http` 또는 `https`인지 검증한다.
2. SSRF guard를 통과한 뒤 browser context에서 페이지를 연다.
3. `domcontentloaded`를 기다린다.
4. `networkidle` 또는 DOM 안정화 조건을 제한 시간 안에서 기다린다.
5. 필요하면 제한된 횟수만큼 scroll을 수행해 lazy-loaded 콘텐츠를 노출한다.
6. DOM에서 코드·UI·입력 요소를 제거한다.
7. `document.body.innerText` 기반으로 rendered visible text를 추출한다.
8. title, canonical, link 후보, image 후보를 metadata로 추출한다.
9. 텍스트 길이와 노이즈 기준을 통과하면 `SourceMaterial`을 반환한다.

DOM 제거 규칙:

```text
script, style, noscript, svg, canvas, template, iframe,
header, nav, footer, form, dialog,
button, input, select, textarea
```

추출 규칙:

| 필드 | 추출 방식 |
|---|---|
| `title` | `og:title` → `document.title` → 첫 번째 `h1` |
| `canonical_url` | `<link rel="canonical">` → `location.href` |
| `content_text` | 제거된 DOM의 `document.body.innerText` |
| `metadata.links` | 렌더링 후 DOM 안의 주요 article/list candidate 링크 |
| `metadata.images` | 본문 후보 주변 image URL과 alt. 이미지는 metadata only |
| `metadata.page_kind` | AI/heuristic이 `article`, `list`, `mixed`, `unknown` 중 판정 |

후처리:

- 반복 공백과 3개 이상 연속 빈 줄을 줄인다.
- 완전히 같은 라인이 과도하게 반복되면 중복 제거한다.
- 너무 짧은 메뉴성 라인 제거는 optional로 둔다.
- 최대 입력 길이를 초과하면 chunk로 나누고, AXKG-SPEC-011 요약 stage에서 chunk summary를 병합한다.

AI 입력 지시:

```text
아래는 웹페이지에서 렌더링 후 추출한 visible text다.
네비게이션, 메뉴, 푸터, 광고, 관련글, 댓글, 폼 문구가 섞여 있을 수 있다.
주요 본문과 보조 영역을 구분하고, source summary에는 주요 본문만 반영하라.
목록 페이지라면 article 후보 목록을 추출하고 page_kind=list로 표시하라.
```

동적 수집 가능성 기준:

| 기준 | 통과 조건 | 실패 코드 |
|---|---|---|
| 렌더링 가능 | 제한 시간 안에 DOM이 로드됨 | `DYNAMIC_RENDER_FAILED` |
| visible text | 제거 후 `content_text`가 최소 500자 이상 | `CONTENT_EXTRACT_FAILED` |
| 공개 접근 | 로그인, CAPTCHA, paywall 없이 접근 가능 | `PAYWALL_OR_AUTH_REQUIRED` |
| 목록 페이지 | 단일 본문이 아니라 여러 article 후보가 주 콘텐츠임 | 성공 + `metadata.page_kind=list` |
| 과도한 노이즈 | 본문/목록 후보보다 메뉴·폼·광고가 지배적임 | `CONTENT_EXTRACT_FAILED` |

테스트 fixture 후보:

- `https://enterprise.kt.com/bt/P_BT_TI_LT_001.do?utm_source=google&utm_medium=searched&utm_campaign=googlesa_p_&utm_content=sa_pc_axstory_20260626&utm_term=&gad_source=1&gad_campaignid=22926266627`

이 fixture는 서버 HTML에 목록 placeholder가 있고, 렌더링 후 JS가 article 목록을 채우는 `dynamic_web` list page 케이스다.

## 3. Failure Contract

| 에러 코드 | 조건 | AXKG 매핑 |
|---|---|---|
| `INVALID_URL` | HTTP(S)가 아님, 또는 YouTube로 판정된 URL에서 video id를 추출할 수 없음 | `ai_tasks.failed`, `sources.collection_failed` |
| `UNSUPPORTED_SOURCE_TYPE` | MVP adapter가 없는 URL | `ai_tasks.failed`, `sources.collection_failed` |
| `CONTENT_FETCH_FAILED` | metadata 또는 transcript API 호출 실패 | `ai_tasks.failed`, `sources.collection_failed` |
| `CONTENT_EXTRACT_FAILED` | HTML은 받았지만 본문 추출 기준 미달 | `ai_tasks.failed`, `sources.collection_failed` |
| `TRANSCRIPT_UNAVAILABLE` | transcript 없음 또는 최소 길이 미달 | `ai_tasks.failed`, `sources.collection_failed` |
| `DYNAMIC_RENDER_REQUIRED` | JS 렌더링 없이는 본문을 얻을 수 없음 | `ai_tasks.failed`, `sources.collection_failed` |
| `DYNAMIC_RENDER_FAILED` | 브라우저 렌더링 실패 또는 timeout | `ai_tasks.failed`, `sources.collection_failed` |
| `PAYWALL_OR_AUTH_REQUIRED` | 로그인, paywall, 권한 필요 | `ai_tasks.failed`, `sources.collection_failed` |
| `SOURCE_TOO_LARGE` | adapter별 size limit 초과 | `ai_tasks.failed`, `sources.collection_failed` |
| `FETCH_TIMEOUT` | timeout 초과 | `ai_tasks.failed`, `sources.collection_failed` |

실패한 경우:

- 실패한 `ai_tasks` row는 보존한다.
- Source Detail에는 최신 실패 task의 `error_code`와 `error_message`를 표시한다.
- `collection_failed` source는 AXKG-SPEC-003의 `요약 재시도`로 새 task를 만들 수 있다.
- 단, `UNSUPPORTED_SOURCE_TYPE`(PDF/RSS 등)은 adapter가 추가되기 전까지 재시도해도 결과가 같다. 재시도 자체는 막지 않되, Source Detail에는 "지원 예정 형식" 안내를 함께 표시한다.

## 4. Security And Limits

- `http`/`https`만 허용한다.
- redirect는 제한된 횟수만 허용한다.
- private, loopback, link-local, non-global IP로 resolve되는 URL은 차단한다.
- adapter별 timeout과 byte limit을 둔다.
- transcript 전문, raw HTML, 추출 본문 전문, credential, app/bot token은 application log에 남기지 않는다.
- dynamic adapter는 브라우저 실행 시간, scroll 횟수, networkidle 대기 시간을 제한한다.
- dynamic adapter는 파일 다운로드, 권한 요청, 팝업, 새 창 열기를 차단한다.
- CAPTCHA, 로그인, 결제, 개인정보 입력이 필요한 페이지는 우회하지 않는다.
- user-agent와 rate limit 정책은 adapter별 구현 기본값으로 시작하고, 운영 관찰 후 조정한다.

## 5. Integration

요약 스테이지는 이 spec의 adapter를 먼저 호출한 뒤, 반환된 `SourceMaterial`을 AXKG-SPEC-011의 context builder 입력으로 사용한다.

```text
sources.received
→ collect_source_summary task 생성
→ Source Collection Adapter collect(source_url)
→ SourceMaterial
→ AXKG-SPEC-011 context assembly
→ open-kknaks 실행
→ sources.summary_payload
→ sources.summarized
```

## 6. Verification

### Acceptance Criteria

- [ ] YouTube watch URL에서 video id를 추출하고 canonical URL을 만든다.
- [ ] `youtu.be` URL에서 video id를 추출하고 canonical URL을 만든다.
- [ ] YouTube metadata와 transcript를 `SourceMaterial`로 정규화한다.
- [ ] transcript가 없으면 `TRANSCRIPT_UNAVAILABLE`로 실패한다.
- [ ] 정적 HTML article에서 title, canonical_url, content_text를 추출한다.
- [ ] 정적 HTML article에서 author와 published_at은 가능하면 추출하고 없으면 null로 둔다.
- [ ] 본문이 HTML에 없고 JS 렌더링이 필요하면 `DYNAMIC_RENDER_REQUIRED`로 실패한다.
- [ ] `DYNAMIC_RENDER_REQUIRED` 또는 본문 부족 static page는 `dynamic_web` adapter로 fallback한다.
- [ ] dynamic adapter는 렌더링된 DOM에서 코드·UI 요소를 제거한 뒤 `document.body.innerText` 기반 visible text를 추출한다.
- [ ] dynamic list page는 실패하지 않고 `metadata.page_kind=list`와 `metadata.links` 후보를 반환한다.
- [ ] 사이트별 내부 API endpoint는 일반 adapter에 하드코딩하지 않는다.
- [ ] HTML 본문 추출 기준 미달이면 `CONTENT_EXTRACT_FAILED`로 실패한다.
- [ ] unsupported URL은 `UNSUPPORTED_SOURCE_TYPE`으로 실패한다.
- [ ] 수집 실패는 `sources.collection_failed`와 실패 `ai_tasks` row로 표면화된다.
- [ ] transcript와 추출 본문 전문은 application log에 남지 않는다.

## 7. Open Questions

- 수집된 `SourceMaterial` snapshot을 DB에 영구 저장할지, `ai_tasks.payload`에만 보존할지.
- dynamic adapter를 FastAPI 내부에서 실행할지 별도 browser worker/service로 분리할지.
- `page_kind=list` 결과의 후속 UX — `metadata.links`의 article 후보를 사용자가 선택해 개별 source로 등록하는 흐름은 AXKG-SPEC-003 확장으로 후속 결정. MVP는 list의 visible text가 그대로 요약 입력이 된다.
