# [backend] be-2 — WORK-002 backend+web — Delivery CENTURION_DAY#287

너는 day `backend` 워커다. 역할 문서 경로 · 워크트리 공유 규칙 · §8 검증 · §9 완료 보고는 같은 폴더 `day-app-re1-be-brief.md`(WORK-001 판)를 따른다(먼저 읽어라). **범위 · allowed_paths · 금지는 아래가 이긴다.**

작업 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`(HEAD `96036397` = WORK-001 코드 · 그 위에 쌓는다). mobile 워커가 같은 워크트리의 `app/` 을 동시에 고친다 — 너는 `app/` 금지. git stash · checkout · reset · 커밋 금지.

## 1. SSOT

- Delivery Issue **CENTURION_DAY#287**(`gh issue view 287 -R MediSolveAIDev/CENTURION_DAY`) — WP 범위 · 계약(압축판)
- `delivery-2-report.md` §4 · **§5 B 상세판 계약 전문**(같은 폴더) — Issue 와 같은 뜻 · 길면 이쪽
- SPEC(문서 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` HEAD `a018f4fa` · `products/day/20-spec/`): **spec-007**(고침 5 · 띄우기 · 여권 스캔 저장 · 고객 문진 공개 웹 / API) · **spec-006**(⑭ 앱 목록 · 스트림 JSON) · **spec-005**(띄우기 푸시 · 기기 하나) · **spec-000**(migration 칸) · spec-003 ㉒(앱이 부르는 쪽 · 기기 이름)
- 결정 SoT `_RESUME.md` §2 WORK-002 행 전부 · 원천 cc `/Users/kknaks/git/toy_pr2/cc-prototype` origin/main(`git show` 만 — 백 `procedure/back/app/service/{display,questionnaire,passport_scan,id_photo,push}.py` · `api/{display,public_questionnaire}.py` · 웹 `procedure/front/components/q/` · 6언어 `lib/q/text.ts`) · research-2/3 리포트(파일:줄)

## 2. allowed_paths

- `backend/` 전부(이번엔 **웹 = 이 WP** — `routers/`(api 포함) · `templates/` · `static/` · `styles/` · migration 포함)
- `pyproject.toml` · `uv.lock`(꼭 필요한 의존성만 · 리포트에 이유)
- `deploy/Caddyfile` 류(공개 경로 · 헤더가 필요할 때만 · 리포트에 이유)

## 3. 구현

#287 범위 전부 — 앱 예약 목록 · 스트림 · 상세(여권번호 뺌) · 여권 확인 값 읽기 · 기기 목록 · 띄우기 만들기 / 메우기 / 닫기(클라이언트 = canceled 만) / 상태 · **기기 하나로 가는** SSE `display` · 푸시(APNs + FCM · 채널 「고객 입력 요청」 · 스캔 제목 「여권 스캔 요청」) · 여권 스캔 저장(KOS 고객 수정 = 그 기기 로그인 직원 토큰 · 사진 KOS(시술전후 내부 경로 · 분류 「여권」) + DAY 저장소 · `identity_check` · 외국인 → [상담 대기] · [시술 대기]) · kos-retry · 고객 문진 공개 Jinja 페이지(6언어 = cc 글자) · 공개 API(cc 보안 규칙 · IP = ext_peer 규칙) · KOS 문진 경로 · `questionnaire_history` DAY 먼저 → KOS · 상태 · `sending` 고착 규칙 · [다시 보내기] · 기기 이름 저장 · migration 1(0028 뒤 · up/down) · **웹** 예약 상세 [문진 QR] · [여권 스캔] 켬 · 「태블릿에 보내기」 기기 고르기 · 진행 줄 · 초진 문진 · 건강정보 값.

- 라우터는 얇게 · 서비스 하나를 웹 · 앱 · 공개가 같이 부른다(복사 금지) · 계층 규약(router → service → repository)
- 화면 · 문진 글자는 SPEC · cc 원천에 있는 것만 — 없으면 비우고 리포트에
- 테스트: 경로 계약(성공 · 오류 코드 · 권한 · Bearer / 쿠키 · 공개 경로 보안 · 기기 하나 닿기) · 스캔 저장 · 문진 순서 · 웹 Jinja 회귀 — KOS 는 기존 테스트처럼 가짜

## 4. 금지

KOS 실물 호출 · 로컬 스택 띄우기 · `deploy/*.env` 값 · 사용자 포트 / 프로세스(실물 e2e A6 = 코디 몫) · `app/` · 결정에 없는 업무 규칙 · 커밋 · push · PR · Issue 라벨 / 댓글.

## 5. 보고

`be-2-report.md`(같은 폴더) — 변경 파일 · 경로 표(메서드 · 경로 · 인증 · 응답 · 오류) · migration · 테스트 수치 · **계약 차이**(리포트 맨 위 · mobile 이 볼 것) · 코디가 실물(A6 — 고객 수정 · 사진 · 문진 제출 각 1)로 확인할 순서. 완료 보고 = dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입(subject 「backend 완료: be-2」).
