# projects/

## 1. 개요

**정의**
- 끝이 있는 일. **지금 살아 있는 것만** 여기 남는다.
- 현역이 아니면 `archive/` 로 내린다. 지우는 것이 아니라 자리를 옮기는 것이다.

**특징**
- 유한성 : 시작과 끝이 있다.
- 국소성 : 그 프로젝트에서만 쓰는 판단을 갖는다. 어디서나 다시 쓰이면 `areas/` 로 올린다.

**구조**

```text
para/projects/
├── company/       회사 일 — 기획과 스펙의 원천이 회사 레포에 있다
└── summer-star/   여름별컴퍼니 — 기획부터 전부 여기 있다
```

소속으로 나누는 이유는 이름이 겹쳐서가 아니라 **안에 들어가는 것이 다르기 때문**이다.

**필드**

```yaml
sot: here | external        # 기획 · 스펙의 원천이 여기냐 밖이냐
status: active | done
```

`org` 는 필드로 두지 않는다. 폴더가 이미 말한다.

---

## 2. company/

**무엇**
- 회사에서 한 일. `sot: external` 이다.

**구조**

```text
company/<제품>/
├── README.md      제품 지도
├── showcase.md    공개 카드가 가리키는 상세
└── log/           작업 회고 — YYYY-MM-DD-<slug>.md
```

**스펙 단계가 없다.** 원천이 회사 레포라 복사하는 순간 어긋난다.
여기 남는 것은 **내 경험뿐**이다.

**회고는 날짜별로 `log/` 에 쌓는다.** 스펙 단계가 없어서 README 옆에 기록이 계속 쌓이면
목록이 흐려진다.

---

## 3. summer-star/

**무엇**
- 여름별컴퍼니의 제품. `sot: here` 다. 기획부터 전부 여기 있다.
- 문서 파이프라인의 목적은 문서를 늘리는 것이 아니라, **날것의 아이디어가 실제 구현
  작업으로 내려가는 경로를 고정하는 것**이다.

**구조**

```text
summer-star/<제품>/
├── README.md          제품 전체 지도
├── showcase.md        공개 카드가 가리키는 상세
├── log.md             제품 통합 변경 로그
├── log/               작업 회고 — YYYY-MM-DD-<slug>.md (오케스트레이션 SUMMARY 착지)
├── 00-baseline/       날것 입력 — 아이디어 · 요구 · 레퍼런스 · 문제 · 관찰
├── 10-decision/       baseline 을 어떻게 적용할지의 결정
├── 20-spec/           user flow · state machine · UI/UX · API 계약
├── 21-html/           spec 시각화 HTML 시안 — optional, 검증 대상 아님
├── 30-work/           spec 을 조합한 구현 작업 · acceptance · 테스트 지시
├── 40-architecture/   여러 spec · work 가 공유하는 장기 구조 — optional
├── 60-release/        배포 버전별 릴리즈 노트 — optional
├── 70-runbook/        반복 실행 절차 — optional
└── _archive/          버전 컷오프 동결본 — optional, 읽기 전용
```

### 3.1 핵심 흐름

문서는 번호 순서대로 구체화된다.

```text
00-baseline → 10-decision → 20-spec → 30-work → 60-release → log.md
```

`00` · `10` · `20` · `30` 이 뼈대다. **`40` 이상은 필요해질 때 생긴다** — 미리 파 두지 않는다.

**작업이 들어오면 종류에 따라 시작 단계가 다르다.**

| 종류 | 무엇 | 시작 위치 |
| --- | --- | --- |
| new-feature | 새 기능 구현 | `00-baseline` 또는 `10-decision` |
| spec-up | 기존 기능의 요구 · 정책 · UX 확장 | `10-decision` 또는 `20-spec` |
| refactor | 사용자 기능 변화 없이 내부 구조 개선 | `30-work` |
| bugfix | 의도와 다른 동작 수정 | `00-baseline` 또는 `30-work` |
| release | 출시 준비 · 배포 · 심사 · 운영 체크 | `30-work` (`work_type: release`) |
| ops | 지표 · 비용 · CS · 운영 자동화 | `00-baseline` 또는 `30-work` |

