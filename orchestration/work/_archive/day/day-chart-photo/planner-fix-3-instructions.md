# [planner] fix-3 — 코드 검수가 찾은 판정 틈을 SPEC 에 반영 (결정 C18 ~ C21)

**읽을 것** (이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/`)
- 결정 파일 `chart-photo-decisions.md` 의 **C18 · C19 · C20 · C21-기본값**(새로 들어옴 · 사용자 승인 · 다시 열지 않음)
- 코드 검수 `review-code-1-report.md` 의 W1 ~ W5

**작업 자리**
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` — 지금 커밋 `a896cda0`(PR #960) 위
- allowed_paths `products/day/` · 커밋하지 마라

## 할 것

규칙 31(충돌 판정) · U-14 · 매트릭스 · API 를 고친다.
- **C18**: KOS 동기화 이력(`source=kos`)이 `baseLogId` 뒤에 쌓였어도, 마지막 글(+집도의)이 요청 `base` 와 같으면 DAY 쪽 판정에서 걸리지 않음
- **C19**: 마지막 이력이 같은 직원 · `source=day` · 같은 글 · 같은 담당자면 그 줄은 이미 저장됨으로 본다 — 건너뜀 · 200
- **C20**: 비교 정규화에 CRLF · CR → LF 를 넣는다
- **C21-기본값**
  - 보내는 동안 그 탭 칸을 잠근다(E57 · U-14)
  - 집도의 「한 명」 = 매핑 전 KOS 외부 id 개수(DAY 기준값 · KOS 지금 값 같은 단계)

§4 차이 표 · `10-decision` · `log` 를 갱신한다. 앞 문장은 취소선 관례를 따른다.

## 검증 · 보고

- lint `--strict` 로 `products/day` ERROR 0
- 보고 `planner-fix-3-report.md` + preamble 의 worker_done 두 채널
