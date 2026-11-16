# [planner] 마감 — 스펙 사실 반영(spec-sync) + Delivery #251 마감 sync

같은 역할. 맥락: 이 폴더(`/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`)의 `_RESUME.md` §2 결정 표 · §5 이력 · `app-1~6-report.md` · `review-code-1~4-report.md` · `e2e-feedback.md` · `spec-3/4-report.md` · `delivery-v2-report.md`.

## 상태

- 스펙 #940 머지(`855bab4f`) 뒤 사실이 많이 바뀌었다. 코드 PR **CENTURION_DAY#253 squash 머지 `4f8316a7`**(dev) — AND-1~7 + F1.
- Play: DAY Dev 내부 테스트 vc3 · **정식 DAY(`day.medisolveai` · `DAY` · prod) 비공개 테스트 vc1 → vc3 출시 · 프로덕션 vc3 심사 중**(2026-11-15 제출 · 공개 출시로 사용자 결정 「이제 출시 준비도 하면 되나?」). 사용자 실기기(Z Fold3) 확인 끝(통역 음성 입력 포함 · F1 해소).
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec` — `git fetch origin && git checkout -B kknaksss/android-app-close origin/main` 으로 새 브랜치(이름은 그대로 써라). allowed_paths `products/day/`. **커밋 · push · PR 금지**(코디가 한다).

## 할 것

### A. 스펙 사실 반영 — 전수조사로
`grep -rn -i "android\|play\|aab\|keystore\|업로드 키\|day.medisolveai\|미결\|\[미결\]" products/day/` 로 **쓰는 곳 전부**를 센 뒤, 아래 사실과 다른 줄만 고친다. 표(파일:줄 · 전 · 후 · 근거)를 리포트에.
1. **정식 Android 앱** = `day.medisolveai` · `DAY` · prod 서버 · Play 비공개 테스트 → **프로덕션(공개) 출시 진행**(M-3 · M-4 · M-17 · §7 · §9 · §12 의 [미결] 중 닫힌 것). iOS 정식과 같은 「정식 빌드 = prod · 데모 계정 → dev」 규칙.
2. 업로드 키 = dev · 정식 **공유** · 로컬 `~/.config/day/android/`(백업 위치는 [미결] 그대로면 그대로). 서비스 계정 = Play 업로드 전용 서비스 계정(이름은 쓰지 말고 「Play 업로드 전용 서비스 계정 · 키는 로컬」) · 조직 정책상 키 생성은 막혀 있어 프로젝트 한정 재정의로 한 번 발급(운영 메모 수준 · 값 X).
3. Android **id · 이름 · 서명 주입 3단**(`-P` > `identity.local.properties` > placeholder) · release 는 업로드 키 없으면 빌드가 멈춤.
4. **세션 저장** = Android Keystore AES-256-GCM + 앱 전용 prefs · 단일 직렬 실행기 · 백업 · 기기 이전 제외.
5. minSdk 24 · targetSdk/compileSdk 36.
6. **F1** — Android(edge-to-edge) 태블릿 칸 · 바닥 목록 끝은 하단 시스템 영역만큼 비움 · iOS 불변. 어느 SPEC 의 레이아웃 절에 한 줄로(새 [확정] 남발 금지 · 사실만).
7. **업로드 = `app/android/play_upload.py`**(Play Developer API · dev→internal · 정식→alpha 만 · 프로덕션은 Console 손 단계). 첫 AAB 는 손 업로드.
8. A-48(로컬 에뮬레이터) · A-49(Play 내부 테스트) 결과 반영 — 통역 음성 입력은 실기기에서 확인됨.
9. Play 콘텐츠 선언(데이터 보안 · 사진/동영상 권한 「채팅 최근 사진 줄」 신고 통과 · 18+ · 광고 없음)은 mobile-deployment 의 사용자 손 단계 절에 「했다」로(값 X).
- 하지 말 것: 계정 이메일 · 키 · 서비스 계정 이메일 · 개발자 id 값. 화면 문구 발명. FCM · 동영상 보내기 · KOS 세션 14시간 문제(별도 작업)는 [미결]/범위 밖 그대로.

### B. Delivery #251 마감 sync — mediness #936 과 같은 꼴
- `gh pr view 936 -R MediSolveAIDev/mediness` 를 읽고 같은 방식으로: `products/day/30-work.md` Delivery 대시보드 · Spec Coverage 에 #251 행 · `log.md` 한 행.
- review-delivery 판단: #253 이 Delivery v2 의 Target Delta · Acceptance(A1~A6)를 지키는지 대조 표(A 마다 근거 = 리포트 · 실물 · 사용자 확인). 범위 밖으로 커진 것(F1 · 정식 앱 · 프로덕션)은 「Delivery 뒤 사용자 결정으로 늘어남」으로 정직하게 적는다.
- Issue #251 에 남길 마감 댓글 초안을 리포트에(게시는 코디).

### C. lint
`python3 scripts/lint-pipeline.py --strict` → products/day ERROR 0 · WARN 수.

## 산출물
`spec-close-report.md`(같은 폴더) — A 전수 표 · B 대조 표 · 댓글 초안 · 변경 파일 · lint · PR 제목/본문 초안(templates 꼴). 완료 보고는 1회차 브리프 §9 두 명령(새 preamble 값).
