#!/usr/bin/env node
// AI递归自我改进论文汇报PPT
// 基于论文: Recursive Self-Improvement in AI (arXiv:2607.07663v1)

const pptxgen = require('pptxgenjs');
const pres = new pptxgen();

// 设置幻灯片尺寸
pres.layout = 'LAYOUT_16x9';

// 定义配色方案 - 参考电力AI PPT的深蓝主题
const COLORS = {
  navy: '1E3A8A',      // 深蓝色 - 标题
  blue: '3B82F6',      // 蓝色 - 强调
  lightBlue: 'DBEAFE', // 浅蓝 - 背景
  gold: 'F59E0B',      // 金色 - 高亮
  text: '1F2937',      // 深灰 - 正文
  grey: '6B7280',      // 中灰 - 辅助
  lightGrey: 'F3F4F6', // 浅灰 - 卡片背景
  white: 'FFFFFF'
};

// 通用样式
const titleStyle = {
  fontSize: 32,
  bold: true,
  color: COLORS.navy,
  fontFace: 'Microsoft YaHei'
};

const bodyStyle = {
  fontSize: 18,
  color: COLORS.text,
  fontFace: 'Microsoft YaHei'
};

const smallStyle = {
  fontSize: 16,
  color: COLORS.grey,
  fontFace: 'Microsoft YaHei'
};

// 第1页：封面
function slide01_cover() {
  const slide = pres.addSlide();

  // 背景渐变
  slide.background = { fill: COLORS.lightBlue };

  // 主标题
  slide.addText('AI递归自我改进', {
    x: 1.0, y: 1.8, w: 8.0, h: 1.0,
    fontSize: 44, bold: true, color: COLORS.navy,
    fontFace: 'Microsoft YaHei', align: 'center'
  });

  // 副标题
  slide.addText('从有界自我精炼到自主研究循环', {
    x: 1.0, y: 2.9, w: 8.0, h: 0.6,
    fontSize: 28, color: COLORS.blue,
    fontFace: 'Microsoft YaHei', align: 'center'
  });

  // 论文信息
  slide.addText('arXiv:2607.07663v1 [cs.AI] • July 2026', {
    x: 1.0, y: 3.8, w: 8.0, h: 0.4,
    fontSize: 18, color: COLORS.grey,
    fontFace: 'Microsoft YaHei', align: 'center'
  });

  // 作者
  slide.addText('Mingguang Chen (UCR) • Licheng Wang (AlphaAvatar) • Bo Qu (IIT)', {
    x: 1.0, y: 4.4, w: 8.0, h: 0.4,
    fontSize: 16, color: COLORS.text,
    fontFace: 'Microsoft YaHei', align: 'center'
  });

  // 装饰图形
  slide.addShape(pres.ShapeType.roundRect, {
    x: 3.5, y: 1.0, w: 3.0, h: 0.15,
    fill: { color: COLORS.gold }
  });
}

