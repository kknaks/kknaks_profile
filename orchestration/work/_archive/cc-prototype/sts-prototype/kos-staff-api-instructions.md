# [backend] 읽기 전용 — KOS 직원 · 직군 조회 API 확인 (+ 있으면 읽기 호출 1회)

사용자 결정(2026-10-13): 직원 직군(의사 · 상담사 · 코디 등)을 추정하지 말고 KOS 값으로. KOS 는 **운영 DB — 쓰기 · 수정 · 삭제 절대 금지.**

1. 문서 확인: 가이드 `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` · OpenAPI 스냅샷(가이드가 가리키는 `para/archive/inbox_archive/2026-09-18-kos-openapi.yaml`, 같은 레포) · 스크립트 `/Users/kknaks/git/ax-clinic-project/scripts/kos_*.py`(특히 `kos_query_catalog.py`)
   - 직원(staff · employee · user · member · doctor · counselor …) 목록과 직군 · 역할(role · roleTags) 을 주는 **조회 전용** 작업이 있나 — 작업 이름 · 경로(`/queries/` 인지) · 요청 · 응답 필드
   - 가이드상 모든 작업이 `POST` 다. **이름 · 경로 · 스펙으로 조회 전용임이 분명한 것만** 후보로
2. 키: 스크립트가 KOS API 키를 어디서 읽나(env 이름 · 파일 위치)만 확인 — **값 출력 금지**
3. 조회 전용 작업이 분명하고 키가 있으면 **그 작업 1회만** 호출해 결과를 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/kos-staff.json` 에 저장(gitignore 폴더). 페이지가 있으면 필요한 만큼만. 분명하지 않으면 호출하지 말고 보고
4. 받은 결과와 10-09 일정에 나오는 직원(id)을 대조 — 직군이 다 채워지나

- 코드(`cc/back/app`) 수정 금지 — 이번엔 확인 · 저장만. 사용자 E2E 서버(8600) · `data/cc.db` · `seed.json` 금지
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/kos-staff-api-report.md` — 후보 작업 · 조회 전용 근거 · 호출 여부 · 대조 결과(직원 이름은 써도 됨)
- 완료 보고는 WP2 브리프 §5 두 명령(subject 「backend 완료: KOS 직원 API …」, taskId/dispatchId 는 WP2 것)
