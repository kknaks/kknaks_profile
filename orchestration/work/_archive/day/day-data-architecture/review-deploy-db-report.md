# review-deploy-db — deployment.md 받은 서버 · DB 반영 검수 (읽기 전용)

**결론: PASS.** 커밋해도 된다. 아래 「남은 것」은 글귀 셋 — 막는 것 아님.

대상: mediness 미커밋 diff(`products/day/40-architecture/deployment.md` · `log.md` 1행) ↔ 지시 `planner-deploy-db-instructions.md` · 리포트 `planner-deploy-db-report.md` · 원천 system/README 「받은 서버 · DB」(54행) · `day.json` `infra`.

## 확인한 것

| 항목 | 결과 |
|---|---|
| 원천과 맞나 | ✓ VM 이름 · B2s · Ubuntu 24.04 · 64GB · `<VM 사용자>`(sudo) · 22/80/443 · 처음엔 docker 없음 · DB 호스트 · PG 16 · DB `day` · 스키마 주인 `day_dev_app` / `day_prod_app` · search_path · 서로 · `public` 쓰기 막힘 · `dayadmin` 초기 설정용 · 공개 꺼짐 · TLS verify-full · 삭제 방지 잠금 — README 54행 · day.json 과 전부 일치. 지어낸 값 없음 |
| IP · 비밀번호 없음 | ✓ grep(IP 정규식 · pgpass · password · 키 이름 `<SSH 키>` · 터널 15432 · 별칭 `day-vm`/`day-db`) — deployment.md · log.md 에 IP 0건 · 비밀번호 0건. 남은 「비밀번호」 단어는 "두지 않는다" · redis 설정 항목뿐. 리소스 그룹 · 지역 · 공인 IP 값은 "안 적음" 으로 명시 |
| 준비됨 / 아직 구분 | ✓ 준비됨 = VM · 네트워크 22/80/443 · 공인 IP · 관리형 PG(모두 원천에 있음). 아직 = Docker · 로그 회전 · DNS A 레코드 둘 · Key Vault · ACR · OIDC · VM identity(지시와 같음). **DNS 는 `dig` 로 실측 — `day-dev.medisolveai.com` · `day.medisolveai.com` 둘 다 응답 없음 → 「아직 없음」 맞음** |
| 미결 닫힘 = 사용자 승인 | ✓ 「스키마 생성 권한」 닫음 = 앱 계정이 주인 · migration 도 앱 계정 · 별도 migration 계정 없음 — README 54행 "**migration 도 앱 계정으로**(별도 migration 계정 없음 — 코디 추천 · 사용자 승인)" 과 동일. 승인 범위 밖으로 넓힌 것 없음 |
| 새 모순 | ✓ 없음. system.md 「DB · 환경 분리」(스키마별 계정 · dev 는 `day_prod` 권한 없음) · 결정 요약 · 그림 · env 표 서로 일치. `DATABASE_URL` 행의 호스트 · TLS · VM 경유 = 원천과 같음 |
| lint `--strict` | ✓ 0 error |
| log.md | ✓ `arch-change` 1행 · #909 · 요약이 diff 와 맞음 |

## 남은 것 (글귀 — 선택)

1. **머리말 3번째 줄 낡음** — "결정에 없는 값(**VM 이름** · … · IP · …)은 짓지 않는다 — 아래 「사용자 준비 · **값 미정**」". 이제 VM 이름은 적혀 있고(받은 값이라 '짓지 않는다' 와 모순은 아니나 읽는 사람이 헷갈림) 절 제목에서 「(값 미정)」 을 뗐으니 참조도 「사용자가 Azure 에서 준비할 것」 으로. 한 줄 손질.
2. **`env.py` 서술 정밀도** — 미결 닫힘 글 "`env.py` 의 `CREATE SCHEMA IF NOT EXISTS` 는 아무것도 하지 않는다". 실제 DAY `backend/migrations/env.py` 는 온라인 모드에서 `pg_namespace` 조회 후 없을 때만 `CREATE SCHEMA`(`IF NOT EXISTS` 는 offline `--sql` 출력에만). 결론(스키마가 이미 있어 아무것도 안 함)은 맞다 — "스키마가 없을 때만 만들므로" 정도로 바꾸면 정확.
3. **`40-architecture/README.md` 21행** "deployment.md … **아직 만들지 않음**" — diff 밖. 배포 자체는 아직이라 틀린 말은 아니나 서버 · DB 는 받았으니 다음 손질 때 "배포 아직 · 서버 · DB 는 받음(2026-11-09)" 으로 맞추면 좋다.

## 같이 본 사실(기록만)

- 네트워크 행의 "8000 · Redis 는 열려 있지 않음" · "나가는 IP 는 미확인" 은 원천이 22/80/443 만 말한 데서 나온 추론 — 타당.
- 22 포트를 닫을지는 사용자 판단으로 남겨둠 — 결정 발명 아님.
