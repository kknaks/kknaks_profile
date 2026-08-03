"""HTTP 요청·응답 모델 (KDEV-WORK-018 P3).

`service/*/dto.py` 의 도메인 DTO 와 **겸하지 않는다.** 겸하면 HTTP 표면을 바꿀 때
도메인이 따라 바뀌고, 반대로 도메인 필드가 API 로 새어 나간다
(`40-architecture/system` 「백엔드 계층 규약」).

라우터 파일 안에 `BaseModel` 을 두던 레거시(`api/routers/queue.py`) 방식을 대체한다 —
신규 도메인만 해당한다.
"""
