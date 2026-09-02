from __future__ import annotations

from dto.profile import ProfileDTO
from repository.career_repo import CareerRepository
from repository.company_repo import CompanyRepository
from repository.problem_repo import ProblemRepository
from repository.profile_repo import ProfileRepository
from repository.product_repo import ProductRepository
from service.persona_service import PersonaService


def _service() -> PersonaService:
    return PersonaService(
        CareerRepository(),
        ProductRepository(),
        ProblemRepository(),
        CompanyRepository(),
        ProfileRepository(),
    )


def test_render_profile_contains_every_public_profile_field() -> None:
    profile = ProfileDTO(
        id=1,
        handle="kknaks",
        name="이건학",
        role="백엔드 엔지니어",
        years="1년차",
        location="서울, 대한민국",
        focus="AI · Python",
        avatar_url="/assets/profile/me.png",
        email="dh221009@naver.com",
        github="github.com/kknaks",
        linkedin="linkedin.com/in/kknaks",
        stack=["Python", "FastAPI"],
    )

    rendered = _service()._render_profile(profile)

    assert "SoT 는 DB(profile)" in rendered
    assert "# 이건학 · 프로필" in rendered
    assert "| 핸들 | `kknaks` |" in rendered
    assert "| 역할 | 백엔드 엔지니어 |" in rendered
    assert "| 연차 | 1년차 |" in rendered
    assert "| 위치 | 서울, 대한민국 |" in rendered
    assert "| 집중 분야 | AI · Python |" in rendered
    assert "| 프로필 이미지 | /assets/profile/me.png |" in rendered
    assert "| 이메일 | dh221009@naver.com |" in rendered
    assert "| GitHub | github.com/kknaks |" in rendered
    assert "| LinkedIn | linkedin.com/in/kknaks |" in rendered
    assert rendered.endswith("Python · FastAPI\n")


def test_render_profile_marks_nullable_fields_without_inventing_values() -> None:
    profile = ProfileDTO(
        id=1,
        handle="kknaks",
        name="이건학",
        role="백엔드 엔지니어",
        years=None,
        location=None,
        focus=None,
        avatar_url=None,
        email="dh221009@naver.com",
        github=None,
        linkedin=None,
        stack=None,
    )

    rendered = _service()._render_profile(profile)

    assert "| 연차 | - |" in rendered
    assert "| 위치 | - |" in rendered
    assert "| 집중 분야 | - |" in rendered
    assert "| 프로필 이미지 | - |" in rendered
    assert "| GitHub | - |" in rendered
    assert "| LinkedIn | - |" in rendered
    assert rendered.endswith("_(아직 없음)_\n")
