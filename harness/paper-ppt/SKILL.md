---
name: paper-ppt
description: 将学术论文制作成参考驱动、原生可编辑且逐页渲染验证的 PowerPoint（Python + python-pptx + SVG 插图）
tags: [presentation, academic, pptx]
---

# Paper PPT

收到论文和制作 PPT 请求时，先完整阅读同目录的 [WORKFLOW.md](WORKFLOW.md)，按顺序执行。

- 论文提供事实，参考提供视觉语法，每页构图由 agent 根据内容关系设计。HarnessDev 只代表制作质量与可编辑性，不是固定模板；不同参考应得到明显不同的成品。
- 执行入口是 `tools/run_pipeline.py` 的 `reference`、`build`、`deliver` 三个阶段。先看参考的渲染图并写 design_brief.md，校准 2–3 张代表页，再做整套；每次 build 后查看联系表和逐页 PNG，修复后重建，直到复核干净。
- 接口以 `python tools/deckkit_api.py` 的输出为准，不要猜函数名。工具报错就修复后重跑，不要换用 PptxGenJS 或其他生成器。
- 不交付占位内容、整页图片或 HTML 转换结果；所有文字不小于 16 磅。

交付物：PPTX、slide_plan.json、design_brief.md、build_deck.py，以及 review/ 中的渲染图、复核记录和 delivery.json。
