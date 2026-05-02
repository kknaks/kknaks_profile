---
id: adr-03
type: adr
title: 스케쥴러는 포트폴리오 시스템 인프라 — 백엔드 권한 모델 명시
status: accepted
created: 2026-05-01
updated: 2026-05-01
sources:
  - "[[planning-01-portfolio-overview]]"
tags: [adr, architecture, scheduler, persona]
---

# 스케쥴러는 포트폴리오 시스템 인프라 — 백엔드 권한 모델 명시

## Summary

AI 잡(스케쥴러)은 **포트폴리오 시스템의 인프라**로 귀속. 코드 위치는 `back/`, 실행 환경은 백엔드 프로세스 안 APScheduler. 백엔드의 페르소나 폴더 접근 권한은 **md 파일 read-only + `activity.yaml` (잡 산출물)만 write**. 사람의 모든 콘텐츠 변경과 백엔드의 모든 산출물 갱신은 git commit으로 audit.

---

## 1. Context

planning-01 §3.4의 architectural seam:
> 스케쥴러가 어느 시스템에 속하는지(포트폴리오 인프라 vs 페르소나 gen 레이어)는 ADR-03에서 정의.

이 결정이 미정이면 spec-01(페르소나 형식)과 spec-03(잔디 잡 명세)이 같은 부분(activity.yaml 쓰는 주체가 누구냐, 코드 어디 살나)을 다툼. 명확화 필요.

추가 컨텍스트 — 사용자가 명확히 한 멘탈 모델:
> "백엔드의 데이터베이스가 persona md들"  
> "md 편집은 내가 직접 보고 작성하고 클로드랑 최종본을 만들어서 올릴거야"  
> "백엔드쪽에서는 읽어오는거 말고 md 수정은 commit 밖에 없을듯"

→ 페르소나 = 사람 도메인. 백엔드는 read 위주. 자동 산출물(activity.yaml)은 백엔드가 갱신.

---

## 2. Decision

### 2.1 시스템 귀속

**스케쥴러 = 포트폴리오 시스템의 인프라**.

- 코드 위치: `back/scheduler.py` (또는 `back/jobs/`)
- 실행 환경: 백엔드 FastAPI 프로세스 안 APScheduler (별도 워커 X)
- 페르소나는 콘텐츠 저장소(데이터베이스 역할), 자가 갱신 능력 X

### 2.2 백엔드 권한 모델

백엔드 프로세스의 `persona/` 폴더 접근 권한:

| 파일 | 권한 | 변경 주체 |
|---|---|---|
| `persona/profile.md` | **read-only** | 사람 (사용자 + Claude 협업) |
| `persona/career/*.md` | **read-only** | 사람 |
| `persona/projects/*.md` | **read-only** | 사람 |
| `persona/notes/*.md` | **read-only** | 사람 |
| `persona/contents/*.md` | **read-only** | 사람 |
| `persona/daily/*.md` | **read-only** | 사람 (잔디 잡의 입력 소스) |
| `persona/_meta.yaml` | **read-only** | 사람 |
| `persona/activity.yaml` | **write 허용** | 백엔드 스케쥴러 (잡 산출물) |
| `persona/_map.md` | **write 허용** | 백엔드 부팅 시 빌드 (멱등) — spec-04. git pre-commit hook도 같은 빌드 실행 (옵시디언 갱신용) |

→ 백엔드가 직접 쓰는 파일은 **`activity.yaml` + `_map.md` 두 개** (둘 다 자동 산출물, 사람이 안 만짐).

### 2.3 모든 쓰기는 git commit

| 변경 주체 | 워크플로우 |
|---|---|
| **사람** (md 편집) | vscode/Claude로 편집 → `git commit & push` 수동 → webhook → 백엔드 reload |
| **백엔드 스케쥴러** (activity.yaml 갱신) | yaml 갱신 → `git add activity.yaml && git commit && git push` 자동 → reload endpoint 셀프 호출 |

→ git history가 곧 변경 audit log. 별도 audit 시스템 불요.

---

## 3. Alternatives Considered

