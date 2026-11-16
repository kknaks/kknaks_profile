"""실버 빌드 — 브론즈만 읽어 `silver_*` 6종을 만든다.

`reference/ontology_demo/scripts/` 의 `build_reservations` · `build_catalog` ·
`reviews_prepare` · `reviews_finalize` 이식이다. **변환 규칙은 기록 04 그대로**이고
입출력만 파일 → DB 로 갈았다. 새 해석을 넣지 않는다.

리뷰 채점은 재실행하지 않는다 — 기존 LLM 산출물(`silver/_scoring/output_batch_*.json`)을
그대로 병합한다(기록 04 7장 항목 4).
"""

from __future__ import annotations

import glob
import json
import re
import sqlite3
from pathlib import Path

from config import sources_for

from .errors import (
    AgreementBelowThreshold,
    ClosedListViolation,
    EnumViolation,
    MaskingResidue,
    NegativeAmount,
    ReviewScoreViolation,
    RowcountMismatch,
    UnknownBranch,
)
from .masking import MASK_TOKEN, staff_names
from db.connection import atomic

BRANCH_ALIAS = {"세라미크의원 강남": "CERAMIQUE-GN-001"}
GANGNAM_CODE = "CERAMIQUE-GN-001"
VALID_STATUS = {"내원", "취소", "부도"}

# 원본 11필드 완전 동일 행만 중복 제거한다(기록 04 2.2 — staff 포함).
DEDUP_FIELDS = ["branch", "resvDate", "chartNo", "patientName", "birthday", "phone",
                "staff", "sales", "receipt", "visitCount", "visitStatus"]

# 시술 개념 폐쇄 목록 13종 (기록 03 2장)
CONCEPTS = {"시그니처", "보톡스", "통증 케어", "필러", "제모", "세라셀 / 수액 테라피",
            "리프팅", "메디컬 스킨케어", "스킨부스터", "레이저", "모공 • 흉터",
            "지방분해", "수액"}
GU_AGREEMENT_THRESHOLD = 0.8


def age_band(birthday: str | None, resv_date: str) -> str:
    """10세 단위 연령대. 결측·이상치는 「미상」(기록 03 3장)."""
    if not birthday or len(birthday) != 8 or not birthday.isdigit():
        return "미상"
    try:
        by, bm, bd = int(birthday[:4]), int(birthday[4:6]), int(birthday[6:])
        ry, rm, rd = int(resv_date[:4]), int(resv_date[4:6]), int(resv_date[6:])
    except ValueError:
        return "미상"
    age = ry - by - (1 if (rm, rd) < (bm, bd) else 0)
    if age < 0 or age > 120:
        return "미상"
    return f"{age // 10 * 10}대" if age >= 10 else "10세 미만"


def classify_sentiment(score: float | None) -> str:
    """≥4 긍정 / 3~3.5 중립 / ≤2.5 부정 / 점수 없음 판정불가 (기록 03 1장)."""
    if score is None:
        return "판정불가"
    if score >= 4:
        return "긍정"
    if score >= 3:
        return "중립"
    return "부정"


# --- silver_reservations --------------------------------------------------


