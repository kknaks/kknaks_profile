# charty-consult-mockup — RESUME

## 1. 목표
M3D 피부 스캐너 리포트(reference/2026-10-21-charty-poc)를 재구성한 피부과 상담용 웹 목업. 메디킷 DS · 차티(origin/stg) 화면 문법 기준.

## 2. 정해진 것
- DS = 메디킷(`/Users/kknaks/git/medikit` main) · 차티 기준 = `CENTURION-CHARTY` **origin/stg**(v1.8.0-rc.3, 10-16). 로컬 체크아웃 release/v1.3.1 은 낡음
- 1판은 read-only 조사 — 완료(research-report.md)
- 메디킷 **1.4.0** 기준 · **Next.js** 로 프론트 화면 2개만 · 목데이터(고객명 이건학=사용자 본인) · M3D 리포트는 참고만, 실 API 는 추후 3D 스캔 업체에서 (10-21 사용자)
- 화면 ① 큰 스크린(상담사+고객 공동 시청): 좌 3D + 필터(잔주름·굵은주름·염증…) / 우 분석 그래프 + 상담사가 추가한 시술 + 조정된 최종 가격
- 코드 위치 = `reference/2026-10-21-charty-poc/web/` (Next.js, `npm run dev` 로만 공유) · 원본 에셋 `m3d-assets/` 는 gitignore
- 3D = **실물**(리포트 링크 살아 있음, ZIP 4개 93MB 확인) — 자리표시자 기본값 폐기
- 화면 ② 상담사 태블릿: 기존 차티 상담 화면(시술 추가·체크리스트·차트 …) — 여기서의 조작이 ①에 반영

## 3. 열린 것 · 진행
- 두 화면 동기화 — 기본값 BroadcastChannel(같은 PC 탭 2개)
- HAR(개인정보 포함) 커밋 여부 — 미정
- researcher 2판 완료 — assets-report.md · m3d-assets 290MB
- 다음: 스펙(planner 워커) → 승인 → 구현
- 차티 stg 에 가격 조정 기능 실재 여부 — 확인 안 됨
- project config 없음(centurion·cc-prototype 와 별개) — 조사 뒤 정한다
- 코디 handle: term_210dc6eb-3363-4f0c-9c78-b2b05f193d94 (10-21 재확인 — term_342408b8 는 죽음. 핸들이 오간다, 발주 직전마다 list)
- researcher: term_90640d1b-3c18-453b-aa3c-68292d96eedb · task_b5d67b936d91 · dispatch ctx_7278e51889d3 · 산출 research-report.md

## 4. 진행 (10-21 사용자: 「코드 구현까지 다 끝내」 — 스펙→구현→리뷰→검증 일괄 승인)
- 에셋 기본값 7건 확정(오버레이 hd_ai · 함몰/피문 제외 · _M 3242 · OBJ 그대로 · public/m3d gitignore · 받은 파일 고정 · 회전+필터만)
- HAR 커밋 여부 — 기본값 gitignore(사용자 무응답)
- planner: term_e0283cd2-3c09-4041-bb7f-8323d8b35e82 · task_57aec9db940e · ctx_16364aa1a3dd → SPEC.md
- planner 완료 — SPEC.md(WP1~8 · AC 25). §11 정할 것 5건 전부 기본값 확정(태블릿 좌우분할 · 피부분석 탭 · 금액 직접수정 없음 · 굵은주름 id 기준 · 추천 표대로)
- frontend: term_770074d3-4037-42b7-95af-7ef8493b7570 · task_0678a79d3617 · ctx_bb3d20cdfe08 · fe-brief.md → fe-report.md · 포트 3417
- 다음: reviewer(AC 대조) → 코디 실물 검증 → 커밋
- frontend 1판 완료(verify 통과, 코디 직접 재실행 exit 0) · reviewer term_8201fd4c · task_27da1aa1ffe3 → review-report.md **FAIL**(F-1 AC-11 타이밍 · F-2 테스트 보고서.html PII)
- F-2 코디 처리(.gitignore `reference/2026-10-21-charty-poc/*.html`). 잔주름 얼룩 코디 눈 확인 → dilate 로
- 수정 1판 발주 fix1-instructions.md (F-1 · 잔주름 선 · W-1 32px · W-2 · W-3 · 테스트 빈틈). W-6 태블릿 금기 원문은 유지
- 다음: 수정 확인 → 재검수 → 코디 실물 → 커밋
- 수정 1판 완료 · 재검수 **PASS** · 코디 verify 재실행 exit 0(vitest 36 · e2e 16) · 커밋 대상에 m3d/HAR/screens/html 0건
- 미리보기 dev 3417(코디가 띄움). 커밋·PR·아카이브는 사용자 확인 대기
