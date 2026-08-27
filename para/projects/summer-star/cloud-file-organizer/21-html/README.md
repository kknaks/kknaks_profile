# cloud-file-organizer HTML screens

정적 HTML 시안 위치. 실제 사용자가 보는 프론트 라우트 기준으로 화면당 1 파일로 구성한다. 모든 페이지는 상단 nav의 정적 링크(`문서` / `승인` / `관리` / `로그인/RBAC`)로 서로 연결된다.

- [login-rbac.html](login-rbac.html) — 로그인/RBAC 진입, admin/member 노출 차이 (SPEC-001)
- [page-documents.html](page-documents.html) — 문서 탐색 (SPEC-002, SPEC-006)
  - 조직/문서 트리 사이드바 + `조직 설정` CTA
  - ① 물리 귀속 목록 ② 관련 문서 ③ 검색 결과(출처 badge) ④ 선택 문서 상세(승인 metadata / Drive mirror) ⑤ 문서 연결(승인 relation graph) ⑥ 문서 이관 modal(admin)
- [page-approvals.html](page-approvals.html) — 승인 게이트, admin 전용 (SPEC-005)
  - 후보 큐 + 상태 필터(전체/승인 대기/stale/재분석 중/차단됨/본문 분석 없음)
  - 후보 metadata form(문서 정보/귀속/권한/요약), 민감 문서 권한 preset, 문서 연결 relation 후보(unresolved 처리), 상태별 배너 문구, stale 승인 차단, fingerprint/AI queue aside
  - 상태 표기: 원장 5개(pending/stale/approved/rejected/blocked) + 표시용 3개(재분석 중/새 후보 준비됨/재분석 실패)
- [page-admin-settings.html](page-admin-settings.html) — 관리 설정 (SPEC-002 U-4, SPEC-004)
  - ① Google Drive 연동 상태(연결됨/설정 필요/갱신 필요/오류, watch 갱신) ② Sync Activity(다시 처리) ③ 문서 수집 결과(승인 게이트로 이동) ④ 조직도 ⑤ 문서 트리 설정 ⑥ 문서종류 추가 ⑦ 사용자/RBAC 보정
- [assets/cloud-file-organizer.css](assets/cloud-file-organizer.css) — 공통 CSS/token

## 기준 문서

- `00-baseline/README.md`
- `10-decision/README.md`
- `20-spec/README.md`
- `40-architecture/README.md`
- `20-spec/spec-001-user-rbac.md` ~ `spec-007-ai-classification-pipeline.md`
- 각 spec의 "2. UX Contract" 문구/상태/CTA를 그대로 사용한다.
- `40-architecture/system/system-001-system-architecture.md`
- `40-architecture/database/database-001-ai-queue-state.md`

## 반영 범위

- 로그인/RBAC 진입과 admin/member 역할 차이.
- 화면 간 이동은 JS 탭이 아니라 페이지 단위 정적 링크로 표현한다.
- `page-documents`에 물리 귀속/관련 문서/검색을 시각적으로 구분된 섹션으로 분리하고, spec 빈 상태 문구("이 위치에 귀속된 문서가 없습니다.", "관련 문서가 없습니다.", "검색 결과가 없습니다.", "연결된 문서가 없습니다.")를 표기한다.
- `page-approvals`에 승인 게이트 배너 문구("Drive 파일이 변경되어 이 후보는 승인할 수 없습니다.", "본문 분석 없이 Drive 정보만으로 생성된 후보입니다.", "현재 문서 상태에서는 승인할 수 없습니다.", 빈 상태 "승인할 후보가 없습니다.")와 원장/표시용 상태 구분을 표기한다.
- `page-admin-settings`에 Drive connector 상태, sync activity, 수집 결과, 조직도/문서 트리 설정, 문서종류 catalog, RBAC 보정을 모은다.
- Google Drive가 파일 SoT이고 DB가 metadata/relation/approval/job state SoT라는 경계.
- AI 후보는 승인 전까지 확정 metadata처럼 보이지 않는 UX.
- member 화면에는 승인 게이트, AI queue, admin 메뉴가 보이지 않는 UX.
- 권한 없는 문서는 잠금/마스킹이 아니라 목록/검색/관계에서 제거되는 UX.

## 구현 메모

- shadcn/ui 기준 컴포넌트 매핑: `Button`, `Badge`, `Table`, `ScrollArea`, `Dialog`, `Input`, `Select`, `Textarea`, `Separator`.
- 페이지 섹션은 카드 남발 대신 shell/sidebar/main/aside, panel, table, form 중심으로 구성했다.
- 구현 시 route는 `/login`, `/app/documents`, `/app/approvals`, `/app/admin` 구성이 적합하다.
- member session에서는 `approvals`, `admin` route/nav 자체를 렌더하지 않는다.
- 이 산출물은 제품/UX 흐름 확인용 정적 HTML이며 실제 API 연동 코드는 포함하지 않는다.
