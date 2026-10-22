import * as THREE from 'three';

// 텍스처 두 장(직전·지금 광원) 페이드 + 오버레이 1장을 셰이더 하나로 합성(SPEC §6-3).
// 조명 없음 — 텍스처가 이미 촬영 사진이다.
const vertexShader = /* glsl */ `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const fragmentShader = /* glsl */ `
uniform sampler2D uBase;
uniform sampler2D uBasePrev;
uniform float uMix;
uniform sampler2D uOverlay;
uniform float uOverlayOn;
uniform vec3 uOverlayColor;
varying vec2 vUv;
void main() {
  vec3 base = mix(texture2D(uBasePrev, vUv).rgb, texture2D(uBase, vUv).rgb, uMix);
  float a = texture2D(uOverlay, vUv).a * uOverlayOn;
  gl_FragColor = vec4(mix(base, uOverlayColor, a), 1.0);
}
`;

export function createEmptyTexture(): THREE.Texture {
  const t = new THREE.DataTexture(new Uint8Array([0, 0, 0, 0]), 1, 1, THREE.RGBAFormat);
  t.needsUpdate = true;
  return t;
}

export function createFaceMaterial(base: THREE.Texture): THREE.ShaderMaterial {
  return new THREE.ShaderMaterial({
    uniforms: {
      uBase: { value: base },
      uBasePrev: { value: base },
      uMix: { value: 1 },
      uOverlay: { value: createEmptyTexture() },
      uOverlayOn: { value: 0 },
      uOverlayColor: { value: new THREE.Color('#ffffff') },
    },
    vertexShader,
    fragmentShader,
    side: THREE.DoubleSide,
  });
}

/** 사진 픽셀을 그대로 — 색공간 변환 없음, 밉맵 + 이방성. flipY 는 기본값(true) 그대로 둔다(OBJ vt.v = 1 − 이미지 v). */
export function prepareTexture(t: THREE.Texture, maxAnisotropy: number): THREE.Texture {
  t.colorSpace = THREE.NoColorSpace;
  t.minFilter = THREE.LinearMipmapLinearFilter;
  t.magFilter = THREE.LinearFilter;
  t.generateMipmaps = true;
  t.anisotropy = maxAnisotropy;
  t.needsUpdate = true;
  return t;
}
