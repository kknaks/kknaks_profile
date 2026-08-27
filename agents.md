# Agents

에이전트가 이 레포에 들어왔을 때 가장 먼저 읽는 **인덱스**다.

**이 문서는 규칙을 갖지 않는다.** 어디로 가야 하는지만 가리킨다. 규칙을 여기 복사하면 원천이 둘이 되고, 한쪽만 고쳐지는 날 조용히 어긋난다.

## 루트

| 루트 | 담는 것 | 계약 |
|---|---|---|
| `para/` | 문서 — 사실과 판단 | [[para\|para/para.md]] |
| `app/` | 코드 — 그것을 서빙하는 것 | [[architecture]] |
| `orchestration/` | 자동화 — 워커 발주와 검증 | [[orchestration/runbook\|runbook]] |

루트를 셋으로 나눈 근거와 미정 항목은 [[architecture]] 가 갖는다.

## 무엇을 하려는지에 따라

| 하려는 것 | 읽을 것 |
|---|---|
| **문서를 쓰거나 고친다** | [[para\|para/para.md]] — 네 버킷 중 어디인지부터 가른다 |
| **코드·문서 작업을 워커에게 발주** | [[orchestration/runbook\|orchestration/runbook.md]] |
| 구조를 바꾸거나 루트를 추가 | [[architecture]] |
| 리뉴얼이 왜 시작됐는지 · 무엇을 정해야 하는지 | [[CLAUDE]] |

발주는 직접 하지 않는다. 코디네이터가 `runbook.md` 절차를 따라 워커를 띄우고, 워커는 브리프 한 장만 받는다.

## 문서를 쓸 때 — 어디로 내려가나

**규칙은 각 버킷 문서가 갖고, 양식은 `templates/` 가 갖는다.** 여기에 복사하지 않는다.

```text
para/para.md              네 버킷 중 어디인가
├── areas/area.md         personal/ 이냐 concept/ 이냐 · 아홉 영역 중 어디냐 · 개념 규약
│                         양식 → templates/areas/concept.md
├── projects/project.md   company/ 냐 summer-star/ 냐 · 단계 00~70 · 무엇을 어디에 두나
│                         양식 → templates/projects/
└── resources/resource.md 어느 출처냐 · note 하위 · 불변 규약
                          양식 → templates/resources/
```

`archive/` 만 아직 자기 문서가 없다. `para.md` 가 직접 갖고 있다.

## 정할 것 — 첫 갈래는 「어느 레포를 건드리나」

지금 이 문서는 *무엇을 하려는지*로 가른다. 그보다 앞에 와야 하는 갈래가 있다 —
**어느 레포에 변경이 남느냐.** 둘은 일하는 방식 자체가 다르다.

```text
이 레포 밖 (회사 mediness 등)
  → 코디네이터가 된다. 직접 코딩하지 않는다. 워커를 발주한다.
  → orchestration/runbook.md

이 레포 안 (kknaks_profile)
  → 직접 작업한다.
  ├ 문서·지식      → para/
  ├ 코드           → app/
  └ 발주 설정 자체  → orchestration/ (config·roles·templates·scripts)
```

두 레포에 걸치면 **밖이 우선**이다 — 발주 절차를 타고, 이 레포 쪽 변경은 코디가 직접 한다.

아직 이 갈래를 문서 본문에 세우지 않았다. `app/` 내부 구조가 정해지면
**이 문서를 처음부터 다시 쓴다.** 지금은 기록만 해 둔다.

## 아직 없는 것

`app/` 은 비어 있다 — [[architecture]] 「아직 정하지 않은 것」 참고.

옛 규칙 중 `persona-artifacts.md` 의 공개 글(`posts`) 규정이 아직 새 자리를 못 찾았다 —
발행물의 자리가 미정이다.

이전 레포 전체는 `_archive/` 에 동결돼 있다. **읽기 전용이다.** 새 구조에 필요한 것은 거기서 끌어올리되, 그대로 복사하지 않는다.
