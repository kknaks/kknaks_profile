# [researcher] 통키 아이디어 — 단계별 모식도 · 목업 (`idea.md`)

너는 **interpret-pwa `researcher` 워커**다. 앞 맥락은 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/researcher/` (`role.md` 외 4개)
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (코디 워크트리 탑승 — reviewer 워커가 read-only 로 같이 있다. 너는 §5 경로만 쓴다) · ⚠ PUBLIC — 키 · 실명 금지.

## 0. 규칙

- **아이디어 문서다. 구현 · 일정 · 결정은 다루지 않는다.** 목업으로 「이런 모습」을 보여 주는 게 목적.
- 단계 정의는 아래 §2 사용자 말 그대로. 늘리거나 바꾸지 마라.
- 정해지지 않은 부분은 **선택지로 그려 둔다**(예: 직원 화면 = 지금 통키 화면 / 여러 방 콘솔 두 가지 목업). 질문으로 막지 마라.
- 특정 병원 · 지점 데이터(내원 수 · 방 구성 · 평면도 · 인터뷰)는 쓰지 않는다. 동선 예시는 일반적인 피부과 흐름으로 「예시」 표기.
- 원가 · 요금 숫자는 넣지 않는다(요금제는 별도 보고서 `pricing-design.md`).

## 1. 원천

- 외부 제안서 2건(아이디어 참고): `reference/2026-11-12-interpreter-idea/TAMION_Hotel_Proposal_v2.pdf` · `TAMION_MEDICAL_의료관광_제안서_v2.pdf` (`pdftotext -layout`). 문구 · 수치 · 이미지 복사 금지 — 아이디어만, 쪽 번호로 출처.
- 대표 대화(코디 요약): 「원격으로 — 환자가 방에서 말하고 로비에서 듣는 것」이 좋은 아이디어라고 함.
- 지금 통키 화면(0단계 목업의 기준): 코드 `/Users/kknaks/git/toy_pr2/interpret-pwa/front/` (main `17c26b5`) — 통역 화면 구성(외국어 영역 180° 뒤집힘 등)을 코드에서 읽어 그대로 옮긴다. 설계 `para/projects/summer-star/interpret-pwa/10-decision/` 참고.

## 2. 단계 (사용자 정의)

| 단계 | 내용 |
|---|---|
| **0 · 지금** | 통역앱 — 마주 보고 통역(기기 1대) |
| **1단계** | 통역 + **원격 통역**(제안서 H 기능처럼). **QR 1단계** — QR = **고객 화면**: 고객이 QR 을 찍으면 자기 폰이 고객 쪽 통역 화면이 된다. 고객은 방에서 말하고 직원은 로비에서 듣고 답한다 |
| **2단계** | 통역 + 원격 통역 + **오늘 피부과 동선 안내 · 호출**. **QR 2단계** — 같은 고객 화면에 동선 안내 · 호출이 더해진다 |

## 3. 산출물

`reference/2026-11-12-interpreter-idea/idea.md` + 같은 폴더 `idea-*.svg`(또는 png)

1. 요약 — 단계별 한 줄
2. 단계별(0 · 1 · 2) 각각:
   - **모식도** — 누가 · 어디서 · 어떤 화면으로 · 말이 어디로 가나(고객 / 직원 / 통키 서버)
   - **화면 목업** — 고객 화면(QR) · 직원 화면. 미정인 곳은 선택지 목업 2개(예: 1단계 직원 화면 = 지금 통키 화면 그대로 / 여러 방 콘솔)
   - 지금 통키에서 **새로 필요한 것** — 한 줄 목록 수준(설계 · ERD 금지)
3. 제안서에서 가져온 아이디어 표 — 아이디어 · 제안서 쪽 · 우리 단계(0/1/2/해당 없음)
4. 열린 것 — 선택지로 그린 것들의 목록(결정 금지)

목업 형식: 와이어프레임 수준 SVG(텍스트 · 상자 · 화살표). 한글 · 외국어 예시 문장은 **가짜 예시**(「예: 아프면 말씀해 주세요」 같은 일반 문장)로, 실제 기록 · 실명 금지. md 에서 `![](idea-….svg)` 로 보이게.

## 5. allowed_paths

- `reference/2026-11-12-interpreter-idea/idea.md` · 같은 폴더 `idea-*.svg|png` (새 파일)
- `orchestration/work/interpreter-idea/idea-src/` (목업 생성 스크립트가 있으면)
- 그 외 read-only. Soniox · 운영 서버 호출 금지.

## 8. 검증

- 단계 정의가 §2 와 같은지 · 결정 문장 0 · 숫자(원가 · 병원) 0 · 제안서 문단 복사 0(20자 이상 겹침 grep) · 키 · 실명 0.
- 모든 SVG 가 md 에서 열리는지(파일 존재 · 문법) 확인.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_ca45be95-dbb7-43a4-8784-0aa6cee432de \
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
