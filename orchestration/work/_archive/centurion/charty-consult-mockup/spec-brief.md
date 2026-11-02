# planner 브리프 — 피부 상담 목업 화면 2개 스펙

너는 이 작업의 맥락이 없다. 아래 「읽을 것」을 먼저 읽어라. **코드를 쓰지 않는다. 스펙만 쓴다.**

## 1. 읽을 것 (절대경로, read-only)
- `/Users/kknaks/orca/workspaces/kknaks_profile/차티-화면-구상/orchestration/work/charty-consult-mockup/_RESUME.md` — 정해진 것
- 같은 폴더 `research-report.md`(메디킷·차티 stg·M3D API) · `assets-report.md`(3D 에셋·필터 연결표)
- 차티 stg 상담 화면: `git -C /Users/kknaks/git/harness_works/CENTURION-CHARTY show origin/stg:<path>` 로만(체크아웃 금지). 시작점 `frontend/src/pages/consultation/consultation-desktop.tsx`, `left-bottom-panel.tsx`, `features/chart/components/chart-toolbar.tsx`, `layouts/header.tsx`, PricingPanel·ChartyRecommendation 관련 파일. **가격 조정(할인·금액 수정) 기능이 실재하는지 확인해 스펙에 반영**
- 메디킷 1.4.0: npm 공개(`npm view @medisolve-ai/medikit@1.4.0`), 설치본 `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2/procedure/front/node_modules/@medisolve-ai/medikit/dist` (`index.d.ts`·`styles/base.css`)
- 원본 데이터: `/Users/kknaks/orca/workspaces/kknaks_profile/차티-화면-구상/reference/2026-10-21-charty-poc/m3d-ai-h5.migamedi.co.kr.har` (measure·analyze·render API 3개) · 에셋 `…/m3d-assets/`

## 2. 정해진 것 (다시 논의하지 마라)
- Next.js(App Router, TS) · `reference/2026-10-21-charty-poc/web/` · `npm run dev` 로만 공유 · 배포·백엔드 없음
- 메디킷 **1.4.0** + 차티 테마(차티 stg 처럼 `:root` 에 primary `#6f21ff` 덮어쓰기)
- 목데이터 — HAR 수치 사용, 고객명 **이건학**(사용자 본인). 실 API 는 추후 3D 스캔 업체 → **데이터 계층을 어댑터로 분리**(M3D 응답 형태 → 화면 모델)
- 화면 ① **큰 스크린**(상담사+고객이 함께 봄): 좌 **3D 얼굴 + 필터** / 우 **분석 결과 그래프(설명이 쉽게)** + 상담사가 추가한 **시술** + 상담사가 조정한 **최종 가격**
- 화면 ② **상담사 태블릿**: 기존 차티 상담 화면 문법(체크리스트·차트·상담 텍스트 탭, 가격표, 시술 추천 등). 여기서 시술 추가·가격 조정·필터 선택(선택) 등이 ①에 **실시간 반영**
- 동기화: `BroadcastChannel`(같은 PC 탭 2개). 서버 없음
- 3D: three.js(`@react-three/fiber` 여부는 네가 제안) · `Rgb.obj` 그대로 · 텍스처 `thumb/*_M.jpg`(3242px) · 회전·확대 + 필터만. 좌우비교·등고선·노화시뮬 제외
- 필터: 잔주름 · 굵은주름 · 모공 = `hd_ai/` 검출 이미지 오버레이 / 붉은기(염증) · 색소 · 포르피린 = 광원 텍스처 교체 / 기본 자연광. 함몰·피문 제외. 연결은 `assets-report.md` §5
- 에셋: 준비 스크립트가 `m3d-assets/` → `web/public/m3d/` 로 가공(오버레이 3242px 축소, 투명 PNG 화 등). `public/m3d/` 는 gitignore. 커밋 금지(본인 얼굴)
- 원본 품질 이슈(중국어 title·좌우 반전·-1 점수)는 보정 표시

## 3. 쓸 것 — `orchestration/work/charty-consult-mockup/SPEC.md` 1개
1. 화면 ①·② 각각 — 레이아웃(구역·크기 비율·해상도 가정: ① 1920×1080 가로, ② 태블릿 1180×820 가로 등 제안), 구성 요소, 상태, 상호작용. ASCII 와이어 포함
2. ①의 그래프 목록 — 무엇을 어떤 차트로(레이더·막대·부위 맵 등), 쉬운 설명 문구 규칙, 등급 4단계 색(메디킷 팔레트로)
3. ②의 기능 — 차티 stg 의 어떤 화면/컴포넌트를 본뜨는지 근거(`stg:path:줄`)와 함께. 시술 목록·가격 목데이터 출처
4. 동기화 메시지 계약(이벤트 타입·페이로드), 라우트(`/screen` · `/tablet` 등), 초기 상태
5. 데이터 모델 + 어댑터 경계, 목데이터 파일 구성
6. 3D 뷰어 설계 — 로더, 텍스처·오버레이 합성 방식(셰이더 or 다중 재질), flipY·좌표 주의점
7. 에셋 준비 스크립트 명세(입력→출력 파일 목록)
8. 메디킷 1.4.0 적용 방법(tailwind preset·base.css·쓸 컴포넌트 목록 / 없는 부품 직접 구현 목록)
9. **WP 분할**(구현 워커 1명이 순서대로 할 단위) + WP 마다 완료 조건
10. **수용 기준(AC)** — 번호 매겨서. 「`npm run build` 통과」「두 탭에서 ②에서 시술 추가 시 ①에 1초 안에 보임」「3D 얼굴이 필터별로 바뀜」 등 검증 가능한 문장
11. 정할 것 — 네가 못 정한 것만. 기본값 제안과 함께

## 9. 완료
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_210dc6eb-3363-4f0c-9c78-b2b05f193d94 --text "[planner 완료] orchestration/work/charty-consult-mockup/SPEC.md" --enter
```
질문은 같은 terminal send 로 `[질문] ...`.
