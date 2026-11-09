# 리뷰 리포트 — day-data-architecture / code · 시술 현황 1차 기본 권한 채우기 (2026-11-08)

대상: 커밋 `e5912d2b` 이후 미커밋 중 백엔드.
- 새 `services/default_permissions.py` · `services/emr_sync.py` diff
- 테스트 `tests/day/test_default_permissions.py` · `tests/day/emr/test_emr_sync_service.py`
- 템플릿 · CSS · `test_screen_copy.py` 는 frontend F21 몫이라 뺐다.

근거: 원천 `procedure-board-decisions.md` 「결정 — 시술 현황 1차 기본 권한」 · SPEC-002 ⑨ · ⑩ · 발주서 · `backend-perm-report.md`.
읽기 전용으로 봤다. **compose 는 건드리지 않았다.** `day_dev` 는 읽기 쿼리 한 번만 했다(SELECT · 직무 이름 · 태그 · 권한 키만).

## 판정: PASS — 커밋 가능

데모 15직무 결과가 결정 표와 **정확히 같다**(DB 실물로 확인).
- 이름 표 다섯 줄은 모두 표를 내는 데 필요하다.
- seed 는 기준 정보와 같은 transaction 안에서 돈다.
- 「없는 행만 넣음」으로 사람이 고친 값 · 지운 행이 보존된다.

아래 「참고」는 판정 밖이다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **309 passed · 158 deselected / 5.3s** |
| `uv run ruff check backend scripts` | All checks passed |
| `day_dev` 읽기(직무 이름 · 태그 · 살아 있는 권한 행) | 15직무 — 아래 표 |

### 데모 15직무 — 실물 DB ↔ 결정 표

| 직무(KOS 이름) | 태그(실물) | 실물 권한 행 | 결정 표 | 판정 경로 |
|---|---|---|---|---|
| 간호 | nurse | board=edit · board.accept=edit | 보기 · 수정 · 수락 | 태그 |
| 피부관리 | skincare | 〃 | 〃 | 태그 |
| 마취과 | (없음) | 〃 | 〃 | **이름 표** |
| 원장 | doctor | 〃 | 〃 | 태그 |
| 대표원장 | doctor · admin | 〃 | 〃 | 태그 |
| OWNER | admin · doctor | 〃 | 〃 | 태그 |
| 관리자 | admin 외 6 | 〃 | 〃 | 태그 |
| ADMIN | admin · nurse · skincare · call_counselor · coordinator | 〃 | 〃 | 태그 |
| 코디 | call_counselor · counselor · coordinator | board=view | 보기 | 태그 |
| 상담실장 | counselor | board=view | 보기 | 태그 |
| 상담총괄실장 | counselor · **admin** | board=view | 보기 | **이름 표** |
| CS팀(콜센터) | **call_counselor** | 없음 | 없음(표 「CS팀」) | **이름 표** |
| 경영지원 | **admin** | 없음 | 없음 | **이름 표** |
| 마케팅 | **admin** | 없음 | 없음 | **이름 표** |
| 촬영팀 | (없음) | 없음 | 없음 | 태그(없음) |

**15/15 일치.** 실물 태그는 DB 테스트 고정본(`test_default_permissions.py` `DEMO_ROLES`)과도 같다(「day_dev 그대로」가 사실).

## 볼 것별

