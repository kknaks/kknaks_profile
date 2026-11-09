# day-data-architecture 결과 보고

## 상태: done

## 수행 내용

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` · `products/day/` 만 수정. 커밋 · push · PR 없음.

| 파일 | 내용 |
|---|---|
| `products/day/20-spec/spec-000-data-model.md` (신규 · DAY-SPEC-000 · doc_no DAY-DOC-4 · draft) | §1 개요(1차 범위 · 주제와 상태 · 표 읽는 법) · §2 공통 규칙(원천 README 「모든 테이블에 공통」 표 그대로) · §3 1차 테이블(01~07) · §4 1차 범위 밖 — 자체 운영 단계 설계(04-1 메뉴) · §5 관계(erd 링크) · §6 Open Questions(원천의 정할 것 · 확인할 것 · 논의 중 · 보류 전부, 결정하지 않음). frontmatter `sources` = 원천 9개 파일 |
| `products/day/20-spec.md` | Scope · 용어 · SPEC Bundle · SPEC List(SPEC-000 한 줄) · 읽는 순서 · ESC 링크 |
| `products/day/30-work.md` | Spec Coverage 에 `DAY-SPEC-000 \| — (WP · Delivery Issue 미발주) \| proposed` 한 줄(lint 동기 규칙). 그 밖은 템플릿 그대로 |
| `products/day/40-architecture/README.md` | 핵심 도메인 표 9행(1차 8 + 메뉴 1) · 장기 invariant 5개(SPEC §2 가리킴) · 승격 기준. `domains/` 비움 |
| `products/day/40-architecture/system.md` | KOS ↔ DAY 1차 토폴로지 · 원장 두 단계 · 폴링(10초 / 1시간) · 쓰기 큐 sequence · 로그인 · APP_ENV · KOS 를 뗄 때 지우는 것(`external_ref` · `external_session` · `external_outbox` · `crm_connection` · `emr/`) · 외부 통합 |
| `products/day/40-architecture/erd.md` | 원천 관계도를 1차(관계 62) / 메뉴(관계 9) 두 그림으로 나눔 + 테이블 인벤토리 49행(책임 1줄 · 핵심 키만). 칸 목록 없음 → SPEC-000 링크 |
| `products/day/10-decision.md` | `## 미완료` 에 DAY-ESC-001(법적 검토) 1건 · 현재 결론 · 로그 · 리스크 |
| `products/day/log.md` | 표 형식으로 정리 — 2026-11-03 `spec-add, arch-change`(SPEC-000 초안) · `decision-add`(ESC-001) · 스캐폴드 `migration` |
| `products/day/README.md` | DAY 정의 · 왜 · 1차 범위 · 원장 두 단계 · 관련 레포 · 진입점 |

옮기는 방법: 원천 표 · 본문을 손으로 다시 쓰지 않고 스크립트로 그대로 붙였다(헤딩만 2단계 내림). 바꾼 것은 ① `[README.md](README.md)` · `README 「…」` → `§2 공통 규칙` ② claude.ai 검토표 링크 제거 ③ 07 법적 검토 줄 끝에 `→ DAY-ESC-001` ④ 열린 것 절을 §6 으로 이동 — 넷뿐.

## 검증

### lint

```
python3 scripts/lint-pipeline.py --strict → exit 0 · 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0
```

263 WARN 은 전부 타 제품(selly 등) 기존 것 — 무관. 작업 전 기준선도 0 error · 263 warning.

placeholder: `products/day/` 안에 `<…>` 없음(남은 `spec-NNN-*` · `DAY-ESC-NNN` 은 스캐폴드의 명명 패턴 설명).

### 원천 → SPEC-000 대조 (주제별)

원천 각 파일의 모든 줄(표 행 + 본문, 열린 것 절 제외)이 SPEC 에 그대로 있는지 스크립트로 대조.

| 주제 | 원천 파일 | 테이블 수 | 원천 표 수 | 원천 표 데이터 행 | SPEC 에 그대로 | 누락 | 본문 줄 누락 |
|---|---|---|---|---|---|---|---|
| 공통 | README.md | — | 2 (주제 순서 · 공통 규칙) | 21 | 21 | 0 | — (관계도는 erd.md) |
| 01 | 01-hospital.md | 3 (`brand` · `hospital` · `crm_connection`) | 6 | 31 | 31 | 0 | 0 |
| 02 | 02-customer.md | 7 (`customer` · `external_ref` · 코드 5) | 5 | 60 | 60 ※ | 0 | 0 |
| 03 | 03-visit.md | 4 | 4 | 57 | 57 | 0 | 0 |
| 04 | 04-staff.md | 7 | 8 | 48 | 48 | 0 | 0 |
| 05 | 05-task.md | 9 | 10 | 72 | 72 | 0 | 0 |
| 06 | 06-room.md | 6 | 7 | 38 | 38 | 0 | 0 |
| 07 | 07-misc.md | 13 | 13 | 104 | 104 | 0 | 0 |
| 04-1 (1차 밖) | 04-1-menu.md | 13 | 12 | 81 | 81 | 0 | 0 |
| 합계 | | 1차 49 + 메뉴 13 | 67 | 512 | 512 | 0 | 0 |

