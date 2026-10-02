# 작업 요약 — strong-hajin-polish (strong-hajin)

기간: `2026-10-01` ~ `2026-10-02`
결과: 코드 kknaks/Strong_hajin#9 · 문서 kknaks/kknaks_profile#70 · 인프라 MediSolveAIDev/k8s_infra_mac#7 머지, **2026-10-02 운영 반영**(`3d47a32-arm64`, Argo Synced/Healthy 8/8)

## 1. 무엇을 했나

운영 첫 배포(10-01) 뒤 사용자가 실제로 쓰며 낸 수정 요청(참조자 누락 버그·담당자 변경 모달·검색칸·간트/타임라인 범위·탭 깜박임·AX 업무 초안 카드)을 조사 → SPEC 반영 → WP(WORK-008) → 페이지별 구현·검수·재수정으로 처리했다.
도중에 운영 회의 요약 실패(Phase 4)와 AX 가 업무 생성 때 프로젝트를 찾지 않는 문제(Phase 5)가 드러나 같은 판에 넣었다.
사용자 로컬 E2E 를 두 바퀴 돌며 AX 카드 모양을 다시 잡았고(무채색·제목 줄·채워지는 바·채팅 안 색 원칙), 운영에 반영했다. 배포 직후 옛 AX 대화 세션 소실(Phase 6 핫픽스)은 사용자 결정으로 버렸다.

## 2. 적용한 기술·개념

- **같은 화면 데이터 기억(stale-while-revalidate) + 세대 토큰** [[stale-while-revalidate]] — 탭 이동 깜박임을 라이브러리 없이 없앴다
  - 왜 이걸 골랐나: 원인은 응답 속도가 아니라 탭마다 페이지가 언마운트되고 캐시가 0 인 구조였다(조사). react-query 를 들이면 api.ts 규율·테스트가 통째로 바뀌어, 모듈 Map 하나 + 화면 훅으로 좁혔다
  - 무엇이 어려웠나: 첫 구현이 「지금 주인」만 봐서, 로그아웃 뒤 늦게 도착한 옛 사람의 응답이 새 사람의 기억에 들어갔다(검수 FAIL). 요청 시작 세대 = 지금 세대일 때만 기억하는 토큰으로 닫고, **기억한 권한으로는 명령을 열지 않게** 갱신 응답 전 단추를 잠갔다. 그 잠금이 진입 effect 성공에서만 풀려 갱신 한 번 실패하면 영구 잠김인 것도 재검수에서 나왔다
  - 근거: `frontend/src/lib/screenCache.ts` · `review-fe-p2-report.md` · `review-fe-p2b-report.md` · `1ef8db0`
- **「AX 초안 = 새 업무 추가를 AI 가 채운 것」(P-1)** [[human-in-the-loop]] — AX 경로를 따로 두지 않고 사람 경로와 같은 필드·필수·검증으로
  - 왜 이걸 골랐나: 사용자 「사람이 채우냐 AI 가 채우냐 차이야」. 이 원칙 하나로 AX 전용 기한 필수 검사 제거, 초안 필드 대조(빠진 parent_task_id), 「수정」= 새 폼이 아닌 `CreateWorkModal` 재사용, Phase 5 의 「AI 도 프로젝트를 찾아 채운다」가 줄줄이 결정됐다
  - 무엇이 어려웠나: 380px 채팅 카드에 모달 필드 전부가 안 들어간다 → 카드는 읽기 전용 요약, 편집은 모달(사용자 3안 선택). 모달 재사용 때 참고 업무가 비동기로 채워지는 칸이라 등록이 빨리 눌리면 빈 배열로 덮이는 손실이 검수에서 나왔다(초안 값 보존으로 닫음)
  - 근거: SPEC-001 S-9 · SPEC-002 §2.9 · `review-fe-p3b-report.md` · `8700bd0`
