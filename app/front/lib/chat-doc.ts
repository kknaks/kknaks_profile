"use client";

/**
 * 근거 카드 → 문서 패널의 재료 (KDEV-SPEC-017 §2 U-5, spec v0.0.12).
 *
 * ## 어떤 유형이 패널로 열리나
 *
 * `company_product` · `career` · `problem` **셋뿐이다.** 셋은 전용 공개 페이지가
 * 없어서 카드 url 이 셋 다 `/career` 한 곳을 가리킨다(BE `core/chat_slugs.py`
 * `_URL_BUILDERS`) — 눌러도 타임라인에 떨어뜨릴 뿐이라 패널로 그 자리에서 보여주는
 * 이득이 크다. `project` · `note` 는 `/projects/<slug>` · `/notes/<slug>` 전용
 * 페이지가 있어 **기존대로 이동한다**(owner 확정, spec v0.0.12 U-5 ②).
 *
 * ## 어디서 읽나
 *
 * 공개 번들 `GET /api/career` 한 벌이면 셋 다 나온다 — 제품 showcase 전문
 * (`career[].products[].body`), 역할 상세(`career[].body`), 문제 본문
 * (`career[].problems[].body`)이 모두 실려 온다. **chat-tool API 는 쓰지 않는다** —
 * 그쪽은 turn 토큰이 필요한 AI 전용이다.
 *
 * ## slug 매칭 — BE 규약의 거울
 *
 * `product` 는 `slug` 컬럼을 가져 그대로 맞춘다. `career` 와 `problem` 은 컬럼이
 * 없어 BE 가 합성 slug 를 준다(`chat_slugs.py`):
 *
 *     career   `<company.slug>-<career.id>`   예: `medisolve-ai-3`
 *     problem  `problem-<problem.id>`
 *
 * 공개 번들에는 `company.slug` 가 없다. 그래도 맞출 수 있는 이유는 BE 의
 * `parse_career_slug` 자체가 `rpartition("-")` 으로 **뒤 숫자만** 쓰기 때문이다 —
 * 앞자리는 모델이 눈으로 보라고 붙인 것이고 신원은 id 다. 그래서 여기서도 뒤
 * 숫자를 id 로 읽어 `career[]` 를 찾는다. 못 찾으면 `null` 이고, 호출부는 패널
 * 대신 기존 url 이동으로 접는다.
 */

import { api } from "@/lib/api";
import type { ChatSource, ChatSourceType } from "@/lib/chat";
import type { CareerItem, CareerResponse } from "@/lib/types";

/** 패널로 여는 유형(U-5 ①). 나머지는 링크 그대로 둔다. */
const PANEL_TYPES: ReadonlySet<ChatSourceType> = new Set<ChatSourceType>([
  "company_product",
  "career",
  "problem",
]);

export function opensInPanel(type: ChatSourceType): boolean {
  return PANEL_TYPES.has(type);
}

/**
 * 유형 태그의 표기 — 계약값(`source.type`)이 아니라 **보이는 라벨**이다.
 * 근거 카드와 패널 머리가 같은 말을 써야 해서 여기 한 자리에 둔다.
 *
 * 나머지 넷은 계약값 그대로가 짧고 읽히므로 손대지 않는다. `company_product` 만
 * 밑줄 있는 두 단어라 태그 한 칸에 길어 같은 관례(짧은 소문자 한 단어)로 줄인다.
 */
const TYPE_LABEL: Partial<Record<ChatSourceType, string>> = {
  company_product: "product",
};

export function sourceTypeLabel(type: ChatSourceType): string {
  return TYPE_LABEL[type] ?? type;
}