// 第2页：研究背景
function slide02_background() {
  const slide = pres.addSlide();

  slide.addText('研究背景：AI自我改进的爆发式增长', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  const bullets = [
    { text: 'AI系统日益参与自身改进过程', options: { bullet: true, indentLevel: 0 } },
    { text: '修正输出 (self-refine)', options: { bullet: true, indentLevel: 1 } },
    { text: '自我奖励 (self-reward)', options: { bullet: true, indentLevel: 1 } },
    { text: '自我进化 (self-evolve)', options: { bullet: true, indentLevel: 1 } },
    { text: '甚至参与AI研究本身', options: { bullet: true, indentLevel: 1 } },
    { text: '文献激增但术语混乱，缺乏统一框架', options: { bullet: true, indentLevel: 0 } },
    { text: '当前焦点问题', options: { bullet: true, indentLevel: 0, color: COLORS.blue } },
    { text: '哪些循环是真正的"自我改进"？', options: { bullet: true, indentLevel: 1 } },
    { text: '工程技巧 vs. 开放式递归自我改进 (RSI)', options: { bullet: true, indentLevel: 1 } },
    { text: '评估器设计如何决定循环强度？', options: { bullet: true, indentLevel: 1 } }
  ];

  slide.addText(bullets, {
    x: 0.5, y: 1.2, w: 9.0, h: 4.0,
    fontSize: 18, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第3页：核心贡献
function slide03_contributions() {
  const slide = pres.addSlide();

  slide.addText('本综述的三大核心贡献', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 贡献1
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 1.3, w: 9.0, h: 1.2,
    fill: { color: COLORS.lightGrey },
    line: { color: COLORS.blue, width: 2 }
  });
  slide.addText('① 双轴分类法', {
    x: 0.7, y: 1.4, w: 8.6, h: 0.4,
    fontSize: 22, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('评估器类型 × 改进范围，区分工程技巧与真正RSI', {
    x: 0.7, y: 1.85, w: 8.6, h: 0.4,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 贡献2
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 2.7, w: 9.0, h: 1.2,
    fill: { color: COLORS.lightGrey },
    line: { color: COLORS.blue, width: 2 }
  });
  slide.addText('② 验证层级理论', {
    x: 0.7, y: 2.8, w: 8.6, h: 0.4,
    fontSize: 22, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('形式化验证器 > 过程奖励模型 > 内在自评估', {
    x: 0.7, y: 3.25, w: 8.6, h: 0.4,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 贡献3
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 4.1, w: 9.0, h: 1.2,
    fill: { color: COLORS.lightGrey },
    line: { color: COLORS.blue, width: 2 }
  });
  slide.addText('③ 失效模式分析', {
    x: 0.7, y: 4.2, w: 8.6, h: 0.4,
    fontSize: 22, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('自确认循环、模型崩溃、多样性崩溃的根源', {
    x: 0.7, y: 4.65, w: 8.6, h: 0.4,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第4页：双轴分类法
function slide04_taxonomy() {
  const slide = pres.addSlide();

  slide.addText('双轴分类法：评估器类型 × 改进范围', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 表格数据
  const rows = [
    [
      { text: '评估器轴', options: { bold: true, fill: COLORS.navy, color: COLORS.white } },
      { text: '外部验证', options: { bold: true, fill: COLORS.navy, color: COLORS.white } },
      { text: '模型判断', options: { bold: true, fill: COLORS.navy, color: COLORS.white } },
      { text: '内在信号', options: { bold: true, fill: COLORS.navy, color: COLORS.white } }
    ],
    [
      { text: '参数更新', options: { bold: true, fill: COLORS.lightBlue } },
      { text: 'RLHF (人类)', options: {} },
      { text: 'RLAIF (LLM评分)', options: {} },
      { text: 'Self-Reward', options: {} }
    ],
    [
      { text: '推理时改进', options: { bold: true, fill: COLORS.lightBlue } },
      { text: 'Self-Refine+单测', options: {} },
      { text: 'Self-Refine+Judge', options: {} },
      { text: 'Self-Refine纯循环', options: {} }
    ],
    [
      { text: '元改进', options: { bold: true, fill: COLORS.lightBlue } },
      { text: 'AI Scientist', options: { fill: COLORS.gold } },
      { text: 'Eureka (人类筛选)', options: {} },
      { text: 'Self-Discover', options: {} }
    ]
  ];

  slide.addTable(rows, {
    x: 0.5, y: 1.3, w: 9.0, h: 3.5,
    fontSize: 14,
    fontFace: 'Microsoft YaHei',
    border: { pt: 1, color: COLORS.grey },
    align: 'center',
    valign: 'middle'
  });

  slide.addText('关键观察：外部验证器越弱，自我改进越难证明', {
    x: 0.5, y: 5.0, w: 9.0, h: 0.4,
    fontSize: 18, bold: true, color: COLORS.blue, fontFace: 'Microsoft YaHei'
  });
}

// 第5页：四大技术类别
function slide05_categories() {
  const slide = pres.addSlide();

  slide.addText('四大技术类别', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 类别1
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 1.3, w: 4.3, h: 1.8,
    fill: { color: COLORS.lightGrey }
  });
  slide.addText('1️⃣ 输出修正', {
    x: 0.7, y: 1.4, w: 3.9, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('Self-Refine, Self-Debug\n推理时循环修正输出\n外部验证器：单测/rubric', {
    x: 0.7, y: 1.85, w: 3.9, h: 1.0,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 类别2
  slide.addShape(pres.ShapeType.roundRect, {
    x: 5.2, y: 1.3, w: 4.3, h: 1.8,
    fill: { color: COLORS.lightGrey }
  });
  slide.addText('2️⃣ 合成数据训练', {
    x: 5.4, y: 1.4, w: 3.9, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('Self-Instruct, WizardLM\n用自生成数据微调\n风险：模型崩溃', {
    x: 5.4, y: 1.85, w: 3.9, h: 1.0,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 类别3
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 3.3, w: 4.3, h: 1.8,
    fill: { color: COLORS.lightGrey }
  });
  slide.addText('3️⃣ 自我奖励', {
    x: 0.7, y: 3.4, w: 3.9, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('Self-Rewarding LMs\n模型生成偏好对\n问题：自确认循环', {
    x: 0.7, y: 3.85, w: 3.9, h: 1.0,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 类别4
  slide.addShape(pres.ShapeType.roundRect, {
    x: 5.2, y: 3.3, w: 4.3, h: 1.8,
    fill: { color: COLORS.lightGrey }
  });
  slide.addText('4️⃣ 元改进', {
    x: 5.4, y: 3.4, w: 3.9, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('AI Scientist, Eureka\n改进算法/提示/架构\n最接近真正RSI', {
    x: 5.4, y: 3.85, w: 3.9, h: 1.0,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第6页：验证层级
function slide06_verification() {
  const slide = pres.addSlide();

  slide.addText('验证层级：评估器强度决定改进可信度', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 层级1 - 最强
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.5, y: 1.2, w: 7.0, h: 0.7,
    fill: { color: '22C55E' }
  });
  slide.addText('L1: 形式化验证器 (单测、证明检查器)', {
    x: 1.7, y: 1.35, w: 6.6, h: 0.4,
    fontSize: 18, bold: true, color: COLORS.white, fontFace: 'Microsoft YaHei'
  });

  // 箭头
  slide.addShape(pres.ShapeType.downArrow, {
    x: 4.5, y: 2.0, w: 1.0, h: 0.5,
    fill: { color: COLORS.grey }
  });

  // 层级2
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.5, y: 2.6, w: 7.0, h: 0.7,
    fill: { color: 'EAB308' }
  });
  slide.addText('L2: 过程奖励模型 (人类标注的中间步骤)', {
    x: 1.7, y: 2.75, w: 6.6, h: 0.4,
    fontSize: 18, bold: true, color: COLORS.white, fontFace: 'Microsoft YaHei'
  });

  // 箭头
  slide.addShape(pres.ShapeType.downArrow, {
    x: 4.5, y: 3.4, w: 1.0, h: 0.5,
    fill: { color: COLORS.grey }
  });

  // 层级3
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.5, y: 4.0, w: 7.0, h: 0.7,
    fill: { color: 'F59E0B' }
  });
  slide.addText('L3: LLM判断器 (另一个模型评分)', {
    x: 1.7, y: 4.15, w: 6.6, h: 0.4,
    fontSize: 18, bold: true, color: COLORS.white, fontFace: 'Microsoft YaHei'
  });

  // 箭头
  slide.addShape(pres.ShapeType.downArrow, {
    x: 4.5, y: 4.8, w: 1.0, h: 0.5,
    fill: { color: COLORS.grey }
  });

  // 层级4 - 最弱
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.5, y: 5.4, w: 7.0, h: 0.7,
    fill: { color: 'EF4444' }
  });
  slide.addText('L4: 内在自评估 (模型评价自己)', {
    x: 1.7, y: 5.55, w: 6.6, h: 0.4,
    fontSize: 18, bold: true, color: COLORS.white, fontFace: 'Microsoft YaHei'
  });
}

// 第7页：评估器瓶颈
function slide07_bottleneck() {
  const slide = pres.addSlide();

  slide.addText('评估器瓶颈：自我改进的根本限制', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  const bullets = [
    { text: '核心洞察：每个改进循环都是一个断言', options: { bullet: true, indentLevel: 0, bold: true } },
    { text: '"某种信号可以替代人类判断"', options: { bullet: true, indentLevel: 1 } },
    { text: '评估器质量上限决定改进上限', options: { bullet: true, indentLevel: 1 } },
    { text: '三大失效模式', options: { bullet: true, indentLevel: 0, color: COLORS.blue, bold: true } },
    { text: '自确认循环：模型偏好与人类判断脱钩', options: { bullet: true, indentLevel: 1 } },
    { text: '模型崩溃：合成数据稀释真实分布', options: { bullet: true, indentLevel: 1 } },
    { text: '多样性崩溃：奖励黑客攻击导致输出趋同', options: { bullet: true, indentLevel: 1 } },
    { text: '实证证据', options: { bullet: true, indentLevel: 0, color: COLORS.blue, bold: true } },
    { text: 'AlphaCode 2 (形式化验证) vs Self-Rewarding LMs (内在评估)', options: { bullet: true, indentLevel: 1 } },
    { text: '前者性能持续提升，后者3轮后饱和', options: { bullet: true, indentLevel: 1 } }
  ];

  slide.addText(bullets, {
    x: 0.5, y: 1.2, w: 9.0, h: 4.2,
    fontSize: 18, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第8页：案例研究 - AlphaCode 2
function slide08_alphacode() {
  const slide = pres.addSlide();

  slide.addText('案例研究：AlphaCode 2 的成功要素', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 成功要素
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 1.3, w: 4.3, h: 2.5,
    fill: { color: COLORS.lightGrey },
    line: { color: '22C55E', width: 3 }
  });
  slide.addText('✅ 成功要素', {
    x: 0.7, y: 1.4, w: 3.9, h: 0.4,
    fontSize: 22, bold: true, color: '22C55E', fontFace: 'Microsoft YaHei'
  });
  const successBullets = [
    { text: '单元测试作为验证器', options: { bullet: true } },
    { text: '形式化、客观、无偏', options: { bullet: true } },
    { text: '搜索+筛选架构', options: { bullet: true } },
    { text: '生成100万候选方案', options: { bullet: true } },
    { text: '单测筛选正确解', options: { bullet: true } }
  ];
  slide.addText(successBullets, {
    x: 0.7, y: 1.9, w: 3.9, h: 1.8,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 结果
  slide.addShape(pres.ShapeType.roundRect, {
    x: 5.2, y: 1.3, w: 4.3, h: 2.5,
    fill: { color: COLORS.lightBlue },
    line: { color: COLORS.blue, width: 3 }
  });
  slide.addText('📊 性能表现', {
    x: 5.4, y: 1.4, w: 3.9, h: 0.4,
    fontSize: 22, bold: true, color: COLORS.blue, fontFace: 'Microsoft YaHei'
  });
  slide.addText('Codeforces比赛\n排名：前15%\n超越85%人类程序员\n验证器强度 = 改进上限', {
    x: 5.4, y: 1.9, w: 3.9, h: 1.8,
    fontSize: 18, color: COLORS.text, fontFace: 'Microsoft YaHei', lineSpacing: 32
  });

  // 对比
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 4.0, w: 9.0, h: 0.8,
    fill: { color: COLORS.gold }
  });
  slide.addText('对比：Self-Rewarding LMs 无外部验证，3轮后性能饱和', {
    x: 0.7, y: 4.2, w: 8.6, h: 0.4,
    fontSize: 18, bold: true, color: COLORS.white, fontFace: 'Microsoft YaHei'
  });
}

// 第9页：失效模式详解
function slide09_failures() {
  const slide = pres.addSlide();

  slide.addText('三大失效模式：根源与表现', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 表格
  const rows = [
    [
      { text: '失效模式', options: { bold: true, fill: COLORS.navy, color: COLORS.white } },
      { text: '根源', options: { bold: true, fill: COLORS.navy, color: COLORS.white } },
      { text: '表现', options: { bold: true, fill: COLORS.navy, color: COLORS.white } },
      { text: '典型案例', options: { bold: true, fill: COLORS.navy, color: COLORS.white } }
    ],
    [
      { text: '自确认循环', options: { bold: true } },
      { text: '评估器=生成器', options: {} },
      { text: '偏好与真实质量脱钩', options: {} },
      { text: 'Self-Rewarding LMs', options: {} }
    ],
    [
      { text: '模型崩溃', options: { bold: true } },
      { text: '合成数据反馈训练', options: {} },
      { text: '分布退化、多样性丧失', options: {} },
      { text: 'Self-Instruct迭代', options: {} }
    ],
    [
      { text: '多样性崩溃', options: { bold: true } },
      { text: '奖励黑客攻击', options: {} },
      { text: '输出趋同、风格固化', options: {} },
      { text: 'RLHF过度优化', options: {} }
    ]
  ];

  slide.addTable(rows, {
    x: 0.5, y: 1.3, w: 9.0, h: 2.5,
    fontSize: 15,
    fontFace: 'Microsoft YaHei',
    border: { pt: 1, color: COLORS.grey },
    valign: 'middle'
  });

  // 解决方案
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 4.0, w: 9.0, h: 1.5,
    fill: { color: COLORS.lightBlue }
  });
  slide.addText('缓解策略', {
    x: 0.7, y: 4.1, w: 8.6, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  const solutions = [
    { text: '引入外部验证器 (单测、人类反馈、形式化证明)', options: { bullet: true } },
    { text: '混合真实数据 (至少10-20%防崩溃)', options: { bullet: true } },
    { text: '多样性正则化 (熵奖励、温度采样)', options: { bullet: true } }
  ];
  slide.addText(solutions, {
    x: 0.7, y: 4.6, w: 8.6, h: 0.8,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第10页：AI Scientist
function slide10_aiscientist() {
  const slide = pres.addSlide();

  slide.addText('AI Scientist：最接近真正RSI的尝试', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  const bullets = [
    { text: '系统设计', options: { bullet: true, indentLevel: 0, bold: true, color: COLORS.blue } },
    { text: '全自动科研循环：生成假设 → 设计实验 → 编写代码 → 分析结果 → 撰写论文', options: { bullet: true, indentLevel: 1 } },
    { text: '评估器：LLM模拟会议审稿人打分', options: { bullet: true, indentLevel: 1 } },
    { text: '实验结果', options: { bullet: true, indentLevel: 0, bold: true, color: COLORS.blue } },
    { text: '生成论文质量：部分可发表 (人类筛选后)', options: { bullet: true, indentLevel: 1 } },
    { text: '成本：约$15 per paper (Sonnet模型)', options: { bullet: true, indentLevel: 1 } },
    { text: '局限性', options: { bullet: true, indentLevel: 0, bold: true, color: COLORS.blue } },
    { text: '✗ 评估器瓶颈：LLM审稿人与真实同行评审有差距', options: { bullet: true, indentLevel: 1 } },
    { text: '✗ 新颖性有限：多数想法是已知方法组合', options: { bullet: true, indentLevel: 1 } },
    { text: '✗ 未达到"自举"：仍需人类筛选有价值的idea', options: { bullet: true, indentLevel: 1 } },
    { text: '启示', options: { bullet: true, indentLevel: 0, bold: true, color: COLORS.gold } },
    { text: '元改进是RSI最有希望的路径，但评估器仍是核心瓶颈', options: { bullet: true, indentLevel: 1 } }
  ];

  slide.addText(bullets, {
    x: 0.5, y: 1.2, w: 9.0, h: 4.2,
    fontSize: 17, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第11页：理论边界
function slide11_bounds() {
  const slide = pres.addSlide();

  slide.addText('RSI的三大边界：为何开放式递归尚未实现', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 边界1
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 1.3, w: 9.0, h: 1.2,
    fill: { color: COLORS.lightGrey },
    line: { color: 'EF4444', width: 2 }
  });
  slide.addText('🔴 基础模型依赖 (Grounding Requirement)', {
    x: 0.7, y: 1.4, w: 8.6, h: 0.4,
    fontSize: 20, bold: true, color: 'EF4444', fontFace: 'Microsoft YaHei'
  });
  slide.addText('所有循环都依赖预训练的基础模型，无法自举创建新能力', {
    x: 0.7, y: 1.85, w: 8.6, h: 0.4,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 边界2
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 2.7, w: 9.0, h: 1.2,
    fill: { color: COLORS.lightGrey },
    line: { color: 'F59E0B', width: 2 }
  });
  slide.addText('🟠 崩溃动力学 (Collapse Dynamics)', {
    x: 0.7, y: 2.8, w: 8.6, h: 0.4,
    fontSize: 20, bold: true, color: 'F59E0B', fontFace: 'Microsoft YaHei'
  });
  slide.addText('合成数据训练 → 分布退化 → 多样性丧失 → 性能下降', {
    x: 0.7, y: 3.25, w: 8.6, h: 0.4,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 边界3
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 4.1, w: 9.0, h: 1.2,
    fill: { color: COLORS.lightGrey },
    line: { color: '3B82F6', width: 2 }
  });
  slide.addText('🔵 算力约束 (Compute Constraints)', {
    x: 0.7, y: 4.2, w: 8.6, h: 0.4,
    fontSize: 20, bold: true, color: '3B82F6', fontFace: 'Microsoft YaHei'
  });
  slide.addText('搜索空间指数增长，实际可探索范围有限 (AlphaCode: 100万→10个)', {
    x: 0.7, y: 4.65, w: 8.6, h: 0.4,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第12页：安全风险
function slide12_safety() {
  const slide = pres.addSlide();

  slide.addText('安全与治理：RSI的五大风险', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  const bullets = [
    { text: '① 加速风险 (Acceleration Risk)', options: { bullet: true, indentLevel: 0, bold: true } },
    { text: 'RSI可能大幅压缩AI能力提升时间线，削弱人类适应窗口', options: { bullet: true, indentLevel: 1 } },
    { text: '② 对齐脆弱性 (Alignment Fragility)', options: { bullet: true, indentLevel: 0, bold: true } },
    { text: '自我改进可能绕过或削弱原有的安全guardrails', options: { bullet: true, indentLevel: 1 } },
    { text: '③ 目标错位 (Goal Misgeneralization)', options: { bullet: true, indentLevel: 0, bold: true } },
    { text: '优化器的诅咒：模型可能优化代理指标而非真实目标', options: { bullet: true, indentLevel: 1 } },
    { text: '④ 不可预测性 (Unpredictability)', options: { bullet: true, indentLevel: 0, bold: true } },
    { text: '涌现能力难以提前评估，可能突然获得危险能力', options: { bullet: true, indentLevel: 1 } },
    { text: '⑤ 军备竞赛 (Arms Race)', options: { bullet: true, indentLevel: 0, bold: true } },
    { text: 'RSI技术可能加剧AI竞争，激励放松安全标准', options: { bullet: true, indentLevel: 1 } }
  ];

  slide.addText(bullets, {
    x: 0.5, y: 1.2, w: 9.0, h: 4.2,
    fontSize: 18, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 警告标识
  slide.addShape(pres.ShapeType.triangle, {
    x: 4.5, y: 5.5, w: 1.0, h: 0.8,
    fill: { color: 'EF4444' },
    rotate: 180
  });
}

// 第13页：治理建议
function slide13_governance() {
  const slide = pres.addSlide();

  slide.addText('治理建议：负责任的RSI研发', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 技术措施
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 1.3, w: 4.3, h: 2.2,
    fill: { color: COLORS.lightBlue }
  });
  slide.addText('技术措施', {
    x: 0.7, y: 1.4, w: 3.9, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  const techMeasures = [
    { text: '评估器审计', options: { bullet: true } },
    { text: '能力监控', options: { bullet: true } },
    { text: '可逆性设计', options: { bullet: true } },
    { text: '沙盒测试', options: { bullet: true } }
  ];
  slide.addText(techMeasures, {
    x: 0.7, y: 1.9, w: 3.9, h: 1.5,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 政策措施
  slide.addShape(pres.ShapeType.roundRect, {
    x: 5.2, y: 1.3, w: 4.3, h: 2.2,
    fill: { color: COLORS.lightBlue }
  });
  slide.addText('政策措施', {
    x: 5.4, y: 1.4, w: 3.9, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  const policyMeasures = [
    { text: '透明度要求', options: { bullet: true } },
    { text: '风险分级', options: { bullet: true } },
    { text: '国际协调', options: { bullet: true } },
    { text: '红线机制', options: { bullet: true } }
  ];
  slide.addText(policyMeasures, {
    x: 5.4, y: 1.9, w: 3.9, h: 1.5,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });

  // 研究方向
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 3.7, w: 9.0, h: 1.8,
    fill: { color: COLORS.lightGrey }
  });
  slide.addText('优先研究方向', {
    x: 0.7, y: 3.8, w: 8.6, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  const research = [
    { text: '可验证的评估器 (Verifiable Evaluators)', options: { bullet: true } },
    { text: '对齐保持机制 (Alignment Preservation)', options: { bullet: true } },
    { text: '崩溃检测算法 (Collapse Detection)', options: { bullet: true } }
  ];
  slide.addText(research, {
    x: 0.7, y: 4.3, w: 8.6, h: 1.1,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第14页：未来展望
function slide14_future() {
  const slide = pres.addSlide();

  slide.addText('未来展望：从工程技巧到真正RSI', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 当前状态
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 1.3, w: 4.0, h: 1.5,
    fill: { color: COLORS.lightGrey }
  });
  slide.addText('现状 (2026)', {
    x: 0.7, y: 1.4, w: 3.6, h: 0.4,
    fontSize: 18, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('有界自我精炼\n依赖外部验证器\n工业界已采用', {
    x: 0.7, y: 1.9, w: 3.6, h: 0.8,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei', lineSpacing: 28
  });

  // 箭头
  slide.addShape(pres.ShapeType.rightArrow, {
    x: 4.7, y: 1.8, w: 0.8, h: 0.6,
    fill: { color: COLORS.blue }
  });

  // 未来状态
  slide.addShape(pres.ShapeType.roundRect, {
    x: 5.7, y: 1.3, w: 4.0, h: 1.5,
    fill: { color: COLORS.lightBlue }
  });
  slide.addText('未来 (?)', {
    x: 5.9, y: 1.4, w: 3.6, h: 0.4,
    fontSize: 18, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  slide.addText('开放式RSI\n自主研究循环\n自举能力增长', {
    x: 5.9, y: 1.9, w: 3.6, h: 0.8,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei', lineSpacing: 28
  });

  // 关键挑战
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5, y: 3.0, w: 9.0, h: 2.5,
    fill: { color: COLORS.lightGrey }
  });
  slide.addText('通往真正RSI的关键挑战', {
    x: 0.7, y: 3.1, w: 8.6, h: 0.4,
    fontSize: 20, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });
  const challenges = [
    { text: '① 突破评估器瓶颈：开发更强的验证方法', options: { bullet: true } },
    { text: '② 防止模型崩溃：理解并缓解分布退化', options: { bullet: true } },
    { text: '③ 保持对齐性：确保改进不削弱安全性', options: { bullet: true } },
    { text: '④ 可验证性：让RSI过程可审计、可控', options: { bullet: true } },
    { text: '⑤ 社会治理：建立国际规范防止军备竞赛', options: { bullet: true } }
  ];
  slide.addText(challenges, {
    x: 0.7, y: 3.6, w: 8.6, h: 1.8,
    fontSize: 16, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
}

// 第15页：核心结论
function slide15_conclusions() {
  const slide = pres.addSlide();

  slide.addText('核心结论', {
    x: 0.5, y: 0.4, w: 9.0, h: 0.6,
    ...titleStyle
  });

  // 结论1
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.0, y: 1.3, w: 8.0, h: 0.9,
    fill: { color: COLORS.lightBlue }
  });
  slide.addText('① 当前AI自我改进≠开放式RSI，而是有界的工程技巧', {
    x: 1.2, y: 1.5, w: 7.6, h: 0.5,
    fontSize: 18, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });

  // 结论2
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.0, y: 2.4, w: 8.0, h: 0.9,
    fill: { color: COLORS.lightBlue }
  });
  slide.addText('② 评估器强度是自我改进的根本瓶颈', {
    x: 1.2, y: 2.6, w: 7.6, h: 0.5,
    fontSize: 18, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });

  // 结论3
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.0, y: 3.5, w: 8.0, h: 0.9,
    fill: { color: COLORS.lightBlue }
  });
  slide.addText('③ 失效模式(崩溃、脱钩)源于违反验证层级', {
    x: 1.2, y: 3.7, w: 7.6, h: 0.5,
    fontSize: 18, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });

  // 结论4
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.0, y: 4.6, w: 8.0, h: 0.9,
    fill: { color: COLORS.lightBlue }
  });
  slide.addText('④ 真正RSI需要技术突破+社会治理协同', {
    x: 1.2, y: 4.8, w: 7.6, h: 0.5,
    fontSize: 18, bold: true, color: COLORS.navy, fontFace: 'Microsoft YaHei'
  });

  // 引用
  slide.addText('"递归自我改进不是单一技术，而是一个设计空间"', {
    x: 1.0, y: 5.7, w: 8.0, h: 0.4,
    fontSize: 20, italic: true, color: COLORS.blue, fontFace: 'Microsoft YaHei', align: 'center'
  });
}

// 第16页：致谢与参考
function slide16_thanks() {
  const slide = pres.addSlide();

  slide.addText('谢谢！', {
    x: 1.0, y: 2.0, w: 8.0, h: 1.0,
    fontSize: 48, bold: true, color: COLORS.navy,
    fontFace: 'Microsoft YaHei', align: 'center'
  });

  slide.addText('欢迎讨论与交流', {
    x: 1.0, y: 3.2, w: 8.0, h: 0.6,
    fontSize: 24, color: COLORS.blue,
    fontFace: 'Microsoft YaHei', align: 'center'
  });

  // 论文信息
  slide.addShape(pres.ShapeType.roundRect, {
    x: 2.0, y: 4.2, w: 6.0, h: 1.2,
    fill: { color: COLORS.lightGrey }
  });
  slide.addText('论文：Recursive Self-Improvement in AI', {
    x: 2.2, y: 4.3, w: 5.6, h: 0.4,
    fontSize: 16, bold: true, color: COLORS.text, fontFace: 'Microsoft YaHei'
  });
  slide.addText('arXiv:2607.07663v1 [cs.AI]\nMingguang Chen, Licheng Wang, Bo Qu', {
    x: 2.2, y: 4.75, w: 5.6, h: 0.5,
    fontSize: 14, color: COLORS.grey, fontFace: 'Microsoft YaHei'
  });
}

// 生成所有幻灯片
slide01_cover();
slide02_background();
slide03_contributions();
slide04_taxonomy();
slide05_categories();
slide06_verification();
slide07_bottleneck();
slide08_alphacode();
slide09_failures();
slide10_aiscientist();
slide11_bounds();
slide12_safety();
slide13_governance();
slide14_future();
slide15_conclusions();
slide16_thanks();

// 保存文件
const outputPath = process.argv[2] || 'AI_RSI_Presentation.pptx';
pres.writeFile({ fileName: outputPath })
  .then(() => {
    console.log(`✅ PPT已生成: ${outputPath}`);
    console.log('📊 共16页幻灯片');
    console.log('🎨 深蓝主题，参考电力AI汇报PPT风格');
  })
  .catch(err => {
    console.error('❌ 生成失败:', err);
    process.exit(1);
  });
