# 리뷰 리포트 — day-data-architecture / doc 재검수 (2026-11-03)

대상: `mediness-mediness/day-data-architecture-spec` `products/day/`. planner 가 수정 1 · 2판을 반영한 뒤의 상태이며 아직 untracked · 미커밋이다.
기준: 바뀐 원천 `kknaks_profile/day/reference/2026-11-03-cc-day/erd/` 9개 파일. 1판 리포트 `review-doc-report.md` 의 F1 · F2 · W1 · W4.
방법: 1판과 같다. 원천 9개 파일과 SPEC-000 의 해당 절을 줄 순서로 diff 했고(헤딩 단계만 정규화), 표 · 행 · 테이블 수는 다시 직접 셌다. 이번에는 절 범위를 헤딩으로 자동으로 찾았다(줄 번호가 밀렸으므로). planner 리포트 숫자는 보지 않고 센 뒤에 대조했다.
제외: W2(ESC-001 값)는 사용자가 그대로 두기로 했다. W3(log PR 칸)은 코디가 PR 때 채운다.

## 판정: PASS

1판의 FAIL 2건과 WARN 2건이 모두 풀렸다. 바뀐 원천 전체를 다시 대조했고, 수정하면서 새로 생긴 누락 · 발명 · 왜곡은 없다.

## FAIL

없음.

## WARN

없음.

---

## 1판 지적 해소 확인

| 1판 | 지금 위치 | 결과 | 근거 |
|---|---|---|---|
| F1 묶은 행 → `deleted_at` NOT NULL | `spec-000-data-model.md:74` (「§2 가 우선」 추가) · 구 :77 「묶은 행 = 같은 필수 여부」 줄 삭제됨 · `:98` §2 삭제 「NULL 허용」 | **해소** | SPEC 의 모든 표 행을 파싱해 확인했다. 필드 칸에 `deleted_at` 이 있으면서 필수가 ✓ 인 행은 **0**이다. 원천도 분리 행이 됐다(예: `erd/06-room.md:98-99`, `erd/03-visit.md` 각 표). 칸 목록 요약표(`spec-000:312-316` — 02 코드 테이블)는 원천 `erd/02-customer.md` 의 형식 그대로이고 필수 표기가 없다. §2 가 적용되므로 문제없다 |
| F2 「타입 `—` = 만들지 않는다」 | `spec-000:76` 「원천 표기 그대로 … (보류 / 다른 곳으로 / 연결 테이블로)」 · §6 머리 문구 삭제 · OQ-03-2 · OQ-06-1 삭제 | **해소** | `consultation_procedure` 칸 표(원천 `erd/03-visit.md:92-`), `visit_occupied_resource_doctor` 칸 표(원천 `erd/06-room.md:92-99`)를 원천에 넣었고 SPEC 은 그대로 옮겼다. 줄 diff 결과 동일하다. SPEC 에 남은 「만들지 않」 문구 7곳(`:65, 490, 508, 509, 1078, 1086, 1091`)은 모두 원천 문장이다 |
| W1 깨진 상대 링크 8개 | `spec-000:61-68` → `§3 01` ~ `§3 07` · `§4 04-1` | **해소** | `products/day/**/*.md` 의 상대 링크를 전수 검사했고 깨진 링크는 **0**이다 |
| W4 03 「정함 / 정하는 중」 엇갈림 | `spec-000:352` 03 머리말 「사용자와 정함」 | **해소** | 원천 `erd/03-visit.md:3` 이 「정함」으로 바뀌었고, SPEC 도 그 줄과 같다 |

## 바뀐 원천 전체 대조 (리뷰어가 직접 셈)

「행」은 표 데이터 행(머리줄 · 구분줄 제외)이다.

| 주제 | 원천 파일 | DB 테이블 원천 / SPEC | 표 수 원천 / SPEC | 표 데이터 행 원천 / SPEC | 줄 순서 diff |
|---|---|---|---|---|---|
| 공통 | `erd/README.md` 「주제 순서」 · 「모든 테이블에 공통」 | — | 2 / 2 | 21 / 21 | 동일 (주제 표 링크 → 절 이름) |
| 01 | `erd/01-hospital.md` | 3 / 3 | 6 / 6 | 31 / 31 | 동일 |
| 02 | `erd/02-customer.md` | 7 / 7 | 5 / 5 | 61 / 61 | 동일 (README 참조 → §2) |
| 03 | `erd/03-visit.md` | 5 / 5 | 5 / 5 | 69 / 69 | 동일 |
| 04 | `erd/04-staff.md` | 7 / 7 | 8 / 8 | 55 / 55 | 동일 |
| 05 | `erd/05-task.md` | 9 / 9 | 10 / 10 | 79 / 79 | 동일 |
| 06 | `erd/06-room.md` | 7 / 7 | 8 / 8 | 47 / 47 | 동일 |
| 07 | `erd/07-misc.md` | 13 / 13 | 13 / 13 | 116 / 116 | 동일 (법적 검토 줄 끝 `→ DAY-ESC-001`) |
| 04-1 (1차 밖) | `erd/04-1-menu.md` | 13 / 13 | 12 / 12 | 90 / 90 | 동일 |
| 합계 | | 1차 51 + 메뉴 13 | 69 / 69 | 569 / 569 | |

