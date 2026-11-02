// src/data/face-anchors.ts — 찍기 도구(/screen?anchors=edit) 산출물. 이 고객 메시 기준 고정값.
// uv = 그 자리의 텍스처 좌표(__faceViewer.anchorUv, 2루프) — 부위 확대 사진이 쓴다
export const FACE_ANCHORS = {
  meshBytes: 21369718, // public/m3d/manifest.json mesh.bytes — 다른 메시면 점을 안 그린다
  points: [
    { key: 'forehead', p: [0.0014, 0.0356, 0.0600], n: [0.0463, -0.2060, 0.9775], uv: [0.5215, 0.6581] },
    { key: 'eye', p: [-0.0314, 0.0022, 0.0490], n: [-0.1781, -0.1456, 0.9732], uv: [0.4475, 0.5236] },
    { key: 'nasolabial', p: [-0.0188, -0.0375, 0.0571], n: [-0.4032, 0.2079, 0.8912], uv: [0.4766, 0.3485] },
    { key: 'sebum', p: [0.0299, 0.0673, 0.0419], n: [0.3873, 0.4200, 0.8207], uv: [0.5836, 0.8008] },
    { key: 'cheek', p: [0.0442, -0.0124, 0.0492], n: [0.3205, 0.2420, 0.9158], uv: [0.6146, 0.4619] },
    { key: 'poreTexture', p: [0.0433, -0.0543, 0.0466], n: [0.3813, -0.2096, 0.9004], uv: [0.6166, 0.2859] },
  ] as { key: string; p: [number, number, number]; n: [number, number, number]; uv?: [number, number] }[],
} as const;
