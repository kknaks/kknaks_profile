
# [researcher] cc 시술현황 — 화면 목록 · 필요한 메디킷 컴포넌트 전수조사

너는 **cc-prototype `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터와 같은 워크트리다. **리포트 파일 1개 외에는 아무것도 만들거나 고치지 마라.** 너는 앞 맥락이 없다 — 이 브리프와 아래 파일만 믿어라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-기획안-시술현황.md` ← **이번 조사의 원천.** 화면·상태·정책은 여기서만 뽑는다. 여기 없는 화면·상태는 발명하지 마라.
- `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-개요.md` · `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-개발확인.md` — 용어·범위 확인용(시술현황과 겹치는 부분만)
- `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/_첨부/` 의 html 3개 — 시술현황과 이어지는 동선이면 참고(원천은 아님)
- 메디킷 컴포넌트 원천: `/Users/kknaks/git/harness_works/medikit/src/ui/` (v1.4.0, 40종) · 스크린샷 `/Users/kknaks/git/harness_works/medikit/ds-bundle/_screenshots/`
- 메디킷 HTMX 클래스판: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.css` (`.ms-btn` · `.ms-badge` · …) — DAY 가 실제로 쓰는 것
- ⚠ **이미 만들어진 시술현황 페이지(DAY · cc-prototype 등)는 절대 참고하지 않는다** — 사용자 지시, `research-correction-1.md`

**기대는 개념**

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/para/areas/concept/design/design-system.md` — 화면은 DS 컴포넌트로 짓는다. 컴포넌트가 없는 자리는 손으로 그리지 말고 「메디킷에 없음」으로 드러낸다.

## 2. 배경 / 무엇을 바꾸나

cc 시술현황 탭 전체 화면을 OpenPencil 캔버스에 「맵」처럼 그리고, 각 화면 옆에 그 화면의 정책을 붙이려 한다. 디자인 시스템은 메디킷(CRM 테마, primary `#1d8bff`)이다.
지금 OpenPencil 문서에는 메디킷 **토큰만**(색 29 · 타이포 28 · 그림자 3) 있고 컴포넌트는 0개다. 다음 단계에서 **시술현황에 필요한 컴포넌트만** OpenPencil 로 들여온다. 이 조사는 그 범위를 정하는 원료다 — 무엇을 몇 개, 어떤 상태로 들여와야 하는지.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-기획안-시술현황.md` 전체(738줄) — 절 1~7(시술 현황 보기 · 시술 준비 · 호출 · 시술 진행 · 귀가 대기 · 관리실 기록 · 고도화)
- `/Users/kknaks/git/harness_works/medikit/src/ui/<컴포넌트>/` — 각 컴포넌트의 variant · size · state props

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`
- 리포트 파일: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/research-components.md` (이것 하나만 만든다)

## 6. 구현 단계

1. **화면 목록** — 기획안을 끝까지 읽고 시술현황 탭이 보여 주는 화면·패널·모달·상태를 **전부** 센다(grep 으로 「모달」「팝업」「패널」「토스트」「확인」「빈 상태」 등 표면을 훑어 빠진 것이 없게). 표: `screenId`(kebab-case 영문, 예 `procedure/customer-card`) · 이름 · 종류(화면/패널/모달/토스트/상태) · 기획안 절 번호 · 줄. `screenId` 는 맵에서 바뀌지 않을 키다 — 기획안 절 구조를 따라 짓는다.
2. **화면별 정책 위치** — 각 화면에 붙을 정책이 기획안 어느 줄에 있는지(줄 범위만. 정책 본문을 요약·재작성하지 마라).
3. **화면별 필요한 UI 요소** — 각 화면에 나오는 UI 요소(버튼·배지·칩·탭·표·카드·입력·모달·토스트 …)를 기획안 문장 근거와 함께.
4. **메디킷 대응** — 3의 요소를 메디킷 컴포넌트에 대응시킨다: 컴포넌트 이름 · 필요한 variant/size/state(소스 props 근거 `파일:줄`). 대응이 없으면 「메디킷에 없음」.
5. **들여올 컴포넌트 목록(합계)** — 4를 컴포넌트 단위로 모은 표: 컴포넌트 · 필요한 variant×state 조합 · 쓰는 화면 수. 정렬은 쓰는 화면 수 내림차순.
6. **정할 것** — 기획안이 모호하거나 메디킷에 없어 사용자가 정해야 하는 것만 모은다(추천안 1줄씩).

리포트 머리에 요약 3줄: 화면 수 · 들여올 컴포넌트 수(조합 수) · 메디킷에 없는 요소 수.

## 7. 범위 제약 — 하지 말 것

- 리포트 1개 외 파일 생성·수정 금지. 기획안·메디킷·DAY 레포는 읽기만.
- OpenPencil 에 그리지 마라(이번 판은 조사만).
- 기획안에 없는 화면·상태·문구를 지어내지 마라. 추정은 「추정」 표시 + 근거.
- 정책 본문을 다시 쓰지 마라 — 위치(줄 범위)만.

## 8. 검증

```
모든 행에 근거(파일:줄). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다.
기획안의 ## / ### 절 전부가 1의 표에 최소 한 번 나온다(빠진 절 0).
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 --from term_4a81aeb5-f039-46a8-a846-b1d220629f82 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
