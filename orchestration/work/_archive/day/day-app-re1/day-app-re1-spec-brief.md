
# [planner] 직원 앱 차트를 웹과 같은 기능으로 — DAY-SPEC-003 · 002 개정

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/_RESUME.md` §2 결정 ← **이번 작업의 사용자 결정(범위 · D1 ~ D11). 계약의 SoT. 다시 열지 마라. 여기 없는 정책은 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/research-1-report.md` ← 현황 조사(앱 · 웹 · 백엔드 · 스펙 대조 · 근거 파일:줄 @CENTURION_DAY `55e60aa4`). §0 요약 · §2 기능 전수표(28행) · §3 API · §5 스펙 대조 · §6 정할 것(→ 결정으로 닫힘)
- 웹 차트 결정 정본(앞 작업): `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/_archive/day/day-chart-photo/_RESUME.md` §2 와 거기서 가리키는 `chart-photo-decisions.md`(C1 ~ C36) — 웹 동작은 이것 그대로. 앱이 웹과 같아야 하는 기준

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

직원 앱(DAY-SPEC-003) 시술현황의 차트는 지금 **읽기 전용**이다(스냅샷 노트만 보여 줌 · 차트 API 0건 · 인수 조건 A-38). 웹 차트는 11-24 에 탭 3(간호관리 · 의사 · 시술전후사진) · 탭별 명시적 저장 · KOS 확인 / 이어 붙이기 · 사진 여러 장 + KOS 등록 · 사진 탭 10초 가져오기로 끝났다.

이번 작업 = **앱 차트를 웹과 같은 기능으로.** 사용자 범위는 **차트만**이다 — 여권 스캐너 · 문진 QR · 예약 탭은 다음 작업이니 스펙에 쓰지 않는다.

산출물:
1. **DAY-SPEC-003 개정(다음 개정 번호)** — 앱 차트: 여는 곳(시술 줄 누름 · 그대로) · 띄우는 자리(D4 루트 Navigator · 탭바까지 덮음) · 폰 = 전체 화면 / 아이패드 = 가운데 창 · 탭 3 · 탭별 [저장] · 「최근 저장」 · 담당자 고르기(D5) · 미저장 닫기 확인(D6 — ✕ · 뒤로 가기 제스처 · 끌어 내림 · 바깥 누름 각각) · 사진 탭(목록 · 카메라 / 앨범 올리기 여러 장 · 삭제 확인 · 크게 보기 · 「KOS 미반영」 다시 시도 · 열린 동안 10초 가져오기) · 값 원천 = `GET /api/visits/{id}/chart`(D11) · 권한(웹과 같은 편집 / 보기 규칙을 끌어옴 · 바꾸지 않음) · 오류 글자 · 인수 조건(A-38 등 「읽기 전용」 조항은 ~~취소선~~ + 날짜 · 사유) · OQ-A30 · OQ-A34 처분 · §1 「뺌」 표 · §3 API 계약 · §4 권한 · 까만 줄 / 탭바 겹침 고침(D9 — 같은 탭 Navigator 시트 포함 · 어느 시트들인지 research §1-3 근거) · iOS 권한 문구는 지금 그대로 + OQ(D10)
2. **DAY-SPEC-002 개정** — API 계약 표에 앱용 `/api` JSON 짝(D7 · **이름 제안**): 탭 저장 · 사진 목록 · 올리기 · 삭제 · 다시 시도 · 파일(썸네일 / 원본). 앱 Bearer 인증 · 응답 모양 · 오류 코드는 웹 경로와 같은 서비스 · 같은 규칙(규칙 31 · 사진 대상 규칙 23 · D8 — 대상 확장 없음). C15 「앱 경로 없음 — 웹만」 · U-16 마지막 줄을 ~~취소선~~ + 날짜 · 사유로 바꾼다. 웹 동작은 바꾸지 않는다
3. `20-spec.md` · `10-decision.md` · `log.md` 반영

