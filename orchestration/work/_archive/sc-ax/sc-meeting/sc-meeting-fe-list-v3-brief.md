# [frontend] 회의록 페이지 v3 — 사용자 실물 피드백 12건 (목록 · 패널 · 예약 모달 · 삭제 모달)

너는 **sc-ax frontend 워커**다. 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = 1925a76, PR #5 OPEN — 같은 브랜치에 이어 쌓는다). `frontend/` 만. 커밋 금지.

**범위는 회의록(목록) 페이지만** — `MeetingListPage.tsx` · `BookingModal.tsx` · 삭제 모달 · 그 안의 부품. 회의실(상세)·다른 페이지는 손대지 않는다(사용자: 「현재 본 페이지만 — 나중에 하나씩 보고 교체」).

## 반영할 것 — 사용자가 실물 화면(1919×936)을 보고 준 12건 (`orchestration/work/sc-meeting/design/피드백-회의록.md`)

| 1 | 왼쪽 목록 패널 `section.meeting-panel[aria-label="회의 목록"] > .meeting-scroll` (예정·지난 목록) | 패널이 내용 높이만큼만 서고(368px), 목록이 페이지 안에서 늘어남 | **패널이 화면 높이 전체를 쓴다.** 목록 영역은 패널 안에서 **투명 스크롤**(스크롤바 트랙 안 보이게, 내용만 흐름). 뷰포트 1919×936 기준 | 기록 |
| 2 | 오른쪽 회의록 패널 `section.meeting-panel[aria-label="회의록"]` (머리 `.meeting-panel-head` · 본문 `.meeting-scroll` · 푸터 `.meeting-panel-foot`) | 본문이 558px 로 서고 패널이 내용을 따라감 | **패널 전체 높이 = 화면 높이**, 3단 고정: 위 **회의 정보(머리, 고정)** / 가운데 **상세 내용(스크롤, 투명)** / 아래 **[공유] [내보내기] [회의록 열기] (푸터, 고정)**. 1 과 같은 투명 스크롤 | 기록 |
| 3 | MOD-102 예약 모달 · 날짜 `input#meeting-date` | 브라우저 기본 `type="date"` | **캘린더 컴포넌트**로(DS `DatePicker`/`DateField` 가 있음 — 그걸로 교체) | 기록 |
| 4 | MOD-102 · 시작/종료 시각 `select[aria-label="시작 시각"]` | 브라우저 기본 `<select>` 00:00~23:30 | **시간 셀렉터 공용 컴포넌트** 필요(DS 에 없음 → 새 부품 후보, 코드에 `TimeField.tsx` 있음 — 확인 후 재사용/신설) | 기록 |
| 5 | MOD-102 · 입력 칸 포커스 `input#meeting-purpose`(목적 등 전부) | 포커스 시 주변에 **파란 테두리(브라우저 focus ring)** | 파란 링 **안 뜨게**(DS 포커스 스타일로 통일) | 기록 |
| 6 | MOD-102 · 참석자 이름 찾기 결과 `PersonSearch` 팝오버 | 「이건학」처럼 직원이 없으면 결과 없이 「이건학 사외 참석자로 추가」만 뜸 | 구성: `─── 직원 정보 없음 ─── / 이건학 사외 참석자로 추가` — **「직원 정보 없음」 줄을 위에 두고** 그 아래 사외 추가 | 기록 |
| 7 | MOD-102 · 장소(회의실 목록) | 회의실 A 10인 · B 6인 · 소 4인 · 대 20인 | 목록 **맨 위에 「회의실 선택 안 함」** 항목 — 이걸 고르면 회의실 예약(the Connect) 호출을 안 함. ⚠ the Connect 예약은 SPEC §2.2 데모 범위 밖으로 둔 상태 — 「선택 안 함」 항목 자체는 넣되 호출 여부는 별건 | 기록 |
| 8 | MOD-102 푸터 · [회의실까지 예약] 버튼 | 두 버튼(회의실까지 예약 / 회의록만 생성) | **[회의실까지 예약] 버튼 제거** — 장소에 「선택 안 함」이 있으니 갈래가 필요 없음 | 기록 |
| 9 | MOD-102 푸터 · [회의록만 생성] 버튼 | 문구 「회의록만 생성」 | **「회의 생성」 하나만** — 위에서 선택·입력을 다 끝내고 아래는 버튼 하나 | 기록 |
| 10 | MOD-102 닫기 확인 `alertdialog` | 「쓴 내용을 버리고 닫을까요?」 [취소][버리기] | 문구 **「입력 정보는 저장되지 않습니다.」** · 버튼 **[취소][나가기]** | 기록 |
| 11 | 「예정」 행 삭제 모달(MOD 삭제, `alertdialog`) | 제목 「무엇을 삭제할까요?」 · 본문 「회의 삭제 시 회의 자료가 삭제되고 회의도 취소됩니다.」 · 버튼 [회의록만 삭제][회의 취소] | 제목 **「회의를 취소할까요?」** · 버튼 **[회의 취소] 하나만**(「회의록만 삭제」 갈래 제거, 본문은 그대로 두거나 한 줄로) | 기록 |
| 12 | 이 페이지 전체(목록 + MOD-102 예약 모달 + 삭제 모달)의 **모든 셀렉터·드롭다운·입력 부품** | 브라우저 기본 `<select>`·`<input type=date>` 등이 섞여 있음 | **공용 컴포넌트로 전부 교체** — DS/코드에 있는 것(`Select`·`DateField`/`DatePicker`·`TimeField`·`Popover` 등) 재사용, 없는 것은 새 공용 부품으로 세워 DS 후보에 올림(D25). **범위는 이 페이지만** — 다른 페이지는 나중에 하나씩 보며 교체 | 기록 |

