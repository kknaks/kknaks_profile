# S01 — /problems/0 P1 쁘띠시술

[← review.md](review.md) · 범위 /problems/0 및 /problems/0/** 전체 · 소유 노드 456 · 말단 292 · 빈 값 6 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S01.txt 로 c0~c16 전부(procedures 32·combos 17·alternatives 17) 위에서 아래로 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 5 | `/problems/0` | `(problems 원소)` | 0 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 6 | `/problems/0/problem_id` | `problem_id` |  | string | P1 |  |
| 7 | `/problems/0/problem` | `problem` |  | string | 쁘띠시술 |  |
| 8 | `/problems/0/complaints` | `complaints` |  | array[17] | (배열 · 17개) |  |
| 9 | `/problems/0/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 10 | `/problems/0/complaints/0/cc` | `cc` |  | string | 코필러 | OB-S01-01 |
| 11 | `/problems/0/complaints/0/cc_detail` | `cc_detail` |  | string | 콧대/코끝 | OB-S01-02 |
| 12 | `/problems/0/complaints/0/cc_group` | `cc_group` |  | string | 코 |  |
| 13 | `/problems/0/complaints/0/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 14 | `/problems/0/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 15 | `/problems/0/complaints/0/procedures/0/name` | `name` |  | string | 필러 |  |
| 16 | `/problems/0/complaints/0/procedures/0/category` | `category` |  | string | M2 |  |
| 17 | `/problems/0/complaints/0/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 18 | `/problems/0/complaints/0/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 19 | `/problems/0/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 20 | `/problems/0/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 이브아르 |  |
| 21 | `/problems/0/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 22 | `/problems/0/complaints/0/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 23 | `/problems/0/complaints/0/procedures/1/category` | `category` |  | string | M1 |  |
| 24 | `/problems/0/complaints/0/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 25 | `/problems/0/complaints/0/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 26 | `/problems/0/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 27 | `/problems/0/complaints/0/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 28 | `/problems/0/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 29 | `/problems/0/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 30 | `/problems/0/complaints/0/combos/0/name` | `name` |  | string | 필러 + 보톡스 | OB-S01-04 |
| 31 | `/problems/0/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 32 | `/problems/0/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 33 | `/problems/0/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 34 | `/problems/0/complaints/0/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 | OB-S01-14 |
| 35 | `/problems/0/complaints/0/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 36 | `/problems/0/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 37 | `/problems/0/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 38 | `/problems/0/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 39 | `/problems/0/complaints/1/cc` | `cc` |  | string | 코실리프팅 | OB-S01-01 |
| 40 | `/problems/0/complaints/1/cc_detail` | `cc_detail` |  | string | 코끝 거상 |  |
| 41 | `/problems/0/complaints/1/cc_group` | `cc_group` |  | string | 코 |  |
| 42 | `/problems/0/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 43 | `/problems/0/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 44 | `/problems/0/complaints/1/procedures/0/name` | `name` |  | string | 실리프팅 |  |
| 45 | `/problems/0/complaints/1/procedures/0/category` | `category` |  | string | M7 |  |
| 46 | `/problems/0/complaints/1/procedures/0/role` | `role` |  | string | 물리적 거상 |  |
| 47 | `/problems/0/complaints/1/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 48 | `/problems/0/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 민트리프트 |  |
| 49 | `/problems/0/complaints/1/procedures/0/products/1` | `(products 원소)` | 1 | string | 테스리프트 |  |
| 50 | `/problems/0/complaints/1/procedures/0/products/2` | `(products 원소)` | 2 | string | 실루엣소프트 |  |
| 51 | `/problems/0/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 52 | `/problems/0/complaints/1/procedures/1/name` | `name` |  | string | 필러 |  |
| 53 | `/problems/0/complaints/1/procedures/1/category` | `category` |  | string | M2 |  |
| 54 | `/problems/0/complaints/1/procedures/1/role` | `role` |  | string | 볼륨 보충 |  |
| 55 | `/problems/0/complaints/1/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 56 | `/problems/0/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 57 | `/problems/0/complaints/1/procedures/1/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 58 | `/problems/0/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 59 | `/problems/0/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 60 | `/problems/0/complaints/1/combos/0/name` | `name` |  | string | 실리프팅 + 필러 |  |
| 61 | `/problems/0/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 62 | `/problems/0/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 실리프팅 |  |
| 63 | `/problems/0/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 필러 |  |
| 64 | `/problems/0/complaints/1/combos/0/reason` | `reason` |  | string | 거상 + 볼륨 = 입체적 리프팅 | OB-S01-14 |
| 65 | `/problems/0/complaints/1/combos/0/evidence` | `evidence` |  | string | 실이 당기고 필러가 채움 |  |
| 66 | `/problems/0/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 67 | `/problems/0/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 실 시술 후 2개월간 HIFU/RF 피할 것 | OB-S01-09 |
| 68 | `/problems/0/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 69 | `/problems/0/complaints/2/cc` | `cc` |  | string | 이마필러 | OB-S01-01 |
| 70 | `/problems/0/complaints/2/cc_detail` | `cc_detail` |  | string | 볼륨/라운딩 | OB-S01-02 |
| 71 | `/problems/0/complaints/2/cc_group` | `cc_group` |  | string | 이마/관자놀이 |  |
| 72 | `/problems/0/complaints/2/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 73 | `/problems/0/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 74 | `/problems/0/complaints/2/procedures/0/name` | `name` |  | string | 필러 |  |
| 75 | `/problems/0/complaints/2/procedures/0/category` | `category` |  | string | M2 |  |
| 76 | `/problems/0/complaints/2/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 77 | `/problems/0/complaints/2/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 78 | `/problems/0/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 79 | `/problems/0/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 80 | `/problems/0/complaints/2/procedures/0/products/2` | `(products 원소)` | 2 | string | 이브아르 |  |
| 81 | `/problems/0/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 82 | `/problems/0/complaints/2/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 83 | `/problems/0/complaints/2/procedures/1/category` | `category` |  | string | M1 |  |
| 84 | `/problems/0/complaints/2/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 85 | `/problems/0/complaints/2/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 86 | `/problems/0/complaints/2/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 87 | `/problems/0/complaints/2/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 88 | `/problems/0/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 89 | `/problems/0/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 90 | `/problems/0/complaints/2/combos/0/name` | `name` |  | string | 필러 + 보톡스 | OB-S01-04 |
| 91 | `/problems/0/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 92 | `/problems/0/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 93 | `/problems/0/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 94 | `/problems/0/complaints/2/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 |  |
| 95 | `/problems/0/complaints/2/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 96 | `/problems/0/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 97 | `/problems/0/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 98 | `/problems/0/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 99 | `/problems/0/complaints/3/cc` | `cc` |  | string | 이마지방이식 | OB-S01-01 |
| 100 | `/problems/0/complaints/3/cc_detail` | `cc_detail` |  | string | 자가지방 |  |
| 101 | `/problems/0/complaints/3/cc_group` | `cc_group` |  | string | 이마/관자놀이 |  |
| 102 | `/problems/0/complaints/3/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 103 | `/problems/0/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 104 | `/problems/0/complaints/3/procedures/0/name` | `name` |  | string | 지방이식 |  |
| 105 | `/problems/0/complaints/3/procedures/0/category` | `category` |  | string | M6 |  |
| 106 | `/problems/0/complaints/3/procedures/0/role` | `role` |  | string | 자가지방 이식 |  |
| 107 | `/problems/0/complaints/3/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) | OB-S01-12 |
| 108 | `/problems/0/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 109 | `/problems/0/complaints/3/procedures/1/name` | `name` |  | string | PRP/자가혈 | OB-S01-05 |
| 110 | `/problems/0/complaints/3/procedures/1/category` | `category` |  | string | M5 | OB-S00-07 |
| 111 | `/problems/0/complaints/3/procedures/1/role` | `role` |  | string | 생착률 향상 |  |
| 112 | `/problems/0/complaints/3/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 113 | `/problems/0/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 114 | `/problems/0/complaints/3/procedures/1/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 115 | `/problems/0/complaints/3/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 116 | `/problems/0/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 117 | `/problems/0/complaints/3/combos/0/name` | `name` |  | string | 지방이식 + PRP |  |
| 118 | `/problems/0/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 119 | `/problems/0/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 지방이식 |  |
| 120 | `/problems/0/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05, OB-S01-05 |
| 121 | `/problems/0/complaints/3/combos/0/reason` | `reason` |  | string | 자가지방 + 성장인자 = 생착률 향상 | OB-S01-14 |
| 122 | `/problems/0/complaints/3/combos/0/evidence` | `evidence` |  | string | PRP가 지방세포 생존율 높임 |  |
| 123 | `/problems/0/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 124 | `/problems/0/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 필러가 간편한 대안 |  |
| 125 | `/problems/0/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 126 | `/problems/0/complaints/4/cc` | `cc` |  | string | 턱필러 | OB-S01-01 |
| 127 | `/problems/0/complaints/4/cc_detail` | `cc_detail` |  | string | 턱끝 연장 |  |
| 128 | `/problems/0/complaints/4/cc_group` | `cc_group` |  | string | 턱/턱선 |  |
| 129 | `/problems/0/complaints/4/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 130 | `/problems/0/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 131 | `/problems/0/complaints/4/procedures/0/name` | `name` |  | string | 필러 |  |
| 132 | `/problems/0/complaints/4/procedures/0/category` | `category` |  | string | M2 |  |
| 133 | `/problems/0/complaints/4/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 134 | `/problems/0/complaints/4/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 135 | `/problems/0/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 136 | `/problems/0/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 137 | `/problems/0/complaints/4/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 138 | `/problems/0/complaints/4/procedures/1/category` | `category` |  | string | M1 |  |
| 139 | `/problems/0/complaints/4/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 140 | `/problems/0/complaints/4/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 141 | `/problems/0/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 142 | `/problems/0/complaints/4/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 143 | `/problems/0/complaints/4/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 144 | `/problems/0/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 145 | `/problems/0/complaints/4/combos/0/name` | `name` |  | string | 필러 + 보톡스 | OB-S01-04 |
| 146 | `/problems/0/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 147 | `/problems/0/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 148 | `/problems/0/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 149 | `/problems/0/complaints/4/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 |  |
| 150 | `/problems/0/complaints/4/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 151 | `/problems/0/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 152 | `/problems/0/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 153 | `/problems/0/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 154 | `/problems/0/complaints/5/cc` | `cc` |  | string | 턱보톡스 | OB-S01-01 |
| 155 | `/problems/0/complaints/5/cc_detail` | `cc_detail` |  | string | 사각턱 축소 | OB-S01-08 |
| 156 | `/problems/0/complaints/5/cc_group` | `cc_group` |  | string | 턱/턱선 |  |
| 157 | `/problems/0/complaints/5/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 158 | `/problems/0/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 159 | `/problems/0/complaints/5/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 160 | `/problems/0/complaints/5/procedures/0/category` | `category` |  | string | M1 |  |
| 161 | `/problems/0/complaints/5/procedures/0/role` | `role` |  | string | 근육 이완 |  |
| 162 | `/problems/0/complaints/5/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 163 | `/problems/0/complaints/5/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 164 | `/problems/0/complaints/5/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 165 | `/problems/0/complaints/5/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 166 | `/problems/0/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 167 | `/problems/0/complaints/5/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 168 | `/problems/0/complaints/5/procedures/1/category` | `category` |  | string | M4 |  |
| 169 | `/problems/0/complaints/5/procedures/1/role` | `role` |  | string | 피부 재생 |  |
| 170 | `/problems/0/complaints/5/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 171 | `/problems/0/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 HB+ | OB-S01-10 |
| 172 | `/problems/0/complaints/5/procedures/1/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 173 | `/problems/0/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 174 | `/problems/0/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 175 | `/problems/0/complaints/5/combos/0/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 176 | `/problems/0/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 177 | `/problems/0/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 178 | `/problems/0/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 179 | `/problems/0/complaints/5/combos/0/reason` | `reason` |  | string | 근이완 + 피부재생 동시 개선 |  |
| 180 | `/problems/0/complaints/5/combos/0/evidence` | `evidence` |  | string | 보톡스는 동적주름 완화, 스킨부스터는 피부결·재생 개선으로 상호 보완 (근이완이 스킨부스터 흡수·효능을 높인다는 직접 임상근거는 없음) | OB-S01-07, OB-S01-08, OB-S11-02 |
| 181 | `/problems/0/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 182 | `/problems/0/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 183 | `/problems/0/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 184 | `/problems/0/complaints/6/cc` | `cc` |  | string | 턱선실리프팅 | OB-S01-01 |
| 185 | `/problems/0/complaints/6/cc_detail` | `cc_detail` |  | string | V라인 |  |
| 186 | `/problems/0/complaints/6/cc_group` | `cc_group` |  | string | 턱/턱선 |  |
| 187 | `/problems/0/complaints/6/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 188 | `/problems/0/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 189 | `/problems/0/complaints/6/procedures/0/name` | `name` |  | string | 실리프팅 |  |
| 190 | `/problems/0/complaints/6/procedures/0/category` | `category` |  | string | M7 |  |
| 191 | `/problems/0/complaints/6/procedures/0/role` | `role` |  | string | 물리적 거상 |  |
| 192 | `/problems/0/complaints/6/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 193 | `/problems/0/complaints/6/procedures/0/products/0` | `(products 원소)` | 0 | string | 민트리프트 |  |
| 194 | `/problems/0/complaints/6/procedures/0/products/1` | `(products 원소)` | 1 | string | 테스리프트 |  |
| 195 | `/problems/0/complaints/6/procedures/0/products/2` | `(products 원소)` | 2 | string | 실루엣소프트 |  |
| 196 | `/problems/0/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 197 | `/problems/0/complaints/6/procedures/1/name` | `name` |  | string | 필러 |  |
| 198 | `/problems/0/complaints/6/procedures/1/category` | `category` |  | string | M2 |  |
| 199 | `/problems/0/complaints/6/procedures/1/role` | `role` |  | string | 볼륨 보충 |  |
| 200 | `/problems/0/complaints/6/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 201 | `/problems/0/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 202 | `/problems/0/complaints/6/procedures/1/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 203 | `/problems/0/complaints/6/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 204 | `/problems/0/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 205 | `/problems/0/complaints/6/combos/0/name` | `name` |  | string | 실리프팅 + 필러 |  |
| 206 | `/problems/0/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 207 | `/problems/0/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 실리프팅 |  |
| 208 | `/problems/0/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | 필러 |  |
| 209 | `/problems/0/complaints/6/combos/0/reason` | `reason` |  | string | 거상 + 볼륨 = 입체적 리프팅 |  |
| 210 | `/problems/0/complaints/6/combos/0/evidence` | `evidence` |  | string | 실이 당기고 필러가 채움 |  |
| 211 | `/problems/0/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 212 | `/problems/0/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 실 시술 후 2개월간 HIFU/RF 피할 것 | OB-S01-09 |
| 213 | `/problems/0/complaints/7` | `(complaints 원소)` | 7 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 214 | `/problems/0/complaints/7/cc` | `cc` |  | string | 입술필러 | OB-S01-01 |
| 215 | `/problems/0/complaints/7/cc_detail` | `cc_detail` |  | string | 볼륨/모양 | OB-S01-02 |
| 216 | `/problems/0/complaints/7/cc_group` | `cc_group` |  | string | 입술 |  |
| 217 | `/problems/0/complaints/7/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 218 | `/problems/0/complaints/7/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 219 | `/problems/0/complaints/7/procedures/0/name` | `name` |  | string | 필러 |  |
| 220 | `/problems/0/complaints/7/procedures/0/category` | `category` |  | string | M2 |  |
| 221 | `/problems/0/complaints/7/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 222 | `/problems/0/complaints/7/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 223 | `/problems/0/complaints/7/procedures/0/products/0` | `(products 원소)` | 0 | string | 레스틸렌 |  |
| 224 | `/problems/0/complaints/7/procedures/0/products/1` | `(products 원소)` | 1 | string | 쥬비덤 |  |
| 225 | `/problems/0/complaints/7/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 226 | `/problems/0/complaints/7/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 227 | `/problems/0/complaints/7/procedures/1/category` | `category` |  | string | M1 |  |
| 228 | `/problems/0/complaints/7/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 229 | `/problems/0/complaints/7/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 230 | `/problems/0/complaints/7/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 231 | `/problems/0/complaints/7/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 232 | `/problems/0/complaints/7/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 233 | `/problems/0/complaints/7/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 234 | `/problems/0/complaints/7/combos/0/name` | `name` |  | string | 필러 + 보톡스 | OB-S01-04 |
| 235 | `/problems/0/complaints/7/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 236 | `/problems/0/complaints/7/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 237 | `/problems/0/complaints/7/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 238 | `/problems/0/complaints/7/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 |  |
| 239 | `/problems/0/complaints/7/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 240 | `/problems/0/complaints/7/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 241 | `/problems/0/complaints/7/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 242 | `/problems/0/complaints/8` | `(complaints 원소)` | 8 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 243 | `/problems/0/complaints/8/cc` | `cc` |  | string | 애교필러 | OB-S01-01 |
| 244 | `/problems/0/complaints/8/cc_detail` | `cc_detail` |  | string | 눈밑 볼륨 | OB-S01-13 |
| 245 | `/problems/0/complaints/8/cc_group` | `cc_group` |  | string | 눈가 |  |
| 246 | `/problems/0/complaints/8/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 247 | `/problems/0/complaints/8/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 248 | `/problems/0/complaints/8/procedures/0/name` | `name` |  | string | 필러 |  |
| 249 | `/problems/0/complaints/8/procedures/0/category` | `category` |  | string | M2 |  |
| 250 | `/problems/0/complaints/8/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 251 | `/problems/0/complaints/8/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 252 | `/problems/0/complaints/8/procedures/0/products/0` | `(products 원소)` | 0 | string | 레스틸렌 |  |
| 253 | `/problems/0/complaints/8/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 254 | `/problems/0/complaints/8/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 255 | `/problems/0/complaints/8/procedures/1/category` | `category` |  | string | M1 |  |
| 256 | `/problems/0/complaints/8/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 257 | `/problems/0/complaints/8/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 258 | `/problems/0/complaints/8/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 259 | `/problems/0/complaints/8/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 260 | `/problems/0/complaints/8/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 261 | `/problems/0/complaints/8/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 262 | `/problems/0/complaints/8/combos/0/name` | `name` |  | string | 필러 + 보톡스 | OB-S01-04 |
| 263 | `/problems/0/complaints/8/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 264 | `/problems/0/complaints/8/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 265 | `/problems/0/complaints/8/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 266 | `/problems/0/complaints/8/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 |  |
| 267 | `/problems/0/complaints/8/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 268 | `/problems/0/complaints/8/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 269 | `/problems/0/complaints/8/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 270 | `/problems/0/complaints/9` | `(complaints 원소)` | 9 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 271 | `/problems/0/complaints/9/cc` | `cc` |  | string | 눈가보톡스 | OB-S01-01 |
| 272 | `/problems/0/complaints/9/cc_detail` | `cc_detail` |  | string | 까마귀발 주름 |  |
| 273 | `/problems/0/complaints/9/cc_group` | `cc_group` |  | string | 눈가 |  |
| 274 | `/problems/0/complaints/9/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 275 | `/problems/0/complaints/9/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 276 | `/problems/0/complaints/9/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 277 | `/problems/0/complaints/9/procedures/0/category` | `category` |  | string | M1 |  |
| 278 | `/problems/0/complaints/9/procedures/0/role` | `role` |  | string | 근육 이완 |  |
| 279 | `/problems/0/complaints/9/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 280 | `/problems/0/complaints/9/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 281 | `/problems/0/complaints/9/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 282 | `/problems/0/complaints/9/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 283 | `/problems/0/complaints/9/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 284 | `/problems/0/complaints/9/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 285 | `/problems/0/complaints/9/procedures/1/category` | `category` |  | string | M4 |  |
| 286 | `/problems/0/complaints/9/procedures/1/role` | `role` |  | string | 피부 재생 |  |
| 287 | `/problems/0/complaints/9/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 288 | `/problems/0/complaints/9/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 HB+ | OB-S01-10 |
| 289 | `/problems/0/complaints/9/procedures/1/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 290 | `/problems/0/complaints/9/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 291 | `/problems/0/complaints/9/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 292 | `/problems/0/complaints/9/combos/0/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 293 | `/problems/0/complaints/9/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 294 | `/problems/0/complaints/9/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 295 | `/problems/0/complaints/9/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 296 | `/problems/0/complaints/9/combos/0/reason` | `reason` |  | string | 근이완 + 피부재생 동시 개선 |  |
| 297 | `/problems/0/complaints/9/combos/0/evidence` | `evidence` |  | string | 보톡스는 동적주름 완화, 스킨부스터는 피부결·재생 개선으로 상호 보완 (근이완이 스킨부스터 흡수·효능을 높인다는 직접 임상근거는 없음) | OB-S01-07 |
| 298 | `/problems/0/complaints/9/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 299 | `/problems/0/complaints/9/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 300 | `/problems/0/complaints/10` | `(complaints 원소)` | 10 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 301 | `/problems/0/complaints/10/cc` | `cc` |  | string | 다크서클필러 | OB-S01-01 |
| 302 | `/problems/0/complaints/10/cc_detail` | `cc_detail` |  | string | 눈밑꺼짐 | OB-S01-13 |
| 303 | `/problems/0/complaints/10/cc_group` | `cc_group` |  | string | 눈가 |  |
| 304 | `/problems/0/complaints/10/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 305 | `/problems/0/complaints/10/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 306 | `/problems/0/complaints/10/procedures/0/name` | `name` |  | string | 필러 |  |
| 307 | `/problems/0/complaints/10/procedures/0/category` | `category` |  | string | M2 |  |
| 308 | `/problems/0/complaints/10/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 309 | `/problems/0/complaints/10/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 310 | `/problems/0/complaints/10/procedures/0/products/0` | `(products 원소)` | 0 | string | 레스틸렌 |  |
| 311 | `/problems/0/complaints/10/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 312 | `/problems/0/complaints/10/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 313 | `/problems/0/complaints/10/procedures/1/category` | `category` |  | string | M1 |  |
| 314 | `/problems/0/complaints/10/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 315 | `/problems/0/complaints/10/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 316 | `/problems/0/complaints/10/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 317 | `/problems/0/complaints/10/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 318 | `/problems/0/complaints/10/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 319 | `/problems/0/complaints/10/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 320 | `/problems/0/complaints/10/combos/0/name` | `name` |  | string | 필러 + 보톡스 | OB-S01-04 |
| 321 | `/problems/0/complaints/10/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 322 | `/problems/0/complaints/10/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 323 | `/problems/0/complaints/10/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 324 | `/problems/0/complaints/10/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 |  |
| 325 | `/problems/0/complaints/10/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 326 | `/problems/0/complaints/10/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 327 | `/problems/0/complaints/10/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 328 | `/problems/0/complaints/11` | `(complaints 원소)` | 11 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 329 | `/problems/0/complaints/11/cc` | `cc` |  | string | 볼필러 | OB-S01-01 |
| 330 | `/problems/0/complaints/11/cc_detail` | `cc_detail` |  | string | 볼륨 회복 |  |
| 331 | `/problems/0/complaints/11/cc_group` | `cc_group` |  | string | 볼/광대 |  |
| 332 | `/problems/0/complaints/11/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 333 | `/problems/0/complaints/11/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 334 | `/problems/0/complaints/11/procedures/0/name` | `name` |  | string | 필러 |  |
| 335 | `/problems/0/complaints/11/procedures/0/category` | `category` |  | string | M2 |  |
| 336 | `/problems/0/complaints/11/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 337 | `/problems/0/complaints/11/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 338 | `/problems/0/complaints/11/procedures/0/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 339 | `/problems/0/complaints/11/procedures/0/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 340 | `/problems/0/complaints/11/procedures/0/products/2` | `(products 원소)` | 2 | string | 이브아르 |  |
| 341 | `/problems/0/complaints/11/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 342 | `/problems/0/complaints/11/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 343 | `/problems/0/complaints/11/procedures/1/category` | `category` |  | string | M1 |  |
| 344 | `/problems/0/complaints/11/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 345 | `/problems/0/complaints/11/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 346 | `/problems/0/complaints/11/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 347 | `/problems/0/complaints/11/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 348 | `/problems/0/complaints/11/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 349 | `/problems/0/complaints/11/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 350 | `/problems/0/complaints/11/combos/0/name` | `name` |  | string | 필러 + 보톡스 | OB-S01-04 |
| 351 | `/problems/0/complaints/11/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 352 | `/problems/0/complaints/11/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 353 | `/problems/0/complaints/11/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 354 | `/problems/0/complaints/11/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 |  |
| 355 | `/problems/0/complaints/11/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 356 | `/problems/0/complaints/11/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 357 | `/problems/0/complaints/11/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 358 | `/problems/0/complaints/12` | `(complaints 원소)` | 12 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 359 | `/problems/0/complaints/12/cc` | `cc` |  | string | 볼지방이식 | OB-S01-01 |
| 360 | `/problems/0/complaints/12/cc_detail` | `cc_detail` |  | string | 자가지방 |  |
| 361 | `/problems/0/complaints/12/cc_group` | `cc_group` |  | string | 볼/광대 |  |
| 362 | `/problems/0/complaints/12/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 363 | `/problems/0/complaints/12/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 364 | `/problems/0/complaints/12/procedures/0/name` | `name` |  | string | 지방이식 |  |
| 365 | `/problems/0/complaints/12/procedures/0/category` | `category` |  | string | M6 |  |
| 366 | `/problems/0/complaints/12/procedures/0/role` | `role` |  | string | 자가지방 이식 |  |
| 367 | `/problems/0/complaints/12/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) | OB-S01-12 |
| 368 | `/problems/0/complaints/12/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 369 | `/problems/0/complaints/12/procedures/1/name` | `name` |  | string | PRP/자가혈 | OB-S01-05 |
| 370 | `/problems/0/complaints/12/procedures/1/category` | `category` |  | string | M5 |  |
| 371 | `/problems/0/complaints/12/procedures/1/role` | `role` |  | string | 생착률 향상 |  |
| 372 | `/problems/0/complaints/12/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 373 | `/problems/0/complaints/12/procedures/1/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 374 | `/problems/0/complaints/12/procedures/1/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 375 | `/problems/0/complaints/12/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 376 | `/problems/0/complaints/12/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 377 | `/problems/0/complaints/12/combos/0/name` | `name` |  | string | 지방이식 + PRP |  |
| 378 | `/problems/0/complaints/12/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 379 | `/problems/0/complaints/12/combos/0/combo/0` | `(combo 원소)` | 0 | string | 지방이식 |  |
| 380 | `/problems/0/complaints/12/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05, OB-S01-05 |
| 381 | `/problems/0/complaints/12/combos/0/reason` | `reason` |  | string | 자가지방 + 성장인자 = 생착률 향상 |  |
| 382 | `/problems/0/complaints/12/combos/0/evidence` | `evidence` |  | string | PRP가 지방세포 생존율 높임 |  |
| 383 | `/problems/0/complaints/12/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 384 | `/problems/0/complaints/12/alternatives/0` | `(alternatives 원소)` | 0 | string | 필러가 간편한 대안 |  |
| 385 | `/problems/0/complaints/13` | `(complaints 원소)` | 13 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 386 | `/problems/0/complaints/13/cc` | `cc` |  | string | 눈썹반영구 | OB-S01-01 |
| 387 | `/problems/0/complaints/13/cc_detail` | `cc_detail` |  | string | 엠보/콤보/파우더 | OB-S01-02 |
| 388 | `/problems/0/complaints/13/cc_group` | `cc_group` |  | string | 반영구화장 | OB-S01-03 |
| 389 | `/problems/0/complaints/13/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 390 | `/problems/0/complaints/13/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 391 | `/problems/0/complaints/13/procedures/0/name` | `name` |  | string | 반영구화장 |  |
| 392 | `/problems/0/complaints/13/procedures/0/category` | `category` |  | string | M15 | OB-S00-07, OB-S06-08 |
| 393 | `/problems/0/complaints/13/procedures/0/role` | `role` |  | string | 반영구 색소 시술 |  |
| 394 | `/problems/0/complaints/13/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) | OB-S01-12 |
| 395 | `/problems/0/complaints/13/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 396 | `/problems/0/complaints/13/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 397 | `/problems/0/complaints/13/combos/0/name` | `name` |  | string | 반영구 단독 | OB-S01-06 |
| 398 | `/problems/0/complaints/13/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 399 | `/problems/0/complaints/13/combos/0/combo/0` | `(combo 원소)` | 0 | string | 반영구화장 | OB-S01-06 |
| 400 | `/problems/0/complaints/13/combos/0/reason` | `reason` |  | string | 단독 시술 |  |
| 401 | `/problems/0/complaints/13/combos/0/evidence` | `evidence` |  | string | 전문 시술자 필요 |  |
| 402 | `/problems/0/complaints/13/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 403 | `/problems/0/complaints/13/alternatives/0` | `(alternatives 원소)` | 0 | string | 터치업 3-6개월 후 |  |
| 404 | `/problems/0/complaints/14` | `(complaints 원소)` | 14 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 405 | `/problems/0/complaints/14/cc` | `cc` |  | string | 아이라인반영구 | OB-S01-01 |
| 406 | `/problems/0/complaints/14/cc_detail` | `cc_detail` |  | string | 상/하 | OB-S01-02 |
| 407 | `/problems/0/complaints/14/cc_group` | `cc_group` |  | string | 반영구화장 | OB-S01-03 |
| 408 | `/problems/0/complaints/14/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 409 | `/problems/0/complaints/14/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 410 | `/problems/0/complaints/14/procedures/0/name` | `name` |  | string | 반영구화장 |  |
| 411 | `/problems/0/complaints/14/procedures/0/category` | `category` |  | string | M15 |  |
| 412 | `/problems/0/complaints/14/procedures/0/role` | `role` |  | string | 반영구 색소 시술 |  |
| 413 | `/problems/0/complaints/14/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) | OB-S01-12 |
| 414 | `/problems/0/complaints/14/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 415 | `/problems/0/complaints/14/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 416 | `/problems/0/complaints/14/combos/0/name` | `name` |  | string | 반영구 단독 | OB-S01-06 |
| 417 | `/problems/0/complaints/14/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 418 | `/problems/0/complaints/14/combos/0/combo/0` | `(combo 원소)` | 0 | string | 반영구화장 |  |
| 419 | `/problems/0/complaints/14/combos/0/reason` | `reason` |  | string | 단독 시술 |  |
| 420 | `/problems/0/complaints/14/combos/0/evidence` | `evidence` |  | string | 전문 시술자 필요 |  |
| 421 | `/problems/0/complaints/14/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 422 | `/problems/0/complaints/14/alternatives/0` | `(alternatives 원소)` | 0 | string | 터치업 3-6개월 후 |  |
| 423 | `/problems/0/complaints/15` | `(complaints 원소)` | 15 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 424 | `/problems/0/complaints/15/cc` | `cc` |  | string | 입술반영구 | OB-S01-01 |
| 425 | `/problems/0/complaints/15/cc_detail` | `cc_detail` |  | string | 틴트/풀립 | OB-S01-02 |
| 426 | `/problems/0/complaints/15/cc_group` | `cc_group` |  | string | 반영구화장 | OB-S01-03 |
| 427 | `/problems/0/complaints/15/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 428 | `/problems/0/complaints/15/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 429 | `/problems/0/complaints/15/procedures/0/name` | `name` |  | string | 반영구화장 |  |
| 430 | `/problems/0/complaints/15/procedures/0/category` | `category` |  | string | M15 |  |
| 431 | `/problems/0/complaints/15/procedures/0/role` | `role` |  | string | 반영구 색소 시술 |  |
| 432 | `/problems/0/complaints/15/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) | OB-S01-12 |
| 433 | `/problems/0/complaints/15/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 434 | `/problems/0/complaints/15/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 435 | `/problems/0/complaints/15/combos/0/name` | `name` |  | string | 반영구 단독 | OB-S01-06 |
| 436 | `/problems/0/complaints/15/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 437 | `/problems/0/complaints/15/combos/0/combo/0` | `(combo 원소)` | 0 | string | 반영구화장 |  |
| 438 | `/problems/0/complaints/15/combos/0/reason` | `reason` |  | string | 단독 시술 |  |
| 439 | `/problems/0/complaints/15/combos/0/evidence` | `evidence` |  | string | 전문 시술자 필요 |  |
| 440 | `/problems/0/complaints/15/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 441 | `/problems/0/complaints/15/alternatives/0` | `(alternatives 원소)` | 0 | string | 터치업 3-6개월 후 |  |
| 442 | `/problems/0/complaints/16` | `(complaints 원소)` | 16 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 443 | `/problems/0/complaints/16/cc` | `cc` |  | string | 헤어라인반영구 | OB-S01-01 |
| 444 | `/problems/0/complaints/16/cc_detail` | `cc_detail` |  | string | SMP | OB-S01-11 |
| 445 | `/problems/0/complaints/16/cc_group` | `cc_group` |  | string | 반영구화장 | OB-S01-03 |
| 446 | `/problems/0/complaints/16/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 447 | `/problems/0/complaints/16/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 448 | `/problems/0/complaints/16/procedures/0/name` | `name` |  | string | 반영구화장 |  |
| 449 | `/problems/0/complaints/16/procedures/0/category` | `category` |  | string | M15 |  |
| 450 | `/problems/0/complaints/16/procedures/0/role` | `role` |  | string | 반영구 색소 시술 |  |
| 451 | `/problems/0/complaints/16/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) | OB-S01-12 |
| 452 | `/problems/0/complaints/16/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 453 | `/problems/0/complaints/16/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 454 | `/problems/0/complaints/16/combos/0/name` | `name` |  | string | 반영구 단독 | OB-S01-06 |
| 455 | `/problems/0/complaints/16/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 456 | `/problems/0/complaints/16/combos/0/combo/0` | `(combo 원소)` | 0 | string | 반영구화장 |  |
| 457 | `/problems/0/complaints/16/combos/0/reason` | `reason` |  | string | 단독 시술 |  |
| 458 | `/problems/0/complaints/16/combos/0/evidence` | `evidence` |  | string | 전문 시술자 필요 |  |
| 459 | `/problems/0/complaints/16/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 460 | `/problems/0/complaints/16/alternatives/0` | `(alternatives 원소)` | 0 | string | 터치업 3-6개월 후 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S01-01 | P | `/problems/0/complaints/0/cc`<br>`/problems/0/complaints/1/cc`<br>`/problems/0/complaints/2/cc`<br>`/problems/0/complaints/3/cc`<br>`/problems/0/complaints/4/cc`<br>`/problems/0/complaints/5/cc`<br>`/problems/0/complaints/6/cc`<br>`/problems/0/complaints/7/cc`<br>`/problems/0/complaints/8/cc`<br>`/problems/0/complaints/9/cc`<br>`/problems/0/complaints/10/cc`<br>`/problems/0/complaints/11/cc`<br>`/problems/0/complaints/12/cc`<br>`/problems/0/complaints/13/cc`<br>`/problems/0/complaints/14/cc`<br>`/problems/0/complaints/15/cc`<br>`/problems/0/complaints/16/cc` | cc 값은 부위 표현과 시술 표현이 띄어쓰기 없이 붙은 형태가 대부분이다(코필러·턱보톡스·이마지방이식·눈썹반영구 등). '다크서클필러' 는 부위가 아니라 증상 표현(다크서클)+시술 표현이다. 경계 분리는 형태소 결과와 대조(K-02). |
| OB-S01-02 | P | `/problems/0/complaints/0/cc_detail`<br>`/problems/0/complaints/2/cc_detail`<br>`/problems/0/complaints/7/cc_detail`<br>`/problems/0/complaints/13/cc_detail`<br>`/problems/0/complaints/14/cc_detail`<br>`/problems/0/complaints/15/cc_detail` | cc_detail 의 '/' 가 '콧대/코끝'(부위 둘), '볼륨/라운딩'·'볼륨/모양'(목표 둘), '엠보/콤보/파우더'(기법 셋), '상/하'(위치 둘), '틴트/풀립'(형태 둘) 로 쓰였다. README 의 '/ = 둘 중 하나' 규칙이 cc_detail 에 적용되는지(대안인지 병렬 나열인지)는 원문만으로 정해지지 않는다(F-02). |
| OB-S01-03 | P | `/problems/0/complaints/13/cc_group`<br>`/problems/0/complaints/14/cc_group`<br>`/problems/0/complaints/15/cc_group`<br>`/problems/0/complaints/16/cc_group` | cc_group 은 c0~c12 에서 부위 표현(코·이마/관자놀이·턱/턱선·입술·눈가·볼/광대)이지만 c13~c16 은 '반영구화장' 으로 시술 표현이다. 같은 필드에 정보 종류가 섞여 있다(F-03). |
| OB-S01-04 | P | `/problems/0/complaints/0/combos/0/name`<br>`/problems/0/complaints/2/combos/0/name`<br>`/problems/0/complaints/4/combos/0/name`<br>`/problems/0/complaints/7/combos/0/name`<br>`/problems/0/complaints/8/combos/0/name`<br>`/problems/0/complaints/10/combos/0/name`<br>`/problems/0/complaints/11/combos/0/name` | '필러 + 보톡스' combo 블록(name·combo·reason·evidence)과 alternatives '바이오스티뮬레이터로 장기 관리' 가 7개 complaint 에서 글자 그대로 반복된다. products 만 complaint 마다 다르다. description 의 '자동 생성' 과 맞는 템플릿 반복으로 보이며, 부위별 차이가 원문에 없다(B-02). |
| OB-S01-05 | I | `/problems/0/complaints/3/procedures/1/name`<br>`/problems/0/complaints/3/combos/0/combo/1`<br>`/problems/0/complaints/12/procedures/1/name`<br>`/problems/0/complaints/12/combos/0/combo/1` | procedures 의 name 은 'PRP/자가혈' 인데 같은 complaint 의 combos.combo 원소는 'PRP' 이고 combo name 도 '지방이식 + PRP'. 같은 시술을 가리키는지 원문에 연결 근거가 없다(I-01). |
| OB-S01-06 | I | `/problems/0/complaints/13/combos/0/name`<br>`/problems/0/complaints/13/combos/0/combo/0`<br>`/problems/0/complaints/14/combos/0/name`<br>`/problems/0/complaints/15/combos/0/name`<br>`/problems/0/complaints/16/combos/0/name` | combo name '반영구 단독' 과 combo 원소 '반영구화장' 표기가 다르다. combo 원소가 1개뿐인 '단독' 묶음이다(I-02). |
| OB-S01-07 | P | `/problems/0/complaints/5/combos/0/evidence`<br>`/problems/0/complaints/9/combos/0/evidence` | evidence 에 괄호로 부정 단서 '(근이완이 스킨부스터 흡수·효능을 높인다는 직접 임상근거는 없음)' 가 붙는다. reason '근이완 + 피부재생 동시 개선' 의 근거를 스스로 제한한다. 부정이 괄호 안에 있어 절 분할 시 떨어지지 않도록 전체 값을 보존한다. |
| OB-S01-08 | P | `/problems/0/complaints/5/combos/0/evidence`<br>`/problems/0/complaints/5/cc_detail` | c5 턱보톡스(cc_detail '사각턱 축소')의 evidence 는 '보톡스는 동적주름 완화' 로 눈가보톡스 c9 와 글자 그대로 같다. 사각턱 축소와 동적주름 완화의 대응은 원문에 설명이 없다(B-02 템플릿 반복의 사례). |
| OB-S01-09 | P | `/problems/0/complaints/1/alternatives/0`<br>`/problems/0/complaints/6/alternatives/0` | alternatives 칸에 대안 시술이 아니라 시간 조건이 붙은 금지 지시('실 시술 후 2개월간 HIFU/RF 피할 것')가 들어 있다. alternatives 의 정보 종류가 값마다 다르다: 대안(c3 '필러가 간편한 대안'), 장기 관리 제안(c0), 조건부 추가(c5 '효과 부족 시 리프팅기기 추가'), 일정(c13 '터치업 3-6개월 후') (F-04). |
| OB-S01-10 | K | `/problems/0/complaints/5/procedures/1/products/0`<br>`/problems/0/complaints/9/procedures/1/products/0` | 제품 표기 '리쥬란 HB+' 는 이름 안에 '+' 를 포함한다. README 의 '+ = 함께' 기호 규칙과 글자가 겹친다. 이 원장에서는 products 배열 원소 하나의 값이므로 구조상 단일 값이다(K-03). |
| OB-S01-11 | B | `/problems/0/complaints/16/cc_detail` | cc_detail 'SMP' 는 약어이며 원문에 풀이가 없다(B-03). 풀어 쓰지 않는다. |
| OB-S01-12 | P | `/problems/0/complaints/3/procedures/0/products`<br>`/problems/0/complaints/12/procedures/0/products`<br>`/problems/0/complaints/13/procedures/0/products`<br>`/problems/0/complaints/14/procedures/0/products`<br>`/problems/0/complaints/15/procedures/0/products`<br>`/problems/0/complaints/16/procedures/0/products` | 지방이식·반영구화장 procedures 는 products 가 빈 배열이다. 제품이 없다는 뜻인지 미기재인지 원문만으로 구분할 수 없다(B-04). |
| OB-S01-13 | P | `/problems/0/complaints/8/cc_detail`<br>`/problems/0/complaints/10/cc_detail` | '눈밑 볼륨'(띄어 씀) 과 '눈밑꺼짐'(붙여 씀) — 같은 '눈밑' 부위 표현이 띄어쓰기만 다르게 나온다. 형태소 결과에서 '눈밑꺼짐' 분절 확인(K-02). |
| OB-S01-14 | P | `/problems/0/complaints/0/combos/0/reason`<br>`/problems/0/complaints/1/combos/0/reason`<br>`/problems/0/complaints/3/combos/0/reason` | reason 은 'A + B = C' 공식형 문장('볼륨 + 근이완 = 시너지', '거상 + 볼륨 = 입체적 리프팅', '자가지방 + 성장인자 = 생착률 향상'). '+' 는 combo 의 두 시술이 내는 작용을, '=' 는 결과를 잇는 것으로 보이나 기호 의미는 원문에 정의돼 있지 않다(F-02). |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 콧대/코끝 | `/problems/0/complaints/0/cc_detail` [0,5) | 부위 표현, 기호(/) |
| 볼륨/라운딩 | `/problems/0/complaints/2/cc_detail` [0,6) | 기호(/), 목표·효과 표현 |
| 볼륨/모양 | `/problems/0/complaints/7/cc_detail` [0,5) | 기호(/), 목표·효과 표현 |
| 코끝 거상 | `/problems/0/complaints/1/cc_detail` [0,5) | 부위 표현, 목표·효과 표현 |
| 턱끝 연장 | `/problems/0/complaints/4/cc_detail` [0,5) | 부위 표현, 목표·효과 표현 |
| 사각턱 축소 | `/problems/0/complaints/5/cc_detail` [0,6) | 부위 표현, 목표·효과 표현 |
| 눈밑 볼륨 | `/problems/0/complaints/8/cc_detail` [0,5) | 부위 표현, 목표·효과 표현 |
| 까마귀발 주름 | `/problems/0/complaints/9/cc_detail` [0,7) | 부위 표현, 증상 표현, 비유 표현 |
| 눈밑꺼짐 | `/problems/0/complaints/10/cc_detail` [0,4) | 부위 표현, 증상 표현, 붙여 쓴 복합어 |
| 볼륨 회복 | `/problems/0/complaints/11/cc_detail` [0,5) | 목표·효과 표현 |
| 엠보/콤보/파우더 | `/problems/0/complaints/13/cc_detail` [0,9) | 기호(/), 기법 나열 |
| 상/하 | `/problems/0/complaints/14/cc_detail` [0,3) | 기호(/), 위치 표현 |
| 틴트/풀립 | `/problems/0/complaints/15/cc_detail` [0,5) | 기호(/), 형태 나열 |
| SMP | `/problems/0/complaints/16/cc_detail` [0,3) | 약어(원문 풀이 없음) |
| 이마/관자놀이 | `/problems/0/complaints/2/cc_group` [0,7)<br>`/problems/0/complaints/3/cc_group` [0,7) | 부위 표현, 기호(/) |
| 턱/턱선 | `/problems/0/complaints/4/cc_group` [0,4)<br>`/problems/0/complaints/5/cc_group` [0,4)<br>`/problems/0/complaints/6/cc_group` [0,4) | 부위 표현, 기호(/) |
| 볼/광대 | `/problems/0/complaints/11/cc_group` [0,4)<br>`/problems/0/complaints/12/cc_group` [0,4) | 부위 표현, 기호(/) |
| 다크서클필러 | `/problems/0/complaints/10/cc` [0,6) | 증상 표현+시술명 표현, 붙여 쓴 복합어 |
| 헤어라인반영구 | `/problems/0/complaints/16/cc` [0,7) | 부위 표현+시술명 표현, 붙여 쓴 복합어 |
| 턱선실리프팅 | `/problems/0/complaints/6/cc` [0,6) | 부위 표현+시술명 표현, 붙여 쓴 복합어 |
| PRP/자가혈 | `/problems/0/complaints/3/procedures/1/name` [0,7)<br>`/problems/0/complaints/12/procedures/1/name` [0,7) | 시술명 표현, 기호(/), 약어+한글 병기 |
| 리쥬란 HB+ | `/problems/0/complaints/5/procedures/1/products/0` [0,7)<br>`/problems/0/complaints/9/procedures/1/products/0` [0,7) | 제품명 표현, 이름 안의 기호(+) |
| 리젠ACR | `/problems/0/complaints/3/procedures/1/products/1` [0,5)<br>`/problems/0/complaints/12/procedures/1/products/1` [0,5) | 제품명 표현, 혼합 표기(한글+로마자) |
| 볼륨 + 근이완 = 시너지 | `/problems/0/complaints/0/combos/0/reason` [0,14)<br>`/problems/0/complaints/2/combos/0/reason` [0,14)<br>`/problems/0/complaints/4/combos/0/reason` [0,14)<br>`/problems/0/complaints/7/combos/0/reason` [0,14)<br>`/problems/0/complaints/8/combos/0/reason` [0,14)<br>`/problems/0/complaints/10/combos/0/reason` [0,14)<br>`/problems/0/complaints/11/combos/0/reason` [0,14) | 공식형 문장, 기호(+), 기호(=) |
| 보톡스가 근육 움직임 줄여 필러 유지력 향상 | `/problems/0/complaints/0/combos/0/evidence` [0,24)<br>`/problems/0/complaints/2/combos/0/evidence` [0,24)<br>`/problems/0/complaints/4/combos/0/evidence` [0,24)<br>`/problems/0/complaints/7/combos/0/evidence` [0,24)<br>`/problems/0/complaints/8/combos/0/evidence` [0,24)<br>`/problems/0/complaints/10/combos/0/evidence` [0,24)<br>`/problems/0/complaints/11/combos/0/evidence` [0,24) | 인과·기전 진술, 시술명 표현 |
| 근육 움직임 줄여 | `/problems/0/complaints/0/combos/0/evidence` [5,14)<br>`/problems/0/complaints/2/combos/0/evidence` [5,14)<br>`/problems/0/complaints/4/combos/0/evidence` [5,14)<br>`/problems/0/complaints/7/combos/0/evidence` [5,14)<br>`/problems/0/complaints/8/combos/0/evidence` [5,14)<br>`/problems/0/complaints/10/combos/0/evidence` [5,14)<br>`/problems/0/complaints/11/combos/0/evidence` [5,14) | 감소 표현, 기전 표현 |
| 필러 유지력 향상 | `/problems/0/complaints/0/combos/0/evidence` [15,24)<br>`/problems/0/complaints/2/combos/0/evidence` [15,24)<br>`/problems/0/complaints/4/combos/0/evidence` [15,24)<br>`/problems/0/complaints/7/combos/0/evidence` [15,24)<br>`/problems/0/complaints/8/combos/0/evidence` [15,24)<br>`/problems/0/complaints/10/combos/0/evidence` [15,24)<br>`/problems/0/complaints/11/combos/0/evidence` [15,24) | 증가 표현, 효과 표현 |
| 거상 + 볼륨 = 입체적 리프팅 | `/problems/0/complaints/1/combos/0/reason` [0,17)<br>`/problems/0/complaints/6/combos/0/reason` [0,17) | 공식형 문장, 기호(+), 기호(=) |
| 실이 당기고 필러가 채움 | `/problems/0/complaints/1/combos/0/evidence` [0,13)<br>`/problems/0/complaints/6/combos/0/evidence` [0,13) | 기전 진술, 병렬(-고) |
| 자가지방 + 성장인자 = 생착률 향상 | `/problems/0/complaints/3/combos/0/reason` [0,20)<br>`/problems/0/complaints/12/combos/0/reason` [0,20) | 공식형 문장, 기호(+), 기호(=), 증가 표현 |
| PRP가 지방세포 생존율 높임 | `/problems/0/complaints/3/combos/0/evidence` [0,16)<br>`/problems/0/complaints/12/combos/0/evidence` [0,16) | 기전 진술, 증가 표현 |
| 근이완 + 피부재생 동시 개선 | `/problems/0/complaints/5/combos/0/reason` [0,16)<br>`/problems/0/complaints/9/combos/0/reason` [0,16) | 기호(+), 동시성(동시), 효과 표현 |
| 보톡스는 동적주름 완화, 스킨부스터는 피부결·재생 개선으로 상호 보완 | `/problems/0/complaints/5/combos/0/evidence` [0,38)<br>`/problems/0/complaints/9/combos/0/evidence` [0,38) | 대조 병렬(-는 ... -는), 기호(·), 효과 표현 |
| (근이완이 스킨부스터 흡수·효능을 높인다는 직접 임상근거는 없음) | `/problems/0/complaints/5/combos/0/evidence` [39,75)<br>`/problems/0/complaints/9/combos/0/evidence` [39,75) | 부정(없음), 근거 한정, 괄호 보충 |
| 직접 임상근거는 없음 | `/problems/0/complaints/5/combos/0/evidence` [63,74)<br>`/problems/0/complaints/9/combos/0/evidence` [63,74) | 부정(없음), 근거 수준 표현 |
| 단독 시술 | `/problems/0/complaints/13/combos/0/reason` [0,5)<br>`/problems/0/complaints/14/combos/0/reason` [0,5)<br>`/problems/0/complaints/15/combos/0/reason` [0,5)<br>`/problems/0/complaints/16/combos/0/reason` [0,5) | 단독(조합 없음) |
| 반영구 단독 | `/problems/0/complaints/13/combos/0/name` [0,6)<br>`/problems/0/complaints/14/combos/0/name` [0,6)<br>`/problems/0/complaints/15/combos/0/name` [0,6)<br>`/problems/0/complaints/16/combos/0/name` [0,6) | 단독(조합 없음), 축약 표기 |
| 전문 시술자 필요 | `/problems/0/complaints/13/combos/0/evidence` [0,9)<br>`/problems/0/complaints/14/combos/0/evidence` [0,9)<br>`/problems/0/complaints/15/combos/0/evidence` [0,9)<br>`/problems/0/complaints/16/combos/0/evidence` [0,9) | 필요·요건 표현, 시술자 조건 |
| 바이오스티뮬레이터로 장기 관리 | `/problems/0/complaints/0/alternatives/0` [0,16)<br>`/problems/0/complaints/2/alternatives/0` [0,16)<br>`/problems/0/complaints/4/alternatives/0` [0,16)<br>`/problems/0/complaints/7/alternatives/0` [0,16)<br>`/problems/0/complaints/8/alternatives/0` [0,16)<br>`/problems/0/complaints/10/alternatives/0` [0,16)<br>`/problems/0/complaints/11/alternatives/0` [0,16) | 시술명 표현, 기간 표현(장기) |
| 실 시술 후 2개월간 HIFU/RF 피할 것 | `/problems/0/complaints/1/alternatives/0` [0,24)<br>`/problems/0/complaints/6/alternatives/0` [0,24) | 시간 조건(후·기간), 금지·회피(피할 것), 기호(/), 약어 |
| 2개월간 | `/problems/0/complaints/1/alternatives/0` [7,11)<br>`/problems/0/complaints/6/alternatives/0` [7,11) | 수량·단위·시간 |
| HIFU/RF | `/problems/0/complaints/1/alternatives/0` [12,19)<br>`/problems/0/complaints/6/alternatives/0` [12,19) | 시술명 표현, 기호(/), 약어 |
| 필러가 간편한 대안 | `/problems/0/complaints/3/alternatives/0` [0,10)<br>`/problems/0/complaints/12/alternatives/0` [0,10) | 대안 표현, 비교(간편한) |
| 효과 부족 시 리프팅기기 추가 | `/problems/0/complaints/5/alternatives/0` [0,16)<br>`/problems/0/complaints/9/alternatives/0` [0,16) | 조건(-시), 부족 표현, 추가 표현 |
| 터치업 3-6개월 후 | `/problems/0/complaints/13/alternatives/0` [0,11)<br>`/problems/0/complaints/14/alternatives/0` [0,11)<br>`/problems/0/complaints/15/alternatives/0` [0,11)<br>`/problems/0/complaints/16/alternatives/0` [0,11) | 범위(-), 수량·단위·시간, 시간 순서(후) |
| 3-6개월 | `/problems/0/complaints/13/alternatives/0` [4,9)<br>`/problems/0/complaints/14/alternatives/0` [4,9)<br>`/problems/0/complaints/15/alternatives/0` [4,9)<br>`/problems/0/complaints/16/alternatives/0` [4,9) | 범위(-), 수량·단위·시간 |
| 반영구 색소 시술 | `/problems/0/complaints/13/procedures/0/role` [0,9)<br>`/problems/0/complaints/14/procedures/0/role` [0,9)<br>`/problems/0/complaints/15/procedures/0/role` [0,9)<br>`/problems/0/complaints/16/procedures/0/role` [0,9) | role 표현, 시술명 표현 |
| 근이완 보조 | `/problems/0/complaints/0/procedures/1/role` [0,6)<br>`/problems/0/complaints/2/procedures/1/role` [0,6)<br>`/problems/0/complaints/4/procedures/1/role` [0,6)<br>`/problems/0/complaints/7/procedures/1/role` [0,6)<br>`/problems/0/complaints/8/procedures/1/role` [0,6)<br>`/problems/0/complaints/10/procedures/1/role` [0,6)<br>`/problems/0/complaints/11/procedures/1/role` [0,6) | role 표현, 보조(주/부 구분) |
| 물리적 거상 | `/problems/0/complaints/1/procedures/0/role` [0,6)<br>`/problems/0/complaints/6/procedures/0/role` [0,6) | role 표현, 기전 수식(물리적) |
| 생착률 향상 | `/problems/0/complaints/3/procedures/1/role` [0,6)<br>`/problems/0/complaints/12/procedures/1/role` [0,6) | role 표현, 증가 표현 |

## 이 구획에서 연 미결

- **I-01** (I) procedures.name 'PRP/자가혈' ↔ 같은 complaint 의 combos.combo 'PRP' 표기 불일치(다른 구획에도 반복될 수 있음 — 구획별 관찰 참조). — 영향: combo 원소를 procedures 항목에 이름으로 잇는 후속 작업에서 문자열 일치가 깨진다. 원본 변경 제안은 후속 확인 후보.
- **I-02** (I) combo name 이 combo 원소 이름과 다르게 축약된 경우('반영구 단독' ↔ '반영구화장'). — 영향: combo name 을 combo 원소의 조합 표기로 간주할 수 없는 사례.
- **B-02** (B) 같은 combo 블록·alternatives 문장이 부위·세부(cc_detail)가 다른 complaint 들에 글자 그대로 반복된다. 부위별 차이 정보가 원문에 없다. — 영향: complaint 단위 근거·대안을 부위별로 구분해 쓸 수 없다. 반복을 개별 사실로 셀지 템플릿으로 셀지는 후속 설계 과제.
- **B-03** (B) 약어 'SMP' 풀이 없음. — 영향: cc_detail 의미 확정 불가. 풀어 쓰지 않고 보존.
- **B-04** (B) products 빈 배열의 뜻(제품 없음/미기재) 원문 정보 없음. 전체 47곳. — 영향: 빈 products 를 '제품 불필요' 로 해석하면 근거 없는 의미 부여.
- **F-02** (F) 기호 '/'·'+'·'=' 의 의미가 필드마다 다르게 쓰인다(cc_detail·cc_group·procedures.name·reason·alternatives). README 규칙의 적용 범위 확인 필요. — 영향: 기호만으로 대안/병렬/결과 관계를 확정하지 않는다.
- **F-03** (F) cc_group 에 부위 표현과 시술 표현('반영구화장')이 섞여 있다. — 영향: cc_group 을 부위 축으로 바로 쓰면 오분류.
- **F-04** (F) alternatives 에 대안·조건부 추가·금지·일정·장기 관리 등 정보 종류가 섞여 있다. — 영향: alternatives 를 '대체 시술 목록' 으로 해석하면 금지 지시('피할 것')가 대안으로 뒤집힌다.