**WORK(30-work)는 이번에 쓰지 않는다** — SPEC 검수 뒤 따로 발주한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음(문서 단계). 경로 · 칸 이름은 **「이름 제안」**, 정하지 못한 것은 OQ + 「기본값(코디 제안)」 칸.

## 4. 먼저 읽을 핵심 파일

문서(이 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`):
- `products/day/20-spec/spec-003-mobile-app.md` — 고칠 본문. **개정 머리글 · 표 · 취소선 관례를 그대로 따른다**
- `products/day/20-spec/spec-002-procedure-board.md` — 웹 차트 · 사진 계약(U-14 · U-16 · 규칙 23 · 31 · C15 · API 계약 표)
- `products/day/20-spec/spec-000-data-model.md` — `visit_photo` 등(바꿀 것 없을 가능성 — 확인만)
- `products/day/20-spec.md` · `10-decision.md` · `log.md`

코드(read-only — `git -C /Users/kknaks/git/CENTURION_DAY show 55e60aa4:<path>` · checkout · 수정 금지): research-1 이 근거로 짚은 파일:줄을 따라가 확인한다. 특히 `app/lib/ui/chart_sheet.dart` · `app/lib/ui/room_screen.dart` · `app/lib/ui/doctor_picker.dart` · `app/lib/chat/screens/chat_attach_sheet.dart` · `backend/day/routers/api/board.py` · `backend/day/routers/board.py` · `backend/day/services/board_chart*.py` · 사진 서비스 · `app/lib/core/copy.dart` · `app/ios/Runner/Info.plist`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 결정 D1 ~ D11 · 범위를 SPEC-003 / 002 의 어느 절 · 규칙 · 요소 · 인수 조건을 바꾸는지 표로 짝짓는다(새 개정 머리글에 「① ② …」로)
2. research-1 §2 기능 전수표 28행을 하나씩 SPEC-003 에 반영한다 — 행마다 「앱에 넣음 / 웹 전용으로 둠(근거)」. 빠뜨린 행 0
3. SPEC-003 앱 차트 절 · 화면 구성 · 인수 조건 · OQ 를 쓴다. 폰 / 아이패드 모양 차이를 적는다
4. SPEC-002 API 계약 표에 앱 `/api` 짝을 넣는다 — 웹 경로와 짝을 표로 대응(요청 · 응답 · 인증 · 오류)
5. 화면 글자: 웹 SPEC-002 · 앱 SPEC-003 에 이미 있는 글자만 쓴다. 탭 이름 차이(앱 「간호 관리 차트」 vs 웹 「간호관리차트」 — research §6 끝)는 OQ 로. 없는 글자는 비워 두고 OQ — **지어 넣지 않는다**
6. migration 필요 여부 판단(근거와 함께 — 기대: 없음)
7. `20-spec.md` · `10-decision.md` · `log.md` 반영 → §8 검증

## 7. 범위 제약 — 하지 말 것

- 결정을 다시 열지 않는다. 결정과 앞 판이 다르면 결정을 따르고 차이를 적는다
- 여권 스캐너 · 문진 QR · 예약 탭은 쓰지 않는다(Out Of Scope 에 「다음 작업」 한 줄만)
- 웹 차트 동작 · 권한 규칙 · 사진 대상 규칙을 바꾸지 않는다
- 화면 문구 · iOS 권한 문구를 지어 넣지 않는다
- 기획안(`00-baseline/`) · 다른 제품 폴더를 고치지 않는다 · WORK 를 쓰지 않는다 · 커밋 · push 하지 않는다

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **(코디 추가 · 2026-11-25)** 이번 발주는 orca Run(`worker-start`)으로 나간다. **dispatch preamble 에 적힌 `worker_done` 명령(Task · Dispatch ID · `--outcome` · `--report-path`)이 아래 (1)보다 우선**이다. (2) 직접 주입은 그대로 해도 된다. 리포트는 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/planner-1-report.md` 에 쓴다(바꾼 절 목록 · 전수표 28행 처분 · OQ · lint 결과).

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_414d6113-407d-486b-ab54-10a4a6b455cb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
