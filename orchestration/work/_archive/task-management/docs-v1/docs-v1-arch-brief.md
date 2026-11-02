
# [architect] 아키텍처 ① — 시스템 · DB · 백엔드

너는 **task-management `architect` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**⚠ 이 워크트리는 코디네이터와 공유한다.** §5 가 지정한 파일 외에는 **만들거나 고치지 마라.** git 은 읽기만.

## 1. SSOT — 먼저 읽을 것

경로는 전부 `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/` 기준.

**정책 (닫힌 계약 — 여기 없는 건 발명하지 마라)**
- `para/projects/summer-star/task-management/10-decision/decision-001-auth-settings.md` — 인증·설정. 세션·동적 유형·프로젝트·소프트 딜리트·**v2 스코프 규칙**
- `.../decision-002-my-tasks.md` — 내 업무. 유형 필수·프로젝트 N:1 무소속·**완료 게이트**·상태 전이
- `.../decision-003-meeting-notes.md` — 회의록. **사람·AI 2트랙**·배치 파이프라인·**실패 정책**·STT 전제
- `.../decision-004-library.md` — 문서함. PARA 고정·md 전용·연결
- `.../decision-005-calendar.md` — 캘린더. **`schedule` 테이블 분리**·겹침 차단
- `.../decision-006-messages.md` — 메시지함(v1 UI 만)
- 대응 기획서 `00-baseline/baseline-001~006-*.md` — 기능명세·인바운드/아웃바운드

**분석·조사**
- `orchestration/work/docs-v1/docs-v1-design-report.md` — 화면 P-01~72 · 사실 F-1~13 · 공용 컴포넌트 S-01~34
- `orchestration/work/docs-v1/soniox-study.md` — STT 프로토콜·토큰 모델·화자 분리·한도
- `orchestration/work/docs-v1/design-requests.md` — **§C 기술 선택 확정**(정적 빌드·shadcn·유동 반응형)과 정정 A-1~13

**양식**
- `templates/projects/40-architecture/README.md` · `system/README.md` · `database/README.md`

**참고할 기존 코드 규약** — 이 레포 `app/back/` 이 같은 계층 구조(router→service→repository, dto/schemas 분리)로 이미 돌고 있다. **읽어서 모범으로 삼되 그대로 복사하지 말고**, 이 제품에 맞게 쓴다.

## 2. 배경 / 무엇을 바꾸나

v1 6영역 정책(DEC-001~006)이 확정됐고 기술 선택도 닫혔다. 이제 **spec 을 쓰기 전에 구조와 규약을 세운다.** 이 문서들은 이후 모든 spec 과 코드 워커가 참조하고, **리뷰어가 판정 기준으로 삼는다** — 「이렇게 하는 게 좋다」가 아니라 **「이렇게 한다」**로 쓴다.

이번 발주는 **시스템 · DB · 백엔드** 셋이다. 프론트는 이 결과(특히 schema 계약)를 받아 다음 발주에서 쓴다.

## 3. 계약 — 사용자가 못박은 제약 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| 백엔드 | **FastAPI**, 패키지 관리 **uv** |
| 계층 | **router → service → repository** |
| 데이터 이동 | **`schema` = 프론트↔백 계약(pydantic)** / **`dto` = 백 내부 전달**. 둘을 섞지 않는다 |
| DB | **PostgreSQL**, **비동기** 드라이버·엔진 |
| AI 워커 | **open-kknaks** 의 **codex**. 호스트에 codex 바이너리가 있으므로 **바인드 마운트**해서 쓴다 |
| STT | Soniox. **프론트 → 백엔드 → Soniox 릴레이**(백엔드가 키 보유 + 원본 적재 겸함), v1 마이크만 |
| 프론트(참고) | Next.js **정적 빌드**(`output: 'export'`) + shadcn/ui → **백엔드는 서버 렌더를 전제하지 않는다.** 모든 데이터는 클라이언트에서 REST/WS 로 온다 |

**LLM 은 open-kknaks 를 통해서만 쓴다** — Anthropic/OpenAI SDK 를 직접 import 하지 않는다.

## 4. 먼저 읽을 핵심 파일

- `DEC-005 §3` — `schedule` 테이블 분리. 업무·회의의 시간을 여기가 단독 소유(둘 다 이관)
- `DEC-003 §4·§7` — 2트랙·배치 파이프라인·**실패 정책**(스키마 위반 폐기 · 없는 업무 화이트리스트 · 통합 실패 재시도 · **설계 외 예외는 fallback 없이 전파**)
- `DEC-002 §3·§4` — 완료 게이트, 상태 전이, 소프트 딜리트
- `DEC-001 §3·§4` — 세션(access 1h/refresh 7d), 동적 유형(종류 미팅|업무), 기본 3종 잠금
- `design-requests.md §A` — 디자인 정정 13건. **정책이 정본**이고 디자인 문서가 틀린 것이니 정책을 따른다

