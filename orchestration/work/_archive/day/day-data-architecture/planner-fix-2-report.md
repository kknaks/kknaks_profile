# day-data-architecture 수정 2판 결과 보고

## 상태: done

## 수행 내용

수정 1판 미결 1 · 2(원천 쪽)를 코디가 고친 원천으로 SPEC-000 을 다시 생성했다(같은 스크립트 · 표 그대로). 생성 전후 diff 가 **아래 6개 표의 12행뿐**임을 확인 — 그 밖은 바뀌지 않았다. `products/day/` 밖 · 커밋 없음. erd.md 등 다른 파일은 손대지 않음(테이블 · 관계 · 키 변화 없음).

| 표 | 파일:줄 (`products/day/20-spec/spec-000-data-model.md`) | 바뀐 것 |
|---|---|---|
| 02 `external_ref` | :303-304 | 묶은 행 `deleted_at · created_at · updated_at`(필수 빈칸) → `created_at · updated_at \| ✓ \| 생성 · 수정` + `deleted_at \| (빈칸) \| 소프트 딜리트 — null = 살아 있음` |
| 06 `zone` | :795-796 | 「외부에서 사라지면 … (cc zone.present)」 설명 → `deleted_at` 행 |
| 06 `reservation_group` | :820-821 | 외부(KOS) `deleted` → `deleted_at` 행 |
| 07 `chat_message` | :1047-1048 | 「보존 기간 없음(cc 그대로)」 · cc `chat_message.deleted_at` → `deleted_at` 행 |
| 07 `chat_attachment` | :1060-1061 | cc `chat_photo.deleted_at` → `deleted_at` 행 |
| 07 `notice` | :1071-1072 | cc `notice.deleted · synced_at` → `deleted_at` 행(「외부 id 는 external_ref」 설명은 `created_at · updated_at` 행에 그대로 — 원천대로) |

## 검증

```
python3 scripts/lint-pipeline.py --strict → 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 WARN 은 전부 타 제품 기존 — 무관)
```

### 원천 → SPEC-000 대조 (원천 / SPEC)

원천 모든 표 행 · 본문 줄(열린 것 절 제외)이 SPEC 에 그대로 있는지 스크립트로 대조. 행 = 표 데이터 행.

| 주제 | 원천 파일 | 표 수 원천 / SPEC | 표 데이터 행 원천 / SPEC | 누락(표 행 · 본문 줄) |
|---|---|---|---|---|
| 공통 | README.md | 2 / 2 | 21 / 21 | 0 · 0 |
| 01 | 01-hospital.md | 6 / 6 | 31 / 31 | 0 · 0 |
| 02 | 02-customer.md | 5 / 5 | 61 / 61 | 0 · 0 |
| 03 | 03-visit.md | 5 / 5 | 69 / 69 | 0 · 0 |
| 04 | 04-staff.md | 8 / 8 | 55 / 55 | 0 · 0 |
| 05 | 05-task.md | 10 / 10 | 79 / 79 | 0 · 0 |
| 06 | 06-room.md | 8 / 8 | 47 / 47 | 0 · 0 |
| 07 | 07-misc.md | 13 / 13 | 116 / 116 | 0 · 0 |
| 04-1 (1차 밖) | 04-1-menu.md | 12 / 12 | 90 / 90 | 0 · 0 |
| 합계 | | 69 / 69 | 569 / 569 | 0 |

묶은 deleted_at 행(SPEC): 0

1판 대비 +1행 = 02 `external_ref` 분리. DB 테이블 수 변화 없음(1차 51 + 메뉴 13).

## 미결·주의점

- 수정 1판 미결 1 · 2 해소. SPEC 에 `deleted_at` 을 다른 칸과 묶은 행 0.
- 1판 리포트의 나머지 미결(product_option_id FK · owner TBD · version 0.0.1 · context/products.md 등)은 그대로 유효.
