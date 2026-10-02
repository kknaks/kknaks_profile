# [backend 추가 지시] 대시보드 배포 링크를 결정적으로 — 사용자 결정 2026-09-22

**Phase 1~5 통과다.** 코디가 직접 돌려 확인했다 — `test_0139_deployment_surface_key.py` **8 passed**(왕복 + down 중복가드), `test_gm_command.py` + `test_deployment.py` **57 passed**, `test_admin_deployments.py` 36 passed.

**12 failed 는 네 판정이 맞다.** 코디가 교차 확인했다 — **네가 한 글자도 안 건드린** `tests/schema/test_product_assignment_schema.py` 가 같은 사유로 9/11 실패한다(테스트 DB 의 `org_unit↔department` 매핑 seed 누락). 판정을 `orchestration/work/deploy-surface-multi/flaky-baseline-evidence.md` 에 박아 뒀으니 **다시 조사하지 마라.**

**migration 번호도 네가 맞다.** head 는 `0138_task_body_and_references` 이고 WP 의 `0124`/`0125` 가 stale 이었다(planner 가 canonical 체크아웃에서 읽었는데 그게 `origin/dev` 보다 뒤처져 있었다). 브리프가 「네가 직접 확인하라」고 한 게 이 자리다 — **WP 문서 쪽을 코디가 고친다.**

그리고 **네가 미결 ① 로 올린 대시보드 건, 사용자가 판단했다.**

## 결정 — 결정적으로만 만든다 (계약 변경 없음)

`app/services/dashboard/db_source.py:134-136` 이 배포 행을 `{slug: {env: url}}` **2축 dict** 로 접어서, 한 (제품, 환경)에 행이 여럿이면 **마지막 것이 앞을 덮고 어느 게 남는지가 조회 순서에 달려 있다.** 소비처 `ProductLinks(dev=…, prod=…)` 는 환경당 링크 한 칸이다.

**사용자 결정(2026-09-22)**: 카드는 **여전히 환경당 1개만** 보여준다. 다만 **어느 것이 뜰지를 결정적으로 고정**한다.

- 우선순위 = **`surface_key == "기본"` 인 행 우선**, 없으면 **`surface_key` 오름차순 첫째**.
- **6개를 다 보여주는 것은 스펙 판으로 남긴다** — 「대표 surface」 개념 신설은 이번 범위가 아니다. 계약을 새로 만들지 마라.
- `ProductLinks` shape 을 바꾸지 마라. `dev`·`prod` 한 칸씩 그대로다.

**⚠ 네가 「손대지 않았다」고 한 판단 자체는 옳았다** — WP §Code Surface 밖이었고 대시보드는 SPEC-100/101 소유다. 범위를 넓히는 건 코디·사용자 몫이고, 지금 그 결정이 났으니 넓힌다.

## 할 것

1. `app/services/dashboard/db_source.py` 의 접는 로직을 **결정적 선택**으로 바꿔라. 정렬을 DB 쿼리에서 할지 파이썬에서 할지는 네 재량 — 다만 **`기본` 을 sentinel 로 쓰지 마라.** 「`기본` 이면 우선」은 **표시 우선순위 규칙**이지 서버 분기가 아니다. 주석에 그 구분을 남겨라(SPEC-051 §4 Functional Rule 이 「`기본` 은 sentinel 아님」을 계약으로 갖고 있다).
2. **회귀 테스트 1건** — 같은 (제품, prod)에 surface 2~3행을 만들고 `ProductLinks.prod` 가 **항상 같은 값**(`기본` 행)인지. `기본` 이 없는 경우도 한 케이스(오름차순 첫째). `tests/services/test_dashboard_split.py` 에 붙여라(이미 네가 픽스처를 만진 파일이다).
3. 기존 대시보드 동작이 **안 바뀌는 것**도 확인해라 — 행이 1건뿐인 제품(현행 8행 전부)은 결과가 그대로여야 한다.

## 하지 말 것

- **`ProductLinks` shape·대시보드 계약을 바꾸지 마라.** 링크는 환경당 1칸 그대로.
- **「대표 surface」 개념을 만들지 마라** — 스펙 판이다.
- **`front/` 금지** (FE 워커 몫. 지금 FE 터미널은 죽었지만 변경은 워크트리에 살아 있다 — `front/` 를 건드리면 그게 날아간다).
- **12건 기존 실패를 고치려 들지 마라.** 판정 끝났다.
- **WP·SPEC 문서를 고치지 마라** — 다른 레포고 코디가 한다.
- 커밋·push·PR 금지.

## 검증

```
cd back && uv run python -m pytest tests/services/test_dashboard_split.py -q
```

**네가 만진 파일만.** 전체 스위트 금지 — 사용자 방침. 검증은 1회만.
`ruff` 도 변경 파일 한정.

## 리포트

완료 보고 본문에 ① 고친 자리(파일:줄) ② 우선순위 규칙을 어디에 어떻게 적었는지 ③ 회귀 테스트가 무엇을 고정하는지 ④ 행 1건 제품 결과 불변 확인.

끝나면 §9 완료 보고 두 채널 그대로. **코디handle 은 preamble 값을 믿어라.**
