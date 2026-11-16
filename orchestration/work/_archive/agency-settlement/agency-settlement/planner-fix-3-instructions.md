# planner 수정 3판 — 별도 프로젝트로 옮김 (SPEC-001 0.2.0 · WORK-001)

**사용자 정정**: cc-prototype 의 기능 폴더가 아니라 **별도 프로젝트 `agency-settlement`** 이다(_RESUME §2 새 줄 · DEC-001 D-08 고침). 코디가 문서를 옮기고 번호를 바꿨다:

- `para/projects/summer-star/agency-settlement/` — DEC-001(옛 DEC-009) · SPEC-001(옛 SPEC-007) · WORK-001(옛 WORK-011) · OQ-1nn(옛 OQ-9nn) · D1-nn(옛 D9-nn). 기계 치환이라 어색한 곳이 남았다
- 코드 레포 = `kknaksss/agency-settlement`(private · 로컬 `/Users/kknaks/git/toy_pr2/agency-settlement` · README · .gitignore 만 있음). **레포 루트에 `back/` · `front/`** — `sales/` 폴더 없음. cc-prototype 은 디자인 · KOS 클라이언트 본보기로 **읽기만**
- cc-prototype 의 문서 번호를 가리킬 때는 「cc-prototype DEC-001」처럼 프로젝트 이름을 붙인다

할 것:
1. SPEC-001 · WORK-001 에서 `sales/` · 「새 기능 폴더」 · 「kknaksss/cc-prototype 루트」 · 「다른 기능 import 0」 · 「루트 README 기능 표 한 줄」 · cc-prototype DEC-001 D-02 · D-03(기능 폴더 규칙) 근거 등 **옛 구조 문구를 전부 grep 해서** 새 구조로 고친다. 「procedure 의 `.env` 에 넣지 않는다」류는 「이 레포 `back/.env` 에만」으로
2. 근거 태그 · 링크 · frontmatter(id · product · links) · 부록 A 가 새 번호와 맞는지
3. 판 0.2.0(구조 변경) · 인덱스 `20-spec/README.md` · `30-work/README.md` 판 맞춤
4. 검증 §8(근거 · public grep: 실명 · 실제 금액 · 에이전시 이름 · 키 0) + `grep -n "sales/\|기능 폴더\|cc-prototype 루트"` 결과를 보고에 적는다

allowed_paths: `para/projects/summer-star/agency-settlement/20-spec/` · `30-work/` 만(DEC-001 · README 는 코디 몫). 끝나면 원 브리프 §9 두 채널(같은 task/dispatch · subject 「planner 수정 3판 완료」).
