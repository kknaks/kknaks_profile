# report-fe-icon — 앱 아이콘 교체 (메디솔브 M, macOS 격자)

- 브랜치: `kknaksss/strong-hajin-icon` (origin/main cdb0f3f 기준) · 커밋·push 안 함

## 원본
- 브리프 지정 `mediness-rust/src-tauri/icons-prod/icon.png` 는 512. 같은 폴더의 `icons-prod/icon.icns` 에 **네이티브 1024 표현(ic10)** 이 들어 있어(iconutil 로 scratchpad 에 풀어 확인 — 512 LANCZOS 확대본과 비교해 가장자리가 뚜렷, 512 로 축소하면 icon.png 와 평균 차 0.23/255) 그 1024 를 원천으로 썼다. 원본 레포는 읽기만.
- 이렇게 하면 M 은 **축소만** 된다(배율 0.7816). 512 를 원천으로 삼았으면 M 폭 494px 를 위해 1.56배 확대가 필요했다.

## 수치 (1024 캔버스)
| 항목 | 값 |
|---|---|
| 몸통 | 흰 둥근 사각형 824×824, 위치 (100,100), 여백 100, 모서리 반경 185 (4x 슈퍼샘플 AA) |
| 원본 M bbox (1024) | 632×530 @ (203,256) — 원본 폭 대비 61.7% |
| 새 M | 494×414 @ (265,304) — **몸통 폭의 60.0%** (캔버스 대비 48.2%), bbox 중심 = 캔버스 중심 |
| 리샘플 | Pillow LANCZOS, 축소만 |
| 바깥 | 투명 + **옅은 드롭섀도**(검정 22%, blur 14, y+8) — 흰 몸통이 밝은 Dock/Finder 에서 사라지지 않게 macOS 관례를 따름. 원치 않으면 스크립트 `sh` 합성 한 줄 빼고 재생성 |

## 마스터
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/work/strong-hajin-deploy/fe-icon-master-1024.png` (scratchpad 원본: `/private/tmp/claude-501/.../scratchpad/icon-master-1024.png`)
- 생성 스크립트: 같은 폴더 `fe-icon-make_master.py`

## 바뀐 파일
- `frontend/src-tauri/icons/32x32.png`, `128x128.png`, `128x128@2x.png`, `icon.png`(512), `icon.ico`(16~256) — 갱신
- `frontend/src-tauri/icons/icon.icns` — 신규(16~1024)
- `frontend/src-tauri/tauri.conf.json` — `bundle.icon` 에 `icons/icon.icns` 한 줄 추가
- `npx tauri icon` 부산물(64x64·Square*·StoreLogo·ios·android)은 scratchpad 에만 두고 레포에 넣지 않음

## 검증
- 눈 확인(Read): 1024 마스터, 32/128/256/512 시트 — 32px 에서도 M 식별됨
- `make shell-verify`: 문제 0 · 구성 미비 0(이전 `.icns 부재` 항목 사라짐) · 호스트 한계 1(Windows)
- `make shell-verify-strict`: 통과
- `cargo check`: 통과
- `npx tauri build --bundles app`: 52초, `Strong Hajin.app` 생성. `Contents/Resources/icon.icns` 가 레포 icons/icon.icns 와 바이트 동일, `CFBundleIconFile=icon`
- **pending**: Finder 에서 실제 아이콘 눈 확인 — `qlmanage` 썸네일이 헤드리스에서 멈춰 못 봤다. 번들 안 icns 동일성으로 대체 확인

## 주의
- 빌드 산출물 `frontend/src-tauri/target/` 은 gitignore 대상(그대로 둠)
