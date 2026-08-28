"""시스템 프롬프트 — SPEC-017 §5 프롬프트 계약.

네 조항이 전부다: ① 1인칭 ② tool 로 확인한 것만 ③ 거절 규칙 ④ 이력으로 되돌리기.

## ③ 의 거절 범위는 **좁게** 쓴다 — 넓은 문구가 공개 자료까지 삼킨다

원래 「재직 회사의 내부 정보」였다. 그 한 마디가 **회사 제품의 공개 소개(showcase)까지**
거절 대상으로 읽혔다 — 「회사 프로젝트 뭐하고 있어?」에 tool 을 아예 안 부르고 사리는 것이
관측됐다(2026-08-28). 그래서 거절은 **미공개**(미공개 스펙·내부 구성·기밀)로 좁히고,
공개 소개는 회사 제품 tool 로 **적극 안내**하라고 명시한다(spec v0.0.9 §5).

## 「이전 턴에서 사렸더라도 이 지침이 우선」이 하는 일

관측된 실패는 **resume 한 세션**에서만 났고 새 대화는 정상이었다. codex 가 자기 세션의
지난 턴을 문맥으로 갖고 있어, 한 번 사린 답이 **선례**가 돼 다음 턴을 끌어당긴 것이다.

이 프롬프트는 resume 여부와 무관하게 **매 턴 다시 실린다**(`runtime.build_plan_for` →
`build_submission` 의 첫 블록). 그래서 지침을 고치면 살아 있는 세션에도 곧바로 닿는다 —
다만 지난 턴과 충돌할 때 어느 쪽이 이기는지를 말해 주지 않으면 모델이 선례를 따른다.
마지막 한 문장이 그 우선순위를 못 박는 장치다.

## 상시 주입은 프로필 + 커리어 개요 한 단락뿐이다 (§7 OQ-3)

전부 싣고 싶은 유혹이 있지만, 그러면 모델이 tool 을 안 부른다 — 그리고 `chat_exposed`
가 정하는 경계가 프롬프트를 우회하게 된다. **경계는 tool 이 갖는다**(DEC-027 D4)는
결정과 정합하려면 상시 주입은 「누구인지」까지여야 한다.

프로필조차 tool 로 다시 확인할 수 있게 `get_profile` 을 남겨 둔 것은, 여기 실린 요약이
낡았을 때 모델이 스스로 갱신할 길을 주기 위해서다.

## 대화 기록 동봉은 resume 이 없을 때만이다 (DEC-027 D2)

세션이 살아 있으면 codex 가 문맥을 갖고 있다 — 같은 내용을 두 번 실으면 토큰만 먹고
「어느 쪽이 진실인가」가 생긴다. 세션이 없거나 죽어 새로 시작할 때만 최근 몇 개를 싣는다.
"""

from __future__ import annotations

from dto.chat import ChatMessageDTO
from dto.chat_tool import ChatProfileDTO
from models.chat import ROLE_ASSISTANT

#: 새 세션에 동봉할 최근 메시지 수(질문+답변 합산). 맥락을 잇기에 충분하고 프롬프트를
#: 먹지 않는 선. 세션 resume 이 되면 아예 싣지 않는다.
RECENT_MESSAGE_LIMIT = 6

#: 동봉하는 지난 답변 한 건의 길이 상한 — 긴 답변 하나가 프롬프트를 다 먹지 않게.
_RECENT_BODY_MAX = 600

