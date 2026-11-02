# [frontend] WORK-010 Phase 2b fix1 — 검수 WARN 처리

검수 `review-fe-p2b-report.md`(같은 폴더) WARN 4. 코디 답:
- **W1** 업무 version 을 올리는 **나머지 명령도 같은 직렬 대기열**로 — 제안 생성·응답(`:1746,1759`), 자료 upload/attachLink/떼기, 완료 보고 제출, 연결 편집 저장. 완료 보고 모달을 연 채 제목을 저장해도 422 가 나지 않게 + 시험 1건(모달 제출과 인라인 저장이 겹칠 때)
- **W2** 담당 후보는 **상세를 연 동안 한 번만** 조회(셀렉트가 다시 서도 재조회 안 함). 「변경 제안 중」 대상 이름은 **후보 목록(또는 서버 assignment 응답)** 에서 찾고, 못 찾으면 빈칸이 아니라 기존 대체 문구
- **W3** `styles/ax.css:312-316` `.scax-chat__context*` 죽은 규칙 삭제(사용처 0 확인)
- **W4** `⋯` 글리프·`Select tone=danger` 는 DS-gaps 기록만(고치지 않음)
범위·allowed_paths·하지 말 것은 2b 브리프 그대로(`App.tsx` 다운로드 수신부 금지). 검증: 바뀐 테스트 + 전체 `npx vitest run --no-file-parallelism`(기준선 5건) + `npx tsc --noEmit`. 리포트 `fe-p2b-worker-report.md` 끝에 「fix1」 절. 완료 보고는 같은 두 채널(subject 「frontend 완료: WORK-010 Phase 2b fix1」).
