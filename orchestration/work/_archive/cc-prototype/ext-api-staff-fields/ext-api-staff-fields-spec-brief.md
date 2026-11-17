# [planner] SPEC-008 0.4.7 · WORK-015 — ext 직원 목록에 email · realName · kosAccountId 추가

너는 **cc-prototype `planner` 워커**다. 너는 앞 판 맥락이 없다 — 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3` (코디 워크트리 — 코디와 같은 트리. 다른 워커 없음)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- `para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md` — **D-48**(오늘 추가 · 이번 작업의 결정 전부) · D-15(고침 줄) · D-21 · D-29. **D-48 에 없는 건 발명하지 마라.**
- `para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` — 지금 0.4.6. 고칠 곳: §6.17 · §9 T67 · 부록 F · 변경 이력 표 · 머리(version · updated_at) · §0 한눈에(필요하면)
- `para/projects/summer-star/cc-prototype/30-work/work-014-ext-api-charty1.md` — WORK 양식 선례(머리 · Meta · 계약 고정점 · WP 표 · 주의)
- `orchestration/work/_archive/cc-prototype/ext-api-charty1/research-clinic-staff.md` §2.2 — 내부 `get-accounts` 원소 모양 `{id, userId, email, name, realName, roleId, roleName, role{…}, activate, …}`

**기대는 개념**: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

배포된 `GET /api/ext/clinics/{clinicId}/staff`(코드 main `969f44f`)는 이메일 · 실명 · KOS id 를 일부러 빼고 있다(DEC-012 D-15 · SPEC §6.17 「넣지 않는 칸」 · T67 「키 0」). 연동처가 셋 다 필요하다고 해서 사용자가 D-15 를 뒤집었다(D-48). 필드 추가만 한다.

## 3. 계약 (D-48 그대로)

`staff[]` 원소에 세 칸을 더한다. 기존 다섯 칸 · 행 고르기 · 차례 · 오류 · KOS 호출 수(1)는 그대로.

| 칸 | 타입 | 원천 | null |
|---|---|---|---|
| `email` | string \| null | 내부 원소 `email` | 빈 문자열 · 칸 없음 → null |
| `realName` | string \| null | 내부 원소 `realName` (기존 `name` 과 다른 칸 · `name` 그대로) | 빈 문자열 · 칸 없음 → null |
| `kosAccountId` | string | 내부 원소 `id` (KOS 계정 id · 다른 ext 응답의 `staffId` 와 다른 체계) | 없음 — 지금 코드가 이 id 로 사본을 잇고 있으니 이미 필수 |

- 「넣지 않는 칸」 목록에서 셋을 빼고 나머지(`userId` · `licenseNumber` · `mfaMethods` · `roleId`)는 그대로 둔다.
- CC 직원 사본에 이메일을 저장하지 않는다(그대로). 세 값을 `ext_call` · 로그에 남기지 않는다.
- Swagger 설명 줄 「이메일 · 실명 · KOS id 는 내지 않는다」를 고친다(§8 에 해당 규약이 있으면 거기도).
- `kosAccountId` 타입: 연구 리포트 §2.2 와 코드(`procedure/back/app/kos/` · `service/ext.py` staff)를 보고 KOS id 가 문자열(uuid)인지 확인해서 적어라. 코드 레포 읽기 경로: `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-staff-fields` (read-only).

## 4. 먼저 읽을 핵심 파일

- SPEC-008 §6.17(860줄 근처) · T67(1059줄 근처) · 부록 F(1191줄 근처) · 변경 이력(80~100줄)
- 코드(read-only) `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-staff-fields/procedure/back/app/schemas/ext.py:491` `ExtStaff` · `app/service/ext.py` 의 `staff()` · `app/api/ext.py` `STAFF_DOC`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` · `20-spec/README.md`(인덱스 버전 줄)
- `para/projects/summer-star/cc-prototype/30-work/work-015-ext-api-staff-fields.md`(새) · `30-work/README.md`(인덱스)
- DEC 는 코디 소유 — 고칠 게 보이면 고치지 말고 보고에 적어라.

## 6. 구현 단계

1. SPEC-008 0.4.7: §6.17 응답 표에 세 줄 · 「넣지 않는 칸」 고침 · Swagger 설명 줄 고침 · T67 을 「세 키 있음 · 빈 문자열 → null · `kosAccountId` = 내부 `id` · 가짜 값만」으로 고침(기존 「키 0」 은 취소선) · 부록 F 에 D-48 행 · 변경 이력 0.4.7 행 · 머리 version · updated_at 2026-11-17.
2. WORK-015 새로: WP 는 작게 — **WP-BE1**(스키마 · 서비스 · Swagger 문구 · T67 시험 · 가짜 KOS 원소에 세 칸) → **WP-REVIEW**(reviewer) → **WP-E2E-LOCAL**(코디: 데모 KOS 실호출 1번 — 세 칸이 채워지는지 · 값은 기록하지 않음) → **WP-DEPLOY**(코디: main 머지 → back 이미지 → infra `back.imageTag` → ArgoCD sync → 운영 실호출 1번). 검증 명령은 `uv run pytest -q tests/test_ext_clinic.py tests/test_openapi_docs.py` · `uv run ruff check .`. Phase Status 칸은 「대기」.
3. 인덱스 두 곳 갱신.

## 7. 범위 제약 — 하지 말 것

- 다른 ext 경로 · 직원 API · 사본 테이블 · 동기화는 손대지 않는다(계약에 넣지 않는다).
- 실명 · 이메일 · KOS id **실제 값**을 문서에 쓰지 않는다(public). 예시는 지어낸 값.
- 커밋 · push 금지.

## 8. 검증

```
SPEC 의 모든 절이 DEC · workflow · 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 실명 0(grep)
```

- 부록 F 「빠짐 0」 제목 범위를 D-48 까지로.
- `python3 orchestration/scripts/sync-work-links.py --check` 1회.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94d17da5-ee50-4f74-ade5-221f35a1ea02 --from term_db02145b-6732-492e-bb39-120ba5de14a5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94d17da5-ee50-4f74-ade5-221f35a1ea02 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94d17da5-ee50-4f74-ade5-221f35a1ea02 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
