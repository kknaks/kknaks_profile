---
type: spec
id: AXKG-SPEC-012
title: "Source Collection Adapter: YouTube·웹 원문 수집 계약"
status: stable
product: ax-knowledge-graph
version: 0.0.1
created_at: 2026-07-07
updated_at: 2026-07-21
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
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
  works:
    - "[[work-002-source-intake|AXKG-WORK-002]]"
    - "[[work-010-inbox-md-upload-intake|AXKG-WORK-010]]"
  releases: []
  related: []
---

# Source Collection Adapter: YouTube·웹 원문 수집 계약

Source Inbox에 들어온 URL을 요약 AI가 읽을 수 있는 `SourceMaterial`로 변환하는 수집 adapter 계약을 정의한다. MVP에서는 YouTube, 정적 웹 article, 동적 렌더링 웹 페이지, 그리고 업로드된 **docx의 본문 텍스트 추출**을 포함한다. PDF, RSS 등은 이 spec의 adapter 목록을 확장해 추가한다.

> 이 spec은 "원문을 어떻게 가져오는가"만 다룬다. URL 수신과 상태 관리는 AXKG-SPEC-003, 수집된 원문을 프롬프트·스키마와 조립해 AI task로 실행하는 흐름은 AXKG-SPEC-011 소관이다.

> **경계 — 업로드 md는 이 spec의 adapter 대상이 아니다** (2026-07-14, AXKG-SPEC-003 T-004): `source_channel=upload`(md 파일 업로드)은 URL 원문 수집 단계가 없다. 업로드된 md 본문(`raw_text`)이 곧 원문이므로 adapter를 거치지 않고 그대로 요약 스테이지(AXKG-SPEC-011 ①)의 입력이 된다. chat의 User Note Fallback과 달리 "수집 실패 시 대체"가 아니라 **원문 그 자체**다 — 따라서 아래 URL 기반 수집 실패 코드·재시도 계약(§3)은 upload에 적용되지 않는다. (단 업로드 `.docx`는 md와 달리 바이너리라 본문 텍스트 추출이 필요하다 — 아래 Docx Text Extraction Adapter가 처리하며, 표/이미지 파싱 계약은 두지 않는다. AXKG-DEC-007 D5.)

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
- 웹 페이지의 UI 제거 후 visible text 추출과 title/author/published_at metadata 추출 (static/dynamic 공통 규칙)
- 정적 수집 가능 여부 판단과 동적 렌더링 fallback (Playwright/Chrome)
- `SourceMaterial` 정규화 출력
- 수집 실패 코드와 보안 제한
- 기존 profile YouTube 수집 코드 재사용 경로 기록
- 업로드 `.docx` 파일의 **본문 텍스트 추출**(구조화는 어댑터가 아니라 적응형 요약①, AXKG-SPEC-011). 표 보존·이미지 파싱 계약은 두지 않음(AXKG-DEC-007 D5)

Out of scope:

- Source Inbox row 생성과 상태 UI (AXKG-SPEC-003)
- AI prompt 조립, output_schema 검증, ai_tasks lifecycle (AXKG-SPEC-011)
- PDF, RSS adapter 구현 계약 (후속 확장)
- 업로드 md 파일(`source_channel=upload`) intake — adapter 대상 아님(URL 수집 스킵, 업로드 md 본문이 곧 원문). 데이터 계약은 AXKG-SPEC-003 소관이며, 이 spec의 수집 실패/재시도 계약을 적용하지 않는다
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
| 업로드 `.docx` 파일(`source_channel=upload`) | `docx_text` | 지원 — 본문 텍스트만 추출(구조화는 요약①, 아래 Docx Text Extraction Adapter) |
| PDF, RSS, 기타 non-HTML URL | `unsupported` | 후속 adapter 전까지 `UNSUPPORTED_SOURCE_TYPE` |

Adapter 선택은 4단계로 한다.

