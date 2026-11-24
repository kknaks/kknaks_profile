# [spec · 고침 1] SPEC-012 0.1.0 → 0.1.1 — 검수 FAIL 반영 (사용자 승인 11-23 「추천대로 · 품질 먼저」 범위)

너는 스펙 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **고칠 것 = `$W/SPEC-012-consult-quality.md` · `$W/quality/` 측정 계약 칸(run.py · score.py 의 gold_hash 기록만)** · 앱 코드 · 프롬프트 · 데이터 · 허브 수정 0 · 커밋 0 · 서브에이전트 0 · 18222 · 18105 손대지 마라(허브 GET 만) · 키 값 출력 0 · **LLM 호출 0**.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(`35b56e5`) · 검수 `$W/review-spec-012.md`(FAIL · P1 7 · P2 8) · 작성 지시(사용자 결정) `$W/quality-spec-task.md` · 허브 데이터 고침 `$W/data-gap3-report.md`(새 gold `9e21d638…` · 검수 `$W/review-data-gap3.md`) · 정해진 것 `$W/_RESUME.md` §2.

## 할 일
1. **P1-1 ~ P1-7 · P2 8 전부** 검수 「고칠 방향」 대로. 요지:
   - HB1 뺌(조건 = kept · 볼 유지 · 점 결정 지킴) · 어긋남은 `list_held` 표지로.
   - HA2 뺌 · 새 주제 판단은 HA1(허브 고민 부위)만.
   - HU1 「새 값」 = 되돌릴 사진에 없는 값(아까 거 = 복원 · 다른 이름 = 교체).
   - HP1 · HW1 효과는 칸에 남기고 셈에서만 쉼(`suspended`) · 넓히기는 되살림.
   - H6 원인 다시 짚음(`fetch_read.py:123-134` owner · 층 없는 outcome 줄의 대상 칸).
   - H1 부위 가족 판단을 행 칸이 아니라 **층 holder(케이스 부위)** 에 · 부위 없는 holder 는 늘 · 크기 전 → 후 기록.
   - 측정: 전 · 후 같은 gold_hash(`meta.json`) · `run.py` · `score.py` 가 gold_hash 를 적게(이 둘은 고쳐도 됨 · LLM 0).
2. 바뀐 계약마다 **결정 칸(정답 19 칸 · `_RESUME` §2) 을 연속 재생 시나리오로 머리로 따라가** 깨지는 칸이 없는지 표로(턴 → 조건 · 목록 · 점 · 판정). 검수가 짚은 S05 T1→T4 · S06 T1→T3 · S10 T3 는 꼭.
3. **WP-0 = 새 gold 위 기준선 다시 재기** — 허브가 바뀌었으므로 `35b56e5` 를 새 gold(코디가 18105 재기동 뒤)로 S01 ~ S13 × 3 번 다시 돌려 「전」 을 새로 잰다(비용 기록 · 이번 고침에서는 돌리지 말고 WP 로만 적어라).
4. 판 0.1.1 · 판 기록 · 「사용자 결정 필요」(0 이 목표).

## 검증
`git -C $A status --short` 0 줄 · 18222 · 18105 그대로 · LLM 호출 0 · 키 grep 0.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-012 0.1.1" --body "P1 닫음 수 / 결정 칸 재생 표 깨짐 수 / 사용자 결정 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-012 0.1.1 완료 — <한 줄>. 상세는 인박스." --enter
```
