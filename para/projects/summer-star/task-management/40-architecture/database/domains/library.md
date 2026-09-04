---
type: architecture
id: DOMAIN-005
title: "library — PARA 폴더와 md 문서"
status: draft
product: "task-management"
created_at: 2026-09-04
updated_at: 2026-09-04
tags:
  - product/task-management
  - doc/architecture
  - architecture/database
links:
  baselines: [BASE-004]
  decisions: [DEC-004, DEC-002, DEC-003]
  specs: []
  works: []
  related: []
---

# library

문서함 — **PARA 고정 트리 + 하위 자유 폴더**, md 문서, 사람이 직접 거는 연결. 업무·회의의 첨부가 여기서 온다.

## Purpose

DEC-004 의 v1 범위를 담는다. **폴더 축과 연결 축이 독립**이라는 것이 이 도메인의 핵심 결정이다.

## Entities / Tables

| Entity/Table | Purpose | Notes |
|---|---|---|
| `folder` | 폴더 트리 | PARA 4종은 `is_system=true` 시드. **하드 삭제** |
| `document` | md 문서 | 소프트 딜리트 |
| `document_tag` | 태그 | 사람이 입력. 태그 마스터 테이블 없음 |
| `document_link` | 연결 | `target_type ∈ {project, task, meeting}` |

## Invariants

- **L-1** **최상위 폴더는 PARA 4종 시드 고정**(`01 Projects` / `02 Areas` / `03 Resources` / `04 Archive`)이다. `parent_id IS NULL` 인 행은 이 넷뿐이고 **삭제·이름 변경 불가**다(DEC-004 §4).
- **L-2** **폴더는 프로젝트를 따라 자동 생성되지 않는다.** 폴더는 사람이 정리하는 축, 연결은 관계 축 — **두 축은 독립**이고 프로젝트 개명·삭제가 폴더에 전파되지 않는다(DEC-004 §4).
- **L-3** **`ext` 는 v1 에서 `md` 만**이다. 그 외 형식은 업로드 단계에서 거부하고 부분 업로드하지 않는다(DEC-004 §3·§7).
- **L-4** **문서는 업로드로만 생긴다.** 문서함에서 빈 문서 만들기도, 회의·업무에서 문서 생성도 v1 에 없다(DEC-004 §4).
- **L-5** **「위치」 경로 문자열을 저장하지 않는다.** 트리·breadcrumb·메타데이터가 쓰는 같은 문자열은 `parent_id` 체인에서 만든다(14-library §경로 일관성 · G-7).
- **L-6** **폴더는 빈 것만 삭제할 수 있고, 하드 삭제**다. 문서가 하나라도 있으면 거부한다 — 복원 수단이 없으므로 통째로 날리는 것을 막는다(DEC-004 §4).
- **L-7** **문서는 소프트 딜리트만**이다. 목록·검색·첨부 선택에서 사라지고 DB 에는 남는다. **휴지통·복원 UI 는 v2**(DEC-004 §4 · §A-12).
- **L-8** **버전 스냅샷을 남기지 않는다.** 편집은 자동 저장으로 본문을 덮어쓰고, 변경 이력 테이블이 없다(DEC-004 §4·§6).
- **L-9** **AI 색인 상태·버전 컬럼을 만들지 않는다.** v2 스코프는 프론트만 그린다(DEC-004 §3 · DEC-001 §v2).
- **L-10** `is_favorite` 는 **목록 정렬에만** 쓴다. 즐겨찾기 필터·전용 화면은 v2 다(DEC-004 §3).
- **L-11** **연결 카드는 문서 쪽에만** 있다. 업무·회의 쪽에 역방향 연결 카드를 만들지 않는다 — 참고/결과자료와 첨부 탭이 이미 그 역할을 한다(DEC-004 OQ-5).
- **L-12** `document_link` 에 **FK 를 걸지 않는다**(`target_type` + `target_id` 다형). 대상 삼종이 서로 다른 테이블이고, 대상이 소프트 딜리트되면 조회 시 걸러낸다.
- **L-13** 자동 링크 추출·백링크·임베딩이 없다. **연결은 전부 사람이 건다**(DEC-004 §3·§6).
- **L-14** 본문은 DB 에 넣지 않는다 — `storage_path` 가 파일을 가리킨다(정보는 DB, 상세는 파일).
- **L-15** 용량은 **표시만** 한다. 상한·차단이 없다(DEC-004 §4).
- **L-16** **검색 테이블·인덱스를 만들지 않는다** — 검색은 v2 다. v1 은 폴더 트리로 탐색한다(DEC-004 OQ-4).

## Related Specs / Works

- SPEC-00x 문서함 (DEC-004 Resulting Spec)
- 소비처: `domains/task.md`(참고자료·결과자료) · `domains/meeting.md`(첨부)
