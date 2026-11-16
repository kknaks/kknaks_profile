# S08 — /problems/7 P8 홍조/혈관

[← review.md](review.md) · 범위 /problems/7 및 /problems/7/** 전체 · 소유 노드 144 · 말단 92 · 빈 값 0 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S08.txt 로 c0~c4 전부(procedures 10·combos 5·alternatives 5) 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 1987 | `/problems/7` | `(problems 원소)` | 7 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 1988 | `/problems/7/problem_id` | `problem_id` |  | string | P8 |  |
| 1989 | `/problems/7/problem` | `problem` |  | string | 홍조/혈관 |  |
| 1990 | `/problems/7/complaints` | `complaints` |  | array[5] | (배열 · 5개) |  |
| 1991 | `/problems/7/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1992 | `/problems/7/complaints/0/cc` | `cc` |  | string | V빔 |  |
| 1993 | `/problems/7/complaints/0/cc_detail` | `cc_detail` |  | string | 595nm PDL |  |
| 1994 | `/problems/7/complaints/0/cc_group` | `cc_group` |  | string | 안면홍조 |  |
| 1995 | `/problems/7/complaints/0/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1996 | `/problems/7/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S08-01 |
| 1997 | `/problems/7/complaints/0/procedures/0/name` | `name` |  | string | 혈관레이저 |  |
| 1998 | `/problems/7/complaints/0/procedures/0/category` | `category` |  | string | M8 |  |
| 1999 | `/problems/7/complaints/0/procedures/0/role` | `role` |  | string | 혈관 수축/파괴 | OB-S08-05 |
| 2000 | `/problems/7/complaints/0/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2001 | `/problems/7/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 엑셀V |  |
| 2002 | `/problems/7/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2003 | `/problems/7/complaints/0/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2004 | `/problems/7/complaints/0/procedures/1/category` | `category` |  | string | M4 |  |
| 2005 | `/problems/7/complaints/0/procedures/1/role` | `role` |  | string | 피부 장벽 강화 | OB-S08-06 |
| 2006 | `/problems/7/complaints/0/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2007 | `/problems/7/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 2008 | `/problems/7/complaints/0/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 2009 | `/problems/7/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2010 | `/problems/7/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2011 | `/problems/7/complaints/0/combos/0/name` | `name` |  | string | 혈관레이저 + 스킨부스터 |  |
| 2012 | `/problems/7/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2013 | `/problems/7/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 혈관레이저 |  |
| 2014 | `/problems/7/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2015 | `/problems/7/complaints/0/combos/0/reason` | `reason` |  | string | 혈관 수축 + 장벽 강화 |  |
| 2016 | `/problems/7/complaints/0/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진 |  |
| 2017 | `/problems/7/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2018 | `/problems/7/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | LDM 진정 관리 병행 | OB-S08-04 |
| 2019 | `/problems/7/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2020 | `/problems/7/complaints/1/cc` | `cc` |  | string | IPL홍조 |  |
| 2021 | `/problems/7/complaints/1/cc_detail` | `cc_detail` |  | string | 광범위 |  |
| 2022 | `/problems/7/complaints/1/cc_group` | `cc_group` |  | string | 안면홍조 |  |
| 2023 | `/problems/7/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2024 | `/problems/7/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S08-01 |
| 2025 | `/problems/7/complaints/1/procedures/0/name` | `name` |  | string | 혈관레이저 |  |
| 2026 | `/problems/7/complaints/1/procedures/0/category` | `category` |  | string | M8 |  |
| 2027 | `/problems/7/complaints/1/procedures/0/role` | `role` |  | string | 혈관 수축/파괴 |  |
| 2028 | `/problems/7/complaints/1/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2029 | `/problems/7/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 엑셀V |  |
| 2030 | `/problems/7/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2031 | `/problems/7/complaints/1/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2032 | `/problems/7/complaints/1/procedures/1/category` | `category` |  | string | M4 |  |
| 2033 | `/problems/7/complaints/1/procedures/1/role` | `role` |  | string | 피부 장벽 강화 |  |
| 2034 | `/problems/7/complaints/1/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2035 | `/problems/7/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 2036 | `/problems/7/complaints/1/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 2037 | `/problems/7/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2038 | `/problems/7/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2039 | `/problems/7/complaints/1/combos/0/name` | `name` |  | string | 혈관레이저 + 스킨부스터 |  |
| 2040 | `/problems/7/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2041 | `/problems/7/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 혈관레이저 |  |
| 2042 | `/problems/7/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2043 | `/problems/7/complaints/1/combos/0/reason` | `reason` |  | string | 혈관 수축 + 장벽 강화 |  |
| 2044 | `/problems/7/complaints/1/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진 |  |
| 2045 | `/problems/7/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2046 | `/problems/7/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | LDM 진정 관리 병행 | OB-S08-04 |
| 2047 | `/problems/7/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2048 | `/problems/7/complaints/2/cc` | `cc` |  | string | 리쥬란+LDM | OB-S08-03 |
| 2049 | `/problems/7/complaints/2/cc_detail` | `cc_detail` |  | string | 장벽강화+재생 | OB-S08-03 |
| 2050 | `/problems/7/complaints/2/cc_group` | `cc_group` |  | string | 안면홍조 |  |
| 2051 | `/problems/7/complaints/2/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2052 | `/problems/7/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S08-01 |
| 2053 | `/problems/7/complaints/2/procedures/0/name` | `name` |  | string | 혈관레이저 |  |
| 2054 | `/problems/7/complaints/2/procedures/0/category` | `category` |  | string | M8 |  |
| 2055 | `/problems/7/complaints/2/procedures/0/role` | `role` |  | string | 혈관 수축/파괴 |  |
| 2056 | `/problems/7/complaints/2/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2057 | `/problems/7/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 엑셀V |  |
| 2058 | `/problems/7/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2059 | `/problems/7/complaints/2/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2060 | `/problems/7/complaints/2/procedures/1/category` | `category` |  | string | M4 |  |
| 2061 | `/problems/7/complaints/2/procedures/1/role` | `role` |  | string | 피부 장벽 강화 |  |
| 2062 | `/problems/7/complaints/2/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2063 | `/problems/7/complaints/2/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 2064 | `/problems/7/complaints/2/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 2065 | `/problems/7/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2066 | `/problems/7/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2067 | `/problems/7/complaints/2/combos/0/name` | `name` |  | string | 혈관레이저 + 스킨부스터 |  |
| 2068 | `/problems/7/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2069 | `/problems/7/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 혈관레이저 |  |
| 2070 | `/problems/7/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2071 | `/problems/7/complaints/2/combos/0/reason` | `reason` |  | string | 혈관 수축 + 장벽 강화 |  |
| 2072 | `/problems/7/complaints/2/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진 |  |
| 2073 | `/problems/7/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2074 | `/problems/7/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | LDM 진정 관리 병행 | OB-S08-04 |
| 2075 | `/problems/7/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2076 | `/problems/7/complaints/3/cc` | `cc` |  | string | 엑셀V |  |
| 2077 | `/problems/7/complaints/3/cc_detail` | `cc_detail` |  | string | 532+1064nm | OB-S08-02 |
| 2078 | `/problems/7/complaints/3/cc_group` | `cc_group` |  | string | 모세혈관확장 |  |
| 2079 | `/problems/7/complaints/3/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2080 | `/problems/7/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S08-01 |
| 2081 | `/problems/7/complaints/3/procedures/0/name` | `name` |  | string | 혈관레이저 |  |
| 2082 | `/problems/7/complaints/3/procedures/0/category` | `category` |  | string | M8 |  |
| 2083 | `/problems/7/complaints/3/procedures/0/role` | `role` |  | string | 혈관 수축/파괴 |  |
| 2084 | `/problems/7/complaints/3/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2085 | `/problems/7/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 엑셀V |  |
| 2086 | `/problems/7/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2087 | `/problems/7/complaints/3/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2088 | `/problems/7/complaints/3/procedures/1/category` | `category` |  | string | M4 |  |
| 2089 | `/problems/7/complaints/3/procedures/1/role` | `role` |  | string | 피부 장벽 강화 |  |
| 2090 | `/problems/7/complaints/3/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2091 | `/problems/7/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 2092 | `/problems/7/complaints/3/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 2093 | `/problems/7/complaints/3/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2094 | `/problems/7/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2095 | `/problems/7/complaints/3/combos/0/name` | `name` |  | string | 혈관레이저 + 스킨부스터 |  |
| 2096 | `/problems/7/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2097 | `/problems/7/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 혈관레이저 |  |
| 2098 | `/problems/7/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2099 | `/problems/7/complaints/3/combos/0/reason` | `reason` |  | string | 혈관 수축 + 장벽 강화 |  |
| 2100 | `/problems/7/complaints/3/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진 |  |
| 2101 | `/problems/7/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2102 | `/problems/7/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | LDM 진정 관리 병행 | OB-S08-04 |
| 2103 | `/problems/7/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2104 | `/problems/7/complaints/4/cc` | `cc` |  | string | 혈관레이저 |  |
| 2105 | `/problems/7/complaints/4/cc_detail` | `cc_detail` |  | string | 선택적 혈관파괴 |  |
| 2106 | `/problems/7/complaints/4/cc_group` | `cc_group` |  | string | 모세혈관확장 |  |
| 2107 | `/problems/7/complaints/4/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2108 | `/problems/7/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S08-01 |
| 2109 | `/problems/7/complaints/4/procedures/0/name` | `name` |  | string | 혈관레이저 |  |
| 2110 | `/problems/7/complaints/4/procedures/0/category` | `category` |  | string | M8 |  |
| 2111 | `/problems/7/complaints/4/procedures/0/role` | `role` |  | string | 혈관 수축/파괴 |  |
| 2112 | `/problems/7/complaints/4/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2113 | `/problems/7/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 엑셀V |  |
| 2114 | `/problems/7/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2115 | `/problems/7/complaints/4/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2116 | `/problems/7/complaints/4/procedures/1/category` | `category` |  | string | M4 |  |
| 2117 | `/problems/7/complaints/4/procedures/1/role` | `role` |  | string | 피부 장벽 강화 |  |
| 2118 | `/problems/7/complaints/4/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2119 | `/problems/7/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 2120 | `/problems/7/complaints/4/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 2121 | `/problems/7/complaints/4/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2122 | `/problems/7/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2123 | `/problems/7/complaints/4/combos/0/name` | `name` |  | string | 혈관레이저 + 스킨부스터 |  |
| 2124 | `/problems/7/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2125 | `/problems/7/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 혈관레이저 |  |
| 2126 | `/problems/7/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2127 | `/problems/7/complaints/4/combos/0/reason` | `reason` |  | string | 혈관 수축 + 장벽 강화 |  |
| 2128 | `/problems/7/complaints/4/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진 |  |
| 2129 | `/problems/7/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2130 | `/problems/7/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | LDM 진정 관리 병행 | OB-S08-04 |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S08-01 | B | `/problems/7/complaints/0/procedures/0`<br>`/problems/7/complaints/1/procedures/0`<br>`/problems/7/complaints/2/procedures/0`<br>`/problems/7/complaints/3/procedures/0`<br>`/problems/7/complaints/4/procedures/0` | 다섯 complaint 의 procedures·combos·alternatives 가 글자 그대로 같다. cc 'V빔'(cc_detail '595nm PDL')·'IPL홍조'·'리쥬란+LDM'·'엑셀V'(cc_detail '532+1064nm')·'혈관레이저' 로 cc 는 서로 다른 장비·시술 표현인데 products 는 모두 '엑셀V' 하나다(B-02). |
| OB-S08-02 | P | `/problems/7/complaints/3/cc_detail` | cc_detail '532+1064nm' — '+' 가 두 수치를 잇고 단위 'nm' 는 뒤 수치에만 붙어 있다. 여기의 '+' 는 '함께 시술' 이 아니라 수치 병기로 읽힌다(F-02). 앞 수치의 단위를 채우지 않는다. |
| OB-S08-03 | P | `/problems/7/complaints/2/cc`<br>`/problems/7/complaints/2/cc_detail` | cc '리쥬란+LDM', cc_detail '장벽강화+재생' — cc 값 자체가 '+' 조합이다. 'LDM' 은 procedures 에 없고 원문에 풀이가 없다(B-03 같은 유형). |
| OB-S08-04 | P | `/problems/7/complaints/0/alternatives/0`<br>`/problems/7/complaints/1/alternatives/0`<br>`/problems/7/complaints/2/alternatives/0`<br>`/problems/7/complaints/3/alternatives/0`<br>`/problems/7/complaints/4/alternatives/0` | alternatives 'LDM 진정 관리 병행' — 병행 관리 지시. 대안 시술 목록이 아니다(F-04). |
| OB-S08-05 | P | `/problems/7/complaints/0/procedures/0/role` | role '혈관 수축/파괴' — '/' 로 두 기전을 나란히 둔다. 대안인지 병렬인지 정해지지 않는다(F-02). reason 은 '혈관 수축' 만 쓴다. |
| OB-S08-06 | P | `/problems/7/complaints/0/procedures/1/role` | 스킨부스터 role 이 여기서는 '피부 장벽 강화'(다른 구획: 피부 재생·콜라겐 재생·재생·톤개선). 같은 name 의 role 이 problem 마다 다르다. |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 595nm PDL | `/problems/7/complaints/0/cc_detail` [0,9) | 수량·단위(nm), 약어(PDL) |
| 532+1064nm | `/problems/7/complaints/3/cc_detail` [0,10) | 수량·단위(nm), 기호(+ 수치 병기) |
| 광범위 | `/problems/7/complaints/1/cc_detail` [0,3) | 범위 수식(광범위) |
| 장벽강화+재생 | `/problems/7/complaints/2/cc_detail` [0,7) | 기호(+ 공백 없음), 효과 표현 |
| 선택적 혈관파괴 | `/problems/7/complaints/4/cc_detail` [0,8) | 기전 수식(선택적), 기전 표현 |
| 리쥬란+LDM | `/problems/7/complaints/2/cc` [0,7) | 제품·시술 표현, 기호(+ 공백 없음), 약어(LDM) |
| IPL홍조 | `/problems/7/complaints/1/cc` [0,5) | 시술+증상 표현, 혼합 표기 |
| V빔 | `/problems/7/complaints/0/cc` [0,2) | 장비명 표현, 혼합 표기 |
| 모세혈관확장 | `/problems/7/complaints/3/cc_group` [0,6)<br>`/problems/7/complaints/4/cc_group` [0,6) | 증상 표현, 붙여 쓴 복합어 |
| 혈관 수축/파괴 | `/problems/7/complaints/0/procedures/0/role` [0,8)<br>`/problems/7/complaints/1/procedures/0/role` [0,8)<br>`/problems/7/complaints/2/procedures/0/role` [0,8)<br>`/problems/7/complaints/3/procedures/0/role` [0,8)<br>`/problems/7/complaints/4/procedures/0/role` [0,8) | role 표현, 기호(/), 기전 표현 |
| 피부 장벽 강화 | `/problems/7/complaints/0/procedures/1/role` [0,8)<br>`/problems/7/complaints/1/procedures/1/role` [0,8)<br>`/problems/7/complaints/2/procedures/1/role` [0,8)<br>`/problems/7/complaints/3/procedures/1/role` [0,8)<br>`/problems/7/complaints/4/procedures/1/role` [0,8) | role 표현, 증가 표현(강화) |
| 혈관 수축 + 장벽 강화 | `/problems/7/complaints/0/combos/0/reason` [0,13)<br>`/problems/7/complaints/1/combos/0/reason` [0,13)<br>`/problems/7/complaints/2/combos/0/reason` [0,13)<br>`/problems/7/complaints/3/combos/0/reason` [0,13)<br>`/problems/7/complaints/4/combos/0/reason` [0,13) | 기호(+), 결과 없는 공식형 |
| 레이저 후 재생 촉진 | `/problems/7/complaints/0/combos/0/evidence` [0,11)<br>`/problems/7/complaints/1/combos/0/evidence` [0,11)<br>`/problems/7/complaints/2/combos/0/evidence` [0,11)<br>`/problems/7/complaints/3/combos/0/evidence` [0,11)<br>`/problems/7/complaints/4/combos/0/evidence` [0,11) | 시간 순서(후), 증가 표현(촉진) |
| LDM 진정 관리 병행 | `/problems/7/complaints/0/alternatives/0` [0,12)<br>`/problems/7/complaints/1/alternatives/0` [0,12)<br>`/problems/7/complaints/2/alternatives/0` [0,12)<br>`/problems/7/complaints/3/alternatives/0` [0,12)<br>`/problems/7/complaints/4/alternatives/0` [0,12) | 병행, 약어(LDM), 관리 지시 |

## 이 구획에서 연 미결

- 새로 연 미결 없음(관찰은 기존 미결 유형에 연결).
