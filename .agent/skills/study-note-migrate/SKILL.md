---
name: study-note-migrate
description: inbox/_restored/ 에 복구해 둔 옛 학습 필기(bitcamp·codingTest·BackendSchool 등) 하나를 resources/source/ 로 옮기고, 그 안의 개념을 resources/concept/ 로 쪼개 4층 지식모델에 편입한다. 한 번에 출처 파일 하나씩만 다룬다. 트리거 "학습노트 이관", "다음 노트 정리", "Day NN 정리", "bitcamp 노트 옮겨".
allowed_tools: [Read, Write, Edit, Bash, Grep, Glob]
runs_scripts:
  - "../../scripts/knowledge_bundle_check.py"
---

# Study Note Migrate — 옛 학습 필기 → source + concept

`inbox/_restored/` 에 복구한 학습 필기를 4층 지식모델(`source` → `concept` →
`synthesis` → `execution`)로 옮긴다.

> 복구된 159개 파일 중 **학습 필기는 149건**이다. 나머지 10개는 이미지·drawio 였고
> `resources/source/assets/` 로 옮겼다. 「159건」을 노트 수로 세지 않는다.

> **이 필기는 작성자가 개발을 처음 배우며 개념을 쌓은 기록이다.** 빨리 끝내는 것이
> 목적이 아니다. 한 파일에서 나올 개념을 다 뽑는 것이 목적이다.

## 작업 단위는 개념이 아니라 **출처 하나**다

개념은 서로를 `[[]]` 로 가리킨다. `상속` 만 만들고 멈추면 `[[polymorphism]]`·
`[[abstract-class]]`·`[[method-overriding]]` 이 전부 dead link 로 남는다.

**한 출처에서 나오는 개념을 한 묶음으로 끝까지 만든다.** 작업 중 링크가 깨져 있는 건
정상이다 — 묶음이 닫힐 때 0이면 된다.

한 번에 **출처 파일 하나**만 다룬다. 여러 개를 동시에 열지 않는다.

## 절차

### 1. 출처를 고르고 통째로 읽는다

**순서는 `bitcamp` 를 날짜순으로 처음부터다.** 작업자가 따로 지정하지 않으면 남은 것 중
가장 이른 날짜를 집는다.

```bash
ls inbox/_restored/bitcamp/*.md | sort | head -1
```

건너뛰지 않는다. 배운 순서대로 가야 뒤 노트가 앞 개념을 `[[]]` 로 가리킬 수 있고,
앞을 비워 두면 그 링크가 전부 dead link 가 된다. `bitcamp` 가 끝나면 `BackendSchool` →
나머지 순으로 간다.

> `2024-07-01-Day26` 만 시범 삼아 먼저 했다. 순서에서 벗어난 유일한 건이고, 거기까지
> 오면 이미 끝나 있으니 넘어간다.

**읽기 전에 개념 목록을 추측하지 않는다** — 소제목이 곧 개념 후보다.

### 2. `resources/source/` 로 옮긴다

```bash
mv inbox/_restored/{그룹}/{파일}.md resources/source/{파일}.md
```

frontmatter 를 넣는다. 없으면 그래프에 안 잡힌다.

```yaml
---
type: reference        # source 층은 type: reference 다 (디렉토리가 아니라 type 이 층을 정한다)
id: {파일명 stem}
title: {원본 제목}
tags: [...]
---
```

**frontmatter 는 본문과 다르다 — 여기 있는 오류는 고친다.**

옛 노트는 앞 파일 frontmatter 를 복사해 쓴 흔적이 많다. Day03 은 Java 노트인데
`summary` 가 Day02 것("git 개념 및 Application 개념")이고 `tags` 에 `git` 이 남아 있었다.

- **복사돼 온 `summary`** — 그 노트의 내용으로 다시 쓴다
- **내용에 없는 `tags`** — 뺀다. Java 노트에 `git` 이 남으면 태그 검색이 거짓으로 답한다
- **콤마가 든 단일 항목** (`- bitcamp, sc기초`) — 항목을 쪼갠다. 태그 두 개가 아니라
  `"bitcamp, sc기초"` 한 개로 읽히던 것이다

없는 값을 새로 채우지는 않는다 — **틀린 것을 고치는 것과 살을 붙이는 것은 다르다.**

본문과 갈리는 이유: 본문은 *그때 무엇을 배웠나*의 기록이라 틀린 것도 증거로 남길 값이
있지만, frontmatter 는 *그래프가 이 노트를 어떻게 취급하나*를 정하는 기계용 값이다.
여기가 틀리면 옛 기록이 보존되는 게 아니라 검색과 그래프가 조용히 거짓말을 한다.

본문에서 고치는 것은 **형식뿐이다.**

