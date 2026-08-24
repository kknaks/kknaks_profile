# Architecture Index

규칙: `para/projects/project.md`

> 여러 spec/work가 공유하는 장기 구조를 관리한다.
> 단일 work 안에서 끝나는 구현 메모는 `30-work/`에 둔다.

**아직 architecture 문서가 없다.** 이 라이브러리는 package 경계(공통 계약 / turn 반복 / provider adapter / tool 실행 / session / context / skill / subprocess)가 여러 spec과 work에 걸쳐 재사용될 가능성이 커서 index만 먼저 열어 두었다. 실제 문서는 spec이 나오고 공유 구조가 확인된 뒤에 작성한다.

## 문서 맵

| Area | Purpose | Index |
|---|---|---|
| system | package 경계, 컴포넌트, turn 흐름 | (미작성) |
| database | 영속 session store를 도입하면 작성 | (미작성) |
| deploy | 배포 대상이 생기면 작성 | (미작성) |

## 원칙

- 코드와 schema 전문을 복사하지 않는다.
- 오래 유지되는 구조, 경계, invariant만 둔다.
- 여러 spec/work에서 반복 참조될 때만 작성한다.
