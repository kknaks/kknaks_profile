# [spec · 고침 1] SPEC-012 0.1.1 → 0.1.2 — 재검수 r2 FAIL 반영 (사용자 승인 11-23 「추천대로 · 품질 먼저」 범위)

너는 스펙 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **고칠 것 = `$W/SPEC-012-consult-quality.md` · `$W/quality/` 측정 계약 칸(run.py · score.py 의 gold_hash 기록만)** · 앱 코드 · 프롬프트 · 데이터 · 허브 수정 0 · 커밋 0 · 서브에이전트 0 · 18222 · 18105 손대지 마라(허브 GET 만) · 키 값 출력 0 · **LLM 호출 0**.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(`35b56e5`) · 재검수 `$W/review-spec-012-r2.md`(FAIL · P1-A 1 · P2 6 · 앞 P1 7 닫힘) · 앞 검수 `$W/review-spec-012.md` · 작성 지시(사용자 결정) `$W/quality-spec-task.md` · 허브 데이터 고침 `$W/data-gap3-report.md`(gold `ab5eebc9…` · 검수 r2 PASS · 사람 판단 J 반영 고침 2 진행 중 — 최종 gold 는 코디 재기동 때 정해짐) · 정해진 것 `$W/_RESUME.md` §2.

## 할 일
1. **P1-A · P2-1 ~ P2-6 전부** 재검수 「고칠 방향」 대로. 특히 P1-A: 동형 어미(있어 · 없어 · 돼 …) 낱말로 물음을 가르지 마라 — 판단은 소넷(1차 kinds · 출력 칸) 또는 데이터(고르기가 지금 목록을 좁히나)로 · 맞춤법 꼴(「있어」) · 오타 꼴(「잇어」) 시험을 둘 다 더함. P2-5 gold 는 「코디 재기동 때 최종 gold」 로 적음. P2-3 정답표 gold_hash 기록 · 다르면 멈춤(측정 스크립트는 고쳐도 됨 · LLM 0).
2. 결정 칸 연속 재생 표를 다시 · 낱말 · 문장 목록이 앱 뜻 판정을 맡는 곳이 남았는지 전수(0 이 목표).
3. 판 0.1.2 · 판 기록 · 「사용자 결정 필요」(0 이 목표).

## 검증
`git -C $A status --short` 0 줄 · 18222 · 18105 그대로 · LLM 호출 0 · 키 grep 0.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-012 0.1.2" --body "P1-A · P2 닫음 / 남은 낱말 판정 수 / 결정 칸 재생 깨짐 수 / 사용자 결정 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-012 0.1.2 완료 — <한 줄>. 상세는 인박스." --enter
```
