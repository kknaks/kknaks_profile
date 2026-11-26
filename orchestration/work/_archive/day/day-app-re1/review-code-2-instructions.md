# [reviewer] review-code-2 — WORK-002 구현 검수(backend+web #287 · mobile #288)

너는 day `reviewer` 워커다. 역할 문서 경로 · allowed_paths(read-only · 리포트 1개) · 판정 형식 · 완료 보고는 같은 폴더 `day-app-re1-review-brief.md`(WORK-001 판)를 따른다(먼저 읽어라 — 거기 대상 · 계약 문장은 아래로 바꿔 읽는다).

대상 = `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` 커밋 **`fb08fe4e`**(= `git diff 96036397..fb08fe4e` · 119 파일). 빌드 · 테스트 실행은 해도 되지만 로컬 스택 · KOS · 시뮬레이터 실행 금지(실물 = 코디 몫). 픽셀 · 간격은 FAIL 로 잡지 마라.

## SSOT

- 계약: `delivery-2-report.md` §5 B 상세판 · Issue CENTURION_DAY#287 · #288(읽기만)
- SPEC `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec/products/day/20-spec/`(HEAD `a018f4fa`): spec-003 ㉒ · 007 고침 5 · 006 ⑭ · 005 · 000
- 결정 `_RESUME.md` §2 WORK-002 행 전부 · 워커 보고 `be-2-report.md`(§0 계약 차이) · `app-2-report.md`(§5 애매했던 곳 · §6 비운 글자)

## 볼 것(이 순서로 · 행마다 PASS / WARN / FAIL + 파일:줄)

1. **backend ↔ app 계약 맞물림** — 앱이 부르는 경로 · 칸 이름(camel) · 상태 값 · 오류 코드 · SSE 이벤트 · 푸시 본문(Android data · iOS APNs 커스텀 칸)이 backend 실제 코드와 한 글자씩 맞나. be-2 §0 계약 차이(`crm_status` · `customer_not_linked` · `display_closed` 등)를 앱이 따라갔나
2. **결정 위반** — 앱 상세 쓰기 0(버튼 셋만) · 기기 하나로만(같은 계정 다른 기기에 새지 않음) · 문진 DAY 먼저 → KOS · 실패여도 남음 · `sending` 고착 · [다시 보내기] · 외국인 스캔 = 신분확인 → [상담 대기] · [시술 대기] · 여권번호 상세 JSON 에 없음 · 공용 코디 계정 판정 · 「태블릿에 보내기」 글자 · 웹과 닮게
3. **보안** — 공개 API · `/q` 페이지: 토큰 헤더만 · 수명 · 1회 · 속도 제한(Redis) · IP = ext_peer 규칙 · no-store · no-referrer · 응답 허용 키 · 직원 인증을 비켜 가는 다른 경로 0 · 닫기 = canceled 만 · 기기 하나 대상 검사(남의 병원 · 남의 기기) · 여권 사진 · 문진 답 로그 · 토스트 노출 0
4. **조용히 통과하는 자리** — KOS 실패 · 15초 넘김 · 푸시 실패 · SSE 끊김 · 손 입력 / MRZ 체크숫자 · Android 카메라 권한 거절 · CAMERA 선언이 차트 · 채팅 카메라에 준 영향(OQ-A91)
5. **지은 글자** — 화면 · 문진 6언어 · 알림 글자가 SPEC · cc 원천 · 웹 템플릿에 있는 것만인가(app-2 §6 · be-2 처분 대조)
6. migration 0029 up/down · 계층 규약(router → service → repository · ORM 이 repository 를 넘지 않음) · 새 의존성(segno · CameraX · ML Kit · ZXing) 이유 · 라이선스

## 보고

리포트 `review-code-2-report.md`(같은 폴더) — 판정 PASS / WARN / FAIL · 지적마다 파일:줄 + 재현 / 근거 + 고칠 방향 · backend / app 어느 워커 몫인지. 완료 보고 = dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입(subject 「reviewer 완료: review-code-2」).
