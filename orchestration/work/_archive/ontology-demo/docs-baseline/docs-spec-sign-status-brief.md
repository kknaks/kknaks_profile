
# [docs] 소수정 3건 — SPEC-002 예시 grain·SPEC-003 sign 표기·work-002 한 단어

너는 **ontology-demo `docs` 워커**다. 정확히 3건 (backend 실측·코디 확정):

1. **SPEC-002** (v0.0.3→0.0.4): §4 query_kpi 응답 예시의 grain 을 weekly→daily 로 바꿔 status 가 실리는 예시가 정본과 맞게. 서술 추가 — 「status·status_thresholds 는 grain=daily 에만 실린다. 주별·월별 정본에는 상태 컬럼이 없고 도구는 상태를 만들지 않는다(S-002) — weekly/monthly 응답은 status:{} · status_thresholds:[] 로 빈다.」
2. **SPEC-003** (v0.0.5→0.0.6): 엣지 `sign` 값이 정본 원형 유니코드 마이너스 '−'(U+2212)임을 명시(허용값 나열: '+' · '−'(U+2212) · '0' · 'exo' · '?' 등 정본 그대로 — ontology/edges.csv 대조는 코디 확인값 사용, 원천 열지 마라). ASCII '-' 로 적힌 예시 표기를 정정하고 「FE 는 문자 비교 시 U+2212 기준」 경고 한 줄.
3. **30-work/work-002-tools-and-api.md**: P5 cards 필드 나열에 `has_prev_period` 한 단어 추가 (지난 태스크 드리프트 보고 건 — 이번엔 30-work 수정 허용, 이 한 단어만).

version·updated_at·README Spec List 동기·log 1줄. 그 밖 수정 금지. 커밋·push 금지.
완료 보고 동일 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "docs 완료: sign·status·드리프트".
