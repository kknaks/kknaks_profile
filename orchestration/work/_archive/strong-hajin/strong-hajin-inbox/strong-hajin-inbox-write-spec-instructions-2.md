# [writer] SPEC 추가 지시 2 — 검수 FAIL 4 · WARN 17 전부 + SPEC-006 개정 (2026-10-06)

검수 리포트 **`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-008-009.md`** 를 처음부터 끝까지 읽어라. **FAIL 4건과 WARN 17건을 하나도 빼지 말고** 고친다. 리포트 각 행의 「고칠 것」을 따르되, 아래 사용자 결정이 우선한다.

## 사용자 결정 (원장 `_RESUME.md` §2 2026-10-06 마지막 두 행)
- **F-1** → (a): 카톡 방 목록·선택은 **Mac 이 정본**. 서버는 웹 방 고르기 창을 위해 **중계만**(목록 저장 안 함 · 앱 꺼지면 시안 문구) · 서버에 남는 방 = 메시지가 올라온 방뿐 · `rooms/report` 는 저장하지 않는 중계로 · **서버는 업로드가 그 사용자의 고른 방인지 검사**(검사 근거를 앱이 보내는 서명/목록 중 무엇으로 할지 너가 계약으로 정하고 근거를 적어라)
- **W-7**: 카톡 수집은 **회사판 medi-ax** 앱에 넣는다. 개인판(Strong Hajin flavor)은 주소가 정해질 때
- **W-6 / SPEC-006 개정 수용**: 백그라운드 상주 · **메뉴 막대 아이콘** · 전체 디스크 접근 권한 · F-2 의 OAuth 외부 열기 흐름

## 기술 FAIL (리포트대로)
- **F-2** 연결 시작 = 서버가 회원에 묶인 일회용 `state` 의 동의 URL 을 JSON 으로 → 웹은 이동, 데스크톱은 `open_external` · 콜백은 쿠키가 아니라 `state` 로 회원을 찾는다 · reconnect 같은 모양 · 콜백 뒤 목적지 `AX_WEB_ORIGIN` 기준
- **F-3** HTML 메일 소독·격리 계약(서버 소독 + 샌드박스 iframe/CSP · 외부 이미지 처리 · 링크 열기)
- **F-4** §4.3·4.4·4.6 요청/응답/오류 모양 전부(페이지네이션 · 스레드 · 실시간 갱신 방식 · 카톡 업로드 · 연동 생성)

## allowed_paths (이번 판)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` · `spec-009-mac-kakao-collector.md` → v0.3.0
- **`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md`** — 개정(버전 올리고 변경 이력 · 바뀌는 불변식·AC·셸 시험 목록을 명시, I-2 · 창 하나/트레이/백그라운드 · AC-T23·T33·T47 등 리포트 W-6 의 항목 전부)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/10-decision/decision-008-external-channels.md` — **W-16 만**: D-49 를 「보존·파기 없음(사용자 결정 2026-10-06)」으로 대체한다는 행 추가(앞 결정 문장은 고치지 말고 뒤집힌 결정 표 방식)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/README.md` 행 버전 칸
- 그 밖 금지 · 커밋 금지 · SPEC-009 DB 여는 절차는 여전히 쓰지 마라

## 끝나면
리포트의 F/W 번호마다 「어디를 어떻게 고쳤나」 한 줄 표를 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-008-009-fix.md` 에 쓰고 §9 로 보고.
