# Architecture

규칙: `rules/product-doc-pipeline.md`

## 목적

`open-kknaks`의 장기 유지 가치가 있는 시스템 구조와 운영 절차를 관리한다.

## Architecture Map

| Area | Index | Notes |
|---|---|---|
| Deploy | `deploy/README.md` | PyPI package 배포 절차 |

## 경계

- 사용자-facing 기능 계약은 `20-spec/`에 둔다.
- 구현 작업 순서와 PR 분리는 `30-work/`가 생길 때 둔다.
- 배포 절차처럼 반복 운영에 필요한 안정적인 절차만 이 계층에 둔다.
