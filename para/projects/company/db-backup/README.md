---
sot: external
status: active
---

# db-backup — 사내 서비스 DB 백업

사내 8개 서비스의 운영 DB를 맥스튜디오 백업 서버로 상시 수집하는 인프라 작업.
기획·스펙의 원천은 회사 쪽에 있고, 여기 남는 것은 내 경험이다.

## 무엇

시니어는 덤프를 제안했고, 전송 시간이 문제라는 판단에서 대안을 설계했다.
**베이스 백업 1회 + 바이너리 로그 상시 스트리밍**으로 방향을 잡았다.

- 수집: `pg_receivewal` · `mysqlbinlog` — 호스팅 형태와 무관, 엔진 단위 단일
- 배포: 맥스튜디오 k8s (Lima VM 3대 + kubeadm, arm64), ArgoCD GitOps
- 설계 문서: `reference/2026-09-19-data-backup/`

## log

- [[2026-09-21-data-backup]] — 방식 선정과 인프라 조사
