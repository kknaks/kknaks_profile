# [backend] 업무·프로젝트 도메인 read-only 조사 — 「프로젝트」 화면이 요구하는 사실 D-1~D-9 대조

너는 **strong-hajin `backend` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 아래를 먼저 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/design-read-projects.md` ← **이번 조사의 출발점.** 코디네이터가 시안을 읽고 뽑은 「화면이 요구하는 사실 D-1~D-9」가 §8 에 있다
- 코드 레포 `AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (**이번 작업은 read-only 조사라 PR 없음**)

⚠ **같은 워크트리에 `frontend` 워커가 동시에 붙어 있다.** 그쪽은 `frontend/` 를 조사한다.
둘 다 **아무 파일도 고치지 않는다.** 서로의 리포트 파일도 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

이번 조사에는 **새 spec 이 없다.** 계약의 SoT 는 **지금 돌아가는 코드**다.
기존 문서는 배경으로만 읽고, 문서와 코드가 다르면 **코드를 사실로 적고 그 차이를 리포트에 적어라.**

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-003-task-lifecycle-v2.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-004-calendar-scheduling.md` (기간·배정이 여기서 왔다)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md` (선행업무가 여기 있다)

**기대는 개념** — 해당 없음 (조사라 구현 판단이 없다).

## 2. 배경 / 무엇을 하나

회의·업무 워크스페이스에 **「프로젝트」 화면**을 새로 만든다. 확정 시안이 있고(위 §1 의
`design-read-projects.md`), 시안은 **레이아웃·색·위치의 정본**이다. 그러나 **상태값과 논리
구조는 시안이 아니라 우리 코드가 정본**이다 — 시안의 목데이터는 목업이라 우리 도메인과
이름도 개수도 다르다.

그래서 이번 조사의 질문은 하나다:

> **시안을 그리려면 필요한 사실 9개(D-1~D-9)가 우리 백엔드에 지금 있는가? 어떤 이름으로, 어떤 모양으로?**

**아무것도 바꾸지 마라.** 산출물은 리포트 파일 하나다. 구현은 이 조사 결과로 코디네이터와
사용자가 범위를 정한 뒤, 다음 발주에서 한다.

## 3. 계약 (다른 워커와 합의됨)

해당 없음 — read-only 조사. 단, `frontend` 워커가 같은 D-1~D-9 를 **프론트 쪽에서** 조사하고
있으니 **백엔드 사실만** 적어라. 프론트 파일을 읽어 판단하지 마라.

## 4. 조사 항목 — D-1~D-9 전부에 답한다

`design-read-projects.md` §8 의 표가 질문지다. **9개 전부**에 아래 꼴로 답한다:

```
D-N | 판정: 있다 / 없다 / 다르다
    | 우리 이름·모양: <테이블.컬럼 · enum 실값 · 응답 필드명>
    | 근거: <파일:줄> (여러 개면 전부)
    | 시안과의 차이: <한 줄. 없으면 "없음">
```

- **`다르다` 가 제일 중요하다.** 예: 상태가 5종이 아니라 N종이거나, 이름이 `blocked` 가
  아니라 다른 말이거나, 진행률이 저장값이 아니라 파생값이거나.
- **추측 금지.** 못 찾으면 「찾지 못했다 — 이렇게 찾아봤다」로 적어라. 있다고 지어내지 마라.

### 특히 파고들 것

- **D-3 진행률**: 저장 컬럼인가, 체크리스트/하위업무에서 계산되는 파생값인가, **아예 없는가.**
  없으면 「무엇으로 대체 계산이 가능한가」까지 적어라(가능한 재료만 나열, 설계하지 마라).
- **D-4 의존(선행→후행)**: 별도 표인가 컬럼인가. **양방향 조회가 되는가.** 순환 방지가 있는가.
- **D-5 상위–하위**: 몇 단계까지 허용되나. 시안은 **1단계만** 그린다 — 우리가 더 깊으면 그 사실을 적어라.
- **D-7 상태**: **enum 실값을 전부** 적어라(코드에서 그대로 복사). 전이 규칙이 있으면 어디 있는지도.
- **D-1/D-9 프로젝트**: 프로젝트가 **독립 엔티티인가**, 아니면 업무의 라벨/분류인가. 목록 API 가 있나.

### 표면 전수조사 (목록이 아니라 grep 으로 센다)

위 사실들이 **밖으로 나가는 입구를 전부** 센다. 「N개일 것이다」로 시작하지 말고 grep 으로 세라:

- 라우터·엔드포인트 (경로 · 메서드 · 응답 스키마 · envelope 모양)
- operation inventory / 스키마 정의 파일
- 목록 조회의 **필터·정렬·페이징** 현황 — 프로젝트 단위로 업무를 긁는 경로가 이미 있는가
- 마이그레이션 (해당 테이블이 언제 어떻게 생겼나)

## 5. allowed_paths — 이 밖은 건드리지 마라

- **read-only.** 코드·설정·테스트 **어느 것도 수정하지 마라.** 커밋·push 금지.
- **쓰는 파일은 정확히 하나**:
  `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-be-domain.md`
  (scratchpad 에 쓰지 마라 — 터미널이 죽으면 같이 죽는다. 위 절대경로에 직접 써라.)

## 6. 조사 단계

1. 역할 문서 + `design-read-projects.md` + `AGENTS.md` 읽기
2. 도메인 모델·마이그레이션에서 D-1~D-9 의 **저장 구조** 확인
3. 라우터·스키마에서 **표면** 전수조사 (grep 으로 센다)
4. 문서(§1 spec/WP)와 코드가 어긋나는 지점 수집
5. 리포트 1개 작성 → 완료 보고

## 7. 범위 제약 — 하지 말 것

- **설계하지 마라.** 「이렇게 만들면 된다」를 쓰지 마라. 지금 무엇이 있는지만 적는다.
- **고치지 마라.** 조사 중 버그를 봐도 고치지 말고 리포트 말미 「눈에 띈 것」에 한 줄로 남겨라.
- **프론트를 보지 마라** (`frontend/` 는 다른 워커 담당).
- **서버·DB 를 띄우지 마라.** 사용자 포트·프로세스를 건드리지 않는다. 정적 읽기로 끝낸다.
- 테스트를 돌리지 마라 — 이번엔 검증할 변경이 없다.

## 8. 검증

이번 작업의 검증은 테스트가 아니라 **근거**다.

- D-1~D-9 **9개 전부**에 판정이 있다. 빠진 번호가 없다.
- **모든 판정에 `파일:줄` 이 붙는다.** 근거 없는 문장은 쓰지 마라.
- 상태 enum 은 **코드에서 복사한 실값**이다 (기억으로 쓰지 마라).
- 표면은 **grep 결과로 센 수**다 (「주요 엔드포인트」 같은 요약 금지 — 전부 나열).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_fb34b326-d200-4c55-83e7-3a205707772a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 업무·프로젝트 도메인 조사" \
  --body "리포트 경로 / D-1~D-9 판정 요약(있다·없다·다르다 개수) / 가장 큰 차이 3개 / 표면 개수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] backend 완료 — 도메인 조사 리포트 작성. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
