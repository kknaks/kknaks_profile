# [frontend 3차] 앱 이름 Strong Hajin → medi-ax · 재빌드·서명·공증 (2026-10-01, 사용자 지시)

사용자가 설치본을 열어 보니 창 제목이 「Strong Hajin」이다. 회사용 이름은 **`medi-ax`**(소문자·하이픈 그대로).
워크트리: `git fetch && git checkout -B kknaksss/strong-hajin-medi-ax origin/main` (main 에 #7 origin 까지 있다).

## 바꾸는 것 — 사용자 눈에 보이는 이름 전부
- 알려진 곳: `tauri.conf.json` productName · `src/lib.rs:375` 창 title · `shell-noop/index.html` <title> · `Info.plist`(마이크 사용 설명 등 문구)
- **목록으로 끝내지 말고** `git grep -n "Strong Hajin\|StrongHajin" -- frontend` 로 전수. 셸 자기 화면(연결 오류·설정 안 됨) 문구, 메뉴/About, dmg 볼륨 이름까지
- dmg 파일명: `medi-ax_0.0.1_arm64.dmg`

## 바꾸지 않는 것 — 이유 있음
- `identifier: app.stronghajin.desktop` — 바꾸면 저장소가 새로 잡혀 로그아웃된다(`build-shell-fixture.mjs:115`, `lib.rs:632` 시험). 그대로
- `stronghajin://` 스킴 · crate 이름 `strong-hajin-shell` · 주석 · 레포/차트 이름

## 검증·빌드
- `cargo test` · `make shell-verify-strict` · 바꾼 문구를 단언하는 시험 갱신
- fe-02 와 같은 절차: 빌드 → Developer ID 서명 → notarytool(AC_NOTARY) → staple → spctl 확인 → `~/Downloads/medi-ax_0.0.1_arm64.dmg`. 기존 `StrongHajin_0.0.1_arm64.dmg` 는 남겨 둔다
- .app 의 `CFBundleName`·`CFBundleDisplayName`·실행 파일 이름이 medi-ax 로 나오는지 `PlistBuddy` 로 확인
- 리포트 `report-fe-rename.md` (전수 결과: 바꾼 것/안 바꾼 것 이유). 커밋·Release 금지. 두 채널 보고
