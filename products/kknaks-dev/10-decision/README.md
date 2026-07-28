# Decision Index

규칙: `rules/product-doc-pipeline.md`

## 결정 로그

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| KDEV-DEC-001 | products 단일 루트 통합 | accepted | KDEV-BL-001 | accepted | 디렉토리 구조 |
| KDEV-DEC-002 | 지식 파이프라인 층 (루트 레벨) | accepted | KDEV-BL-001 | accepted | 디렉토리 구조 |
| KDEV-DEC-003 | 노드 타입 + 식별자(파일명 stem) | accepted | KDEV-BL-001 | accepted | 스키마 |
| KDEV-DEC-004 | 엣지 모델 + 스키마 SSOT | accepted | KDEV-BL-001 | accepted | 스키마 |
| KDEV-DEC-005 | 분류 워크플로 (독립 SSOT) | accepted (2026-07-27 개정) | KDEV-BL-001 | 정제 주체·종착지 목록 개정 (DEC-010/011) · 나머지 유효 | 워크플로 |
| KDEV-DEC-006 | 검증 게이트 L1~L6 | accepted | KDEV-BL-001 | accepted | 검증 |
| KDEV-DEC-007 | 블로그 그래프 시각화 | **superseded** (DEC-010 D7) | KDEV-BL-001 | 렌더 방식 폐기 · `_graph.json`/백링크 결정은 유효 | 시각화 |
| KDEV-DEC-008 | contents 잔류 (YouTube 요약, 그래프 무관) | accepted | KDEV-BL-001 | accepted | 디렉토리 구조 |
| KDEV-DEC-009 | 애플리케이션 DB화 토대 + 관리자 인증 방식 | accepted | KDEV-BL-002 | accepted | 관리자 인증 |
| KDEV-DEC-010 | 지식 그래프 재설계 — 4층 모델과 원자 개념(concept) 층 | accepted | KDEV-BL-003 | SPEC-001·002·004·005 반영 완료 | 디렉토리 구조 · 스키마 · 검증 · 시각화 |
| KDEV-DEC-011 | 승인 게이트 체인 — 소스별 가변 스테이지와 큐 모델 | accepted | KDEV-BL-003 | SPEC-007·008·009·003 반영 완료 | 승인 큐 · 게이트 체인 · 피드백/재생성 · 워크플로 |
| KDEV-DEC-012 | 저장·발행 경계 — draft는 DB, 확정은 md, 발행은 원자적 | accepted | KDEV-BL-003 | SPEC-010·004 반영 완료 (40-arch 대기) | Apply Executor · 검증 · database |
| KDEV-DEC-013 | 프로세스 경계 — Slack bridge를 back에 흡수 | accepted | KDEV-BL-003 | SPEC-007/010에 반영 (OKK-SPEC-011·40-arch 대기) | OKK-SPEC-011 §4 개정 · system architecture |

### 개정 관계

| 개정 주체 | 대상 | 무엇이 바뀌나 | 무엇이 유지되나 |
|---|---|---|---|
| DEC-010 | DEC-003 | 노드 타입 목록 재편(`concept` 추가·`note` 제거·`layer` 축) | stem 식별자 + `aliases` |
| DEC-010 | DEC-004 | — | 엣지 모델 전부(본문 `[[]]` + `up:` 오버레이) |
| DEC-010 D7 | **DEC-007** | force-directed 렌더 폐기 → 트리 문서 렌더러 | `_graph.json` 산출·백링크 데이터 |
| DEC-010/011 | DEC-005 | 정제 주체(사람 → AI 초안 + 사람 승인), 종착지에 `concept`·`inbox` 보류 추가 | 평행 독립 SSOT, `up:`=인용, idea 휘발, 분류=배치 |

DEC-005는 *"정제를 에이전트가 초안까지 하는 안"*을 명시적으로 기각했었다. DEC-011이 이를 뒤집되, 기각 근거였던 "연결은 본인 사고여야 한다"는 **승인 게이트가 흡수**한다 — AI는 제안만 하고 판단은 사람이 게이트에서 한다.

