---
type: work
id: WORK-001
title: ""
status: todo
product: ""
work_type: release
platform: ""
target_version: ""
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 0
created_at: 2026-05-28
updated_at: 2026-05-28
tags:
  - product/
  - doc/work
  - work-type/release
  - status/todo
links:
  baselines: []
  decisions: []
  specs: []
  works: []
  releases: []
  related: []
---

# Title

<1-2줄 요약: 어떤 버전을 어느 스토어/채널에 출시·심사하는 작업인지 적는다.>

> `work_type: release` 작업. 출시 준비·심사 제출·심사 대응·운영 체크를 추적한다.
> *어떻게* 배포/제출하는지 재사용 절차는 `40-architecture/deploy/`에, 출시된 *결과* 요약은 `60-release/`에 둔다.
> 이 문서는 *이번 제출 시도*의 체크리스트·제출 기록·심사 결과 상태를 담는다.

## Work Summary

| Field | Value |
|---|---|
| Type | release |
| Platform |  |
| Target Version |  |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Next |  |

## 출시 대상

| Item | Value |
|---|---|
| Platform / Store |  |
| Version |  |
| Build |  |
| 배포 채널 |  |
| 재사용 런북 | `40-architecture/deploy/...` |

## 심사 체크리스트

제출 전에 충족해야 하는 항목. 누락 시 스토어 validation/심사에서 거부된다.

| # | 항목 | 충족 | 근거/비고 |
|---|------|------|-----------|
| 1 | 빌드/서명/버전 | [ ] |  |
| 2 | 스토어 메타데이터(설명·키워드·카테고리) | [ ] |  |
| 3 | 스크린샷(기기별) | [ ] |  |
| 4 | 개인정보(App Privacy)·연령 등급 | [ ] |  |
| 5 | Export compliance | [ ] |  |
| 6 | 심사 노트·데모(필요 시 영상/계정) | [ ] |  |

## 제출 기록

각 제출 시도를 누적한다.

| 날짜 | Version (Build) | 채널 | 결과 | 비고 |
|---|---|---|---|---|
|  |  |  |  |  |

## 심사 결과

심사 반려/승인 로그. 반려 사유 → 수정 → 재제출을 누적한다.

| 날짜 | 상태 | 사유 / 메모 | 후속 조치 |
|---|---|---|---|
|  |  |  |  |

## 출시 정보

이 작업이 생성할 release note.

| Resulting Release | Action | Notes |
|---|---|---|
|  | create `60-release/release-*.md` |  |

## Acceptance Criteria

- [ ] 심사 체크리스트가 모두 충족됐다.
- [ ] 스토어 심사를 통과(또는 승인)했다.
- [ ] 출시 후 `60-release/`에 release note를 생성했다.

## Done Criteria

- [ ] 제출 기록과 심사 결과가 최신 상태다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.
- [ ] 출시 완료 시 관련 release note 링크를 frontmatter `links.releases`에 추가했다.

## Open Issues

- 
