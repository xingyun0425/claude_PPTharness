# PPT Harness 入口

当前 Claude 入口：C:/Users/16947/.claude/skills/paper-ppt/SKILL.md。
执行流程：C:/Users/16947/.claude/skills/paper-ppt/WORKFLOW.md。

每次制作论文 PPT：读取论文并记录来源，分析用户此次提供的参考，制定逐页设计计划，用原生 PowerPoint 元素生成，逐页渲染检查并修复。harnessdev-deck-native.pptx 是质量与可编辑性的实例，不是固定配色、图标或布局模板。

~/.claude/ppt-harness/README-page-level.md 和页面类型库仅供检索参考，不能自动决定每页版式。旧 generate_paper_ppt.py 和 harness.py 已停用，因为它们忽略参考并生成占位内容。

当前用户偏好：参考的使用方法和原生生成流程应可迁移到不同参考；不要照搬 HarnessDev 的视觉设计。详细偏好见 ~/.claude/ppt-harness/memory/subjective/，应用时服从此次提供的参考和具体需求。
