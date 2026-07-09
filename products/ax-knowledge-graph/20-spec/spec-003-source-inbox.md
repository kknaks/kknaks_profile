---
type: spec
id: AXKG-SPEC-003
title: "Source Inbox: URL 1차 수신 위치"
status: stable
product: ax-knowledge-graph
version: 0.0.1
created_at: 2026-07-07
updated_at: 2026-07-08
tags:
  - product/ax-knowledge-graph
  - doc/spec
  - status/stable
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
    - "[[decision-002-markdown-sot-postgres-storage|AXKG-DEC-002]]"
    - "[[decision-004-mvp-defaults-and-scope|AXKG-DEC-004]]"
  specs:
    - "[[spec-001-curation-pipeline|AXKG-SPEC-001]]"
    - "[[spec-002-approval-gate-feedback-loop|AXKG-SPEC-002]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
    - "[[spec-012-source-collection-adapter|AXKG-SPEC-012]]"
  works:
    - "[[work-002-source-intake|AXKG-WORK-002]]"
  releases: []
  related: []
---

# Source Inbox: URL 1차 수신 위치

Slack으로 들어오거나 페이지에서 직접 입력한 URL은 처음부터 reference나 permanent로 가지 않고, 미분류 raw input queue인 Source Inbox에 저장된다.

> Source Inbox는 PARA의 Inbox/Fleeting 역할이다. 아직 AI가 읽지 않았고, 아직 분류되지 않았고, 아직 영구 지식으로 승인되지 않은 입력만 담는다.

## 1. Context

### Meta

- Decision reference: AXKG-DEC-001, AXKG-DEC-002
- Baseline reference: AXKG-BL-001
- Domain note: `Source Inbox`, `Source`
- Storage: Source Inbox 상태는 PostgreSQL `sources` table에 저장한다.
- 용어: `collection`은 요약 스테이지의 "원문 수집 + 요약 생성" task 전체를 가리킨다. `collection_failed`·`queue-collection`·`COLLECTION_FAILED`는 모두 이 요약 파이프라인(AXKG-SPEC-011 ①)의 실패/재시도를 뜻하며, 별도의 수집 단계가 있는 것이 아니다.

### Business Requirement

사용자는 Slack에 AX 관련 URL을 빠르게 던지거나, 제품 페이지에서 직접 Inbox에 URL을 넣을 수 있어야 한다. 시스템은 이 입력을 잃지 않고 보존하고, source가 `received`가 되면 **자동으로** 요약 AI(①)를 실행해 제목·요약·키워드·자료 유형의 **요약 초안**을 만든다. 요약 초안은 사용자가 검토하는 게이트다 — 자동으로 분류로 넘어가지 않고, 사용자가 초안을 보고 `피드백`(재요약)하거나 `분류`(분류 게이트 진입)를 눌러야 파이프라인이 진행한다. 요약과 승인 게이트를 거치기 전에는 지식그래프의 확정 노드로 취급하지 않는다.

### Scope

In scope:

- Slack URL 1차 수신
- 페이지 내 직접 URL 입력
- raw input metadata 저장
- Source Inbox 상태 관리
- `received` 시 요약 AI 자동 트리거 상태 전이 및 재시도 상태 관리
- 요약 초안 렌더(수정 가능 형태) + 피드백 재요약(세션 resume) + `[분류]` 진입 트리거

Out of scope:

- URL 본문 탐색과 요약 생성 로직 (트리거는 여기서 자동, 탐색·요약 생성 자체는 AXKG-SPEC-001 소관)
- 분류 게이트(②)·문서화 승인 게이트(③) — `[분류]`는 여기서 트리거만, 분류 AI 실행·PARA 분류 생성·md 변환은 AXKG-SPEC-001/AXKG-WORK-004(WP3) 소관
- 영구 문서 생성
- Slack bot 인증/배포 세부

## 2. UX Contract

### Placement

Source Inbox는 제품의 첫 큐 화면이다.

```text
+--------------------------------------------------+
| Source Inbox                                     |
+---------------------+----------------------------+
| Received Sources    | Selected Source             |
| - received          | URL                         |
| - summarizing       | Slack metadata              |
| - summarized        | Raw text                    |
| - collection_failed | (재시도 가능)               |
+---------------------+----------------------------+
```

