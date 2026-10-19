# 记忆索引

此文件是所有记忆的索引，每条记忆一行。每次会话开始时自动加载。

## PPT Harness（可演化系统）

**入口文档：** [ppt-harness-entry.md](ppt-harness-entry.md) — 从这里开始

**主观偏好已迁移至：** `~/.claude/ppt-harness/memory/subjective/`

- 审美偏好：`aesthetic.md` — 配色、图标风格、留白
- 结构偏好：`structure.md` — 大纲、页数分配、章节划分
- 表达偏好：`expression.md` — 标题措辞（32 磅、结论式、≤22 字）、术语
- 交互偏好：`interaction.md` — 动画、备注、隐藏页
- 优先级：`priority.md` — 冲突时的选择规则

**模板库：** `~/.claude/ppt-harness/templates/`
- business-blue: 商业汇报风格（深蓝、数据密集）
- academic-green: 医学学术风格（绿色、流程图）
- academic-minimal: 计算机学术极简风格（深蓝、留白多）

**当前工具：** `~/.claude/skills/paper-ppt/tools/`，以 `run_pipeline.py` 串联构建、结构检查和 PowerPoint 渲染；旧 harness 目录的代码仅供历史参考。

**演化规则：**
- 用户对宏观问题提要求时，Agent 主动提取偏好并写入对应的 subjective/ 文件
- 无需询问，先提取，用户纠正后再修正
- 偏好复用：下次生成 PPT 时自动应用已记录的偏好

**原记忆文件（已废弃，仅供参考）：**
- [字号要求](ppt-font-size-requirement.md)
- [标题风格](ppt-title-style.md)
- [原生格式](ppt-native-format.md)
- [视觉风格](ppt-visual-style.md)
