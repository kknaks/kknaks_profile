# [frontend] WORK-008 Phase 2 — 탭 이동 깜박임 (B-01)

너는 Phase 1 을 끝낸 **strong-hajin `frontend` 워커**다. 같은 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` (Phase 1 은 커밋 `9255028` 로 들어갔다).
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ rules 등)

## 1. SSOT
- WP `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 2** + 원칙 P-2·P-3
- SPEC: 반영 없음(외부 계약 변화 없음 — 클라이언트 데이터 재사용)
- 원인 조사: `…/orchestration/work/strong-hajin-polish/fe-survey-report.md` **§7(B-01)** · `be-survey-report.md` §2-0

## 2. 계약 (WP Phase 2 그대로)
- 한 번 받은 화면 데이터를 기억해 두고, 다시 들어가면 **이전 데이터를 즉시 보여 준 뒤 뒤에서 갱신**
- 스켈레톤은 **데이터가 하나도 없는 첫 진입**에만
- 사이드 메뉴 화면 **전부**(홈·업무·캘린더·프로젝트·자료함·회의·조직·관계 탐색 — 실제 메뉴를 세어라)에 같은 규칙. 빠지는 화면은 이유를 적는다
- 쓰기(생성·변경·판단) 뒤에는 그 화면 데이터가 갱신된다 — 옛 데이터가 남지 않는다
- 권한(envelope) 판단은 갱신된 응답 기준
- 로그아웃·사용자 전환 때 기억해 둔 데이터를 버린다(다른 사람 데이터가 비치면 안 된다)

## 3. 방법 — 정하는 기준
- **새 라이브러리를 들이지 않는다**(react-query 등). `lib/api.ts` 의 `request()` 와 각 화면의 로딩 상태를 쓰는 지금 구조 위에서 최소로 한다. 들여야만 한다고 판단되면 먼저 [질문]
- `api.ts` 밖 fetch 금지 규칙은 그대로
- 화면마다 따로 캐시를 짜지 말고 **하나의 공용 장치**(예: 키별 마지막 응답 저장 + 화면 훅)로. 쓰는 곳을 전부 센다(P-3) — 「loading」 상태로 되돌리는 자리·`Skeleton` 을 띄우는 자리·진입 effect 의 fetch 전부
- 실시간 갱신·폴링 동작이 있는 화면(AX 대화 등)은 바꾸지 않는다

## 4. 순서
1. 기준선: 직렬 vitest 는 Phase 1 커밋 기준 1125 중 5 실패(날짜 의존, `flaky-baseline-evidence.md`). 새로 재지 않아도 된다
2. 공용 장치 → 화면별 적용 → 쓰기 뒤 갱신 → 로그아웃 시 비움
3. 테스트: 재진입 때 스켈레톤이 안 뜨고 이전 데이터가 바로 보임 · 뒤에서 갱신된 값으로 바뀜 · 쓰기 뒤 갱신 · 로그아웃 뒤 비움

## 5. allowed_paths
- `frontend/src/` 만. `src-tauri/`·`backend/` 금지

## 6. 하지 말 것
- 커밋·push 금지. 서버·브라우저 띄우지 마라 — 코디의 로컬 스택(8001·5176)이 떠 있다, 건드리지 마라
- 테스트는 **직렬**(`npx vitest run --no-file-parallelism`). 바뀐 파일 위주, 마지막에 전체 1회

## 7. 검증
```
make frontend-test 대신 직렬 vitest · npx tsc --noEmit · make frontend-build. envelope 권한 판단, api.ts 밖 fetch 금지, 기존 부품 재사용. 못 한 검증은 pending 으로.
```

## 8. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 2" \
  --body "변경 파일 / 공용 장치 설명 / 화면별 적용표(적용·제외+이유) / 전수조사 개수 / 테스트·tsc·build / 미결"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 완료 — WORK-008 Phase 2. 상세는 인박스." --enter
```
막히면: `orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --text "[질문] frontend: <질문>" --enter`