### U-1. Source Inbox List

- **상태**: 비어 있음, 수신됨, 요약 중, 요약 완료, 요약 실패
- **문구**: URL, 수신 채널, 수신 시각, 제출자, 상태
- **CTA**: `Inbox에 넣기`, `열기`, `무시`, `삭제`
- **기대 결과**: `Inbox에 넣기`를 누르면 URL 입력 모달이 열린다. source가 `received`가 되면 별도 조작 없이 자동으로 요약 AI(①)가 실행되어 `summarizing → summarized`로 전이한다. 요약이 끝난(`summarized`) 항목을 열면 U-2의 요약 초안 검토로 들어간다 — **요약이 자동으로 분류로 넘어가지 않고**, 사용자가 초안을 검토해 `분류`를 눌러야 AXKG-SPEC-001의 분류 게이트로 진입한다.

### U-2. Source Detail · 요약 초안 검토

- **상태**: 선택 없음, source 선택됨(요약 중 / 요약 완료(초안) / 요약 실패)
- **문구**: 원본 URL, Slack 메시지 링크, raw text(메모), 제출자, 수신 시각, 요약 상태. `summarized`이면 요약 초안(제목·요약·키워드·자료 유형)을 **수정 가능한 형태**로 렌더한다 — 문서보기 모달(요약 md 미리보기)과 폼(제목/요약/키워드 필드) 두 표면.
- **CTA**:
  - `summarized`(요약 초안): `피드백`(자연어 입력 → 세션 resume 재요약, `summary_payload` v2 갱신) · `분류`(분류 게이트로 진입 트리거, AXKG-SPEC-001)
  - `collection_failed`: `메모 추가`/`메모 수정` · `요약 재시도`
  - 공통: `Source 삭제`
- **기대 결과**: source의 원본 정보와 요약 진행 상태를 확인한다.
  - 요약이 끝나면(`summarized`) 요약 초안이 수정 가능한 형태로 뜬다. 사용자는 `피드백`으로 원하는 방향을 자연어로 남겨 재요약(v2)을 받거나, 초안이 만족스러우면 `분류`를 눌러 분류 게이트로 진입시킨다. **요약이 자동으로 분류로 넘어가지 않는다 — 사용자가 `분류`를 눌러야 진입한다.** 요약 초안은 `sources.summary_payload`에 임시 저장되고 재요약 시 v2로 갱신된다(확정 md 파일은 문서화 후 — AXKG-WORK-004/WP3). 피드백 재생성은 직전 초안(v1)을 참조로 두고 세션 resume로 원문·지침 재전송 없이 이어서 생성한다(버전·resume 규칙 AXKG-SPEC-002, 배선 AXKG-SPEC-011).
  - 요약이 실패했으면(`collection_failed`) `요약 재시도`로 다시 자동 요약을 태울 수 있다. **원문 수집이 안 되는 사이트(Cloudflare/봇 방어 등)라 `collection_failed`가 된 경우, 사용자는 메모(복붙 텍스트 등)를 추가·수정한 뒤 재요약할 수 있고, 그러면 그 메모를 원문 대신 요약 입력으로 삼아(AXKG-SPEC-012 User Note Fallback) `summarized`에 도달할 수 있다.** 메모 기반 요약과 원문 기반 요약을 UI에서 구분 표기하지 않는다.

### U-3. Direct Inbox Modal

- **상태**: 닫힘, 열림, 제출 중, 제출 실패, 중복 URL
- **문구**: URL, 메모, 출처 채널, 제출자, 저장
- **CTA**: `저장`, `취소`
- **기대 결과**: 사용자가 URL을 입력하고 `저장`하면 `source_channel=manual`인 Source가 `received` 상태로 Source Inbox에 추가된다. 여기서 입력한 **메모(`note`)는 원문 수집이 실패했을 때 요약 입력으로 쓰이는 fallback 소스다**(AXKG-SPEC-012 User Note Fallback). URL 수집이 성공하면 원문을 우선하고 메모는 요약에 쓰지 않는다.

## 3. User Scenario

### S-1. User — Slack 슬래시 커맨드로 URL을 던진다