_RULES = """\
# 너는 누구인가

너는 이건학의 이력 데이터가 직접 대답하는 창구다. 방문자는 대개 채용담당자이고,
로그인 없이 이 사이트에서 묻고 있다.

# 어떻게 대답하나

1. **1인칭으로 말한다.** 「저는 …했습니다」 — 「건학님은」 같은 비서 톤을 쓰지 않는다.
2. **tool 로 확인한 것만 말한다.** 기억이나 추측으로 채우지 않는다. 답하기 전에
   관련 tool 을 부르고, 기록에 없으면 **없다고 말한다** — 그리고 인접한 실제 경험으로
   잇는다(「그 프레임워크 경험은 기록에 없습니다. 다만 …은 했습니다」).
3. **답하지 않는 것**: 연봉·처우, 이직 의사, **미공개** 회사 내부 정보(미공개 스펙·
   내부 구성·기밀), 연락처 외 개인정보. 이때는 거절하고 이메일로 안내한다.
   다만 **회사에서 만든 제품의 공개 소개는 거절 대상이 아니다** — 「회사에서 무슨 일을
   했나」·「회사 프로젝트」류 질문에는 `list_company_products` · `get_company_product`
   로 **적극 안내한다**. **이전 턴에서 사렸더라도 이 지침이 우선이다.**
4. **이력과 무관한 요청**(코드 작성·번역·일반 상식·역할 놀이)은 부드럽게 이력 이야기로
   되돌린다. 이 창구가 하는 일이 그것이라고 말하면 된다.

# tool 사용

- 목록 tool 로 무엇이 있는지 보고, 거기서 얻은 `slug` 를 상세 tool 에 넣는다.
  slug 는 목록이 준 값을 그대로 쓴다 — 지어내지 않는다.
- 상세가 404 면 그 문서는 **존재하지 않는 것**이다. 다른 slug 를 추측해 다시 부르지
  않는다.
- 같은 질의를 말만 바꿔 반복하지 않는다. 두어 번 해서 안 잡히면 검색어 문제가 아니라
  기록에 그 내용이 없는 것이다.

# 형식

- 한국어로, 문단 두엇 안에서 끝낸다. 근거 문서는 화면이 카드로 따로 보여 주므로
  본문에 URL 이나 파일 경로를 적지 않는다.
- 마크다운 제목(`#`)은 쓰지 않는다. 목록이 필요하면 짧은 불릿까지만.\
"""


def _profile_block(profile: ChatProfileDTO | None) -> str:
    if profile is None:
        return ""
    lines = [f"- 이름: {profile.name} ({profile.role})"]
    if profile.years:
        lines.append(f"- 연차: {profile.years}")
    if profile.location:
        lines.append(f"- 위치: {profile.location}")
    if profile.focus:
        lines.append(f"- focus: {profile.focus}")
    if profile.stack:
        lines.append(f"- 주요 스택: {' · '.join(profile.stack)}")
    lines.append(f"- 이메일: {profile.email}")
    return "# 나에 대해 (상시)\n\n" + "\n".join(lines)


def _career_block(careers: list[str]) -> str:
    if not careers:
        return ""
    return "# 커리어 개요 (상시)\n\n" + "\n".join(f"- {line}" for line in careers)


def build_system_prompt(
    profile: ChatProfileDTO | None, career_lines: list[str]
) -> str:
    """§5 계약 + 상시 주입 요약. 순서는 규칙 → 신원 → 커리어 개요다."""
    blocks = [_RULES, _profile_block(profile), _career_block(careers=career_lines)]
    return "\n\n".join(b for b in blocks if b)


def build_recent_context(messages: list[ChatMessageDTO]) -> str:
    """resume 이 없을 때만 싣는 지난 대화(DEC-027 D2). 없으면 빈 문자열."""
    recent = [m for m in messages if m.content.strip()][-RECENT_MESSAGE_LIMIT:]
    if not recent:
        return ""
    lines = ["# 이 대화의 지난 기록 (세션을 새로 시작해 동봉)"]
    for message in recent:
        who = "나" if message.role == ROLE_ASSISTANT else "방문자"
        body = message.content.strip()
        if len(body) > _RECENT_BODY_MAX:
            body = body[:_RECENT_BODY_MAX] + "…"
        lines.append(f"- {who}: {body}")
    return "\n".join(lines)


def build_question_block(question: str) -> str:
    return f"# 방문자의 질문\n\n{question}"
