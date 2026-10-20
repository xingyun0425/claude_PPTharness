"""
AI Recursive Self-Improvement Survey Deck Builder
基于论文 2607.07663v1.pdf 和参考 合稿-20260707电力人工智能自主科研引擎方案汇报.pptx
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from deckkit import new_presentation, configure_theme, Canvas, IconStore, notes
from icons import ICONS
import deckkit as _dk

# Speaker notes: one short paragraph per slide, in deck order.
NOTES = [
    '封面。本页说明综述主题：把“自我改进”拆成可度量的类别，并把有界自我精修与开放式递归自我改进区分开。',
    '研究背景。1965 年 Good 提出智能爆炸，Schmidhuber 的 Gödel 机把它形式化；今天 FunSearch、AlphaEvolve 和 AI Scientist 已经让环路中的片段成为工程实践。',
    '核心问题。Anthropic 的五阶段光谱把自主性分成从人写代码到“闭环”设计后继模型；当前执行侧推进很快，方向设定仍由人承担。',
    '调研范围。1,250 篇 arXiv 论文分两阶段收集：871 篇种子检索加 379 篇定向补充，全部按两轴分类。',
    '核心洞察。self-refine、self-reward、self-evolve、self-research 描述的是性质完全不同的操作，术语混淆是文献难以比较的根源。',
    '分类法两轴。轴一回答“改进什么”（部署行为、训练策略、评估器、研究过程），轴二回答环路闭合程度。',
    '图 1。4×3 网格显示代表系统；密度集中在中间一行（human-on-loop），闭环一行普遍稀疏。',
    '观察一。绝大多数被调研工作仍由人类审核结果，自动信号只替代了部分判断。',
    '观察二。评估器列是承重列：它既定义有界与开放式的边界，也是各类失败模式的来源。',
    '表 1。四类技术文献加基础理论共 1,250 篇，自评类 2026 年占比最高（82%）。',
    '第 3 章。部署时自我演化包含六个子方向，从输出自评到技能库的持久积累。',
    '图 3。按持久性给部署时方法排序：输出修订会蒸发，测试时更新是会话级，harness 编辑跨会话，技能积累才真正留存。',
    '第 4 章。训练时自我迭代的五个范式共享同一循环：模型生成数据、数据更新策略。',
    '第 5 章。评估器设计空间包括 judge、过程奖励模型、验证器、评分细则与元评估。',
    '图 5。验证层级：形式验证器最可靠但覆盖窄，内在自评覆盖最广但最弱；已展示的自我改进强度与该层级一致。',
    '失败模式。自我确认回路、模型崩塌与多样性崩塌，都是对验证层级的违反。',
    '第 6 章。自动科研分两支：进化式程序发现与 AI 科学家智能体。',
    '第 7 章。理论条件与四条现实约束并列：grounding、崩塌动力学、算力与方向设定瓶颈。',
    '安全与治理。闭环的独特风险在于系统改写“更好”的定义，需要测量与控制机制同步跟进。',
    '五点发现。总结全文的可迁移结论。',
    '开放问题。治理级测量是目前最空白的领域。',
    '结论。综述把 1,250 篇论文组织成可操作分类，并标出评估器这一承重柱。',
    '数据与可复现性。语料、查询脚本与分类规则全部公开。',
]

# Allow theme role names ('blue', 'zone', 'line', ...) wherever deckkit expects hex.
_orig_rgb = _dk.rgb
def _rgb(h):
    if isinstance(h, str) and h in _dk.C:
        h = _dk.C[h]
    return _orig_rgb(h)
_dk.rgb = _rgb

# ===== THEME =====
THEME = {
    'colors': {
        'navy': '1F2937',      # 深灰（背景深色元素）
        'blue': '1E3A8A',      # 深蓝（主题色）
        'rose': 'C00000',      # 红色（强调/警告）
        'pale': 'F1F5F9',      # 浅灰蓝（浅底色）
        'zone': 'E0E7FF',      # 浅蓝紫（区域底色）
        'line': '3B82F6',      # 亮蓝（边框线）
        'text': '1F2937',      # 深灰（正文）
        'gold': 'F59E0B',      # 金色（次要强调）
        'sky': '60A5FA',       # 天蓝（辅助色）
        'white': 'FFFFFF',
        'grey': '6B7280',
        'neutral': '9CA3AF',
        'paleRose': 'FEE2E2',  # 浅红（警告背景）
        'darkRose': 'DC2626',  # 深红
    },
    'font': 'Microsoft YaHei',
    'icons': ICONS,
}

# 颜色role到hex的映射
C = THEME['colors']

TITLE_PT = 24
BODY_PT = 16
CAPTION_PT = 16

# ===== BUILDER =====
def build(output_path):
    from pathlib import Path
    import tempfile

    prs, layout = new_presentation()
    configure_theme(THEME['colors'], THEME['font'], THEME['icons'])

    # 创建临时目录供IconStore使用
    tmp_dir = Path(tempfile.mkdtemp())

    # 将tmp_dir传递给每个slide函数（通过闭包）
    global _tmp_dir
    _tmp_dir = tmp_dir

    slide_cover(prs)
    slide_background(prs)
    slide_problem(prs)
    slide_corpus(prs)
    slide_insight(prs)
    slide_taxonomy_axes(prs)
    slide_matrix(prs)
    slide_observation1(prs)
    slide_observation2(prs)
    slide_table1(prs)
    slide_chapter3(prs)
    slide_persistence(prs)
    slide_chapter4(prs)
    slide_chapter5(prs)
    slide_hierarchy(prs)
    slide_failures(prs)
    slide_chapter6(prs)
    slide_chapter7(prs)
    slide_safety(prs)
    slide_findings(prs)
    slide_open_problems(prs)
    slide_conclusion(prs)
    slide_acknowledgments(prs)

    for slide, text in zip(prs.slides, NOTES):
        notes(slide, text)

    prs.save(output_path)
    print(f'Saved: {output_path}')

    # 清理临时目录
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

# 全局临时目录变量
_tmp_dir = None
_store = None


def _icons(prs):
    """One shared IconStore per deck so each icon SVG is embedded once."""
    global _store
    if _store is None:
        _store = IconStore(prs, _tmp_dir)
    return _store

# ===== SLIDE 1: 封面 =====
def _slide_bg(slide, hex_color):
    """Set a true slide background (not a shape) so no blank first shape exists."""
    from pptx.oxml.ns import qn
    from lxml import etree
    csld = slide._element.find(qn('p:cSld'))
    for old in csld.findall(qn('p:bg')):
        csld.remove(old)
    bg = etree.Element(qn('p:bg'))
    bgPr = etree.SubElement(bg, qn('p:bgPr'))
    fill = etree.SubElement(bgPr, qn('a:solidFill'))
    etree.SubElement(fill, qn('a:srgbClr'), val=hex_color)
    etree.SubElement(bgPr, qn('a:effectLst'))
    csld.insert(0, bg)


def slide_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
    cv = Canvas(slide.shapes, _icons(prs))

    _slide_bg(slide, C['navy'])

    # 中央loop-arrow图标
    cv.icon_c('loop-arrow', 800, 280, 100, name='HeroIcon')

    # 主标题
    cv.text('Recursive Self-Improvement in AI:', 800, 400, pt=36,
            bold=True, color='white', align='c', name='TitleLine1')
    cv.text('From Bounded Self-Refinement to', 800, 448, pt=28,
            color='sky', align='c', name='TitleLine2')
    cv.text('Autonomous Research Loops', 800, 486, pt=28,
            color='sky', align='c', name='TitleLine3')

    # 作者信息
    cv.text('Mingguang Chen¹, Licheng Wang², Bo Qu³', 800, 580, pt=20,
            color='white', align='c', name='Authors')
    cv.text('¹UC Riverside   ²AlphaAvatar   ³Illinois Institute of Technology',
            800, 614, pt=16, color='neutral', align='c', name='Affils')

    # 日期
    cv.text('July 2026  |  arXiv:2607.07663v1', 800, 828, pt=16,
            color='neutral', align='c', name='DateLine')

# ===== SLIDE 2: 研究背景 =====
def slide_background(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('AI Systems Participate in Their Own Improvement')
    cv.page(2)

    # 三个横向卡片展示演进阶段
    cards = [
        {
            'y': 200, 'icon': 'research-flask',
            'head': 'Theoretical Foundations',
            'body': "Good's intelligence explosion (1965)\nSchmidhuber's Gödel machines (2000s)\nRSI as theoretical endpoint"
        },
        {
            'y': 370, 'icon': 'training-gear',
            'head': 'Engineering Practice',
            'body': 'LLMs critique & revise outputs\nTrain on self-generated data\nRewrite agent scaffolding'
        },
        {
            'y': 540, 'icon': 'agent-robot',
            'head': 'Frontier Exploration',
            'body': 'FunSearch: discover algorithms\nAlphaEvolve: AI development loop\nThe AI Scientist: conduct research'
        },
    ]

    for i, card in enumerate(cards):
        # 卡片
        cv.card(120, card['y'], 1360, 130, fill='zone', line='line', r=12, shadow=False)
        # 图标
        cv.icon_c(card['icon'], 200, card['y'] + 65, 50)
        # 标题
        cv.text(card['head'], 270, card['y'] + 35, pt=20, bold=True, color='blue')
        # 内容
        y_text = card['y'] + 62
        for line in card['body'].split('\n'):
            cv.text('• ' + line, 270, y_text, pt=BODY_PT, color='text')
            y_text += 24

    # 连接箭头
    for i in range(2):
        y_mid = cards[i]['y'] + 130
        cv.arrow(800, y_mid, 800, y_mid + 40, color='line', lw=3)

# ===== SLIDE 3: 核心问题 =====
def slide_problem(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('The Spectrum of AI Autonomy: Execution vs. Direction-Setting')
    cv.page(3)

    # 左侧：五阶段
    cv.text('Anthropic 5-Stage Spectrum:', 120, 160, pt=18, bold=True, color='blue')

    stages = [
        ('Stage 1', 'Humans write all code'),
        ('Stage 2', 'Chatbot-assisted coding'),
        ('Stage 3', 'Autonomous coding agents'),
        ('Stage 4', 'Agents delegate to agents'),
        ('Stage 5', 'Closing the loop: agents design successors'),
    ]

    y_stage = 200
    for i, (stage, desc) in enumerate(stages):
        # 阶段卡片
        is_stage5 = (i == 4)
        fill_col = 'paleRose' if is_stage5 else 'pale'
        line_col = 'rose' if is_stage5 else 'line'
        cv.card(120, y_stage, 600, 70, fill=fill_col, line=line_col, r=8, shadow=False)
        cv.text(stage, 150, y_stage + 20, pt=BODY_PT, bold=True,
                color='rose' if is_stage5 else 'blue')
        cv.text(desc, 150, y_stage + 45, pt=CAPTION_PT, color='text')

        # 连接箭头（除最后一个）
        if i < 4:
            cv.arrow(420, y_stage + 70, 420, y_stage + 100, color='line', lw=2.5)

        y_stage += 100

    # 右侧：瓶颈说明
    cv.card(800, 200, 680, 480, fill='zone', line='line', r=12, shadow=True)
    cv.text('Current Bottleneck', 840, 230, pt=20, bold=True, color='blue')

    cv.icon_c('hierarchy-pyramid', 1140, 320, 70)

    bottleneck_text = [
        ('Execution:', 'Claude writes >80% of Anthropic merged code (May 2026)'),
        ('', ''),
        ('Direction-Setting:', 'Choosing which problems matter'),
        ('', '→ Humans still in the loop'),
        ('', '→ Most consequential open question'),
    ]

    y_bn = 380
    for label, desc in bottleneck_text:
        if label:
            cv.text(label, 840, y_bn, pt=BODY_PT, bold=True, color='blue')
        if desc:
            x_desc = 840 if not label else 950
            cv.text(desc, x_desc, y_bn, pt=BODY_PT, color='text')
        y_bn += 30

# ===== SLIDE 4: 调研范围 =====
def slide_corpus(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('Survey Scope: 1,250 arXiv Papers (2024-2026)')
    cv.page(4)

    # 中央大数字
    cv.text('1,250', 800, 300, pt=72, bold=True, color='blue', align='c')
    cv.text('Papers Systematically Classified', 800, 380, pt=20, color='text', align='c')

    # 四个小卡片围绕
    cards_info = [
        (220, 480, 'Seed Harvest', '871 papers\n7 research threads', 'data-flow'),
        (620, 480, 'Supplemental', '379 papers\nTargeted extension', 'research-flask'),
        (1020, 480, 'Time Range', 'arXiv 2024-2026\n74% posted in 2026', 'agent-robot'),
        (420, 620, 'Method', 'Systematic queries\nRule-based classification', 'verifier-shield'),
    ]

    for x, y, head, body, icon in cards_info:
        cv.card(x, y, 340, 140, fill='zone', line='line', r=10, shadow=False)
        cv.icon_c(icon, x + 50, y + 70, 40)
        cv.text(head, x + 110, y + 30, pt=18, bold=True, color='blue')
        y_body = y + 60
        for line in body.split('\n'):
            cv.text(line, x + 110, y_body, pt=CAPTION_PT, color='text')
            y_body += 22

# ===== SLIDE 5: 核心洞察 =====
def slide_insight(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('"Self-Improvement" Is Not One Thing')
    cv.page(5)

    cv.text('The literature conflates fundamentally different ambitions under one term:',
            120, 170, pt=18, color='text')

    # 四个横向卡片展示术语混淆
    terms = [
        ('self-refine', 'Output revision at inference time', 'neural-net'),
        ('self-reward', 'Training with self-generated rewards', 'training-gear'),
        ('self-evolve', 'Harness/skill evolution during deployment', 'deployment-rocket'),
        ('self-research', 'AI systems conducting AI research', 'research-flask'),
    ]

    y_term = 240
    for term, desc, icon in terms:
        cv.card(120, y_term, 1360, 100, fill='zone', line='line', r=10, shadow=False)
        cv.icon_c(icon, 180, y_term + 50, 45)
        cv.text(f'"{term}"', 260, y_term + 30, pt=20, bold=True, color='rose')
        cv.text(desc, 260, y_term + 60, pt=BODY_PT, color='text')
        y_term += 120

    # 底部说明
    cv.text('→ Same mechanism label, categorically different operations',
            400, 780, pt=18, bold=True, color='blue')

# ===== SLIDE 6: 分类法两轴 =====
def slide_taxonomy_axes(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('The Two-Axis Taxonomy')
    cv.page(6)

    # 左卡片：Axis 1（四类）
    cv.card(120, 180, 680, 540, fill='pale', line='line', r=12, shadow=True)
    cv.text('Axis 1: What Does the System Improve?', 160, 210, pt=20,
            bold=True, color='blue')

    categories = [
        ('1. Deployment-time', 'Behavior in deployment', 'deployment-rocket'),
        ('2. Training-time', 'Policy through training', 'training-gear'),
        ('3. Self-evaluation', 'The evaluator itself', 'verifier-shield'),
        ('4. Auto Research', 'The research process', 'research-flask'),
    ]

    y_cat = 270
    for cat, desc, icon in categories:
        cv.icon_c(icon, 190, y_cat + 20, 35)
        cv.text(cat, 240, y_cat + 5, pt=18, bold=True, color='blue')
        cv.text(desc, 240, y_cat + 30, pt=CAPTION_PT, color='text')
        y_cat += 120

    # 右卡片：Axis 2（三级循环）
    cv.card(820, 180, 660, 540, fill='pale', line='line', r=12, shadow=True)
    cv.text('Axis 2: Loop Closure', 860, 210, pt=20, bold=True, color='blue')

    cv.icon_c('loop-arrow', 1150, 340, 80)

    loops = [
        ('Human-in-loop', 'Human approves each action', 'pale'),
        ('Human-on-loop', 'Automatic signal, human audits outcomes', 'zone'),
        ('Closed-loop', 'No human intervention', 'paleRose'),
    ]

    y_loop = 420
    for loop_name, desc, fill in loops:
        cv.card(880, y_loop, 540, 60, fill=fill, line='line', r=8, shadow=False)
        cv.text(loop_name, 910, y_loop + 15, pt=16, bold=True, color='blue')
        cv.text(desc, 910, y_loop + 38, pt=CAPTION_PT, color='text')
        y_loop += 80

# ===== SLIDE 7: 分类矩阵 Figure 1 =====
def slide_matrix(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('Figure 1: The 4×3 Taxonomy Grid')
    cv.page(7)

    # 表格坐标
    x0, y0 = 100, 180
    col_w = 440
    row_h = 130
    header_h = 60

    # 列标题
    headers = ['Human-in-loop', 'Human-on-loop', 'Closed-loop']
    for i, h in enumerate(headers):
        cv.box(x0 + 180 + i * col_w, y0, col_w, header_h,
               fill='blue', line='line', lw=1.5, r=8)
        cv.text(h, x0 + 180 + i * col_w + col_w // 2, y0 + header_h // 2,
                pt=18, bold=True, color='white', align='c')

    # 行标题
    rows = ['Deployment-time', 'Training-time', 'Self-evaluation', 'Auto Research']
    for i, r in enumerate(rows):
        cv.box(x0, y0 + header_h + i * row_h, 180, row_h,
               fill='navy', line='line', lw=1.5, r=8)
        # 多行文本处理
        words = r.split('-')
        if len(words) == 2:
            cv.text(words[0] + '-', x0 + 90, y0 + header_h + i * row_h + row_h // 2 - 12,
                    pt=16, bold=True, color='white', align='c')
            cv.text(words[1], x0 + 90, y0 + header_h + i * row_h + row_h // 2 + 12,
                    pt=16, bold=True, color='white', align='c')
        else:
            cv.text(r, x0 + 90, y0 + header_h + i * row_h + row_h // 2,
                    pt=16, bold=True, color='white', align='c')

    # 单元格内容（简化示例系统名）
    cells = [
        # Deployment-time行
        ['CoT self-critic', 'Self-refining agents', 'TTT'],
        # Training-time行
        ['Supervised CoT', 'Self-rewarding RL', 'SPIN zero-data'],
        # Self-evaluation行
        ['LLM judge', 'Process RM', 'Verifier-driven'],
        # Auto Research行
        ['Idea gen', 'FunSearch', 'AI Scientist (partial)'],
    ]

    for i in range(4):  # 4行
        for j in range(3):  # 3列
            cell_x = x0 + 180 + j * col_w
            cell_y = y0 + header_h + i * row_h
            cv.box(cell_x, cell_y, col_w, row_h,
                   fill='zone', line='line', lw=1, r=6)
            # 居中文本
            cv.text(cells[i][j], cell_x + col_w // 2, cell_y + row_h // 2,
                    pt=CAPTION_PT, color='text', align='c')

    # 底部注释
    cv.text('Density concentrated in middle row (human-on-loop)',
            160, 740, pt=16, bold=True, color='rose')

# ===== SLIDE 8: 观察1 =====
def slide_observation1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('Key Observation 1: Density Concentrated in Middle Row')
    cv.page(8)

    # 三行卡片，中间高亮
    rows = [
        ('Human-in-loop', 'Sparse', 'pale', 'grey', 280),
        ('Human-on-loop', 'Most papers here', 'zone', 'rose', 400),
        ('Closed-loop', 'Sparse everywhere', 'pale', 'grey', 520),
    ]

    for row_name, label, fill, label_color, y in rows:
        # 主卡片
        line_col = 'rose' if fill == 'zone' else 'line'
        lw = 3 if fill == 'zone' else 1.5
        cv.card(200, y, 1000, 100, fill=fill, line=line_col, r=10, shadow=(fill == 'zone'))

        cv.text(row_name, 240, y + 28, pt=20, bold=True, color='blue')
        cv.text(label, 240, y + 58, pt=BODY_PT, bold=True, color=label_color)

    # 右侧图标
    cv.icon_c('judge-gavel', 1300, 450, 70)
    cv.text('Human audits', 1220, 540, pt=CAPTION_PT, color='text', align='c')

# ===== SLIDE 9: 观察2 =====
def slide_observation2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('Key Observation 2: Evaluation Is the Load-Bearing Column')
    cv.page(9)

    # 左侧：简化网格高亮evaluator列
    cv.text('Self-evaluation column:', 140, 180, pt=18, bold=True, color='blue')

    # 简化4x3网格，红框高亮中间列
    x0, y0 = 140, 220
    col_w = 180
    row_h = 100

    for i in range(4):
        for j in range(3):
            fill = 'paleRose' if j == 2 else 'pale'
            line_col = 'rose' if j == 2 else 'line'
            lw = 3 if j == 2 else 1
            cv.box(x0 + j * col_w, y0 + i * row_h, col_w, row_h,
                   fill=fill, line=line_col, lw=lw, r=6)

    # evaluator列顶部图标
    cv.icon_c('verifier-shield', x0 + 2 * col_w + col_w // 2, y0 - 50, 50)

    # 右侧：说明
    cv.card(720, 220, 760, 480, fill='zone', line='line', r=12, shadow=True)
    cv.text('Why Self-Evaluation Matters', 760, 250, pt=20, bold=True, color='blue')

    reasons = [
        ('1. Signal Substitution', 'Every improvement loop claims some signal can substitute for human judgment'),
        ('', ''),
        ('2. Bounded vs. Open-ended', 'Defines the boundary between bounded self-refinement and open-ended RSI'),
        ('', ''),
        ('3. Failure Modes', 'Violations of the verification hierarchy cause self-confirming loops, collapse'),
    ]

    y_reason = 320
    for num, text in reasons:
        if num:
            cv.text(num, 780, y_reason, pt=BODY_PT, bold=True, color='rose')
        if text:
            cv.para(text, 780, y_reason + 25, w=680, pt=BODY_PT, color='text')
        y_reason += 90 if text else 0

# ===== SLIDE 10: Table 1统计 =====
def slide_table1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))

    cv.title('Table 1: Corpus by Category')
    cv.page(10)

    # 表格数据
    table_data = [
        ('Deployment-time self-evolution', '393', '74%'),
        ('Training-time self-iteration', '340', '69%'),
        ('Self-evaluation', '318', '82%'),
        ('Auto Research', '139', '76%'),
        ('Foundations, limits & safety', '60', '57%'),
    ]

    # 左侧表格
    x_table, y_table = 120, 200
    col_widths = [450, 120, 120]
    row_h = 70
    header_h = 60

    # 表头
    headers = ['Category', 'Papers', '% in 2026']
    for i, h in enumerate(headers):
        x_col = x_table + sum(col_widths[:i])
        cv.box(x_col, y_table, col_widths[i], header_h,
               fill='blue', line='line', lw=1.5, r=8)
        cv.text(h, x_col + col_widths[i] // 2, y_table + header_h // 2,
                pt=18, bold=True, color='white', align='c')

    # 数据行
    for row_idx, (cat, papers, pct) in enumerate(table_data):
        y_row = y_table + header_h + row_idx * row_h
        cv.box(x_table, y_row, col_widths[0], row_h,
               fill='zone', line='line', lw=1, r=6)
        cv.text(cat, x_table + 20, y_row + row_h // 2, pt=CAPTION_PT, color='text')

        cv.box(x_table + col_widths[0], y_row, col_widths[1], row_h,
               fill='pale', line='line', lw=1, r=6)
        cv.text(papers, x_table + col_widths[0] + col_widths[1] // 2, y_row + row_h // 2,
                pt=BODY_PT, bold=True, color='blue', align='c')

        cv.box(x_table + col_widths[0] + col_widths[1], y_row, col_widths[2], row_h,
               fill='pale', line='line', lw=1, r=6)
        cv.text(pct, x_table + sum(col_widths[:2]) + col_widths[2] // 2,
                y_row + row_h // 2, pt=CAPTION_PT, color='text', align='c')

    # 右侧横向条形图（简化）
    x_chart, y_chart = 840, 240
    max_val = 393
    for i, (cat, papers, _) in enumerate(table_data):
        bar_w = int(papers) / max_val * 550
        y_bar = y_chart + i * 90
        cv.box(x_chart, y_bar, bar_w, 50, fill='blue', line=None, r=4)
        cv.text(papers, x_chart + bar_w + 20, y_bar + 25, pt=BODY_PT,
                bold=True, color='blue')
        cv.text(cat.split()[0], x_chart, y_bar + 70, pt=CAPTION_PT, color='text')

# ===== SLIDE 11-23: 剩余幻灯片（简化实现）=====

def slide_chapter3(prs):
    """第3章概览"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('3. Deployment-Time Self-Evolution')
    cv.page(11)
    cv.icon_c('deployment-rocket', 1400, 200, 80)

    topics = [
        ('3.1 Self-critique & verification', 'judge-gavel'),
        ('3.2 Code self-repair', 'training-gear'),
        ('3.3 Multimodal critique', 'neural-net'),
        ('3.4 Test-time training', 'neural-net'),
        ('3.5 Harness self-evolution', 'loop-arrow'),
        ('3.6 Skill libraries', 'data-flow'),
    ]

    for i, (topic, icon) in enumerate(topics):
        row = i // 3
        col = i % 3
        x = 120 + col * 480
        y = 240 + row * 200
        cv.card(x, y, 440, 140, fill='zone', line='line', r=10, shadow=False)
        cv.icon_c(icon, x + 50, y + 70, 40)
        cv.text(topic, x + 110, y + 60, pt=BODY_PT, bold=True, color='blue')

