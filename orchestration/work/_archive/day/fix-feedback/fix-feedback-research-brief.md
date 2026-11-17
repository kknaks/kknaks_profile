# [researcher] 현장 피드백 — F-3 시작 규칙 · F-7 수락 흐름 · F-6 차트 아이콘 표면 (read-only)

너는 **day `researcher` 워커**다. 너는 앞 맥락이 없다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback` (코디 워크트리)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 코디 워크트리다 — 리포트 파일 1개 외 수정 · 생성 금지.

## 1. SSOT — 먼저 읽을 것

- 사용자 피드백: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/e2e-feedback.md` — F-1 ~ F-7 표. **이번 조사는 F-3 · F-7 · F-6 만.**
- 코드(읽기만): `/Users/kknaks/git/CENTURION_DAY` — **`origin/dev` `4f8316a7`(#253)**. 사용자 체크아웃 · pull/checkout 금지 — `git -C … show origin/dev:<path>` · `git -C … grep … origin/dev` 로 읽는다. 레포 루트 `AGENTS.md` 먼저.
- 스펙(읽기만): mediness `origin/main` — `git -C /Users/kknaks/git/harness_works/mediness-mediness show origin/main:<path>`(canonical 은 더티 체크아웃 · checkout/pull 금지). `products/day/20-spec/spec-002-procedure-board.md` · `spec-000-data-model.md` · `spec-003-mobile-app.md` · `spec-005-notifications.md` · `products/day/00-baseline/planning/` 의 시술 현황 · 원내 현황 · 요청함 기획안.
- KOS 앞 조사(읽기만): `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/_archive/day/day-procedure-board-2/research-har-room-chart-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/_archive/day/day-data-architecture/backend-233-kos-kv-report.md`.

기대는 개념: 해당 없음.

## 2. 배경

사용자 2026-11-17 현장 피드백. 이번 조사는 셋이다.

- **F-3** 시술 현황 액션바(전체 선택 뒤)에 「의사 호출 · N건」 옆 「**바로 시작** · N건」 버튼을 추가하려 한다. 현장 말: 원장 호출 없이 바로 시작해도 되는 시술이 있다. **지금 시작 규칙(우리 코드 + KOS 반영)이 그걸 허락하는지** 모른다 — 사용자가 「코드를 봐야 하고 KOS 도 봐야 한다」고 했다.
- **F-7** 「수락」 버튼: 간호 · 관리 · 기타 직원은 대리 수락(지금 그대로), 원장(의사) 계정이면 **로그인한 계정이 집도의**로 바로 수락하게 바꾸려 한다. 지금 흐름을 알아야 한다.
- **F-6** 차트 아이콘: 앞으로 **작성된 차트만** 아이콘을 띄운다(미작성 흐린 아이콘 없앰). 시술 현황 · 시술 완료 · 그 밖에 아이콘이 나오는 **모든 곳**에 같은 규칙 — 바꿀 곳을 전부 센다.

수정 발주 전에 현황만 잰다. **결정하지 않는다** — 후보와 「정할 것」만.

## 3. 계약

해당 없음.

## 4. 먼저 읽을 핵심 파일 (출발점일 뿐 — 목록 밖도 grep 으로 센다)

- `backend/day/services/board_rules.py` — `call_block` :222 · `accept_block` :258 · `start_block` :280 · `accept_of` :127
- `backend/day/services/board.py` — `call` :581 · `accept` :694 · `start` :807
- `backend/day/routers/board.py`(웹) :475 · :502 · `backend/day/routers/api/board.py`(앱) :184 · :211
- `backend/day/emr/kos/` — `writes.py` · `mapper.py` · `client.py` · `staff_client.py`
- 템플릿 `backend/day/templates/partials/board_parts.html` · `board_chart*.html` · `ui.html` · 앱 `app/lib/ui/room_screen.dart` · `chart_sheet.dart`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 6. 조사 질문

**F-3 시작 규칙**
1. 지금 「시작」이 되려면 무엇이 먼저여야 하나 — 원장 호출 · 수락(집도의 지정)이 전제인지. `start_block` 의 거절 사유를 전부, 웹 · 앱 API 양쪽으로. 호출 없이 시작하는 경로가 이미 있는지(단건 · 여러 건).
2. 시작 시 KOS 로 무엇을 보내나 — 호출 · 수락 · 시작 각각 KOS 쓰기(writes) 내용, **집도의(원장) 값이 KOS 쪽에서 필수인지**, 비어 있으면 어떻게 되는지(코드 · 앞 KOS 리포트 · 확인 못 하면 「확인 안 됨」).
3. 「원장 호출이 필요 없는 시술」을 가를 근거가 데이터에 있나 — 시술 · 카탈로그 · 설정 · KOS 값 중 그런 칸이 있는지. 없으면 「없음」.
4. 액션바 「의사 호출 · N건」의 N 계산과 일괄 호출 경로(템플릿 · JS · 라우터 · 서비스). 일괄 시작 엔드포인트가 있는지. 선택에 호출 필요 / 불필요 시술이 섞일 때 지금 어떻게 되는지.
5. 스펙 · 기획안에서 시작 · 호출 · 수락 순서를 정한 곳(파일 · 절 · 줄). 지금 코드와 어긋난 곳이 있으면 따로.

**F-7 수락 흐름**
6. 「수락」을 누른 뒤 집도의가 정해지는 경로 — 원장 고르는 단계(모달 등)가 있는지, 누가 집도의로 기록되는지(누른 계정 · 고른 원장 · 호출 대상). 웹 · 앱 둘 다.
7. 로그인 계정이 원장(의사)인지 가르는 기준이 지금 코드에 있나 — 직무 태그 `doctor` 등 · 계정 ↔ 원장(doctors[]) 연결. 그 연결로 「로그인 계정 = 집도의」를 바로 정할 수 있는지.
8. 수락이 KOS 로 보내는 값(집도의 id 등)과, 대리 수락 / 본인 수락이 KOS 에서 구분되는지.
9. 권한 — `board.accept` edit 를 누가 갖나. 원장 계정이 지금 수락을 누를 수 있는지.

**F-6 차트 아이콘 표면 — 목록을 받지 말고 grep 으로 전부 센다**
10. 차트 아이콘(간호 · 의사 차트 · 작성 / 미작성 · `day-ic--disabled` 등)이 나오는 곳 **전부**: 웹 템플릿 · CSS · JS · 앱(Flutter) · 스냅샷 / API 필드 · 테스트 단언. 화면별(시술 현황 · 시술 완료 · 원내 현황 · 요청함 · 앱 방 화면 등) 표로.
11. 「작성됨」 판정 원천 — 어떤 값으로 작성 / 미작성을 가르나(웹 · 앱 같은 원천인지).
12. 지금 미작성 아이콘을 누르면 차트 작성으로 들어가는 동작이 있나 — 없애면 **작성 진입로가 사라지는 곳**이 있는지(웹 · 앱 각각). 이것이 가장 중요한 「조용히 깨지는 자리」다.

## 7. 범위 제약 — 하지 말 것

- 파일 수정(리포트 외) · 커밋 금지. CENTURION_DAY · mediness canonical 에서 checkout · pull · 빌드 금지(읽기 · `git show`/`git grep` 만).
- 사용자 포트 · 프로세스 · 로컬 컨테이너 금지. dev/prod 서버 · KOS 실호출 불필요.
- 고객 값 · 키 · 토큰 · 계정 이메일 출력 금지.
- F-1 · F-2 · F-4 · F-5 는 이번 범위 밖.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · 문서 URL). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/research-1-report.md` — 질문 1 ~ 12 각각 답 + 근거(파일:줄 · git ref) · 「확인 안 됨」 · F-6 표면 표 · 항목별 「웹만 / API 같이 / 앱 수정 필요」 판정 · 고칠 방향 후보 · 정할 것.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94fbe396-828d-4fa4-8bd8-829294f10614 --from term_3f6b3c6a-1f34-49f9-b324-cb4323c19d6e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
