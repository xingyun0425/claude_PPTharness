# Paper PPT harness 改造说明

本次修改的是 C:/Users/16947/.claude/skills/paper-ppt/ 中实际的 Claude skill 和工具。用户认可的 HarnessDev 成品作为质量案例，具体设计跟随每次提供的参考。

## 为什么原流程跑偏

实查旧 harness 的论文解析器返回占位内容，页面构建器只做封面，reference 参数被忽略，PowerPoint 渲染还是 TODO。原 paper-ppt 模板调用 IconStore() 和 register()，与实际需要 IconStore(prs, tmp) 的接口不符，还调用不存在的 get_layout_problems()，且只在循环结束后检查最后一页。模板还含低于 16 pt 的示例文字。日志中的失败后切换到通用生成路径，使参考分析和逐页修复更难落实。

旧诊断中“JavaScript 导致丑”“skill 一定高于自定义代码”的解释缺乏证据。Python 与 JavaScript 都能生成原生 PPT；效果取决于参考理解、构图、内容密度、组件能力和渲染后的迭代。

## 已落实的改造

- SKILL.md 与 WORKFLOW.md：记录论文证据，先看参考的渲染图，写 design_brief.md 与逐页计划，校准 2–3 张代表页，再生成整套。每页说明参考借鉴与适配原因。
- build_deck_template.py：修复实际接口；每页独立函数；逐页检查重叠，问题阻止保存；要求演讲者备注和明确主题。
- deckkit.py：常用组件在运行时读取主题；重建内置 SVG；支持自定义 SVG；字体测量跟随配置字体；文字和图表保留 16 pt 下限。历史颜色键名为兼容接口保留，不强制使用蓝色。
- inspect_reference.py：读取分组内元素、表格、图表与主题 XML，输出参考结构证据。显式统计不能替代视觉分析，旋转和继承样式仍需查看渲染。
- validate_deck.py：检查逐页计划、原生文字、备注、整页图片；递归检查分组；独立读取 PPTX XML 检查表格和图表等显式字号。
- render_review.py：本机 PowerPoint 逐页导出；记录 PPTX 和图片哈希；复核记录默认未完成；要求逐页具体评估；拒绝过期或不完整记录。
- run_pipeline.py：统一 build 与 deliver；记录 PPTX、参考、构建脚本和计划的哈希。未通过检查不会产生新的成功交付记录。
- 工作区 CLAUDE.md 和记忆入口：指向真实 skill；历史审美记忆增加用户此次修正，旧配色和卡片不是全局偏好。
- 旧 harness.py 和 generate_paper_ppt.py 改为明确迁移提示，原文件保存在 ~/.claude/ppt-harness/legacy-entry-backup/。

## 实际验证

1. 新模板最小构建成功；检查生成后的原生标题，确认新主题色确实写入 PPTX。
2. 读取 HarnessDev 17 页参考，成功输出包含分组和主题证据的分析。
3. 两页合成测试包含分组内原生文字、自定义 SVG 与 PNG 后备图、原生表格和折线图；完整 build 命令成功，并通过本机 PowerPoint 导出。两页 PNG 已实际查看并记录具体评估。
4. 回归测试确认：分组内小字、整页截图、缺少计划、未复核页面、过期 PPTX 渲染会失败；合格分组文字可通过。
5. deliver 成功生成 harness-validation/review/delivery.json；改变计划后交付被拒绝，恢复计划后重新通过。

测试 PPT：harness-validation/native-components.pptx。它使用合成内容，仅验证技术流程，不能作为论文成品或审美基准。

## 下次怎么用

在新的 Claude 会话中明确调用 /paper-ppt，提供论文和本次参考 PPT，并说明页数与汇报对象。当前工作区还会通过 CLAUDE.md 指向该流程。skill 文件已修改，但未在另一个实际 Claude 会话里验证其加载行为；如果旧会话缓存了技能说明，使用新会话。

推荐提示：使用 /paper-ppt，将这篇论文制作成原生可编辑 PPT。分析此次参考的视觉层级、构图和图表处理，先校准代表页，再生成整套。按 paper-ppt 的 run_pipeline.py 完成 build、逐页 PowerPoint 渲染修复和 deliver 验收。HarnessDev 仅作质量标准，设计按本次参考与内容重新组织。

执行命令与逐页计划格式见 ~/.claude/skills/paper-ppt/WORKFLOW.md。默认由 Agent 完成生成和复核，不要求用户逐页设置标志。

## 能力边界

本次验证的是原生组件、主题配置、渲染和验收闭环，没有重做 RSI 全套，也没有完成多论文、多参考的审美评测。准确的论文阅读、设计决策和 PNG 视觉复核仍由 Agent 判断；脚本无法证明填写复核记录的人实际看过图片，也不能自动判断漂亮或核实所有事实。字号 XML 审计检查显式设置，继承字号和实际文字裁切仍需渲染检查。

支持本地 PowerPoint 与 Chrome 的当前 Windows 环境。SVG 的后备图用浏览器渲染，但幻灯片不经过 HTML 转换。PowerPoint 直接编辑后重新运行构建脚本会覆盖手工改动，建议另存或把修改同步回脚本。

## 第二轮检查与改进（Claude，2026-10-19）

实测发现的问题与修改：

- 渲染依赖的 pywin32 在本机 Python 3.14 未安装，render 实际无法运行。改为 tools/ppt_render.ps1 通过 PowerShell 调用 PowerPoint COM，不再需要 pywin32。
- 新增 PowerPoint 实测排版审计：读取 PowerPoint 自己测量的文字范围，检查文字裁切、重叠、出界。HarnessDev 成品 0 条，RSI 成品 23 条（封面标题裁切、第 7 页标题出界、第 8/11/12/13 页重叠等），与肉眼观察一致。
- 构建脚本发现排版问题时不再拒绝保存，草稿照常渲染；问题写入 review.json 的 auto_issues，交付前必须修复或逐条写明豁免理由。这样保留"渲染→看图→修复"的迭代循环。
- 新增 reference 阶段：渲染参考（pptx / pdf / 图片 / 图片文件夹），生成联系表、画面密度和母版装饰区坐标；build 前必须完成。deliver 要求 design_brief.md。
- 支持 BASE：直接继承参考 PPT 的母版（logo、页眉线、背景、页码），默认选参考正文页最常用的版式。
- deckkit：删除 HarnessDev 专用常量；内置图标的写死颜色全部改为主题色；新增 cv.svg() 用于每页自绘插图；Chrome 缺失时用 Edge；新增 deckkit_api.py 输出准确接口。
- WORKFLOW.md 写入 HarnessDev 做得好的可迁移原因，以及 RSI 失败的具体原因。

验证：regression_checks 12 项、smoke_test 通过；harness-validation/v2 以电力 PPT 为参考和母版完成 reference → build → PowerPoint 渲染 → deliver 全流程，并确认缺少 brief、未复核时交付被拒绝，人为制造的文字重叠被两层检查同时捕获。
