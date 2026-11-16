# [backend] D1 독립리뷰 F1/W1~W4 수정

원 역할/작업범위/계약/사용자 지시의 전문은 이 브리프 안에 아래 원브리프를 포함했다. 이번 태스크의 변경 목표가 원브리프보다 우선. live preamble 새 task/dispatch id로 보고한다.

읽을 보고서: /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/review-backend-code-report.md 전부. 기존 backend-code-report.md, 현재 D1코드 및 사용자 implementation-user-direction.md.

## 이번 수정
- F1: deploy/compose.local.yaml backend-environment 명시목록에 DAY_PUBLIC_API_BASE/DAY_DEMO_LOGIN_EMAILS/DAY_DEMO_API_BASE를 ${VAR:-}로 전달. 이 파일은 이번에 allowed_paths 추가허용. 컨테이너기동/재기동은금지.
- W1: json.loads의 RecursionError도모르는응답503처리, 중첩본문200/4xx 회귀검증.
- W2: AGENTS 동시성상한준수. 데모넘김만 perprocess 최대4개·대기열없이 넘치면 기존503 environment_unavailable. 60초전체timeout내처리·취소시슬롯반환·retries0 유지. 4는 기술기본값/상수이며새업무정책아님, 로그도비밀없음. 동시유입·완료/실패/취소복구 의미있는테스트.
- W3: 설정검증로그에원값/userinfo가노출되지않도록 SettingsConfigDict hide_input_in_errors 등 최소수정, 비밀모양입력의str/repr예외검증. 새값/주소를실env에넣지않음.
- W4: deploy/config/dev.env, prod.env에 새이름3개 빈placeholder+주석만 추가. 둘은 코드로관리되는 일반설정파일이며이번수정허용. 기존값을바꾸거나새배포주소/계정값채우지않는다. 실제비밀env·KeyVault·서버설정작업은여전히사용자몫. 서버 manifest는이미env_file로받으므로수정불필요.
- W5: 기존infra6건은코디 scripts/test.sh -q로647passed 확인됐다. 이미검증된성공경로를단위로중복작성할필요없음, 이판정보고서에기록.
- 참고R2: dev의자유문자열error.code가로그에그대로새지않도록 로그값만알려진결과코드/안전한고정값으로제한. dev4xx응답본문원본보존은유지.
- 참고R4: 새settings테스트가호출자 DAY_*환경변수에흔들리지않게해당새env들을fixture에서명시제거/주입. 기존fixture의user값출력금지.
- R1오류클래스위치는동작문제없으니이동하지않음. R3설정불량기동실패는정해진계약유지.

