# [backend] 고도화 3차 — 사용자 요청 6건의 서버 쪽 현재 코드 전수조사

너는 **strong-hajin `backend` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3/AGENTS.md`
- 직전 판 기록: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-007-task-detail.md`(업무 상세를 세운 판) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md`
- 직전 조사(출발점 — 줄 번호는 옛 값): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/_archive/strong-hajin/strong-hajin-polish2/be-survey-report.md` · `fe-survey-report.md` (같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3`
base: `origin/main` (`d1b5137` — 운영 반영 코드)

⚠ **같은 워크트리에 다른 워커(backend/frontend)가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트 파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.** 네 몫이 아닌 쪽도 답에 필요하면 읽어라.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 사용자가 이 리포트를 보고 계약을 정한다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 운영(`https://ax.medisolveai.xyz`)을 쓰며 요청 여섯을 냈고, 업무 상세 모달은 **전면 개편**하기로 정했다(아래 R4 「정해진 방향」).
이 리포트가 계약(SPEC·WP)의 근거다. 각 요청이 닿는 코드가 **어디에 몇 군데** 있는지, 지금 **어떻게** 동작하는지를 확정한다.
빠진 자리가 곧 다음 판의 FAIL 이다 — **시작점에서 멈추지 말고, 같은 심볼·패턴·API 를 쓰는 곳을 grep 으로 전부 세어 숫자로 적어라.**

## 요청 6건 (사용자 원문 요지 — 참고용 맥락)

- **R1 로그인** — 브랜드 h1 「기록 → 판단 → 수행 → 보고를 한 흐름으로」→「메디솔브 AX 프로젝트」, 그 아래 설명 문장 삭제
- **R2 회의 상세 「내보내기」** — 옆 「공유」「다음 회의 예약」과 단추 크기가 다르다(내보내기만 `<a>` — `href="/api/meetings/{id}/export?format=html"`). **Tauri 앱에서 다운로드가 안 되는 것 같다**
- **R3 회의 제목** — 「제목 없는 회의」 옆에 「제목 후보 …」가 따로 뜬다. 제목을 클릭해 인라인으로 고치고(blur/Enter 저장), 제목 없을 때 후보를 [적용]으로 반영할 예정
- **R4 업무 상세 모달 개편 — 정해진 방향**: 헤더 = 제목(클릭 인라인 수정) + 닫기(×)만. 「메타 정보」 구역 신설(진행 상태 셀렉트 · 담당 셀렉트 · 시작 예정일/마감일 날짜 선택 즉시 저장 · 실제 시작일/버전 읽기 전용 · 출처 「AX 제안에서 생성됨 · [링크]」). 업무 내용 인라인 수정(blur 저장). **삭제**: 푸터 전체(업무 취소·시작·막힘·완료 처리), 「편집」 단추와 편집 모드, 「진행과 판단」 구역, 헤더의 「AX」 단추·상태 칩·「업무 상세」 머리글. 업무 취소는 진행 상태 셀렉트 맨 아래로. 「자료」「이력」 구역은 그대로
- **R5 선행업무 안내** — 본문 위 빨간 「시작할 수 없습니다 — ○○이 끝나지 않았습니다」 박스와 푸터 문구 「끝나지 않은 선행업무가 있습니다: ○○」 삭제. 막는 규칙은 유지하고, 상태를 바꾸려 할 때 토스트로 알릴 예정
- **R6 업무 상세 헤더 아래 여백** — 칩 줄과 「담당 …」 줄 사이(헤더 아래 패딩 + 본문 위 패딩)가 너무 크다

## 2. 요청별 물음 (네 몫 = 서버 계약·규칙)

### R2 회의 내보내기 API
1. `/api/meetings/{id}/export` 라우터·서비스 위치(파일:줄), 지원 `format` 값 전부, 응답 `Content-Type`·`Content-Disposition`(attachment 여부·파일명 규칙·한글 파일명 인코딩)
2. 인증 방식 — 쿠키 세션인가, `Authorization` 헤더인가. **`<a href>` 로 바로 열 때 인증이 실리는 구조인가**. Tauri 데스크톱(flavor `strong-hajin` origin null / `medi-ax` origin `https://ax.medisolveai.xyz`)에서 API 를 부를 때 인증이 어떻게 실리는지 서버가 기대하는 바(CORS·쿠키 SameSite 설정 포함, 파일:줄)
3. 서버에서 파일을 내려주는 다른 엔드포인트 **전부**(자료 파일 다운로드 등) — 같은 인증·헤더 방식인가 (표)

### R3 회의 제목
1. 회의 제목 필드와 「제목 후보」 필드가 어디서 만들어지고 저장되나(모델·컬럼·생성 시점 — 전사/요약 워커 중 누가 채우나, 파일:줄)
2. 회의 제목을 **바꾸는 API 가 지금 있나**. 있으면 경로·페이로드·권한(누가 바꿀 수 있나)·이력/버전 기록 여부. 없으면 회의 수정 계열 API 가 무엇이 있나(전부)
3. 제목이 비었을 때 「제목 없는 회의」는 서버가 주는 값인가 화면이 채우는 값인가

### R4 업무 수정 계약 — 개편의 근거
1. 업무를 **바꾸는 API 전부**(필드 수정·담당 변경·날짜·상태 전이·취소·체크리스트·연결) — 경로·메서드·페이로드·응답·권한·파일:줄을 표로
2. 지금 상세 「편집」 저장이 부르는 API 가 **실제로 받아서 바꾸는 필드** 목록(제목·내용·시작 예정일·마감일 외에 더 있나) — 화이트리스트/스키마 파일:줄
3. **버전(`v9` 같은 값)** — 무엇이 버전을 올리나(어떤 API·어떤 필드 변경), 낙관적 잠금(expected_version 등)에 쓰이나, 충돌 시 응답 코드·본문. **필드 하나씩 연달아 저장하면**(인라인 자동 저장) 무엇이 일어나나 — 버전이 매번 오르나, 연속 요청이 충돌하나
4. **담당자 변경** — 필드 수정과 별도 API·이벤트인가, 이력·알림·수신함·권한(누가 바꿀 수 있나)이 붙나. 담당 후보 목록은 어느 API 로 얻나
5. **상태 전이표** — 상태 값 전부 × 가능한 전이(시작·막힘·재개·완료·취소·되돌리기 등) × 각 전이의 API·필수 입력(사유 등)·부수효과(실제 시작일·완료일 채움, 마감일 채움 등). 「막힘」은 상태인가 별도 플래그인가
6. 날짜 검증 — 시작 예정일 > 마감일을 서버가 막나, 실제 시작일은 사람이 바꿀 수 있나
7. **출처** — 「AX 제안에서 생성됨」 의 데이터(필드·관계)와 그 옆 링크가 가리키는 대상(원 AX 초안? 원 대화? 원 업무?). 출처 종류 전부(AX 제안·회의·하위 업무 등)
8. 업무 상세 응답(task get) 스키마 — 위 개편 화면이 쓸 값(진행 상태·담당·날짜 넷·버전·출처·선행업무 막힘 정보)이 이미 다 오나, 빠진 것은 무엇인가

### R5 선행업무 막힘 규칙
1. 「선행업무가 안 끝나면 시작 못 한다」를 **서버가 판정하나**(파일:줄) — 어느 전이를 막나(시작만? 완료도?), 거부 응답 코드·본문(문장이 서버에서 오나)
2. 상세 응답에 막힘 정보(미완 선행업무 목록 등)가 어떤 필드로 오나
3. 같은 규칙을 판정·노출하는 자리 전부(수신함·목록·AX 도구 등)

### 공통
- 위 각 API 의 계약 테스트·acceptance journey 가 어디 있나(파일) — 다음 판이 고칠 테스트 범위를 세기 위해

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/be-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트·CSS 를 고치지 마라. 테스트·빌드를 돌리지 마라
- **서버·프론트·Tauri 를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329)
- 브라우저를 열지 마라. **운영 서버에 접속하지 마라**
- 「이렇게 바꾸자」를 쓰지 마라
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 고도화 3차 조사 (backend)

## 0. 한 줄 요약 — 요청별 한 줄 (원인이 보이면 원인 한 줄)
## 1~. 요청별 절 — §2 물음 번호대로 답
## N. grep 개수표 — 요청별로 센 심볼과 개수
## N+1. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 조사 한계에)
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3 status --short` 가 비어 있다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 3차 조사" \
  --body "리포트 경로 / 요청별 한 줄 요약 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 \
  --text "[worker_done] backend 3차 조사 완료 — <한 줄 요약>. 리포트 be-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[질문] backend: <질문>" --enter`
