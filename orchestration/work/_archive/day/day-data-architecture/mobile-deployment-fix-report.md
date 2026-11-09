# 수정 리포트 — day-data-architecture / mobile-deployment / 검수 WARN 반영 (2026-11-08)

대상: `products/day/40-architecture/mobile-deployment.md` 한 파일(작업 트리 수정, 커밋 없음 · `05b9a195` 위에 얹음).
근거: `mobile-deployment-review-report.md` WARN 1~7 · 코디네이터 brief. 재조사 · 새 설계 없음.

## 반영 내용

| WARN | 자리 | 바꾼 것 |
|---|---|---|
| 1 | §2 Mermaid · §2 본문 · §9 「앱에 든 비밀」 | 「앱이 APNs · FCM 을 부르지 않는다」 → 앱은 KOS · 푸시 **발송** API 를 부르지 않는다로 한정. 앱은 OS(iOS) · SDK(Android FCM)로 등록해 기기 토큰을 받고 DAY 서버에 전달한다고 명시. Mermaid 에 등록 · 토큰 전달 점선 4개 추가, 서버→APNs/FCM 선에 「발송」 라벨. 서버 발송 자격증명 금지 vs `google-services.json`(클라이언트 SDK 설정) 구분. 「서명 키를 앱에 넣지 않음 ≠ 서명하지 않음」 한 문장 추가(항목 8) |
| 2 | §1 · §5-2 · §13 | `DEVELOPMENT_TEAM` 이 `project.pbxproj` 에 기록되는 점, Team ID 는 비밀키가 아님, 저장소 기록 범위는 기존 규칙 해석 · 개정 전까지 **[미결]**. 로컬 비추적 xcconfig · CI env · 규칙 재해석은 **후보로만**. **M-16** 추가. CENTURION_DAY `AGENTS.md` 는 건드리지 않음 |
| 3 | §12 3단계 · Android 후속 문장 | 3단계에서 Android productFlavors 제거, Android 후속 안내 문장으로 이동 |
| 4 | §1 · §7 머리 · §13 | 「Android 도 나중에 낸다 [확정]」 제거 → 확정은 「문서에 함께 적음 · 실제 설정은 iOS 부터」만. Android 착수 · 출시 여부와 시점 **[미결]**, **M-17** 추가 |
| 5 | §6 Unlisted | 「요구」 → 「권고」 |
| 6 | §2 Mermaid · §9 KOS 행 · §13 | prod 「[확정] 실제 병원 연결」 → 「실제 병원 연결 포함 가능 · 데모 연결 배제 여부 [미결]」. dev = 데모 연결만 [확정]은 유지. 미결 목록 일관성을 위해 **M-18** 추가 |
| 7 | §14 출처 표 · 미검증 문단 | Flutter iOS 배포 행에서 「TestFlight 도 심사 지침 대상」 제거. 미검증 문단에 「외부 베타 심사」 · 「TestFlight 빌드 = production APNs(배포 profile → production 으로 미루어 적음)」 추가 |

### WARN 7 의 APNs 공식 근거

- brief 의 URL(`.../RemoteNotificationsPG/Chapters/APNsOverview.html`)은 **HTTP 404**.
- 대체로 연 `.../RemoteNotificationsPG/CommunicatingwithAPNs.html` 에는 TestFlight 언급이 없음.
- 그래서 **출처를 추가하지 않았다.** §8-2 는 기존대로 배포 profile 기준 설명만 두고, TestFlight = production 은 미검증으로 표시했다.

### 손대지 않은 것

- 빌드 mode ↔ flavor 독립(§4) 설명은 그대로(이미 정확).
- brief 범위 밖인 §5-4 「외부는 베타 심사 있음」 · §8-2 표 「TestFlight · App Store · Ad Hoc 등 배포 profile → production」 문장은 바꾸지 않았다(미검증 문단으로 커버).

## WARN 8 (log.md) — 확인만, 변경 없음

- `AGENTS.md:148-150` · `rules/document-pipeline.md` §변경 라우팅: 「decision/spec/work 본문 변경 PR **머지 시점**」에 entry 1건 추가. `arch-change` 는 종류 enum 에 있고, DAY 의 앞선 40-architecture 변경도 모두 행을 남겼다(`log.md:35 · 40 · 41 · 43`).
- 결론: 규칙상 **PR 머지 전에 필요**(관례 · enum 기준). 이번 scope 밖이라 넣지 않았다. **코디네이터가 PR 전에** `| 2026-11-08 | arch-change | — | #… | 40-architecture mobile-deployment.md 신설(초안) — iOS 우선 · 비공개 배포 · 서명 · 푸시 구조 |` 한 행을 넣을지 정해야 한다.

## 검증

- `python3 scripts/lint-pipeline.py --strict` — exit 0 · **0 error** · 263 warning. `products/day` 출력 **0건**(warning 은 다른 제품 기존분).
- `git diff --check` — 통과.
- `git status` — `products/day/40-architecture/mobile-deployment.md` 만 수정(27+ / 14-). 커밋 · push · PR 없음.
