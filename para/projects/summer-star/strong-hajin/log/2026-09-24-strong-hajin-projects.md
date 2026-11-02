# 작업 요약 — strong-hajin-projects (strong-hajin)

기간: `2026-09-21` ~ `2026-09-24`
결과: 프로젝트 화면과 Tauri 로컬 래퍼를 구현·검수하고 코드 PR #3, 문서 PR #58·#60을 squash merge했다. 운영 배포와 설치파일 발행은 다음 작업으로 넘겼다.

## 1. 무엇을 했나

프로젝트 화면의 재귀 간트·참여/배정 계약을 구현하고 사용자 E2E에서 발견한 캘린더 레이아웃과 드래그 앤 드롭 문제를 수정했다. Tauri 셸에는 녹음 중 OS 절전 방지, 쿠키 기반 원격 웹 사용, 로컬 실행 경로와 최종 빌드 관문을 추가했다. 운영용 라우트 등록을 인증 판정에서 분리하고 Mac Studio GitOps 구조를 설계했다. 로컬 macOS Tauri에서 월간·주간 드래그 앤 드롭까지 사용자 확인을 마쳤다.

## 2. 적용한 기술·개념

- **Tauri 원격 웹 래퍼와 네이티브 절전 점유** — 웹 앱 계약을 유지하면서 녹음 중 macOS·Windows의 idle sleep을 막는 셸을 구성했다.
  - 왜 이걸 골랐나: 프론트·백엔드를 앱에 동봉하지 않고 Mac Studio의 같은 HTTPS origin을 쓰면 세션 쿠키와 WebSocket 계약을 유지할 수 있다.
  - 무엇이 어려웠나: 웹뷰 타이머 갱신은 화면 비가시 상태에서 신뢰할 수 없어 점유 수명을 Rust 네이티브가 소유하게 했다.
  - 근거: `tauri-p1-implementation-report.md` · `tauri-p4-web-wiring-report.md` · 코드 PR #3
- **HTML5 드래그 앤 드롭과 Tauri 파일 드롭 경계** — 제품 창의 네이티브 파일 드롭 핸들러를 꺼 웹 캘린더의 기존 DnD 이벤트가 WKWebView에 도달하게 했다.
  - 왜 이걸 골랐나: 포인터 폴백은 웹과 다른 조작 체계를 하나 더 만들고 기존 드래그 미리보기를 잃는다.
  - 무엇이 어려웠나: 카드 자체는 떠도 드롭 영역이 반응하지 않아 CSS 문제가 아니라 Tauri가 이벤트를 선점하는 문제임을 사용자 실측으로 좁혔다.
  - 근거: `tauri-week-drop-fix-report.md` · `frontend/src-tauri/src/lib.rs` · 코드 PR #3
- **같은 origin 운영 구조** — `/`는 nginx 프론트, `/api/`와 WebSocket은 FastAPI로 보내는 Mac Studio Kubernetes 구조를 잡았다.
  - 왜 이걸 골랐나: 상대경로 API, Secure 세션 쿠키와 쿠키 기반 WebSocket 인증을 바꾸지 않기 위해서다.
  - 무엇이 어려웠나: PRODUCTION에서 라우트 등록과 로그인 가능 여부가 한 게이트에 섞여 있었다. 라우트 등록은 분리했지만 세션 발급 수단은 제품 결정으로 남겼다.
  - 근거: `tauri-deploy-design.md` · `tauri-p6b-backend-report.md`
- **실행·발행 관문** — 로컬 Tauri 실행기와 origin·capability·증거·아티팩트 동일성 검증기를 만들었다.
  - 왜 이걸 골랐나: 미정 origin이나 검증하지 않은 설치파일이 Release로 올라가는 경로를 자동으로 막기 위해서다.
  - 무엇이 어려웠나: 측정할 수 없는 항목을 초록으로 만들지 않고 rehearsal과 실제 통과의 종료 코드를 분리했다.
  - 근거: `tauri-p7-build-report.md` · `tauri-p8-preflight-report.md`

## 3. 막혔던 것 / 사고

