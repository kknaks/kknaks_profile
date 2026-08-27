"use client";

import { useEffect, useRef, useState } from "react";

/**
 * mermaid 코드블록을 SVG 로 그린다. mermaid 는 window·DOM 을 만지므로 렌더는
 * **브라우저에서만**(useEffect) 돌린다 — 모듈도 동적 import 라 SSR 번들에 안 낀다.
 */
let seq = 0;

export function Mermaid({ code }: { code: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [svg, setSvg] = useState<string>("");
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const mermaid = (await import("mermaid")).default;
        mermaid.initialize({
          startOnLoad: false,
          // 원본은 우리 showcase.md — 신뢰 입력이라 loose 로 <br/> 줄바꿈을 살린다.
          securityLevel: "loose",
          theme: "dark",
          fontFamily: "var(--font-mono)",
        });
        const id = `mmd-${Date.now()}-${seq++}`;
        const { svg } = await mermaid.render(id, code);
        if (alive) setSvg(svg);
      } catch {
        if (alive) setFailed(true);
      }
    })();
    return () => {
      alive = false;
    };
  }, [code]);

  // 그리기 전(또는 실패) 에는 원본을 코드블록으로 둔다.
  if (failed || !svg) {
    return (
      <pre>
        <code>{code}</code>
      </pre>
    );
  }

  return (
    <div
      ref={ref}
      className="mermaid-diagram"
      // eslint-disable-next-line react/no-danger
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}
