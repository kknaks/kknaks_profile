# [frontend] WORK-006 Phase 4~6 — 회의록 목록 · 생성 드로어 · 시작 전

너는 **task-management `frontend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
**코드 워커는 한 번에 하나만 돈다** — 이 트리에서 직접 작업한다. 백엔드 Phase 1~3 이 이미 들어와 있다.

**문서는 코디 워크트리 절대경로로 읽는다(읽기 전용).**

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-006-meeting-setup.md          ← 네 빌드 계획. Phase 4·5·6 만
  20-spec/spec-006-meeting-setup.md          ← UX 계약(§2 U-n)·API(§4)·Acceptance(§6)
  00-design/회의록.dc.html                    ← 시각 정본. L24~231 · L232~541 · L542~649 · L650~760
  00-design/디자인 시스템.dc.html              ← [09] MEETING NOTE(L649~755) + 05·06·07·10
  10-decision/decision-003-meeting-notes.md  ← 정책
  40-architecture/frontend/README.md         ← 구조 규약. 리뷰어 판정 기준
```

**`00-design/*.md` 요약본을 열지 마라.** 그걸 읽고 시안을 안 본 것이 이 프로젝트 최대 사고였다.

## 1. 범위 — Phase 4 · 5 · 6

```
Phase 4  목록 페이지 · 미리보기 패널 · 삭제 모달
Phase 5  새 회의록 드로어 · 셀렉터 인라인 행
Phase 6  회의 시작 전 화면 · 첨부 탭 · 파일 드로어 · 반응형
```

**Phase 1~3(백엔드)은 끝났다. `app/back/` 을 건드리지 마라.**

## ⛔ 2. 코디가 정한 것 — 문서보다 이게 우선이다

| 항목 | 결정 |
|---|---|
| **`MeetingDetail` 트랙 필드** | **`agendas.{human, ai, merged}`** — 안건 배열, 줄은 안건 안 `lines[]` |
| **배치 회차 필드** | **`latestBatchSeq`** |
| **상태 가드 에러코드** | **`invalid_meeting_status`** 하나 |
| **자식 쓰기 응답** | **`MeetingDetail` 전체** · 삭제만 `204` · 없는 자식 `404` |
| **안건 `next` 배지 문구** | **회의 중 「대기」 / 종료 후·목록 「다음 논의로」**(DEC-003 §1 표). **네가 그리는 목록·미리보기·시작 전은 「다음 논의로」** — 회의 중 화면은 WORK-007 이다 |
| **AI 한 줄 요약 바** | `headline` 이 있으면 상단 `1640×56` 한 개(디자인 시스템 [09] L727~733). **`null` 이면 안 그린다.** 문단 요약은 그리지 않는다 |

## ⛔ 3. 시안에 있어도 그리지 마라 — 기획·정책에 없다

SPEC-006 §7 「시안에 있으나 기획·정책에 없어 제외」 18행이 정본이다. 특히 —

```
L120~127   취소된 회의 행(「취소」 배지 + 취소선)   status 4종에 취소가 없다
L153·L361  일시 뒤 「· 회의실 A」                  장소는 v1 에 없다
L167~174   「요약」 문단 + 「AI 생성」 배지          한 줄 요약만 있다
L466~468   유형 고정 칩 3종                        동적 유형 셀렉터로
L519~525   「만들면 바로 회의 시작」 토글
L579·L687  「회의 정보 수정」 버튼                  수정은 상세 드로어·캘린더 드래그
L607~633   AI 안건 생성 일체 — 프롬프트 모드 칩 · 추천 안건 칩 3개 · 전송 버튼
           「안건 초안을 만들어 줍니다」 문구
           → 프롬프트 바는 **안건 입력창 + 「추가」** 로만 남긴다
L643~645   푸터 「MacBook Pro 마이크 · 내 목소리 등록됨」
L222~226   PNG 첨부 행                             첨부는 md · URL 두 갈래
```

**드롭 영역과 「최대 50MB」 문구는 그리되 `V2Gate`** — 파일을 놓으면 「v2에서 제공됩니다」 토스트만, **네트워크 요청 0**.

## 4. 다시 만들지 마라 — 공용 컴포넌트를 쓴다

리뷰어가 이걸 축으로 본다. **두 번째 구현이 있으면 FAIL 이다.**

| 무엇 | 어디 |
|---|---|
| `DrawerFrame` 840 | `components/shared/` — 생성 드로어가 이 위에 얹힌다 |
| `Selector` + 하단 「+ 새 프로젝트로 추가」 인라인 행 | `components/shared/Selector.tsx` — **규격 정본은 SPEC-006 U-3.** WORK-004 가 먼저 만들었으니 **대조해서 맞춘다**. 고치면 업무 생성 드로어도 바뀌므로 **그쪽 확인도 완료 증거에** |
| 첨부 팝오버 360 | SPEC-003 U-7 — 회의용 두 번째 구현 금지 |
| `Calendar` | 한 벌. 기간 스테퍼와 일시 입력이 공유 |
| `ItemRow` 행 규격 | h44 · 테두리 없음 · `padding 0 16` · `border-bottom #F1F2F5` |
| `EmptyState` · `StatusDot` · 배지 · 팔레트 8종 | WORK-003·004 |
| `V2Gate` | 로컬 업로드 |
| **상단 바** | `MeetingTopBar` **한 파일** — `waiting`(기록 대기) · `headline`(한 줄 요약) 두 변형. Phase 4 미리보기와 Phase 6 시작 전이 공유 |