def build_reservations(conn: sqlite3.Connection) -> dict:
    rows = [dict(r) for r in conn.execute(
        "SELECT branch, resvDate, chartNo, patientName, birthday, phone, staff, "
        "sales, receipt, visitCount, visitStatus FROM bronze_vegas_reservations"
    )]
    bronze_total = len(rows)

    # fail-fast — 경고가 아니라 빌드 중단(기록 04 2.3)
    for r in rows:
        if r["visitStatus"] not in VALID_STATUS:
            raise EnumViolation(
                "visit_status enum 밖 값",
                [f"resvDate={r['resvDate']} chartNo={r['chartNo'] or '(빈값)'} "
                 f"visitStatus={r['visitStatus']!r}"],
            )
        if r["sales"] < 0 or r["receipt"] < 0 or r["visitCount"] < 0:
            raise NegativeAmount(
                "금액·횟수 음수",
                [f"resvDate={r['resvDate']} chartNo={r['chartNo'] or '(빈값)'} "
                 f"sales={r['sales']} receipt={r['receipt']} visitCount={r['visitCount']}"],
            )

    seen: set[tuple] = set()
    out, removed = [], 0
    for r in rows:
        key = tuple(r[f] for f in DEDUP_FIELDS)
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        status, sales, receipt, vc = r["visitStatus"], r["sales"], r["receipt"], r["visitCount"]
        outstanding = sales != receipt
        if r["branch"] not in BRANCH_ALIAS:
            # 다른 fail-fast 와 같이 코드를 남긴다 — KeyError 로 죽으면 원인이 로그에 안 남는다
            raise UnknownBranch(
                "지점 alias 매핑에 없는 표기",
                [f"resvDate={r['resvDate']} branch={r['branch']!r} "
                 f"(알려진 표기: {sorted(BRANCH_ALIAS)})"],
            )
        out.append((
            BRANCH_ALIAS[r["branch"]],
            f"{r['resvDate'][:4]}-{r['resvDate'][4:6]}-{r['resvDate'][6:]}",
            r["chartNo"],
            int(r["chartNo"] == ""),
            age_band(r["birthday"], r["resvDate"]),
            r["staff"], sales, receipt, vc, status,
            int(vc == 1 and status == "내원"),
            int(vc >= 2 and status == "내원"),
            int(vc == 0),
            int(status == "취소" and sales != 0),
            int(outstanding),
            ("미수" if sales > receipt else "수납 선행") if outstanding else "",
            int(sales != 0 and status == "내원"),
            int(bool(re.search(r"[A-Za-z]", r["patientName"] or ""))),  # 외국인 추정(개정 3)
        ))

    conn.execute("DELETE FROM silver_reservations")
    conn.executemany(
        "INSERT INTO silver_reservations VALUES (" + ",".join("?" * 18) + ")", out
    )
    return {
        "table": "silver_reservations", "bronze": bronze_total, "silver": len(out),
        "filter_excluded": 0, "dedup_removed": removed,
        "reconciled": bronze_total == len(out) + removed,
    }


# --- silver_reviews -------------------------------------------------------


