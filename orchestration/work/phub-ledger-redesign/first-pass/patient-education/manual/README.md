# manual/ — 구획별 직접 읽기 기록 (사람이 쓰는 정본)

build.py 가 이 파일들을 읽어 expressions.json·coverage.json·review-part-*.md 를 생성한다. 생성물은 직접 고치지 않는다.

- `read_status`: `direct_read`(원문 전체를 직접 읽음) / `planned`(미독)
- `last_read_pointer`: 그 구획에서 마지막으로 실제 읽은 Pointer
- `expressions`: { 구획 루트 기준 상대 Pointer: [[원문 부분문자열, "facet,facet", 메모, (선택) n번째 출현], ...] }
  - 부분문자열은 원문 그대로여야 하며 build 가 위치를 찾지 못하면 실패한다. 겹침은 의도(문장·구절·내부 수식어)
- `observations`: [[상대 Pointer, 상태, 관찰], ...]  상태 = P 잠정 · F 후속 의미 조사 · B 원문 정보 부족 · I 원문 내 불일치 · K 알려진 분석 한계 · A 에이전트 추출/해석 오류 · C 사용자 결정 필요