## 5. 지킬 것 — 아키텍처

`frontend/README.md` 가 판정 기준이다.

```
정적 빌드     동적 세그먼트 0 · 모든 page 에 'use client' · 쿼리스트링으로 상태를 나른다
색            컴포넌트에 hex 리터럴 0. 토큰만 (styles/tokens.css)
날짜          new Date() 직접 포맷 0 — lib/datetime 을 쓴다
오버레이      Sheet/Dialog 직접 import 0 — DrawerFrame·lib/overlay 경유
토큰 저장소    tokenStore 밖에서 키체인/localStorage 호출 0
영역 사이 import  features/meetings 가 features/tasks 를 부르지 않는다
              공유는 components/shared/ 나 lib/ 로 올린다
              단 하나의 예외: 업무·회의 드로어는 소유 영역에 두고 직접 import (FE §163)
IME           Enter 제출은 lib/keyboard.ts 의 isEnterSubmit() 를 쓴다 — 새로 만들지 마라
자동 재시도    없다. 실패는 실패 표시 + 「다시 시도」 (DEC-001 §7)
낙관적 갱신    없다
```

## ⛔ 6. 검증 — **앱 창 E2E 는 하지 마라**

WP 의 검증 항목이 「앱 창에서 …」로 적혀 있다. **이번 발주는 실물 확인을 하지 않는다.**

```bash
cd app/front && npx tsc --noEmit        # 네가 만진 파일 0 에러
cd app/front && npx vitest run          # 네가 만들거나 고친 테스트만
```

**WP 의 앱 창 확인 항목을 테스트 코드로 옮겨라.**

```
목록·필터·정렬·달 이동   훅/컴포넌트 테스트 (MSW 로 API 목)
칩 숫자가 안 바뀐다       projectCounts 렌더 테스트
상태 표기 4종            props 별 렌더 테스트
한 줄 요약 바 유무        headline null / 값 있음 두 케이스
삭제 모달 문안·비활성     recording 행에서 「삭제」 disabled
드로어 기본값            오늘 · 30분 올림 · +1시간
겹침 409 · 301분 422     에러 응답 목 → 인라인/토스트 렌더
V2Gate 드롭             요청 0건 (fetch 스파이)
```

**정적 검사는 `grep` 결과를 완료 증거에 남겨라.**

```
Sheet/Dialog 직접 import · 인라인 hex · new Date() 포맷 · 동적 세그먼트
'use client' 누락 · tokenStore 밖 저장소 호출 · MeetingTopBar 파일 수
```

**테스트 코드로 못 덮은 항목은 「실물 확인 필요」 목록으로 보고에 남겨라.** 임의로 통과 처리하지 마라.

## 7. 지킬 것 — 일반

1. **`app/front/` 밖을 건드리지 마라**
2. **문서를 고치지 마라** — SPEC·WP·정책·아키텍처·시안 전부 읽기 전용
3. **커밋·push 하지 마라**
4. **WP 범위 밖을 하지 마라.** 필요해 보여도 하지 말고 보고에 적어라
5. **기획·정책에 없는 기능을 만들지 마라.** 시안에 있어도 — §3 목록
6. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 8. Done Criteria

- [ ] Phase 4·5·6 의 WP 작업 항목이 전부 구현됐다
- [ ] `tsc --noEmit` 0 에러 · `vitest` 통과
- [ ] **WP 의 앱 창 확인 항목이 테스트 코드로 옮겨졌다.** 못 옮긴 것은 「실물 확인 필요」로 목록화
- [ ] §3 의 「그리지 마라」 항목이 화면에 **0건**
- [ ] §4 공용 컴포넌트를 **재사용**했다 — 두 번째 구현 0건 (`Selector` 는 업무 드로어 영향까지 확인)
- [ ] `MeetingTopBar` 가 **한 파일**이다
- [ ] 배지 문구가 **「다음 논의로」**(네 화면은 목록·미리보기·시작 전이다)
- [ ] 정적 검사 7종 `grep` 결과가 완료 증거에 있다
- [ ] `app/front/` 밖 변경 0건 · 커밋 없음

## 9. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_f902cdae-be94-4879-8989-b6c73a9854d9 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-006 Phase 4~6 완료" \
  --body "만든 파일 목록 / 재사용한 공용 컴포넌트와 대조 결과(Selector 업무 드로어 영향 포함) / tsc·vitest 결과 / 앱 창 항목을 테스트로 옮긴 목록 / **실물 확인 필요 목록** / 정적 검사 7종 grep 결과 / 시안에 있으나 안 그린 것 / 범위 밖이라 안 한 것 / SPEC·WP 와 어긋나 못 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-006 Phase 4~6 완료. 상세는 인박스." --enter
```