def slide_persistence(prs):
    """持久性光谱"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('Figure 3: Persistence Spectrum')
    cv.page(12)

    # 横向渐变箭头（用box模拟）
    stages = ['Refined outputs', 'Test-time updates', 'Harness edits', 'Skill accumulation']
    for i, stage in enumerate(stages):
        x = 120 + i * 360
        cv.box(x, 300, 340, 100, fill='zone', line='line', r=10)
        cv.text(stage, x + 170, 350, pt=BODY_PT, bold=True, color='blue', align='c')
        if i < 3:
            cv.arrow(x + 340, 350, x + 360, 350, color='line', lw=3)

    cv.text('Evaporates → Session-level → Cross-session → Permanent',
            800, 480, pt=18, color='text', align='c')

def slide_chapter4(prs):
    """第4章：训练时迭代"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('4. Training-Time Self-Iteration')
    cv.page(13)

    # 左侧循环图
    cv.card(120, 200, 600, 500, fill='pale', line='line', r=12, shadow=True)
    cv.text('Training Loop', 160, 230, pt=18, bold=True, color='blue')

    nodes = [
        (420, 320, 'Model θ'),
        (420, 450, 'Generate data'),
        (420, 580, 'Update policy'),
    ]
    for x, y, label in nodes:
        cv.box(x - 80, y - 30, 160, 60, fill='zone', line='line', lw=2, r=8)
        cv.text(label, x, y, pt=CAPTION_PT, bold=True, color='blue', align='c')
        if label != 'Update policy':
            cv.arrow(x, y + 30, x, y + 90, color='line', lw=3)
    # 闭环箭头（从Update回到Model）
    cv.arrow(340, 600, 280, 320, color='line', lw=3, ctrl=(280, 460))

    cv.icon_c('loop-arrow', 420, 420, 60)

    # 右侧五个范式
    cv.card(800, 200, 680, 500, fill='pale', line='line', r=12, shadow=True)
    cv.text('Five Paradigms', 840, 230, pt=18, bold=True, color='blue')

    paradigms = [
        'Self-reward RL',
        'CoT self-training',
        'Self-distillation',
        'Self-play',
        'Embodied loops',
    ]

    y_p = 290
    for p in paradigms:
        cv.icon_c('training-gear', 870, y_p, 30)
        cv.text(f'• {p}', 910, y_p, pt=BODY_PT, color='text')
        y_p += 80

