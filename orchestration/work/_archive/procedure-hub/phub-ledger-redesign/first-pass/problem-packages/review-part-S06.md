# S06 — /problems/5 P6 여드름

[← review.md](review.md) · 범위 /problems/5 및 /problems/5/** 전체 · 소유 노드 253 · 말단 165 · 빈 값 3 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S06.txt 로 c0~c7 전부(procedures 18·combos 9·alternatives 9) 읽음. c7 의 긴 cc_detail 은 절 단위로 다시 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 1511 | `/problems/5` | `(problems 원소)` | 5 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 1512 | `/problems/5/problem_id` | `problem_id` |  | string | P6 |  |
| 1513 | `/problems/5/problem` | `problem` |  | string | 여드름 |  |
| 1514 | `/problems/5/complaints` | `complaints` |  | array[8] | (배열 · 8개) |  |
| 1515 | `/problems/5/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1516 | `/problems/5/complaints/0/cc` | `cc` |  | string | 압출 | OB-S06-02 |
| 1517 | `/problems/5/complaints/0/cc_detail` | `cc_detail` |  | string | 면포 제거 + 진정 |  |
| 1518 | `/problems/5/complaints/0/cc_group` | `cc_group` |  | string | 급성(활성) 여드름 |  |
| 1519 | `/problems/5/complaints/0/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1520 | `/problems/5/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S06-02 |
| 1521 | `/problems/5/complaints/0/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1522 | `/problems/5/complaints/0/procedures/0/category` | `category` |  | string | M11 |  |
| 1523 | `/problems/5/complaints/0/procedures/0/role` | `role` |  | string | 피지선 파괴 |  |
| 1524 | `/problems/5/complaints/0/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1525 | `/problems/5/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1526 | `/problems/5/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 제니스 |  |
| 1527 | `/problems/5/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1528 | `/problems/5/complaints/0/procedures/1/name` | `name` |  | string | 메디컬스킨케어 | OB-S06-01 |
| 1529 | `/problems/5/complaints/0/procedures/1/category` | `category` |  | string | M15 | OB-S00-07, OB-S06-08 |
| 1530 | `/problems/5/complaints/0/procedures/1/role` | `role` |  | string | 각질 제거 |  |
| 1531 | `/problems/5/complaints/0/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 1532 | `/problems/5/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1533 | `/problems/5/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1534 | `/problems/5/complaints/0/combos/0/name` | `name` |  | string | 니들RF + 필링 |  |
| 1535 | `/problems/5/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1536 | `/problems/5/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1537 | `/problems/5/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 필링 | OB-S00-05, OB-S06-01 |
| 1538 | `/problems/5/complaints/0/combos/0/reason` | `reason` |  | string | 피지선 파괴 + 각질 제거 |  |
| 1539 | `/problems/5/complaints/0/combos/0/evidence` | `evidence` |  | string | 피지 줄이고 모공 열어줌 |  |
| 1540 | `/problems/5/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1541 | `/problems/5/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 1542 | `/problems/5/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1543 | `/problems/5/complaints/1/cc` | `cc` |  | string | PDT | OB-S06-02 |
| 1544 | `/problems/5/complaints/1/cc_detail` | `cc_detail` |  | string | 감광제+LED |  |
| 1545 | `/problems/5/complaints/1/cc_group` | `cc_group` |  | string | 급성(활성) 여드름 |  |
| 1546 | `/problems/5/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1547 | `/problems/5/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1548 | `/problems/5/complaints/1/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1549 | `/problems/5/complaints/1/procedures/0/category` | `category` |  | string | M11 |  |
| 1550 | `/problems/5/complaints/1/procedures/0/role` | `role` |  | string | 피지선 파괴 |  |
| 1551 | `/problems/5/complaints/1/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1552 | `/problems/5/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1553 | `/problems/5/complaints/1/procedures/0/products/1` | `(products 원소)` | 1 | string | 제니스 |  |
| 1554 | `/problems/5/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1555 | `/problems/5/complaints/1/procedures/1/name` | `name` |  | string | 메디컬스킨케어 |  |
| 1556 | `/problems/5/complaints/1/procedures/1/category` | `category` |  | string | M15 |  |
| 1557 | `/problems/5/complaints/1/procedures/1/role` | `role` |  | string | 각질 제거 |  |
| 1558 | `/problems/5/complaints/1/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 1559 | `/problems/5/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1560 | `/problems/5/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1561 | `/problems/5/complaints/1/combos/0/name` | `name` |  | string | 니들RF + 필링 |  |
| 1562 | `/problems/5/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1563 | `/problems/5/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1564 | `/problems/5/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 필링 | OB-S00-05, OB-S06-01 |
| 1565 | `/problems/5/complaints/1/combos/0/reason` | `reason` |  | string | 피지선 파괴 + 각질 제거 |  |
| 1566 | `/problems/5/complaints/1/combos/0/evidence` | `evidence` |  | string | 피지 줄이고 모공 열어줌 |  |
| 1567 | `/problems/5/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1568 | `/problems/5/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 1569 | `/problems/5/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1570 | `/problems/5/complaints/2/cc` | `cc` |  | string | 약물치료 | OB-S06-02, OB-S06-03 |
| 1571 | `/problems/5/complaints/2/cc_detail` | `cc_detail` |  | string | 이소트레티노인 등 |  |
| 1572 | `/problems/5/complaints/2/cc_group` | `cc_group` |  | string | 급성(활성) 여드름 |  |
| 1573 | `/problems/5/complaints/2/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1574 | `/problems/5/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1575 | `/problems/5/complaints/2/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1576 | `/problems/5/complaints/2/procedures/0/category` | `category` |  | string | M11 |  |
| 1577 | `/problems/5/complaints/2/procedures/0/role` | `role` |  | string | 피지선 파괴 |  |
| 1578 | `/problems/5/complaints/2/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1579 | `/problems/5/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1580 | `/problems/5/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 제니스 |  |
| 1581 | `/problems/5/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1582 | `/problems/5/complaints/2/procedures/1/name` | `name` |  | string | 메디컬스킨케어 |  |
| 1583 | `/problems/5/complaints/2/procedures/1/category` | `category` |  | string | M15 |  |
| 1584 | `/problems/5/complaints/2/procedures/1/role` | `role` |  | string | 각질 제거 |  |
| 1585 | `/problems/5/complaints/2/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 1586 | `/problems/5/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1587 | `/problems/5/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1588 | `/problems/5/complaints/2/combos/0/name` | `name` |  | string | 니들RF + 필링 |  |
| 1589 | `/problems/5/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1590 | `/problems/5/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1591 | `/problems/5/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 필링 | OB-S00-05, OB-S06-01 |
| 1592 | `/problems/5/complaints/2/combos/0/reason` | `reason` |  | string | 피지선 파괴 + 각질 제거 |  |
| 1593 | `/problems/5/complaints/2/combos/0/evidence` | `evidence` |  | string | 피지 줄이고 모공 열어줌 |  |
| 1594 | `/problems/5/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1595 | `/problems/5/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 | OB-S06-03 |
| 1596 | `/problems/5/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1597 | `/problems/5/complaints/3/cc` | `cc` |  | string | 아그네스 | OB-S00-06, OB-S07-06 |
| 1598 | `/problems/5/complaints/3/cc_detail` | `cc_detail` |  | string | 피지선 파괴 · 니들RF | OB-S06-09 |
| 1599 | `/problems/5/complaints/3/cc_group` | `cc_group` |  | string | 피지/모공 |  |
| 1600 | `/problems/5/complaints/3/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1601 | `/problems/5/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1602 | `/problems/5/complaints/3/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1603 | `/problems/5/complaints/3/procedures/0/category` | `category` |  | string | M11 |  |
| 1604 | `/problems/5/complaints/3/procedures/0/role` | `role` |  | string | 모공 수축 |  |
| 1605 | `/problems/5/complaints/3/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 1606 | `/problems/5/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1607 | `/problems/5/complaints/3/procedures/0/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1608 | `/problems/5/complaints/3/procedures/0/products/2` | `(products 원소)` | 2 | string | 제니스 |  |
| 1609 | `/problems/5/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1610 | `/problems/5/complaints/3/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1611 | `/problems/5/complaints/3/procedures/1/category` | `category` |  | string | M4 |  |
| 1612 | `/problems/5/complaints/3/procedures/1/role` | `role` |  | string | 콜라겐 재생 |  |
| 1613 | `/problems/5/complaints/3/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1614 | `/problems/5/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1615 | `/problems/5/complaints/3/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1616 | `/problems/5/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1617 | `/problems/5/complaints/3/combos/0/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1618 | `/problems/5/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1619 | `/problems/5/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1620 | `/problems/5/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1621 | `/problems/5/complaints/3/combos/0/reason` | `reason` |  | string | 모공 수축 + 재생 | OB-S07-02 |
| 1622 | `/problems/5/complaints/3/combos/0/evidence` | `evidence` |  | string | 쥬베룩이 모공에 특화 |  |
| 1623 | `/problems/5/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1624 | `/problems/5/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 1625 | `/problems/5/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1626 | `/problems/5/complaints/4/cc` | `cc` |  | string | 스킨보톡스 | OB-S00-06, OB-S07-06 |
| 1627 | `/problems/5/complaints/4/cc_detail` | `cc_detail` |  | string | 피지↓ 모공↓ | OB-S06-05 |
| 1628 | `/problems/5/complaints/4/cc_group` | `cc_group` |  | string | 피지/모공 |  |
| 1629 | `/problems/5/complaints/4/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 1630 | `/problems/5/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1631 | `/problems/5/complaints/4/procedures/0/name` | `name` |  | string | 보톡스 | OB-S06-06 |
| 1632 | `/problems/5/complaints/4/procedures/0/category` | `category` |  | string | M1 |  |
| 1633 | `/problems/5/complaints/4/procedures/0/role` | `role` |  | string | 진피내 피지선·입모근의 콜린성 신호 차단 |  |
| 1634 | `/problems/5/complaints/4/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 1635 | `/problems/5/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 1636 | `/problems/5/complaints/4/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 1637 | `/problems/5/complaints/4/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 1638 | `/problems/5/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S06-04 |
| 1639 | `/problems/5/complaints/4/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1640 | `/problems/5/complaints/4/procedures/1/category` | `category` |  | string | M4 |  |
| 1641 | `/problems/5/complaints/4/procedures/1/role` | `role` |  | string | 피부 재생 |  |
| 1642 | `/problems/5/complaints/4/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1643 | `/problems/5/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 HB+ |  |
| 1644 | `/problems/5/complaints/4/procedures/1/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 1645 | `/problems/5/complaints/4/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1646 | `/problems/5/complaints/4/procedures/2/name` | `name` |  | string | 니들RF |  |
| 1647 | `/problems/5/complaints/4/procedures/2/category` | `category` |  | string | M11 |  |
| 1648 | `/problems/5/complaints/4/procedures/2/role` | `role` |  | string | 모공 수축 |  |
| 1649 | `/problems/5/complaints/4/procedures/2/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 1650 | `/problems/5/complaints/4/procedures/2/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1651 | `/problems/5/complaints/4/procedures/2/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1652 | `/problems/5/complaints/4/procedures/2/products/2` | `(products 원소)` | 2 | string | 제니스 |  |
| 1653 | `/problems/5/complaints/4/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S06-04 |
| 1654 | `/problems/5/complaints/4/procedures/3/name` | `name` |  | string | 스킨부스터 |  |
| 1655 | `/problems/5/complaints/4/procedures/3/category` | `category` |  | string | M4 |  |
| 1656 | `/problems/5/complaints/4/procedures/3/role` | `role` |  | string | 콜라겐 재생 |  |
| 1657 | `/problems/5/complaints/4/procedures/3/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1658 | `/problems/5/complaints/4/procedures/3/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1659 | `/problems/5/complaints/4/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1660 | `/problems/5/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1661 | `/problems/5/complaints/4/combos/0/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 1662 | `/problems/5/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1663 | `/problems/5/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 1664 | `/problems/5/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1665 | `/problems/5/complaints/4/combos/0/reason` | `reason` |  | string | 마이크로보톡스로 피지·모공 감소 + 스킨부스터로 피부 재생 보조 | OB-S06-06 |
| 1666 | `/problems/5/complaints/4/combos/0/evidence` | `evidence` |  | string | 마이크로보톡스는 피지선의 콜린성 신호 차단으로 피지·모공을 감소시킴 | OB-S06-06 |
| 1667 | `/problems/5/complaints/4/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1668 | `/problems/5/complaints/4/combos/1/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1669 | `/problems/5/complaints/4/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1670 | `/problems/5/complaints/4/combos/1/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1671 | `/problems/5/complaints/4/combos/1/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1672 | `/problems/5/complaints/4/combos/1/reason` | `reason` |  | string | 모공 수축 + 재생 |  |
| 1673 | `/problems/5/complaints/4/combos/1/evidence` | `evidence` |  | string | 쥬베룩이 모공에 특화 |  |
| 1674 | `/problems/5/complaints/4/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 1675 | `/problems/5/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 1676 | `/problems/5/complaints/4/alternatives/1` | `(alternatives 원소)` | 1 | string | 약물치료 병행 추천 |  |
| 1677 | `/problems/5/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1678 | `/problems/5/complaints/5/cc` | `cc` |  | string | 케미컬필링 |  |
| 1679 | `/problems/5/complaints/5/cc_detail` | `cc_detail` |  | string | AHA/BHA |  |
| 1680 | `/problems/5/complaints/5/cc_group` | `cc_group` |  | string | 피지/모공 |  |
| 1681 | `/problems/5/complaints/5/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1682 | `/problems/5/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1683 | `/problems/5/complaints/5/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1684 | `/problems/5/complaints/5/procedures/0/category` | `category` |  | string | M11 |  |
| 1685 | `/problems/5/complaints/5/procedures/0/role` | `role` |  | string | 모공 수축 |  |
| 1686 | `/problems/5/complaints/5/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 1687 | `/problems/5/complaints/5/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1688 | `/problems/5/complaints/5/procedures/0/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1689 | `/problems/5/complaints/5/procedures/0/products/2` | `(products 원소)` | 2 | string | 제니스 |  |
| 1690 | `/problems/5/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1691 | `/problems/5/complaints/5/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1692 | `/problems/5/complaints/5/procedures/1/category` | `category` |  | string | M4 |  |
| 1693 | `/problems/5/complaints/5/procedures/1/role` | `role` |  | string | 콜라겐 재생 |  |
| 1694 | `/problems/5/complaints/5/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1695 | `/problems/5/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1696 | `/problems/5/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1697 | `/problems/5/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1698 | `/problems/5/complaints/5/combos/0/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1699 | `/problems/5/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1700 | `/problems/5/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1701 | `/problems/5/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1702 | `/problems/5/complaints/5/combos/0/reason` | `reason` |  | string | 모공 수축 + 재생 |  |
| 1703 | `/problems/5/complaints/5/combos/0/evidence` | `evidence` |  | string | 쥬베룩이 모공에 특화 |  |
| 1704 | `/problems/5/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1705 | `/problems/5/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 1706 | `/problems/5/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1707 | `/problems/5/complaints/6/cc` | `cc` |  | string | 토닝 |  |
| 1708 | `/problems/5/complaints/6/cc_detail` | `cc_detail` |  | string | 색소자국 개선 |  |
| 1709 | `/problems/5/complaints/6/cc_group` | `cc_group` |  | string | 여드름자국(PIH/PIE) | OB-S06-10 |
| 1710 | `/problems/5/complaints/6/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1711 | `/problems/5/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1712 | `/problems/5/complaints/6/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1713 | `/problems/5/complaints/6/procedures/0/category` | `category` |  | string | M8 |  |
| 1714 | `/problems/5/complaints/6/procedures/0/role` | `role` |  | string | 색소 제거 | OB-S06-11 |
| 1715 | `/problems/5/complaints/6/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1716 | `/problems/5/complaints/6/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1717 | `/problems/5/complaints/6/procedures/0/products/1` | `(products 원소)` | 1 | string | 엑셀V |  |
| 1718 | `/problems/5/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1719 | `/problems/5/complaints/6/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1720 | `/problems/5/complaints/6/procedures/1/category` | `category` |  | string | M4 |  |
| 1721 | `/problems/5/complaints/6/procedures/1/role` | `role` |  | string | 재생 |  |
| 1722 | `/problems/5/complaints/6/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1723 | `/problems/5/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1724 | `/problems/5/complaints/6/procedures/1/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 1725 | `/problems/5/complaints/6/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1726 | `/problems/5/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1727 | `/problems/5/complaints/6/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1728 | `/problems/5/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1729 | `/problems/5/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1730 | `/problems/5/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1731 | `/problems/5/complaints/6/combos/0/reason` | `reason` |  | string | 색소제거 + 재생 |  |
| 1732 | `/problems/5/complaints/6/combos/0/evidence` | `evidence` |  | string | 자국 빠르게 개선 |  |
| 1733 | `/problems/5/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1734 | `/problems/5/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |
| 1735 | `/problems/5/complaints/7` | `(complaints 원소)` | 7 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1736 | `/problems/5/complaints/7/cc` | `cc` |  | string | 재생치료 |  |
| 1737 | `/problems/5/complaints/7/cc_detail` | `cc_detail` |  | string | 리쥬란/엑소좀. 엑소좀은 국내 허가된 주사 의약품이 아닌 화장품 분류 제품으로 주사·MTS 채널 전달은 미허가·위법 소지와 감염·이물육아종 위험이 있으며 미용 효과의 임상 검증은 제한적 | OB-S06-07, OB-S13-02 |
| 1738 | `/problems/5/complaints/7/cc_group` | `cc_group` |  | string | 여드름자국(PIH/PIE) | OB-S06-10 |
| 1739 | `/problems/5/complaints/7/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1740 | `/problems/5/complaints/7/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1741 | `/problems/5/complaints/7/procedures/0/name` | `name` |  | string | 레이저 |  |
| 1742 | `/problems/5/complaints/7/procedures/0/category` | `category` |  | string | M8 |  |
| 1743 | `/problems/5/complaints/7/procedures/0/role` | `role` |  | string | 색소 제거 |  |
| 1744 | `/problems/5/complaints/7/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1745 | `/problems/5/complaints/7/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 1746 | `/problems/5/complaints/7/procedures/0/products/1` | `(products 원소)` | 1 | string | 엑셀V |  |
| 1747 | `/problems/5/complaints/7/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1748 | `/problems/5/complaints/7/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1749 | `/problems/5/complaints/7/procedures/1/category` | `category` |  | string | M4 |  |
| 1750 | `/problems/5/complaints/7/procedures/1/role` | `role` |  | string | 재생 |  |
| 1751 | `/problems/5/complaints/7/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1752 | `/problems/5/complaints/7/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1753 | `/problems/5/complaints/7/procedures/1/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 1754 | `/problems/5/complaints/7/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1755 | `/problems/5/complaints/7/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1756 | `/problems/5/complaints/7/combos/0/name` | `name` |  | string | 레이저 + 스킨부스터 |  |
| 1757 | `/problems/5/complaints/7/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1758 | `/problems/5/complaints/7/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 1759 | `/problems/5/complaints/7/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1760 | `/problems/5/complaints/7/combos/0/reason` | `reason` |  | string | 색소제거 + 재생 |  |
| 1761 | `/problems/5/complaints/7/combos/0/evidence` | `evidence` |  | string | 자국 빠르게 개선 |  |
| 1762 | `/problems/5/complaints/7/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1763 | `/problems/5/complaints/7/alternatives/0` | `(alternatives 원소)` | 0 | string | 약물치료 병행 추천 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S06-01 | I | `/problems/5/complaints/0/combos/0/combo/1`<br>`/problems/5/complaints/0/procedures/1/name`<br>`/problems/5/complaints/1/combos/0/combo/1`<br>`/problems/5/complaints/2/combos/0/combo/1` | combo '니들RF + 필링' 의 원소 '필링' 이 같은 complaint 의 procedures 에 없다. procedures[1] 은 '메디컬스킨케어'(role '각질 제거')이며 reason '피지선 파괴 + 각질 제거' 의 둘째 항과 role 이 같다. 이름이 다르므로 연결은 잠정(I-06). |
| OB-S06-02 | B | `/problems/5/complaints/0/cc`<br>`/problems/5/complaints/1/cc`<br>`/problems/5/complaints/2/cc`<br>`/problems/5/complaints/0/procedures/0` | cc '압출'·'PDT'·'약물치료' 세 complaint 의 procedures·combos·alternatives 가 글자 그대로 같다(니들RF+메디컬스킨케어). cc 가 가리키는 처치(압출·PDT·약물)는 procedures 에 없다(B-02 · I-03 같은 유형). |
| OB-S06-03 | P | `/problems/5/complaints/2/cc`<br>`/problems/5/complaints/2/alternatives/0` | c2 cc 가 '약물치료' 인데 alternatives 는 '약물치료 병행 추천' — 자기 자신과 병행을 권하는 문장이 템플릿 반복으로 들어 있다. |
| OB-S06-04 | I | `/problems/5/complaints/4/procedures/1`<br>`/problems/5/complaints/4/procedures/3` | c4 procedures 에 name '스킨부스터'(M4) 가 두 번(P1 role '피부 재생' products 리쥬란 HB+·쥬베룩 / P3 role '콜라겐 재생' products 쥬베룩) 나온다. combo 원소 '스킨부스터' 가 어느 항목인지 원문으로 구분할 수 없다(I-07). |
| OB-S06-05 | P | `/problems/5/complaints/4/cc_detail` | cc_detail '피지↓ 모공↓' — 화살표 기호로 감소를 나타낸다. 형태소 분석에서 기호 처리 확인(K-05). |
| OB-S06-06 | P | `/problems/5/complaints/4/combos/0/reason`<br>`/problems/5/complaints/4/combos/0/evidence`<br>`/problems/5/complaints/4/procedures/0/name` | reason·evidence 는 '마이크로보톡스' 를 말하고 procedures name 은 '보톡스' 다. 시술 방식의 수식이 combo 문장에만 있다. |
| OB-S06-07 | P | `/problems/5/complaints/7/cc_detail` | c7 cc_detail 은 '리쥬란/엑소좀.' 뒤에 규제·안전 문장이 이어진다: '엑소좀은 국내 허가된 주사 의약품이 아닌 화장품 분류 제품으로 주사·MTS 채널 전달은 미허가·위법 소지와 감염·이물육아종 위험이 있으며 미용 효과의 임상 검증은 제한적'. 부정('아닌')·법적 진술('미허가·위법 소지')·위험·근거 한정이 한 값에 있다. 법적 사실로 승인하지 않는다. 엑소좀은 procedures·products 에 없다. |
| OB-S06-08 | P | `/problems/5/complaints/0/procedures/1/category`<br>`/problems/0/complaints/13/procedures/0/category` | category 'M15' 가 S01 에서는 '반영구화장', 여기서는 '메디컬스킨케어' 의 코드다. 코드 하나에 이름 둘(F-01 taxonomy 대조 대상). |
| OB-S06-09 | P | `/problems/5/complaints/3/cc_detail` | cc_detail '피지선 파괴 · 니들RF' — 띄어 쓴 가운뎃점으로 효과와 시술을 잇는다. |
| OB-S06-10 | P | `/problems/5/complaints/6/cc_group`<br>`/problems/5/complaints/7/cc_group` | cc_group '여드름자국(PIH/PIE)' — 괄호 안 약어 두 개. PIH 는 S05 에 '색소침착(PIH)' 병기가 있고 PIE 는 원문 어디에도 풀이가 없다(B-03 같은 유형). |
| OB-S06-11 | P | `/problems/5/complaints/6/procedures/0/role`<br>`/problems/4/complaints/0/procedures/0/role` | 레이저 role 이 여기서는 '색소 제거', S05 에서는 '색소 파괴'. products 도 '피코슈어·엑셀V' 로 S05 와 다르다. |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 면포 제거 + 진정 | `/problems/5/complaints/0/cc_detail` [0,10) | 기호(+), 효과 표현 |
| 감광제+LED | `/problems/5/complaints/1/cc_detail` [0,7) | 기호(+ 공백 없음), 재료·장비 표현, 약어 |
| 이소트레티노인 등 | `/problems/5/complaints/2/cc_detail` [0,9) | 성분 표현, 열린 목록(등) |
| 피지선 파괴 · 니들RF | `/problems/5/complaints/3/cc_detail` [0,13) | 기호(· 띄어 씀), 효과+시술명 표현 |
| 피지↓ 모공↓ | `/problems/5/complaints/4/cc_detail` [0,7) | 기호(↓), 감소 표현 |
| AHA/BHA | `/problems/5/complaints/5/cc_detail` [0,7) | 성분 약어, 기호(/) |
| 색소자국 개선 | `/problems/5/complaints/6/cc_detail` [0,7) | 증상 표현, 효과 표현 |
| 급성(활성) 여드름 | `/problems/5/complaints/0/cc_group` [0,10)<br>`/problems/5/complaints/1/cc_group` [0,10)<br>`/problems/5/complaints/2/cc_group` [0,10) | 상태 수식(급성), 괄호 보충 |
| 여드름자국(PIH/PIE) | `/problems/5/complaints/6/cc_group` [0,14)<br>`/problems/5/complaints/7/cc_group` [0,14) | 증상 표현, 괄호 보충, 약어, 기호(/) |
| 피지/모공 | `/problems/5/complaints/3/cc_group` [0,5)<br>`/problems/5/complaints/4/cc_group` [0,5)<br>`/problems/5/complaints/5/cc_group` [0,5) | 증상 표현, 기호(/) |
| 피지선 파괴 + 각질 제거 | `/problems/5/complaints/0/combos/0/reason` [0,14)<br>`/problems/5/complaints/1/combos/0/reason` [0,14)<br>`/problems/5/complaints/2/combos/0/reason` [0,14) | 기호(+), 결과 없는 공식형 |
| 피지 줄이고 모공 열어줌 | `/problems/5/complaints/0/combos/0/evidence` [0,13)<br>`/problems/5/complaints/1/combos/0/evidence` [0,13)<br>`/problems/5/complaints/2/combos/0/evidence` [0,13) | 감소 표현, 병렬(-고), 기전 진술 |
| 약물치료 병행 추천 | `/problems/5/complaints/0/alternatives/0` [0,10)<br>`/problems/5/complaints/1/alternatives/0` [0,10)<br>`/problems/5/complaints/2/alternatives/0` [0,10)<br>`/problems/5/complaints/3/alternatives/0` [0,10)<br>`/problems/5/complaints/4/alternatives/1` [0,10)<br>`/problems/5/complaints/5/alternatives/0` [0,10)<br>`/problems/5/complaints/6/alternatives/0` [0,10)<br>`/problems/5/complaints/7/alternatives/0` [0,10) | 병행, 권고(추천) |
| 진피내 피지선·입모근의 콜린성 신호 차단 | `/problems/5/complaints/4/procedures/0/role` [0,22) | role 표현, 층위(진피내), 기호(·), 기전 표현, 차단 표현 |
| 마이크로보톡스로 피지·모공 감소 + 스킨부스터로 피부 재생 보조 | `/problems/5/complaints/4/combos/0/reason` [0,35) | 기호(+), 수단(-로)+결과, 감소 표현, 보조 |
| 마이크로보톡스는 피지선의 콜린성 신호 차단으로 피지·모공을 감소시킴 | `/problems/5/complaints/4/combos/0/evidence` [0,37) | 기전 진술, 수단(-으로)+결과, 감소 표현 |
| 모공 수축 + 재생 | `/problems/5/complaints/3/combos/0/reason` [0,10)<br>`/problems/5/complaints/4/combos/1/reason` [0,10)<br>`/problems/5/complaints/5/combos/0/reason` [0,10) | 기호(+), 결과 없는 공식형 |
| 쥬베룩이 모공에 특화 | `/problems/5/complaints/3/combos/0/evidence` [0,11)<br>`/problems/5/complaints/4/combos/1/evidence` [0,11)<br>`/problems/5/complaints/5/combos/0/evidence` [0,11) | 제품명 표현, 특화 주장 |
| 효과 부족 시 리프팅기기 추가 | `/problems/5/complaints/4/alternatives/0` [0,16) | 조건(-시), 부족 표현, 추가 표현 |
| 색소제거 + 재생 | `/problems/5/complaints/6/combos/0/reason` [0,9)<br>`/problems/5/complaints/7/combos/0/reason` [0,9) | 기호(+), 결과 없는 공식형 |
| 자국 빠르게 개선 | `/problems/5/complaints/6/combos/0/evidence` [0,9)<br>`/problems/5/complaints/7/combos/0/evidence` [0,9) | 속도 수식(빠르게), 효과 표현 |
| 리쥬란/엑소좀 | `/problems/5/complaints/7/cc_detail` [0,7) | 제품·재료 표현, 기호(/) |
| 엑소좀은 국내 허가된 주사 의약품이 아닌 화장품 분류 제품으로 | `/problems/5/complaints/7/cc_detail` [9,43) | 부정(아닌), 허가 상태 진술, 범위(국내) |
| 주사·MTS 채널 전달은 미허가·위법 소지와 감염·이물육아종 위험이 있으며 | `/problems/5/complaints/7/cc_detail` [44,85) | 허가 상태 진술, 법적 진술(위법 소지), 위험 표현, 기호(·), 약어(MTS) |
| 미용 효과의 임상 검증은 제한적 | `/problems/5/complaints/7/cc_detail` [86,103) | 근거 수준 표현(제한적) |
| 모공 수축 | `/problems/5/complaints/3/procedures/0/role` [0,5)<br>`/problems/5/complaints/4/procedures/2/role` [0,5)<br>`/problems/5/complaints/5/procedures/0/role` [0,5) | role 표현, 감소 표현(수축) |
| 피지선 파괴 | `/problems/5/complaints/0/procedures/0/role` [0,6)<br>`/problems/5/complaints/1/procedures/0/role` [0,6)<br>`/problems/5/complaints/2/procedures/0/role` [0,6) | role 표현, 기전 표현 |

## 이 구획에서 연 미결

- **I-06** (I) combos.combo 원소가 같은 complaint 의 procedures.name 에 없다('필링' ↔ procedures '메디컬스킨케어'). — 영향: combo 원소를 procedures 로 이을 수 없다. 원본 변경 제안은 후속 확인 후보.
- **I-07** (I) 한 complaint 안에 같은 procedures.name('스킨부스터')이 role·products 를 달리해 두 번 나온다. — 영향: name 으로 procedure 를 식별하는 연결은 모호해진다. 배열 순번(Pointer)으로만 구분 가능.
