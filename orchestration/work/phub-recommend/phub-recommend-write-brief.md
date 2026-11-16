
# [writer] DEC-001 — Procedure Hub 데이터 그래프 + 외부 상담 에이전트 결정 문서 초안

너는 **procedure-hub `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터 워크트리에 함께 탄다. 만들 파일은 `DEC-001.md` 1개뿐 — `_RESUME.md` · 리포트 · 브리프를 포함해 다른 파일을 고치지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 「결정」 표 ← **결정의 정본. 여기 없는 결정을 만들지 마라**
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/research-report.md` ← 현 구조 사실(수치 · 파일:줄). 배경과 근거로 인용
- 이 브리프 §3 ← 2026-10-26 사용자와 합의한 내용 전문(_RESUME 표의 요약을 풀어 쓴 것)
- 양식: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/templates/projects/10-decision/decision.md` (+ 같은 폴더 `README.md`). 쓰임 예시: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/summer-star/cc-prototype/10-decision/decision-002-cc-poc.md`

**기대는 개념**
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/areas/concept/db/medallion-architecture.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/resources/note/db/2026-09-10-data-medallion-overview.md` — 레이어 매핑은 이 노트의 4레이어(브론즈 · 실버 · 골드 · 시맨틱) 정의를 그대로 쓴다. 시맨틱은 순차 단계가 아니라 실버·골드에 의미를 붙이는 별도 책임
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/areas/concept/db/data-lineage.md` — 엣지 근거 · 응답의 발행본 버전은 리니지 요구로 설명한다

## 2. 배경 / 무엇을 바꾸나

Procedure Hub(PROCEDURE-HUB `release/v1.2.0`) 데이터로 「○○가 고민이에요」 → 추천 시술 상담을 하려 한다. 조사(research-report) 결과 고민→시술 연결이 시술군(17) 단위에서 끝나고, 시너지 · 순서 · 금기가 따로 저장돼 서로 어긋나며, 추천 경로를 읽는 코드가 호출되지 않는다.
사용자와 방향 · 경계를 합의했다. 이 합의를 **DEC-001 한 장**으로 고정한다. 다음 단계(SPEC — Hub 그래프 · tool / 에이전트)의 근거가 된다.

## 3. 계약 — 문서에 담을 결정 (사용자 합의, 2026-10-26)

D 번호는 아래 순서대로 쓴다. 각 D 에 근거(사용자 합의 · 리포트 절)를 붙인다.

- **D-01 목표** — 「○○가 고민이에요」 질의에 데이터 그래프를 탐색해 추천 시술과 근거를 돌려주는 상담. 먼저 로컬에서 세운다
- **D-02 메달리온 매핑** — 브론즈 = 원천(원장 JSON · 검수 엑셀 · 문헌) 원본 보존 / 실버 = 개체 원장(고민 · 시술 · 제품 · 부작용 · 부위 · 근거, 각 노드에 id · 동의어 · 다국어 이름) / 시맨틱 = 개체 간 관계 엣지 + 스키마 설명 / 골드 = 사용 목적별 조회(추천 · 조합 확인 · 치료계획 경로)
- **D-03 시술↔시술 관계는 엣지 하나** — 시너지 · 같은 날 가능 · 순서 · 최소 간격 · 금기 수준을 한 엣지의 속성으로 둔다. 지금의 synergy · treatment-sequence · contraindications 는 이 엣지의 브론즈 원천이 된다(리포트: 보톡스·필러 순서가 원천끼리 반대 — 코디가 stg 로 확인)
- **D-04 엣지 메타데이터** — 엣지마다 근거(출처) · 강도 · 조건(부위 · 중증도 등) · 검수 상태 · 원천(리니지)
- **D-05 Hub 의 책임 = 데이터 그래프 + 범용 조회 tool** — Hub 는 **모델을 부르지 않는다.** tool 은 읽기 전용 · 범용: 노드 검색(별칭 · 검색으로 후보만, 결정론) · 이웃 조회 · 부분 그래프 · 노드 목록/스키마 설명. MCP 와 REST 가 같은 조회 계층을 읽는다. 추천 판단 · 질의 해석 · 설명 생성은 Hub 가 하지 않는다
- **D-06 안전 엣지 동반 · 버전 표기** — 시술 노드를 내보낼 때 금기 · 간격 · 부작용 엣지를 항상 같이 낸다. 응답에 그래프 발행본 버전을 싣는다
- **D-07 Hub 가 해야 할 일 다섯** — ① 원천 보존 ② 개체 원장 ③ 관계 엣지 ④ 검증 게이트(끊긴 참조 · 원천 충돌 · 연결 빈칸 — 리포트 Q3 수치가 검사 항목) 와 발행 ⑤ 조회 tool. 그래프를 사람이 고치고 검수하는 운영 화면도 필요하다(범위는 열린 것)
- **D-08 LLM 은 전부 외부** — 외부 상담 에이전트가 `Jev(TypeSafe, 1차 판단: 발화 → 고민 · 부위 · 중증도 · 조건 슬롯을 Hub 노드 id 로) → Hub tool(부분 그래프) → 프론티어 모델(Claude, 응답 생성)` 순서로 돈다. Jev 의 선택지는 Hub 의 노드 목록/스키마 tool 로 만든다. Jev 가 신뢰도 낮다고 낸 슬롯은 프론티어 모델이 되묻는 데 쓴다. 참고: https://docs.typesafe.ai · https://simonwillison.net/2026/Sep/21/jev/
- **D-09 작업 형태** — ① Hub: PROCEDURE-HUB 를 `release/v1.2.0` 에서 새 브랜치로 따서 로컬 실행 ② 상담 채팅 에이전트: 새 개인 레포(kknaksss 계정), 로컬 실행
- **D-10 로컬 데이터 원천** — 로컬 DB 에는 dump 가 없으므로 stg 공개 GET 목록 엔드포인트(리포트 부록의 21개)를 받아 브론즈로 보관하고 거기서 실버 · 시맨틱을 만든다
- **D-11 모델 키** — Jev · Claude 키는 사용자가 보유하고 **상담 에이전트에서만** 쓴다. 값은 env 로만, 문서 · 레포에 쓰지 않는다

