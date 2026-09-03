
# 작업 요약 — task-ref-multi-upload (mediness)

기간: `2026-09-03` ~ `2026-09-03`
결과: 머지·배포 완료 — code #149(dev)→#150 릴리스(main), 인프라 k8s_infra_mac#4. 413 은 외부 프로브로 prod 실검증까지 끝.

## 1. 무엇을 했나

prod 실사용 반려 2건 — ① 태스크 완료 산출물 1.4MB 첨부가 413, ② 파일을 하나 올리고 기다렸다 다시 하나 올려야 함. ①은 앱이 아니라 **인그레스 어노테이션 부재**(nginx-ingress 기본 proxy-body-size 1m)가 원인이라 k8s_infra_mac 차트에 `50m` 어노테이션을 코디가 직접 넣어 별도 PR 로 해소했다. ②는 공용 첨부 폼 `TaskReferenceAdder` 가 전 층 단일 파일이라, frontend 워커 발주로 **폼 한 곳만** 다중 선택 + 순차 업로드로 고쳤다(API·백엔드 무변경). 리뷰(WARN)·머지·릴리스·GitOps 라이트백 확인까지 당일 완료.

## 2. 적용한 기술·개념

- **계층 소거로 413 발생 지점 격리** — 원인 추적을 코드 수정 전에 확정 → [[fault-isolation]]
  - 왜 이걸 골랐나: "업로드 안 됨"은 클라 가드(25MB)→BFF(50mb)→uvicorn(무제한)→인그레스 중 어디서든 날 수 있다. 앱 각 층의 제한값·에러코드를 먼저 전수 확인해 앱에는 413 을 내는 층이 없음을 소거하고, 남는 후보(인그레스 기본 1m)를 특정했다 — 추측 수정으로 앱 제한만 올렸다면 못 고쳤다.
  - 무엇이 어려웠나: 앱 자체 제한은 400(`TASK_REFERENCE_FILE_TOO_LARGE`)으로 말한다는 것이 결정적 단서 — 413 은 앱 어휘에 없었다.
  - 근거: `back/app/services/task_reference_storage.py:44` · `front/next.config.ts`(proxyClientMaxBodySize 50mb) · k8s_infra_mac#4
- **프록시 제한은 앱 제한보다 크게 — 에러 UX 의 소유권** — proxy-body-size 를 26m 이 아닌 50m 으로 → [[reverse-proxy]]
  - 왜 이걸 골랐나: 인그레스 제한을 앱 제한(25MB)에 딱 맞추면 25MB 초과 시 nginx 의 맨 413 페이지가 나간다. 여유 있게 열어 앱의 400 + 한국어 안내가 먼저 말하게 했다 — 거절 문구의 소유권을 앱에 남기는 선택.
  - 근거: `charts/mediness/templates/ingress.yaml` 주석 · k8s_infra_mac#4
- **다중화는 폼 내부 순차 루프 — 계약·콜사이트 무변경** — 백엔드 배치(form.getlist) 대안을 버림 → [[multipart-form-data]]
  - 왜 이걸 골랐나: 한 요청에 N파일을 묶으면 부분 실패 응답 형태를 새로 설계해야 하고 BE+FE 동시 발주가 된다. 요청당 1파일은 이미 계약("개수 제한은 없다")에 맞고, 생성 모달·랜딩챗에 순차 루프 + 건별 실패 수집 선례가 있었다. 루프를 폼 안에 두어 `onAddFile` 시그니처와 콜사이트 4곳을 안 건드렸다.
  - 무엇이 어려웠나: SPEC-154 §4.19.1 「폼 본체는 한 벌」이 지렛대 — 한 컴포넌트 수정이 레일 다이얼로그·완료 모달 두 표면에 동시에 적용됨을 스펙이 보장했다. 제목 축은 N개일 때 입력을 없애고 파일명을 쓰는 것으로 단순화(파일별 제목 입력은 폼의 축이 아님).
  - 근거: `front/components/tasks/TaskReferenceList.tsx` · mediness-app#149 · `review-code-report.md`(WARN, 계약 8항목 통과)
- **무인증 413 프로브 — 인프라 반영을 외부에서 판별** — ssh 불통에서의 검증 대체 → [[reverse-proxy]] · [[fault-isolation]]
  - 왜 이걸 골랐나: nginx 바디 제한 검사는 앱 인증보다 앞단이다. 1.5MB 무인증 POST 의 응답이 413 이면 인그레스가 자르는 것, 401 이면 앱까지 도달한 것 — 로그인·kubectl 없이 반영 여부가 갈린다. prod/dev × api/front 4개 호스트 전부 401 확인.
  - 근거: `_RESUME.md` §5 · curl 프로브 (2026-09-03)

## 3. 막혔던 것 / 사고

- ssh `medi-me` 터널 불통(104.21.75.230:443 timeout) → kubectl 로 파드 태그·인그레스 직접 확인 불가 → GitOps 라이트백 커밋(46fdf88·04d588c) + 무인증 프로브로 대체 검증. 터널 복구는 별도 건.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-03 | 413 수정은 k8s_infra_mac 코디 직접(워커 발주 안 함) | 어노테이션 2곳 — 설정 변경 범주. 사용자 승인 |
| 2026-09-03 | proxy-body-size 50m, front·api 두 인그레스 | 앱 25MB 제한이 먼저 말하게. 업로드는 front 호스트 BFF 경유라 front 필수 |
| 2026-09-03 | 다중 업로드 FE only — 순차 루프, API 무변경. 백엔드 배치 폐기 | 부분 실패 응답 신설 비용 > 요청 1회 이득. 사용자 선택 |
| 2026-09-03 | planner/스펙 단계 생략 | 버그픽스 — SPEC-154 「개수 제한 없다」 이미 명시. 사용자 선택 |
| 2026-09-03 | 리뷰 WARN 4건(stale title·key 중복·실패사유 증발·dedup)은 머지 후 잔여로 | 계약 8항목 전부 통과 — 경미. PR 본문·리포트에 기록 |
| 2026-09-03 | 릴리스 #150 은 merge commit(squash 아님) | #148 관례 유지 — dev/main 히스토리 경계 보존 |

## 5. 날짜별 로그

- `2026-09-03` 스코핑(계층 소거로 413=인그레스 특정) → 인프라 PR#4 → FE 발주 → 코디 검증(테스트 8/8·tsc 0) → 리뷰 WARN → #149(dev)·#150(main)·#4 전부 머지 → GitOps 라이트백·413 프로브 검증.

## 6. 산출물

- spec PR: 없음(스펙 단계 생략)
- code PR: https://github.com/MediSolveAIDev/mediness-app/pull/149 (dev, squash e64b97cf) → 릴리스 https://github.com/MediSolveAIDev/mediness-app/pull/150 (main, merge 366b0756)
- 인프라 PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/4 (main, squash 0f4f6b5b)

- `kknaksss/task-ref-multi-upload` → `dev`
  - `f3689292` fix(front): 태스크 참고자료 다중 파일 첨부 — 한 번에 N개 선택·순차 업로드
- 리포트: `review-code-report.md` (WARN — 계약 8항목 통과, 경미 4건)

## 7. 잔여

- 리뷰 경미 4건(W1 재시도 stale title · W2 에러 key 중복 · W3 실패 사유 증발 · W4 중복 파일 dedup) — 후속 수정 여부는 사용자 판단, #149 본문에 기록
- ssh `medi-me` 터널 불통 — 복구 후 파드 태그 kubectl 확인 여지(비차단)
- prod 브라우저 실사용 3개 동시 첨부 확인 — 사용자 몫