- 4칸 들여쓰기 코드블록 → ` ```java ` 펜스로 변환
- 깨진 표·리스트 복구
- `#` 없이 텍스트로만 있는 제목 줄, setext(`----`) 제목 → 같은 층의 `#` 제목으로
- **티스토리 내보내기 잔재 제거** — `{#code_1717487665585}` 같은 마커, 레포 밖을
  가리키는 깨진 상대링크(`[x](../../../bitcamp-mystudy/...)`). 필기가 아니라 플랫폼이
  남긴 것이라 지운다. frontmatter 와 같은 논리다 — 남겨두면 보존이 아니라 렌더가
  거짓 링크를 보여준다

**내용은 고치지 않는다.** 오탈자도, 잘못 배운 것도 그대로 둔다. 이건 그때의 기록이고,
바로잡을 것이 있으면 **개념 노트의 `## 경계와 오해`** 에 적는다.

#### 이미지 링크

로컬 이미지는 `resources/source/assets/` 에 있다. 이름이 겹쳐서(`img.png` 가 세 그룹에
있었다) 그룹 접두사를 붙여 뒀다 — `ncpcloud-img_1.png`, `backendschool-img.png`.

**옮기는 노트가 로컬 이미지를 참조하면 `assets/{파일명}` 으로 고친다.** 단, 복구된
이미지는 10개뿐이고 **참조 중 대부분은 이미 대상 파일이 없다**(`Day31` 의
`image-6.png`~`image-14.png`, `k8s` 의 `../../assets/notes/`, `work` 의
`/assets/img/`). 없는 것을 만들어 내지 말고, 깨진 채로 두고 보고에 적는다.

### 3. 개념을 뽑는다

`templates/knowledge/concept.md` 가 양식 원천이다. **읽고 따른다.**

소제목 하나가 개념 하나로 곧장 가지 않는다. 「1.2 클래스 상속」·「1.3 부모 생성자 호출」
은 **한 개념(`상속`)의 정의와 예시**다. 반대로 한 소제목에 두 개념이 섞여 있기도 하다.

파일명은 **영문 kebab-case** (`method-overriding.md`). 사람이 부를 이름은 `aliases` 가
받는다.

놓치기 쉬운 것 셋:

- **링크는 영문 stem 으로 건다** — 파일명이 `inheritance.md` 면 `[[inheritance]]` 가
  그대로 풀린다. `aliases` 는 필수가 아니라 **다른 이름으로 찾게 될 때만** 넣는 보조다
  (약어 · 흔한 오기 · 한국어 표기). 옵시디언은 `title` 을 안 읽으므로, 별칭에 없는
  이름으로 링크하면 새 빈 노트가 생긴다는 것만 기억한다.
- **`up:` 은 출처 stem** 을 가리키고, `## 출처` 본문에도 `[[stem]]` 이 있어야 한다
  (`up:` 만 있고 본문에 없으면 L3 위반).
- **`## 사용 예시` 는 선택이다.** 코드로 보일 수 있는 개념에만 둔다. 원론적·추상적
  개념(법칙·성질·전략)에 억지로 코드를 붙이면 개념이 좁아진다. 다만 **출처에 예시
  코드가 있으면 반드시 살린다** — 그게 그 필기를 읽은 값의 절반이다.

「정의」와 「사용 예시」는 역할이 다르다. **정의는 문법 골격**(`Child extends Parent`),
**사용 예시는 도메인 코드**(`SmartPhone extends Phone`). 원본이 대개 이미 그렇게 나뉘어
있다.

### 4. 이미 있는 개념은 새로 만들지 않는다

```bash
ls resources/concept/
grep -rn "aliases:" -A6 resources/concept/ | grep {찾는말}
```

같은 개념이 이미 있으면 **그 노트에 `up:` 으로 이번 출처를 추가**하고 부족한 내용을
보탠다. 새 파일을 만들면 SoT 가 둘로 갈라진다.

### 5. 묶음을 닫는다

```bash
python3 .agent/scripts/knowledge_bundle_check.py {출처_stem}
```

**0건이 될 때까지 끝내지 않는다.** 위반이 남았는데 "나중에" 로 넘기지 않는다 — 다음
세션에서 그 dead link 가 어디서 왔는지 아무도 모른다.

### 6. 보고하고 멈춘다

커밋은 작업자가 확인한 뒤에 한다. 보고에 담을 것:

- 출처 1건 → 개념 N건 (새로 만든 것 / 기존에 보탠 것 구분)
- 뽑지 **않은** 소제목과 그 이유 (너무 얕음 / 이미 있음 / 개념이 아니라 실습)
- 검사기 결과

**뽑지 않은 것을 반드시 적는다.** 조용히 빠뜨리면 나중에 "다 옮겼다" 로 읽힌다.

## 하지 않는 것

- `inbox/_restored/` 의 다른 파일을 미리 손대기
- 원본 필기 내용 교정
- 한 번에 여러 출처 처리
- `products/**` 수정 (이 스킬 범위 밖이다)

## 진행 상황

```bash
ls inbox/_restored/*/ | wc -l          # 남은 것
ls resources/source/ resources/concept/ # 옮긴 것
```
