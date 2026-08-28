"use client";

import ReactMarkdown, { defaultUrlTransform } from "react-markdown";
import remarkGfm from "remark-gfm";
import { assetUrl } from "@/lib/api";
import { Mermaid } from "@/components/markdown/mermaid";

/**
 * 원장 md 전문 렌더러 — remark-gfm · mermaid · 이미지 상대참조 재작성.
 *
 * career-view 의 `ShowcaseBody` 를 그대로 끌어올렸다. **복사가 아니라 이동**이다 —
 * career 의 showcase 모달과 `/chat` 문서 패널이 같은 것을 그려야 하기 때문이다.
 *
 * 달라진 것은 자산 기준 경로를 인자로 받는다는 점뿐이다. 이미지 상대참조
 * (`./assets/…`)의 기준은 **그 md 원장이 앉은 디렉토리**라 유형마다 다르다 —
 * 회사 제품 `para/projects/company/<slug>/`, 개인 프로젝트
 * `para/projects/summer-star/<slug>/`, 글 `para/resources/note/<folder>/`.
 * `assetBase` 가 없으면 재작성하지 않는다(기준을 모르면 건드리지 않는 게 낫다).
 */
export function DocBody({
  body,
  assetBase,
  emptyLabel = "상세 — 준비 중",
}: {
  body?: string | null;
  /** 끝에 `/` 를 포함한 para 상대 디렉토리. 없으면 상대참조를 그대로 둔다. */
  assetBase?: string | null;
  emptyLabel?: string;
}) {
  const hasBody = !!body && body.trim().length > 0;

  if (!hasBody) {
    return (
      <div className="mono" style={{ fontSize: 13, color: "var(--fg-3)" }}>
        // {emptyLabel}
      </div>
    );
  }

  return (
    <article className="contents-body">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        urlTransform={(url, key) =>
          key === "src" && assetBase && !/^(https?:|data:|\/)/.test(url)
            ? assetUrl(`${assetBase}${url.replace(/^\.\//, "")}`)
            : defaultUrlTransform(url)
        }
        components={{
          // ```mermaid 블록은 SVG 다이어그램으로. 그 외 코드블록은 그대로 pre.
          pre: ({ node, children, ...rest }) => {
            const child = Array.isArray(children) ? children[0] : children;
            const cls =
              (child as { props?: { className?: string } })?.props?.className ?? "";
            if (/language-mermaid/.test(cls)) {
              const raw = (child as { props?: { children?: unknown } })?.props
                ?.children;
              return <Mermaid code={String(raw).replace(/\n$/, "")} />;
            }
            return <pre {...rest}>{children}</pre>;
          },
        }}
      >
        {body ?? ""}
      </ReactMarkdown>
    </article>
  );
}