- **여러 파드가 이어 쓰는 AI 세션 = 공유 저장소의 문제** [[shared-session-storage]] · [[no-silent-fallback]] — 회의 요약 실패 원인
  - 왜 이걸 골랐나: 회의 중 세션은 back 파드에서 열리고, 종료 합성은 worker-meeting 이 resume 한다. 세션 파일이 파드 로컬이라 「세션 없음」으로 200ms 만에 3번 실패. 코디는 처음 「코드 콜드스타트만」으로 정했으나 사용자 지적(「PVC 가 없어서 못 읽는 거 아니야?」)이 맞았다 — 핵심은 공유, 콜드스타트는 안전장치. 녹음처럼 Mac 호스트 hostPath 를 앱 기본 경로에 그대로 마운트해 env 도 필요 없게 했다
  - 무엇이 어려웠나: 공유 디렉터리의 codex sqlite 를 다섯 파드가 동시에 쓴다(같은 VM 커널·virtiofs 라 원리상 성립, 증명 안 됨) → 반영 뒤 오류를 보고 문제 시 sessions/ 만 공유로. 배포 직후에는 공유 이전에 열린 대화 세션이 사라져 그 대화만 실패했다(일회성)
  - 근거: `research-meeting-summary.md` · `review-p4-report.md` · `dd4bd7c` · k8s_infra_mac#7
- **AI 에게 「찾되 지어내지 말라」** [[evidence-binding]] · [[human-in-the-loop]] — 업무 생성 때 AX 가 프로젝트·업무를 아예 찾지 않던 문제
  - 왜 이걸 골랐나: 도구 설명은 「대화가 준 필드만」, 라우팅 정책은 「graph_search 먼저 부르지 말라」, project_list 는 「회의용」이었다 — 탐색을 막고 있던 건 프롬프트·도구 설명이었다. 한 후보로 확정될 때만 채우고 못 찾으면 비우고 말하게 했다
  - 무엇이 어려웠나: 근거(answer resources)를 넓히자 회의 causation(`meeting-batch:` 처럼 UUID 가 아닌 값)에서 기억 코드가 터졌다 — 같은 원인으로 회의 중 task_list·meeting_get 이 **이전부터** 깨져 있던 것이 검수에서 함께 드러났다
  - 근거: `research-graph-search.md` · `review-p5-report.md` · `33e8f1b`
- **E2E 피드백은 모아서 한 번에** — 운영 방식
  - 왜: 지적 하나를 받자마자 단건 발주했다가 질책. 워커가 같은 화면을 여러 번 뜯고 뒤 지적과 충돌한다. 기록만 하고 「다 됐어」 뒤 한 브리프로 묶었다(E2E-3~11 한 번)

## 3. 막혔던 것 / 사고

- **세션 재연결로 코디·워커 핸들이 바뀌어 완료 신호를 놓쳤다** → 사용자가 「워커 신호 못 받은 거 아니야?」로 짚음 → `orca terminal list` 로 새 핸들을 찾아 보니 백엔드·리뷰어 Claude 세션은 꺼져 있었고, 프론트 보고는 인박스에만 있었다. 이후 모든 브리프에 새 코디 핸들을 박고 죽은 일은 새 워커로 재발주. 「보고가 조용하면 핸들을 다시 확인」을 늦게 했다
- **Docker Desktop 이 중간에 꺼져** 로컬 스택 재시작이 실패했다 → `open -a Docker` 로 살렸으나 사용자의 다른 프로젝트 컨테이너(task-management)는 자동으로 다시 뜨지 않았다(사용자에게 알림)
- **코디가 계약을 잘못 적은 자리** — 와이어프레임에 프로젝트를 「기본 정보」에 넣었다(실제 모달은 「업무 연결」), 체크리스트 페이지를 「N개 · 첫 항목」 요약으로 적어 목록이 안 떴다. 둘 다 사용자가 잡았다 → 화면 계약은 **실제 모달 코드를 열어 1:1** 로 적는다
- **화면 확인을 Playwright 로만** 했다 — 이 세션엔 데스크톱 제어가 없어 Tauri(WebKit) 검색칸은 사용자 눈으로만 확인. Playwright WebKit 은 버전 불일치로 멈췄다
- 실제 시드 DB 에는 데모 계정이 없어 화면 확인용 `ax_demo_polish` 를 따로 만들었다(`reset_demo` 는 `ax_demo*`/`ax_test*` 이름만 허용)

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-01 | 발주는 문서 → WP → 코드 순, WP 하나를 페이지로 나눠 순차 발주 | 사용자 · 런북 |
| 2026-10-01 | P-1 AX 초안 = 새 업무 추가를 AI 가 채운 것 | 사용자 |
| 2026-10-01 | 초안 카드 = 읽기 전용 요약, 「수정」 = `CreateWorkModal` | 380px 에 필드 전부가 안 들어감 · 사용자 3안 |
| 2026-10-01 | B-01 깜박임은 프론트만, 서버 성능은 체감 뒤 | 원인의 직접 몫이 FE · 사용자 |
| 2026-10-01 | ~~회의 요약은 코드 콜드스타트만, 인프라 볼륨 안 함~~ → 세션 홈을 Mac 호스트 hostPath 로 공유(+콜드스타트 안전장치) | 사용자 지적이 맞았다 |
| 2026-10-01 | 채팅 서랍 안 색 원칙: 사람 행동 = 검정, 파랑 = AI 진행만 | 사용자 · 범위는 채팅만 |
| 2026-10-01 | 초안 카드 넘김 = 본문 위 제목 줄 + 늘 보이는 ‹ › (호버 화살표 대체) | 사용자 |
| 2026-10-01 | E2E 피드백은 모아서 한 번에 발주 | 사용자 질책 |
| 2026-10-01 | AX 업무 생성 전 프로젝트·업무 탐색, 못 찾으면 비우고 말함 | P-1 연장 · 사용자 질문 |
| 2026-10-02 | ~~Phase 6 핫픽스(세션 잃은 대화·배치 재개)~~ → 버림 | 사용자 「옛 데이터면 크게 문제 없어 · 버리자」 |

