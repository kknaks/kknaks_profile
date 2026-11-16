# [writer] SPEC-002 · SPEC-003 — 식약처 데이터: 작업용 MCP · Hub 적재

너는 **procedure-hub `writer` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (코디 워크트리 공유 — 아래 2개 파일 외 수정 금지)

## 1. SSOT (`orchestration/work/phub-recommend/`)

- `DEC-003.md` ← 원장 셋 · 식약처 두 갈래(D-04) · 승인 게이트. `_RESUME.md` §2 10-27 행 전부(특히 「DEC-003 OQ 처리」 · 「외국어 이름 오타 → 정확히 일치하지 않으면 승인 게이트」)
- **실호출 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/NOTES.md`** ← 오퍼레이션 이름 · 대문자 파라미터 · 필드 · 취소 허가 섞임 · 브랜드가 PRDUCT 로 안 걸림. 필요하면 같은 폴더 `.env` 키로 **엔드포인트당 몇 번만** 다시 호출해 필드를 확인해도 된다(키 값을 문서 · 로그에 쓰지 않는다). 의약품 API(DrugPrdtPrmsnInfoService07)는 아직 미등록 — SPEC 에 「응답 미확인」으로 두고 실호출 후 채울 칸을 표시
- `SPEC-001.md` · 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/app/modules/graph/` ← Hub 브론즈 적재 · 검증 · 발행의 기존 관례(SPEC-003 은 이 위에 원천 하나를 더한다)
- 양식 `templates/projects/20-spec/spec.md`

## 2. SPEC-002 — 작업용 식약처 MCP (`reference/2026-10-27-mfds-mcp/`)

- 용도: 작업자(코디 · 워커 · 사용자)가 Claude Code 에서 붙여 원장 매칭 · 확인에 쓰는 **작업 도구**. 나중에 상담 에이전트가 DUR 용으로 재사용
- 기본값(코디 결정, 사용자 통보): **Python + 공식 MCP SDK · stdio** — Hub 와 같은 언어 · 같은 SDK. 다르게 가야 할 이유가 있으면 OQ 로
- tool: 의료기기 품목 검색(모델명 · 업체 · 품목명) · 의료기기 상세 · 의료기기 업체 조회 · 의약품 검색 · 상세(응답 미확인 표시) · DUR(병용 · 임부 · 연령 — API 신청 전이면 「나중」 표시). tool 마다 입력 · 출력 필드 · 실제 파라미터 매핑(대문자) · 페이지 처리 · 취소 허가 걸러내기 옵션
- 응답 캐시(gitignore) · 호출 횟수 · 에러(미등록 키 · 서비스 없음) 처리 · 키는 env
- public 레포 — 키 0 · 실명 0

## 3. SPEC-003 — Hub 식약처 원천 적재 · 매칭 (PROCEDURE-HUB 브랜치 `kknaksss/phub-recommend`)

- 원천 추가: 식약처 API 응답을 **브론즈로 저장**(SPEC-001 브론즈와 같은 규칙: 원본 · 수집 시각 · 해시 · 멱등). LLM 없음(DEC-001 D-12)
- 무엇을 받나: 분류표의 제품 · 장비 판정 항목(`taxonomy-classify.json`) 이 가리키는 업체 · 모델로 좁혀서 받는다(전체 21만 건을 받지 않는다) — 질의 목록을 만드는 규칙
- 매칭: 원장 이름 ↔ 허가(업체 + 모델명 + 사용목적). **정규화 완전 일치만 자동, 나머지는 후보로 승인 게이트**(외국어 오타 결정). 매칭 결과 · 후보를 어디에 두고 게이트 답을 어떻게 되받는지(아티팩트 db → 다시 Hub 로)
- 원장 반영: 제조사 · 제품/장비 · 규격 원장(DEC-003 D-01)을 어느 단계에서 만드나 — 스키마는 이 SPEC 이 정한다(SPEC-001 graph 모듈 확장 · 기존 레거시 · canonical 미접촉)
- 검증 게이트 항목 추가(매칭 안 된 제품 수 · 취소 허가 · 원어명 빈칸 …)

## 4. allowed_paths

- 생성: `orchestration/work/phub-recommend/SPEC-002-mfds-mcp.md` · `SPEC-003-mfds-ingest.md` 2개만

## 5. 제약

- DEC-003 · _RESUME 에 없는 정책은 OQ. API 호출은 필드 확인용 최소 횟수. 코드 · 다른 문서 수정 금지

## 6. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: SPEC-002 · SPEC-003" \
  --body "tool 목록 / 적재·매칭 흐름 / 다시 호출해 확인한 필드 / OQ"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] writer 완료 — SPEC-002 · SPEC-003. 상세는 인박스." --enter
```
