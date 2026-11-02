---
type: baseline
id: BASE-008
title: "명동 PoC v2 — 시술 현황판(10-16 명동점 인터뷰 · KOS 데모 지점 실연동)"
status: raw
product: cc-prototype
feature: procedure
source:
  type: interview
  ref: "명동점 1차 현장 인터뷰 2026-10-16(ax-clinic-project sources/interviews/2026-10-16-*.md) · 사용자 대화 2026-10-20~21"
links:
  baselines:
    - "[[baseline-003-cc-idea|BASE-003]]"
    - "[[baseline-007-planner-feedback|BASE-007]]"
  decisions:
    - "[[decision-005-procedure-board|DEC-005]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-10-21
updated_at: 2026-10-21
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/baseline
  - status/raw
---

# 명동 PoC v2 — 시술 현황판

## 들어온 것

10-16 명동점 1차 현장 인터뷰 뒤 사용자: **「지금 현황판 말고 시술에 대한 현황판이 필요하다」**. 1 · 2차(`cc` — 데스크 현황판 · 직원 페이지 · 예약관리)는 사용자가 생각한 흐름(v1)이고, v2 는 인터뷰에서 찾은 **실제 문제점**으로 만든다.

## 원천

| 무엇 | 어디 |
|---|---|
| 인터뷰 6건(간호팀 부팀장 · 간호사 · 코디 2 · 대표원장 · 총괄실장) | ax-clinic-project(private) `para/projects/clinic-myeongdong-ax/sources/interviews/2026-10-16-*.md` |
| 업무 흐름 정본 | `reference/2026-10-12-cc-prototype/workflow-v2.md`(v1 = `workflow-v1.md`) |
| KOS 데모 지점 API | `reference/2026-10-12-cc-prototype/kos-demo-api.md` · 이 폴더의 HAR(gitignore) |
| 확정 시안 | claude design `dda9a931` 「Ceramique 시술현황판 v2.dc.html」(사용자 수정본, 2026-10-21) |

## 인터뷰에서 나온 문제(요약)

- 오더지(노티)를 **종이로 뽑아** 방 번호 · 고객 이름과 꽂아 두고, 한 것은 지우고 체크한다(부팀장 07:55)
- KOS 에 「마취 중」이 없어 **「마취용」 가짜 계정**에 배정해 타이머로 쓴다(대표원장 16:56 · 부팀장 18:33). 준비실 벽에 영수증 · 방 번호 · 마취 시간을 손으로 적는다(대표원장 24:52)
- **KOS 담당자 칸을 채워야 의사 호출이 된다** → 실제 어시가 아니라 누른 사람이 담당자로 들어간다(부팀장 16:34)
- 원장들이 KOS 를 보지 않아 **호출을 놓친다**(대표원장 21:16 · 49:14). 호출 로그로 원장별 기여를 보고 싶다(50:18)
- 시술 순서는 기계 · 겹침 때문에 **현장에서 바뀐다** · 구두 · 보드판 · 무전(부팀장 06:07 · 10:07)
- KOS 상태는 매 건 바꾸지 않는다 — 시술 대기 → (원장 콜) 시술 진행 → 귀가 대기만(부팀장 24:26)
- 마취 기본 20분 · 알람은 「방치 아니냐」는 느낌이라 원치 않는다(부팀장 19:01)

## 사용자가 짚은 것

- KOS 를 **화면 하나씩 점진 교체**해 나중에 제거한다 — 당장 CRM 을 못 만들어서
- 시술은 시술실 안(태블릿 · 폰)에서 제어하는 게 원칙 — 지금은 앱이 없어 간호 스테이션에서
- 기존 `cc` 코드를 무시하고 새로 만든다 · 테마 · 디자인 시스템은 유지 · 기존 주소로 올린다
