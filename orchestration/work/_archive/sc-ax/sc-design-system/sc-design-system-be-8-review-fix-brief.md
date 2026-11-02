# [backend] PR #2 리뷰 수정 — F1 개인정보 노출 · F8 타 회사 변경 기록 · F2 has_account · F4 커서 · F5 회수 이력

너는 **sc-ax `backend` 워커**다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/backend/`.
워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `58c9ed4`, PR MediSolveAIDev/ax-workspace#2). **같은 워크트리에서 backend 워커·frontend 워커·사용자의 디자인 시스템 세션이 동시에 작업한다** — 자기 영역 밖 파일은 절대 만지지 않고, `git status` 에 남의 변경이 보여도 되돌리지 않는다. 커밋·push 는 코디가 한다.

리뷰: PR #2 의 zeroam 리뷰(2026-09-09, 코드 위치별 인라인 코멘트 8건). 원문은 `gh api repos/MediSolveAIDev/ax-workspace/pulls/2/comments` 로 읽어라 — 각 코멘트에 **재현 방법**이 적혀 있으니 그 재현을 먼저 테스트로 옮겨 RED 를 만든 뒤 고친다. 리뷰어가 「별도 판단」으로 분리한 2건(부서 관리자의 전사 개인정보 열람 정책 · null=비공개/없음 동일 표현)은 **손대지 않는다.**

## 3. 계약 — 고칠 것 5건 (리뷰 번호 그대로)
- **F1 [높음]** `platform/organization_access.py` 공통 조회에 넣은 `phone`·`birth_date` 가 `member_candidates()` 를 거쳐 `GET /api/work-request-cc-candidates` 로 나간다(마스킹 없음). 후보 조회는 **필요한 필드만** 반환하게 분리하고, 비관리자가 이 API 로 개인정보를 못 받는 회귀 테스트를 추가. 다른 후보 API(`work-request-assignee-candidates`·`task-assignment-candidates`)도 같은 함수를 쓰는지 전수 확인.
- **F8 [높음]** `application.py` `organization_activity`: `unit_id` 생략 시 `member_ids=None` 으로 조직 필터가 사라진다. 권한 검사에 쓴 조직 범위(루트 이하 구성원)로 **조회도 제한**. 구성원 외 대상(역할·조직 사건)의 귀속 범위도 정해서 보고. 두 회사 루트 픽스처로 회귀 테스트.
- **F2 [중간]** `entrypoints/http.py` `MemberResponse.has_account` 기본값 `False` 가 수행자·배정 후보 API 에 섞여 나간다. **후보 전용 응답 모델**로 분리하거나 실제 계정 유무를 채운다 — 어느 쪽인지 근거와 함께 보고.
- **F4 [중간]** activity 커서: 정렬은 `(occurred_at, id)` 인데 커서가 시각만 쓴다. `(occurred_at, id)` 복합 커서로, 경계 조건을 정렬과 일치. 동일 시각 3건 · limit 2 회귀 테스트.
- **F5 [중간]** grant 이력 종료일 `valid_until or revoked_at` → **둘 중 먼저 끝난 시점**. 만료 30일 뒤 + 즉시 회수 회귀 테스트.

## 5. allowed_paths
- `backend/src/ax_workspace/{platform/organization_access.py, modules/organization_access/*, entrypoints/http.py}` (+ 후보 API 가 `modules/work/*` 에 있으면 그 파일) · `backend/tests/contract/`
- **금지**: `frontend/` · `platform/persistence.py` 스키마 · `Makefile` · 커밋·push · 실데이터 픽스처

## 8. 검증
```
cd backend && uv run pytest -q <만진 테스트 + 새 회귀 테스트 5개> tests/architecture -m 'not integration'. 보고에 F1·F8·F2·F4·F5 각각 「재현 테스트(RED 확인) → 수정 → GREEN」 표 + F2 선택 근거 + F8 의 비구성원 사건 귀속 결정. git status 에 네 변경 = backend/ 만.
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e9a4432b-f153-45a5-97d4-63887e3329f1 --from term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e9a4432b-f153-45a5-97d4-63887e3329f1 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e9a4432b-f153-45a5-97d4-63887e3329f1 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
