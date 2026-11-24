# planner-fix-11 결과 보고 — 결정 C33 · C34 + 검수 4 기본값

## 상태: done

워크트리 `mediness-mediness/day-chart-photo-spec` · `7c5820d5` 위 · 미커밋. 바꾼 파일 = `products/day/20-spec/spec-002-procedure-board.md` · `40-architecture/deployment.md` · `10-decision.md` · `log.md`.

| 항목 | 자리 | 반영 |
|---|---|---|
| 전부 | spec-002 :45 머리글 | 「보충 9」 ㉖ ~ ㉘ |
| **C33** | API 사진 올리기 행 · 매트릭스 :834 새 줄 · deployment.md :33 새 줄 | 올리기 경로(`POST /board/visits/{visit_id}/photos`)만 서버 앞단(Caddy) `request_body` 100MiB · 다른 경로 6MiB 그대로 · 넘으면 앞단 413(DAY 코드 · `X-Day-Error` 없음) → 화면이 상태 코드로 오류 토스트 · 아무것도 저장 안 됨 · 글자 OQ-88 |
| **C34** | 규칙 39 ⑪ ⓕ(:1223) | 그 회차 삭제 판정 안 함(가져오기 · ⓘ 는 그대로): ⓐ KOS 목록에 매핑 실패 항목이 하나라도 ⓑ 목록이 비었는데 KOS 반영된 DAY 사진이 있음 |
| 기본값 — 10초 확인 = 목록만 · 고르기 · 보내기 중 건너뜀 | U-16 :427 | 사진 목록(두 묶음)만 다시 그림 · 올리기 칸 유지 · 파일 고르기 창 열림 · 보내는 중 · 삭제 확인 창 열림 = 건너뜀(e2e 2회차 F2 · review-code-4 W2) |
| 기본값 — 토스트 층 | U-14 :408 새 bullet | 차트 모달이 열려 있으면 그 모달의 토스트(C29 · C27 등) = 모달과 같은 층(덮개 아래로 깔리지 않게)(e2e 2회차 F1) |
| 기본값 — 빠진 장 토스트 | 매트릭스 「여러 장 중 일부만 실패」 줄 | 형식 `photo_type` · 크기 `photo_too_large` · 저장소 `photo_disabled`(저장소가 멈추면 남은 장도 안 저장) — 코드마다 토스트 1장(바로 시작 선례) · 말없이 빠지지 않음(W3) · 비어 있는 글자는 OQ-88 |
| 기본값 — 숨겨진 탭 멈춤 | U-16 | 숨겨진 브라우저 탭에서 멈추고 다시 보이면 바로 한 번(판 새로고침과 같은 꼴 · W4) |
| 기본값 — KOS 에 없는 사진 재삭제 안 함 | 규칙 39 ⑪ ⓘ | 그 KOS id 가 그 회차 KOS 목록에 이미 없으면 KOS 를 부르지 않고 ref 만 소프트 삭제 · 목록 읽기 실패 회차는 지금처럼(W5) |
| 기본값 — 엇갈린 응답 | U-16 | 삭제 · 10초 확인 응답이 엇갈려도 지운 사진을 다시 그리지 않음(W7) |
| 전부 | §4 결정 짝 표 :1306 | C33 · C34 · 기본값 행 |

- 기본값은 모두 「기본값(코디 · review-code-4 · e2e 2회차)」 표시. 결정 파일에 없는 글자는 짓지 않음(413 토스트 · 빠진 장 중 빈 글자 = OQ-88).
- `10-decision.md` 「현재 결론」 한 줄(escalation 없음 · 배포 설정 자리 안내) · `log.md` 1행(spec-change, arch-change).
- review-code-4 W6(캐시 어댑터 교체 · 동시 첫 생성)은 코드 몫이라 SPEC 에 넣지 않음.

## 검증

`python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning** · `products/day/` 0건(전부 타 제품 — 무관). 바꾼 표 열 수 · `~~` 짝 점검 통과.

## 미결 · 주의

- 413(앞단) 토스트 · `photo_type` · 「KOS 미반영」 글자는 비어 있음(OQ-88).
- deployment.md 의 앞단 상한 줄은 Caddyfile 실제 값과 맞춰야 한다(코드 · 배포 몫).
