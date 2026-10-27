# 작업 요약 — interpret-pwa-poc (interpret-pwa)

기간: `2026-10-26` ~ `2026-10-27`
결과: 머지 · 배포 완료(2026-10-26 첫 배포 · 8차까지, https://tongky.medisolveai.xyz) — 코드 `kknaksss/interpret-pwa#1` ~ `#8` · infra `MediSolveAIDev/k8s_infra_mac#25` ~ `#30` · `#32` · `#33` · 문서 `kknaks/kknaks_profile#106`

## 1. 무엇을 했나

ccc(cc-prototype)의 통역이 피부과 시술명을 직역한다(중국어에서 「부비동과 심방」 같은 오역)는 문제에서 출발해, 통역만 떼어 **새 레포의 실시간 통역 PWA 「통키(Tongky)」**를 세웠다. 상담사와 외국인 손님이 폰 하나를 가운데 두고 쓰는 화면(외국어 영역 180° · 원 상태 8개 · 말풍선 · 자동 스크롤)이고, back 이 Soniox STT(two_way) · TTS 두 연결을 WebSocket 으로 중계한다.
용어 보정은 처음엔 Procedure Hub 용어집을 Soniox `context`(`translation_terms`)로 넣었고, 폰 테스트에서 대만명 · 써마지 단독 · 괄호 병기가 막히자 **우리 시드 사전(정규화 · 157 term × 7개 언어)**으로 옮긴 뒤 웹 조사로 대만 현지명 77개를 채웠다. 사용자가 로컬 E2E 를 건너뛰고 폰으로 바로 테스트해서, 배포 → 폰 피드백 → 수정 → 재배포를 하루에 여덟 번 돌았다. 마지막에 외부로는 통역만 오가게(용어집 API 삭제 · 응답 최소화) 닫았다.

## 2. 적용한 기술·개념

- **Soniox `context` 로 용어 보정 — 한도는 실측으로** [[transcript-term-correction]] — 시술명을 정방향(ko → 현지명) · 역방향(현지명 · 별칭 → ko) `translation_terms` 로 넣는다
  - 왜 이걸 골랐나: 번역 뒤에 우리가 치환하면 문장이 어색해지고 TTS 와 어긋난다. Soniox 번역 단계에 용어를 주는 게 자막 · 음성을 한 번에 맞춘다. 실물: 용어집 넣음 en · zh 3/3 vs 없음 1/3 · 0/3
  - 무엇이 어려웠나: 문서 한도는 「8,000토큰(약 1만 자)」뿐이라 역방향을 넣자(15 ~ 18k자) 「terms 를 다 빼도 넘는다」는 계산이 나왔다 → 문서값 대신 **같은 언어 짝을 덧붙이며 이분 탐색**으로 실제 한도를 쟀다(ja 20,925 ~ 25,922자 통과 · 거절은 오디오 없이 0.41 ~ 0.46초) → 기본값 = 가장 작은 통과치 × 0.9(18,832 → 시드 뒤 20,251). 줄이기 순서는 `terms` → 역방향 별칭 → 역방향 기본 → 정방향 별칭, 정방향 기본은 끝까지 · 거절되면 정방향만으로 1회 재연결
  - 근거: `back/app/service/glossary.py` · `back/app/config.py` · `live-check-2026-10-26.json` · `live-check-wp6-2026-10-26.json` · DEC-001 D-05 · D-18 · SPEC-001 §4.4
- **외부 원천 대신 우리 시드 사전 · 정규화** [[seed-data]] — 「영문（현지명）」 한 칸을 term(ko · 별칭) × 언어별 현지명 · 별칭 · 출처 · 검수로 나눔
  - 왜 이걸 골랐나: Procedure Hub 는 대만 열이 없고 써마지는 「써마지FLX」만, zh 칸은 「Thermage FLX（美版热玛吉FLX）」라 TTS 가 괄호를 빼면 영어만 읽혔다. 원천 수정을 기다리는 대신 첫 1회만 가져오고 git PR 로 고치는 시드로(DB · 편집 화면은 PoC 에 과함)
  - 무엇이 어려웠나: 괄호 분해 모양이 다섯 갈래(설명 괄호 60칸은 `reviewed:false` + `raw` 보존) · 같은 ko 행 합치기 · 시드가 깨지면 기동 실패(우리 파일이라 시험이 게이트)
  - 근거: `back/seed/glossary.json` · `back/scripts/import_glossary.py` · `back/tests/test_seed.py` · DEC-001 D-33 · 코드 #4
- **OpenCC 변환 단계 — 매핑은 간체, 출력만 번체** [[transcript-term-correction]] — Soniox 는 중국어를 간체로만 낸다
  - 왜: 대만 손님 발화도 간체로 받아써지므로 매핑(context)은 간체로, 자막 · 화면만 번체로. TTS 는 간체(번체는 발음이 깨짐 — ccc 실물)
  - 무엇이 어려웠나: 대만식 표현까지 바꿔 준다는 `s2twp` 를 넣었다가(D-32) 조사에서 「鐳射」는 홍콩 표기 · 대만은 「雷射」, 「导入 → 匯入」 같은 오변환이 드러나 `s2tw` + 激光 → 雷射 하나로 되돌렸다(D-35). 기기 현지 별명(美國音波 · 鳳凰電波)은 글자 변환이 아니라 단어가 달라 어떤 라이브러리로도 안 나온다 → 데이터로
  - 근거: `back/app/service/interpret/langs.py` · `chinese.py` · `research-tw-names-report.md` · DEC-001 D-17 · D-32 · D-35
- **Soniox TTS WebSocket keepalive 형식** [[websocket-relay]] — 멈춤 중 40초 idle 끊김을 막는 keepalive
  - 무엇이 어려웠나: 운영에서 통역이 50초 만에 `invalid_request` 로 끊겼다. 로그엔 오류 종류만 있어 원인을 못 봤다 → 채널 · 메시지 · 상태를 남기게 하고 재현. TTS 에 `{}` 를 보내고 있었고 Soniox 는 `Missing stream_id` 오류를 소켓에 쌓아 뒀다가 **다음 발화 TTS 에서** 터뜨렸다(TTS 뒤 20초 이상 쉬면 발생 · 언어 무관). 공식 형식 `{"keep_alive": true}` · 다른 stream_id 오류는 경고만
  - 근거: `back/app/service/interpret/soniox.py` · `session.py` · `d35-be-report.md` 장애 절 · 코드 #6
- **반이중 + 누르고 말하기** [[half-duplex-echo-suppression]] — TTS 재생 중 마이크 송신 0 · 주변 노래가 계속 들어오는 문제에 「누르고 말하기」 모드
  - 왜: 브라우저 noiseSuppression 은 일정한 소음만 지운다 — 노래는 말소리라 그대로 받아써졌다. 음량 문턱은 큰 음악 · 작은 목소리에 둘 다 틀린다 → 누르는 동안만 보내기(누름 = `resume` · 뗌 = `pause` → finalize). 기존 WS 메시지를 그대로 써서 back 무변경
  - 무엇이 어려웠나: 멈춤 중에도 `finalize` 로 확정된 발화의 TTS 는 나온다 → 원 상태 판정에서 「출력 중」을 「멈춤」 위로(문서 리뷰 FAIL-2) · 멈춘 뒤 남은 TTS 조각을 다음 `audio_start` 까지 버림(코드 리뷰 FAIL-1)
  - 근거: `front/lib/interpret.ts` · `front/lib/ptt.ts` · `review-doc-report.md` · `review-code-report.md` · DEC-001 D-09 · D-36
- **마주 보는 화면 — 회전은 레이아웃 한 벌 + 영역째 회전** — 외국어 영역 180° · 말풍선(보는 사람 기준 내 말 오른쪽) · 원 위 외국어 안내
  - 왜: 뒤집힘 · 바로 보기를 따로 짜면 두 모드가 어긋난다 → 바로 선 기준으로 짜고 회전만
  - 무엇이 어려웠나: medikit ComboBox 가 목록을 Popover portal 로 body 에 붙여 **회전을 못 받았다**(실기기에서 목록이 바로 선 채 펼쳐짐 · 끄는 prop 없음) → 카드 안 자체 목록. iOS Safari 는 16px 미만 입력에 포커스하면 화면을 확대 → 입력 16px(확대 잠금은 접근성 때문에 안 씀)
  - 근거: `front/components/interpret/LangSelect.tsx` · `InterpretScreen.tsx` · `app/login/page.tsx` · DEC-001 D-08 · D-24 · D-27 · D-31
- **밖으로는 통역만 — 최소 노출 · 경로 고정 시험** [[field-level-visibility]] — 사전 JSON 노출 금지
  - 왜: 데모 원탭 로그인(D-30)을 켜 두니 버튼 하나면 `/api/glossary` 로 사전 전체를 가져갈 수 있었다. `/api/health` 는 사전 버전, `/me` 는 아이디, 오류 문구는 env 이름을 흘렸다
  - 무엇을: 용어집 API · 메뉴 삭제 · health/me `{ok}` · 오류 일반 문구 4종 · docs/openapi 끔 · **허용 경로 6개를 고정하는 시험**(새 경로가 생기면 실패) · 빌드 산출물에 용어 데이터 0(grep)
  - 근거: `back/tests/test_api_surface.py` · `front/tests/minimal-exposure.test.ts` · DEC-001 D-37 · 코드 #8
- **데모 원탭 로그인 — env 스위치** [[demo-stand-in-for-integration]] — 비밀번호를 front 번들에 넣지 않고 back `INTERPRET_DEMO_LOGIN` 으로 `POST /api/auth/demo`
  - 왜: 공개 번들에 비밀번호를 넣으면 누구나 본다. 스위치면 Secret 값만 지우고 back 재시작으로 원래 로그인
  - 근거: `back/app/api/auth.py` · DEC-001 D-30
- **폴더별 이미지 빌드와 차트 태그** [[ci-cd]] — Actions 가 바뀐 폴더만 빌드
  - 무엇이 어려웠나: front 만 바뀐 배포에서 그 sha 의 back 이미지가 없어 `image.tag` 하나로는 못 올렸다 → `front.imageTag` / `back.imageTag` 오버라이드 → 둘 다 같은 sha 로 빌드된 배포(#33)에서 하나로 정리
  - 근거: `charts/interpret-pwa/values-prod.yaml` · infra #29 · #30 · #32 · #33
- **시안이 화면 정본 — Claude Design 캔버스** [[design-system]] — 1차 화면에 디자인이 하나도 안 들어갔다는 지적 뒤 designer 워커가 「Interpret PWA」 캔버스(21화면)를 만들고 사용자가 거기서 고침
  - 무엇이 어려웠나: front 브리프에 「medikit 연결 방식」만 적고 ccc 의 **세라믹 테마**(`data-product="ceramique"` · `ceramique-theme.css`)를 안 적어서 medikit 기본 파랑으로 나왔다. 시안이 front 보다 늦게 나오면 문구가 어긋남 → 시안 나온 뒤 값 맞춤을 한 번 더
  - 근거: `design/` · https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd · DEC-001 D-20 · D-21

## 3. 막혔던 것 / 사고

- **1차 화면에 디자인 누락** → 사용자 「디자인이 하나도 안들어갓잖아」 · 「세라믹 ccc 테마랑 같은 색깔」 → 원인은 front 브리프에 테마를 안 적은 것 → 시안 정본(D-20)으로 다시 세움. 다음엔 원형 기능을 옮길 때 테마 · 시안 위치를 브리프 §1 에 먼저
- **로그인 401 · 429** → 사용자가 `.env` 에 넣은 계정값이 합의값과 달랐다(코드 문제 아님) → 값을 출력하지 않고 비교해 확인 → 합의값으로 교체 · back 재시작으로 잠금 해제
- **대만어 울쎄라 · 써마지 직역(「미국 음파」 · 「봉황전파」)** → 원천 용어집에 대만 열이 없었다(간체 · 번체 문제가 아니라 단어가 다름) → 시드 · 웹 조사. 중간에 「사전 배포했다면서」 — 사전(D-33)과 대만명(D-35)을 한 말로 뭉뚱그려 답해 혼선
- **s2twp 를 근거 없이 넣었다가 되돌림** → 실측은 일반 단어만 봤고 표기 지역(홍콩 · 대만)은 안 봤다 → 조사 리포트에서 드러남 → D-35
- **운영 통역 끊김** → keepalive 형식(§2). 로그에 오류 메시지 · 채널이 없어 첫 판단이 늦었다 → 외부 서비스 오류 로그에는 처음부터 채널 · 메시지 · 상태를
- **코디 핸들이 세션 중 세 번 바뀜**(ce3ec → 855a → ce3ec → b9fdf) → 워커 완료 보고가 엉뚱한 곳으로 갈 뻔 → 브리프에 「보고 직전 `terminal list` 에서 제목으로 찾기」를 넣어 해결
- **새 워크트리 신뢰 창** → 숫자 키 · Enter 가 안 먹고 위쪽 화살표 + Enter 로 통과(메모리의 방법대로)
- **워커 세션이 끝나 있음**(planner 2회) → `dispatch --inject` 가 「no recognized agent」 → 새 터미널에 같은 task 를 다시 dispatch
- **스쿼시 머지 뒤 워크트리 브랜치** → 다음 커밋이 머지된 커밋 위에 쌓여 PR 이 꼬일 뻔 → 매번 `checkout -B <브랜치> origin/main`(트리 같음 확인) · 한 번은 `--force-with-lease`

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-26 | 새 레포 `kknaksss/interpret-pwa` · Next.js PWA + FastAPI · back 이 Soniox 중계(D-01 ~ D-03) | 사용자 「새 레포」 · ccc 원형 |
| 2026-10-26 | 언어는 시작 때 고름 · two_way(D-04 · Option A) | 사용자 「a로 가자」 |
| 2026-10-26 | 단일 계정 · 값은 env(D-06) | public 문서 레포 |
| 2026-10-26 | 화면 정본 = Claude Design 캔버스 · 통키(D-20 · D-21) | 디자인 누락 지적 |
| 2026-10-26 | 원 위 외국어 안내 · 원 축소 · 말풍선 · 자동 스크롤(D-22 ~ D-25) | 사용자 화면 피드백 |
| 2026-10-26 | 배포 tongky.medisolveai.xyz · cc-prototype 방식(D-26) · 로컬 E2E 건너뜀 | 사용자 「배포해서 내 폰으로」 |
| 2026-10-26 | 중국 · 대만 별도 항목 · 초기화 · 데모 원탭 로그인 · 목록 180°(D-28 ~ D-31) | 폰 피드백 |
| 2026-10-27 | ~~대만어 출력 s2twp(D-32)~~ → s2tw + 激光→雷射(D-35, 10-27 뒤집음) | 조사: 鐳射 = 홍콩 표기 |
| 2026-10-27 | 용어집을 우리 시드로 · 정규화(D-33) | Procedure Hub 모양이 통역에 안 맞음 · 「시드로 가자 poc 니까」 |
| 2026-10-27 | 시작 오버레이 = 언어 단추(D-34) | 「탭화면 누르기 전에 언어 선택」 |
| 2026-10-27 | 누르고 말하기 모드(D-36) | 주변 노래 입력 |
| 2026-10-27 | ~~용어집 메뉴(D-13)~~ → 최소 노출 · 용어집 API 삭제(D-37, 10-27 뒤집음) | 「외부 api에 json이 노출 되면 안돼」 |

전체 결정 원장: `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`

## 5. 날짜별 로그

- `2026-10-26` 착수 — 새 레포 · config/roles · BASE-001 · DEC-001 · SPEC-001 0.1 → 0.3(문서 리뷰 FAIL 2) · back/front 1루프(pytest 123 · Soniox 실물 ①~⑦) · 코드 리뷰 FAIL 1 · 시안 캔버스 · WP6 묶음 수정 · infra 준비 · 첫 배포 · 폰 피드백 1 · 2 재배포(PR #1 · #2)
- `2026-10-27` 폰 피드백 3(목록 180° · s2twp · PR #3) · 우리 시드 사전(PR #4) · 시작 오버레이 언어 단추(PR #5) · 대만명 웹 조사 77/157 · 운영 끊김 원인(TTS keepalive) 수정 + 대만명 시드(PR #6) · 누르고 말하기(PR #7) · 최소 노출(PR #8) · 문서 PR #106

## 6. 산출물

- spec PR: https://github.com/kknaks/kknaks_profile/pull/106
- code PR: https://github.com/kknaksss/interpret-pwa/pull/1 ~ /pull/8 (main `fe8475e`)
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/25 ~ /pull/30 · /pull/32 · /pull/33
- 시안: https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd (21화면)
- 리포트: `review-doc-report.md` · `review-code-report.md` · `research-tw-names-report.md` · `live-check-2026-10-26.json` · `live-check-wp6-2026-10-26.json` · `wp*-report.md` · `fix-phone*-report.md` · `d3*-report.md` · `design-r*-report.md`

## 7. 잔여

- **사람 목소리 E2E** — 실물 확인은 합성 음성이었다. 한국어 STT 가 「신펄」 · 「울쎄라」를 반쯤 받아써 정방향 적중이 낮게 나온 표본이 있다(SPEC §10)
- **대만명 못 찾은 80개** — 한국 전용 브랜드 · 부위 보톡스 · 스킨케어 일반어. 「검수 전」 그대로 · 시드 PR 로 사람이 채움
- **모호한 중국어 구어**(超声刀 · 韩版超声刀 · 韩版热玛吉) — 일부러 안 넣었다. 실제 상담에서 어떻게 불리는지 보고 결정
- **데모 원탭 로그인 끄기** — Secret `INTERPRET_DEMO_LOGIN` 지우고 back 재시작. 켜져 있는 동안 주소만 알면 통역 사용(Soniox 과금)
- **누르고 말하기 실기기 감각** — 누름 반응 · 뗄 때 말 끝 잘림을 폰에서 확인
- **SPEC-001 0.5.0 동기** — planner 진행 중(D-35 ~ D-37 · 장애) → #106 에 포함
