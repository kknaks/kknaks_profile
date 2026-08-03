"""제품 레지스트리 도메인 DTO (KDEV-WORK-018 P2).

**계층을 넘는 데이터는 여기 정의된 pydantic 모델로만 옮긴다** — `40-architecture/system`
「백엔드 계층 규약」. dict 를 그대로 넘기면 키 오타가 런타임까지 살아남고, 어느 계층이
무엇을 넣었는지 추적이 안 된다.

두 방향을 구분한다.

- `repository` → `service` → `api` : `TrackedRepoDTO`
- `api` → `service` → `repository` : `RepoCreate` · `RepoPatch`

**ORM(`core.models.TrackedRepo`)은 이 파일을 지나지 않는다.** repository 가 경계에서
변환을 끝내므로, service 는 세션 수명도 lazy load 도 알 필요가 없다.

`api/schemas/products.py` 의 요청·응답 모델과 **겸하지 않는다.** 겸하면 HTTP 표면을
바꿀 때 도메인이 따라 바뀌고, 반대로 도메인 필드가 API 로 새어 나간다.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrackedRepoDTO(BaseModel):
    """레지스트리 한 행. **repository 가 돌려주는 유일한 형태다.**

    운영 상태(`last_fetched_at`·`last_error`)를 함께 들고 다닌다 — 화면이 "추적 중인데
    클론은 실패" 를 한 행에서 읽어야 하기 때문이다. 그 조합이 정상이고, 그것이 곧
    고쳐야 할 것을 가리킨다(KDEV-SPEC-014 §4 State).
    """

    model_config = ConfigDict(frozen=True)

    id: int
    slug: str
    type: str
    detail: str | None = None
    product_slug: str | None = None
    account: str
    enabled: bool
    path_rules: list | None = None
    last_fetched_at: datetime | None = None
    last_error: str | None = None


class RepoCreate(BaseModel):
    """레지스트리 행 생성 입력.

    `product_slug` 가 실재하는 디렉토리인지 **여기서 보지 않는다.** 저장은 되고 경고는
    조회 응답이 싣는다(D7) — 막지 않고 알린다.
    """

    slug: str
    type: str
    detail: str | None = None
    product_slug: str | None = None
    account: str = "personal"
    enabled: bool = True


class RepoPatch(BaseModel):
    """부분 수정. **`None` 과 "값을 비운다" 를 구분해야 한다.**

    `detail` 을 지우는 것(company → studio 전환)과 손대지 않는 것이 다르므로,
    `model_fields_set` 으로 실제 전달된 필드만 반영한다. `exclude_unset=True` 가
    그 구분을 만든다 — 이 모델을 dict 로 펼치는 쪽이 반드시 그 옵션을 쓴다.
    """

    detail: str | None = None
    product_slug: str | None = None
    enabled: bool | None = None
