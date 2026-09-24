# WORK-006 야간 실행 상태

사용자 승인: 각 Phase 구현→독립 검수→수정 직렬. 코드/자동검증 우선, 설치·최종 E2E는 내일. 이 표는 완료 증거가 없는 항목을 완료로 만들지 않는다.

| Phase | 코드·준비 | 자동 검증 | 실기/운영 증거 | 다음 |
|---|---|---|---|---|
| 1 탐침·fixture | 구현·R1/R2 검수 완료(WARN, 진행 가능) | tsc, FE 1040, cargo 21, 제품 build 통과 | M-1·OS 실행 미확인, CA 신뢰 설치 필요 | Phase 2 실측 |
| 2 fixture 계측 | IN_PROGRESS (게이트 미도달·조건부 보완 태세) | M-1 미측정, M-7 불일치 기록·검수 완료 | CA 신뢰·마이크·절전·Windows 실기 대기 | M-1 후 게이트 재평가; Phase 3 조건부 착수 |
| 3 제품 셸 | DONE (Phase2 조건부, 저지 0·WARN 4) | Rust 45, FE 회귀·제품 build 통과 | Windows·운영 origin 미확인 | M-1 완료 전 Release 금지 |
| 4 웹 배선 | DONE (FAIL 0, WARN 3 이월) | tsc, shell 13, browser+shell 24, 1053/1053 3연속 | 실기 미확인 | Phase 5 통합 검증 |
| 5 통합 검증 | DONE (자동검증 PASS, FAIL 0; 실기 대기) | tsc, 배선 215, 전체 스위트 기준선 불안정 기록, assets/build, cargo 45, clippy | AC ✅2·🟡11·⬜8, M-1·제품판 8칸·Windows·운영 origin 미측정 | Phase 6a 운영 설계 |
| 6a 운영 설계 | DONE (FAIL 0; 문구 보정 검수 완료) | 설계·보정·독립 검수 완료 | 운영 도메인·레지스트리·로그인 수단 등 사용자 결정 대기 | 6b backend B-1/B-2 |
| 6b 운영 코드·인프라 준비 | DONE (backend B-1/B-2 + Strong Hajin Helm/Argo 구조, 최종 인프라 검수 FAIL 0) | backend make test 1454 병렬 + 130 직렬, WS 4401·REST 401; Helm lint 4종·placeholder 주입 prod 10/dev 6/datastores 4 렌더 | D-1 운영 호스트·D-2 레지스트리·D-3 org push·D-4 로그인·D-6 dev 공개 범위 미결; 클러스터 적용·push 미수행 | 사용자 결정 후 Phase 8 origin 설정·최종 빌드 |
| 7 설치 빌드 준비 | DONE (fixture 빌드 구성·strict 검증기·N-1 문구 보정, FAIL 0) | shell-verify 기본/strict·태그 조합·cargo/clippy/tsc 검증, FE 스위트 불안정 이월 | 설치파일 생성·M-10·Windows 실기 미측정, .icns 없음 | Phase 8 최종판 검증 |
| 8 최종판 검증 준비 | PREPARED (preflight gate 구현·FAIL 0 검수, 운영 origin 미정으로 최종판 보류) | origin 형식 12종·설정 불일치·증거 없는 G5 차단, rehearsal exit3·직접 자동화 진입점 확인 | 운영 origin·D-4·서버 실재·M-1/M-5/M-10·Windows·.icns 미측정/미결 | 사용자 결정 후 최종 origin 설정→빌드→검증 |
| 9 Release 준비 | PREPARED (동일성 preflight 구현·최종2 검수 FAIL 0, WARN 1은 유지보수성 이월) | fixture 11건·독립 재검수 11건, 코드 0/2/3/4/5/6/7/8 일치·현재 저장소 nonzero | GitHub Release·태그·push·서명·공증·실제 설치파일 발행 미수행; 운영 origin·D-4·M-1/M-5/M-10·Windows 미결 | Phase 8 최종판 산출물 후 Release 발행 |

## 2026-09-24 로컬 Tauri 확인

- `make tauri-local` 로 macOS Tauri 창을 실제 실행하고 로컬 프론트엔드·백엔드에 연결했다.
- 월간 날짜, 주간 종일, 주간 시간 칸의 HTML5 드래그 앤 드롭을 사용자가 직접 확인했다.
- Tauri 기본 네이티브 파일 드롭 핸들러가 WKWebView의 HTML5 `dragover/drop`을 먼저 소비하던 원인을 확인해, 제품 창에서 해당 핸들러를 비활성화했다. 포인터 기반 대체 동작은 두지 않고 웹과 같은 드래그 미리보기·드롭 흐름을 유지한다.
- 날짜 선택기의 요일 정렬·하단 여백과 월간 일정 막대 폭도 로컬 앱에서 확인해 보정했다.
- 다음 세션 범위는 **화면 디자인 정리와 배포 준비**다. 운영 origin·PRODUCTION 로그인 수단·아이콘·서명/공증·Windows 실기·설치파일 생성과 GitHub Release는 아직 완료로 쓰지 않는다.

진행 기준 문서는 WORK-006, 오늘 범위 조정은 tauri-overnight-execution.md. P4 Rust verify·P5 인프라 설정 완료. 현재 task/dispatch는 _RESUME의 최신 Tauri 절 참조.
