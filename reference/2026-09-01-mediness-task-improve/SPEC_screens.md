# 화면 사양

공통 셸: 상단 헤더 52px(로고 28px `#476CFF` radius 8 + 전역 내비 + 240px 검색박스) / 좌측 사이드바 224px(`내 업무`: AX 채팅·인박스(배지)·태스크·워크플로우 / `관리자`: 인박스(전체)·태스크(전체), 하단 사용자 카드) / 우측 콘텐츠. 구분선은 모두 `1px #F3F3F3`.

---

# 1. 태스크 보드 (`screens/task-board.dc.html`)

## 목적
내 태스크를 상태별로 훑고, 상태를 바꾸고, 지난 완료를 월 단위로 회고.

## 레이아웃
```
[헤더 영역: padding 20 24 0]
  eyebrow  — AX ASSISTANT · 내 업무      (11/600/0.08em/uppercase/#476CFF, 앞에 18×2px 바)
  타이틀줄  태스크 [BETA] [ ‹ | 2026년 8월 | › ]      ......   [+ Task 생성]
  뷰 탭    (칸반)(테이블)  |                          ← 하단 border 1px #F3F3F3
[본문]
  칸반: display:flex; gap:16; overflow-x:auto; padding:18 24 24
  테이블: overflow:auto; padding:8 24 28
```
- 월 이동: 화살표 28×28 원형(`1px #E3E3E3`), 라벨 min-width 112 / height 28 / pill / 12.5px 600. 연·월 롤오버(1월에서 ‹ → 전년 12월).
- Task 생성: primary 32px height, 12.5px 600.
- 뷰 탭: pill 34px height, padding 0 20. 선택 `#476CFF` 배경 + 흰 글자 600, 비선택 흰 배경 + `1px #E3E3E3` + `#3E3E3E`.

## 칸반
- 컬럼 4개 고정: **대기 · 진행 중 · 완료 · 중단** (수락 대기 없음, 취소 미노출). `flex:1 1 0; min-width:240px`
- 컬럼 헤더: 상태 점 7px + 라벨 13/600 `#3E3E3E` + 건수 12px `#9F9F9F`. 항목 0이면 opacity .55. (+ 버튼 없음)
- 빈 컬럼: `1px dashed #E3E3E3` / `#FBFBFB` / radius 8 / "비어 있음" 12px `#CFCFCF`, min-height 120.
- **완료 컬럼만** 선택된 월로 필터(카드 마감월 기준). 다른 컬럼은 월과 무관.

### 카드
`1px #E3E3E3` / radius 8 / padding 11 12 / hover `#FBFBFB` + 보더 `#CFCFCF`
```
[출처 점]  제목 14/500/1.45
           [상태 칩 ▾] [메타 11.5 #9F9F9F]        [마감 11.5] [아바타 20px]
           (중단 시) 사유 11.5 #FF4E51
```
- 출처 점 8×8 radius 2: AX `#DDE6FF` + inset 보더 `#A9BEFF` / 의사결정 `#F3F3F3` + inset `#E3E3E3`
- 마감 지남이면 `#FF4E51`
- 상태 칩 클릭 → 카드 내 드롭다운(150px, radius 8, shadow, "상태 변경" 헤더 + 5개 항목, 현재 값 `#F0F4FF`/`#476CFF`/600)

## 테이블 뷰
상태별 그룹 헤더(점 + 라벨 13/600 + 건수) 아래 행 나열. 행: 출처 점 · 제목(1줄 ellipsis, 14px) · 메타 · 마감(92px 우측정렬) · 아바타. 행 높이 padding 10 4, 구분선 `1px #F3F3F3`, hover `#FBFBFB`.

---

# 2. 태스크 상세 (`screens/task-detail.dc.html`)

## 목적
하나의 태스크를 읽고, 진행시키고, 완료 근거를 남긴다.

## 레이아웃
```
[고정 헤더 블록  padding 14 40 16, 하단 border]
  ← 태스크                                   (13px #6E6E6E)
  — AX ASSISTANT · 태스크 상세                (eyebrow)
  [제품][메디니스][WBS] | [상태 칩] [D-4 · 08. 28. 마감]      [액션 버튼들] [···]
  제품 개발 파이프라인 워크플로우                (26/700/-0.02em)
  [메타 스트립] 이건학·백엔드 재배정 | 제품 메디니스·v0.0.2 | 기한 08. 28. | ● WBS 연결됨 ↗
  (사유·근거 배너 / terminal 안내문)
[스크롤 본문  display:flex; gap:40; padding:24 40 56]
  main(flex:1)                       aside(320px)
```
- 태그 칩: padding 3 9 / radius 6 / 11.5px. 제품·WBS `#F3F3F3`+`#6E6E6E`, 제품명 `#F0F4FF`+`#476CFF`.
- 메타 스트립: 12.5px, 항목 사이 `1px×12px #F3F3F3` 구분선, gap 0 18. 기한은 **최종 기한만** 표시.

