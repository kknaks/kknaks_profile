# [backend] 고도화 2차 E2E-6 조사 — AX 가 업무 초안 전에 무엇을 찾아볼 수 있나 (읽기 전용)

너는 이 워크트리에서 조사·Phase 1 을 한 **strong-hajin `backend` 워커**다. 역할 문서·AGENTS 는 앞 판과 같다. 작업 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` (Phase 1 커밋 `6efdac1` 위).

## 0. 이것은 조사다 — 고치지 마라
코드를 한 줄도 바꾸지 않는다. 산출물은 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/be-survey2-report.md` 한 장. 「이렇게 고치자」는 쓰지 않고 지금 무엇이 있고 어떻게 도는지만 적는다. 서버·DB·codex 를 띄우지 마라(코디의 로컬 스택이 8001·5176·54329 에 떠 있다 — 건드리지 마라).

## 1. 왜
사용자 로컬 E2E: 「○○ 업무 만들어 줘」 → 실물 대화의 도구 호출이 `task_list` · `list_projects` · `task_create_self` 셋뿐이었다. graph_search·회의·자료 조회 0. 체크리스트·내용은 제목만 보고 일반론으로 나왔다.
사용자 계약(E2E-6): **초안 전에 주제 관련 회의(회의록·할 일)·기존 업무(내용·체크리스트)·자료를 찾아 업무 내용·체크리스트의 근거로 쓰고, 연결(프로젝트·참고·선행·상위)도 거기서 찾는다.** 한 후보로 확정될 때만 연결(현행). **사람·날짜 채움은 하지 않는다.**

## 2. 물음 (모든 답에 파일:줄)
1. **AX 가 쓸 수 있는 조회 도구 전부** — 카탈로그(`tool_catalog.py`)의 이름·설명·입력 스키마·돌려주는 것. 특히 graph_search·graph 계열, 회의(회의 목록·회의 상세·회의록·할 일), 업무(목록·상세·체크리스트), 자료 검색. 각 도구가 **내용(본문·체크리스트·회의록 텍스트)** 을 돌려주나, 이름·ID 목록만 주나
2. 업무 생성 턴에서 **도구를 고르게 하는 문장 전부** — 라우팅 정책(`codex_cli.py` 정책 6절), 관계 지침, 도구 설명 안의 「먼저 부르지 말라」「회의용」 같은 제약. 1차 Phase 5(`33e8f1b`)에서 무엇을 바꿨고 무엇이 아직 막고 있나. 원문 인용
3. 실물 대화가 `task_list`·`list_projects` 만 부른 이유로 코드에서 보이는 것(정책 문장·도구 설명 순서·턴 예산·도구 수 제한 등)
4. **근거 묶기** — 조회한 회의·업무·자료를 답변 근거(answer resources)·초안 근거로 묶는 길. 1차 Phase 5 의 `_remember`·project 참조 종류. 회의록/회의 할 일/자료 조각이 근거 종류로 있나, 초안(SubjectVersion·Submission Evidence)에 근거가 붙는 길이 있나
5. 권한 — 조회 도구가 principal 권한으로 거르나(남의 회의·업무 내용이 새지 않나)
6. 비용·시간 — 관련 도구의 결과 크기 상한, 턴 타임아웃, 지금 업무 생성 턴의 평균 도구 호출 수를 알 수 있는 테스트·로그
7. 테스트 — 정책 문장을 단언하는 테스트(`test_ax_work_lookup_policy.py` 등), 도구 호출 순서를 보는 테스트가 있나

## 3. 리포트 형식
```
# 고도화 2차 E2E-6 서버 조사
## 0. 한 줄 요약
## 1~7. 물음 번호대로
## 8. grep 개수표
## 9. 조사 한계
```
실명·메일 금지(공개 레포 아카이브).

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_2cf4fdea-dd6c-411f-b344-41b6d61078de \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: E2E-6 조사" \
  --body "리포트 경로 / 물음별 한 줄 / 조사 한계"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] backend E2E-6 조사 완료 — <한 줄>. 리포트 be-survey2-report.md" --enter
```
