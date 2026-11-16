
# [reviewer_doc] SPEC-001 · WORK-001 검수 — 구현 발주 전 마지막 문서 게이트

너는 **procedure-hub `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터 워크트리에 함께 탄다. 만들 파일은 리뷰 리포트 1개뿐 — 검수 대상 문서를 고치지 마라.

## 1. SSOT — 먼저 읽을 것

- 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/DEC-001.md` (D-01~D-13, 특히 D-05 · D-06 · D-12 · D-13a~g) · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2
- 대상: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-001.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/WORK-001.md`
- 사실 확인용: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/research-report.md` · 코드 `/Users/kknaks/git/PROCEDURE-HUB` (`release/v1.2.0`, read-only)

## 2. 배경

이 두 문서를 백엔드 워커가 **그대로** 구현하고, 사용자가 다음 날 로컬 E2E 를 한다. 문서 결함은 곧 구현 결함이다. 사용자 확인 없이 진행하는 야간 작업이므로 이 검수가 유일한 문서 게이트다.

## 3. 계약

해당 없음.

## 4. 볼 것 (판정 축)

1. **DEC 이탈** — DEC 에 없는 정책을 SPEC 이 정했나. 특히 Hub 에 모델 호출이 끼었나(D-12), 레거시 · canonical 테이블을 읽거나 고치나(D-13c), 큐레이션을 합치나(D-13e), 정규화 완전 일치 밖의 매칭이 있나(D-13d)
2. **구현 가능성** — 백엔드 워커가 문서만 보고 막힘 없이 만들 수 있나. 노드 · 엣지 · 응답 shape 이 필드 단위로 닫혀 있나. 원천 JSON 필드 경로가 실물(stg 응답 구조 · 코드 모델)과 맞나 — 의심 가는 것은 코드나 stg GET(엔드포인트당 1회 이내)으로 확인
3. **기존 코드와의 충돌** — 별도 진입점 `app/graph_main.py` 판단(공개 API 계약 테스트 `tests/test_public_api_contract.py`)이 맞나. 기존 테스트 · alembic 단일 baseline 과 새 마이그레이션이 공존 가능한가. `app/model/__init__.py` 수정이 기존 앱 메타데이터에 미치는 영향
4. **MCP 결정** — 근거 URL 이 결정을 실제로 뒷받침하나. 마운트 경로 · stateless 설정이 구현 가능한가
5. **E2E 시나리오** — 기대값이 재현 가능하고 정직한가(되는 척 금지 — 「처짐」). 사용자가 Swagger · MCP 클라이언트로 따라 할 수 있게 명령 · 경로가 다 있나
6. **WORK Phase** — 순서 · 완료 기준 · 테스트가 SPEC 절과 1:1 로 이어지나. 테스트가 stg 를 부르지 않나. 로컬 포트(55434 · 18005)가 사용자 포트(3700 · 3800 · 8700 · 8800 · 54329)를 피하나
7. **사용자가 실물에서 만날 자리** — 막히진 않지만 E2E 에서 이상해 보일 곳을 따로 모은다

## 5. allowed_paths

- 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-spec-001-report.md` **1개만**

## 6. 구현 단계

1. 위 축마다 지적을 `파일:줄 + 근거(DEC D-번호 · 코드 파일:줄 · stg 실물)` 로
2. 지적마다 FAIL(구현 전 반드시 고침) · WARN(고치면 좋음) 구분
3. 맨 위에 종합 판정 PASS / WARN / FAIL 과 FAIL 목록

## 7. 범위 제약

- 문서 · 코드를 고치지 않는다. 대안 설계를 길게 쓰지 않는다 — 무엇이 왜 틀렸는지만
- 취향 지적 금지. 구현 · E2E · DEC 정합에 영향이 있는 것만

## 8. 검증

```
DEC · SPEC · WORK 를 _RESUME 결정 · 조사 리포트 · 코드에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
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
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
