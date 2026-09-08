# [frontend] WORK-008 Phase 3·4·6 — 생성중 · 상세 · 편집 모드 · 상세 드로어

너는 **task-management `frontend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
**코드 워커는 한 번에 하나만 돈다.** WORK-006·007 전부와 WORK-008 백엔드(Phase 1·2)가 들어와 있다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-008-meeting-close.md            ← 네 빌드 계획. Phase 3·4·6 만
  20-spec/spec-008-meeting-close.md            ← UX(§2 U-1~U-11) · §4 · §6 Acceptance 25개
  00-design/회의록.dc.html                      ← 시각 정본. L1403~2882
  00-design/디자인 시스템.dc.html                ← [09] MEETING NOTE(L649~755) + 05·06·07·10
  10-decision/decision-003-meeting-notes.md    ← 정책
  40-architecture/frontend/README.md
```

**`00-design/*.md` 요약본을 열지 마라.**

## 1. 범위 — Phase 3 · 4 · 6

```
Phase 3  생성중 · 실패 배너 · 상세 페이지 · 한 줄 요약 바 · 폴링
Phase 4  편집 모드 · 논의/결정 드로어 · 줄 삭제 모달 · 안건 이름
Phase 6  회의 상세 드로어 · 반응형
```

**Phase 5(업무 연동)는 별도 발주다. 건드리지 마라** — 줄 버튼·연관업무 드로어·액션 드로어는 그쪽이다.
**Phase 1·2(백엔드)는 끝났다. `app/back/` 을 건드리지 마라.**

## ⛔ 2. WORK-006·007 이 만든 것 — 다시 만들지 마라

```
AgendaLineTree     **track='merged' 로 부르기만 한다.** 컴포넌트 안에 track 비교 0건이
                   정적 검사로 고정돼 있다 — 통합본 탭 때문에 그 규칙을 깨지 마라
                   편집 가능 여부·근거 칩 표시는 **props 로만**
MeetingStatusBar   상단 바 **한 자리**(top 150 · 1640×56). waiting · connecting · live ·
                   paused · **headline** 변형을 이미 갖고 있다. 두 번째 상단 바 금지
TranscriptPanel    scrollToRange + 하이라이트 + Esc. 근거 칩이 이걸 부른다
PromptBar · LineKindPopover   편집 모드의 줄 추가가 재사용한다
첨부 탭 · 팝오버 · 파일 드로어  WORK-006 것
DrawerFrame 840    상세 드로어(U-4)가 이 위에 얹힌다. 폭 리터럴 0
ConfirmModal 600   삭제 모달. SPEC-004 U-8 프레임
ItemRow · EmptyState · V2Gate · TypeBadge · Selector
lib/               useRowFailures · useWorkSettings · inlineErrorMessage · datetime · ws
features 사이 import 0   static.test 가 고정 중
```

**Phase 6 의 상세 드로어는 `MeetingDetailBody` 를 `mode='drawer'` 로 감싸는 것**이다(WP Phase 6).
**전체 페이지와 드로어가 같은 본문을 쓴다** — 규격이 갈리지 않는 것이 그 Phase 의 목적이다.

## ⛔ 3. 정본

```
agendas.{human, ai, merged}   latestBatchSeq   invalid_meeting_status
안건 next 배지                 **「다음 논의로」**  ← 종료 후다. 회의 중 「대기」는 WORK-007
한 줄 요약 바                  headline 이 있으면 상단 1640×56 한 개([09] L727~733)
                              null 이면 안 그린다. **문단 요약은 그리지 않는다**
422 validation_error          응답에 field 가 온다 — 해당 컨트롤에 붙여라
```

## ⛔ 4. 그리지 마라 (SPEC-008 §7 제외 목록)

```
L1883·L2101·L2365·L2659   편집 중 헤더 「되돌리기」   ← 삭제가 생겨도 이력을 만들지 않는다
L1537~1547·L1752~1762     종료 후 보기 모드의 하단 프롬프트 바
L2288~2294                근거 구간 수동 선택 · 「구간 추가」
L2283                     캡션 「비워두면 회의 종료 후 AI가 채웁니다」
L2850~2851                「시작 상태」 셀렉터          ← Phase 5 것이지만 그리지 마라
L2863~2866 · L2858        「회의록 줄을 연관 업무로 바꾸기」 토글 + 캡션
L1437                     고정 유형명 「미팅·회의」
L2550·L2557·L2564         후보 목록 상태 표기 「대기·진행 중」
```

**살아난 것** — **편집 중 안건 제목 입력 상자**(L1894 · L1924 · L1959 +복제 9곳)는 결정 ②로 **계약이 됐다.** 그려라.

## ⛔ 5. 정책 — 뒤집지 마라

