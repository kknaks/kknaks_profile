# [researcher] batch-01 / products.json 전체 1차 조사

너는 Opus 조사 워커다. 코디와 동일 트리를 공유하며, 다른 원장 워커 4명과 병렬 실행된다. 네 담당 원장과 결과 폴더만 소유한다. 추가 워커·서브에이전트를 띄우지 않는다. 최신 라이브 preamble의 task/dispatch와 보고 명령이 §9보다 우선한다. 이 파일만으로 이번 발주 범위를 판단한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/AGENTS.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md` — 수정 완료된 1차 수집 절차·출력·종료 기준
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-ledger-redesign/_RESUME.md` — 읽기 전용. 이번 batch 승인과 현재 상태
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/bronze/phub-ledger/README.md` — 원장 작성 규칙. 원본 수정 허가가 아니며 기호만으로 의미 관계를 확정하지 않는다.

역할 자료가 필요하면 `orchestration/roles/procedure-hub/researcher/`를 읽되, 단일 리포트 경로 등 기본 역할과 이번 브리프가 다르면 이번 사용자 승인 범위를 우선한다.

## 2. 배경 / 무엇을 바꾸나

procedure-profiles.json 샘플 1차 수집은 종료했고 사용자가 다음 5개를 Opus 워커 5명에게 병렬 조사하도록 승인했다. 이번 대상은 `products.json` **전체**다. 기존 조사 주장·이전 ERD를 근거로 사용하지 않는다. 구조·전체 값·원문·문맥·형태소·복합 표현을 직접 수집하며 의미 모델 설계·정규화·관계 확정은 하지 않는다.

## 3. 계약

읽기용 review.md에 컬럼 구성 표(원본 컬럼명/경로 패턴·자료형·중첩 구조·원문 예시와 위치)를 제공하고, 모든 항목의 실제 내부 값을 원본 컬럼명 그대로 보여준다. 원문 값과 잠정 관찰은 별도 칸/절로 분리한다. 필드명을 줄이지 않는다. 필드·빈도·토큰 목록만으로 전수 읽기를 대신하지 않는다.

기계 기록은 모든 구조·키·말단 값·빈 값·배열 순서·JSON Pointer·정확한 구간·문맥을 포함한다. 원문 키 중복·이스케이프가 있을 수 있으므로 실제 파일 조건에 맞게 처리한다. 코드포인트/바이트, 디코딩 문자열/JSON 리터럴 구간을 구분한다.

형태소 분석 환경은 `uv run --python 3.12 --with kiwipiepy==0.24.1`을 쓸 수 있다. `cong` 모델을 사용하고 스레드는 1개로 제한한다. 버전·사전·옵션을 실제로 기록한다. 도구가 제공하지 않는 기본형을 임의로 생성하지 않는다. 필드명·언어 텍스트·ID/코드값의 적용/제외는 각각 사유와 위치를 남긴다. 사용자 사전은 필수가 아니며 이번에는 기본 결과를 보존하고 알려진 오분절을 출현별로 기록하면 된다.

전체 원문을 문맥과 함께 직접 읽는다. 형태소·정규식·키워드는 수집 보조다. 전문어 오분절, 수식·부정·가능성·조건·범위·시간이 사라지거나 오탐이 되는 곳은 원문 구간과 영향으로 표시한다. 원시 분석은 도메인 정답이 아니다.

## 4. 먼저 읽을 핵심 파일

유일한 조사 데이터: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/bronze/phub-ledger/products.json`. 다른 원장을 열어 조사하거나 통합 의미 체계를 가정하지 않는다. 원문이 다른 항목을 참조하면 참조 표현과 원문 위치를 보존하고 후속 연결 과제로 둔다.

## 5. allowed_paths

**쓰기 허용은 `orchestration/work/phub-ledger-redesign/first-pass/products/` 아래뿐이다.** 없는 결과 폴더만 생성한다. 공통 스킬·_RESUME·batch 계획·원본·다른 워커 폴더는 수정·삭제하지 않는다. 작업 중 자신이 만든 신규 결과의 필요한 보정은 허용하나 기존 타 작업을 덮어쓰지 않는다.

산출 파일: review.md, source-map.json, morphology.json, expressions.json, issues.md, validation.md. 재현 build.py·독립 verify.py와 꼭 필요한 수동 검토 기록도 같은 폴더 안에 둔다. 임시 산출물·캐시도 다른 워커와 경로를 공유하지 않는다. 공유 uv 패키지 캐시를 이용하는 것은 허용하며 전역 설정은 바꾸지 않는다.

## 6. 수행 단계

1. 원본 해시·크기와 전체 구조·값 대응 범위를 고정한다.
2. 전체 원문을 위에서 아래로 구획별 직접 읽고, 구조·값·문맥을 수집한다.
3. 전체 텍스트 형태소 분석과 문맥 포함 복합 표현 수집을 수행한다. 자동 처리와 직접 읽기 범위를 정확히 구분한다.
4. 원문 누락·중복·포인터·문자구간·해시·적용/제외 대응을 검증한다. 별도 읽기 검토로 수식·조건·부정·오분절 영향을 확인한다.
5. 에이전트가 해결할 실제 추출 오류는 고친다. 원문 부족, 잠정 해석, 후속 의미 조사, 실제 사용자 결정 필요를 구분한다. 도구 선택 같은 에이전트 판단을 사용자 결정으로 넘기지 않는다.
6. 1차 수집 기준을 충족하면 종료하고 코디에 보고한다. 최종 의미 해석이나 모든 형태소 정답을 얻기 위해 반복하지 않는다. 알려진 오류의 위치·영향·한계를 남기고 후속 과제로 구분한다. 새로운 누락·오류가 있으면 그 부분만 수정·재검증한다.

## 7. 하지 말 것

원본·기존 작업 수정/삭제·복구·다른 원장 조사·공통 문서 갱신·추가 에이전트·커밋·push·PR·Git clean/reset/checkout 금지. 임상·법적 사실을 승인하거나 외부 자료로 보충하지 않는다. 원문에 없는 단위·백분율·뜻·적용 부위를 채우지 않는다. 선택을 받지 않은 해석을 확정 데이터로 쓰지 않는다. 원문 보존만으로 미결을 닫지 않는다.

## 8. 검증·완료 보고

원본 해시 시작/끝 불변, 원문 구조·값 양방향 대응, Pointer·구간 원문 재현, 중복/누락 검사, 분석 적용·제외 대응을 실제 검증하고 명령·결과를 validation.md에 남긴다. verify.py는 원본과 결과를 읽고 실패 시 nonzero로 종료하며 다른 파일을 수정하지 않게 만든다. 코디가 레포 루트에서 `python3 orchestration/work/phub-ledger-redesign/first-pass/products/verify.py`로 재실행할 수 있어야 한다.

상태는 1차 수집 범위와 원장 전체를 분리한다. 1차 종료 여부, 남은 원문 부족·잠정·후속·사용자 결정 필요의 실제 검토 상태를 보고한다. 미결이 남은 원장은 전체 완료라고 하지 않는다. 결과 전달은 3문장 요약(범위·검증·한계/미결)과 실제 review.md 경로만, 긴 원문은 메인에 보내지 않는다. worker_done 이후 추가 작업 없이 idle한다.

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
