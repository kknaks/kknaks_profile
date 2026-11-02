# WP1-FE 기준선 (frontend)

- 코드: 워크트리 `strong-hajin-enhance` · `f0ad522` · **아무것도 고치기 전**(git status 비어 있음)
- 준비: 워크트리에 `frontend/node_modules` 가 없어 `npm ci`(lock 그대로) 를 먼저 돌렸다
- 시험 명령: `cd frontend && npx vitest run --no-file-parallelism`
  - `make frontend-test`(= `vitest run`, 기본 파일 병렬) 대신 **직렬**로 돌렸다 — 병렬 vitest 가 사용자 로컬 스택을 죽인 전례(WORK-012 P-9 · 사용자 메모). 같은 시험 집합이고 병렬 플래그만 다르다
- 빌드: `make frontend-build` 와 같은 `npm run build`(`tsc -b && vite build`)

## 결과 (2026-10-07 13:04 시작 · 172.9초)

| 항목 | 값 |
|---|---|
| 시험 파일 | 92 — 통과 88 · **실패 4** |
| 시험 | 1371 — 통과 1362 · **실패 9** |
| 빌드 | **통과**(청크 500kB 경고만) |

## 기존 실패 9건 (이번 판과 무관 — 손대기 전부터 실패)

| 파일 | 시험 | 오류 |
|---|---|---|
| `src/features/action/ActionCenter.test.tsx` | adjustment and resubmission > prefills the revision form, shows the diff before sending, and refuses a revision that changes nothing | `Unable to find … role "button" and name "수정안 재상신"` |
| `src/features/work/CreateWork.test.tsx` | 업무 갈래의 시작일과 마감일 > 적어 둔 시작일을 그대로 실어 보낸다 | `Unable to fire a "click" event - please provide a DOM element.` |
| 〃 | 업무 갈래의 시작일과 마감일 > 시작일이 마감일보다 늦으면 보내기 전에 막는다 | 〃 |
| 〃 | 요청 갈래의 시작일과 마감일 > 시작일이 마감일보다 늦으면 보내기 전에 막는다 | 〃 |
| 〃 | 요청 갈래의 시작일과 마감일 > 앞뒤가 맞으면 그대로 나간다 — 막는 것은 뒤집힌 경우뿐이다 | 〃 |
| `src/features/work/CreateWorkLayout.test.tsx` | 기본 정보의 참조자와 결재자 > 요청 갈래에도 시작일이 서고 그대로 실려 나간다 | 〃 |
| `src/features/work/TaskDetailDates.test.tsx` | 메타 정보 격자 (SPEC-007 §2.10.2) > 짝의 한쪽만 비면 그 칸 자리만 빈다 — 실제 시작·종료가 없으면 오른쪽이 빈 칸이다 | 격자 배열 `toEqual` 불일치 |
| 〃 | 메타 정보 격자 > 시작 전 업무 — 실제 두 값의 행은 서지 않는다 | 〃 |
| 〃 | 메타 정보 격자 > 담당\|출처 짝, 결재\|참조는 둘 다 있으면 한 줄의 짝이다 | 〃 |

네 파일 모두 WP1-FE 가 여는 파일(회의 모달·메시지함 첨부·labels)과 겹치지 않는다. 원인은 조사하지 않았다(범위 밖) — 날짜에 기대는 시험(달력에서 날짜 단추를 찾지 못함)으로 보이나 확인하지 않았다.