| 단계 | 언제 만드나 |
| --- | --- |
| `40-architecture` | 여러 spec · work 가 반복 참조하는 구조가 생겼을 때 |
| `60-release` | 실제 배포하거나 외부에 설치 가능한 버전을 낼 때 |
| `70-runbook` | 반복 실행하는 절차가 생겼을 때. 한 번 하고 마는 일은 올리지 않는다 |

### 3.2 문서별 역할

| 문서 | 역할 | 넣는 것 | 넣지 않는 것 |
| --- | --- | --- | --- |
| `README.md` | 제품 전체 지도 | 현재 상태 · 문서 맵 · 코드 레포 위치 · 최근 로그 링크 | 상세 아이디어 · 결정 근거 · spec 본문 · 작업 지시 |
| `log.md` | 통합 변경 로그 | 문서 변경 이력 · 상태 변경 · 연결 변경 | 단계별 본문 복사 |
| `log/` | 작업 회고 1건 (`company/` 의 `log/` 와 같은 층) | 오케스트레이션 작업 종료 시 SUMMARY — 새로 쓴 것 · 판단이 갈린 것 · 막혔다가 푼 것. 잔디·concept·problem 의 원료 | 「무엇을 완성했다」식 나열 · 문서 변경 이력(`log.md` 몫) |
| `00-baseline/baseline-*.md` | 날것 입력 1건 | 원문 · 배경 · 중요성 · 가능한 방향 | 확정 결정 · 구현 지시 |
| `10-decision/decision-*.md` | 결정 1건 | 선택지 · 결정 · 미결 · 영향 범위 · **근거 개념** | 상세 구현 단계 · 개념 상세 |
| `20-spec/spec-*.md` | 기능 계약 1건 | user flow · state machine · UI/UX · API · acceptance criteria | PR 계획 · 작업 순서 · 특정 work ID 참조 |
| `30-work/work-*.md` | 작업 지시 1건 | scope · code surface · phase 별 실행과 완료 증거 · rollback | 제품 결정 자체 · spec 본문 복사 |
| `40-architecture/` | 장기 구조 | ERD · 시스템 구성 · 배포 구조 | schema · migration 전문 복사 · 일회성 메모 |
| `60-release/release-*.md` | 릴리즈 노트 1건 | 버전 요약 · 수정 사항 · breaking change · rollback | 다음 버전 계획 · spec 본문 복사 |
| `70-runbook/runbook-*.md` | 실행 절차 1건 | 목적 · 절차 · 검증 · 트러블슈팅 | 배포 환경 정적 구조 · 일회성 실행 로그 |

각 단계의 `README.md` 는 **index 다** — 목록 · 상태 · 연결만 두고 본문을 복사하지 않는다.

**스키마의 SoT 는 제품 코드와 마이그레이션이다.** 문서 어디에도 전문을 복사하지 않는다.
- `20-spec` — 사용자 · QA · 프론트 · 외부 연동자에게 드러나는 것만. API 계약 · enum · 상태
- `30-work` — 구현 중 필요한 도메인 초안. aggregate 경계 · 마이그레이션 필요 여부
- `40-architecture` — 여러 곳이 반복 참조하는 경계와 invariant 만

**`10-decision` 은 근거 개념 검토 흔적을 남긴다** — frontmatter `up:` 과 본문 「근거 개념」 절.
**결론이 「없음」이어도 통과한다**(`up: []` + 사유 한 줄). 요구하는 것은 개념을 반드시 잇는
것이 아니라 **검토했다는 사실이 남는 것**이다. 억지로 이으면 계보가 거짓이 된다.
개념이 필요한데 없으면 **그 결정을 쓰는 쪽이 같은 턴에** 출처 노트와 `para/areas/concept/`
노트를 만들어 잇는다 — 판정 기준은 [[area|para/areas/area.md]] 3.3.

### 3.3 매핑

```text
BASE-001 → DEC-001 → SPEC-001 → WORK-001
```

