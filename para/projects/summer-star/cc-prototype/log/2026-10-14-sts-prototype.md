# 작업 요약 — sts-prototype (cc-prototype)

기간: `2026-10-10` ~ `2026-10-14` (코드 커밋은 10-13 ~ 10-14)
결과: **main 머지 · 배포 완료** — https://ccc.medisolveai.xyz (코드 `kknaksss/cc-prototype#1` → `cb74d05`, 인프라 `MediSolveAIDev/k8s_infra_mac#16~#19`). 10-16 세라미크 지점 시연용 PoC

## 1. 무엇을 했나

세라미크 지점 시연을 위해 「병원 현황판(데스크) + 직원 개인 화면 + 외국인 환자 통역」 PoC 를 만들었다. sts(실시간 통역)는 별도 기능이 아니라 cc 직원 화면 안의 통역으로 접었다(DEC-001 D-06). 시안 → 구현 → 사용자 E2E 를 세 바퀴 돌며, 처음의 「시안 그대로 + KOS 캡처 재구성」에서 **「동선이 메인 데이터 · 메모는 원문 · 배정은 데스크/시작·종료는 본인」** 이라는 업무 원칙으로 갈아엎었고, 그 원칙은 사용자와 단계별로 정리한 `reference/2026-10-12-cc-prototype/workflow.md` 에 남았다. 데이터는 KOS 운영 캡처를 대본으로 한 목데이터 시나리오(사람 이름 · 이메일만 가짜), 배포는 Mac Studio k8s(`k8s_infra_mac`)에 ArgoCD 로.

## 2. 적용한 기술·개념

- **동선을 메인 데이터로, 메모는 참고용 원문으로** [[structured-work-as-primary-data]] — 환자 상세 · 방 패널의 정보 구조
  - 왜 이걸 골랐나: 처음엔 오더 메모를 「오늘 오더」 칸으로 보여 줬는데, 데스크가 메모를 보고 시술을 순서대로 넣는 순간 **그 동선이 곧 오더**이고 메모 글은 이후 아무도 고치지 않는다(사용자). 의사가 바꾸라고 하면 메모가 아니라 동선을 고친다
  - 무엇이 어려웠나: 「오늘 오더」 칸을 넣었다 뺐다 세 번 뒤집혔다 — 「누가 언제 무엇을 넣나」(상담사가 상담 중 → 결제 → 데스크가 후보에서)를 먼저 정하지 않고 화면부터 지었기 때문
  - 근거: `workflow.md` 「동선이 메인 데이터」 · `e2e-feedback-batch-2.md` #18~#20
- **메모 양식에 기대지 않는다(원문 그대로)** [[no-inference-from-free-text]] — 명동점 상담실장들의 양식(`------` · `[특이사항]` · `OUT TIME` · 예약 메모 `날짜/유입처/희망시술/…`)을 잘라 읽어 ⚠ 주의 · 아웃 시각 · 예약 시술을 만들었다
  - 왜 버렸나: 사용자 「안양점이 ------ 이렇게 안 쓰면 어떻게 할 건데?」 — 지점마다 양식이 다르다. 구조화된 값은 KOS 구조 필드에서만
  - 같은 이유로 「지정 직원」(메모에 이름이 글자로 나옴 → 서명 · `실장 : ○○` 도 걸림) · 위험 단어 강조(`[임플란트 여부] x` 도 빨강)도 근거 없는 추정이라 삭제
  - 근거: SPEC-001 0.3.0 §0-b · `e2e-feedback-batch-2.md` #25 #27 · WP10 · WP12
- **메모 공개 = 쓰인 시점** [[as-of-visibility]] — 하루 끝 캡처를 「개원 전」 시드로 쓰니 상담 뒤에야 생길 오더 · 상담 메모가 접수 때 보이는 「미래 정보」 문제
  - 풀이: 과거 방문 메모 · 시술권은 언제나, 오늘 상담 · 오더는 상담 종료 뒤, 담당자 메모는 히스토리에만. 방문 카드로 오늘/지난 분리
  - 근거: `workflow.md` 「메모 원칙」 · WP10 `visits[]`
- **목데이터 시나리오 = 시드(아침 KOS 조회) + 이벤트(진행 중 KOS 에서 들어오는 것)** [[seed-data]] · [[as-of-visibility]]
  - 왜 이걸 골랐나: 캡처를 14:45 시점으로 재구성한 시드는 위치 · 단계 · 큐 · 담당이 22개 항목 추정이었다(`api-source-audit-report.md`). 「아무도 접수 안 한 아침」에서 시작하고 상담 종료 · 결제 · 시술 종료 때 대본 방문의 실데이터를 이벤트로 넣으면 추정이 사라진다
  - 근거: `scenario-format.md` · `scenario-report.md` · WP7b
