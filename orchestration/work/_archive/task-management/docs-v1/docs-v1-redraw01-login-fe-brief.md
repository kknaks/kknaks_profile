# [frontend] REDRAW-01 — 로그인 화면의 **시각만** 시안대로 고친다

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

---

## ⛔ 0. 이 work 의 성격 — 새로 만들지 않는다

**로그인 화면은 이미 완성되어 돌아간다.** 동작은 전부 구현돼 있다 —
빈 입력 비활성 · 제출 중 읽기전용 · 자격증명 실패 인라인 · 키체인 실패 토스트 · v2 게이트 · 1280 분기.
**하나도 건드리지 마라.**

**틀린 것은 시각뿐이다.** 지난 파이프라인이 시안 `.dc.html` 을 열지 않고 요약본으로 만들어서
색·크기·간격·배치가 어긋나 있다. **아래 25건을 고치는 것이 이 work 의 전부다.**

> 앞선 REDRAW-00(토큰 3파일)은 완료됐다. `--tm-canvas` · radius · 그림자 · 브랜드 그라디언트가
> 이미 시안 값이다. **그 파일들을 다시 손보지 마라** — 단, §3 의 토큰 3개만 더한다.

### 정본

| 순위 | 무엇 | 어디 |
|---|---|---|
| 1 | **사용자 승인 정정** | `orchestration/work/docs-v1/design-requests.md` §A |
| 2 | **시안 — 시각 정본** | `.dc.html` |
| 3 | **SPEC — 동작 정본** | `20-spec/spec-001-auth-session.md` |