/** 패널이 그리는 한 건. `render` 가 본문 렌더러를 고른다. */
export interface ChatDoc {
  type: ChatSourceType;
  slug: string;
  title: string;
  /** 제목 아래 한 줄 — 어느 회사·역할의 것인지. */
  subtitle?: string | null;
  /** 공개 페이지 경로. 있으면 패널 하단에 「페이지에서 보기 →」. */
  url?: string | null;
  body?: string | null;
  /**
   * `md` = 원장 showcase(이미지·mermaid 있음) · `prose` = 컬럼에 든 짧은 글.
   * career · problem 은 detail_path 가 없어 후자다(erd.md §career).
   */
  render: "md" | "prose";
  /** `md` 일 때 이미지 상대참조의 기준 디렉토리. */
  assetBase?: string | null;
}

/**
 * 번들 캐시 — **프라미스를 담는다.** 카드를 연달아 누를 때 같은 요청이 여러 번
 * 나가지 않게 하려는 것이고, 값이 아니라 프라미스라 동시 클릭도 한 번으로 접힌다.
 * 대화 한 판 동안 이력이 바뀔 일은 없으므로 무효화는 두지 않았다.
 */
let careerBundle: Promise<CareerResponse> | null = null;

function loadCareer(): Promise<CareerResponse> {
  if (!careerBundle) {
    careerBundle = api.career().catch((e) => {
      careerBundle = null; // 실패는 캐시하지 않는다 — 다음 클릭에 다시 시도한다.
      throw e;
    });
  }
  return careerBundle;
}

/** `<company.slug>-<id>` → id. BE `parse_career_slug` 와 같은 규칙. */
function parseCareerSlug(slug: string): number | null {
  const tail = (slug ?? "").slice((slug ?? "").lastIndexOf("-") + 1);
  return /^\d+$/.test(tail) ? Number(tail) : null;
}

/** `problem-<id>` → id. BE `parse_problem_slug` 와 같은 규칙. */
function parseProblemSlug(slug: string): number | null {
  const PREFIX = "problem-";
  if (!(slug ?? "").startsWith(PREFIX)) return null;
  const tail = slug.slice(PREFIX.length);
  return /^\d+$/.test(tail) ? Number(tail) : null;
}

/**
 * 카드 하나를 패널이 그릴 수 있는 모양으로 푼다.
 *
 * 매칭에 실패하면 `null` — 호출부가 기존 url 이동으로 폴백한다. 「없는 것」과
 * 「못 찾은 것」을 여기서 가르지 않는다(BE 가 404 를 하나로 접는 것과 같은 이유).
 */
export async function resolveChatDoc(source: ChatSource): Promise<ChatDoc | null> {
  if (!opensInPanel(source.type)) return null;

  const bundle = await loadCareer();
  const careers: CareerItem[] = bundle["career[]"] ?? [];

  if (source.type === "company_product") {
    for (const c of careers) {
      const p = (c.products ?? []).find((x) => x.slug === source.slug);
      if (p) {
        return {
          type: source.type,
          slug: source.slug,
          title: p.title || source.title,
          subtitle: `${c.org} · ${c.title}`,
          url: source.url,
          body: p.body,
          render: "md",
          assetBase: `para/projects/company/${p.slug}/`,
        };
      }
    }
    return null;
  }

  if (source.type === "career") {
    const id = parseCareerSlug(source.slug);
    if (id == null) return null;
    const c = careers.find((x) => x.id === id);
    if (!c) return null;
    return {
      type: source.type,
      slug: source.slug,
      title: c.title || source.title,
      subtitle: `${c.org} · ${c.period}`,
      url: source.url,
      body: c.body,
      render: "prose",
    };
  }

  // problem — career 에 매달린 행이라 부모를 같이 찾아 맥락 줄을 만든다.
  const id = parseProblemSlug(source.slug);
  if (id == null) return null;
  for (const c of careers) {
    const pr = (c.problems ?? []).find((x) => x.id === id);
    if (pr) {
      return {
        type: source.type,
        slug: source.slug,
        title: pr.title || source.title,
        subtitle: pr.productTitle ? `${c.org} · ${pr.productTitle}` : c.org,
        url: source.url,
        body: pr.body,
        render: "prose",
      };
    }
  }
  return null;
}