## 보충 (코디)
- 1·2: 페이지가 뷰포트 높이를 채우고(shell 안 flex column, `min-height:0`) 두 패널이 세로로 꽉 찬다. 목록·본문은 패널 안 스크롤 + **투명 스크롤바**(`scrollbar-width: none` + `::-webkit-scrollbar{display:none}` — 공용 클래스 하나로, styles.css). 오른쪽 패널 3단(머리 고정·본문 스크롤·푸터 고정).
- 3·4·12: **이 페이지의 모든 `<select>`·`<input type=date>`·시각 선택을 공용 부품으로** — 있는 것 재사용(`Select.tsx`·`DateField.tsx`/`DatePicker.tsx`·`TimeField.tsx`/`TimeRangeField`·`Popover.tsx`). 30분 단위 시각은 `TimeField` 가 이미 있으니 그걸로. 새로 세우는 부품은 `src/` 최상위 + 「DS 추가 후보」 표(D25).
- 5: 포커스 링 — 브라우저 기본 outline 을 DS 포커스 스타일로 통일(전역이 아니라 이 페이지 부품 범위, 공용 부품 안에서면 부품 단위 OK).
- 6: 이름 찾기 결과가 0건일 때 첫 줄에 「직원 정보 없음」(비활성 텍스트 줄) → 그 아래 「{입력} 사외 참석자로 추가」.
- 7: 장소 목록 맨 위 「회의실 선택 안 함」 = 기본값(location null). the Connect 호출은 범위 밖 그대로.
- 8·9: 푸터 버튼 **[회의 생성]** 하나(primary) — `bookMeeting` 하나로. 「회의실까지 예약」 코드·문구 제거.
- 10: 닫기 확인 문구 「입력 정보는 저장되지 않습니다.」 [취소][나가기]. 11: 삭제 모달 「회의를 취소할까요?」 + [회의 취소](danger) 하나 — `scope=note` 갈래 UI 제거(API 는 그대로).
- 문구는 `labels.ts` 에.

## 검증
```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/meetings/ src/App.test.tsx (기존 테스트 문구 갱신 포함). 서버·5176 금지 — 실물은 코디.
```
테스트: 삭제 모달 버튼 하나 · 푸터 버튼 하나 · 장소 기본 「선택 안 함」 · 이름 0건 시 「직원 정보 없음」 줄 · 날짜/시각이 공용 부품으로 렌더.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 회의록 페이지 v3(피드백 12)" \
  --body "항목 12 처리 표 / 변경 파일 / 검증 수치 / DS 추가 후보 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 회의록 v3. 상세는 인박스." --enter
```
