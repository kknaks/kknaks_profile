# WP-131 BE — 승인 카드 본문 확장 (WBS 등록 + task.draft)

사용자 반려: **WBS 업무 등록 승인 카드가 4칸(버전·PHASE·업무·담당자)뿐**.
코디 확장: 카드 본문의 정본 컬럼 세트 = **웹 Task 생성 모달(`ManualTaskCreateRequest`)과 동일**.
코디 판정(2026-09-01): ① 빈 **메타** 행은 아예 싣지 않는다 · «미기재» 는 **배경·목표 두 자리 전용**
② 라벨은 레일 정본 사전 — «시작 예정»·«완료 예정»·«마감기한». FE 는 서버 행 그대로 렌더.

> ⚠ **front/ 는 손대지 않았다**(FE 병렬). migration 0건 — 전부 기존 컬럼·기존 seam.

---

## 1. 정본 컬럼 세트 — 어디서 어디로

| 축 | 카드(review_surface) | 승인 착지(`tasks`) |
|---|---|---|
| 배경 | `background` 슬롯 (**비면 «미기재»**) | `tasks.background` |
| 목표 | `goal` 슬롯 (**비면 «미기재»**) | `tasks.goal` |
| 체크리스트 | `checklist: [{title, sort_order}]` (비면 부재) | `task_check_items` |
| 요청자 | fact «요청자» | `created_by_member_id` |
| 참조자 | fact «참조자» | `task_ccs` |
| 시작 예정 | fact «시작 예정» | `planned_start_at` |
| 마감기한 | fact «마감기한» | `due` |
| 완료 예정 | fact «완료 예정» | `expected_completion` |
| owner 조직 | fact «owner 조직» | `owner_org_unit_id` |
| 실행 조직 | fact «실행 조직» | `execution_org_unit_id` |
| 제품·버전 | fact «버전»(제품 포함) | `product_slug`·`product_version_id` |

메타 축(요청자~조직)은 **값이 있을 때만 행이 선다**. 배경·목표는 **비어도 슬롯이 서고 «미기재»**.
가르는 기준: 「그 빈칸이 무언가를 가르치는가」 — 배경·목표는 이 라운드가 에이전트에게 채우라고
시킨 자리라 비었다는 사실 자체가 정보고, 메타 축은 말 안 하면 없는 것이 정상이다.

---

## 2. 변경 파일 (16 · +835/−80)

### MCP
- `mcp/app/tools/wbs_task_create.py` — 인자 6 추가: `background`·`goal`·`start_date`·`due_date`·
  `expected_completion`·`cc_member_ids`. 빈 값은 **키를 안 보낸다**(«미기재» ≠ «명시적으로 비움»).
  날짜는 왕복 전에 `YYYY-MM-DD` 선검증(인자 이름으로 사유를 말한다).
- `mcp/app/tools/wbs_task_update.py` — `background`·`goal` 추가(`description` 은 구 이름, 저장 자리 동일).
- `mcp/app/server.py` — 두 툴 시그니처 + **툴 설명에 «대화 문맥에서 채워라 — 비우면 카드에 «미기재» 로
  뜬다»** 명시. 「사용자가 말한 것은 옮겨 담되 지어내지 않는다」도 함께.
  ⚠ 인자 이름은 `due` 가 아니라 **`due_date`** — `wbs_task_update_tool` 과 같은 어휘로 맞췄다.
  ⚠ `checklist` 는 새로 만들지 않고 **기존 `check_items`** 를 그대로 쓴다(같은 것에 이름 두 벌 금지).

### 스키마 / 서비스
- `back/app/schemas/version_wbs.py` — `WbsTaskCreateRequest` +`background`·`goal`·`expectedCompletion`·
  `cc`·`ownerOrgUnitId`. `WbsTaskPatchRequest` +`background`·`goal`.
- `back/app/services/version_wbs.py`
  - `create_task` work_item 분기: **계획일 거절을 걷었다**(구 422 「WBS 생성에서는 계획일을 받지
    않습니다」 — 그 자리에서 채팅 발 기한이 통째로 유실됐다). phase 확장은 **기존
    `ensure_wbs_projection` → `_expand_phase`** 가 그대로 한다(새 확장 경로 0).
  - canonical seam(`create_task_with_cc`)에 background/goal/planned_start_at/due/expected_completion/
    cc_member_ids/owner_org_unit_id 전달 — **전부 그 함수의 기존 인자**다.
  - owner 조직 미지정 → **실행 조직(부모 phase)** 으로 앉힌다(초안 승인 실행과 같은 규칙).
  - `patch_task`: `background`·`goal` 반영 + `task_log` 문구.
- `back/app/services/version_wbs_status.py` — `write_background`(=`write_description` 과 같은 컬럼) ·
  `write_goal` · 공개 별칭 `as_utc`(생성/수정이 **같은 date→datetime 변환**을 쓴다).

