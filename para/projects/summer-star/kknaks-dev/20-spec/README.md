# Spec Index

규칙: `para/projects/project.md`

## Spec 목록

| ID | Title | Status | Decision | Coverage | Work |
|---|---|---|---|---|---|
| KDEV-SPEC-001 | 지식그래프 디렉토리 구조 (4층 + concept) | draft (**v0.0.14**) | DEC-001/002/008/010/015/**018** | WORK-013 | WORK-013 (todo) · **WORK-019 (미발주)** |
| KDEV-SPEC-002 | 그래프 스키마 (노드·layer·식별자·엣지·산출물) | draft | DEC-003/004/010 | WORK-013 | WORK-013 (todo) |
| KDEV-SPEC-003 | 지식 워크플로 (4층 생명주기 · 승인 기반 정제) | draft | DEC-005(개정)/010/011/015 | WORK-013 | WORK-013 (todo) |
| KDEV-SPEC-004 | 그래프 검증 게이트 L1~L6 (층별 판정 · 발행 전 검증) | draft | DEC-006/010/012 | WORK-013·015 | WORK-013·015 (todo) |
| KDEV-SPEC-005 | 지식 열람 표면 — 트리 문서 렌더러와 공개 경계 | draft (**v0.0.4**) | DEC-007(대체)/010/**018** | — | (미발주) |
| KDEV-SPEC-006 | 관리자 인증 — 로그인/세션/admin 진입 | implemented | DEC-009 | WORK-011 | WORK-011 (done) |
| KDEV-SPEC-007 | 승인 큐 — 지식 입력 접수와 항목 상태기계 | draft | DEC-011/012/013 | WORK-012·014 | WORK-012·014 (todo) |
| KDEV-SPEC-008 | 게이트 체인 — 파이프라인 정의와 스테이지 계약 | draft (**v0.0.14**) | DEC-010/011/016/**021**/**023** | WORK-014·015·020·**021** | WORK-014·015 (todo) · WORK-021 (todo) |
| KDEV-SPEC-009 | 게이트 피드백과 재생성 — 버전·resume·supersede | draft (**v0.0.3**) | DEC-011/012/**024** | WORK-014·**022** | WORK-014 (todo) · WORK-022 (todo) |
| KDEV-SPEC-010 | Apply Executor — 발행 계획 검증과 원자적 발행 | draft | DEC-010/012/013/016 | WORK-015 | WORK-015 (todo) |
| KDEV-SPEC-011 | 커밋 조사 — 레포 레지스트리와 로컬 git 수집 | draft | DEC-014 | — | (미발주) |
| KDEV-SPEC-012 | 잔디 산출물 — daily·career·concept 계약 | draft | DEC-015 | — | (미발주) |
| KDEV-SPEC-013 | 잔디 승인 게이트 — daily_commit 파이프라인과 발행 | draft (v0.0.2) | DEC-016 | WORK-017 | WORK-017 (in_progress) |
| KDEV-SPEC-014 | 제품 레지스트리 — 등록·스캐폴딩·미등록 발견 | draft | DEC-017 | — | (미발주) |
| KDEV-SPEC-015 | 공개 글 발행과 노출 | implemented | DEC-020/021 | — | (미발주 — 구현이 문서보다 앞섰다) |
| KDEV-SPEC-016 | 웹 본문 수집 — 정적 → 동적 → 최종 실패 | implemented | — (BL-007 OQ-6) | — | (work 없음 — 코드 선행) |
| KDEV-SPEC-017 | 채용담당자 채팅 — 홈 히어로 · /chat · 익명 세션 · tool 경계 실행 | draft (**v0.0.14**) | DEC-025/026/027 | WORK-023·024 | WORK-023·024 (in_progress — 2026-08-28 발주) |

## 읽는 순서

| 묶음 | 문서 | 무엇을 다루나 |
|---|---|---|
| 지식 구조 | SPEC-001 → 002 → 004 → 005 | 어디에 두나 · 어떻게 잇나 · 무엇을 막나 · 어떻게 읽나 |
| 워크플로 | SPEC-003 | 노트가 어떻게 흐르나 (구현체 = 게이트 체인) |
| 승인 파이프라인 | SPEC-007 → 008 → 009 → 010 | 접수 → 체인 → 피드백 → 발행 |
| 잔디 파이프라인 | SPEC-011 → 012 → 013 | 무엇을 조사하나 · 무엇이 되나 · 어떻게 승인·발행되나 |
| 수집 | SPEC-016 | 블로그 URL 이 본문이 되는 경로 (SPEC-008 `blog` 파이프라인의 `collect`) |
| 공개 글 | SPEC-015 | 자료 하나가 글 한 편이 되어 `/notes` 에 서기까지 (SPEC-008 `post` 게이트의 산출) |
| 인증 | SPEC-006 | admin 진입 |
| 제품 관리 | SPEC-014 | 제품·레포 등록과 연결 (SPEC-011 레지스트리의 관리 표면) |