def slide_chapter5(prs):
    """第5章：评估器设计空间"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('5. Self-Evaluation Design Space')
    cv.page(14)

    cv.icon_c('verifier-shield', 1400, 200, 80)

    evaluators = [
        ('Judges', 'LLM-as-judge', 'judge-gavel'),
        ('Process RM', 'Reward models', 'neural-net'),
        ('Verifiers', 'Test-based/formal', 'verifier-shield'),
        ('Rubrics', 'Structured criteria', 'research-flask'),
        ('Meta-eval', 'Evaluate evaluators', 'hierarchy-pyramid'),
    ]

    for i, (name, desc, icon) in enumerate(evaluators):
        x = 120 + (i % 3) * 480
        y = 240 + (i // 3) * 180
        cv.card(x, y, 440, 140, fill='zone', line='line', r=10, shadow=False)
        cv.icon_c(icon, x + 50, y + 70, 40)
        cv.text(name, x + 110, y + 45, pt=18, bold=True, color='blue')
        cv.text(desc, x + 110, y + 75, pt=CAPTION_PT, color='text')

def slide_hierarchy(prs):
    """验证层级"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('Figure 5: The Verification Hierarchy')
    cv.page(15)

    # 左侧金字塔
    cv.card(120, 180, 680, 540, fill='pale', line='line', r=12, shadow=True)

    pyramid_layers = [
        (320, 250, 260, 60, 'Formal verifiers', '1E3A8A'),
        (280, 320, 340, 60, 'Test-based verifiers', '3B82F6'),
        (240, 390, 420, 60, 'Process verifiers', '60A5FA'),
        (200, 460, 500, 60, 'Outcome judges', '93C5FD'),
        (160, 530, 580, 60, 'Intrinsic self-assessment', 'DBEAFE'),
    ]

    for x, y, w, h, label, fill in pyramid_layers:
        cv.box(x, y, w, h, fill=fill, line='line', lw=1.5, r=6)
        cv.text(label, x + w // 2, y + h // 2, pt=CAPTION_PT, bold=True,
                color='white' if fill == '1E3A8A' else 'navy', align='c')

    cv.text('↑ Reliability', 220, 220, pt=CAPTION_PT, bold=True, color='rose')
    cv.text('↓ Coverage', 720, 580, pt=CAPTION_PT, bold=True, color='rose')

    # 右侧说明
    cv.card(840, 180, 640, 540, fill='zone', line='line', r=12, shadow=True)
    cv.text('Two Axes', 880, 210, pt=18, bold=True, color='blue')

    cv.text('Signal Reliability: Formal verifiers (strongest) → Intrinsic assessment (weakest)',
            900, 280, pt=BODY_PT, color='text')
    cv.text('Task Coverage: Formal verifiers (narrow) → Judges (broad)',
            900, 380, pt=BODY_PT, color='text')

    cv.text('Key Insight:', 900, 500, pt=BODY_PT, bold=True, color='rose')
    cv.text('Demonstrated self-improvement strength tracks this hierarchy',
            900, 530, pt=BODY_PT, color='text')

