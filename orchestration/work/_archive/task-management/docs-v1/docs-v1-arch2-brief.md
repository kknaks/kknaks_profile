
# [architect] 아키텍처 ② — 프론트 + ① 정정 반영

너는 **task-management `architect` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**⚠ 이 워크트리는 코디네이터와 공유한다.** §5 가 지정한 파일 외에는 **만들거나 고치지 마라.** git 은 읽기만.

**⚠ 아키텍처 ①(system·database·backend)은 이미 커밋됐다.** 네가 쓴 문서다. 이번엔 **프론트를 새로 쓰고, ① 문서 중 정정 대상만 고친다.**

## 1. SSOT — 먼저 읽을 것

경로는 전부 `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/` 기준.

**① 산출물 (네가 이어받을 계약)**
- `para/projects/summer-star/task-management/40-architecture/backend/README.md` — 특히 **§10 API 표면(schema 계약의 형태)**·§6 비동기 API·§8 에러 규약
- `.../40-architecture/system/README.md` — 구성·흐름 3종
- `.../40-architecture/database/README.md` (+ `domains/`) — 데이터 모델

**정책 (닫힌 계약)**
- `.../10-decision/decision-001~006-*.md` 여섯 건 — 특히 DEC-001 **§v2 스코프**, DEC-002 §4 완료 게이트, DEC-003 §4 2트랙·증분 반영, DEC-005 §3·§4 schedule·드래그 규격
- `.../00-baseline/baseline-001~006-*.md`

**분석·결정**
- `orchestration/work/docs-v1/docs-v1-design-report.md` — **§3.2 라우트 트리 제안**·§3.3 레이아웃 계층·§4 shadcn 매핑 C-01~49·§5 공용 컴포넌트 S-01~34·§2 화면 P-01~72
- `orchestration/work/docs-v1/design-requests.md` — **§C 기술 선택**(정적 빌드·shadcn·유동 반응형·Bearer·웹 우선)과 정정 A-1~15
- `.../00-design/09-design-tokens.md` · `08-responsive.md` · `디자인 시스템.dc.html` — 토큰·반응형 원본

## 2. 배경 / 무엇을 바꾸나

①에서 시스템·DB·백엔드를 세웠다. 이번엔 **프론트 구조와 컨벤션**을 세운다. 코드 워커가 이 문서만 읽고도 같은 방식으로 화면을 만들 수 있어야 하고, 리뷰어가 이걸 기준으로 판정한다.

**동시에 ① 문서 두 곳을 정정한다** — 발주 후 사용자 결정으로 뒤집힌 것들이다(§3 참조).

## 3. ① 정정 — 반드시 반영할 것

발주 ① 이후 확정된 사항이라 네 문서가 낡았다. **`database/` 와 `backend/` 를 고쳐라.**

### 정정 1 — `schedule` 은 파생이다 (가장 중요)

네가 「시간은 `schedule` 이 단독 소유」로 잡았는데 **뒤집혔다**(DEC-005 §3, 2026-09-05 개정):

| 사실 | 원본(소유) | schedule |
|---|---|---|
| 업무의 **기한** | **업무 `due_date`** — 리스트 정렬·D-day 를 **조인 없이** 읽는다 | 기한이 있으면 **종일 일정**으로 파생 |
| 업무에 시간까지 지정 | 업무 | 시간 일정으로 파생 |
| 회의 일시 | **회의록** | 시간 일정으로 파생 |

- `schedule` 이 갖는 것은 **시간축 배치뿐**(`start_at`·`end_at`·`is_all_day`). 도메인 속성(기한)을 담지 않는다
- **단방향** — 캘린더 드래그는 **원본을 고치고** 그 결과가 `schedule` 로 내려온다
- 캘린더 조회·겹침 검사가 `schedule` 한 테이블에서 끝나는 이점은 **유지**한다(분리한 이유)
- ERD·도메인 문서(`task.md`·`meeting.md`·`calendar.md`)의 불변식(T-1·M-1·C-1·SCH-1 등)을 이 방향으로 고쳐라

