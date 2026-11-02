# [mobile] 앱 E2E 피드백 A1~A6 수정 + WP12 앱 푸시

같은 cc-prototype `mobile` 워커 · 같은 워크트리 · `procedure/app/` 만.

## 1. E2E 피드백 — `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/e2e-app-feedback-batch-1.md` A1 ~ A6 전부
- A1 · A4 · A6: 머리 줄 · 카드 줄의 오른쪽 정렬(배지 · 시각이 오른쪽 끝) — **내용이 짧을 때만 오른쪽이 빈다**(단서 줄 참고). 앱 전체 Row 를 **전수 grep** 해 같은 증상을 다 고치고, 짧은 배지 · 긴 배지 둘 다로 시뮬레이터 확인. 배지 잘림은 문구 「시술 완료」 등으로
- A2: 호출 시트 「호출할 시술」 위에 [전체 선택](pickable 만)
- A3: 토스트 노란 이중 밑줄(Material/DefaultTextStyle 밖) → 고치고 **화면 위쪽**(머리 아래 · safe area)에
- A5: 룸 상세 본문 순서 = **오더 메모 → 마취 → 시술(+[의사 호출])** · 호출 상자 · 완료 상자는 맨 위 그대로 · 태블릿 2열 = 왼쪽 오더 메모 · 마취 / 오른쪽 시술

## 2. WP12 앱 푸시 — 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` 0.2.0 §5-1.1 · §5-1.3 · WORK-004 WP12
- APNs 직접(Firebase 0) · 로그인 뒤 알림 권한 요청 · 기기 토큰 → `POST /api/devices` · 로그아웃 때 `DELETE /api/devices/{token}` · 알림 누르면 payload `visitId` 룸 상세 · 앱이 앞에 있을 때도 배너 표시 · Xcode Push Notifications capability(entitlements — 팀 id 값은 레포에 0 · Signing.xcconfig)
- APNs 키는 아직 없다 — **`xcrun simctl push <시뮬레이터> <번들 id> <payload.apns>` 로 가짜 알림**을 넣어 배너 · 누르면 룸 상세 이동을 확인(payload 예시 파일을 `procedure/app/tool/` 같은 곳에 두고 README 에)

## 3. 검증 · 맥 렉 주의
- **iPhone 시뮬레이터 하나만**(iPad 는 마지막에 A5 태블릿만 잠깐 켜고 끈다) · 빌드 중복 금지 · 확인 끝나면 앱을 실 back 으로 다시 띄워 둔 채 보고
- flutter analyze · 바뀐 시험 · 마지막에 test 전체 1회 · 커밋 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
