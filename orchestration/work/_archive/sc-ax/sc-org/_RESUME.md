
# 재개 노트 — sc-org (mediness)

**지금**: 마감 (2026-09-07) — 반입 산출물 3종 완성, 슬러그 아카이브·main 머지
**다음**: 새 작업으로 SC 조직도 코드레포 생성 → `sc-ax.json` repos.app 등록 → `output/` 반입·적재

세팅: `scripts/new-work.sh mediness sc-org` · 설정 SSOT `config/projects/mediness.json`
코디handle: `term_4d21fab2-947e-495f-9df5-0418f447a15b`

⚠ 이 `work/sc-org/` 는 **sc-org 워크트리 공용 발주 디렉토리다** — 발주마다 새 slug 를 파지 않고
여기 브리프·리포트를 쌓는다 (2026-09-04 사용자 지시).

## 워크트리

⚠ 아래 워크트리 이름의 `task` 는 slug 교정(task→sc-org) 이전에 생성된 것 — 조사 끝났고 clean 이라
그대로 두고, 정리 시점에 삭제한다. 후속 발주로 새 워크트리를 팔 땐 slug `sc-org` 를 쓴다.

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/task-spec` (branch `kknaksss/task-spec`, base `origin/mediness` → PR `mediness`)
- `app`: `/Users/kknaks/orca/workspaces/mediness-app/task` (branch `kknaksss/task`, base `origin/dev` → PR `dev`)

둘 다 read-only 조사용 — PR 없음.

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [ ] 리포트 §5.3 미결 질문을 사용자와 닫고 반입 방식 결정 (코어 9테이블 이식 vs 축소 신규)
- [!] 설계·구현 발주는 사용자 승인 뒤
- [!] 워커 터미널(`term_153ae551…`)·워크트리(task/task-spec)는 후속 발주 가능성 있어 유지 중

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-04 | `para/projects/company/sc-ax/` 스캐폴딩 + `sc-ax.json` summary_dest 연결 | 사용자 지시 (para 에 sc 자리 없음) |
| 2026-09-04 | 발주 디렉토리는 `work/sc-org/` 공용 1개 — 발주마다 새 slug 금지 | 사용자 지시 |
| 2026-09-04 | mediness 조직도 조사 워커 1명 (문서+코드, read-only, 이번 1회) | 사용자 지시 |
| 2026-09-04 | SC 조직도 = mediness 테이블 구조 그대로 반입 (코어 9 + job_function 2를 직급 어휘로) | CSV 대조 — 조직도 본체 전부 수용됨 |
| 2026-09-04 | 이메일 원본 = **위하고메일** → `work_email`. 지메일은 뺀다 | 사용자 지시 |
| 2026-09-04 | `organization_member` 에 컬럼 추가: 전화·생년월일 | 사용자 지시 (CSV 에 자리 없던 컬럼) |
| 2026-09-04 | 담당 프로젝트 축은 **보류** — 이번 반입 범위 밖 | 사용자 지시 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| reviewer_code | `term_153ae551-7c1d-4739-bda9-abc138f93c60` | `task_cdb0a684f6d4` | `ctx_6951ae1606bd` | `sc-org-review-code-brief.md` | 완료 (worktree clean·리포트 검증 통과) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- 리포트: `org-chart-survey-report.md` (595줄 — 테이블 16개 전수·코드 지도·결합도·재사용 판단 재료·미결 10문)
- `output/erd.md` — SC 반입 ERD·CSV 매핑·mediness 와의 차이 6건
- `output/models.py` — SQLAlchemy 11테이블 (mediness 코어 9 + 직급용 job_function 2, py_compile·import 검증)
- `output/seed_sc_org.py` — CSV 적재 (dry-run 실측: unit 28·member 165·membership 169·직책배정 22)

## 5. 이력 (최신이 위)

- `2026-09-04` 조사 완료 — 리포트 수신, 코디 스팟체크(16 테이블·MEDISOLVE 상수·서비스 5개) 일치, 워크트리 수정 0 확인
- `2026-09-04` sc-ax para 스캐폴딩 → mediness 조직도 조사 워커 발주 (worktree task/task-spec 생성)
