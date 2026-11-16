# S02 — /problems/1 P2 주름

[← review.md](review.md) · 범위 /problems/1 및 /problems/1/** 전체 · 소유 노드 330 · 말단 226 · 빈 값 0 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S02.txt 로 c0~c6 전부(procedures 23·combos 15·alternatives 7) 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 461 | `/problems/1` | `(problems 원소)` | 1 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 462 | `/problems/1/problem_id` | `problem_id` |  | string | P2 |  |
| 463 | `/problems/1/problem` | `problem` |  | string | 주름 |  |
| 464 | `/problems/1/complaints` | `complaints` |  | array[7] | (배열 · 7개) |  |
| 465 | `/problems/1/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 466 | `/problems/1/complaints/0/cc` | `cc` |  | string | 이마주름 |  |
| 467 | `/problems/1/complaints/0/cc_detail` | `cc_detail` |  | string | 보톡스 | OB-S02-01 |
| 468 | `/problems/1/complaints/0/cc_group` | `cc_group` |  | string | 표정주름 | OB-S02-07 |
| 469 | `/problems/1/complaints/0/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 470 | `/problems/1/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 471 | `/problems/1/complaints/0/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 472 | `/problems/1/complaints/0/procedures/0/category` | `category` |  | string | M1 |  |
| 473 | `/problems/1/complaints/0/procedures/0/role` | `role` |  | string | 근육 이완으로 주름 완화 | OB-S02-08 |
| 474 | `/problems/1/complaints/0/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 475 | `/problems/1/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 476 | `/problems/1/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 477 | `/problems/1/complaints/0/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 478 | `/problems/1/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 479 | `/problems/1/complaints/0/procedures/1/name` | `name` |  | string | 리프팅기기 |  |
| 480 | `/problems/1/complaints/0/procedures/1/category` | `category` |  | string | M9 |  |
| 481 | `/problems/1/complaints/0/procedures/1/role` | `role` |  | string | 피부 타이트닝 |  |
| 482 | `/problems/1/complaints/0/procedures/1/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 483 | `/problems/1/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 484 | `/problems/1/complaints/0/procedures/1/products/1` | `(products 원소)` | 1 | string | 써마지FLX | OB-S02-09 |
| 485 | `/problems/1/complaints/0/procedures/1/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 | OB-S02-09 |
| 486 | `/problems/1/complaints/0/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 487 | `/problems/1/complaints/0/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 488 | `/problems/1/complaints/0/procedures/2/category` | `category` |  | string | M4 |  |
| 489 | `/problems/1/complaints/0/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 490 | `/problems/1/complaints/0/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 491 | `/problems/1/complaints/0/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 | OB-S02-09 |
| 492 | `/problems/1/complaints/0/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 493 | `/problems/1/complaints/0/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 494 | `/problems/1/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 495 | `/problems/1/complaints/0/combos/0/name` | `name` |  | string | 보톡스 + 리프팅기기 |  |
| 496 | `/problems/1/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 497 | `/problems/1/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 498 | `/problems/1/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 499 | `/problems/1/complaints/0/combos/0/reason` | `reason` |  | string | 근이완 + 타이트닝 = 이중 효과 | OB-S02-06 |
| 500 | `/problems/1/complaints/0/combos/0/evidence` | `evidence` |  | string | 동적+정적 주름 동시 해결 | OB-S02-04 |
| 501 | `/problems/1/complaints/0/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 502 | `/problems/1/complaints/0/combos/1/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 503 | `/problems/1/complaints/0/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 504 | `/problems/1/complaints/0/combos/1/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 505 | `/problems/1/complaints/0/combos/1/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 506 | `/problems/1/complaints/0/combos/1/reason` | `reason` |  | string | 근이완 + 재생 |  |
| 507 | `/problems/1/complaints/0/combos/1/evidence` | `evidence` |  | string | 주름+피부결 개선 |  |
| 508 | `/problems/1/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 509 | `/problems/1/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 510 | `/problems/1/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 511 | `/problems/1/complaints/1/cc` | `cc` |  | string | 미간주름 |  |
| 512 | `/problems/1/complaints/1/cc_detail` | `cc_detail` |  | string | 보톡스 | OB-S02-01 |
| 513 | `/problems/1/complaints/1/cc_group` | `cc_group` |  | string | 표정주름 |  |
| 514 | `/problems/1/complaints/1/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 515 | `/problems/1/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 516 | `/problems/1/complaints/1/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 517 | `/problems/1/complaints/1/procedures/0/category` | `category` |  | string | M1 |  |
| 518 | `/problems/1/complaints/1/procedures/0/role` | `role` |  | string | 근육 이완으로 주름 완화 |  |
| 519 | `/problems/1/complaints/1/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 520 | `/problems/1/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 521 | `/problems/1/complaints/1/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 522 | `/problems/1/complaints/1/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 523 | `/problems/1/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 524 | `/problems/1/complaints/1/procedures/1/name` | `name` |  | string | 리프팅기기 |  |
| 525 | `/problems/1/complaints/1/procedures/1/category` | `category` |  | string | M9 |  |
| 526 | `/problems/1/complaints/1/procedures/1/role` | `role` |  | string | 피부 타이트닝 |  |
| 527 | `/problems/1/complaints/1/procedures/1/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 528 | `/problems/1/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 529 | `/problems/1/complaints/1/procedures/1/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 530 | `/problems/1/complaints/1/procedures/1/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 |  |
| 531 | `/problems/1/complaints/1/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 532 | `/problems/1/complaints/1/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 533 | `/problems/1/complaints/1/procedures/2/category` | `category` |  | string | M4 |  |
| 534 | `/problems/1/complaints/1/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 535 | `/problems/1/complaints/1/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 536 | `/problems/1/complaints/1/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 537 | `/problems/1/complaints/1/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 538 | `/problems/1/complaints/1/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 539 | `/problems/1/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 540 | `/problems/1/complaints/1/combos/0/name` | `name` |  | string | 보톡스 + 리프팅기기 |  |
| 541 | `/problems/1/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 542 | `/problems/1/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 543 | `/problems/1/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 544 | `/problems/1/complaints/1/combos/0/reason` | `reason` |  | string | 근이완 + 타이트닝 = 이중 효과 |  |
| 545 | `/problems/1/complaints/1/combos/0/evidence` | `evidence` |  | string | 동적+정적 주름 동시 해결 |  |
| 546 | `/problems/1/complaints/1/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 547 | `/problems/1/complaints/1/combos/1/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 548 | `/problems/1/complaints/1/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 549 | `/problems/1/complaints/1/combos/1/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 550 | `/problems/1/complaints/1/combos/1/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 551 | `/problems/1/complaints/1/combos/1/reason` | `reason` |  | string | 근이완 + 재생 |  |
| 552 | `/problems/1/complaints/1/combos/1/evidence` | `evidence` |  | string | 주름+피부결 개선 |  |
| 553 | `/problems/1/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 554 | `/problems/1/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 555 | `/problems/1/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 556 | `/problems/1/complaints/2/cc` | `cc` |  | string | 눈가주름 |  |
| 557 | `/problems/1/complaints/2/cc_detail` | `cc_detail` |  | string | 보톡스 | OB-S02-01 |
| 558 | `/problems/1/complaints/2/cc_group` | `cc_group` |  | string | 표정주름 |  |
| 559 | `/problems/1/complaints/2/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 560 | `/problems/1/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 561 | `/problems/1/complaints/2/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 562 | `/problems/1/complaints/2/procedures/0/category` | `category` |  | string | M1 |  |
| 563 | `/problems/1/complaints/2/procedures/0/role` | `role` |  | string | 근육 이완으로 주름 완화 |  |
| 564 | `/problems/1/complaints/2/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 565 | `/problems/1/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 566 | `/problems/1/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 567 | `/problems/1/complaints/2/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 568 | `/problems/1/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 569 | `/problems/1/complaints/2/procedures/1/name` | `name` |  | string | 리프팅기기 |  |
| 570 | `/problems/1/complaints/2/procedures/1/category` | `category` |  | string | M9 |  |
| 571 | `/problems/1/complaints/2/procedures/1/role` | `role` |  | string | 피부 타이트닝 |  |
| 572 | `/problems/1/complaints/2/procedures/1/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 573 | `/problems/1/complaints/2/procedures/1/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 574 | `/problems/1/complaints/2/procedures/1/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 575 | `/problems/1/complaints/2/procedures/1/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 |  |
| 576 | `/problems/1/complaints/2/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 577 | `/problems/1/complaints/2/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 578 | `/problems/1/complaints/2/procedures/2/category` | `category` |  | string | M4 |  |
| 579 | `/problems/1/complaints/2/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 580 | `/problems/1/complaints/2/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 581 | `/problems/1/complaints/2/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 582 | `/problems/1/complaints/2/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 583 | `/problems/1/complaints/2/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 584 | `/problems/1/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 585 | `/problems/1/complaints/2/combos/0/name` | `name` |  | string | 보톡스 + 리프팅기기 |  |
| 586 | `/problems/1/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 587 | `/problems/1/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 588 | `/problems/1/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 589 | `/problems/1/complaints/2/combos/0/reason` | `reason` |  | string | 근이완 + 타이트닝 = 이중 효과 |  |
| 590 | `/problems/1/complaints/2/combos/0/evidence` | `evidence` |  | string | 동적+정적 주름 동시 해결 |  |
| 591 | `/problems/1/complaints/2/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 592 | `/problems/1/complaints/2/combos/1/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 593 | `/problems/1/complaints/2/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 594 | `/problems/1/complaints/2/combos/1/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 595 | `/problems/1/complaints/2/combos/1/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 596 | `/problems/1/complaints/2/combos/1/reason` | `reason` |  | string | 근이완 + 재생 |  |
| 597 | `/problems/1/complaints/2/combos/1/evidence` | `evidence` |  | string | 주름+피부결 개선 |  |
| 598 | `/problems/1/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 599 | `/problems/1/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 600 | `/problems/1/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 601 | `/problems/1/complaints/3/cc` | `cc` |  | string | 팔자주름 | OB-S02-03 |
| 602 | `/problems/1/complaints/3/cc_detail` | `cc_detail` |  | string | 필러/바이오스티뮬레이터 | OB-S02-01, OB-S02-02 |
| 603 | `/problems/1/complaints/3/cc_group` | `cc_group` |  | string | 깊은주름 | OB-S02-07 |
| 604 | `/problems/1/complaints/3/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 605 | `/problems/1/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 606 | `/problems/1/complaints/3/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 607 | `/problems/1/complaints/3/procedures/0/category` | `category` |  | string | M1 |  |
| 608 | `/problems/1/complaints/3/procedures/0/role` | `role` |  | string | 근육 이완으로 주름 완화 |  |
| 609 | `/problems/1/complaints/3/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 610 | `/problems/1/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 611 | `/problems/1/complaints/3/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 612 | `/problems/1/complaints/3/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 613 | `/problems/1/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 614 | `/problems/1/complaints/3/procedures/1/name` | `name` |  | string | 필러 |  |
| 615 | `/problems/1/complaints/3/procedures/1/category` | `category` |  | string | M2 |  |
| 616 | `/problems/1/complaints/3/procedures/1/role` | `role` |  | string | 깊은 주름 볼륨 충전 | OB-S02-08 |
| 617 | `/problems/1/complaints/3/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 618 | `/problems/1/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 619 | `/problems/1/complaints/3/procedures/1/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 620 | `/problems/1/complaints/3/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 621 | `/problems/1/complaints/3/procedures/2/name` | `name` |  | string | 리프팅기기 |  |
| 622 | `/problems/1/complaints/3/procedures/2/category` | `category` |  | string | M9 |  |
| 623 | `/problems/1/complaints/3/procedures/2/role` | `role` |  | string | 피부 타이트닝 |  |
| 624 | `/problems/1/complaints/3/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 625 | `/problems/1/complaints/3/procedures/2/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 626 | `/problems/1/complaints/3/procedures/2/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 627 | `/problems/1/complaints/3/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 628 | `/problems/1/complaints/3/procedures/3/name` | `name` |  | string | 스킨부스터 |  |
| 629 | `/problems/1/complaints/3/procedures/3/category` | `category` |  | string | M4 |  |
| 630 | `/problems/1/complaints/3/procedures/3/role` | `role` |  | string | 피부 재생·수분 공급으로 목주름·잔결 개선 | OB-S02-03 |
| 631 | `/problems/1/complaints/3/procedures/3/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 632 | `/problems/1/complaints/3/procedures/3/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 633 | `/problems/1/complaints/3/procedures/3/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 634 | `/problems/1/complaints/3/combos` | `combos` |  | array[3] | (배열 · 3개) |  |
| 635 | `/problems/1/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 636 | `/problems/1/complaints/3/combos/0/name` | `name` |  | string | 보톡스 + 필러 |  |
| 637 | `/problems/1/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 638 | `/problems/1/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 639 | `/problems/1/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 필러 |  |
| 640 | `/problems/1/complaints/3/combos/0/reason` | `reason` |  | string | 근이완 + 볼륨 = 깊은 주름 해결 |  |
| 641 | `/problems/1/complaints/3/combos/0/evidence` | `evidence` |  | string | 동적+정적 주름 동시 해결 | OB-S02-04 |
| 642 | `/problems/1/complaints/3/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 643 | `/problems/1/complaints/3/combos/1/name` | `name` |  | string | 필러 + 리프팅기기 |  |
| 644 | `/problems/1/complaints/3/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 645 | `/problems/1/complaints/3/combos/1/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 646 | `/problems/1/complaints/3/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 647 | `/problems/1/complaints/3/combos/1/reason` | `reason` |  | string | 볼륨 + 타이트닝 = 근본 해결 | OB-S02-06 |
| 648 | `/problems/1/complaints/3/combos/1/evidence` | `evidence` |  | string | 처짐 원인까지 해결 | OB-S02-06, OB-S03-01 |
| 649 | `/problems/1/complaints/3/combos/2` | `(combos 원소)` | 2 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 650 | `/problems/1/complaints/3/combos/2/name` | `name` |  | string | 스킨부스터 + 리프팅기기 |  |
| 651 | `/problems/1/complaints/3/combos/2/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 652 | `/problems/1/complaints/3/combos/2/combo/0` | `(combo 원소)` | 0 | string | 스킨부스터 |  |
| 653 | `/problems/1/complaints/3/combos/2/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 654 | `/problems/1/complaints/3/combos/2/reason` | `reason` |  | string | 재생·수분 + 타이트닝 = 목주름 복합 개선 | OB-S02-03 |
| 655 | `/problems/1/complaints/3/combos/2/evidence` | `evidence` |  | string | 고주파 리프팅과 스킨부스터 병행 시 만족도 상승(국문·영문 문헌 일치) | OB-S02-05 |
| 656 | `/problems/1/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 657 | `/problems/1/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 658 | `/problems/1/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 659 | `/problems/1/complaints/4/cc` | `cc` |  | string | 마리오네트라인 |  |
| 660 | `/problems/1/complaints/4/cc_detail` | `cc_detail` |  | string | 필러/실리프팅 | OB-S02-01, OB-S02-02 |
| 661 | `/problems/1/complaints/4/cc_group` | `cc_group` |  | string | 깊은주름 |  |
| 662 | `/problems/1/complaints/4/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 663 | `/problems/1/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 664 | `/problems/1/complaints/4/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 665 | `/problems/1/complaints/4/procedures/0/category` | `category` |  | string | M1 |  |
| 666 | `/problems/1/complaints/4/procedures/0/role` | `role` |  | string | 근육 이완으로 주름 완화 |  |
| 667 | `/problems/1/complaints/4/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 668 | `/problems/1/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 669 | `/problems/1/complaints/4/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 670 | `/problems/1/complaints/4/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 671 | `/problems/1/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 672 | `/problems/1/complaints/4/procedures/1/name` | `name` |  | string | 필러 |  |
| 673 | `/problems/1/complaints/4/procedures/1/category` | `category` |  | string | M2 |  |
| 674 | `/problems/1/complaints/4/procedures/1/role` | `role` |  | string | 깊은 주름 볼륨 충전 |  |
| 675 | `/problems/1/complaints/4/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 676 | `/problems/1/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 677 | `/problems/1/complaints/4/procedures/1/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 678 | `/problems/1/complaints/4/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 679 | `/problems/1/complaints/4/procedures/2/name` | `name` |  | string | 리프팅기기 |  |
| 680 | `/problems/1/complaints/4/procedures/2/category` | `category` |  | string | M9 |  |
| 681 | `/problems/1/complaints/4/procedures/2/role` | `role` |  | string | 피부 타이트닝 |  |
| 682 | `/problems/1/complaints/4/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 683 | `/problems/1/complaints/4/procedures/2/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 684 | `/problems/1/complaints/4/procedures/2/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 685 | `/problems/1/complaints/4/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 686 | `/problems/1/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 687 | `/problems/1/complaints/4/combos/0/name` | `name` |  | string | 보톡스 + 필러 |  |
| 688 | `/problems/1/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 689 | `/problems/1/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 690 | `/problems/1/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | 필러 |  |
| 691 | `/problems/1/complaints/4/combos/0/reason` | `reason` |  | string | 근이완 + 볼륨 = 깊은 주름 해결 |  |
| 692 | `/problems/1/complaints/4/combos/0/evidence` | `evidence` |  | string | 동적+정적 주름 동시 해결 |  |
| 693 | `/problems/1/complaints/4/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 694 | `/problems/1/complaints/4/combos/1/name` | `name` |  | string | 필러 + 리프팅기기 |  |
| 695 | `/problems/1/complaints/4/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 696 | `/problems/1/complaints/4/combos/1/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 697 | `/problems/1/complaints/4/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 698 | `/problems/1/complaints/4/combos/1/reason` | `reason` |  | string | 볼륨 + 타이트닝 = 근본 해결 |  |
| 699 | `/problems/1/complaints/4/combos/1/evidence` | `evidence` |  | string | 처짐 원인까지 해결 |  |
| 700 | `/problems/1/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 701 | `/problems/1/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 702 | `/problems/1/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 703 | `/problems/1/complaints/5/cc` | `cc` |  | string | 목주름 |  |
| 704 | `/problems/1/complaints/5/cc_detail` | `cc_detail` |  | string | 스킨부스터/기기리프팅 | OB-S02-01 |
| 705 | `/problems/1/complaints/5/cc_group` | `cc_group` |  | string | 깊은주름 |  |
| 706 | `/problems/1/complaints/5/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 707 | `/problems/1/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 708 | `/problems/1/complaints/5/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 709 | `/problems/1/complaints/5/procedures/0/category` | `category` |  | string | M1 |  |
| 710 | `/problems/1/complaints/5/procedures/0/role` | `role` |  | string | 근육 이완으로 주름 완화 |  |
| 711 | `/problems/1/complaints/5/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 712 | `/problems/1/complaints/5/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 713 | `/problems/1/complaints/5/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 714 | `/problems/1/complaints/5/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 715 | `/problems/1/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 716 | `/problems/1/complaints/5/procedures/1/name` | `name` |  | string | 필러 |  |
| 717 | `/problems/1/complaints/5/procedures/1/category` | `category` |  | string | M2 |  |
| 718 | `/problems/1/complaints/5/procedures/1/role` | `role` |  | string | 깊은 주름 볼륨 충전 |  |
| 719 | `/problems/1/complaints/5/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 720 | `/problems/1/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 721 | `/problems/1/complaints/5/procedures/1/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 722 | `/problems/1/complaints/5/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 723 | `/problems/1/complaints/5/procedures/2/name` | `name` |  | string | 리프팅기기 |  |
| 724 | `/problems/1/complaints/5/procedures/2/category` | `category` |  | string | M9 |  |
| 725 | `/problems/1/complaints/5/procedures/2/role` | `role` |  | string | 피부 타이트닝 |  |
| 726 | `/problems/1/complaints/5/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 727 | `/problems/1/complaints/5/procedures/2/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 728 | `/problems/1/complaints/5/procedures/2/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 729 | `/problems/1/complaints/5/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 730 | `/problems/1/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 731 | `/problems/1/complaints/5/combos/0/name` | `name` |  | string | 보톡스 + 필러 |  |
| 732 | `/problems/1/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 733 | `/problems/1/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 734 | `/problems/1/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 필러 |  |
| 735 | `/problems/1/complaints/5/combos/0/reason` | `reason` |  | string | 근이완 + 볼륨 = 깊은 주름 해결 |  |
| 736 | `/problems/1/complaints/5/combos/0/evidence` | `evidence` |  | string | 동적+정적 주름 동시 해결 |  |
| 737 | `/problems/1/complaints/5/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 738 | `/problems/1/complaints/5/combos/1/name` | `name` |  | string | 필러 + 리프팅기기 |  |
| 739 | `/problems/1/complaints/5/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 740 | `/problems/1/complaints/5/combos/1/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 741 | `/problems/1/complaints/5/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 742 | `/problems/1/complaints/5/combos/1/reason` | `reason` |  | string | 볼륨 + 타이트닝 = 근본 해결 |  |
| 743 | `/problems/1/complaints/5/combos/1/evidence` | `evidence` |  | string | 처짐 원인까지 해결 |  |
| 744 | `/problems/1/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 745 | `/problems/1/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 746 | `/problems/1/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 747 | `/problems/1/complaints/6/cc` | `cc` |  | string | 잔주름 |  |
| 748 | `/problems/1/complaints/6/cc_detail` | `cc_detail` |  | string | 스킨부스터/레이저/기기리프팅 | OB-S02-01, OB-S02-02 |
| 749 | `/problems/1/complaints/6/cc_group` | `cc_group` |  | string | 잔주름 | OB-S02-07 |
| 750 | `/problems/1/complaints/6/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 751 | `/problems/1/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 752 | `/problems/1/complaints/6/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 753 | `/problems/1/complaints/6/procedures/0/category` | `category` |  | string | M1 |  |
| 754 | `/problems/1/complaints/6/procedures/0/role` | `role` |  | string | 근육 이완으로 주름 완화 |  |
| 755 | `/problems/1/complaints/6/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 756 | `/problems/1/complaints/6/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 757 | `/problems/1/complaints/6/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 758 | `/problems/1/complaints/6/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 759 | `/problems/1/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 760 | `/problems/1/complaints/6/procedures/1/name` | `name` |  | string | 리프팅기기 |  |
| 761 | `/problems/1/complaints/6/procedures/1/category` | `category` |  | string | M9 |  |
| 762 | `/problems/1/complaints/6/procedures/1/role` | `role` |  | string | 피부 타이트닝 |  |
| 763 | `/problems/1/complaints/6/procedures/1/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 764 | `/problems/1/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 765 | `/problems/1/complaints/6/procedures/1/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 766 | `/problems/1/complaints/6/procedures/1/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 |  |
| 767 | `/problems/1/complaints/6/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 768 | `/problems/1/complaints/6/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 769 | `/problems/1/complaints/6/procedures/2/category` | `category` |  | string | M4 |  |
| 770 | `/problems/1/complaints/6/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 771 | `/problems/1/complaints/6/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 772 | `/problems/1/complaints/6/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 773 | `/problems/1/complaints/6/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 774 | `/problems/1/complaints/6/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 775 | `/problems/1/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 776 | `/problems/1/complaints/6/combos/0/name` | `name` |  | string | 보톡스 + 리프팅기기 |  |
| 777 | `/problems/1/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 778 | `/problems/1/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 779 | `/problems/1/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 780 | `/problems/1/complaints/6/combos/0/reason` | `reason` |  | string | 근이완 + 타이트닝 = 이중 효과 |  |
| 781 | `/problems/1/complaints/6/combos/0/evidence` | `evidence` |  | string | 동적+정적 주름 동시 해결 |  |
| 782 | `/problems/1/complaints/6/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 783 | `/problems/1/complaints/6/combos/1/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 784 | `/problems/1/complaints/6/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 785 | `/problems/1/complaints/6/combos/1/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 786 | `/problems/1/complaints/6/combos/1/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 787 | `/problems/1/complaints/6/combos/1/reason` | `reason` |  | string | 근이완 + 재생 |  |
| 788 | `/problems/1/complaints/6/combos/1/evidence` | `evidence` |  | string | 주름+피부결 개선 |  |
| 789 | `/problems/1/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 790 | `/problems/1/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S02-01 | P | `/problems/1/complaints/0/cc_detail`<br>`/problems/1/complaints/1/cc_detail`<br>`/problems/1/complaints/2/cc_detail`<br>`/problems/1/complaints/3/cc_detail`<br>`/problems/1/complaints/4/cc_detail`<br>`/problems/1/complaints/5/cc_detail`<br>`/problems/1/complaints/6/cc_detail` | S01 에서 cc_detail 은 부위·목표·기법 표현이었으나 S02 에서는 전부 시술 표현('보톡스', '필러/바이오스티뮬레이터', '필러/실리프팅', '스킨부스터/기기리프팅', '스킨부스터/레이저/기기리프팅')이다. 같은 키에 정보 종류가 problem 마다 다르다(F-05). |
| OB-S02-02 | I | `/problems/1/complaints/3/cc_detail`<br>`/problems/1/complaints/4/cc_detail`<br>`/problems/1/complaints/6/cc_detail` | cc_detail 에 적힌 시술 표현 중 일부가 같은 complaint 의 procedures 에 없다: c3 '바이오스티뮬레이터', c4 '실리프팅', c6 '레이저'. c5 '스킨부스터' 도 c5 procedures 에 없다(I-03). |
| OB-S02-03 | I | `/problems/1/complaints/3/procedures/3/role`<br>`/problems/1/complaints/3/combos/2/reason`<br>`/problems/1/complaints/3/cc` | c3 cc '팔자주름' 의 procedures[3] role 이 '피부 재생·수분 공급으로 목주름·잔결 개선', combos[2] reason 이 '... = 목주름 복합 개선' 이다. 목주름은 c5 의 cc 인데 c5 에는 스킨부스터 procedure 와 이 combo 가 없다. 내용이 다른 complaint 의 것일 가능성이 있으나 원문만으로 확정하지 않는다(I-04). |
| OB-S02-04 | P | `/problems/1/complaints/0/combos/0/evidence`<br>`/problems/1/complaints/3/combos/0/evidence` | evidence '동적+정적 주름 동시 해결' 은 서로 다른 combo(보톡스 + 리프팅기기 / 보톡스 + 필러)에 같은 문장으로 쓰였다. '+' 가 공백 없이 쓰여 combo name 의 ' + ' 와 표기가 다르다. |
| OB-S02-05 | B | `/problems/1/complaints/3/combos/2/evidence` | evidence '고주파 리프팅과 스킨부스터 병행 시 만족도 상승(국문·영문 문헌 일치)' — 문헌을 언급하나 서지 정보가 없다(B-05). '고주파 리프팅' 은 combo 원소 '리프팅기기' 와 다른 표기이며 products(울쎄라·써마지FLX)와의 대응은 원문에 없다. |
| OB-S02-06 | P | `/problems/1/complaints/3/combos/1/reason`<br>`/problems/1/complaints/3/combos/1/evidence`<br>`/problems/1/complaints/0/combos/0/reason` | '근본 해결', '처짐 원인까지 해결', '이중 효과' 같은 효과 강도 표현이 근거 없이 쓰였다. 정도 표현으로 보존. |
| OB-S02-07 | P | `/problems/1/complaints/0/cc_group`<br>`/problems/1/complaints/3/cc_group`<br>`/problems/1/complaints/6/cc_group` | cc_group 은 주름 유형(표정주름·깊은주름·잔주름)이다. c6 은 cc 와 cc_group 이 둘 다 '잔주름'. |
| OB-S02-08 | P | `/problems/1/complaints/0/procedures/0/role`<br>`/problems/1/complaints/3/procedures/1/role` | role 이 '근육 이완으로 주름 완화'(수단+결과), '깊은 주름 볼륨 충전' 처럼 기전과 대상을 함께 담는다. S01 의 같은 보톡스 role('근이완 보조'·'근육 이완')과 표기가 다르다. |
| OB-S02-09 | K | `/problems/1/complaints/0/procedures/1/products/1`<br>`/problems/1/complaints/0/procedures/1/products/2`<br>`/problems/1/complaints/0/procedures/2/products/0` | 제품 표기 '써마지FLX'·'슈링크유니버스'·'리쥬란 힐러' — 혼합 표기·붙여 쓴 복합 제품명. 형태소 분절 확인(K-02). |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 필러/바이오스티뮬레이터 | `/problems/1/complaints/3/cc_detail` [0,12) | 시술명 표현, 기호(/) |
| 필러/실리프팅 | `/problems/1/complaints/4/cc_detail` [0,7) | 시술명 표현, 기호(/) |
| 스킨부스터/기기리프팅 | `/problems/1/complaints/5/cc_detail` [0,11) | 시술명 표현, 기호(/) |
| 스킨부스터/레이저/기기리프팅 | `/problems/1/complaints/6/cc_detail` [0,15) | 시술명 표현, 기호(/) |
| 근육 이완으로 주름 완화 | `/problems/1/complaints/0/procedures/0/role` [0,13)<br>`/problems/1/complaints/1/procedures/0/role` [0,13)<br>`/problems/1/complaints/2/procedures/0/role` [0,13)<br>`/problems/1/complaints/3/procedures/0/role` [0,13)<br>`/problems/1/complaints/4/procedures/0/role` [0,13)<br>`/problems/1/complaints/5/procedures/0/role` [0,13)<br>`/problems/1/complaints/6/procedures/0/role` [0,13) | role 표현, 수단(-으로)+결과, 감소 표현(완화) |
| 피부 타이트닝 | `/problems/1/complaints/0/procedures/1/role` [0,7)<br>`/problems/1/complaints/1/procedures/1/role` [0,7)<br>`/problems/1/complaints/2/procedures/1/role` [0,7)<br>`/problems/1/complaints/3/procedures/2/role` [0,7)<br>`/problems/1/complaints/4/procedures/2/role` [0,7)<br>`/problems/1/complaints/5/procedures/2/role` [0,7)<br>`/problems/1/complaints/6/procedures/1/role` [0,7) | role 표현, 외래어 효과 표현 |
| 깊은 주름 볼륨 충전 | `/problems/1/complaints/3/procedures/1/role` [0,11)<br>`/problems/1/complaints/4/procedures/1/role` [0,11)<br>`/problems/1/complaints/5/procedures/1/role` [0,11) | role 표현, 정도 수식(깊은), 대상+기전 |
| 피부 재생·수분 공급으로 목주름·잔결 개선 | `/problems/1/complaints/3/procedures/3/role` [0,23) | role 표현, 기호(·), 수단(-으로)+결과, 부위 표현(목주름) |
| 근이완 + 타이트닝 = 이중 효과 | `/problems/1/complaints/0/combos/0/reason` [0,18)<br>`/problems/1/complaints/1/combos/0/reason` [0,18)<br>`/problems/1/complaints/2/combos/0/reason` [0,18)<br>`/problems/1/complaints/6/combos/0/reason` [0,18) | 공식형 문장, 기호(+), 기호(=), 정도 표현(이중) |
| 동적+정적 주름 동시 해결 | `/problems/1/complaints/0/combos/0/evidence` [0,14)<br>`/problems/1/complaints/1/combos/0/evidence` [0,14)<br>`/problems/1/complaints/2/combos/0/evidence` [0,14)<br>`/problems/1/complaints/3/combos/0/evidence` [0,14)<br>`/problems/1/complaints/4/combos/0/evidence` [0,14)<br>`/problems/1/complaints/5/combos/0/evidence` [0,14)<br>`/problems/1/complaints/6/combos/0/evidence` [0,14) | 기호(+ 공백 없음), 동시성(동시), 효과 강도(해결) |
| 근이완 + 재생 | `/problems/1/complaints/0/combos/1/reason` [0,8)<br>`/problems/1/complaints/1/combos/1/reason` [0,8)<br>`/problems/1/complaints/2/combos/1/reason` [0,8)<br>`/problems/1/complaints/6/combos/1/reason` [0,8) | 기호(+), 결과 없는 공식형 |
| 주름+피부결 개선 | `/problems/1/complaints/0/combos/1/evidence` [0,9)<br>`/problems/1/complaints/1/combos/1/evidence` [0,9)<br>`/problems/1/complaints/2/combos/1/evidence` [0,9)<br>`/problems/1/complaints/6/combos/1/evidence` [0,9) | 기호(+ 공백 없음), 효과 표현 |
| 근이완 + 볼륨 = 깊은 주름 해결 | `/problems/1/complaints/3/combos/0/reason` [0,19)<br>`/problems/1/complaints/4/combos/0/reason` [0,19)<br>`/problems/1/complaints/5/combos/0/reason` [0,19) | 공식형 문장, 기호(+), 기호(=), 정도 수식(깊은) |
| 볼륨 + 타이트닝 = 근본 해결 | `/problems/1/complaints/3/combos/1/reason` [0,17)<br>`/problems/1/complaints/4/combos/1/reason` [0,17)<br>`/problems/1/complaints/5/combos/1/reason` [0,17) | 공식형 문장, 기호(+), 기호(=), 효과 강도(근본) |
| 처짐 원인까지 해결 | `/problems/1/complaints/3/combos/1/evidence` [0,10)<br>`/problems/1/complaints/4/combos/1/evidence` [0,10)<br>`/problems/1/complaints/5/combos/1/evidence` [0,10) | 범위(까지), 효과 강도(해결), 증상 표현(처짐) |
| 재생·수분 + 타이트닝 = 목주름 복합 개선 | `/problems/1/complaints/3/combos/2/reason` [0,24) | 공식형 문장, 기호(·), 기호(+), 기호(=), 부위 표현(목주름) |
| 고주파 리프팅과 스킨부스터 병행 시 만족도 상승(국문·영문 문헌 일치) | `/problems/1/complaints/3/combos/2/evidence` [0,39) | 조건(-시), 병행, 증가 표현, 근거 언급(서지 없음), 괄호 보충 |
| 병행 시 | `/problems/1/complaints/3/combos/2/evidence` [15,19) | 조건(-시), 병행 |
| (국문·영문 문헌 일치) | `/problems/1/complaints/3/combos/2/evidence` [26,39) | 근거 언급(서지 없음), 괄호 보충, 기호(·) |
| 고주파 리프팅 | `/problems/1/complaints/3/combos/2/evidence` [0,7) | 시술명 표현, 기전 수식(고주파) |
| 효과 부족 시 리프팅기기 추가 | `/problems/1/complaints/0/alternatives/0` [0,16)<br>`/problems/1/complaints/1/alternatives/0` [0,16)<br>`/problems/1/complaints/2/alternatives/0` [0,16)<br>`/problems/1/complaints/3/alternatives/0` [0,16)<br>`/problems/1/complaints/4/alternatives/0` [0,16)<br>`/problems/1/complaints/5/alternatives/0` [0,16)<br>`/problems/1/complaints/6/alternatives/0` [0,16) | 조건(-시), 부족 표현, 추가 표현 |
| 써마지FLX | `/problems/1/complaints/0/procedures/1/products/1` [0,6)<br>`/problems/1/complaints/1/procedures/1/products/1` [0,6)<br>`/problems/1/complaints/2/procedures/1/products/1` [0,6)<br>`/problems/1/complaints/3/procedures/2/products/1` [0,6)<br>`/problems/1/complaints/4/procedures/2/products/1` [0,6)<br>`/problems/1/complaints/5/procedures/2/products/1` [0,6)<br>`/problems/1/complaints/6/procedures/1/products/1` [0,6) | 제품명 표현, 혼합 표기(한글+로마자) |
| 슈링크유니버스 | `/problems/1/complaints/0/procedures/1/products/2` [0,7)<br>`/problems/1/complaints/1/procedures/1/products/2` [0,7)<br>`/problems/1/complaints/2/procedures/1/products/2` [0,7)<br>`/problems/1/complaints/6/procedures/1/products/2` [0,7) | 제품명 표현, 붙여 쓴 복합어 |
| 마리오네트라인 | `/problems/1/complaints/4/cc` [0,7) | 부위·증상 표현, 외래어 복합어 |

## 이 구획에서 연 미결

- **I-03** (I) cc_detail 에 적힌 시술 표현이 같은 complaint 의 procedures 에 없다(바이오스티뮬레이터·실리프팅·스킨부스터·레이저). — 영향: cc_detail 을 procedures 목록의 요약으로 쓰면 어긋난다. 원본 변경 제안은 후속 확인 후보.
- **I-04** (I) '팔자주름' complaint(c3) 안에 '목주름' 개선을 말하는 role·combo 가 있고, '목주름' complaint(c5) 에는 그 시술·combo 가 없다. — 영향: complaint 별 시술 구성을 그대로 쓰면 다른 부위 내용이 섞인다.
- **B-05** (B) '국문·영문 문헌 일치' 는 서지 정보가 없는 근거 언급. — 영향: 근거 수준·출처를 확인할 수 없다. 외부 자료로 보충하지 않는다.
- **F-05** (F) cc_detail 의 정보 종류가 problem 마다 다르다(부위·목표·기법·시술). — 영향: cc_detail 을 단일 의미 칸으로 정의하지 못한다. 후속 의미 조사에서 값별 분해 필요.
