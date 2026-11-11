
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
- 보고서 1개: /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/planner-policy-report.md
- 새 baseline이 레포 규약상 필수면 products/day/00-baseline/ 아래 기존 양식으로 사용자 결정 근거만 정리 가능. log.md는 레포 규약대로(머지 전 로그를 완료로 쓰지 않는다).

## 6. 이번 태스크 — 사용자 확정 정책 2건과 향후 확장 요구 반영

현재 기술 지적은 fix2까지 모두 수정됐다. 새 preamble id로만 보고한다. 수정은 기존 SPEC-003에 아래 세 가지를 반영하는 것만. WP·코드는 아직 금지. 이번 보고서는 planner-policy-report.md. 이전 보고서 보존.

1. 통역: 사용자 확정 = 시술현황에서 해당 고객 정보를 볼 수 있는 사람 모두 통역 사용 가능. U-15·WS권한·AC에서 기존 고객정보/board view 권한을 따른다고 명시하고 OQ-A15를 확정 결정으로 닫는다. 수정권한이나 별도 interpret 권한을 새로 요구하지 않는다. 서버 인증/해당 병원·고객 조회 범위는 그대로 유지.
2. 푸시: 기존 호출 대상과 동일. 모든 의사면 해당 병원 원장 목록 전체, 한 명 지정이면 그 원장. 이것을 코디가 설명했고 사용자가 “응 맞아”로 확인했다. 관리자 별도 추가·호출한 원장 자동 제외 등 새 수신자 정책을 만들지 않는다. U-14·푸시계약·AC·OQ-A17의 받는 사람 미결을 이 결정으로 닫는다. 알림 수락은 기존 본인수락·board.accept 서버 권한을 그대로 따르는 표현으로 두고 신규 정책처럼 다시 질문하지 않는다. 간호사 대리 수락과 푸시 수신 대상은 별개다.
3. 향후 사용자 요구: “나중에 코디가 상담사를 호출할 수도 있다.” 미래 확장 항목으로 보존하고 현재 의사호출·푸시 계약을 모든 직무 호출의 영구 규칙으로 일반화하지 않는다. 지금 API/데이터모델 이름을 전면 변경하거나 상담사 호출 기능을 1차에 추가하지 않는다. 미래 호출의 대상·발신 권한·수락 규칙은 그 기능 SPEC에서 정한다.
4. 사용자 원문은 profile orchestration/work/day-app/_RESUME.md 최신 결정 표. 먼저 읽고 해당 문장 근거를 남긴다. 다른 정책·UI·문구는 변경하지 않는다. SPEC-001/002·30-work.md 수정 필요 없다. SPEC-003만 수정하고 보고서1개 작성. lint와 diff --check 각1회. 수정 후 코디가 좁은 재리뷰를 한다.

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