1. 사용자는 Slack 채널 또는 DM에서 슬래시 커맨드로 `<커맨드> <URL>`을 입력한다. 원문 수집이 어려운 링크는 메모를 함께 넘길 수 있다: `<커맨드> <URL> << 메모 내용 >>` — `<< >>`로 감싼 텍스트가 메모다.
2. Slack은 등록된 Request URL로 커맨드 payload(command/text/channel_id/user_id/team_id/trigger_id)를 POST한다.
3. 시스템은 서명을 검증하고 `text`에서 URL을 추출한다. URL이 없거나 형식이 틀리면 사용법을 ephemeral로 안내하고 저장하지 않는다. URL 추출 후 `text`에 `<< >>`로 감싼 구간이 있으면 그 안(trim 후 non-empty)을 메모(`raw_text`)로 저장한다. `<< >>`가 없으면 메모 없음이다.
4. 유효하면 시스템은 URL을 Source Inbox에 `received`(`source_channel=slack`) 상태로 저장하고, 3초 내에 "접수" ephemeral ack를 반환한다. `trigger_id` 기반 합성 키로 더블서밋을 막는다.
5. 슬래시 커맨드는 채널 메시지를 남기지 않으므로, 접수 후 봇이 채널에 앵커 메시지를 post하고 그 `ts`를 source metadata에 저장한다.
6. 저장 즉시 시스템은 요약 AI(①)를 자동 실행하고 source를 `summarizing`으로 전이한다.
7. 요약이 끝나면 source는 `summarized`가 되어 봇이 앵커 스레드에 요약 초안을 회신하고, 실패하면 `collection_failed`가 되어 실패 사유를 스레드에 회신하고 재시도할 수 있다.
8. 이 시점의 source는 reference, permanent, product 문서가 아니다. 요약 초안은 `sources.summary_payload`(DB 임시)일 뿐이다.
9. 사용자는 Source Inbox에서 URL과 요약 초안을 확인하고, U-2에서 `피드백`으로 재요약하거나 `분류`를 눌러 AXKG-SPEC-001의 분류 게이트로 진입시킨다. 요약이 자동으로 분류로 넘어가지 않는다.

### S-2. System — 중복 URL이 들어온다

1. 같은 URL이 다시 들어온다.
2. 시스템은 기존 Source가 있는지 확인한다.
3. 기존 Source가 아직 `documented` 전이면 새 Slack 메시지 metadata를 기존 Source에 연결한다.
4. 기존 Source가 이미 문서화되었으면 새 입력을 duplicate candidate로 표시한다.

### S-3. User — 페이지에서 직접 Inbox에 URL을 넣는다

1. 사용자는 Source Inbox 화면에서 `Inbox에 넣기`를 누른다.
2. 시스템은 URL 입력 모달을 연다.
3. 사용자는 URL과 선택 메모를 입력한다.
4. 사용자가 `저장`을 누르면 시스템은 URL을 검증한다.
5. 시스템은 `source_channel=manual`인 Source를 `received` 상태로 저장한다.
6. 저장된 Source는 Slack으로 들어온 Source와 같은 Source Inbox 목록에 표시된다.

## 4. Interface Contract

### API Contract

| Method | Path | 요약 | 권한 |
|---|---|---|---|
| POST | `/api/v1/slack/commands` | Slack 슬래시 커맨드 수신 → `text`에서 URL 추출·Source Inbox 저장. Slack 등록 Request URL과 문자 그대로 일치(다른 라우트의 무prefix 관례에 대한 예외, rewrite 없음) | slack signing secret |
| POST | `/sources/manual` | 페이지에서 직접 입력한 URL을 Source Inbox에 저장 | owner |
| GET | `/sources?status=received` | Source Inbox 목록 조회 | owner |
| GET | `/sources/{source_id}` | Source 원본 정보 조회 | owner |
| POST | `/sources/{source_id}/queue-collection` | `collection_failed` source의 요약 재시도 (정상 흐름은 `received` 시 자동 트리거이므로 수동 호출 불필요). optional `note`를 함께 보내면 source 메모(`raw_text`)를 갱신한 뒤 재큐한다 — 원문 수집 불가 사이트에 메모를 추가·수정해 재요약하는 경로(User Note Fallback). 최종 파라미터 형태는 BE 구현과 정합 | owner |
| GET | `/sources/{source_id}/ai-tasks` | source와 연결된 AI task 이력 조회 | owner |
| POST | `/sources/{source_id}/ignore` | source를 `ignored`로 전이 (파이프라인 제외, row 보존) | owner |
| DELETE | `/sources/{source_id}` | source soft delete → `deleted`(+`deleted_at`), row 보존·기본 목록 숨김 | owner |