- 표 바깥 본문 줄도 diff 했다. 다른 곳은 1판과 같은 정해진 변환뿐이다. 원천 README 링크 → §2, 검토표(claude.ai) 링크 제거, 「정할 것 · 확인할 것 · 논의 중」 → §6, 01 phone · address 문장 → `#### 두지 않는 칸`, 03 예약 그룹 해결 → `#### 예약 그룹`.
- planner 수정 2판 리포트의 숫자(69 · 569 · 51 + 13)는 실물과 같다.
- 관계도: 원천 `erd/README.md` erDiagram 관계 **74** = `40-architecture/erd.md` 관계 74(1차 65 + 메뉴 9). 정렬 diff 결과 동일하다. 새 관계 3개(`consultation ||--o{ consultation_procedure` · `visit_occupied_resource ||--o{ visit_occupied_resource_doctor` · `staff ||--o{ visit_occupied_resource_doctor`)는 원천 `erd/README.md:81, 121-122` 그대로다.
- erd 인벤토리: 1차 51행이다(직접 셈). 새 2행의 핵심 키를 원천과 대조했다. `consultation_procedure` 는 `id` · FK `consultation_id` (`erd/03-visit.md` 표), `visit_occupied_resource_doctor` 는 PK (`occupied_resource_id`, `staff_id`) (`erd/06-room.md:97`)로 일치한다. 칸 전체 목록은 없다(규칙 준수). 공통 설명 `erd.md:110` 「`deleted_at` NULL 허용」은 원천 `erd/README.md` 「삭제」와 같다.

## 열린 것 → OQ

§6 은 OQ-00-1 · 01-1 · 02-1 · 02-2 · 03-1 · 04-1 · 04-2 · 041-1~6 · 05-1 · 07-1 · 07-2 · 07-3 에 (해결) 1 · 04-1 범위 밖을 더한 것이다. 원천의 정할 것 · 확인할 것 · 논의 중 · 보류와 1:1 로 맞는다. 원천에 없는 OQ(1판 F2 의 OQ-03-2 · 06-1)는 빠졌다. 결정된 것처럼 쓴 곳은 없다.
「보류 · 1차 밖 · 범위 밖 · 바로 적용 — 검토는 이후」 표시는 모두 살아 있다(`spec-000:65, 1078, 1086` · OQ-03-1 · 04-1 범위 밖 · OQ-07-3 · 07 머리말).

## 문서 규칙 · 보안

- lint `python3 scripts/lint-pipeline.py --strict` 1회 → **exit 0 · 0 error · 263 warning**. `products/day/` 범위는 ERROR 0 · WARN 0이다. 263 WARN 은 전부 타 제품의 기존 경고라 **무관**하다(1판과 같은 수).
- 보안 grep(이메일 · JWT · uuid · 32자 이상 토큰 · Bearer · claude.ai 링크 · wss): **0건**.
- `git status`: `?? products/day/` 뿐이다. 범위를 벗어난 곳은 없다.

## 직원이 실물에서 만날 자리

없음. 1판에서 걱정한 두 가지가 모두 풀렸다. `deleted_at` NOT NULL 로 살아 있는 행을 만들 수 없는 문제와, 상담 시술 · 지정 의사가 담기지 않는 문제다.

## 참고(설계 판정 아님)

- `spec-000:74` 「§2 공통 규칙과 어긋나면 §2 가 우선한다」는 원천 문장이 아니다. planner 가 더한 읽기 안내다. 원천 내용과 부딪치지 않고 F1 같은 오독을 막는 장치라 문제 삼지 않는다.
- `consultation_procedure.product_option_id` 가 `uuid FK` 인데 「1차는 비워 둔다」고 되어 있다. 1판 미결 1(`visit_requested_procedure.product_option_id`)과 같은 모양이고 원천 그대로다.
- 1판 「참고」의 템플릿 부채(20-spec.md `:20` 문구 · 30-work.md enum · QA 컬럼)는 그대로다. 원천과 무관하다.
