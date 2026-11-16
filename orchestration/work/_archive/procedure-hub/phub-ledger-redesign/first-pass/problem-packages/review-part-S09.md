# S09 — /problems/8 P9 흉터

[← review.md](review.md) · 범위 /problems/8 및 /problems/8/** 전체 · 소유 노드 493 · 말단 325 · 빈 값 6 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S09.txt 로 c0~c11 전부(procedures 38·combos 19·alternatives 13) 읽음. c6·c7 의 ±·괄호·세미콜론 문장은 기호 단위로 다시 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 2131 | `/problems/8` | `(problems 원소)` | 8 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 2132 | `/problems/8/problem_id` | `problem_id` |  | string | P9 |  |
| 2133 | `/problems/8/problem` | `problem` |  | string | 흉터 |  |
| 2134 | `/problems/8/complaints` | `complaints` |  | array[12] | (배열 · 12개) |  |
| 2135 | `/problems/8/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2136 | `/problems/8/complaints/0/cc` | `cc` |  | string | 서브시전 | OB-S00-06 |
| 2137 | `/problems/8/complaints/0/cc_detail` | `cc_detail` |  | string | 유착해제 |  |
| 2138 | `/problems/8/complaints/0/cc_group` | `cc_group` |  | string | 여드름흉터 |  |
| 2139 | `/problems/8/complaints/0/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 2140 | `/problems/8/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S09-01 |
| 2141 | `/problems/8/complaints/0/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2142 | `/problems/8/complaints/0/procedures/0/category` | `category` |  | string | M8 |  |
| 2143 | `/problems/8/complaints/0/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2144 | `/problems/8/complaints/0/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2145 | `/problems/8/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2146 | `/problems/8/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2147 | `/problems/8/complaints/0/procedures/1/name` | `name` |  | string | 서브시전 |  |
| 2148 | `/problems/8/complaints/0/procedures/1/category` | `category` |  | string | M8 | OB-S09-04 |
| 2149 | `/problems/8/complaints/0/procedures/1/role` | `role` |  | string | 유착 박리 |  |
| 2150 | `/problems/8/complaints/0/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2151 | `/problems/8/complaints/0/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2152 | `/problems/8/complaints/0/procedures/2/name` | `name` |  | string | PRP/자가혈 |  |
| 2153 | `/problems/8/complaints/0/procedures/2/category` | `category` |  | string | M5 |  |
| 2154 | `/problems/8/complaints/0/procedures/2/role` | `role` |  | string | 재생 촉진 |  |
| 2155 | `/problems/8/complaints/0/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2156 | `/problems/8/complaints/0/procedures/2/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 2157 | `/problems/8/complaints/0/procedures/2/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 2158 | `/problems/8/complaints/0/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S09-02 |
| 2159 | `/problems/8/complaints/0/procedures/3/name` | `name` |  | string | 니들RF |  |
| 2160 | `/problems/8/complaints/0/procedures/3/category` | `category` |  | string | M11 |  |
| 2161 | `/problems/8/complaints/0/procedures/3/role` | `role` |  | string | 콜라겐 자극 |  |
| 2162 | `/problems/8/complaints/0/procedures/3/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2163 | `/problems/8/complaints/0/procedures/3/products/0` | `(products 원소)` | 0 | string | 인트라셀 |  |
| 2164 | `/problems/8/complaints/0/procedures/3/products/1` | `(products 원소)` | 1 | string | 포텐자 |  |
| 2165 | `/problems/8/complaints/0/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 2166 | `/problems/8/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) | OB-S09-02 |
| 2167 | `/problems/8/complaints/0/combos/0/name` | `name` |  | string | 프락셔널 + PRP |  |
| 2168 | `/problems/8/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2169 | `/problems/8/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2170 | `/problems/8/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 2171 | `/problems/8/complaints/0/combos/0/reason` | `reason` |  | string | 미세구멍 + 성장인자 = 재생 2배 | OB-S09-06 |
| 2172 | `/problems/8/complaints/0/combos/0/evidence` | `evidence` |  | string | PRP가 채널로 깊이 침투 | OB-S09-07, OB-S13-10 |
| 2173 | `/problems/8/complaints/0/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) | OB-S09-02 |
| 2174 | `/problems/8/complaints/0/combos/1/name` | `name` |  | string | 서브시전 + 프락셔널 + PRP |  |
| 2175 | `/problems/8/complaints/0/combos/1/combo` | `combo` |  | array[3] | (배열 · 3개) | OB-S09-05 |
| 2176 | `/problems/8/complaints/0/combos/1/combo/0` | `(combo 원소)` | 0 | string | 서브시전 |  |
| 2177 | `/problems/8/complaints/0/combos/1/combo/1` | `(combo 원소)` | 1 | string | 프락셔널 |  |
| 2178 | `/problems/8/complaints/0/combos/1/combo/2` | `(combo 원소)` | 2 | string | PRP | OB-S00-05 |
| 2179 | `/problems/8/complaints/0/combos/1/reason` | `reason` |  | string | 박리+리서페이싱+재생 = 최대 효과 | OB-S09-05 |
| 2180 | `/problems/8/complaints/0/combos/1/evidence` | `evidence` |  | string | 가장 강력한 흉터 콤보 | OB-S09-06 |
| 2181 | `/problems/8/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2182 | `/problems/8/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 | OB-S09-14 |
| 2183 | `/problems/8/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2184 | `/problems/8/complaints/1/cc` | `cc` |  | string | 에어서브시전 |  |
| 2185 | `/problems/8/complaints/1/cc_detail` | `cc_detail` |  | string | 공기압 박리 |  |
| 2186 | `/problems/8/complaints/1/cc_group` | `cc_group` |  | string | 여드름흉터 |  |
| 2187 | `/problems/8/complaints/1/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 2188 | `/problems/8/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S09-01 |
| 2189 | `/problems/8/complaints/1/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2190 | `/problems/8/complaints/1/procedures/0/category` | `category` |  | string | M8 |  |
| 2191 | `/problems/8/complaints/1/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2192 | `/problems/8/complaints/1/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2193 | `/problems/8/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2194 | `/problems/8/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2195 | `/problems/8/complaints/1/procedures/1/name` | `name` |  | string | 서브시전 |  |
| 2196 | `/problems/8/complaints/1/procedures/1/category` | `category` |  | string | M8 |  |
| 2197 | `/problems/8/complaints/1/procedures/1/role` | `role` |  | string | 유착 박리 |  |
| 2198 | `/problems/8/complaints/1/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2199 | `/problems/8/complaints/1/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2200 | `/problems/8/complaints/1/procedures/2/name` | `name` |  | string | PRP/자가혈 |  |
| 2201 | `/problems/8/complaints/1/procedures/2/category` | `category` |  | string | M5 |  |
| 2202 | `/problems/8/complaints/1/procedures/2/role` | `role` |  | string | 재생 촉진 |  |
| 2203 | `/problems/8/complaints/1/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2204 | `/problems/8/complaints/1/procedures/2/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 2205 | `/problems/8/complaints/1/procedures/2/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 2206 | `/problems/8/complaints/1/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2207 | `/problems/8/complaints/1/procedures/3/name` | `name` |  | string | 니들RF |  |
| 2208 | `/problems/8/complaints/1/procedures/3/category` | `category` |  | string | M11 |  |
| 2209 | `/problems/8/complaints/1/procedures/3/role` | `role` |  | string | 콜라겐 자극 |  |
| 2210 | `/problems/8/complaints/1/procedures/3/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2211 | `/problems/8/complaints/1/procedures/3/products/0` | `(products 원소)` | 0 | string | 인트라셀 |  |
| 2212 | `/problems/8/complaints/1/procedures/3/products/1` | `(products 원소)` | 1 | string | 포텐자 |  |
| 2213 | `/problems/8/complaints/1/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 2214 | `/problems/8/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2215 | `/problems/8/complaints/1/combos/0/name` | `name` |  | string | 프락셔널 + PRP |  |
| 2216 | `/problems/8/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2217 | `/problems/8/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2218 | `/problems/8/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 2219 | `/problems/8/complaints/1/combos/0/reason` | `reason` |  | string | 미세구멍 + 성장인자 = 재생 2배 |  |
| 2220 | `/problems/8/complaints/1/combos/0/evidence` | `evidence` |  | string | PRP가 채널로 깊이 침투 |  |
| 2221 | `/problems/8/complaints/1/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2222 | `/problems/8/complaints/1/combos/1/name` | `name` |  | string | 서브시전 + 프락셔널 + PRP |  |
| 2223 | `/problems/8/complaints/1/combos/1/combo` | `combo` |  | array[3] | (배열 · 3개) |  |
| 2224 | `/problems/8/complaints/1/combos/1/combo/0` | `(combo 원소)` | 0 | string | 서브시전 |  |
| 2225 | `/problems/8/complaints/1/combos/1/combo/1` | `(combo 원소)` | 1 | string | 프락셔널 |  |
| 2226 | `/problems/8/complaints/1/combos/1/combo/2` | `(combo 원소)` | 2 | string | PRP | OB-S00-05 |
| 2227 | `/problems/8/complaints/1/combos/1/reason` | `reason` |  | string | 박리+리서페이싱+재생 = 최대 효과 |  |
| 2228 | `/problems/8/complaints/1/combos/1/evidence` | `evidence` |  | string | 가장 강력한 흉터 콤보 |  |
| 2229 | `/problems/8/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2230 | `/problems/8/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2231 | `/problems/8/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2232 | `/problems/8/complaints/2/cc` | `cc` |  | string | TCA크로스 | OB-S09-12 |
| 2233 | `/problems/8/complaints/2/cc_detail` | `cc_detail` |  | string | 점 도포 |  |
| 2234 | `/problems/8/complaints/2/cc_group` | `cc_group` |  | string | 여드름흉터 |  |
| 2235 | `/problems/8/complaints/2/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 2236 | `/problems/8/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S09-01 |
| 2237 | `/problems/8/complaints/2/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2238 | `/problems/8/complaints/2/procedures/0/category` | `category` |  | string | M8 |  |
| 2239 | `/problems/8/complaints/2/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2240 | `/problems/8/complaints/2/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2241 | `/problems/8/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2242 | `/problems/8/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2243 | `/problems/8/complaints/2/procedures/1/name` | `name` |  | string | 서브시전 |  |
| 2244 | `/problems/8/complaints/2/procedures/1/category` | `category` |  | string | M8 |  |
| 2245 | `/problems/8/complaints/2/procedures/1/role` | `role` |  | string | 유착 박리 |  |
| 2246 | `/problems/8/complaints/2/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2247 | `/problems/8/complaints/2/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2248 | `/problems/8/complaints/2/procedures/2/name` | `name` |  | string | PRP/자가혈 |  |
| 2249 | `/problems/8/complaints/2/procedures/2/category` | `category` |  | string | M5 |  |
| 2250 | `/problems/8/complaints/2/procedures/2/role` | `role` |  | string | 재생 촉진 |  |
| 2251 | `/problems/8/complaints/2/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2252 | `/problems/8/complaints/2/procedures/2/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 2253 | `/problems/8/complaints/2/procedures/2/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 2254 | `/problems/8/complaints/2/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2255 | `/problems/8/complaints/2/procedures/3/name` | `name` |  | string | 니들RF |  |
| 2256 | `/problems/8/complaints/2/procedures/3/category` | `category` |  | string | M11 |  |
| 2257 | `/problems/8/complaints/2/procedures/3/role` | `role` |  | string | 콜라겐 자극 |  |
| 2258 | `/problems/8/complaints/2/procedures/3/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2259 | `/problems/8/complaints/2/procedures/3/products/0` | `(products 원소)` | 0 | string | 인트라셀 |  |
| 2260 | `/problems/8/complaints/2/procedures/3/products/1` | `(products 원소)` | 1 | string | 포텐자 |  |
| 2261 | `/problems/8/complaints/2/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 2262 | `/problems/8/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2263 | `/problems/8/complaints/2/combos/0/name` | `name` |  | string | 프락셔널 + PRP |  |
| 2264 | `/problems/8/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2265 | `/problems/8/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2266 | `/problems/8/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 2267 | `/problems/8/complaints/2/combos/0/reason` | `reason` |  | string | 미세구멍 + 성장인자 = 재생 2배 |  |
| 2268 | `/problems/8/complaints/2/combos/0/evidence` | `evidence` |  | string | PRP가 채널로 깊이 침투 |  |
| 2269 | `/problems/8/complaints/2/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2270 | `/problems/8/complaints/2/combos/1/name` | `name` |  | string | 서브시전 + 프락셔널 + PRP |  |
| 2271 | `/problems/8/complaints/2/combos/1/combo` | `combo` |  | array[3] | (배열 · 3개) |  |
| 2272 | `/problems/8/complaints/2/combos/1/combo/0` | `(combo 원소)` | 0 | string | 서브시전 |  |
| 2273 | `/problems/8/complaints/2/combos/1/combo/1` | `(combo 원소)` | 1 | string | 프락셔널 |  |
| 2274 | `/problems/8/complaints/2/combos/1/combo/2` | `(combo 원소)` | 2 | string | PRP | OB-S00-05 |
| 2275 | `/problems/8/complaints/2/combos/1/reason` | `reason` |  | string | 박리+리서페이싱+재생 = 최대 효과 |  |
| 2276 | `/problems/8/complaints/2/combos/1/evidence` | `evidence` |  | string | 가장 강력한 흉터 콤보 |  |
| 2277 | `/problems/8/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2278 | `/problems/8/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2279 | `/problems/8/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2280 | `/problems/8/complaints/3/cc` | `cc` |  | string | CO2프락셔널 |  |
| 2281 | `/problems/8/complaints/3/cc_detail` | `cc_detail` |  | string | 박피재생 |  |
| 2282 | `/problems/8/complaints/3/cc_group` | `cc_group` |  | string | 여드름흉터 |  |
| 2283 | `/problems/8/complaints/3/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 2284 | `/problems/8/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S09-01 |
| 2285 | `/problems/8/complaints/3/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2286 | `/problems/8/complaints/3/procedures/0/category` | `category` |  | string | M8 |  |
| 2287 | `/problems/8/complaints/3/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2288 | `/problems/8/complaints/3/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2289 | `/problems/8/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2290 | `/problems/8/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2291 | `/problems/8/complaints/3/procedures/1/name` | `name` |  | string | 서브시전 |  |
| 2292 | `/problems/8/complaints/3/procedures/1/category` | `category` |  | string | M8 |  |
| 2293 | `/problems/8/complaints/3/procedures/1/role` | `role` |  | string | 유착 박리 |  |
| 2294 | `/problems/8/complaints/3/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2295 | `/problems/8/complaints/3/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2296 | `/problems/8/complaints/3/procedures/2/name` | `name` |  | string | PRP/자가혈 |  |
| 2297 | `/problems/8/complaints/3/procedures/2/category` | `category` |  | string | M5 |  |
| 2298 | `/problems/8/complaints/3/procedures/2/role` | `role` |  | string | 재생 촉진 |  |
| 2299 | `/problems/8/complaints/3/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2300 | `/problems/8/complaints/3/procedures/2/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 2301 | `/problems/8/complaints/3/procedures/2/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 2302 | `/problems/8/complaints/3/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2303 | `/problems/8/complaints/3/procedures/3/name` | `name` |  | string | 니들RF |  |
| 2304 | `/problems/8/complaints/3/procedures/3/category` | `category` |  | string | M11 |  |
| 2305 | `/problems/8/complaints/3/procedures/3/role` | `role` |  | string | 콜라겐 자극 |  |
| 2306 | `/problems/8/complaints/3/procedures/3/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2307 | `/problems/8/complaints/3/procedures/3/products/0` | `(products 원소)` | 0 | string | 인트라셀 |  |
| 2308 | `/problems/8/complaints/3/procedures/3/products/1` | `(products 원소)` | 1 | string | 포텐자 |  |
| 2309 | `/problems/8/complaints/3/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 2310 | `/problems/8/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2311 | `/problems/8/complaints/3/combos/0/name` | `name` |  | string | 프락셔널 + PRP |  |
| 2312 | `/problems/8/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2313 | `/problems/8/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2314 | `/problems/8/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 2315 | `/problems/8/complaints/3/combos/0/reason` | `reason` |  | string | 미세구멍 + 성장인자 = 재생 2배 |  |
| 2316 | `/problems/8/complaints/3/combos/0/evidence` | `evidence` |  | string | PRP가 채널로 깊이 침투 |  |
| 2317 | `/problems/8/complaints/3/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2318 | `/problems/8/complaints/3/combos/1/name` | `name` |  | string | 서브시전 + 프락셔널 + PRP |  |
| 2319 | `/problems/8/complaints/3/combos/1/combo` | `combo` |  | array[3] | (배열 · 3개) |  |
| 2320 | `/problems/8/complaints/3/combos/1/combo/0` | `(combo 원소)` | 0 | string | 서브시전 |  |
| 2321 | `/problems/8/complaints/3/combos/1/combo/1` | `(combo 원소)` | 1 | string | 프락셔널 |  |
| 2322 | `/problems/8/complaints/3/combos/1/combo/2` | `(combo 원소)` | 2 | string | PRP | OB-S00-05 |
| 2323 | `/problems/8/complaints/3/combos/1/reason` | `reason` |  | string | 박리+리서페이싱+재생 = 최대 효과 |  |
| 2324 | `/problems/8/complaints/3/combos/1/evidence` | `evidence` |  | string | 가장 강력한 흉터 콤보 |  |
| 2325 | `/problems/8/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2326 | `/problems/8/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2327 | `/problems/8/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2328 | `/problems/8/complaints/4/cc` | `cc` |  | string | 니들RF | OB-S00-06, OB-S09-13 |
| 2329 | `/problems/8/complaints/4/cc_detail` | `cc_detail` |  | string | 포텐자/시크릿 | OB-S09-03 |
| 2330 | `/problems/8/complaints/4/cc_group` | `cc_group` |  | string | 여드름흉터 |  |
| 2331 | `/problems/8/complaints/4/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 2332 | `/problems/8/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S09-01 |
| 2333 | `/problems/8/complaints/4/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2334 | `/problems/8/complaints/4/procedures/0/category` | `category` |  | string | M8 |  |
| 2335 | `/problems/8/complaints/4/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2336 | `/problems/8/complaints/4/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2337 | `/problems/8/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2338 | `/problems/8/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2339 | `/problems/8/complaints/4/procedures/1/name` | `name` |  | string | 서브시전 |  |
| 2340 | `/problems/8/complaints/4/procedures/1/category` | `category` |  | string | M8 |  |
| 2341 | `/problems/8/complaints/4/procedures/1/role` | `role` |  | string | 유착 박리 |  |
| 2342 | `/problems/8/complaints/4/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2343 | `/problems/8/complaints/4/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2344 | `/problems/8/complaints/4/procedures/2/name` | `name` |  | string | PRP/자가혈 |  |
| 2345 | `/problems/8/complaints/4/procedures/2/category` | `category` |  | string | M5 |  |
| 2346 | `/problems/8/complaints/4/procedures/2/role` | `role` |  | string | 재생 촉진 |  |
| 2347 | `/problems/8/complaints/4/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2348 | `/problems/8/complaints/4/procedures/2/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 2349 | `/problems/8/complaints/4/procedures/2/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 2350 | `/problems/8/complaints/4/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2351 | `/problems/8/complaints/4/procedures/3/name` | `name` |  | string | 니들RF |  |
| 2352 | `/problems/8/complaints/4/procedures/3/category` | `category` |  | string | M11 |  |
| 2353 | `/problems/8/complaints/4/procedures/3/role` | `role` |  | string | 콜라겐 자극 |  |
| 2354 | `/problems/8/complaints/4/procedures/3/products` | `products` |  | array[2] | (배열 · 2개) | OB-S09-03 |
| 2355 | `/problems/8/complaints/4/procedures/3/products/0` | `(products 원소)` | 0 | string | 인트라셀 |  |
| 2356 | `/problems/8/complaints/4/procedures/3/products/1` | `(products 원소)` | 1 | string | 포텐자 |  |
| 2357 | `/problems/8/complaints/4/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 2358 | `/problems/8/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2359 | `/problems/8/complaints/4/combos/0/name` | `name` |  | string | 프락셔널 + PRP |  |
| 2360 | `/problems/8/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2361 | `/problems/8/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2362 | `/problems/8/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 2363 | `/problems/8/complaints/4/combos/0/reason` | `reason` |  | string | 미세구멍 + 성장인자 = 재생 2배 |  |
| 2364 | `/problems/8/complaints/4/combos/0/evidence` | `evidence` |  | string | PRP가 채널로 깊이 침투 |  |
| 2365 | `/problems/8/complaints/4/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2366 | `/problems/8/complaints/4/combos/1/name` | `name` |  | string | 서브시전 + 프락셔널 + PRP |  |
| 2367 | `/problems/8/complaints/4/combos/1/combo` | `combo` |  | array[3] | (배열 · 3개) |  |
| 2368 | `/problems/8/complaints/4/combos/1/combo/0` | `(combo 원소)` | 0 | string | 서브시전 |  |
| 2369 | `/problems/8/complaints/4/combos/1/combo/1` | `(combo 원소)` | 1 | string | 프락셔널 |  |
| 2370 | `/problems/8/complaints/4/combos/1/combo/2` | `(combo 원소)` | 2 | string | PRP | OB-S00-05 |
| 2371 | `/problems/8/complaints/4/combos/1/reason` | `reason` |  | string | 박리+리서페이싱+재생 = 최대 효과 |  |
| 2372 | `/problems/8/complaints/4/combos/1/evidence` | `evidence` |  | string | 가장 강력한 흉터 콤보 |  |
| 2373 | `/problems/8/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2374 | `/problems/8/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2375 | `/problems/8/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2376 | `/problems/8/complaints/5/cc` | `cc` |  | string | 필러+서브시전 | OB-S09-15 |
| 2377 | `/problems/8/complaints/5/cc_detail` | `cc_detail` |  | string | 복합치료 |  |
| 2378 | `/problems/8/complaints/5/cc_group` | `cc_group` |  | string | 여드름흉터 |  |
| 2379 | `/problems/8/complaints/5/procedures` | `procedures` |  | array[6] | (배열 · 6개) |  |
| 2380 | `/problems/8/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2381 | `/problems/8/complaints/5/procedures/0/name` | `name` |  | string | 필러 |  |
| 2382 | `/problems/8/complaints/5/procedures/0/category` | `category` |  | string | M2 |  |
| 2383 | `/problems/8/complaints/5/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 2384 | `/problems/8/complaints/5/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 2385 | `/problems/8/complaints/5/procedures/0/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 2386 | `/problems/8/complaints/5/procedures/0/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 2387 | `/problems/8/complaints/5/procedures/0/products/2` | `(products 원소)` | 2 | string | 이브아르 |  |
| 2388 | `/problems/8/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2389 | `/problems/8/complaints/5/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 2390 | `/problems/8/complaints/5/procedures/1/category` | `category` |  | string | M1 |  |
| 2391 | `/problems/8/complaints/5/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 2392 | `/problems/8/complaints/5/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2393 | `/problems/8/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 2394 | `/problems/8/complaints/5/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 2395 | `/problems/8/complaints/5/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2396 | `/problems/8/complaints/5/procedures/2/name` | `name` |  | string | 프락셔널 |  |
| 2397 | `/problems/8/complaints/5/procedures/2/category` | `category` |  | string | M8 |  |
| 2398 | `/problems/8/complaints/5/procedures/2/role` | `role` |  | string | 리서페이싱 |  |
| 2399 | `/problems/8/complaints/5/procedures/2/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2400 | `/problems/8/complaints/5/procedures/2/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2401 | `/problems/8/complaints/5/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2402 | `/problems/8/complaints/5/procedures/3/name` | `name` |  | string | 서브시전 |  |
| 2403 | `/problems/8/complaints/5/procedures/3/category` | `category` |  | string | M8 |  |
| 2404 | `/problems/8/complaints/5/procedures/3/role` | `role` |  | string | 유착 박리 |  |
| 2405 | `/problems/8/complaints/5/procedures/3/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2406 | `/problems/8/complaints/5/procedures/4` | `(procedures 원소)` | 4 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2407 | `/problems/8/complaints/5/procedures/4/name` | `name` |  | string | PRP/자가혈 |  |
| 2408 | `/problems/8/complaints/5/procedures/4/category` | `category` |  | string | M5 |  |
| 2409 | `/problems/8/complaints/5/procedures/4/role` | `role` |  | string | 재생 촉진 |  |
| 2410 | `/problems/8/complaints/5/procedures/4/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2411 | `/problems/8/complaints/5/procedures/4/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 2412 | `/problems/8/complaints/5/procedures/4/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 2413 | `/problems/8/complaints/5/procedures/5` | `(procedures 원소)` | 5 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2414 | `/problems/8/complaints/5/procedures/5/name` | `name` |  | string | 니들RF |  |
| 2415 | `/problems/8/complaints/5/procedures/5/category` | `category` |  | string | M11 |  |
| 2416 | `/problems/8/complaints/5/procedures/5/role` | `role` |  | string | 콜라겐 자극 |  |
| 2417 | `/problems/8/complaints/5/procedures/5/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2418 | `/problems/8/complaints/5/procedures/5/products/0` | `(products 원소)` | 0 | string | 인트라셀 |  |
| 2419 | `/problems/8/complaints/5/procedures/5/products/1` | `(products 원소)` | 1 | string | 포텐자 |  |
| 2420 | `/problems/8/complaints/5/combos` | `combos` |  | array[3] | (배열 · 3개) |  |
| 2421 | `/problems/8/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) | OB-S09-15 |
| 2422 | `/problems/8/complaints/5/combos/0/name` | `name` |  | string | 필러 + 보톡스 |  |
| 2423 | `/problems/8/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2424 | `/problems/8/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 2425 | `/problems/8/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 2426 | `/problems/8/complaints/5/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 |  |
| 2427 | `/problems/8/complaints/5/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 2428 | `/problems/8/complaints/5/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2429 | `/problems/8/complaints/5/combos/1/name` | `name` |  | string | 프락셔널 + PRP |  |
| 2430 | `/problems/8/complaints/5/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2431 | `/problems/8/complaints/5/combos/1/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2432 | `/problems/8/complaints/5/combos/1/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 2433 | `/problems/8/complaints/5/combos/1/reason` | `reason` |  | string | 미세구멍 + 성장인자 = 재생 2배 |  |
| 2434 | `/problems/8/complaints/5/combos/1/evidence` | `evidence` |  | string | PRP가 채널로 깊이 침투 |  |
| 2435 | `/problems/8/complaints/5/combos/2` | `(combos 원소)` | 2 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2436 | `/problems/8/complaints/5/combos/2/name` | `name` |  | string | 서브시전 + 프락셔널 + PRP |  |
| 2437 | `/problems/8/complaints/5/combos/2/combo` | `combo` |  | array[3] | (배열 · 3개) |  |
| 2438 | `/problems/8/complaints/5/combos/2/combo/0` | `(combo 원소)` | 0 | string | 서브시전 |  |
| 2439 | `/problems/8/complaints/5/combos/2/combo/1` | `(combo 원소)` | 1 | string | 프락셔널 |  |
| 2440 | `/problems/8/complaints/5/combos/2/combo/2` | `(combo 원소)` | 2 | string | PRP | OB-S00-05 |
| 2441 | `/problems/8/complaints/5/combos/2/reason` | `reason` |  | string | 박리+리서페이싱+재생 = 최대 효과 |  |
| 2442 | `/problems/8/complaints/5/combos/2/evidence` | `evidence` |  | string | 가장 강력한 흉터 콤보 |  |
| 2443 | `/problems/8/complaints/5/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 2444 | `/problems/8/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 2445 | `/problems/8/complaints/5/alternatives/1` | `(alternatives 원소)` | 1 | string | 여러 회 시리즈 필요 | OB-S09-14 |
| 2446 | `/problems/8/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2447 | `/problems/8/complaints/6/cc` | `cc` |  | string | 스테로이드주사 | OB-S09-11 |
| 2448 | `/problems/8/complaints/6/cc_detail` | `cc_detail` |  | string | 켈로이드 축소 |  |
| 2449 | `/problems/8/complaints/6/cc_group` | `cc_group` |  | string | 켈로이드/비후성 |  |
| 2450 | `/problems/8/complaints/6/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 2451 | `/problems/8/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2452 | `/problems/8/complaints/6/procedures/0/name` | `name` |  | string | 병변내 스테로이드주사 | OB-S09-11 |
| 2453 | `/problems/8/complaints/6/procedures/0/category` | `category` |  | string | M15 | OB-S09-04 |
| 2454 | `/problems/8/complaints/6/procedures/0/role` | `role` |  | string | 1차 치료·켈로이드 축소 |  |
| 2455 | `/problems/8/complaints/6/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2456 | `/problems/8/complaints/6/procedures/0/products/0` | `(products 원소)` | 0 | string | 트리암시놀론(±5-FU) | OB-S09-08 |
| 2457 | `/problems/8/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2458 | `/problems/8/complaints/6/procedures/1/name` | `name` |  | string | 레이저 |  |
| 2459 | `/problems/8/complaints/6/procedures/1/category` | `category` |  | string | M8 |  |
| 2460 | `/problems/8/complaints/6/procedures/1/role` | `role` |  | string | 홍반·혈관성 및 흉터 보조 개선 |  |
| 2461 | `/problems/8/complaints/6/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2462 | `/problems/8/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | PDL(V빔) |  |
| 2463 | `/problems/8/complaints/6/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2464 | `/problems/8/complaints/6/procedures/2/name` | `name` |  | string | 보톡스 |  |
| 2465 | `/problems/8/complaints/6/procedures/2/category` | `category` |  | string | M1 |  |
| 2466 | `/problems/8/complaints/6/procedures/2/role` | `role` |  | string | 보조요법(두께 축소 근거 제한) | OB-S09-10 |
| 2467 | `/problems/8/complaints/6/procedures/2/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2468 | `/problems/8/complaints/6/procedures/2/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 2469 | `/problems/8/complaints/6/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2470 | `/problems/8/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2471 | `/problems/8/complaints/6/combos/0/name` | `name` |  | string | 트리암시놀론(±5-FU) + PDL(V빔) | OB-S09-08, OB-S09-09 |
| 2472 | `/problems/8/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) | OB-S09-09 |
| 2473 | `/problems/8/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 병변내 스테로이드주사 |  |
| 2474 | `/problems/8/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | 레이저 |  |
| 2475 | `/problems/8/complaints/6/combos/0/reason` | `reason` |  | string | 병변내 1차 치료 + 혈관성·홍반 보조 개선 |  |
| 2476 | `/problems/8/complaints/6/combos/0/evidence` | `evidence` |  | string | 트리암시놀론(±5-FU)이 1차 치료이며 PDL은 보조 치료; 보톡스의 두께 축소 근거는 제한적 | OB-S09-08, OB-S09-10 |
| 2477 | `/problems/8/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2478 | `/problems/8/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2479 | `/problems/8/complaints/7` | `(complaints 원소)` | 7 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2480 | `/problems/8/complaints/7/cc` | `cc` |  | string | 레이저치료 |  |
| 2481 | `/problems/8/complaints/7/cc_detail` | `cc_detail` |  | string | V빔/프락셔널 |  |
| 2482 | `/problems/8/complaints/7/cc_group` | `cc_group` |  | string | 켈로이드/비후성 |  |
| 2483 | `/problems/8/complaints/7/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 2484 | `/problems/8/complaints/7/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2485 | `/problems/8/complaints/7/procedures/0/name` | `name` |  | string | 병변내 스테로이드주사 |  |
| 2486 | `/problems/8/complaints/7/procedures/0/category` | `category` |  | string | M15 |  |
| 2487 | `/problems/8/complaints/7/procedures/0/role` | `role` |  | string | 1차 치료·켈로이드 축소 |  |
| 2488 | `/problems/8/complaints/7/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2489 | `/problems/8/complaints/7/procedures/0/products/0` | `(products 원소)` | 0 | string | 트리암시놀론(±5-FU) |  |
| 2490 | `/problems/8/complaints/7/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2491 | `/problems/8/complaints/7/procedures/1/name` | `name` |  | string | 레이저 |  |
| 2492 | `/problems/8/complaints/7/procedures/1/category` | `category` |  | string | M8 |  |
| 2493 | `/problems/8/complaints/7/procedures/1/role` | `role` |  | string | 홍반·혈관성 및 흉터 보조 개선 |  |
| 2494 | `/problems/8/complaints/7/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2495 | `/problems/8/complaints/7/procedures/1/products/0` | `(products 원소)` | 0 | string | PDL(V빔) |  |
| 2496 | `/problems/8/complaints/7/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2497 | `/problems/8/complaints/7/procedures/2/name` | `name` |  | string | 보톡스 |  |
| 2498 | `/problems/8/complaints/7/procedures/2/category` | `category` |  | string | M1 |  |
| 2499 | `/problems/8/complaints/7/procedures/2/role` | `role` |  | string | 보조요법(두께 축소 근거 제한) |  |
| 2500 | `/problems/8/complaints/7/procedures/2/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2501 | `/problems/8/complaints/7/procedures/2/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 2502 | `/problems/8/complaints/7/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2503 | `/problems/8/complaints/7/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2504 | `/problems/8/complaints/7/combos/0/name` | `name` |  | string | 트리암시놀론(±5-FU) + PDL(V빔) |  |
| 2505 | `/problems/8/complaints/7/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2506 | `/problems/8/complaints/7/combos/0/combo/0` | `(combo 원소)` | 0 | string | 병변내 스테로이드주사 |  |
| 2507 | `/problems/8/complaints/7/combos/0/combo/1` | `(combo 원소)` | 1 | string | 레이저 |  |
| 2508 | `/problems/8/complaints/7/combos/0/reason` | `reason` |  | string | 병변내 1차 치료 + 혈관성·홍반 보조 개선 |  |
| 2509 | `/problems/8/complaints/7/combos/0/evidence` | `evidence` |  | string | 트리암시놀론(±5-FU)이 1차 치료이며 PDL은 보조 치료; 보톡스의 두께 축소 근거는 제한적 |  |
| 2510 | `/problems/8/complaints/7/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2511 | `/problems/8/complaints/7/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2512 | `/problems/8/complaints/8` | `(complaints 원소)` | 8 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2513 | `/problems/8/complaints/8/cc` | `cc` |  | string | 프락셔널레이저 | OB-S00-06, OB-S09-13 |
| 2514 | `/problems/8/complaints/8/cc_detail` | `cc_detail` |  | string | CO2/어븀 |  |
| 2515 | `/problems/8/complaints/8/cc_group` | `cc_group` |  | string | 수술흉터/화상흉터 |  |
| 2516 | `/problems/8/complaints/8/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2517 | `/problems/8/complaints/8/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2518 | `/problems/8/complaints/8/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2519 | `/problems/8/complaints/8/procedures/0/category` | `category` |  | string | M8 |  |
| 2520 | `/problems/8/complaints/8/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2521 | `/problems/8/complaints/8/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2522 | `/problems/8/complaints/8/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2523 | `/problems/8/complaints/8/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2524 | `/problems/8/complaints/8/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2525 | `/problems/8/complaints/8/procedures/1/category` | `category` |  | string | M4 |  |
| 2526 | `/problems/8/complaints/8/procedures/1/role` | `role` |  | string | 재생 |  |
| 2527 | `/problems/8/complaints/8/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2528 | `/problems/8/complaints/8/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 2529 | `/problems/8/complaints/8/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 힐러 |  |
| 2530 | `/problems/8/complaints/8/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2531 | `/problems/8/complaints/8/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2532 | `/problems/8/complaints/8/combos/0/name` | `name` |  | string | 프락셔널 + 스킨부스터 |  |
| 2533 | `/problems/8/complaints/8/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2534 | `/problems/8/complaints/8/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2535 | `/problems/8/complaints/8/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2536 | `/problems/8/complaints/8/combos/0/reason` | `reason` |  | string | 리서페이싱 + 재생 |  |
| 2537 | `/problems/8/complaints/8/combos/0/evidence` | `evidence` |  | string | 프락셔널 후 재생 촉진 |  |
| 2538 | `/problems/8/complaints/8/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2539 | `/problems/8/complaints/8/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2540 | `/problems/8/complaints/9` | `(complaints 원소)` | 9 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2541 | `/problems/8/complaints/9/cc` | `cc` |  | string | 실리콘시트 | OB-S09-12 |
| 2542 | `/problems/8/complaints/9/cc_detail` | `cc_detail` |  | string | 보조요법 |  |
| 2543 | `/problems/8/complaints/9/cc_group` | `cc_group` |  | string | 수술흉터/화상흉터 |  |
| 2544 | `/problems/8/complaints/9/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2545 | `/problems/8/complaints/9/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2546 | `/problems/8/complaints/9/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2547 | `/problems/8/complaints/9/procedures/0/category` | `category` |  | string | M8 |  |
| 2548 | `/problems/8/complaints/9/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2549 | `/problems/8/complaints/9/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2550 | `/problems/8/complaints/9/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2551 | `/problems/8/complaints/9/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2552 | `/problems/8/complaints/9/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2553 | `/problems/8/complaints/9/procedures/1/category` | `category` |  | string | M4 |  |
| 2554 | `/problems/8/complaints/9/procedures/1/role` | `role` |  | string | 재생 |  |
| 2555 | `/problems/8/complaints/9/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2556 | `/problems/8/complaints/9/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 2557 | `/problems/8/complaints/9/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 힐러 |  |
| 2558 | `/problems/8/complaints/9/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2559 | `/problems/8/complaints/9/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2560 | `/problems/8/complaints/9/combos/0/name` | `name` |  | string | 프락셔널 + 스킨부스터 |  |
| 2561 | `/problems/8/complaints/9/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2562 | `/problems/8/complaints/9/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2563 | `/problems/8/complaints/9/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2564 | `/problems/8/complaints/9/combos/0/reason` | `reason` |  | string | 리서페이싱 + 재생 |  |
| 2565 | `/problems/8/complaints/9/combos/0/evidence` | `evidence` |  | string | 프락셔널 후 재생 촉진 |  |
| 2566 | `/problems/8/complaints/9/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2567 | `/problems/8/complaints/9/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2568 | `/problems/8/complaints/10` | `(complaints 원소)` | 10 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2569 | `/problems/8/complaints/10/cc` | `cc` |  | string | 프락셔널레이저 | OB-S00-06, OB-S09-13 |
| 2570 | `/problems/8/complaints/10/cc_detail` | `cc_detail` |  | string | 성장선/임신선 |  |
| 2571 | `/problems/8/complaints/10/cc_group` | `cc_group` |  | string | 튼살 |  |
| 2572 | `/problems/8/complaints/10/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2573 | `/problems/8/complaints/10/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2574 | `/problems/8/complaints/10/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2575 | `/problems/8/complaints/10/procedures/0/category` | `category` |  | string | M8 |  |
| 2576 | `/problems/8/complaints/10/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2577 | `/problems/8/complaints/10/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2578 | `/problems/8/complaints/10/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2579 | `/problems/8/complaints/10/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2580 | `/problems/8/complaints/10/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2581 | `/problems/8/complaints/10/procedures/1/category` | `category` |  | string | M4 |  |
| 2582 | `/problems/8/complaints/10/procedures/1/role` | `role` |  | string | 재생 |  |
| 2583 | `/problems/8/complaints/10/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2584 | `/problems/8/complaints/10/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 2585 | `/problems/8/complaints/10/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 힐러 |  |
| 2586 | `/problems/8/complaints/10/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2587 | `/problems/8/complaints/10/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2588 | `/problems/8/complaints/10/combos/0/name` | `name` |  | string | 프락셔널 + 스킨부스터 |  |
| 2589 | `/problems/8/complaints/10/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2590 | `/problems/8/complaints/10/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2591 | `/problems/8/complaints/10/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2592 | `/problems/8/complaints/10/combos/0/reason` | `reason` |  | string | 리서페이싱 + 재생 |  |
| 2593 | `/problems/8/complaints/10/combos/0/evidence` | `evidence` |  | string | 프락셔널 후 재생 촉진 |  |
| 2594 | `/problems/8/complaints/10/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2595 | `/problems/8/complaints/10/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |
| 2596 | `/problems/8/complaints/11` | `(complaints 원소)` | 11 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2597 | `/problems/8/complaints/11/cc` | `cc` |  | string | 니들RF | OB-S00-06, OB-S09-13 |
| 2598 | `/problems/8/complaints/11/cc_detail` | `cc_detail` |  | string | 콜라겐리모델링 |  |
| 2599 | `/problems/8/complaints/11/cc_group` | `cc_group` |  | string | 튼살 |  |
| 2600 | `/problems/8/complaints/11/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2601 | `/problems/8/complaints/11/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2602 | `/problems/8/complaints/11/procedures/0/name` | `name` |  | string | 프락셔널 |  |
| 2603 | `/problems/8/complaints/11/procedures/0/category` | `category` |  | string | M8 |  |
| 2604 | `/problems/8/complaints/11/procedures/0/role` | `role` |  | string | 리서페이싱 |  |
| 2605 | `/problems/8/complaints/11/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2606 | `/problems/8/complaints/11/procedures/0/products/0` | `(products 원소)` | 0 | string | 프락셀 |  |
| 2607 | `/problems/8/complaints/11/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2608 | `/problems/8/complaints/11/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2609 | `/problems/8/complaints/11/procedures/1/category` | `category` |  | string | M4 |  |
| 2610 | `/problems/8/complaints/11/procedures/1/role` | `role` |  | string | 재생 |  |
| 2611 | `/problems/8/complaints/11/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2612 | `/problems/8/complaints/11/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 2613 | `/problems/8/complaints/11/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 힐러 |  |
| 2614 | `/problems/8/complaints/11/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2615 | `/problems/8/complaints/11/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2616 | `/problems/8/complaints/11/combos/0/name` | `name` |  | string | 프락셔널 + 스킨부스터 |  |
| 2617 | `/problems/8/complaints/11/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2618 | `/problems/8/complaints/11/combos/0/combo/0` | `(combo 원소)` | 0 | string | 프락셔널 |  |
| 2619 | `/problems/8/complaints/11/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2620 | `/problems/8/complaints/11/combos/0/reason` | `reason` |  | string | 리서페이싱 + 재생 |  |
| 2621 | `/problems/8/complaints/11/combos/0/evidence` | `evidence` |  | string | 프락셔널 후 재생 촉진 |  |
| 2622 | `/problems/8/complaints/11/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2623 | `/problems/8/complaints/11/alternatives/0` | `(alternatives 원소)` | 0 | string | 여러 회 시리즈 필요 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S09-01 | B | `/problems/8/complaints/0/procedures/0`<br>`/problems/8/complaints/1/procedures/0`<br>`/problems/8/complaints/2/procedures/0`<br>`/problems/8/complaints/3/procedures/0`<br>`/problems/8/complaints/4/procedures/0` | c0~c4(서브시전·에어서브시전·TCA크로스·CO2프락셔널·니들RF)는 procedures 4개·combos 2개·alternatives 가 글자 그대로 같다. c8~c11 도 서로 같다(B-02). cc 의 차이(cc_detail '공기압 박리'·'점 도포'·'박피재생'·'포텐자/시크릿')가 procedures 에 반영돼 있지 않다. |
| OB-S09-02 | P | `/problems/8/complaints/0/procedures/3`<br>`/problems/8/complaints/0/combos/0`<br>`/problems/8/complaints/0/combos/1` | c0~c5 에서 니들RF(P3/P5) 는 procedures 에 있으나 어떤 combo 에도 들어가지 않는다. procedures 와 combos 원소가 일대일이 아니다. |
| OB-S09-03 | I | `/problems/8/complaints/4/cc_detail`<br>`/problems/8/complaints/4/procedures/3/products` | c4 cc '니들RF' 의 cc_detail '포텐자/시크릿' 중 '시크릿' 이 니들RF products('인트라셀','포텐자')에 없다(I-03 같은 유형). |
| OB-S09-04 | P | `/problems/8/complaints/0/procedures/1/category`<br>`/problems/8/complaints/6/procedures/0/category` | category 코드: '서브시전' 이 M8(프락셔널·레이저와 같은 코드), '병변내 스테로이드주사' 가 M15(다른 구획의 반영구화장·메디컬스킨케어와 같은 코드). 코드-이름 대응 확인은 taxonomy 대조 과제(F-01). |
| OB-S09-05 | P | `/problems/8/complaints/0/combos/1/combo`<br>`/problems/8/complaints/0/combos/1/reason` | combo 원소 3개인 combo('서브시전 + 프락셔널 + PRP')가 처음 나온다. reason '박리+리서페이싱+재생 = 최대 효과' 는 원소 순서대로 작용을 공백 없는 '+' 로 잇는다. |
| OB-S09-06 | P | `/problems/8/complaints/0/combos/0/reason`<br>`/problems/8/complaints/0/combos/1/evidence` | '재생 2배', '최대 효과', '가장 강력한 흉터 콤보' — 배수·최상급 주장. 근거 출처가 없다. '2배' 를 수치 사실로 바꾸지 않는다. |
| OB-S09-07 | B | `/problems/8/complaints/0/combos/0/evidence` | 'PRP가 채널로 깊이 침투' — '채널' 이 무엇인지 문장 안에 없다(reason 의 '미세구멍' 과 같은 것으로 읽힐 수 있으나 확정하지 않음). |
| OB-S09-08 | P | `/problems/8/complaints/6/procedures/0/products/0`<br>`/problems/8/complaints/6/combos/0/name`<br>`/problems/8/complaints/6/combos/0/evidence` | products '트리암시놀론(±5-FU)' — '±' 와 괄호로 선택적 병용 성분을 한 값에 담는다. '5-FU' 의 '-' 는 범위가 아니라 이름 일부. 형태소 분석 기호 처리 확인(K-05). |
| OB-S09-09 | I | `/problems/8/complaints/6/combos/0/name`<br>`/problems/8/complaints/6/combos/0/combo` | combo name '트리암시놀론(±5-FU) + PDL(V빔)' 은 products 표기로 쓰였고 combo 원소는 procedures 이름('병변내 스테로이드주사','레이저')이다(I-02 같은 유형). |
| OB-S09-10 | P | `/problems/8/complaints/6/combos/0/evidence`<br>`/problems/8/complaints/6/procedures/2/role` | evidence 는 세미콜론으로 두 진술을 잇는다: 'X이 1차 치료이며 PDL은 보조 치료' ; '보톡스의 두께 축소 근거는 제한적'. 둘째 진술은 combo 에 없는 procedure(보톡스)에 관한 것이다. role '보조요법(두께 축소 근거 제한)' 과 같은 한정이다. '1차'·'보조' 는 치료 순위 표현으로 보존. |
| OB-S09-11 | P | `/problems/8/complaints/6/cc`<br>`/problems/8/complaints/6/procedures/0/name` | cc '스테로이드주사' ↔ procedures name '병변내 스테로이드주사' — procedures 쪽에 '병변내' 수식이 붙어 있다. |
| OB-S09-12 | I | `/problems/8/complaints/2/cc`<br>`/problems/8/complaints/9/cc` | cc 'TCA크로스'·'실리콘시트' 가 가리키는 처치가 procedures 에 없다(I-03 같은 유형). |
| OB-S09-13 | P | `/problems/8/complaints/8/cc`<br>`/problems/8/complaints/10/cc`<br>`/problems/8/complaints/4/cc`<br>`/problems/8/complaints/11/cc` | 같은 problem 안에서 cc '프락셔널레이저' 가 c8(cc_group '수술흉터/화상흉터')·c10('튼살') 두 번, cc '니들RF' 가 c4('여드름흉터')·c11('튼살') 두 번 나온다. cc 문자열만으로 complaint 를 식별할 수 없다. |
| OB-S09-14 | B | `/problems/8/complaints/0/alternatives/0`<br>`/problems/8/complaints/5/alternatives/1` | alternatives '여러 회 시리즈 필요' — 회수가 막연하다('여러 회'). 수치로 바꾸지 않는다. |
| OB-S09-15 | P | `/problems/8/complaints/5/cc`<br>`/problems/8/complaints/5/combos/0` | c5 cc '필러+서브시전' — cc 가 조합 표기다. combos 에는 '필러 + 서브시전' 이 없고 '필러 + 보톡스'(S01 템플릿) 가 들어 있다. |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 유착해제 | `/problems/8/complaints/0/cc_detail` [0,4) | 기전 표현, 붙여 쓴 복합어 |
| 공기압 박리 | `/problems/8/complaints/1/cc_detail` [0,6) | 기전 수식(공기압), 기전 표현 |
| 점 도포 | `/problems/8/complaints/2/cc_detail` [0,4) | 적용 방식 표현 |
| 박피재생 | `/problems/8/complaints/3/cc_detail` [0,4) | 붙여 쓴 복합어, 기전·효과 표현 |
| 포텐자/시크릿 | `/problems/8/complaints/4/cc_detail` [0,7) | 제품명 표현, 기호(/) |
| 복합치료 | `/problems/8/complaints/5/cc_detail` [0,4) | 붙여 쓴 복합어, 조합 표현 |
| 켈로이드 축소 | `/problems/8/complaints/6/cc_detail` [0,7) | 증상 표현, 감소 표현 |
| V빔/프락셔널 | `/problems/8/complaints/7/cc_detail` [0,7) | 장비·시술 표현, 기호(/) |
| CO2/어븀 | `/problems/8/complaints/8/cc_detail` [0,6) | 장비·매질 표현, 기호(/), 혼합 표기 |
| 보조요법 | `/problems/8/complaints/9/cc_detail` [0,4) | 치료 순위(보조) |
| 성장선/임신선 | `/problems/8/complaints/10/cc_detail` [0,7) | 증상 표현, 기호(/) |
| 콜라겐리모델링 | `/problems/8/complaints/11/cc_detail` [0,7) | 붙여 쓴 복합어, 기전 표현 |
| 필러+서브시전 | `/problems/8/complaints/5/cc` [0,7) | 시술명 조합, 기호(+ 공백 없음) |
| TCA크로스 | `/problems/8/complaints/2/cc` [0,6) | 시술명 표현, 혼합 표기, 약어(TCA) |
| 켈로이드/비후성 | `/problems/8/complaints/6/cc_group` [0,8)<br>`/problems/8/complaints/7/cc_group` [0,8) | 증상 표현, 기호(/) |
| 수술흉터/화상흉터 | `/problems/8/complaints/8/cc_group` [0,9)<br>`/problems/8/complaints/9/cc_group` [0,9) | 증상 표현, 기호(/) |
| 미세구멍 + 성장인자 = 재생 2배 | `/problems/8/complaints/0/combos/0/reason` [0,19)<br>`/problems/8/complaints/1/combos/0/reason` [0,19)<br>`/problems/8/complaints/2/combos/0/reason` [0,19)<br>`/problems/8/complaints/3/combos/0/reason` [0,19)<br>`/problems/8/complaints/4/combos/0/reason` [0,19)<br>`/problems/8/complaints/5/combos/1/reason` [0,19) | 공식형 문장, 기호(+), 기호(=), 배수 주장(2배) |
| 재생 2배 | `/problems/8/complaints/0/combos/0/reason` [14,19)<br>`/problems/8/complaints/1/combos/0/reason` [14,19)<br>`/problems/8/complaints/2/combos/0/reason` [14,19)<br>`/problems/8/complaints/3/combos/0/reason` [14,19)<br>`/problems/8/complaints/4/combos/0/reason` [14,19)<br>`/problems/8/complaints/5/combos/1/reason` [14,19) | 배수 주장(2배), 수량 |
| PRP가 채널로 깊이 침투 | `/problems/8/complaints/0/combos/0/evidence` [0,14)<br>`/problems/8/complaints/1/combos/0/evidence` [0,14)<br>`/problems/8/complaints/2/combos/0/evidence` [0,14)<br>`/problems/8/complaints/3/combos/0/evidence` [0,14)<br>`/problems/8/complaints/4/combos/0/evidence` [0,14)<br>`/problems/8/complaints/5/combos/1/evidence` [0,14) | 기전 진술, 정도(깊이), 지시 대상 불명(채널) |
| 박리+리서페이싱+재생 = 최대 효과 | `/problems/8/complaints/0/combos/1/reason` [0,19)<br>`/problems/8/complaints/1/combos/1/reason` [0,19)<br>`/problems/8/complaints/2/combos/1/reason` [0,19)<br>`/problems/8/complaints/3/combos/1/reason` [0,19)<br>`/problems/8/complaints/4/combos/1/reason` [0,19)<br>`/problems/8/complaints/5/combos/2/reason` [0,19) | 공식형 문장, 기호(+ 공백 없음), 기호(=), 최상급(최대) |
| 가장 강력한 흉터 콤보 | `/problems/8/complaints/0/combos/1/evidence` [0,12)<br>`/problems/8/complaints/1/combos/1/evidence` [0,12)<br>`/problems/8/complaints/2/combos/1/evidence` [0,12)<br>`/problems/8/complaints/3/combos/1/evidence` [0,12)<br>`/problems/8/complaints/4/combos/1/evidence` [0,12)<br>`/problems/8/complaints/5/combos/2/evidence` [0,12) | 최상급(가장), 정도(강력한) |
| 여러 회 시리즈 필요 | `/problems/8/complaints/0/alternatives/0` [0,11)<br>`/problems/8/complaints/1/alternatives/0` [0,11)<br>`/problems/8/complaints/2/alternatives/0` [0,11)<br>`/problems/8/complaints/3/alternatives/0` [0,11)<br>`/problems/8/complaints/4/alternatives/0` [0,11)<br>`/problems/8/complaints/5/alternatives/1` [0,11)<br>`/problems/8/complaints/6/alternatives/0` [0,11)<br>`/problems/8/complaints/7/alternatives/0` [0,11)<br>`/problems/8/complaints/8/alternatives/0` [0,11)<br>`/problems/8/complaints/9/alternatives/0` [0,11)<br>`/problems/8/complaints/10/alternatives/0` [0,11)<br>`/problems/8/complaints/11/alternatives/0` [0,11) | 회차(막연), 필요 지시 |
| 바이오스티뮬레이터로 장기 관리 | `/problems/8/complaints/5/alternatives/0` [0,16) | 시술명 표현, 기간 표현(장기) |
| 볼륨 + 근이완 = 시너지 | `/problems/8/complaints/5/combos/0/reason` [0,14) | 공식형 문장, 기호(+), 기호(=) |
| 보톡스가 근육 움직임 줄여 필러 유지력 향상 | `/problems/8/complaints/5/combos/0/evidence` [0,24) | 인과·기전 진술 |
| 병변내 스테로이드주사 | `/problems/8/complaints/6/procedures/0/name` [0,11)<br>`/problems/8/complaints/7/procedures/0/name` [0,11)<br>`/problems/8/complaints/6/combos/0/combo/0` [0,11)<br>`/problems/8/complaints/7/combos/0/combo/0` [0,11) | 시술명 표현, 위치 수식(병변내) |
| 1차 치료·켈로이드 축소 | `/problems/8/complaints/6/procedures/0/role` [0,13)<br>`/problems/8/complaints/7/procedures/0/role` [0,13) | role 표현, 치료 순위(1차), 기호(·), 감소 표현 |
| 트리암시놀론(±5-FU) | `/problems/8/complaints/6/procedures/0/products/0` [0,13)<br>`/problems/8/complaints/7/procedures/0/products/0` [0,13) | 제품·성분 표현, 기호(±), 괄호 보충, 선택적 병용 |
| PDL(V빔) | `/problems/8/complaints/6/procedures/1/products/0` [0,7)<br>`/problems/8/complaints/7/procedures/1/products/0` [0,7) | 약어+장비명 병기, 괄호 보충 |
| 홍반·혈관성 및 흉터 보조 개선 | `/problems/8/complaints/6/procedures/1/role` [0,17)<br>`/problems/8/complaints/7/procedures/1/role` [0,17) | role 표현, 기호(·), 병렬(및), 보조 |
| 보조요법(두께 축소 근거 제한) | `/problems/8/complaints/6/procedures/2/role` [0,17)<br>`/problems/8/complaints/7/procedures/2/role` [0,17) | role 표현, 치료 순위(보조), 근거 수준 표현(제한), 괄호 보충 |
| 트리암시놀론(±5-FU) + PDL(V빔) | `/problems/8/complaints/6/combos/0/name` [0,23)<br>`/problems/8/complaints/7/combos/0/name` [0,23) | combo name(제품 표기), 기호(+), 기호(±), 괄호 보충 |
| 병변내 1차 치료 + 혈관성·홍반 보조 개선 | `/problems/8/complaints/6/combos/0/reason` [0,24)<br>`/problems/8/complaints/7/combos/0/reason` [0,24) | 기호(+), 치료 순위(1차·보조), 위치 수식(병변내) |
| 트리암시놀론(±5-FU)이 1차 치료이며 PDL은 보조 치료 | `/problems/8/complaints/6/combos/0/evidence` [0,33)<br>`/problems/8/complaints/7/combos/0/evidence` [0,33) | 치료 순위(1차·보조), 병렬(-이며), 기호(±) |
| 보톡스의 두께 축소 근거는 제한적 | `/problems/8/complaints/6/combos/0/evidence` [35,53)<br>`/problems/8/complaints/7/combos/0/evidence` [35,53) | 근거 수준 표현(제한적), combo 밖 시술 언급 |
| 리서페이싱 + 재생 | `/problems/8/complaints/8/combos/0/reason` [0,10)<br>`/problems/8/complaints/9/combos/0/reason` [0,10)<br>`/problems/8/complaints/10/combos/0/reason` [0,10)<br>`/problems/8/complaints/11/combos/0/reason` [0,10) | 기호(+), 결과 없는 공식형 |
| 프락셔널 후 재생 촉진 | `/problems/8/complaints/8/combos/0/evidence` [0,12)<br>`/problems/8/complaints/9/combos/0/evidence` [0,12)<br>`/problems/8/complaints/10/combos/0/evidence` [0,12)<br>`/problems/8/complaints/11/combos/0/evidence` [0,12) | 시간 순서(후), 증가 표현(촉진) |
| 유착 박리 | `/problems/8/complaints/0/procedures/1/role` [0,5)<br>`/problems/8/complaints/1/procedures/1/role` [0,5)<br>`/problems/8/complaints/2/procedures/1/role` [0,5)<br>`/problems/8/complaints/3/procedures/1/role` [0,5)<br>`/problems/8/complaints/4/procedures/1/role` [0,5)<br>`/problems/8/complaints/5/procedures/3/role` [0,5) | role 표현, 기전 표현 |
| 콜라겐 자극 | `/problems/8/complaints/0/procedures/3/role` [0,6)<br>`/problems/8/complaints/1/procedures/3/role` [0,6)<br>`/problems/8/complaints/2/procedures/3/role` [0,6)<br>`/problems/8/complaints/3/procedures/3/role` [0,6)<br>`/problems/8/complaints/4/procedures/3/role` [0,6)<br>`/problems/8/complaints/5/procedures/5/role` [0,6) | role 표현, 기전 표현 |

## 이 구획에서 연 미결

- **B-08** (B) '채널' 등 문장 안에서 지시 대상이 정의되지 않은 표현. — 영향: 기전 진술의 대상을 확정할 수 없다.
