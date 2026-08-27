# @mediness-be — Workflow

## 태스크 수행 절차

1. **시작**: dispatch brief에 적힌 작업 워크트리와 base를 확인한다. canonical checkout이나 다른 브랜치로 이동하지 않는다.
2. **태스크 입력**: brief의 SSOT·계약·핵심 파일을 읽는다. **brief가 이번 태스크의 유일한 입력**이며 legacy 큐를 탐색하지 않는다.
3. **영향 분석**: 라우터/서비스/모델/마이그레이션/WebSocket/워커 영향을 확인하고 누락을 점검한다.
4. **기존 코드 탐색**: 관련 모듈의 컨벤션·네이밍·계층 패턴을 확인한다.
5. **테스트 먼저**: 적용 가능한 범위에서 RED 테스트를 작성하고 실패를 확인한다.
6. **구현**: brief의 allowed_paths와 계약을 지키며 최소 변경한다.
7. **검증**: brief §8의 명령을 우선한다. pytest는 반드시 `mediness_test` DB override로 실행한다.

   ```bash
   cd back && DATABASE_URL="postgresql+asyncpg://mediness:mediness@localhost:25434/mediness_test" uv run python -m pytest <경로> -q
   ```

   `DATABASE_URL`을 기본 `mediness` DB로 두고 pytest를 실행하지 않는다. 로그인·시드 데이터가 파괴될 수 있다.
8. **보고**: 변경 파일, 구현 요약, 검증 수치, 마이그레이션/API 영향, 미결 사항을 정리한다.
9. **완료**: 커밋·push·PR·별도 legacy 리포트·`.processed` 갱신을 하지 않는다. brief §9와 dispatch preamble의 `taskId`·`dispatchId`로 `worker_done`을 보낸 뒤 멈춘다.

## 모호할 때

- 정책·스펙·FE/DB 계약 판단이 필요하면 임의 결정하지 말고 dispatch preamble의 질문 채널로 코디네이터에게 확인한다.
