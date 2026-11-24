# [app] 모달 효과 · 부작용 정리 (사용자 승인 11-22 · 허브 부작용 분류 끝난 뒤)

너는 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo`. **허브 워커가 `adverse-class-hub-task.md` 를 끝낸 뒤 시작**(허브 칸 `severity_class` · `guidance_texts` · `guidance_kinds` · `guidance_timings` · `guidance_levels` · `guidance_alerts`(「이럴 땐 바로 병원」 줄 표지 — `adverse-class2-report.md`) · `$W/adverse-class-report.md` · 18105 는 코디가 새 gold 로 재기동). 커밋 0 · 서브에이전트 0 · **18222 손대지 마라** · 빈 포트 확인 · 시험은 관련만. 이 작업 범위 밖(점 웨이브 · 스피너 · 침샘 계층 · 장바구니)은 손대지 마라.

## 사용자 결정(11-22)
모달 효과 · 부작용을 고객이 보기 좋게:
1. **같은 이름은 하나로 합친다**(멍 3 줄 → 「멍」 하나 · 그 아래 빈도 · 지속 · 대처법을 모음).
2. **계열(modality)에서 물려받은 줄은 모달에서 뺀다** — 케이스 자기 · 시술 줄만(LLM 블록에는 그대로).
3. **부작용을 일시적 / 주의 / 위급으로 묶어** 보인다(허브 `severity_class`). 위급은 맨 위 · 눈에 띄게.
3b. **「이럴 땐 바로 병원」**: guidance_alerts = true 인 대처 줄은 분류와 별도로 각 부작용 아래 경고로(원문 그대로 · 머리 문구 slot).
4. **고객 문구** = 허브 칸 원문을 잇는다 — 빈도(freq) · 심한 정도 · 언제 · 얼마나(onset · duration) · 대처법(guidance_texts). 예 「멍 — 흔함 · 1 ~ 2 주 · 냉찜질」. 값 없는 칸은 비운다(**지어 넣지 마라**). 묶음 머리 · 칸 이름 등 시안에 없는 글은 slot(빈칸 시작).
5. **효과**도 같은 이름 합침 + 계열 줄 뺌 + 「언제부터 · 얼마나 지속」(onset · peak · duration 원문).
완료: 시험 · 실물 모달 스크린숏 `$W/e2e-shots/modal2-*.png`(입꼬리보톡스 제오민 · 얼굴필러 쥬비덤 · 울쎄라 — 효과 · 부작용 탭) · 줄 수 전 → 후 표 · 리포트 `$W/modal2-report.md`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: 모달 효과 · 부작용" --body "줄 수 / 스크린숏"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app 모달 효과 · 부작용 완료 — <한 줄>. 상세는 인박스." --enter
```
