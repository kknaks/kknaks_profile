# [code] SPEC-012 0.1.2 구현 — WP-1 → WP-2 → WP-3 (사용자 승인 11-23 「품질 먼저 · 쭉 진행해」 · 「추천대로」)

너는 앱 코드 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` 에서만 코드 · 프롬프트 수정 · **커밋 0** · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 18105 GET 만) · 키 · 토큰 값 출력 0 · **LLM 호출 0**(측정 WP-0 · WP-4 는 코디가 따로 발주) · 시험은 WP 마다 관련만 · 전체 pytest 는 맨 끝 한 번.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 정본 **`$W/SPEC-012-consult-quality.md` 0.1.2**(검수 r3 PASS `$W/review-spec-012-r3.md`) · 기준선 `$W/quality/base-report.md` · 정해진 것 `$W/_RESUME.md` §2 · 기준 커밋 `35b56e5`.

## 사용자 결정(다시 묻지 마라)
- 품질 먼저 · **비용 쪽 변경(자료 줄이기 · 한도 · 가격 빼기) 0** · 새 고정 한도 0 · 판단은 소넷 그대로(앱은 허브 사실 · 상태로 붙잡기) · **낱말 · 문장 목록으로 뜻을 가르는 새 규칙 0**.
- 정답 19 칸 · `_RESUME` §2 결정(주제 찢기 · 좁히기 + 넓히기 + 되돌리기 · 점 늘 다 뜸 · 0 이면 앞 목록 + 까닭).

## 할 일
1. 스펙 §5 **WP-1 → WP-2 → WP-3** 순서. 자리 · 완료 조건 · 관련 시험은 스펙 표 그대로. **§3-D 연속 재생 시험**(S05 T1 → T4 · S06 T1 → T3 · S10 T3 · T4 · 맞춤법 「있어」 · 오타 「잇어」 꼴)을 시험 파일로.
2. 검수 r3 P2 4 개도 반영: P2-1 기존 낱말 판정 `consult/kos_block.py:21` `TOGETHER` 를 HD1 「물었을 때만」 과 맞춤(낱말이 아니라 1차 이해 출력으로) · 다른 기존 낱말 판정 자리 전수(grep · 목록을 리포트에) · P2-2 `score.py` 정답표 gold 비면 멈춤 · P2-3 스펙 표 머리 · S11 T6 판정 칸(스펙 문서 고침은 코디가 하지 않음 — 리포트에 적기만) · P2-4 HQ1 물음 턴의 뺌 · 고르기는 답 재료로만.
3. WP 마다 바뀐 `파일:줄` · 관련 시험 결과. 끝에 전체 pytest 한 번(기준 701 통과 · 옛 실패 1).
4. 화면이 깨지지 않았나 — 빈 포트에 띄워 **LLM 없이 열리는 화면만**(첫 화면 · 시험 대화 재생이 있으면 그것) 스크린숏 `$W/e2e-shots/spec012-*.png` · 띄운 포트는 끔.

## 산출
`$W/spec-012-code-report.md`: WP 별 바뀐 파일:줄 · 구멍 → 고친 자리 표 · 시험 결과(관련 · 전체) · 기존 낱말 판정 자리 목록 · 남은 것.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: SPEC-012 WP-1~3" --body "구멍 닫음 수 / 시험 수 / 남은 것"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-012 구현 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] spec012-code: <질문>" --enter`
