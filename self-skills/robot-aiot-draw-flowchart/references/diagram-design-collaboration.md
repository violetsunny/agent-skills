# diagram-design 协作指引

## 运行时依赖

`diagram-design` 在运行时独立部署于 `~/.agents/skills/diagram-design`，本 SKILL 通过调用其能力获得编辑级设计系统支持。

## 何时调用

1. 需要 39 类视觉类型的专业布局规则时
2. 需要通用质量硬规则（删除优先哲学、复杂度预算、连接线六规则）的权威判定时
3. 需要形状词汇表和 Z-order 画家模型参考时
4. 需要 Taste Gate 清单做交付前审查时

## 协作边界

- 本 SKILL 负责 draw.io XML 路径（路径 A）和静态页面 HTML
- `diagram-design` 提供设计系统规则和视觉类型参考
- 配色以本 SKILL 的 `color-schemes.md` 为品牌基准，`diagram-design` 的风格皮肤作为补充选项
- 机器人/IoT 图标以本 SKILL 的 `robot-icons.md` 为准

## 冲突裁决

当 `diagram-design` 规则与本 SKILL 规则冲突时：
1. 用户明确要求 > 一切
2. 本 SKILL 的机器人视觉语言 > `diagram-design` 通用规则
3. `diagram-design` 的设计系统细则 > 本 SKILL 的通用默认值
4. 几何校验门永远活跃，任何一方都不能豁免
