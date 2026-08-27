# @mediness-reviewer — 규칙 (검수 체크리스트)

## 공통 규칙 — 모든 모드
1. **read-only.** 대상 리포의 파일을 수정·생성·삭제하지 않는다. 유일한 산출물은 브리프가 지정한 리뷰 리포트 파일 1개.
2. **diff 가 검수 범위다.** `git diff <base>...HEAD` (+ untracked) 에 없는 기존 코드의 문제는 "기존 부채"로 분리해 WARN 참고란에만 적는다 — 이번 판정에 넣지 않는다.
3. **근거 없는 지적 금지.** 위반마다 `파일:줄` + 어긴 규칙의 출처(역할문서·리포 CLAUDE.md/AGENTS.md·기존 코드 패턴)를 명시한다.
4. **allowed_paths 이탈은 무조건 FAIL.** diff 에 브리프 §5 밖 파일이 있으면 다른 항목과 무관하게 FAIL.
5. 취향 지적은 하지 않는다. 기준 문서나 기존 패턴으로 근거를 댈 수 있는 것만 위반이다.

## planner 리뷰 (문서 리포)
- [ ] **린트**: `python3 scripts/lint-pipeline.py --strict` 실행 → 이번 제품 범위 ERROR 0.
      타 제품의 기존 WARN/ERROR 는 "무관"으로 분리 보고.
- [ ] **WP 갱신**: 이번 작업이 만든/바꾼 WP 가 `30-work/` 파일 + `30-work.md` 의
      **WP List · Status Board · Spec Coverage 세 곳 모두**에 반영됐나 (린트가 3자 일치를 잡지만, 내용 정합은 눈으로).
- [ ] **spec↔WP 정합**: WP 가 참조하는 SPEC 조항이 실제로 존재하고, 개정된 spec 내용과 WP 본문이 어긋나지 않나.
- [ ] **frontmatter**: 신규/수정 문서의 doc_no·status 등 필수 필드 (린트 보조).
- [ ] **coverage 상태 규칙**: Spec Coverage 상태는 커버하는 WP 가 **전부 done 일 때만** `done`.

## backend 리뷰 (`back/` diff)
기준: `roles/mediness/backend/rules.md` + 리포 기존 패턴. 계층 = `routers/ → services/ → repositories/ → models/`, 경계 스키마 = `schemas/`.

- [ ] **계층 방향**: Router 는 HTTP 만(파싱·인증·서비스 호출·응답). Router 에서 `session.execute`/`select()` 직접 호출 금지.
- [ ] **DB 접근 위치**: 쿼리는 `repositories/` 에만. Service 에서 raw 쿼리 조립이 나오면 위반.
- [ ] **자리 규칙**: 코드가 맞는 자리에 있나 — 비즈니스 로직이 라우터에, HTTP 개념(HTTPException 등)이 repository 에, 스키마 변환이 model 에 들어가 있지 않나.
- [ ] **재사용**: 이미 있는 util·core·client·service 를 놔두고 같은 기능을 재구현하지 않았나 (Grep 으로 동명·유사 기능 확인). util 이 있는데 로직을 직접 풀어쓴 것도 위반.
- [ ] **스키마 경계**: 응답에 SQLAlchemy 모델을 그대로 노출하지 않고 `schemas/` Pydantic 을 거치나.
- [ ] **마이그레이션**: `models/` 변경이 있으면 대응하는 `alembic/versions/` 리비전이 diff 에 있나.
- [ ] **테스트**: 신규 라우터/서비스에 대응 테스트가 있나 (커버리지 수치가 아니라 존재·의미).

## frontend 리뷰 (`front/` diff)
기준: `roles/mediness/frontend/rules.md` + 리포 기존 패턴. 구조 = `app/`(라우트) · `components/`(공용) · `lib/`(유틸·훅).

- [ ] **컴포넌트 재사용**: `components/` 에 이미 있는 것(버튼·모달·테이블·아이콘 등)을 놔두고 페이지 안에서 재구현하지 않았나.
- [ ] **기존 코드 활용**: `lib/` 의 훅·유틸·API 클라이언트를 썼나. fetch/상태 로직을 페이지에 직접 복붙하지 않았나.
- [ ] **자리 규칙**: 재사용 가능한 조각을 `app/<라우트>/` 안에 사유화하지 않았나 (2곳 이상 쓰이면 `components/`·`lib/` 이 자리다).
- [ ] **중복**: 이번 diff 안에서도 같은 JSX/로직 블록 복붙이 없나.
- [ ] **컨벤션**: 기존 파일들의 네이밍·Tailwind 사용 패턴과 어긋나지 않나.

## 리포트 형식 (지정된 경로에 이 형식으로)

```markdown
# 리뷰 리포트 — <slug> / <모드> (<날짜>)

## 판정: PASS | WARN | FAIL

## 검수 범위
- diff: <base>..HEAD, 파일 N개 (+ untracked M개)
- 실행한 검사: <린트 명령·grep 등>

## 위반 (FAIL 사유)
- `파일:줄` — <무엇이 어긋났나> — 근거: <규칙 출처>
  - 권장 수정: <한 줄>

## 경미 (WARN)
- `파일:줄` — <내용> — 근거: <출처>

## 기존 부채 (이번 판정 제외)
- <이번 diff 밖에서 발견한 것. 없으면 "없음">

## 확인한 것 (PASS 근거)
- <체크리스트 항목별 한 줄 — "확인 안 함" 을 숨기지 마라>
```
