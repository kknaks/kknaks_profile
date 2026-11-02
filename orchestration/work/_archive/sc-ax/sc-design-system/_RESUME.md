
# 재개 노트 — sc-design-system (sc-ax)

**지금**: 2026-09-09 PR #2 리뷰 8건 수정 push(`ef3fa96`·`be66afb`, 15커밋) + 리뷰 답글. **재리뷰·머지 대기.** 정책 2건(전사 개인정보 열람 범위 · null=비공개/없음)은 별도. archive-work 는 머지 후
**다음(다음 세션)**: ① 소속·직책 변경 command(BE) — 규칙 3개 결정 필요(이전 역할 회수 기본값 · 미래 적용일 · 겸직 해제 사유) → FE 소속/직책 Drawer + ConfirmModal → 행 메뉴 envelope ② PR(main) ③ 로그인 목록(도메인 전체 vs 4명) ④ 실제 위하고메일 150명분 오면 재적재 ⑤ 모아둔 버그(Popover ResizeObserver·옛 .org-grid CSS 정리) ⑥ 디자인 판정(1281~1440)

세팅: `scripts/new-work.sh sc-ax sc-design-system` · 설정 SSOT `config/projects/sc-ax.json`
코디handle: `term_e9a4432b-f153-45a5-97d4-63887e3329f1` (09-09 세션 재연결로 갱신 — 이전 `term_4fcd67c5…` stale)

## 워크트리

- `app`: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (branch `kknaksss/sc-design-system`, base `origin/main` → PR `main`)

## 1. 지금

