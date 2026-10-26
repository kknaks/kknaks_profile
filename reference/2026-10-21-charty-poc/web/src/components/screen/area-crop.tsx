'use client';

import { ScanFace } from 'lucide-react';
import type { CSSProperties } from 'react';

/** 부위 확대 사진의 원천 — 지금 필터의 3D 텍스처(+오버레이)와 그 카드 앵커의 UV */
export interface CropSource {
  tex: { url: string; w: number; h: number };
  overlay: { url: string; color: string } | null;
  uv: [number, number];
  /** 잘라 올 틀(텍스처 px) — 반경 r · 앵커에서 중심 이동 dx/dy(+는 이미지 오른쪽/아래) */
  frame: CropFrame;
}

export interface CropFrame {
  r: number;
  dx: number;
  dy: number;
}

/**
 * 부위별 틀(3루프 V-3) — 반경 120 은 피부결만 보여 어느 부위인지 몰랐다. 윤곽(눈썹·눈·코·입)이 들어오게 넓히고 중심을 옮긴다.
 * 텍스처 3242×1621 기준. 값은 scratch 미리보기로 정했다(파일로 남기지 않음).
 */
export const CROP_FRAMES: Record<string, CropFrame> = {
  forehead: { r: 260, dx: 0, dy: -90 }, // 미간 위로 올려 이마 + 양 눈썹 사이
  eye: { r: 230, dx: -20, dy: -70 }, // 눈밑에서 위로 — 눈 · 눈썹이 같이
  nasolabial: { r: 250, dx: 20, dy: 0 }, // 콧방울 옆 ~ 입가
  sebum: { r: 280, dx: 0, dy: 40 }, // 이마 오른쪽 T존 — 머리선 ~ 눈썹 끝
  cheek: { r: 260, dx: -30, dy: 0 }, // 콧방울 옆 볼 — 코 · 눈 아래가 같이
  poreTexture: { r: 250, dx: -30, dy: -10 }, // 입꼬리 옆 볼 — 입가 · 콧방울이 같이
};

/**
 * 부위 확대 사진(U-4) — 텍스처 jpg 를 CSS background 로 잘라 보인다. 잘라낸 이미지를 파일로 만들지 않는다.
 * three 텍스처는 flipY 기본이라 이미지 px = (u·W, (1−v)·H). 오버레이는 알파 마스크라 필터 색을 mask 로 칠한다(셰이더와 같은 합성).
 */
export function AreaCrop({ testId, src, size }: { testId: string; src: CropSource | null; size: number }) {
  if (!src) {
    return (
      <div className="flex shrink-0 items-center justify-center rounded-lg bg-ms-gray-200 text-ms-gray-500" style={{ width: size, height: size }} data-testid={testId} data-bg="">
        <ScanFace className="h-6 w-6" />
      </div>
    );
  }
  const { r, dx, dy } = src.frame;
  const k = size / (2 * r);
  const x = (src.uv[0] * src.tex.w + dx) * k - size / 2;
  const y = ((1 - src.uv[1]) * src.tex.h + dy) * k - size / 2;
  const box: CSSProperties = { backgroundSize: `${src.tex.w * k}px ${src.tex.h * k}px`, backgroundPosition: `${-x}px ${-y}px` };
  const mask: CSSProperties | null = src.overlay
    ? {
        backgroundColor: src.overlay.color,
        maskImage: `url(${src.overlay.url})`,
        WebkitMaskImage: `url(${src.overlay.url})`,
        maskSize: box.backgroundSize,
        WebkitMaskSize: box.backgroundSize as string,
        maskPosition: box.backgroundPosition,
        WebkitMaskPosition: box.backgroundPosition as string,
        maskRepeat: 'no-repeat',
        WebkitMaskRepeat: 'no-repeat',
      }
    : null;
  return (
    <div
      className="relative shrink-0 overflow-hidden rounded-lg bg-no-repeat"
      style={{ width: size, height: size, backgroundImage: `url(${src.tex.url})`, ...box }}
      data-testid={testId}
      data-bg={src.tex.url}
      data-overlay={src.overlay?.url ?? ''}
      data-radius={r}
    >
      {mask && <div className="absolute inset-0" style={mask} />}
    </div>
  );
}
