# WP2-FE 결과 보고 (frontend)

## 상태: done

- 워크트리 `strong-hajin-enhance` · WP1 커밋 `e51fe3b` 위 · 커밋·push 없음(변경은 워크트리에만)
- 범위: WORK-012 「Phase WP2-FE」 계약 2건(SPEC-010 §2.5 · §4.7-4 · §4.7-7 · H-3)
- 응답 위치 — **코디 판정(2026-10-07)**: 회의 상세 응답 **최상위 `term_corrections`**(`meeting`·`agendas` 옆). `term_corrected_at` 이 null 이면 `null` · 있으면 행 목록(0개면 `[]`) · 행 = `{heard, corrected, grade}`. SPEC 의 「최종 벌에 싣는다」 는 상세 응답에 「최종 벌」 객체가 없어 물어서 정했다

## 1. 계약 체크박스별 구현 위치 — 2/2

| # | 계약 | 구현 위치(파일:줄) |
|---|---|---|
| 1 | 최종 회의록 끝 「용어 보정」 표(들린 말 · 바로잡은 말 · 처리 「바꿈」/「표에만」) · 읽기 전용 · `[]` 이면 「바로잡은 용어 없음」 한 줄, `null` 이면 자리 없음(H-3) | 타입 `frontend/src/lib/viewModels.ts:1297`(`MeetingTermCorrection`) · `:1304`(`MeetingRecord.term_corrections?: … \| null` — 칸이 없는 옛 응답은 `null` 과 같이 본다) · 문구 `lib/labels.ts:921-930`(제목·열 셋·빈 줄·등급 `auto`→「바꿈」 `presumed`→「표에만」) · 부품 `features/meetings/TermCorrections.tsx`(새 파일 — DS `DataTable`, 회의록 안건 블록과 같은 `scax-agenda-block` 틀, `[]` 이면 표 대신 한 줄, 모르는 등급은 서버 값 그대로) · 놓는 자리 `features/meetings/MeetingDetailPage.tsx:719`(`termCorrections` — 배열일 때만) · `:1308-1314`(회의록 본문 `.scax-note__body` 의 **마지막** — 안건 목록·[안건 추가] 뒤 · 조건 = 최종 벌을 볼 때 + 「종료」·「실패」 + 정리 중 아님) · 제목 수정(PATCH) 응답이 이 칸을 싣지 않으면 들고 있던 표를 지우지 않는다 `:568-570` · 스타일 `styles/meetings.css:69-71`(공유 표와 같은 촘촘한 높이 + 긴 용어는 줄바꿈) |
| 2 | 안건 순서는 서버가 준 대로(화면이 다시 정렬하지 않음) | **코드 변경 없음.** 안건을 줄 세우는 자리는 전부 서버 값 `order` 만 쓴다 — `MeetingDetailPage.tsx:430`(안건 목록) · `:723`(AI 배치) · `:91`·`:752`·`:819`(줄 순서 — 안건이 아님). 근거 시각(`start_ms`)으로 정렬하는 `:763` 은 **한 줄 안의 시각 칩** 정렬이라 안건 순서와 무관. 서버가 `order_index` 를 근거 시각으로 매기면(WP2-BE) 화면은 그 순서로 선다 — 시험으로 잠금(§3) |

## 2. Code Surface WP2 표 대비 닿은 자리

WP2 표에서 프론트 자리는 「정정·보정 표」 줄의 **화면 `MeetingDetailPage.tsx` · `viewModels.ts`** 둘이다(나머지는 서버).

| 자리 | 닿음 |
|---|---|
| `viewModels.ts` | `MeetingRecord` 에 `term_corrections` · 새 타입 `MeetingTermCorrection` |
| `MeetingDetailPage.tsx` | 표를 놓는 자리 1 · 줄 값 1 · 제목 PATCH 의 덮어쓰기 막기 1 |
| 안건 순서(표 「안건 순서 `order_index`」 줄의 화면 쪽) | 다시 셈 — `rg "\.sort\("` 로 프론트 전체 정렬 7곳 중 안건을 줄 세우는 곳 2(`:430` · `:723`) 모두 `order` 기준 → 바꿀 것 없음 |

**표 밖에서 더 본 것**
- `MeetingRecord` 를 쓰는 곳 전부(`rg MeetingRecord` — `api.ts` 반환 타입 6 · `BookingModal.tsx` 3 · `MeetingEditModal.tsx` 1 · `MeetingDetailPage.tsx` 1): 상세 화면의 `setRecord` 는 상세 읽기(`:230`)와 제목 PATCH(`:568`) 둘뿐 — PATCH 쪽만 막아 두었다(§1-1). 생성·빠른 시작·시작·종료 응답은 상세 화면에 바로 세우지 않고 다시 읽는다 → 손댈 것 없음. 칸이 선택(`?`)이라 다른 쓰는 곳은 그대로 컴파일된다
- 내보내기(`export.py`)는 바꾸지 않는다(OQ-1006) — 프론트 내보내기 링크도 그대로

