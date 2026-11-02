---
type: concept
id: argv-length-limit
title: 실행 인자 길이 한도 — 큰 입력은 argv 가 아니라 stdin 으로 (Argument Length Limit)
aliases:
  - argv 한도
  - MAX_ARG_STRLEN
  - ARG_MAX
  - Argument list too long
  - E2BIG
  - 프롬프트를 stdin 으로
up:
  - 2026-10-07-strong-hajin-enhance
tags:
  - 운영체제
  - 프로세스
  - cli
---

# 실행 인자 길이 한도 — 큰 입력은 argv 가 아니라 stdin 으로

하위 프로세스를 띄울 때 넘기는 **실행 인자(argv)에는 운영체제가 정한 크기 한도가 있다.** 리눅스는 인자 **한 칸**이 128KiB(`MAX_ARG_STRLEN` = 32 페이지)를 넘으면 `execve` 가 `E2BIG`(「Argument list too long」)로 실패한다. 크기를 미리 알 수 없는 입력은 처음부터 **표준 입력(stdin)** 으로 흘려보낸다.

## 정의

1. **두 한도가 따로 있다** — 인자 하나의 상한(`MAX_ARG_STRLEN`, 128KiB)과 인자·환경 변수 전체의 상한(`ARG_MAX`, 보통 스택 한도의 1/4). 전체가 넉넉해도 **한 칸**이 넘으면 실패한다
2. **stdin 은 길이 한도가 없다** — 파이프로 흘려보내면 읽는 쪽이 끝(EOF)까지 받는다. 받는 프로그램이 「인자 대신 stdin 에서 읽기」 를 지원해야 한다(흔한 관례: 인자 자리에 `-`)
3. **지원 여부는 버전마다 다르다** — 로컬에서 되는 것이 운영 이미지의 다른 버전에서도 되는지는 **운영 환경에서 실호출 1회**로 닫는다

## 사용 예시

Strong Hajin 회의록 최종 합성은 재전사 원문 전량 + AI 맥락 목록을 매번 싣게 되면서 프롬프트가 커졌다. 23.5분짜리 운영 회의 하나만으로 **169KB** — argv 한 칸 한도를 넘어 배포 첫 회의부터 합성이 실패할 자리였다. CLI 호출을 `codex exec -` + stdin 으로 바꾸고, 운영 파드에서 `echo … | codex exec -` 로 응답을 받아 운영 CLI 판(로컬보다 낮은 판)에서도 된다는 것을 확인했다.

## 왜 중요한가

- 입력이 작은 동안에는 드러나지 않는다 — 데이터가 자라는 순간 **조용히 운영에서만** 깨진다. 로컬 시험 데이터는 대개 작다
- 크기를 줄여 한도 안에 넣는 처방(요약·잘라 싣기)은 입력을 잃는다. 원문 전량이 필요한 일(정정 pass)에는 쓸 수 없다

## 경계와 오해

- **「안 되면 옛 방식으로 되돌아가기」 를 붙이지 않는다** — stdin 이 실패하면 argv 로 다시 부르는 되돌이는 오류 문구를 맞추는 식으로 짜기 쉽고, 첫 호출이 이미 프로세스를 띄운 뒤라면 **같은 일을 두 번 실행**한다. 부작용이 있는 하위 프로세스는 재실행이 안전하지 않다 → [[idempotency]] · [[no-silent-fallback]]
- **[[command-line-arguments]] 는 「무엇을 넘기나」, 이 개념은 「얼마나 넘길 수 있나」** — 짧은 설정값은 여전히 인자가 맞다
- 환경 변수로 우회해도 같은 한도(`ARG_MAX`)에 걸린다

## 함께 보는 개념

- [[standard-input]] — 큰 입력이 가는 통로
- [[process]] — 한도가 걸리는 자리(`execve`)
- [[dev-prod-parity]] — 로컬 CLI 판과 운영 판이 다른 것을 실호출로 닫은 이유

## 출처

- [[2026-10-07-strong-hajin-enhance]] §2 — Strong Hajin WORK-012 최종 합성 프롬프트(`cli_process.py` · 검수가 argv 한 칸 128KiB 를 짚음 · 운영 Codex 판 실호출 · 되돌이의 이중 실행 결함)
