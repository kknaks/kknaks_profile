# [planner] fix 스펙 7판 — 파일 저장소(Blob) 구조 + 채팅 첨부를 관리 ID 로 연결 · WP · Delivery #241 갱신

너는 **day `planner` 워커**(같은 터미널)다. 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(브랜치 `kknaksss/fix-app-re1-spec` · 1 ~ 6판 미커밋 위에 이어서). 커밋 · push · PR 금지.

사용자(2026-11-11): 「우리 스토리지도 설계해야 해. dev/prod 디렉토리 나누고 거기서 chat/passport(→ 신분증 이름) 이렇게 디렉토리 구조를 가져가야 하지 않을까」 · 「스토리지는 해결됐어. 이번에 같이 가야 하는데」 — 인프라 담당이 저장소를 만들어 줬고, **이번 작업에 같이 넣는다.**

## 읽을 것

- **저장소 안내문(인프라 담당 · 사실의 원천)**: 사용자 로컬 `~/.config/day/blob-guide-2026-11-11.md` — ⚠ **계정 이름 · 주소 · 리소스 그룹 · 구독 · VM 이름 · 로그인 계정 같은 값을 스펙 · 리포트 · Delivery 에 옮기지 않는다**(profile 레포는 PUBLIC · mediness 스펙에는 「이름은 서버 설정에」 규칙). env **이름**과 구조만 적는다.
- 지금 코드(읽기): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` — `backend/day/services/chat_storage.py`(`new_key` = `chat/{hospital_id}/{임의}.{ext}` · `BlobClient.from_connection_string`) · `common/config.py`(`day_chat_storage` · `day_chat_blob_container` · `day_chat_blob_connection_string`) · `scripts/deploy/day_vm.py`(`OPTIONAL_SECRETS` 의 `…chat-blob-connection-string`) · `deploy/config/*.env` · `deploy/compose*.yaml` · `backend/tests/deploy/test_chat_env_contract.py` · `pyproject.toml`(`azure-storage-blob[aio]` 있음 · `azure-identity` 없음)
- 지금 스펙: `20-spec/spec-004-internal-chat.md`(첨부 · 저장소 꺼짐 = 409 `photo_disabled` · 저장소 절) · `40-architecture/deployment.md`(env 표 · Blob 행 · 선택 비밀) · `20-spec/spec-000-data-model.md`(신분증 · 여권 사진 · 「법적 검토 필요」 줄)

## 사실 (바꾸지 마라)

안내문 + 코디 확인(2026-11-11):
- 컨테이너 **하나**. 인증 = **VM 의 시스템 할당 관리 ID**. 계정 키 · 연결 문자열 · SAS · 익명 접근은 **꺼져 있다** → 지금 코드의 연결 문자열 방식으로는 붙을 수 없다.
- dev · prod 서버는 같은 VM · 같은 관리 ID · 권한은 컨테이너 전체 → **폴더 분리는 정리용이지 차단이 아니다**(dev 가 prod 파일을 읽을 수 있다).
- 자동 삭제 규칙 · soft delete · 버전 관리 = 꺼짐. 브라우저 직접 업로드 · 공유 링크 · CORS 없음 → 서버가 읽어 전달(지금 채팅 구조와 같다).
- **코디 실물 확인**: dev api 컨테이너 **안에서** 관리 ID 로 저장소용 토큰을 받는 것 = 됨(IMDS 접근 OK). 컨테이너에 `azure.identity` 는 없다(의존성 추가 필요). 앱 SDK 로 올리기 · 읽기 · 지우기는 아직 확인 안 함.

## 사용자 확정 · 코디 기본값

- **사용자 확정**: 맨 위를 환경(`dev` / `prod`)으로 나눈다 · 그 아래 용도 폴더 — 채팅 `chat`, 신분증.
- **코디 기본값(통보 · 뒤집을 수 있음 — OQ 로)**:
  - 신분증 폴더 이름 = **`identity`**(여권만이 아니라 주민등록증 · 외국인등록증도 올 수 있어 `passport` 는 좁다 — 사용자가 「passport 아니면 …?」로 물었고 코디가 추천 · 답 없음).
  - 경로 = `{환경}/chat/{병원 id}/{임의 이름}.{확장자}`(지금 `new_key` 앞에 환경만 붙임 — 환경 값 = 서버 `APP_ENV`) · `{환경}/identity/{병원 id}/…` 는 **이름만 예약**(신분증 사진 기능은 이번에 없다 — 구현 · 세부 경로 · 암호화 · 보관 기간 · 열람 기록은 따로. SPEC-000 「법적 검토 필요」 그대로).
  - dev ↔ prod 차단 안 됨 = 지금은 받아들임(dev 는 데모 데이터만). 진짜 차단이 필요하면 컨테이너 분리를 인프라에 요청 — 사용자 질문으로 남긴다.
  - 보관 · 복구(soft delete) = 지금 그대로(꺼짐) · 사용자 질문으로 남긴다.

## 네가 쓸 것

### A. 스펙
1. **저장소 구조를 어디에 적나** — 채팅만의 것이 아니라 DAY 파일 저장소 전체의 규칙이다(환경 폴더 · 용도 폴더 · 병원 id · 인증 · 서버 경유 · 공개 금지 · dev/prod 공유의 한계). `40-architecture/` 의 맞는 문서(지금 `deployment.md` Blob 행 · 필요하면 새 절)에 한 곳으로 두고, SPEC-004 는 채팅 첨부가 그 규칙을 어떻게 쓰는지만 가리킨다. 같은 규칙을 두 문서에 적지 않는다.
2. **인증 · 설정 계약** — 연결 문자열 → 관리 ID. 설정 칸(계정 주소 · 컨테이너 — 비밀 아님 · env 이름은 기존 `DAY_…` 규칙)과 **없어지는 것**(연결 문자열 칸 · 선택 비밀 `…chat-blob-connection-string`)을 정한다. 로컬 개발 = 기존 `disk` 그대로인지 · 로컬에서 Blob 에 붙는 길을 둘지(안내문 「로컬 = 사용자 자격증명」) — 필요 없으면 「두지 않음」으로. 저장소 꺼짐(fail-closed) 규칙은 그대로.
3. **실패 동작** — 관리 ID 토큰을 못 받음 · 권한 없음(403) · 컨테이너 없음 · 시간 초과가 채팅 올리기 · 열기에 어떻게 보이는지를 **지금 있는 오류 코드 · 글자**로(새 글자 없음). 기동을 막는지(막지 않는 쪽이 지금 fail-closed 방식과 맞는지 판단해 적는다). AGENTS 「timeout · 동시성 상한 명시」.
4. **경로 바뀜의 파급** — 이미 저장된 키가 있는 환경이 있는지(dev 는 저장소가 꺼져 있었다 · 로컬 `disk` 는 옛 키) · 옛 키를 읽어야 하는지 · DB 에 저장된 키 칸(SPEC-000)과 `check_key` 규칙.
5. 수용 항목 — 서버 단위(가짜 저장소) · **실물**(dev 배포 뒤 dev 컨테이너에서 올리기 → 읽기 → 지우기 · 경로가 `dev/chat/{병원 id}/…` 인지 · TestFlight 에서 사진 · 동영상 보내기 · 받기 — 사용자 실기기) · 누구 몫.
6. 배포 문서: env 표 · Key Vault 선택 비밀 수(연결 문자열이 빠진다) · 새 의존성 `azure-identity` · Docker 안 관리 ID · prod 는 값만 다르고 같은 구조.
7. 정할 것(사용자 몫만 · 후보 · 추천): 신분증 폴더 이름 · dev/prod 차단 · 보관/복구 · 그 밖.

### B. 작업 계획
`/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` 에 **WP-BE-4 파일 저장소(관리 ID · 환경 경로)** 를 더한다 — 앞과 같은 틀(근거 스펙 절 · 수용 항목 · grep 으로 센 고칠 파일 — 연결 문자열 · 컨테이너 · `new_key` · `check_key` 를 **쓰는 곳 전부** · 설정 계약 시험 · 배포 스크립트 · compose · 예시 env · 문서 · 하지 말 것 · 시험 · 실물 몫). 앱 변경이 있는지 판단해 적는다(없을 것으로 본다 — 첨부가 켜지면 앱의 기존 올리기 길이 그대로 도는지 코드로 확인).

### C. Delivery #241
같은 key 로 **contract_version 을 올려** 저장소를 더한다. 더해진 것이 「파일 저장소 연결(관리 ID · 환경 경로)」뿐이고 위험 수준이 L3 그대로면, 사용자의 위 지시(「이번에 같이 가야」)를 근거로 새 plan_digest 에 승인 receipt(`human` · `kknaksss`)를 적용한다. 그 밖이 더해지거나 등급 · 조건이 달라지면 승인하지 말고 멈춰 보고한다. 2차 Delivery 는 건드리지 않는다.

## 규칙
근거 없는 정책 0 · 화면 문구 지어 넣지 않기 · 영향받는 절 전수 수정 · 개정 머리말 · `log.md` · 값(계정 이름 · 주소 · 리소스 그룹 · VM 이름 · 계정) 없음.

## 검증 · 보고
`python3 scripts/lint-pipeline.py --strict`(products/day ERROR 0).
리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-7-report.md` — 바꾼 문서 · 절 · 구조를 어느 문서에 왜 · 설정 계약(더하는 칸 · 없애는 칸) · 실패 동작 표 · 정할 것 · `wp-plan.md` WP-BE-4 요약 · 앱 변경 유무 · Delivery(version · digest · 승인) · lint.

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "바꾼 문서 / 설정 계약 / 정할 것 N건 / Delivery digest · 승인 / lint"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] planner: <질문>" --enter`
