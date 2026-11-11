# [reviewer] fix 1판 검수 — TestFlight 준비(앱 아이콘 · 수출 규정 키) + dev 서버 설정

너는 **day `reviewer` 워커**다. **너는 앞 판의 맥락이 없다.** 작성자가 아니다 — 독립으로 본다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 문서)
- 레포 규칙: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/AGENTS.md`
- 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/_RESUME.md` §2
- 작성자 브리프 · 리포트(같은 폴더): `fix-app-brief.md` · `app-testflight-prep-report.md` · `fix-app-upload-brief.md` · `app-testflight-upload-report.md` · `fix-app-export-compliance-brief.md` · `app-export-compliance-report.md` · `fix-be-dev-env-brief.md` · `be-dev-env-report.md`
- 계약: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-001-login-session.md`(§3 앱 환경 연결) · `spec-003-mobile-app.md` · `spec-004-*`(채팅 · 푸시) · `40-architecture/deployment.md` · `mobile-deployment.md`

검수 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` 의 **미커밋 변경 전부**(`git status` · `git diff origin/dev`).

```
app/README.md
app/ios/Runner/Info.plist                               (ITSAppUsesNonExemptEncryption=false)
app/ios/Runner/Assets.xcassets/AppIcon.appiconset/      (Contents.json + PNG 15)
app/assets/brand/app-icon.svg
deploy/config/dev.env                                   (공개 주소 · APNs Key/Team ID · 허용 앱)
backend/tests/deploy/test_chat_env_contract.py
```

## 볼 것

1. **dev.env** — `dev` 에 머지되면 자동 배포된다. 이 값으로 dev 서버가 뜨는지, 앱 로그인 응답에 `api_base_url` · `environment` 가 실리는지를 코드 경로로 따라간다(`common/config.py` → 로그인 서비스 → 응답). APNs 칸은 채웠는데 키(Key Vault)는 아직 없는 **중간 상태**에서 기기 등록 · 채팅 보내기 · 알림이 어떻게 동작하는지(오류 없이 `skipped_no_key` 인지 · 부팅 실패나 500 이 나는 자리가 없는지). 채팅 저장소 칸이 빈 상태도 같이.
2. **시험 계약 변경** — `test_chat_env_contract.py` 가 계약을 느슨하게 만들지 않았는지. prod 는 여전히 전부 빈 값으로 묶이는지. 조용히 통과하는 자리.
3. **비밀값** — diff 에 키 본문 · 토큰 · 연결 문자열 · IP · 리소스 ID 가 없는지. `dev.env` 의 Key ID · Team ID 는 설계상 허용(비공개 레포 · 사용자 확인) — 그 밖을 본다. `day_vm.py` 의 금지 키 검사에 걸리지 않는지.
4. **앱** — `Info.plist` 키 한 개 · 수출 규정 `false` 의 근거가 맞는지(리포트의 근거를 코드에서 다시 확인). 아이콘 세트 19칸 · 1024 알파 없음 · `Contents.json` 정합. 소스 기본 Bundle ID 가 placeholder 그대로인지(dev 값이 소스에 박히지 않았는지). `app/README.md` 가 사실과 맞는지 · 비밀값 없는지.
5. **범위** — 브리프가 허용한 경로 밖 변경이 없는지. 화면 문구를 지어 넣은 곳이 없는지.

## 돌려 볼 것(각 1회)

```
cd backend && uv run pytest -q tests/deploy tests/day/auth/test_environments_api.py
cd backend && uv run ruff check tests/deploy/test_chat_env_contract.py
cd app && fvm flutter analyze
plutil -lint app/ios/Runner/Info.plist
```

## 하지 말 것

- 레포 파일 수정 금지(read-only). 서명 · 업로드 · 배포 · Key Vault · Azure · ASC 호출 금지. 사용자 포트(11040) · 프로세스 금지.
- `dev.env` 의 Key ID · Team ID 값을 리포트 · 화면에 옮기지 않는다(리포트는 PUBLIC 레포).

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-1-report.md`
— 판정 **FAIL / WARN / PASS** · 각 지적에 `파일:줄` + 근거(SPEC 절 · 코드) · 「조용히 통과하는 자리」 절 따로 · 돌린 명령과 수치.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_4afcc88b-79e9-4f89-82de-783b5f10c7c9 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: <판정 · 한 줄>" \
  --body "판정 / FAIL·WARN 목록(파일:줄) / 돌린 명령 수치"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] reviewer 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] reviewer: <질문>" --enter`
