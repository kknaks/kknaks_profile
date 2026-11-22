
# [planner] DAY 직원 앱 0.2.0 — SPEC 개정 · WP 나누기 · Delivery 발행

너는 **day `planner` 워커**다. 너는 앞 맥락이 없다 — 이 브리프가 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

혼자 쓰는 워크트리다.

## 1. SSOT — 먼저 읽을 것

### 사용자 결정 (2026-11-20 · 이 표가 정본 — 여기 없는 정책은 짓지 말고 「정할 것」으로)

| # | 결정 |
|---|---|
| M-1 출시 | 직원 앱 다음 버전 **0.2.0**. DAY Dev 앱(dev 서버)으로 먼저 내고 실기기 통과하면 같은 코드를 prod 설정(정식 DAY)으로 빌드. 빌드 번호 최소 iOS Dev 4 · iOS 정식 3 · Android 둘 다 4. iOS 0.1.0 (2) 심사 건은 그대로 둔다 |
| M-2 호환 | 지금 깔린 0.1.0 은 1차 배포라 **쓰는 사람이 없다** · 이 버전까지 해서 병원 인계 → **옛 앱 호환을 챙기지 않는다**. 앱 버전으로 옛/새 가르기 없음. 서버 응답 · 알림 종류 · 통역 프로토콜은 새 앱 기준으로 바로 바꾼다 |
| M-3 기기 제한 | 앱 로그인에도 웹(#257)과 같은 **기기 선택 단계** — 웹 서비스 로직 재사용 · 앱용 JSON 만 더함. 글자 = 웹과 같은 KOS 글자. **로그아웃 때 KOS 해제는 안 한다**(해제 API 가 비밀번호 요구 — SPEC-001 규칙 15 유지) |
| M-4 시술 현황 앱 범위 | **넣음**: 바로 시작 · 호출 취소 · 「간호관리」 표시(시스템 계정 집도의) · 방 옮기기 · 원장 바꾸기. **뺌**: 귀가 대기 취소(앱에 귀가 대기 목록 없음) · 정렬 탭 · 순서 변경 |
| M-5 API | 바로 시작 앱 JSON 경로 새로(`board.quick_start` 서비스 재사용 · 일부 거절 응답 모양은 정할 것). 호출 취소 · 방 옮기기 · 원장 바꾸기 `/api` 는 이미 있음. 앱은 「서버 계산 값만」 규칙 → 호출 취소 · 바로 시작 가능 여부 `can*` 를 스냅샷에 더한다(방 옮기기 · 원장 바꾸기 쪽도 필요한 칸이 있는지 확인) |
| M-6 호출 취소 알림 | 받는 사람 = 그 호출을 받았던 원장(들) · 원래 원장 호출 알림은 닫는다. 제목 「호출 취소」 · 본문 「{방} · 시술 {N}건 · 호출 취소」(방 없으면 「방」 — 원장 호출과 같은 꼴). 앱 푸시 · **웹 알림 목록 · 종 배지 · 웹 OS 알림 모두**(원장 호출과 같은 대우). 새 notification_kind(push_kind) = migration. 옛 앱 배지 어긋남은 M-2 로 고려 안 함 |
| M-7 Android 푸시 | **FCM 이번에 넣는다**(원장 호출 · 채팅 · 호출 취소 등 iOS 와 같은 범위). Firebase 프로젝트 · google-services.json · 서버 발송 키는 사용자가 만든다(값은 레포 밖) — 스펙엔 칸 이름 · 위치만 |
| M-8 통역 | **통역 엔진 정본 = 통키(interpret-pwa main `56e43a0`) 최신본** — DAY 는 그대로 따라간다: STT v6(v5 는 2026-12-15 종료) · 시드 `.11`(DAY 로더 허용 칸 넓힘) · 끊김 D-67 · 세 참여자 D-68 ~ D-70(앱 반이중 걷음 · `audio_stop` · `playback_stopped`) · 바로잡기 D-58 ~ D-66(records 의존 함수만 가져옴). 통역 기록(records · D-42)만 DAY 에 없음 |
| M-9 | 토스트 · 화면 글자는 원천(결정 표 · 웹 · 시안)에 있는 것만. 없으면 「미정」 — 짓지 마라 |

### 조사 리포트 (현황 · 근거 파일:줄 — 반드시 읽어라)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/research-current-state.md` — A(버전 · 빌드 · 깨질 곳) · B(기기 제한) · C(시술 현황 21동작 표) · D(알림) · E(통역 차이 5커밋) · F(정할 것 18 — 위 결정 표로 대부분 닫힘). §F 중 결정 표로 안 닫힌 것만 OQ 로 남겨라.

### 문서 · 코드
- 스펙: `products/day/20-spec/spec-001-login-session.md`(앱 기기 선택) · `spec-002-procedure-board.md`(quick-start JSON · can*) · `spec-003-mobile-app.md`(주 — 앱 범위 표 「뺌」 갱신 · 통역 · 버전) · `spec-005-notifications.md`(호출 취소 알림 OQ-N14 · FCM) · `spec-000-data-model.md`(enum · 기기 토큰 칸) · `40-architecture/mobile-deployment.md`(버전 · FCM · M-9 · M-13) · `20-spec.md` · `30-work.md` · `log.md` · `10-decision.md`
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2`(origin/dev `844eace4`) — 레포 루트 `AGENTS.md` 먼저 · `backend/day/` · `app/`
- 통키(읽기만): `/Users/kknaks/git/toy_pr2/interpret-pwa`(`origin/main` `56e43a0`) · 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/para/projects/summer-star/interpret-pwa/`(DEC D-42 ~ D-71 · SPEC-001)
- Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`

기대는 개념: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/para/areas/concept/` 에서 `tolerant-reader` · `websocket-relay` 를 찾아 읽어라(M-2 로 옛 앱 호환은 안 챙기지만 새 앱이 모르는 값을 받을 때 기준은 그대로).

## 2. 배경

DAY 직원 앱(Flutter) 0.2.0 — 기기 제한 · 시술 현황 · 호출 취소 알림 · Android 푸시 · 통역 최신화. 이 버전까지 해서 병원에 인계한다. 통역 STT v5 종료(2026-12-15)가 사실상 마감. 스펙을 먼저 닫고 검수 뒤 코드(backend · mobile · designer)로 간다.

## 3. 계약

결정 표가 뼈대다. 새 API(앱 기기 선택 JSON · 바로 시작 JSON · can* 칸 · 알림 종류 · FCM 토큰 등록 · 통역 WS 메시지)를 코드 사실에 맞춰 이름 · 모양 · 오류 코드까지 적는다. 새 이름이 필요하면 제안으로 적고 「정할 것」에 올린다(기본값 함께).

## 4. 먼저 읽을 핵심 파일

위 §1 의 조사 리포트가 파일:줄 지도다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-report.md`(생성 1개)

## 6. 구현 단계

1. SPEC 개정 — M-1 ~ M-8 을 해당 SPEC 에 반영(규칙 · 흐름 · 케이스 매트릭스 · API · 화면 글자). SPEC-003 「뺌」 표는 M-4 대로 갱신. 통역은 통키 DEC 번호를 근거로 단다.
2. 열린 것 OQ 로 — **코드 착수를 막는 것**은 기본값 후보와 함께 따로 표로.
3. `30-work` — WP 나누기 제안: 워커(backend · mobile · designer)별 · 순서 · 의존(예: designer 시안 → mobile 화면 · backend API → mobile). FCM 은 사용자 Firebase 준비에 걸리므로 따로 떼어라. 앱 화면 시안이 필요한 곳(기기 선택 · 바로 시작 다중 선택 · 방 옮기기 · 원장 바꾸기 · 간호관리 표시)을 표로.
4. Delivery Issue 발행(`mediness start-delivery --mediness-repo <이 워크트리> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2 --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`) · 승인 receipt 는 적용하지 마라(사용자 몫).

## 7. 범위 제약 — 하지 말 것

- 코드 수정 · 커밋 · push · PR 금지. 기획안(00-baseline) 수정 금지.
- 비밀번호 · 이메일 · IP · 키 · Azure 이름 · Firebase 값을 문서에 넣지 마라.
- 화면 글자 짓기 금지(M-9). 결정 표에 없는 정책을 정하지 마라.
- 옛 앱 호환 장치(버전 가르기 등)를 넣지 마라(M-2).

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 리포트 `spec-report.md`: 변경 파일:줄 · 결정 표 반영 위치(M-1 ~ M-9 각각) · 착수 막는 OQ 표 · WP 표 · Issue 번호 · digest.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **완료 보고는 dispatch preamble 의 worker_done 명령을 그대로 따른다**(아래 옛 형식과 다르면 preamble 이 맞다).
- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
