# [app] 앱 구현 — WORK-008(SPEC-002 0.5.2)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더) 의 역할 · allowed_paths · 공개 레포 제약 · §9 완료 보고 그대로(핸들은 preamble 값). 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(미커밋 위에 이어서).

**이번 일 = `WORK-008-app-v052.md`(같은 폴더) WP-1 ~ WP-6 전부.** 계약 = `SPEC-002-chat-eval.md` 0.5.2. `_RESUME.md` §2 맨 위 행들 반영.

- **순서**: WP-1 · WP-2 · WP-5 · WP-4 코드는 지금. **WP-3(답 키 다시 뽑기) · WP-4 후보 뽑기 · WP-6 은 코디가 「허브 0.5.2 18106 준비」 를 알려 준 뒤**(허브 워커가 병행 중). 그전에 할 게 없으면 그 상태를 코디에게 알리고 기다려라.

검수 `review-work-v052.md` 의 앱 WARN 넷을 이렇게 닫아라:
- **A-1**: §11 B-1 · B-3 은 **결정됨(코디 11-17)** — 세트 선택 칸 `expected_kinds_by_entry{표:코드: kinds[]}`(있으면 그 대상은 그 종류만 · 없으면 `expected_kinds[]`) · B-3 은 꼴만(`question` 비움). **Q03 · Q05 둘 다 고친다.** Q03 = 케이스 쪽 `overview · mechanism · indication · outcome` / 계열 M1 쪽은 `expected_kinds[]` 그대로(`lineup` 남음). Q05 = `lineup` 빼고 `indication · outcome` 더함. `expected_kinds` 를 읽는 곳을 **grep 으로 전부 세어**(`walk/calls.py:273-278` · `key_calls.py:269` · `answer_key.py:284 · 431` · `report.py:229` · `quality/checks.py:201` · `loader.py:83` 등) 대상별 칸을 따라야 하는 곳은 고치고, 문항 합집합을 쓰는 곳(report 종류 지표 · D11)은 그대로임을 확인해 보고.
- **A-2**: WP-1 맨 앞에 **고치기 전** `data/eval-set/` 의 `set.jsonl` · `calls/` · `answer-key/` · `key-summary.md` · `key-table.md` 를 `_v052a/` 로 **복사**(옮기지 마라 — 18220 이 읽는 자리). 걸음 (나) 는 `EVAL_SET_DIR=<…/_v052b>` 사본으로 돌리고, (다) 에서 본 세트의 키 전용 칸(`key_upper_entries` · `key_lower_entries`)을 지우고 다시 뽑아 행이 같은지 대조.
- **A-3**: K4 가 보는 것은 `layer_depth`(늘 붙음)로 못 박고 `layer_via`(이름)는 얻었을 때만. 이름은 먼저 같은 조회의 `depth` 1 행의 `layer.holder.holder_name`(호출 0) · 그래도 없을 때만 `label` 조회 → 건수 보고(되적기 후보).
- **A-4**: 실물 넷(F1~F4)은 **18221 화면 속도 탭 API(effort low · 동시)** 로 — v05 와 같은 조건(0.5.1 run `53da717fd7a6` · `ce5d23661812` 와 나란히 비교). 18221 은 네가 띄웠다 내림 · 허브는 18106.

- `--confirm` 하지 마라(사용자 확인 몫). 18220 · 18105 는 코디 것.
- 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/app-v052-report.md` — WP 별 · 키 전후 대조(키 전용 칸 뺀 뒤 행 같나) · F1~F4 표(0.5.1 run 대비 B · C 시술 수 · 종료 상태 · 첫 답 ms).
