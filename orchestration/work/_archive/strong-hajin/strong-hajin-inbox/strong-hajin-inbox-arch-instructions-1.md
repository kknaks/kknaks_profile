# [architect] 추가 지시 1 — 시안 파일을 로컬에 내려받는다 (사용자 2026-10-05)

브리프는 그대로 유효하다. **allowed_paths 에 아래 폴더를 더한다.**

- 대상 폴더: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/reference/2026-09-10-sc-meeting/package 2/` — 같은 Claude Design 프로젝트(7e839512)의 로컬 사본이 이미 있다(Calendar.html·TaskDetail.html 등)
- DesignSync 로 받아 **원문 그대로** 저장:
  1. `Inbox.html` (수신함 시안 — 파일명 확정됨: https://claude.ai/design/p/7e839512-977c-4142-b4b5-d992df566ffc?file=Inbox.html)
  2. `Settings.html`
  3. `_ds_bundle.css` · `_ds_bundle.js` — 폴더에 이미 있다. **받은 것과 다르면 덮어쓰고**, 다른지 여부를 보고에 적어라
  4. 두 시안이 import 하는 다른 파일(styles.css·이미지·폰트 등)이 폴더에 없거나 다르면 함께 받는다
- 그 폴더의 다른 기존 파일은 건드리지 마라
- **구현(TSX 작성)은 하지 마라** — 사용자가 시안을 보면서 정책을 먼저 논의한다. 코드 레포 손대지 않는다
- 내려받은 뒤 `design-survey.md` 는 **로컬 사본을 근거로** 쓴다(근거 위치 = 로컬 파일명)
- 보고 body 에 받은 파일 목록 + 바이트 수를 넣어라