| 항목 | 판정 | 근거 |
|---|---|---|
| 이름 표 다섯 줄이 정당한가 | **정당** | 굵게 표시한 태그대로면 다섯 직무가 표와 어긋난다. 경영지원 · 마케팅(admin → 전부) · 상담총괄실장(admin 포함 → 전부) · CS팀(call_counselor → 보기) · 마취과(태그 없음 → 없음). 원천 「태그만으로 안 되는 줄은 이름으로 덮는다 · 구현이 정확히 이 표를 내야 한다」에 따라 다섯 줄 모두 필요하다. 표에 없는 줄은 이름 표에 하나도 없다(넘치게 덮지 않음). SPEC-002 ⑩ 이 이 다섯 줄 · 판정 순서를 이미 반영했다(`spec-002:40 · 355-356`) |
| 판정 순서 | 맞음 | `grant_of`(`default_permissions.py:57-65`): ① 이름 표(`name.strip()` · 괄호 포함 정확히 일치) → ② 태그(FULL = nurse · skincare · doctor · admin 중 하나라도 → 전부 / VIEW = counselor · coordinator · call_counselor → 보기) → ③ 없음. 원천 태그 문구 「…만이면 보기」를 「FULL 이 없고 VIEW 가 있으면」으로 읽은 것은 같은 뜻이다 |
| 묶음 → 행 | 맞음 | 전부 = `board` edit(edit ⊇ view · `level_allows`) + `board.accept` edit / 보기 = `board` view / 없음 = 행 없음 |
| seed 가 기준 정보 transaction 안 | 맞음 | `emr_sync.run_master`(`:159-167`): `apply_master` → `default_permissions.seed` → `commit` 한 세션. KOS 받기는 그 앞, 세션 밖이다. 회차 상한(`asyncio.timeout`) · 병원 잠금 안이다 |
| 사람이 고친 값 보존 | 맞음 | `INSERT … ON CONFLICT (job_role_id, permission_key) DO NOTHING`(`:91-96`). PK 가 지운 행(`deleted_at`)도 잡으므로, 사람이 **낮춘** 수준 · **지운** 행이 다음 회차에 되돌아오지 않는다. infra `test_기준_정보_회차가_직무_기본_권한을_채우고_고친_행은_두다` — `board` 를 view 로 낮추고 `board.accept` 를 지운 뒤 다시 회차 → 0행 · 그대로 |
| 병원 경계 | 맞음 | `seed` 는 `JobRole.hospital_id == hospital_id` · 살아 있는 직무만. `job_role` 이 병원마다 따로라 다른 병원 직무를 건드리지 않는다 |
| 테스트 규칙 | 맞음 | 판정은 순수 함수 → DB 없이(데모 15 · 다른 병원 이름 · 앞뒤 공백). DB 가 보장하는 것(ON CONFLICT · PK · 같은 transaction)만 infra 1 |
| 누출 | 없음 | 로그 · 결과에 직무 이름 · 키 · 수만. 개인정보 없음 |

## 조용히 통과하는 자리

- infra 테스트의 기대값은 `defaults_for(name, tags)` 로 만든다. 그래서 「seed 가 판정 함수대로 넣는가」만 보고, 표가 맞는지는 DB 없는 15직무 테스트가 따로 지킨다. 둘이 함께라 빈틈은 없다.
- 고정본 직무가 전부/보기/없음 세 묶음을 모두 포함하는지는 단언하지 않는다(`assert roles` 만). 낮음 — `expected` 에 세 묶음이 다 나오는지 한 줄 더하면 튼튼해진다.

## 참고 (판정 밖)

1. **로그인이 기준 정보보다 먼저 만든 직무는 다음 기준 정보 회차까지 권한 행이 없다.** 로그인 `_upsert_job_role`(`services/auth.py:426-`)은 직무를 만들지만 `seed` 를 부르지 않는다. 새 병원의 첫 로그인이 기준 정보 회차보다 빠르면, 그 직원은 `/` · `/board` 에서 잠깐 권한 없음 화면을 본다(`needs_master` 발행 · 1시간 주기로 메워짐). 데모는 이미 다 채워져 해당 없음. 다듬으려면 로그인 `_finish` 의 같은 transaction 에서 그 직무 하나만 `seed` 를 부른다.
2. **「없는 행만」 정책의 한계**(구현 리포트에 정직하게 적혀 있음 · 받아들임):
   - KOS 에서 태그가 늘어 보기 → 전부가 되면 `board.accept` 만 새로 들어가고 `board` 는 view 로 남아 「보기 + 수락」 섞인 상태가 된다.
   - 표가 바뀌어도 있던 행은 안 바뀐다.
   - 제안(`source = default | manual` · migration)은 관리 화면 Delivery 에서 정할 것.
3. **이름 표는 정확히 일치**다. KOS 에서 직무 이름을 바꾸면(예: 「CS팀(콜센터)」 → 「CS팀」) 조용히 태그 규칙(보기)으로 떨어진다. 다른 병원 연결 · 이름 변경 때 코디 확인 대상(리포트 「남은 것」과 같음). 이름 표 밖으로 떨어진 admin 태그 직무를 기준 정보 회차 로그에 한 줄 남기면 눈에 띈다(낮음).
4. `JobRoleTag(t)` 는 모르는 태그 문자열이면 `ValueError` 다. 지금 태그는 mapper 가 enum 으로만 넣으니 닿지 않는다.
