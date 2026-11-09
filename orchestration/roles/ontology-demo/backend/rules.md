# @ontology-be — 규칙

## 이 데모의 원칙 (위반 = FAIL)
- **S-001 관계는 데이터에** — 온톨로지 관계 지식(어떤 KPI 가 어떤 KPI 의 원인인지)을
  프롬프트·코드 상수에 쓰지 않는다. 관계는 `ontology_edges` 조회로만 나온다.
- **S-002 Agent 는 판단만** — 집계는 골드 View, 관계는 edges 조회. 도구는 파라미터화된
  조회만 제공(자유 SQL 금지), DB 는 read-only 모드(`mode=ro`)로 연다.
- **ADR-04 LLM 경로** — Anthropic 등 LLM SDK 직접 import 금지. 실행은 open-kknaks
  (AgentClient + RedisBroker) 경유. `app/back/service/chat/` 이 모범 코드다.
- **PII** — `patientName`·`birthday`·`phone`(리뷰 작성자명 포함)은 화면·API·에이전트
  응답 어디에도 원값 노출 0건. 브론즈 접근은 마스킹 뷰 경유만. PII 를 로그·테스트
  픽스처·리포트에도 쓰지 않는다.
- **변환 규칙·게이트는 이식이지 재설계가 아니다** — 명세는 기록 04(실버)·05(골드)가
  SoT. 기존 `reference/ontology_demo/scripts/` 의 규칙·fail-fast·대사 로직을 그대로
  옮기고 입출력만 파일→DB 로 바꾼다. LLM 리뷰 재채점 금지(기존 `_scoring/` 산출물 사용).

## 코딩 컨벤션
- 기존 코드가 규약이다 — `app/back/` 의 인접 패턴(config·서비스 구조)을 먼저 읽는다
- SQLite 는 표준 라이브러리 `sqlite3` — ORM 불필요. 경로·설정은 `config.py`(env) 경유, 하드코딩 금지
- open-kknaks 는 설치본 그대로 — 라이브러리 수정 금지

## TDD
- 신규 빌드 단계·도구·API 는 `tests/` 에 테스트. 테스트 통과 없이 "완료" 표현 금지
- 전체 스위트 돌리지 않는다 — **네가 만들거나 고친 테스트 파일만** (사용자 방침)

## 스코프 규칙
- allowed_paths(`app/ontology-agent/`) 밖 수정 금지. `para/`·`orchestration/`·`reference/` 는 코디네이터 소유
- 원천 데이터(브리프의 절대경로)는 read-only — 복사·커밋·수정 금지. 산출 DB 는 자기 워크트리 로컬(env 지정 경로)
- 게이트 기준(행수 대사·대조값·PII 0건)을 임의로 완화하지 않는다 — 미달이면 그대로 보고

## 리포트 형식

```markdown
# {WP-ID} 결과 보고
## 상태: done / in-progress / blocked
## 수행 내용 — 파일 목록 · DB 스키마/도구/API 변경
## 게이트 결과 — 브리프 §8 게이트별 수치 (통과/미달)
## 테스트 결과 — pytest 수치 · 새 테스트 목록
## 이슈/블로커
```