- **KOS 공개 OpenAPI vs 웹앱 내부 API** [[public-vs-internal-api]] — 관제 조작을 나중에 KOS 에 반영할 수 있나
  - 알아낸 것: 공개 75개 중 쓰기는 예약 · `changeFlowStep`(`scheduleId` · `step` 두 칸뿐, 시술권 차감 없음, 상담 담당 · 시술 목록 · 미완료 시술로 거절) · 메모 2종뿐. 시술 완료 · 담당 · 집도의 · 상담사 지정은 **DEMO HAR 로 내부 API 확인**(`change-tasks-complete` 등, 모두 `scheduleId + sequences[]`). 시술권은 작업 DONE → USED, CANCELED → 유지(캡처 11건)
  - 판단: PoC 는 KOS 호출 0 · 조작 자리마다 `kos api 연동 필요` 주석. 정식 연동은 공개 API 요청, 사람 세션 토큰 · 내부 API 직결은 쓰지 않는다
  - 근거: `research-kos-har-report.md` · `research-kos-har2-report.md` · `workflow.md` 「KOS 반영 표」
- **Soniox 통역 = STT(two_way 번역) + TTS 두 WS 를 back 이 중계** [[websocket-relay]] · [[half-duplex-echo-suppression]] · 국적 → 언어(TW · HK 자막 번체 변환, TTS 는 간체만)
  - 막혔다가 푼 것: 폰에서 번역 음성이 마이크로 다시 들어가 재번역(되먹임) — `echoCancellation` 은 폰 · Web Audio 재생에서 무력. **반이중**(재생 중 송신 중지 + 끝나고 400ms) 으로 해결
  - 근거: `wp2-be-report.md`(실물 호출 4건) · `interpret-fix1-report.md`
- **k8s 배포(Helm + ArgoCD 수동 sync + Cloudflare Tunnel)** [[kubernetes]] · [[ci-cd]] — strong-hajin 차트 패턴 재사용
  - 막혔다가 푼 것: local-path 가 **lima-worker-1 에만** 볼륨을 만든다 → back(PVC) Pending → nodeSelector 고정 + Pending PVC 삭제. 데이터는 public 레포라 이미지 · git 에 안 넣고 Secret(하위 폴더 불가 → `event-<id>.json` 평평하게)
  - 근거: `deploy-infra-report.md` fix1 · infra #17

## 3. 막혔던 것 / 사고

