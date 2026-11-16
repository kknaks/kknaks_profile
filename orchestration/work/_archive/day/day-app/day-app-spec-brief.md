
# [planner] DAY iOS 직원 앱 최종 SPEC 작성 — 시술현황·대리 수락·통역 사전·데모 환경 연결

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 대화 맥락이 없다. 이 브리프가 최종 사용자 결정이다. 다른 day-procedure-board-2 세션은 별도 워크트리에서 방 이동·차트·시작 취소 정리를 한다. 그 워크트리와 산출물을 수정하지 마라. 현재 태스크는 SPEC만. WP·코드·PR은 작성하지 않는다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec/products/day/ (SPEC-000~002 · 40-architecture/system.md · deployment.md · mobile-deployment.md 포함)` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/_RESUME.md · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/research-prototype-board.md · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/para/projects/company/day/log/2026-11-09-day-data-architecture.md §7 · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/reference/2026-11-03-cc-day(screen/procedure-board-decisions.md 포함) · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- `해당 없음` — 기존 DAY 계약과 원천 결정을 따른다. 도메인 정책을 새로 만들지 않는다.

## 2. 배경 / 무엇을 바꾸나

사용자는 프로토 앱의 시술현황을 조사한 뒤 DAY 기준으로 적용하는 것을 승인했다. Flutter iOS 먼저(폰·아이패드). 로그인·컬러·권한·업무 동작은 DAY 기준이며 간호사 대리 수락은 필수다. 통역에는 interpret-pwa의 외국어 매핑 사전을 적용한다. 기능을 줄여 앱 심사를 빨리 통과하는 목표를 유지하되 이미 승인한 기능을 임의로 빼지 않는다.

사용자는 Apple 등록값·서명·TestFlight·서버 설정과 연동 준비는 직접 하므로 코드부터 준비하라고 했다. 설정 미완료를 앱 구현 착수 조건으로 걸지 않는다. 단 API 계약과 서버 구현 유무, 앱 구현과 통합 검증의 완료 조건은 구분해야 한다.

최종 환경 결정: 정식 prod 앱 하나에서 데모 계정으로 로그인하면 dev 환경, 일반 실제 계정이면 prod로 연결한다. 백엔드 로그인에서 데모 계정을 판별해 dev에서 인증하고, 앱에 연결할 API 주소와 해당 환경 세션을 전달하는 방향에 사용자 동의했다. 같은 바이너리를 심사·배포에 사용하고 심사관은 운영 데이터를 조작하지 않아야 한다. HTTPS env/JSON 원격설정 배포 방식, 심사 뒤 env 변경·재빌드 방식은 폐기. 이 기능을 위한 백엔드 로그인 변경은 기존 app/만 범위의 명시적 예외로 사용자 승인됐다. 아직 구현되지 않았으므로 현행 기능처럼 쓰지 않는다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

확정 원천: DAY-SPEC-001 로그인(이메일·비밀번호·client=app, signed_in/choose_hospital, Bearer·병원 선택·/me·로그아웃), DAY-SPEC-002의 JSON 스냅샷·SSE·API와 현재 dev 구현. 주의: 조사 보고서의 “스냅샷/스트림 계약이 없다”는 주장은 부정확하다. SPEC-002 §3에 모양과 SSE가 있고 backend/day/routers/api/board.py에 구현돼 있다. 그대로 재사용하되 불일치는 사실대로 식별해 고친다. UUID를 프로토 정수 ID로 오해하지 않는다. 앱이 can*·pickable·권한 규칙을 재계산하지 않는다.

새 환경 연결 계약을 SPEC-001 및 앱 SPEC에 한 원천으로 정의한다: 로그인 이전 고정 진입점, 서버가 관리하는 데모 계정 식별과 실제 비밀번호 인증, 인증 전·후 환경 연결, 병원 여러 개 선택 중의 pending_token·API 대상 유지, token과 API 대상의 함께 저장/복원/삭제, 로그인 재시도와 만료, SSE·HTTP·통역·푸시 등록까지 같은 환경, dev 장애 시 prod로 우회 금지, dev/prod 토큰 혼용 금지. 클라이언트가 임의 헤더로 데모 권한을 얻지 않게 한다. 응답 필드와 오류를 실제 구현 가능한 수준으로 명시하되 새 도메인 정책·실계정 값·비밀은 만들지 않는다. 단일 서버 프로세스의 APP_ENV/DB_SCHEMA 전역 교체가 아니다. 환경별 기존 Azure 서버·DB 스키마 분리는 유지한다. 공식 심사 안내에 데모 계정이 테스트 데이터로 같은 기능을 사용한다는 것을 명시하는 방향으로 둔다(심사 기능 은폐·축소 금지).

프로토의 간호사 수락 불가/코디·상담 수락 가능은 DAY와 반대다. DAY 권한 표를 따르고 간호사는 의사를 골라 대리 수락, 의사 본인은 본인 수락. 서버 판정이 정본. 시작 취소 버튼 유지·KOS에 쓰지 않는 동작은 옆 세션 담당.

통역 원천: profile para/projects/summer-star/interpret-pwa/README.md → 20-spec/spec-001-interpret-pwa.md §4 및 코드 /Users/kknaks/git/toy_pr2/interpret-pwa origin/main:back/seed/glossary.json(version 2026-10-27.6, 170개 용어, en/ja/zh/zh-Hant/th/vi/yue), back/app/service/glossary.py·service/interpret/. 한국어 대표명·별칭↔현지명·별칭 양방향 맵. 파일 체크아웃에 없으면 git show origin/main:<path>로 읽기. 읽기 전용. 사전 메뉴·편집 화면은 요청하지 않았다. 기존 서버 컨텍스트 사용 방식과 7언어·대만/홍콩 구분을 확인한다. 값을 새로 번역하지 않는다.

푸시 사용자 기준: 로그인 시 사용자+APNs 토큰 연결, 로그아웃 시 연결 해제. 별도 기기 등록 화면·사용자 절차를 만들지 않는다. App ID/환경/APNs production-sandbox 구분은 mobile-deployment가 정본. 토큰 교체·여러 설치·권한 거부·네이티브 수락과 세션 환경을 계약에 명시한다. 현재 dev에 통역·기기 등록/푸시 발송 API는 없다. 기존 구현과 제안 계약·사용자 담당 서버 연동을 구분하고, 구현 필요분은 명시된 의존성 표로 남긴다. 이번 작업이 통역/푸시 서버 전체를 구현한다고 임의로 확장하지 않는다.

방 이동·차트·테스트 시드는 day-procedure-board-2의 SPEC·머지 이후 소비. 이 태스크에서 그 API를 발명하지 않는다. 통역·푸시 의존성과 달리 시술현황 기본 조작은 현재 dev API로 구현 가능하다.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app/AGENTS.md · backend/day/{routers/api/auth.py,routers/api/board.py,schemas/auth.py,session.py,services/auth.py,services/sessions.py,dtos/board.py} · backend/day/styles/ · /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/lib/ · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` — 현재 API/응답·권한·세션·DAY 테마와 프로토 화면을 파일 근거로 대조한다. 코드 모두 읽기 전용.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/20-spec/spec-003-mobile-app.md`(이 번호 충돌이면 먼저 확인해 다음 번호를 선택)
- `products/day/20-spec/spec-001-login-session.md`(환경 연결·로그인 계약 변경만)
- `products/day/30-work.md`의 Spec Coverage에 `DAY-SPEC-003 | — (WP · Delivery Issue 미발주) | proposed` 행 한 줄만 추가 가능(형식은 기존 표 기준). WP 생성 아님.
- `products/day/20-spec.md` · `products/day/10-decision.md`(이번 결정·미결만) · `products/day/40-architecture/mobile-deployment.md`(이번 결정과 정합만)
- 보고서 1개: /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/planner-spec-report.md
- 새 baseline이 레포 규약상 필수면 products/day/00-baseline/ 아래 기존 양식으로 사용자 결정 근거만 정리 가능. log.md는 레포 규약대로(머지 전 로그를 완료로 쓰지 않는다).

## 6. 구현 단계

1. 레포 AGENTS.md가 지시한 context/manifest.yaml·index.md·current-state.md, rules/document-pipeline.md·delivery-workflow.md·design/llms.md, 제품 README·20-spec.md·30-work.md를 읽는다.
2. 관련 SPEC과 실제 dev API를 직접 대조한다. 사용자 승인 범위를 앱 SPEC 초안으로 정리한다. 목록·필터·룸 상세·마취·호출/재호출·본인/대리 수락·시작/종료/취소·귀가 대기·SSE·푸시·통역/사전·폰/아이패드까지 누락 없이 분류한다. 프로토와 DAY가 다른 곳은 DAY 결정을 우선한다.
3. 로그인 환경 연결 계약을 본문/API/케이스/인수조건까지 작성한다. 기존 SPEC-001의 병원 선택·세션을 깨뜨리지 않는다. 서버 지원 누락은 실패 처리·의존성·인수조건을 구분해 기록한다. 모르는 정책을 닫힌 것으로 만들지 않는다.
4. UI는 프로토의 모바일 배치를 참고하고 DAY의 확정 브랜드·medikit 컬러와 원천 문구를 적용한다. 새 화면 문구를 창작하지 않는다. 기존 DAY 웹 호출 팝오버와 폰 바텀 시트 등 플랫폼 배치 차이는 근거 있는 적응으로 명시하고 문구/업무규칙은 유지한다. 레이아웃·문구 근거가 없으면 정확한 미결 항목과 영향만 보고한다.
5. 인수조건에 읽기 전용 직무·대리 수락·데모/일반 로그인·여러 병원·앱 재실행·만료·SSE·오프라인/재연결·이중탭·KOS 반영 중/실패·폰/아이패드·통역 사전 적용·푸시 환경 격리를 넣는다. 테스트 더블과 실연동 검증을 구분한다.
6. 앱 구현에 필요한 SPEC만 이번 단계에서 작성한다. 초안 종료 즉시 코디가 reviewer_doc을 발주한다. SPEC 리뷰 통과 전 WP/Delivery나 코드를 시작하지 않는다. 이후 WP는 mediness의 신규 실행원장(Delivery Issue) 규약을 따를 예정이며 기존 Legacy WP를 임의 생성하지 않는다. WP 작성은 이번 태스크 아님.
7. lint-pipeline --strict를 1회 실행하고 DAY 에러와 타제품 기존 이슈를 분리한다. 실제 변경 파일·API 변경표·미결·서버 의존성 표를 지정 보고서에 남긴다.

## 7. 범위 제약 — 하지 말 것

- 코드·배포·DB·Azure·기기·시뮬레이터 조작 금지. 실제 자격증명 읽기/출력 금지. Apple 계정/식별자 등록 금지.
- 커밋·push·PR·외부 메시지·GitHub Issue 생성 금지(현재 SPEC 단계).
- 제품 정책/문구/외국어 번역/미확정 API를 기존 사실처럼 발명하지 않는다. 설치값 미확정을 이유로 SPEC 진행을 멈추지 않는다.
- products/day/30-work.md는 Spec Coverage에 DAY-SPEC-003 미발주 행 한 줄 추가만 허용(코디 후속 지시). 실행계획/WP 본문 생성은 금지. 30-work/ 수정 금지. 옆 세션 SPEC-002·SPEC-000 소유 변경 금지(필요 변경은 보고).
- 서명·TestFlight는 사용자 몫, 코드 PR 하나→dev, 머지는 사용자가 말할 때.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_6acba11d-0262-431b-aea2-37a4e7366b4b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
