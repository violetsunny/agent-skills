<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: zh-CN
- audience: 技术Leader
- objective: 对比OTA1与OTA2两套升级系统的核心差异，使技术Leader快速掌握关键区别和规则
- core_message: OTA1按SN8升级且作为入口转发OTA2；OTA2按release发版记录升级且支持定推

## mode
- mode: briefing

## visual_style
- visual_style: swiss-minimal

## colors
- background: #FFFFFF
- secondary_bg: #F5F7FA
- primary: #1A5F7A
- accent: #E8723C
- secondary_accent: #2D6A4F
- body_text: #2D3436

## typography
- font_family: Microsoft YaHei, Arial, sans-serif
- title_family: Microsoft YaHei, Arial, sans-serif
- body_family: Microsoft YaHei, Arial, sans-serif
- body: 24
- title: 42
- subtitle: 32
- annotation: 18

## icons
- library: tabler-outline
- stroke_width: 2
- inventory: tabler-outline/arrow-right, tabler-outline/database, tabler-outline/check, tabler-outline/x, tabler-outline/download, tabler-outline/refresh, tabler-outline/alert-triangle, tabler-outline/file-check

## page_rhythm
- P01: anchor
- P02: anchor

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
