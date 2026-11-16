# [researcher] `pricing-design.md` 검수 FAIL 수정 (F1 · F2 · WARN 8 전부)

너는 **interpret-pwa `researcher` 워커**다. 앞 맥락은 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/researcher/`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (코디 워크트리 — **다른 researcher 가 `idea.md` · `idea-*` 를 쓰는 중. 그 파일은 건드리지 마라**) · PUBLIC — 키 · 실명 금지.

## 읽을 것
1. 원 작성 브리프 `orchestration/work/interpreter-idea/interpreter-idea-research-brief.md` — §0 규칙 · §2 사용자 지정 · §3 8단계. **이게 계약이다.**
2. 검수 리포트 `orchestration/work/interpreter-idea/review-pricing-design-report.md` — F1 · F2 · WARN 전부.
3. 대상 `reference/2026-11-12-interpreter-idea/pricing-design.md` · `pd-*.png` · `orchestration/work/interpreter-idea/pricing-calc/`.

## 고칠 방향
- **F1 (발화마다 수동 stop = 세션 최대)** · **F2 (실사용 1시간 = STT 스트림 1시간)** — 사용자가 정하지 않은 가정이다. **확정하지 말고 §8 「정할 것」에 올리고**, 가격 역산(§5 · §6 · §7)은 **두 경우를 나란히** 계산한다: (가) 수동 stop 허용 — 세션 최대 = 발화 수 · (나) 무발화 60초 자동 종료만. F2 도 해석별로 갈리는 숫자가 있으면 나란히. 하나를 고르지 마라.
- WARN 전부 리포트의 고칠 방향대로(300분 한도 해석 기재 · 토큰 단일단가 「적자 0」 문구를 격자 최대와 맞춤 · 요약 절 추가(워스트 세트 ≠ 범위 최대 ×4.28 포함) · 토큰제 2형태 분할 근거 · 태그 출처 4곳 · D ≤ 5 vs TTS 동시 한도 3 · 2만원은 참고선으로만(Q 입력가로 쓰지 않음) · 그래프 겹침 · 참고선 보이게).
- 무발화 1분 종료가 통키에 아직 없다는 점은 §8 에 사실로.
- Soniox 문서 URL 은 다시 열어 실제 주소로.
- 숫자 · 그래프는 `calc.py` 재실행으로만(손 편집 금지). Soniox 새 호출 금지(usage-logs 조회만).

## allowed_paths
- `reference/2026-11-12-interpreter-idea/pricing-design.md` · `pd-*.png` · `orchestration/work/interpreter-idea/pricing-calc/`

## 검증
- `check_tags.py` 근거 없는 줄 0 · 〔정의〕 · 〔코드〕 같은 보조 태그로 가정을 확정한 곳 0 · `calc.py` 재실행 diff 0 · 키 0.
- 보고 body 에 반영 표(F/W 번호 → 줄).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_49b296be-c26f-40e5-a687-57e4e0998787 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
