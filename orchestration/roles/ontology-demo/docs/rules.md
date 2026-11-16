# @ontology-docs — 규칙

## 문서 체계 (위반 = FAIL)
- **규칙의 SoT 는 `para/projects/project.md`** — 단계 역할·frontmatter·links·상태 값·
  index/log 동기 갱신 전부 그 문서를 따른다. 양식은 `templates/projects/`.
- **1 파일 = 1 건.** baseline 은 보존이 우선(날것 유지), decision 은 선택지·결정·근거,
  spec 은 외부 계약만(내부 구현·work ID 본문 참조 금지), work 는 빌드 계획.
- **본문 복사 금지** — 상위/하위 문서는 ID 와 wikilink 로만 잇는다. 관계는 frontmatter
  `links` 가 소유. SPEC→WORK 는 단방향(work 의 `links.specs` 가 갖는다).
- **문서를 만들거나 고치면 해당 단계 README(index)와 제품 `log.md` 를 같은 커밋 단위로 갱신.**
- decision 의 `up:`(근거 개념)은 검토 흔적이 남으면 된다 — 억지로 잇지 않는다.
  `up: []` + 사유 한 줄 허용.

## 사실 규칙
- **원천 기록(note)이 사실의 SoT 다** — 기록 01~09 에 없는 수치·결정을 지어내지 않는다.
  기록끼리 어긋나거나 근거가 없으면 그 자리에서 멈추고 질문 채널로 보고한다.
- note 는 스펙이 아니다 — 기록을 요약·재배치해 계약으로 굳히되, **새 해석·새 결정을
  추가하지 않는다.** 결정은 사용자 몫이다.
- **PII** — `patientName`·`birthday`·`phone`·리뷰 작성자명 원값을 문서 본문·예시에도
  쓰지 않는다. 예시가 필요하면 마스킹된 형태로.
- 대조값은 근거와 함께 적는다 (예: 리뷰 1,962 는 csv 파서 기준 — `wc -l` 은 셀 내 개행
  때문에 2,118).

## 스코프 규칙
- allowed_paths(`para/projects/summer-star/ontology-demo/`) 밖 수정 금지.
- 브리프가 지정한 문서 범위만 쓴다 — 다음 단계 문서를 앞질러 만들지 않는다.
- git commit·push·PR 금지 — 워크트리에 변경만 남긴다.

## 리포트 형식

```markdown
# {작업 ID} 결과 보고
## 상태: done / in-progress / blocked
## 산출 문서 — 파일 목록 (신규/갱신 구분)
## index·log 갱신 — 어느 README·log.md 를 어떻게
## 원천 대비 임의 판단 없음 확인 — 어긋난 곳·질문했던 곳 목록
## 이슈/블로커
```
