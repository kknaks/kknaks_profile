# problem-packages 1차 — 진행 기록

원본 `orchestration/work/phub-recommend/bronze/phub-ledger/problem-packages.json` · 73526 바이트 · sha256 `e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc`

## 구획 계획 (구조 확인 후 확정)

S00 = 루트·version·updated·description·/problems 컨테이너. S01~S14 = /problems/0~13 각각 전체(problem 하나 = 구획 하나, complaint 문맥을 끊지 않음).

## 직접 읽기 상태

| 구획 | 범위 | 직접 읽기 | 기록 |
|---|---|---|---|
| S00 | 루트·메타 | done | manual/S00.json |
| S01 | /problems/0 (P1 쁘띠시술, c0~c16) | done | manual/S01.json |
| S02 | /problems/1 (P2 주름, c0~c6) | done | manual/S02.json |
| S03 | /problems/2 (P3 쳐짐, c0~c4) | done | manual/S03.json |
| S04 | /problems/3 (P4 항노화, c0~c6) | done | manual/S04.json |
| S05 | /problems/4 (P5 색소/미백, c0~c7) | done | manual/S05.json |
| S06 | /problems/5 (P6 여드름, c0~c7) | done | manual/S06.json |
| S07 | /problems/6 (P7 모공, c0~c5) | done | manual/S07.json |
| S08 | /problems/7 (P8 홍조/혈관, c0~c4) | done | manual/S08.json |
| S09 | /problems/8 (P9 흉터, c0~c11) | done | manual/S09.json |
| S10 | /problems/9 (P10 제모, c0~c3) | done | manual/S10.json |
| S11 | /problems/10 (P11 얼굴윤곽, c0~c6) | done | manual/S11.json |
| S12 | /problems/11 (P12 바디, c0~c10) | done | manual/S12.json |
| S13 | /problems/12 (P13 두피/탈모, c0~c10) | done | manual/S13.json |
| S14 | /problems/13 (P14 기타, c0~c6) | done | manual/S14.json |

마지막으로 직접 읽은 Pointer: `/problems/13/complaints/6/alternatives/0` (S14 끝). 남은 구획 없음.

## 단계

- [x] 원본 해시·구조 고정, 구간 보존 파서(pp_common.py) — 중복 키 0, 이스케이프 0, 줄바꿈 0, 전부 BMP
- [x] 구획별 직접 읽기(reading/Sxx.txt 덤프 → manual/Sxx.json 관찰·수동 표현·미결)
- [x] build.py: source-map·morphology·expressions·coverage·review·issues 생성
- [x] 단서 누락 검토(정규식 단서 ↔ 수동 표현 대조) 후 보강 — S11 '장기 콜라겐' 2건 보강, '반영구' 15건 판단 기록
- [x] 원장 전체 대조 관찰 OB-S00-05~07 추가
- [x] verify.py 91851 검사 실패 0 + 변조 시험 7종 감지 → validation.md

**상태: 1차 범위 종료 · 원장 전체 완료 아님.** 열린 문제는 issues.md(B 9 · I 10 · F 8 · K 5 · C 0 · A 0).

## 재현 명령 (레포 루트)

```sh
python3 orchestration/work/phub-ledger-redesign/first-pass/problem-packages/reading_dump.py
OMP_NUM_THREADS=1 uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/problem-packages/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/problem-packages/verify.py
```
