---
name: ppt-native-format
description: 学术 PPT 必须输出可编辑的原生 pptx，不要整页截图或 Canvas
metadata:
  type: project
---

为学术论文制作 PPT 时，输出格式必须是原生可编辑的 .pptx，所有元素（文字、表格、图表）都是 PowerPoint 原生对象。

**不要使用：**
- Canvas 绘制整页 PNG/JPG 后插入 PowerPoint
- SVG 整页导出后转 PNG
- HTML 页面截图
- PDF 转 PowerPoint

**必须使用：**
- python-pptx 或 PptxGenJS 生成原生元素
- 文字是文本框对象，可以直接编辑
- 表格是 PowerPoint 原生表格，可以右键"编辑数据"
- 图表是原生图表（内嵌 Excel 数据），可以右键"编辑数据"修改数值

**Why：** 
1. 用户需要在汇报前调整内容（改错别字、更新数据）
2. Canvas 渲染的字号只是估算，实际投影后可能太小或太大
3. 截图的表格和图表无法编辑，数据有误时要重做整个文件

**How to apply：**
使用 `paper-ppt` 技能（`/paper-ppt`），按其 WORKFLOW.md 执行。deckkit 的准确接口以 `python ~/.claude/skills/paper-ppt/tools/deckkit_api.py` 的输出为准，不要凭记忆写函数名（没有 chart_line、arc_arrow、Deck 类）。

相关记忆：[[ppt-font-size-requirement]], [[ppt-title-style]]
