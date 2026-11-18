# [writer] SPEC-008 0.2.0 · SPEC-001 0.8.1 — 검수 WARN 16 고침

너는 **procedure-hub `writer` 워커**다. 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/writer/role.md`(+ 같은 폴더 문서). `W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`.

먼저 읽어라: `$W/review-spec-008.md`(결함 F-1~F-16 · 근거 · 고칠 방향) · `$W/SPEC-008-consult-entry.md` · `$W/SPEC-001-hub-gold-mcp.md` 0.8.0 · `$W/spec-008-brief.md`(처음 작성 브리프 — 제약 그대로) · `$W/_RESUME.md` §2 맨 위 11-18 행 · `$W/research-input-space/scripts/README.md` · `score.py`.

## 코디 결정(이대로 · 다시 묻지 마라)

- **F-1 ⓒ**: 상담 0.4 서버는 **끈 상태 대화를 새로 열지 않는다**(`chat_state` 기본 on · 끈 상태로 시작하는 새 대화 없음). 0.4 이전에 시작된 끈 대화는 열면 「옛 판 대화」 로 읽기만(새 턴 막음 — 막는 화면 문구는 빈칸 + 정할 것). SPEC-001 영향 표에 이 행을 더하고, 「상담 0.4 켠 상태는 목록 꼴만 써서 0.7.2 허브로도 돈다 — 같이 올리는 것이 필수는 아니다」 를 적는다.
- **F-5**: D-6 의 「고민만 **답**」 = **앞 턴 되물음(ask)에 대한 답**으로 좁힌다(바로 앞 턴이 부위만 + 그 턴에 앱이 고민 선택지를 물었고 + 이번 턴이 고민만일 때만 부위를 잇는다). OU7 · S8-T7 을 그 뜻으로. C15-3 · C28-3 · C05-2 · C38-4 가 이 규칙에서 어떻게 되는지 표로(키와 맞는지).
- **F-6**: E8-6a = 이미 있는 정보 종류 키 134 턴으로 잰다(문턱 U8-2 90% — 코디 기본값 채택). 값 · 깊이(U8-1 = 추천 (가) 채택 — 소넷 호출 안 더함 · 깊이 = 이번 턴 대상만 · 값 표지 없앰)의 **정답 키 꼴**을 E8-6b 에 적고(그 턴 재료에 꼭 있어야 하는 행 · 깊이 읽기 대상 등), **표본 키를 20 턴 이상 실제로 보탠다** — `research-input-space/scripts/convs.py` · `convs2.py` 에 칸을 더하고 `build.py` 로 `conversations.jsonl` 을 다시 낸다(기존 키 · 턴은 바꾸지 않는다 · gold 근거 칸).
- **F-8**: 부위는 **늘 `targets[]` 에도 넣는다**(table = site). `sites[]` = 그 가운데 「이번 턴 부위 거르개」 로 쓸 것. QM3 · OU7 · S8-T7 · §7 규칙을 그 뜻으로.
- **F-9**: `targets` 순서 = **말에 나온 차례** · focus = 마지막 고민. §7 규칙 1 에 한 줄 + S8-T6 에 순서 시험.
- **F-10**: 함수 서명 표(부를 함수 · 넘길 그릇 · `Walk` 칸)를 SPEC 에 짓는다. 안 맞으면 **`walk/` 에 공개 함수(얇은 감쌈 · 동작 변경 0)를 더하는 것은 diff 0 의 예외로 허용** — S8-T18 을 「기존 함수 동작 · 시험 불변」 으로 고친다.
- F-2 · F-3(앞 답 가리키는 턴 = **표 실행에서 답 LLM 실제 호출** · 그 턴이 든 대화 전부) · F-4(장부에 거르개 칸 · score.py/slim.py 를 0.4 장부 칸에 맞추는 일을 E8 앞 단계로) · F-7 · F-11 · F-12 ~ F-16: 리포트 「고칠 방향」 대로. 표 수는 고정 수 대신 「실행 때 score.py 가 낸 수」.
- `ref.to = answer` 턴 수가 검수 5 / 코디 7 로 갈린다 — `conversations.jsonl` 에서 직접 세어 SPEC 에 적어라.

## 쓸 것 · allowed_paths

- `$W/SPEC-008-consult-entry.md` → 0.2.0(변경 기록에 F 번호별 고친 곳) · `$W/SPEC-001-hub-gold-mcp.md` → 0.8.1(F-1 영향 행 · F-11 고칠/지울 시험 표).
- `$W/research-input-space/scripts/convs.py` · `convs2.py` · `build.py`(칸 더하기만) · `$W/research-input-space/conversations.jsonl`(build 로만 다시 냄) · `$W/research-input-space/scripts/README.md`(새 칸 설명).
- 그 밖 금지. 코드(앱 · 허브) · 서버 · LLM · Jev 호출 금지(build.py 실행은 됨).

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer(SPEC-008 fix1) 완료: <한 줄>" \
  --body "변경 파일 / F 별 처분 / 보탠 키 수 / 남은 정할 것 / 주의점" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] writer(SPEC-008 fix1) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