## 3. 새 시험 (6개 · `features/meetings/MeetingAfter.test.tsx:805~` 「WP2-FE — 「용어 보정」 표 · 안건 순서」)

| 시험 | 계약 |
|---|---|
| 행이 있으면 최종 회의록 «끝»에 표 — 머리 셋 · 값 · 「바꿈」/「표에만」 · 서버 순서 그대로 · 본문 마지막 블록 · 칸·단추 없음(읽기 전용) | 1 |
| `[]` 이면 「바로잡은 용어 없음」 한 줄 · 표 없음 | 1 (H-3) |
| `null` 이면 자리 없음 · 칸 없는 옛 응답도 자리 없음 | 1 (H-3) |
| 「실패」 화면에서도 선다 · 「정리 중」·「예정」에는 없다 | 1 |
| 표가 서도 「참석 N명」 그대로(화자 라벨은 기존 스크립트 시험이 잠금 — 원문은 이 판이 안 바꾼다) | 완료 조건 · D-17 |
| 최종 안건은 서버 `order` 그대로 — 배열 순서도, 근거 시각도 아니다(일부러 근거가 늦은 안건을 order 1 로) | 2 (D-15) |

고친 기존 시험: `MeetingAfter.test.tsx` 의 `renderAfter` 에 세 번째 인자(`extra: Partial<MeetingRecord>`)만 더함 — 기존 호출은 그대로

## 4. 검증 수치

| | 기준선(`fe-baseline.md`) | 이번 |
|---|---|---|
| 시험 명령 | `npx vitest run --no-file-parallelism`(직렬) | 같음 |
| 시험 | 1371 — 통과 1362 · 실패 9 | **1399 — 통과 1390 · 실패 9** |
| 기준선과 같은 실패 | — | 8 — `CreateWork.test.tsx` 4 · `CreateWorkLayout.test.tsx` 1 · `TaskDetailDates.test.tsx` 3 |
| 기준선 밖 실패 | — | 1 — `App.test.tsx` > product surfaces > decides an AX proposal through the same judgement drawer…(「AX가 준비한 변경을 승인할지 결정하세요」 를 못 찾음). **이 판과 무관**: 이 시험만 2회 · `App.test.tsx` 파일 전체 1회 다시 돌려 **3회 모두 통과**(33/33). 회의 화면을 거치지 않는 AX 판단 서랍 시험이다. WP1 때의 `ActionCenter.test.tsx` 처럼 전체 직렬 실행에서만 가끔 지는 시간 의존 시험으로 보인다 |
| 이번 판이 만든 실패 | — | **0** |
| 빌드 `make frontend-build` | 통과 | **통과**(청크 500kB 경고만) · `tsc -b` 0 오류 |

## 5. 미결 · 주의점

1. **WP2-BE 와 같이 나가야 표가 선다** — 서버가 `term_corrections` 를 싣기 전까지는 칸이 없어(`undefined`) 표 자리가 없다(= `null` 과 같은 화면). 깨지지는 않는다
2. **제목 PATCH 응답** — 서버가 PATCH 응답에도 `term_corrections` 를 실어 주면 그대로 쓰고, 안 실으면 들고 있던 값을 지킨다. 다만 PATCH 응답에 `null` 이 실려 오면(서버가 상세와 다른 값을 내면) 표가 사라진다 — BE 가 상세와 같은 조립을 쓰는지 WP2-BE 리뷰 때 확인 필요
3. **안건 순서는 화면 변경 없음** — 순서는 WP2-BE 의 적재(`order_index` 를 가장 이른 근거 시각으로)가 정한다. 앱 E2E(재합성 1회)에서 확인
4. **완료 조건(실물 · 앱)** — 재합성한 회의를 앱에서 열어 표가 끝에 · 「참석 N명」·화자 라벨 그대로: 코디 E2E 몫
5. 「바꿈」 항목을 [수정]에서 되돌리는 것(D-16)은 사람이 본문을 고치는 기존 흐름 그대로다 — 표에 되돌리기 단추는 없다(이번 판 읽기 전용)

## 다른 팀 영향

- BE: 상세 응답 최상위 `term_corrections`(코디 판정 (A)) — PATCH 응답도 같은 조립이면 좋다(§5-2)
- SPEC: §4.7-4 「최종 벌에 싣는다」 문구가 실제 위치(최상위)와 다르다 — planner 정리 필요