def slide_failures(prs):
    """失败模式"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('Failure Modes of Self-Evaluation')
    cv.page(16)

    failures = [
        ('Self-confirming loops', 'Weak evaluators approve their own outputs, creating false improvement signals'),
        ('Model collapse', 'Training on self-generated data leads to quality degradation'),
        ('Diversity collapse', 'Iterated self-selection narrows the output distribution'),
    ]

    y_fail = 220
    for i, (name, desc) in enumerate(failures):
        cv.card(120, y_fail, 1360, 140, fill='paleRose', line='darkRose', r=10, shadow=False)
        cv.icon_c('warning-sign', 200, y_fail + 70, 50)
        cv.text(f'{i + 1}. {name}', 280, y_fail + 35, pt=20, bold=True, color='darkRose')
        cv.para(desc, 280, y_fail + 65, w=1100, pt=BODY_PT, color='text')
        y_fail += 180

def slide_chapter6(prs):
    """第6章：AI科研"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('6. Auto Research: AI Systems Conducting AI Research')
    cv.page(17)

    # 左：进化程序发现
    cv.card(120, 200, 680, 500, fill='pale', line='line', r=12, shadow=True)
    cv.text('Evolutionary Program Discovery', 160, 230, pt=18, bold=True, color='blue')
    cv.text('FunSearch (2023), AlphaEvolve', 160, 260, pt=CAPTION_PT, color='text')

    steps_evo = ['Initial population', 'Evaluate (verifier)', 'Mutate', 'Select', 'New population']
    y_evo = 320
    for i, step in enumerate(steps_evo):
        cv.box(200, y_evo, 400, 60, fill='zone', line='line', lw=1.5, r=8)
        cv.text(step, 400, y_evo + 30, pt=CAPTION_PT, bold=True, color='blue', align='c')
        if i < 4:
            cv.arrow(400, y_evo + 60, 400, y_evo + 90, color='line', lw=2.5)
        y_evo += 90

    cv.icon_c('loop-arrow', 620, 450, 50)

    # 右：AI科学家
    cv.card(820, 200, 660, 500, fill='pale', line='line', r=12, shadow=True)
    cv.text('AI Scientist Agents', 860, 230, pt=18, bold=True, color='blue')
    cv.text('The AI Scientist (2024)', 860, 260, pt=CAPTION_PT, color='text')

    steps_sci = ['Idea generation', 'Experiment design', 'Code + Run', 'Write paper']
    y_sci = 340
    for step in steps_sci:
        cv.icon_c('research-flask', 890, y_sci, 35)
        cv.text(f'→ {step}', 950, y_sci, pt=BODY_PT, bold=True, color='blue')
        y_sci += 90

    cv.icon_c('agent-robot', 1350, 550, 60)