1. URL host/path 기반으로 명확한 source type을 먼저 판정한다. YouTube URL은 HTTP content-type 확인 전에 `youtube` adapter로 보낸다.
2. 명확한 전용 adapter가 없으면 HTTP HEAD 또는 GET 응답의 content-type과 body를 보고 `static_web` 가능 여부를 판정한다.
3. `static_web`이 `DYNAMIC_RENDER_REQUIRED` 또는 본문 부족으로 실패하면 `dynamic_web` adapter를 시도한다.
4. **최종 fallback — User Note.** 위 URL 기반 수집이 모두 `CollectionError`로 실패했을 때(예: Cloudflare/봇 방어로 static·dynamic 모두 원문 미달), 사용자가 함께 남긴 메모가 있으면 그 메모를 `user_note` `SourceMaterial`로 만들어 수집을 성립시킨다. 메모가 없으면 실패를 그대로 유지한다(collection_failed). 메모 "있음"은 **trim 후 non-empty** 기준이다.

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
  "adapter": "youtube | static_web | dynamic_web | user_note | docx_text",
  "title": "...",
  "author": "...",
  "published_at": "YYYY-MM-DD or null",
  "duration_seconds": 1234,
  "content_text": "... extracted body ...",
  "content_format": "transcript | video_description | page_text | user_note | doc_text",
  "fetch_method": "youtube_transcript_api | youtube_metadata | static_html | playwright_chrome | user_note | docx_text",
  "fetched_at": "ISO-8601",
  "external_id": "youtube video id or null",
  "metadata": {
    "description": "yt-dlp description (youtube only)",
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
- `adapter`는 **수집 방식 식별자**다. 콘텐츠 유형 `source_type`(`article`/`video`/`document`/`unknown`, AXKG-SPEC-001/002 계약)과 다른 필드이며 어휘를 섞지 않는다. adapter는 요약 AI에 유형 힌트를 준다: `youtube→video`, `static_web`/`dynamic_web`→기본 `article`(요약 AI가 본문 기준으로 보정), `user_note`→기본 `unknown`(요약 AI가 메모 내용 기준으로 보정), `docx_text`→기본 `document`(요약 AI가 본문 기준으로 보정).
- `canonical_url`은 중복 source 판단과 trace에 사용한다. 수집 성공 시 `sources.normalized_url`을 canonical 기준으로 갱신하고 중복을 재검사한다(예: `youtu.be/X`와 `watch?v=X`는 canonical에서 합류). 갱신 결과 기존 source와 충돌하면 AXKG-SPEC-003 S-2 중복 규칙(기존 source에 연결)을 따른다.
- `duration_seconds`는 YouTube처럼 재생 시간이 있는 source에서만 값이 있고, 정적 웹에서는 null이다.
- `external_id`는 source provider의 안정 식별자다. YouTube는 video id, 정적 웹은 null이다.
- `fetch_method`는 운영 디버깅을 위해 저장 또는 `ai_tasks.payload`에 스냅샷한다.
- `metadata.page_kind=list`인 경우 `content_text`는 목록 페이지의 visible text이며, `metadata.links`에는 사용자가 선택할 수 있는 article 후보를 담는다.
- transcript·page_text 전문은 application log에 남기지 않는다. 필요한 경우 DB payload 또는 material snapshot에만 저장한다.

### YouTube Adapter

입력:

- `source_id`
- `source_url`
- 선택 metadata: `submitted_by`, `source_channel`, `raw_text`

처리:

YouTube 수집은 **두 갈래**다: ① metadata(yt-dlp — title, description, duration, channel, tags, thumbnail, upload_date) + ② transcript(youtube-transcript-api, ko 우선 → en). 자막이 없어도 실패하지 않는다 — description fallback으로 진행한다.

1. URL scheme이 `http` 또는 `https`인지 검증한다.
2. host와 path/query에서 YouTube video id를 추출한다.
3. canonical URL을 `https://www.youtube.com/watch?v=<video_id>`로 정규화한다.
4. metadata를 수집한다. `description`은 `metadata.description`으로 보존한다.
5. transcript를 수집한다(ko 우선, 없으면 en).
6. transcript가 있으면 `content_text=transcript`, `content_format=transcript`.
7. transcript가 비어 있거나 너무 짧으면 **description fallback**: `metadata.description`이 최소 길이를 넘으면 `content_text=description`, `content_format=video_description`, `fetch_method=youtube_metadata`로 계속한다.
8. transcript도 없고 description도 부실하면 `TRANSCRIPT_UNAVAILABLE`로 실패 처리한다.
9. `SourceMaterial`을 반환한다.

기존 구현 참고:

- `app/back/service/jobs/content_enrich.py`
  - `extract_metadata(youtube_id)`
  - `extract_transcript(youtube_id)`
- `app/back/service/knowledge_capture/source.py`
  - `fetch_source(url)`
  - `_fetch_youtube(url)`
  - `_youtube_id(url)`

구현 시 위 코드를 직접 import할 수 있지만, AXKG 구현에서는 장기적으로 `service/source_collection/` 같은 공통 fetcher로 분리해 `persona/contents`, `knowledge_capture`, `ax-knowledge-graph`가 같은 adapter를 공유하는 편이 낫다.

### Web Adapter (static_web / dynamic_web)

두 web adapter는 **텍스트를 얻는 방식만 다르고, 그 이후는 전부 공통**이다. 정교한 본문 추출(article container 탐색, 텍스트 밀도 판정, readability)은 하지 않는다 — UI 요소를 제거한 페이지 전체 visible text를 넘기고, 본문/노이즈 구분은 요약 AI(AXKG-SPEC-011 ①)가 한다.

| | `static_web` | `dynamic_web` |
|---|---|---|
| 텍스트 획득 | HTTP GET → `content-type: text/html` 확인 → HTML 파싱 DOM | Playwright/Chrome 렌더링 → `domcontentloaded` → `networkidle`/DOM 안정화(제한 시간) → 제한 횟수 scroll(lazy-load 노출) |
| content_format | `page_text` | `page_text` |
| fetch_method | `static_html` | `playwright_chrome` |

입력(공통): `source_id`, `source_url`, 선택 metadata(`submitted_by`, `source_channel`, `raw_text`).

공통 처리(획득 이후):

1. URL scheme `http`/`https` 검증, SSRF guard, 제한된 redirect.
2. 위 표의 방식으로 DOM을 얻는다.
3. DOM 제거 규칙을 적용한다:

```text
script, style, noscript, svg, canvas, template, iframe,
header, nav, footer, form, dialog,
button, input, select, textarea
```

4. 남은 DOM의 visible text를 `content_text`로 추출한다(dynamic은 `document.body.innerText` 기준).
5. metadata를 추출한다(추출 실패 필드는 null — 실패 사유가 아니다):

| 필드 | 추출 방식 (공통) |
|---|---|
| `title` | `og:title` → `<title>`/`document.title` → 첫 번째 `h1` |
| `canonical_url` | `<link rel="canonical">` → 최종 redirect URL/`location.href` |
| `author` | `article:author` → `author` meta → byline 영역 |
| `published_at` | `article:published_time` → `datePublished` JSON-LD → time tag |
| `metadata.headings` | `h1`~`h3` |
| `metadata.links` | 주요 article/list candidate 링크 |
| `metadata.images` | 본문 후보 주변 image URL과 alt (이미지는 metadata only) |
| `metadata.page_kind` | heuristic/AI가 `article`/`list`/`mixed`/`unknown` 판정 |

6. 후처리한다: 반복 공백·3연속 이상 빈 줄 축소, 동일 라인 과다 반복 제거, 짧은 메뉴성 라인 제거는 optional. 최대 입력 길이 초과 시 chunk 분할(병합은 AXKG-SPEC-011 요약 stage).
7. 수집 기준을 판정하고 `SourceMaterial`을 반환한다.

수집 기준(공통):

| 기준 | 조건 | 결과 |
|---|---|---|
| 텍스트 분량 | 제거·후처리 후 `content_text` 최소 500자 이상 | static에서 미달 → `dynamic_web` fallback 시도. dynamic에서도 미달 → `CONTENT_EXTRACT_FAILED` |
| JS 의존 의심 | "enable javascript", 빈 root div 등 (static만 해당) | `DYNAMIC_RENDER_REQUIRED` → `dynamic_web` fallback |
| 렌더링 가능 | 제한 시간 안 DOM 로드 (dynamic만 해당) | 실패 시 `DYNAMIC_RENDER_FAILED` |
| 공개 접근 | 로그인/CAPTCHA/paywall 안내가 본문을 대체 | `PAYWALL_OR_AUTH_REQUIRED` (우회하지 않음) |
| 목록 페이지 | 단일 본문이 아니라 article 후보 목록이 주 콘텐츠 | 성공 + `metadata.page_kind=list`, `metadata.links`에 후보 |

AI 입력 지시(공통 — 요약 스테이지에 함께 전달):

```text
아래는 웹페이지에서 UI 요소를 제거하고 추출한 visible text다.
네비게이션, 메뉴, 푸터, 광고, 관련글, 댓글, 폼 문구가 섞여 있을 수 있다.
주요 본문과 보조 영역을 구분하고, source summary에는 주요 본문만 반영하라.
목록 페이지라면 article 후보 목록을 추출하고 page_kind=list로 표시하라.
```

테스트 fixture 후보:

- static article: `https://bums-life.tistory.com/entry/Graphify%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-AI%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%B4-%EC%BD%94%EB%93%9C%EC%99%80-%EB%AC%B8%EC%84%9C%EB%A5%BC-%EC%A7%80%EC%8B%9D-%EA%B7%B8%EB%9E%98%ED%94%84%EB%A1%9C-%EB%B0%94%EA%BE%B8%EB%8A%94-%EB%B0%A9%EB%B2%95` — HTML 응답만으로 title/author/published_at/본문이 나오는 케이스
- dynamic list: `https://enterprise.kt.com/bt/P_BT_TI_LT_001.do?utm_source=google&utm_medium=searched&utm_campaign=googlesa_p_&utm_content=sa_pc_axstory_20260626&utm_term=&gad_source=1&gad_campaignid=22926266627` — 서버 HTML은 placeholder이고 렌더링 후 JS가 목록을 채우는 케이스

### User Note Fallback (최종 fallback)

URL 기반 수집(youtube/static_web/dynamic_web)이 모두 실패했을 때, 사용자가 함께 남긴 메모가 있으면 그 메모 텍스트 자체를 요약 입력 원문으로 삼는다. Cloudflare/봇 방어 등으로 원문을 못 가져와도 사용자가 넣은 메모/복붙 텍스트로 요약이 성립하게 하는 MVP 경로다.

입력:

- `source_id`, `source_url`, 사용자 메모(manual `note` 또는 Slack `<< >>` 안 텍스트, AXKG-SPEC-003)

처리:

1. URL 수집 체인(1~3단계)이 모두 `CollectionError`인지 확인한다.
2. 메모가 **trim 후 non-empty**면 아래 `SourceMaterial`로 성립시킨다. 메모가 없거나 trim 후 비어 있으면 수집 실패를 유지한다(`collection_failed`).

| 필드 | 값 |
|---|---|
| `adapter` | `user_note` |
| `content_text` | 사용자 메모 원문 |
| `content_format` | `user_note` |
| `fetch_method` | `user_note` |
| `canonical_url` | 원 URL(수집 실패로 canonical을 못 얻으므로 입력 URL 그대로) |
| `title`/`author`/`published_at`/`duration_seconds`/`external_id` | null |

규칙:

- URL 수집이 성공하면 메모는 사용하지 않는다(원문 우선). User Note는 URL 수집이 모두 실패했을 때만 성립한다.
- 메모 기반 수집과 원문 기반 수집을 **구분 표기하지 않는다** — 둘 다 정상 `SourceMaterial`이고 이후 요약 스테이지·상태(`summarized`)는 동일하다. source_basis 플래그/배지 같은 구분자를 두지 않는다.
- `canonical_url`이 원 URL 그대로이므로 중복 재검사·S-2 규칙은 URL 기준으로 동일하게 적용된다.

### Docx Text Extraction Adapter (업로드 docx)

기업 AX 요구사항은 `.docx`로 업로드된다(`source_channel=upload`, AXKG-SPEC-003). 업로드 `.md`는 본문(`raw_text`)이 곧 원문이라 adapter를 거치지 않지만(위 경계 각주), **`.docx`는 바이너리라 본문 텍스트 추출이 필요**하므로 이 adapter가 처리한다. 회사 프로젝트 팬아웃·정규화 계약은 AXKG-SPEC-014, project destination 결정은 AXKG-DEC-007이 SSOT다.

입력:

- `source_id`, `source_url`(업로드 파일 참조), `source_channel=upload`

처리:

1. docx 컨테이너에서 **본문 텍스트만** 추출해 `content_text`로 정규화한다.
2. `SourceMaterial`을 반환한다(`adapter=docx_text`, `content_format=doc_text`, `fetch_method=docx_text`, `canonical_url`은 업로드 파일이라 원 참조 그대로).

규칙:

- **본문 텍스트 추출만 한다.** 표 보존·이미지 대체텍스트·병합셀·중첩표·스캔이미지 처리 같은 파싱 계약은 **두지 않는다**(과설계 배제, AXKG-DEC-007 D5). 표가 텍스트로 딸려 나와도 그대로 두고, 본문/노이즈 구분·구조 정리는 요약①이 한다(web adapter가 visible text만 넘기고 본문 구분을 요약 AI에 맡기는 것과 같은 원칙).
- **기능별 구조화는 어댑터가 아니라 적응형 요약①(AXKG-SPEC-011 §4 Layer Taxonomy) 소관**이다 — 요약①이 원문(docx)의 기능 목록 구조를 그대로 따라 기능별 줄글을 산출하고, 그 산출물이 회사 프로젝트 `projects/{corp}/baseline/` 원본요약이 되어 spec 팬아웃의 입력이 된다(AXKG-SPEC-014).
- URL 기반 수집(youtube/static_web/dynamic_web)의 실패 코드·재시도 계약(§3)은 docx에 적용되지 않는다 — 업로드 파일이라 URL 원문 수집 단계가 없다. 요약 실행 자체 실패는 요약 스테이지 실패 계약(AXKG-SPEC-011)으로 표면화된다(업로드 md와 동일).

## 3. Failure Contract

| 에러 코드 | 조건 | AXKG 매핑 |
|---|---|---|
| `INVALID_URL` | HTTP(S)가 아님, 또는 YouTube로 판정된 URL에서 video id를 추출할 수 없음 | `ai_tasks.failed`, `sources.collection_failed` |
| `UNSUPPORTED_SOURCE_TYPE` | MVP adapter가 없는 URL | `ai_tasks.failed`, `sources.collection_failed` |
| `CONTENT_FETCH_FAILED` | metadata 또는 transcript API 호출 실패 | `ai_tasks.failed`, `sources.collection_failed` |
| `CONTENT_EXTRACT_FAILED` | UI 제거·후처리 후 텍스트가 최소 분량 미달 (dynamic fallback 이후에도) | `ai_tasks.failed`, `sources.collection_failed` |
| `TRANSCRIPT_UNAVAILABLE` | transcript 없음/미달 **이고** description fallback도 부실함 | `ai_tasks.failed`, `sources.collection_failed` |
| `DYNAMIC_RENDER_REQUIRED` | JS 렌더링 없이는 본문을 얻을 수 없음 | `ai_tasks.failed`, `sources.collection_failed` |
| `DYNAMIC_RENDER_FAILED` | 브라우저 렌더링 실패 또는 timeout | `ai_tasks.failed`, `sources.collection_failed` |
| `PAYWALL_OR_AUTH_REQUIRED` | 로그인, paywall, 권한 필요 | `ai_tasks.failed`, `sources.collection_failed` |
| `SOURCE_TOO_LARGE` | adapter별 size limit 초과 | `ai_tasks.failed`, `sources.collection_failed` |
| `FETCH_TIMEOUT` | timeout 초과 | `ai_tasks.failed`, `sources.collection_failed` |

위 에러 코드는 **URL 기반 수집(youtube/static_web/dynamic_web)의 실패 조건**이다. 이 실패들이 발생해도 사용자 메모가 있으면 User Note Fallback으로 수집이 성립하므로 `collection_failed`가 되지 않는다. **`sources.collection_failed`로 표면화되는 것은 "URL 원문 수집 실패 AND 메모 없음(trim 후 empty)"일 때만**이다.

**업로드 파일(`source_channel=upload`)은 위 URL 실패 계약 밖이다**: URL 수집 단계가 없어 위 에러 코드가 발생하지 않는다. `.md`는 본문이 곧 원문이라 요약 스테이지로 바로 가고, `.docx`는 위 Docx Text Extraction Adapter로 본문 텍스트만 추출한 뒤 요약 스테이지(AXKG-SPEC-011 ①)로 넘어간다. `.md`/`.docx`가 아닌 파일은 source 생성 전 intake validation에서 `UNSUPPORTED_UPLOAD_TYPE`으로 거부된다(AXKG-SPEC-003, 수집 실패 아님). 요약 실행 자체가 실패하면 다른 채널과 동일하게 요약 스테이지 실패 계약으로 표면화된다(AXKG-SPEC-011).

실패한 경우(원문 수집 실패 + 메모 없음):

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

`source_channel=upload`(md)은 이 adapter 경로를 타지 않는다 — 업로드 md 본문(`raw_text`)이 곧 원문이므로 adapter collect 단계 없이 AXKG-SPEC-011 요약 입력으로 직접 넘어간다. upload md 본문을 요약 스테이지가 소비하는 표현(SourceMaterial 합성 여부·`content_format` 값)은 구현 소관이다.

## 6. Verification

### Acceptance Criteria

- [ ] YouTube watch URL에서 video id를 추출하고 canonical URL을 만든다.
- [ ] `youtu.be` URL에서 video id를 추출하고 canonical URL을 만든다.
- [ ] YouTube metadata(description 포함)와 transcript를 `SourceMaterial`로 정규화한다.
- [ ] transcript가 없고 description이 충분하면 `content_format=video_description`으로 fallback해 성공한다.
- [ ] transcript도 없고 description도 부실하면 `TRANSCRIPT_UNAVAILABLE`로 실패한다.
- [ ] static/dynamic 두 web adapter가 **동일한** DOM 제거·metadata 추출·후처리 규칙을 적용해 `content_format=page_text`를 반환한다(차이는 텍스트 획득 방식뿐).
- [ ] web 페이지에서 title, canonical_url, content_text를 추출하고, author/published_at은 가능하면 추출하고 없으면 null로 둔다.
- [ ] 텍스트 분량 미달 또는 JS 의존 static page는 `dynamic_web` adapter로 fallback한다.
- [ ] list page(static/dynamic 모두)는 실패하지 않고 `metadata.page_kind=list`와 `metadata.links` 후보를 반환한다.
- [ ] 사이트별 내부 API endpoint는 일반 adapter에 하드코딩하지 않는다.
- [ ] dynamic fallback 후에도 텍스트 분량 미달이면(그리고 메모가 없으면) `CONTENT_EXTRACT_FAILED`로 실패한다.
- [ ] URL 수집이 모두 실패하고 사용자 메모(trim 후 non-empty)가 있으면 `adapter=user_note`·`content_format=user_note`·`content_text=메모`·`canonical_url=원 URL`인 `SourceMaterial`로 성립한다.
- [ ] URL 수집이 성공하면 메모가 있어도 원문을 우선하고 메모는 사용하지 않는다.
- [ ] 메모 기반 수집과 원문 기반 수집을 구분하는 플래그/배지를 두지 않는다(둘 다 동일한 `SourceMaterial`·`summarized`).
- [ ] unsupported URL은 `UNSUPPORTED_SOURCE_TYPE`으로 실패한다.
- [ ] 수집 실패는 `sources.collection_failed`와 실패 `ai_tasks` row로 표면화된다(단, 메모가 있으면 User Note로 성립해 실패가 아니다).
- [ ] transcript와 추출 본문 전문은 application log에 남지 않는다.
- [ ] 업로드 `.docx`는 본문 텍스트만 추출해 `adapter=docx_text`·`content_format=doc_text`인 `SourceMaterial`로 정규화하고, 표 보존·이미지 대체텍스트 등 파싱 계약을 적용하지 않는다(기능별 구조화는 요약① 소관).

## 7. Open Questions

- 수집된 `SourceMaterial` snapshot을 DB에 영구 저장할지, `ai_tasks.payload`에만 보존할지.
- dynamic adapter를 FastAPI 내부에서 실행할지 별도 browser worker/service로 분리할지.
- `page_kind=list` 결과의 후속 UX — `metadata.links`의 article 후보를 사용자가 선택해 개별 source로 등록하는 흐름은 AXKG-SPEC-003 확장으로 후속 결정. MVP는 list의 visible text가 그대로 요약 입력이 된다.
- 정교한 본문 추출(readability, article container 탐색, 텍스트 밀도 판정)은 MVP에서 하지 않는다 — page_text + AI 구분으로 시작하고, 요약 품질/토큰 비용 관찰 후 후속 최적화로 검토.
