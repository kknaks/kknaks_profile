#!/usr/bin/env python3
"""SC 조직도 CSV 한 장을 ax-workspace dataset 폴더의 표로 옮긴다.

읽는 것은 조직도 CSV 한 장, 쓰는 것은 `modules/datasets/schema.py` 가 정한 표 11개다. 표준 라이브러리만 쓰고,
데이터베이스를 모르며, 같은 입력에 같은 출력을 낸다 — 두 번 돌려도 폴더의 바이트가 같다.

원문이 말하지 않는 것은 만들어 내지 않는다. 사번만은 예외로, 원문에 사번 열이 없어 화면이 사람을 부를 이름이
없기 때문에 **임시 번호**(1001부터)를 `members.key` 로 붙인다. 그 밖에 입사일·직무·프로젝트는 비운다.

옮기지 않는 열: 지메일·메모·담당 프로젝트. 비고는 겸임 판정에만 쓰고 저장하지 않는다.
전화·생년월일은 `members` 의 옵셔널 열로 들어간다 — 원문이 말한 사람만이고, 나머지는 빈 칸이다.
위하고메일은 `logins` 의 주소가 된다 — 빈 사람은 계정을 만들지 않는다. 비밀번호는 이 폴더에 없고 적재할 때 환경이 준다.
이 파일에는 사람의 이름이 상수로 들어가지 않는다 — 겸임과 동명이인은 이름이 아니라 규칙이 가른다.

    python3 build_dataset.py <조직도.csv> <dataset 폴더>

계정은 165명 전원에게 하나씩 있고, 주소는 회사 메일이다. 위하고메일이 적힌 사람은 그 주소를 그대로 쓰고(대소문자
정규화만), 아직 적히지 않은 사람은 `<사번>@companysc.com` 을 **임시로** 쓴다. 가짜 도메인은 쓰지 않는다 —
로그인 계정은 회사 계정 하나이고, 실제 주소가 오면 CSV 를 갱신해 다시 만들면 임시 주소가 덮인다.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
import re
from pathlib import Path
import sys

#: 회사 루트. CSV 는 부서부터 시작하므로 위 한 칸은 여기서 준다.
COMPANY_KEY = "the-sc"
COMPANY_NAME = "더에쓰씨"

#: 부서·팀 slug — sc-org 선행 적재에서 쓰던 표를 그대로 재사용한다(이름이 같으면 키도 같아야 한다).
DEPT_SLUGS = {
    "경영진": "executive",
    "글로벌마케팅부": "global-marketing",
    "글로벌사업부": "global-business",
    "에스테틱사업부": "aesthetic-business",
    "국내사업부": "domestic-business",
    "비주얼콘텐츠부": "visual-content",
    "경영관리부": "management-support",
    "국내마케팅부": "domestic-marketing",
    "국내전략기획부": "domestic-strategy",
    "기타": "etc",
}

TEAM_SLUGS = {
    "G일본": "g-japan",
    "G중국": "g-china",
    "G태국1": "g-thailand-1",
    "G태국2": "g-thailand-2",
    "G대만": "g-taiwan",
    "G베트남": "g-vietnam",
    "G인도네시아": "g-indonesia",
    "G홍콩": "g-hongkong",
    "GB태국3": "gb-thailand-3",
    "GB일본": "gb-japan",
    "GB영어+아랍": "gb-english-arabic",
    "GB글로벌컨텐츠": "gb-global-content",
    "GB인도네시아": "gb-indonesia",
    "GBCIS": "gb-cis",
    "비주얼디자인팀": "visual-design",
    "영상콘텐츠팀": "video-content",
    "인사총무팀": "hr-general-affairs",
    "재무회계팀": "finance-accounting",
}

#: 직급 → `grades`. 나열 순서가 곧 서열이고 `display_order` 가 된다.
#:
#: `grades` 와 `positions` 는 조직을 묻지 않는 전역 어휘라, 같은 데이터베이스에 서 있는 예시 회사와 키를 나눠 쓴다.
#: 예시 회사에는 이미 `associate`(대리) · `director`(부장) 가 있고 SC 는 같은 키를 주임 · 이사로 쓰므로, 접두사
#: 없이 넣으면 먼저 있던 이름이 이깁니다 — 화면에 「주임」이 「대리」로 나온다. 그래서 SC 어휘에는 `sc-` 를 붙인다.
#: 접두사를 뺀 뒷부분은 sc-org 선행 적재의 slug 표 그대로다.
VOCABULARY_PREFIX = "sc-"

GRADE_SLUGS = {
    "사원": "sc-staff",
    "주임": "sc-associate",
    "대리": "sc-assistant-manager",
    "과장": "sc-manager",
    "차장": "sc-deputy-general-manager",
    "부장": "sc-general-manager",
    "이사": "sc-director",
    "상무": "sc-managing-director",
    "전무": "sc-executive-vice-president",
    "대표이사": "sc-ceo",
}

#: 이 직급인 사람은 대표다. 직책 열은 비어 있어서 직급이 유일한 근거다.
EXECUTIVE_GRADE = "대표이사"

#: 고용형태 → `members.employment_type`. 빈칸은 빈칸으로 남긴다(선택 열).
EMPLOYMENT_TYPES = {"정규직": "regular", "시간제": "part_time"}

#: 직책 → `positions` 정의. 부서 단계의 「팀장」은 부서장 자리로 간다 — 부서에는 head 슬롯이 하나뿐이다.
POSITIONS = (
    # key, name, unit_type, slot, role_key
    ("sc-dept-head", "부서장", "division", "head", "team-lead"),
    ("sc-team-lead", "팀장", "team", "head", "team-lead"),
    ("sc-deputy-team-lead", "부팀장", "team", "deputy", "team-lead"),
)
TITLES = {"부서장": "sc-dept-head", "팀장": "sc-team-lead", "부팀장": "sc-deputy-team-lead"}


#: 겸임 표시. 같은 이름의 행이 이 표시를 달고 다시 나오면 같은 사람의 두 번째 소속이다.
CONCURRENT_MARK = "겸임"

#: 임시 사번의 시작. 원문에 사번이 없어 병합 후 사람 순서(CSV 첫 등장)로 붙인다.
FIRST_EMPLOYEE_NUMBER = 1001

ROLE_EXECUTIVE = "executive"
ROLE_LEAD = "team-lead"
ROLE_MEMBER = "member"

#: 계정을 만들 주소가 적힌 열. 지메일이 아니라 회사 메일이다.
LOGIN_EMAIL_COLUMN = "위하고메일"

#: 아직 주소가 적히지 않은 사람에게 줄 임시 주소의 도메인. CSV 의 위하고메일 대부분이 쓰는 회사 도메인이며,
#: 가짜 도메인이 아니라 실제 주소가 올 자리를 사번으로 채워 둔 것이다.
FALLBACK_EMAIL_DOMAIN = "companysc.com"

#: 전화는 숫자와 하이픈만 남긴다 — 괄호·공백·국가번호 표기가 섞여도 한 모양이 되도록.
PHONE_ALLOWED = re.compile(r"[^0-9-]")

#: 이번 CSV 가 채우지 않는 표. 헤더만 남긴다 — 파일이 없으면 검사가 걸린다.
EMPTY_TABLES = {
    "jobs": ["key", "name"],
    "job_assignments": ["member_key", "job_key", "kind"],
    "projects": ["key", "name", "state", "starts_on", "ends_on", "description"],
    "project_assignments": ["member_key", "project_key", "kind", "valid_from", "valid_until"],
}


class SourceError(SystemExit):
    """CSV 가 이 변환이 아는 모양이 아니다. 지어내지 않고 멈춘다."""


def warn(message: str) -> None:
    print(f"경고: {message}", file=sys.stderr)


def parse_day(raw: str) -> date | None:
    """사람이 적은 날짜. 비어 있으면 오늘이 되지 않고 그대로 비어 있다."""
    raw = raw.strip()
    if not raw:
        return None
    for pattern in ("%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, pattern).date()
        except ValueError:
            continue
    return None


def normalize_phone(raw: str) -> str:
    """사람이 적은 전화번호. 숫자와 하이픈만 남기고, 비어 있으면 비운 채로 둔다."""
    return PHONE_ALLOWED.sub("", raw.strip()).strip("-")


class Person:
    """CSV 의 여러 행이 가리키는 한 사람. 소속은 나온 순서대로 쌓이고 첫 번째가 주소속이다."""

    __slots__ = (
        "key", "display_name", "grade", "employment_type", "employed_from", "email", "phone", "birth_date",
        "units", "titles", "has_title",
    )

    def __init__(self, key: str, display_name: str) -> None:
        self.key = key
        self.display_name = display_name
        self.grade = ""
        self.employment_type = ""
        self.employed_from: date | None = None
        #: 계정을 만들 주소. 원문이 비워 둔 사람은 계정이 없다.
        self.email = ""
        #: 인사 정보. 원문이 말한 사람만 갖는다.
        self.phone = ""
        self.birth_date: date | None = None
        #: 이 사람이 속한 조직 key — CSV 순서. 첫 번째가 주소속이다.
        self.units: list[str] = []
        #: (조직 key, position key) — 직책이 적힌 행마다 하나.
        self.titles: list[tuple[str, str]] = []
        self.has_title = False


def read_rows(source: Path) -> list[dict[str, str]]:
    with source.open(encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def build(rows: list[dict[str, str]]) -> dict[str, list[list[str]]]:
    """CSV 행들 → 표별 데이터 행. 여기서만 판단하고, 쓰기는 하지 않는다."""
    cell = lambda row, column: (row.get(column) or "").strip()  # noqa: E731

    # ── 조직: 부서와 팀이 CSV 에 처음 나온 순서가 곧 표시 순서다.
    departments: list[str] = []
    teams: dict[str, list[str]] = {}
    for index, row in enumerate(rows, start=2):
        dept, team = cell(row, "부서"), cell(row, "팀")
        if not dept:
            raise SourceError(f"{index}행: 부서가 비어 있습니다")
        if dept not in DEPT_SLUGS:
            raise SourceError(f"{index}행: 매핑 없는 부서 {dept!r} — DEPT_SLUGS 에 추가하라")
        if team and team not in TEAM_SLUGS:
            raise SourceError(f"{index}행: 매핑 없는 팀 {team!r} — TEAM_SLUGS 에 추가하라")
        if dept not in teams:
            departments.append(dept)
            teams[dept] = []
        if team and team not in teams[dept]:
            teams[dept].append(team)

    units: list[list[str]] = [[COMPANY_KEY, COMPANY_NAME, "company", "", "0"]]
    for order, dept in enumerate(departments, start=1):
        units.append([DEPT_SLUGS[dept], dept, "division", COMPANY_KEY, str(order)])
        for team_order, team in enumerate(teams[dept], start=1):
            units.append([TEAM_SLUGS[team], team, "team", DEPT_SLUGS[dept], str(team_order)])

    # ── 사람: 「비고=겸임 + 같은 이름 + 앞 행에 이미 겸임으로 나옴」이면 같은 사람이다.
    #    이름이 같아도 겸임 표시가 없으면 다른 사람이다 — 동명이인은 병합하지 않는다.
    people: list[Person] = []
    concurrent_by_name: dict[str, Person] = {}
    division_level_leads = 0
    unknown_employment = 0
    grade_conflicts = 0
    no_team_rows = 0

    for index, row in enumerate(rows, start=2):
        name = cell(row, "이름")
        if not name:
            raise SourceError(f"{index}행: 이름이 비어 있습니다")
        grade = cell(row, "직급")
        if grade not in GRADE_SLUGS:
            raise SourceError(f"{index}행: 매핑 없는 직급 {grade!r} — GRADE_SLUGS 에 추가하라")
        title = cell(row, "직책")
        if title and title not in TITLES:
            raise SourceError(f"{index}행: 매핑 없는 직책 {title!r}")
        dept, team = cell(row, "부서"), cell(row, "팀")
        if not team:
            no_team_rows += 1
        unit_key = TEAM_SLUGS[team] if team else DEPT_SLUGS[dept]
        is_concurrent = CONCURRENT_MARK in cell(row, "비고")

        person = concurrent_by_name.get(name) if is_concurrent else None
        if person is None:
            person = Person(f"{FIRST_EMPLOYEE_NUMBER + len(people)}", name)
            employment = cell(row, "고용형태")
            if employment and employment not in EMPLOYMENT_TYPES:
                warn(f"{index}행: 모르는 고용형태 {employment!r} — 비워 둔다")
                unknown_employment += 1
            person.grade = GRADE_SLUGS[grade]
            person.employment_type = EMPLOYMENT_TYPES.get(employment, "")
            raw_day = cell(row, "입사일")
            person.employed_from = parse_day(raw_day)
            if raw_day and person.employed_from is None:
                warn(f"{index}행: 읽을 수 없는 입사일 형식 — 비워 둔다")
            people.append(person)
            if is_concurrent:
                concurrent_by_name[name] = person
        elif person.grade != GRADE_SLUGS[grade]:
            warn(f"{index}행: 겸임 행의 직급이 첫 행과 다릅니다 — 첫 값을 쓴다")
            grade_conflicts += 1

        if not person.email:
            person.email = cell(row, LOGIN_EMAIL_COLUMN)
        if not person.phone:
            person.phone = normalize_phone(cell(row, "전화"))
        if person.birth_date is None:
            raw_born = cell(row, "생년월일")
            person.birth_date = parse_day(raw_born)
            if raw_born and person.birth_date is None:
                warn(f"{index}행: 읽을 수 없는 생년월일 형식 — 비워 둔다")
        if unit_key not in person.units:
            person.units.append(unit_key)
        if title:
            person.has_title = True
            position = TITLES[title]
            if position == "sc-team-lead" and not team:
                # 부서에는 팀장 자리가 없다. 부서 단계의 「팀장」은 그 부서의 head 로 넣는다.
                position = "sc-dept-head"
                division_level_leads += 1
                warn(f"{index}행: 팀 없이 「팀장」 — 부서장(sc-dept-head) 자리로 넣는다")
            if position == "sc-dept-head" and team:
                warn(f"{index}행: 팀에 붙은 「부서장」 — 팀장(sc-team-lead) 자리로 넣는다")
                position = "sc-team-lead"
            pair = (unit_key, position)
            if pair not in person.titles:
                person.titles.append(pair)

    # ── 표
    grades = [[slug, name, str(order)] for order, (name, slug) in enumerate(GRADE_SLUGS.items(), start=1)]
    positions = [list(entry) for entry in POSITIONS]

    members: list[list[str]] = []
    memberships: list[list[str]] = []
    appointments: list[list[str]] = []
    logins: list[list[str]] = []
    #: 아직 위하고메일이 없어 임시 주소를 받은 사람. 원문이 준 주소와 섞이지 않도록 따로 센다.
    provisional_logins: list[str] = []
    role_counts = {ROLE_EXECUTIVE: 0, ROLE_LEAD: 0, ROLE_MEMBER: 0}
    role_of: dict[str, str] = {}

    for person in people:
        primary_unit = person.units[0]
        if person.grade == GRADE_SLUGS[EXECUTIVE_GRADE]:
            role = ROLE_EXECUTIVE
        elif person.has_title:
            role = ROLE_LEAD
        else:
            role = ROLE_MEMBER
        role_counts[role] += 1
        role_of[person.key] = role
        members.append(
            [
                person.key,
                person.display_name,
                "active",
                person.employment_type,
                primary_unit,
                role,
                person.grade,
                person.employed_from.isoformat() if person.employed_from else "",
                "",
                person.phone,
                person.birth_date.isoformat() if person.birth_date else "",
            ]
        )
        for position, unit_key in enumerate(person.units):
            memberships.append([person.key, unit_key, "primary" if position == 0 else "additional", "", ""])
        for unit_key, position_key in person.titles:
            kind = "primary" if unit_key == primary_unit else "concurrent"
            appointments.append([person.key, unit_key, position_key, kind, "", ""])

    # ── 계정: 165명 전원에게 하나씩. 위하고메일이 적힌 사람은 그 주소, 아직 없는 사람은 사번으로 만든
    #    같은 회사 도메인의 임시 주소다. 사번에서만 만들어지므로 이름·전화 같은 원문 값이 주소에 새지 않고,
    #    실제 주소가 CSV 에 들어오면 다시 만들 때 그대로 덮인다.
    for person in people:
        if person.email:
            logins.append([person.key, person.email.strip().lower()])
        else:
            logins.append([person.key, f"{person.key}@{FALLBACK_EMAIL_DOMAIN}"])
            provisional_logins.append(person.key)

    if provisional_logins:
        warn(
            f"위하고메일이 아직 없는 {len(provisional_logins)}명에게 <사번>@{FALLBACK_EMAIL_DOMAIN} 임시 주소를 줬다 — "
            "실제 주소가 오면 CSV 를 갱신해 다시 만들면 덮인다"
        )

    print(
        "요약: "
        f"부서 {len(departments)} · 팀 {sum(len(v) for v in teams.values())} · 조직 {len(units)} · "
        f"직급 {len(grades)} · 직책 {len(positions)} · 사람 {len(people)}(원본 {len(rows)}행) · "
        f"소속 {len(memberships)} · 보직 {len(appointments)} · "
        f"계정 {len(logins)}(위하고메일 {len(logins) - len(provisional_logins)} · 임시 주소 {len(provisional_logins)}) · "
        f"전화 {sum(1 for p in people if p.phone)} · 생년월일 {sum(1 for p in people if p.birth_date)}",
        file=sys.stderr,
    )
    print(
        "판단이 걸린 곳: "
        f"겸임 병합 {len(rows) - len(people)}행({len(concurrent_by_name)}명) · "
        f"부서 단계 팀장 {division_level_leads} · 팀 없는 행 {no_team_rows} · "
        f"모르는 고용형태 {unknown_employment} · 겸임 직급 불일치 {grade_conflicts} · "
        f"역할 executive {role_counts[ROLE_EXECUTIVE]} · team-lead {role_counts[ROLE_LEAD]} · member {role_counts[ROLE_MEMBER]}",
        file=sys.stderr,
    )

    return {
        "organization_units": units,
        "grades": grades,
        "positions": positions,
        "members": members,
        "memberships": memberships,
        "appointments": appointments,
        "logins": logins,
    }


HEADERS = {
    "organization_units": ["key", "name", "unit_type", "parent_key", "display_order"],
    "grades": ["key", "name", "display_order"],
    "positions": ["key", "name", "unit_type", "slot", "role_key"],
    "members": [
        "key",
        "display_name",
        "employment_state",
        "employment_type",
        "primary_unit_key",
        "role_key",
        "grade_key",
        "employed_from",
        "employed_until",
        "phone",
        "birth_date",
    ],
    "memberships": ["member_key", "unit_key", "kind", "valid_from", "valid_until"],
    "appointments": ["member_key", "unit_key", "position_key", "kind", "valid_from", "valid_until"],
    "logins": ["member_key", "email"],
}


def write_tables(target: Path, tables: dict[str, list[list[str]]]) -> None:
    """표를 폴더에 쓴다. 채우는 표는 덮어쓰고, 이 CSV 가 말하지 않는 표는 헤더만 남긴다."""
    target.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        with (target / f"{name}.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(HEADERS[name])
            writer.writerows(rows)
    for name, header in EMPTY_TABLES.items():
        with (target / f"{name}.csv").open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle).writerow(header)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SC 조직도 CSV → ax-workspace dataset 표")
    parser.add_argument("source", type=Path, help="조직도 CSV")
    parser.add_argument("target", type=Path, help="dataset 폴더 (manifest.yaml 이 있는 곳)")
    arguments = parser.parse_args(argv)

    source = arguments.source.expanduser().resolve()
    target = arguments.target.expanduser().resolve()
    if not source.is_file():
        raise SourceError(f"조직도 CSV 가 없습니다: {source}")

    tables = build(read_rows(source))
    write_tables(target, tables)
    print(f"{target} 에 표 {len(tables) + len(EMPTY_TABLES)}개를 썼습니다.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
