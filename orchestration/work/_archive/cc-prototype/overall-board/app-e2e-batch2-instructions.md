# 앱 실기기 E2E batch 2 수정 (코디 · 2026-10-28 · 사용자 「응 고쳐」)

원천 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-e2e-feedback-batch2.md`(#1 ~ #4). 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — **새 브랜치 `kknaksss/overall-board-4`**(origin/main `333f30f` = 운영 배포본 · 코디가 만들어 체크아웃함). 커밋 · push 금지 · 사용자 포트 금지 · 끝나면 보고서에 「E2E batch 2」 절 + 두 명령(코디 `term_678ac61d-2472-4a9b-ba73-61883337b957`).

## backend (`procedure/back/**`)
- **#1 아이폰 2대**: 운영 코디 계정 기기 행 8 · 9 둘 다 `install_id` 없음. 규칙: 어떤 계정에 installId 있는 행이 생기면 **그 계정의 installId 없는 옛 행(같은 kind)은 targets 에서 뺀다**(지우진 않음 · 푸시 대상에서도 뺌). 등록 때 `installId` 와 함께 온 토큰이 옛 행(installId 없음)의 토큰과 같으면 그 행에 installId 를 붙인다(새 행 안 만듦). 시험
- **띄우기 푸시 건너뜀 위험**(mobile batch 1 보고): hub 가 죽은 연결을 ping 전까지 online 으로 봐서 잠긴 · 뒤 폰에 푸시를 건너뛴다 → **display 는 SSE 와 푸시를 둘 다 보낸다**(앱이 requestId 로 한 번만 연다 — batch 1 W1). 시험
- **#3 짝**: 기기 이름이 없으면 등록 때 앱이 보내는 기종 이름(`name`)을 그대로 쓴다 — back 변경 필요 없으면 「없음」

## mobile (`procedure/app/**`)
- **#3 이름 입력 창 뺀다**(사용자 「유저 불편하게」): 첫 로그인 창 제거 · 기본 이름 = **기종 이름 자동**(`utsname.machine` 모델 코드 → 「iPhone 15 Pro」 · 「iPad Pro 11-inch」 표 — 모르는 코드면 「iPhone」/「iPad」 + 모델 코드) · 설정에서 바꾸기는 그대로 · 이미 이름 넣은 기기는 그대로
- **#4 여권 자동 촬영 안 됨**: ① MRZ 문자 보정(OCR 오인식 `«`/`K`/공백 → `<` · 숫자 칸 `O→0` · `I→1` · `S→5` · `B→8` 등 칸 종류별) 뒤 검사 숫자 ② **같은 판독이 연속 2 프레임**이면 확정 · 검사 숫자는 여권번호 · 생년월일 · 만료일 셋이 맞으면 통과(합성 검사 숫자 실패는 허용) ③ **[촬영] 버튼 항상** — 누르면 그 사진으로 MRZ 다시 인식 → 실패면 손 입력 ④ 화면 상태 글자 「판독 줄 찾는 중 / 두 줄 읽음 / 확인 중」 ⑤ 틀 영역 ↔ 영상 좌표 변환(방향 · 크기 · `videoPreviewLayer.metadataOutputRectConverted`) 다시 확인 ⑥ **debug 빌드만** 인식 글자 오버레이 · 견본 MRZ 단위 시험(오인식 섞은 것 포함)
- **#2 기본 카메라 QR**: 빌드 6 의 `ccc` 스킴 그대로 — 빌드 7 에서 다시 본다(변경 없음). 단 딥링크 처리 시험이 있는지 확인
- 검증 `flutter analyze` · `flutter test`(`/Users/kknaks/fvm/versions/3.44.8/bin/flutter`)