### Request / Response

Slack 수신 요청은 슬래시 커맨드 payload(command/text/channel_id/user_id/team_id/trigger_id)이며, URL은 `text`에서 추출한다. 수동 입력 요청은 URL과 선택 메모를 포함한다.

### Validation

| 필드 | 규칙 |
|---|---|
| `source_url` | `http` 또는 `https` URL. Slack은 커맨드 `text`에서 추출(없거나 형식 오류면 저장하지 않고 사용법 ephemeral) |
| `source_channel` | `slack` 또는 `manual` |
| `slack_message_ts` | 접수 후 봇이 post한 앵커 메시지 timestamp(요약 회신 스레드 기준). 수동 입력이면 `null` |
| `submitted_at` | ISO timestamp |
| `raw_text` | 선택값. 수동 입력 메모, 또는 Slack 커맨드 `text`의 `<< >>` 안 텍스트. 원문 수집 실패 시 요약 입력이 되는 fallback 메모다(AXKG-SPEC-012 User Note Fallback). "있음/없음"은 trim 후 non-empty 기준 |
| `trigger_id` | Slack 슬래시 커맨드 멱등 키 원천(더블서밋 차단), Slack 수신 시에만 |

### Case Matrix

| 에러 코드 | 백엔드 출력 | 프론트 출력 | 표시 위치 |
|---|---|---|---|
| `INVALID_URL` | URL 형식 오류 | 올바른 URL이 아닙니다. | Source Detail |
| `DUPLICATE_SOURCE` | 기존 Source 존재 | 이미 받은 URL입니다. 기존 항목에 연결했습니다. | Source Inbox List |
| `SLACK_URL_MISSING` | 커맨드 `text`에 URL 없음/형식 오류 | 사용법: `<커맨드> <URL>` 형식으로 링크를 함께 보내주세요. | Slack ephemeral |
| `MANUAL_NOTE_TOO_LONG` | 수동 메모 길이 초과 | 메모는 2000자 이하로 입력해 주세요. | Direct Inbox Modal |
| `COLLECTION_RETRY_NOT_ALLOWED` | 재시도 불가 상태 | 현재 상태에서는 요약을 재시도할 수 없습니다. | Source Detail |

### Flow

Slack 입력 (슬래시 커맨드):

```mermaid
sequenceDiagram
    actor User
    participant Slack
    participant AX as AX Product
    participant Store

    User->>Slack: /커맨드 URL 입력
    Slack->>AX: POST /api/v1/slack/commands (서명된 payload)
    AX->>AX: 서명 검증 + text에서 URL 추출
    AX->>Store: Source Inbox에 received 저장 (source_channel=slack)
    AX-->>Slack: 3초 내 ephemeral ack ("접수")
    AX->>Slack: 봇이 채널에 앵커 메시지 post
    Slack-->>AX: 앵커 ts
    AX->>Store: source metadata에 앵커 ts 저장
    Note over AX,Store: summarized/collection_failed 도달 시 봇이 앵커 스레드에 회신
```

페이지 직접 입력:

```mermaid
sequenceDiagram
    actor User
    participant FE
    participant AX as AX Product
    participant Store

    User->>FE: Inbox에 넣기
    FE->>FE: URL 입력 모달 표시
    User->>FE: URL + 메모 저장
    FE->>AX: POST /sources/manual
    AX->>AX: URL/metadata 검증
    AX->>Store: Source Inbox에 저장
    AX-->>FE: Source 반환
```

### State / Lifecycle

이 상태 모델은 제품 전체의 source lifecycle SSOT다. `received`부터 `summarized`까지가 Source Inbox 소관이고, `summarized` 이후 승인 게이트 흐름은 AXKG-SPEC-001이 이어받는다. 최종 문서가 생성된 source는 삭제하지 않고 `documented`로 전이해 기본 Inbox 목록에서 숨긴다.

