# [planner 다음 판] WP 작성 — surface 축 구현 계획

**수정판 통과다.** 코디가 직접 검증했다 — `lint --strict` 0 error/**264** warning(늘어난 1건이 `30-work.md:247 SPEC-051 in_dev`, 바로 위 `:243` SPEC-030 동형 선례와 나란히), `node --check` 통과, **`commitDeploys` 판정부를 내가 독립 재현해 6케이스 전부 확인**(빈 surface+빈 URL → 400, 공백만 → 400, 같은환경 다른surface 통과, 같은surface 409, 다른환경 같은이름 통과, 한환경 6surface 통과), 정렬 `prod → stg` 회귀 해소, 「17 row」·「환경별 URL」 잔존 0, 리포트 16번호 누락 0.

W-12 를 한 줄로 안 끝내고 **왜 새는지**까지 적은 것, W-5 를 「카탈로그 전체로 조회하면 안 되는 이유가 이것」으로 오독 자체를 막게 바꾼 것, O-4 에 「계정 0건 행은 확인 없이」 경계를 그은 것 — 세 판단 다 좋았다.

## 이번 판 — WP 를 만든다

**사용자 지시(2026-09-22): 스펙과 WP 를 한 번에 리뷰하겠다.** 그래서 Delivery Issue 가 아니라 **WP 파일**을 만든다.

⚠ **이건 규칙 예외이고 사용자가 알고 고른 것이다.** `rules/document-pipeline.md:10` 은 「새 `30-work/work-NNN-*.md`를 만들지 않습니다」이고, 실제로 규칙 도입(2026-08-31, #648) 이후 마지막 WP 가 2026-09-01 로 3주간 신규가 없다. 그래도 만드는 이유는 **WP 는 같은 PR 에서 스펙과 함께 리뷰되고 Delivery Issue 는 그게 안 되기 때문**이다.

→ **WP §메타 에 이 사정을 한 줄 남겨라.** 「Harness v1 상 신규 실행 원장은 Delivery Issue(`rules/document-pipeline.md` §Harness v1). 이 WP 는 SPEC 과 동시 리뷰를 위해 사용자 판단으로 만든 예외다.」 나중에 왜 여기만 WP 가 있는지 아무도 모르면 그게 더 비싸다.

## 무엇을 쓰나

- **파일**: `products/mediness/30-work/work-131-deploy-surface-axis.md` (번호 131 = 130 다음)
- **doc_no**: 현재 최대가 `MEDINESS-DOC-253` 이다. **네가 직접 전수 확인하고** 비어 있는 다음 번호를 써라(린트가 전역 유일성을 본다).
- **틀**: `products/mediness/30-work/work-071-deploy-demo-env-gm.md` — **같은 SPEC(051)의 동형 선례**다. 환경 enum 에 값 하나 추가하며 DB·API·`/gm`·FE 를 함께 정합한 판이라 이번과 모양이 같다. frontmatter·절 구성·Phase 쪼개는 결·Pre-deploy Check·Rollback 의 세밀도를 **여기에 맞춰라.** 템플릿은 `templates/30-work.md` 도 함께 본다.
- **covers**: `MEDINESS-SPEC-051` / **status**: `todo`(또는 work-071 의 초기 관례를 따라라) / **owner**: 적절히

## 내용 — 스펙이 WP 로 넘긴 것들

SPEC-051 이 **의도적으로 WP 에 남긴** 결정들이 있다. 스펙 본문에서 「WP 이관」·「WP 몫」으로 적힌 자리를 **전수로 찾아** WP 가 전부 받게 해라. 최소한 아래는 들어간다:

1. **마이그레이션** — 스펙 §4 DB 가 5단계 순서를 계약으로 박았다(컬럼 추가 → `기본` 백필 → NOT NULL → 구 유니크 DROP → 확장 유니크 ADD). **번호·컬럼 타입·인덱스 컬럼 순서는 네가 정한다.** 현행 alembic 최신 리비전을 **코드 레포에서 확인**하고 다음 번호를 잡아라.
2. **모델/스키마** — `models/product_deployment.py` 의 `UniqueConstraint` 교체 + `surface_key` 컬럼. `schemas/deployment.py` 의 POST/PATCH/응답 3곳.
3. **seed idempotent 키** — ⚠ **검수가 짚은 자리다.** `seeds/deployments.py` 의 스킵 키가 `(slug, env)` 2축이라 **3축으로 안 바꾸면 재실행 때 중복이 들어온다.** 스펙엔 없는 구현 세부이니 WP 가 받아야 한다.
4. **`/gm`** — `services/gm_command.py` 정렬 3키 + 표기 규칙(그룹 행 2건 이상일 때만 surface). **기존 단일 surface 제품 출력이 한 글자도 안 바뀌는 것**이 이 Phase 의 완료 조건이다.
5. **FE** — `useDeployInfo.ts`(`usedEnvs` 소진 규칙 폐지, 중복 축 3축 교체, 클라이언트 사전검증) · `EnvBlockCard.tsx`(surface 입력, 저장 행 환경 읽기전용 칩, 표시 정렬 `prod → stg → dev → demo`, 삭제 확인). **시안이 정본이다** — `21-html/Product Management.html` 의 확정 모양대로.
6. **권한** — 건드리지 않는다. 기존 게이트 그대로라는 것을 **명시**해라(안 적으면 구현자가 손댈지 고민한다).
7. **테스트** — surface 복수·409·400·전이(2행→1행 삭제 시 `/gm` 표기 사라짐)·백필 행 조회. **스펙 §5 AC 와 1:1 로 맞춰라.**

**Phase 를 BE/FE 로 쪼개라** — work-071 처럼 「FE 가 무엇만 알면 BE 머지 전 착수 가능한지」를 §메타 병렬 항목에 적어라. 이번엔 **`surface_key` 필드명과 3축 중복 규칙**이 그 접점이다.

**Pre-deploy Check 와 Rollback 을 성의 있게 써라.** 이번 마이그레이션은 **유니크 제약을 바꾸는 파괴적 DDL** 이다 — 백필이 덜 된 상태에서 NOT NULL 이 터지면 어떻게 되는지, 롤백하면 확장 유니크로 들어간 행(같은 환경 2행)이 구 유니크에 걸린다는 것까지 적어라. **되돌릴 수 없는 지점이 어디인지**가 이 절의 핵심이다.

## 하지 말 것

- **SPEC 본문을 복제하지 마라** — link 만. WP 는 빌드 계획이지 계약 사본이 아니다.
- **`spec-051`·`21-html`·`log.md`·`30-work.md` 를 고치지 마라.** 확정됐다. (단 `30-work.md` 의 **WP 인덱스·Status Board 에 work-131 행 등재**는 필요하면 해라 — 린트 3표 동기가 요구하면.)
- **코드 레포(`mediness-app`)를 고치지 마라** — 읽기만. alembic 리비전·현행 시그니처 확인용.
- **`start-delivery` 실행 금지.**
- 커밋·push·PR 금지.

## 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec
python3 scripts/lint-pipeline.py --strict
```

- **기준선 = 0 error / 264 warning.** WP 추가로 늘어난 WARN 이 있으면 **전문을 인용하고 해소**해라(frontmatter 누락·인덱스 미등재 등은 네 몫이다). `30-work.md:247`·`:243` 의 derive WARN 2건은 **의도된 신호라 남는 게 정상**이다.
- `doc_no` 전역 유일성 직접 확인.
- WP 의 각 Phase 완료 조건이 **스펙 §5 AC 와 대응되는지** 스스로 대조해라. 대응 안 되는 AC 가 있으면 그게 구멍이다.

## 리포트

`planner-report.md` 에 **「6차 — WP 작성」** 절로 이어 붙여라. WP 가 받은 「WP 이관」 항목 전수 목록 + 스펙 AC ↔ Phase 완료조건 대응표 + 린트 수치.

끝나면 §9 완료 보고 두 채널. **코디handle 이 또 바뀌었다 — preamble 값을 믿어라.**