def slide_chapter7(prs):
    """第7章：理论与限制"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('7. Theoretical Foundations and Limits of RSI')
    cv.page(18)

    # 上方：理论
    cv.card(120, 180, 1360, 200, fill='zone', line='line', r=10, shadow=False)
    cv.text('Theoretical Conditions (Good 1965)', 300, 220, pt=20, bold=True, color='blue')
    cv.text('"Intelligence Explosion" hypothesis', 300, 260, pt=18, color='text')
    cv.arrow(800, 300, 800, 340, color='line', lw=4)

    # 分界线
    cv.line(120, 400, 1480, 400, color='rose', lw=3)

    # 下方：约束
    cv.text('Current Reality: Four Constraints', 300, 440, pt=20, bold=True, color='rose')

    constraints = [
        ('Grounding requirements', 'verifier-shield'),
        ('Collapse dynamics', 'warning-sign'),
        ('Compute constraints', 'training-gear'),
        ('Direction-setting bottleneck', 'hierarchy-pyramid'),
    ]

    for i, (const, icon) in enumerate(constraints):
        x = 120 + i * 360
        cv.card(x, 500, 340, 140, fill='paleRose', line='darkRose', r=10, shadow=False)
        cv.icon_c(icon, x + 50, x + 70, 40)
        cv.text(const, x + 110, 570, pt=CAPTION_PT, bold=True, color='darkRose')

def slide_safety(prs):
    """安全与治理"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('Safety and Governance: Risks of Closing the Loop')
    cv.page(19)

    # 左：封闭循环警示
    cv.card(120, 200, 680, 500, fill='paleRose', line='darkRose', r=12, shadow=True)
    cv.text('Closed Self-Improvement Loop', 160, 230, pt=18, bold=True, color='darkRose')

    loop_nodes = [
        (420, 320, 'AI research'),
        (420, 440, 'Train model'),
        (420, 560, 'Deploy agent'),
    ]
    for x, y, label in loop_nodes:
        cv.box(x - 80, y - 30, 160, 60, fill='white', line='darkRose', lw=2, r=8)
        cv.text(label, x, y, pt=CAPTION_PT, bold=True, color='darkRose', align='c')
        if label != 'Deploy agent':
            cv.arrow(x, y + 30, x, y + 90, color='darkRose', lw=3)
    cv.arrow(340, 580, 280, 330, color='darkRose', lw=3, ctrl=(280, 455))

    cv.icon_c('warning-sign', 420, 410, 60)

    # 右：治理清单
    cv.card(820, 200, 660, 500, fill='zone', line='line', r=12, shadow=True)
    cv.text('Governance Challenges', 860, 230, pt=18, bold=True, color='blue')

    gov_items = [
        'Measurement gaps',
        'Control mechanisms',
        'Takeoff scenarios',
        'Policy implications',
    ]

    y_gov = 300
    for item in gov_items:
        cv.icon_c('verifier-shield', 890, y_gov, 35)
        cv.text(f'• {item}', 950, y_gov, pt=BODY_PT, color='text')
        y_gov += 90

