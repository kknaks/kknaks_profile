"""DB 접근 전담 계층 (KDEV-WORK-018 P2).

`select()` 와 ORM 이 사는 유일한 자리다. 이 계층 밖으로는 도메인 DTO 만 나간다 —
규약은 `40-architecture/system/README.md` 「백엔드 계층 규약」이 SoT 다.

**신규 도메인만 여기 들어온다.** 레거시(`queue.py`·`service/pipeline/**`)는 일괄
리팩터하지 않고, 만질 일이 생긴 도메인만 옮긴다.
"""