```mermaid
stateDiagram-v2
    [*] --> received
    received --> summarizing: 자동 트리거 (요약 AI ①)
    summarizing --> summarized
    summarizing --> collection_failed
    collection_failed --> summarizing: 요약 재시도
    received --> ignored
    summarized --> [*]: AXKG-SPEC-001 승인 게이트로
    summarized --> documented: 문서화 승인 완료
    summarized --> archived: 분류 게이트 destination=archive 승인 (AXKG-SPEC-001)
    documented --> archived: 목록 숨김 유지/운영 archive
    received --> deleted: soft delete
    summarized --> deleted: soft delete
    ignored --> [*]
    archived --> [*]
    deleted --> [*]
```

### Data Contract

| Resource | Field | 설명 |
|---|---|---|
| Source | `id` | 제품 내부 source 식별자 |
| Source | `source_url` | Slack 또는 수동 입력으로 들어온 원본 URL |
| Source | `source_channel` | `slack`, `manual` |
| Source | `slack_message_ts` | 접수 후 봇 앵커 메시지 timestamp(요약 회신 스레드 기준). 수동 입력이면 `null` |
| Source | `submitted_at` | 수신 시각 |
| Source | `submitted_by` | Slack 사용자 식별자 또는 제품 사용자 식별자 |
| Source | `raw_text` | Slack 메시지 원문 또는 수동 입력 메모 |
| Source | `status` | `received`, `summarizing`, `summarized`, `collection_failed`, `ignored`, `documented`, `archived`, `deleted` |
| Source | `visible_in_inbox` | 기본 Inbox 목록 표시 여부. `documented`, `archived`, `deleted`는 기본 false |

`archived`의 진입 경로는 두 가지이며 상태는 하나다: (1) 분류 게이트에서 destination=archive 승인(`summarized → archived`, 문서·연결 생성 없음), (2) `documented` 이후 운영상 보관. 두 경우 모두 목록에서 숨기고 row는 보존한다.
| Source | `documented_at` | 최종 문서화 완료 시각 |
| Source | `deleted_at` | soft delete 시각. hard delete는 MVP 범위 밖 |

### Source Inbox Document Form

Source Inbox를 파일 기반으로 남기거나 UI에서 preview할 때는 아래 양식을 따른다. 이 문서는 승인된 지식 문서가 아니라 raw source record다.

필수 frontmatter:

| Field | 설명 |
|---|---|
| `type` | `source` |
| `id` | 제품 내부 source id |
| `status` | `received`, `summarizing`, `summarized`, `collection_failed`, `ignored`, `documented`, `archived`, `deleted` |
| `source_channel` | `slack` 또는 `manual` |
| `source_url` | 원본 URL |
| `submitted_at` | 수신 시각 |
| `submitted_by` | Slack 사용자 식별자 또는 제품 사용자 식별자 |
| `slack_message_ts` | 접수 후 봇 앵커 메시지 timestamp. 수동 입력이면 `null` |
| `classification_gate` | 아직 없으면 `null` |
| `destination_type` | 아직 분류 전이면 `null` |

필수 본문 섹션:

| Section | 역할 |
|---|---|
| `## Raw Input` | Slack 원문과 URL을 보존 |
| `## Source Metadata` | 채널, 제출자, 수신 시각, Slack thread/message 정보 |
| `## Collection Status` | AI 수집 전/후 상태와 실패 사유 |
| `## Next Gate` | 다음에 생성해야 할 승인 게이트 |

Source Inbox 문서는 다음 내용을 넣지 않는다.

- AI가 정리한 최종 reference note 본문
- 사용자가 승인한 permanent note
- 제품 decision/spec 본문
- 문서화 승인 게이트의 최종 승인 연결 목록

## 5. Implementation Rules

