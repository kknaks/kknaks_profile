# archive/

## 1. 개요

**정의**
- 버림이 아니라 **상태**다. 현역이 아니면 여기로 내린다. 끝났든 손을 뗐든 마찬가지다.
- 그래서 `projects/` 에는 지금 살아 있는 것만 남고 목록이 선명해진다.

**되돌릴 수 있다.**
- 다시 그 일을 맡게 되면 `projects/` 로 이관한다. 지우는 게 아니라 자리를 옮기는 것이다.

**구조**

```text
para/archive/
├── company/       회사에서 했던 일 — 현역이 아닌 제품
└── summer-star/   여름별컴퍼니 — 손 뗀 것
```

`projects/` 와 **같은 모양으로 나눈다.** 이관이 소속을 건너뛰지 않으므로 자리가 그대로
대응한다 — `projects/company/<제품>` 이 `archive/company/<제품>` 으로 내려간다.

---

## 2. company/

**무엇**
- 회사에서 했던 일. `sot: external` 이다 — 원천이 회사 레포라 여기 남는 것은 **내 경험뿐**.

**구조** — `projects/company/` 와 같다.

```text
company/<제품>/
├── README.md      제품 지도 (있으면)
├── showcase.md    상세 — 개요·주요기능·핵심 설계·아키텍처·기술스택
└── log/           작업 회고 — YYYY-MM-DD-<slug>.md (있으면)
```

**`showcase.md` 는 현역과 같은 양식이다.** [[showcase|templates/projects/showcase.md]] 를
따른다 — frontmatter 없이 본문만(메타는 DB), 채용 담당자가 위에서 아래로 읽는 순서로.
아카이브라고 양식을 낮추지 않는다. 경력의 증거다.

**공개 여부는 DB 가 정한다.** 파일이 archive 에 있다고 자동으로 숨겨지는 게 아니다 —
`product.visible` 로 표면 노출을 가른다. archive 는 「현역인가」의 축이고 공개는 별개다.

---

## 3. summer-star/

**무엇**
- 여름별컴퍼니에서 하다 손 뗀 것. `sot: here` 라 기획·스펙까지 여기 있었다.

**구조** — `projects/summer-star/` 의 단계 구조를 그대로 안고 내려온다. 이관이 자리를
바꾸는 것이지 내용을 덜어내는 게 아니다.

---

## 4. 이관 규칙

- **소속을 건너뛰지 않는다.** `projects/company/x` → `archive/company/x`. 폴더가 대응하므로
  되돌릴 때도 자리를 그대로 되짚는다.
- **덜어내지 않는다.** showcase·log·스펙을 그대로 안고 내려온다. 아카이브는 압축이 아니다.
- **되살릴 때는 반대로.** 다시 맡으면 `projects/` 로 올리고, 살아 있는 것만 남긴다는 규칙을
  회복한다.