def slide_findings(prs):
    """关键发现总结"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('Five Key Findings')
    cv.page(20)

    findings = [
        ('1', 'Bounded ≠ Open-ended RSI', 'loop-arrow'),
        ('2', 'Evaluation quality determines ceiling', 'verifier-shield'),
        ('3', 'Human-on-loop dominates current practice', 'judge-gavel'),
        ('4', 'Direction-setting is the bottleneck', 'hierarchy-pyramid'),
        ('5', 'Measurement is underpopulated', 'research-flask'),
    ]

    for i, (num, text, icon) in enumerate(findings):
        row = i // 3
        col = i % 3
        x = 120 + col * 480
        y = 220 + row * 260
        cv.card(x, y, 440, 200, fill='zone', line='line', r=10, shadow=True)
        cv.text(num, x + 50, y + 60, pt=48, bold=True, color='blue')
        cv.icon_c(icon, x + 330, y + 60, 50)
        cv.para(text, x + 120, y + 60, w=180, pt=BODY_PT, bold=True, color='text')

def slide_open_problems(prs):
    """开放问题"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('Open Research Directions')
    cv.page(21)

    problems = [
        ('Governance-grade measurement', 'verifier-shield'),
        ('Robustness of self-evaluation', 'neural-net'),
        ('Long-horizon accumulation', 'loop-arrow'),
        ('Collapse detection', 'warning-sign'),
        ('Direction-setting automation', 'agent-robot'),
        ('Safety alignment', 'verifier-shield'),
    ]

    for i, (prob, icon) in enumerate(problems):
        row = i // 3
        col = i % 3
        x = 120 + col * 480
        y = 220 + row * 260
        cv.card(x, y, 440, 200, fill='pale', line='line', r=10, shadow=False)
        cv.icon_c(icon, x + 220, y + 60, 50)
        cv.text(prob, x + 220, y + 130, pt=BODY_PT, bold=True, color='blue', align='c')

