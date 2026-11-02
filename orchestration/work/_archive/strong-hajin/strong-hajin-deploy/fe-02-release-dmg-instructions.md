# [frontend 2차] 운영 origin dmg — 빌드 · Developer ID 서명 · 공증 (2026-10-01)

아이콘은 머지됐다(#6 b0eb4b4). 워크트리를 `git fetch && git checkout -B kknaksss/strong-hajin-origin origin/main` 로 새로 선다.

## 사실(코디 확인)
- 운영 서버 가동: https://ax.medisolveai.xyz — / 200 · providers {local:true} · 사용자가 웹 로그인 성공(2026-10-01)
- 서명 인증서: `Developer ID Application: keonhak lee (UYQF47UCVR)` (login keychain) · 공증 프로필 `AC_NOTARY` (`xcrun notarytool history --keychain-profile AC_NOTARY` 동작)

## 할 것
1. 운영 origin 을 채운다 — `frontend/src-tauri/shell.config.json` `operationalOrigin: "https://ax.medisolveai.xyz"` 와 `capabilities/product-shell.json` remote urls 를 같은 origin 으로. **주소를 쓰는 곳을 grep 으로 전부 세라**(`operational-origin-not-yet-decided`, `operationalOrigin`, `.invalid`). `make shell-verify-strict` 통과
2. `make shell-final-preflight SHELL_OPERATING_ORIGIN=https://ax.medisolveai.xyz` — 막히는 항목(D-4·서버 실재·M-1·M-5)을 증거 파일로 채운다. 증거는 **실측한 것만**: D-4=사용자 웹 로그인 성공, 서버 실재=curl 200, M-1=`curl -v` 인증서 체인. **M-5(앱 재시작 후 쿠키 유지)는 서명본을 사용자가 설치해 확인할 항목** — 증거에 pending 으로 적고 preflight 가 그걸 막으면 막힌 채로 보고(우회 금지)
3. 빌드 → Developer ID 서명(hardened runtime, Entitlements.plist) → `xcrun notarytool submit --keychain-profile AC_NOTARY --wait` → `xcrun stapler staple` → `spctl -a -vvv -t install <dmg>` / `.app` 에 `accepted source=Notarized Developer ID` 확인
4. 결과 dmg 를 `~/Downloads/` 에 복사(파일명에 버전·arm64 포함). 이전 `_local.dmg` 는 지우지 마라
5. 리포트 `report-fe-release-dmg.md` — 바뀐 파일, preflight 결과, 서명·공증 출력 요지(비밀값 없음), dmg 경로·sha256

## 하지 말 것
- GitHub Release 발행·태그 · 비밀값/Apple ID 출력 · 커밋·push(코디 몫)
- 운영 서버·infra 건드리기
