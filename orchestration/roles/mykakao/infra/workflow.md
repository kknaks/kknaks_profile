# @mykakao-infra — Workflow

1. **시작**: brief 의 워크트리·base 확인.
2. **입력**: brief 의 SSOT(spec·work 문서 — read-only 절대경로)와 현재 compose·스크립트를 읽는다.
3. **맞물림 확인**: `backend/summarize.py` 의 NAMESPACE/QUEUES 와 `.env.example` 을 대조한다.
   어긋나 있으면 **고치기 전에 보고**한다 — 어느 쪽이 정본인지는 코디네이터가 정한다.
4. **구현**: 최소 변경. 기존 macOS 경로를 지우지 않고 플랫폼별로 나눈다.
5. **검증**: 가능한 범위만. 못 한 것은 이유와 함께 명시.
6. **보고**: brief §9 의 2채널로.
7. **완료 후 멈춘다** — 커밋·push·PR 없음.

## 모호할 때
- 자격증명·네트워크·호스트 설치가 필요한 판단은 임의로 하지 말고 질문 채널로.
