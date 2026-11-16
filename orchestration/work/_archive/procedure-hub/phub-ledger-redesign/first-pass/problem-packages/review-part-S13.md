# S13 — /problems/12 P13 두피/탈모

[← review.md](review.md) · 범위 /problems/12 및 /problems/12/** 전체 · 소유 노드 293 · 말단 181 · 빈 값 11 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S13.txt 로 c0~c10 전부(procedures 22·combos 11·alternatives 11) 읽음. c2 의 긴 cc_detail 은 절 단위로 다시 읽고 S06 c7 과 대조함.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 3224 | `/problems/12` | `(problems 원소)` | 12 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 3225 | `/problems/12/problem_id` | `problem_id` |  | string | P13 |  |
| 3226 | `/problems/12/problem` | `problem` |  | string | 두피/탈모 |  |
| 3227 | `/problems/12/complaints` | `complaints` |  | array[11] | (배열 · 11개) |  |
| 3228 | `/problems/12/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3229 | `/problems/12/complaints/0/cc` | `cc` |  | string | 두피메조 |  |
| 3230 | `/problems/12/complaints/0/cc_detail` | `cc_detail` |  | string | 성장인자 주사 |  |
| 3231 | `/problems/12/complaints/0/cc_group` | `cc_group` |  | string | 주사치료 |  |
| 3232 | `/problems/12/complaints/0/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3233 | `/problems/12/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3234 | `/problems/12/complaints/0/procedures/0/name` | `name` |  | string | PRP/자가혈 | OB-S13-01 |
| 3235 | `/problems/12/complaints/0/procedures/0/category` | `category` |  | string | M5 |  |
| 3236 | `/problems/12/complaints/0/procedures/0/role` | `role` |  | string | 모낭 활성화 |  |
| 3237 | `/problems/12/complaints/0/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 3238 | `/problems/12/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 3239 | `/problems/12/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 3240 | `/problems/12/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3241 | `/problems/12/complaints/0/procedures/1/name` | `name` |  | string | 마이크로니들링(MTS) | OB-S13-01 |
| 3242 | `/problems/12/complaints/0/procedures/1/category` | `category` |  | string | M12 |  |
| 3243 | `/problems/12/complaints/0/procedures/1/role` | `role` |  | string | 두피 자극 |  |
| 3244 | `/problems/12/complaints/0/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3245 | `/problems/12/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3246 | `/problems/12/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3247 | `/problems/12/complaints/0/combos/0/name` | `name` |  | string | PRP + MTS |  |
| 3248 | `/problems/12/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) | OB-S13-01 |
| 3249 | `/problems/12/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | PRP | OB-S00-05 |
| 3250 | `/problems/12/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | MTS | OB-S00-05 |
| 3251 | `/problems/12/complaints/0/combos/0/reason` | `reason` |  | string | 성장인자 + 미세채널 = 침투율 향상 |  |
| 3252 | `/problems/12/complaints/0/combos/0/evidence` | `evidence` |  | string | MTS 채널로 PRP 깊이 침투 | OB-S13-10 |
| 3253 | `/problems/12/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3254 | `/problems/12/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3255 | `/problems/12/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3256 | `/problems/12/complaints/1/cc` | `cc` |  | string | 두피PRP |  |
| 3257 | `/problems/12/complaints/1/cc_detail` | `cc_detail` |  | string | 자가혈 |  |
| 3258 | `/problems/12/complaints/1/cc_group` | `cc_group` |  | string | 주사치료 |  |
| 3259 | `/problems/12/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3260 | `/problems/12/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3261 | `/problems/12/complaints/1/procedures/0/name` | `name` |  | string | PRP/자가혈 |  |
| 3262 | `/problems/12/complaints/1/procedures/0/category` | `category` |  | string | M5 |  |
| 3263 | `/problems/12/complaints/1/procedures/0/role` | `role` |  | string | 모낭 활성화 |  |
| 3264 | `/problems/12/complaints/1/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 3265 | `/problems/12/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 3266 | `/problems/12/complaints/1/procedures/0/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 3267 | `/problems/12/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3268 | `/problems/12/complaints/1/procedures/1/name` | `name` |  | string | 마이크로니들링(MTS) |  |
| 3269 | `/problems/12/complaints/1/procedures/1/category` | `category` |  | string | M12 |  |
| 3270 | `/problems/12/complaints/1/procedures/1/role` | `role` |  | string | 두피 자극 |  |
| 3271 | `/problems/12/complaints/1/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3272 | `/problems/12/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3273 | `/problems/12/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3274 | `/problems/12/complaints/1/combos/0/name` | `name` |  | string | PRP + MTS |  |
| 3275 | `/problems/12/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3276 | `/problems/12/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | PRP | OB-S00-05 |
| 3277 | `/problems/12/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | MTS | OB-S00-05 |
| 3278 | `/problems/12/complaints/1/combos/0/reason` | `reason` |  | string | 성장인자 + 미세채널 = 침투율 향상 |  |
| 3279 | `/problems/12/complaints/1/combos/0/evidence` | `evidence` |  | string | MTS 채널로 PRP 깊이 침투 |  |
| 3280 | `/problems/12/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3281 | `/problems/12/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3282 | `/problems/12/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3283 | `/problems/12/complaints/2/cc` | `cc` |  | string | 두피엑소좀 |  |
| 3284 | `/problems/12/complaints/2/cc_detail` | `cc_detail` |  | string | ASCE+ 등 엑소좀은 국내 허가된 주사 의약품이 아닌 화장품 분류 제품으로 주사·MTS 채널 전달은 미허가·위법 소지와 감염·이물육아종 위험이 있으며 발모 효과의 임상 검증은 제한적 | OB-S13-02 |
| 3285 | `/problems/12/complaints/2/cc_group` | `cc_group` |  | string | 주사치료 |  |
| 3286 | `/problems/12/complaints/2/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3287 | `/problems/12/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3288 | `/problems/12/complaints/2/procedures/0/name` | `name` |  | string | PRP/자가혈 |  |
| 3289 | `/problems/12/complaints/2/procedures/0/category` | `category` |  | string | M5 |  |
| 3290 | `/problems/12/complaints/2/procedures/0/role` | `role` |  | string | 모낭 활성화 |  |
| 3291 | `/problems/12/complaints/2/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 3292 | `/problems/12/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 3293 | `/problems/12/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 3294 | `/problems/12/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3295 | `/problems/12/complaints/2/procedures/1/name` | `name` |  | string | 마이크로니들링(MTS) |  |
| 3296 | `/problems/12/complaints/2/procedures/1/category` | `category` |  | string | M12 |  |
| 3297 | `/problems/12/complaints/2/procedures/1/role` | `role` |  | string | 두피 자극 |  |
| 3298 | `/problems/12/complaints/2/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3299 | `/problems/12/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3300 | `/problems/12/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3301 | `/problems/12/complaints/2/combos/0/name` | `name` |  | string | PRP + MTS |  |
| 3302 | `/problems/12/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3303 | `/problems/12/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | PRP | OB-S00-05 |
| 3304 | `/problems/12/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | MTS | OB-S00-05 |
| 3305 | `/problems/12/complaints/2/combos/0/reason` | `reason` |  | string | 성장인자 + 미세채널 = 침투율 향상 |  |
| 3306 | `/problems/12/complaints/2/combos/0/evidence` | `evidence` |  | string | MTS 채널로 PRP 깊이 침투 |  |
| 3307 | `/problems/12/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3308 | `/problems/12/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3309 | `/problems/12/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3310 | `/problems/12/complaints/3/cc` | `cc` |  | string | LLLT |  |
| 3311 | `/problems/12/complaints/3/cc_detail` | `cc_detail` |  | string | 저출력레이저 · LED · FDA | OB-S13-03 |
| 3312 | `/problems/12/complaints/3/cc_group` | `cc_group` |  | string | 장비치료 |  |
| 3313 | `/problems/12/complaints/3/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3314 | `/problems/12/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S13-04 |
| 3315 | `/problems/12/complaints/3/procedures/0/name` | `name` |  | string | 레이저 |  |
| 3316 | `/problems/12/complaints/3/procedures/0/category` | `category` |  | string | M8 |  |
| 3317 | `/problems/12/complaints/3/procedures/0/role` | `role` |  | string | 두피 혈류 촉진 |  |
| 3318 | `/problems/12/complaints/3/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3319 | `/problems/12/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 헤어맥스(LLLT) |  |
| 3320 | `/problems/12/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3321 | `/problems/12/complaints/3/procedures/1/name` | `name` |  | string | 마이크로니들링(MTS) |  |
| 3322 | `/problems/12/complaints/3/procedures/1/category` | `category` |  | string | M12 |  |
| 3323 | `/problems/12/complaints/3/procedures/1/role` | `role` |  | string | 두피 자극 |  |
| 3324 | `/problems/12/complaints/3/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3325 | `/problems/12/complaints/3/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3326 | `/problems/12/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3327 | `/problems/12/complaints/3/combos/0/name` | `name` |  | string | 레이저 + MTS |  |
| 3328 | `/problems/12/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3329 | `/problems/12/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 3330 | `/problems/12/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | MTS | OB-S00-05 |
| 3331 | `/problems/12/complaints/3/combos/0/reason` | `reason` |  | string | 혈류촉진 + 자극 |  |
| 3332 | `/problems/12/complaints/3/combos/0/evidence` | `evidence` |  | string | 두피 환경 개선 |  |
| 3333 | `/problems/12/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3334 | `/problems/12/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3335 | `/problems/12/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3336 | `/problems/12/complaints/4/cc` | `cc` |  | string | 두피스케일링 |  |
| 3337 | `/problems/12/complaints/4/cc_detail` | `cc_detail` |  | string | 각질/피지제거 |  |
| 3338 | `/problems/12/complaints/4/cc_group` | `cc_group` |  | string | 장비치료 |  |
| 3339 | `/problems/12/complaints/4/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3340 | `/problems/12/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S13-04 |
| 3341 | `/problems/12/complaints/4/procedures/0/name` | `name` |  | string | 레이저 |  |
| 3342 | `/problems/12/complaints/4/procedures/0/category` | `category` |  | string | M8 |  |
| 3343 | `/problems/12/complaints/4/procedures/0/role` | `role` |  | string | 두피 혈류 촉진 |  |
| 3344 | `/problems/12/complaints/4/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3345 | `/problems/12/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 헤어맥스(LLLT) |  |
| 3346 | `/problems/12/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3347 | `/problems/12/complaints/4/procedures/1/name` | `name` |  | string | 마이크로니들링(MTS) |  |
| 3348 | `/problems/12/complaints/4/procedures/1/category` | `category` |  | string | M12 |  |
| 3349 | `/problems/12/complaints/4/procedures/1/role` | `role` |  | string | 두피 자극 |  |
| 3350 | `/problems/12/complaints/4/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3351 | `/problems/12/complaints/4/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3352 | `/problems/12/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3353 | `/problems/12/complaints/4/combos/0/name` | `name` |  | string | 레이저 + MTS |  |
| 3354 | `/problems/12/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3355 | `/problems/12/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 3356 | `/problems/12/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | MTS | OB-S00-05 |
| 3357 | `/problems/12/complaints/4/combos/0/reason` | `reason` |  | string | 혈류촉진 + 자극 |  |
| 3358 | `/problems/12/complaints/4/combos/0/evidence` | `evidence` |  | string | 두피 환경 개선 |  |
| 3359 | `/problems/12/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3360 | `/problems/12/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3361 | `/problems/12/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3362 | `/problems/12/complaints/5/cc` | `cc` |  | string | MTS두피 |  |
| 3363 | `/problems/12/complaints/5/cc_detail` | `cc_detail` |  | string | 약물침투 |  |
| 3364 | `/problems/12/complaints/5/cc_group` | `cc_group` |  | string | 장비치료 |  |
| 3365 | `/problems/12/complaints/5/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3366 | `/problems/12/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S13-04 |
| 3367 | `/problems/12/complaints/5/procedures/0/name` | `name` |  | string | 레이저 |  |
| 3368 | `/problems/12/complaints/5/procedures/0/category` | `category` |  | string | M8 |  |
| 3369 | `/problems/12/complaints/5/procedures/0/role` | `role` |  | string | 두피 혈류 촉진 |  |
| 3370 | `/problems/12/complaints/5/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3371 | `/problems/12/complaints/5/procedures/0/products/0` | `(products 원소)` | 0 | string | 헤어맥스(LLLT) |  |
| 3372 | `/problems/12/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3373 | `/problems/12/complaints/5/procedures/1/name` | `name` |  | string | 마이크로니들링(MTS) |  |
| 3374 | `/problems/12/complaints/5/procedures/1/category` | `category` |  | string | M12 |  |
| 3375 | `/problems/12/complaints/5/procedures/1/role` | `role` |  | string | 두피 자극 |  |
| 3376 | `/problems/12/complaints/5/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3377 | `/problems/12/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3378 | `/problems/12/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3379 | `/problems/12/complaints/5/combos/0/name` | `name` |  | string | 레이저 + MTS |  |
| 3380 | `/problems/12/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3381 | `/problems/12/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 3382 | `/problems/12/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | MTS | OB-S00-05 |
| 3383 | `/problems/12/complaints/5/combos/0/reason` | `reason` |  | string | 혈류촉진 + 자극 |  |
| 3384 | `/problems/12/complaints/5/combos/0/evidence` | `evidence` |  | string | 두피 환경 개선 |  |
| 3385 | `/problems/12/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3386 | `/problems/12/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3387 | `/problems/12/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3388 | `/problems/12/complaints/6/cc` | `cc` |  | string | 미녹시딜 | OB-S13-06 |
| 3389 | `/problems/12/complaints/6/cc_detail` | `cc_detail` |  | string | 외용 | OB-S13-06 |
| 3390 | `/problems/12/complaints/6/cc_group` | `cc_group` |  | string | 약물치료 |  |
| 3391 | `/problems/12/complaints/6/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3392 | `/problems/12/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3393 | `/problems/12/complaints/6/procedures/0/name` | `name` |  | string | 약물치료 | OB-S13-07 |
| 3394 | `/problems/12/complaints/6/procedures/0/category` | `category` |  | string | M15 | OB-S13-05 |
| 3395 | `/problems/12/complaints/6/procedures/0/role` | `role` |  | string | 탈모 억제 |  |
| 3396 | `/problems/12/complaints/6/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3397 | `/problems/12/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3398 | `/problems/12/complaints/6/procedures/1/name` | `name` |  | string | PRP/자가혈 |  |
| 3399 | `/problems/12/complaints/6/procedures/1/category` | `category` |  | string | M5 |  |
| 3400 | `/problems/12/complaints/6/procedures/1/role` | `role` |  | string | 재생 보조 |  |
| 3401 | `/problems/12/complaints/6/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3402 | `/problems/12/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 3403 | `/problems/12/complaints/6/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3404 | `/problems/12/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3405 | `/problems/12/complaints/6/combos/0/name` | `name` |  | string | 약물 + PRP | OB-S13-08 |
| 3406 | `/problems/12/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3407 | `/problems/12/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 약물치료 | OB-S13-08 |
| 3408 | `/problems/12/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 3409 | `/problems/12/complaints/6/combos/0/reason` | `reason` |  | string | 억제 + 재생 = 이중 접근 |  |
| 3410 | `/problems/12/complaints/6/combos/0/evidence` | `evidence` |  | string | 약물+시술 병행이 효과적 |  |
| 3411 | `/problems/12/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3412 | `/problems/12/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 | OB-S13-07 |
| 3413 | `/problems/12/complaints/7` | `(complaints 원소)` | 7 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3414 | `/problems/12/complaints/7/cc` | `cc` |  | string | 피나스테리드 | OB-S13-06 |
| 3415 | `/problems/12/complaints/7/cc_detail` | `cc_detail` |  | string | 경구 | OB-S13-06 |
| 3416 | `/problems/12/complaints/7/cc_group` | `cc_group` |  | string | 약물치료 |  |
| 3417 | `/problems/12/complaints/7/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3418 | `/problems/12/complaints/7/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3419 | `/problems/12/complaints/7/procedures/0/name` | `name` |  | string | 약물치료 |  |
| 3420 | `/problems/12/complaints/7/procedures/0/category` | `category` |  | string | M15 |  |
| 3421 | `/problems/12/complaints/7/procedures/0/role` | `role` |  | string | 탈모 억제 |  |
| 3422 | `/problems/12/complaints/7/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3423 | `/problems/12/complaints/7/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3424 | `/problems/12/complaints/7/procedures/1/name` | `name` |  | string | PRP/자가혈 |  |
| 3425 | `/problems/12/complaints/7/procedures/1/category` | `category` |  | string | M5 |  |
| 3426 | `/problems/12/complaints/7/procedures/1/role` | `role` |  | string | 재생 보조 |  |
| 3427 | `/problems/12/complaints/7/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3428 | `/problems/12/complaints/7/procedures/1/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 3429 | `/problems/12/complaints/7/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3430 | `/problems/12/complaints/7/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3431 | `/problems/12/complaints/7/combos/0/name` | `name` |  | string | 약물 + PRP |  |
| 3432 | `/problems/12/complaints/7/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3433 | `/problems/12/complaints/7/combos/0/combo/0` | `(combo 원소)` | 0 | string | 약물치료 |  |
| 3434 | `/problems/12/complaints/7/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 3435 | `/problems/12/complaints/7/combos/0/reason` | `reason` |  | string | 억제 + 재생 = 이중 접근 |  |
| 3436 | `/problems/12/complaints/7/combos/0/evidence` | `evidence` |  | string | 약물+시술 병행이 효과적 |  |
| 3437 | `/problems/12/complaints/7/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3438 | `/problems/12/complaints/7/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3439 | `/problems/12/complaints/8` | `(complaints 원소)` | 8 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3440 | `/problems/12/complaints/8/cc` | `cc` |  | string | 두타스테리드 | OB-S13-06 |
| 3441 | `/problems/12/complaints/8/cc_detail` | `cc_detail` |  | string | 경구 |  |
| 3442 | `/problems/12/complaints/8/cc_group` | `cc_group` |  | string | 약물치료 |  |
| 3443 | `/problems/12/complaints/8/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3444 | `/problems/12/complaints/8/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3445 | `/problems/12/complaints/8/procedures/0/name` | `name` |  | string | 약물치료 |  |
| 3446 | `/problems/12/complaints/8/procedures/0/category` | `category` |  | string | M15 |  |
| 3447 | `/problems/12/complaints/8/procedures/0/role` | `role` |  | string | 탈모 억제 |  |
| 3448 | `/problems/12/complaints/8/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3449 | `/problems/12/complaints/8/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3450 | `/problems/12/complaints/8/procedures/1/name` | `name` |  | string | PRP/자가혈 |  |
| 3451 | `/problems/12/complaints/8/procedures/1/category` | `category` |  | string | M5 |  |
| 3452 | `/problems/12/complaints/8/procedures/1/role` | `role` |  | string | 재생 보조 |  |
| 3453 | `/problems/12/complaints/8/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3454 | `/problems/12/complaints/8/procedures/1/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 3455 | `/problems/12/complaints/8/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3456 | `/problems/12/complaints/8/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3457 | `/problems/12/complaints/8/combos/0/name` | `name` |  | string | 약물 + PRP |  |
| 3458 | `/problems/12/complaints/8/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3459 | `/problems/12/complaints/8/combos/0/combo/0` | `(combo 원소)` | 0 | string | 약물치료 |  |
| 3460 | `/problems/12/complaints/8/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 3461 | `/problems/12/complaints/8/combos/0/reason` | `reason` |  | string | 억제 + 재생 = 이중 접근 |  |
| 3462 | `/problems/12/complaints/8/combos/0/evidence` | `evidence` |  | string | 약물+시술 병행이 효과적 |  |
| 3463 | `/problems/12/complaints/8/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3464 | `/problems/12/complaints/8/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3465 | `/problems/12/complaints/9` | `(complaints 원소)` | 9 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3466 | `/problems/12/complaints/9/cc` | `cc` |  | string | FUE | OB-S13-09 |
| 3467 | `/problems/12/complaints/9/cc_detail` | `cc_detail` |  | string | 모낭단위추출 | OB-S13-09 |
| 3468 | `/problems/12/complaints/9/cc_group` | `cc_group` |  | string | 모발이식 |  |
| 3469 | `/problems/12/complaints/9/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3470 | `/problems/12/complaints/9/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3471 | `/problems/12/complaints/9/procedures/0/name` | `name` |  | string | 모발이식 |  |
| 3472 | `/problems/12/complaints/9/procedures/0/category` | `category` |  | string | M15 | OB-S13-05 |
| 3473 | `/problems/12/complaints/9/procedures/0/role` | `role` |  | string | 영구적 모발 복원 | OB-S13-11 |
| 3474 | `/problems/12/complaints/9/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3475 | `/problems/12/complaints/9/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3476 | `/problems/12/complaints/9/procedures/1/name` | `name` |  | string | PRP/자가혈 |  |
| 3477 | `/problems/12/complaints/9/procedures/1/category` | `category` |  | string | M5 |  |
| 3478 | `/problems/12/complaints/9/procedures/1/role` | `role` |  | string | 생착률 향상 |  |
| 3479 | `/problems/12/complaints/9/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3480 | `/problems/12/complaints/9/procedures/1/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 3481 | `/problems/12/complaints/9/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3482 | `/problems/12/complaints/9/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3483 | `/problems/12/complaints/9/combos/0/name` | `name` |  | string | 모발이식 + PRP |  |
| 3484 | `/problems/12/complaints/9/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3485 | `/problems/12/complaints/9/combos/0/combo/0` | `(combo 원소)` | 0 | string | 모발이식 |  |
| 3486 | `/problems/12/complaints/9/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 3487 | `/problems/12/complaints/9/combos/0/reason` | `reason` |  | string | 이식 + 성장인자 = 생착률 향상 |  |
| 3488 | `/problems/12/complaints/9/combos/0/evidence` | `evidence` |  | string | PRP가 이식모 생존율 높임 |  |
| 3489 | `/problems/12/complaints/9/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3490 | `/problems/12/complaints/9/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 3491 | `/problems/12/complaints/10` | `(complaints 원소)` | 10 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3492 | `/problems/12/complaints/10/cc` | `cc` |  | string | FUT | OB-S13-09 |
| 3493 | `/problems/12/complaints/10/cc_detail` | `cc_detail` |  | string | 모낭단위이식 | OB-S13-09 |
| 3494 | `/problems/12/complaints/10/cc_group` | `cc_group` |  | string | 모발이식 |  |
| 3495 | `/problems/12/complaints/10/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3496 | `/problems/12/complaints/10/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3497 | `/problems/12/complaints/10/procedures/0/name` | `name` |  | string | 모발이식 |  |
| 3498 | `/problems/12/complaints/10/procedures/0/category` | `category` |  | string | M15 |  |
| 3499 | `/problems/12/complaints/10/procedures/0/role` | `role` |  | string | 영구적 모발 복원 |  |
| 3500 | `/problems/12/complaints/10/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3501 | `/problems/12/complaints/10/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3502 | `/problems/12/complaints/10/procedures/1/name` | `name` |  | string | PRP/자가혈 |  |
| 3503 | `/problems/12/complaints/10/procedures/1/category` | `category` |  | string | M5 |  |
| 3504 | `/problems/12/complaints/10/procedures/1/role` | `role` |  | string | 생착률 향상 |  |
| 3505 | `/problems/12/complaints/10/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3506 | `/problems/12/complaints/10/procedures/1/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 3507 | `/problems/12/complaints/10/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3508 | `/problems/12/complaints/10/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3509 | `/problems/12/complaints/10/combos/0/name` | `name` |  | string | 모발이식 + PRP |  |
| 3510 | `/problems/12/complaints/10/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3511 | `/problems/12/complaints/10/combos/0/combo/0` | `(combo 원소)` | 0 | string | 모발이식 |  |
| 3512 | `/problems/12/complaints/10/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 3513 | `/problems/12/complaints/10/combos/0/reason` | `reason` |  | string | 이식 + 성장인자 = 생착률 향상 |  |
| 3514 | `/problems/12/complaints/10/combos/0/evidence` | `evidence` |  | string | PRP가 이식모 생존율 높임 |  |
| 3515 | `/problems/12/complaints/10/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3516 | `/problems/12/complaints/10/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S13-01 | I | `/problems/12/complaints/0/combos/0/combo`<br>`/problems/12/complaints/0/procedures/0/name`<br>`/problems/12/complaints/0/procedures/1/name` | combo 'PRP + MTS' 의 원소 'PRP'·'MTS' 가 procedures name 'PRP/자가혈'·'마이크로니들링(MTS)' 과 다르다(I-01 같은 유형). 'MTS' 는 여기서 procedures name 괄호 안에 병기돼 있다. |
| OB-S13-02 | P | `/problems/12/complaints/2/cc_detail`<br>`/problems/5/complaints/7/cc_detail` | c2 cc_detail 은 S06 c7 cc_detail 과 거의 같은 규제·안전 문장이다. 차이: 앞부분이 'ASCE+ 등' (S06: '리쥬란/엑소좀.'), 끝이 '발모 효과의 임상 검증은 제한적' (S06: '미용 효과의'). 템플릿 문장에 대상만 바꾼 변형으로 보인다. 'ASCE+' 는 '+' 를 포함한 제품 표기(K-03). |
| OB-S13-03 | B | `/problems/12/complaints/3/cc_detail` | cc_detail '저출력레이저 · LED · FDA' — 'FDA' 가 무엇에 관한 표기(승인 등)인지 문장 성분이 없다(B-09). |
| OB-S13-04 | B | `/problems/12/complaints/3/procedures/0`<br>`/problems/12/complaints/4/procedures/0`<br>`/problems/12/complaints/5/procedures/0` | c3~c5(LLLT·두피스케일링·MTS두피)의 procedures·combos·alternatives 가 같다. c4 cc '두피스케일링'(cc_detail '각질/피지제거') 에 해당하는 처치는 procedures 에 없다(B-02 · I-03 같은 유형). |
| OB-S13-05 | P | `/problems/12/complaints/6/procedures/0/category`<br>`/problems/12/complaints/9/procedures/0/category` | category 'M15' 가 '약물치료'·'모발이식' 에도 쓰인다. 원장 전체에서 M15 에 붙은 name: 반영구화장·메디컬스킨케어·병변내 스테로이드주사·약물치료·모발이식(F-01 taxonomy 대조 대상). |
| OB-S13-06 | P | `/problems/12/complaints/6/cc`<br>`/problems/12/complaints/7/cc`<br>`/problems/12/complaints/8/cc`<br>`/problems/12/complaints/6/cc_detail`<br>`/problems/12/complaints/7/cc_detail` | cc 가 약물 성분명(미녹시딜·피나스테리드·두타스테리드)이고 cc_detail 이 투여 경로('외용'·'경구')다. cc 의 정보 종류가 problem 마다 다르다(B-01 과 연결). |
| OB-S13-07 | P | `/problems/12/complaints/6/alternatives/0`<br>`/problems/12/complaints/6/procedures/0/name` | 약물치료가 procedures 에 있는 complaint 에도 alternatives '약물치료 병행 추천' 이 반복된다(템플릿 반복). |
| OB-S13-08 | I | `/problems/12/complaints/6/combos/0/name`<br>`/problems/12/complaints/6/combos/0/combo/0` | combo name '약물 + PRP' ↔ 원소 '약물치료' 표기 차이(I-02 같은 유형). |
| OB-S13-09 | P | `/problems/12/complaints/9/cc`<br>`/problems/12/complaints/9/cc_detail`<br>`/problems/12/complaints/10/cc`<br>`/problems/12/complaints/10/cc_detail` | cc 'FUE'·'FUT' 옆 cc_detail '모낭단위추출'·'모낭단위이식' 은 약어의 풀이처럼 놓여 있으나 원문이 풀이라고 명시하지 않는다. 원문 병치로만 기록한다. |
| OB-S13-10 | P | `/problems/12/complaints/0/combos/0/evidence`<br>`/problems/8/complaints/0/combos/0/evidence` | 'MTS 채널로 PRP 깊이 침투' — S09 의 'PRP가 채널로 깊이 침투' 에 없던 '채널' 의 수식(MTS)이 여기에는 있다(B-08 과 대조). |
| OB-S13-11 | P | `/problems/12/complaints/9/procedures/0/role` | role '영구적 모발 복원' — 영구성 진술(S10 의 영구성 한정 문장과 대조 대상, I-08 참고). |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 성장인자 주사 | `/problems/12/complaints/0/cc_detail` [0,7) | 재료+시술 표현 |
| ASCE+ 등 | `/problems/12/complaints/2/cc_detail` [0,7) | 제품명 표현, 이름 안의 기호(+), 열린 목록(등) |
| 엑소좀은 국내 허가된 주사 의약품이 아닌 화장품 분류 제품으로 | `/problems/12/complaints/2/cc_detail` [8,42) | 부정(아닌), 허가 상태 진술, 범위(국내) |
| 주사·MTS 채널 전달은 미허가·위법 소지와 감염·이물육아종 위험이 있으며 | `/problems/12/complaints/2/cc_detail` [43,84) | 허가 상태 진술, 법적 진술(위법 소지), 위험 표현, 기호(·), 약어(MTS) |
| 발모 효과의 임상 검증은 제한적 | `/problems/12/complaints/2/cc_detail` [85,102) | 근거 수준 표현(제한적) |
| 저출력레이저 · LED · FDA | `/problems/12/complaints/3/cc_detail` [0,18) | 기호(· 띄어 씀), 정도 수식(저출력), 약어, 문장 성분 생략 |
| 각질/피지제거 | `/problems/12/complaints/4/cc_detail` [0,7) | 기호(/), 효과 표현 |
| 약물침투 | `/problems/12/complaints/5/cc_detail` [0,4) | 붙여 쓴 복합어, 기전 표현 |
| 모낭단위추출 | `/problems/12/complaints/9/cc_detail` [0,6) | 붙여 쓴 복합어, 방법 표현 |
| 모낭단위이식 | `/problems/12/complaints/10/cc_detail` [0,6) | 붙여 쓴 복합어, 방법 표현 |
| 마이크로니들링(MTS) | `/problems/12/complaints/0/procedures/1/name` [0,12)<br>`/problems/12/complaints/1/procedures/1/name` [0,12)<br>`/problems/12/complaints/2/procedures/1/name` [0,12)<br>`/problems/12/complaints/3/procedures/1/name` [0,12)<br>`/problems/12/complaints/4/procedures/1/name` [0,12)<br>`/problems/12/complaints/5/procedures/1/name` [0,12) | 시술명 표현, 괄호 약어 병기 |
| 헤어맥스(LLLT) | `/problems/12/complaints/3/procedures/0/products/0` [0,10)<br>`/problems/12/complaints/4/procedures/0/products/0` [0,10)<br>`/problems/12/complaints/5/procedures/0/products/0` [0,10) | 제품명 표현, 괄호 약어 병기 |
| 성장인자 + 미세채널 = 침투율 향상 | `/problems/12/complaints/0/combos/0/reason` [0,20)<br>`/problems/12/complaints/1/combos/0/reason` [0,20)<br>`/problems/12/complaints/2/combos/0/reason` [0,20) | 공식형 문장, 기호(+), 기호(=), 증가 표현 |
| MTS 채널로 PRP 깊이 침투 | `/problems/12/complaints/0/combos/0/evidence` [0,17)<br>`/problems/12/complaints/1/combos/0/evidence` [0,17)<br>`/problems/12/complaints/2/combos/0/evidence` [0,17) | 기전 진술, 수단(-로), 정도(깊이), 약어 |
| 혈류촉진 + 자극 | `/problems/12/complaints/3/combos/0/reason` [0,9)<br>`/problems/12/complaints/4/combos/0/reason` [0,9)<br>`/problems/12/complaints/5/combos/0/reason` [0,9) | 기호(+), 결과 없는 공식형 |
| 두피 환경 개선 | `/problems/12/complaints/3/combos/0/evidence` [0,8)<br>`/problems/12/complaints/4/combos/0/evidence` [0,8)<br>`/problems/12/complaints/5/combos/0/evidence` [0,8) | 효과 표현(막연) |
| 두피 혈류 촉진 | `/problems/12/complaints/3/procedures/0/role` [0,8)<br>`/problems/12/complaints/4/procedures/0/role` [0,8)<br>`/problems/12/complaints/5/procedures/0/role` [0,8) | role 표현, 증가 표현(촉진) |
| 모낭 활성화 | `/problems/12/complaints/0/procedures/0/role` [0,6)<br>`/problems/12/complaints/1/procedures/0/role` [0,6)<br>`/problems/12/complaints/2/procedures/0/role` [0,6) | role 표현, 기전 표현 |
| 억제 + 재생 = 이중 접근 | `/problems/12/complaints/6/combos/0/reason` [0,15)<br>`/problems/12/complaints/7/combos/0/reason` [0,15)<br>`/problems/12/complaints/8/combos/0/reason` [0,15) | 공식형 문장, 기호(+), 기호(=), 정도 표현(이중) |
| 약물+시술 병행이 효과적 | `/problems/12/complaints/6/combos/0/evidence` [0,13)<br>`/problems/12/complaints/7/combos/0/evidence` [0,13)<br>`/problems/12/complaints/8/combos/0/evidence` [0,13) | 기호(+ 공백 없음), 병행, 효과 판단 |
| 탈모 억제 | `/problems/12/complaints/6/procedures/0/role` [0,5)<br>`/problems/12/complaints/7/procedures/0/role` [0,5)<br>`/problems/12/complaints/8/procedures/0/role` [0,5) | role 표현, 억제 표현 |
| 영구적 모발 복원 | `/problems/12/complaints/9/procedures/0/role` [0,9)<br>`/problems/12/complaints/10/procedures/0/role` [0,9) | role 표현, 정도 수식(영구적) |
| 이식 + 성장인자 = 생착률 향상 | `/problems/12/complaints/9/combos/0/reason` [0,18)<br>`/problems/12/complaints/10/combos/0/reason` [0,18) | 공식형 문장, 기호(+), 기호(=), 증가 표현 |
| PRP가 이식모 생존율 높임 | `/problems/12/complaints/9/combos/0/evidence` [0,15)<br>`/problems/12/complaints/10/combos/0/evidence` [0,15) | 기전 진술, 증가 표현 |
| 약물치료 병행 추천 | `/problems/12/complaints/0/alternatives/0` [0,10)<br>`/problems/12/complaints/1/alternatives/0` [0,10)<br>`/problems/12/complaints/2/alternatives/0` [0,10)<br>`/problems/12/complaints/3/alternatives/0` [0,10)<br>`/problems/12/complaints/4/alternatives/0` [0,10)<br>`/problems/12/complaints/5/alternatives/0` [0,10)<br>`/problems/12/complaints/6/alternatives/0` [0,10)<br>`/problems/12/complaints/7/alternatives/0` [0,10)<br>`/problems/12/complaints/8/alternatives/0` [0,10)<br>`/problems/12/complaints/9/alternatives/0` [0,10)<br>`/problems/12/complaints/10/alternatives/0` [0,10) | 병행, 권고(추천) |

## 이 구획에서 연 미결

- **B-09** (B) 'FDA' 가 문장 성분 없이 나열돼 무엇에 관한 표기인지 알 수 없다. — 영향: 허가 정보로 해석하면 근거 없는 의미 부여.