- Slack URL과 페이지에서 직접 입력한 URL은 1차로 Source Inbox에만 저장한다.
- Slack intake는 슬래시 커맨드로 받는다. Slack이 등록된 Request URL(`POST /api/v1/slack/commands`, 등록 문자열과 그대로 일치)로 커맨드 payload를 POST한다. 이 경로는 토큰 로그인(AXKG-SPEC-008) 대상이 아니라 Slack signing secret 서명 검증으로 보호하며, 서버는 커맨드 이름과 무관하게 `text`의 URL로 동작한다.
- 슬래시 커맨드 수신 시 3초 내 ephemeral ack("접수")를 반환하고, `trigger_id` 기반 합성 키로 더블서밋을 막는다. `text`에 유효한 URL이 없으면 사용법을 ephemeral로 안내하고 저장하지 않는다.
- 접수 후 봇이 채널에 앵커 메시지를 post하고 그 `ts`를 source metadata에 저장한다. `summarized` 도달 시 앵커 스레드에 요약 결과를, `collection_failed` 시 실패 사유를 회신한다.
- Source Inbox의 항목은 승인된 지식이 아니므로 reference/permanent/product 문서로 간주하지 않는다.
- Source Inbox 항목을 파일 또는 preview 문서로 표현할 때는 AXKG-SPEC-003의 Source Inbox Document Form을 따른다.
- source가 `received`가 되면 사용자 조작 없이 자동으로 요약 AI(①)를 실행하고 `summarizing`으로 전이한다. 요약 성공은 `summarized`, 실패는 `collection_failed`이며 `collection_failed`는 재시도할 수 있다.
- 요약이 끝나(`summarized`) 만들어진 요약 초안은 `sources.summary_payload`(DB 임시)에 저장되고, U-2에서 수정 가능한 형태(문서보기 모달·폼)로 렌더된다. 확정 md 파일 변환은 이 spec 범위 밖이다(문서화 승인 후 — AXKG-WORK-004/WP3).
- **요약이 자동으로 분류로 넘어가지 않는다.** `summarized`는 게이트 상태이며, 사용자가 U-2에서 `분류`를 눌러야 분류 게이트로 진입한다(`POST /sources/{source_id}/classification-gates`, AXKG-SPEC-001). 이 spec은 진입 트리거까지이고 분류 AI 실행·PARA 분류 생성은 AXKG-SPEC-001 소관이다.
- 요약 초안 `피드백`은 자연어 입력을 받아 재요약(v2)을 실행한다. 재요약은 새 `ai_tasks` row로 실행되고 직전 요약 실행의 `open_kknaks_session_id`를 resume로 이어서(원문·방법 지침 재전송 없이) 피드백만 반영하며, 결과로 `sources.summary_payload`를 v2로 갱신한다(버전·resume 규칙 AXKG-SPEC-002, submit 배선 AXKG-SPEC-011). 직전 초안(v1)은 참조로 보존한다. 피드백/재요약 API의 최종 파라미터 형태는 BE 구현과 정합한다(코드 병렬 태스크 소관).
- 요약 초안 단계에는 승인/잠금 개념이 없다. 사용자는 만족할 때까지 `피드백`으로 재요약하고, `분류`로만 다음 단계로 넘어간다.
- 원문 수집 계약과 수집 가능 범위는 AXKG-SPEC-012 소관이다(MVP: YouTube·정적 웹·동적 웹. PDF/RSS 등은 `UNSUPPORTED_SOURCE_TYPE`으로 `collection_failed` 보존, 재시도 대신 "지원 예정 형식" 안내 병기).
- URL 원문 수집이 모두 실패해도 source에 메모(`raw_text`, trim 후 non-empty)가 있으면 그 메모를 요약 입력으로 삼아 `summarized`에 도달한다(AXKG-SPEC-012 User Note Fallback). `collection_failed`는 "원문 수집 실패 AND 메모 없음"일 때만이다. URL 수집이 성공하면 원문을 우선하고 메모는 요약에 쓰지 않는다.
- `collection_failed` source에는 메모를 추가·수정한 뒤 재요약할 수 있다. 메모 갱신 재요약은 `queue-collection`에 `note`를 함께 보내 `raw_text`를 갱신하고 새 `ai_tasks` row로 재큐한다(기존 실패 task 보존). 메모 기반 요약과 원문 기반 요약을 상태·payload·UI에서 구분 표기하지 않는다(source_basis 플래그/배지 없음).
- 수집 성공 시 adapter의 `canonical_url` 기준으로 `normalized_url`을 갱신하고 중복을 재검사한다. 기존 source와 합류하면 S-2 중복 규칙을 따른다(AXKG-SPEC-012).
- 요약 AI 실패 시 실패한 `ai_tasks` row를 보존하고 `sources.status=collection_failed`로 전이한다. Source Detail에는 최신 실패 task의 `error_message`와 `요약 재시도` CTA를 표시한다.
- `요약 재시도`는 기존 failed task를 덮어쓰지 않고 새 `ai_tasks` row를 만든다. 새 task는 `retry_of_task_id`로 원 failed task를 참조한다.
- 요약 이후 source는 분류 게이트(②, AXKG-SPEC-001)에서 `project`, `area`, `resource`, `archive` 중 하나로 분류되고, archive 외 destination은 문서화 승인 게이트(③, AXKG-SPEC-004)로 이어진다.
- 문서화 승인 게이트가 최종 승인되고 `documents` row가 생성되면 source는 `documented`가 된다.
- `documented` source는 기본 Source Inbox 목록에서 보이지 않지만, source detail/history와 문서 trace에서는 조회 가능해야 한다.
- Source Inbox에서 삭제한 항목은 hard delete하지 않고 `deleted` 상태와 `deleted_at`을 남기는 soft delete로 처리한다.
- Source Inbox에서 삭제 또는 무시한 항목은 영구 문서화 파이프라인으로 넘어가지 않는다.
- 중복 URL은 새 source를 무조건 만들지 않고 기존 source와 연결할 수 있어야 한다.

