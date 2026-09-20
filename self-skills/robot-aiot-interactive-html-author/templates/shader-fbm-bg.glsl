// ============================================================================
// shader-fbm-bg.glsl — WebGL FBM 噪声流场背景（余弦调色板 + 暗角）fragment shader
//
// 来源：references/animation-fx-catalog.md §3 shader-fbm-bg 骨架（逐字提取）
// 用途：高级感封面、章节页的全屏 quad 背景（原生 WebGL 零依赖，
//       全屏 quad + 单 fragment shader）
// 接线：顶点 shader 提供 v_uv（全屏 quad 的 0-1 纹理坐标）；uniform u_time
//       由 rAF 线性推进并遵守画布生命周期契约（离页即停）；u_res 为画布
//       像素尺寸。调色板相位偏移量（vec3(0.0,0.33,0.67) 的加数）换成从语义
//       token 主色推导的值以贴合品牌色。
// 降级：getContext('webgl') 失败 → 降级 gradient-blob 或 CSS 多层
//       radial-gradient 静态背景；reduced-motion 直接静帧。
// 预算：持续/氛围型特效，计入"全套 ≤3 页"预算（animation-fx-catalog.md §1）。
// ============================================================================

precision mediump float;
varying vec2 v_uv; uniform float u_time; uniform vec2 u_res;
float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p){
  vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1,0)), f.x),
             mix(hash(i + vec2(0,1)), hash(i + vec2(1,1)), f.x), f.y);
}
float fbm(vec2 p){
  float v = 0.0, a = 0.5; mat2 R = mat2(0.8, 0.6, -0.6, 0.8);
  for (int i = 0; i < 5; i++){ v += a * noise(p); p = R * p * 2.02; a *= 0.5; }
  return v;
}
vec3 palette(float t){ return vec3(0.5) + vec3(0.5) * cos(6.28318 * (t + vec3(0.0, 0.33, 0.67))); }
void main(){
  vec2 uv = v_uv; uv.x *= u_res.x / u_res.y;
  float t = u_time * 0.4;
  vec2 q = vec2(fbm(uv*3.0 + t*0.3), fbm(uv*3.0 + vec2(5.2,1.3) + t*0.2));
  vec2 r = vec2(fbm(uv*3.0 + q*4.0 + vec2(1.7,9.2) + t*0.15), fbm(uv*3.0 + q*4.0 + vec2(8.3,2.8) + t*0.1));
  float n = fbm(uv*3.0 + r*2.0);
  vec3 col = palette(n*2.0 + t*0.2);
  col = mix(col, palette(length(q)*3.0 + t*0.1), 0.4);
  col *= 0.7 + 0.3*n;
  gl_FragColor = vec4(col * (1.0 - 0.4*length(v_uv - 0.5)), 1.0);
}
