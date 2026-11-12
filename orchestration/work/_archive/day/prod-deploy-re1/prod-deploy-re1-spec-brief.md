
# [planner] prod 첫 배포 — 운영 연결 등록 경로(OQ-01-2 닫기) · prod 설정 시험 · Delivery Issue 발행

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` 은 **읽기만**(backend 워커가 나중에 쓴다). 거기 `deploy/config/prod.env` 는 코디가 이미 채운 미커밋 변경이다 — 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `products/day/20-spec/spec-000-data-model.md` — §3 01 `crm_connection.is_demo`(:187) · 「환경」(:229 ~ :235) · **OQ-01-2**(:1381)
- `products/day/40-architecture/deployment.md` — :78(dev/prod 분리 = 스키마에 넣는 연결 데이터) · :215(Key Vault) · :235(prod 실제 병원 연결 — 안 정함)
- Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`
- 3차 발행 기록(형식 참고): `git -C /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app show origin/main:orchestration/work/_archive/day/fix/delivery-report.md`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

DAY prod 서버를 처음 올린다(같은 VM · `day_prod` 스키마). Key Vault prod 비밀 8개 · `prod.env` 일반 설정은 코디가 끝냈다. 남은 코드 두 건을 Delivery 하나로 묶는다.

1. **운영 연결 등록 경로** — `crm_connection` 행을 만드는 길이 데모 시드(`scripts/seed_demo_connection.py` → `services/crm_connections.py` `seed_demo_kos_connection`) 하나뿐이고 `is_demo=True` 가 고정이다. 사용자 결정(2026-11-11): **운영용으로 따로 — 「데모」 표시 없이**(`is_demo=false`) 넣는다. Docker 이미지에 `scripts/` 가 없으므로(`deploy/Dockerfile` 은 `backend/` 만 COPY) **prod api 컨테이너 안에서 돌릴 진입점**(`backend` 안 모듈 · `python -m …`)이 있어야 한다. 값(open 키 · 테넌트 · 시스템 계정 · 방 배정 id · 브랜드 코드/이름 · 병원 이름)은 env/표준입력에서만 읽는다. 이것으로 **SPEC-000 OQ-01-2 를 닫는다**.
2. **배포 계약 시험** — `backend/tests/deploy/test_chat_env_contract.py:83` `test_prod_서버_채팅_설정은_아직_비움` 이 prod.env 채팅 · APNs 6칸이 비었는지 본다(3차의 임시 잠금). prod 값이 들어갔으니 dev 시험(:89)처럼 「prod 는 정식 앱만 받고(`day.medisolveai`) · 공개 주소 `https://day.medisolveai.com` · 데모 넘김 주소 = dev 공개 주소 · 저장소 blob 켜짐 · 컨테이너 `prod` · Key ID 와 Team ID 함께」를 확인하도록 바꾼다.

사용자가 정한 값(스펙에 적을 것 — 고객 값 · 키는 적지 않는다): prod 시스템 계정 · 데모 계정 · 전체 권한 계정은 `prod.env`/연결 값(레포 밖) · 브랜드 코드 `ceramique` · 병원 = 실제 병원 1곳 · 방 배정 id 는 연결 설정 값.

## 3. 계약

해당 없음(BE↔FE 없음). 공개 API 변경 없음 · migration 없음.

## 4. 먼저 읽을 핵심 파일 (코드 워크트리 · 읽기만)

- `backend/day/services/crm_connections.py` — `seed_demo_kos_connection`(is_demo 고정)
- `scripts/seed_demo_connection.py` · `scripts/set_room_assign_etc_task.py` — 지금 진입점
- `deploy/Dockerfile` — 이미지에 들어가는 것
- `backend/tests/deploy/test_chat_env_contract.py:28 · :83 · :89`
- `docs/development/deployment.md` — 레포 쪽 배포 문서(정본은 mediness deployment.md)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 스펙 개정: SPEC-000 OQ-01-2 를 사용자 결정으로 닫고(운영 연결 = 운영용 등록 진입점 · `is_demo=false` · prod api 컨테이너 안에서 1회 · 값은 레포 밖) · `is_demo` 설명(:187 「데모 시드가 true」)에 운영 등록은 false 를 더한다. `deployment.md` :235 행을 같은 내용으로 고치고, prod 첫 배포 절차(Key Vault 8 · prod.env · migrate-prod · deploy-prod · 운영 연결 등록 · KOS IP 허용)를 레포 사실대로 적는다. 사실이 아닌 것 · 정하지 않은 것을 지어 넣지 마라.
2. 리포트에 스펙 변경 요약을 남긴 뒤, **Delivery Issue 를 발행**한다(`mediness start-delivery --mediness-repo <이 워크트리> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1 --github-repo MediSolveAIDev/CENTURION_DAY` — `--plan` → `--apply`). baseline 은 스펙 PR 머지 전이라 pending 이어도 된다. Target Delta = 위 두 건 + 스펙 개정 · Non-Goals = migration 없음 · 공개 API 변경 없음 · 앱 변경 없음 · 웹 버그 없음 · prod 배포 실행 자체(코디 몫).
3. **승인 receipt 는 적용하지 마라** — 승인은 사용자 몫이다. plan_digest 와 승인 대기 상태를 보고한다.

## 7. 범위 제약 — 하지 말 것

- 코드 워크트리 수정 금지 · 커밋 · push · PR 금지.
- 고객 값(병원 이름 외) · 키 · 토큰 · 비밀번호 · 계정 이메일을 스펙 · Issue 에 적지 마라.
- 화면 문구를 지어 넣지 마라.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/delivery-report.md` (Issue 번호 · URL · 라벨 · risk · digest · baseline · 스펙 변경 파일:줄)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_c4381756-d7e6-4556-923a-c9e239892740 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
