
# [etl] WORK-001 WP4 — reviewer WARN W-1 ~ W-3 반영

너는 consult-analysis `etl` 워커다(load/verify 를 쓴 그 워커). 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석`.

## 입력
- 리뷰 `orchestration/work/consult-layer1/review-layer1-report.md` §WARN W-1 ~ W-3
- SPEC-001 **0.2.1**(`para/projects/summer-star/consult-analysis/20-spec/spec-001-layer1-schema.md`) — §1 · §4.1 · §5.1 · §5.4 의 G-12 확장 · G-13 신설
- WORK-001 WP4 행

## 할 일
1. **W-1** `load_layer1.py:180` 근처 — 보관함 바로 아래의 폴더도 `*.json` 도 아닌 보통 파일(숨김 아님) → G-12 로 멈춤(채널 · 보관함 · 규칙 번호만 찍음 · 파일명 금지)
2. **W-2** `load_layer1.py:191-192 · 487-489` — 원본 파일 읽기 실패(열기 오류 · 비 ASCII 바이트 · JSON 깨짐) → G-13 으로 멈춤 · 채널 · 보관함 · 몇 번째 방 · 규칙 번호. 번호 없는 「예기치 않은 오류」 경로가 원본 읽기에서 안 나오게. `verify_layer1.py` 도 같은 원본 읽기 실패에서 위치를 찍고 종료 1 이 되는지 확인
3. **W-3** 시험 추가 — G-12 보통 파일 · G-13 세 꼴(비 ASCII · JSON 깨짐 · 열 수 없음은 가능하면) · G-6 최다 발신자 동률 · G-6 채널에 방 0개
4. 실물 다시: load → verify(274칸 일치 · 종료 0) · unittest 전부 OK

## allowed_paths
- `para/projects/summer-star/consult-analysis/scripts/`
- `para/projects/summer-star/consult-analysis/data/` (생성물만)

## 하지 말 것
- SPEC · WORK 수정 금지 · 2층 금지 · 외부 패키지 0 · 출력 · 코드 · 시험에 고객 정보 0

## 검증
- `python3 -I -m unittest discover -s para/projects/summer-star/consult-analysis/scripts/tests` 전부 OK(수)
- verify 274/274 · 종료 0
- 고객 이름 · 폴더명 grep 0(메모리 목록 · 보관함 이름 오탐은 따로)

## 완료 보고 — 문구 변경 금지
> preamble 의 코디네이터 핸들이 아래와 다르면 preamble 이 맞다.
- 커밋 · push · PR 금지. 끝나면 두 명령 모두:
```bash
orca orchestration send --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "etl 완료: WP4" --body "변경 / 시험 수 / verify / 미결"
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[worker_done] etl 완료 — WP4(W-1~W-3). 상세는 인박스." --enter
```
