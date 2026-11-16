# day-data-architecture 수정 1판 결과 보고

## 상태: done

## 수행 내용

워크트리 `mediness-mediness/day-data-architecture-spec` · `products/day/` 만 수정. 커밋 · push · PR 없음. W2(ESC-001 값) · W3(log PR 칸)는 지시대로 손대지 않았다.

방법은 1판과 같다 — 바뀐 원천(`kknaks_profile/day/reference/2026-11-03-cc-day/erd/`)에서 SPEC-000 을 스크립트로 다시 생성(표 · 본문 그대로, 헤딩 단계만 맞춤). 옮기며 바꾸는 것은 ① 원천 README 링크 → `§2` ② **원천 파일 링크 `[0N-*.md](…)` → `§3 0N` / `§4 04-1`(W1 — 이번에 추가)** ③ claude.ai 검토표 링크 제거 ④ 07 법적 검토 줄 끝 `→ DAY-ESC-001` ⑤ 열린 것 절 → §6.

### 고친 곳

| 지적 | 파일:줄 | 내용 |
|---|---|---|
| F1 | `products/day/20-spec/spec-000-data-model.md:74` | 「필수 ✓ = NOT NULL. 빈칸 = NULL 허용.」 뒤에 「§2 공통 규칙과 어긋나면 §2 가 우선한다.」 추가 |
| F1 | 같은 파일 (구 :77) | 「묶은 행은 각 칸이 같은 타입 · 필수 여부」 줄 삭제 |
| F1 | 같은 파일 :98 | §2 「삭제」 — 원천대로 `deleted_at`(timestamptz, **NULL 허용** — null = 살아 있음) |
| F1 | 같은 파일 §3 · §4 전체 | 원천의 분리 행 그대로 — `created_at · updated_at \| ✓` + `deleted_at \| (빈칸)`. 묶은 `created_at · updated_at · deleted_at` 행 **0** · `deleted_at` 단독 행 51 |
| F2 | 같은 파일 :76 | 「타입 `—` = … 만들지 않는다」 → 「원천 표기 그대로. 그 행의 설명이 무엇인지 말한다(보류 / 다른 곳으로 / 연결 테이블로)」 |
| F2 | 같은 파일 :1265 | §6 머리 「(또는 타입 `—` 이면 만들지 않음)」 삭제 |
| F2 | 같은 파일 §6 | OQ-03-2 · OQ-06-1 삭제(06 소절째 — 남은 OQ 없음) |
| F2 | 같은 파일 :437 · :441 | `consultation.procedures` 행이 `consultation_procedure` 를 가리킴 + 새 표 `#### consultation_procedure — 상담 시술 (상담 1 : N)` |
| F2 | 같은 파일 :851 · :855 | `visit_occupied_resource.doctor_ids` 행이 `visit_occupied_resource_doctor` 를 가리킴 + 새 표 `#### visit_occupied_resource_doctor · 예약 칸 지정 의사 (N:M)` |
| W1 | 같은 파일 :61-68 | 「주제와 상태」 표의 깨진 링크 8개 → `§3 01` ~ `§3 07` · `§4 04-1`(링크 없는 절 이름) |
| W4 | 같은 파일 :352 | 03 머리말 「사용자와 정함」(원천 갱신 반영) |
| 원천 | 같은 파일 :61-68 | 주제 표 상태 칸 원천대로 — 03 「상담 시술 칸 추가(검수 F2)」 · 06 「지정 의사 칸 추가(검수 F2)」 |
| erd | `products/day/40-architecture/erd.md:18` | 1차 관계 62 → 65 |
| erd | 같은 파일 :39 · :69-70 | 관계 추가 `consultation ‖--o{ consultation_procedure` · `visit_occupied_resource ‖--o{ visit_occupied_resource_doctor` · `staff ‖--o{ visit_occupied_resource_doctor` |
| erd | 같은 파일 :110 | 공통 설명에 `deleted_at` NULL 허용 명시 |
| erd | 같은 파일 :127 · :151 | 인벤토리 2행 — `consultation_procedure`(PK `id` · FK `consultation_id`) · `visit_occupied_resource_doctor`(PK (`occupied_resource_id`, `staff_id`)) |
| erd | 같은 파일 :166 | 1차 49 → 51 |