- **[PR #2 리뷰 — zeroam 09-09]** 결함 8건 → 09-09 전부 수정·답글 완료. 원문:(높음 3: F1 참조자 후보 API 개인정보 노출 · F3 상세 응답 경합으로 권한 부여 대상 불일치 · F8 activity unit_id 생략 시 타 회사 기록 노출 / 중간 5: F2 후보 API has_account 항상 false · F4 activity 커서 동시각 누락 · F5 조기 회수 grant 이력 종료일 · F6 Select Esc 가 Drawer 까지 닫음 · F7 조직 전환 후 더 보기 응답 합쳐짐). 별도 판단 2건(부서 관리자의 전사 개인정보 열람 정책 · null=비공개/없음 동일 표현). 수정 발주 대기.

- 로컬 데모 DB 에 워커 검증 흔적(권한 부여→회수 사건 2건·회수 grant 1건) 남음 — 깨끗이 하려면 reset-catalog + 재적재.
- Popover 가 늦게 온 내용의 높이를 모름 → FE 가 resize 이벤트로 우회. 제대로는 Popover.tsx 에 ResizeObserver(모아서 수정 목록).

- 팝오버: 실제 소비처는 내 업무 상태필터·DatePicker 뿐. 사용자가 본 「다른 팝오버」가 있으면 다른 부품일 수 있음 — 확인 필요. 상한 420/하한 160/가장자리 8 은 코디·워커 임의값(v2 14 에 높이 규정 없음).

- **[디자인 판정]** 1281~1440 폭에서 핸드오프 3분할 최소폭 합(300+380+440+48=1168)이 본문 1080 을 넘음 → 그 구간만 비율(24%·1fr·37%)로 축소해 둠. 디자이너 확인 필요.
- 옛 조직 CSS(`.org-grid` 2열 등)는 남아 있음 — 정리는 2단계에서.

- **[사용자 필요]** 실제 위하고메일 150명분 — 오면 CSV 갱신 → `build_dataset.py` → reset-catalog·재적재(임시 `<사번>@companysc.com` 이 덮인다). 담당 프로젝트 12명분은 **보류**(사용자).
- 로컬 API 재시작 시 `AX_DEMO_EMAIL_DOMAIN=companysc.com` 을 잊지 말 것(없으면 목록 0명). wehago.com 2명은 목록에 안 뜨고 직접 입력.
- **[주의]** ax-workspace 워크트리에 코디·워커가 아닌 변경이 있음(`.gitignore` 수정, `.design-sync/`, `frontend/ds-entry.tsx`) — 「Claude code 디자인 싱크」 세션의 것으로 보임. 커밋 때 제외.
- 「부서」가 화면에 「본부」로 표시됨 — division 종류 이름은 제품 catalog 소유. 바꾸려면 별도 결정.

- **[사용자 판단 필요]** `TaskQuickActions`(WorkModals.tsx:1490)가 `task.state` 로 상태 버튼을 만든다 — rules.md 「권한은 envelope 로만」 위반. 고치려면 BE 가 DirectTask 에 `allowed_commands` 를 주는 계약 변경 선행(backend 워커 발주 + SPEC-001/002 확인). 디자인 작업 범위 밖이라 별도 결정.

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [ ] **[디자인 확장 2건 — 코드 완료·동기화 완료, 미커밋]** DatePicker.tsx·Toast tone 이 워크트리에 미커밋으로 있음(다른 코디의 backend 변경과 섞여 있으니 `frontend/` 만 골라 커밋). v2 01·14 에 DatePicker·Toast tone 등록 요청은 디자이너 전달 목록에 추가. 화면 연결(DateField→DatePicker, Toast 호출부 tone)은 별도 결정. 원문: 결정: 완료 체크 = `--accent`(초록 금지) · DatePicker 는 Popover 위 280 · 화면 연결 0. ⚠ 같은 워크트리에 타 코디(`term_64a88609`)의 backend 워커(`term_9ad0847d`)가 `backend/` 작업 중 — 경로 분리로 병행. 원문: (a) DateField 의 달력이 브라우저 기본 피커(v2 09 는 Date h38 만 정의, DateField.tsx 가 의도적으로 플랫폼 달력 사용) → 디자인 시스템 DatePicker 팝오버 신설 요청. (b) Toast 에 완료(초록 체크)·에러(빨간 x원) 아이콘 → v2 14 는 400×56 다크 + 실행취소만 정의. 둘 다 v2 에 없고 코드에도 없다 = 디자인 확장 + frontend 워커 발주 + 재동기화.

- [~] <진행 중 — 누가 · 무엇을>
- [ ] <다음 할 일>
- [!] <막힌 것 · 사용자 게이트 · 주의>

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-07 | 디자인 SoT = `docs/design/design-system-v2.dc.html` (reference/ 의 확정본과 동일). 21-screen 비어 있어 화면 명세 없음 | 사용자 지정 |
| 2026-09-07 | 디자인 v2 「요청자·담당자 없음」 전제는 sc-ax 에 맞춰 **확장** — 사람 표기 유지 | 사용자 승인(코디 권장) |
| 2026-09-07 | 홈 3열 392/600/600 · Hero 120 (디자인 내부 모순은 최신 절 기준) | 사용자 승인 |
| 2026-09-07 | 적용 순서 1차 CSS 규칙(버그2+A22) → 2차 컴포넌트(B2~B7·B13~B16) → 3차 레이아웃·반응형(B8~B12). 설정·캘린더 일/주·자료함은 새 기능 → 별도 스펙 | 사용자 승인 |
| 2026-09-07 | 1차는 PR 없이 커밋만, 바로 2차 진행 | 사용자 지시 |
| 2026-09-07 | v2 가 컴포넌트 절에서만 준 색(AI·Danger 상태색 등)은 `:root` 시맨틱 토큰으로 올린다. 디자인 01 등록 요청은 별도 | 코디 결정(사용자 확인 필요 시 번복 가능) |
| 2026-09-07 | 2차를 a(상태·폼·오버레이 프리미티브) / b(아이콘·토스트·프로그레스·테이블·그래프색) 로 직렬 분할. 안 쓰는 프리미티브는 만들지 않음 | 코디 결정 |
| 2026-09-07 | 2차-a B4+A14 는 보류(A안) — 상태 변경 `<select>` 가 없어 Popover 소비처 0. §8 popover 게이트 면제. Popover 는 2차-b 에서 툴바 '업무 유형 ▾' 칩(v2 05) 소비처로 재검토 | 워커 질문 → 코디 결정 |
| 2026-09-07 | Popover 소비처 = v2 05 툴바 「업무 유형 ▾」 칩(MyWorkPage 상태 필터). 아이콘은 라이브러리 없이 사용처만큼 손으로 그림. 그래프 15색은 값 유지·토큰화만 | 코디 결정(2차-b) |
| 2026-09-07 | 3차 B9: 내 업무의 좌측 「판단이 필요한 업무」 패널은 단일 컬럼 안 목록 위 접이식 섹션으로(A안). 상세는 이미 드로어라 이동 없음. 이 섹션은 「디자인 확장 필요」로 기록 | 워커 질문 → 코디 결정 |
| 2026-09-07 | **이 slug 의 범위를 조직도 화면 개편 + SC 조직도 시드까지 확장** — 새 slug 안 팜, 이 코디 그대로 | 사용자 지시 |
| 2026-09-07 | 사번은 **임시 번호**로 넣는다 — dataset `members.key` 를 4자리 임시 사번(CSV 순 1001~)으로 쓴다. 스키마 변경 없음. 동명이인 key 문제도 이것으로 해소 | 사용자 지시 + 코디 구현 방식 |
| 2026-09-07 | 겸임자(팀 5곳 팀장)의 주소속 = **CSV 첫 행의 팀**(GB영어+아랍). sc-org 의 GB일본 휴리스틱은 폐기 | 사용자 지시 |
| 2026-09-07 | 동명이인 2명(국내사업부 직속, 메모 「동명이인」)은 별개 인물로 각자 key | CSV 메모 |
| 2026-09-07 | 기본값: 전원 active · 대표이사는 역할만(직책 행 없음) · 부서 단계 팀장은 부서장 slot · 프로젝트 12건 미반입 · 전화·생년월일 미반입 · 경영진/기타 division | 코디 기본값(사용자 미반대) |
| 2026-09-07 | **logins 전원 생성** — 위하고메일로 로그인시킨다(조직도 매핑의 열쇠). 공통 임시 비밀번호 scax-demo-1234. 지메일 제외 | 사용자 지시(코디 기본값 「없음」 번복) |
| 2026-09-07 | members 에 phone·birth_date **옵셔널 컬럼** 추가 → 계약·적재·API 확장 → 시드 재생성·재적재. API 노출은 조직 관리 capability 보유자에게만(코디 기본값) | 사용자 지시 |
| 2026-09-07 | 담당 프로젝트 12명분 **보류** | 사용자 지시 |
| 2026-09-07 | 데모 회사 시드 제거, SC 단독. 이메일 없는 구성원은 **로컬 테스트 로그인**(`sc-<key>@scax.example`, 커밋 CSV 불변, 실제 주소 오면 옵션 없이 재생성) — 대표·부서장·팀장·팀원으로 테스트 | 사용자 지시 |
| 2026-09-07 | 테스트 로그인은 **역할별 1명, 국내사업부·경영관리부만** — 대표 1 + 인사총무팀 팀장 1 + 팀원 1 (국내사업부는 실제 메일 15명으로 충분) | 사용자 지시 |
| 2026-09-07 | 「바로 로그인」 목록 = 역할 4명(대표·부서장·팀장·팀원) 클릭 진입. 국내사업부 부서장·팀원 1명씩은 로컬 dataset 에서 테스트 주소로 **대체**(원문 CSV 불변) | 사용자 지시 |
| 2026-09-07 | **가짜 도메인 계정 금지.** 로그인 = 위하고 이메일(테이블 하나 `member_credentials`). 실제 주소 없는 150명은 `<사번>@companysc.com` 임시, 실제 주소 오면 CSV 갱신·재생성. 나열 도메인은 env 로 | 사용자 지시(코디의 scax.example 대체 3회 번복) |
| 2026-09-07 | 조직 화면 디자인 SoT = Claude Design 「SCAX」 `templates/org-chart/OrgChart.dc.html` + 핸드오프 README(사본 커밋 `7ecebdd`). 소속 변경은 모달 아닌 Drawer 840 | 사용자 지정 |
| 2026-09-07 | 1단계는 읽기 전용: BE 없는 기능(소속·직책 변경·이력·변경 기록·행 메뉴)은 그리지 않음(SPEC-005 §5). 이력 버튼만 disabled 로 | 코디 결정 |
| 2026-09-07 | 로그인 목록(도메인 전체 나열 vs 4명) 결정은 내일 | 사용자 |
| <YYYY-MM-DD> | <무엇을 정했나> | <사용자 지시 · 조사 리포트 · 리뷰 판정> |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| frontend(조사) | `term_99679654-1a7c-470e-90a8-6978c0aa6c1a` | `task_7570ab60999e` | `ctx_4af712723600` | `sc-design-system-fe-survey-brief.md` | 완료 (코디 검증 통과 — 워크트리 무변경·수치 일치) |
| frontend(1차 CSS) | `term_99679654-1a7c-470e-90a8-6978c0aa6c1a` | `task_6bde9b300f5a` | `ctx_5ec19129e35e` | `sc-design-system-fe-brief.md` | 완료 (코디 검증 통과 — diff 3파일 allowed 내·게이트 0·tsc 0·36테스트) — 커밋 `7e6fc53` |
| frontend(2차-a 프리미티브) | `term_99679654-1a7c-470e-90a8-6978c0aa6c1a` | `task_7ce30e0a668f` | `ctx_2af340f77379` | `sc-design-system-fe-2a-brief.md` | 완료 (검증 통과 — 20파일 allowed 내·tsc 0·210테스트·hex 3) — 커밋 `efc4c94` |
| frontend(2차-b 아이콘·Popover·토스트·테이블·그래프) | `term_99679654-1a7c-470e-90a8-6978c0aa6c1a` | `task_984ff78b29d9` | `ctx_0d7d2fd87626` | `sc-design-system-fe-2b-brief.md` | 완료 (검증 통과 — 23파일 allowed 내·tsc 0·224테스트·tsx hex 0) — 커밋 `d873c00` |
| frontend(3차 레이아웃·반응형) | `term_99679654-1a7c-470e-90a8-6978c0aa6c1a` | `task_289ea7289a52` | `ctx_55b222eea807` | `sc-design-system-fe-3-brief.md` | 완료 (검증 통과 — 10파일 allowed 내·tsc 0·228테스트·@media 게이트) — 커밋 `922ed65` |
| frontend(4차 DatePicker·Toast tone) | `term_e17ed244-1384-4eda-a88c-7c93b1c66ba8` | `task_cbfd248e22c4` | `ctx_cdac6f558e09` | `sc-design-system-fe-4-brief.md` | 완료 (검증 통과 — diff allowed 내(Modal·labels·styles + DatePicker·테스트·ds-entry)·tsc 0·vitest 30/30·hex 0·DateField 무변경) → 3차 동기화 업로드 완료 |
| frontend(조직 화면 조사 — 다음 작업 입력) | `term_99679654-1a7c-470e-90a8-6978c0aa6c1a` | `task_89468fcecf90` | `ctx_a2ec29ed2184` | `org-screen-survey-brief.md` | 완료 (검증 통과 — 워크트리 무변경·PII 0) → `org-screen-survey-report.md` |
| backend(SC 조직도 시드) | `term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36` | `task_f8efde827177` | `ctx_d2779f1ac158` | `sc-design-system-be-brief.md` | 완료 (검증 통과 — SC 29/165/169/22/10/3/15, 워크트리 무변경) — 변환기 프로필 커밋 |
| backend(전화·생년월일 컬럼 + 재적재) | `term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36` | `task_eef9ddfe922d` | `ctx_421276c27a8c` | `sc-design-system-be-2-brief.md` | 완료 (검증 통과 — 49테스트·SQL 15/15·API 두 계정 비교) — 커밋(ax-workspace) |
| backend(SC 단독 시드 + 테스트 로그인) | `term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36` | `task_f6e023d32412` | `ctx_5edc108cdb17` | `sc-design-system-be-3-brief.md` | 완료 (SC 단독·계정 165 검증) — 커밋 `130d4c1` |
| backend(테스트 로그인 3개로 축소) | `term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36` | `task_42bdee9b5b57` | `ctx_292495f0f8ad` | `sc-design-system-be-4-brief.md` | 완료 (테스트 계정 3 검증) — 커밋 |
| backend(바로 로그인 목록 4명) | `term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36` | `task_59ed36a28986` | `ctx_614d38726d5b` | `sc-design-system-be-5-brief.md` | 완료 (providers 4 · credentials 17 검증) — 커밋 |
| backend(전원 위하고 도메인 로그인 + 나열 도메인 env) | `term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36` | `task_e441ff64bea9` | `ctx_3b4817146727` | `sc-design-system-be-6-brief.md` | 완료 (credentials 165 · 가짜 0 · providers 163 · 22테스트) — 양쪽 커밋 |
| frontend(조직 화면 1단계 읽기 전용 v3) | `term_072aa511-0dd8-4318-8318-769bb9d30ac3` | `task_91ce4ba92648` | `ctx_8944aa0977e1` | `sc-design-system-fe-org-brief.md` | 완료 (검증 통과 — tsc 0·257테스트·게이트 0) — 커밋 `9b437bc` |
| frontend(팝오버 스크롤 버그) | `term_072aa511-0dd8-4318-8318-769bb9d30ac3` | `task_e87f6a4884c5` | `ctx_ac8f9b7c50e0` | `sc-design-system-fe-popover-fix-brief.md` | 완료 (tsc 0·45테스트) — 커밋 `010a594` |
| backend(조직 화면 읽기 API BE-1·2·6·7) | `term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36` | `task_c09e6851bdfc` | `ctx_55ab627ce16f` | `sc-design-system-be-7-brief.md` | 완료 (41+테스트·실측 두 Principal) — 커밋 `5f8b608` |
| frontend(조직 화면 2단계 — 읽기 API 소비) | `term_072aa511-0dd8-4318-8318-769bb9d30ac3` | `task_41d9710551ee` | `ctx_adb02e670e21` | `sc-design-system-fe-org2-brief.md` | 완료 (tsc 0·272테스트·게이트 0) — 커밋 `663319c` |
| frontend(리뷰 수정 F3·F7·F6) | `term_84848caa-720e-43c6-a5e8-cace7ddfd166` | `task_2a6c25451724` | `ctx_8cd5b89f7334` | `sc-design-system-fe-review-fix-brief.md` | 완료 (회귀 5·309 passed) — 커밋 `be66afb` |
| backend(리뷰 수정 F1·F8·F2·F4·F5) | `term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36` | `task_9d4f74d58ae5` | `ctx_f6af5e983fb8` | `sc-design-system-be-8-review-fix-brief.md` | 완료 (회귀 6·147 passed) — 커밋 `ef3fa96` |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- 3차 동기화(2026-09-07 21:30): DatePicker 추가 + Toast tone 스토리 → 15개, 80파일. 워커 산출 검증 후 업로드.
- 2차 동기화(2026-09-07 저녁): Popover 카드 single 모드로 수정(제품 카드에서 잘림) · TaskCalendar(WorkViews) 추가 → 14개. 앵커 갱신.
- **claude.ai/design 동기화 (2026-09-07, 코디 직접 `/design-sync`)**: 프로젝트 `SCAX` (`8fa54d76-58d6-481a-aed9-743dff9d6c09`, https://claude.ai/design/p/8fa54d76-58d6-481a-aed9-743dff9d6c09) — 프리미티브 13개·프리뷰 13개 전부 good·렌더 검사 clean·75파일. 워크트리에 **미커밋** durable 파일: `.design-sync/`(config·NOTES·conventions·previews 13·fonts) · `frontend/ds-entry.tsx` · `.gitignore` 추가분. PR 에 태울지 사용자 결정. 재동기화 절차·위험은 `.design-sync/NOTES.md`
- 조직 화면 조사: `org-screen-survey-report.md`(332줄 · 대조표 50행 · BE 제안 8 · CSV 매핑 6표 · 미결 13) + `org-v3-shots/` 3장 + `ref-spec-main/`(origin/main 스펙 사본 5개). **다음 작업(sc-org-screen) 의 입력**
- 3차: MinWidthNotice 신설, 홈 3열·List 단일 패널·여백 3단·1280 햄버거. **디자인 확장 필요(디자이너 전달)**: List 위 판단 섹션 · 홈 셋째 열 「오늘의 보고」 · 테이블 사람 열 숨김 순서 · 그래프 팔레트 15색 · AI/Danger 상태색 primitive 등록. **v2 내부 모순**: 15 「최대폭 제한 없음」 vs 04·05 「1640」(1640 따름) · 04 금지 간격 10 vs 10·14 절의 gap 10
- 2차-a/b: Skeleton·Empty·FormControls·Icon(26종)·Popover·ProgressBar 신설, :root 밖 hex 3·tsx hex 0. 대응 자리 없음: Radio·Toggle·Search·StatusDropdown·Toast 실행취소·정렬 chevron
- 1차 구현: 워크트리 `frontend/src/styles.css`(+123/-111) · `TodayPage.tsx`·`ActionCenter.tsx` 죽은 className 2줄. 리포트 오탐 4건(버튼 패딩 14·18, font-size 14·18 은 v2 값 / conflict·final 은 문자열)
- 조사 리포트: `fe-survey-report.md` (356줄 · 대조표 97행 · A1~A22 / B1~B18 · 미결 8건)

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-09-07` 저녁: SC 조직도 시드(165명) + phone·birth_date 컬럼·재적재 완료. 조직 화면 v3 조사 완료. 사용자 지시로 일시 정지(디자인 확정 대기). 워커 터미널 2개(fe `term_99679654…`, be `term_9ad0847d…`) 유지
- `2026-09-07` 사용자 요청으로 디자인 시스템 v2 를 claude.ai/design 새 프로젝트 `SCAX` 에 동기화. 워커 발주 대신 코디 세션에서 `/design-sync` 직접 실행(사용자 선택). 리포가 앱이라 `frontend/ds-entry.tsx` 엔트리 + `dtsPropsFor` 수동 작성
- `2026-09-07` 첫 워커 터미널(`term_34c6fb40…`, task_4955d835c588)이 폴더 신뢰 프롬프트에서 종료 → 새 터미널로 재발주(위 표). 옛 task 는 폐기
- `2026-09-07` 세팅: config 에 ax-workspace 추가·roles backend/frontend 신설·워크트리 생성. 조사 브리프는 사용자 「워커 써」 지시로 서브에이전트 대신 워커 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
