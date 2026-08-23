# Architecture Index

규칙: `rules/product-doc-pipeline.md`

> 여러 spec/work가 공유하는 장기 구조를 관리한다.
> 단일 work 안에서 끝나는 구현 메모는 `30-work/`에 둔다.

## 문서 맵

| Area | Purpose | Index |
|---|---|---|
| database | ERD, 테이블, 도메인 데이터 구조 | `database/README.md` |
| system | 시스템 아키텍처와 구성요소 | `system/README.md` |
| deploy | 배포 프로세스와 환경 | `deploy/README.md` |

## 원칙

- 코드와 schema 전문을 복사하지 않는다.
- 오래 유지되는 구조, 경계, invariant만 둔다.
- 여러 spec/work에서 반복 참조될 때만 작성한다.
