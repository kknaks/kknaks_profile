# [reviewer · 읽기만] SPEC-012 상담 품질 고침 검수 (자동 검수 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 앱 · 허브 · 데이터 · 프롬프트 · `quality/` 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 GET 만) · 키 값 출력 0 · LLM 호출 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(`35b56e5`) · 대상 `$W/SPEC-012-consult-quality.md` 0.1.0 · `$W/quality/`(v0.3 재채점 · 늘린 시나리오) · 작성 지시(사용자 결정 — 기준) `$W/quality-spec-task.md` · 기준선 `$W/quality/base-report.md` · 앞 검수 `$W/review-quality-base-r2.md` · 정해진 것 `$W/_RESUME.md` §2 · 앞 스펙 `$W/SPEC-010*.md` · `$W/SPEC-011-fetch-plan.md`.

## 볼 것
1. **사용자 결정대로인가** — 정답 19 칸 결정 · 「품질 먼저 · 비용 변경 안 넣음 · 새 고정 한도 0」 · `_RESUME` §2 결정(주제 찢기 · 좁히기 + 넓히기 + 되돌리기 · 점 늘 다 뜸 · 0 이면 앞 목록 + 까닭 · 판단은 소넷). 어긋나거나 정해진 것을 다시 묻는 것.
2. **구멍 전수** — H1 ~ H15 가 다 계약에 있나 · 자리 `파일:줄` 을 직접 열어 맞나 · 바뀔 동작이 그 구멍을 실제로 닫나(장부 근거 턴으로 머리로 따라가 보기) · 한 구멍을 막으며 다른 기준(특히 2 · 18 · 20 · 22)을 깨지 않나.
3. **증상 막기 금지** — 낱말 · 문장 하나씩 막는 규칙(정규식 금지어를 프롬프트에 더하기 등)으로 때운 자리는 없나. 입력 꼴 × 데이터 조합으로 일반화됐나.
4. **완료 조건** — 측정 가능 · 전 → 후 같은 시나리오 · 늘린 시나리오의 정답 칸이 매핑 · 허브 값으로만(지은 진료항목 0) · 새 판단 칸이 「확인 필요」 없이 숨어 있지 않나.
5. **재채점 v0.3 재현** — `score.py` 를 스크래치 복사본으로 다시 돌려 1,009/1,116 · 기준 표가 같은가.
6. **WP** — 순서대로 할 수 있나 · 관련 시험만 · 허브 데이터 고침(`$W/data-gap3-task.md` 진행 중)과 장바구니 · SPEC-011 비용 작업과 겹치는 자리.

## 산출
`$W/review-spec-012.md`: 판정 PASS / FAIL · 지적(P0 / P1 / P2 · 근거 = 파일:줄 · 실측 · 고칠 방향) · 재현 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-012" --body "판정 / P0 · P1 · P2 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review SPEC-012 완료 — <한 줄>. 상세는 인박스." --enter
```
