
# [docs] BASE-001 — 데모 에이전트 앱 baseline 등재 (기록 09 → 00-baseline)

너는 **ontology-demo `docs` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/roles/ontology-demo/docs/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline`
base 브랜치: `origin/ontology-demo` → 최종 PR 대상 `ontology-demo` (PR 은 코디네이터가 올린다)

이 워크트리는 docs 워커 단독이다 — 병렬 워커 없음.

## 1. SSOT — 먼저 읽을 것

전부 네 워크트리 안에 있다 (base 에 커밋돼 있음). 레포 루트 기준 경로:

- `para/resources/note/ontology/2026-09-01-ontology-09-agent-app-plan.md` ← **baseline 원문의 SoT.** 여기 없는 수치·결정은 발명하지 마라.
- `para/resources/note/ontology/2026-09-01-ontology-07-meta.md` · `2026-09-01-ontology-08-agent.md` — 배경 참조 (훑기만)
- `para/projects/project.md` — 문서 규칙 SoT (frontmatter·links·index·log 규약)
- `templates/projects/00-baseline/baseline.md` — 양식. 이 스켈레톤을 복사해 채운다

**기대는 개념** — 해당 없음 (baseline 은 날것 보존이 우선).

## 2. 배경 / 무엇을 바꾸나

온톨로지 실행 기록 01~08 이 완주됐고(데이터·그래프·에이전트 검증 완료), 기록 09 가
데모 앱 구축 계획을 세웠다. 이제 note 기록을 제품 문서 파이프라인(00→10→20→30)으로
내리는 첫 단계다 — **기록 09 를 `00-baseline/` 에 날것 입력 1건으로 등재한다.**

코디네이터가 준 추가 사실 (2026-09-02 사용자 확정 — 원천 기록에는 없다. 이대로만 적고 재해석 금지):

- 웹 형태는 기록 09 §3.7 의 "FastAPI 단일 페이지(또는 Streamlit)" 미결이 **정식 프론트로
  전환됐다** — 기존 `app/front/`(Next.js) 통합 3페이지: 채팅 · 모니터링 · 데이터.
  이 결정 자체는 10-decision 에서 굳힐 예정이니 baseline 에는 「가능한 방향/이후 경과」로만 부기한다.
- 디자인은 별도 세션에서 진행 중 (핸드오프 나감). baseline 범위 아님.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

고정값 — 이대로 쓴다:

- 파일: `para/projects/summer-star/ontology-demo/00-baseline/baseline-001-demo-agent-app.md`
- frontmatter: `id: BASE-001` · `type: baseline` · `status: raw` · `product: ontology-demo` ·
  tags `product/ontology-demo` · `doc/baseline` · `status/raw` · 날짜 2026-09-02
- source ref: 기록 09 wikilink (`[[2026-09-01-ontology-09-agent-app-plan]]`)

## 4. 먼저 읽을 핵심 파일

- `para/projects/summer-star/kknaks-dev/00-baseline/baseline-008-recruiter-chat.md` — 모범 baseline. 같은 결로 쓴다
- `para/projects/summer-star/ontology-demo/README.md` · `00-baseline/README.md` · `log.md` — 갱신 대상 (스캐폴딩만 된 상태)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/ontology-demo/`

## 6. 구현 단계

1. 역할 문서 → `project.md` → 양식 → 모범 baseline 순으로 읽는다.
2. 기록 09 를 정독하고 07·08 을 훑는다.
3. `baseline-001-demo-agent-app.md` 작성 — 양식 절 그대로:
   - **Raw**: 기록 09 의 핵심을 등재 — 원칙(앱은 기록 01~08 구축 순서 재현, 어느 계층이든
     원본까지 드릴다운), 아키텍처 결정 7건 표, 화면 구성 7종, 구현 순서 8단계, 게이트 5종,
     범위 밖. **본문 통복사 금지** — 요약 + 원문 링크. 수치(78,216 · 1,962 등)는 기록 09 값 그대로.
   - **Context**: 기록 01~08 완주 → 09 계획 → 문서 파이프라인 시작이라는 경위.
   - **Why It Matters**: 기록 09 가 말하는 것만 (다음 단계 수집 파이프라인의 기반, 문서가
     설명서·앱이 증명).
   - **가능한 방향**: 기록 09 구현 순서 + §2 의 프론트 전환 사실 부기.
4. index·log 동기 갱신 — `00-baseline/README.md` 표에 BASE-001 행, 제품 `README.md`
   현재 상태 표(Baseline 행), `log.md` 에 엔트리 1줄.
5. 자체 점검(frontmatter·links·PII 없음·복사 없음) 후 §9 로 보고.

## 7. 범위 제약 — 하지 말 것

- decision·spec·work 문서를 앞질러 만들지 않는다 — 이번 산출물은 baseline 1건 + index/log 갱신뿐.
- 기록 09 에 없는 결정·수치 발명 금지. 어긋남 발견 시 §9 (2) 채널로 질문.
- `reference/ontology_demo/`(원천 데이터) 접근 불필요 — 열지 마라 (PII).
- PII(실명·전화·생년월일·리뷰 작성자명)를 문서에 쓰지 않는다.
- git commit·push·PR 금지.

## 8. 검증

```
기계 검증 없음 — frontmatter·links·index·log.md 동기 갱신을 스스로 점검하고 보고에 명시. 판정은 코디네이터 검증 + 사용자 리뷰
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
  --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "docs 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] docs 완료 — <한 줄 요약>. 상세는 인박스." --enter

# 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --text "[질문] docs: <질문>" --enter
# (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
```
