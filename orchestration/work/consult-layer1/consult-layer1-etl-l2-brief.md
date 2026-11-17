
# [etl] WORK-002 WP1 · WP2 · WP3(표본까지) — 2층 규칙 판정 · 사람 확인 큐 · LLM 라벨 표본

너는 consult-analysis `etl` 워커다(1층 load/verify 를 쓴 그 워커). 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석`.

**사용자가 결과를 빨리 원한다.** 이번 태스크는 표본 LLM 결과까지 내고 멈춘다 — 전체 1,883방 라벨은 코디가 표본을 본 뒤 다음 태스크로.

## 1. SSOT
- `para/projects/summer-star/consult-analysis/20-spec/spec-002-layer2-analysis.md` **0.1.0 accepted** — 계약. 없는 건 발명하지 마라
- `para/projects/summer-star/consult-analysis/30-work/work-002-layer2-analysis.md` — WP1 ~ WP3 · 수용 기준
- `para/projects/summer-star/consult-analysis/10-decision/decision-002-layer2-analysis.md` — **D-14 ~ D-18 = SPEC §8 OQ-201 ~ 205 를 전부 권장 A 로 닫음**(claude -p · handoff 표시만 · confirmed 없음 · `zh` 값 · flow 표 포함)
- 1층 DB `para/projects/summer-star/consult-analysis/data/layer1.sqlite` — `l2_` 테이블만 쓴다. 1층 테이블은 손대지 않는다

## 2. 할 일
1. **WP1** `scripts/judge_layer2.py` + `scripts/requirements-layer2.txt`(opencc-python-reimplemented 버전 고정). 의존성은 스크립트 옆 가상환경(`scripts/.venv` — gitignore 대상이니 `.gitignore` 는 코디가 처리 · 너는 만들기만) 또는 `uv run --with` 중 편한 쪽. 실행 후 보고: 단계 건수를 SPEC §2.3 표와 나란히 · 번체 / 간체 / `zh` / en / ko / ja / other / none 방 수(채널별) · `flow` 메시지 수 · 자동응답 받은 방(FB) · 국적 ① ③ 분포
2. **WP2** `l2_review_queue` + `data/review_queue.csv`(본문 포함 · 로컬만 · 고객 이름은 넣지 말고 `[C]`/`[S]` 머리표 + 본문 · 방 id). 사유별 건수. 50 넘으면 멈춤. `--decisions data/review_decisions.csv` 반영 경로까지 구현(형식: `queue_id,human_stage`)
3. **WP3 표본까지** `scripts/label_layer2_llm.py` — SPEC §5 그대로. 로컬 `claude -p`(도구 끔 · 표준 입력) · 표본 30방(단계 3종 × 채널 고르게) 을 **작은 모델(haiku) · 큰 모델(sonnet)** 둘로 → 주제 · 시술 일치율 · `other` 비율 · 실패 건수 · 방당 걸린 시간 보고. DB 에는 **큰 모델 결과만** `l2_llm_label` 에 남기고(모델 이름 칸에 기록) 작은 모델 결과는 메모리 비교만
4. 표본 30방의 라벨 결과는 코디가 볼 수 있게 `data/llm_sample_review.csv`(로컬 · 방 id · 단계 · 언어 · 두 모델 라벨 · 고객 본문 앞 300자) 로 낸다 — 커밋 안 됨
5. 단위 시험(`scripts/tests/` · 지어낸 문장만): 칸 세기 · 자동응답 판별 · 언어 판정 · 단계 규칙 · LLM 출력 검증(깨진 JSON · 목록 밖 값 → 실패)

## 3. allowed_paths
- `para/projects/summer-star/consult-analysis/scripts/`
- `para/projects/summer-star/consult-analysis/data/` (생성물만)

## 4. 하지 말 것
- 1층 테이블 · SPEC · WORK · DEC 수정 금지 · 전체 1,883방 라벨 금지(표본까지) · `stats` · 보고서 금지(다음 태스크)
- 규칙 건수가 SPEC 과 다르면 규칙을 비틀지 말고 차이와 이유를 보고
- 표준 출력 · 코드 · 시험 · 보고에 고객 본문 · 이름 · 계정명 · 폴더명 0. LLM 입력도 파일로 쓰지 않는다(표준 입력으로만)

## 5. 검증
- 1층 verify 가 여전히 274/274(1층 무손상)
- WORK-002 수용 기준 1(규칙 테이블 행 수) · 2 · 3 · 4 · 6 · 8
- 단위 시험 OK 수
- 고객 정보 0 대조(1층 때와 같은 방식)

## 6. 완료 보고 — 문구 변경 금지
> preamble 의 코디네이터 핸들이 아래와 다르면 preamble 이 맞다.
- 커밋 · push · PR 금지. 끝나면 두 명령 모두:
```bash
orca orchestration send --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "etl 완료: WP1~WP3 표본" --body "변경 파일 / 단계·언어 건수(SPEC 대조) / 큐 건수 / 표본 두 모델 비교 / 시험 / 미결"
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[worker_done] etl 완료 — 2층 판정 · 큐 · LLM 표본. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[질문] etl: <질문>" --enter`