### 정정 2 — OQ 10건 해소 반영

네가 남긴 OQ 는 **전부 답이 나왔다**. 해당 절과 OQ 표를 갱신하라(이미 표기해 둔 것과 어긋나지 않게 본문도 맞춰라):

| OQ | 결정 |
|---|---|
| DB-OQ-1 | **URL 링크 첨부 허용** — 첨부는 「자료함 문서(md) \| URL 링크」. `kind`+`url` 을 연다 |
| DB-OQ-2 | **`account.work_start_at`/`work_end_at` 제거** — v1 에 쓰는 곳이 없다 |
| DB-OQ-3 | **AI 안건도 `track='ai'` 에만** — 회의 중 사람 탭에 보이지 않는다. 공유 축 + `origin` 안은 폐기. 종료 후 통합본에서 합친다 |
| DB-OQ-4 | `document.origin` 컬럼 유지, v1 배지 미표시 |
| BE-OQ-1 | **AI 증분 즉시 반영** + 반영된 배치 회차 표시(「배치 2회 → 3회 → 종결」). 버퍼링 없음 |
| BE-OQ-2 | `pendingChange` = **기한(업무 `due_date`)** · 상태(완료는 게이트) · **note = 업무 메모에 새 항목 추가** |
| BE-OQ-3 | **무소속 회의 → 무소속 업무**를 웜스타트 컨텍스트로 |
| SYS-OQ-1 | 마이크는 **웹 `getUserMedia`**. Tauri 확인은 래핑 시점 |
| SYS-OQ-2 | **v1 타깃은 macOS · Windows 둘 다** |
| SYS-OQ-3 | 오디오 포맷은 **Soniox 지원 형식 중 구현 시점 결정** — 특정 포맷에 묶지 마라 |

### 정정 3 — 웹 우선 개발

**개발은 웹(브라우저) 기준이고 Tauri 래핑은 마지막**이다(2026-09-05 확정). system 문서가 Tauri 셸을 상시 전제로 그렸다면, **Tauri 는 배포 단계 포장**임을 드러내라. 특히 refresh 토큰 보관 — 래핑 후엔 OS 키체인, **웹 개발 중에는 브라우저 저장소로 임시 대체**하되 **저장소를 한 곳(토큰 저장소 추상화)에서만 다뤄 교체가 한 파일에서 끝나게** 한다.

## 4. 프론트 아키텍처 — 담을 것

`frontend/README.md` 를 새로 쓴다. 최소한 이것들:

1. **라우트 트리 확정** — 리포트 §3.2 제안을 **확정으로 승격**한다. 정적 빌드(`output: 'export'`)라 동적 라우트는 `generateStaticParams` 또는 쿼리로 처리해야 하니 그 규칙까지. 드로어에 URL 을 줄지(리포트 Q-29)도 **여기서 정한다**
2. **디렉토리 구조·명명** — `components/ui`(shadcn 생성물) / **공용 컴포넌트 S-01~34** / 영역별 컴포넌트 / 훅 / API 클라이언트 / 타입. 어디에 무엇을 두는지 **한 가지 방식으로**
3. **데이터 페칭·상태** — 서버가 없으므로 전부 클라이언트. 페칭 라이브러리를 **하나 고르고 근거를 달아라**. 캐시 키 규약, 낙관적 갱신을 쓰는 자리(캘린더 드래그·상태 변경), 에러 표면화(백엔드 §8 에러 코드 → 화면). **`{ items: [...] }` 응답 규약**(backend §10) 소비 방식
4. **인증 연동** — Bearer 헤더 부착, access 만료 시 refresh 재시도, **토큰 저장소 추상화**(§3 정정 3)
5. **토큰 → CSS 변수 → shadcn 테마** — `09-design-tokens.md` 의 색·타입·간격을 CSS 변수로 옮기는 규칙. **동적 유형 색**(설정에서 고른 팔레트)은 토큰이 아니라 런타임 값이니 그 처리도
6. **오버레이 3종 공통 프레임** — Drawer 840 / Modal 600 / Popover 200–400. **「편집은 드로어, 결정은 모달」·「드로어 위에 모달을 겹치지 않는다」를 컴포넌트로 강제**하는 방법
7. **유동 반응형 규약** — 1920 실측 좌표는 **참고값**이고 absolute 로 박지 않는다(A-13). 브레이크포인트, 여백 240→80→48, 최소 폭, 드로어가 좁은 화면에서 전체화면이 되는 규칙(F-6)
8. **실시간 처리** — 회의 스트림 WS(`backend §10`) 소비: 오디오 업로드, 토큰 스트림 렌더(**잠정 토큰은 갱신·확정 토큰은 append**), AI 증분 즉시 반영 + 배치 회차 표시
9. **v2 스코프 표시** — UI 는 그리되 비활성 + 「v2에서 제공됩니다」 토스트(DEC-001 §v2 스코프). **공통 컴포넌트로** 처리하는 방식
10. **테스트·품질 규약** — 무엇을 검증하고 무엇을 하지 않는지