def build_reviews(conn: sqlite3.Connection, *, scoring_dir: Path | None = None) -> dict:
    """브론즈 리뷰 + 기존 LLM 채점 산출물 → `silver_reviews`. **재채점하지 않는다.**"""
    sdir = scoring_dir or sources_for().scoring_dir
    names = staff_names(conn)

    scores: dict[str, dict] = {}
    for fp in sorted(glob.glob(str(sdir / "output_batch_*.json"))):
        with open(fp, encoding="utf-8") as f:
            for item in json.load(f):
                scores[item["review_pk"]] = item

    rows = [dict(r) for r in conn.execute(
        "SELECT reviewPk, platform, reviewDate, collectedAt, rating, body FROM bronze_reviews"
    )]

    # 위반은 원인별로 갈라 담는다 — Case Matrix 의 `ENUM_VIOLATION` 은 `visit_status` 전용이라
    # 다른 원인을 그 코드로 올리면 로그가 원인을 가리키지 못한다.
    score_errors: list[str] = []
    residue_errors: list[str] = []
    missing = [r["reviewPk"] for r in rows if r["reviewPk"] not in scores]
    if missing:
        score_errors.append(f"채점 누락 {len(missing)}건: {missing[:5]}")

    out = []
    gu_total = gu_match = exceptions = 0
    masked_count = 0
    for r in rows:
        pk = r["reviewPk"]
        body = r["body"] or ""
        masked = body
        for n in names:  # 길이 내림차순 — 뷰의 중첩 replace 와 같은 순서
            masked = masked.replace(n, MASK_TOKEN)
        if masked != body:
            masked_count += 1

        s = scores.get(pk, {})
        score = s.get("predicted_score")
        if score is not None:
            score = float(score)
            if not (0.5 <= score <= 5) or (score * 2) != int(score * 2):
                score_errors.append(f"{pk}: 점수 범위/단위 위반 {score}")
        concept = s.get("procedure_concept") or ""
        if concept and concept not in CONCEPTS:
            raise ClosedListViolation(
                "procedure_concept 폐쇄 목록 13종 밖", [f"{pk}: {concept!r}"]
            )
        evidence = s.get("score_evidence") or ""
        if score is not None and evidence not in masked:
            score_errors.append(f"{pk}: 근거 문장 본문 미실존")
        for n in names:
            if n in masked:
                # 잔존한 실명 자체는 로그에 남기지 않는다 — 리뷰 PK 만 남긴다
                residue_errors.append(f"{pk}: 마스킹 잔존")

        if r["platform"] == "강남언니" and r["rating"] and score is not None:
            gu_total += 1
            diff = abs(score - float(r["rating"]))
            if diff <= 0.5:
                gu_match += 1
            if diff >= 1.5:
                exceptions += 1

        out.append((
            pk, r["platform"], r["reviewDate"], r["collectedAt"], r["rating"],
            masked, concept, s.get("body_part") or "",
            None if score is None else score, evidence,
            classify_sentiment(score),
            "유기" if r["platform"] == "강남언니" else "개입",
        ))

    if score_errors:
        raise ReviewScoreViolation(
            f"리뷰 채점 System 검증 위반 {len(score_errors)}건", score_errors[:20])
    if residue_errors:
        raise MaskingResidue(
            f"마스킹 잔존 {len(residue_errors)}건", residue_errors[:20])

    # 게이트 6(기록 04) — 정합률 미달은 **빌드 중단**이다.
    # 이식 원본 `reviews_finalize.py:117` 의 `sys.exit(2)` 동등물. 출력만 하는 게이트는
    # 게이트가 아니다 — 재빌드에서 미달이 나도 exit 0 으로 끝나면 차단력이 없다.
    agreement = gu_match / gu_total if gu_total else 0.0
    if agreement < GU_AGREEMENT_THRESHOLD:
        raise AgreementBelowThreshold(
            f"강남언니 평점 정합률 미달 — {gu_match}/{gu_total} = {agreement:.1%} "
            f"(기준 {GU_AGREEMENT_THRESHOLD:.0%})",
            ["채점기(프롬프트·모델)를 개선해 재실행해야 한다 (기록 04 3.2 4단계)"],
        )

    conn.execute("DELETE FROM silver_reviews")
    conn.executemany("INSERT INTO silver_reviews VALUES (" + ",".join("?" * 12) + ")", out)

    return {
        "table": "silver_reviews", "bronze": len(rows), "silver": len(out),
        "filter_excluded": 0, "dedup_removed": 0, "reconciled": len(rows) == len(out),
        "masked_bodies": masked_count, "name_tokens": len(names),
        "gu_agreement": agreement, "gu_total": gu_total, "gu_match": gu_match,
        "gu_threshold": GU_AGREEMENT_THRESHOLD,
        "gu_agreement_pass": True,  # 미달이면 위에서 이미 중단됐다
        "exception_queue": exceptions,
    }


# --- silver_branch_alias · silver_catalog · silver_promotions · silver_mappings ---


def _nexus(conn: sqlite3.Connection, name: str) -> list[dict]:
    return [dict(r) for r in conn.execute(f"SELECT * FROM bronze_nexus_{name}")]


