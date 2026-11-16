# S05 — /problems/4 P5 색소/미백

[← review.md](review.md) · 범위 /problems/4 및 /problems/4/** 전체 · 소유 노드 262 · 말단 172 · 빈 값 2 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S05.txt 로 c0~c7 전부(procedures 18·combos 10·alternatives 10) 읽음. c0~c2 의 긴 evidence, c7 의 긴 cc_detail 은 문장 단위로 다시 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 1249 | `/problems/4` | `(problems 원소)` | 4 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 1250 | `/problems/4/problem_id` | `problem_id` |  | string | P5 |  |
| 1251 | `/problems/4/problem` | `problem` |  | string | 색소/미백 |  |
| 1252 | `/problems/4/complaints` | `complaints` |  | array[8] | (배열 · 8개) |  |
| 1253 | `/problems/4/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1254 | `/problems/4/complaints/0/cc` | `cc` |  | string | 레이저토닝 |  |
| 1255 | `/problems/4/complaints/0/cc_detail` | `cc_detail` |  | string | 1064nm 반복 | OB-S05-12 |
| 1256 | `/problems/4/complaints/0/cc_group` | `cc_group` |  | string | 기미 |  |
| 1257 | `/problems/4/complaints/0/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1258 | `/problems/4/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1259 | `/problems/4/complaints/0/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1260 | `/problems/4/complaints/0/procedures/0/category` | `category` |  | string | M8 |  |
| 1261 | `/problems/4/complaints/0/procedures/0/role` | `role` |  | string | 색소 파괴 | OB-S06-11 |
| 1262 | `/problems/4/complaints/0/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1263 | `/problems/4/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1264 | `/problems/4/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 1265 | `/problems/4/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1266 | `/problems/4/complaints/0/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1267 | `/problems/4/complaints/0/procedures/1/category` | `category` |  | string | M4 |  |
| 1268 | `/problems/4/complaints/0/procedures/1/role` | `role` |  | string | 재생·톤개선 |  |
| 1269 | `/problems/4/complaints/0/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1270 | `/problems/4/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1271 | `/problems/4/complaints/0/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 1272 | `/problems/4/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1273 | `/problems/4/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1274 | `/problems/4/complaints/0/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1275 | `/problems/4/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1276 | `/problems/4/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1277 | `/problems/4/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1278 | `/problems/4/complaints/0/combos/0/reason` | `reason` |  | string | 색소파괴 + 재생 = 미백+피부결 |  |
| 1279 | `/problems/4/complaints/0/combos/0/evidence` | `evidence` |  | string | 스킨부스터는 시술 후 재생·보습을 보조하나 색소침착(PIH) 예방 효과의 임상 근거는 제한적임(근거 확립된 PIH 예방책은 국소 스테로이드·트라넥삼산). 저출력 1064nm 토닝은 누적 조사 과다·짧은 간격 시 반동성 색소침착·반점상 저색소증 위험이 있어 보수적 세션 간격(2-4주) 필요. | OB-S05-01, OB-S05-02, OB-S05-03, OB-S05-12 |
| 1280 | `/problems/4/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1281 | `/problems/4/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 자외선 차단 필수 |  |
| 1282 | `/problems/4/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1283 | `/problems/4/complaints/1/cc` | `cc` |  | string | 피코토닝 |  |
| 1284 | `/problems/4/complaints/1/cc_detail` | `cc_detail` |  | string | 피코초 정밀 |  |
| 1285 | `/problems/4/complaints/1/cc_group` | `cc_group` |  | string | 기미 |  |
| 1286 | `/problems/4/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1287 | `/problems/4/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1288 | `/problems/4/complaints/1/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1289 | `/problems/4/complaints/1/procedures/0/category` | `category` |  | string | M8 |  |
| 1290 | `/problems/4/complaints/1/procedures/0/role` | `role` |  | string | 색소 파괴 |  |
| 1291 | `/problems/4/complaints/1/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1292 | `/problems/4/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1293 | `/problems/4/complaints/1/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 1294 | `/problems/4/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1295 | `/problems/4/complaints/1/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1296 | `/problems/4/complaints/1/procedures/1/category` | `category` |  | string | M4 |  |
| 1297 | `/problems/4/complaints/1/procedures/1/role` | `role` |  | string | 재생·톤개선 |  |
| 1298 | `/problems/4/complaints/1/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1299 | `/problems/4/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1300 | `/problems/4/complaints/1/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 1301 | `/problems/4/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1302 | `/problems/4/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1303 | `/problems/4/complaints/1/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1304 | `/problems/4/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1305 | `/problems/4/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1306 | `/problems/4/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1307 | `/problems/4/complaints/1/combos/0/reason` | `reason` |  | string | 색소파괴 + 재생 = 미백+피부결 |  |
| 1308 | `/problems/4/complaints/1/combos/0/evidence` | `evidence` |  | string | 스킨부스터는 시술 후 재생·보습을 보조하나 색소침착(PIH) 예방 효과의 임상 근거는 제한적임(근거 확립된 PIH 예방책은 국소 스테로이드·트라넥삼산). 저출력 1064nm 토닝은 누적 조사 과다·짧은 간격 시 반동성 색소침착·반점상 저색소증 위험이 있어 보수적 세션 간격(2-4주) 필요. | OB-S05-01 |
| 1309 | `/problems/4/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1310 | `/problems/4/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 자외선 차단 필수 |  |
| 1311 | `/problems/4/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1312 | `/problems/4/complaints/2/cc` | `cc` |  | string | 미백필링 | OB-S05-04 |
| 1313 | `/problems/4/complaints/2/cc_detail` | `cc_detail` |  | string | 트라넥삼산 등 | OB-S05-04 |
| 1314 | `/problems/4/complaints/2/cc_group` | `cc_group` |  | string | 기미 |  |
| 1315 | `/problems/4/complaints/2/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1316 | `/problems/4/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1317 | `/problems/4/complaints/2/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1318 | `/problems/4/complaints/2/procedures/0/category` | `category` |  | string | M8 |  |
| 1319 | `/problems/4/complaints/2/procedures/0/role` | `role` |  | string | 색소 파괴 |  |
| 1320 | `/problems/4/complaints/2/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1321 | `/problems/4/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1322 | `/problems/4/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 1323 | `/problems/4/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1324 | `/problems/4/complaints/2/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1325 | `/problems/4/complaints/2/procedures/1/category` | `category` |  | string | M4 |  |
| 1326 | `/problems/4/complaints/2/procedures/1/role` | `role` |  | string | 재생·톤개선 |  |
| 1327 | `/problems/4/complaints/2/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1328 | `/problems/4/complaints/2/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1329 | `/problems/4/complaints/2/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 1330 | `/problems/4/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1331 | `/problems/4/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1332 | `/problems/4/complaints/2/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1333 | `/problems/4/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1334 | `/problems/4/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1335 | `/problems/4/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1336 | `/problems/4/complaints/2/combos/0/reason` | `reason` |  | string | 색소파괴 + 재생 = 미백+피부결 |  |
| 1337 | `/problems/4/complaints/2/combos/0/evidence` | `evidence` |  | string | 스킨부스터는 시술 후 재생·보습을 보조하나 색소침착(PIH) 예방 효과의 임상 근거는 제한적임(근거 확립된 PIH 예방책은 국소 스테로이드·트라넥삼산). 저출력 1064nm 토닝은 누적 조사 과다·짧은 간격 시 반동성 색소침착·반점상 저색소증 위험이 있어 보수적 세션 간격(2-4주) 필요. | OB-S05-01 |
| 1338 | `/problems/4/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1339 | `/problems/4/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 자외선 차단 필수 |  |
| 1340 | `/problems/4/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1341 | `/problems/4/complaints/3/cc` | `cc` |  | string | 피코레이저 |  |
| 1342 | `/problems/4/complaints/3/cc_detail` | `cc_detail` |  | string | 1~2회 집중 | OB-S05-11 |
| 1343 | `/problems/4/complaints/3/cc_group` | `cc_group` |  | string | 주근깨/잡티 |  |
| 1344 | `/problems/4/complaints/3/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1345 | `/problems/4/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1346 | `/problems/4/complaints/3/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1347 | `/problems/4/complaints/3/procedures/0/category` | `category` |  | string | M8 |  |
| 1348 | `/problems/4/complaints/3/procedures/0/role` | `role` |  | string | 색소 파괴 |  |
| 1349 | `/problems/4/complaints/3/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1350 | `/problems/4/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1351 | `/problems/4/complaints/3/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 1352 | `/problems/4/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1353 | `/problems/4/complaints/3/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1354 | `/problems/4/complaints/3/procedures/1/category` | `category` |  | string | M4 |  |
| 1355 | `/problems/4/complaints/3/procedures/1/role` | `role` |  | string | 재생·톤개선 |  |
| 1356 | `/problems/4/complaints/3/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1357 | `/problems/4/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1358 | `/problems/4/complaints/3/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 1359 | `/problems/4/complaints/3/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1360 | `/problems/4/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1361 | `/problems/4/complaints/3/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1362 | `/problems/4/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1363 | `/problems/4/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1364 | `/problems/4/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1365 | `/problems/4/complaints/3/combos/0/reason` | `reason` |  | string | 색소파괴 + 재생 = 미백+피부결 |  |
| 1366 | `/problems/4/complaints/3/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진으로 색소침착 방지 | OB-S05-02 |
| 1367 | `/problems/4/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1368 | `/problems/4/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 자외선 차단 필수 |  |
| 1369 | `/problems/4/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1370 | `/problems/4/complaints/4/cc` | `cc` |  | string | IPL | OB-S05-04 |
| 1371 | `/problems/4/complaints/4/cc_detail` | `cc_detail` |  | string | 광범위 색소 |  |
| 1372 | `/problems/4/complaints/4/cc_group` | `cc_group` |  | string | 주근깨/잡티 |  |
| 1373 | `/problems/4/complaints/4/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1374 | `/problems/4/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1375 | `/problems/4/complaints/4/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1376 | `/problems/4/complaints/4/procedures/0/category` | `category` |  | string | M8 |  |
| 1377 | `/problems/4/complaints/4/procedures/0/role` | `role` |  | string | 색소 파괴 |  |
| 1378 | `/problems/4/complaints/4/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1379 | `/problems/4/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1380 | `/problems/4/complaints/4/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 1381 | `/problems/4/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1382 | `/problems/4/complaints/4/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1383 | `/problems/4/complaints/4/procedures/1/category` | `category` |  | string | M4 |  |
| 1384 | `/problems/4/complaints/4/procedures/1/role` | `role` |  | string | 재생·톤개선 |  |
| 1385 | `/problems/4/complaints/4/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1386 | `/problems/4/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1387 | `/problems/4/complaints/4/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 1388 | `/problems/4/complaints/4/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1389 | `/problems/4/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1390 | `/problems/4/complaints/4/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1391 | `/problems/4/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1392 | `/problems/4/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1393 | `/problems/4/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1394 | `/problems/4/complaints/4/combos/0/reason` | `reason` |  | string | 색소파괴 + 재생 = 미백+피부결 |  |
| 1395 | `/problems/4/complaints/4/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진으로 색소침착 방지 |  |
| 1396 | `/problems/4/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1397 | `/problems/4/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 자외선 차단 필수 |  |
| 1398 | `/problems/4/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1399 | `/problems/4/complaints/5/cc` | `cc` |  | string | 피코/Q스위치 | OB-S05-04 |
| 1400 | `/problems/4/complaints/5/cc_detail` | `cc_detail` |  | string | 진피색소 |  |
| 1401 | `/problems/4/complaints/5/cc_group` | `cc_group` |  | string | 오타모반/ABNOM | OB-S05-10 |
| 1402 | `/problems/4/complaints/5/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1403 | `/problems/4/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1404 | `/problems/4/complaints/5/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1405 | `/problems/4/complaints/5/procedures/0/category` | `category` |  | string | M8 |  |
| 1406 | `/problems/4/complaints/5/procedures/0/role` | `role` |  | string | 색소 파괴 |  |
| 1407 | `/problems/4/complaints/5/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1408 | `/problems/4/complaints/5/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1409 | `/problems/4/complaints/5/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 1410 | `/problems/4/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1411 | `/problems/4/complaints/5/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1412 | `/problems/4/complaints/5/procedures/1/category` | `category` |  | string | M4 |  |
| 1413 | `/problems/4/complaints/5/procedures/1/role` | `role` |  | string | 재생·톤개선 |  |
| 1414 | `/problems/4/complaints/5/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1415 | `/problems/4/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1416 | `/problems/4/complaints/5/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 1417 | `/problems/4/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1418 | `/problems/4/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1419 | `/problems/4/complaints/5/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1420 | `/problems/4/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1421 | `/problems/4/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1422 | `/problems/4/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1423 | `/problems/4/complaints/5/combos/0/reason` | `reason` |  | string | 색소파괴 + 재생 = 미백+피부결 |  |
| 1424 | `/problems/4/complaints/5/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진으로 색소침착 방지 |  |
| 1425 | `/problems/4/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1426 | `/problems/4/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 자외선 차단 필수 |  |
| 1427 | `/problems/4/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1428 | `/problems/4/complaints/6/cc` | `cc` |  | string | 백옥주사 |  |
| 1429 | `/problems/4/complaints/6/cc_detail` | `cc_detail` |  | string | 글루타치온 IV |  |
| 1430 | `/problems/4/complaints/6/cc_group` | `cc_group` |  | string | 전체미백 |  |
| 1431 | `/problems/4/complaints/6/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 1432 | `/problems/4/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1433 | `/problems/4/complaints/6/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1434 | `/problems/4/complaints/6/procedures/0/category` | `category` |  | string | M8 |  |
| 1435 | `/problems/4/complaints/6/procedures/0/role` | `role` |  | string | 색소 파괴 |  |
| 1436 | `/problems/4/complaints/6/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1437 | `/problems/4/complaints/6/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1438 | `/problems/4/complaints/6/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 1439 | `/problems/4/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1440 | `/problems/4/complaints/6/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1441 | `/problems/4/complaints/6/procedures/1/category` | `category` |  | string | M4 |  |
| 1442 | `/problems/4/complaints/6/procedures/1/role` | `role` |  | string | 재생·톤개선 |  |
| 1443 | `/problems/4/complaints/6/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1444 | `/problems/4/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1445 | `/problems/4/complaints/6/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 1446 | `/problems/4/complaints/6/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1447 | `/problems/4/complaints/6/procedures/2/name` | `name` |  | string | 미백주사 |  |
| 1448 | `/problems/4/complaints/6/procedures/2/category` | `category` |  | string | M16 |  |
| 1449 | `/problems/4/complaints/6/procedures/2/role` | `role` |  | string | 미백 목적 허가 외 사용(유효성 근거 제한) | OB-S05-07 |
| 1450 | `/problems/4/complaints/6/procedures/2/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 1451 | `/problems/4/complaints/6/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1452 | `/problems/4/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1453 | `/problems/4/complaints/6/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1454 | `/problems/4/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1455 | `/problems/4/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1456 | `/problems/4/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1457 | `/problems/4/complaints/6/combos/0/reason` | `reason` |  | string | 색소파괴 + 재생 = 미백+피부결 |  |
| 1458 | `/problems/4/complaints/6/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진으로 색소침착 방지 |  |
| 1459 | `/problems/4/complaints/6/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1460 | `/problems/4/complaints/6/combos/1/name` | `name` |  | string | 레이저 + 미백주사 |  |
| 1461 | `/problems/4/complaints/6/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1462 | `/problems/4/complaints/6/combos/1/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1463 | `/problems/4/complaints/6/combos/1/combo/1` | `(combo 원소)` | 1 | string | 미백주사 |  |
| 1464 | `/problems/4/complaints/6/combos/1/reason` | `reason` |  | string | 미용 목적 정맥 글루타치온/비타민C의 미백 유효성 근거는 부족하며 단기 효과에 그칠 수 있음 | OB-S05-06 |
| 1465 | `/problems/4/complaints/6/combos/1/evidence` | `evidence` |  | string | 근거 없는 시너지 주장은 배제하며, 아나필락시스·간/신장 부담 등 안전성 경고 필요 | OB-S05-06, OB-S05-09 |
| 1466 | `/problems/4/complaints/6/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 1467 | `/problems/4/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 자외선 차단 필수 |  |
| 1468 | `/problems/4/complaints/6/alternatives/1` | `(alternatives 원소)` | 1 | string | 정맥 미백주사는 근거 부족·허가 외 사용과 알레르기·아나필락시스, 간·신장 부담 위험을 사전 고지 | OB-S05-08, OB-S05-09 |
| 1469 | `/problems/4/complaints/7` | `(complaints 원소)` | 7 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1470 | `/problems/4/complaints/7/cc` | `cc` |  | string | 비타민C주사 |  |
| 1471 | `/problems/4/complaints/7/cc_detail` | `cc_detail` |  | string | 항산화/미백. 고용량 정맥 투여 전 G6PD 결핍 스크리닝 권고(급성 용혈 위험), 고용량·반복 투여 시 옥살산 신병증·급성신손상 위험 | OB-S05-05 |
| 1472 | `/problems/4/complaints/7/cc_group` | `cc_group` |  | string | 전체미백 |  |
| 1473 | `/problems/4/complaints/7/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 1474 | `/problems/4/complaints/7/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1475 | `/problems/4/complaints/7/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1476 | `/problems/4/complaints/7/procedures/0/category` | `category` |  | string | M8 |  |
| 1477 | `/problems/4/complaints/7/procedures/0/role` | `role` |  | string | 색소 파괴 |  |
| 1478 | `/problems/4/complaints/7/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1479 | `/problems/4/complaints/7/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1480 | `/problems/4/complaints/7/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 1481 | `/problems/4/complaints/7/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1482 | `/problems/4/complaints/7/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1483 | `/problems/4/complaints/7/procedures/1/category` | `category` |  | string | M4 |  |
| 1484 | `/problems/4/complaints/7/procedures/1/role` | `role` |  | string | 재생·톤개선 |  |
| 1485 | `/problems/4/complaints/7/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1486 | `/problems/4/complaints/7/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1487 | `/problems/4/complaints/7/procedures/1/products/1` | `(products 원소)` | 1 | string | 리쥬란 HB+ |  |
| 1488 | `/problems/4/complaints/7/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1489 | `/problems/4/complaints/7/procedures/2/name` | `name` |  | string | 미백주사 |  |
| 1490 | `/problems/4/complaints/7/procedures/2/category` | `category` |  | string | M16 |  |
| 1491 | `/problems/4/complaints/7/procedures/2/role` | `role` |  | string | 미백 목적 허가 외 사용(유효성 근거 제한) | OB-S05-07 |
| 1492 | `/problems/4/complaints/7/procedures/2/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 1493 | `/problems/4/complaints/7/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1494 | `/problems/4/complaints/7/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1495 | `/problems/4/complaints/7/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1496 | `/problems/4/complaints/7/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1497 | `/problems/4/complaints/7/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1498 | `/problems/4/complaints/7/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1499 | `/problems/4/complaints/7/combos/0/reason` | `reason` |  | string | 색소파괴 + 재생 = 미백+피부결 |  |
| 1500 | `/problems/4/complaints/7/combos/0/evidence` | `evidence` |  | string | 레이저 후 재생 촉진으로 색소침착 방지 |  |
| 1501 | `/problems/4/complaints/7/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1502 | `/problems/4/complaints/7/combos/1/name` | `name` |  | string | 레이저 + 미백주사 |  |
| 1503 | `/problems/4/complaints/7/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1504 | `/problems/4/complaints/7/combos/1/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1505 | `/problems/4/complaints/7/combos/1/combo/1` | `(combo 원소)` | 1 | string | 미백주사 |  |
| 1506 | `/problems/4/complaints/7/combos/1/reason` | `reason` |  | string | 미용 목적 정맥 글루타치온/비타민C의 미백 유효성 근거는 부족하며 단기 효과에 그칠 수 있음 | OB-S05-06 |
| 1507 | `/problems/4/complaints/7/combos/1/evidence` | `evidence` |  | string | 근거 없는 시너지 주장은 배제하며, 아나필락시스·간/신장 부담 등 안전성 경고 필요 | OB-S05-06 |
| 1508 | `/problems/4/complaints/7/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 1509 | `/problems/4/complaints/7/alternatives/0` | `(alternatives 원소)` | 0 | string | 자외선 차단 필수 |  |
| 1510 | `/problems/4/complaints/7/alternatives/1` | `(alternatives 원소)` | 1 | string | 정맥 미백주사는 근거 부족·허가 외 사용과 알레르기·아나필락시스, 간·신장 부담 위험을 사전 고지 | OB-S05-08 |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S05-01 | P | `/problems/4/complaints/0/combos/0/evidence`<br>`/problems/4/complaints/1/combos/0/evidence`<br>`/problems/4/complaints/2/combos/0/evidence` | c0~c2 의 evidence 는 두 문장이다. 1문장: 스킨부스터의 재생·보습 보조를 인정하되 '색소침착(PIH) 예방 효과의 임상 근거는 제한적임' 으로 한정하고, 괄호로 '근거 확립된 PIH 예방책은 국소 스테로이드·트라넥삼산' 을 덧붙인다. 2문장: '저출력 1064nm 토닝은 누적 조사 과다·짧은 간격 시 ... 위험이 있어 보수적 세션 간격(2-4주) 필요'. 조건(과다·짧은 간격 시)·위험·필요 지시·범위(2-4주)가 한 문장 안에 있다. 범위 단위 '주' 는 '4주' 에만 붙어 있고 '2' 에도 같은 단위가 걸리는 것으로 읽힌다(표면상 '2-4주'). |
| OB-S05-02 | I | `/problems/4/complaints/0/combos/0/evidence`<br>`/problems/4/complaints/3/combos/0/evidence` | 같은 combo('레이저 + 스킨부스터', reason 동일)의 evidence 가 c0~c2 에서는 '스킨부스터 ... PIH 예방 효과의 임상 근거는 제한적임' 이고 c3~c7 에서는 '레이저 후 재생 촉진으로 색소침착 방지' 이다. 같은 묶음에 서로 맞지 않는 진술이 있다(I-05). |
| OB-S05-03 | P | `/problems/4/complaints/0/combos/0/evidence` | 약어 'PIH' 는 원문 안에서 '색소침착(PIH)' 으로 병기돼 있다(원문 자체 풀이). 이후 '반동성 색소침착' 과 같은 대상인지는 판단하지 않는다. |
| OB-S05-04 | B | `/problems/4/complaints/2/cc`<br>`/problems/4/complaints/2/cc_detail`<br>`/problems/4/complaints/4/cc`<br>`/problems/4/complaints/5/cc` | cc '미백필링'(cc_detail '트라넥삼산 등'), 'IPL', '피코/Q스위치' 인데 procedures 는 모두 레이저(products 피코슈어·피코웨이)+스킨부스터로 c0 과 같다. cc 와 procedures·products 의 구체 대응은 원문에 없다(B-02 템플릿 반복). 필링 procedure 는 이 complaint 에 없다(I-03 같은 유형). |
| OB-S05-05 | P | `/problems/4/complaints/7/cc_detail` | c7 cc_detail 은 '항산화/미백.' 으로 시작한 뒤 마침표 다음에 안전 문장이 이어진다: '고용량 정맥 투여 전 G6PD 결핍 스크리닝 권고(급성 용혈 위험), 고용량·반복 투여 시 옥살산 신병증·급성신손상 위험'. cc_detail 칸에 목적과 안전 경고가 함께 있다(F-05). 조건(투여 전·투여 시)·권고·위험이 들어 있다. |
| OB-S05-06 | P | `/problems/4/complaints/6/combos/1/reason`<br>`/problems/4/complaints/6/combos/1/evidence`<br>`/problems/4/complaints/7/combos/1/reason`<br>`/problems/4/complaints/7/combos/1/evidence` | combo '레이저 + 미백주사' 의 reason 은 '... 미백 유효성 근거는 부족하며 단기 효과에 그칠 수 있음', evidence 는 '근거 없는 시너지 주장은 배제하며, ... 안전성 경고 필요' 이다. 조합이 combos 에 올라 있지만 그 칸의 문장은 조합 근거를 부정·한정한다. combos 등재가 추천을 뜻하는지 원문만으로 정해지지 않는다(F-08). |
| OB-S05-07 | P | `/problems/4/complaints/6/procedures/2/role`<br>`/problems/4/complaints/7/procedures/2/role` | role '미백 목적 허가 외 사용(유효성 근거 제한)' — role 칸에 허가 상태·근거 수준 진술이 있다. 법적 사실로 승인하지 않고 원문으로만 보존. |
| OB-S05-08 | P | `/problems/4/complaints/6/alternatives/1`<br>`/problems/4/complaints/7/alternatives/1` | alternatives 2번째 값이 사전 고지 지시('... 위험을 사전 고지')다. 대안이 아니다(F-04). |
| OB-S05-09 | P | `/problems/4/complaints/6/combos/1/evidence`<br>`/problems/4/complaints/6/alternatives/1` | 같은 짝을 '간/신장'(evidence) 과 '간·신장'(alternatives) 로 다른 기호로 쓴다. '/' 가 여기서는 대안이 아닌 병렬로 읽힌다(F-02). |
| OB-S05-10 | B | `/problems/4/complaints/5/cc_group` | cc_group '오타모반/ABNOM' 의 'ABNOM' 은 약어이며 원문에 풀이가 없다(B-03 같은 유형). |
| OB-S05-11 | P | `/problems/4/complaints/3/cc_detail` | cc_detail '1~2회 집중' — 회차 범위(~)와 정도(집중). README 는 회차를 일정 수식어로 둔다. 수치 범위로 보존. |
| OB-S05-12 | K | `/problems/4/complaints/0/cc_detail`<br>`/problems/4/complaints/0/combos/0/evidence` | '1064nm' 숫자+단위 붙여 씀. 형태소 결과에서 SN+SL 분리 확인(K-04). |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 1064nm 반복 | `/problems/4/complaints/0/cc_detail` [0,9) | 수량·단위(nm), 반복 표현 |
| 피코초 정밀 | `/problems/4/complaints/1/cc_detail` [0,6) | 단위 표현(피코초), 정도 수식(정밀) |
| 트라넥삼산 등 | `/problems/4/complaints/2/cc_detail` [0,7) | 성분 표현, 열린 목록(등) |
| 1~2회 집중 | `/problems/4/complaints/3/cc_detail` [0,7) | 범위(~), 회차, 정도(집중) |
| 광범위 색소 | `/problems/4/complaints/4/cc_detail` [0,6) | 범위 수식(광범위), 증상 표현 |
| 진피색소 | `/problems/4/complaints/5/cc_detail` [0,4) | 층위(진피)+증상, 붙여 쓴 복합어 |
| 글루타치온 IV | `/problems/4/complaints/6/cc_detail` [0,8) | 성분 표현, 투여 경로 약어(IV) |
| 피코/Q스위치 | `/problems/4/complaints/5/cc` [0,7) | 시술명 표현, 기호(/), 혼합 표기 |
| 오타모반/ABNOM | `/problems/4/complaints/5/cc_group` [0,10) | 증상 표현, 기호(/), 약어(원문 풀이 없음) |
| 주근깨/잡티 | `/problems/4/complaints/3/cc_group` [0,6)<br>`/problems/4/complaints/4/cc_group` [0,6) | 증상 표현, 기호(/) |
| 재생·톤개선 | `/problems/4/complaints/0/procedures/1/role` [0,6)<br>`/problems/4/complaints/1/procedures/1/role` [0,6)<br>`/problems/4/complaints/2/procedures/1/role` [0,6)<br>`/problems/4/complaints/3/procedures/1/role` [0,6)<br>`/problems/4/complaints/4/procedures/1/role` [0,6)<br>`/problems/4/complaints/5/procedures/1/role` [0,6)<br>`/problems/4/complaints/6/procedures/1/role` [0,6)<br>`/problems/4/complaints/7/procedures/1/role` [0,6) | role 표현, 기호(·) |
| 색소파괴 + 재생 = 미백+피부결 | `/problems/4/complaints/0/combos/0/reason` [0,18)<br>`/problems/4/complaints/1/combos/0/reason` [0,18)<br>`/problems/4/complaints/2/combos/0/reason` [0,18)<br>`/problems/4/complaints/3/combos/0/reason` [0,18)<br>`/problems/4/complaints/4/combos/0/reason` [0,18)<br>`/problems/4/complaints/5/combos/0/reason` [0,18)<br>`/problems/4/complaints/6/combos/0/reason` [0,18)<br>`/problems/4/complaints/7/combos/0/reason` [0,18) | 공식형 문장, 기호(+), 기호(=), 기호(+ 공백 없음) |
| 스킨부스터는 시술 후 재생·보습을 보조하나 색소침착(PIH) 예방 효과의 임상 근거는 제한적임 | `/problems/4/complaints/0/combos/0/evidence` [0,52)<br>`/problems/4/complaints/1/combos/0/evidence` [0,52)<br>`/problems/4/complaints/2/combos/0/evidence` [0,52) | 양보·대조(-하나), 근거 수준 표현(제한적), 시간 순서(시술 후), 약어 병기 |
| 색소침착(PIH) 예방 효과의 임상 근거는 제한적임 | `/problems/4/complaints/0/combos/0/evidence` [24,52)<br>`/problems/4/complaints/1/combos/0/evidence` [24,52)<br>`/problems/4/complaints/2/combos/0/evidence` [24,52) | 근거 수준 표현(제한적), 부정적 한정 |
| (근거 확립된 PIH 예방책은 국소 스테로이드·트라넥삼산) | `/problems/4/complaints/0/combos/0/evidence` [52,84)<br>`/problems/4/complaints/1/combos/0/evidence` [52,84)<br>`/problems/4/complaints/2/combos/0/evidence` [52,84) | 괄호 보충, 근거 수준 표현(확립된), 기호(·), 성분 표현 |
| 저출력 1064nm 토닝은 누적 조사 과다·짧은 간격 시 반동성 색소침착·반점상 저색소증 위험이 있어 보수적 세션 간격(2-4주) 필요 | `/problems/4/complaints/0/combos/0/evidence` [86,161)<br>`/problems/4/complaints/1/combos/0/evidence` [86,161)<br>`/problems/4/complaints/2/combos/0/evidence` [86,161) | 조건(-시), 위험 표현, 정도 수식(저출력·과다·짧은·보수적), 범위(-), 필요 지시, 수량·단위(nm·주) |
| 누적 조사 과다·짧은 간격 시 | `/problems/4/complaints/0/combos/0/evidence` [101,117)<br>`/problems/4/complaints/1/combos/0/evidence` [101,117)<br>`/problems/4/complaints/2/combos/0/evidence` [101,117) | 조건(-시), 정도 수식(과다·짧은), 기호(·) |
| 반동성 색소침착·반점상 저색소증 위험 | `/problems/4/complaints/0/combos/0/evidence` [118,138)<br>`/problems/4/complaints/1/combos/0/evidence` [118,138)<br>`/problems/4/complaints/2/combos/0/evidence` [118,138) | 위험 표현, 부작용 표현, 기호(·) |
| 보수적 세션 간격(2-4주) 필요 | `/problems/4/complaints/0/combos/0/evidence` [143,161)<br>`/problems/4/complaints/1/combos/0/evidence` [143,161)<br>`/problems/4/complaints/2/combos/0/evidence` [143,161) | 간격, 범위(-), 괄호 보충, 필요 지시 |
| 2-4주 | `/problems/4/complaints/0/combos/0/evidence` [153,157)<br>`/problems/4/complaints/1/combos/0/evidence` [153,157)<br>`/problems/4/complaints/2/combos/0/evidence` [153,157) | 범위(-), 수량·단위·시간 |
| 저출력 1064nm 토닝 | `/problems/4/complaints/0/combos/0/evidence` [86,99)<br>`/problems/4/complaints/1/combos/0/evidence` [86,99)<br>`/problems/4/complaints/2/combos/0/evidence` [86,99) | 시술명 표현, 정도 수식(저출력), 수량·단위(nm) |
| 레이저 후 재생 촉진으로 색소침착 방지 | `/problems/4/complaints/3/combos/0/evidence` [0,21)<br>`/problems/4/complaints/4/combos/0/evidence` [0,21)<br>`/problems/4/complaints/5/combos/0/evidence` [0,21)<br>`/problems/4/complaints/6/combos/0/evidence` [0,21)<br>`/problems/4/complaints/7/combos/0/evidence` [0,21) | 시간 순서(후), 수단(-으로)+결과, 예방 표현(방지) |
| 자외선 차단 필수 | `/problems/4/complaints/0/alternatives/0` [0,9)<br>`/problems/4/complaints/1/alternatives/0` [0,9)<br>`/problems/4/complaints/2/alternatives/0` [0,9)<br>`/problems/4/complaints/3/alternatives/0` [0,9)<br>`/problems/4/complaints/4/alternatives/0` [0,9)<br>`/problems/4/complaints/5/alternatives/0` [0,9)<br>`/problems/4/complaints/6/alternatives/0` [0,9)<br>`/problems/4/complaints/7/alternatives/0` [0,9) | 필수 지시, 관리 지시 |
| 미백 목적 허가 외 사용(유효성 근거 제한) | `/problems/4/complaints/6/procedures/2/role` [0,24)<br>`/problems/4/complaints/7/procedures/2/role` [0,24) | role 표현, 허가 상태 진술, 근거 수준 표현, 괄호 보충 |
| 미용 목적 정맥 글루타치온/비타민C의 미백 유효성 근거는 부족하며 단기 효과에 그칠 수 있음 | `/problems/4/complaints/6/combos/1/reason` [0,51)<br>`/problems/4/complaints/7/combos/1/reason` [0,51) | 근거 수준 표현(부족), 가능성(-ㄹ 수 있음), 기간 표현(단기), 기호(/), 투여 경로(정맥) |
| 단기 효과에 그칠 수 있음 | `/problems/4/complaints/6/combos/1/reason` [37,51)<br>`/problems/4/complaints/7/combos/1/reason` [37,51) | 가능성(-ㄹ 수 있음), 한정(그치다), 기간 표현(단기) |
| 근거 없는 시너지 주장은 배제하며 | `/problems/4/complaints/6/combos/1/evidence` [0,18)<br>`/problems/4/complaints/7/combos/1/evidence` [0,18) | 부정(없는), 배제 지시 |
| 아나필락시스·간/신장 부담 등 안전성 경고 필요 | `/problems/4/complaints/6/combos/1/evidence` [20,46)<br>`/problems/4/complaints/7/combos/1/evidence` [20,46) | 위험 표현, 기호(·), 기호(/), 열린 목록(등), 필요 지시 |
| 정맥 미백주사는 근거 부족·허가 외 사용과 알레르기·아나필락시스, 간·신장 부담 위험을 사전 고지 | `/problems/4/complaints/6/alternatives/1` [0,54)<br>`/problems/4/complaints/7/alternatives/1` [0,54) | 고지 지시, 근거 수준 표현, 허가 상태 진술, 위험 표현, 시간 순서(사전) |
| 항산화/미백 | `/problems/4/complaints/7/cc_detail` [0,6) | 효과 표현, 기호(/) |
| 고용량 정맥 투여 전 G6PD 결핍 스크리닝 권고(급성 용혈 위험) | `/problems/4/complaints/7/cc_detail` [8,45) | 조건(정도 수식 고용량), 시간 순서(투여 전), 권고, 괄호 보충, 위험 표현, 약어(G6PD) |
| 고용량·반복 투여 시 옥살산 신병증·급성신손상 위험 | `/problems/4/complaints/7/cc_detail` [47,75) | 조건(-시), 정도 수식(고용량·반복), 위험 표현, 기호(·) |
| 백옥주사 | `/problems/4/complaints/6/cc` [0,4) | 시술명 표현(속칭), 붙여 쓴 복합어 |

## 이 구획에서 연 미결

- **I-05** (I) 같은 combo '레이저 + 스킨부스터' 의 evidence 가 complaint 에 따라 'PIH 예방 임상 근거 제한적'(c0~c2)과 '재생 촉진으로 색소침착 방지'(c3~c7)로 서로 맞지 않는다. — 영향: evidence 를 combo 단위 근거로 합치면 모순된 주장이 섞인다. 어느 쪽이 옳은지는 임상 판단이므로 이 단계에서 판정하지 않는다.
- **F-08** (F) combos 에 올라 있으나 reason·evidence 가 조합 근거를 부정·한정하는 항목('레이저 + 미백주사'). combos 등재의 의미(추천/언급/경고)가 정의돼 있지 않다. — 영향: combos 를 추천 조합으로 일괄 해석하면 원문의 부정 진술이 뒤집힌다.
