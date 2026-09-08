# [frontend] REDRAW-07 — 버그 2건

너는 **task-management `frontend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`

> **포트 3000 을 쓰지 마라.** `PORT=3100` 으로 띄우고 3100 만 정리해라.

---

## B-1. 한글로 Enter 치면 **할일이 2개** 등록된다

**원인** — 한글 IME 조합 확정 Enter 와 `keydown` 이 **둘 다 발생**한다. 레포 전체에 `isComposing` 가드가 **0건**이다.

**고칠 것**
- `event.nativeEvent.isComposing` 이 `true` 면 **무시**한다(`keyCode === 229` 도 함께 보면 안전하다)
- **`Enter` 로 등록하는 자리를 전수로 찾아 전부 고쳐라.** 지금 아는 곳 — `TaskDetailBody.tsx` **L453 할일** · **L583 메모** · **L794**(확장). 그 밖에도 있으면 같이
- **한 곳에 모아라** — 같은 가드를 여러 파일에 복붙하지 말고 헬퍼 하나로(예: `lib/` 의 `isEnterSubmit(event)`)

**검증** — playwright 로 **한글 조합 입력**을 재현해 1건만 들어가는 것을 확인해라. 자동화가 안 되면 「자동 검증 불가」로 보고하고 넘어가라 — 되는 척하지 마라.

## B-2. 연관업무·참고자료 항목이 **박스**로 그려진다 — 시안은 **구분선 행**이다

**원인** — `components/shared/ItemRow.tsx` L39 가 `h-10 rounded-control border border-border` 로 **행마다 테두리 카드**를 그리고, `ItemRows` 가 `gap-2` 로 띄운다.
**코디가 REDRAW-06 브리프에 「항목이 행 카드」라고 잘못 적었다.** 시안을 확인하지 않고 쓴 것이다.

**시안 실측** — `업무 화면 정의서.dc.html` **L1953~1975**(드로어 참고자료·연관업무)

```
height:44px; display:flex; align-items:center; gap:9px; padding:0 16px;
border-bottom:1px solid #F1F2F5; font-size:13px
```

| | 시안 | 지금 |
|---|---|---|
| 행 높이 | **h44** | h40 |
| 테두리 | **없음** — `border-bottom 1px #F1F2F5` 만 | `border` 사방 + `rounded-control` |
| 목록 간격 | **없음**(행이 맞붙어 구분선으로 갈린다) | `gap-2` |
| padding | **`0 16`** | `px-[11px]` |
| gap | **9** | 9 ✓ |
| 글자 | **13px** | text-meta ✓ |

**마지막 행(추가)** — 시안 L1962·L1975 는 **테두리 없는 h44 행**이다(「+ 자료 첨부」·「+ 업무 연결」, 아이콘 13px + 텍스트 전체 `#9EA2AE`). **점선 박스가 아니다.** 지금 `DashedAddButton` 이 점선이면 그것도 고쳐라.

> **결과자료의 「+ 결과물 등록」만 점선**이다(시안 L1988 — `h44 · border 1px dashed #D9D9D9 · r8`). **둘을 섞지 마라.**

**대상** — `components/shared/ItemRow.tsx` · 그걸 쓰는 `TaskDetailBody` · `TaskCreateDrawer` · `AttachmentList`
**확장 페이지도 같은 규격**이다(시안 L1657~). 확장에서 항목 우측 상태 텍스트(`완료`·`진행중`)는 **그대로 둔다** — 그건 확장 시안에 있다.

---

## 검증

```bash
cd app/front && npx tsc --noEmit   # 0 에러. 1회만
```

**캡처 3장** — ① 드로어 참고자료·연관업무(구분선 행) ② 확장 페이지 같은 자리 ③ 결과자료(점선 유지 확인)

## 지킬 것

1. **이 두 건만 고친다.** 다른 자리를 손대지 마라
2. **컴포넌트 hex 리터럴 0개**
3. **`app/back/` 금지**
4. **커밋·push 하지 마라**
5. 막히면 물어라 — `orca terminal send`. `orca orchestration ask` 는 답이 안 닿는다

## Done Criteria

- [ ] 한글 Enter 로 **1건만** 등록된다(할일·메모·확장 전부)
- [ ] IME 가드가 **헬퍼 하나**에 모여 있다
- [ ] 항목 행이 **h44 · 테두리 없음 · `border-bottom #F1F2F5` · `padding 0 16`** 이고 목록 `gap` 이 없다
- [ ] 추가 행이 **테두리 없는 h44 행**이다(결과자료 점선은 그대로)
- [ ] `npx tsc --noEmit` 0 에러 · 캡처 3장

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: 버그 2건" \
  --body "IME 가드 적용 위치 / 행 규격 실측치 / 검증 방법 / tsc / 캡처 경로"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — 버그 2건. 상세는 인박스." --enter
```
