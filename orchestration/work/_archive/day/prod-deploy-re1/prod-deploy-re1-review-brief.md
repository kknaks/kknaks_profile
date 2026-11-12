
# [reviewer] prod 첫 배포 — 운영 연결 등록 진입점 · prod 설정 시험 코드 리뷰 (#243)

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ 워크트리의 미커밋 변경(backend 워커 결과 + 코디 `deploy/config/prod.env`)을 **읽기만** 한다. 수정 · 커밋 · stash 금지. `prod.env` 값 출력 금지.

## 1. SSOT — 먼저 읽을 것

- Delivery CENTURION_DAY#243(`gh issue view 243 -R MediSolveAIDev/CENTURION_DAY`) — v1 본문. v2 request(범위 같음 + A2b 거절): planner scratchpad `prod.v2.request.json`(경로는 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/delivery-report.md` 「수정 1」)
- 스펙(mediness#933 · 브랜치 `kknaksss/prod-deploy-re1-spec`): `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/20-spec/spec-000-data-model.md` :31 · :189 · :205 · :238 · :1384 · `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/40-architecture/deployment.md` 「prod 첫 배포 절차」
- backend 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/be-1-report.md` · 브리프 `prod-deploy-re1-be-brief.md`(같은 폴더 · 「코디 결정」)

기대는 개념: 해당 없음.

## 2. 배경

DAY prod 첫 배포. 운영 병원 연결을 `is_demo=false` 로 prod api 컨테이너 안에서 넣는 진입점(`python -m day.register_connection`)과 prod 설정 계약 시험 · 레포 배포 문서. 코디 결정: 같은 이름 연결이 데모 표시가 다르면 거절(종료 · 쓰기 0) · 비밀은 env/표준입력만 · 출력에 비밀 없음 · APP_ENV 가드 없음 · `DAY_SEED_*` 재사용 안 함.

## 3. 계약

해당 없음 — migration · 모델 · 공개 API 변경 없어야 한다.

## 4. 먼저 읽을 핵심 파일

- `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1 diff` + 새 파일 `backend/day/register_connection.py` · `backend/tests/day/test_register_connection.py`
- `backend/day/services/crm_connections.py` · `backend/day/public.py` · `backend/tests/deploy/test_chat_env_contract.py` · `docs/development/deployment.md`
- `.github/workflows/deploy-prod.yaml` · `migrate-prod.yaml` · `scripts/deploy/day-deploy.sh` (문서 절차 4 · 5 대조)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 구현 단계

1. 정확성: 거절이 정말 쓰기 0 인가(브랜드 · 병원을 먼저 만들고 나서 거절하는 길이 없나) · 재실행 행 수 · 방 배정 보존 · 데모 시드 기존 동작 변화(리포트 「주의」 — 데모 시드가 운영 연결을 만나면 멈춤)가 스펙과 맞나 · 트랜잭션 커밋 위치.
2. 비밀: 출력 · 예외 메시지 · 로그 · 시험 이름/메시지에 키 · 비번 · 테넌트 · 이메일이 새는 길. 명령줄 인자로 비밀을 받는 길이 없나.
3. 컨테이너 실행 가능: 이미지(`deploy/Dockerfile` — `backend/` 만 COPY · WORKDIR `/app/backend`)에서 `python -m day.register_connection` 이 import 되고 설정을 읽는가(로컬에서 같은 cwd 로 import 만 확인 — DB 쓰기 금지).
4. 시험: `test_chat_env_contract.py` 가 prod.env 를 제대로 확인하나 · 사용자 포트 · 프로세스 건드리지 않고 `uv run pytest -q backend/tests/deploy backend/tests/day/test_register_connection.py -m "not infra"` 1회 · ruff 1회.
5. 문서 절차 4 · 5 가 워크플로 사실과 맞나.
6. Delivery Acceptance(v1 + v2 A2b) 항목별 충족 여부.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 · push · PR · Issue 댓글 금지.
- DB · 서버 · Key Vault 접속 금지 · 사용자 포트/프로세스(11040 · day-local) 금지.

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/review-code-1-report.md` — 판정 PASS/WARN/FAIL · 지적마다 파일:줄 + 근거 + 고칠 방향 · Acceptance 표.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_58369002-ab53-4e14-943b-1959a2dc71d4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
