---
name: ppt-native-format
description: PPT 制作流程：原生格式 + 必须有插图
metadata:
  type: project
---

使用 `paper-ppt` 技能（`/paper-ppt`），按其 WORKFLOW.md 执行。deckkit 的准确接口以 `python ~/.claude/skills/paper-ppt/tools/deckkit_api.py` 的输出为准，不要凭记忆写函数名（没有 chart_line、arc_arrow、Deck 类）。

**插图和图标是必须保留的做法，具体风格跟随本次参考。** 先建立 icons.py 图标库（本领域专用图标，不是 HarnessDev 的机器人/锁），再在每页用 cv.svg() 和 cv.icon_c() 绘制插图。文字一律原生，不写进 SVG。

**Why:** HarnessDev 成品正文页平均 4.6 个 SVG 元素，RSI 只有 0.5 个，后者被判定为欠加工。页面没有任何插图、图表、表格、图片时，说明构图偷工了。

**How to apply:** 每页计划必须包含 visual 字段，写明画什么、哪些 SVG、哪些原生形状；design_brief.md 必须记录参考的图标风格（线性/扁平/彩色，线宽，有无底托）；icons.py 渲染后与参考对比校准。

相关记忆：[[ppt-font-size-requirement]], [[ppt-title-style]]