```
편집 저장        포커스 해제 자동 저장(인라인 · 종류 전환 · 안건 이름)
줄 삭제          **확인 모달 600**. 자동 저장이 아니다 — 되돌릴 이력이 없다([10] L800)
                 지우는 것은 회의록 탭(merged)뿐. AI 탭·스크립트·녹음은 남는다
안건            이름만 고친다. **안건 삭제·추가·상태 변경은 종료 후에 없다**
줄 순서          변경 없다
통합본 재생성     없다. 「다시 생성」은 **ended + 실패** 조합에서만
생성중           스피너 + 단계 문구 + **사람 원본 노출** + 편집 잠금
통합 실패        스피너 걷고 회의록 탭에 사람 원본 + 「통합 정리 실패 · 다시 생성」 배너
자동 재시도       프론트는 하지 않는다. 폴링은 계약된 주기로만
```

## 6. 지킬 것 — 아키텍처

```
정적 빌드 · hex 0 · text-[NNpx] 0 · new Date( 0 · Sheet/Dialog 직접 import 0
features 사이 import 0 · tokenStore 격리 · isEnterSubmit 재사용
프리셋에 없는 크기가 필요하면 tailwind.config 에 계단을 더하고
  **lib/utils.ts twMerge 에 등록**(빠뜨리면 조용히 버려진다 — 이 프로젝트에서 밟았다)
```

## ⛔ 7. 검증 — **앱 창 E2E 는 하지 마라**

```bash
cd app/front && npx tsc --noEmit
cd app/front && npx vitest run
```

**WP 의 앱 창 항목을 테스트로 옮겨라.**

```
생성중          job 응답 목 → 스피너·단계 문구·사람 원본 노출·편집 잠금
통합 실패        ended+failed → 배너 + 「다시 생성」. 정상 ended 에는 없다
한 줄 요약 바     headline 있음/null 두 케이스. 문단 요약 0
편집 자동 저장    blur 에 PATCH 1회. 실패 시 U-7 규격(재요청 0 · 롤백)
줄 삭제          「제거」 → 확인 모달 → DELETE. 모달 취소 시 요청 0
안건 이름        blur 저장. 추가·삭제 어포던스 0
배지            「다음 논의로」
상세 드로어      같은 MeetingDetailBody 를 쓴다(컴포넌트 동일성 단언)
폴링            계약 주기로만. 실패해도 자동 재시도 0
```

**정적 검사 grep 을 완료 증거에** — 위 6항목 + `AgendaLineTree` 를 `track='merged'` 로만 부르는지.

**테스트로 못 덮은 것은 「실물 확인 필요」 목록으로 보고에 남겨라.** 통과 처리하면 리뷰에서 FAIL 이다.

## 8. 지킬 것 — 일반

1. **`app/front/` 밖을 건드리지 마라**
2. **Phase 5(업무 연동)를 만들지 마라** — 줄 버튼·드로어 둘은 별도 발주다
3. **문서를 고치지 마라** · **커밋·push 하지 마라**
4. **WP 범위 밖을 하지 마라.** 발견하면 보고에 적어라
5. **기획·정책에 없는 기능을 만들지 마라.** 시안에 있어도 — §4 목록
6. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 9. Done Criteria

- [ ] Phase 3·4·6 의 WP 작업 항목이 전부 구현됐다
- [ ] **`AgendaLineTree` 를 `track='merged'` 로 부르기만 했다** — 컴포넌트 안 `track` 비교 여전히 0
- [ ] **두 번째 상단 바가 없다** — `MeetingStatusBar` 의 `headline` 변형을 쓴다
- [ ] **전체 페이지와 상세 드로어가 같은 `MeetingDetailBody`** 를 쓴다
- [ ] §4 「그리지 마라」 9항목이 화면에 **0건**. 안건 제목 입력 상자는 **있다**
- [ ] 줄 삭제가 **확인 모달**을 지난다. 다른 편집은 자동 저장이다
- [ ] 배지가 **「다음 논의로」**
- [ ] `tsc` 0 · `vitest` 통과 · **WORK-006·007 화면 회귀 없음**
- [ ] 정적 검사 grep 이 완료 증거에 있다
- [ ] `app/front/` 밖 변경 0 · 커밋 없음

## 10. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_baaf8bb8-be7b-43a1-a2e6-5682613fa40b \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-008 Phase 3·4·6 완료" \
  --body "만든 파일 / AgendaLineTree·MeetingStatusBar·MeetingDetailBody 재사용 증거 / 편집 저장 경계(자동 저장 vs 확인 모달) / tsc·vitest 결과 / **실물 확인 필요 목록** / 정적 검사 grep / 시안에 있으나 안 그린 것 / Phase 5 라서 안 만든 것 / 범위 밖이라 안 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-008 Phase 3·4·6 완료. 상세는 인박스." --enter
```