### 반드시 열 파일 (절대경로 · 읽기 전용)

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/로그인 · 계정 · 프로필.dc.html   ← 22~111줄이 로그인
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/디자인 시스템.dc.html
```

**`00-design/*.md` 요약본은 열지 마라.** 그것이 이 사고의 원인이다.

아래 값은 코디가 시안에서 직접 뽑았다. **적힌 값과 시안이 다르면 시안이 맞다.**

> ⚠ **시안의 「설명 그림」과 「설명 문장」이 다르면 문장이 맞다.**
> 예: 07 OVERLAY 의 드로어 목업에는 `-8px 0 20px rgba(0,0,0,0.16)` 이 적혀 있지만
> 그건 150px 로 축소된 삽화다. 바로 아래 문장이 「그림자 `-24px 0 60px rgba(0,0,0,0.18)`」로 못박는다.
> **목업의 그림자·크기를 값으로 읽지 마라.**

---

## 1. 범위 — 파일 5개

| 파일 | 무엇 |
|---|---|
| `src/features/auth/components/BrandMark.tsx` | 로고 5건 |
| `src/features/auth/components/BrandPanel.tsx` | 브랜드 패널 8건 |
| `src/features/auth/components/LoginScreen.tsx` | 폼 · 푸터 11건 |
| `src/styles/tokens.css` | **토큰 3개 추가만** |
| `tailwind.config.ts` | 그 3개 연결만 |

**하지 않는 것**
- **동작·상태·문구·조건을 바꾸지 마라.** `useMutation` · `canSubmit` · `onError` 분기 · `V2Gate` 사용 · 라우팅 전부 그대로
- 컴포넌트를 쪼개거나 합치지 마라
- 다른 화면 파일을 건드리지 마라
- 토큰을 고치거나 지우지 마라 — **더하기만** 한다
- **hex 리터럴을 컴포넌트에 쓰지 마라.** 값은 토큰을 지난다

---

## 2. 고칠 것 — 25건

### BrandMark.tsx — 5건

| # | 지금 | 시안 (24~30줄) |
|---|---|---|
| 1 | `bg-primary` **단색** | **`linear-gradient(135deg,#7181F8,#A6CDFF)`** — 토큰 `--tm-brand-mark` 를 새로 만들어 담아라 |
| 2 | `h-9 w-9` (36px) | **32px** |
| 3 | "M" `text-section` (15/700) | **16 / 800** |
| 4 | 브랜드 `text-panel` (16/700) | **20 / 800 / `-0.01em`** |
| 5 | `gap-3` (12) | **11** |

> BrandMark 는 1280 구간 폼 상단에서도 쓰인다. **시안 로그인 패널 규격(32px)으로 통일한다** — 두 벌로 나누지 마라.

### BrandPanel.tsx — 8건

| # | 지금 | 시안 (24~51줄) |
|---|---|---|
| 6 | `justify-between` 3등분 | 로고 `top 64` · 헤드라인 `top 376` · 특징 `bottom 80`. **`absolute` 로 박지 말고** 유동으로 그 비율에 수렴시켜라 |
| 7 | `py-16` (상하 64) | 상 **64** / 하 **80** |
| 8 | `brand-title` lh `1.25` · `-0.03em` | lh **1.28** · **`-0.035em`** |
| 9 | 헤드라인 블록 `gap-6` (24) | **20** |
| 10 | 서브 `text-body` (15 / lh 1.65) | **16 / 400 / lh 1.7** — §3 신설 토큰 |
| 11 | **특징에 체크 타일이 없다** | 22px r6 `rgba(255,255,255,0.85)` 타일 + 체크 아이콘 12px stroke `#7181F8` 1.8, 타일↔글 `gap 11` |
| 12 | 특징 `text-meta` 13 · `#757575` | **14 / 400 / `#5F6470`** — §3 신설 토큰 |
| 13 | 특징 줄 간 `gap-3` (12) | **14** |

서브·헤드라인·특징 **문구는 그대로다.** 바꾸지 마라.

### LoginScreen.tsx — 11건

| # | 지금 | 시안 (55~110줄) |
|---|---|---|
| 14 | 폼 컬럼 `justify-center` (세로 중앙) | **`top 264`** — 중앙보다 위다. 1080 기준 비율로 잡아라 |
| 15 | 폼 `gap-6` (24) | 블록 간 **32** |
| 16 | header `gap-1` (4) | **8** |
| 17 | 부제 `text-meta` (13) | **14 / `#757575`** |
| 18 | 라벨 `text-section` (15/700) | **13 / 600** — §3 신설 토큰 |
| 19 | 눈 아이콘 크기 미지정 · `text-fg-caption`(`#9EA2AE`) | **18px** · `#B3B3B3`(`--tm-fg-placeholder`. 없으면 추가) |
| 20 | 체크박스 16px · `gap-2`(8) | **18px** · **`gap 10`** |
| 21 | 체크박스 라벨 `text-body`(15) · `text-foreground`(`#1E1E1E`) | **14 / 400 / `#5F6470`** — §3 신설 토큰 |
| 22 | 캡션 `pl-6` (24) | 체크박스 18 + gap 10 = **28** |
| 23 | 구분선 행 `gap-3` (12) | **14** |
| 24 | 「회사 계정으로 계속하기」에 **아이콘 없음** | 좌측 18px 아이콘 stroke `#5F6470` + `gap 10`. 시안 93줄의 사각형+세로선 글리프를 인라인 SVG 로 |
| 25 | 푸터 3링크 — 구분자 없음 · 폼 바로 아래 | 링크 사이 **3px 원 `#D9D9D9`** · 위치 **`bottom 56`** · `gap 16` · `12 / #9EA2AE` · hover `#757575` |

**맞아서 안 고치는 것 — 확인만 하고 손대지 마라**
- 입력칸 `h-input-lg`(48) · `rounded-control`(8) · `px-4`(16) · `text-body`(15) ✓
- 로그인 버튼 `h-cta`(50) · `text-body font-semibold`(15/600) ✓
- 「또는」 `text-caption`(12) · `#9EA2AE` ✓
- 라벨↔입력 `gap-2`(8) ✓
- 푸터 `gap-4`(16) ✓
- 실패 인라인이 비밀번호 **아래**에 붙는 것 ✓

**추가 1건 — 1280 구간 헤드라인**
`text-detail-title`(26px)을 쓰는데 **시안에 없는 값**이다. **`text-hero-date`(24 / 700 / `-0.03em`)** 로 바꿔라.
근거: 같은 화면의 폼 제목 「로그인」이 `page-title`(28)이라, 헤드라인이 그보다 크거나 같으면 위계가 무너진다. 24 는 시안 03 TYPE 에 실재하는 스케일이다.

**제출 중 문구는 그대로 둔다** — 「로그인 중…」 + `Loader2` 스핀. 이미 구현된 것이 맞다. 바꾸지 마라.

---

## 3. 더할 토큰 3개

시안 로그인이 쓰는데 디자인 시스템 03 TYPE 에 없는 조합이다. `tokens.css` 에 더하고 `tailwind.config.ts` 에 연결해라.

| 이름 | 값 | 쓰는 곳 |
|---|---|---|
| `field-label` | `13px / 600 / -0.02em` | 아이디·비밀번호 라벨 (#18) |
| `control-label` | `14px / 400 / -0.02em` | 체크박스 라벨 (#21) · 브랜드 특징 3줄 (#12) |
| `brand-body` | `16px / 400 / lh 1.7 / -0.02em` | 브랜드 서브 (#10) |

`--tm-brand-mark`(로고 그라디언트, #1)와 `--tm-fg-placeholder: #b3b3b3`(#19)도 없으면 더해라.
**기존 토큰의 값을 고치지 마라.**

---

## 4. 검증

```bash
cd app/front && npx tsc --noEmit   # 0 에러. 전체 빌드 금지, 1회만
```

자기점검 — **컴포넌트에 hex 리터럴 0개** · 동작 코드 diff 0줄 · `git status` 에 §1 의 5파일만

**캡처 3장** (`npm run dev`)
1. **1920** `/login` — 좌 브랜드 패널 + 우 폼
2. **1280** `/login` — 브랜드 패널이 사라지고 폼이 가운데, 상단에 로고 + 헤드라인 1줄
3. **1920** `/login` — 아이디·비밀번호를 채운 상태(로그인 버튼 활성)

---

## 5. 지킬 것

1. **시각만 고친다.** 동작 코드를 한 줄도 바꾸지 마라
2. **§2 에 없는 것을 고치지 마라.** 「이것도 이상해 보인다」는 고치지 말고 **완료 보고에 적어라**
3. **막히면 물어라** — `orca terminal send`. `orca orchestration ask` 는 답이 안 닿는다
4. **시안에도 SPEC 에도 없으면 물어라.** 추측하지 마라
5. **커밋·push 하지 마라**

## 6. Done Criteria

- [ ] 25건 전부 반영, 각 항목이 시안 값과 일치
- [ ] 토큰 3(+2)개 추가, **기존 토큰 값 변경 0**
- [ ] 동작 코드 diff **0줄** (`useMutation`·`canSubmit`·`onError`·`V2Gate`·라우팅)
- [ ] 컴포넌트 hex 리터럴 0개
- [ ] `npx tsc --noEmit` 0 에러
- [ ] `git status` 에 5파일만
- [ ] 캡처 3장

---

## 7. 질문하는 법 — **`orca orchestration ask` 를 쓰지 마라**

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[질문] frontend: <질문>" --enter
```

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 / 25건 각각 반영 결과 / 추가 토큰 / 동작 diff 0줄 근거 / tsc / 캡처 경로 / 눈에 띄었지만 안 고친 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
