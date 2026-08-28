
# [backend] fix6 — 시스템 프롬프트 거절 범위 좁히기 (한 곳, 마지막)

너는 WORK-023 의 **kknaks-dev `backend` 워커**다. 관측된 문제: fix4 이전 세션을 resume 한 대화에서 「회사 프로젝트 뭐하고 있어?」에 tool 을 안 부르고 사렸다. 새 대화는 정상. 원인 일부가 프롬프트 ③의 넓은 문구(「회사 내부 정보 거절」)다 — spec §5 프롬프트 계약이 개정됐다(v0.0.9 본문 참조).

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`

## 수정
`service/chat/prompt.py` 의 거절 조항을 spec 개정대로: 거절은 **미공개** 내부 정보(미공개 스펙·내부 구성·기밀)로 좁히고, **「회사 제품의 공개 소개는 회사 제품 tool 로 적극 안내한다 — 이전 턴에서 사렸더라도 이 지침이 우선」** 을 명시(마지막 절이 stale 세션 선례를 뒤집는 장치다). 기존 프롬프트 톤·형식 유지, 이 조항만.

## 검증
```
cd app/back && uv run pytest -q tests/
```

## 완료 보고 — 2채널, 핸들은 preamble 우선 (subject "backend fix6 완료")
orca send: --to term_53806a6d-ced5-4948-88bd-4181b7ba4323