검증: 새회귀케이스+auth notinfra 및 architecture/ruff; 코디가infra포함전체test최종재실행하므로워커는DB조작/실env읽기금지. manifest는가짜placeholderenv만사용해docker compose config로전달shape확인가능(출력에기존실값/secret나오지않게3키/구조만검사). app/**는모바일진행중이므로읽기/수정금지. profile backend-fix1-report.md 및 backend-evidence/fix1-*만보고. 원브리프의§9는보존하되livepreamble이우선.

---
원브리프(배경·계약, 이번수정과충돌하는allowed_paths는위가우선):
# [backend] DAY 앱 D1 로그인 환경 연결 구현

사용자가 방금 「엥 아니 머지는 마지막인데 코드 구현해」라고 명시 지시했다. SPEC PR #921은 OPEN으로 두고, 리뷰 PASS인 spec branch의 exact commit 78f3ee59c8a10e0abb1bde8896302873a46d0732와 이미 승인된 Delivery #235를 구현 기준으로 사용한다. main baseline pending은 그대로 정직하게 기록한다. 사용자 지시가 로컬 skill의 baseline-before-code 절차보다 우선이다. baseline ready로 속이거나 머지하지 않는다. 결과계약·기능범위는 변하지 않는다. 모든 merge·배포·서명·TestFlight는 마지막 사용자 지시까지 금지. 코드 PR 하나→dev, commit/push/PR은 코디만.

기준 문서 경로: /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec/products/day/20-spec/spec-003-mobile-app.md 및 spec-001-login-session.md, 인접 spec-002-procedure-board.md 및 40-architecture/mobile-deployment.md. 모두 전문을 읽는다. profile 작업폴더 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/의 delivery-request.json(승인된 WP 입력; canonical 이슈 https://github.com/MediSolveAIDev/CENTURION_DAY/issues/235), review-policy-report.md, review-wp2-report.md, review-baseline-report.md, research-prototype-board.md도 읽는다. 최신 main 기획원문과 차이는 보고되어 있으며 이번 사용자가 승인한 직접 결정이 우선이다. 그 범위를 또 미정으로 만들거나 재승인을 요구하지 않는다.

코드 트리 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app, origin/dev=917287374723871d554f8a094610d46c39450534, app/이 아직 없다. 로컬 backend는 사용자 canonical ~/git/CENTURION_DAY(dev)의 day-local, deploy/local.env. 실제 키/비밀번호/env 내용을 출력/복사/기록하지 않는다. 사용자 포트·컨테이너·프로세스·기기 조작 금지. 다른 세션 day-procedure-board-2의 방이동·차트작성·KOS·seed는 건드리지 않는다. 프로토 /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app는 read-only.

고정 정책: UUID ID, can*·pickable·need·inbox.section은 서버값; 통역=해당 고객정보 보기직원(board view/is_admin), 간호사 대리수락 필수, 푸시 대상=기존호출(모든의사→병원원장전체/지정→그원장), 관리자추가·호출자제외 신설 없음. 상담사호출 향후만. D1 로그인 환경연결 backend는 승인예외, D2 APNs발송/기기 서버전체·D3 통역WS/사전 서버전체는 이번구현밖, 앱소비+더블만. OQ-A1/A9/A11은 보류, 문구는 DAY·프로토 원천 그대로만 쓰고 원천없으면 빈칸/오류코드. 원문을 새로 번역하지 않는다.


먼저 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/backend/의 role.md·rules.md·skills.md·tools.md·workflow.md와 코드 AGENTS.md 전문을 읽는다. 모바일 워커는 같은 트리 app/**만 수정 중. app/** 읽기만, 수정금지.

## 1. SSOT
공통문서 중 SPEC001 §3 앱환경연결 전문과 케이스매트릭스·규칙14, SPEC003 세션연결/A3~A8/A18~A23, delivery-request.json D1/verification/rollback을 읽는다. 사용자최신명시지시로 미머지SPEC기준 구현, status/baseline위조 금지.

## 2. 목표
기존 웹인증 동작을 보존하며 앱로그인 응답에 environment/api_base_url, /me environment를 추가한다. prod app로그인 데모이메일만 고정dev로 전달해 인증. prod에 KOS호출/DB행생성0, dev장애 fail-closed. 정확한 모양은 SPEC001. D2/D3는 구현금지.

## 3. 계약
- 설정 제안명 DAY_DEMO_LOGIN_EMAILS/DAY_DEMO_API_BASE/DAY_PUBLIC_API_BASE를 기준으로 예제만 추가하고 실제값은 사용자. origin은 https·userinfo없음·port없음or443·root이외path/query/fragment없음 정규화. 잘못된demo주소는 데모로그인503, 이메일목록은 유지해야 fail-closed. 일반계정/웹로그인 영향없게.
- APP_ENV prod+client app+목록이메일 일치만 relay. dev는 relay0. 공백/소문자정규화. auth.login 서비스/DB쓰기/KOS호출 전에 분기. 전체60초 async timeout, redirect0/retry0, 받은 body메모리전달/비밀번호로그저장0.
- signed_in/choose_hospital 응답 검증, dev의 environment/api_base_url은 dev+고정대상 일치해야하며 미상·3xx·5xx·잘못된성공은503 environment_unavailable. 정상4xx HTTP/본문은 계약대로 전달. 서버별 일반app응답·병원선택에도 자기환경과 공개origin. /me environment.
- DB_SCHEMA/APP_ENV process값을 요청마다 변경금지. 임시병원선택은 dev로직이담당, prod가 토큰재발급/쿠키생성하지않음. 기존 웹 /login 및 client=web 유지.

## 4. 먼저 읽을 코드
backend/day/routers/api/auth.py, schemas/auth.py, services/{auth,sessions}.py, session.py, dtos/auth.py, errors.py, backend/common/config.py, backend/tests/day/auth/**, backend/tests/architecture/**, deploy/config 예제(비밀없는것만), deploy/local.env.example, pyproject.toml, scripts/test.sh.

## 5. allowed_paths
backend/day/routers/api/auth.py, schemas/auth.py, D1전용 서비스/DTO 파일(기존 services/auth.py는 필요한최소), backend/common/config.py 및 관련 비밀없는 설정검증테스트, backend/tests/day/auth/**, D1 설정관련 deploy/config 예제와 deploy/local.env.example. 실제env수정금지. 의존성 httpx이미있음, pyproject/uv.lock 수정 필요없을것이나 정말 필요시 먼저질문. AGENTS.md 앱절 주소규칙 한줄만 ‘고정로그인진입점·허용origin은빌드설정, 세션대상은검증된로그인응답’뜻으로 정합수정 허용(#235 승인범위). 나머지 backend·웹·migration·seed·push·interpret서버 수정금지. profile 작업폴더 backend-code-report.md 및 backend-evidence/만.

## 6. 구현
현구조를 지키고 라우터는 HTTP만·환경라우팅서비스에서 외부전달/응답검증. 기존오류핸들러 사용. 테스트는 실제 네트워크/KOS 없이 주입 HTTP더블로 일반/데모/웹/dev/다중병원·대소문자·비활성·잘못된주소·redirect·전체timeout·4xx/5xx·wrongenv/origin·prod행0 축을 검증. 기존단위baseline을 수정전1회 측정하고 범위안변경과 비교한다.

## 7. 금지
실서버요청·DB접속/마이그레이션·Docker기동정지·포트조작·배포·서명·키열람 금지. 사용자 canonical에는읽기만. app/**와 옆세션 건드리지 않는다. 범위외 코드청소 금지. 하위워커임의발주금지.

## 8. 검증·보고
uv run pytest -q -m 'not infra' backend/tests/day/auth, uv run ruff check 변경backend경로, backend/tests/architecture 검증을 실행. infra는 코디가 나중에 기존day-local접속만으로 실행하므로 워커는기동/실env읽기하지않고 pending. backend-code-report.md에 실제명령·수치·파일·환경변수명확정·기존웹보존·보안경계·실통합pending. live preamble worker_done outcome필수. 커밋/push/PR은코디.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_35755602-37fe-4166-a552-a61eb956e9e9 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
