# [frontend · 시안] 시안 v3 — 설정(수수료율) · 유입채널 · 결산 표 · PDF 명세서 · 반응형 (claude design · 코드 금지)

너는 **agency-settlement `frontend` 워커**(시안 담당). **맥락이 없다고 가정하고** 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/frontend/role.md`
- **사용자 피드백(이번 판의 SoT)**: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/feedback-2026-11-02.md` — 전부
- 앞 시안 · 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v2.dc.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-v2-report.md` · 업로드 방법 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload-instructions.md`
- 지금 구현(정본 화면 — v2 이후 바뀜): `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement/front/` · 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/shots-fe3/` — 「최종 결제만」(D-18): 머리 = 실결제 · 품목 = 최종 결제된 것만 · 취소 · 환불은 숫자만 · 1600px 가운데
- 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` 0.4.3 · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` — `front/` · `back/` 건드리지 마라.

## 만들 것 — 새 파일 1개: **`Ceramique 월별 매출 v3.dc.html`**
v2 · 지금 구현을 바탕으로, 피드백 묶음 0 ~ 7 전부:
1. **헤더 메뉴 = 「월별 조회 | 유입채널 | 설정」**
2. **설정 페이지(새로)** — KOS 상품 목록(상품 → 옵션 · 카테고리) · 상품마다 **수수료율(%)** 입력 · **달별 스냅샷**: 위에 월 선택 · 「2026년 10월 수수료율」 · 그 달 값이 정산에 쓰인다(10월 10% → 11월 30% 면 10월 자료 = 10%) · 새 달은 앞 달 값을 복사해 시작(코디 기본값) · 확정 달은 잠금(고치려면 확인) · 검색 · 카테고리 필터 · 미설정 표시 · 일괄 적용(카테고리 · 선택한 상품) · [KOS 상품 다시 받기] · 저장 상태
3. **유입채널 화면**(옛 에이전트별) — 탭 = 최초 유입 채널마다 하나(「(에이전시)」 꼬리 뗌 · 본사 · 워크인 · (없음) 포함) · 탭 줄 오른쪽 안내 문구 없음 · 요약 칩 대신 **결산 표**(채널마다 한 줄: 손님 · 결제 손님 · 실결제 · 수수료 · 미설정 품목 수 · 합계 줄) — 「전체」 탭에서 · 채널 탭에선 그 채널 결산 한 줄 + 손님 묶음
4. **품목 줄 금액 칸 = 상품 실결제 | 수수료율 | 수수료** · 머리 = 실결제 · 수수료 총액 · 미설정 = 「미설정」(수수료 0)
5. **PDF 거래 명세서** — [엑셀 내보내기] 대신 [거래 명세서(PDF)] · 「전체 내보내기」 = 채널마다 PDF → zip 하나. **명세서 한 장 모양도 그려라**(A4 · 병원 · 채널 · 기간 · 손님별 · 상품 · 실결제 · 수수료율 · 수수료 · 합계)
6. **반응형** — 데스크톱(1600) · 태블릿(1024) · 폰(390). 폰에서 표 → 카드 · 탭 → 가로 스크롤 · 설정 표 → 목록
7. 9월 ⚠ 같은 「앞 달 결제의 이 달 취소」 꼴은 ⚠ 를 띄우지 않는 모양 · 「앞 달 결제 취소」 머리 표시

## 장면
`monthly` · `channel-all`(결산 표) · `channel-one` · `settings` · `settings-month-locked` · `settings-bulk` · `statement-pdf`(명세서 한 장) · `export-zip`(전체 내보내기 확인) · 각 주요 장면의 `-tablet` · `-mobile`

## 데이터 · 하지 말 것
- 이름 · 채널 이름은 가짜(「채널A(에이전시)」 · 「본사」 같은 일반 이름은 써도 됨) · 실제 금액 금지
- 업로드: `dda9a931` 에 **새 파일 1개 추가**(사용자 허락 — 이 프로젝트 시안 추가에 한함 · 기존 파일 수정 · 삭제 금지 · 같은 이름이면 멈춤)
- 코드 · 레포 파일 수정 · 커밋 금지

## 검증 · 리포트
list_files 수 +1 · 다시 받아 바이트 대조 · node 로 장면 값 · 가짜 이름 grep · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-v3-report.md`(장면 표 · 피드백 0~7 반영 · **정할 것**(설정 화면 규칙 등) · 지금 구현과 다른 곳)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_efe97060-5339-4432-9b2d-edf35ff94a0f \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 시안 v3 업로드" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] frontend: <질문>" --enter`
