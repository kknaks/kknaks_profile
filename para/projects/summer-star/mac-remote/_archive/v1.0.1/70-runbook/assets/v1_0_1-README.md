# Assets Manifest — mac-remote

규칙: `para/projects/project.md`

> App Store 제출용 바이너리 자산을 모으고 상태를 추적한다. 절차는 [RB-002](../v1_0_1-runbook-002-ios-testflight-appstore.md).
> 자산 파일은 `appstore/` 하위에, 이 README는 manifest.

## App Store 자산

| 자산 | 필수 | 규격(참고) | 상태 | 위치 | 원본 |
|---|---|---|---|---|---|
| App Icon 1024 | 필수 | 1024×1024 PNG, **알파 없음** | ✅ 있음 | `appstore/icon/AppIcon-1024.png` | `mac-remote/icon/AppIcon-1024.png` (1024², 알파 없음 확인·복사) |
| iPhone 스크린샷 | 필수 | 6.9"(1320×2868) 또는 6.5"(1242×2688 / 1284×2778), 알파 없음 | ✅ 있음 | `appstore/screenshots/` | 3장 받음 — 1284×2778(6.5") JPEG, 알파X |
| iPad 스크린샷 | N/A | — | N/A | — | iPhone 전용으로 변경(빌드 family=1) → 불필요 |
| 앱 프리뷰 영상 | 선택 | 스토어 규격(.mov/.mp4) | 없음 | `appstore/preview/` | 화면 녹화 |

> ✅ 빌드를 **iPhone 전용**으로 변경함 (`TARGETED_DEVICE_FAMILY = "1"`) → **iPad 스크린샷 불필요.** iPhone 6.9"만 제출.
> ⚠️ 스크린샷은 **알파 채널 없는 RGB**여야 함(투명도 있으면 거부). 정확한 필수 크기는 App Store Connect 업로드 화면에서도 확인.
> ⚠️ `preview/`의 디자인 PNG는 **앱 프리뷰(영상) 아님** — 스크린샷 소스다. 최종본은 위 규격으로 `screenshots/iphone/`에 둔다.

## 캡처할 화면 (스크린샷 구성안)

제품 핵심 플로우 기준. companion Mac 연결된 상태. **iPhone 6.9"** 기준 3~10장.

1. 창 목록 탭 — 창 카드 + 아이콘 ([[v1_0_1-spec-001-window-list|MRT-SPEC-001]])
2. 매크로 탭 — 매크로 버튼 그리드 ([[v1_0_1-spec-003-key-input|MRT-SPEC-003]])
3. 설정 탭 — QR 페어링 화면 ([[v1_0_1-spec-007-pairing|MRT-SPEC-007]])

## 구조

```text
assets/
└── appstore/
    ├── icon/                # 1024 앱 아이콘
    ├── screenshots/
    │   ├── iphone/          # iPhone 스크린샷
    │   └── ipad/            # iPad 스크린샷 (Universal 타겟이라 세트로 필수)
    └── preview/             # (선택) 프리뷰 영상
```

> 상태: `있음` / `없음` / `N/A`. 자산이 들어오면 위 표의 상태를 갱신한다.