### 3.1 B안 — 페르소나 시스템의 gen 레이어
- **장점**: 페르소나가 입력+가공 둘 다 책임. "AI-readable Self-Doc" 사상에 멋지게 부합. 향후 다른 잡(이력서 자동 생성 등) 추가 시 같은 위치
- **단점**: 코드가 `back/`과 `persona/_jobs/` 두 군데. 1인 운영에서 작위적 분리. 실행 환경은 어차피 백엔드 프로세스라 sub-system 경계가 코드 디렉토리에만 존재
- **기각 이유**: 사용자 멘탈 모델("백엔드의 DB가 persona")과 충돌. 분리의 가치 < 분리 비용

### 3.2 별도 워커 프로세스
- **장점**: API 서빙과 잡 실행 분리 → 한쪽 문제가 다른 쪽 영향 X
- **단점**: 호스팅 부담 추가 (uvicorn + 워커 daemon). 1년차 셀프호스팅 컨텍스트 오버
- **기각 이유**: 잡 실행 빈도 매일 1회 → API 서빙에 영향 무시 가능

---

## 4. Consequences

### 4.1 즉시 효과
- 코드 위치 명확: `back/`에 모든 백엔드 코드
- 페르소나 폴더 책임 단순: "사람이 쓰는 SoT" + "백엔드가 박는 캐시 한 개"
- spec-03(잔디 잡 명세)이 자연스럽게 "백엔드 안 cron"으로 결정됨

### 4.2 사용자 워크플로우 (사람의 페르소나 편집)

```
1. vscode 또는 Claude와 대화로 persona/**/*.md 편집
2. git diff 확인
3. git commit + git push (사람 손)
4. GitHub webhook → 홈서버 reload endpoint 호출
5. 백엔드: git pull + load_all() → 메모리 dict 갱신
6. 다음 사이트 요청부터 새 콘텐츠 노출
```

### 4.3 스케쥴러 워크플로우 (백엔드 자동)

```
1. APScheduler cron trigger (매일 23:55 KST)
2. GitHub API + 로컬 git log → 오늘 활동 수집
3. Anthropic API → ko/en 한 줄 요약 + kind 결정
4. activity.yaml 갱신 (메모리 + 디스크)
5. push loop (최대 3회 retry):
     git fetch origin
     git rebase origin/main           # activity.yaml은 백엔드만 쓰므로 rebase 충돌 불가
     git add persona/activity.yaml
     git commit -m "chore: activity YYYY-MM-DD"
     git push                         # 실패 시 1번부터 retry
6. load_all() 셀프 호출 → 메모리 dict 갱신
```

retry 3회 모두 실패 시: 로그 + 다음 날 같은 entry로 다시 시도 (그날 활동 데이터는 commit-pending 상태로 남되 잃지 않음).

### 4.4 위험 + 완화

| 위험 | 완화 |
|---|---|
| 백엔드 push가 history divergence로 reject (사람 push가 사이에 들어감) | push 전 `git fetch + rebase origin/main` (§4.3 step 5). activity.yaml은 백엔드만 쓰므로 rebase 충돌 불가. push 실패 시 retry loop 3회 |
| webhook 누락 시 사이트 stale | 5분 주기로 git pull + diff check fallback (선택, plan-01에서 결정) |
| activity.yaml git commit 메시지 노이즈 | 매일 1회 `chore: activity YYYY-MM-DD` 한 줄 — git log 노이즈 허용 범위 |
| 백엔드가 실수로 md 파일 write | 코드 레벨 가드 (write 함수에 path whitelist `persona/activity.yaml` 만 허용) + spec-03 명세에서 강제 |
| 백엔드 git auth 실패 | systemd EnvironmentFile에 PAT 또는 deploy SSH key 박음. 키 권한 = repo write only. plan-01에서 셋업 단계 명시 |
| `uvicorn --workers N`으로 스케쥴러 N번 발동 | 홈서버는 single worker 운영 (또는 APScheduler distributed lock). spec-03에서 강제 |

### 4.5 향후 확장 여지
- 다른 자동 산출물 (예: weekly digest, monthly summary) 추가 시 같은 패턴 — `persona/digests/*.yaml` 등 yaml 화이트리스트 확대
- 페르소나의 비-포트폴리오 활용 (이력서 자동 생성 등)은 **별도 프로세스**가 같은 `persona/` 폴더 read해서 처리. 본 ADR의 권한 모델은 무영향
