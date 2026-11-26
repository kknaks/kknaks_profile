# [planner] planner-fix-3 — review-doc-3 WARN 13 + 사용자 확인 U1 ~ U4 반영

너는 day `planner` 워커다. 역할 · 규칙 · 검증 · 완료 보고는 같은 폴더 `day-app-re1-spec-brief.md` 를 따르고, 대상 · 범위는 `planner-2-instructions.md`(보충 1 포함)를 그대로 잇는다(둘 다 먼저 읽어라). 작업 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`(지금 HEAD `22f7c30f` · 커밋 · push 금지).

읽을 것(같은 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/`): `review-doc-3-report.md` 전체 · `_RESUME.md` §2 의 review-doc-3 U1 · U2 ~ U4 행.

## 고칠 것

1. **W1 ~ W13 전부** — 리포트 §5 표의 「고칠 방향」대로. 행마다 처분(고침 · 파일:줄 / 그대로 + 이유). W2 는 「확인 안 됨」을 사실로 쓴 문장을 「확인 안 됨 · OQ」로 되돌리고, Android CAMERA 선언이 차트 · 채팅 카메라(image_picker)에 주는 영향을 OQ + 구현 때 확인할 인수 조건으로. W3 `sending` 고착은 상태 규칙으로 빈칸을 메운다(근거 있는 최소 규칙 · 발명이면 OQ). W4 IP 헤더는 DAY 배포의 신뢰할 프록시 기준을 따르는 규칙으로(근거 · 모르면 OQ).
2. **U1(사용자 결정)** — 외국인 여권 스캔 저장 = 신분확인 「O」 → 웹 [상담 대기] 켜짐. SPEC-007 케이스 표 · D23 · OQ-D36(닫음 + 날짜 · 사용자) · 관련 인수 조건 · SPEC-000 `identity_check` 기록 규칙을 맞춘다. 웹 예약 동작이 바뀌는 곳은 개정 머리글에 적는다.
3. **U2(기본값)** — Android 띄우기 알림 채널 이름 = 「고객 입력 요청」(cc 푸시 제목 `service/push.py:155-163`) · OQ-N22 닫음.
4. **U3(기본값)** — 같은 동작 글자 = 웹 · 앱 모두 「태블릿에 보내기」 · W5 · OQ-A83 정리.
5. **U4(기본값)** — 앱 예약 상세 JSON 에 여권번호를 싣지 않는다. 스캔 확인 화면을 열 때만 따로 읽는 경로(권한 = 스캔할 수 있는 직원 · 이름 제안). OQ-D29 닫음.
6. **U5 는 열어 둔다** — iOS 카메라 문구 여권 용도(OQ-A79)는 사용자 문구 대기. 글자를 짓지 마라.

## 검증 · 보고

lint `--strict` day 범위 0/0. 리포트 `planner-fix-3-report.md`(같은 폴더 · W1 ~ W13 · U1 ~ U4 처분표 · 바꾼 파일:줄). 완료 보고 = dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입.