## 검증

### lint

```
python3 scripts/lint-pipeline.py --strict → exit 0 · 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 WARN 은 전부 타 제품 기존 — 무관, 1판과 같음)
```

### 원천 → SPEC-000 대조 (원천 / SPEC)

원천 파일의 모든 표 행과 본문 줄(열린 것 절 제외)이 SPEC 에 그대로 있는지 스크립트로 대조. 「행」은 표 데이터 행(머리줄 · 구분줄 제외).

| 주제 | 원천 파일 | DB 테이블 원천 / SPEC | 표 수 원천 / SPEC | 표 데이터 행 원천 / SPEC | 누락(표 행 · 본문 줄) |
|---|---|---|---|---|---|
| 공통 | README.md | — | 2 / 2 | 21 / 21 | 0 · — |
| 01 | 01-hospital.md | 3 / 3 | 6 / 6 | 31 / 31 | 0 · 0 |
| 02 | 02-customer.md | 7 / 7 | 5 / 5 | 60 / 60 | 0 · 0 |
| 03 | 03-visit.md | **5 / 5** (+`consultation_procedure`) | 5 / 5 | 69 / 69 | 0 · 0 |
| 04 | 04-staff.md | 7 / 7 | 8 / 8 | 55 / 55 | 0 · 0 |
| 05 | 05-task.md | 9 / 9 | 10 / 10 | 79 / 79 | 0 · 0 |
| 06 | 06-room.md | **7 / 7** (+`visit_occupied_resource_doctor`) | 8 / 8 | 47 / 47 | 0 · 0 |
| 07 | 07-misc.md | 13 / 13 | 13 / 13 | 116 / 116 | 0 · 0 |
| 04-1 (1차 밖) | 04-1-menu.md | 13 / 13 | 12 / 12 | 90 / 90 | 0 · 0 |
| 합계 | | 1차 51 + 메뉴 13 | 69 / 69 | 568 / 568 | 0 |

(1판 대비 행 증가 = deleted_at 분리 행 + 새 표 2개. 02 `customer.deleted_at` · 주제 표 링크 8개는 위 ②로 바꾼 줄 — 바꾼 뒤 같은 줄로 대조.)

관계도: 원천 README 관계 74 = erd.md 1차 65 + 메뉴 9. 누락 0.

§6 OQ: OQ-00-1 · 01-1 · 02-1 · 02-2 · 03-1 · 04-1 · 04-2 · 041-1~6 · 05-1 · 07-1 · 07-2 · 07-3 (+ 03 해결 1 · 04-1 범위 밖). 원천 「정할 것 · 확인할 것 · 논의 중 · 보류」 밖에서 끌어온 OQ 없음.

## 미결·주의점

1. **원천에 남은 묶은 행 하나**: `external_ref` 의 `` `deleted_at` · `created_at` · `updated_at` | timestamptz | (필수 빈칸) `` (`spec-000:303`) — 이번 원천 분리에서 빠졌다. 필수가 비어 있어 F1 같은 NOT NULL 오독은 없지만, 대신 `created_at` · `updated_at` 이 NULL 허용으로 읽힌다(다른 테이블은 ✓). 원천대로 둠 — 원천 쪽 확인 필요.
2. 분리 뒤 설명이 `created_at · updated_at` 행에 남은 곳(원천 그대로): `zone`(`spec-000:794` 「외부에서 사라지면 deleted_at」) · `chat_message`(`:1046` 「소프트 딜리트 · 보존 기간 없음」 · cc `deleted_at`) · `chat_attachment`(`:1059` cc `deleted_at`). 뜻이 `deleted_at` 쪽 설명이다. 원천 쪽 정리 여부 코디 판단.
3. 02 코드 테이블 요약표(`spec-000:311-315`)는 칸 목록 형식이라 `deleted_at` 필수 표기가 없다 — §2 가 우선(문제 없음).
4. 1판 미결 중 W2 · W3 는 지시대로 그대로. 나머지(product_option_id FK · owner TBD · version 0.0.1 · context/products.md 등)는 1판 리포트 그대로 유효.
