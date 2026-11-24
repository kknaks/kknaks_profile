# 계약 보충 1 — K3 조각 값 이름 · 헤더 로그인 표시 (코디 · 2026-11-24)

원천 = frontend [질문] · 코디 답. backend · frontend 가 같은 글자로 맞춘다.

## 헤더 「이름 직군」 — backend 몫
- `web.render` 공통 값에 `header_staff = {name: str, job: 'nurse' | 'skincare' | 'doctor' | None}` 를 backend 가 넣는다
  - 세션 없으면 `header_staff = None` · 직군이 둘 이상이면 `job = None`(차트 담당자 칸 규칙과 같음)
- frontend 는 `base.html` 에서 `{% if header_staff %}` 이름 + 직군 글자(차트 담당자 칸과 같은 글자 · 같은 모양)
- frontend 는 `web.py` 를 고치지 않는다

## K3 — `partials/board_chart_tab.html` 넘기는 값 (frontend 가 정함 · backend 가 맞춤)
- `chart` — 차트 JSON. 걸린 줄 · 보낸 줄은 이미 보여 줄 값으로 합친 것. `tasks[].{kind}.base` · `logId` = baseLogId
- `tab` — `'assignee' | 'doctor'`
- `saved_at` — 그 탭 최근 저장 datetime | None
- `edit` — bool
- `message` — 토스트 글자. 빈 값이면 토스트를 그리지 않는다(OQ-90 — 지금은 빈 값)
- `action` — bool. 집도의 OOB(지금 board_action include 그대로)
- 409 일 때 `X-Day-Error: chart_conflict` 헤더. `HX-Reswap` 은 건드리지 않는다(조각이 target 을 바꾼다)

## K4 — `partials/board_photos.html`
- `photos` — delivery-1-report K4 그대로. 사진 서버(WP ②)는 아직 발주 전이다(사용자 확인 대기)

## 보충 2 — 자동 저장 걷어내며 깨지는 검사 (frontend [질문] · 코디 답)
- **frontend 담당 (allowed_paths 를 넓힘)**: `scripts/frontend/tests/chart-*.test.mjs` · `controllers.test.mjs` 의 차트 부분 · `scripts/frontend/bombadil/chart*.mjs` · `chart-trace(.mjs/.test.mjs)`
  - 자동 저장에만 쓰이던 것(입력 2초 묶음 저장 · 복구)은 지운다
  - 의미가 남는 것(재입력 · 닫기 · 저장 중 상태 · 네트워크 실패)은 탭 저장으로 바꾼다
  - 지운 파일과 바꾼 파일 목록을 보고에 적는다
- **backend 담당**: `scripts/devtools/verification_chart_races.py` 등 `verification_*` 중 줄 저장 경로를 검증하던 것 → 탭 저장 경로로 바꾸거나 지운다(이유를 적는다)

## 보충 3 — K4 사진 조각 (frontend 제안 · 코디 채택 · 2026-11-24 · SPEC `4d9214af` 기준)

### 조각 값
`partials/board_photos.html` 에 넘기는 값 `photos`:
```text
photos = {
  visit_id,
  edit: bool,          # board edit 권한
  reread: bool,        # 3초 안에 가져오기 작업이 안 끝나면 True
                       # → 조각이 5초 뒤 ?poll=1 로 한 번 다시 읽음 (OQ-97 기본값)
  groups: [{
    category: 'before' | 'after',
    title: '시술 전' | '시술 후',
    items: [{
      photo_id,        # visit_photo.id
      shot_at,
      kos_synced: bool # False 면 「KOS 미반영」 + [다시 시도]
    }]
  }]
}
```

### 경로 (템플릿이 만든다)
| 동작 | 메서드 · 경로 |
|---|---|
| 썸네일 · 원본 | GET `/board/visits/{v}/photos/{photo_id}/file` |
| 삭제 | POST `…/{photo_id}/delete` |
| 다시 시도 | POST `…/{photo_id}/kos-retry` |
| 올리기 | POST `/board/visits/{v}/photos` — multipart `category` · `file` · accept `image/jpeg`,`image/png` |

### 응답
- 성공: 모두 같은 조각을 `#chart-photos-{v}` 에 innerHTML 로 넣는다.
- 실패: `X-Day-Error` + `HX-Reswap: none` + 토스트 조각.
  - 토스트 글자는 OQ-88 이라 비워 둔다.
  - `message` 가 빈 값이면 토스트를 그리지 않는다.