## 6. Verification

### Acceptance Criteria

- [ ] Slack URL이 들어오면 Source Inbox에 `received` 상태로 저장된다.
- [ ] 사용자는 페이지에서 `Inbox에 넣기`를 눌러 URL 입력 모달을 열 수 있다.
- [ ] 수동 URL을 저장하면 `source_channel=manual`인 Source가 `received` 상태로 저장된다.
- [ ] 저장된 Source에는 URL, Slack metadata, raw text, 수신 시각이 남는다.
- [ ] Source Inbox 파일/preview는 AXKG-SPEC-003의 필수 frontmatter와 본문 섹션을 따른다.
- [ ] Source Inbox 항목은 reference/permanent/product 문서로 취급되지 않는다.
- [ ] source가 `received`가 되면 자동으로 `summarizing`으로 전이하고 요약 AI가 실행된다.
- [ ] 요약 실패(`collection_failed`) source는 재시도할 수 있다.
- [ ] 요약 재시도는 새 ai_task로 실행되고 기존 실패 task는 보존된다.
- [ ] Slack 커맨드 `text`에 `<< 메모 >>`가 있으면 그 안 텍스트를 `raw_text` 메모로 저장한다(없으면 메모 없음).
- [ ] URL 원문 수집이 실패해도 메모가 있으면 `summarized`에 도달하고, 메모가 없을 때만 `collection_failed`가 된다.
- [ ] `collection_failed` source에 메모를 추가·수정해 재요약하면 그 메모로 요약이 성립한다.
- [ ] 메모 기반 요약과 원문 기반 요약을 상태·UI에서 구분 표기하지 않는다.
- [ ] `summarized` source의 요약 초안이 U-2에서 수정 가능한 형태(문서보기 모달·폼)로 렌더된다.
- [ ] 요약이 자동으로 분류로 넘어가지 않고, 사용자가 `분류`를 눌러야 분류 게이트로 진입한다.
- [ ] 요약 초안 `피드백`은 세션 resume 재요약으로 `summary_payload`를 v2로 갱신하고 직전 초안(v1)은 참조로 보존한다.
- [ ] 요약 이후 분류 목적지는 Source Inbox가 아니라 AXKG-SPEC-001의 승인 게이트에서 확정된다.
- [ ] 최종 문서화된 source는 `documented`가 되고 기본 Inbox 목록에서 숨겨진다.
- [ ] 삭제한 source는 hard delete하지 않고 `deleted` 상태로 soft delete된다.
- [ ] 중복 URL은 기존 Source와 연결되거나 duplicate candidate로 표시된다.

## 7. Open Questions

없음. Slack intake는 슬래시 커맨드 payload에서 URL과 metadata 중심으로 저장하고, Source Inbox는 PostgreSQL `sources` table로 관리한다.