- Tauri가 흰 화면으로 열림 → 로컬 프론트 스택보다 셸을 먼저 실행한 순서 문제를 확인 → `make local-stack` 준비 후 `make tauri-local` 순서를 RUNBOOK-001로 고정했다.
- 캘린더 월간 일정이 날짜 칸마다 잘려 보임 → 멀티데이 막대가 아니라 셀별 조각으로 렌더되는 스타일을 확인 → 웹과 같은 연속 막대 폭으로 복원했다.
- 주간 드롭 시 카드 미리보기는 뜨지만 칸이 반응하지 않음 → Tauri 네이티브 파일 드롭 핸들러가 HTML5 이벤트를 선점 → 제품 창에서 핸들러를 비활성화하고 사용자 E2E로 확인했다.
- PRODUCTION API가 모두 사라짐 → `developer_auth_enabled`가 권한뿐 아니라 라우트 등록까지 감싼 사실 확인 → 등록과 권한 판정을 분리했다. 로그인 수단 부재는 아직 남았다.
- 전체 프론트 테스트가 매번 다른 파일에서 간헐 실패 → 변경을 되돌린 기준선에서도 재현 → 변경 회귀로 꾸미지 않고 스위트 시간 의존 불안정으로 기록했다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-22 | Tauri 래퍼의 목적은 회의 녹음 중 절전 방지와 후속 OS 알림이다 | 사용자 요구 |
| 2026-09-22 | 로그인은 기존 same-origin 세션 쿠키를 유지한다 | 키체인 토큰 전환 없이 현재 웹 계약을 유지 |
| 2026-09-22 | macOS와 Windows를 모두 지원한다 | 사용자 요구 |
| 2026-09-22 | 운영 프론트·백엔드는 Mac Studio에 함께 올린다 | 사용자 요구; Vercel 불필요 |
| 2026-09-22 | 설치파일은 Strong_hajin 코드 저장소 GitHub Releases, 릴리즈 문서는 프로필에서 관리한다 | 사용자 요구 |
| 2026-09-24 | 로컬 Tauri는 운영 설정을 고치지 않는 임시 loopback 실행 경로를 쓴다 | 로컬 검증과 운영 origin을 분리 |
| 2026-09-24 | 캘린더 DnD는 기존 HTML5 방식을 유지하고 Tauri 파일 드롭만 끈다 | 웹과 동일한 드래그 미리보기·드롭 경험 보존 |

## 5. 날짜별 로그

- `2026-09-21` 프로젝트 화면 조사·결정·스펙·작업 계획을 작성하고 구현 루프를 시작했다.
- `2026-09-22` 프로젝트 화면 구현과 검수를 닫고 Tauri 결정·스펙·WORK-006을 확정했다.
- `2026-09-23` Tauri 셸·웹 배선·운영 준비·빌드 관문을 구현하고 단계별 독립 검수를 반복했다.
- `2026-09-24` 로컬 Tauri 사용자 E2E에서 캘린더 레이아웃·드래그 문제를 수정하고 PR을 병합했다.

## 6. 산출물

- 문서 PR: https://github.com/kknaks/kknaks_profile/pull/58
- 환경 문서 PR: https://github.com/kknaks/kknaks_profile/pull/60
- 코드 PR: https://github.com/kknaks/Strong_hajin/pull/3
- 코드 브랜치 최종 커밋: `3b012a0` feat(desktop): Tauri wrapper와 녹음 절전 방지를 구현한다
- 주요 리포트: `tauri-implementation-status.md` · `tauri-deploy-design.md` · `tauri-p6b-backend-report.md` · `tauri-p7-build-report.md` · `tauri-p8-preflight-report.md`

## 7. 잔여

- Mac Studio 운영 호스트와 PRODUCTION 로그인 수단 확정
- arm64 프론트·백엔드 이미지 및 Strong Hajin 전용 Helm/Argo CD 구성 실제 배포
- 운영 origin에서 쿠키 유지·원격 IPC·녹음·절전 방지 실측
- macOS 아이콘·서명·공증과 Windows 빌드·서명·실기 검증
- 최종 설치파일 생성·설치 E2E·GitHub Release 발행
- 프론트 전체 테스트 스위트의 시간 의존 불안정 후속 정리
