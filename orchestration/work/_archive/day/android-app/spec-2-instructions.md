# [planner] 2회차 — 리뷰 WARN 반영 + Android 통역 범위 안

너는 1회차 planner 와 같은 역할이다. 맥락이 없으면 먼저 읽어라:
- 1회차 브리프 `android-app-spec-brief.md` · 1회차 리포트 `spec-report.md` · 리뷰 `review-doc-1-report.md` (모두 이 폴더: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`)
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec` (1회차 미커밋 변경 위에 이어서 고친다) · allowed_paths `products/day/` · 커밋 · push · PR · receipt 금지는 그대로

## 사용자 결정 (2026-11-13 · 새로 정해짐)

- **Android 통역도 이번 범위 안이다**(사용자 「안드로이드도 통역 넣어야지」). 통역이 Android 개발 앱에서 동작해야 완료다 — 마이크 권한 요청 · 녹음 · 통역 결과 표시 · 소리 출력(TTS 등 지금 iOS 에서 하는 것 그대로).
- 통역에 필요한 Android 쪽 일(권한 · 매니페스트 · 플러그인 Android 설정)은 코드 작업 범위. **Dart 변경이 필요하면 그때 코디에게 묻는다** — 지금 스펙에 Dart 변경을 정하지 마라.

## 고칠 것

1. **통역 범위 반영** — spec-003 개정 ⑭ · §1 범위 표 · 「Android 개발 앱 — 네이티브 채널」 절 · mobile-deployment §7-0 에서 「Android 통역 확인은 완료 조건 밖」을 **범위 안**으로 바꾼다. 통역 기능을 정의한 절(spec-003 · 필요하면 spec-001 의 통역 관련 줄)이 「iOS 만」이라 적은 곳이 있으면 전수조사(`grep -rn "통역" products/day/20-spec/`)로 찾아 고친다. 표로 리포트에.
2. **A-48 인수 조건**에 통역 항목 추가: 에뮬레이터에서 통역 화면 → 마이크 권한 요청 → 말하기(에뮬레이터 호스트 마이크 입력) → 통역 결과 표시 · 소리 출력. 화면 문구는 지어 넣지 마라(있는 화면 이름 · 절 번호로 가리킨다).
3. **W-1** spec-003 :570 「통역은 푸시와 관계없이 쓴다」 — 위 결정에 맞게 「푸시와 무관 · Android 에서도 범위 안(A-48)」으로.
4. **W-2** 「Dart 동작 무변경」[확정] (mobile-deployment :188 · spec-003 :64 · :565) → **이번 착수(§7-0) 범위에 묶는다**: 「이번 착수는 Dart 를 바꾸지 않는 것이 기본 — 바꿔야 하면 코디 · 사용자 확인」. 영구 [확정] 아님.
5. **W-3** A-48 「로그아웃 뒤 세션 묶음 없음」 → 「로그아웃 뒤 앱을 다시 켜면 로그인 화면」(보이는 결과).
6. **W-4** spec-003 :570 결과 칸에 「설정 탭 「알림」 칸은 늘 OS 알림 꺼짐 안내(DAY-SPEC-005) — Android 개발 앱에서는 OS 설정에서 켜도 사라지지 않는다(푸시 스텁)」 한 줄. spec-005 는 그대로.
7. lint `python3 scripts/lint-pipeline.py --strict` → products/day ERROR 0.

## 이번엔 하지 말 것

- **Delivery v2 재결속은 아직 하지 마라.** 승인 경로는 (b): 스펙 PR 머지 → 같은 key v2 재결속(target_specs 에 DAY-SPEC-004 추가 · 통역이 걸리면 해당 SPEC 도 · W-3 문구 · 통역 Target Delta/A-48) → 사용자 승인. v2 는 코디가 머지 뒤 따로 발주한다. 다만 v2 에 넣을 변경 목록(Target Delta · A 조건 · target_specs 차이)은 리포트에 적어 둔다.
- 참고 항목(README:22 · spec-003 title 등)은 고치지 않는다 — 단, spec-003 title 「(iOS · 1차 시술 현황)」은 Android 개발 앱 · 통역이 범위에 들어오면서 틀린 말이 되는지 판단해 리포트에 적어라(고칠지 말지만).

## 산출물

- 리포트 `spec-2-report.md`(같은 폴더) — 변경 파일:줄 · 통역 전수조사 표 · W-1~W-4 처리 · v2 변경 목록 · lint 결과 · 정할 것
- 완료 보고는 1회차 브리프 §9 와 같은 두 명령(이번 taskId · dispatchId 는 새 dispatch preamble 값).