- **D-12 Hub 에는 LLM 이 없다(재확인)** — 브론즈 적재 · 실버/시맨틱 생성 · 검증 · tool 전부 결정론(규칙 · 정규화 · 사전). 이름 매칭에도 모델을 쓰지 않는다. 안 맞는 것은 검증 리포트에 남긴다
- **D-13 로컬 1차 임시 기본값** — 사용자가 「Hub 를 먼저 로컬 E2E 까지 세우고 다음 날 고친다」고 했다. 아래는 그걸 위한 **임시 기본값**이다. 각 줄에 「임시 — 사용자 확인 대기」를 붙이고, 같은 내용을 OQ 에도 남겨 뒤집을 자리를 둔다
  - 노드 단위: 시술군(17)과 시술 항목(521)을 **둘 다** 노드로, 둘 사이는 계층 엣지. 데이터가 시술군까지만 있는 연결은 시술군에 붙인다
  - 원천 충돌(예: 보톡스·필러 순서): 자동으로 고르지 않는다. 원천별 값을 엣지에 모두 남기고 검수 상태를 「충돌」로 표시한다
  - 저장: 같은 PostgreSQL 안에 **새 그래프 모듈 · 새 테이블**. 레거시 · canonical 테이블은 읽지도 고치지도 않는다(브론즈는 stg JSON 에서 받는다)
  - 고민 노드: taxonomy 고민 트리(problem · subcategory · item)를 고민 노드로. 다른 어휘(optimization 고민 · synergy target 등)는 별도 노드로 두고, 정규화 완전 일치일 때만 동의어 엣지로 잇는다. 안 이어진 것은 검증 리포트로
  - 큐레이션 3종: 전부 적재하고 엣지에 원천을 표시한다. 합치지 않는다
  - 부위: 위험 부위 11곳만 부위 노드로. 나머지는 OQ
  - E2E 표면: REST(Swagger) + MCP. 프론트 화면은 이번 범위 밖

**열린 것(OQ)** — 결정하지 말고 질문 + 왜 정해야 하나 + 영향받는 D 로만 적는다:
노드 단위(시술군 17 vs 시술 항목 521) · 원천 충돌 정리 주체(의료진 검수 여부) · 저장 위치(canonical 계층 확장 vs 새로 — 저장 기술 포함) · 고민 어휘 정본과 고민이 아닌 항목(쁘띠시술 · 제모 등) 처리 · 큐레이션 원장 3종(problem-combos · problem-packages · treatment-optimization) 처리 · 부위 엔티티 · Jev 한국어 성능 평가와 외부 API 로 발화가 나가는 데이터 정책 · Noul 안전 슬롯의 기준값 · 채팅 UI 형태 · 운영 화면 범위 · 회사 기획 문서(mediness `products/procedure-hub/`, v1.1.0) 반영 시점 · 회사 org 반영 여부.
리포트 Q7 의 14개 중 위와 겹치지 않는 것도 OQ 로 옮긴다.

## 4. 먼저 읽을 핵심 파일

- 위 §1 의 _RESUME · research-report(요약 · Q2 · Q3 · Q5 · Q7) · 양식 · 개념 노트

## 5. allowed_paths — 이 밖은 건드리지 마라

- 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/DEC-001.md` **1개만**

## 6. 구현 단계

1. 양식(`decision.md`)대로 DEC-001 을 쓴다. 맨 위 한 단락에 무엇을 정했는지 요약
2. D-01 ~ D-13 을 §3 순서로. 각 D 에 근거 한 줄. 리포트 수치를 인용할 때는 절 번호를 붙인다
3. 「Hub 경계」 다이어그램 1장(mermaid) — 외부 에이전트(Jev → tool 호출 → 프론티어) 와 Hub(그래프 · tool, 모델 없음) 사이 흐름
4. OQ 목록 — 질문 · 왜 정해야 하나 · 영향받는 D
5. 이 문서가 다음에 낳을 것: SPEC 두 갈래(Hub 그래프 · tool / 상담 에이전트)를 한 줄씩. SPEC 내용은 쓰지 않는다

## 7. 범위 제약 — 하지 말 것

- §3 에 없는 결정을 추가하지 않는다. 좋아 보여도 OQ 로
- 스키마 · 테이블 · API 필드 · 알고리즘 설계를 쓰지 않는다(SPEC 몫)
- PROCEDURE-HUB · 회사 문서 레포를 고치지 않는다. stg 를 다시 부르지 않는다(리포트 수치를 쓴다)
- public 레포 — 키 · 토큰 값 · 실명 금지. 「이건학」 등 사람 이름 대신 「사용자」

## 8. 검증

```
모든 결정·요구가 _RESUME §2 결정 · 조사 리포트 · 코드(파일:줄) 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. public — 키 · 토큰 · 실명 0(grep)
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