## 본문(main) 순서
1. **할일 목록 카드** — `1px #E3E3E3` radius 12 overflow hidden
   - 헤더(배경 `#FBFBFB`, padding 9 14): "할일 목록" 12.5/600 + 진행 바 72×4 + `n / 4 완료` 11.5px
   - 행: 드래그 핸들(6점, `#E3E3E3`) · 체크박스 17px(체크 시 `#476CFF`) · 제목 13px(현재 항목 600, 완료 항목 `#9F9F9F` + line-through) · 다음 항목에 `진행 중` 배지 · 연필 · X. padding 5 8, radius 6, hover `#FBFBFB`
   - 마지막 줄: 점선 + 아이콘 + "항목을 입력하고 Enter" (보더 없는 인라인 입력 28px)
2. **배경** — 섹션 라벨(11/600/uppercase/`#9F9F9F`) + 연필. 본문 14/1.75 `#3E3E3E`
3. **목표** — 동일 라벨. 5px 파란 점 불릿 목록, 항목 간 10px
4. **댓글 / 진행 로그 탭** — 상단 `1px #F3F3F3` 구분선, 탭 32px pill(선택 `#F3F3F3`+`#000`600, 비선택 `#9F9F9F`) + 건수
   - 댓글: 아바타 30px + 이름 13.5/600 + 시각 12px + 본문 14/1.7. 하단에 내 아바타 + textarea 3행 + "@로 멘션할 수 있습니다" + 등록(primary 34px)
   - 진행 로그: 좌측 7px 점 + 세로선(최신만 `#476CFF` 채움, 나머지 흰 배경 + `1.5px #E3E3E3`), 우측 본문 13.5px + `시각 · 작성자` 12px `#9F9F9F`. 최신순.

## 우측 레일(320px) — 카드 3개, `1px #F3F3F3` radius 10 padding 15 16, 제목 12.5/600
1. **일정** — 미니 타임라인(점 7px + 세로선). 행: 라벨 12px `#9F9F9F` / 값 12px 우측. 순서: 생성 · 시작 예정 · 시작 · 완료 예정 · 완료 · **마감기한**(파란 600). 값 없으면 `—` `#CFCFCF`. 날짜만 표기(시각 없음). 시작·완료는 전이 시 자동 기록.
2. **참고자료** (건수) — 행: 아이콘 26px(링크 `#F0F4FF`/`#476CFF`, 파일 `#F3F3F3`/`#6E6E6E`) + 제목 12.5px 1줄 + 출처·용량·작성자 11px + **삭제 X**(hover `#FFEFEF`/`#FF4E51`). 하단 "＋ 링크 · 파일 추가"(텍스트 버튼 12px)
3. **제출자료** — 참고자료와 동일 구조. 안내문 "완료 처리 시 이 자료가 결과물로 첨부됩니다."
   - `done`이면 카드 강조: 보더 `#C7EBD6`, 배경 `#F9FDFB`, 배지 `제출 완료`(`#E7F8EE`/`#15803D`), 안내문 "완료 시점에 제출된 결과물입니다."

## 데이터 형태 (목데이터 기준)
```ts
Task {
  id, title, status,                    // SPEC_state.md
  product: '메디니스', version: 'v0.0.2',
  tags: ['제품','메디니스','WBS'],
  assignee: { name:'이건학', org:'ax' }, ownerOrg: null, executionOrg: '백엔드',
  background: string, goals: string[],
  checklist: { title, done }[],
  createdAt, plannedStartAt, startedAt, plannedDueAt, doneAt, dueAt,
  wbs: { linked: true, product, version, phase, executionOrg },
  refs:  { kind:'link'|'file', title, sub }[],
  deliverables: { kind:'link'|'file', title, sub }[],
  comments: { author, at, body }[],
  logs: { at, who, text }[],
  note: string,                         // 확정된 완료 근거 / 중단·취소 사유
}
```
