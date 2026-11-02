# [backend] 직원 앱 내부 채팅 — WORK-011 WP-BE1 → WP-BE2 (procedure/back)

너는 **cc-prototype `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **mobile 워커가 같은 워크트리의 `procedure/app/` 에서 병렬 작업 중이다 — `procedure/app/` 는 건드리지 마라.** `procedure/front/` 도 건드리지 않는다.


## 0. 코디 처분 — review-doc r2 WARN 6 (SPEC-007 0.2.0 보충 · **SPEC 과 이 절이 다르면 이 절이 이긴다** — SPEC 은 E2E 뒤 planner 가 맞춘다)

리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r2.md`

| # | 처분 |
|---|---|
| W2-1 | **DEC-009 D-45**: 방을 만들 때 · 참여자로 처음 추가될 때 `last_read_message_id` = 그 순간 방의 마지막 메시지 id(없으면 0). 다시 초대(D-43)도 같은 규칙. 시험: 메시지 3개 있는 그룹에 새로 추가된 사람의 `unread` = 0 |
| W2-2 | 메시지 0개 방: `since` 없이 부르면 최근 50(빈 목록) · 앱은 받은 메시지가 없으면 `since` 를 보내지 않는다 · `POST …/read {messageId: 0}` = 200 · 아무것도 안 바꿈 |
| W2-3 | 숨김(D-44) 세 길에 **예약 상세의 실제 호출 자리 `app/lib/screens/reservation_detail_screen.dart:301-304 · 309-311`** 를 넣는다. 시험은 `openQrScreen` · `openPassportScan` 을 가짜로 바꾸지 말고 실제 화면을 push 해서 「열린 수」가 오르는 것을 단언한다 |
| W2-4 | 루트 Navigator 위 화면(사진 크게 보기 · 대화상자 · 아이패드 시트) 위에서는 앱 안 배너가 안 보여도 된다(OQ-933 그대로) — 놓친 메시지는 탭 배지 · 방 목록으로 보인다 |
| W2-5 | `flutter_image_compress` 를 `pubspec.yaml` 과 A14 대상에 넣는다(늘 JPEG 다시 인코딩) |
| W2-6 | 검증 grep 은 **라우트 핸들러만**: `grep -n -A1 "@router\." procedure/back/app/api/chat.py \| grep -c "^[0-9]*-def "` = 0 (도우미 함수 `def` 는 괜찮다) |

## 1. SSOT — 먼저 읽을 것 (이기는 순)

1. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` (0.2.0 · 리뷰 r2 처분이 있으면 그 판) ← **계약의 SoT. 여기 없는 건 발명하지 마라**
2. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` ← WP · 대상 파일 · 완료 조건 · 검증 명령 · 「계약 고정점」
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` (D-01 ~ D-45)
4. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` (지금 앱 계약 — 채팅이 얹히는 바닥)
5. 확정 시안(화면 정본): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design/Ceramique 의료진 앱 — 채팅.dc.html` + `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design-chat-report.md` (r2) — 단 헤더는 DEC D-38 이 이긴다
6. 문서 리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r1.md` · `review-doc-r2.md` 의 「조용히 통과하는 자리」 · 「사용자가 실물에서 만날 자리」

코디 워크트리 문서는 **읽기만** 한다.

**기대는 개념**: 해당 없음

## 2. 배경

직원 앱에 1:1 + 그룹 메신저(텍스트 · 사진 · 푸시)를 넣는다. back 은 표 4 · API 14 · SSE 5 · 채팅 푸시 · 사진 저장 · 열기를 만든다. 계약은 SPEC-007 이 전부 갖고 있다.

## 3. 계약 (mobile 과 합의됨 — 이대로 제공)

WORK-011 「계약 고정점」 표 그대로: 표 · 모양(`Person` · `Member` · `Room` · `Preview` · `Message`) · 시각 = 응답 KST 오프셋 밀리초(`iso_ms`) · DB UTC 밀리초(`to_db_ms`) · 안 읽음 = `id > last_read_message_id` · `since` = parse 뒤 `>=` · API 14(prefix `/api/chat`) · 오류 코드(SPEC-007 §6.3) · 경로 65 · SSE 5종 · 푸시 payload · 사진 규칙. **바꿔야 하면 고치지 말고 코디에게 `[질문]`** — mobile 이 같은 계약으로 짓고 있다.

## 4. 먼저 읽을 핵심 파일

SPEC-007 §12 「바뀌는 코드 자리」의 B 행 전부(파일:줄). 특히 `back/app/service/push.py:175-187`(`_dispatch` — 이벤트 루프 없으면 건너뜀) · `back/app/service/stream.py:59-75` · `back/app/domain/clock.py` · `back/app/repository/db.py` · `back/app/api/photos.py` · `back/app/main.py` · `back/tests/test_order.py:247`.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `procedure/back/` (WORK-011 WP-BE1 · WP-BE2 대상 파일 + `tests/`)
- `procedure/docker-compose.yml` · `procedure/.env.example` 는 필요할 때만(WORK-011 은 새 env 0 이라 원칙상 안 고친다)

## 6. 구현 단계

1. WP-BE1 (표 · 방 · 메시지 API · 경로 65) → WORK-011 의 BE1 검증 명령 1회
2. WP-BE2 (SSE · 푸시 · 사진) → BE2 검증 명령 1회
3. 마지막에 `cd procedure/back && uv run ruff check . && uv run pytest -q` 전체 1회
4. 완료 보고 전에 확인: 라우트 핸들러 `def` = 0(§0 W2-6 명령) · `grep -rn "법적 검토 필요: 직원 채팅" procedure/back` = 4

## 7. 범위 제약 — 하지 말 것

- 커밋 · push · PR 금지
- `procedure/app/` · `procedure/front/` · 다른 기능 폴더 수정 금지 · procedure 밖 import 금지
- 사용자 포트 · 프로세스 · docker 를 건드리지 마라 — 로컬 서버 · compose 를 띄우지 않는다(시험은 TestClient · 가짜 KOS · 가짜 APNs)
- 원장 · 상담사 호출 푸시 만료(0) · 알림 목록 종류(둘)를 바꾸지 않는다
- 로그에 메시지 본문 · 이름 · 푸시 제목 금지(id 만)
- 실명 · 키 · 토큰 금지(public)

## 8. 검증

```
<기능>/back 에서 uv run pytest · uv run ruff check . — Phase 범위에 맞게 1회씩, 통과하면 반복하지 마라. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- SPEC-007 §13.1 줄마다 「시험 이름 → 통과」 표를 보고에 넣는다
- 기존에 이미 깨져 있던 무관한 실패는 「무관」으로 분리해 보고한다

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_61179808-14b1-431b-a85f-619d2c232e8e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
