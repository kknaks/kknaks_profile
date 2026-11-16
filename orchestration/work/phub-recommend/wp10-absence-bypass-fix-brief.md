# WP-10 F1 부재 안내 혼합 주장 우회 제거

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 코드. `reference/2026-10-30-hub-evals/build-out/wp10-final-code-review.md` 잔여 F1 P1의 직접/5개 fake 전체 경로 재현을 고친다. F2/F3·고정 UI·공개 안전·동적 page·부분 답 PASS 범위를 유지한다.
- `정보 없음` 포함 여부나 범위 단어 존재로 전체 자유 문장을 승인하는 예외를 제거한다. 원천 부재 안내는 검증된 target×section×condition 완료 상태에서 **앱이 생성한 닫힌 문장/구조화 claim**만 허용하고 추가 절/의료 내용이 들어가면 거부한다. LLM이 쓴 임의 부재 문장에 대해 substring/토큰 검사로 승인하지 않는다. 같은 줄 일반 마침표/질문/세미콜론/인용 경계 뒤 추가 주장도 독립 검증한다. 원문 내 문장부호·숫자·ID 파싱은 보존한다.
- 검증기·보정기·최종 반환 경로의 모든 포괄 예외(return True/skip/absence bridge)를 함께 점검해 비슷한 승인 우회를 남기지 않는다. 의료 단어 blacklist 추가로 해결하지 않는다. 고정 UI/검증 원문/앱 생성 범위 부재 외 임의 문장을 승인할 때는 근거를 분명히 하며 불명확하면 보류한다.
- 보고서 5개 혼합 재현과 변형(인용 유무·줄바꿈/무공백·다른 부재 표현·효과/위험/조건/수치) 직접·보정·fake 전체 경로 음성, 정당한 완료 범위 부재 양성/미완료 거부를 추가한다. 전체 suite/Ruff/diff PASS와 저장 Q002 오프라인 답 확인. 새 provider/Hub/judge/batch 호출 금지.
- 앱/관련 테스트만 수정. Hub/DB/서비스·포트/컨테이너·커밋/푸시/PR 금지. `reference/2026-10-30-hub-evals/build-out/wp10-absence-bypass-fix-report.md`에 변경/잔여 한계/검증을 적고 Orca worker_done 보고.