## 5. allowed_paths — 이 밖은 건드리지 마라

아래 **3개 디렉토리에만** 파일을 만든다 (경로는 `para/projects/summer-star/task-management/40-architecture/`):

1. `system/README.md` — 시스템 아키텍처
2. `database/README.md` (+ 필요하면 `database/domains/<domain>.md`) — DB
3. `backend/README.md` — 백엔드 계층·규약 (**새 디렉토리** — 템플릿에 없으니 `system/README.md` 양식을 참고해 만든다)

그 외 일체 수정 금지. **`40-architecture/README.md`(인덱스)·log·index 는 코디네이터가 쓴다 — 건드리지 마라.** 커밋·push 금지.

## 6. 구현 단계

1. 역할 문서 → §1 SSOT 순서대로 읽는다.
2. **system** — Mermaid flowchart 로 전체 구성(Tauri 셸 · Next 정적 번들 · FastAPI · Postgres · Soniox · open-kknaks codex). 컴포넌트 책임 표, 외부 연동 표, **핵심 흐름 3종**: ① 로그인·세션 갱신 ② 업무 생성·완료(게이트 포함) ③ **회의 STT·배치 요약·종료 통합**(웹소켓 2단 중계와 배치 세션 유지가 드러나게).
3. **database** — Mermaid erDiagram. 최소한 이걸 담아라:
   - 계정, 유형(종류 미팅|업무·기본 3종 시드·색), 프로젝트, **schedule**(source_type task|meeting · 시간 단독 소유), 업무(+완료 결과·할일·메모·참고/결과자료·로그·연관업무), 회의록(**사람 줄 / AI 줄 / 통합본 3집합** · 안건 · 트랜스크립트 · 첨부 · 녹음), 문서·폴더(PARA 고정 4종)·연결·태그
   - **소프트 딜리트 컬럼 규약**(전 영역 공통), 인덱스가 필요한 곳(캘린더 기간 조회·겹침 검사)
   - 마이그레이션 도구는 네가 제안하고 근거를 달아라
4. **backend** — 계층별 책임과 금지, `schema`/`dto` 경계와 명명, 디렉토리 구조, **비동기 엔진**(배치 요약 세션 유지 · STT 중계 · 작업 큐), **비동기 API 규약**(장시간 작업의 시작·상태 조회·완료 통지 — 회의록 「생성중」이 이걸 쓴다), 트랜잭션 경계, **에러 규약**(도메인 예외 → HTTP 매핑, 설계한 실패만 처리), 설정·환경변수, 테스트 규약.
5. 자기점검(§8) → 완료 보고(§9).

## 7. 범위 제약 — 하지 말 것

- **프론트 아키텍처는 이번 범위가 아니다** — 다음 발주. 다만 백엔드가 제공할 **schema 계약의 형태**는 여기서 정한다.
- 코드를 만들지 않는다(스캐폴딩·설정 파일·마이그레이션 파일 일체). **문서만.**
- 정책(DEC-001~006)을 다시 논의하거나 어기지 않는다. 충돌을 발견하면 고치지 말고 Open Questions.
- 디자인 원본·기획서·정책서를 수정하지 않는다.
- 선택지를 나열하고 끝내지 않는다 — **하나로 정하고 근거를 단다.** 정말 못 정하는 것만 Open Questions.
- 미설계 화면(`design-requests.md §B`)은 구조 결정을 막지 않는다 — 화면과 무관한 구조는 그냥 쓴다.

## 8. 검증

```
산출물은 브리프가 지정한 파일들뿐. DEC-001~006 을 어기는 구조를 제안하지 않았는지 자기점검(충돌 발견 시 고치지 말고 Open Questions). 사용자가 못박은 스택·계층 제약 준수. 결정마다 근거(DEC-00x §y · P/C/S/F/Q-xx) 병기, 선택지를 남기지 말고 단일 방식으로 서술
```

추가 자기점검 — 리포트에 결과를 적어라:

- §3 제약 7항목이 전부 반영됐나 (uv · 계층 · schema/dto · Postgres 비동기 · open-kknaks codex 바인드 마운트 · STT 릴레이 · 서버 렌더 미전제)
- DEC-003 §7 의 실패 정책이 **에러 규약에 그대로 반영**됐나 (특히 **설계 외 예외 fallback 금지**)
- `schedule` 이 업무·회의 시간을 **단독 소유**하는가 (업무·회의 테이블에 시간 컬럼이 없어야 한다)
- 회의록이 **사람 줄 / AI 줄 / 통합본** 세 집합으로 모델링됐나
- 소프트 딜리트가 **전 영역 공통 규약**으로 잡혔나 (v1 은 복원 UI 없음)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] architect 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] architect: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
