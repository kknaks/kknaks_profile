# [frontend · 시안] 매출 페이지 디자인 — claude design 새 시안 (코드 금지)

너는 **agency-settlement `frontend` 워커**(이번엔 시안 담당). claude design 작업(DesignSync). **코드 · 레포 파일 수정 금지.**
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` — **`front/` · `back/` 를 건드리지 마라.** 산출물은 아래 경로뿐.

## 1. SSOT

- 지금 구현된 화면(데이터는 붙어 있음 · 디자인은 기본): `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement/front/` — 칸 · 상태 · 배지는 여기와 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` §3 · §4.2 · §6 그대로
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md`
- **디자인 언어**: claude design `https://claude.ai/design/p/dda9a931-097f-4780-9301-972d5ac1fc23` 의 Ceramique 시안들(시술현황판 v2 등) — 같은 medikit · Ceramique 테마 · 헤더 · 컴포넌트. **기존 파일은 하나도 고치지 않는다**(새 파일 추가만)
- 형식 본보기(앞 프로젝트의 시안 브리프 · 리포트): `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/_archive/cc-prototype/myeongdong-poc-v2/myeongdong-poc-v2-design-brief.md` · `design-report.md`

## 2. 만들 것 — 새 파일 1개

**`Ceramique 월별 매출 v1.dc.html`** — 병원 내부 PC(데스크톱 가로). 같은 프로젝트에 **추가**만. 업로드 전 로컬 사본을 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/` 에 둔다.

## 3. 화면 (사용자 지시)

- **헤더에 메뉴 두 개: 「월별 조회 | 에이전트별 조회」** (지금 화면 헤더 = 로고 + 「월별 매출」 + 오른쪽 「운영 명동점 · 조회 전용」 → 메뉴 탭 형태로)
- **화면 좌우를 넓게 쓴다** — 본문 최대 폭 제한을 풀거나 크게(1440 ~ 1920 에서 표가 화면을 채운다). 칸이 좁아 줄바꿈되던 곳(최초 유입 채널 · 상품 · 옵션)이 한 줄에 보이게
- **월별 조회** = 지금 기능 그대로를 제대로 디자인: 월 선택 [‹][›] · 다시 불러오기 · 기준 시각 · 건수 줄 · 「상태는 지금 기준」 안내 · 수납 묶음 머리(결제일 · 이름 · 방문일 · 최초 유입 채널 · 수납 · 결제 수단 · 그달 결제) + 품목 줄(품목 종류 · 상품 · 옵션 · 금액 · 상태) · 취소/환불 음수 줄 · 배지(⚠ 결제 ≠ 품목 · ⚠ 통화 섞임 · 품목은 다른 달에 · 시각 없음 · 이름 없음) · 0원 구성품 줄이 덜 시끄럽게 · 상태 화면(로딩 · 빈 달 · 오류 · 잘못된 월 · 설정 없음)
- **에이전트별 조회** = 아직 기능 없음(다음 판). **시안만 가장 단순하게**: 월 + 에이전시(최초 유입 채널이 「(에이전시)」인 값) 고르기 → 그 에이전시 손님들의 수납 · 품목 줄(같은 묶음 모양) · 손님 수 · 결제 손님 수. **수수료 칸 · 합계 정책은 그리지 말고** 자리만(「수수료 — 다음 판」). 정해야 할 것은 리포트 「정할 것」에

## 4. 장면(캔버스 props `scene`)

`monthly`(섞인 상태 묶음 8~10개) · `monthly-loading` · `monthly-empty` · `monthly-error` · `agency`(에이전시 하나 골라진 상태) · `agency-empty`

## 5. 데이터

- 모양은 운영 10월 실물과 같게: 상품명 꼴 「[오픈] 울써마지 300샷」 · 「[10월 이벤트] 울쎄라피프라임300샷+써마지600샷」 · 「[첫방문] 써마지 FLX」 · 0원 구성품 · 선불카드 · 기타 상품 · 카드/현금/간편결제/선불카드
- **사람 이름 · 에이전시 이름은 전부 가짜**(예: 「에이전시A(에이전시)」 · 홍길동 꼴 가명). 실제 고객 · 에이전시 이름 · 실제 금액 금지

## 6. 하지 말 것

- 기존 시안 파일 수정 · 삭제 · 코드 · 레포 파일 수정 · 커밋 · push
- 수수료 계산 · 엑셀 · 로그인 같은 새 기능을 그리지 마라

## 7. 검증 · 리포트

- 업로드 뒤 `list_files` 로 기존 파일 수 그대로 + 새 파일 1개 · 다시 받아 로컬 사본과 같은지
- 장면마다 값이 바뀌는지(렌더를 못 보면 앞 프로젝트처럼 node 로 장면별 값 확인)
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-report.md` — 파일 · 장면 표 · §3 항목별 반영 · 지금 코드와 달라지는 곳 · 정할 것 · 가짜 이름 grep 결과

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_eb595f4c-ebea-448b-b27d-7137f208d9e5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 시안 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
