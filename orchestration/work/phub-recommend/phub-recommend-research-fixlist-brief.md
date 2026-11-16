# [researcher] 원천 수정 목록 — Procedure Hub stg 데이터에서 고칠 곳 · 이유 · 확인 방법

너는 **procedure-hub `researcher` 워커**다(read-only). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (코디 워크트리 공유 — 아래 2개 파일 외 수정 금지)

## 1. 배경

사용자 결정(2026-10-27): 「처짐/쳐짐」 같은 문제는 Hub 동의어 사전이 아니라 **원천(stg Procedure Hub 데이터) 표기 수정**으로 푼다.
원천은 회사 데이터라 우리가 직접 고치지 않고, 데이터 관리자에게 넘길 **수정 목록**을 만든다. 사용자가 항목마다 답(수정 / 보류 / 확인 요청 + 메모)을 다는 화면(아티팩트)의 원료가 된다 — 그래서 **JSON 이 정본**이다.

## 2. 원천 — 먼저 읽을 것 (`orchestration/work/phub-recommend/`)

- `research-report.md` §Q3 · §Q2 · §Q5 · §Q6 · `SPEC-001.md` §3 · §6.3 · `review-spec-001-report.md` §7 · `review-code-report.md` §7
- **항목 단위의 정본 = 로컬 그래프 검증 이슈.** 로컬 DB `phub-graph-postgres`(localhost:55434, 접속 정보는 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/envs/.env.graph`)의 graph 이슈 · 노드 · 엣지 · 브론즈 테이블을 **SELECT 만** 해서 뽑는다(테이블 이름은 `backend/app/model/graph.py`). 발행본 v1
- 원본 JSON: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` (stg 응답 21개 저장본 — stg 는 다시 부르지 않는다)

## 3. 분류 (코디가 사용자에게 보인 A~D)

- **A 표기 · 이름** — A1 고민 이름 오기(「쳐짐」 3곳) · A2 synergy 끝점 이름 67/230 · A3 optimization 조합 문자열 48/74 · A4 CC 권장 시술 name 66/254 · A5 CC 조합 이름 36/277 · A6 treatment-sequence 이름 23/35 · A7 패키지 제품 문장 36/88
- **B 값 오류 · 충돌(의료 판단 필요)** — B1 원천 충돌 7쌍 · B2 「서브시전」 시술군 불일치 6행 · B3 이소트레티노인이 시술 항목 · B4 CC 권장 목록 98/115 동일
- **C 연결 빈칸** — C1 고민 항목 시술 연결 없음 26/117 · C2 패키지 없는 고민 6 · C3 금기 규칙 없는 시술군 6 · C4 합병증 없는 시술군 7
- **D 구조(표기 수정만으로 안 됨)** — D1 고민 아닌 항목이 고민 트리에 · D2 고민 항목 이름이 시술명 · D3 같은 제품 두 원장(57쌍) · D4 부위 마스터 없음
- 수치가 위와 다르면 실물 값을 쓰고 `notes` 에 차이를 적는다. 분류에 안 맞는 새 문제가 보이면 `E 기타` 로

## 4. 산출물

1. `orchestration/work/phub-recommend/source-fix-list.json` — **정본.** 구조:
```json
{
  "generated_at": "...", "graph_version": "v1", "source_snapshot": "phub-stg-2026-10-26",
  "groups": [ { "id": "A2", "category": "A", "title": "...", "why": "그래프·추천에서 무엇이 끊기나 2~3문장", "verify": "고친 뒤 줄어야 할 검증 코드·숫자", "evidence": ["research-report.md §Q3 3-3", "..."], "count": 67 } ],
  "items": [ {
    "id": "A2-001", "group": "A2",
    "endpoint": "synergy", "location": "원천 JSON 경로 또는 id (예: links[12].to)", "field": "to",
    "current": "M9-리프팅기기", "occurrences": 4,
    "proposed": "M9-<원장의 실제 이름 후보>" , "proposed_basis": "원장에 정규화 일치하는 후보가 있으면 그 이름 · 근거. 확신 없으면 null",
    "candidates": ["원장 이름 후보 0~3개"],
    "needs_medical_review": false,
    "why": "이 항목이 안 고쳐지면 끊기는 엣지 한 줄",
    "validation_code": "unresolved_name_ref"
  } ]
}
```
   - **같은 `current` 문자열이 여러 번 나오면 한 항목으로 묶고 `occurrences`** 에 횟수, `location` 에 대표 위치 + 나머지 개수
   - `proposed` 는 **원장에 실제로 있는 이름일 때만**(정규화 일치 · 부분 일치 후보는 `candidates` 로). 의료 판단이 필요한 B 는 `proposed: null` · `needs_medical_review: true`
   - C 는 항목마다 「무엇이 비었나」를 `current` 에, `proposed: null`
   - D 는 그룹만 두고 항목은 대표 예시 3~5개
2. `orchestration/work/phub-recommend/source-fix-list.md` — 사람이 읽는 요약: 그룹별 why · verify · 건수 · 대표 예시 3개. JSON 과 수치 일치

## 5. 제약

- DB 는 SELECT 만 · 로컬 55434 외 접속 금지 · stg 호출 금지 · 코드 · 다른 문서 수정 금지 · API 서버를 띄우지 않는다
- 추측 금지 — 후보는 원장 실물에서만. 판정 못 하면 `null` + `notes`
- public 레포 — 키 · 토큰 · 비밀번호 값 · 실명 금지(DB 비밀번호를 문서에 적지 않는다)

## 6. 검증

JSON 이 `python3 -m json.tool` 통과 · 그룹 `count` == 그 그룹 항목 `occurrences` 합(또는 차이를 notes 에) · A~C 수치가 검증 리포트와 일치

## 7. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 원천 수정 목록" \
  --body "그룹별 건수 / 항목 수 / proposed 채운 수 · null 수 / 수치 차이 / 미결"

orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] researcher 완료 — 원천 수정 목록. 상세는 인박스." --enter
```
