
# [planner] SPEC-002 · WORK-002 — 2층 판정 · 분석(예약 전환 · 언어별 특징)

너는 consult-analysis `planner` 워커다(SPEC-001 을 쓴 그 워커). 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석`.

**사용자가 결과를 빨리 원한다.** 문서는 etl 이 바로 구현할 만큼만 — 길게 쓰지 마라. 실측은 1층 DB 로 한다(원본 JSON 재집계 불필요).

## 1. SSOT
- `para/projects/summer-star/consult-analysis/10-decision/decision-002-layer2-analysis.md` **accepted** — D-01 ~ D-13 · 열린 것 OQ-201 ~ 203
- `para/projects/summer-star/consult-analysis/00-baseline/baseline-002-conversion-language.md` — 대략치
- DEC-001 · SPEC-001 0.2.1(1층 테이블)
- 1층 DB `para/projects/summer-star/consult-analysis/data/layer1.sqlite` (gitignore · 읽기만 · `python3 -I` + sqlite3)

## 2. SPEC-002 에 들어갈 것 (`20-spec/spec-002-layer2-analysis.md`)
1. **2층 테이블**(같은 SQLite 파일 · 1층 id FK · 판정 주체 / 근거 message_id / 판정 버전 칸 — D-01 · D-02): 메시지 언어 · 방 언어(+ 섞임 비율) · 방 예약 단계 · 국적 · 방 LLM 라벨(문의 주제 · 시술) · 사람 확인 큐
2. **예약 단계 규칙**(D-03 · D-04 · D-07) — 1층 DB 에서 **실측**으로: 자동응답 판별 규칙(우리 메시지 중 반복 문구 · 건수) · 상담사 예약표 판(版)별 머리 문구 · 예약표 칸 사전(언어 · 판별) · 「칸 2개 이상 채움」 판정법 · 경계 사례 정의와 예상 건수(**50 안쪽** · D-05). 채널별 건수
3. **언어 규칙**(D-06) — 번체 / 간체 판별 방법(외부 패키지 허용 · D-13 · 예: OpenCC 또는 번간 대응표) · 라틴 문자 방의 언어 판별 방법 · 메시지 → 방 집계
4. **LLM 라벨 계약**(D-07 · D-08) — 입력(방의 고객 + 우리 메시지 · 길이 제한) · 출력 JSON 스키마(주제 목록 · 시술명 정규화 · 신뢰도) · 로컬 CLI. OQ-201 은 **권장 + 근거**로 올린다(실행은 하지 마라 — 시험은 etl 몫)
5. **통계 정의**(D-10 · D-11) — 항목마다 정확한 계산식(턴 · 시간 · 첫 응답 · KST · 이모지 판별 등) · 분모 · 소표본 표시 기준
6. **산출물**(D-12) — 집계 스크립트가 내는 JSON(차트 페이지 입력) · 보고서 md 위치 `para/projects/summer-star/consult-analysis/50-report/`(새 폴더 · 이 SPEC 에서 정함)의 절 구성. 둘 다 건수 · 비율만
7. 실행 인터페이스(스크립트 이름 · 인자 · 다시 돌리면 2층만 새로) · OQ-202 · 203 은 실측 근거로 권장안

## 3. WORK-002 (`30-work/work-002-layer2-analysis.md`)
- WP: ① 규칙 판정(언어 · 예약 단계 · 국적) ② 사람 확인 큐 출력 ③ LLM 라벨(표본 시험 → 전체) ④ 집계 JSON ⑤ 보고서 md ⑥ 검수. 담당 etl(①~⑤) · reviewer(⑥) · 차트 페이지는 코디
- 수용 기준: 판정 행 수 = 방 · 메시지 수 · 고객 본문 · 이름 0 · 판정 주체 · 근거 id 빠짐 0

## allowed_paths
- `para/projects/summer-star/consult-analysis/20-spec/` · `30-work/`
- 하지 말 것: DEC · BASE 수정 · 스크립트 작성 · LLM 호출 · 문서에 고객 본문 · 이름 인용(규칙 문구 예시는 우리 계정 상용 문구의 **머리 몇 글자**까지만 · 고객 문장 금지)

## 검증
- SPEC 의 규칙 · 건수가 1층 DB 실측 · 근거 D 번호 · 고객 이름 grep 0 · 인덱스 갱신

## 완료 보고 — 문구 변경 금지
> preamble 의 코디네이터 핸들이 아래와 다르면 preamble 이 맞다.
- 커밋 · push · PR 금지. 끝나면 두 명령 모두:
```bash
orca orchestration send --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC-002" --body "변경 / 실측 수치 / 열린 것(옵션+권장)"
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[worker_done] planner 완료 — SPEC-002 · WORK-002. 상세는 인박스." --enter
```
