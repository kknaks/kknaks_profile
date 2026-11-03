
# [researcher] Procedure Hub 데이터 구조 파악 — 「○○가 고민이에요」 추천에 쓸 수 있나

너는 **procedure-hub `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터 워크트리에 함께 탄다. 이 워크트리에서 만들 파일은 리포트 1개뿐이다 — 다른 파일을 고치지 마라.

## 1. SSOT — 먼저 읽을 것

이번 작업은 조사다. 계약 문서는 없고, **원천 세 곳을 그대로 읽는다.**

- 코드: `/Users/kknaks/git/PROCEDURE-HUB` (`release/v1.2.0`, 커밋 `5b9af03`) — read-only. pull/checkout 금지
  - 레포 진입 `AGENTS.md` · `README.md` · `docs/README.md`. **`AGENTS.md` 첫 줄의 `/Users/marin/AGENTS.md` 는 다른 개발자 머신 경로라 없다 — 무시**
- 기획 문서: `/Users/kknaks/git/harness_works/mediness-mediness` 의 `origin/main:products/procedure-hub/` — **canonical 은 사용자 더티 체크아웃이라 파일을 직접 열지 말고 `git show origin/main:<경로>` 로 읽어라.** 문서는 v1.1.0(2026-07-03)에서 멈췄다
- 운영 데이터: stg API (인증 없는 `GET /api/*` — 주소는 코드 레포 `docs/guides/deployment.md` · `docs/guides/api.md` 에서 찾는다)
- 참고: 지난 목업이 stg 에서 받은 스냅샷 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-21-charty-poc/web/src/data/hub/hub-snapshot.json` (2026-10-26, 일부 시술만)

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

Procedure Hub 위에 **추천 시스템**을 만들려 한다. 목표 질의는 「○○가 고민이에요」(예: 모공 · 기미 · 처짐 · 여드름 흉터)가 들어오면
데이터를 탐색해 **추천 시술**(과 그 근거)을 돌려주는 것이다.

사용자 판단은 「지금 데이터 구조가 추천에 맞지 않는다 — 매핑이 빠진 곳이 많고, 그래프 구조가 아니라 고민에서 시술로 타고 갈 수 없다」이다.
이번 조사는 **이 판단을 실물로 확인하거나 반박하는 것**이다. 고칠 방향을 정하지 않는다 — 다음 단계(설계 결정)의 원료를 만든다.

## 3. 계약

해당 없음 (조사 — 다른 워커 없음).

## 4. 먼저 읽을 핵심 파일

- `backend/app/model/` 전체 — 레거시 도메인(`problem_combos` · `problem_packages` · `combo_recipes` · `contraindications` …)과 `canonical_*`(catalog · knowledge · recommendation · safety · guidance · publication) 두 계층이 있다
- `backend/app/model/canonical_recommendation.py` · `knowledge_search.py` — 이미 추천·검색 비슷한 것이 있다. 무엇인지 확인
- `docs/architecture/data-model.md` · `domain-contracts.md` · `retrieval.md` · `overview.md`
- `docs/adr/0002-canonical-data-strangler-and-publication-gate.md` · `0003-generalized-safety-subjects.md`
- `backend/alembic/versions/` — 실제 스키마 정본(문서와 다르면 마이그레이션이 맞다)
- 기획: `products/procedure-hub/20-spec/spec-001-taxonomy.md` · `spec-004-problem-combos.md` · `spec-018-problem-packages.md` · `spec-019-procedure-profiles.md` · `spec-050-charty-consumer-contract.md`

위 목록은 출발점이다. **추천 경로에 닿는 모델·라우터·서비스는 `grep` 으로 전부 세고** 목록 밖에서 찾은 것도 리포트에 넣어라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/research-report.md` **1개만**
- 그 밖 전부 read-only

## 6. 구현 단계 — 리포트가 답할 질문

각 질문마다 **답 → 근거(파일:줄 · 테이블.컬럼 · API 응답 발췌)** 순서. 확인 못 한 것은 「확인 안 됨」.

**Q1. 데이터 지도.** 테이블(모델) 전부를 나열하고 각각 무엇을 담는지 한 줄. 레거시 계층과 `canonical_*` 계층의 관계 — 어느 쪽이 지금 API 로 서빙되나, 이관은 어디까지 왔나(ADR-0002).

**Q2. 엔티티 연결.** 고민(problem/concern) · 부위 · 증상/피부 상태 · 시술(분류 계층) · 제품/장비 · 금기 · 부작용 · 효과 · 가격 사이가 **무엇으로 이어져 있나.**
연결마다 종류를 구분하라 — ① FK ② 조인 테이블 ③ JSON/배열 안의 id ④ **JSON/텍스트 안의 이름 문자열**(조인 불가) ⑤ 연결 없음.
mermaid ER(또는 노드-엣지) 다이어그램 1장 포함.

**Q3. 매핑 누락 실측.** stg 데이터(또는 레포 안 시드/fixture)로 수치를 낸다.
- 고민 N개 중 시술로 이어지는 것 / 안 이어지는 것
- 시술 M개 중 어떤 고민에도 안 걸리는 것
- 이름 문자열 참조 중 실제 엔티티와 안 맞는 것(끊긴 참조)
- 부위 · 효과 · 금기 등 다른 연결도 같은 방식으로
수치마다 어떻게 셌는지(호출한 엔드포인트 · 쿼리 · 스크립트)를 적어라. 끊긴 예시는 3~5건 실물로.

**Q4. 지금 코드로 「○○가 고민이에요」 를 넣으면 어디까지 가나.** `canonical_recommendation` · `knowledge_search` · `retrieval.md` · problem_combos/packages 경로를 실제로 추적한다.
stg 에 **모공 · 기미 · 처짐** 세 질의를 가장 가까운 엔드포인트로 실제 호출해 응답을 발췌하라. 추천이 나오는지, 나오면 무엇을 근거로 고르는지, 끊기면 어디서 끊기는지.

**Q5. 그래프로 옮기면.** 현재 구조를 노드 타입 · 엣지 타입으로 옮긴 표. 엣지마다 지금 데이터에 있는가 / 근거(문헌 · 출처) · 강도(가중치)가 있는가 / 없는가.
「고민 → 시술」 경로가 몇 홉이고 어디가 비는지.

**Q6. 문서 ↔ 코드 차이 (추천 관련 부분만).** v1.1.0 기획 문서의 SPEC 들이 말하는 구조와 v1.2.0 코드가 다른 곳.

**Q7. 정할 것.** 조사 중 나온 결정거리를 목록으로만 모은다(예: 고민 어휘를 어디서 정본으로 둘지). **답을 정하지 마라.**

리포트 맨 위에 **요약 5줄** — 사용자 판단(「매핑 누락 · 그래프 아님 · 고민→시술 탐색 불가」)이 각각 맞는지 / 부분적으로 맞는지 / 틀린지를 근거 한 줄과 함께.

## 7. 범위 제약 — 하지 말 것

- 코드 · 문서 레포를 고치지 않는다. 브랜치 · 커밋 · pull · checkout 금지
- stg 에는 **GET 만**. POST/PUT/PATCH/DELETE · 업로드 · 게시 금지. 호출은 필요한 만큼만(수백 건 반복 금지 — 목록 엔드포인트를 써라)
- 개발 · 운영 DB 에 직접 붙지 않는다. 사용자 포트 · 프로세스를 건드리지 않는다
- **설계안 · 스키마 제안 · 추천 알고리즘 제안을 쓰지 않는다** — 다음 단계 몫이다. Q7 「정할 것」에 질문으로만
- 리포트는 public 레포에 남는다 — 키 · 토큰 · 비밀번호 값과 실명을 쓰지 않는다

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · 테이블/컬럼 · API 응답 실물). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
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
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
