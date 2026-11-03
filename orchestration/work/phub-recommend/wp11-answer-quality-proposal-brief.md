# WP-11 근거를 보존한 자연어 답·최종 전달 계측 제안

- 읽기 전용으로 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`, SPEC-006 0.3.13/WORK-012, `wp10-final-q002-live-report.md`/실제 답과 `para/resources/note/ai/llms.txt`를 읽는다. 현재 Q002 judge4 PASS지만 필러 21줄 원문·내부 ID·숫자/중복, 여섯 갈래 보류, 원문 전체 승인 정책이라 표현 품질 미완료다.
- TypeSafe 공식 llms.txt 인덱스→citation_check/primitives/fan-out/SDK를 확인하고 **작은 하나의 구현 계획**을 제안한다: Claude의 환자용 자연어 claim+source IDs 구조화 출력, 앱의 ID/build/source/scope 대조, Jev가 여러 claim의 지원/반대/미지원 판단을 한 요청에 독립 평가하는 의미 검증, 필수 안전·조건·부재 hard gate, 실패 시 안전한 축약/범위 보류. 기존 exact-source fallback은 최후 경로이며 자연스러운 의역을 허용할 수 있는지와 한계를 명확히 한다. 임상 의미를 토큰 겹침/정규식만으로 승인하지 않는다.
- 내부 fact ID는 trace에 보존하고 사용자 답에서는 짧은 번호/출처로 표시하는 전달 계층, 안전 고지 중복을 없애도 필수 항목 커버가 유지되는 대응표, 최종 검증 후 on_text 시각을 정확히 저장하는 계측을 포함한다. 여섯 갈래의 Gold 공개 안전 공백 해결과 표현 작업은 별개로 기록하며 필러 부분 답 통과를 전체 추천 완료로 부풀리지 않는다.
- 기능/파일/API 스키마·상태 전이·실패 처리·수용 fixture/실물 관문·비용/지연 위험을 구체적으로 `orchestration/work/phub-recommend/wp11-answer-quality-proposal.md`에 작성한다. 코드/DB/서비스/새 provider/judge/batch 호출·정본 SPEC/WORK 편집 금지. Orca worker_done 보고.