- 상위 문서는 하위 문서의 본문을 복사하지 않고 ID 와 링크만 둔다.
- **SPEC → WORK 는 단방향이다.** spec 본문에 work ID 를 박지 않는다. work 의
  frontmatter `links.specs` 가 소유하고, spec 중심 목록은 `30-work/README.md` 의
  Spec Coverage 가 **derived view** 로 만든다. 원본에 복사하면 두 곳을 맞춰야 하고
  반드시 어긋난다.
- 관계 링크는 frontmatter `links` 에만 둔다. 본문에 중복 작성하지 않는다.

```yaml
links:
  baselines: ["[[baseline-001-...]]"]
  decisions: ["[[decision-001-...]]"]
  specs:     ["[[spec-001-...]]"]
  works:     []                        # spec 은 비워 둔다 — 위 단방향 규정
  releases:  ["[[release-001-...]]"]
```

### 3.4 frontmatter 와 상태

모든 개별 문서가 갖는다.

| 필드 | 무엇 |
| --- | --- |
| `type` | `baseline` · `decision` · `spec` · `work` · `release` · `runbook` |
| `id` | 제품 안에서 유일. `BASE-001` `DEC-001` `SPEC-001` `WORK-001` |
| `title` · `status` · `created_at` · `updated_at` · `tags` | 공통 |
| `links` | wikilink 연결 — 위 3.3 |

파일명은 사람이 읽는 slug(`spec-001-label-analysis.md`), ID 는 frontmatter 가 갖는다.
태그는 `product/<slug>` · `doc/<type>` · `status/<status>` 패턴.

**상태 값**

| type | 값 |
| --- | --- |
| baseline | `raw` → `reviewing` → `accepted` / `rejected` / `deferred` |
| decision | `proposed` → `accepted` / `rejected` / `pending` / `superseded` |
| spec | `draft` → `ready` → `in_dev` → `implemented` / `deprecated` |
| work | `todo` → `in_progress` / `blocked` / `review` → `done` |
| release | `draft` → `ready` → `released` / `failed` / `rolled_back` |
| runbook | `draft` → `active` → `deprecated` |

work 본문은 phase 단위로 추적한다. phase 상태(`TODO` `IN_PROGRESS` `DONE` `BLOCKED`
`SUPERSEDED`)와 frontmatter `status` 를 동기화한다 — 전부 TODO 면 `todo`, 하나라도 돌면
`in_progress`, 전부 DONE/SUPERSEDED 면 `done`. `30-work/README.md` 의 Status Board 가
실행 상태의 owning view 다.

### 3.5 작업 후 갱신

문서를 만들거나 고치면 **해당 단계 index(README) 와 `log.md` 를 같이 갱신한다.**
연결된 상위 index(예: decision 을 고치면 baseline index)도 함께 본다.

`log.md` 는 제품 단위 통합 로그다. 단계별 디렉토리에 별도 로그를 두지 않는다.

```markdown
| Date | Type | IDs | Summary | Links |
```

### 3.6 릴리즈와 버전 컷오프

**출시 준비 · 심사 제출 · 심사 대응은 `30-work/` 의 work 로 추적한다** —
frontmatter `work_type: release`, 양식은 `templates/projects/30-work/work-release.md`.

| 무엇 | 어디 |
| --- | --- |
| *어떻게* 제출 · 배포하나 (재사용 절차) | `70-runbook/` |
| 배포 *구조 · 환경* (환경 목록 · 타겟 · 채널) | `40-architecture/deploy/` |
| *이번* 제출 시도의 체크리스트 · 심사 결과 | `30-work/` release work |
| 출시된 *결과* 요약 | `60-release/` |

**버전 컷오프** — 한 버전으로 배포 · 심사에 나간 시점에 문서 전체를
`<제품>/_archive/vX.Y.Z/` 로 동결한다. 릴리즈 노트와 별개다 — 노트는 변경 요약,
컷오프는 문서 전체 동결.

- 동결본은 읽기 전용. 갱신은 live 에서 하고 다음 컷오프에 반영한다
- 동결본 파일명과 내부 링크에 버전 prefix(`v1_0_1-`)를 단다 — basename 이 live 와
  겹치면 옵시디언 wikilink 가 모호해져 **live 링크까지 오염**된다
- 같은 버전 폴더는 덮어쓰지 않는다