## 5. allowed_paths — 이 밖은 건드리지 마라

경로는 `para/projects/summer-star/task-management/40-architecture/`.

**신규**
- `frontend/README.md`

**수정 (정정 대상만)**
- `database/README.md` · `database/domains/*.md`
- `backend/README.md`
- `system/README.md`

그 외 일체 금지. **`40-architecture/README.md`(인덱스)·log·index·정책서·기획서·디자인 원본은 코디네이터 소관 — 건드리지 마라.** 커밋·push 금지.

## 6. 구현 단계

1. 역할 문서 → §1 SSOT.
2. **§3 정정 먼저** 반영한다(schedule 파생 · OQ 10건 · 웹 우선). 정정이 프론트 설계의 전제가 된다.
3. `frontend/README.md` 를 §4 순서대로 쓴다.
4. 자기점검(§8) → 완료 보고(§9).

## 7. 범위 제약 — 하지 말 것

- 코드를 만들지 않는다(스캐폴딩·컴포넌트·설정 파일 일체). **문서만.**
- 정책(DEC-001~006)을 다시 논의하거나 어기지 않는다. 충돌은 고치지 말고 Open Questions.
- **미설계 화면(`design-requests.md §B`)은 구조 결정을 막지 않는다** — 화면 규격이 필요한 자리만 「디자인 대기」로 표시하고 나머지 구조는 확정해서 써라.
- 선택지를 나열하고 끝내지 않는다 — **하나로 정하고 근거를 단다.**
- ① 문서를 §3 이외의 이유로 고치지 마라.

## 8. 검증

```
산출물은 브리프가 지정한 파일들뿐. DEC-001~006 을 어기는 구조를 제안하지 않았는지 자기점검(충돌 발견 시 고치지 말고 Open Questions). 사용자가 못박은 스택·계층 제약 준수. 결정마다 근거(DEC-00x §y · P/C/S/F/Q-xx) 병기, 선택지를 남기지 말고 단일 방식으로 서술
```

추가 자기점검 — 보고에 결과를 적어라:

- **§3 정정 3건이 전부 반영**됐나. 특히 `schedule` 이 파생으로 바뀌었고, `task`·`meeting` 쪽 불변식이 그에 맞게 고쳐졌나
- ①에 남긴 **OQ 10건이 전부 닫힌 것으로** 갱신됐나 (본문과 OQ 표가 어긋나지 않게)
- 프론트 문서에 §4 열 항목이 다 있나
- 라우트·디렉토리·페칭이 **단일 방식**으로 서술됐나(선택지 나열 금지)
- **정적 빌드 제약**(서버 컴포넌트 런타임 페칭·Route Handler·미들웨어 없음)이 라우트·페칭 설계에 반영됐나

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] architect 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] architect: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