def slide_conclusion(prs):
    """结论"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('Conclusion: From Fragments to System')
    cv.page(22)

    # 中央大图标
    cv.icon_c('loop-arrow', 800, 280, 120)

    # 三个要点
    points = [
        'Organized 1,250 papers into actionable taxonomy',
        'Identified evaluation as the load-bearing pillar',
        'Mapped path from bounded refinement to open-ended RSI',
    ]

    y_pt = 430
    for i, pt in enumerate(points):
        cv.text(f'{i + 1}.', 300, y_pt, pt=24, bold=True, color='blue')
        cv.text(pt, 350, y_pt, pt=20, color='text')
        y_pt += 80

    # 底部作者信息
    cv.text('Mingguang Chen (UCR), Licheng Wang (AlphaAvatar), Bo Qu (IIT)',
            800, 720, pt=CAPTION_PT, color='grey', align='c')
    cv.text('arXiv:2607.07663v1 | July 2026', 800, 750, pt=CAPTION_PT, color='neutral', align='c')

def slide_acknowledgments(prs):
    """致谢"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    cv = Canvas(slide.shapes, _icons(prs))
    cv.title('Data Availability & Reproducibility')
    cv.page(23)

    cv.icon_c('data-flow', 1350, 700, 60)

    cv.text('All materials released for reproducibility:',
            800, 300, pt=20, bold=True, color='blue', align='c')

    items = [
        'Corpus: 1,250 papers with classifications',
        'Query scripts and seed/supplemental harvest logic',
        'Rule-based classification code',
        'Per-paper category assignments (auditable)',
    ]

    y_item = 380
    for item in items:
        cv.text(f'• {item}', 400, y_item, pt=18, color='text')
        y_item += 60

    cv.text('[GitHub/arXiv supplementary materials]',
            800, 600, pt=BODY_PT, color='line', align='c')

    cv.text('Acknowledgments: [Funding agencies, collaborators, ...]',
            800, 700, pt=CAPTION_PT, color='grey', align='c')

# ===== MAIN =====
if __name__ == '__main__':
    import sys
    output = sys.argv[1] if len(sys.argv) > 1 else 'deck.pptx'
    build(output)