- **추정으로 화면을 채웠다** → 사용자 질책 2회(「X만 가짜」인데 실값을 막음 / 「실제 존재하는 api로만」). 작성자 = 상담 담당자, 직군 = 이름이 나온 칸, 예약 시술 = 사후 실적값 등 22개를 점검으로 찾아 제거 → 메모리 `feedback_real_data_scope` · `feedback_only_real_api_fields`
- **업무 흐름을 지어내 설명** — 「접수하면 동선 자동 생성」 「상담 종료 때 시술 자동 부착」 → 「고객 동선 관리가 자동으로 안 되는데 왜 자꾸 자동이라고 우기냐」. workflow.md 를 사용자와 단계별로 다시 썼다
- **브랜치 코드가 배포됐다** — Actions 가 모든 브랜치 push 에서 빌드 → 사용자 「main 에만 배포할 거고」. 워크플로를 `branches: [main]` 으로 막고 main 빌드(`cb74d05`)로 교체(infra #19)
- **워커 터미널 핸들이 수시로 바뀌고 죽음** — 새 워크트리의 신뢰 확인 창이 inject 를 먹음 · 시안 워커 핸들 사망 · 핸들 오타. 발주 직후 `terminal read` 로 claude 화면 확인을 습관으로(메모리 `feedback_orca_terminal_pitfalls` 보강)
- **Cloudflare 엣지가 해외(LHR · PDX)** — 「Mac 에 올려서 느리냐」 → LAN 5~10ms · 외부 0.5~1.5s, `cdn-cgi/trace colo=LHR`. Mac · 앱 문제가 아니라 존 라우팅 — **미해결**(§7)

## 4. 결정

정본은 DEC-002(D-01~D-30) · DEC-003(D-01~D-07) · SPEC-001 0.3.0 §0-b · `workflow.md`. 큰 줄기만:

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-12 | sts 는 cc 직원 화면 안의 통역(DEC-001 D-06) | 사용자 |
| 2026-10-13 | ~~시드 = 10-09 14:45 재구성~~ → 개원 전 + 시나리오 이벤트 | 추정 22개 · 사용자 「실데이터 바탕으로 더미」 |
| 2026-10-13 | ~~직원 큐 · 배정 = 방에 있음~~ → 단계 단위 배정, 시작 · 종료는 본인(의사 · 상담사 · 피부관리사) | 사용자 「배정은 데스크, 시작 종료는 본인 화면」 |
| 2026-10-13 | ~~가짜는 고객명뿐~~(D-09) → 사람 이름 · 이메일은 가짜(DEC-003 D-04) | 공개 배포 |
| 2026-10-13 | 메모 양식 가공 · 지정 · 위험 단어 강조 전부 삭제 | 지점마다 양식 다름 · 근거 없음 |
| 2026-10-13 | KOS 호출 없음 · 주석만 | 운영 DB · 「되는 가능성 확인했으니」 |
| 2026-10-13 | 배포 = k8s_infra_mac · ccc.medisolveai.xyz · 공개 | DEC-003 |
| 2026-10-14 | 이미지 빌드 · 배포는 main 에서만 | 사용자 |

## 5. 날짜별 로그

- `2026-10-10` sts 조사(Soniox STT 번역 내장 + TTS) · 기능 실험실 DEC-001
- `2026-10-12` cc 문서 · 시안 사본 커밋 · cc 시안 × KOS 캡처 적합성 조사 · 기획 논의 시작
- `2026-10-13` DEC-002 · SPEC 0.1.0 → 구현 WP1~4 · E2E 1차(20건) → 워크플로 정리 · KOS HAR 1·2차 → SPEC 0.2.x · 0.3.0 → WP6~WP12 · 배포(infra #16~#18)
- `2026-10-14` 코드 main 머지(#1) · main 빌드로 재배포(infra #19) · 아카이브

## 6. 산출물

- code PR: https://github.com/kknaksss/cc-prototype/pull/1 (squash `cb74d05`)
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/16 · /17 · /18 · /19
- 배포: https://ccc.medisolveai.xyz (ns `cc-prototype-prod`, ArgoCD 수동 sync)
- 문서: DEC-002 · DEC-003 · SPEC-001 0.3.0 · WORK-001 · `reference/2026-10-12-cc-prototype/workflow.md`
- 데이터(로컬만): `reference/2026-10-12-cc-prototype/cc-back-data/`(시나리오 · 가짜 이름 직원 · 원본 · 대응표 — gitignore)

- `kknaksss/sts-prototype` → `main`
  - `8d691bd` ci(cc): 이미지 빌드는 main push 에서만 — 배포는 main 코드만
  - `14e5250` fix(cc): 통역 되먹임 — 번역 음성 재생 중 마이크 송신 중지(반이중), 재생 끝 +400ms 재개
  - `2abe704` fix(cc): E2E #27~#30 — 근거 없는 지정·강조 삭제 · 셀렉터 직군 목록 · 예약 메모 · 동선 줄 정렬 · 방 패널 고정·열 스크롤·메모 접기
  - `8f86bbd` feat(cc): SPEC 0.3.0 — 메모 원문 · 방문 카드 · 방 패널 2열 · 셀렉터 배정 · 후보 묶음 n/m · 예약 상세/노쇼 + 배포 이미지(arm64 GHCR)
  - `9f8f712` feat(cc): SPEC 0.2.1 — 단계 단위 배정 · 고객 중심 방 패널 · 5직군 · 목데이터 시나리오 · 결제 완료
  - `470b3f7` feat(cc): PoC — 데스크 현황판 · 직원 페이지(의사·코디) · 환자 상세 · 통역(Soniox 중계)
  - `1d11cf2` chore(cc): claude design 시안 사본 — 현황판 v3 · 의사 모바일
- `kknaksss/cc-prototype-main` → `main`
  - `ff6249d` deploy(cc-prototype): main cb74d05 — 배포는 main 빌드만(브랜치 이미지 대체)
- 리포트: `research-soniox-report.md` · `research-soniox-chinese-report.md` · `research-cc-data-fit-report.md` · `research-patient-detail-report.md` · `research-counselor-trace-report.md` · `research-kos-har-report.md` · `research-kos-har2-report.md` · `api-source-audit-report.md` · `scenario-report.md` · `wp*-report.md` · `deploy-*-report.md` · `e2e-feedback-batch-1/2/3.md`

## 7. 잔여

- **배포본 정리**: 공개 주소라 통역(Soniox 과금) 노출 — 시연(10-16) 뒤 내리거나 Cloudflare Access(DEC-003 위험)
- **Cloudflare 엣지 해외(LHR · PDX)** — `medisolveai.xyz` 존 요금제 · 라우팅 확인(사용자). 같은 터널의 모든 앱이 느림
- **KOS 연동 요청**: 시술 작업 상태 변경(완료/취소 · 시술권 차감) · 시술 작업 추가 · 방 · 담당 · 집도의 · 상담사 지정 — 공개 OpenAPI 로 열어 달라. 방 · 우선순위 · 시술 추가는 HAR 추가 녹화 필요
- **현장 확인**(`workflow.md` 「현장 확인할 것」): 수납필요 작업 생성 시점 · 수면 시술 구분 · 시술 단위 배정 · 순서 정하는 사람 · 원장 상담/시술 묶음 · 세팅 중 원장 동선 · 시술 작업 생성 주체 · 간호사 단계 시작/종료 · 시술별 기본 방
- **시안 미반영**: [현장 접수] 기능(계약 없음) · 로그인 시연 카드(가짜 이름이라 직군 첫 사람으로 대체)
- **차티 연동**: 상담 종료 때 상담내역 · 상품이 차티 → 관제 → KOS 로 오는 경로(지금은 이벤트 파일이 대신함)
- **재시드**: 배포 DB 는 PVC 에 남아 있다 — 데이터를 바꾸면 PVC 의 `cc.db` 삭제 후 back 재시작
- **통역 지연**: 확정 발화 뒤 TTS(문장 단위) — 번역 토큰 스트리밍 TTS 로 줄일 수 있음(미적용)