def build_catalog(conn: sqlite3.Connection) -> list[dict]:
    recon: list[dict] = []

    # --- silver_branch_alias ---
    branches = _nexus(conn, "branches")
    alias_rows = []
    for b in branches:
        for alias in {b["name"], b["slug"], b["branch_id"]}:
            alias_rows.append((alias, b["branch_id"], b["id"]))
    alias_rows.append(("세라미크의원 강남", GANGNAM_CODE, "2"))   # vegas 표기
    alias_rows.append(("세라미크의원_강남", GANGNAM_CODE, "2"))   # 리뷰 파일명 표기
    conn.execute("DELETE FROM silver_branch_alias")
    conn.executemany("INSERT INTO silver_branch_alias VALUES (?,?,?)", sorted(alias_rows))

    # --- silver_catalog ---
    cats = _nexus(conn, "categories")
    tr = {t["category_id"]: (t["name"] or "").strip()
          for t in _nexus(conn, "category_translations_ko")}
    out = []
    concepts = [c for c in cats
                if c["branch_id"] == "2" and not c["parent_id"] and not c["deleted_at"]]
    for c in concepts:
        out.append(("concept", "", c["id"], c["ca_id"], tr.get(c["id"], ""), "2", "", "", 0))
    recon.append({"table": "categories(개념)", "bronze": len(cats), "silver": len(concepts),
                  "filter_excluded": len(cats) - len(concepts), "dedup_removed": 0,
                  "reconciled": True})

    specs = [("standing", "group", "procedure_groups", "group_code"),
             ("event", "group", "event_procedure_groups", "group_code"),
             ("standing", "product", "procedure_products_ko", "product_code"),
             ("event", "product", "event_procedure_products_ko", "product_code")]
    for line, etype, name, code_col in specs:
        rows = _nexus(conn, name)
        before = len(out)
        kept = 0
        for r in rows:
            # 원본 `build_catalog.py:60` 과 같은 의미 — 컬럼이 **없을 때만** ko 로 본다.
            # `or "ko"` 로 쓰면 빈 문자열까지 ko 취급해 원본과 필터 결과가 갈린다.
            if r.get("language", "ko") != "ko":
                continue
            kept += 1
            out.append((etype, line, r["id"], r.get(code_col, ""), r.get("name", ""),
                        r["branch_id"], r.get("regular_price", ""),
                        r.get("discounted_price", ""), int(bool(r["deleted_at"]))))
        # 실제로 산출에 들어간 행수로 대사한다 — `kept + (len(rows) - kept)` 처럼
        # 항상 참인 식은 「대사했다」는 착시만 남기고 append 누락을 못 잡는다.
        appended = len(out) - before
        excluded = sum(1 for r in rows if r.get("language", "ko") != "ko")
        recon.append({"table": name, "bronze": len(rows), "silver": appended,
                      "filter_excluded": excluded, "dedup_removed": 0,
                      "reconciled": len(rows) == appended + excluded})

    conn.execute("DELETE FROM silver_catalog")
    conn.executemany("INSERT INTO silver_catalog VALUES (" + ",".join("?" * 9) + ")", out)
    # 적재본 = 산출 행수. 소스별 대사가 전부 맞아도 적재에서 새면 여기서 걸린다.
    loaded = conn.execute("SELECT COUNT(*) FROM silver_catalog").fetchone()[0]
    recon.append({"table": "silver_catalog(적재)", "bronze": len(out), "silver": loaded,
                  "filter_excluded": 0, "dedup_removed": 0, "reconciled": loaded == len(out)})

    # --- silver_promotions ---
    # `source_id` 는 원천 내부 id 를 그대로 보존한 컬럼이다. 이게 없으면 골드가
    # 프로모션 구성(매핑 사슬)을 잇지 못해 브론즈를 직접 읽게 된다 — 계층 경계 위반.
    # **식별자를 버리지 않는 것이지 값을 바꾸는 게 아니라서 이식 원칙과 충돌하지 않는다.**
    promo_out = []
    v1 = _nexus(conn, "promotions_v1")
    for r in v1:
        promo_out.append(("v1", r["promotion_code"], "", r["branch_id"],
                          r["promotion_started_at"], r["promotion_ended_at"],
                          r["display_started_at"], r["display_ended_at"],
                          int(bool(r["deleted_at"])), r["id"]))
    v2 = _nexus(conn, "promotion_v2s")
    v2_ko = [r for r in v2 if r["language"] == "ko"]
    for r in v2_ko:
        promo_out.append(("v2", r["promotion_code"], r.get("title", ""), r["branch_id"],
                          r["promotion_started_at"], r["promotion_ended_at"],
                          r["display_started_at"], r["display_ended_at"],
                          int(bool(r["deleted_at"])), r["id"]))
    recon.append({"table": "promotions_v1", "bronze": len(v1), "silver": len(v1),
                  "filter_excluded": 0, "dedup_removed": 0, "reconciled": True})
    recon.append({"table": "promotion_v2s", "bronze": len(v2), "silver": len(v2_ko),
                  "filter_excluded": len(v2) - len(v2_ko), "dedup_removed": 0,
                  "reconciled": True})
    conn.execute("DELETE FROM silver_promotions")
    conn.executemany(
        "INSERT INTO silver_promotions VALUES (" + ",".join("?" * 10) + ")", promo_out)

    # --- silver_mappings (개정 1 — 매핑 3종 전량, 하드 삭제 테이블이라 필터 없음) ---
    map_specs = [("standing_group_product", "procedure_group_product_mappings",
                  "procedure_group_id", "procedure_product_id"),
                 ("event_group_product", "event_procedure_group_product_mappings",
                  "event_procedure_group_id", "event_procedure_product_id"),
                 ("promo_v2_event_group", "promotion_v2_event_group_mappings",
                  "promotion_v2_id", "event_procedure_group_id")]
    map_rows = []
    for mtype, name, pcol, ccol in map_specs:
        rows = _nexus(conn, name)
        for r in rows:
            map_rows.append((mtype, r[pcol], r[ccol]))
        recon.append({"table": name, "bronze": len(rows), "silver": len(rows),
                      "filter_excluded": 0, "dedup_removed": 0, "reconciled": True})
    conn.execute("DELETE FROM silver_mappings")
    conn.executemany("INSERT INTO silver_mappings VALUES (?,?,?)", map_rows)

    # 대사는 「했다」가 아니라 「맞았다」여야 한다 — 한 소스라도 어긋나면 빌드 중단
    broken = [r["table"] for r in recon if not r["reconciled"]]
    if broken:
        raise RowcountMismatch(
            f"카탈로그·프로모션 행수 대사 불일치 {len(broken)}건",
            [f"{r['table']}: 브론즈 {r['bronze']:,} vs 실버 {r['silver']:,} "
             f"+ 제외 {r['filter_excluded']:,}" for r in recon if not r["reconciled"]],
        )
    return recon


def build(conn: sqlite3.Connection, *, scoring_dir: Path | None = None) -> dict:
    """실버 전 계층 빌드. fail-fast 위반이면 되감기고 이전 상태가 남는다."""
    with atomic(conn, "silver"):
        resv = build_reservations(conn)
        if not resv["reconciled"]:
            raise RowcountMismatch(
                "예약 행수 대사 불일치 — 브론즈 ≠ 실버 + 제외 + 중복 제거",
                [f"브론즈 {resv['bronze']:,} vs 실버 {resv['silver']:,} "
                 f"+ 제외 {resv['filter_excluded']} + 중복 {resv['dedup_removed']:,}"],
            )
        reviews = build_reviews(conn, scoring_dir=scoring_dir)
        catalog = build_catalog(conn)

    counts = {
        t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in ("silver_reservations", "silver_reviews", "silver_catalog",
                  "silver_promotions", "silver_branch_alias", "silver_mappings")
    }
    return {"reservations": resv, "reviews": reviews, "catalog_recon": catalog, "counts": counts}