※ 02 `customer.deleted_at` 1행은 설명의 `README 「삭제」` 를 `§2 공통 규칙 「삭제」` 로 바꾼 것(내용 동일).

열린 것 → §6: README 1(소켓) · 01 1(Vegas) · 02 2(gender 등 · updatedDateTimeUtc) · 03 2(보류 3칸 · 상담 시술) + 해결 1 · 04 2 · 04-1 6 + 범위 밖 · 05 1 · 06 1 · 07 3. 01 「정할 것」 안의 결정(`hospital` phone · address 두지 않음)은 §3 01 에 남김.

## 계약 준수

- 설계 변경 0 — 이름 · 타입 · 관계 · enum 원천 그대로. 원천에 없는 테이블 · 칸 · 정책 추가 0.
- 보류 · 범위 밖은 그대로 보류 · 범위 밖(§6 · §4).
- KOS 키 · 토큰 · 테넌트 id · 실명 없음(원천 01 「환경」 표는 키 이름 없이 응답 코드만 — 그대로 옮김).
- WP · 코드 · migration 없음.

## 미결·주의점

원천에서 이상해 보이지만 고치지 않은 것(설계 변경 금지):

1. **`visit_requested_procedure.product_option_id` 가 `uuid FK` 인데 1차에는 `product_option` 테이블이 없다.** §2 「참조 + 스냅샷」은 「1차는 스냅샷만(참조는 자체 운영 단계에서)」. 원천 관계도도 `product_option ||--o{ visit_requested_procedure` 를 그린다 → erd.md 에선 메뉴 그림 쪽에 둠. 옵션: (a) 1차는 칸만 두고 FK 는 자체 운영 때 건다 (b) 1차에서 칸을 뺀다. 권장 (a) — 사용자 확인.
2. **타입 `—` 칸**: `visit.purchase_ids` · `prescription_ids` · `reactions`(보류) · `consultation.procedures`(상담 시술 — 「시술 개념 셋」은 `consultation_procedure` 테이블로 그리나 칸 표 없음) · `visit_occupied_resource.doctor_ids`(`visit_occupied_resource_doctor` N:M — 칸 표 없음). SPEC 은 「만들지 않음 · §6」으로 표시. 둘(`consultation_procedure` · `visit_occupied_resource_doctor`)은 원천 관계도 · 인벤토리에도 없다.
3. **공통 규칙 예외**: §2 는 「모든 테이블에 `deleted_at`」인데 `external_outbox` · `event_log` · `push_log` 에는 없음(뒤 둘은 「쌓기만」). `crm_connection` 은 `created_at` 대신 `connected_at`. 원천대로 둠.
4. **`visit.room_id` 와 `visit_task.room_id` 둘 다 있다**(방문 카드 위치 / 작업이 들어간 방). 원천대로.
5. **03 원천 머리말이 「사용자와 정하는 중」**, README 주제표는 「정함」. 그대로 옮김.
6. **07 은 「바로 적용 — 검토는 이후」** — 칸 단위 승인 전. §3 07 머리와 OQ-07-3 에 표시.
7. 열린 enum 값: `display_request.kind`(값 없음) · `id_photo.doc_type`(`passport · id_card …`) · `identity_check.status · method` · `taxation` 등 — 원천 그대로.
8. **DAY-ESC-001 칸 값은 내가 고른 기본값**: 긴급도 `mid` · 결정레벨 `경영지원` · 보고방법 `mediness` · 담당자 `기획`. 원천엔 「법적 검토 필요」만 있다 — 코디 · 사용자가 맞춰 줄 것.
9. **frontmatter**: SPEC `owner: TBD`(개인 owner 미지정 — 규칙상 TBD) · `version: 0.0.1`(템플릿 기본값, 상위기획 없음 — 「v2」를 버전으로 쓸지 판단 필요).
10. **sources 경로**: 원천이 작업 중 `day/reference/2026-11-03-cc-day/erd/` 하위로 옮겨졌다(브리프 경로엔 이제 파일 없음 · 내용은 크기 동일). sources 는 `kknaks/kknaks_profile day/reference/2026-11-03-cc-day/erd/*.md` 로 적음.
11. 원천 검토표(claude.ai artifact) 링크는 SPEC 에 옮기지 않음 — 필요하면 다시 넣을 수 있다.
12. `products/day/` 밖 — `context/products.md` 의 DAY 행이 「**비활성**」(2026-08-05 prod 실측)으로 남아 있고 설명이 「환자 · 상담 · 접수 · 예약 · 수납 CRM」이다. v2 재시작 · 1차 범위(시술실 · 의국)에 맞게 갱신할지 코디 판단.
13. `30-work.md` 의 스캐폴드 Status enum 문구(`draft`, `ready_for_qa` …)는 rules 의 WP enum(`proposed` · `in_dev` · `done`)과 다르지만 템플릿 그대로 둠.
