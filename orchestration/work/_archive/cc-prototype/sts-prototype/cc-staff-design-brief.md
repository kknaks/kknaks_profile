# [frontend · 시안] cc 직원 페이지 시안 — 로그인 · 코디 내원 환자 목록 · 공통 환자 상세 · 통역 모달

너는 **cc-prototype `frontend` 워커**다. 이번 판은 **코드가 아니라 claude design 시안 작업**이다(DesignSync 사용).
먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

너는 앞 맥락이 없다. 맥락은 아래 파일에만 있다.

## 1. SSOT — 먼저 읽을 것

- **결정 목록(정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/_RESUME.md` §2 — 2026-10-13 행들(페이지 3종 · 직원 페이지 두 갈래 · 환자 상세 공통 구성 · 통역 메신저형 · 의사·코디 둘만 · 버튼)
- **기존 시안(정본)**: claude.ai/design 프로젝트 `dda9a931-097f-4780-9301-972d5ac1fc23`
  - 「Ceramique 현황판 v3」(데스크 페이지 — **이번 판에 손대지 않는다**)
  - 「Ceramique 의사 모바일」(의사 직원 페이지의 바탕 — 스타일 · 컴포넌트 · 색의 기준)
  - 로컬 사본(읽기용): `/Users/kknaks/git/toy_pr2/cc-prototype/cc/design/` — `README.md` 먼저(medikit · `data-product="ceramique"` · `ceramique-theme.css` · `medikit-patches.css`)
- **데이터에 실제로 있는 칸**(시안 칸을 이 범위에서 짓는다): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-cc-data-fit-report.md` §B · §C(매핑표)
- 통역 동작(시안 설명용): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-soniox-report.md` 결론 · `research-soniox-chinese-report.md` 결론

**기대는 개념** — 해당 없음.

## 2. 배경

cc PoC(2026-10-16 지점 시연)는 페이지 3종이다 — **로그인 · 데스크 페이지(=현황판 v3, 그대로) · 직원 페이지**.
직원 페이지는 이번 PoC 에서 **의사 · 코디 두 역할만** 만든다. 두 역할은 첫 화면이 다르고 환자 상세는 같다.
**직원 페이지와 데스크 페이지(현황판)는 연결된다** — back 이 상태 하나를 들고, 현황판에서 방·직원을 배정하면 의사 일정·코디 목록에 바로 반영되고, 의사가 [진료 시작] 을 누르면 현황판의 그 방 상태가 바뀐다. 시안의 값·상태 표시는 이 「같은 상태를 두 화면이 본다」를 전제로 짓는다(현황판의 상태 이름·단계와 같은 말을 쓴다).
통역은 「본 상담은 전문 프로그램이 있고, 시술·이동 중에 **잠깐** 통역이 필요할 때 통역사를 부르지 않고 폰으로」 쓰는 기능이다.

## 3. 그릴 것 — 모바일(390px) 기준, 태블릿에서 깨지지 않게

기존 「의사 모바일」의 스타일·컴포넌트를 그대로 쓴다. 새 디자인 언어를 만들지 않는다.

1. **로그인** — 직원이 자기 계정으로 들어온다. 로그인 후 역할(의사/코디)에 맞는 첫 화면으로 간다. 데스크 페이지로 가는 길도 있어야 한다(데스크 계정 또는 선택 — 어느 쪽인지 시안에서 제안하고 리포트에 적어라)
2. **의사 첫 화면** — 기존 「의사 모바일」의 「지금 진행 중」 + 「오늘 내 일정」 부분을 그대로 쓴다. 일정 행을 누르면 3번 환자 상세
3. **코디 첫 화면 — 지금 내원 환자 목록** (새로). 코디·간호는 시술실을 돌아다니므로 「내 일정」이 없다. 지금 병원에 와 있는 환자 전부를 행으로(환자명 · 지금 위치(방) · 지금 단계/상태 · 경과 시간 · 외국인이면 국적 표시). 행을 누르면 3번 환자 상세
4. **환자 상세 — 두 역할 공통** (기존 의사 모바일의 환자 카드를 이 구성으로 재배치)
   ```
   환자명
   (오늘 예약 내역)
   [통역] [진료 시작]          ← 코디는 [통역]만. KR 국적이면 [통역] 숨김
   ──────────
   환자 차트 [펼치기]
   환자 메모 [펼치기]          ← 기존 「주의사항」 박스 자리. 메모가 여기로 들어간다
   시술 이력
   ──────────
   오늘 고객 동선
   ```
   - 내 동선(「지금 진행 중」·「오늘 내 일정」)은 의사 첫 화면에만. 환자 상세에는 넣지 않는다
5. **통역 모달** — 환자 상세의 [통역] 을 누르면 뜬다. 닫으면 환자 상세로 돌아간다
   - **메신저형**: 상대(환자) 말풍선 왼쪽 · 나(직원) 말풍선 오른쪽. 말풍선마다 원문(크게) + 번역(작게)
   - 상단: 「통역 · <언어>」 — 언어는 환자 국적으로 자동 선택, 눌러서 바꿀 수 있다 · [닫기]
   - 하단: 듣기 켜기/멈춤 버튼 하나(켜짐 상태 표시). **말하는 사람 전환 버튼은 없다**(양방향 자동 판별)
   - 상태: 연결 중 · 듣는 중 · 멈춤 · 오류(마이크 권한 없음 등) 각각 한 장
   - 위아래 분할(마주 보기) 하지 않는다

샘플 값은 **가짜 이름**으로 채운다(실제 고객 데이터를 시안에 넣지 마라). 칸 이름·종류는 §1 데이터 리포트에 있는 것으로 짓는다.

## 4. 계약

해당 없음(화면 계약은 이 시안이 확정된 뒤 SPEC 으로 쓴다).

## 5. allowed_paths — 이 밖은 건드리지 마라

- claude design 프로젝트 `dda9a931-…` 에 **새 파일 추가만**. 기존 「현황판 v3」·「의사 모바일」 및 다른 파일은 수정·삭제 금지(바탕이 필요하면 복제해서 새 이름으로)
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-staff-report.md`
- 그 외 로컬 파일 생성·수정 금지(코드 레포 포함). 커밋·push·PR 금지

## 6. 산출물

- claude design 새 파일 — 이름은 `Ceramique 직원 — <페이지>` 꼴(예: `Ceramique 직원 — 로그인`). 한 파일에 여러 화면을 묶어도 된다
- 리포트 `design-staff-report.md`:

```markdown
# cc 직원 페이지 시안 결과 (<날짜>)
## 상태: done / in-progress / blocked
## 만든 파일 — 파일명 · 담은 화면 · 원본 링크
## 화면별 설명 — §3 의 1~5 각각: 무엇을 어떻게 그렸나, 기존 시안에서 가져온 것 / 새로 만든 것
## 시안이 쓰는 데이터 칸 — 칸 → 데이터 리포트 필드 (없는 칸은 「데이터에 없음」으로 표시)
## 내가 정한 것 — 브리프가 정하지 않아 시안에서 고른 것 (코디가 사용자에게 확인)
## 이슈 · 코디가 확인할 것
```

## 7. 범위 제약 — 하지 말 것

- 코드 작성 금지(이번 판은 시안만). 현황판 v3 수정 금지
- 브리프에 없는 화면·기능을 더하지 마라(상담·피부·간호 페이지 등). 필요해 보이면 리포트 「이슈」에
- 실제 고객 데이터(이름·전화·메모 본문)를 시안에 옮기지 마라

## 8. 검증

```
§3 의 1~5 가 전부 claude design 에 있다(파일 링크) · 기존 두 시안 무수정 · 환자 상세 구성이 §3-4 순서와 같다 · 통역 모달이 메신저형(왼쪽 상대·오른쪽 나)이고 화자 전환 버튼이 없다 · 리포트 「내가 정한 것」 빠짐없음
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
  --subject "frontend(시안) 완료: <한 줄>" \
  --body "만든 파일·링크 / 요약 / 검증 결과 / 내가 정한 것 / 미결·주의점"

# (2) 직접 주입 — 코디네이터를 깨운다
orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend(시안) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 (2) 방식으로 물어라:
  `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
