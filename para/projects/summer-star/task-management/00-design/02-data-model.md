# 데이터 모델

## Task (업무)

| 필드 | 타입 | 필수 | 생성 시 입력 | 비고 |
|---|---|---|---|---|
| `id` | string | ✓ | 자동 | |
| `title` | string | ✓ | ✓ | 유일한 필수 입력값. 인라인 편집 대상 |
| `type` | enum | ✓ | ✓ | `미팅·회의` \| `개인 업무` \| `문서·보고` |
| `status` | enum | ✓ | 자동 | 생성 시 항상 `시작전`. `05-status.md` |
| `projectId` | string \| null | — | ✓ | 프로젝트 연결. 미지정 허용 |
| `startDate` | date \| null | — | ✓ | |
| `endDate` | date \| null | — | ✓ | 없으면 리스트 종료일 칸 비움, D-day 미표시 |
| `background` | text | — | ✓ | 왜 하는가. 인라인 편집 |
| `goal` | text | — | ✓ | 무엇이 되면 끝인가. 인라인 편집 |
| `todos` | Todo[] | — | ✓ | 진행률 계산 근거 |
| `memos` | Memo[] | — | — | 생성 시 비어 있음 |
| `references` | Attachment[] | — | ✓ | 참고자료. 자료함/링크 |
| `deliverables` | Attachment[] | — | — | 결과자료. 완료 처리 시 등록 |
| `relatedTaskIds` | string[] | — | ✓ | `06-related-tasks.md` |
| `logs` | Log[] | ✓ | 자동 | 시스템 기록. 사용자 입력 불가 |
| `cancelReason` | string \| null | — | — | 상태가 `취소`일 때만 |

## Todo

| 필드 | 타입 | 비고 |
|---|---|---|
| `id` | string | |
| `text` | string | |
| `done` | boolean | |
| `dueDate` | date \| null | 리스트에 `오늘` / `08.29` 형식으로 표시 |

진행률 = `done` 개수 / 전체 개수. 상세 헤더에 `2 / 5` + 바로 표시.

## Memo

| 필드 | 타입 | 비고 |
|---|---|---|
| `id` | string | |
| `text` | string | |
| `createdAt` | datetime | 표시: 당일이면 `오늘 09:12`, 아니면 `08.28 16:40` |

작성자 필드 없음(단일 사용자). 최신순 정렬.

## Attachment

| 필드 | 타입 | 비고 |
|---|---|---|
| `id` | string | |
| `kind` | enum | `file` \| `doc` \| `link` |
| `name` | string | |
| `size` | number \| null | 파일만. 표시 `2.4MB` |
| `sourceId` | string \| null | 자료함 문서 id |

## Log

| 필드 | 타입 | 비고 |
|---|---|---|
| `id` | string | |
| `text` | string | 예: `상태 시작전 → 진행중`, `할일 2건 완료`, `참고자료 2건 첨부`, `업무 생성` |
| `createdAt` | datetime | |

작성자 없음. 최신 1건만 dot `#7181F8`, 나머지 `#D9D9D9`.

## 표시 규칙

- 날짜: 리스트 `08월 27일`, 카드·드로어 `08.27`, 기간 `08.27 – 08.29`
- D-day: 종료일이 오늘이면 `D-0`(#7181F8), 이후면 `D-1`(#757575), 지난 경우 `05-status.md`의 지연 규칙
- 취소된 업무 제목: `#9EA2AE` + line-through
