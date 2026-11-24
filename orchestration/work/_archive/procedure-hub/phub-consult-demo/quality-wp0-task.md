# [측정] SPEC-012 WP-0 — 새 gold 위 기준선 다시 재기 (사용자 승인 11-23 「품질 먼저 · 쭉 진행해」)

너는 측정 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 앱 · 프롬프트 · 데이터 · 허브 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 18105 GET 만 — 코디가 새 gold `e8f02287…` 로 재기동해 둠) · 키 · 토큰 값 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 측정 `$W/quality/`(`run.py` · `score.py` · `build_answers.py` · `scenarios.json` S01 ~ S13) · 스펙 `$W/SPEC-012-consult-quality.md` 0.1.2 §5 WP-0 · §4 완료 조건 C1 · C5 · 앞 기준선 `$W/quality/base-report.md`.

## 주의 — 앱 워크트리는 지금 다른 워커가 고치는 중이다
`A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` 의 작업 트리는 **쓰지 마라**(커밋 안 된 SPEC-012 코드가 들어 있다). 기준선은 **커밋 `35b56e5` 그대로**여야 한다:
- `git -C $A archive 35b56e5 | tar -x -C <스크래치>/base-35b56e5` 로 따로 풀고, git 무시 파일(`data/kos/` · `.env`)은 `$A` 에서 **읽기 전용 링크나 복사**로만 가져온다(`$A` 에 쓰기 0). `uv sync` 는 그 스크래치 폴더에서.
- `run.py` 가 앱 경로를 받게 되어 있지 않으면 **인자만 더해** 고친다(측정 스크립트는 고쳐도 됨).
- 기동 env 는 18222 와 같게: `CHAT_STATE=on CHAT_KOS_MAP=data/kos/myeongdong-mapping-20261120-v3.json CHAT_KOS_MAP_SHA=d21903f5 CHAT_IMAGE_DIR=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images` · 빈 포트 · 장부는 따로 `CHAT_DIR`.

## 할 일
1. `build_answers.py` → `answers.json`(gold_hash = `e8f02287…` 기록 확인).
2. `run.py --runs 3` S01 ~ S13(S12 · S13 첫 측정) → `out/base2-<시각>/`(meta 에 gold_hash · 앱 커밋 `35b56e5`).
3. `score.py` → 기준 22 × 통과율 · 흔들림 · 비용 · **옛 기준선(661335b6 gold) 대비 데이터만 바뀐 효과** 표(같은 앱 · 다른 gold).
4. `$W/quality/base2-report.md` — 이것이 SPEC-012 「전」 기준선이 된다.

## 검증
`git -C $A status --short` 이 시작 전과 같음(다른 워커 변경은 그대로 · 네 쓰기 0) · 18222 · 18105 그대로 · 띄운 포트 끔 · 키 grep 0.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "측정 완료: WP-0 새 gold 기준선" --body "확정 통과 / 낮은 기준 / 데이터 효과 / 비용"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] WP-0 기준선 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] wp0: <질문>" --enter`
