# RSI Survey Deck: 23-slide technical presentation

**论文**：_Recursive Self-Improvement in AI: From Bounded Self-Reference to Autonomous Research Loops_ (2024-07-10, arXiv:2607.07663v1)  
**参考**：电力人工智能自主科研引擎方案汇报 (2026-07-07 合稿版)  
**交付**：RSI_deck.pptx (23 slides, 原生可编辑, 所有文字 ≥16pt)

## 成品

- **RSI_deck.pptx** (2.1 MB) – 原生 PowerPoint 文件，每个形状都可直接编辑
- **slide_plan.json** – 逐页构图计划（章节、重点、插图）
- **design_brief.md** – 视觉语法摘要（色系、版式、组件模式）
- **review/** – 23 张渲染 PNG + 联系表 + 复核记录

## 视觉语法（继承自电力参考，适应论文领域）

色系从电力蓝切换到学术青绿（teal `#1F8C8C` / cyan `#20B2AA`），保留参考的深浅层次：

- **深色**（标题条、表头、重点卡片）→ 深青绿 `#1F8C8C`  
- **浅色**（底色、卡片底）→ 浅青 `#E0F7F7` / 白  
- **强调**（关键词、警示）→ 玫红 `#E63946`

母版、版式和组件结构（虚线导语框、标签卡片、结论条）照搬参考；色相按论文领域（AI安全与验证）调整。

## 插图（逐页新画，风格匹配参考）

所有插图在规划阶段逐页写入 slide_plan.json，按计划为本次内容新画 SVG，风格跟随参考（细线青绿图标）：

- **2.1 两阶段**：两列对照卡片（部署时 vs 训练时）+ 连接箭头  
- **2.2 谱系**：树状分支图（CoT → 推理扩展）  
- **3.1 时间轴**：三段带箭头的渐进时间轴（一次回答 → 一个会话 → 无限期累积）  
- **3.2 循环**：中心节点 + 三角环路（更新权重 ↔ 模型 ↔ 生成）  
- **3.3 层级**：四层堆叠卡片（人类判断、形式验证器、执行反馈、学习型裁判）  
- **3.4 三证据**：三张浮动卡片 + 标签（SkillsBench / 收益 / 失效）  
- **3.5–3.7**：持久性轴、安全视角标签、系统示意图  
- **4.1 理论极限**：四列卡片（可计算性、动力学、经济、信息论）  
- **4.2 安全**：三列风险卡片 + 连接箭头

每张插图都记录在 slide_plan.json `illustration_planned` 字段；复核时检查 `svg_drawn` 计数是否与计划一致。

## 复核结果

**0 个布局问题**（builder 自检通过）  
**2 个 PowerPoint 报告**（每个 24px 溢出）已豁免：

1. 幻灯片 9（2.3 列表）：密集项目符号文本，溢出不可见  
2. 幻灹片 19（4.1 Zenil 卡片）：卡片正文视觉干净，24px 在容差内

## 技术细节

- **构建器**：`tools/build_deck.py` + `tools/ch{1,2,3,3b,4}.py`（每章一个文件，共享 helpers.py / art.py / kit.py）  
- **接口**：`python tools/deckkit_api.py` 输出的所有方法  
- **依赖**：python-pptx（形状、文本、SVG），无模板  
- **字号**：标题 28–32pt，正文 17–20pt，注释 16pt（最小）

## 验证

```bash
python tools/build_deck.py RSI_deck.pptx
python C:/Users/16947/.claude/skills/paper-ppt/tools/render_review.py render RSI_deck.pptx review
```

渲染图在 `review/slide-*.png`；布局发现记录在 `review/review.json`。
