# [backend] WORK-001 WP7 — SPEC 0.2.0: 단계 단위 배정 모델 · 조작 API · 5직군 · 개원 전 시드 · 메모 공개 시점 · KOS 주석

너는 **cc-prototype `backend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더).
작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` — **`cc/back/` 만.** (frontend 는 지금 시안 작업 중이라 `cc/front/` 를 아무도 안 건드리지만, 너도 건드리지 마라)

## 1. SSOT

- **SPEC-001 0.2.0**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md` — **§0 · §2 · §4 · §5 · §6 · §7 · §9 · §10 · §11** 이 계약. 여기 없는 건 발명하지 마라
- **업무 흐름(정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md`
- 직원 · 직군 원천: `cc/back/data/kos-staff.json`(이미 있음 · gitignore) · 대조 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/kos-staff-api-report.md`
- KOS 주석 근거: `research-kos-har-report.md` · `research-kos-har2-report.md` (같은 폴더)
- 앞 판: `wp1-be-report.md` · `wp2-be-report.md` · `api-source-audit-report.md`(추정 22개 — 0.2.0 에서 대부분 없어진다)

## 2. 할 것

1. **상태 모델 교체**(§5.1): 직원 큐 모델 → customer · step · log · version. 방 상태 계산(§5.1 문구). `flowStep` 전이
2. **조작 API**(§5.3 표 전부) · 막는 조건(400 + `{error:{code,message}}`) · 응답 `{version}` · SSE · log. 0.1.0 의 `/api/board/*` 조작 경로는 없앤다
3. **읽기 API**(§5.2) — `procedure-candidates`(§5.4) 포함. 배정형 / 순회형 home
4. **5직군**(§4 규칙 — 복수 태그 · 마취용 제외 · 그날 나온 직원만) · 로그인 목록(§7) · 응답에 이메일 없음
5. **환자 상세 메모 공개 시점 · 작성자 이름 제거 · `**` 는 그대로 두되 front 가 굵게 하도록 원문 유지 · 빈 양식 줄 제거 · 「이전 시술 기록 없음」 제거**(§3.4)
6. **시드 = 개원 전**(§6) · reset · save
7. **KOS 주석**(§9 표 그대로 — 조작 함수마다 주석 블록, **호출 코드 0**)
8. 통역(WS)은 건드리지 않는다
9. `.env.example` 에 `CC_KOS_STAFF_PATH` · README 갱신

## 3. 계약 — frontend(WP8)가 이대로 쓴다

§5 경로 · 필드를 그대로. JSON camelCase. 응답 모양을 정하면 **`cc/back/README.md` 에 API 예시(요청 · 응답 JSON 1개씩)** 를 적어라 — WP8 이 그걸 보고 `types.ts` 를 맞춘다.

## 4. allowed_paths

- `cc/back/` 전부. 그 밖 금지. 커밋 · push · PR 금지
- **KOS 호출 금지**(어떤 것도). 사용자 E2E 서버(8600) · `data/cc.db` · `data/seed.json` 은 시험에 쓰지 말고 별도 DB 로. 끝나면 `seed build --date 2026-10-09` 로 `data/seed.json` 을 0.2.0 형식으로 다시 만들어 둔다(코디가 서버 재시작)

## 5. 검증

```
cc/back 에서 uv run pytest · uv run ruff check . — 각 1회. 기능 폴더 밖 import 없음. 사용자 포트·프로세스 안 건드림. 실행 못 한 검증은 사유와 함께 pending
```
- 이번 WP 항목만: §11 의 1 · 2 · 3 · 4 · 5 · 6 · 8 을 API 시험으로(화면 빼고) · 응답 전체 실제 고객 이름 · 이메일 0 대조 · 주석 수 = 조작 함수 수 · KOS 호출 코드 0(grep)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp7-be-report.md`

## 6. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_eb0f5374-235a-4757-bb3a-1b2768c7e255 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] backend: <질문>" --enter`