스토어 제출용 스크린샷 · 아이콘 같은 바이너리는 `70-runbook/assets/` 에만 둔다.
`assets/README.md` 가 manifest 다.

### 3.7 규약

- **디렉토리가 먼저, DB 가 나중.** 어드민 등록은 디렉토리가 있어야 열린다.
  **프로젝트의 시작은 스캐폴딩이지 등록이 아니다.**
- **`showcase.md` 가 공개 표면의 상세다.** 카드 메타(제목 · 요약 · 기술 · 상태)는 DB 행이고,
  문단짜리 상세는 여기가 원장이다. DB 는 `detail_path` 로 가리키기만 한다.
- **같은 사실은 한 곳에만 둔다.** index 는 본문을 복사하지 않고, 변경 이력은 `log.md`
  하나에만 둔다.
- **끝나면 `archive/summer-star/` 로 내린다.** 같은 모양이라 자리가 그대로 대응한다.

양식은 `templates/projects/`.

---

## 4. 맵

| 구분 | 소속 | 제품 | 내용 | 비고 |
| --- | --- | --- | --- | --- |
| 1 | `company` | `mediness` | 사내전용 AX 프로젝트 | 스펙은 회사 레포 |
| 2 | `summer-star` | `ax-knowledge-graph` | AX 기사 · 영상 · 링크를 모아 개념 · 사례 · 도구 관계를 지식그래프로 전환 |  |
| 3 | `summer-star` | `cloud-file-organizer` | Google Drive 파일을 AI 가 메타데이터 후보를 내고 사람이 승인하는 부서 문서 관리 |  |
| 4 | `summer-star` | `kknaks-agents` | LLM 을 교체 가능한 추론 모듈로 쓰는 최소 Python 런타임 라이브러리 |  |
| 5 | `summer-star` | `kknaks-dev` | 이 포트폴리오 사이트와 레포 자체 |  |
| 6 | `summer-star` | `language-diary` | AI 와 음성 대화로 일기를 만들고 영어 학습 포인트를 주는 모바일 앱 |  |
| 7 | `summer-star` | `mac-remote` | iPhone 을 Mac 리모컨으로 쓰는 앱 | DeskDeck 으로 App Store 출시 |
| 8 | `summer-star` | `mini-game` | 매일 커피 내기를 하는 모바일 웹 미니게임 |  |
| 9 | `summer-star` | `mykakao` | 카카오톡 대화를 내보내기 없이 로컬에서 추출 |  |
| 10 | `summer-star` | `open-kknaks` | PTY 기반 Claude Code CLI 태스크 큐 라이브러리 + MCP 서버 |  |
| 11 | `summer-star` | `persona-counselor` | 영향받은 책 · 인물 · 철학으로 AI 상담사 페르소나를 만들어 대화 |  |
| 12 | `summer-star` | `study-timelapse` | 공부하는 모습을 녹화해 자동 타임랩스 생성 |  |
| 13 | `summer-star` | `summer-star-company` | NFC 카드로 사무실 출퇴근 자동 트래킹 |  |
| 14 | `summer-star` | `wine-log` | 와인 기록 · 관리 모바일 앱 + 관리자 웹 + AI 라벨 분석 |  |

---

## 5. 미결

- **검증기 · pre-commit 이 없다.** 옛 구조는 파이프라인 스크립트가 3.3~3.5 를 기계로
  검증하고 pre-commit 이 `products/**` 변경마다 불렀다. `.agent/` 미착수라 지금은
  전부 사람이 지킨다. 버전 컷오프 스크립트(`version-cutoff` 스킬)도 미이관.
- ~~**개인 프로젝트의 회고** — `company/` 는 `log/` 가 있는데 여기는 없다.
  잔디가 읽을 것이 커밋 메시지뿐이다.~~ **해소 (2026-08-28)** — summer-star 에도
  `log/` 를 도입했다. 오케스트레이션 작업 종료 시 SUMMARY 가
  `<제품>/log/YYYY-MM-DD-<slug>.md` 로 착지한다(`orchestration/scripts/archive-work.sh`
  + config `summary_dest`). 첫 사례는 kknaks-dev recruiter-chat 예정.
