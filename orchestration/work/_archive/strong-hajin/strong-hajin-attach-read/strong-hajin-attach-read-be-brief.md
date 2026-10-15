# [backend] 조사(read-only) — 결과 자료 첨부가 「내용을 읽지 못함 · 본문에 텍스트가 없습니다」로 뜨는 원인

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-attach-read`
base 브랜치: `origin/main`

**이번 작업은 조사다. 코드를 고치지 않는다.** 산출물은 리포트 파일 하나다(§5).

## 1. SSOT — 먼저 읽을 것

- 스크린샷: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/orchestration/work/strong-hajin-attach-read/screenshot-result-material.png`
  ← 사용자가 본 화면. 「결과 자료 1」 아래 3.1MB · 2026/10/13 파일 하나가 빨간 배지
  「내용을 읽지 못함 · 본문에 텍스트가 없습니다 (스캔…」(뒤가 잘림)로 떠 있다.
- 제품 문서(필요할 때만, read-only): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/para/projects/summer-star/strong-hajin/`
  — 자료(material) 첨부·텍스트 추출에 관한 spec 이 있으면 그 계약과 코드를 대조한다.

**기대는 개념**: 해당 없음.

## 2. 배경 / 무엇을 알아오나

사용자가 결과 자료에 파일(3.1MB)을 올렸더니 위 상태가 됐다. **왜 이렇게 되는지 코드로 설명**해 와라.

답해야 할 질문:

1. 이 문구(「내용을 읽지 못함」 · 「본문에 텍스트가 없습니다」 · 잘린 뒷부분 전체)는 **어디서 만들어지나** — 백엔드 사유 코드/메시지 → 프론트 표시까지 경로를 파일:줄로.
2. **어떤 조건에서 이 상태로 판정되나** — 지원 형식별(PDF·이미지·docx·hwp 등 코드가 다루는 것 전부) 추출 경로와, 「텍스트 없음」으로 떨어지는 분기 전부. 스캔 PDF 판정 기준(글자 수 임계값 등)이 있으면 값까지.
3. **OCR(또는 이미지 → 텍스트) 경로가 있나.** 있으면 왜 이 경우 안 탔는지, 없으면 없다고.
4. 이 상태가 되면 **이후 무엇이 안 되나** — 회의록·보고서·AI 입력 등에서 이 자료가 빠지는지, 재시도 수단이 있는지.
5. 이 상태가 **의도된 계약(spec)대로**인지, 아니면 오판(텍스트가 있는 PDF 인데 추출 실패를 「텍스트 없음」으로 뭉뚱그림 등)일 수 있는 자리가 있는지. 예외를 삼켜 같은 사유로 떨어뜨리는 곳이 있으면 반드시 짚어라.
6. (가능하면) 실제 그 파일의 기록 — 로컬 DB(`postgresql://127.0.0.1:54329/ax_demo`)에서 2026-10-13 생성된 3.1MB 결과 자료 행을 **SELECT 만으로** 찾아 저장된 상태·사유·파일 형식을 확인. 원본 파일이 로컬 저장소에 있으면 그 파일에 대해 코드가 쓰는 추출 함수를 **읽기 전용으로** 한 번 돌려 실제 결과(추출 글자 수 등)를 확인해도 된다. 로컬에 없으면(운영에서 올린 것이면) 「로컬에 없음」으로 적고 넘어가라 — 운영 DB·서버에는 접근하지 마라.

## 3. 계약

해당 없음 (조사).

## 4. 먼저 읽을 핵심 파일

목록을 주지 않는다 — **문구 문자열과 사유 코드를 레포 전체(backend/ · frontend/)에서 grep 해서 쓰는 곳을 전부** 세고 시작하라. 첫 grep 결과만 보고 결론 내지 마라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- **수정 금지.** 코드·설정·DB 어느 것도 바꾸지 않는다.
- 쓰는 파일은 하나뿐: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/orchestration/work/strong-hajin-attach-read/research-attach-read-report.md`

## 6. 단계

1. 문구·사유 코드 grep 으로 생산 지점·소비 지점 전수 파악
2. 업로드 → 저장 → 추출(워커/잡) → 상태 기록 → API → 프론트 배지까지 흐름 추적
3. 질문 1~6 에 답하는 리포트 작성. 모든 주장에 `파일:줄` 근거. 추측은 「추측」이라고 표시
4. 리포트 끝에 「원인 한 줄 요약」과 「고친다면 선택지(결정은 하지 말 것)」

## 7. 범위 제약 — 하지 말 것

- 코드 수정·커밋·push·PR 금지
- 사용자가 띄운 스택(포트 8001·5176·54329 프로세스) 재시작·종료 금지. DB 는 SELECT 만
- `make reset-demo`·`sync-demo-schema` 등 데이터 바꾸는 타겟 실행 금지
- 운영(`ax.medisolveai.xyz`)·클러스터 접근 금지

## 8. 검증

테스트 실행 불필요. 근거 `파일:줄` 이 실제 레포 내용과 맞는지가 검증이다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ad33d6e7-c7ef-4304-895c-99adc0578c5a --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ad33d6e7-c7ef-4304-895c-99adc0578c5a \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ad33d6e7-c7ef-4304-895c-99adc0578c5a --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
