---
name: ppt-visual-style
description: 学术 PPT 插图风格：浅色圆底图标、胶囊标签、圆角卡片、弧形虚线箭头
metadata:
  type: reference
---

学术 PPT 的插图风格参考了第 3 页的设计：浅色圆底图标、胶囊标签、圆角卡片、弧形虚线箭头，整体简洁、信息密度高。

**具体元素：**

1. **图标：** 浅色圆底 + 蓝色图标
   - 用 `cv.icon_c(name, cx, cy, size)` 居中放置
   - deckkit 不再内置图标：每套 PPT 按论文内容新画 SVG（`cv.svg(markup, x, y, w)`），风格跟随本次参考

2. **胶囊标签（pill）：** 圆角 999px 的文字容器
   - 用 `cv.pill(text, cx, cy, pt=16, fill=C['blue'], color='white')`
   - 适合标注类别、状态、模块名

3. **圆角卡片：** 白色或浅灰底、细灰边框
   - 用 `cv.card(x, y, w, h, fill=C['white'], line=C['line'])`
   - 适合包裹文字、表格、插图

4. **箭头：** 蓝色、可选虚线、弧形
   - 直线箭头：`cv.arrow(x1, y1, x2, y2, color=C['blue'], dash=False)`
   - 弧形箭头：`cv.arrow(x1, y1, x2, y2, ctrl=(cx, cy), dash=True, color=C['blue'])`

5. **配色：**
   - 深蓝标题（`C['navy']` #1E3A5F）
   - 蓝色强调（`C['blue']` #2563EB）
   - 金色亮点（`C['gold']` #F59E0B）
   - 浅灰背景（`C['pale']` #F3F4F6）

**Why：** 这种风格在第 3 页"方法：从弱种子创建外壳"中被用户认可，视觉清晰、层次分明，适合展示技术流程和系统架构。

**How to apply：**
- 在封面、方法、结论等需要插图的页面使用这些元素组合
- 避免装饰性图标，只画传达信息的图（流程、结构、对比）
- 颜色不要超过 4 种（深蓝、蓝、金、灰）

参考页面：HarnessDev PPT 第 3 页（s_method_overview）
相关记忆：[[ppt-native-format]]
