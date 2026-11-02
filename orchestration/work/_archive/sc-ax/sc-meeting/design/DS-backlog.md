# DS 추가 백로그 — 회의·미팅노트에서 생긴 부품

정본 세 겹: ① Claude Design DS 프로젝트 `8fa54d76-58d6-481a-aed9-743dff9d6c09`(디자인) ② 코드 `frontend/src/styles.css` + 최상위 컴포넌트 파일(구현) ③ 코드 `docs/design/design-system-v2.dc.html`(참조본, 편입 SHA 고정).
DS 에 있는 컴포넌트(2026-09-10 manifest): Checkbox · ConfirmModal · DateField · DatePicker · Drawer · Empty · EmptyValue · FieldMessage · Icon · MinWidthNotice · Popover · ProgressBar · Skeleton · TaskCalendar · Toast (+ `.modal`·`.badge`·`.table` 류 클래스).

절차(D25): FE 워커는 화면을 만들며 DS 에 없는 부품을 **재사용 가능한 컴포넌트로 분리**해 만들고 완료 보고에 「DS 추가 후보」 표(이름 · 쓰인 자리 · props/상태 · 로컬 클래스)를 올린다 → 코디가 이 표에 적재 → 화면 WP 가 닫히면 designer 워커(DesignSync)가 DS 프로젝트에 컴포넌트로 올리고 `_ds` 번들 재수령 → 참조본 `docs/design/*.dc.html` 갱신 커밋(별건).

| # | 부품 | 출처 | 상태 | 비고 |
|---|---|---|---|---|
| DS-1 | `Icon name="pencil"` | 회의실 시안 M14 (머리 인라인 편집) | 디자인 로컬 그림 | 들어오면 한 줄 교체 |
| DS-2 | 큰 폼 모달(760, 본문만 스크롤, 머리·푸터 고정) | 회의록 시안 MOD-102 · 코드 BookingModal | `.modal` 위에 인라인 | DS 모달 기준선 600 → 폼용 변형 |
| DS-3 | **`Composer`** `src/Composer.tsx` (leading·value·onSubmit·sendLabel·disabled·error / 기본·포커스·비활성·오류) | 회의실 시안 진행 중 · 코드 MemoComposer 껍데기 | **코드 구현됨(FE P3)** `.composer`·`.composer-divider` | DS 프로젝트 등록 대기 |
| DS-4 | `line-edit` (줄 편집 행) | 회의실 시안 완료·편집 | 페이지 로컬 클래스 | |
| DS-5 | `share-table` (공유 대상 표) | 회의실 MOD-105 · 코드 ShareModal | 페이지 로컬 클래스 | |
| DS-6 | `mm-scroll` (패널 내부 스크롤 헬퍼) | 두 시안 공통 | 원본 시안 로컬 헬퍼 | 토큰화 여부 판단 |
| DS-7 | PeoplePicker(참석자 선택) | 코드 meetings/PeoplePicker | 코드만 | 시안·DS 양쪽 없음 |
| DS-8 | AgendaBlock(안건 > 줄 > 다음 할 일 블록) | 코드 meetings/AgendaBlock | 코드만 | 회의 전용이면 DS 밖 |
| DS-9 | **`GutterList`** `src/GutterList.tsx` (label·rows[{key,gutter,body,muted,active}]·gutterWidth / 기본·muted·**active**(가리켜진 줄, P4 확장)) — 같은 시각 축에 종류 다른 줄이 섞이는 목록 | 코드 LiveScript 줄 모양 | **코드 구현됨(FE P3)** `.gutter-list`·`.gutter-row`·`.gutter-meta`·`.gutter-body(.muted)` | DS 프로젝트 등록 대기 |
| DS-10 | **`StatusNote`** `src/StatusNote.tsx` (tone muted|danger · role=status) | 진행 표시 띠의 스트림·마이크 상태 | **코드 구현됨(FE P3)** `.status-note(.danger)` | DS 프로젝트 등록 대기 |
| DS-11 | **`DropZone`** `src/DropZone.tsx` (hint·pickLabel·accept·onFiles·disabled·children / 기본·over·비활성 — 받는 것을 판단하지 않음) | 회의 자료 첨부(업무 자료·요청 증빙에도 쓸 자리) | **코드 구현됨(FE P5)** `.drop-zone(.over)` | DS 프로젝트 등록 대기 |
| DS-12 | **`FileList`** `src/FileList.tsx` (label·rows[{key,name,size,reason,onOpen,onRemove,removeLabel,active}] / 기본·reason·active) | 첨부 모달 고른 파일 · 자료 탭 | **코드 구현됨(FE P5)** `.file-list`·`.file-row(.active)`·`.file-open`·`.file-name(.muted)` | DS 프로젝트 등록 대기 |
| DS-13 | **`Select`** (label·value·options[{value,label}]·onChange·disabled / 기본·열림·포커스·비활성) | 회의록 시안 v3 MOD-102 제안 카드 회차 | 디자인 로컬 규격 | `.field-select` + DS `popover`·`popover-item`. 네이티브 `<select>` 를 이 페이지에서 전부 걷어낸 자리 |
| DS-14 | **`TimeField`** (label·value"HH:MM"·onChange·step 30 / 기본·열림·포커스) | 회의록 시안 v3 MOD-102 시작·종료 시각 | 디자인 로컬 규격 | DS-13 과 트리거 규격 동일 — **Select 위의 얇은 껍데기로 세우는 쪽 권장**. 코드 `TimeField.tsx` 와 대조 필요 |
| DS-15 | `Radio` (장소 목록) | 회의록 시안 v3 MOD-102 장소 | 네이티브 + `accent-color` | DS 에 Checkbox 만 있고 Radio 가 없다 |
| DS-16 | **`DateField` 한 칸 변형** (칸 안에 날짜 + 오른쪽 안쪽 달력 아이콘 · 칸 전체가 트리거 · 표기 하이픈) | 회의록 시안 v3 항목 18 MOD-102 일시 | 디자인 로컬 규격 | 지금 DS `DateField` 는 「텍스트 칸 + 바깥 아이콘 버튼」 두 조각이라 시각 칸(DS-14)과 모양이 안 맞는다. 판은 DS `date-picker-*` 그대로 |
| — | MemoComposer · LiveScript · 진행 표시 띠(`.meeting-live-bar`) · MaterialDrawer(`.material-frame`, 안쪽은 DS `Drawer`) | meetings/ 유지 | 도메인 부품 | DS 밖 |

FE P3 이후 완료 보고마다 행을 늘린다.

## 2026-09-11 실물 테스트에서(사용자)
- **DS-17 DateField 기본값을 우리 DatePicker 로**: 지금 기본 `calendar="platform"`(OS 달력 showPicker) → 업무 요청·업무 생성·수정 요청의 「희망 기한/기한」이 크롬 기본 달력. 기본값을 `inline`(DatePicker 팝오버)으로 바꾸고 platform 갈래·숨은 `input[type=date]` 삭제 → 전 화면 일괄. 발주 task_e6d1b6a19896(09-11).
- **DS-18 Select 팝오버 위치 어긋남(표 행 안)**: 업무 화면(판단 대기 행)의 담당자 Select 가 칸에서 떨어져 아래·오른쪽으로 뜸. Popover 앵커 계산이 스크롤 컨테이너/표 안에서 틀어짐. + 그 Select 후보에 유나만 보이는 것(후보 범위) 같이 확인. 발주 task_e6d1b6a19896(09-11).
