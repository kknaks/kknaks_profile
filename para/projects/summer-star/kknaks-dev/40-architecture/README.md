# Architecture Index

규칙: `para/projects/project.md`

> 여러 spec/work가 공유하는 장기 구조를 관리한다.
> 단일 work 안에서 끝나는 구현 메모는 `30-work/`에 둔다.

## 문서 맵

| Area | Purpose | Index |
|---|---|---|
| database | SoT 경계 · ERD · 테이블/도메인 인덱스 | `database/README.md` |
| system | 구성요소 · **쓰기 소유권 경계** · 외부 연동 · 주요 흐름 | `system/README.md` |
| deploy | 배포 환경 · 서비스 목록 · 릴리즈 흐름 | `deploy/README.md` |

## 핵심 경계 두 개

이 제품에서 반복 참조되는 구조는 결국 두 경계다.

- **저장 경계** — 발행된 md는 파일 SoT, 운영 상태와 승인 전 초안은 PostgreSQL. 미커밋 md를 작업트리에 둘 수 없다는 제약(`reset --hard`)이 이 경계를 강제한다. → `database/README.md`
- **쓰기 소유권 경계** — AI는 계획만 내고, 파일·git은 Apply Executor가 단독으로 건드린다. → `system/README.md`

## 원칙

- 코드와 schema 전문을 복사하지 않는다.
- 오래 유지되는 구조, 경계, invariant만 둔다.
- 여러 spec/work에서 반복 참조될 때만 작성한다.
