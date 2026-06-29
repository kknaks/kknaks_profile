# Product Log

| Date | Entry | Links |
|---|---|---|
| 2026-06-29 | WORK-001 그래프 빌더+검증기 report-only 완료 (255 passed, abcfbc4). probe nodes 309/edges 301, 검증 위반(ERROR 165/WARN 196)=WORK-002 worklist. | [[work-001-graph-builder-validator\|KDEV-WORK-001]] · [[spec-002-graph-schema\|KDEV-SPEC-002]] · [[spec-004-graph-validation\|KDEV-SPEC-004]] |
| 2026-06-29 | WORK-002 검증기 정교화 완료 (260 passed, 0014790). probe L1 12→0·L2 154→34·L5 196→0, false-positive 0. 잔존 L2=34=아카이브 사본 id 충돌(version-cutoff 가 id 에 버전 prefix 미부여) → SPEC-004 §7 OPEN. 여전히 report-only. | [[work-002-validator-refinement\|KDEV-WORK-002]] · [[spec-002-graph-schema\|KDEV-SPEC-002]] · [[spec-004-graph-validation\|KDEV-SPEC-004]] |
