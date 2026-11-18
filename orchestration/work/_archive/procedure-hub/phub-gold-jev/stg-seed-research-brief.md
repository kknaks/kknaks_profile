# [researcher] stg 반입 준비 조사 — 일회성 적재 · 레포 데이터 폴더

너는 **procedure-hub `researcher` 워커**다(read-only). 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/researcher/role.md`(+ 같은 폴더 문서). 회사 레포라 비밀값 · 접속 문자열 · 내부 주소 값은 리포트에 쓰지 마라(이름 · 자리만).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 작업 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(branch kknaksss/phub-gold-jev · HEAD fdc155b · base origin/release/v1.2.0) · 허브 원 레포 `~/git/PROCEDURE-HUB`(읽기 · `git show origin/<브랜치>:<경로>` 로 · checkout 금지) · 데이터 `…/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/`(silver · gold · notes · 스크립트) · 원장 `…/orchestration/work/phub-recommend/bronze/phub-ledger/`.

## 정해진 것(_RESUME §2 맨 위 11-18 「stg 시드 = 일회성 적재」 · 11-16 「stg 로 올린다」 · 11-17 SPEC-003 · SPEC-007 · 그림 결정)

- 원천 = 허브 레포(silver CSV 59 · gold 15 · ledger-check-list · 원장 JSON 21 · 그림 SVG 103 은 이미 `assets/procedure-images/`). stg = `alembic upgrade head`(새 표 76 · 기존 표 안 건드림) → `scripts/load_medallion.py --dry-run` → 적재. 배포 경로 = feat → release/v1.2.0 → stg PR → Azure 자동 배포. 머지 · 배포 · 반입은 각각 사용자 승인.

## 볼 것

1. **stg 배포 구조**: `docs/guides/deployment.md`(release/v1.2.0 · stg 브랜치 둘 다) · CI/CD 워크플로(`.github/workflows/*`) · Dockerfile · compose · 시작 명령(alembic 을 시작 때 자동으로 도나 · 누가 언제) · env 주입 방식(이름만).
2. **stg alembic 위치**: stg 브랜치(또는 stg 배포 기준 커밋)의 `alembic/versions` 머리 — 우리 `b202611170001` 의 down `b202610300001` 과 맞나 · stg 에만 있는 revision 이 있나(체인 갈림). release/v1.2.0 ↔ stg 브랜치 차이.
3. **일회성 적재를 어디서 돌리나** — 후보를 근거와 함께: ⓐ 배포된 컨테이너 안 `exec` ⓑ 같은 이미지로 일회성 컨테이너(job) ⓒ 배포 파이프라인 단계 ⓓ 그 밖. 이미지에 CSV 가 실리나(.dockerignore — 그림은 실리지 않게 해 둠) · 적재기 env(GOLD_CSV_DIR · GOLD_SILVER_DIR · GOLD_LEDGER_CHECK_PATH · GOLD_IMAGE_DIR · DATABASE_URL)를 어떻게 줄지.
4. **레포 데이터 폴더 자리 제안**: 허브 레포 안 경로 · 크기(silver 5.8MB · gold 6.3MB · 원장 1.3MB) · 레포 관례(기존 data · fixtures 폴더) · `.gitignore` · `.dockerignore` 영향 · CSV 를 만드는 스크립트(silver-supplement.py · gold-build.py · gold-check.py 등)를 같이 넣을지(추천 붙임).
5. **그림 서빙 자리**(다음 스펙 재료): stg 에 정적 파일 마운트 가능한 자리가 있나(compose volume · VM 디렉터리 · 이미지에 실기).
6. **허브 시작 모드**: stg 에서 `GOLD_REPOSITORY=db` 로 띄우는 데 필요한 env · 지금 stg 허브가 쓰는 gold 관련 env(있으면) · 빈 표 상태로 허브가 뜨면 어떻게 되나(적재 전 배포 순서 문제).
7. **되돌리기 · 갱신**: 적재 실패 시 · 다음 gold 판 갱신 절차(적재기의 「판 하나 교체」 동작 · alembic downgrade 는 쓰지 않는다 — 11-17 사고).

## 산출

`$W/research-stg-seed.md` 1개: 머리 요약 · 위 7 항목 표(근거 경로 · 커밋) · **반입 절차 초안(순서 · 누가 · 승인 지점)** · 「정할 것」(추천 붙임 · 사용자 몫만).

## 하지 마라

쓰기는 그 1개만(임시는 scratchpad). 코드 · 데이터 수정 · git checkout · 원격 push 금지. **stg 서버 · DB · Azure 에 접속하지 마라**(레포 · 문서만). 결정하지 마라.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher(stg-seed) 완료: <한 줄>" \
  --body "변경 파일 / alembic 체인 판정 / 적재 자리 추천 / 정할 것" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] researcher(stg-seed) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
