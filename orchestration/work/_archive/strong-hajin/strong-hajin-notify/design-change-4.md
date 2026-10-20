# strong-hajin-notify — 시안 변경 4: 설정 업무 `answer` 문구

- 작성: architect 워커 · 2026-10-08
- 대상: Claude Design `7e839512-977c-4142-b4b5-d992df566ffc` — 1파일 (DesignSync `write_files` 1회 · 지운 것 없음)
- 입력: 지시서 `design-fix3-instructions.md` · DEC-010 「시안 고칠 것」 ⑦ · D-19
- **시작 전 확인**: 원격 `handoff/settings/js/data.js` 전문을 다시 읽었다. 앞 판(design-change-3)에서 올린 내용과 같았고, 로컬 sha256 도 앞 판 값(`75bdd2c9c60b`)과 같았다

## 1. 파일별 바이트 (원격 = 로컬 사본)

업로드는 로컬 사본(`reference/2026-09-10-sc-meeting/package 2/`) 파일을 `localPath` 로 바로 읽어서 했다. 그래서 원격과 사본은 같은 바이트다. 업로드 뒤 원격 전문을 다시 읽어 바뀐 줄과 나머지가 같은 것을 확인했다.

| 파일 | 바이트 | sha256 앞 12 | 바뀐 것 |
|---|---:|---|---|
| `handoff/settings/js/data.js` | 7,811 | `0d09cb5f4091` | 업무 `answer` 의 label · desc 만 |

## 2. 바꾼 것

| | 앞 | 뒤 |
|---|---|---|
| label | 내 요청이 수락·거절됐을 때 | **내가 보낸 요청·배정·제안에 답이 왔을 때** |
| desc | 내가 보낸 업무 요청에 받는 사람이 답하면 | **받는 사람이 수락·거절하거나 제안에 답하면** |

id(`answer`) · 기본값(켬) · 다른 항목 · 다른 파일은 그대로다.

## 3. 확인한 것
- node(jsdom + `_ds_bundle.js` 실물)로 설정을 렌더해 예외 0건을 확인했다. 카드 머리는 업무 8개 중 7개 · 메시지 3개 중 3개 · 회의 5개 중 5개이고, 항목은 모두 16개다
