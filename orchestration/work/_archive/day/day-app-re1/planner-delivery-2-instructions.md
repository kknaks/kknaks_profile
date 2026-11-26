# [planner] planner-delivery-2 — WORK-002 가벼운 지적 N1 ~ N6 → WP 나누기 · Delivery Issue 발행

너는 day `planner` 워커다. 역할 · allowed_paths(`products/day/`) · 완료 보고 형식은 같은 폴더 `day-app-re1-spec-brief.md` 를 따른다. 절차 · 금지 · 파일 관례는 **`planner-delivery-1-instructions.md`(WORK-001 판)와 `delivery-1-report.md` 를 그대로** 따른다(먼저 읽어라). 이번 대상만 아래로 바꾼다.

문서 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`(HEAD `8195c0a8` · PR MediSolveAIDev/mediness#964 draft · **머지 금지**). 코드 워크트리(읽기만) `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`(HEAD `96036397` = WORK-001 코드 · 미push · WORK-002 코드는 이 위에 쌓는다).

## 1. N1 ~ N6 먼저(SPEC 한 줄씩)

`review-doc-4-report.md`(같은 폴더) N1 ~ N6 을 리포트의 고칠 방향대로 고친다 — 근거 없는 정책이면 OQ. N5 는 cc 원천대로(문진 푸시 = 「고객 입력 요청」 · 스캔 푸시 = 「여권 스캔 요청」 — 채널 이름 「고객 입력 요청」 결정은 그대로 두고 출처만 바로잡음). lint day 0/0 → **커밋**(push 는 3 에서 같이).

## 2. WP 나누기 · Delivery

SPEC = DAY-SPEC-003 개정 ㉒ · 007 고침 5 · 006 ⑭ · 005 · 004 · 000(+ fix-3 보충 · N1 ~ N6). 결정 SoT = `_RESUME.md` §2 WORK-002 행 전부.

- 병렬이 되게 나눈다(의존은 실제 순서만). 기대 모양(근거가 다르면 고치고 이유를 적어라):
  - **BE**: 앱 `/api` 예약 목록 · 상세(읽기 · 여권번호 뺌) · 여권 읽기 경로 · 기기 목록 · 띄우기 요청 / 메우기 / 닫기 / 상태 · 기기 하나로 가는 SSE · 푸시(APNs · FCM) · 여권 스캔 저장(KOS 고객 수정 · 사진 KOS + DAY · `identity_check` · 외국인 신분확인 → [상담 대기] · [시술 대기]) · 문진 공개 API · 공개 Jinja 페이지(6언어) · KOS 문진 경로 · `questionnaire_history` 저장 → KOS · 상태 · [다시 보내기] · migration · 테스트
  - **WEB**(같은 BE 레포 Jinja · BE 와 나눌지 합칠지 네가 근거로 정함): 웹 예약 상세 [문진 QR] · [여권 스캔] 켬 · 「태블릿에 보내기」 기기 고르기 · 진행 표시 · 초진 문진 · 건강정보 값
  - **APP**: 예약현황 탭(폰 목록 · 태블릿 시간표 · 웹과 닮게) · 상세(읽기 전용) · 문진 QR 화면 · 여권 스캔(iOS Vision 채널 · **Android CameraX + ML Kit 번들 채널** · MRZ 파서 · 손 입력) · 태블릿 받기(실시간 · 알림 · 메우기) · 「이 기기 이름」 · 권한(Android CAMERA · iOS 문구는 OQ-A79 열린 채 — 지금 문구 유지)
  - 각 WP: 범위 · **WP 사이 계약**(경로 · 요청 · 응답 · 오류 · 이벤트 — SPEC 인용) · 완료 조건(BE = 로컬 KOS 데모 지점 실물 호출 1회 — 고객 수정 · 사진 · 문진 제출 각 1 / APP = 시뮬레이터에서 로컬 BE 로 QR · 손 입력 스캔 · 받기 1회 + Android 에뮬레이터 빌드 · 카메라 스캔 실기기는 사용자 E2E) · migration · 되돌리기
- **Delivery 발행**: `mediness start-delivery --mediness-repo <문서 워크트리> --code-repo <코드 워크트리> --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. baseline = 1 의 커밋(머지 전 · spec-baseline:pending). 막히면 우회하지 말고 출력 그대로 보고. **승인 receipt 적용 금지**(사용자 몫). json 은 같은 폴더 `delivery/`(이름에 `-2` · WORK-001 파일 덮어쓰기 금지).

## 3. 마무리

`30-work.md` Spec Coverage 행 · `log.md` 한 줄 → 커밋 · **push 해서 PR #964 에 얹어라**(lint 0 error).

## 보고

`delivery-2-report.md`(같은 폴더) — N1 ~ N6 처분 · Issue 번호 · WP 표 · WP 사이 계약 전문 · baseline · 막힌 것. 완료 보고 = dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입(subject 「planner 완료: Delivery 2」).
