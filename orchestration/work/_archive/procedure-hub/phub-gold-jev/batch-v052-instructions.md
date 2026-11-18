# [app] 37 문항 시험 실행 — batch · 채점 · 보고서(0.5.2)

**너는 앞 판의 맥락이 없다.** /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/phub-gold-jev-app-brief.md 의 역할 · 공개 레포 제약 · §9 완료 보고 그대로(핸들은 preamble 값). 워크트리 /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev. **이번 판은 코드를 고치지 마라 — 돌리고 읽고 보고만.** 막히는 버그가 있으면 고치지 말고 `[질문]`. **디스크 여유 2~3GB — 큰 파일 만들지 마라.**

사용자가 답 키 37 을 확인했다(confirmed 37 — 코디가 기록). 답 프롬프트는 미확정 그대로 돌린다(보고서에 표시).

## 할 것

1. `uv run python -m clinic_chat.batch --check` — 전부 됨인지.
2. `uv run python -m clinic_chat.batch --label v052-37 --columns a,b,c --no-b-on` — 37 문항 × A · B · C(허브 18105 · 18220 은 코디 것 · 띄우거나 내리지 마라). 중간에 끊기면 `--resume <batch_id>`.
3. `uv run python -m clinic_chat.quality.grade --batch <batch_id>` → `uv run python -m clinic_chat.report --batch <batch_id>`.
4. 보고서(`runs/reports/<batch_id>.md`)를 읽고 요약 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/batch-v052-summary.md` 를 쓴다 — **회사 데이터 본문(질문 문장 · 답 · 이름) 넣지 마라: id · 수 · 판정만**:
   - 열별(A · B · C): 키 대비 빠짐(대상 × 정보) · 종료 상태 맞음 · 틀린 말 검사(G · D) 걸림 · Opus 채점 점수 · 첫 답 ms · 입력 토큰 — 합계 · 중앙값
   - B 가 C 보다 못한 문항 · B 가 진 문항 목록(id · 무엇이 빠졌나 · trace 로 본 원인 한 줄)
   - 오늘 고친 꼴 문항(Q03 · Q05 · Q10 · Q12 · Q13 · Q14 · Q35)의 결과
5. 완료 보고에 batch_id · 걸린 시간 · 위 핵심 수.
