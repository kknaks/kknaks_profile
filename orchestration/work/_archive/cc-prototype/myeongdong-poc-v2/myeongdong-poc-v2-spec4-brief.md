# [planner] SPEC-004 · WORK-004 — 시술실 앱(Flutter · iOS) · 계정 · 권한 · 통역

너는 cc-prototype `planner` 워커다(역할: `orchestration/roles/cc-prototype/planner/`). 작업 워크트리 = 코디 워크트리(public 레포).

## 1. SSOT — 이 순서로 이긴다

1. 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/_RESUME.md` §2 의 **2026-10-21 「디자인 2단계」 이후 줄 전부**(Flutter · 로직 정본 = 구현 코드 · 계정 · 통역 · 빠른 말하기 · 뺀 것 · 의사 = 자기 자신으로 수락 · **권한 back 검사** · iOS/TestFlight · 앱 위치 · 기기 back = 배포 주소) + 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-mobile-read-report.md` §9 · §9-1 · §9-2
2. 계약 기준(로직 정본): `para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` 0.2.0 + 구현 코드 `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2/procedure/back`(read-only — 스냅샷 · 조작 API · SSE 실제 모양) + E2E 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/e2e-feedback-batch-1.md`
3. 화면 정본(모양만): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-mobile/Ceramique 간호사 모바일.dc.html` · `Ceramique 시술실 태블릿.dc.html` + 리포트 §2(화면) · §7(재사용)
4. 통역 원천: 이전 PoC `/Users/kknaks/git/toy_pr2/cc-prototype` `origin/main` 의 `cc/back`(`WS /api/interpret` · Soniox · 언어 목록) — `git show origin/main:<경로>` 로 read-only

## 2. 만들 것

### A. `20-spec/spec-004-procedure-app.md`(+ README 인덱스)
1. 범위 In/Out(뺀 것 명시)
2. 폴더 · 실행 — `procedure/app/` Flutter(iOS 만) · 로컬 실행 · TestFlight 빌드 절차(번들 id · 서명 · 마이크 권한 문구 `NSMicrophoneUsageDescription`) · env(back 주소: 로컬 / 배포 `https://ccc.medisolveai.xyz`)
3. **계정 · 권한**(back 변경) — 계정 테이블(어드민 · 의사 · 간호사 · 원장 = KOS 원장 연결 · DB 에 사람마다) · 로그인 카드(PoC = 어드민 + 의사 1(데모 실제 원장) + 간호사 1) · 토큰에 역할 + 원장 id · **조작 API 마다 역할 검사 표**(허용/403) · 수락 규칙 · actor = 로그인 계정. 웹 로그인 · 의국 화면도 이 계정 체계로(어드민)
4. **통역**(back 변경) — `cc/back` 통역을 `procedure/back` 으로 복사 · 언어 목록(이전 PoC) · **WS 토큰 인증**(Origin 만으로 안 됨) · 오디오 형식(PCM16 송신 · 24kHz PCM 재생)
5. 빠른 말하기 — 시안 문구 6개 × 언어(하드코딩 표 — 번역 문구는 이 SPEC 에 표로)
6. **앱 화면** — 모바일 · 태블릿 각각: 목록 · 룸 상세 · 호출 시트 · 통역 바/드로어 · 로그인. **모든 버튼 활성 · 상태 · 필터 = back 스냅샷 값**(시안 로직 X — 리포트 §5 의 X6 · X7 · M3 · M5 · M8 · M10 · M11 버림). 시안과 다른 곳 표
7. 데이터 — SSE 를 Flutter 에서 HTTP 스트림으로 읽기 · 재연결 · version · 첫 스냅샷. 기존 API 재사용 / 새 API 목록
8. 검증 — 로컬 E2E + **아이폰 · 아이패드 실기기 E2E**(마이크 · 통역 재생 · 권한 1회가 완료 조건) · 권한 단위 시험
9. 열린 것

### B. `30-work/work-004-procedure-app.md`(+ README)
WP 순서: back 계정 · 권한 · 통역(backend) ∥ Flutter 앱 뼈대 · 화면(새 워커 `mobile`) → 리뷰 → 수정 → **배포(WP7 — 기기가 https 로 닿게: `ccc.medisolveai.xyz` 에 procedure back · front · SSE 버퍼링 off · wss)** → TestFlight → 기기 E2E. WP 마다 담당 · 경로 · 완료 조건 · 검증 명령(부분만 · 통합은 마지막)

## 3. allowed_paths
- `para/projects/summer-star/cc-prototype/20-spec/` · `para/projects/summer-star/cc-prototype/30-work/` — 그 밖 read-only · 커밋 금지

## 4. 하지 말 것
- 결정에 없는 정책 발명(비면 열린 것) · 키 · 토큰 · 비밀번호 · 실명 · 연락처 · Apple 팀 id 값(public)

## 5-1. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "planner 완료: SPEC-004 · WORK-004" \
  --body "변경 파일 / SPEC 절 요약 / WP 목록 / 열린 것 / DEC 대응표 누락 0 여부 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] planner SPEC-004 · WORK-004 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] planner: <질문>" --enter`