## 미결 사항

### 해소됨

| ID | Question | 결론 |
|---|---|---|
| ~~OQ-1~~ | medi_docs 폐기 | 완료 2026-06-29, spec-02/04는 KDEV-SPEC-002 계승 |
| ~~OQ-2~~ | force graph 라이브러리 선택 | DEC-010 D7에서 force-graph 자체 폐기 → 무효 |
| ~~DEC-010 OQ-4~~ | `layer` frontmatter 명시 vs 도출 | **도출** — 중복 SoT 회피. 빌더가 `_graph.json`에 담는다 (SPEC-002 v0.0.3) |
| ~~DEC-011 OQ-1~~ | 자동 스테이지 실패 시 회생 경로 | **메모 보완 재시도** — 메모가 있으면 원문 없이도 준비 성립 (SPEC-007 S-3) |
| ~~DEC-011 OQ-2~~ | route 목적지 조합 vs 단일 | **조합** + `inbox 보류`·`폐기`는 배타 옵션 (SPEC-008 §7) |
| ~~DEC-011 OQ-3~~ | concept 개별 vs 묶음 승인 | **묶음 승인 + 개별 제외 토글** — 개별 승인은 마찰 폭발 (SPEC-008 §7) |

### 진행 전 필요 (없음)

work 착수를 막는 미결은 없다. 아래는 전부 work 안에서 측정하거나 실전 후 판단한다.

### work 안에서 결정

| ID | Question | Next |
|---|---|---|
| SPEC-004 OQ | L2 type별 필수 필드·L4 방향 반전의 기존 데이터 위반 수 (미측정) | report-only 선행 후 측정 |
| SPEC-008 OQ | 파이프라인 정의 저장 위치 (코드 상수 vs DB vs 설정) | 게이트 체인 work |
| SPEC-010 OQ | 가상 그래프 검증 — 전체 재조립 vs 증분 | Executor work |
| DEC-012 OQ-1 | 발행 커밋 메시지 형식 | Executor work |
| DEC-012 OQ-4 | 발행 실패 반복 시 Slack 알림 임계 | Executor work |
| DEC-013 OQ-1 | 웹소켓 task 반복 실패 시 back 종료 vs 캡처만 비활성화 | 흡수 work |
| DEC-013 OQ-2 | `slack-capture` 프로필 제거 후 로컬 개발 기본값 | 흡수 work |

### 실전 관찰 후 판단 (데이터가 있어야 답 가능)

| ID | Question |
|---|---|
| DEC-010 OQ-2 | concept 입도 — "STT" 하나 vs "STT / 스트리밍 ASR / VAD" |
| DEC-011 OQ-4 | 승인 3~4회의 실제 마찰 — 게이트 병합·자동승인 검토 필요 여부 |
| DEC-012 OQ-2 | stale 거부 빈도 (concept 보충이 몰릴 때) |
| DEC-012 OQ-3 | 보호 섹션(`## 내 메모`) 도입 필요 여부 |
| SPEC-009 OQ | 피드백 최소 길이 기준, 프리셋 도입 여부 |

### 이번 범위 밖 (후속)

| ID | Question |
|---|---|
| DEC-010 OQ-1 | `reference/` group 13종 정리 (`BackendSchool`·`bitcamp` 등 교육과정 잔재) |
| DEC-010 OQ-3 | 제품 문서 중 `work`·`release`·`runbook`까지 그래프에 둘지 |
| DEC-013 OQ-3 | `app/scripts/run_*.py`의 `sys.path` 해킹 정리 |
| SPEC-003 OQ | `reference/` 157개 소급 정제 |
| SPEC-005 OQ | 게시 판정 게이트 계약 (`persona/posts/` 배선이 선행) |
| DEC-011 보류 | 커밋·블로그·스케줄 파이프라인 정의 (유튜브 체인 검증 후) |
