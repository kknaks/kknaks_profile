
# [docs] DEC-001~005 작성 + BASE-001 accepted 처리

너는 **ontology-demo `docs` 워커**다. 직전 태스크(BASE-001)와 같은 워크트리에서 이어서 작업한다.
역할 문서(전 태스크에서 읽음): `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/roles/ontology-demo/docs/` 5종.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline`
base 브랜치: `origin/ontology-demo` → 최종 PR 대상 `ontology-demo` (PR 은 코디네이터가 올린다)

이 워크트리는 docs 워커 단독이다. **직전 태스크의 미커밋 산출물(BASE-001 등 4파일)을 건드리지 말고 그 위에 쌓아라** — 단, 이번 지시에 포함된 BASE-001 갱신은 예외다.

## 1. SSOT — 먼저 읽을 것

- `para/projects/summer-star/ontology-demo/00-baseline/baseline-001-demo-agent-app.md` — 네가 만든 BASE-001. decision 들의 상위 입력
- §3 의 「결정 사실 목록」 ← **이번 decision 본문의 SoT. 사용자가 2026-09-02 문답으로 확정한 것들이다. 여기 없는 결정을 발명하지 마라.**
- `para/projects/project.md` §3.2·§3.3·§3.4 — decision 규칙 (`up:` 포함)
- `templates/projects/10-decision/decision.md` — 양식
- `para/projects/summer-star/kknaks-dev/10-decision/decision-027-chat-ai-execution-and-tool-boundary.md` — ADR-04 의 실체 (DEC-003 이 참조할 기존 결정) + 모범 decision 문서

**기대는 개념** — decision frontmatter `up:` 은 `para/areas/concept/` (ai·back·db·infra 등 9영역)에서
관련 개념을 검토해 잇는다. **필요한데 없는 개념은 만들지 말고** 질문 목록에 「개념 필요: <무엇>」으로
보고만 해라 — 개념 노트 생성은 코디네이터 몫(allowed_paths 밖). 검토 결과 없으면 `up: []` + 사유 한 줄.

## 2. 배경 / 무엇을 바꾸나

BASE-001 이 등재됐고 사용자 리뷰로 **accepted** 됐다. 이제 2026-09-02 사용자 문답으로 확정된
결정 5건을 `10-decision/` 에 내리고, BASE-001 의 상태·links 를 동기화한다.

## 3. 계약 — 결정 사실 목록 (이대로 굳힌다. 전건 status: accepted, 날짜 2026-09-02)

파일명·ID 고정:

| ID | 파일 | 제목 요지 |
|---|---|---|
| DEC-001 | `decision-001-db-medallion-all-layers.md` | DB = 메달리온 전 계층 + 빌드의 DB 이식 |
| DEC-002 | `decision-002-pii-masking-boundary.md` | PII = 원값 DB 보존 + 표시·응답 마스킹 |
| DEC-003 | `decision-003-llm-via-open-kknaks-mcp.md` | LLM 경로 = open-kknaks + MCP 도구 |
| DEC-004 | `decision-004-web-three-pages-in-front.md` | 웹 = app/front 통합 3페이지 |
| DEC-005 | `decision-005-internal-demo-deploy.md` | 배포 = 내부 공개 데모 (비밀번호 게이트) |

각 건의 확정 내용 (Options 절은 기록 09·문답에서 실제 있었던 대안으로 짧게 재구성, Decision 절은 아래 그대로):

- **DEC-001** — SQLite 한 DB 에 `bronze_*`(원형) + `silver_*` + `gold_*` + `ontology_*`(nodes·edges)
  전부 적재. 기존 build 스크립트의 입출력을 파일→DB 로 전환하되 변환 규칙·게이트는 기록 04·05
  그대로(이식이지 재설계 아님). 근거: 브론즈가 있어야 재처리·감사·드릴다운 성립, 다음 단계
  수집 파이프라인이 이 빌드의 자동 트리거가 되게. (기록 09 §1 — 2026-09-01 합의의 기록)
- **DEC-002** — PII(`patientName`·`phone`·`birthday`·리뷰 작성자명)는 DB 에 원값 보존, 화면·API·
  에이전트 응답에서 마스킹 표시. 에이전트의 브론즈 접근도 마스킹 뷰 경유만. 게이트: 노출 0건.
  전제: 내부 공유용 데모(DEC-005)라 배포용 PII 소거 사본은 만들지 않는다 — 이 전제가 바뀌면
  (외부 공개 전환) 이 결정을 재검토한다.
- **DEC-003** — LLM SDK 직접 import 금지, 실행은 open-kknaks(AgentClient + RedisBroker) 경유
  (ADR-04 = kknaks-dev decision-027 현행 유지). provider 는 codex(gpt-5.6-terra). 조회 도구
  4종은 `app/ontology-agent/tools/` 에 FastMCP(Streamable HTTP) 서버로 — codex 가 MCP
  클라이언트로 붙는다(모범: `app/mcp/`). 채팅 UX 는 기본 클로드형 자유 대화. 근거: S-001(관계는
  데이터에)·S-002(Agent 는 판단만 — 파라미터화된 조회만, 자유 SQL 금지)를 프로토콜로 강제,
  LLM 교체 가능.
- **DEC-004** — 기록 09 §3 7단계의 「FastAPI 단일 페이지(또는 Streamlit)」 미결을 뒤집어
  정식 프론트로: 기존 `app/front/`(Next.js 15 App Router) 통합 3페이지 — 채팅 · 모니터링 ·
  데이터. 화면 7종 매핑: 데이터=①②③ 계층 탐색, 모니터링=④⑤⑥ KPI·그래프·예보, 채팅=⑦.
  백엔드는 `app/ontology-agent/`(FastAPI, API 서버로 역할 축소 — static 단일 페이지 폐기).
  디자인은 별도 세션 진행 중 — 화면 상세·채팅↔그래프 하이라이트 방식은 SPEC 단계 미결로 명기.
- **DEC-005** — 데모를 내부 공유용으로 배포한다: 프론트는 Vercel(기존 profile 배포에 포함),
  백엔드 + redis + open-kknaks codex 워커는 홈서버(docker + NPM 서브도메인). 접근 가드는
  공유 비밀번호 하나(내부 공유) — 채팅 rate limit·토큰 상한 등 추가 가드 없음. 배포 DB 사본은
  홈서버 볼륨(레포 밖) — 원천·DB gitignore 정책 유지. 「실시간」 표방 금지(일 배치)는 그대로.

frontmatter `links.baselines` 는 전건 `[[baseline-001-demo-agent-app]]`.

## 4. BASE-001 동기 갱신

- frontmatter: `status: raw → accepted` (tags 의 `status/raw` 도 동기), `updated_at: 2026-09-02`,
  `links.decisions` 에 DEC-001~005 wikilink 5건.
- `00-baseline/README.md` 표: Status `accepted`, Decision 열에 DEC-001~005.
- `10-decision/README.md` index 표에 5행, 제품 `README.md` 현재 상태 표(Baseline·Decision 행),
  `log.md` 엔트리(baseline-accept 1줄 + decision-add 1줄).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/ontology-demo/`

## 6. 구현 단계

1. §1 SSOT 읽기 (모범 decision 포함).
2. DEC-001~005 작성 — 양식 스켈레톤 복사, §3 사실 그대로. 각 건 `up:` 검토(§1 규칙).
3. §4 의 BASE-001·index·log 동기 갱신.
4. 자체 점검(frontmatter·links 정합·본문 복사 없음·PII 없음) 후 §9 보고 — 질문 목록(개념 필요 건 포함) 명시.

## 7. 범위 제약 — 하지 말 것

- spec·work 선작성 금지. `para/areas/concept/` 생성·수정 금지(검토·인용만).
- §3 에 없는 결정·수치 발명 금지. 어긋남·빈칸은 질문으로.
- `reference/ontology_demo/` 열지 마라. PII 원값 금지. git commit·push·PR 금지.

## 8. 검증

```
기계 검증 없음 — frontmatter·links·index·log.md 동기 갱신을 스스로 점검하고 보고에 명시. 판정은 코디네이터 검증 + 사용자 리뷰
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "docs 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과 / 계약 준수 / 질문·미결"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] docs 완료 — <한 줄 요약>. 상세는 인박스." --enter

# 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --text "[질문] docs: <질문>" --enter
```
