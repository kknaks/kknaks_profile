# [skill-editor] 1차 조사 스킬에 사용자 합의 반영

너는 Opus 워커다. 추가 워커를 띄우지 않는다. 이 브리프와 라이브 dispatch preamble이 이번 계약이다. §9는 고정 보고 양식이며 최신 preamble의 정확한 인자·outcome 요구가 우선한다.

## 1. SSOT — 먼저 읽을 것

- `AGENTS.md`
- `orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md`
- `orchestration/work/phub-ledger-redesign/_RESUME.md` (읽기 전용)
- skill-creator 스킬: `/Users/kknaks/Library/Application Support/orca/codex-accounts/46865ee7-2849-47a2-a2fb-16759bec7fb9/home/skills/.system/skill-creator/SKILL.md`

## 2. 배경 / 무엇을 바꾸나

사용자는 첫 원장의 1차 조사 정도면 다음 원장으로 넘어가도 된다고 확인했다. 출력 형식과 종료 기준을 다음처럼 스킬에 반영하라고 했고, 그 뒤 Opus 워커 5명에게 5개 원장을 병렬 발주하라고 했다. 이 워커는 스킬 수정만 담당한다. 원장 조사·결과 수정·발주는 하지 않는다.

## 3. 계약

- 읽기용 결과는 원본 컬럼명·자료형·원문 값·잠정 관찰을 분리한다. 컬럼 구성 표는 필드/JSON 경로 패턴, 자료형·배열/객체 중첩 구조, 실제 원문 예시·위치를 한 행씩 보여준다. 값/구조형 변형·선택적 필드·빈 값도 보존한다.
- 각 항목의 모든 값은 원본 컬럼명을 그대로 써서 보여준다. `moa_summary`를 `moa`로 줄이지 않는다. 배열 순서·각 원문 Pointer를 유지한다. 원문과 관찰을 한 칸에 섞지 않는다.
- 1차 수집·검토 기준을 충족하면 다음 원장으로 넘어간다. 의미 분해·공통 개념 식별·관계 확정은 전체 수집 뒤 비교·설계 단계의 과제로 남긴다.
- 알려진 형태소 분석 오류는 출현 위치·원시 토큰·영향을 표시 또는 구조화해 기록하고 한계를 명시한다. 모든 토큰 정답·최종 의미 해석을 얻기 위해 같은 원장을 반복 조사하지 않는다. 누락·잘못된 Pointer·구간·원문 변형 등 실제 추출 오류는 해결한다. 새 누락·오류 발견이나 원장 간 비교 필요가 생길 때 다시 확인한다.
- 기계 검증과 읽기 검토는 여전히 필요하다. 문맥/복합 표현/형용사·부사/부정/조건 수집을 생략하지 않는다. 단순 토큰·컬럼 목록으로 전수 읽기를 대체하지 않는다.
- 1차 범위 종료와 원장 전체 완료를 분리한다. 열린 의미 과제·원문 부족·알려진 분석 오류는 종료 시 명시하고 원장 전체 완료로 표시하지 않는다.
- 승인된 병렬 방식: 한 워커는 한 원장 전체와 자기 결과 폴더만 담당한다. 추가 서브에이전트 금지. 공통 스킬·재개 노트·다른 워커 결과는 수정 금지(이 스킬 편집 워커는 지정 스킬만 예외). 종료 후 세션은 코디가 관리한다.

## 4. 먼저 읽을 핵심 파일

위 스킬과 사용자 합의만 사용한다. 원장이나 지난 조사 결과를 다시 조사하지 않는다. 기존 스킬을 좁게 수정하고 불필요한 규칙·게이트를 추가하지 않는다.

## 5. allowed_paths

- `orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md` 합의 내용 수정
- 새 `orchestration/work/phub-ledger-redesign/skill-update-report.md` 간단 변경·검증 요약

## 6. 구현 단계

1. skill-creator와 현재 스킬을 읽고 합의와 충돌하는 부분을 수정한다.
2. 출력 형식·종료 기준·병렬 소유권을 명시한다.
3. quick_validate.py로 검증하고 변경·검증·남은 제약을 보고한다.

## 7. 범위 제약

원본·기존 작업·재개 노트·조사 결과·전역 설정 수정 금지. 삭제·커밋·push·PR·추가 워커 실행 금지. 기존 문구와 새 기준의 충돌을 없애되 전체 조사 요구를 약화하지 않는다.

## 8. 검증

skill-creator/scripts/quick_validate.py 대상 스킬 폴더. 링크 유효성 및 앞뒤 종료 기준 일관성 확인. 검증은 실제 실행 결과만 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --from term_8c2999f2-0bca-4945-9d09-c5212852bdaa \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9817d7e4-b067-40b3-9235-c8dcddad8f26 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