### wbs_task 워크플로
- `const.py` — fact 라벨 7 + `UNSPECIFIED="미기재"` + 슬롯 키 3(초안 카드와 **같은 키**).
- `surface.py` — 접수가 **표시명을 확정해** payload 에 싣는다(담당자에서 배운 규율의 확장):
  `requester_label`·`cc_labels`·`owner_org_label`·`execution_org_label`·날짜 3종·본문 3종.
  실행이 읽는 원값은 같은 payload 의 `request` 스냅샷이 그대로 나른다.
- `workflow.py` — `_meta_fact`(값 있을 때만 행) · `_attach_body`(배경·목표는 항상, 체크리스트는
  있을 때만) · `_create_preview`. 수정 카드는 `always=False` — 안 보낸 필드에 «미기재» 를 세우면
  「이 승인이 배경을 비운다」로 읽힌다.

### task.draft (SPEC-155) — 동형
- `const.py` — 「시작」→**「시작 예정」**, 「마감」→**「마감기한」**, `FACT_REQUESTER` 신설,
  `BODY_UNSPECIFIED="미기재"` 신설.
- `workflow.py` — `_meta_row`(사유 없는 맨 「미지정」은 **행째 제거**, 사유 붙은 것은 유지) ·
  배경·목표 슬롯 **항상 발신** · `requester_label` 을 content 에 실어 카드가 「누가 시켰나」를 말한다.
- 배경·목표·체크리스트는 **이미 실리고 있었다**(SPEC-155 §6.5) — 확인 결과 계약대로였다.

---

## 3. 테스트

| 파일 | 결과 |
|---|---|
| `back/tests/services/engine_v2/test_wp116_wbs_task_workflow.py` | 8 → **14 passed** (+6) |
| `back/tests/services/engine_v2/test_ax_task_card_fields.py` | **28 passed** (3 정정) |
| `back/tests/services/engine_v2/test_ax_task_draft.py` 외 3 | **green**(계약 전환분 2건 정정) |
| `mcp/tests/` 전량 | **539 passed** (+2 신규, 1 정정) |
| 영향 스위트 합산(back 9파일) | **243 passed / 25 failed — 25는 전부 pre-existing** |

신규 단언:
- **본문 4축+**: 등록 카드가 모달 컬럼 세트 전량을 싣는가(facts 11 + 슬롯 3 + preview).
- **승인 착지**: `create_task` 가 canonical seam 에 background/goal/checklist/due/planned_start/
  expected_completion 을 그대로 넘기는가 + owner==execution.
- **미기재(빈 값)**: ⓐ 빈 메타 축은 **행이 없다** ⓑ 빈 배경·목표는 **«미기재» 슬롯이 선다**
  ⓒ **원장에는 `None` 이 앉는다**(«미기재» 문자열이 `tasks.background` 에 저장되면 안 된다).
- **레일 사전 대조**: wbs_task ↔ task_draft 상수를 실제로 비교(문장으로 두면 한쪽만 고쳐진다).
- MCP: 본문 축이 접수 body 까지 가는가 / 빈 값은 키를 안 보내는가 / 날짜 형식 거절.

### pre-existing red (내 변경 전후 동일 — 손대지 않음)
- `tests/services/engine_v2/` ax_task 계열 **25건** (변경 전 25 / 변경 후 25, 동일 목록).
- `tests/schema/test_version_wbs_schema.py` — `VersionWbsLinkKind` ImportError(수집 실패).
- `tests/api/test_wp116_wbs_task_card_form.py` — WBS API 픽스처 시드 부재(그 파일 §⚠ 가 이미 명시).
- `tests/services/test_decision_gate_bot_and_wbs.py::...duty_not_an_option` — decision 프롬프트 문구 drift.
- 1건 회수: `test_the_schema_has_no_department_slot_at_all` 이 `purpose`→`goal` 개명을 못 따라와
  붉었던 것을 고쳤다(테스트만).

---

## 4. 남은 것 (이 라운드 밖 — 명시)

1. **task.draft 의 참조자(cc)·완료 예정**: 초안 산출 스키마(`TaskDraftContent`)에 그 자리가 없다.
   추가하려면 **LLM 출력 계약 + 프롬프트 + 재생성 + diff 키 + 실행** 을 함께 바꿔야 해서 별도
   라운드가 맞다. **WBS 등록 카드는 두 축 다 싣고 착지한다.**
2. **`wbs_task_update` 의 체크리스트**: 체크 항목은 자기 원장 API(check-item)가 소유한다 — patch 에
   목록을 얹으면 「추가인가 교체인가」가 애매해진다. 이 라운드에서 열지 않았다.
3. **행위 변화 1건(의도)**: work_item 생성이 `startDate`/`dueDate` 를 **더 이상 422 로 거절하지
   않는다**. 웹 폼은 애초에 안 보내던 값이라 넓어지는 방향이고, phase 확장은 기존 경로가 그대로 한다.
