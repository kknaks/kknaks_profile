# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Type | IDs | Summary | Links |
|---|---|---|---|---|
| 2026-08-07 | scaffold | - | 제품 문서 스캐폴딩 생성 (README, log, 00-baseline / 10-decision / 20-spec / 30-work / 40-architecture index). `products/README.md` 제품 표에 `kknaks-agents` 행 추가 | [README](README.md) |
| 2026-08-07 | baseline-add | KAG-BL-001 | provider-neutral LLM runtime 라이브러리 baseline 등록. 특정 agent 제품 종속 문제, provider adapter 경계, 외부 tool 주입, server-owned loop/session/context/compaction/skill, Codex CLI subprocess 첫 실험, 운영 사례와 clean-room 관찰 범위, 미결 질문 11건 | [KAG-BL-001](00-baseline/baseline-001-provider-neutral-llm-runtime.md) |
| 2026-08-08 | decision-add | KAG-DEC-001 | Runtime 디렉터리 구조와 의존 경계 제안(작성 시점 `proposed`, 당시 내용은 전부 권고안). flat / 책임별 package / ports-adapters 3안 비교 후 **책임별 package 권고**(나머지 둘 비권고), 확정 시 채택. repo 상위 구조(`src`·`tests`·`examples`·`docs`), package 이름 `kknaks_agents` 제안, package 내부 8개 책임(core·process·providers·tools·sessions·context·skills·runtime), 4단 의존 계층과 금지 의존 표, provider 종속 코드의 `providers/` 격리 규칙, CLI/queue/web을 라이브러리 바깥 계층에 두자는 권고. 미결 8건 | [KAG-DEC-001](10-decision/decision-001-runtime-directory-boundaries.md) |
| 2026-08-08 | status-change | KAG-BL-001 | decision 검토 시작에 따라 baseline `raw` → `reviewing`. `links.decisions`에 KAG-DEC-001 추가. decision이 proposed인 동안 accepted로 올리지 않음 | [KAG-BL-001](00-baseline/baseline-001-provider-neutral-llm-runtime.md) |
| 2026-08-08 | mapping-change | KAG-BL-001, KAG-DEC-001 | baseline index(Status·Decision·Next), decision index(결정 로그·미결 사항·Next), 제품 README(현재 상태 표·package 이름 주석·최근 로그) 갱신 | [00-baseline](00-baseline/README.md) · [10-decision](10-decision/README.md) · [README](README.md) |
| 2026-08-08 | status-change | KAG-DEC-001 | 사용자 리뷰 확정 — decision `proposed` → `accepted`. Option B(책임별 package) 채택, A(flat)·C(ports/adapters) 기각. 본문의 권고/비권고 어투를 확정 어투로 정리하고 확정 문구(확정일·supersede 조건·여전히 미결인 Open Questions와 Out 범위)를 명시. import package 이름 `kknaks_agents` 확정, PyPI 배포명은 OQ-1로 계속 미결 | [KAG-DEC-001](10-decision/decision-001-runtime-directory-boundaries.md) |
| 2026-08-08 | status-change | KAG-BL-001 | decision 반영에 따라 baseline `reviewing` → `accepted`. 반영 범위는 디렉터리 구조와 의존 방향까지이고, 나머지 Possible Direction과 Open Questions는 이후 decision 대상으로 남는다 | [KAG-BL-001](00-baseline/baseline-001-provider-neutral-llm-runtime.md) |
| 2026-08-08 | mapping-change | KAG-BL-001, KAG-DEC-001 | accepted 상태 정합 — baseline index(Status accepted·Next), decision index(서문·Result 열·Next), 제품 README(현재 상태 표·package 이름 주석·최근 로그) 갱신. 다음 단계는 동작 구조 decision이며 문서는 아직 만들지 않았다 | [00-baseline](00-baseline/README.md) · [10-decision](10-decision/README.md) · [README](README.md) |
