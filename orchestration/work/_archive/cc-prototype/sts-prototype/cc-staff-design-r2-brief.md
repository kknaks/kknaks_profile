# [frontend · 시안 r2] 직원 시안 수정 — 환자 상세 재구성(안 A) · 중복 제거 · 메모 접기 폭 버그

너는 **cc-prototype `frontend` 워커**다. 이번 판도 **claude design 시안 작업**이다(DesignSync). 코드는 쓰지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 나머지)

앞 판(r1) 브리프와 네 리포트가 맥락이다. 앞 판을 기억하지 못하면 이 파일들부터 읽어라.

## 1. SSOT — 먼저 읽을 것

- **결정(정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-002-cc-poc.md` — 특히 **D-09**(가짜는 고객명뿐 — 메모 본문 속 고객·동행인 이름도 가짜로) · **D-20 · D-22 · D-23**(환자 상세 구성 · 아웃 시각)
- **피드백 모음**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-feedback-batch-1.md` — #1 · #3 · #4 전부 이번 판에서 고친다
- **실데이터 조사(환자 상세의 재료)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-patient-detail-report.md` — 결론 · §A(메모별 실제 양식·예시) · §D 안 A
- **실제 데이터**(샘플 값을 여기서 가져온다): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/raw/getScheduleDetail/` 중 **2026-10-09** 일정
- 앞 판: `cc-staff-design-brief.md` · `design-staff-report.md` (같은 폴더)
- 시안: claude.ai/design 프로젝트 `dda9a931-097f-4780-9301-972d5ac1fc23` — 네가 만든 `Ceramique 직원 - 로그인` · `- 의사` · `- 코디` · `- 통역 모달 상태`

**기대는 개념** — 해당 없음.

## 2. 배경

r1 환자 상세는 실제 값을 보지 않고 필드 이름으로만 지어서 (1) 상단 카드와 「환자 차트」가 같은 정보를 두 번 보였고 (2) 메모 다섯 종 중 둘만 넣었다.
이건 r1 브리프가 「실제 값 금지」를 잘못 넣은 탓이다(코디 잘못). **이번엔 실제 10-09 데이터의 메모·시술 값을 그대로 샘플로 쓰고, 고객(·동행인) 이름만 가짜로 바꾼다.**

## 3. 고칠 것 — `Ceramique 직원 - 의사` · `- 코디` 의 환자 상세(두 파일 같은 구성)

D-22 그대로 위에서 아래로:

1. **상단 카드** — 가짜 이름 · 국적 칩 · 성별·나이 · 첫 방문/재방문 / 예약 시각 · 상태 · 지금 방 · **아웃 시각**(D-23) / 상담실장 · 원장 / [통역][진료 시작](코디는 [통역]만 · KR 이면 [통역] 숨김). **차트번호 없음**
2. **환자 메모**(기본 펼침)
   - ① **⚠ 주의** — 오더 메모와 상담 메모 사본 **양쪽**의 `[특이사항]`·`[임플란트 여부]`(값 있을 때) + 메모 앞에 덧붙인 `**…**`·`★` 줄. 비면 칸 자체를 숨긴다
   - ② **오늘 오더** — `orderMemo` 의 시술 번호 줄(제품·샷·부위) + 마취크림
   - ③ **상담 요약** — 상담 메모의 `------` 위쪽(고민·타 병원 이력·거부·예산)
   - ④ **접수 메모** — `reservationMemo`(통역·동행·유입·촬영 거부 등)
   - 역할별 기본 펼침: **의사 = ②③ 펼침 · ④ 접힘 / 코디 = ④ 펼침 · ②③ 접힘(②는 마취 시간 한 줄은 보이게)**. ①은 항상 펼침
   - 각 칸에 출처(어느 메모 · 누가 썼나)를 작게
3. **환자 차트**(접힘) — 유입처 · 예약 그룹 · 동행 · 보유 시술권 · 선불 잔액 · 오늘 결제 품목. **값 없는 줄은 숨김.** 성별·나이·국적·차트번호·오늘 시술 넣지 않는다(상단 카드와 중복 금지)
4. **시술 이력** — 「첫 방문」 표시 + 상담 메모의 타 병원 이력(「받은시술 / H)」 줄)
5. **오늘 고객 동선** — 작업 순서 · 방 · 담당 · 상태 · 시각, 끝난 작업 옆에 담당자 메모

**샘플 값**: 10-09 일정 중 메모가 풍부한 고객 4~6명을 골라 **실제 메모 원문**(오더·상담·예약·담당자 메모 · 실제 시술명 · 실제 직원 이름)을 쓴다. ⚠ 주의가 있는 고객(예: 상담 사본에만 `[특이사항]` 이 있는 경우)을 최소 1명 넣는다. 의사 첫 화면 일정·코디 내원 목록의 행도 이 고객들로 맞춘다.

**버그**: 환자 메모를 접으면 화면 가로폭이 전체적으로 좁아진다(피드백 #1) — 접고 펴도 폭이 그대로이게.

로그인 · 통역 모달 · 의사 첫 화면 레이아웃은 바꾸지 않는다(샘플 값만 위에 맞춘다).

## 4. 계약

해당 없음.

## 5. allowed_paths — 이 밖은 건드리지 마라

- claude design 의 **네가 만든 4개 파일**(`Ceramique 직원 - …`) 수정. 「현황판 v3」·「의사 모바일」 및 다른 파일 수정·삭제 금지
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-staff-r2-report.md`
- 그 외 로컬 파일 생성·수정 금지. 커밋·push·PR 금지

## 6. 산출물

리포트 `design-staff-r2-report.md`:

```markdown
# 직원 시안 r2 결과 (<날짜>)
## 상태: done / in-progress / blocked
## 고친 파일 · 링크
## 피드백 대조 — batch-1 #1·#3·#4 각각 어떻게 고쳤나
## 환자 상세 칸 → 데이터 필드 (D-22 순서대로)
## 쓴 샘플 — 10-09 어느 일정(일정 id)에서 무엇을 가져왔나 · 이름 치환 규칙
## 내가 정한 것 — 코디가 사용자에게 확인
## 이슈
```

## 7. 범위 제약 — 하지 말 것

- **가리는 것은 고객·동행인 이름뿐**(로마자 · 「이름 :」 줄 · 한글 음역 포함, 가짜 이름으로 치환). 전화번호가 메모에 섞여 있으면 그 번호만 `010-****-****` 꼴로. 차트번호는 화면에 없다(D-09). 그 밖의 실제 값은 그대로 쓴다
- 브리프에 없는 칸·화면을 더하지 마라. 필요해 보이면 리포트 「이슈」에
- 코드 작성 금지. KOS API 호출 금지

## 8. 검증

```
의사·코디 두 파일의 환자 상세가 §3 1~5 순서 · 상단 카드와 차트에 같은 정보 0건 · ⚠ 주의 칸이 오더·상담 양쪽에서 모였음(예시 고객 1명 이상) · 역할별 기본 펼침이 §3-2 와 같음 · 메모 접기/펴기 때 폭 변화 없음 · 시안에 실제 고객·동행인 이름 0건(10-09 visitor.name 과 메모 속 이름 대조) · 기존 두 시안 무수정
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령의 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_a10169a1-7391-473c-a46f-c08315dd6775 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(시안 r2) 완료: <한 줄>" \
  --body "고친 파일·링크 / 요약 / 검증 결과(이름 대조 포함) / 내가 정한 것 / 미결·주의점"

# (2) 직접 주입 — 코디네이터를 깨운다
orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend(시안 r2) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 (2) 방식으로 물어라:
  `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
