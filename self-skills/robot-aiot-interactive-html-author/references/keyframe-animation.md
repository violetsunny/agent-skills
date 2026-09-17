# 关键帧动画与动效接缝规则

## 定位

为 Web 演示提供专业级动画编排能力，确保动效流畅、有节奏、不干扰内容阅读。

## 关键帧动画系统

### 核心概念

- **Keyframe**：定义动画起止状态和中间节点
- **Seam**：多个动画元素之间的时序衔接点
- **Orchestration**：全局动画编排，控制节奏和层次

### 接缝门控（Seam Gate）

动画元素之间的衔接必须通过接缝检查：

1. **时序对齐**：前一个元素的结束帧与后一个元素的起始帧时间差 ≤ 50ms
2. **属性连续**：衔接点的 transform/opacity 值不得跳变
3. **缓动一致**：同一组关联动画使用相同缓动函数
4. **层级正确**：z-index 在过渡期间不发生闪烁

### 缓动函数选择

| 场景 | 推荐缓动 | CSS值 |
|------|---------|-------|
| 入场 | ease-out | `cubic-bezier(0, 0, 0.2, 1)` |
| 退场 | ease-in | `cubic-bezier(0.4, 0, 1, 1)` |
| 强调 | ease-in-out | `cubic-bezier(0.4, 0, 0.2, 1)` |
| 弹性 | spring-like | `cubic-bezier(0.34, 1.56, 0.64, 1)` |
| 数据变化 | linear | `linear` |

## 动效分层与时长预算

### 动效分层

1. **结构性动效**：页面切换、布局变化（必须有）
2. **反馈性动效**：hover/click 响应（可选）
3. **装饰性动效**：纯视觉增强（谨慎使用）

### 时长预算

| 类型 | 时长范围 | 说明 |
|------|---------|------|
| 微交互 | 100-200ms | hover/focus/press |
| 元素入场 | 300-500ms | 单个元素淡入/滑入 |
| 页面过渡 | 400-600ms | 整页切换 |
| 数据动效 | 800-1500ms | 数字滚动/图表绘制 |
| 编排序列 | ≤ 2000ms | 一组元素依次入场总时长 |

### prefers-reduced-motion

检测到 `prefers-reduced-motion: reduce` 时：
- 所有过渡降级为即时切换（duration: 0）
- 保留状态变化，移除运动
- 数据动效直接显示最终值

## View Transition API

优先使用 View Transition API 实现页面过渡：

```javascript
if (document.startViewTransition) {
  document.startViewTransition(() => {
    updateDOM();
  });
} else {
  // 降级 CSS transition
  element.classList.add('transition-fallback');
  updateDOM();
}
```

## 性能红线

- 动画仅限 transform / opacity / filter
- 避免触发 layout/paint 的属性（width/height/top/left/margin/padding）
- will-change 仅在动画开始前添加，结束后移除
- 同时运动的元素 ≤ 10 个