## 5. 날짜별 로그

- `2026-10-01` 세팅 · 사용자 요청 수집(8건) · BE/FE 읽기 전용 전수조사 · 항목별 계약 확정 · Docker 정리 · SPEC 반영(검수 FAIL→fix1) · WP · Phase 1~3b 구현·검수·커밋 · 회의 요약 원인 조사·Phase 4 · E2E 1차·묶음 · Phase 5
- `2026-10-02` 코드·문서·인프라 PR 머지 · arm64 이미지 · 노드 디렉터리 · Argo sync · 운영 확인 · Phase 6 핫픽스 취소

## 6. 산출물

- spec PR: https://github.com/kknaks/kknaks_profile/pull/70
- code PR: https://github.com/kknaks/Strong_hajin/pull/9 (squash `3d47a32`)
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/7
- 리포트: `fe-survey-report.md` · `be-survey-report.md` · `research-meeting-summary.md` · `research-graph-search.md` · `review-spec-report.md` · `review-spec2-report.md` · `review-fe-p1-report.md` · `review-fe-p2-report.md` · `review-fe-p2b-report.md` · `review-be-p3a-report.md` · `review-fe-p3b-report.md` · `review-fe-p3b2-report.md` · `review-p4-report.md` · `review-p5-report.md` · `flaky-baseline-evidence.md`

## 7. 잔여 (다음 고도화로)

- **운영 확인(사용자)**: 실패했던 회의 2건 [다시 시도] → 회의록 · 새 회의 종료 → 회의록 · 새 AX 대화로 업무 생성 시 프로젝트 연결
- **공유 세션 홈의 동시성**: 다섯 파드의 codex sqlite 오류 관찰 — 문제 시 파드별 홈 + `sessions/` 만 공유
- **세션을 잃으면 대화·회의 배치는 대비가 없다**(Phase 6 취소) — 공유 hostPath 밖 원인이 생기면 다시 본다
- **서버 성능**(N+1 · 요청마다 인증 재계산 · 캐시 헤더) — `be-survey-report.md` §2, 깜박임 체감 뒤 결정
- **「AX 제안」 칩 대상 확대 여부**(지금은 업무 생성·요청 두 kind) · 결재자 목록이 담당자를 거르지 않는 것 · 「업무 주인」을 고르면 참조자에 남는 것(B-02 범위 밖 기존 동작)
- **DS-gaps**: 검정 solid 단추(채팅만) · 초안 카드 제목 줄 · 채워지는 4칸 바 · 체크리스트 장식 상자 · 추천 대화 가로 칩 — 디자인 시스템에 올릴지
- **기준선 날짜 의존 테스트 5건**(CreateWork 시작일 4 · CreateWorkLayout 1) — 10월이라 9월 칸이 없어 실패, 오늘을 고정하는 테스트로 고칠 것
- 남은 OQ: SPEC-001 OQ-K(간트/타임라인 화면 자리) · DEC-007 OQ(로그인 시도 제한 · M-5 · 개인판 origin · 백업 정책 · 노드 codex 업그레이드 · Releases)
